"""Hằng số pháp lý cho payroll VN.

Mọi hằng số ở đây có hiệu lực theo thời gian (danh sách sort theo
``effective_from`` tăng dần). Khi luật thay đổi, THÊM 1 entry mới với
``effective_from`` mới — KHÔNG sửa/xoá entry cũ (để tính lương lại các kỳ
trong quá khứ vẫn đúng luật tại thời điểm đó).

Các mức tiền có thể thay đổi thường xuyên hơn (giảm trừ gia cảnh, trần miễn
thuế tiền cơm, % đoàn phí...) được cấu hình qua DocType ``VN Payroll
Settings`` / ``Insurance Rate`` / ``Statutory Wage`` — KHÔNG đặt ở đây.
"""

from decimal import ROUND_HALF_UP, Decimal


def round_vnd(amount):
	"""VND không có phần thập phân — làm tròn đến đồng, half-up."""
	return int(Decimal(str(amount)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def get_effective(table, on_date):
	"""Trả về entry có `effective_from` mới nhất <= on_date."""
	on_date = str(on_date)
	candidates = [row for row in table if row["effective_from"] <= on_date]
	if not candidates:
		raise ValueError(f"Không tìm thấy hằng số có hiệu lực tại ngày {on_date}")
	return max(candidates, key=lambda row: row["effective_from"])


# Thuế TNCN lũy tiến từng phần — 7 bậc (Luật thuế TNCN 2007, sửa đổi 2012).
# Mỗi bậc: (mức thu nhập tính thuế tối đa của bậc, tính bằng đồng/tháng; None = không giới hạn), % thuế.
PIT_BRACKETS = [
	{
		"effective_from": "2009-01-01",
		"brackets": [
			(5_000_000, 5),
			(10_000_000, 10),
			(18_000_000, 15),
			(32_000_000, 20),
			(52_000_000, 25),
			(80_000_000, 30),
			(None, 35),
		],
	},
]

# Hệ số tăng ca theo Điều 98 BLLĐ 2019.
OVERTIME_MULTIPLIERS = [
	{
		"effective_from": "2019-01-01",
		"weekday": 1.5,
		"weekend": 2.0,
		"holiday": 3.0,
		"night_extra": 0.2,  # cộng thêm 20% nếu làm vào 22h-6h
	},
]

# Khung giờ làm việc ban đêm — Điều 106 BLLĐ 2019.
NIGHT_SHIFT_WINDOW = [
	{"effective_from": "2019-01-01", "start_hour": 22, "end_hour": 6},
]

# Khấu trừ thuế 10% flat cho HĐ < 3 tháng / thời vụ có thu nhập >= mức sàn mỗi lần trả
# (Thông tư 111/2013/TT-BTC, Điều 25 khoản 1 điểm i).
PROBATION_FLAT_TAX = [
	{"effective_from": "2013-01-01", "rate_percent": 10, "income_floor": 2_000_000},
]

# NLĐ nghỉ không lương >= số ngày này trong tháng thì KHÔNG đóng BHXH tháng đó
# (Luật BHXH 2014, Điều 85 khoản 3).
MIN_WORKING_DAYS_FOR_INSURANCE = [
	{"effective_from": "2016-01-01", "min_days": 14},
]


def get_pit_brackets(on_date):
	return get_effective(PIT_BRACKETS, on_date)["brackets"]


def get_overtime_multipliers(on_date):
	return get_effective(OVERTIME_MULTIPLIERS, on_date)


def get_night_shift_window(on_date):
	return get_effective(NIGHT_SHIFT_WINDOW, on_date)


def get_probation_flat_tax(on_date):
	return get_effective(PROBATION_FLAT_TAX, on_date)


def get_min_working_days_for_insurance(on_date):
	return get_effective(MIN_WORKING_DAYS_FOR_INSURANCE, on_date)["min_days"]


# Tên Salary Component — nguồn duy nhất, dùng chung bởi install.py (seed
# fixture) và payroll/vn_payroll.py (đọc/ghi amount) để tránh lệch tên.
EARNING_COMPONENTS = [
	"Lương cơ bản",
	"Phụ cấp cơm",
	"Phụ cấp điện thoại",
	"Phụ cấp xăng xe",
	"Tăng ca",
	"Lương tháng 13",
]

EMPLOYEE_INSURANCE_COMPONENTS = {
	"BHXH": "BHXH (NLĐ)",
	"BHYT": "BHYT (NLĐ)",
	"BHTN": "BHTN (NLĐ)",
}

EMPLOYER_INSURANCE_COMPONENTS = {
	"BHXH": "BHXH (DN)",
	"BHYT": "BHYT (DN)",
	"BHTN": "BHTN (DN)",
	"TNLĐ-BNN": "TNLĐ-BNN (DN)",
}

UNION_FEE_COMPONENT = "Đoàn phí công đoàn"
UNION_FUNDING_COMPONENT = "Kinh phí công đoàn (DN)"
PIT_COMPONENT = "Thuế TNCN"
MEAL_ALLOWANCE_COMPONENT = "Phụ cấp cơm"
PHONE_ALLOWANCE_COMPONENT = "Phụ cấp điện thoại"
OVERTIME_COMPONENT = "Tăng ca"
BASIC_SALARY_COMPONENT = "Lương cơ bản"

DEDUCTION_COMPONENTS = [
	*EMPLOYEE_INSURANCE_COMPONENTS.values(),
	UNION_FEE_COMPONENT,
	PIT_COMPONENT,
]

EMPLOYER_COMPONENTS = [
	*EMPLOYER_INSURANCE_COMPONENTS.values(),
	UNION_FUNDING_COMPONENT,
]
