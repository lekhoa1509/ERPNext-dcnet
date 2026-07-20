# Module 4: Controllers & Hooks

> **Mục tiêu:** Viết Controllers chuyên nghiệp — hiểu full lifecycle, patterns, hooks.py deep dive, và scheduled jobs. Đây là cach "dùng" để viết business logic trong Frappe apps.
> **Thời lượng:** 5 lessons | **Độ khó:** Intermediate-Advanced
> **Yêu cầu:** Hoàn thành Module 3, hiểu su khác biết giua Server Script và Controller

---

## L4.1: Controller Lifecycle

### Tổng quan
Controller là Python class kế thừa `frappe.model.document.Document`, định nghĩa business logic cho 1 DocType. Mỗi thao tác trên document (tạo, sửa, submit, xóa) deu di qua chuỗi lifecycle methods có thứ tự nghiêm ngặt. Hiểu rõ lifecycle là nền tảng để biết đặt code ở đầu cho dùng.

### Key Concepts

#### 1. Full Lifecycle — Thứ tự gọi

```
=== INSERT (tao document moi) ===

__init__()              # Khoi tao Python object
  │
  ▼
before_validate()       # Truoc validation (hiem dung)
  │
  ▼
validate()              # ⭐ DUNG NHIEU NHAT — validate + transform data
  │                     #    Co the thay doi doc.field → se duoc luu
  ▼
before_save()           # Truoc save — cuoi cung co the thay doi data
  │
  ▼
before_insert()         # Chi chay khi INSERT (khong chay khi update)
  │
  ▼
  ════════ DATABASE INSERT ════════
  │
  ▼
after_insert()          # Sau insert — doc da co name
  │                     #    Tot cho: tao linked docs, send notifications
  ▼
on_update()             # ⭐ Sau moi save (insert + update)
  │                     #    ⚠️ KHONG modify doc.field o day
  ▼
on_change()             # Sau on_update — cho realtime updates
  │
  ▼
after_save()            # Cuoi cung sau save


=== UPDATE (sua document) ===

validate()  →  before_save()  →  DB UPDATE  →  on_update()  →  on_change()  →  after_save()
(Khong co before_insert, after_insert)


=== SUBMIT (cho Submittable DocTypes) ===

before_validate()
  │
  ▼
validate()              # Validate lai truoc submit
  │
  ▼
before_save()
  │
  ▼
before_submit()         # ⭐ Validation dac biet cho submit
  │                     #    VD: check stock availability
  ▼
  ════════ DB UPDATE (docstatus=1) ════════
  │
  ▼
on_submit()             # ⭐ QUAN TRONG — side effects khi submit
  │                     #    VD: create GL entries, update stock
  ▼
on_update()
  │
  ▼
on_change()
  │
  ▼
after_save()


=== CANCEL ===

before_cancel()         # Validate truoc cancel
  │                     #    VD: check linked submitted docs
  ▼
  ════════ DB UPDATE (docstatus=2) ════════
  │
  ▼
on_cancel()             # ⭐ Reverse effects cua on_submit
  │                     #    VD: reverse GL entries, restore stock
  ▼
on_update()
  │
  ▼
on_change()


=== DELETE ===

on_trash()              # Truoc xoa — cleanup linked data
  │
  ▼
  ════════ DATABASE DELETE ════════
  │
  ▼
after_delete()          # Sau xoa
```

#### 2. Khi nào dùng method nao?

| Method | Timing | Modify đọc? | Use case |
|--------|--------|:-----------:|----------|
| `validate()` | Trước save | YES | Validate rules, calculate fields, transform data |
| `before_save()` | Trước DB write | YES | Last-minute changes |
| `before_insert()` | Chi insert | YES | Set defaults cho new đọc |
| `after_insert()` | Sau insert | NO* | Tạo linked docs, send welcome email |
| `on_update()` | Sau mọi save | NO* | Log changes, clear cache, sync |
| `before_submit()` | Trước submit | YES | Final validation (stock check, credit limit) |
| `on_submit()` | Sau submit | NO* | Create GL entries, stock entries, notifications |
| `before_cancel()` | Trước cancel | YES | Check if can cancel |
| `on_cancel()` | Sau cancel | NO* | Reverse GL entries, restore stock |
| `on_trash()` | Trước delete | NO | Cleanup references |

> *NO = thay đổi `self.field` không có tác dụng (đã save rồi). Dùng `frappe.db.set_value()` nếu can.

#### 3. Controller File Structure

```python
# frappe_learn/library/doctype/library_book/library_book.py

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, add_days, getdate, date_diff


class LibraryBook(Document):
    # === VALIDATION ===
    def validate(self):
        self.validate_isbn()
        self.set_title_case()

    def validate_isbn(self):
        """Validate ISBN-13 format"""
        if not self.isbn:
            return

        isbn_clean = self.isbn.replace("-", "")
        if len(isbn_clean) != 13 or not isbn_clean.isdigit():
            frappe.throw("ISBN must be 13 digits")

        # Normalize
        self.isbn = isbn_clean

    def set_title_case(self):
        """Auto-capitalize title"""
        if self.title:
            self.title = self.title.title()

    # === LIFECYCLE ===
    def after_insert(self):
        """Log new book creation"""
        frappe.msgprint(f"Book '{self.title}' added to library")

    def on_update(self):
        """Clear cache when book changes"""
        frappe.cache.hdel("library_stats", "total_books")

    def on_trash(self):
        """Check if book is borrowed before delete"""
        if self.status == "Borrowed":
            frappe.throw("Cannot delete a borrowed book. Return it first.")
```

### Code Examples

```python
# Debug lifecycle — thêm print để thay thứ tự gọi

class LibraryBook(Document):
    def before_validate(self):
        print(f">>> before_validate: {self.name or 'NEW'}")

    def validate(self):
        print(f">>> validate: {self.name or 'NEW'}")

    def before_save(self):
        print(f">>> before_save: {self.name or 'NEW'}")

    def before_insert(self):
        print(f">>> before_insert (only for new docs)")

    def after_insert(self):
        print(f">>> after_insert: {self.name}")

    def on_update(self):
        print(f">>> on_update: {self.name}")

    def on_change(self):
        print(f">>> on_change: {self.name}")

    def after_save(self):
        print(f">>> after_save: {self.name}")
```

```bash
# Test trong console:
bench --site flow.local console
```

