# Implementation Plan: Vận hành quy trình (Process Execution Runtime)

> **Hướng dẫn thực thi:** Mỗi task là một unit làm việc độc lập có thể test được. Thực hiện theo thứ tự (Task 1→2→...→17) vì các task sau phụ thuộc service từ task trước. Chạy tests sau mỗi task trước khi commit.

---

## Phase 1: Schema & Core Services

- [ ] 1. **Cập nhật DocType schema — DC Process Step Instance**

  Thêm 3 field mới vào `dc_process_step_instance.json`:

  ```json
  {
    "fieldname": "parallel_group",
    "fieldtype": "Data",
    "label": "Nhóm song song"
  },
  {
    "fieldname": "assignees_json",
    "fieldtype": "Code",
    "label": "Danh sách người xử lý (JSON)",
    "options": "JSON"
  },
  {
    "fieldname": "is_overdue",
    "fieldtype": "Check",
    "label": "Quá hạn",
    "default": "0"
  }
  ```

  Thêm vào `field_order` sau `action_note`. Chạy `bench migrate`.

  _Requirements: Requirement 6 (Parallel Steps), Requirement 9 (Deadline)_

- [ ] 2. **Cập nhật DocType schema — DC Process Instance**

  Thêm field `is_overdue` (Check, default 0, label "Có bước quá hạn") vào `dc_process_instance.json`. Thêm `in_standard_filter: 1` để lọc được từ list view. Chạy `bench migrate`.

  _Requirements: Requirement 9, Requirement 11_

- [ ] 3. **Service: `condition_evaluator.py`**

  Tạo file `dcnet_process/dcnet_process/services/condition_evaluator.py`.

  Implement hàm `evaluate(condition: dict, form_data: dict) -> bool`:
  - `condition = {}` → trả về `True`
  - Simple condition: lấy `form_data.get(field)`, so sánh với `value` theo `operator`
  - Compound: `logic = "AND"` → `all(...)`, `"OR"` → `any(...)`
  - Operators: `Bằng`, `Khác`, `Lớn hơn`, `Nhỏ hơn`, `Chứa`, `Không chứa`, `Trống`, `Không trống`
  - Raise `ValueError` nếu operator không trong SUPPORTED_OPERATORS

  Viết `tests/test_condition_evaluator.py` với cases:
  - Bằng → True/False
  - AND compound đúng/sai
  - OR compound đúng/sai
  - Trống/Không trống
  - condition = {} → True
  - type mismatch (int vs string) không crash

  ```bash
	bench --site flow.local run-tests --app dcnet_process \
	  --module dcnet_process.dcnet_process.tests.test_condition_evaluator -v
  ```

  _Requirements: Requirement 5 (Conditional Branching)_

- [ ] 4. **Service: `assignee_resolver.py`**

  Tạo file `dcnet_process/dcnet_process/services/assignee_resolver.py`.

  Implement `resolve_assignees(step_dict: dict, instance) -> list[str]`:

  | assignee_type | Logic |
  |---------------|-------|
  | `"Người dùng tự chọn"` | `[instance.requester]` |
  | `"Người tạo quy trình"` | `[instance.requester]` |
  | `"Chọn người cụ thể"` | `[step_dict["assignee_user"]]` nếu tồn tại |
  | `"Theo role"` | `frappe.db.get_list("Has Role", filters={"role": step_dict["assignee_role"]}, fields=["parent"])` → lấy `parent` (là User) |
  | `"Theo phòng ban"` | `frappe.db.get_list("Employee", filters={"department": step_dict["assignee_department"]}, fields=["user_id"])` → lấy `user_id` |
  | `"Trưởng phòng"` | `Employee` của requester → `department` → `Department.department_head` → resolve User |
  | `"Người quản lý trực tiếp"` | `Employee` của requester → `reports_to` (Link Employee) → `user_id` |
  | `"Theo vị trí công việc"` | `Employee` có `designation = step_dict["assignee_position"]` → `user_id` |
  | `"Người thực hiện bước trước"` | Lấy `assignee` của step instance có `completed_at` gần nhất trước bước này |

  Lọc bỏ user không active (`frappe.db.get_value("User", user, "enabled")`). Trả về `[]` nếu không resolve được.

  Viết `tests/test_assignee_resolver.py` với mock `frappe.db`:
  - "Chọn người cụ thể" → đúng user
  - "Theo role" → list user
  - "Người dùng tự chọn" → requester
  - user disabled → bị lọc bỏ
  - không tìm thấy → trả về []

  _Requirements: Requirement 2 (Assignee Resolution)_

---

## Phase 2: Process Engine

