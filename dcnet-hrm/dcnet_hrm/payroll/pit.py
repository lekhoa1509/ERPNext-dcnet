"""Thuế TNCN lũy tiến từng phần (7 bậc).

Tính bằng cách cộng dồn qua từng bậc — kết quả tương đương với "công thức
rút gọn" (bảng trừ nhanh) hay dùng trong thực tế, nhưng tránh phải khai báo
2 bảng số liệu (đầy đủ + rút gọn) dễ lệch nhau khi luật thay đổi. Hàm trả
kèm breakdown theo từng bậc để lưu vào Salary Slip.pit_breakdown.
"""

from dcnet_hrm.constants import get_pit_brackets, round_vnd


def calculate(assessable_income, on_date):
	"""Thuế TNCN theo kỳ lương (tháng). assessable_income: thu nhập tính
	thuế (đã trừ BH bắt buộc + giảm trừ). Trả về (tax_amount, breakdown)."""
	return _walk_brackets(assessable_income, get_pit_brackets(on_date))


def calculate_annual(assessable_income_annual, on_date):
	"""Thuế TNCN quyết toán năm — biểu thuế năm = biểu thuế tháng × 12 theo
	từng bậc (Thông tư 111/2013/TT-BTC, Điều 7 khoản 2), thuế suất giữ
	nguyên. assessable_income_annual = tổng assessable_income các kỳ lương
	đã submit trong năm."""
	monthly_brackets = get_pit_brackets(on_date)
	annual_brackets = [
		(ceiling * 12 if ceiling is not None else None, rate_percent) for ceiling, rate_percent in monthly_brackets
	]
	return _walk_brackets(assessable_income_annual, annual_brackets)


def _walk_brackets(income, brackets):
	if income <= 0:
		return 0, []

	breakdown = []
	total_tax = 0.0
	prev_ceiling = 0
	remaining = income

	for ceiling, rate_percent in brackets:
		if remaining <= 0:
			break
		bracket_width = (ceiling - prev_ceiling) if ceiling is not None else remaining
		taxable_in_bracket = min(remaining, bracket_width)
		if taxable_in_bracket <= 0:
			prev_ceiling = ceiling if ceiling is not None else prev_ceiling
			continue

		bracket_tax = taxable_in_bracket * rate_percent / 100
		total_tax += bracket_tax
		breakdown.append(
			{
				"bracket_from": prev_ceiling,
				"bracket_to": ceiling,
				"rate_percent": rate_percent,
				"taxable_amount": round_vnd(taxable_in_bracket),
				"tax": round_vnd(bracket_tax),
			}
		)
		remaining -= taxable_in_bracket
		prev_ceiling = ceiling

	return round_vnd(total_tax), breakdown