```python
# Tạo document mới → xem lifecycle order
doc = frappe.get_doc({
    "doctype": "Library Book",
    "title": "test lifecycle",
    "author": "Test"
})
doc.insert()
# Output:
# >>> before_validate: NEW
# >>> validate: NEW
# >>> before_save: NEW
# >>> before_insert (only for new docs)
# >>> after_insert: BOOK-0042
# >>> on_update: BOOK-0042
# >>> on_change: BOOK-0042
# >>> after_save: BOOK-0042

# Update document → xem lifecycle order
doc.author = "Updated Author"
doc.save()
# Output:
# >>> before_validate: BOOK-0042
# >>> validate: BOOK-0042
# >>> before_save: BOOK-0042
# (KHÔNG có before_insert, after_insert)
# >>> on_update: BOOK-0042
# >>> on_change: BOOK-0042
# >>> after_save: BOOK-0042
```

### Mini Quiz

<details>
<summary>Q1: Bạn muốn validate rang "quantity must be > 0" trước khi save. Đặt code ở method nao?</summary>

**A:** `validate()`. Đây là method chuyen dùng cho validation — chạy trước mọi save (ca insert và update), có thể thay đổi đọc fields, và `frappe.throw()` sẽ cancel save.
</details>

<details>
<summary>Q2: Bạn muốn tạo Payment Entry tự động khi Sales Invoice submit. Đặt code ở method nao?</summary>

**A:** `on_submit()`. Đây là method chạy SAU KHI document đã submit thành cong (docstatus=1). Thich hop cho side effects nhu tạo linked documents, GL entries, stock entries. Lưu ý: dùng `frappe.get_doc({...}).insert().submit()` để tạo và submit linked đọc.
</details>

<details>
<summary>Q3: Tại sao `self.status = "Closed"` trong `on_update()` KHÔNG được lưu?</summary>

**A:** Vì `on_update()` chạy SAU KHI DB UPDATE. Document đã lưu vao database rồi — thay đổi `self.field` chi ảnh hưởng Python object trong memory. 2 cach fix: (1) Đặt logic trong `validate()` — chạy TRƯỚC save, (2) Dùng `frappe.db.set_value(self.doctype, self.name, "status", "Closed")` — update trực tiếp DB.
</details>

### Skill References

- **DEEP DIVE:** Xem skill `dcnet_quality` -> `syntax/erpnext-syntax-controllers/` cho FULL controller coding rules
- **DEEP DIVE:** Xem skill `erpnext` để hiểu cach ERPNext controllers (Sales Order, Purchase Invoice, etc.) su dùng lifecycle

---

## L4.2: Controller Patterns

### Tổng quan
Viết controller tot không chi là biết lifecycle — con là biết patterns: class inheritance, su dùng `super()` dùng cach, `flags` để control behavior, và `run_method()`. Bài này day nhưng patterns chuyên nghiệp từ ERPNext codebase.

### Key Concepts

#### 1. Class Inheritance

```python
# ERPNext dùng inheritance để chia sẻ logic giua các DocTypes

# Base class cho tất cả transaction documents
# erpnext/controllers/accounts_controller.py
class AccountsController(TransactionBase):
    def validate(self):
        super().validate()  # Goi parent validate
        self.validate_currency()
        self.validate_party()
        self.set_missing_values()

# Sales Invoice kế thừa AccountsController
# erpnext/accounts/doctype/sales_invoice/sales_invoice.py
class SalesInvoice(AccountsController):
    def validate(self):
        super().validate()  # Goi AccountsController.validate()
        self.validate_items()
        self.validate_warehouse()
```

```
Inheritance chain cua Sales Invoice:
Document → TransactionBase → AccountsController → SellingController → SalesInvoice

Moi class them validation/logic rieng, goi super() de chain lại.
```

#### 2. super() — Gọi Parent Method

```python
class LibraryTransaction(Document):
    def validate(self):
        # ⚠️ LUON gọi super() đầu tiên (tru khi có ly do đặc biệt)
        super().validate()

        # Sau do thêm logic của minh
        self.validate_member_status()
        self.validate_book_availability()
        self.calculate_due_dates()

    def on_submit(self):
        super().on_submit()
        self.update_book_status()
        self.create_log_entry()

    def on_cancel(self):
        super().on_cancel()
        self.reverse_book_status()
```

#### 3. flags — Control Behavior

```python
# flags là dict gan vao đọc để control behavior nơi bo

class LibraryTransaction(Document):
    def validate(self):
        if not self.flags.ignore_validate:
            self.validate_member_status()

    def on_update(self):
        if not self.flags.ignore_notification:
            self.send_notification()

# Su dùng flags:
doc = frappe.get_doc("Library Transaction", "LT-001")
doc.flags.ignore_validate = True       # Skip validation
doc.flags.ignore_notification = True   # Skip notification
doc.save()

# Flags phổ biến trong ERPNext:
doc.flags.ignore_permissions = True    # Skip permission check
doc.flags.ignore_mandatory = True      # Skip required field check
doc.flags.ignore_links = True          # Skip link validation
doc.flags.ignore_validate = True       # Skip validate()
```

#### 4. run_method() — Gọi Method ẩn toàn

```python
# run_method gọi method nếu tồn tại, bo qua nếu không
doc.run_method("custom_validate")
# Tuong duong với:
if hasattr(doc, "custom_validate"):
    doc.custom_validate()

# Huu ich cho plugin/extension pattern
```

#### 5. Common Patterns từ ERPNext

