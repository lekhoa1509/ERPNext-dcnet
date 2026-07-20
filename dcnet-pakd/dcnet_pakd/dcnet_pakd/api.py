"""Whitelisted endpoints for the PAKD summary header card + approval reminder service."""

import frappe
from frappe import _
from frappe.utils import get_url_to_form, getdate, now_datetime, today


# ─────────────────────────────────────────────────────────────────────────────
# Permission gates for commission line mutations (pivot UI)
# ─────────────────────────────────────────────────────────────────────────────
_POST_ROLES = {"PAKD Accountant", "PAKD Board", "Accounts Manager", "System Manager"}
_SKIP_ROLES = {"PAKD Board", "Accounts Manager", "System Manager"}
_OVERRIDE_ROLES = {"PAKD Board", "Accounts Manager", "System Manager"}
_REOPEN_ROLES = {"Accounts Manager", "System Manager"}


def _require_any_role(allowed: set) -> None:
	user_roles = set(frappe.get_roles(frappe.session.user))
	if not user_roles.intersection(allowed):
		frappe.throw(
			_("Không đủ quyền — cần một trong: {0}").format(", ".join(sorted(allowed))),
			frappe.PermissionError,
		)


# ─────────────────────────────────────────────────────────────────────────────
# Workflow state → required role mapping (used by reminder lookup)
# ─────────────────────────────────────────────────────────────────────────────
_APPROVER_ROLE_BY_STATE = {
	"Pending Sales Director": ["PAKD Sales Director {branch}", "PAKD Sales Director"],
	"Pending General Dept": ["PAKD General Department"],
	"Pending Branch Director": ["PAKD Branch Director {branch}", "PAKD Branch Director"],
	"Pending Board": ["PAKD Board"],
}


@frappe.whitelist()
def get_summary_kpis(pakd_name: str) -> dict:
	"""Return everything the PAKD summary header card needs in one round-trip."""
	if not pakd_name or not frappe.db.exists("Phuong An Kinh Doanh", pakd_name):
		frappe.throw(_("PAKD not found: {0}").format(pakd_name))

	pakd = frappe.get_cached_doc("Phuong An Kinh Doanh", pakd_name)

	# Margin pct computation
	tr_service = float(pakd.total_revenue_service or 0)
	total_cost = float(pakd.total_cost or 0)
	margin_pct = round((tr_service - total_cost) / tr_service * 100, 1) if tr_service else 0

	# Thresholds from settings
	settings = frappe.get_cached_doc("PAKD Settings")
	green_thr = float(settings.margin_green_threshold or 25)
	amber_thr = float(settings.margin_amber_threshold or 15)
	if margin_pct >= green_thr:
		margin_color = "green"
	elif margin_pct >= amber_thr:
		margin_color = "amber"
	else:
		margin_color = "red"

	# Drift check against contract items (mirrors phuong_an_kinh_doanh.js _item_signature)
	drifted = _is_drifted(pakd)

	# Days waiting in current workflow state
	days_waiting = _days_in_current_state(pakd)

	# Next action decision tree
	next_action = _pakd_next_action(pakd, settings, days_waiting)

	return {
		"workflow_state": pakd.workflow_state or pakd.status or "Draft",
		"status": pakd.status,
		"pakd_type": pakd.pakd_type,
		"contract_ref": pakd.contract_ref,
		"customer": pakd.customer,
		"customer_name": pakd.customer_name,
		"sales_person_name": pakd.sales_person_name,
		"branch": pakd.branch,
		"total_revenue_contract": float(pakd.total_revenue_contract or 0),
		"total_cost": total_cost,
		"total_revenue_service": tr_service,
		"total_sales_commission": float(pakd.total_sales_commission or 0),
		"effective_commission_pct": float(pakd.effective_commission_pct or 0),
		"margin_pct": margin_pct,
		"margin_color": margin_color,
		"drifted": drifted,
		"rejection_reason": pakd.rejection_reason or "",
		"additional_salary": pakd.additional_salary,
		"days_waiting": days_waiting,
		"is_empty": not pakd.items or (pakd.total_revenue_contract or 0) == 0,
		"next_action": next_action,
	}


def _is_drifted(pakd) -> bool:
	"""Mirror of phuong_an_kinh_doanh.js _item_signature() / _check_contract_drift()."""
	if not pakd.contract_ref:
		return False
	contract = frappe.get_cached_doc("DCNet Contract", pakd.contract_ref)
	pakd_sig = _item_signature(pakd.items)
	contract_sig = _item_signature(contract.items)
	return pakd_sig != contract_sig


def _item_signature(items):
	sig = []
	for it in items or []:
		sig.append("|".join([
			(it.item_label or "").strip(),
			it.uom or "",
			str(float(it.qty or 0)),
			str(float(it.unit_price or 0)),
		]))
	return ";".join(sorted(sig))


