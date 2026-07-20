"""Engine tính lương VN — hook vào Salary Slip.validate (chạy SAU khi HRMS
Salary Slip đã tự tính gross_pay/earnings từ Salary Structure).

Chỉ ghi đè `amount` của các Deduction thuộc phạm vi VN (BHXH/BHYT/BHTN,
đoàn phí, thuế TNCN, các khoản DN đóng — statistical, không trừ lương) và,
khi có `net_agreement`, ghi đè earning "Lương cơ bản" để giải NET → GROSS.
Không đụng tới các earning/deduction khác do Salary Structure hoặc
Additional Salary quản lý.
"""

import json

import frappe
from frappe.utils import flt, getdate, month_diff

from dcnet_hrm import constants as const
from dcnet_hrm.payroll import pit, social_insurance

MAX_NET_TO_GROSS_ITERATIONS = 20
NET_TO_GROSS_TOLERANCE = 1  # đồng


def calculate(doc, method=None):
	if doc.get("salary_slip_based_on_timesheet"):
		# Phase 1 chưa xử lý payslip theo timesheet — để nguyên logic gốc của HRMS.
		return

	settings = frappe.get_single("VN Payroll Settings")
	employee = frappe.get_doc("Employee", doc.employee)
	ssa = get_salary_structure_assignment(doc.employee, doc.start_date)
	on_date = doc.start_date

	insurance_salary = flt(ssa.insurance_salary) or flt(ssa.base)

	if ssa.net_agreement and flt(ssa.base):
		# ⚠️ Giả định (cần xác nhận với khách): ssa.base là mức NET thỏa
		# thuận khi net_agreement=1, và "Lương cơ bản" là earning duy nhất
		# được giải ngược — các earning/phụ cấp khác giữ nguyên giá trị đã
		# nhập trên Salary Slip. insurance_salary lấy từ SSA.insurance_salary
		# (độc lập, không phụ thuộc kết quả giải ngược).
		# solve_net_to_gross() đã tự gọi đủ apply_social_insurance/
		# apply_income_tax/apply_union_dues ở vòng lặp hội tụ cuối cùng.
		solve_net_to_gross(doc, employee, settings, insurance_salary, target_net=flt(ssa.base), on_date=on_date)
	else:
		apply_social_insurance(doc, employee, settings, insurance_salary, on_date)
		apply_income_tax(doc, employee, settings, insurance_salary, on_date)
		apply_union_dues(doc, employee, settings, insurance_salary)

	doc.set_net_pay()


# ---------------------------------------------------------------------------
# Salary Structure Assignment / Employee helpers
# ---------------------------------------------------------------------------


def get_salary_structure_assignment(employee, on_date):
	name = frappe.db.get_value(
		"Salary Structure Assignment",
		{"employee": employee, "from_date": ["<=", on_date], "docstatus": 1},
		"name",
		order_by="from_date desc",
	)
	if not name:
		frappe.throw(
			frappe._("No submitted Salary Structure Assignment found for {0} as of {1}.").format(
				employee, on_date
			)
		)
	return frappe.get_doc("Salary Structure Assignment", name)


def should_contribute_insurance(doc, settings, on_date):
	if not settings.enable_skip_insurance_under_min_days:
		return True
	# `payment_days` = ngày công được trả lương trong kỳ, dùng làm số ngày
	# công thực tế của tháng cho mục đích đối chiếu luật BHXH.
	min_days = const.get_min_working_days_for_insurance(on_date)
	return flt(doc.payment_days) >= min_days


# ---------------------------------------------------------------------------
# Bước 1-3: BHXH / BHYT / BHTN / TNLĐ-BNN
# ---------------------------------------------------------------------------