- [ ] 5. **Service: `process_engine.py` — khởi chạy instance**

  Tạo file `dcnet_process/dcnet_process/services/process_engine.py`.

  Implement `start_instance(template_name, form_data, user)`:

  ```python
  # 1. Load template, validate status == "Active"
  template = frappe.get_doc("DC Process Template", template_name)
  if template.status != "Active":
      frappe.throw("Quy trình chưa được kích hoạt.", frappe.ValidationError)

  # 2. Check permission (permissions table của template)
  _check_launch_permission(template, user)

  # 3. Tạo DC Process Instance
  instance = frappe.new_doc("DC Process Instance")
  instance.process_template = template_name
  instance.process_version  = template.version
  instance.requester        = user
  instance.status           = "Đang xử lý"
  instance.submitted_at     = frappe.utils.now_datetime()
  instance.form_data_json   = frappe.as_json(form_data)
  instance.insert(ignore_permissions=True)

  # 4. Ghi history
  _append_history(instance, step="", action="Khởi chạy", actor=user, comment="")

  # 5. Activate bước đầu (step_order=1)
  first_step = min(template.steps, key=lambda s: s.step_order)
  activate_step(instance, first_step.step_key)

  return instance.name
  ```

  Implement `_check_launch_permission(template, user)`:
  - Nếu `permission_type = "Tất cả nhân viên"` → pass (ai cũng được)
  - Nếu có `permissions` table → kiểm tra user/role/dept tương ứng
  - Nếu không pass → `frappe.throw("Bạn không có quyền khởi chạy quy trình này.", frappe.PermissionError)`

  Test: start với template Active → instance được tạo với status đúng. Start với template Draft → ValidationError.

  _Requirements: Requirement 1 (Khởi chạy)_

- [ ] 6. **Service: `process_engine.py` — activate step**

  Implement `activate_step(instance, step_key)` trong `process_engine.py`:

  ```python
  # 1. Lấy step config từ template
  template = frappe.get_doc("DC Process Template", instance.process_template)
  step_dict = next((s.as_dict() for s in template.steps if s.step_key == step_key), None)
  if not step_dict:
      _handle_config_error(instance, f"Không tìm thấy bước '{step_key}' trong template.")
      return

  # 2. Resolve assignees
  from dcnet_process.dcnet_process.services.assignee_resolver import resolve_assignees
  assignees = resolve_assignees(step_dict, instance)
  if not assignees:
      _handle_no_assignee(instance, step_key)
      return

  # 3. Tính deadline
  deadline = None
  if step_dict["deadline_type"] == "Theo giờ":
      deadline = frappe.utils.add_to_date(None, hours=step_dict["deadline_value"])
  elif step_dict["deadline_type"] == "Theo ngày":
      deadline = frappe.utils.add_to_date(None, days=step_dict["deadline_value"])

  # 4. Tạo step instance row
  step_status = "Đang chờ duyệt" if step_dict["is_approval_step"] else "Đang chờ xử lý"
  instance.append("step_instances", {
      "step_template":  step_key,
      "step_name":      step_dict["step_name"],
      "assignee":       assignees[0],
      "assignees_json": frappe.as_json(assignees),
      "status":         step_status,
      "started_at":     frappe.utils.now_datetime(),
      "deadline":       deadline,
  })

  # 5. Cập nhật instance
  instance.current_step = step_key
  instance.save(ignore_permissions=True)

  # 6. Gửi thông báo
  from dcnet_process.dcnet_process.services.notifier import notify_step_assigned
  notify_step_assigned(instance, step_dict["step_name"], assignees)
  ```

  _Requirements: Requirement 1.5, Requirement 2_