def _days_in_current_state(pakd) -> int:
	"""Approximate days waiting since modified — proxy for time in current workflow state."""
	if not pakd.modified:
		return 0
	return max(0, (getdate(today()) - getdate(pakd.modified)).days)


def _pakd_next_action(pakd, settings, days_waiting: int):
	"""Decision tree for 'Việc cần làm' on PAKD card."""
	state = pakd.workflow_state or pakd.status or "Draft"

	if state == "Draft":
		# Map next role for transition
		return {
			"text": _("Gửi duyệt {0}").format(_next_role_name(pakd, "Pending Sales Director")),
			"button_label": _("Gửi duyệt"),
			"button_action": "submit_for_approval",
			"button_args": {"pakd": pakd.name},
		}

	if state in _APPROVER_ROLE_BY_STATE:
		role_name = _format_approver_label(state, pakd.branch)
		return {
			"text": _("Chờ duyệt từ {0} ({1} ngày)").format(role_name, days_waiting),
			"button_label": _("Nhắc duyệt"),
			"button_action": "send_approval_reminder",
			"button_args": {"pakd": pakd.name},
		}

	if state == "Approved":
		auto_post = int(settings.commission_post_on_approval or 0)
		use_hrms = bool(settings.use_hrms_for_commission)
		has_as = bool(pakd.additional_salary)

		# HRMS mode — AS record exists, link user to it
		if has_as:
			as_date = frappe.db.get_value("Additional Salary", pakd.additional_salary, "payroll_date")
			return {
				"text": _("Đã đăng hoa hồng ngày {0} — AS: {1}").format(
					frappe.format_value(as_date, {"fieldtype": "Date"}) if as_date else "",
					pakd.additional_salary,
				),
				"button_label": _("Mở AS"),
				"button_action": "navigate",
				"button_args": {"doctype": "Additional Salary", "name": pakd.additional_salary},
			}

		# Bypass-HRMS mode — surface the latest JE attached to any Posted commission line
		if not use_hrms:
			posted_je = frappe.db.get_value(
				"PAKD Commission Line",
				{"parent": pakd.name, "state": "Posted", "journal_entry": ["is", "set"]},
				"journal_entry",
				order_by="creation desc",
			)
			if posted_je:
				return {
					"text": _("Đã đăng hoa hồng — JE: {0}").format(posted_je),
					"button_label": _("Mở JE"),
					"button_action": "navigate",
					"button_args": {"doctype": "Journal Entry", "name": posted_je},
				}

		if auto_post:
			# Transient state — auto-post in progress or failed
			return {
				"text": _("Đang đăng hoa hồng tự động…"),
				"button_label": None,
				"button_action": None,
			}

		# Manual posting required
		commission_amount = float(pakd.total_sales_commission or 0)
		button_label = _("Đăng hoa hồng (JE)") if not use_hrms else _("Đăng hoa hồng (AS + JE)")
		return {
			"text": _("{0}: {1}").format(
				button_label,
				frappe.format_value(commission_amount, {"fieldtype": "Currency"}),
			),
			"button_label": _("Đăng hoa hồng"),
			"button_action": "post_commission",
			"button_args": {"pakd": pakd.name},
		}

	if state == "Rejected":
		return {
			"text": _("Lý do từ chối: {0}").format(pakd.rejection_reason or _("(không có lý do)")),
			"button_label": _("Sửa & gửi lại"),
			"button_action": "revise_and_resubmit",
			"button_args": {"pakd": pakd.name},
		}

	return {"text": "", "button_label": None, "button_action": None}


def _format_approver_label(state: str, branch: str | None) -> str:
	"""Human-friendly label of who needs to approve next."""
	labels = {
		"Pending Sales Director": _("GĐ KD {0}").format(branch or ""),
		"Pending General Dept": _("Phòng Tổng hợp"),
		"Pending Branch Director": _("GĐ Chi nhánh {0}").format(branch or ""),
		"Pending Board": _("Ban Lãnh đạo"),
	}
	return labels.get(state, state).strip()


def _next_role_name(pakd, target_state: str) -> str:
	return _format_approver_label(target_state, pakd.branch)