def apply_social_insurance(doc, employee, settings, insurance_salary, on_date):
	si_result = {"types": {}, "employee_total": 0, "employer_total": 0, "capped_insurance_salary": 0}

	if should_contribute_insurance(doc, settings, on_date):
		si_result = social_insurance.calculate(
			insurance_salary=insurance_salary,
			insurance_status=employee.insurance_status or "Fully Insured",
			minimum_wage_region=employee.minimum_wage_region,
			on_date=on_date,
		)

	for insurance_type, component in const.EMPLOYEE_INSURANCE_COMPONENTS.items():
		amount = si_result["types"].get(insurance_type, {}).get("employee", 0)
		set_component_amount(doc, "deductions", component, amount)

	for insurance_type, component in const.EMPLOYER_INSURANCE_COMPONENTS.items():
		amount = si_result["types"].get(insurance_type, {}).get("employer", 0)
		set_component_amount(doc, "deductions", component, amount, statistical=True)

	doc.capped_insurance_salary = si_result["capped_insurance_salary"]
	doc._vn_employee_insurance_total = si_result["employee_total"]


# ---------------------------------------------------------------------------
# Bước 4-7: Thuế TNCN
# ---------------------------------------------------------------------------


def apply_income_tax(doc, employee, settings, insurance_salary, on_date):
	employee_insurance_total = getattr(doc, "_vn_employee_insurance_total", 0)

	non_taxable = compute_non_taxable_earnings(doc, settings)
	taxable_income = max(flt(doc.gross_pay) - non_taxable, 0)
	dependents = count_active_dependents(doc.employee, doc.start_date)

	probation = get_probation_flat_tax_rule(employee, on_date)
	if probation and flt(doc.gross_pay) >= probation["income_floor"]:
		tax_amount = round_vnd(taxable_income * probation["rate_percent"] / 100)
		assessable_income = taxable_income
		breakdown = [
			{
				"note": "Khấu trừ 10% flat (HĐ < 3 tháng / thời vụ) — TT111/2013/TT-BTC Điều 25.1.i",
				"rate_percent": probation["rate_percent"],
				"taxable_amount": round_vnd(taxable_income),
				"tax": tax_amount,
			}
		]
	else:
		assessable_income = max(
			taxable_income
			- employee_insurance_total
			- flt(settings.personal_deduction)
			- flt(settings.dependent_deduction) * dependents,
			0,
		)
		tax_amount, breakdown = pit.calculate(assessable_income, on_date)

	set_component_amount(doc, "deductions", const.PIT_COMPONENT, tax_amount)

	doc.taxable_income = taxable_income
	doc.assessable_income = assessable_income
	doc.dependent_count = dependents
	doc.pit_breakdown = json.dumps(breakdown, ensure_ascii=False)


def compute_non_taxable_earnings(doc, settings):
	"""Cơm ≤ trần miễn thuế; các earning khác được Salary Component đánh dấu
	`exempted_from_income_tax` (VD Phụ cấp điện thoại theo quy chế)."""
	total = 0
	exempted_components = {
		row.salary_component
		for row in doc.earnings
		if frappe.get_cached_value("Salary Component", row.salary_component, "exempted_from_income_tax")
	}
	for row in doc.earnings:
		if row.salary_component == const.MEAL_ALLOWANCE_COMPONENT:
			total += min(flt(row.amount), flt(settings.meal_allowance_exemption_cap))
		elif row.salary_component in exempted_components:
			total += flt(row.amount)
	# ⚠️ Phase 1: phần tăng ca vượt hệ số 100% (150/200/300%) được miễn thuế
	# theo luật, nhưng cần breakdown giờ OT theo từng hệ số (Overtime Request
	# — Phase 3) để tách phần miễn/chịu thuế chính xác. Tạm coi toàn bộ
	# "Tăng ca" là thu nhập chịu thuế cho tới khi Phase 3 cung cấp dữ liệu
	# chi tiết — CẦN clarify với khách nếu cần áp dụng ngay ở Phase 1.
	return total


def get_probation_flat_tax_rule(employee, on_date):
	# ⚠️ Phase 1 tạm dùng Employee.employment_type == "Probation" (Employment
	# Type có sẵn của Frappe HR) + contract_end_date/date_of_joining < 3
	# tháng để nhận diện thử việc/HĐ ngắn hạn, do Labor Contract (Phase 2,
	# có contract_type rõ "Thử việc"/"Xác định thời hạn") chưa tồn tại. Sẽ
	# chuyển sang query Labor Contract.contract_type khi Phase 2 triển khai.
	is_probation = employee.get("employment_type") == "Probation"

	is_short_term = False
	contract_end_date = employee.get("contract_end_date")
	date_of_joining = employee.get("date_of_joining")
	if contract_end_date and date_of_joining:
		is_short_term = month_diff(getdate(contract_end_date), getdate(date_of_joining)) < 3

	if not (is_probation or is_short_term):
		return None
	return const.get_probation_flat_tax(on_date)


