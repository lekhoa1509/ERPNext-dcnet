# Design Document: Vận hành quy trình (Process Execution Runtime)

## Overview

Tính năng này bổ sung **engine thực thi** cho app `dcnet-process`. App đã có sẵn phần thiết kế quy trình (DocType `DC Process Template`, các child table Step/Field/Flow Rule/Field Condition, service `process_template.py`, trang builder). Phần runtime hiện chỉ có khung DocType rỗng (`DC Process Instance`, `DC Process Step Instance`, `DC Process History`).

Mục tiêu: người dùng có thể khởi chạy quy trình đã publish → hệ thống tự điều phối bước → người xử lý thực hiện hành động → ghi lịch sử → quản lý deadline → gửi thông báo. UI bám sát MISA AMIS Quy Trình.

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                        UI Layer (Vue.js + frappe-ui)      │
│   Process Catalog | Launch Form | Inbox | Task View | Dashboard │
└────────────────────────────┬─────────────────────────────┘
                             │ frappe.call()
┌────────────────────────────▼─────────────────────────────┐
│                    API Layer  (api.py)                    │
│  list_active_templates | start_instance | take_action     │
│  recall_instance | reassign_step | cancel_instance        │
│  get_my_inbox | get_instance_list | get_dashboard_stats   │
└────────────────────────────┬─────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────┐
│                   Service Layer                           │
│  process_engine.py        — vòng đời instance            │
│  assignee_resolver.py     — phân giải người xử lý        │
│  condition_evaluator.py   — đánh giá điều kiện JSON      │
│  notifier.py              — desk + email notification     │
│  deadline_checker.py      — scheduler quét quá hạn       │
└────────────────────────────┬─────────────────────────────┘
                             │ Frappe ORM
┌────────────────────────────▼─────────────────────────────┐
│                   Data Layer                              │
│  DC Process Instance  →  DC Process Step Instance        │
│                       →  DC Process History              │
└──────────────────────────────────────────────────────────┘
```

### Design Principles

- **Stateless services** — service nhận document/dict, không giữ state nội bộ.
- **Single source of truth** — `DC Process Instance.form_data_json` chứa toàn bộ dữ liệu form tích lũy.
- **Immutable history** — `DC Process History` không được sửa/xóa sau khi tạo (chỉ read cho người thường).
- **Fail-safe** — mọi lỗi phân giải (assignee, flow rule) đều đặt instance sang trạng thái "Lỗi cấu hình" và thông báo Process Admin, KHÔNG tự ý kết thúc.
- **Permission-first** — mọi API endpoint kiểm tra quyền trước khi thực thi, không tin tưởng dữ liệu client.

---

## Components and Interfaces

### 1. Process Engine (`services/process_engine.py`)

Service trung tâm điều phối vòng đời instance.

```python
def start_instance(template_name: str, form_data: dict, user: str) -> str:
    """
    Validate template (status=Active, user có quyền).
    Tạo DC Process Instance (status="Đang xử lý", requester=user, submitted_at=now).
    Lưu form_data vào form_data_json.
    Gọi activate_step() cho bước đầu tiên (step_order=1).
    Returns: instance_name  (VD: "DPI-2026-00001")
    Raises:
        frappe.PermissionError  — user không có quyền khởi chạy
        frappe.ValidationError  — template không Active
    """

def activate_step(instance: Document, step_key: str) -> None:
    """
    Tạo/cập nhật bản ghi DC Process Step Instance tương ứng step_key.
    Gọi assignee_resolver.resolve_assignees() → lưu vào assignees_json + assignee.
    Tính deadline từ step.deadline_type + deadline_value.
    Cập nhật instance.current_step = step_key, instance.status tương ứng.
    Gọi notifier.notify_step_assigned().
    Nếu resolve_assignees() trả về [] → gọi _handle_no_assignee().
    """

def take_action(
    instance_name: str,
    step_row_name: str,   # name của DC Process Step Instance row
    action: str,          # "Đồng ý" | "Từ chối" | "Chuyển tiếp" | "Trả về" | "Hoàn tất"
    comment: str,
    form_data: dict,
    user: str
) -> None:
    """
    Validate user là assignee hợp lệ.
    Validate dữ liệu bắt buộc (nếu action yêu cầu comment).
    Merge form_data vào instance.form_data_json.
    Ghi DC Process History.
    Cập nhật step instance status + action_taken + completed_at.
    Gọi _advance_instance() để xác định bước kế tiếp.
    """