# ─────────────────────────────────────────────────────────────────────────────
# Reminder service — "Nhắc duyệt" button on PAKD header card
# ─────────────────────────────────────────────────────────────────────────────
@frappe.whitelist()
def send_approval_reminder(pakd: str) -> dict:
	"""Send email reminder to user(s) holding the role required for current workflow_state.

	Rate limit: cannot send same PAKD twice from same user within reminder_throttle_hours.

	Returns dict: {sent: int, recipients: list[str], log: str (RL name)}.
	"""
	if not pakd or not frappe.db.exists("Phuong An Kinh Doanh", pakd):
		frappe.throw(_("PAKD not found: {0}").format(pakd))

	pakd_doc = frappe.get_doc("Phuong An Kinh Doanh", pakd)
	state = pakd_doc.workflow_state or pakd_doc.status or "Draft"

	if state not in _APPROVER_ROLE_BY_STATE:
		frappe.throw(_("PAKD '{0}' không ở trạng thái chờ duyệt").format(pakd))

	# Rate limit check
	settings = frappe.get_cached_doc("PAKD Settings")
	throttle_hours = int(settings.reminder_throttle_hours or 24)
	current_user = frappe.session.user

	recent = frappe.db.sql(
		"""SELECT name FROM `tabPAKD Reminder Log`
		   WHERE pakd=%s AND sent_by=%s
		     AND sent_at > NOW() - INTERVAL %s HOUR
		   LIMIT 1""",
		(pakd, current_user, throttle_hours),
	)
	if recent:
		frappe.throw(
			_("Bạn vừa nhắc duyệt PAKD này trong {0} giờ qua. Hãy đợi trước khi nhắc lại.").format(throttle_hours)
		)

	# Resolve recipients via role lookup chain
	recipients = _resolve_approver_emails(state, pakd_doc.branch)
	if not recipients:
		frappe.throw(
			_("Không tìm thấy người duyệt cho bước này — liên hệ quản trị viên.")
		)

	# Render email body from template
	template = settings.reminder_email_template or _default_reminder_template()
	context = {
		"pakd_name": pakd,
		"pakd_url": get_url_to_form("Phuong An Kinh Doanh", pakd),
		"customer_name": pakd_doc.customer_name or pakd_doc.customer or "",
		"total_revenue": frappe.format_value(
			pakd_doc.total_revenue_contract or 0, {"fieldtype": "Currency"}
		),
		"days_waiting": _days_in_current_state(pakd_doc),
		"reminded_by": frappe.utils.get_fullname(current_user) or current_user,
	}
	rendered = frappe.render_template(template, context)
	subject = _("PAKD chờ duyệt: {0} — {1}").format(pakd, context["customer_name"])

	frappe.sendmail(
		recipients=recipients,
		subject=subject,
		message=rendered,
		reference_doctype="Phuong An Kinh Doanh",
		reference_name=pakd,
		now=True,
	)

	# Audit log
	log = frappe.get_doc({
		"doctype": "PAKD Reminder Log",
		"pakd": pakd,
		"sent_by": current_user,
		"sent_at": now_datetime(),
		"recipients": ", ".join(recipients),
		"workflow_state_at_send": state,
	})
	log.flags.ignore_permissions = True
	log.insert()

	return {
		"sent": len(recipients),
		"recipients": recipients,
		"log": log.name,
	}


def _resolve_approver_emails(state: str, branch: str | None) -> list[str]:
	"""4-step fallback chain per spec §4 reminder mechanic."""
	role_patterns = _APPROVER_ROLE_BY_STATE.get(state, [])
	emails: list[str] = []

	for pattern in role_patterns:
		role_name = pattern.format(branch=branch or "")
		role_name = role_name.strip()
		if not role_name:
			continue
		users = frappe.db.sql_list(
			"""SELECT DISTINCT u.email FROM `tabUser` u
			   INNER JOIN `tabHas Role` hr ON hr.parent = u.name
			   WHERE hr.role = %s AND u.enabled = 1 AND u.email IS NOT NULL AND u.email != ''""",
			role_name,
		)
		if users:
			emails = users
			break

	# Final fallback: System Manager
	if not emails:
		emails = frappe.db.sql_list(
			"""SELECT DISTINCT u.email FROM `tabUser` u
			   INNER JOIN `tabHas Role` hr ON hr.parent = u.name
			   WHERE hr.role = 'System Manager' AND u.enabled = 1
			     AND u.email IS NOT NULL AND u.email != ''"""
		)
		if emails:
			frappe.log_error(
				message=f"PAKD reminder fell back to System Manager for state '{state}', branch '{branch}'",
				title="PAKD reminder fallback",
			)

	return emails


def _default_reminder_template() -> str:
	return """
<p>Kính gửi,</p>
<p><strong>{{reminded_by}}</strong> nhắc bạn duyệt PAKD <a href="{{pakd_url}}">{{pakd_name}}</a>.</p>
<table>
<tr><td><b>Khách hàng:</b></td><td>{{customer_name}}</td></tr>
<tr><td><b>Doanh thu HĐ:</b></td><td>{{total_revenue}}</td></tr>
<tr><td><b>Đã chờ:</b></td><td>{{days_waiting}} ngày</td></tr>
</table>
<p>Vui lòng truy cập <a href="{{pakd_url}}">{{pakd_name}}</a> để xem chi tiết và duyệt.</p>
""".strip()