```python
# Pattern 1: Validate + Set missing values
class LibraryTransaction(Document):
    def validate(self):
        self.set_missing_values()       # Set defaults truoc
        self.validate_mandatory()       # Roi validate
        self.calculate_totals()         # Roi calculate

    def set_missing_values(self):
        if not self.transaction_date:
            self.transaction_date = frappe.utils.nowdate()

        for item in self.items:
            if not item.due_date:
                item.due_date = frappe.utils.add_days(
                    self.transaction_date, 14
                )

# Pattern 2: Status updater
class LibraryTransaction(Document):
    def set_status(self, status=None):
        """Update status based on conditions"""
        if status:
            self.db_set("status", status)
            return

        if self.docstatus == 2:
            self.db_set("status", "Cancelled")
        elif self.docstatus == 1:
            if all(item.status == "Returned" for item in self.items):
                self.db_set("status", "Completed")
            else:
                self.db_set("status", "Active")
        else:
            self.db_set("status", "Draft")

# Pattern 3: Permission check trong method
class LibraryTransaction(Document):
    @frappe.whitelist()
    def return_books(self):
        """Called from client via frm.call('return_books')"""
        # ⚠️ self method được gọi qua frappe.call phải có @frappe.whitelist()
        self.check_permission("write")  # Explicit permission check

        for item in self.items:
            if item.status != "Returned":
                item.db_set("status", "Returned")
                item.db_set("return_date", frappe.utils.nowdate())
                frappe.db.set_value("Library Book", item.book, "status", "Available")

        self.set_status()
        self.notify_member()

# Pattern 4: db_set vs set_value
class LibraryBook(Document):
    def on_update(self):
        # db_set — update field của CHINH document này
        self.db_set("last_checked", frappe.utils.nowdate())
        # Tuong duong: frappe.db.set_value("Library Book", self.name, "last_checked", ...)

        # set_value — update field của document KHAC
        frappe.db.set_value("Library Member", self.current_borrower,
            "last_activity", frappe.utils.nowdate())
```

### Code Examples

```python
# Full controller cho Library Transaction
# frappe_learn/library/doctype/library_transaction/library_transaction.py

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, add_days, getdate, date_diff


class LibraryTransaction(Document):
    def validate(self):
        """Validate before save"""
        super().validate()
        self.set_missing_values()
        self.validate_member()
        self.validate_books()
        self.calculate_totals()

    def set_missing_values(self):
        """Set defaults for empty fields"""
        if not self.transaction_date:
            self.transaction_date = nowdate()

        for item in self.items:
            if not item.due_date and self.transaction_type == "Borrow":
                item.due_date = add_days(self.transaction_date, 14)

            if not item.status:
                item.status = "Borrowed" if self.transaction_type == "Borrow" else "Returned"

    def validate_member(self):
        """Check member eligibility"""
        member = frappe.get_doc("Library Member", self.member)

        if member.status != "Active":
            frappe.throw(
                f"Member {member.full_name} is {member.status}. "
                "Only Active members can create transactions."
            )

    def validate_books(self):
        """Check book availability"""
        if self.transaction_type != "Borrow":
            return

        for item in self.items:
            book = frappe.get_doc("Library Book", item.book)
            if book.status != "Available":
                frappe.throw(
                    f"Book '{book.title}' is currently {book.status}. "
                    "Cannot borrow."
                )

        # Check duplicate books in same transaction
        books = [item.book for item in self.items]
        if len(books) != len(set(books)):
            frappe.throw("Duplicate books found in transaction items")

    def calculate_totals(self):
        """Calculate total late fees"""
        self.total_late_fee = sum(
            (item.late_fee or 0) for item in self.items
        )
        self.total_books = len(self.items)

    def on_submit(self):
        """Update book status on submit"""
        super().on_submit()
        self.update_book_statuses()
        self.update_member_stats()

    def on_cancel(self):
        """Reverse book status on cancel"""
        super().on_cancel()
        self.reverse_book_statuses()
        self.update_member_stats()

    def update_book_statuses(self):
        """Set book status based on transaction type"""
        new_status = "Borrowed" if self.transaction_type == "Borrow" else "Available"
        for item in self.items:
            frappe.db.set_value("Library Book", item.book, "status", new_status)

    def reverse_book_statuses(self):
        """Reverse: Borrow cancel → Available, Return cancel → Borrowed"""
        reverse_status = "Available" if self.transaction_type == "Borrow" else "Borrowed"
        for item in self.items:
            frappe.db.set_value("Library Book", item.book, "status", reverse_status)

    def update_member_stats(self):
        """Update books_borrowed count on member"""
        count = frappe.db.count("Library Transaction", {
            "member": self.member,
            "transaction_type": "Borrow",
            "docstatus": 1
        })
        frappe.db.set_value("Library Member", self.member,
            "active_transactions", count)

    @frappe.whitelist()
    def return_books(self):
        """Mark all books as returned — called from client button"""
        if self.docstatus != 1:
            frappe.throw("Transaction must be submitted")

        today = nowdate()
        for item in self.items:
            if item.status != "Returned":
                late_days = max(0, date_diff(today, item.due_date))
                item.db_set("status", "Returned")
                item.db_set("return_date", today)
                item.db_set("late_fee", late_days * 5000 if late_days > 0 else 0)

                frappe.db.set_value("Library Book", item.book, "status", "Available")

        self.calculate_totals()
        self.db_set("total_late_fee", self.total_late_fee)
        self.set_status()
```

### Mini Quiz

<details>
<summary>Q1: `self.db_set("status", "Completed")` khác gì với `self.status = "Completed"`?</summary>

**A:** `self.db_set()` — update TRUC TIEP trong database (SQL UPDATE) và cập nhật Python object. Ẩn toan dùng trong `on_update`, `on_submit`, etc. `self.status = "Completed"` — chi thay đổi Python object, KHÔNG ghi vao DB (tru khi dang trong validate/before_save trước khi save).
</details>

<details>
<summary>Q2: Khi nào dùng `flags.ignore_permissions = True` và tại sao phải cẩn thận?</summary>

**A:** Dùng khi system can thao tác không thuộc user nào (VD: scheduled job update status, background processing). PHẢI CAN THAN vì nó bypass toàn bộ permission system — user không có quyền van thuc hiện được. Chi dùng trong trusted code paths (controller, scheduled jobs), KHÔNG BAO GIỜ dùng trong whitelisted API mà user gọi trực tiếp.
</details>

### Skill References

- **DEEP DIVE:** Xem skill `dcnet_quality` -> `syntax/erpnext-syntax-controllers/` cho controller rules đặc biệt cho ERPNext
- **DEEP DIVE:** Xem skill `dcnet_quality` -> `impl/` cho implementation patterns theo domain
- **DEEP DIVE:** Xem skill `erpnext` để đọc source code của các controllers nhu SalesInvoice, PurchaseOrder

---

## L4.3: hooks.py Deep Dive

### Tổng quan
hooks.py là "bo nao" của Frappe app — nó dang ky mọi thứ app mượn làm với framework. Bài này di sau vao TUNG hook type: doc_events, scheduler, fixtures, overrides, jinja, boot_session, và nhiều hook khác. Đây là reference file — quay lại khi can.

### Key Concepts