def recall_instance(instance_name: str, comment: str, user: str) -> None:
    """
    Validate user là requester, instance đang ở trạng thái active.
    Đặt tất cả step instances đang mở → "Đã hủy".
    Đặt instance.status = "Đã hủy".
    Ghi history. Gọi notifier báo các assignee hiện tại.
    """

def reassign_step(
    instance_name: str, step_row_name: str,
    new_user: str, comment: str, user: str
) -> None:
    """
    Validate user là assignee hợp lệ của bước.
    Cập nhật step instance.assignee = new_user, assignees_json = [new_user].
    Ghi history (action="Chuyển giao").
    Gọi notifier báo new_user.
    """

def cancel_instance(instance_name: str, comment: str, user: str) -> None:
    """
    Validate user là requester hoặc Process Admin.
    Tương tự recall_instance nhưng actor không giới hạn là requester.
    """

def _advance_instance(
    instance: Document,
    from_step_key: str,
    action: str,
    form_data: dict
) -> None:
    """
    Lấy flow_rules của template, lọc by from_step=from_step_key + action.
    Đánh giá condition theo order_index tăng dần (dùng condition_evaluator).
    Rule khớp đầu tiên → target_step (hoặc fallback_target_step).
    Nếu target = "END_COMPLETED" → complete_instance().
    Nếu target = "END_REJECTED"  → reject_instance().
    Nếu không có rule khớp       → _handle_config_error().
    Bước song song (is_parallel=True) → activate_parallel_group().
    """
```

### 2. Assignee Resolver (`services/assignee_resolver.py`)

```python
def resolve_assignees(step_dict: dict, instance: Document) -> list[str]:
    """
    step_dict: serialized DC Process Step (từ template)
    instance:  DC Process Instance document

    assignee_type → logic:
    ─────────────────────────────────────────────────────────
    "Người dùng tự chọn"      → [instance.requester]
    "Người tạo quy trình"     → [instance.requester]
    "Chọn người cụ thể"       → [step_dict["assignee_user"]]
    "Theo role"               → users có role = step_dict["assignee_role"]
                                 (frappe.db.get_list "Has Role")
    "Theo phòng ban"          → users thuộc step_dict["assignee_department"]
                                 (qua Employee.department)
    "Trưởng phòng"            → department head của phòng requester
                                 (Employee.department → Department.department_head → User)
    "Người quản lý trực tiếp" → Employee.reports_to của requester (→ User)
    "Theo vị trí công việc"   → employees có designation = step_dict["assignee_position"]
    "Người thực hiện bước trước" → lấy từ step instance liền trước đã completed
    ─────────────────────────────────────────────────────────
    Returns [] nếu không resolve được bất kỳ user nào.
    """
```

### 3. Condition Evaluator (`services/condition_evaluator.py`)

```python
def evaluate(condition: dict, form_data: dict) -> bool:
    """
    Đánh giá JSON condition dựa trên form_data.
    condition rỗng hoặc {} → trả về True (luôn khớp).

    Simple condition:
    {
        "field": "asset_type",
        "operator": "Bằng",   # Bằng|Khác|Lớn hơn|Nhỏ hơn|Chứa|Không chứa|Trống|Không trống
        "value": "Tài sản CNTT"
    }

    Compound condition (AND/OR):
    {
        "logic": "AND",         # AND | OR
        "conditions": [<condition>, ...]
    }

    Raises ValueError nếu operator không được hỗ trợ.
    Không dùng eval() — so sánh thuần Python.
    """

SUPPORTED_OPERATORS = {
    "Bằng": lambda a, b: str(a) == str(b),
    "Khác": lambda a, b: str(a) != str(b),
    "Lớn hơn": lambda a, b: float(a or 0) > float(b or 0),
    "Nhỏ hơn": lambda a, b: float(a or 0) < float(b or 0),
    "Chứa": lambda a, b: str(b) in str(a or ""),
    "Không chứa": lambda a, b: str(b) not in str(a or ""),
    "Trống": lambda a, _: not a,
    "Không trống": lambda a, _: bool(a),
}
```

### 4. Notifier (`services/notifier.py`)

```python
def notify_step_assigned(
    instance: Document,
    step_name: str,
    assignees: list[str]
) -> None:
    """
    Với mỗi user trong assignees:
      - Tạo frappe.get_doc("Notification Log") → desk notification
      - Nếu user bật email: enqueue email (không block nếu thất bại)
    Subject: "Bạn có việc cần xử lý: {step_name} — {instance.process_template}"
    Link:    /app/process-run/{instance.name}
    """

