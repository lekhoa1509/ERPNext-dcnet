import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields as _create_custom_fields

from dcnet_hrm import constants as const

MODULE = "DCNet HRM"


def after_install():
	after_migrate()


def after_migrate():
	# Idempotent (mọi hàm bên dưới đều tự kiểm tra tồn tại trước khi tạo) —
	# an toàn khi chạy lại. Đặt hết ở đây (không chỉ after_install) vì lúc
	# after_install chạy, DocType mới của app này có thể CHƯA được sync vào
	# DB (việc sync DocType diễn ra trong cùng flow migrate ngay sau đó).
	setup_custom_fields()
	setup_payroll_settings()
	seed_insurance_rate()
	seed_statutory_wage()
	create_salary_components()


def setup_custom_fields():
	_create_custom_fields(get_custom_fields(), update=True)


def get_custom_fields():
	return {
		"Employee": [
			{
				"fieldname": "vn_compliance_section",
				"fieldtype": "Section Break",
				"label": "Vietnamese Compliance Info",
				"insert_after": "salary_mode",
				"module": MODULE,
			},
			{
				"fieldname": "si_number",
				"fieldtype": "Data",
				"label": "Social Insurance Number",
				"insert_after": "vn_compliance_section",
				"unique": 1,
				"module": MODULE,
			},
			{
				"fieldname": "personal_tax_code",
				"fieldtype": "Data",
				"label": "Personal Tax Code",
				"insert_after": "si_number",
				"module": MODULE,
			},
			{
				"fieldname": "citizen_id",
				"fieldtype": "Data",
				"label": "Citizen ID Number",
				"insert_after": "personal_tax_code",
				"module": MODULE,
			},
			{
				"fieldname": "vn_compliance_column_break",
				"fieldtype": "Column Break",
				"insert_after": "citizen_id",
				"module": MODULE,
			},
			{
				"fieldname": "citizen_id_issue_date",
				"fieldtype": "Date",
				"label": "Citizen ID Issue Date",
				"insert_after": "vn_compliance_column_break",
				"module": MODULE,
			},
			{
				"fieldname": "citizen_id_issue_place",
				"fieldtype": "Data",
				"label": "Citizen ID Issue Place",
				"insert_after": "citizen_id_issue_date",
				"module": MODULE,
			},
			{
				"fieldname": "insurance_status",
				"fieldtype": "Select",
				"label": "Insurance Status",
				"options": "Fully Insured\nHealth Insurance Only\nNot Insured",
				"default": "Fully Insured",
				"insert_after": "citizen_id_issue_place",
				"module": MODULE,
			},
			{
				"fieldname": "minimum_wage_region",
				"fieldtype": "Select",
				"label": "Minimum Wage Region",
				"options": "Region I\nRegion II\nRegion III\nRegion IV",
				"insert_after": "insurance_status",
				"module": MODULE,
			},
			{
				"fieldname": "union_member",
				"fieldtype": "Check",
				"label": "Trade Union Member",
				"description": "Ảnh hưởng đoàn phí công đoàn 1% lương đóng BH",
				"insert_after": "minimum_wage_region",
				"module": MODULE,
			},
		],
		"Salary Structure Assignment": [
			{
				"fieldname": "insurance_salary",
				"fieldtype": "Currency",
				"label": "Insurance Contribution Salary",
				"description": "Mức lương đóng BHXH/BHYT/BHTN thỏa thuận — có thể khác lương thực nhận (base)",
				"insert_after": "variable",
				"module": MODULE,
			},
			{
				"fieldname": "net_agreement",
				"fieldtype": "Check",
				"label": "Net Salary Agreement",
				"description": "Nếu tick, engine sẽ giải ngược NET → GROSS khi tính lương",
				"insert_after": "insurance_salary",
				"module": MODULE,
			},
		],
		"Salary Slip": [
			{
				"fieldname": "vn_pit_breakdown_section",
				"fieldtype": "Section Break",
				"label": "Vietnamese PIT / Insurance Breakdown",
				"insert_after": "total_income_tax",
				"module": MODULE,
			},
			{
				"fieldname": "capped_insurance_salary",
				"fieldtype": "Currency",
				"label": "Capped Insurance Salary",
				"read_only": 1,
				"insert_after": "vn_pit_breakdown_section",
				"module": MODULE,
			},
			{
				"fieldname": "taxable_income",
				"fieldtype": "Currency",
				"label": "Taxable Income",
				"read_only": 1,
				"insert_after": "capped_insurance_salary",
				"module": MODULE,
			},
			{
				"fieldname": "vn_pit_breakdown_column_break",
				"fieldtype": "Column Break",
				"insert_after": "taxable_income",
				"module": MODULE,
			},
			{
				"fieldname": "assessable_income",
				"fieldtype": "Currency",
				"label": "Assessable Income",
				"read_only": 1,
				"insert_after": "vn_pit_breakdown_column_break",
				"module": MODULE,
			},
			{
				"fieldname": "dependent_count",
				"fieldtype": "Int",
				"label": "Dependent Count (This Period)",
				"read_only": 1,
				"insert_after": "assessable_income",
				"module": MODULE,
			},
			{
				"fieldname": "pit_breakdown",
				"fieldtype": "Small Text",
				"label": "PIT Bracket Breakdown",
				"read_only": 1,
				"insert_after": "dependent_count",
				"module": MODULE,
			},
		],
	}