- [ ] 7. **Service: `process_engine.py` — take_action (validation + history)**

  Implement `take_action(instance_name, step_row_name, action, comment, form_data, user)`:

  ```python
  instance = frappe.get_doc("DC Process Instance", instance_name)

  # 1. Validate instance chưa kết thúc
  TERMINAL = {"Đã hoàn tất", "Từ chối", "Đã hủy"}
  if instance.status in TERMINAL:
      frappe.throw("Lượt chạy đã kết thúc, không thể thực hiện hành động.", frappe.ValidationError)

  # 2. Tìm step instance
  step_row = next((s for s in instance.step_instances if s.name == step_row_name), None)
  if not step_row:
      frappe.throw("Bước không tồn tại trong lượt chạy này.", frappe.ValidationError)

  # 3. Validate assignee
  assignees = frappe.parse_json(step_row.assignees_json or "[]")
  if user not in assignees:
      frappe.throw("Bạn không được phân công xử lý bước này.", frappe.PermissionError)

  # 4. Validate comment bắt buộc (khi từ chối)
  # (Kiểm tra flow rule có yêu cầu comment không — nếu chưa config thì luôn yêu cầu khi Từ chối)
  if action == "Từ chối" and not comment:
      frappe.throw("Vui lòng nhập lý do từ chối.", frappe.ValidationError)

  # 5. Merge form_data
  existing = frappe.parse_json(instance.form_data_json or "{}")
  step_key = step_row.step_template
  existing.setdefault(step_key, {}).update(form_data)
  instance.form_data_json = frappe.as_json(existing)

  # 6. Cập nhật step instance
  step_row.action_taken   = action
  step_row.action_note    = comment
  step_row.completed_at   = frappe.utils.now_datetime()
  step_row.status         = _map_action_to_step_status(action)

  # 7. Ghi history
  _append_history(instance, step=step_key, action=action, actor=user, comment=comment)
  ```

  `_map_action_to_step_status(action) -> str`:
  - "Đồng ý" → "Đã đồng ý"
  - "Từ chối" → "Đã từ chối"
  - "Chuyển tiếp" → "Đã chuyển tiếp"
  - "Trả về" → "Đã trả về"
  - "Hoàn tất" → "Đã hoàn tất"

  _Requirements: Requirement 3, Requirement 4, Requirement 8_

- [ ] 8. **Service: `process_engine.py` — `_advance_instance` (flow rule evaluation)**

  Implement `_advance_instance(instance, from_step_key, action, form_data)`:

  ```python
  template = frappe.get_doc("DC Process Template", instance.process_template)
  form_data_full = frappe.parse_json(instance.form_data_json or "{}")

  # Lọc flow rules khớp from_step + action, sort theo order_index
  from dcnet_process.dcnet_process.services.condition_evaluator import evaluate
  candidates = sorted(
      [r for r in template.flow_rules
       if r.from_step == from_step_key and r.action == action],
      key=lambda r: r.order_index or 0
  )

  target = None
  for rule in candidates:
      condition = frappe.parse_json(rule.condition_json or "{}")
      if evaluate(condition, form_data_full):
          target = rule.target_step
          break
      elif rule.fallback_target_step:
          target = rule.fallback_target_step
          break

  if not target:
      _handle_config_error(instance, f"Không tìm thấy flow rule từ '{from_step_key}' với hành động '{action}'.")
      return

  # Xử lý markers
  if target == "END_COMPLETED":
      _complete_instance(instance)
  elif target == "END_REJECTED":
      _reject_instance(instance)
  else:
      # Lấy step config
      next_step = next((s for s in template.steps if s.step_key == target), None)
      if next_step and next_step.is_parallel:
          activate_parallel_group(instance, target, template)
      else:
          activate_step(instance, target)
  ```

  Implement `_complete_instance(instance)`:
  - `instance.status = "Đã hoàn tất"`, `instance.completed_at = now()`
  - Ghi history, notify requester (event="completed")

  Implement `_reject_instance(instance)`:
  - `instance.status = "Từ chối"`, `instance.completed_at = now()`
  - Ghi history, notify requester (event="rejected")

  _Requirements: Requirement 5 (Conditional Branching)_

- [ ] 9. **Service: `process_engine.py` — parallel steps**

  Implement `activate_parallel_group(instance, group_leader_key, template)`:

  ```python
  # Tìm tất cả steps có step_order == group_leader_step_order và is_parallel=True
  leader = next(s for s in template.steps if s.step_key == group_leader_key)
  parallel_steps = [
      s for s in template.steps
      if s.is_parallel and s.step_order == leader.step_order
  ]

  parallel_group_id = f"pg_{leader.step_order}"

  for ps in parallel_steps:
      assignees = resolve_assignees(ps.as_dict(), instance)
      if not assignees:
          _handle_no_assignee(instance, ps.step_key)
          return
      instance.append("step_instances", {
          "step_template":  ps.step_key,
          "step_name":      ps.step_name,
          "parallel_group": parallel_group_id,
          "assignee":       assignees[0],
          "assignees_json": frappe.as_json(assignees),
          "status":         "Đang chờ duyệt" if ps.is_approval_step else "Đang chờ xử lý",
          "started_at":     frappe.utils.now_datetime(),
      })

  instance.status = "Chờ duyệt"
  instance.save(ignore_permissions=True)
  ```

  Implement `_check_parallel_convergence(instance, parallel_group_id, action)`:
  - Được gọi sau mỗi take_action nếu step có `parallel_group`
  - Nếu `action == "Từ chối"` → áp dụng reject rule cho nhóm, hủy steps còn lại
  - Nếu tất cả steps cùng group đều completed → gọi `_advance_instance()` từ group leader

  _Requirements: Requirement 6 (Parallel Steps)_