def notify_status_change(
    instance: Document,
    event: str,           # "returned"|"rejected"|"completed"|"recalled"|"cancelled"|"overdue"
    notify_users: list[str],
    comment: str = ""
) -> None:
    """Thông báo thay đổi trạng thái cho danh sách user."""

def notify_admin_intervention(instance: Document, reason: str) -> None:
    """
    reason: "no_assignee" | "no_matching_rule" | "config_error"
    Gửi thông báo cho tất cả users có role "Process Admin".
    """
```

### 5. Deadline Checker (`services/deadline_checker.py`)

```python
def check_overdue_steps() -> None:
    """
    Chạy bởi scheduler mỗi giờ.
    1. Lấy tất cả DC Process Instance có status in ("Đang xử lý", "Chờ duyệt", "Cần bổ sung").
    2. Với mỗi instance, duyệt step_instances đang ở trạng thái chờ.
    3. Nếu step.deadline < frappe.utils.now_datetime() và step.is_overdue = 0:
       - Đặt step.is_overdue = 1
       - Nếu tất cả active steps đều overdue → instance.is_overdue = 1
       - Gọi notifier.notify_status_change(event="overdue", assignees)
    4. instance.save(ignore_permissions=True)
    """
```

### 6. API Layer (`api.py`)

Tất cả endpoints đều dùng `@frappe.whitelist()` và trả về JSON.

```python
@frappe.whitelist()
def list_active_templates(search=None):
    """Trả về templates Active mà user có quyền khởi chạy."""

@frappe.whitelist()
def start_instance(template_name, form_data):
    """form_data: JSON string. Gọi process_engine.start_instance()."""

@frappe.whitelist()
def get_instance(instance_name):
    """Trả về instance + step_instances + history đã serialize."""

@frappe.whitelist()
def take_action(instance_name, step_row_name, action, comment="", form_data="{}"):
    """Gọi process_engine.take_action()."""

@frappe.whitelist()
def recall_instance(instance_name, comment=""):
    """Gọi process_engine.recall_instance()."""

@frappe.whitelist()
def reassign_step(instance_name, step_row_name, new_user, comment=""):
    """Gọi process_engine.reassign_step()."""

@frappe.whitelist()
def cancel_instance(instance_name, comment=""):
    """Gọi process_engine.cancel_instance()."""

@frappe.whitelist()
def get_my_inbox(process_template=None, status=None, from_date=None, to_date=None):
    """
    Trả về các DC Process Step Instance đang chờ user hiện tại xử lý.
    Sắp xếp: quá hạn trước, rồi theo deadline, rồi theo created_at.
    """

@frappe.whitelist()
def get_instance_list(process_template=None, status=None, requester=None,
                      from_date=None, to_date=None, page=1, page_length=20):
    """
    Danh sách DC Process Instance theo quyền của user.
    Process Admin/System Manager → tất cả.
    Người khác → chỉ instance mình là requester hoặc assignee.
    """

@frappe.whitelist()
def get_dashboard_stats(process_template=None, from_date=None, to_date=None):
    """
    Trả về:
    {
        "by_status": {"Đang xử lý": N, "Đã hoàn tất": M, ...},
        "overdue_steps": K,
        "pending_approval": L
    }
    """
```

---

## Data Models

### Thay đổi cần thực hiện trên DocType hiện có

#### DC Process Step Instance — thêm fields

| fieldname | fieldtype | Mô tả |
|-----------|-----------|--------|
| `parallel_group` | Data | Key nhóm bước song song (cùng group chạy đồng thời) |
| `assignees_json` | Code (JSON) | Array email user có thể xử lý bước này |
| `is_overdue` | Check | Bước đã quá hạn |

#### DC Process Instance — thêm fields

| fieldname | fieldtype | Mô tả |
|-----------|-----------|--------|
| `is_overdue` | Check | Có ít nhất 1 bước đang quá hạn |

### State Machine

**DC Process Instance `status`:**

```
Draft
  └─→ Đang xử lý ──→ Cần bổ sung ──→ Đang xử lý (cycle)
          ├──→ Đã hoàn tất
          ├──→ Từ chối
          ├──→ Đã hủy
          └──→ Lỗi cấu hình  (cần Process Admin can thiệp)
```

**DC Process Step Instance `status`:**

```
Chưa tới lượt
  └─→ Đang chờ xử lý / Đang chờ duyệt
          ├──→ Đã đồng ý / Đã chuyển tiếp / Đã hoàn tất
          ├──→ Đã từ chối / Đã trả về
          └── (song song) Quá hạn
