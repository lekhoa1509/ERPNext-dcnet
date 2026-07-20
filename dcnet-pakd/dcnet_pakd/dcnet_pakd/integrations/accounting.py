"""Accounting integration: create + submit Journal Entry for commission components.

Components are posted as SEPARATE JEs (one per component type) so that Sales
Commission (NVKD payroll-like cost), License Fee (state regulatory fee), and
any other component remain traceable + filterable in sổ cái — they have
different deductibility profiles for CIT settlement and group reporting.

When PAKD Settings.use_hrms_for_commission = 0 (bypass-HRMS), Sales Commission
flows through this JE path with the CR row tagged party_type=Employee +
party=sales_person so the credit lands in 334 against the specific NVKD.
When use_hrms = 1, Sales Commission is excluded — it's pushed through
Additional Salary instead and only License Fee remains.
"""

import frappe
from frappe import _
from frappe.utils import today

# Non-deductible helper (vn_accounting Phase 1) — wrapped in try/except to keep
# dcnet_pakd installable without vn_accounting (cross-app dep is soft).
try:
	from vn_accounting.non_deductible.helper import (
		mark_non_deductible,
		REASON_NO_INVOICE,
	)
	_NON_DEDUCTIBLE_AVAILABLE = True
except ImportError:
	_NON_DEDUCTIBLE_AVAILABLE = False
	def mark_non_deductible(row, reason):  # noqa: ARG001
		pass
	REASON_NO_INVOICE = "Không HĐ hợp lệ"


def _is_non_deductible_beneficiary(line, override: bool | None = None) -> tuple[bool, str]:
	"""Return (flag, reason) for a PAKD beneficiary expense.

	Per TT78/2014 + NĐ 132/2020: khoản chi cho cá nhân ngoài lương HĐLĐ
	KHÔNG có HĐ hợp pháp = NON-deductible TNDN, bất kể có khấu trừ TNCN
	hay không. PIT withholding ≠ CIT deductibility — đó là 2 sắc thuế khác
	nhau. Mặc định bật flag; người dùng tick/untick xác nhận trên popup
	"Đăng JE" hoặc trực tiếp trên row JE Account.

	Args:
		line: PAKD Beneficiary Line row (MS / AC / Referral)
		override: explicit user choice from UI popup. ``True`` → force flag;
			``False`` → force unflag (có HĐ); ``None`` → use default heuristic.
	"""
	if override is not None:
		return (bool(override), REASON_NO_INVOICE if override else "")
	# Có HĐ hợp pháp → deductible (schema sẽ bổ sung field invoice_no ở v0.3+)
	if (getattr(line, "invoice_no", None) or "").strip():
		return False, ""
	# Mặc định: PAKD beneficiary không có channel HĐ → non-deductible TNDN
	return True, REASON_NO_INVOICE


# Component → (DR setting key, CR setting key). MS/AC/GPVT are always written
# via this path. Sales Commission is only included when use_hrms=0.
_COMPONENT_ACCOUNT_FIELDS_HRMS = {
	"Manager Services": ("account_manager_services", "counter_account_manager_services"),
	"Add Costs": ("account_add_costs", "counter_account_add_costs"),
	"License Fee": ("account_gpvt", "counter_account_gpvt"),
}
_COMPONENT_ACCOUNT_FIELDS_DIRECT = {
	**_COMPONENT_ACCOUNT_FIELDS_HRMS,
	"Sales Commission": ("account_sales_commission", "account_employee_payable"),
}


def post_journal_entry(
	pakd_doc,
	accounting_lines: list,
	payroll_month: str,
	pe_name: str,
	include_sales_commission: bool = False,
) -> dict[str, str]:
	"""Create + submit ONE JE PER COMPONENT TYPE for the accounting commission lines.

	Args:
		accounting_lines: list of PAKD Commission Line dicts/rows
		include_sales_commission: when True, also book Sales Commission lines
			with party=Employee on the CR side (HRMS-bypass mode)

	Returns ``{component: je_name}`` for each component that produced a JE.
	Returns ``{}`` if no lines map to configured accounts.
	"""
	if not accounting_lines:
		return {}

	settings = frappe.get_cached_doc("PAKD Settings", "PAKD Settings")
	fields_map = (
		_COMPONENT_ACCOUNT_FIELDS_DIRECT if include_sales_commission else _COMPONENT_ACCOUNT_FIELDS_HRMS
	)

	# Group lines by component so each component type produces its own JE.
	by_component: dict[str, list] = {}
	for line in accounting_lines:
		if line.component not in fields_map:
			continue
		by_component.setdefault(line.component, []).append(line)

	result: dict[str, str] = {}
	for component, lines in by_component.items():
		je_name = _post_je_for_component(
			pakd_doc, component, lines, settings, fields_map, payroll_month, pe_name
		)
		if je_name:
			result[component] = je_name
	return result