def count_active_dependents(employee, period_start_date):
	period_start_date = getdate(period_start_date)
	rows = frappe.get_all(
		"Dependent",
		filters={"employee": employee, "deduction_from": ["<=", period_start_date]},
		fields=["deduction_to"],
	)
	return sum(1 for row in rows if not row.deduction_to or getdate(row.deduction_to) >= period_start_date)


# ---------------------------------------------------------------------------
# Bước 9: Đoàn phí / kinh phí công đoàn
# ---------------------------------------------------------------------------


def apply_union_dues(doc, employee, settings, insurance_salary):
	union_fee = 0
	if employee.union_member:
		union_fee = round_vnd(insurance_salary * flt(settings.union_fee_percent) / 100)
		if flt(settings.union_fee_monthly_cap):
			union_fee = min(union_fee, flt(settings.union_fee_monthly_cap))
	set_component_amount(doc, "deductions", const.UNION_FEE_COMPONENT, union_fee)

	union_funding = round_vnd(insurance_salary * flt(settings.union_funding_percent) / 100)
	set_component_amount(doc, "deductions", const.UNION_FUNDING_COMPONENT, union_funding, statistical=True)


# ---------------------------------------------------------------------------
# Bước 8: NET → GROSS (vòng lặp hội tụ)
# ---------------------------------------------------------------------------


def solve_net_to_gross(doc, employee, settings, insurance_salary, target_net, on_date):
	"""Giải ngược "Lương cơ bản" sao cho net_pay của Salary Slip == target_net.

	Các earning khác (phụ cấp...) và insurance_salary giữ cố định; chỉ
	"Lương cơ bản" (gross) được điều chỉnh. Hội tụ nhanh vì thuế TNCN là
	hàm đơn điệu tăng theo gross — sai số < 1 đồng, tối đa 20 vòng."""
	other_earnings = sum(
		flt(row.amount) for row in doc.earnings if row.salary_component != const.BASIC_SALARY_COMPONENT
	)

	def net_from_basic(basic_amount):
		set_component_amount(doc, "earnings", const.BASIC_SALARY_COMPONENT, basic_amount)
		# Không dùng depends_on_payment_days=1: amount trong doc.earnings đã
		# là số tiền cuối cùng cần trả (đã prorate ở nơi khác nếu cần), engine
		# không tự nhân lại theo payment_days/total_working_days.
		doc.gross_pay = doc.get_component_totals("earnings")
		apply_social_insurance(doc, employee, settings, insurance_salary, on_date)
		apply_income_tax(doc, employee, settings, insurance_salary, on_date)
		apply_union_dues(doc, employee, settings, insurance_salary)
		total_deduction = doc.get_component_totals("deductions")
		return doc.gross_pay - total_deduction

	guess = target_net - other_earnings
	for _iteration in range(MAX_NET_TO_GROSS_ITERATIONS):
		net = net_from_basic(guess)
		diff = target_net - net
		if abs(diff) < NET_TO_GROSS_TOLERANCE:
			break
		guess += diff
	# Vòng lặp cuối (break hoặc hết MAX_NET_TO_GROSS_ITERATIONS) đã để lại
	# doc.earnings/deductions/gross_pay khớp với "Lương cơ bản" = guess.


# ---------------------------------------------------------------------------
# Tiện ích chung
# ---------------------------------------------------------------------------


def round_vnd(amount):
	return const.round_vnd(amount)


def set_component_amount(doc, table_name, component_name, amount, statistical=False):
	rows = [row for row in doc.get(table_name) if row.salary_component == component_name]
	if rows:
		rows[0].amount = amount
		if statistical:
			rows[0].statistical_component = 1
			rows[0].do_not_include_in_total = 1
	else:
		row = doc.append(table_name, {"salary_component": component_name, "amount": amount})
		if statistical:
			row.statistical_component = 1
			row.do_not_include_in_total = 1
