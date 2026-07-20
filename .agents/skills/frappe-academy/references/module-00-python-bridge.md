# Module 0: Python Bridge cho Laravel/PHP Developer

> **Mục tiêu / Objective:** Chuyển đổi tư duy từ PHP/Laravel sang Python/Frappe — nắm chắc các điểm khác biệt trước khi vào framework.
> **Dành cho / For:** Developer có background PHP/Laravel, Python cơ bản
> **Thời lượng / Duration:** ~4 giờ thực hành
> **Lưu ý:** Module này là **optional** — nếu bạn đã thoải mái với Python, có thể bỏ qua và bắt đầu từ Module 1.

---

## L0.1: Python Syntax so với PHP/Laravel

### Tổng quan / Overview

Nếu bạn đến từ PHP/Laravel, Python sẽ không khó — cú pháp gọn hơn, ít dấu câu hơn. Bài này tập trung vào **những điểm khác biệt quan trọng** mà Frappe sử dụng nhiều, không phải dạy Python từ đầu.

### Bảng so sánh nhanh

| Khái niệm | PHP/Laravel | Python/Frappe |
|-----------|-------------|---------------|
| **Class** | `class Foo extends Bar` | `class Foo(Bar):` |
| **Method** | `public function doSomething()` | `def do_something(self):` |
| **Array** | `$arr = [1, 2, 3]` | `arr = [1, 2, 3]` |
| **Dict (HashMap)** | `$d = ['key' => 'value']` | `d = {'key': 'value'}` |
| **String interpolation** | `"Hello $name"` | `f"Hello {name}"` |
| **Null** | `null` | `None` |
| **This/Self** | `$this->field` | `self.field` |
| **Import** | `use App\Models\User;` | `from frappe.model import Document` |
| **Boolean** | `true` / `false` | `True` / `False` |
| **Ternary** | `$x ? $a : $b` | `a if x else b` |
| **Type check** | `$x instanceof Foo` | `isinstance(x, Foo)` |
| **Not equal** | `!==` | `!=` |

### Indentation thay dấu {}

Python dùng **indentation (thụt lề)** thay cho `{}`. Đây là điểm khác biệt lớn nhất:

```python
# PHP:
# if ($condition) {
#     doSomething();
# }

# Python:
if condition:
    do_something()   # 4 spaces indent — BẮT BUỘC nhất quán

# Controller trong Frappe:
class SalesOrder(Document):
    def validate(self):
        if not self.customer:
            frappe.throw("Customer is required")   # indent 2 level (8 spaces)
```

### String Formatting

```python
name = "Nguyễn Văn A"
amount = 150000

# f-string (Python 3.6+) — dùng phổ biến nhất trong Frappe
msg = f"Khách hàng {name} nợ {amount:,.0f} VND"

# .format() — cũ hơn nhưng vẫn gặp trong Frappe
msg = "Khách hàng {} nợ {} VND".format(name, amount)

# % formatting — rất cũ, tránh dùng
msg = "Khách hàng %s" % name
```

### None vs null

```python
# Kiểm tra None — dùng 'is None' không phải '== None'
if self.due_date is None:
    frappe.throw("Due date required")

# Cách Frappe hay gặp — Falsy check (None, "", 0, [] đều là falsy)
if not self.customer:
    frappe.throw("Customer required")
```

---

## L0.2: Tính năng Python mà Frappe dùng nhiều

### 1. Decorator (`@`)

Tương tự Annotation trong Java hoặc Attribute trong C#. Frappe dùng decorator rất nhiều:

```python
# @frappe.whitelist() — expose method thành API endpoint
@frappe.whitelist()
def get_customer_balance(customer):
    return frappe.db.get_value("Customer", customer, "outstanding_amount")


# @property — getter không cần gọi ()
class SalesOrder(Document):
    @property
    def is_overdue(self):
        return self.due_date < frappe.utils.today()

# Dùng: order.is_overdue  (không phải order.is_overdue())


# @staticmethod — method không cần instance
class PriceCalculator(Document):
    @staticmethod
    def calculate_vat(amount, rate=0.1):
        return amount * rate

# Dùng: PriceCalculator.calculate_vat(1000)


# @classmethod — factory method
class SalesOrder(Document):
    @classmethod
    def create_from_quotation(cls, quotation_name):
        q = frappe.get_doc("Quotation", quotation_name)
        return cls({"customer": q.customer, "items": q.items})
```