# ─────────────────────────────────────────────────────────────────────────────
# Set rejection reason — called from Workflow Action's reject button
# ─────────────────────────────────────────────────────────────────────────────
@frappe.whitelist()
def set_rejection_reason(pakd: str, reason: str) -> None:
	"""Persist rejection reason on PAKD. Called by JS reject dialog before workflow transition."""
	if not pakd or not frappe.db.exists("Phuong An Kinh Doanh", pakd):
		frappe.throw(_("PAKD not found: {0}").format(pakd))
	if not (reason or "").strip():
		frappe.throw(_("Lý do từ chối không được để trống"))

	frappe.db.set_value(
		"Phuong An Kinh Doanh", pakd, "rejection_reason", reason.strip(),
		update_modified=False,
	)


# ─────────────────────────────────────────────────────────────────────────────
# Post beneficiary JE — unified MS / AC / Referral 2- or 3-leg
# ─────────────────────────────────────────────────────────────────────────────
@frappe.whitelist()
def post_beneficiary_now(beneficiary_line: str, non_deductible: int | str | None = None) -> dict:
	"""Create a draft JE for one PAKD Beneficiary Line (MS / AC / Referral).

	2-leg when ``recipient_name`` blank; 3-leg with TNCN withholding when
	``recipient_name`` + ``recipient_tax_pct`` > 0.

	The PAKD must be Approved. Beneficiary line must be Pending. JE stays Draft.

	Args:
		non_deductible: explicit choice from popup checkbox. Truthy (1/"1"/True)
			→ force flag is_non_deductible=1 trên DR row; falsy (0/"0"/False)
			→ force flag=0 (user xác nhận có HĐ hợp pháp); ``None`` → engine
			dùng heuristic mặc định (PAKD beneficiary = non-deductible).
	"""
	_require_any_role(_POST_ROLES)

	from dcnet_pakd.dcnet_pakd.integrations.accounting import post_beneficiary_je

	if not beneficiary_line or not frappe.db.exists("PAKD Beneficiary Line", beneficiary_line):
		frappe.throw(_("Beneficiary line not found: {0}").format(beneficiary_line))

	line = frappe.get_doc("PAKD Beneficiary Line", beneficiary_line)
	if line.state != "Pending":
		frappe.throw(_("Beneficiary line không ở trạng thái Chờ — không thể đăng."))

	pakd = frappe.get_doc("Phuong An Kinh Doanh", line.parent)
	if pakd.workflow_state != "Approved":
		frappe.throw(_("Chỉ đăng beneficiary khi PAKD đã được duyệt"))

	# Parse non_deductible from frappe.form_dict (always str over HTTP)
	override: bool | None = None
	if non_deductible is not None and str(non_deductible).strip() != "":
		override = str(non_deductible).strip().lower() in ("1", "true", "yes")

	je_name = post_beneficiary_je(pakd, line, non_deductible_override=override)
	if not je_name:
		frappe.throw(_("Không tạo được Journal Entry — kiểm tra cấu hình PAKD Settings"))

	frappe.db.set_value(
		"PAKD Beneficiary Line",
		line.name,
		{
			"state": "Posted",
			"journal_entry": je_name,
		},
		update_modified=False,
	)
	frappe.db.commit()
	return {"journal_entry": je_name, "amount": line.amount_per_period}


@frappe.whitelist()
def post_external_commission(pakd: str) -> dict:
	"""Deprecated — forwards to ``post_beneficiary_now``. The legacy
	``external_commission_*`` flat block was dropped in v0.2.0; PAKDs now
	use PAKD Beneficiary Line rows with ``kind=Referral``.
	"""
	if not pakd or not frappe.db.exists("Phuong An Kinh Doanh", pakd):
		frappe.throw(_("PAKD not found: {0}").format(pakd))

	doc = frappe.get_doc("Phuong An Kinh Doanh", pakd)
	if doc.workflow_state != "Approved":
		frappe.throw(_("Chỉ đăng hoa hồng ngoài khi PAKD đã được duyệt"))

	pending_referral = frappe.get_all(
		"PAKD Beneficiary Line",
		filters={"parent": doc.name, "kind": "Referral", "state": "Pending"},
		fields=["name"],
		limit=1,
	)
	if pending_referral:
		return post_beneficiary_now(pending_referral[0].name)

	frappe.throw(_("Không có dòng Referral nào ở trạng thái Chờ. Tạo PAKD Beneficiary Line kind=Referral để đăng."))


# ─────────────────────────────────────────────────────────────────────────────
# Commission line cell-level actions (pivot UI)
# ─────────────────────────────────────────────────────────────────────────────