#### 1. doc_events — Hook vao Document Lifecycle

```python
# hooks.py

doc_events = {
    # Hook vao DocType cũ the
    "Sales Order": {
        "validate": "my_app.overrides.sales_order.validate",
        "on_submit": "my_app.overrides.sales_order.on_submit",
        "on_cancel": "my_app.overrides.sales_order.on_cancel",
        "on_update": "my_app.overrides.sales_order.on_update",
        "before_save": "my_app.overrides.sales_order.before_save",
        "after_insert": "my_app.overrides.sales_order.after_insert",
        "on_trash": "my_app.overrides.sales_order.on_trash",
    },

    # Hook vao NHIỀU DocTypes
    "Sales Invoice": {
        "on_submit": "my_app.overrides.invoice.on_submit",
    },

    # Hook vao TẤT CẢ DocTypes
    "*": {
        "after_insert": "my_app.audit.log_creation",
        "on_update": "my_app.audit.log_update",
        "on_trash": "my_app.audit.log_deletion",
    }
}
```

```python
# my_app/overrides/sales_order.py

import frappe

def validate(doc, method):
    """
    doc = document object (giong self trong controller)
    method = ten method dang chay ("validate")
    """
    if doc.grand_total > 100000000:  # 100 trieu
        frappe.msgprint("Large order — will need Director approval")

def on_submit(doc, method):
    """Create linked record when SO is submitted"""
    if doc.custom_requires_approval:
        approval = frappe.get_doc({
            "doctype": "Approval Request",
            "reference_doctype": "Sales Order",
            "reference_name": doc.name,
            "amount": doc.grand_total
        })
        approval.insert(ignore_permissions=True)
```

> **Lưu ý:** doc_events handler nhận 2 tham số: `(doc, method)`. `doc` là document object, `method` là string ten event.

#### 2. scheduler_events — Cron Jobs

```python
# hooks.py

scheduler_events = {
    # Chạy mọi ngày luc 00:00
    "daily": [
        "my_app.tasks.daily_cleanup",
        "my_app.tasks.send_daily_report"
    ],

    # Chạy mọi gio
    "hourly": [
        "my_app.tasks.check_overdue_books"
    ],

    # Chạy mọi 15 phut
    "all": [
        "my_app.tasks.process_queue"  # ⚠️ Chay moi 5 phut (khong phai "all")
    ],

    # Chạy mọi tuan (Monday 00:00)
    "weekly": [
        "my_app.tasks.weekly_summary"
    ],

    # Chạy mọi tháng (ngày 1, 00:00)
    "monthly": [
        "my_app.tasks.monthly_report"
    ],

    # Cron expression — linh hoạt nhất
    "cron": {
        "0 9 * * 1-5": [  # 9h sang, thu 2-6
            "my_app.tasks.morning_brief"
        ],
        "0 18 * * *": [   # 6h chieu moi ngay
            "my_app.tasks.end_of_day_sync"
        ],
        "*/30 * * * *": [  # Moi 30 phut
            "my_app.tasks.check_integrations"
        ]
    }
}
```

```python
# my_app/tasks.py

import frappe

def daily_cleanup():
    """Delete old logs — chay moi ngay"""
    frappe.db.sql("""
        DELETE FROM `tabError Log`
        WHERE creation < DATE_SUB(NOW(), INTERVAL 30 DAY)
    """)
    frappe.db.commit()

def check_overdue_books():
    """Check va cap nhat sach qua han — chay moi gio"""
    today = frappe.utils.nowdate()

    overdue_items = frappe.db.sql("""
        SELECT lti.name, lti.parent, lti.book, lti.due_date
        FROM `tabLibrary Transaction Item` lti
        JOIN `tabLibrary Transaction` lt ON lt.name = lti.parent
        WHERE lti.status = 'Borrowed'
          AND lti.due_date < %s
          AND lt.docstatus = 1
    """, today, as_dict=True)

    for item in overdue_items:
        frappe.db.set_value("Library Transaction Item", item.name,
            "status", "Overdue")

    if overdue_items:
        frappe.db.commit()
        frappe.logger().info(f"Marked {len(overdue_items)} items as overdue")
```

#### 3. fixtures — Data Sync

```python
# hooks.py

fixtures = [
    # Export TẤT CẢ records của DocType
    "Role",
    "Workflow",

    # Export có filter
    {
        "dt": "Custom Field",
        "filters": [
            ["dt", "in", ["Sales Order", "Sales Invoice", "Purchase Order"]]
        ]
    },
    {
        "dt": "Property Setter",
        "filters": [
            ["doc_type", "in", ["Sales Order", "Sales Invoice"]]
        ]
    },
    {
        "dt": "Client Script",
        "filters": [
            ["module", "=", "My Module"]
        ]
    }
]
```

```bash
# Export fixtures từ site → JSON files
bench --site flow.local export-fixtures --app my_app

# Files xuất ra: my_app/my_app/fixtures/
# - custom_field.json
# - property_setter.json
# - client_script.json

# Import fixtures (tự động khi bench migrate)
bench --site flow.local migrate
```

#### 4. override_whitelisted_methods

```python
# hooks.py — Thay the API method của app khác

override_whitelisted_methods = {
    # Thay the method goc bang custom method
    "frappe.client.get_count": "my_app.overrides.api.custom_get_count",
    "erpnext.selling.page.point_of_sale.point_of_sale.get_items":
        "my_app.overrides.pos.custom_get_items"
}
```

#### 5. jinja — Custom Template Functions

```python
# hooks.py

jinja = {
    "methods": [
        "my_app.utils.jinja.format_vnd",
        "my_app.utils.jinja.get_company_logo"
    ],
    "filters": [
        "my_app.utils.jinja.currency_in_words"
    ]
}
```

```python
# my_app/utils/jinja.py

def format_vnd(amount):
    """Format so thanh VND: 1000000 → '1.000.000d'"""
    if not amount:
        return "0d"
    return f"{int(amount):,.0f}d".replace(",", ".")

def currency_in_words(amount):
    """Chuyen so thanh chu: 1000000 → 'Mot trieu dong'"""
    # Implementation...
    pass
```

```html
<!-- Dung trong Print Format / Email Template -->
<p>Total: {{ format_vnd(doc.grand_total) }}</p>
<p>In words: {{ doc.grand_total | currency_in_words }}</p>
```