- [ ] 10. **Service: `process_engine.py` — recall, reassign, cancel**

  Implement `recall_instance(instance_name, comment, user)`:
  ```python
  instance = frappe.get_doc("DC Process Instance", instance_name)
  ACTIVE = {"Đang xử lý", "Chờ duyệt", "Cần bổ sung"}
  if instance.status not in ACTIVE:
      frappe.throw("Chỉ thu hồi được khi quy trình đang xử lý.", frappe.ValidationError)
  if instance.requester != user:
      frappe.throw("Chỉ người gửi mới có thể thu hồi.", frappe.PermissionError)
  # Lấy danh sách assignees hiện tại để notify
  active_assignees = _get_active_assignees(instance)
  instance.status = "Đã hủy"
  _append_history(instance, step=instance.current_step, action="Thu hồi", actor=user, comment=comment)
  instance.save(ignore_permissions=True)
  notify_status_change(instance, "recalled", active_assignees, comment)
  ```

  Implement `reassign_step(instance_name, step_row_name, new_user, comment, user)`:
  ```python
  instance = frappe.get_doc("DC Process Instance", instance_name)
  step_row = next((s for s in instance.step_instances if s.name == step_row_name), None)
  assignees = frappe.parse_json(step_row.assignees_json or "[]")
  if user not in assignees:
      frappe.throw("Bạn không được chuyển giao bước này.", frappe.PermissionError)
  step_row.assignee = new_user
  step_row.assignees_json = frappe.as_json([new_user])
  _append_history(instance, step=step_row.step_template, action="Chuyển giao",
                  actor=user, comment=f"Chuyển giao cho {new_user}. {comment}")
  instance.save(ignore_permissions=True)
  notify_step_assigned(instance, step_row.step_name, [new_user])
  ```

  Implement `cancel_instance(instance_name, comment, user)`:
  - Tương tự `recall_instance` nhưng cho phép cả requester và Process Admin
  - Check role: `frappe.db.exists("Has Role", {"parent": user, "role": "Process Admin"})`

  _Requirements: Requirement 7 (Thu hồi, chuyển giao, hủy)_

---

## Phase 3: Notifications & Scheduler

- [ ] 11. **Service: `notifier.py`**

  Tạo file `dcnet_process/dcnet_process/services/notifier.py`.

  ```python
  import frappe

  def notify_step_assigned(instance, step_name: str, assignees: list[str]) -> None:
      subject = f"Bạn có việc cần xử lý: {step_name}"
      message = (
          f"Quy trình: <b>{instance.process_template}</b><br>"
          f"Bước: <b>{step_name}</b><br>"
          f"Người gửi: {instance.requester}"
      )
      link = f"/app/process-run/{instance.name}"
      for user in assignees:
          _send_desk(user, subject, message, link)
          _try_send_email(user, subject, message, link)

  def notify_status_change(instance, event: str, notify_users: list[str], comment: str = "") -> None:
      messages = {
          "returned":   "Yêu cầu bổ sung thông tin",
          "rejected":   "Lượt chạy bị từ chối",
          "completed":  "Lượt chạy đã hoàn tất",
          "recalled":   "Lượt chạy đã bị thu hồi",
          "cancelled":  "Lượt chạy đã bị hủy",
          "overdue":    "Bước đang quá hạn xử lý",
      }
      subject = messages.get(event, "Cập nhật lượt chạy quy trình")
      link = f"/app/process-run/{instance.name}"
      body = f"{subject}<br>Quy trình: {instance.process_template}"
      if comment:
          body += f"<br>Ghi chú: {comment}"
      for user in notify_users:
          _send_desk(user, subject, body, link)

  def notify_admin_intervention(instance, reason: str) -> None:
      admins = frappe.db.get_list(
          "Has Role", filters={"role": "Process Admin"}, fields=["parent"], pluck="parent"
      )
      subject = f"[Cần can thiệp] Quy trình {instance.process_template} — {instance.name}"
      reasons = {
          "no_assignee":       "Không phân giải được người xử lý",
          "no_matching_rule":  "Không tìm được flow rule phù hợp",
          "config_error":      "Lỗi cấu hình quy trình",
      }
      body = reasons.get(reason, reason)
      link = f"/app/dc-process-instance/{instance.name}"
      for admin in admins:
          _send_desk(admin, subject, body, link)

  def _send_desk(user: str, subject: str, message: str, link: str) -> None:
      doc = frappe.new_doc("Notification Log")
      doc.subject  = subject
      doc.for_user = user
      doc.type     = "Alert"
      doc.document_type = "DC Process Instance"
      doc.message  = message
      doc.insert(ignore_permissions=True)

  def _try_send_email(user: str, subject: str, message: str, link: str) -> None:
      try:
          user_doc = frappe.get_doc("User", user)
          if user_doc.email and frappe.db.get_value("User", user, "send_me_a_copy"):
              frappe.sendmail(recipients=[user_doc.email], subject=subject, message=message)
      except Exception:
          frappe.log_error(frappe.get_traceback(), "Process Notify Email Failed")
  ```

  _Requirements: Requirement 10 (Notifications)_