@frappe.whitelist()
def post_pakd_commission_period(pakd: str, month_index) -> dict:
	"""Post all Pending lines in this PAKD's column (period bundle)."""
	_require_any_role(_POST_ROLES)

	from dcnet_pakd.dcnet_pakd.events import _post_pakd_commission_lines

	month_index = int(month_index)
	pakd_doc = frappe.get_doc("Phuong An Kinh Doanh", pakd)

	pe_doc = None
	if pakd_doc.contract_ref:
		contract = frappe.get_cached_doc("DCNet Contract", pakd_doc.contract_ref)
		bs_row = next(
			(r for r in contract.get("billing_schedule", []) if r.month_index == month_index),
			None,
		)
		if bs_row and bs_row.get("sales_invoice"):
			pe_rows = frappe.db.sql(
				"""SELECT per.parent FROM `tabPayment Entry Reference` per
				   JOIN `tabPayment Entry` pe ON pe.name = per.parent
				   WHERE per.reference_doctype = 'Sales Invoice'
				     AND per.reference_name = %s
				     AND pe.docstatus = 1
				     AND pe.payment_type = 'Receive'
				   ORDER BY pe.posting_date DESC LIMIT 1""",
				(bs_row.sales_invoice,),
			)
			if pe_rows:
				pe_doc = frappe.get_doc("Payment Entry", pe_rows[0][0])

	if pe_doc is None:
		from types import SimpleNamespace
		pe_doc = SimpleNamespace(name="", posting_date=today())

	_post_pakd_commission_lines(pakd_doc.name, month_index, pe_doc)

	posted = frappe.get_all(
		"PAKD Commission Line",
		filters={
			"parent": pakd_doc.name,
			"billing_schedule_idx": month_index,
			"state": "Posted",
			"posted_by_cell": 0,
		},
		fields=["name", "journal_entry", "additional_salary"],
	)
	# Each component now produces its own JE — collect distinct JE names.
	distinct_jes = []
	seen = set()
	for p in posted:
		if p.journal_entry and p.journal_entry not in seen:
			seen.add(p.journal_entry)
			distinct_jes.append(p.journal_entry)
	je_name = ", ".join(distinct_jes) if distinct_jes else None
	as_name = next((p.additional_salary for p in posted if p.additional_salary), None)
	return {"je": je_name, "additional_salary": as_name, "lines_posted": len(posted)}


@frappe.whitelist()
def post_pakd_commission_line(line_name: str) -> dict:
	"""Cell-mode: post a single Pending PAKD Commission Line as a 2-leg JE.

	Refused for Sales Commission when use_hrms_for_commission=1.
	"""
	_require_any_role(_POST_ROLES)

	line = frappe.get_doc("PAKD Commission Line", line_name)
	if line.state != "Pending":
		frappe.throw(_("Dòng không ở trạng thái Chờ — không thể đăng."))

	pakd_doc = frappe.get_doc("Phuong An Kinh Doanh", line.parent)
	settings = frappe.get_cached_doc("PAKD Settings", "PAKD Settings")
	use_hrms = bool(settings.use_hrms_for_commission)
	if use_hrms and line.component == "Sales Commission":
		frappe.throw(
			_("Khi 'Dùng HRMS' bật, Hoa hồng NVKD đi qua Lương bổ sung (AS), "
			  "không thể đăng riêng 1 dòng. Dùng 'Đăng toàn kỳ' để gộp.")
		)

	from dcnet_pakd.dcnet_pakd.integrations.accounting import post_journal_entry_single
	from frappe.utils import add_months

	payment_date = getdate(today())
	cutoff_day = settings.cutoff_day_of_month or 5
	ref_month = add_months(payment_date, -1) if payment_date.day <= cutoff_day else payment_date
	payroll_month = ref_month.strftime("%Y-%m")

	je_name = post_journal_entry_single(
		pakd_doc, line, payroll_month,
		include_sales_commission_party=(not use_hrms),
	)

	frappe.db.set_value(
		"PAKD Commission Line",
		line.name,
		{
			"state": "Posted",
			"journal_entry": je_name,
			"posted_by_cell": 1,
			"payroll_month": payroll_month,
		},
		update_modified=False,
	)
	frappe.db.commit()
	return {"je": je_name, "amount": line.amount}


@frappe.whitelist()
def skip_pakd_commission_line(line_name: str, reason: str) -> dict:
	"""Transition a Pending line to Skipped with a reason (≥3 chars)."""
	_require_any_role(_SKIP_ROLES)

	reason = (reason or "").strip()
	if len(reason) < 3:
		frappe.throw(_("Lý do bỏ qua phải có ít nhất 3 ký tự."))

	line = frappe.get_doc("PAKD Commission Line", line_name)
	if line.state != "Pending":
		frappe.throw(_("Chỉ có thể bỏ qua dòng đang ở trạng thái Chờ."))

	frappe.db.set_value(
		"PAKD Commission Line",
		line.name,
		{"state": "Skipped", "skip_reason": reason},
		update_modified=False,
	)
	parent_doc = frappe.get_doc("Phuong An Kinh Doanh", line.parent)
	parent_doc.add_comment(
		"Comment",
		_("Bỏ qua hoa hồng: {0} kỳ {1} — {2}").format(line.component, line.billing_schedule_idx, reason),
	)
	frappe.db.commit()
	return {"state": "Skipped"}