### 2. List Comprehension

Thay cho vòng lặp `array_map` / `array_filter` của PHP:

```python
# PHP: array_filter($items, fn($i) => $i['qty'] > 0)
# Python:
valid_items = [item for item in self.items if item.qty > 0]

# PHP: array_map(fn($i) => $i['amount'], $items)
# Python:
amounts = [item.amount for item in self.items]

# Kết hợp filter + map:
taxable = [item.amount for item in self.items if item.is_taxable]

# Dùng trong Frappe context:
overdue_orders = [
    d.name for d in frappe.db.get_list("Sales Order",
        filters={"due_date": ["<", frappe.utils.today()], "status": "Unpaid"},
        fields=["name"]
    )
]
```

### 3. Dictionary Unpacking (`**`)

```python
# Merge dicts — thay cho array_merge trong PHP
defaults = {"currency": "VND", "status": "Draft", "company": "DCNET"}
overrides = {"status": "Open", "customer": "CUST-001"}
merged = {**defaults, **overrides}
# → {"currency": "VND", "status": "Open", "company": "DCNET", "customer": "CUST-001"}

# Dùng phổ biến trong Frappe khi tạo document:
base_data = {
    "doctype": "Sales Order",
    "customer": customer_name,
    "company": frappe.defaults.get_user_default("Company"),
}
doc = frappe.get_doc({**base_data, **extra_fields})
doc.insert()
```

### 4. Context Manager (`with`)

```python
# Frappe dùng context manager cho transactions:
with frappe.db.savepoint():
    # Tất cả thao tác trong block này là 1 transaction
    doc1.save()
    doc2.save()
    # Nếu exception xảy ra → tự động rollback về savepoint

# Tương đương Laravel:
# DB::transaction(function() {
#     Model1::save(); Model2::save();
# });
```

### 5. Exception Handling

```python
# Frappe exceptions hay gặp:
try:
    doc = frappe.get_doc("Customer", customer_name)
    doc.save()
except frappe.DoesNotExistError:
    frappe.throw(f"Customer {customer_name} not found")
except frappe.ValidationError as e:
    frappe.log_error(str(e), "Validation Failed")
    raise
except Exception:
    frappe.log_error(frappe.get_traceback(), "Unexpected Error")
    frappe.throw("An unexpected error occurred")
finally:
    # Chạy dù có exception hay không
    cleanup()
```

### 6. Type Hints (Python 3.10+)

Frappe v16 hỗ trợ type hints — giúp IDE gợi ý và code rõ ràng hơn:

```python
def get_customer_data(customer_name: str) -> dict:
    return frappe.db.get_value(
        "Customer",
        customer_name,
        ["customer_name", "email_id", "mobile_no"],
        as_dict=True
    )

def process_items(items: list[dict]) -> float:
    return sum(item.get("amount", 0) for item in items)
```

---

## L0.3: Module & Package System

### Tổng quan / Overview

Python dùng hệ thống import khác Laravel. Hiểu điều này giúp bạn đọc Frappe source code và viết import đúng.

### Import trong Python vs PHP

```python
# PHP (Laravel):
# use App\Models\User;
# use Illuminate\Support\Facades\DB;

# Python — import tuyệt đối (absolute):
import frappe
from frappe.model.document import Document
from frappe.utils import today, now_datetime, getdate

# Import nhiều thứ từ 1 module:
from frappe.utils import (
    today,
    now_datetime,
    getdate,
    add_days,
    date_diff,
    flt,        # float conversion
    cint,       # int conversion
    cstr,       # string conversion
)
```

### Frappe Utility Functions hay dùng

```python
import frappe
from frappe.utils import (
    today,           # → "2026-03-19" (string)
    now_datetime,    # → datetime object
    getdate,         # "2026-03-19" → date object
    add_days,        # add_days("2026-03-19", 30) → "2026-04-18"
    date_diff,       # date_diff("2026-04-18", "2026-03-19") → 30
    flt,             # flt("1.5") → 1.5, flt(None) → 0.0
    cint,            # cint("3") → 3, cint(None) → 0
    cstr,            # cstr(None) → ""
    nowdate,         # alias của today()
    format_date,     # format_date("2026-03-19") → "19-03-2026"
)

# Ví dụ thực tế trong Frappe controller:
class SalesOrder(Document):
    def validate(self):
        if self.delivery_date:
            days_left = date_diff(self.delivery_date, today())
            if days_left < 0:
                frappe.throw("Delivery date cannot be in the past")

        self.total = flt(sum(flt(item.amount) for item in self.items), 2)
```