- [ ] 12. **Scheduler: `deadline_checker.py` + hooks**

  Tạo file `dcnet_process/dcnet_process/services/deadline_checker.py`:

  ```python
  import frappe

  def check_overdue_steps() -> None:
      now = frappe.utils.now_datetime()
      active_statuses = ["Đang xử lý", "Chờ duyệt", "Cần bổ sung"]
      instances = frappe.db.get_list(
          "DC Process Instance",
          filters={"status": ["in", active_statuses]},
          fields=["name"],
          ignore_permissions=True
      )
      for row in instances:
          instance = frappe.get_doc("DC Process Instance", row.name)
          changed = False
          for step in instance.step_instances:
              if (
                  step.deadline
                  and step.deadline < now
                  and not step.is_overdue
                  and step.status in ["Đang chờ xử lý", "Đang chờ duyệt"]
              ):
                  step.is_overdue = 1
                  changed = True
                  assignees = frappe.parse_json(step.assignees_json or "[]")
                  from dcnet_process.dcnet_process.services.notifier import notify_status_change
                  notify_status_change(instance, "overdue", assignees)
          if changed:
              any_active_overdue = any(
                  s.is_overdue and s.status in ["Đang chờ xử lý", "Đang chờ duyệt"]
                  for s in instance.step_instances
              )
              instance.is_overdue = 1 if any_active_overdue else 0
              instance.save(ignore_permissions=True)
  ```

  Thêm vào `hooks.py`:
  ```python
  scheduler_events = {
      "hourly": [
          "dcnet_process.dcnet_process.services.deadline_checker.check_overdue_steps"
      ]
  }
  ```

  _Requirements: Requirement 9 (Deadline & Quá hạn)_

---

## Phase 4: API Layer

- [ ] 13. **API: các endpoint runtime trong `api.py`**

  Thêm vào `dcnet_process/api.py` các endpoint sau (import services ở đầu hàm, không ở module level):

  ```python
  @frappe.whitelist()
  def list_active_templates(search=None):
      from dcnet_process.dcnet_process.services.process_template import list_process_templates
      templates = list_process_templates(search=search, status="Active")
      # Lọc thêm theo permission_type (nếu cần) — v1 trả về tất cả Active
      return templates

  @frappe.whitelist()
  def start_instance(template_name, form_data):
      from dcnet_process.dcnet_process.services.process_engine import start_instance
      data = frappe.parse_json(form_data) if isinstance(form_data, str) else form_data
      name = start_instance(template_name, data, frappe.session.user)
      return {"instance_name": name}

  @frappe.whitelist()
  def get_instance(instance_name):
      doc = frappe.get_doc("DC Process Instance", instance_name)
      if not doc.has_permission("read"):
          frappe.throw("Bạn không có quyền xem lượt chạy này.", frappe.PermissionError)
      return doc.as_dict()

  @frappe.whitelist()
  def take_action(instance_name, step_row_name, action, comment="", form_data="{}"):
      from dcnet_process.dcnet_process.services.process_engine import take_action
      data = frappe.parse_json(form_data) if isinstance(form_data, str) else form_data
      take_action(instance_name, step_row_name, action, comment, data, frappe.session.user)
      return {"status": "ok"}

  @frappe.whitelist()
  def recall_instance(instance_name, comment=""):
      from dcnet_process.dcnet_process.services.process_engine import recall_instance
      recall_instance(instance_name, comment, frappe.session.user)
      return {"status": "ok"}

  @frappe.whitelist()
  def reassign_step(instance_name, step_row_name, new_user, comment=""):
      from dcnet_process.dcnet_process.services.process_engine import reassign_step
      reassign_step(instance_name, step_row_name, new_user, comment, frappe.session.user)
      return {"status": "ok"}

  @frappe.whitelist()
  def cancel_instance(instance_name, comment=""):
      from dcnet_process.dcnet_process.services.process_engine import cancel_instance
      cancel_instance(instance_name, comment, frappe.session.user)
      return {"status": "ok"}

  @frappe.whitelist()
  def get_my_inbox(process_template=None, status=None, from_date=None, to_date=None):
      user = frappe.session.user
      # Lấy tất cả instance mà user là assignee của ít nhất 1 step đang active
      # Dùng SQL để query cross-table hiệu quả
      conditions = ["si.assignees_json LIKE %(user_pattern)s",
                    "si.status IN ('Đang chờ xử lý', 'Đang chờ duyệt')"]
      filters_values = {"user_pattern": f'%"{user}"%'}
      if process_template:
          conditions.append("i.process_template = %(template)s")
          filters_values["template"] = process_template
      where = " AND ".join(conditions)
      rows = frappe.db.sql(f"""
          SELECT i.name, i.process_template, i.requester, i.status, i.is_overdue,
                 si.name AS step_row_name, si.step_name, si.deadline, si.is_overdue AS step_overdue
          FROM `tabDC Process Instance` i
          JOIN `tabDC Process Step Instance` si ON si.parent = i.name
          WHERE {where}
          ORDER BY si.is_overdue DESC, si.deadline ASC, i.creation ASC
      """, values=filters_values, as_dict=True)
      return rows

  @frappe.whitelist()
  def get_instance_list(process_template=None, status=None, from_date=None, to_date=None,
                        page=1, page_length=20):
      user = frappe.session.user
      is_admin = frappe.db.exists("Has Role", {"parent": user, "role": ["in", ["System Manager", "Process Admin"]]})
      filters = {}
      if process_template:
          filters["process_template"] = process_template
      if status:
          filters["status"] = status
      if not is_admin:
          # Chỉ xem instance mình gửi hoặc mình là assignee
          filters["requester"] = user  # v1: chỉ lọc requester, assignee cần subquery
      return frappe.db.get_list(
          "DC Process Instance",
          filters=filters,
          fields=["name", "process_template", "requester", "status",
                  "current_step", "submitted_at", "completed_at", "is_overdue"],
          order_by="submitted_at desc",
          page_length=int(page_length),
          start=(int(page) - 1) * int(page_length)
      )

  @frappe.whitelist()
  def get_dashboard_stats(process_template=None, from_date=None, to_date=None):
      filters = {}
      if process_template:
          filters["process_template"] = process_template
      all_instances = frappe.db.get_list(
          "DC Process Instance", filters=filters,
          fields=["status", "is_overdue"], ignore_permissions=False
      )
      by_status = {}
      for row in all_instances:
          by_status[row.status] = by_status.get(row.status, 0) + 1
      overdue = sum(1 for r in all_instances if r.is_overdue)
      pending_approval = by_status.get("Chờ duyệt", 0)
      return {"by_status": by_status, "overdue_steps": overdue, "pending_approval": pending_approval}
  ```

  _Requirements: Requirement 1, 3, 4, 7, 11, 12, 14_