@frappe.whitelist()
def set_pakd_commission_line_override(line_name: str, override_rate=None) -> dict:
	"""Set or clear line.override_rate. Triggers full PAKD save → _sync_commission_lines rescale."""
	_require_any_role(_OVERRIDE_ROLES)

	if override_rate is None or override_rate == "":
		new_rate = 0.0
	else:
		try:
			new_rate = float(override_rate)
		except (TypeError, ValueError):
			frappe.throw(_("Tỷ lệ phải là số."))
		if new_rate < 0 or new_rate > 1000:
			frappe.throw(_("Tỷ lệ phải nằm trong khoảng 0-1000%."))

	line = frappe.get_doc("PAKD Commission Line", line_name)
	if line.state != "Pending":
		frappe.throw(_("Chỉ có thể đặt override cho dòng đang ở trạng thái Chờ."))

	old_amount = float(line.amount or 0)
	frappe.db.set_value(
		"PAKD Commission Line",
		line.name,
		{"override_rate": new_rate},
		update_modified=False,
	)

	parent_doc = frappe.get_doc("Phuong An Kinh Doanh", line.parent)
	parent_doc.save(ignore_permissions=False)
	frappe.db.commit()

	new_amount = float(frappe.db.get_value("PAKD Commission Line", line_name, "amount") or 0)
	return {"old_amount": old_amount, "new_amount": new_amount, "effective_rate": new_rate}


@frappe.whitelist()
def reopen_pakd_commission_line(line_name: str) -> dict:
	"""Cancelled or Skipped → Pending (state-only). Deletes draft JE if any."""
	_require_any_role(_REOPEN_ROLES)

	line = frappe.get_doc("PAKD Commission Line", line_name)
	if line.state not in ("Cancelled", "Skipped"):
		frappe.throw(_("Chỉ có thể khôi phục dòng đang ở trạng thái Đã huỷ hoặc Bỏ qua."))

	if line.journal_entry and frappe.db.exists("Journal Entry", line.journal_entry):
		je_docstatus = frappe.db.get_value("Journal Entry", line.journal_entry, "docstatus")
		if je_docstatus == 1:
			frappe.throw(
				_("JE {0} đã được duyệt — không thể tự động khôi phục. Vui lòng đảo bút toán thủ công.")
				.format(line.journal_entry)
			)
		frappe.delete_doc("Journal Entry", line.journal_entry, ignore_permissions=True, force=1)

	frappe.db.set_value(
		"PAKD Commission Line",
		line.name,
		{
			"state": "Pending",
			"journal_entry": None,
			"additional_salary": None,
			"payment_entry": None,
			"payroll_month": None,
			"posted_by_cell": 0,
			"skip_reason": "",
		},
		update_modified=False,
	)
	parent_doc = frappe.get_doc("Phuong An Kinh Doanh", line.parent)
	parent_doc.add_comment(
		"Comment",
		_("Khôi phục dòng hoa hồng về Chờ: {0} kỳ {1}").format(line.component, line.billing_schedule_idx),
	)
	frappe.db.commit()
	return {"state": "Pending"}