def _post_je_for_component(
	pakd_doc, component: str, lines: list, settings, fields_map: dict,
	payroll_month: str, pe_name: str,
) -> str | None:
	"""Build + submit a single-component JE. Internal helper for post_journal_entry."""
	dr_field, cr_field = fields_map[component]
	dr_account = settings.get(dr_field)
	cr_account = settings.get(cr_field) if cr_field else None

	if not dr_account:
		frappe.throw(
			_("PAKD Settings: account not configured for {0} ({1})").format(component, dr_field)
		)
	if cr_field and not cr_account:
		frappe.throw(
			_("PAKD Settings: counter account not configured for {0} ({1})").format(component, cr_field)
		)

	je = frappe.new_doc("Journal Entry")
	je.posting_date = _last_day_of_month(payroll_month)
	je.voucher_type = "Journal Entry"
	je.company = pakd_doc.company
	je.remark = f"PAKD {component} {payroll_month} | PAKD {pakd_doc.name} | PE {pe_name}"
	je.user_remark = je.remark

	for line in lines:
		je.append("accounts", {
			"account": dr_account,
			"debit_in_account_currency": line.amount,
			"credit_in_account_currency": 0,
			"cost_center": pakd_doc.get("cost_center"),
		})
		if cr_account:
			cr_row = {
				"account": cr_account,
				"debit_in_account_currency": 0,
				"credit_in_account_currency": line.amount,
			}
			if component == "Sales Commission" and pakd_doc.get("sales_person"):
				cr_row["party_type"] = "Employee"
				cr_row["party"] = pakd_doc.sales_person
			je.append("accounts", cr_row)

	if not je.accounts:
		return None

	je.flags.ignore_permissions = True
	je.insert()
	je.submit()
	return je.name


def post_journal_entry_single(
	pakd_doc,
	line,
	payroll_month: str,
	include_sales_commission_party: bool = True,
) -> str:
	"""Create and submit a 2-leg JE for a single PAKD Commission Line (cell mode).

	Args:
		line: a PAKD Commission Line row (has .component, .amount, .name)
		payroll_month: 'YYYY-MM'
		include_sales_commission_party: when component=='Sales Commission' and
			this is True (bypass-HRMS mode), the CR row is tagged with
			party_type=Employee + party=pakd_doc.sales_person.

	Returns the JE name.

	Caller is responsible for verifying that line.state == 'Pending', that the
	component is mappable, and (in HRMS mode) that the component is NOT
	Sales Commission (which goes to AS, not JE).
	"""
	settings = frappe.get_cached_doc("PAKD Settings", "PAKD Settings")
	fields = _COMPONENT_ACCOUNT_FIELDS_DIRECT.get(line.component)
	if not fields:
		frappe.throw(_("Không có mapping TK cho {0}").format(line.component))

	dr_field, cr_field = fields
	dr_account = settings.get(dr_field)
	cr_account = settings.get(cr_field) if cr_field else None
	if not dr_account:
		frappe.throw(_("PAKD Settings: chưa cấu hình {0} ({1})").format(line.component, dr_field))
	if cr_field and not cr_account:
		frappe.throw(_("PAKD Settings: chưa cấu hình TK đối ứng {0} ({1})").format(line.component, cr_field))

	je = frappe.new_doc("Journal Entry")
	je.posting_date = _last_day_of_month(payroll_month)
	je.voucher_type = "Journal Entry"
	je.company = pakd_doc.company
	je.remark = f"PAKD commission CELL {line.component} {payroll_month} | PAKD {pakd_doc.name} | line {line.name}"
	je.user_remark = je.remark

	je.append("accounts", {
		"account": dr_account,
		"debit_in_account_currency": line.amount,
		"credit_in_account_currency": 0,
		"cost_center": pakd_doc.get("cost_center"),
	})
	cr_row = {
		"account": cr_account,
		"debit_in_account_currency": 0,
		"credit_in_account_currency": line.amount,
	}
	if (
		line.component == "Sales Commission"
		and include_sales_commission_party
		and pakd_doc.get("sales_person")
	):
		cr_row["party_type"] = "Employee"
		cr_row["party"] = pakd_doc.sales_person
	je.append("accounts", cr_row)

	je.flags.ignore_permissions = True
	je.insert()
	je.submit()
	return je.name


def _last_day_of_month(payroll_month: str) -> str:
	import calendar
	year, month = map(int, payroll_month.split("-"))
	last_day = calendar.monthrange(year, month)[1]
	return f"{payroll_month}-{last_day:02d}"


_BENEFICIARY_KIND_ACCOUNT_FIELDS = {
	# kind → (DR setting key, counter-payable setting key for 2-leg path)
	"Manager Services": ("account_manager_services", "counter_account_manager_services"),
	"Add Costs": ("account_add_costs", "counter_account_add_costs"),
	"Referral": ("account_external_commission", "account_external_payable"),
}