#### 6. Các hooks khác

```python
# hooks.py

# === BOOT SESSION ===
# Data gửi xuong browser khi page load
boot_session = "my_app.startup.boot_session"

# === AFTER MIGRATE ===
# Chạy sau mọi bench migrate
after_migrate = [
    "my_app.install.after_migrate"
]

# === AFTER INSTALL ===
# Chạy sau install-app
after_install = "my_app.install.after_install"

# === WEBSITE ===
website_route_rules = [
    {"from_route": "/library/<book_id>", "to_route": "book_detail"},
]

# === PERMISSION ===
permission_query_conditions = {
    "Library Book": "my_app.permissions.get_book_conditions"
}

has_permission = {
    "Library Book": "my_app.permissions.has_book_permission"
}

# === OVERRIDE DOCTYPE CLASS ===
override_doctype_class = {
    "Sales Order": "my_app.overrides.custom_sales_order.CustomSalesOrder"
}
```

### Code Examples

```python
# Xem tất cả hooks của installed apps
# Trong bench console:

hooks = frappe.get_hooks()

# Xem doc_events
import json
print(json.dumps(hooks.get("doc_events", {}), indent=2))

# Xem scheduler_events
print(json.dumps(hooks.get("scheduler_events", {}), indent=2))

# Xem fixtures của 1 app cũ the
app_hooks = frappe.get_hooks(app_name="dcnet_apps")
print("fixtures:", app_hooks.get("fixtures", []))

# Xem override methods
print("overrides:", hooks.get("override_whitelisted_methods", {}))
```

### Mini Quiz

<details>
<summary>Q1: Bạn muốn thêm custom validation vao Sales Order của ERPNext mà KHÔNG sửa code ERPNext. Làm cach nao?</summary>

**A:** Dùng `doc_events` trong hooks.py của custom app:
```python
doc_events = {
    "Sales Order": {
        "validate": "my_app.overrides.sales_order.custom_validate"
    }
}
```
Function `custom_validate(doc, method)` sẽ chạy CUNG VOI validate của ERPNext (không thay thế). Đây là cach "extend without modify".
</details>

<details>
<summary>Q2: `fixtures` trong hooks.py export data ở format nào và khi nào được import?</summary>

**A:** Export ra **JSON files** trong `my_app/fixtures/` folder (VD: `custom_field.json`). Tự động import khi chạy `bench --site <site> migrate`. Đây là cach dòng bo customizations (Custom Fields, Property Setters, Workflows) giua environments.
</details>

<details>
<summary>Q3: Phân biệt `doc_events` và `override_doctype_class`. Khi nào dùng cái nao?</summary>

**A:** `doc_events` — THEM logic vao events (chạy THEM, không thay thế). Dùng khi mượn hook vao 1-2 events. `override_doctype_class` — THAY THE cả Python class của DocType. Dùng khi mượn override nhiều methods hoặc thay đổi behavior toàn diện. `override_doctype_class` mạnh hơn nhưng cũng nguy hiếm hơn — nếu ERPNext update class goc, override có thể break.
</details>

### Skill References

- **DEEP DIVE:** Xem skill `dcnet_quality` -> `syntax/erpnext-syntax-hooks/` cho FULL hooks.py reference và rules
- **DEEP DIVE:** Xem skill `dcnet_quality` -> `syntax/erpnext-syntax-jinja/` cho Jinja template patterns
- **DEEP DIVE:** Xem skill `dcnet_quality` -> `syntax/erpnext-syntax-scheduler/` cho scheduler best practices

---

## L4.4: Scheduled Jobs

### Tổng quan
Scheduled jobs (background tasks) là cach chạy code dinh ky hoặc async — không cần user trigger. Frappe dùng Redis Queue (RQ) cho background jobs và built-in scheduler cho cron-like tasks. Bài này day cach tạo scheduled jobs và background jobs dùng cach.

### Key Concepts

#### 1. Scheduler Events (da cover ở L4.3)

```python
# hooks.py — khai báo
scheduler_events = {
    "daily": ["my_app.tasks.daily_task"],
    "hourly": ["my_app.tasks.hourly_task"],
    "cron": {
        "0 9 * * *": ["my_app.tasks.nine_am_task"]
    }
}
```

#### 2. frappe.enqueue() — Background Jobs

```python
# Khi can chạy task nang mà KHÔNG mượn block user

import frappe

@frappe.whitelist()
def process_bulk_returns(member_name):
    """Goi tu client — enqueue de xu ly background"""
    frappe.enqueue(
        method="my_app.tasks.bulk_return_processor",
        queue="long",           # short (5min), default (5min), long (30min)
        timeout=600,            # Timeout in seconds
        is_async=True,          # True = background, False = sync (debug)
        job_name=f"bulk_return_{member_name}",  # Unique job identifier
        # Kwargs truyen xuong method:
        member_name=member_name,
        process_date=frappe.utils.nowdate()
    )
    frappe.msgprint("Processing in background. You will be notified when done.")
```

```python
# my_app/tasks.py

import frappe

def bulk_return_processor(member_name, process_date):
    """Chay trong background worker"""
    transactions = frappe.get_all("Library Transaction",
        filters={
            "member": member_name,
            "transaction_type": "Borrow",
            "docstatus": 1
        }
    )

    for txn_data in transactions:
        txn = frappe.get_doc("Library Transaction", txn_data.name)
        for item in txn.items:
            if item.status == "Borrowed":
                item.db_set("status", "Returned")
                item.db_set("return_date", process_date)
                frappe.db.set_value("Library Book", item.book,
                    "status", "Available")

    frappe.db.commit()

    # Thong bao user khi xong
    frappe.publish_realtime(
        event="bulk_return_complete",
        message={"member": member_name, "count": len(transactions)},
        user=frappe.session.user
    )
```

#### 3. Queues

```python
# Frappe có 3 queues với priorities khác nhau:

# SHORT queue — tasks nhanh (< 5 phut)
frappe.enqueue(method="...", queue="short")
# VD: send email, clear cache, small updates

# DEFAULT queue — tasks bình thường (< 5 phut)
frappe.enqueue(method="...", queue="default")
# VD: generate report, sync data

# LONG queue — tasks nang (< 30 phut)
frappe.enqueue(method="...", queue="long")
# VD: bulk import, large exports, data migration
```

#### 4. frappe.enqueue_đọc() — Enqueue Document Method