### `__init__.py` — Tương tự ServiceProvider

```python
# apps/myapp/myapp/__init__.py
# Thường để trống, hoặc khai báo version:
__version__ = "1.0.0"

# Frappe tự động import các module khi app được install
# Không cần đăng ký như ServiceProvider trong Laravel
```

### Tránh lỗi import hay gặp trong Frappe

```python
# ❌ SAI — Server Script KHÔNG được import
from frappe.utils import today   # → NameError: "from" is not allowed

# ✅ ĐÚNG — Dùng qua namespace
date = frappe.utils.today()

# ❌ SAI — Import ở đầu file Controller (circular import)
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder

# ✅ ĐÚNG — Import lazy bên trong function
def get_so():
    from erpnext.selling.doctype.sales_order.sales_order import SalesOrder
    return SalesOrder
```

---

## L0.4: Bảng Tương Đương Laravel ↔ Frappe

### Framework-level Equivalents

| Laravel | Frappe | Ghi chú |
|---------|--------|---------|
| `php artisan` | `bench` | CLI management tool |
| `php artisan make:model` | Tạo DocType qua UI | Model + Migration + Form |
| `php artisan migrate` | `bench migrate` | Schema sync |
| `php artisan serve` | `bench start` | Dev server |
| `php artisan tinker` | `bench console` | REPL |
| `php artisan schedule:run` | Tự động qua Supervisor | Scheduled tasks |
| `composer require X` | `bench get-app X` | Install package |
| `.env` | `site_config.json` | Environment config |
| `storage/` | `sites/{site}/private/` | Private files |
| `public/` | `sites/{site}/public/` | Public assets |

### Code-level Equivalents

| Laravel | Frappe | Ghi chú |
|---------|--------|---------|
| `Model::find('id')` | `frappe.get_doc("DocType", name)` | Get document |
| `DB::table()->where()->get()` | `frappe.db.get_list(...)` | List query |
| `DB::table()->value()` | `frappe.db.get_value(...)` | Single value |
| `Model::create([])` | `frappe.get_doc({...}).insert()` | Create record |
| `$model->save()` | `doc.save()` | Update record |
| `$model->delete()` | `frappe.delete_doc(...)` | Delete record |
| `Observer::creating()` | `before_insert()` controller hook | Create event |
| `Observer::saving()` | `before_save()` controller hook | Save event |
| `EventServiceProvider` | `hooks.py` | Event registration |
| `Middleware` | Permission hooks, `before_request` | Request middleware |
| `Policy` | Permission rules + `has_permission()` | Authorization |
| `Queue::push()` | `frappe.enqueue(...)` | Background job |
| `Cache::put()` | `frappe.cache().set_value()` | Cache |
| `Mail::send()` | `frappe.sendmail()` | Email |
| `Route::post()` | `@frappe.whitelist()` | API endpoint |
| `Resource::collection()` | REST API tự động | Auto-generated API |

---

## Mini Quiz

<details>
<summary><strong>Câu 1:</strong> Trong Python, để kiểm tra nếu một biến là None, bạn dùng gì? Tại sao không dùng <code>== None</code>?</summary>

**Trả lời:** Dùng `is None`. Lý do: `is` kiểm tra identity (cùng object trong bộ nhớ), còn `==` kiểm tra equality (có thể bị override bởi `__eq__`). Python convention là dùng `is None` / `is not None` cho singleton objects như None, True, False.
</details>

<details>
<summary><strong>Câu 2:</strong> Chuyển đổi PHP sang Python: <code>$items = array_filter($orders, fn($o) => $o['amount'] > 1000000);</code></summary>

**Trả lời:**
```python
items = [o for o in orders if o.get('amount', 0) > 1_000_000]
# hoặc nếu orders là list of Document objects:
items = [o for o in orders if o.amount > 1_000_000]
```
</details>