# ─────────────────────────────────────────────────────────────────────────────
# Proportional auto-post — KTT click button trên PE form sau khi thanh toán
# ─────────────────────────────────────────────────────────────────────────────
@frappe.whitelist()
def auto_post_pakd_proportional(payment_entry: str) -> dict:
	"""Tạo draft JE proportional cho commission + beneficiary lines của PAKD.

	Tỷ lệ = PE.paid_amount / PAKD.total_revenue_contract.
	Mỗi line Pending: incremental_amount = (line.amount × pct) - line.auto_posted_pct%
	của line.amount. Tạo draft JE (docstatus=0) — KTT review + submit.

	Mỗi draft JE register vào Auto Generated Doc Registry với source_key tương ứng.

	Returns dict { je_names: [...], lines_processed, pakd, pct, skipped }.
	"""
	_require_any_role(_POST_ROLES)
	if not payment_entry or not frappe.db.exists("Payment Entry", payment_entry):
		frappe.throw(_("Payment Entry not found: {0}").format(payment_entry))

	pe = frappe.get_doc("Payment Entry", payment_entry)
	if pe.docstatus != 1:
		frappe.throw(_("Phiếu thu/chi phải đã ghi sổ (docstatus=1)."))
	pakd_name = pe.get("linked_pakd")
	if not pakd_name:
		frappe.throw(_("Phiếu thu/chi chưa link PAKD — vào dialog đối soát chọn PAKD trước."))
	if not frappe.db.exists("Phuong An Kinh Doanh", pakd_name):
		frappe.throw(_("PAKD không tồn tại: {0}").format(pakd_name))

	pakd = frappe.get_doc("Phuong An Kinh Doanh", pakd_name)
	if pakd.workflow_state != "Approved":
		frappe.throw(_("PAKD chưa được duyệt — không thể tạo JE."))
	total_revenue = float(pakd.total_revenue_contract or 0)
	if total_revenue <= 0:
		frappe.throw(_("PAKD.total_revenue_contract = 0 — không thể tính tỷ lệ."))

	pct_this_pe = (float(pe.paid_amount or 0) / total_revenue) * 100.0
	if pct_this_pe <= 0:
		frappe.throw(_("Tỷ lệ thanh toán = 0%."))

	je_names: list[str] = []
	skipped: list[str] = []
	lines_processed = 0

	# 1. Commission lines — AGGREGATE per component (1 JE per component thay vì
	# per-period). PAKD dài kỳ N tháng × M component = N×M Pending CL nhưng KTT
	# chỉ cần review ≤4 JE (Sales Commission + License Fee + MS + AC tổng hợp).
	by_component: dict[str, list[dict]] = {}
	for cl in (pakd.commission_lines or []):
		if cl.state != "Pending":
			skipped.append(f"CL {cl.name}: state={cl.state}")
			continue
		current_pct = float(cl.get("auto_posted_pct") or 0)
		new_total_pct = min(current_pct + pct_this_pe, 100.0)
		delta_pct = new_total_pct - current_pct
		if delta_pct <= 0:
			skipped.append(f"CL {cl.name}: đã đạt {current_pct}%")
			continue
		incremental_amount = float(cl.amount or 0) * (delta_pct / 100.0)
		if incremental_amount <= 0:
			continue
		by_component.setdefault(cl.component, []).append({
			"line": cl, "incremental": incremental_amount, "new_total_pct": new_total_pct,
		})

	for component, entries in by_component.items():
		total_amount = sum(e["incremental"] for e in entries)
		je_name = _create_aggregated_commission_je(
			pakd, component, total_amount, pe.name, pct_this_pe, len(entries),
		)
		if je_name:
			je_names.append(je_name)
			lines_processed += len(entries)
			for e in entries:
				e["line"].db_set("auto_posted_pct", e["new_total_pct"], update_modified=False)
			_register_auto_je(je_name, "dcnet_pakd.pe_proportional_commission")
		else:
			# Component không có account mapping (vd Sales Commission khi use_hrms=1)
			skipped.append(f"CL component={component}: không có mapping (use_hrms hoặc thiếu Settings)")

	# 2. Beneficiary lines (MS / AC / Referral với recipient)
	for bl in (pakd.beneficiary_lines or []):
		if bl.state != "Pending":
			skipped.append(f"BL {bl.name}: state={bl.state}")
			continue
		if not (bl.amount_per_period or 0):
			continue
		current_pct = float(bl.get("auto_posted_pct") or 0)
		new_total_pct = min(current_pct + pct_this_pe, 100.0)
		delta_pct = new_total_pct - current_pct
		if delta_pct <= 0:
			skipped.append(f"BL {bl.name}: đã đạt {current_pct}%")
			continue
		incremental_amount = float(bl.amount_per_period) * (delta_pct / 100.0)
		if incremental_amount <= 0:
			continue
		je_name = _create_proportional_beneficiary_je(
			pakd, bl, incremental_amount, pe.name, delta_pct,
		)
		if je_name:
			je_names.append(je_name)
			lines_processed += 1
			bl.db_set("auto_posted_pct", new_total_pct, update_modified=False)
			_register_auto_je(je_name, "dcnet_pakd.pe_proportional_beneficiary")

	frappe.db.commit()
	return {
		"payment_entry": pe.name,
		"pakd": pakd.name,
		"pct": round(pct_this_pe, 2),
		"je_names": je_names,
		"lines_processed": lines_processed,
		"skipped": skipped,
	}