```python
# Enqueue 1 method của document cũ the

frappe.enqueue_doc(
    doctype="Library Transaction",
    name="LT-2026-0001",
    method="return_books",           # Method name tren document
    queue="short",
    timeout=300
)

# Tuong duong với:
# doc = frappe.get_doc("Library Transaction", "LT-2026-0001")
# doc.return_books()
# Nhưng chạy trong background
```

#### 5. Monitor Jobs

```python
# Xem jobs dang chạy
from frappe.utils.background_jobs import get_jobs

jobs = get_jobs()
for site, job_list in jobs.items():
    print(f"Site: {site}")
    for job in job_list:
        print(f"  {job.get('job_name')}: {job.get('status')}")

# Xem job logs trong UI
# /app/rq-job (RQ Job DocType)

# Xem scheduled job status
# /app/scheduled-job-type
```

```bash
# CLI: xem workers
bench doctor

# Xem queue lengths
bench show-pending-jobs

# Retry failed jobs
bench retry-jobs
```

#### 6. Scheduled Job Type (UI-based)

```python
# Ngoai hooks.py, có thể tạo scheduled jobs qua UI:
# /app/scheduled-job-type/new

# Hoặc bang code:
job = frappe.get_doc({
    "doctype": "Scheduled Job Type",
    "method": "my_app.tasks.custom_daily_job",
    "frequency": "Daily",
    "cron_format": "0 6 * * *"  # 6h sang
})
job.insert()
```

### Code Examples

```python
# === Vi du: Overdue Book Checker (Scheduled Job) ===
# my_app/tasks.py

import frappe
from frappe.utils import nowdate, date_diff, add_days

def check_overdue_books():
    """
    Scheduled job: chay moi ngay
    - Tim sach qua han
    - Update status
    - Gui email nhac member
    """
    today = nowdate()

    # Tìm items overdue
    overdue_items = frappe.db.sql("""
        SELECT
            lti.name as item_name,
            lti.book,
            lti.due_date,
            lt.member,
            lt.member_name,
            lb.title as book_title,
            lm.email as member_email
        FROM `tabLibrary Transaction Item` lti
        JOIN `tabLibrary Transaction` lt ON lt.name = lti.parent
        JOIN `tabLibrary Book` lb ON lb.name = lti.book
        JOIN `tabLibrary Member` lm ON lm.name = lt.member
        WHERE lti.status = 'Borrowed'
          AND lti.due_date < %(today)s
          AND lt.docstatus = 1
    """, {"today": today}, as_dict=True)

    if not overdue_items:
        return

    # Update status
    for item in overdue_items:
        frappe.db.set_value("Library Transaction Item", item.item_name,
            "status", "Overdue")

    # Nhóm theo member để gửi 1 email
    from collections import defaultdict
    by_member = defaultdict(list)
    for item in overdue_items:
        by_member[item.member_email].append(item)

    # Gửi email
    for email, items in by_member.items():
        book_list = "\n".join([
            f"- {item.book_title} (due: {item.due_date}, "
            f"{date_diff(today, item.due_date)} days late)"
            for item in items
        ])

        frappe.sendmail(
            recipients=[email],
            subject=f"Overdue Books Reminder - {len(items)} book(s)",
            message=f"""
            <p>Dear {items[0].member_name},</p>
            <p>The following books are overdue:</p>
            <pre>{book_list}</pre>
            <p>Please return them as soon as possible to avoid late fees.</p>
            """,
            now=True  # Gui ngay, khong queue
        )

    frappe.db.commit()
    frappe.logger().info(
        f"Overdue check: {len(overdue_items)} items, "
        f"{len(by_member)} members notified"
    )


def generate_weekly_report():
    """
    Scheduled job: chay moi tuan
    Tao bao cao tuan ve hoat dong thu vien
    """
    from_date = add_days(nowdate(), -7)

    stats = {
        "new_books": frappe.db.count("Library Book", {
            "creation": [">=", from_date]
        }),
        "new_members": frappe.db.count("Library Member", {
            "creation": [">=", from_date]
        }),
        "transactions": frappe.db.count("Library Transaction", {
            "creation": [">=", from_date],
            "docstatus": 1
        }),
        "overdue": frappe.db.count("Library Transaction Item", {
            "status": "Overdue"
        })
    }

    # Gửi report cho admin
    frappe.sendmail(
        recipients=["admin@library.com"],
        subject=f"Weekly Library Report ({from_date} - {nowdate()})",
        message=f"""
        <h3>Weekly Library Report</h3>
        <table border="1" cellpadding="5">
            <tr><td>New Books</td><td>{stats['new_books']}</td></tr>
            <tr><td>New Members</td><td>{stats['new_members']}</td></tr>
            <tr><td>Transactions</td><td>{stats['transactions']}</td></tr>
            <tr><td>Overdue Items</td><td>{stats['overdue']}</td></tr>
        </table>
        """,
        now=True
    )
```

```python
# hooks.py — dang ky scheduled jobs
scheduler_events = {
    "daily": [
        "frappe_learn.tasks.check_overdue_books"
    ],
    "weekly": [
        "frappe_learn.tasks.generate_weekly_report"
    ]
}
```

### Mini Quiz

<details>
<summary>Q1: Phân biệt `frappe.enqueue()` và `scheduler_events`. Khi nào dùng cái nao?</summary>

**A:** `scheduler_events` — chạy **dinh ky** theo lich (daily, hourly, cron). VD: check overdue hàng ngày. `frappe.enqueue()` — chạy **1 lần** trong background khi được trigger (boi user action, API call, etc.). VD: process bulk import khi user upload file. Scheduler = cron job, enqueue = async task.
</details>

<details>
<summary>Q2: Queue "long" có timeout bao lau? Khi nào dùng?</summary>

**A:** Queue "long" có default timeout **1500 giay (25 phut)**. Dùng cho tasks nang: data import lớn, export báo cáo phức tạp, sync dữ liệu từ hệ thống ngoài. Có thể tăng timeout bang `frappe.enqueue(timeout=3600)` cho 1 gio.
</details>

### Skill References

- **DEEP DIVE:** Xem skill `dcnet_quality` -> `syntax/erpnext-syntax-scheduler/` cho scheduler coding rules và error handling
- **DEEP DIVE:** Xem skill `frappe` -> `references/integration/` cho background job patterns với external systems

---

