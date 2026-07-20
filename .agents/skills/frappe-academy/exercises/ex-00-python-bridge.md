# Exercises — Module 0: Python Bridge

> **Mục tiêu:** Thực hành Python ở mức đủ dùng cho Frappe development.
> **Môi trường:** `bench console` hoặc `System Console` trong Frappe UI.

---

## Bài 1: Syntax Conversion (PHP → Python)

Chuyển đổi đoạn code PHP sau sang Python. Không cần framework — pure Python:

```php
<?php
class OrderProcessor {
    private $orders = [];
    private $discount_rate = 0.1;

    public function __construct(array $orders) {
        $this->orders = $orders;
    }

    public function getActiveOrders(): array {
        return array_filter($this->orders, fn($o) => $o['status'] === 'active');
    }

    public function getTotalRevenue(): float {
        $active = $this->getActiveOrders();
        return array_sum(array_map(fn($o) => $o['amount'] * (1 - $this->discount_rate), $active));
    }

    public function getSummary(): array {
        return [
            'total_orders' => count($this->orders),
            'active_orders' => count($this->getActiveOrders()),
            'revenue' => $this->getTotalRevenue(),
        ];
    }
}

$orders = [
    ['id' => 1, 'status' => 'active', 'amount' => 500000],
    ['id' => 2, 'status' => 'cancelled', 'amount' => 300000],
    ['id' => 3, 'status' => 'active', 'amount' => 750000],
];

$processor = new OrderProcessor($orders);
print_r($processor->getSummary());
```

**Kết quả mong đợi:**
```
{'total_orders': 3, 'active_orders': 2, 'revenue': 1125000.0}
```

<details>
<summary>Xem đáp án</summary>

```python
class OrderProcessor:
    discount_rate = 0.1

    def __init__(self, orders: list):
        self.orders = orders

    def get_active_orders(self) -> list:
        return [o for o in self.orders if o['status'] == 'active']

    def get_total_revenue(self) -> float:
        return sum(
            o['amount'] * (1 - self.discount_rate)
            for o in self.get_active_orders()
        )

    def get_summary(self) -> dict:
        return {
            'total_orders': len(self.orders),
            'active_orders': len(self.get_active_orders()),
            'revenue': self.get_total_revenue(),
        }


orders = [
    {'id': 1, 'status': 'active', 'amount': 500_000},
    {'id': 2, 'status': 'cancelled', 'amount': 300_000},
    {'id': 3, 'status': 'active', 'amount': 750_000},
]

processor = OrderProcessor(orders)
print(processor.get_summary())
```
</details>

---

## Bài 2: Frappe Utilities Practice

Chạy trong `bench console` (hoặc System Console):

```python
# Paste từng phần và xem kết quả

# 1. Date utilities
from frappe.utils import today, add_days, date_diff, getdate, format_date

d = today()
print(f"Today: {d}")
print(f"30 days later: {add_days(d, 30)}")
print(f"Days until year end: {date_diff('2026-12-31', d)}")
print(f"Formatted: {format_date(d)}")   # Vietnamese format

# 2. Type conversion utilities
from frappe.utils import flt, cint, cstr

print(flt("1.99999", 2))    # Expect: 2.0
print(flt(None))             # Expect: 0.0
print(cint("3.7"))           # Expect: 3
print(cint(None))            # Expect: 0
print(repr(cstr(None)))      # Expect: ''
print(repr(cstr(0)))         # Expect: '0'

# 3. User & Session
print(frappe.session.user)
print(frappe.get_roles(frappe.session.user))
```

**Kết quả mong đợi (ví dụ):**
```
Today: 2026-03-19
30 days later: 2026-04-18
Days until year end: 287
Formatted: 03-19-2026
2.0
0.0
3
0
''
'0'
Administrator
['System Manager', 'Administrator', ...]
```

---

## Bài 3: Dictionary Manipulation

Frappe dùng dict rất nhiều — master pattern này:

```python
# Chạy trong bench console

# 1. Merge configs
defaults = {
    "currency": "VND",
    "company": "Nhật Minh Sport",
    "status": "Draft",
    "tax_rate": 0.1
}
user_input = {
    "customer": "CUST-0001",
    "status": "Submitted",   # Override default
    "amount": 1_500_000
}
merged = {**defaults, **user_input}
print(merged)
# Expect: currency=VND, company=Nhật Minh, status=Submitted, tax_rate=0.1, customer=CUST-0001, amount=1500000

# 2. List comprehension với dict
items = [
    {"name": "Vợt", "price": 500_000, "qty": 2, "taxable": True},
    {"name": "Quần", "price": 300_000, "qty": 1, "taxable": True},
    {"name": "Thẻ thành viên", "price": 200_000, "qty": 1, "taxable": False},
]

taxable_total = sum(i["price"] * i["qty"] for i in items if i["taxable"])
print(f"Taxable total: {taxable_total:,.0f} VND")   # Expect: 1,300,000 VND

item_names = [i["name"] for i in items if i["qty"] > 0]
print(item_names)   # Expect: ['Vợt', 'Quần', 'Thẻ thành viên']

# 3. Get với default (tránh KeyError)
item = {"name": "Vợt", "price": 500_000}
discount = item.get("discount", 0)     # → 0 (không có key "discount")
category = item.get("category")         # → None
print(f"Discount: {discount}, Category: {category}")
```

---

## Bài 4: Exception Handling Frappe-style

Viết function xử lý exception theo pattern của Frappe:

```python
# Chạy trong bench console

def safe_get_customer(customer_name: str) -> dict | None:
    """
    Lấy thông tin customer, xử lý exception đúng cách.
    Return dict nếu thành công, None nếu không tìm thấy.
    """
    try:
        doc = frappe.get_doc("Customer", customer_name)
        return {
            "name": doc.name,
            "customer_name": doc.customer_name,
            "customer_type": doc.customer_type,
        }
    except frappe.DoesNotExistError:
        return None
    except Exception:
        frappe.log_error(frappe.get_traceback(), f"Error fetching customer {customer_name}")
        return None


# Test
result = safe_get_customer("NON-EXISTENT-CUST")
print(f"Non-existent: {result}")   # → None

# Test với customer thật (thay bằng tên customer thật trong site của bạn)
result = safe_get_customer("Administrator")   # Thường không có, chỉ để test
print(f"Result: {result}")
```

---

## Bài 5: Decorator Pattern

Hiểu cách `@frappe.whitelist()` hoạt động — quan trọng cho Module 5:

```python
# Chạy trong bench console để hiểu decorator

# Decorator là "wrapper function"
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Before calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"After calling {func.__name__}")
        return result
    return wrapper

@my_decorator
def say_hello(name):
    print(f"Hello, {name}!")
    return f"Greeted {name}"

result = say_hello("Frappe")
print(f"Return: {result}")

# Kết quả:
# Before calling say_hello
# Hello, Frappe!
# After calling say_hello
# Return: Greeted Frappe

# Tương tự, @frappe.whitelist() wrap function để:
# 1. Check authentication
# 2. Xử lý JSON serialization của args
# 3. Return response theo Frappe format
```

---

## Checklist hoàn thành

```
[ ] Bài 1: Chuyển PHP → Python thành công, output đúng
[ ] Bài 2: Chạy Frappe utilities, hiểu flt/cint/cstr
[ ] Bài 3: Thành thạo dict manipulation và list comprehension
[ ] Bài 4: Viết exception handling Frappe-style
[ ] Bài 5: Hiểu cơ chế decorator
```

**NEXT:** Sẵn sàng cho [Module 1: Frappe Foundation](../references/module-01-foundation.md)!