---

## Phase 5: UI Pages

- [ ] 14. **UI: Process Catalog — danh sách quy trình để khởi chạy**

  Tạo frappe Page `process_catalog`:
  - File: `dcnet_process/dcnet_process/page/process_catalog/process_catalog.json`
  - File: `dcnet_process/dcnet_process/page/process_catalog/process_catalog.js` (entry Vue)

  Layout: Grid card, mỗi card hiển thị:
  - Icon quy trình
  - Tên quy trình + nhóm (process_group)
  - Mô tả ngắn
  - Nút "Khởi chạy" → navigate tới `/app/process-run?template={name}`
  - Search bar lọc theo tên

  API call: `frappe.call("dcnet_process.api.list_active_templates", {search: q})`

  _Requirements: Requirement 1.1, Requirement 13.1_

- [ ] 15. **UI: Launch Form — màn hình khởi chạy quy trình**

  Trong page `process_run` (tạo mới hoặc tích hợp logic vào catalog):
  Route: `/app/process-run?template={template_name}` (mode: launch)

  Hiển thị form động dựng từ `template.steps[0].form_schema_json`:
  - Field types: `text`, `textarea`, `date`, `select` (radio/dropdown), `file`, `table`
  - Required validation: highlight đỏ field thiếu khi submit
  - Điều kiện hiển thị trường: đọc `display_condition` của field, ẩn/hiện realtime

  Submit → `frappe.call("dcnet_process.api.start_instance", {template_name, form_data})` → redirect `/app/process-run/{instance_name}`

  _Requirements: Requirement 1.2, Requirement 1.3, Requirement 13.1_