def _create_aggregated_commission_je(pakd, component, total_amount, pe_name, pct, num_periods):
	"""Tạo 1 draft JE AGGREGATED cho tất cả Pending lines của 1 component.

	Vd PAKD 20 kỳ × License Fee 480k/kỳ × 30% = 1 JE tổng 2,880k (không 20 JE riêng).

	Sales Commission: skip nếu use_hrms=1 (HRMS lo); nếu use_hrms=0 → set
	party=Employee+sales_person trên CR row (TK 334).
	"""
	from dcnet_pakd.dcnet_pakd.integrations.accounting import (
		_COMPONENT_ACCOUNT_FIELDS_HRMS,
		_COMPONENT_ACCOUNT_FIELDS_DIRECT,
	)
	settings = frappe.get_cached_doc("PAKD Settings", "PAKD Settings")
	use_hrms = bool(settings.get("use_hrms_for_commission"))
	fields_map = _COMPONENT_ACCOUNT_FIELDS_HRMS if use_hrms else _COMPONENT_ACCOUNT_FIELDS_DIRECT
	fields = fields_map.get(component)
	if not fields:
		# Sales Commission khi use_hrms=1 — skip (HRMS lo phần này)
		return None
	dr_field, cr_field = fields
	dr_account = settings.get(dr_field)
	cr_account = settings.get(cr_field)
	if not dr_account or not cr_account:
		return None
	je = frappe.new_doc("Journal Entry")
	je.voucher_type = "Journal Entry"
	je.company = pakd.company
	je.posting_date = today()
	je.remark = (f"PAKD {pakd.name} | {component} {pct:.1f}% × {num_periods} kỳ "
	             f"từ PE {pe_name} (tự sinh — chờ KTT duyệt)")
	je.user_remark = je.remark
	je.append("accounts", {
		"account": dr_account,
		"debit_in_account_currency": total_amount,
		"credit_in_account_currency": 0,
		"cost_center": pakd.get("cost_center"),
	})
	cr_row = {
		"account": cr_account,
		"debit_in_account_currency": 0,
		"credit_in_account_currency": total_amount,
	}
	# TK 334 (Phải trả người lao động) cần party_type=Employee. Khi use_hrms=0,
	# Sales Commission route qua direct JE với party=sales_person.
	if component == "Sales Commission" and pakd.get("sales_person"):
		cr_row["party_type"] = "Employee"
		cr_row["party"] = pakd.sales_person
	je.append("accounts", cr_row)
	je.flags.ignore_permissions = True
	je.insert()
	return je.name


def _create_proportional_beneficiary_je(pakd, bl, amount, pe_name, pct):
	"""Tạo 1 draft JE cho beneficiary_line (MS/AC/Referral với recipient).

	2-leg nếu recipient_name blank hoặc PIT=0; 3-leg với khấu trừ TNCN.
	"""
	from dcnet_pakd.dcnet_pakd.integrations.accounting import (
		_BENEFICIARY_KIND_ACCOUNT_FIELDS,
		_is_non_deductible_beneficiary,
	)
	fields = _BENEFICIARY_KIND_ACCOUNT_FIELDS.get(bl.kind)
	if not fields:
		return None
	dr_field, cr_field = fields
	settings = frappe.get_cached_doc("PAKD Settings", "PAKD Settings")
	dr_account = settings.get(dr_field)
	if not dr_account:
		return None

	pit_rate = float(bl.recipient_tax_pct or 0)
	has_recipient = bool(bl.recipient_name)
	use_3leg = has_recipient and pit_rate > 0
	pit_amount = round(amount * pit_rate / 100, 2) if use_3leg else 0
	net_amount = amount - pit_amount

	je = frappe.new_doc("Journal Entry")
	je.voucher_type = "Journal Entry"
	je.company = pakd.company
	je.posting_date = today()
	recipient_label = bl.recipient_name or ""
	je.remark = (f"PAKD {pakd.name} | {bl.kind} {pct:.1f}% từ PE {pe_name} "
	             f"{recipient_label} (tự sinh — chờ KTT duyệt)")
	je.user_remark = je.remark

	non_ded_flag, non_ded_reason = _is_non_deductible_beneficiary(bl)
	dr_row = {
		"account": dr_account,
		"debit_in_account_currency": amount,
		"credit_in_account_currency": 0,
		"cost_center": pakd.get("cost_center"),
	}
	if non_ded_flag:
		dr_row["is_non_deductible"] = 1
		dr_row["non_deductible_reason"] = non_ded_reason
	je.append("accounts", dr_row)

	if use_3leg:
		cr_payable = settings.account_external_payable
		cr_pit = settings.account_pit_withholding
		if not (cr_payable and cr_pit):
			return None
		je.append("accounts", {
			"account": cr_payable,
			"debit_in_account_currency": 0,
			"credit_in_account_currency": net_amount,
		})
		je.append("accounts", {
			"account": cr_pit,
			"debit_in_account_currency": 0,
			"credit_in_account_currency": pit_amount,
		})
	else:
		cr_payable = settings.get(cr_field)
		if not cr_payable:
			return None
		je.append("accounts", {
			"account": cr_payable,
			"debit_in_account_currency": 0,
			"credit_in_account_currency": amount,
		})

	je.flags.ignore_permissions = True
	je.insert()
	return je.name


def _register_auto_je(je_name: str, source_key: str):
	"""Idempotent register vào Auto Generated Doc Registry (vn_accounting)."""
	try:
		from vn_accounting.auto_source import register as _register
		_register("Journal Entry", je_name, source_key,
		          registered_by="dcnet_pakd.api.auto_post_pakd_proportional")
	except ImportError:
		# vn_accounting chưa cài — skip, không block flow.
		pass