<details>
<summary><strong>Câu 3:</strong> Tại sao Server Script trong Frappe KHÔNG được dùng <code>from frappe.utils import today</code>?</summary>

**Trả lời:** Server Script chạy trong sandbox environment của Frappe (không phải module Python thông thường). Frappe inject các biến sẵn vào context (như `frappe`, `doc`) nhưng không hỗ trợ `import` statement. Thay vào đó dùng `frappe.utils.today()` — namespace đã có sẵn.
</details>

---

## Bài tập thực hành

### Bài 1: Python Rewrite

Viết lại đoạn PHP sau thành Python:

```php
// PHP
public function calculateDiscount($amount, $customerType) {
    $rate = $customerType === 'wholesale' ? 0.15 : 0.05;
    $discount = $amount * $rate;
    $items = array_filter($this->items, fn($i) => $i['price'] > 0);
    $total = array_sum(array_map(fn($i) => $i['price'] * $i['qty'], $items));
    return [
        'discount' => $discount,
        'total' => $total - $discount,
        'item_count' => count($items)
    ];
}
```

<details>
<summary>Xem đáp án</summary>

```python
def calculate_discount(self, amount: float, customer_type: str) -> dict:
    rate = 0.15 if customer_type == "wholesale" else 0.05
    discount = amount * rate
    valid_items = [i for i in self.items if i.price > 0]
    total = sum(i.price * i.qty for i in valid_items)
    return {
        "discount": discount,
        "total": total - discount,
        "item_count": len(valid_items)
    }
```
</details>

### Bài 2: Frappe Utils

Dùng `bench console` (hoặc System Console trong UI), chạy:

```python
import frappe
from frappe.utils import today, add_days, date_diff

# 1. In ngày hôm nay
print(today())

# 2. Tính ngày 30 ngày sau
future = add_days(today(), 30)
print(future)

# 3. Tính số ngày giữa 2 ngày
diff = date_diff(future, today())
print(f"30 days later: {future} ({diff} days from now)")

# 4. Test flt và cint
print(flt("1.99999", 2))   # → 2.0 (rounded to 2 decimals)
print(cint("3.7"))          # → 3 (truncated to int)
print(cstr(None))           # → "" (not "None")
```

Kết quả mong đợi:
```
2026-03-19
2026-04-18
30 days later: 2026-04-18 (30 days from now)
2.0
3

```

**Lưu ý:** `from frappe.utils import flt, cint, cstr` đã được import tự động trong `bench console`.

### Bài 3: Viết Python Class

Tạo file `/tmp/price_calculator.py` và viết:

```python
from frappe.utils import flt, cint


class PriceCalculator:
    """Calculator dùng pattern của Frappe controllers"""

    TAX_RATE = 0.1  # 10% VAT

    def __init__(self, items: list):
        self.items = items

    @property
    def subtotal(self) -> float:
        """Tổng trước thuế"""
        return flt(sum(
            flt(item.get("price", 0)) * cint(item.get("qty", 1))
            for item in self.items
            if item.get("price", 0) > 0
        ), 2)

    @property
    def tax_amount(self) -> float:
        return flt(self.subtotal * self.TAX_RATE, 2)

    @property
    def total(self) -> float:
        return flt(self.subtotal + self.tax_amount, 2)

    def get_summary(self) -> dict:
        return {
            "subtotal": self.subtotal,
            "tax": self.tax_amount,
            "total": self.total,
            "item_count": len([i for i in self.items if i.get("qty", 0) > 0])
        }


# Test
items = [
    {"name": "Vợt cầu lông", "price": 500_000, "qty": 2},
    {"name": "Quần thể thao", "price": 300_000, "qty": 3},
    {"name": "Bóng", "price": 0, "qty": 5},  # Bị loại (price = 0)
]

calc = PriceCalculator(items)
print(calc.get_summary())
# → {'subtotal': 1900000.0, 'tax': 190000.0, 'total': 2090000.0, 'item_count': 2}
```

Chạy trong bench console:
```python
exec(open('/tmp/price_calculator.py').read())
```

---

**NEXT:** Tiếp theo là [Module 1: Frappe Foundation](module-01-foundation.md) — bắt đầu với kiến trúc hệ thống và Bench CLI.