- [ ] 16. **UI: Task Processing View — màn hình xử lý bước**

  Route: `/app/process-run/{instance_name}` (mode: process)

  Layout 3 cột theo MISA:
  ```
  ┌────────────┬──────────────────────┬─────────────────────┐
  │  Timeline  │    Form bước hiện tại│  Comment + Đính kèm │
  │  (dọc)     │    (editable/readonly)│  + Người liên quan  │
  │            │                      │                     │
  │  Bước 1 ✓ │  [trường bắt buộc]  │  💬 Comment          │
  │  Bước 2 ⏳ │  [trường tùy chọn]  │  📎 Đính kèm        │
  │  Bước 3 … │                      │  👥 Người liên quan  │
  └────────────┴──────────────────────┴─────────────────────┘
  ```

  Panel trái (Timeline):
  - Danh sách step instances theo thứ tự step_order
  - Badge trạng thái màu: xanh (hoàn tất), vàng (đang chờ), đỏ (từ chối/quá hạn), xám (chưa tới)
  - Overdue indicator (icon đồng hồ đỏ)

  Panel giữa (Form):
  - Bước hiện tại (user là assignee): render editable form theo step schema
  - Bước khác + show_first_step_fields_in_next_steps: render readonly

  Panel phải:
  - Ô nhập comment + nút gửi
  - Upload đính kèm (Frappe file attachment)
  - Danh sách người liên quan từ step.related_people_json

  Action buttons (dưới form, theo loại bước):
  - Bước phê duyệt (is_approval_step=True): "Đồng ý" (primary) + "Từ chối" (danger)
  - Bước thực hiện: "Chuyển tiếp" (primary) + "Trả về" (secondary)
  - Bước cuối: "Hoàn tất" (primary)
  - Luôn có: "Thu hồi" (requester only) + "Chuyển giao" (assignee only)

  API calls:
  - Load: `frappe.call("dcnet_process.api.get_instance", {instance_name})`
  - Action: `frappe.call("dcnet_process.api.take_action", {...})`
  - Recall: `frappe.call("dcnet_process.api.recall_instance", {...})`
  - Reassign: `frappe.call("dcnet_process.api.reassign_step", {...})`

  _Requirements: Requirement 3, 4, 7, 8, 13.2, 13.3, 13.4, 13.5_

- [ ] 17. **UI: Process Inbox — "Công việc của tôi"**

  Tạo frappe Page `process_inbox`:

  Layout: Danh sách (list view style) với các cột:
  - Tên quy trình | Bước đang chờ | Người gửi | Hạn xử lý | Trạng thái | Ngày tạo

  Filter bar: Theo quy trình, theo trạng thái, khoảng ngày, người gửi.

  Hiển thị chỉ báo quá hạn: row màu đỏ nhạt + badge "Quá hạn".

  Click row → navigate tới `/app/process-run/{instance_name}`

  Badge số công việc trên menu/icon: `frappe.call("dcnet_process.api.get_my_inbox")` → count

  _Requirements: Requirement 11.1, 11.2, 11.5, Requirement 9.4_

- [ ] 18. **UI: Dashboard theo dõi**

  Tạo frappe Page `process_dashboard` (hoặc tích hợp vào workspace):

  Hiển thị:
  - **Cards tổng quan:** Đang xử lý | Đã hoàn tất | Từ chối | Đã hủy (số lượng)
  - **Cảnh báo:** Số bước quá hạn (màu đỏ) + Số đang chờ duyệt (màu cam)
  - **Bảng lọc:** Dropdown chọn quy trình + date range

  Filter tự động theo quyền: Process Admin/System Manager → toàn bộ. Người dùng → chỉ instance của mình.

  API: `frappe.call("dcnet_process.api.get_dashboard_stats", {process_template, from_date, to_date})`

  _Requirements: Requirement 14_

---

## Phase 6: Tests & Integration

- [ ] 19. **Unit tests: condition_evaluator và assignee_resolver**

  File `tests/test_condition_evaluator.py`:
  ```python
  import unittest
  from dcnet_process.dcnet_process.services.condition_evaluator import evaluate

  class TestConditionEvaluator(unittest.TestCase):
      def test_empty_condition_returns_true(self):
          self.assertTrue(evaluate({}, {"field": "value"}))

      def test_bang_true(self):
          self.assertTrue(evaluate({"field": "x", "operator": "Bằng", "value": "A"}, {"x": "A"}))

      def test_bang_false(self):
          self.assertFalse(evaluate({"field": "x", "operator": "Bằng", "value": "A"}, {"x": "B"}))

      def test_and_compound(self):
          cond = {"logic": "AND", "conditions": [
              {"field": "a", "operator": "Bằng", "value": "1"},
              {"field": "b", "operator": "Bằng", "value": "2"},
          ]}
          self.assertTrue(evaluate(cond, {"a": "1", "b": "2"}))
          self.assertFalse(evaluate(cond, {"a": "1", "b": "3"}))

      def test_or_compound(self):
          cond = {"logic": "OR", "conditions": [
              {"field": "a", "operator": "Bằng", "value": "1"},
              {"field": "b", "operator": "Bằng", "value": "2"},
          ]}
          self.assertTrue(evaluate(cond, {"a": "X", "b": "2"}))

      def test_trong_operator(self):
          self.assertTrue(evaluate({"field": "x", "operator": "Trống", "value": ""}, {"x": None}))
          self.assertFalse(evaluate({"field": "x", "operator": "Trống", "value": ""}, {"x": "val"}))

      def test_missing_field_treated_as_empty(self):
          self.assertTrue(evaluate({"field": "x", "operator": "Trống", "value": ""}, {}))
  ```

  Chạy: `python -m pytest dcnet_process/dcnet_process/tests/test_condition_evaluator.py -v`

  _Requirements: Requirement 5_