## L4.5: Hands-on — Full Controller cho Library Transaction

### Tổng quan
Tong hop tất cả kiến thức Module 4: viết controller đầy đủ cho Library Transaction với validate, lifecycle hooks, status management, email notifications, và scheduled overdue check. Đây là bài tập cuối cùng của Module 4.

### Yêu cầu

1. Controller cho Library Transaction với:
   - Validate member status và book availability
   - Auto-set due dates và calculate late fees
   - Update book status on submit/cancel
   - Send email when transaction is submitted
2. Scheduled job check overdue daily
3. hooks.py dang ky doc_events và scheduler

### Step 1: Controller File

```python
# frappe_learn/library/doctype/library_transaction/library_transaction.py

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import nowdate, add_days, getdate, date_diff, fmt_money


class LibraryTransaction(Document):
    # ============================================
    # VALIDATION PHASE
    # ============================================

    def validate(self):
        super().validate()
        self.set_missing_values()
        self.validate_member()
        self.validate_books()
        self.validate_dates()
        self.calculate_totals()

    def set_missing_values(self):
        """Set sensible defaults"""
        if not self.transaction_date:
            self.transaction_date = nowdate()

        for item in self.items:
            # Default due date = 14 days from transaction
            if not item.due_date and self.transaction_type == "Borrow":
                item.due_date = add_days(self.transaction_date, 14)

            # Default status
            if not item.status:
                if self.transaction_type == "Borrow":
                    item.status = "Borrowed"
                else:
                    item.status = "Returned"
                    if not item.return_date:
                        item.return_date = self.transaction_date

    def validate_member(self):
        """Ensure member is active and eligible"""
        if not self.member:
            return

        member = frappe.get_cached_doc("Library Member", self.member)

        if member.status != "Active":
            frappe.throw(
                _("Member {0} is {1}. Only Active members can transact.").format(
                    member.full_name, member.status
                )
            )

        # Check borrow limit (max 5 active borrows)
        if self.transaction_type == "Borrow" and self.is_new():
            active_borrows = frappe.db.count("Library Transaction", {
                "member": self.member,
                "transaction_type": "Borrow",
                "docstatus": 1
            })
            if active_borrows >= 5:
                frappe.throw(
                    _("Member {0} has reached the maximum borrow limit (5).").format(
                        member.full_name
                    )
                )

    def validate_books(self):
        """Check book availability for Borrow transactions"""
        if self.transaction_type != "Borrow":
            return

        seen_books = set()
        for item in self.items:
            # Check duplicates
            if item.book in seen_books:
                frappe.throw(_("Duplicate book {0} in items").format(item.book))
            seen_books.add(item.book)

            # Check availability
            if not self.flags.ignore_book_status:
                book_status = frappe.db.get_value("Library Book", item.book, "status")
                if book_status != "Available":
                    book_title = frappe.db.get_value("Library Book", item.book, "title")
                    frappe.throw(
                        _("Book '{0}' is currently {1}").format(book_title, book_status)
                    )

    def validate_dates(self):
        """Validate date logic"""
        if not self.transaction_date:
            return

        txn_date = getdate(self.transaction_date)

        for item in self.items:
            if item.due_date and getdate(item.due_date) < txn_date:
                frappe.throw(
                    _("Row {0}: Due date cannot be before transaction date").format(item.idx)
                )

            if item.return_date and getdate(item.return_date) < txn_date:
                frappe.throw(
                    _("Row {0}: Return date cannot be before transaction date").format(item.idx)
                )

    def calculate_totals(self):
        """Calculate late fees and totals"""
        late_fee_per_day = 5000  # VND

        total_late_fee = 0
        for item in self.items:
            if item.return_date and item.due_date:
                days_late = date_diff(item.return_date, item.due_date)
                if days_late > 0:
                    item.late_fee = days_late * late_fee_per_day
                else:
                    item.late_fee = 0
            total_late_fee += (item.late_fee or 0)

        self.total_late_fee = total_late_fee
        self.total_books = len(self.items)

    # ============================================
    # SUBMIT / CANCEL
    # ============================================

    def on_submit(self):
        """Side effects when transaction is submitted"""
        super().on_submit()
        self.update_book_statuses()
        self.update_member_stats()
        self.send_transaction_email()

    def on_cancel(self):
        """Reverse effects when transaction is cancelled"""
        super().on_cancel()
        self.reverse_book_statuses()
        self.update_member_stats()

    def update_book_statuses(self):
        """Update book status based on transaction type"""
        new_status = "Borrowed" if self.transaction_type == "Borrow" else "Available"
        for item in self.items:
            frappe.db.set_value("Library Book", item.book, "status", new_status)

    def reverse_book_statuses(self):
        """Reverse book status on cancel"""
        reverse = "Available" if self.transaction_type == "Borrow" else "Borrowed"
        for item in self.items:
            frappe.db.set_value("Library Book", item.book, "status", reverse)

    def update_member_stats(self):
        """Update member's active transaction count"""
        count = frappe.db.count("Library Transaction", {
            "member": self.member,
            "transaction_type": "Borrow",
            "docstatus": 1
        })
        frappe.db.set_value("Library Member", self.member,
            "active_transactions", count)

    # ============================================
    # CUSTOM METHODS
    # ============================================

    @frappe.whitelist()
    def return_books(self):
        """Mark all borrowed books as returned — called from client button"""
        if self.docstatus != 1:
            frappe.throw(_("Transaction must be submitted"))

        if self.transaction_type != "Borrow":
            frappe.throw(_("Can only return books from Borrow transactions"))

        today = nowdate()
        returned_count = 0

        for item in self.items:
            if item.status in ("Borrowed", "Overdue"):
                days_late = max(0, date_diff(today, item.due_date))
                late_fee = days_late * 5000 if days_late > 0 else 0

                item.db_set("status", "Returned")
                item.db_set("return_date", today)
                item.db_set("late_fee", late_fee)

                frappe.db.set_value("Library Book", item.book, "status", "Available")
                returned_count += 1

        # Update totals
        self.reload()
        self.calculate_totals()
        self.db_set("total_late_fee", self.total_late_fee)

        if self.total_late_fee > 0:
            frappe.msgprint(
                _("Late fee: {0}").format(fmt_money(self.total_late_fee, currency="VND")),
                title=_("Late Return"),
                indicator="orange"
            )

        return {"returned": returned_count, "late_fee": self.total_late_fee}

    def send_transaction_email(self):
        """Send email notification to member"""
        if not self.member:
            return

        member = frappe.get_cached_doc("Library Member", self.member)
        if not member.email:
            return

        book_list = "<br>".join([
            f"- {item.book_title or item.book}"
            + (f" (due: {item.due_date})" if item.due_date else "")
            for item in self.items
        ])

        subject = _("{0} Transaction: {1}").format(
            self.transaction_type, self.name
        )

        message = f"""
        <p>Dear {member.full_name},</p>
        <p>Your {self.transaction_type.lower()} transaction has been processed:</p>
        <p>{book_list}</p>
        """

        if self.transaction_type == "Borrow":
            message += "<p><b>Please return books by the due dates listed above.</b></p>"

        if self.total_late_fee:
            message += f"<p>Late fee: {fmt_money(self.total_late_fee, currency='VND')}</p>"

        try:
            frappe.sendmail(
                recipients=[member.email],
                subject=subject,
                message=message,
                now=True
            )
        except Exception:
            frappe.log_error(title=f"Email failed for {self.name}")

    # ============================================
    # TRASH
    # ============================================

    def on_trash(self):
        """Prevent deletion of submitted transactions"""
        if self.docstatus == 1:
            frappe.throw(_("Cannot delete submitted transactions. Cancel first."))
```