def post_beneficiary_je(
	pakd_doc, line, payroll_month: str | None = None, pe_name: str = "",
	non_deductible_override: bool | None = None,
) -> str | None:
	"""Create and submit a JE for a single PAKD Beneficiary Line (MS / AC / Referral).

	JE shape:
	- ``recipient_name`` blank → 2-leg: DR ``account_<kind>`` / CR ``counter_<kind>``.
	- ``recipient_name`` set + ``recipient_tax_pct`` > 0 → 3-leg:
	    DR ``account_<kind>``               gross
	    CR ``account_external_payable``     net   (3388 — payable to person)
	    CR ``account_pit_withholding``      pit   (3335 — withheld for tax authority)
	- ``recipient_name`` set + ``recipient_tax_pct`` == 0 → 2-leg with party
	  optionally tagged (no PIT withholding, e.g. recipient < taxable threshold).

	Returns the JE name, or ``None`` when ``amount_per_period`` <= 0.

	Caller marks the line ``state=Posted`` + sets ``line.journal_entry``.
	"""
	if not line:
		return None

	amount = float(line.amount_per_period or 0)
	if amount <= 0:
		return None

	pit_amount = float(line.pit_amount or 0)
	net_amount = float(line.net_amount or 0)
	has_recipient = bool(line.recipient_name)
	use_3leg = has_recipient and pit_amount > 0

	if use_3leg and abs(amount - (net_amount + pit_amount)) > 0.5:
		frappe.throw(_("Beneficiary {0}: gross ≠ net + PIT — re-save PAKD to refresh.").format(line.kind))

	settings = frappe.get_cached_doc("PAKD Settings", "PAKD Settings")
	fields = _BENEFICIARY_KIND_ACCOUNT_FIELDS.get(line.kind)
	if not fields:
		frappe.throw(_("Unknown beneficiary kind: {0}").format(line.kind))

	dr_field, cr_field = fields
	dr_account = settings.get(dr_field)
	if not dr_account:
		frappe.throw(_("PAKD Settings: chưa cấu hình {0} ({1})").format(line.kind, dr_field))

	if use_3leg:
		cr_payable = settings.account_external_payable
		cr_pit = settings.account_pit_withholding
		for required, label in [
			(cr_payable, "TK Phải trả người ngoài (3388)"),
			(cr_pit, "TK Thuế TNCN tạm giữ (3335)"),
		]:
			if not required:
				frappe.throw(_("PAKD Settings: chưa cấu hình {0}").format(label))
	else:
		cr_payable = settings.get(cr_field)
		if not cr_payable:
			frappe.throw(_("PAKD Settings: chưa cấu hình TK đối ứng cho {0} ({1})").format(line.kind, cr_field))

	posting_date = _last_day_of_month(payroll_month) if payroll_month else today()
	recipient_label = line.recipient_name or ""
	if line.recipient_id:
		recipient_label += f" ({line.recipient_id})"

	je = frappe.new_doc("Journal Entry")
	je.voucher_type = "Journal Entry"
	je.posting_date = posting_date
	je.company = pakd_doc.company
	bs_idx = getattr(line, "billing_schedule_idx", None) or ""
	remark_parts = [f"PAKD {pakd_doc.name}", f"{line.kind}"]
	if bs_idx:
		remark_parts.append(f"kỳ {bs_idx}")
	if recipient_label:
		remark_parts.append(recipient_label)
	if pe_name:
		remark_parts.append(f"PE {pe_name}")
	je.remark = " | ".join(remark_parts)
	je.user_remark = je.remark

	# DR — expense
	dr_remark = f"{line.kind}" + (f" — {recipient_label}" if recipient_label else "")
	non_ded_flag, non_ded_reason = _is_non_deductible_beneficiary(line, override=non_deductible_override)
	if non_ded_flag:
		dr_remark += f" [Không trừ TNDN: {non_ded_reason}]"
	dr_row = {
		"account": dr_account,
		"debit_in_account_currency": amount,
		"credit_in_account_currency": 0,
		"cost_center": pakd_doc.get("cost_center"),
		"user_remark": dr_remark,
	}
	if non_ded_flag:
		dr_row["is_non_deductible"] = 1
		dr_row["non_deductible_reason"] = non_ded_reason
	je.append("accounts", dr_row)

	if use_3leg:
		je.append("accounts", {
			"account": cr_payable,
			"debit_in_account_currency": 0,
			"credit_in_account_currency": net_amount,
			"user_remark": f"Phải trả {recipient_label} (gốc {amount:,.0f} − TNCN {pit_amount:,.0f})",
		})
		je.append("accounts", {
			"account": cr_pit,
			"debit_in_account_currency": 0,
			"credit_in_account_currency": pit_amount,
			"user_remark": f"Khấu trừ TNCN từ {line.kind} cho {recipient_label}",
		})
	else:
		cr_row = {
			"account": cr_payable,
			"debit_in_account_currency": 0,
			"credit_in_account_currency": amount,
			"user_remark": f"Phải trả {recipient_label}" if recipient_label else f"Phải trả khác — {line.kind}",
		}
		je.append("accounts", cr_row)

	je.flags.ignore_permissions = True
	je.insert()
	je.submit()
	return je.name


# Legacy ``post_external_commission_je`` removed in v0.2.0. Use
# ``post_beneficiary_je`` with a ``PAKD Beneficiary Line`` row of
# ``kind=Referral`` (recipient + TNCN) instead.