def setup_payroll_settings():
	if not frappe.db.exists("DocType", "VN Payroll Settings"):
		return
	if frappe.db.get_single_value("VN Payroll Settings", "personal_deduction"):
		return
	settings = frappe.get_single("VN Payroll Settings")
	settings.personal_deduction = 11_000_000
	settings.dependent_deduction = 4_400_000
	settings.meal_allowance_exemption_cap = 730_000
	settings.union_funding_percent = 2
	settings.union_fee_percent = 1
	settings.save()


def seed_insurance_rate():
	if not frappe.db.exists("DocType", "Insurance Rate"):
		return
	if frappe.db.exists("Insurance Rate", {"effective_from": "2024-07-01"}):
		return
	doc = frappe.get_doc(
		{
			"doctype": "Insurance Rate",
			"effective_from": "2024-07-01",
			"rates": [
				{"insurance_type": "BHXH", "employee_percent": 8, "employer_percent": 17.5},
				{"insurance_type": "BHYT", "employee_percent": 1.5, "employer_percent": 3},
				{"insurance_type": "BHTN", "employee_percent": 1, "employer_percent": 1},
				{"insurance_type": "TNLĐ-BNN", "employee_percent": 0, "employer_percent": 0.5},
			],
		}
	)
	doc.insert(ignore_permissions=True)


def seed_statutory_wage():
	if not frappe.db.exists("DocType", "Statutory Wage"):
		return
	if frappe.db.exists("Statutory Wage", {"effective_from": "2024-07-01"}):
		return
	# ⚠️ Cần clarify với khách: xác nhận mức lương cơ sở / tối thiểu vùng đang
	# hiệu lực tại thời điểm triển khai — số liệu dưới đây theo Nghị định
	# 73/2024/NĐ-CP (lương cơ sở) và 74/2024/NĐ-CP (lương tối thiểu vùng),
	# hiệu lực từ 01/07/2024. Nếu đã có Nghị định mới hơn, cập nhật thêm 1
	# dòng Statutory Wage mới (effective_from mới) — KHÔNG sửa dòng cũ.
	doc = frappe.get_doc(
		{
			"doctype": "Statutory Wage",
			"effective_from": "2024-07-01",
			"base_salary": 2_340_000,
			"region_1": 4_960_000,
			"region_2": 4_410_000,
			"region_3": 3_860_000,
			"region_4": 3_450_000,
		}
	)
	doc.insert(ignore_permissions=True)


def create_salary_components():
	if "hrms" not in frappe.get_installed_apps():
		return
	for name in const.EARNING_COMPONENTS:
		extra = {}
		if name == const.PHONE_ALLOWANCE_COMPONENT:
			# Theo quy chế công ty — mặc định miễn thuế TNCN (spec 5.4).
			# Đổi lại ở Salary Component nếu quy chế khách hàng khác.
			extra["exempted_from_income_tax"] = 1
		_ensure_salary_component(name, "Earning", **extra)
	for name in [*const.EMPLOYEE_INSURANCE_COMPONENTS.values(), const.UNION_FEE_COMPONENT, const.PIT_COMPONENT]:
		_ensure_salary_component(name, "Deduction")
	for name in [*const.EMPLOYER_INSURANCE_COMPONENTS.values(), const.UNION_FUNDING_COMPONENT]:
		# Employer-side contributions: not deducted from pay, statistical only.
		_ensure_salary_component(name, "Deduction", statistical_component=1, do_not_include_in_total=1)


def _ensure_salary_component(name, component_type, **extra):
	if frappe.db.exists("Salary Component", name):
		return
	doc = frappe.get_doc(
		{
			"doctype": "Salary Component",
			"salary_component": name,
			"type": component_type,
			# Formula intentionally left empty — dcnet_hrm.payroll.vn_payroll.calculate
			# writes `amount` directly on Salary Slip validate.
			**extra,
		}
	)
	doc.insert(ignore_permissions=True)
