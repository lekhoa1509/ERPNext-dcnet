"""Tính BHXH / BHYT / BHTN / TNLĐ-BNN cho 1 kỳ lương.

Trần đóng:
- BHXH, BHYT, TNLĐ-BNN: 20 × lương cơ sở (Statutory Wage.base_salary).
- BHTN: 20 × lương tối thiểu vùng của NV (Statutory Wage.region_{1..4},
  chọn theo Employee.minimum_wage_region).
"""

import frappe
from frappe.utils import flt

from dcnet_hrm.constants import round_vnd

REGION_FIELD = {
	"Region I": "region_1",
	"Region II": "region_2",
	"Region III": "region_3",
	"Region IV": "region_4",
}

# Chỉ những loại BH này bị ràng buộc trần theo lương tối thiểu vùng (BHTN);
# các loại còn lại dùng trần theo lương cơ sở.
REGION_CAPPED_TYPES = {"BHTN"}

# Employee.insurance_status → các loại BH được đóng.
INSURANCE_STATUS_TYPES = {
	"Fully Insured": {"BHXH", "BHYT", "BHTN", "TNLĐ-BNN"},
	"Health Insurance Only": {"BHYT"},
	"Not Insured": set(),
}


def get_effective_row(doctype, on_date):
	name = frappe.db.get_value(doctype, {"effective_from": ["<=", on_date]}, "name", order_by="effective_from desc")
	if not name:
		frappe.throw(
			frappe._("No effective {0} record found for date {1}. Please set up the data.").format(
				doctype, on_date
			)
		)
	return frappe.get_doc(doctype, name)


def get_caps(statutory_wage, minimum_wage_region):
	base_cap = 20 * flt(statutory_wage.base_salary)
	region_field = REGION_FIELD.get(minimum_wage_region)
	region_wage = flt(statutory_wage.get(region_field)) if region_field else 0
	unemployment_cap = 20 * region_wage
	return {"default": base_cap, "BHTN": unemployment_cap}


def calculate(insurance_salary, insurance_status, minimum_wage_region, on_date):
	"""Trả về dict: {insurance_type: {employee, employer, capped_salary}}, và
	tổng `employee_total` / `employer_total` để vn_payroll.py dùng tiếp."""
	allowed_types = INSURANCE_STATUS_TYPES.get(insurance_status, set())
	if not allowed_types:
		return {"types": {}, "employee_total": 0, "employer_total": 0, "capped_insurance_salary": 0}

	insurance_rate = get_effective_row("Insurance Rate", on_date)
	statutory_wage = get_effective_row("Statutory Wage", on_date)
	caps = get_caps(statutory_wage, minimum_wage_region)

	types = {}
	employee_total = 0
	employer_total = 0
	max_capped_salary = 0

	for rate in insurance_rate.rates:
		if rate.insurance_type not in allowed_types:
			continue
		cap = caps["BHTN"] if rate.insurance_type in REGION_CAPPED_TYPES else caps["default"]
		capped_salary = min(flt(insurance_salary), cap) if cap else flt(insurance_salary)
		employee_amount = round_vnd(capped_salary * flt(rate.employee_percent) / 100)
		employer_amount = round_vnd(capped_salary * flt(rate.employer_percent) / 100)
		types[rate.insurance_type] = {
			"employee": employee_amount,
			"employer": employer_amount,
			"capped_salary": capped_salary,
		}
		employee_total += employee_amount
		employer_total += employer_amount
		max_capped_salary = max(max_capped_salary, capped_salary)

	return {
		"types": types,
		"employee_total": employee_total,
		"employer_total": employer_total,
		# BHXH/BHYT dùng cùng trần (lương cơ sở) nên capped_salary bằng nhau;
		# lấy max để hiển thị 1 số duy nhất lên Salary Slip.capped_insurance_salary.
		"capped_insurance_salary": max_capped_salary,
	}