### Step 2: Client Script

```javascript
// frappe_learn/library/doctype/library_transaction/library_transaction.js

frappe.ui.form.on("Library Transaction", {
    setup(frm) {
        frm.set_query("book", "items", function(doc) {
            if (doc.transaction_type === "Borrow") {
                return { filters: { status: "Available" } };
            } else if (doc.transaction_type === "Return") {
                return { filters: { status: "Borrowed" } };
            }
            return {};
        });

        frm.set_query("member", function() {
            return { filters: { status: "Active" } };
        });
    },

    refresh(frm) {
        // Return Books button
        if (frm.doc.docstatus === 1
            && frm.doc.transaction_type === "Borrow") {

            let has_unreturned = (frm.doc.items || []).some(
                row => row.status !== "Returned"
            );

            if (has_unreturned) {
                frm.add_custom_button(__("Return Books"), function() {
                    frm.call("return_books").then(r => {
                        if (r.message) {
                            frappe.show_alert({
                                message: __("Returned {0} book(s)", [r.message.returned]),
                                indicator: "green"
                            });
                            frm.reload_doc();
                        }
                    });
                }).addClass("btn-primary");
            }
        }
    },

    transaction_type(frm) {
        frm.clear_table("items");
        frm.refresh_field("items");
    }
});
```

### Step 3: hooks.py

```python
# Thêm vao hooks.py của frappe_learn:

scheduler_events = {
    "daily": [
        "frappe_learn.tasks.check_overdue_books"
    ]
}
```

### Step 4: Scheduled Task

```python
# frappe_learn/tasks.py

import frappe
from frappe.utils import nowdate, date_diff

def check_overdue_books():
    """Daily job: mark overdue items and notify members"""
    today = nowdate()

    overdue_items = frappe.db.sql("""
        SELECT lti.name, lti.book, lti.due_date, lt.member
        FROM `tabLibrary Transaction Item` lti
        JOIN `tabLibrary Transaction` lt ON lt.name = lti.parent
        WHERE lti.status = 'Borrowed'
          AND lti.due_date < %(today)s
          AND lt.docstatus = 1
    """, {"today": today}, as_dict=True)

    for item in overdue_items:
        frappe.db.set_value("Library Transaction Item", item.name,
            "status", "Overdue")

    if overdue_items:
        frappe.db.commit()
        frappe.logger("frappe_learn").info(
            f"Marked {len(overdue_items)} items as overdue"
        )
```

### Step 5: Verify

```bash
# Migrate để apply hooks
bench --site flow.local migrate

# Test controller
bench --site flow.local console
```

```python
# Test trong console:

# 1. Tạo book
book = frappe.get_doc({
    "doctype": "Library Book",
    "title": "Design Patterns",
    "author": "Gang of Four",
    "isbn": "9780201633610",
    "category": "Reference"
})
book.insert()

# 2. Tạo member
member = frappe.get_doc({
    "doctype": "Library Member",
    "full_name": "Test User",
    "email": "test@example.com",
    "member_type": "Faculty"
})
member.insert()

# 3. Tạo và submit transaction
txn = frappe.get_doc({
    "doctype": "Library Transaction",
    "member": member.name,
    "transaction_type": "Borrow",
    "items": [{"book": book.name}]
})
txn.insert()
txn.submit()
frappe.db.commit()

# 4. Verify book status changed
book.reload()
print(f"Book status: {book.status}")  # "Borrowed"

# 5. Test return
txn.return_books()
frappe.db.commit()

book.reload()
print(f"Book status: {book.status}")  # "Available"

# 6. Verify late fee
for item in txn.items:
    item.reload()
    print(f"Item status: {item.status}, Late fee: {item.late_fee}")
```

#### Kiểm tra hoàn thành

- [ ] Controller validate: member status, book availability, dates
- [ ] Auto-set due dates khi Borrow
- [ ] Book status update on submit (Available → Borrowed)
- [ ] Book status reverse on cancel (Borrowed → Available)
- [ ] "Return Books" button hoat dòng từ UI
- [ ] Late fee tính dùng
- [ ] Email gửi khi submit transaction
- [ ] Scheduled job check overdue trong hooks.py
- [ ] Member stats cập nhật tự động

> **Tiếp theo:** Module 5 sẽ day về Permissions, Roles, và Security — kiem soat ai được phep làm gì trong hệ thống.

### Skill References

- **DEEP DIVE:** Xem skill `dcnet_quality` -> `syntax/erpnext-syntax-controllers/` cho controller validation rules
- **DEEP DIVE:** Xem skill `dcnet_quality` -> `syntax/erpnext-syntax-hooks/` cho hooks.py patterns
- **DEEP DIVE:** Xem skill `dcnet_quality` -> `syntax/erpnext-syntax-scheduler/` cho scheduled job rules
- **DEEP DIVE:** Xem skill `dcnet_quality` -> `errors/` cho error handling trong controllers
- **DEEP DIVE:** Xem skill `frappe` -> `test_examples/` để hiểu cach test controllers với FrappeTestCase