- [ ] 20. **Integration test: full flow khởi chạy → approve → complete**

  File `tests/test_process_engine.py` (Frappe test format):

  ```python
  import frappe
  import unittest
  from dcnet_process.dcnet_process.services.process_engine import start_instance, take_action
  from dcnet_process.dcnet_process.services.process_template import seed_demo_process_template

  class TestProcessEngine(unittest.TestCase):
      @classmethod
      def setUpClass(cls):
          # Đảm bảo demo template tồn tại
          seed_demo_process_template(ignore_permissions=True)

      def test_start_instance_creates_correct_record(self):
          template = frappe.db.get_value("DC Process Template",
              {"process_name": "Quy trình cấp phát tài sản"}, "name")
          # Activate template nếu chưa
          frappe.db.set_value("DC Process Template", template, "status", "Active")

          form_data = {
              "allocate_for": "Nhân viên",
              "asset_type": "Tài sản CNTT",
              "reason": "Test",
              "required_date": "2026-12-31",
          }
          instance_name = start_instance(template, form_data, "Administrator")
          instance = frappe.get_doc("DC Process Instance", instance_name)

          self.assertEqual(instance.status, "Đang xử lý")
          self.assertEqual(instance.requester, "Administrator")
          self.assertTrue(len(instance.step_instances) > 0)
          self.assertTrue(len(instance.history) > 0)

      def test_take_action_approve_advances_step(self):
          # Cần có instance đang ở bước "department_approval"
          # (setup từ test trước hoặc tạo riêng)
          pass  # Implement khi có test data đầy đủ

  # Chạy:
	# bench --site flow.local run-tests --app dcnet_process \
	#   --module dcnet_process.dcnet_process.tests.test_process_engine -v
  ```

  _Requirements: Requirement 1, 3, 4, 5_

---

## Checklist tổng thể

| Task | Requirement | Status |
|------|-------------|--------|
| 1. Schema DC Process Step Instance | R6, R9 | ⬜ |
| 2. Schema DC Process Instance | R9, R11 | ⬜ |
| 3. condition_evaluator.py | R5 | ⬜ |
| 4. assignee_resolver.py | R2 | ⬜ |
| 5. process_engine: start_instance | R1 | ⬜ |
| 6. process_engine: activate_step | R1, R2 | ⬜ |
| 7. process_engine: take_action | R3, R4, R8 | ⬜ |
| 8. process_engine: _advance_instance | R5 | ⬜ |
| 9. process_engine: parallel steps | R6 | ⬜ |
| 10. process_engine: recall/reassign/cancel | R7 | ⬜ |
| 11. notifier.py | R10 | ⬜ |
| 12. deadline_checker.py + hooks | R9 | ⬜ |
| 13. API endpoints | R1,3,4,7,11,12,14 | ⬜ |
| 14. UI: Process Catalog | R1, R13 | ⬜ |
| 15. UI: Launch Form | R1, R13 | ⬜ |
| 16. UI: Task Processing View | R3,4,7,8,13 | ⬜ |
| 17. UI: Process Inbox | R11, R9 | ⬜ |
| 18. UI: Dashboard | R14 | ⬜ |
| 19. Unit tests | R5 | ⬜ |
| 20. Integration tests | R1,3,4,5 | ⬜ |

**Requirement coverage:**
- R1 Khởi chạy → Task 5, 6, 13, 14, 15
- R2 Assignee Resolution → Task 4, 6
- R3 Hành động phê duyệt → Task 7, 13, 16
- R4 Hành động thực hiện → Task 7, 13, 16
- R5 Rẽ nhánh điều kiện → Task 3, 8, 19
- R6 Bước song song → Task 1, 9
- R7 Thu hồi/chuyển giao/hủy → Task 10, 13, 16
- R8 Lịch sử audit trail → Task 7
- R9 Deadline/quá hạn → Task 1, 2, 12
- R10 Thông báo → Task 11
- R11 Inbox + danh sách → Task 13, 17
- R12 Phân quyền runtime → Task 5, 7, 10, 13
- R13 UI/UX MISA → Task 14, 15, 16, 17
- R14 Dashboard → Task 13, 18