```

### Parallel Steps

Bước song song được nhận diện bằng `step.is_parallel = True` trong template. Khi kích hoạt:

```
Template step "director_approval" (is_parallel=True, step_order=3)
  → Tạo nhiều step instances với parallel_group = "pg_3"
  → Mỗi instance có assignee riêng
  → Tất cả phải complete trước khi _advance_instance() chuyển tiếp
```

Quy tắc hội tụ mặc định: ALL phải đồng ý. Nếu 1 bước từ chối → áp dụng flow rule "Từ chối" của nhóm.

### form_data_json Schema

```json
{
  "request": {
    "allocate_for": "Nhân viên",
    "asset_type": "Tài sản CNTT",
    "reason": "Thiết bị mới cho nhân viên onboard"
  },
  "director_approval": {
    "approval_note": "Đồng ý cấp phát"
  }
}
```

Mỗi key là `step_key`, value là dict field_key → value của bước đó.

---

## Error Handling

| Tình huống | Xử lý |
|-----------|--------|
| Template không Active khi khởi chạy | `frappe.ValidationError` |
| User không có quyền khởi chạy | `frappe.PermissionError` |
| Không resolve được assignee | instance.status = "Lỗi cấu hình", notify_admin_intervention("no_assignee") |
| Không có flow rule khớp | instance.status = "Lỗi cấu hình", notify_admin_intervention("no_matching_rule") |
| User không phải assignee hợp lệ | `frappe.PermissionError` |
| Comment bắt buộc khi từ chối nhưng thiếu | `frappe.ValidationError` |
| Email gửi thất bại | Log lỗi, KHÔNG block luồng xử lý |
| Bước song song bị từ chối | Hủy tất cả step trong parallel_group, áp dụng reject flow rule |
| Instance đã ở trạng thái kết thúc | `frappe.ValidationError` khi cố recall/reassign/cancel |

---

## File Structure

```
dcnet-process/dcnet_process/dcnet_process/
├── services/
│   ├── process_template.py          (EXISTS — không sửa)
│   ├── process_engine.py            (NEW)
│   ├── assignee_resolver.py         (NEW)
│   ├── condition_evaluator.py       (NEW)
│   ├── notifier.py                  (NEW)
│   └── deadline_checker.py          (NEW)
├── doctype/
│   ├── dc_process_instance/
│   │   └── dc_process_instance.json (MODIFY — thêm is_overdue)
│   └── dc_process_step_instance/
│       └── dc_process_step_instance.json (MODIFY — thêm 3 fields)
├── page/
│   ├── dcnet_process/               (EXISTS — builder, không sửa)
│   ├── process_inbox/               (NEW — Vue page: inbox)
│   ├── process_run/                 (NEW — Vue page: launch + task)
│   └── process_dashboard/           (NEW — Vue page: dashboard)
├── api.py                           (MODIFY — thêm runtime endpoints)
└── tests/
    ├── test_condition_evaluator.py   (NEW)
    ├── test_assignee_resolver.py     (NEW)
    └── test_process_engine.py        (NEW)
```

```
dcnet-process/dcnet_process/
└── hooks.py   (MODIFY — thêm scheduler_events)
```

---

## Security Considerations

- Mọi `@frappe.whitelist()` phải gọi `frappe.get_doc(...).has_permission()` hoặc check role trước khi thực thi.
- `form_data_json` chỉ expose cho user có quyền đọc instance.
- Assignee validation: chỉ user có tên trong `assignees_json` của step instance mới có thể gọi `take_action`.
- Process Viewer: chỉ read, không gọi được start/take_action/recall/reassign/cancel.
- Không dùng `eval()` trong condition_evaluator — so sánh thuần Python.
- Input form_data được validate theo `form_schema_json` của bước trước khi lưu.

---

## Testing Strategy

### Unit Tests

- `test_condition_evaluator.py` — test tất cả operators (Bằng, Khác, Chứa, AND/OR, rỗng), edge cases (None values, type mismatch)
- `test_assignee_resolver.py` — mock frappe.db, test từng assignee_type
- `test_process_engine.py` — test start_instance, take_action với mock template + instance

### Integration Tests (chạy trong devcontainer)

```bash
bench --site flow.local run-tests --app dcnet_process --module dcnet_process.tests -v
```

Test scenario chính:
1. Start instance → bước 1 được activate với đúng assignee
2. Approve bước 1 → condition branching → bước kế tiếp đúng
3. Reject → flow về bước trước hoặc END_REJECTED
4. Parallel steps → cả 2 approve → advance; 1 reject → dừng
5. Recall bởi requester → status "Đã hủy", assignee nhận thông báo
6. Deadline vượt quá → is_overdue = 1, notification gửi đi
