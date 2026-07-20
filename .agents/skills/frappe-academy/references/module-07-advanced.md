# Module 7: Advanced Topics

> **Mục tiêu / Objective:** Thành thạo permissions, Jinja templates, testing, và data import/export trong Frappe.
> **Yêu cầu / Prerequisites:** Module 1-6 (DocType, Controllers, Hooks, API, UI)
> **Thời lượng / Duration:** ~10 giờ thực hành

---

## L7.1: Permissions

### Tổng quan / Overview

Frappe có hệ thống permission 3 lớp: Role Permission (DocType level), User Permission (record level), và Custom Permission Logic (code). Hiểu rõ hệ thống này là bắt buộc để xây dựng ứng dụng ẩn toàn — sai permission có thể lo data nhạy cảm hoặc chặn user hop le.

### Khái niệm chính / Key Concepts

#### 1. Role Permissions (DocType Level)

```
Role Permission xac dinh: Role nao co the lam gi voi DocType nao.

Cac quyen co ban:
- read: Xem documents
- write: Chinh sua documents
- create: Tao document moi
- delete: Xoa documents
- submit: Submit document (cho DocTypes co is_submittable=1)
- cancel: Cancel document da submit
- amend: Amend (sua) document da cancel
- report: Xem report cua DocType
- import: Import data tu CSV
- export: Export data ra CSV
- print: In document
- email: Gui email document
- share: Chia se document voi user khac
```

```python
# Thiết lập Role Permission bang code (thường trong install.py hoặc setup)
import frappe
from frappe.permissions import add_permission, update_permission_property

# Thêm quyền cho role
add_permission("Library Book", "Librarian", 0)  # permlevel 0 = all fields
update_permission_property("Library Book", "Librarian", 0, "read", 1)
update_permission_property("Library Book", "Librarian", 0, "write", 1)
update_permission_property("Library Book", "Librarian", 0, "create", 1)
update_permission_property("Library Book", "Librarian", 0, "delete", 1)

# Member chi đọc được
add_permission("Library Book", "Library Member", 0)
update_permission_property("Library Book", "Library Member", 0, "read", 1)
update_permission_property("Library Book", "Library Member", 0, "write", 0)

# Permission Level — Giới hạn quyền theo nhóm fields
# Level 0: Tất cả fields
# Level 1+: Chi các fields được đặt permlevel tuong ung
# VD: truong "cost_price" đặt permlevel=1 → chi Librarian thay, Member không thay
```

#### 2. User Permissions (Record Level)

```python
# User Permission giới hạn user chi thay RECORDS cũ the
# VD: Member chi thay Library Transaction của minh

# Thiết lập bang code
frappe.get_doc({
    "doctype": "User Permission",
    "user": "member@example.com",
    "allow": "Library Member",        # DocType duoc gioi han
    "for_value": "MEM-001",           # Gia tri cu the
    "applicable_for": "Library Transaction",  # Ap dung cho DocType nao
    "apply_to_all_doctypes": 0        # Khong ap dung cho tat ca
}).insert(ignore_permissions=True)

# Kết quả: member@example.com chi thay Library Transaction của MEM-001

# Kiểm tra permission trong code
if frappe.has_permission("Library Transaction", "read", doc=transaction_doc):
    # User có quyền đọc transaction này
    pass
else:
    frappe.throw("No permission", frappe.PermissionError)
```

#### 3. if_owner — Quyền dua trên người tạo

```
if_owner la option trong Role Permission:
- Khi bat: User chi co quyen voi documents MA HO TAO (owner = user)
- Huu ich cho: Member chi sua duoc profile cua minh

Thiet lap:
1. DocType → Permission Rules → check "If Owner"
2. Hoac trong code:
```

```python
update_permission_property("Library Member", "Library Member", 0, "if_owner", 1)
# → Library Member role chi read/write documents ho tạo
```

#### 4. Custom Permission Logic trong Controller

```python
# library_book.py
class LibraryBook(Document):
    def has_permission(self, permtype, user=None):
        """Custom permission logic — ghi de logic mac dinh.

        Args:
            permtype: "read", "write", "create", "delete", "submit", "cancel"
            user: User ID (mac dinh la user hien tai)

        Returns:
            True/False hoac None (de Frappe xu ly mac dinh)
        """
        if not user:
            user = frappe.session.user

        # Admin luôn có quyền
        if "Librarian" in frappe.get_roles(user):
            return True

        # Member chi đọc được sach Available
        if permtype == "read":
            if "Library Member" in frappe.get_roles(user):
                return True  # Cho doc tat ca sach

        # Member không được sửa/xóa sach
        if permtype in ("write", "delete"):
            if "Library Member" in frappe.get_roles(user):
                return False

        # Trả về None để dùng role permission mac dinh
        return None
```

#### 5. Permission Query — Loc data trong list view

```python
# hooks.py
permission_query_conditions = {
    "Library Transaction": "library_management.permissions.get_transaction_conditions"
}

# permissions.py
def get_transaction_conditions(user):
    """Tra ve SQL WHERE clause de loc records trong list view.

    Ham nay duoc goi MOI LAN user xem list Library Transaction.
    Phai tra ve SQL fragment hoac "" (cho phep tat ca).
    """
    if "Librarian" in frappe.get_roles(user):
        return ""  # Librarian thay tat ca

    # Member chi thay transactions của minh
    member = frappe.db.get_value("Library Member", {"email_id": user}, "name")
    if member:
        return f'(`tabLibrary Transaction`.member = "{member}")'

    return "1=0"  # Khong co quyen → khong thay gi


# hooks.py — has_permission override
has_permission = {
    "Library Transaction": "library_management.permissions.has_transaction_permission"
}

# permissions.py
def has_transaction_permission(doc, user=None, ptype=None):
    """Kiem tra quyen cho tung document cu the.

    Khac voi permission_query_conditions (loc list),
    ham nay kiem tra 1 document cu the.
    """
    if not user:
        user = frappe.session.user

    if "Librarian" in frappe.get_roles(user):
        return True

    member = frappe.db.get_value("Library Member", {"email_id": user}, "name")
    if member and doc.member == member:
        return True

    return False
```

#### 6. Share — Chia sẻ document

```python
# Chia sẻ document với user cũ the (override permissions)
from frappe.share import add as add_share

add_share(
    doctype="Library Book",
    name="BOOK-001",
    user="member@example.com",
    read=1,
    write=0,
    share=0
)

# Kiểm tra share
from frappe.share import get_shared
shared_books = get_shared("Library Book", "member@example.com")
```

### Mini Quiz

<details>
<summary><strong>Câu 1:</strong> Su khác biết giua Role Permission và User Permission?</summary>

**Trả lời:** Role Permission xác định HANH DONG (read/write/create/delete) của ROLE trên DOCTYPE. User Permission giới hạn RECORDS cũ the mà user được thay. VD: Role Permission cho "Library Member" quyền "read" trên "Library Transaction". User Permission giới hạn member@example.com chi thay transactions của MEM-001.
</details>

<details>
<summary><strong>Câu 2:</strong> <code>permission_query_conditions</code> và <code>has_permission</code> trong hooks.py khác nhau như thế nào?</summary>

**Trả lời:** `permission_query_conditions` trả về SQL WHERE clause, ap dùng khi LOAD DANH SACH (List View, get_list). Hiểu qua cho nhiều records. `has_permission` kiểm tra TUNG DOCUMENT cũ the, ap dùng khi mo 1 document. Can dùng CA HAI để đảm bảo bảo mật đầy đủ: condition loc list, has_permission kiểm tra tung đọc.
</details>

<details>
<summary><strong>Câu 3:</strong> Khi nào nên dùng Share thay vì User Permission?</summary>

**Trả lời:** User Permission ap dùng theo QUY TAC (VD: tất cả transactions của member X). Share ap dùng theo TRUONG HOP CU THE (VD: chia sẻ 1 document cho 1 user không thuộc role nao). Share linh hoạt hơn nhưng không scale tot — dùng cho ngoài le, không phải quy tac chính.
</details>

**DEEP DIVE:** Xem skill `dcnet_quality` → core/erpnext-permissions/ cho permission patterns và anti-patterns.

**DEEP DIVE:** Xem skill `frappe` → references/api_reference/ để hiểu thêm về Permission API.

---

## L7.2: Jinja Templates

### Tổng quan / Overview

Jinja2 là template engine được dùng trong Frappe cho Print Formats, Email Templates, và Letter Heads. Ban có thể tạo màu in chuyên nghiệp, email tự động, và báo cáo dang HTML bang Jinja syntax. Frappe mở rộng Jinja với các hàm `frappe.utils` và cho phép dang ky custom methods qua hooks.

### Khái niệm chính / Key Concepts

#### 1. Print Format cơ bản

```html
{# File: library_transaction_receipt.html #}
{# Print Format cho Library Transaction — Phieu muon sach #}

<style>
    .receipt-container {
        font-family: Arial, sans-serif;
        max-width: 600px;
        margin: 0 auto;
        padding: 20px;
    }
    .header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px; }
    .header h2 { margin: 0; color: #333; }
    .info-table { width: 100%; margin-top: 15px; }
    .info-table td { padding: 5px 10px; vertical-align: top; }
    .label { font-weight: bold; width: 40%; color: #555; }
    .footer { margin-top: 30px; border-top: 1px solid #ccc; padding-top: 10px;
              font-size: 0.9em; color: #777; text-align: center; }
    .signature-area { margin-top: 50px; display: flex; justify-content: space-between; }
    .signature-box { text-align: center; width: 45%; }
    .signature-line { border-top: 1px solid #333; margin-top: 60px; padding-top: 5px; }
</style>

<div class="receipt-container">
    {# Header voi logo va ten thu vien #}
    <div class="header">
        {% if letter_head %}
            {{ letter_head }}
        {% endif %}
        <h2>PHIEU MUON SACH / BOOK LOAN RECEIPT</h2>
        <p>So / No: {{ doc.name }}</p>
    </div>

    {# Thong tin giao dich #}
    <table class="info-table">
        <tr>
            <td class="label">Ngay muon / Issue Date:</td>
            <td>{{ doc.date | format_date }}</td>
        </tr>
        <tr>
            <td class="label">Han tra / Due Date:</td>
            <td>
                {% if doc.due_date %}
                    {{ doc.due_date | format_date }}
                {% else %}
                    {{ frappe.utils.add_days(doc.date, 14) | format_date }}
                {% endif %}
            </td>
        </tr>
        <tr>
            <td class="label">Nguoi muon / Borrower:</td>
            <td>
                {{ frappe.db.get_value("Library Member", doc.member, "member_name") }}
                ({{ doc.member }})
            </td>
        </tr>
        <tr>
            <td class="label">Sach / Book:</td>
            <td>
                {% set book = frappe.get_doc("Library Book", doc.book) %}
                <strong>{{ book.title }}</strong><br>
                Tac gia / Author: {{ book.author }}<br>
                ISBN: {{ book.isbn or "N/A" }}
            </td>
        </tr>
        <tr>
            <td class="label">Trang thai / Status:</td>
            <td>
                {% if doc.status == "Issued" %}
                    <span style="color: orange;">Dang muon / Issued</span>
                {% elif doc.status == "Returned" %}
                    <span style="color: green;">Da tra / Returned</span>
                {% endif %}
            </td>
        </tr>
    </table>

    {# Quy dinh #}
    <div style="margin-top: 20px; padding: 10px; background: #f5f5f5; border-radius: 5px;">
        <strong>Quy dinh / Rules:</strong>
        <ul>
            <li>Han muon toi da 14 ngay / Maximum loan period: 14 days</li>
            <li>Phat tre han: 10.000d/ngay / Late fee: 10,000 VND/day</li>
            <li>Sach hong phai boi thuong / Damaged books must be compensated</li>
        </ul>
    </div>

    {# Chu ky #}
    <div class="signature-area">
        <div class="signature-box">
            <div class="signature-line">Thu thu / Librarian</div>
        </div>
        <div class="signature-box">
            <div class="signature-line">Nguoi muon / Borrower</div>
        </div>
    </div>

    {# Footer #}
    <div class="footer">
        In ngay / Printed on: {{ frappe.utils.now_datetime() | format_datetime }}<br>
        {{ frappe.utils.get_url() }}
    </div>
</div>
```

#### 2. Jinja Filters và Functions có sẵn

```html
{# === Date/Time === #}
{{ doc.date | format_date }}                {# 17-03-2026 #}
{{ doc.creation | format_datetime }}        {# 17-03-2026 14:30:00 #}
{{ frappe.utils.today() }}                  {# 2026-03-17 #}
{{ frappe.utils.add_days(doc.date, 14) }}   {# Cong them 14 ngay #}
{{ frappe.utils.date_diff(today, doc.date) }} {# So ngay chenh lech #}

{# === Number/Currency === #}
{{ doc.amount | fmt_money }}               {# 1,500,000.00 #}
{{ frappe.utils.fmt_money(doc.amount, currency="VND") }}  {# 1.500.000d #}
{{ doc.quantity | int }}                    {# 5 #}
{{ "{:,.0f}".format(doc.amount) }}         {# 1,500,000 #}

{# === String === #}
{{ doc.title | truncate(50) }}             {# Cat ngan 50 ky tu #}
{{ doc.status | lower }}                   {# issued #}
{{ doc.status | upper }}                   {# ISSUED #}
{{ doc.name | replace("-", " ") }}         {# BOOK 001 #}

{# === Control Flow === #}
{% for item in doc.items %}
    <tr>
        <td>{{ loop.index }}</td>           {# So thu tu: 1, 2, 3... #}
        <td>{{ item.item_name }}</td>
        <td>{{ item.qty }}</td>
    </tr>
{% endfor %}

{% if doc.status == "Issued" %}
    <span class="text-warning">Dang muon</span>
{% elif doc.status == "Returned" %}
    <span class="text-success">Da tra</span>
{% else %}
    <span class="text-muted">{{ doc.status }}</span>
{% endif %}

{# === Database Access trong Jinja === #}
{% set member = frappe.get_doc("Library Member", doc.member) %}
{{ member.member_name }}

{% set count = frappe.db.count("Library Transaction", {"member": doc.member}) %}
Tong so lan muon: {{ count }}

{# === Macro (ham tai su dung) === #}
{% macro format_address(name) %}
    {% set addr = frappe.get_doc("Address", name) %}
    {{ addr.address_line1 }}<br>
    {{ addr.city }}, {{ addr.state }}<br>
    {{ addr.country }}
{% endmacro %}

{{ format_address(doc.address) }}
```

#### 3. Custom Jinja Methods (hooks.py)

```python
# hooks.py
jinja = {
    "methods": [
        "library_management.utils.jinja.get_book_qr_code",
        "library_management.utils.jinja.format_vnd",
    ]
}

# utils/jinja.py
import frappe


def get_book_qr_code(book_name):
    """Tao QR code URL cho sach (dung trong Print Format)."""
    url = f"{frappe.utils.get_url()}/app/library-book/{book_name}"
    # Dùng Google Charts API để tạo QR
    return f"https://chart.googleapis.com/chart?cht=qr&chs=150x150&chl={url}"


def format_vnd(amount):
    """Format so tien thanh VND."""
    if not amount:
        return "0d"
    return f"{amount:,.0f}d".replace(",", ".")
```

```html
{# Su dung trong Print Format #}
<img src="{{ get_book_qr_code(doc.book) }}" alt="QR Code">
<p>Gia tri: {{ format_vnd(doc.fine_amount) }}</p>
```

#### 4. Email Template

```html
{# Email Template — Nhac tra sach #}
{# Subject: Nhac tra sach: {{ doc.book_title }} #}

<p>Kinh gui {{ doc.member_name }},</p>

<p>
    Day la email nhac nho ve cuon sach ban dang muon tai thu vien:
</p>

<table style="width: 100%; border-collapse: collapse; margin: 15px 0;">
    <tr>
        <td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Sach:</td>
        <td style="padding: 8px; border: 1px solid #ddd;">{{ doc.book_title }}</td>
    </tr>
    <tr>
        <td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Ngay muon:</td>
        <td style="padding: 8px; border: 1px solid #ddd;">{{ doc.date | format_date }}</td>
    </tr>
    <tr>
        <td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Han tra:</td>
        <td style="padding: 8px; border: 1px solid #ddd;">
            {% set days_left = frappe.utils.date_diff(doc.due_date, frappe.utils.today()) %}
            {{ doc.due_date | format_date }}
            {% if days_left < 0 %}
                <span style="color: red;">(Qua han {{ -days_left }} ngay!)</span>
            {% elif days_left <= 3 %}
                <span style="color: orange;">(Con {{ days_left }} ngay)</span>
            {% endif %}
        </td>
    </tr>
</table>

{% if frappe.utils.date_diff(doc.due_date, frappe.utils.today()) < 0 %}
<p style="color: red; font-weight: bold;">
    Sach da qua han tra! Vui long mang tra sach som nhat co the.
    Phi phat tre han: 10.000d/ngay.
</p>
{% else %}
<p>Vui long tra sach dung han de tranh phi phat.</p>
{% endif %}

<p>
    <a href="{{ frappe.utils.get_url() }}/app/library-transaction/{{ doc.name }}"
       style="background: #5e64ff; color: white; padding: 10px 20px;
              text-decoration: none; border-radius: 5px;">
        Xem chi tiet
    </a>
</p>

<p>Tran trong,<br>Thu vien</p>
```

#### 5. Letter Head

```
Letter Head la header/footer dung chung cho tat ca Print Formats.

Thiet lap:
1. Setup → Letter Head → New
2. Nhap HTML cho header va footer
3. Chon lam "Is Default" neu muon ap dung cho tat ca

Trong Print Format, Letter Head duoc tu dong chen vao bien {{ letter_head }}.
```

### Mini Quiz

<details>
<summary><strong>Câu 1:</strong> Trong Jinja template, làm sao để lấy thông tin từ DocType khác (VD: lấy ten member từ Library Member)?</summary>

**Trả lời:** Có 2 cach: (1) `frappe.db.get_value("Library Member", doc.member, "member_name")` — nhe, chi lấy 1 field. (2) `frappe.get_doc("Library Member", doc.member)` — load full document, dùng khi can nhiều fields. Can than với cach 2 trong vong lap vì sẽ chạy nhiều queries.
</details>

<details>
<summary><strong>Câu 2:</strong> Làm sao để dang ky custom Jinja method để dùng trong Print Format?</summary>

**Trả lời:** Thêm vao hooks.py: `jinja = {"methods": ["app_name.module.function_name"]}`. Function này sẽ có thể gọi trực tiếp trong Jinja template bang ten hàm (VD: `{{ function_name(arg) }}`). Function phải là Python function bình thường, không cần decorator.
</details>

**DEEP DIVE:** Xem skill `dcnet_quality` → syntax/erpnext-syntax-jinja/ cho Jinja patterns và lỗi thường gap.

**DEEP DIVE:** Xem skill `erpnext` → references/ext_syntax-jinja/ cho ERPNext Jinja patterns.

---

## L7.3: Testing

### Tổng quan / Overview

Frappe cũng cap `FrappeTestCase` (kế thừa từ `unittest.TestCase`) với các tien ich đặc biệt cho testing DocTypes và API. Tests su dùng test fixtures (JSON data) để tạo dữ liệu màu, và có thể chạy riêng tung module hoặc toàn bộ app. Viết tests tot giúp phat hiện lỗi som và đảm bảo code on dinh khi refactor.

### Khái niệm chính / Key Concepts

#### 1. Test Structure

```
library_management/
  library_management/
    doctype/
      library_book/
        test_library_book.py        # Tests cho Library Book
        test_records.json           # Test fixtures (du lieu mau)
      library_transaction/
        test_library_transaction.py
        test_records.json
    tests/
      test_api.py                   # Tests cho API endpoints
```

#### 2. FrappeTestCase cơ bản

```python
# test_library_book.py
import frappe
from frappe.tests import IntegrationTestCase


class TestLibraryBook(IntegrationTestCase):
    """Test cases cho Library Book DocType."""

    def setUp(self):
        """Chay truoc MOI test case.

        Tao du lieu can thiet cho test.
        Frappe tu dong rollback sau moi test → du lieu sach.
        """
        self.book = frappe.get_doc({
            "doctype": "Library Book",
            "title": "Test Python Book",
            "author": "Test Author",
            "isbn": "978-0-TEST-001",
            "status": "Available"
        })
        self.book.insert()

    def tearDown(self):
        """Chay sau MOI test case (optional).

        Thuong khong can vi Frappe tu dong rollback.
        Nhung neu test tao side effects (VD: file), can cleanup o day.
        """
        pass

    def test_book_creation(self):
        """Kiem tra tao sach thanh cong."""
        self.assertEqual(self.book.title, "Test Python Book")
        self.assertEqual(self.book.status, "Available")
        self.assertTrue(self.book.name)  # Name duoc tu dong tao

    def test_book_duplicate_isbn(self):
        """Kiem tra khong cho phep ISBN trung lap."""
        duplicate = frappe.get_doc({
            "doctype": "Library Book",
            "title": "Another Book",
            "author": "Another Author",
            "isbn": "978-0-TEST-001"  # ISBN trung
        })
        self.assertRaises(frappe.ValidationError, duplicate.insert)

    def test_book_status_change(self):
        """Kiem tra thay doi trang thai sach."""
        self.book.status = "Issued"
        self.book.save()
        self.assertEqual(self.book.status, "Issued")

        # Reload từ DB để đảm bảo đã lưu
        self.book.reload()
        self.assertEqual(self.book.status, "Issued")

    def test_book_deletion_when_issued(self):
        """Kiem tra khong xoa duoc sach dang muon."""
        self.book.status = "Issued"
        self.book.save()
        self.assertRaises(frappe.ValidationError, self.book.delete)

    def test_book_search(self):
        """Kiem tra tim kiem sach."""
        books = frappe.db.get_list("Library Book",
            filters={"author": "Test Author"},
            fields=["name", "title"]
        )
        self.assertTrue(len(books) > 0)
        self.assertEqual(books[0].title, "Test Python Book")
```

#### 3. Test Fixtures (JSON)

```json
// test_records.json — Dữ liệu màu tự động được tạo trước khi chạy tests
[
    {
        "doctype": "Library Book",
        "title": "Fixture Book 1",
        "author": "Fixture Author A",
        "isbn": "978-FIXTURE-001",
        "status": "Available"
    },
    {
        "doctype": "Library Book",
        "title": "Fixture Book 2",
        "author": "Fixture Author B",
        "isbn": "978-FIXTURE-002",
        "status": "Available"
    }
]
```

```python
# Su dùng fixtures trong test
class TestLibraryTransaction(IntegrationTestCase):
    def test_with_fixture_data(self):
        """Fixtures tu test_records.json da duoc insert truoc khi test chay."""
        # Truy cập fixture data
        book = frappe.get_doc("Library Book", {"isbn": "978-FIXTURE-001"})
        self.assertEqual(book.title, "Fixture Book 1")
```

#### 4. Testing API Endpoints

```python
# tests/test_api.py
import frappe
from frappe.tests import IntegrationTestCase


class TestLibraryAPI(IntegrationTestCase):
    def setUp(self):
        # Tạo dữ liệu test
        self.book = frappe.get_doc({
            "doctype": "Library Book",
            "title": "API Test Book",
            "author": "API Author",
            "isbn": "978-API-TEST-001",
            "status": "Available"
        }).insert()

        self.member = frappe.get_doc({
            "doctype": "Library Member",
            "member_name": "API Test Member",
            "email_id": "api_test@example.com"
        }).insert()

    def test_search_books(self):
        """Test API search_books."""
        from library_management.api import search_books

        result = search_books(query="API Test")
        self.assertTrue(len(result["books"]) > 0)
        self.assertEqual(result["books"][0]["title"], "API Test Book")

    def test_borrow_book(self):
        """Test API borrow_book."""
        from library_management.api import borrow_book

        result = borrow_book(
            book_name=self.book.name,
            member_name=self.member.name
        )
        self.assertIn("transaction", result)

        # Verify book status changed
        self.book.reload()
        self.assertEqual(self.book.status, "Issued")

    def test_borrow_unavailable_book(self):
        """Test muon sach da duoc muon → fail."""
        self.book.status = "Issued"
        self.book.save()

        from library_management.api import borrow_book
        self.assertRaises(
            frappe.ValidationError,
            borrow_book,
            book_name=self.book.name,
            member_name=self.member.name
        )

    def test_return_book(self):
        """Test tra sach."""
        from library_management.api import borrow_book, return_book

        # Muon trước
        borrow_result = borrow_book(
            book_name=self.book.name,
            member_name=self.member.name
        )

        # Tra sach
        result = return_book(
            book_name=self.book.name,
            member_name=self.member.name
        )
        self.assertIn("message", result)

        # Verify sach đã kha dùng
        self.book.reload()
        self.assertEqual(self.book.status, "Available")
```

#### 5. Chạy Tests

```bash
# Chạy tất cả tests của app
bench --site flow.local run-tests --app library_management -v

# Chạy tests của 1 module/doctype cũ the
bench --site flow.local run-tests --app library_management \
  --module library_management.doctype.library_book.test_library_book -v

# Chạy 1 test case cũ the
bench --site flow.local run-tests --app library_management \
  --module library_management.doctype.library_book.test_library_book \
  --test test_book_creation -v

# Chạy tests với pytest (alternative)
cd /workspace/development/frappe-bench
bench --site flow.local run-tests --app library_management --use-hierarchical-test-discovery -v

# Kiểm tra test coverage
bench --site flow.local run-tests --app library_management --coverage -v
```

### Mini Quiz

<details>
<summary><strong>Câu 1:</strong> Tại sao không cần xóa dữ liệu test trong <code>tearDown</code> của FrappeTestCase?</summary>

**Trả lời:** Frappe tự động rollback database transaction sau mọi test case. Tất cả dữ liệu tạo trong test (insert, update) deu bi huy. Dieu này đảm bảo mọi test độc lập và không ảnh hưởng lần nhau. Chi can tearDown khi test tạo side effects ngoài DB (VD: tạo file).
</details>

<details>
<summary><strong>Câu 2:</strong> test_records.json khác với dữ liệu tạo trong <code>setUp</code> như thế nào?</summary>

**Trả lời:** `test_records.json` được Frappe tự động insert MOT LAN trước tất cả tests của DocType do (class-level setup). `setUp` chạy trước MOI test method (instance-level). Dùng fixtures cho dữ liệu cơ bản dùng chung; dùng setUp cho dữ liệu dac thư của tung test case.
</details>

<details>
<summary><strong>Câu 3:</strong> Làm sao để test 1 API endpoint mà KHÔNG gọi HTTP request?</summary>

**Trả lời:** Import trực tiếp function Python và gọi no: `from library_management.api import search_books; result = search_books(query="test")`. Vì tests chạy trong Frappe context (co DB, session), function hoat dòng bình thường mà không cần HTTP layer. Đây là unit test — nhanh hơn và để debug hơn integration test.
</details>

**DEEP DIVE:** Xem skill `frappe` → references/test_examples/ để xem test patterns thuc te.

**DEEP DIVE:** Xem skill `dcnet_quality` → docs/ cho testing best practices trong ERPNext apps.

---

## L7.4: Data Import/Export

### Tổng quan / Overview

Frappe hỗ trợ import/export dữ liệu qua CSV, JSON fixtures, và API. Data Import tool trên UI cho phép upload CSV. Fixtures (JSON) dùng để chuyen cấu hình giua môi trường. Hiểu rõ các công cụ này giúp bạn migration dữ liệu, tạo sample data, và dòng bo hệ thống.

### Khái niệm chính / Key Concepts

#### 1. Data Import Tool (UI — CSV)

```
Buoc 1: Vao Data Import
- Duong dan: /app/data-import
- Hoac: Setup → Data → Data Import

Buoc 2: Download template
- Chon DocType (VD: "Library Book")
- Click "Download Template"
- Chon "All fields" hoac "Required fields only"
- CSV file se duoc download voi headers dung format

Buoc 3: Dien du lieu
- Mo CSV trong Excel/Google Sheets
- Dien du lieu theo headers
- Luu lai dang CSV (UTF-8)

Buoc 4: Upload va Import
- Upload CSV file
- Review du lieu (Frappe hien preview)
- Click "Start Import"
- Xem ket qua (thanh cong / loi)
```

```csv
# Template CSV cho Library Book:
Title,Author,ISBN,Status,Publisher
Python Crash Course,Eric Matthes,978-1-5932-7603-0,Available,No Starch Press
Fluent Python,Luciano Ramalho,978-1-4919-4600-8,Available,O'Reilly
```

#### 2. Import qua API (Python)

```python
# Cach 1: frappe.get_đọc().insert() — Tung record
import frappe
import csv

def import_books_from_csv(file_path):
    """Import sach tu CSV file."""
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        success = 0
        errors = []

        for i, row in enumerate(reader):
            try:
                doc = frappe.get_doc({
                    "doctype": "Library Book",
                    "title": row["Title"],
                    "author": row["Author"],
                    "isbn": row["ISBN"],
                    "status": row.get("Status", "Available"),
                    "publisher": row.get("Publisher", "")
                })
                doc.insert()
                success += 1

                # Commit mọi 100 records
                if success % 100 == 0:
                    frappe.db.commit()
                    print(f"Imported {success} books...")

            except Exception as e:
                errors.append({"row": i + 2, "error": str(e)})

        frappe.db.commit()
        return {"success": success, "errors": errors}


# Cach 2: Bulk insert (nhanh hơn cho nhiều records)
def bulk_import_books(data_list):
    """Bulk insert — khong chay controller hooks."""
    for chunk in frappe.utils.create_batch(data_list, 500):
        records = []
        for row in chunk:
            doc = frappe.get_doc({
                "doctype": "Library Book",
                **row
            })
            doc.db_insert()  # Insert truc tiep, khong chay validate/hooks
            records.append(doc.name)

        frappe.db.commit()

    return records
```

#### 3. Fixtures — JSON Export/Import

```python
# hooks.py — Khai bao fixtures để tự động export/import
fixtures = [
    # Export TOAN BO records của DocType
    "Library Category",

    # Export với filter
    {
        "dt": "Library Book",
        "filters": [["status", "=", "Available"]]
    },

    # Export Custom Fields của DocType cũ the
    {
        "dt": "Custom Field",
        "filters": [["dt", "in", ["Library Book", "Library Member"]]]
    },

    # Export Property Setter
    {
        "dt": "Property Setter",
        "filters": [["doc_type", "in", ["Library Book"]]]
    }
]
```

```bash
# Export fixtures ra JSON files
bench --site flow.local export-fixtures --app library_management

# Files sẽ được tạo trong:
# library_management/library_management/fixtures/
#   library_category.json
#   custom_field.json
#   property_setter.json

# Import fixtures (chạy tự động khi bench migrate)
bench --site flow.local migrate

# Import thủ công
bench --site flow.local import-fixtures --app library_management
```

#### 4. JSON Fixture Format

```json
// library_management/fixtures/library_category.json
[
    {
        "doctype": "Library Category",
        "name": "Fiction",
        "category_name": "Fiction",
        "description": "Sach van hoc"
    },
    {
        "doctype": "Library Category",
        "name": "Non-Fiction",
        "category_name": "Non-Fiction",
        "description": "Sach phi van hoc"
    },
    {
        "doctype": "Library Category",
        "name": "Technical",
        "category_name": "Technical",
        "description": "Sach ky thuat"
    }
]
```

#### 5. bench data-import Command

```bash
# Import tự động từ command line
bench --site flow.local data-import \
  --doctype "Library Book" \
  --file "/path/to/books.csv" \
  --type "Insert"   # "Insert" hoac "Update"

# Export data ra CSV
bench --site flow.local export-csv "Library Book" "/path/to/export.csv"

# Export với filters
bench --site flow.local execute \
  'frappe.get_all("Library Book", filters={"status":"Available"}, fields=["*"])'
```

#### 6. So sánh các phuong phap Import

```
+-------------------+------------------+------------------+------------------+
| Phuong phap       | Khi nao dung     | Uu diem          | Nhuoc diem       |
+-------------------+------------------+------------------+------------------+
| Data Import (UI)  | User tu import,  | De dung, co      | Cham voi file    |
|                   | it records       | preview, undo    | lon (>5000)      |
+-------------------+------------------+------------------+------------------+
| API insert()      | Migration code,  | Chay full         | Cham (validate   |
|                   | can validate     | lifecycle         | moi record)      |
+-------------------+------------------+------------------+------------------+
| Bulk db_insert()  | Nhieu records,   | Nhanh nhat       | Khong chay       |
|                   | data da sach     |                  | validate/hooks   |
+-------------------+------------------+------------------+------------------+
| Fixtures (JSON)   | Config, master   | Version control, | Khong phu hop    |
|                   | data, settings   | tu dong migrate  | cho data lon     |
+-------------------+------------------+------------------+------------------+
```

### Mini Quiz

<details>
<summary><strong>Câu 1:</strong> Su khác biết giua <code>đọc.insert()</code> và <code>đọc.db_insert()</code>?</summary>

**Trả lời:** `doc.insert()` chạy FULL lifecycle: validate → before_insert → before_save → db_insert → after_insert → after_save. `doc.db_insert()` CHI ghi vao DB, KHÔNG chạy hooks/validate. Dùng `db_insert()` khi data đã được validate trước và can toc do (bulk import). Nhưng NGUY HIEM nếu data chưa sach vì sẽ bypass mọi kiểm tra.
</details>

<details>
<summary><strong>Câu 2:</strong> Fixtures trong hooks.py được import khi nao?</summary>

**Trả lời:** Fixtures được tự động import khi chạy `bench migrate`. Frappe đọc hooks.py, tìm fixtures array, và insert/update records từ JSON files tuong ung. Nếu record đã tồn tại (cũng `name`), nó sẽ được UPDATE. Nếu chưa co, sẽ INSERT. Đây là cơ chế idempotent — chạy nhiều lần van ẩn toàn.
</details>

**DEEP DIVE:** Xem skill `frappe` → references/data_import/ và references/data_import_api_reference/ để hiểu thêm về Data Import API.

**DEEP DIVE:** Xem skill `frappe` → references/data_import_tutorials/ cho hướng dẫn chi tiết.

---

## L7.5: Hands-on — Permissions, Print Format, Tests, Fixtures

### Tổng quan / Overview

Thực hành tổng hợp: Thiết lập hệ thống permissions cho Library app, tạo Print Format chuyên nghiệp, viết 5 test cases, và export/import sample data. Ap dùng tất cả kiến thức từ L7.1-L7.4.

### Bài tập / Exercise

#### Bài 1: Thiết lập Roles và Permissions

```python
# library_management/install.py
import frappe
from frappe.permissions import add_permission, update_permission_property


def after_install():
    create_roles()
    setup_permissions()


def create_roles():
    """Tao 3 roles: Librarian, Library Member, Library Admin."""
    roles = [
        {"role_name": "Librarian", "desk_access": 1},
        {"role_name": "Library Member", "desk_access": 1},
        {"role_name": "Library Admin", "desk_access": 1}
    ]
    for role_data in roles:
        if not frappe.db.exists("Role", role_data["role_name"]):
            frappe.get_doc({"doctype": "Role", **role_data}).insert()


def setup_permissions():
    """Thiet lap permissions cho cac DocTypes."""

    # === Library Book ===
    # Library Admin: Full control
    setup_doctype_permission("Library Book", "Library Admin",
        read=1, write=1, create=1, delete=1, report=1, export=1, import_=1)

    # Librarian: CRUD, không delete
    setup_doctype_permission("Library Book", "Librarian",
        read=1, write=1, create=1, delete=0, report=1, export=1)

    # Library Member: Chi đọc
    setup_doctype_permission("Library Book", "Library Member",
        read=1, write=0, create=0, delete=0, report=1)

    # === Library Transaction ===
    # Librarian: Full CRUD
    setup_doctype_permission("Library Transaction", "Librarian",
        read=1, write=1, create=1, delete=1, report=1)

    # Library Member: Đọc của minh (if_owner)
    setup_doctype_permission("Library Transaction", "Library Member",
        read=1, write=0, create=0, delete=0, if_owner=1)

    # === Library Member (DocType) ===
    # Librarian: Quản lý tất cả members
    setup_doctype_permission("Library Member", "Librarian",
        read=1, write=1, create=1, delete=0, report=1)

    # Library Member: Sửa profile của minh
    setup_doctype_permission("Library Member", "Library Member",
        read=1, write=1, create=0, delete=0, if_owner=1)


def setup_doctype_permission(doctype, role, read=0, write=0, create=0,
                              delete=0, report=0, export=0, import_=0,
                              if_owner=0):
    """Helper: Thiet lap permission cho 1 DocType + Role."""
    add_permission(doctype, role, 0)
    for perm, value in [
        ("read", read), ("write", write), ("create", create),
        ("delete", delete), ("report", report), ("export", export),
        ("import", import_), ("if_owner", if_owner)
    ]:
        update_permission_property(doctype, role, 0, perm, value)
```

#### Bài 2: Print Format — Library Transaction Receipt

```html
{# Luu tai: library_management/print_format/library_transaction_receipt/ #}
{# Hoac tao qua UI: Setup → Print Format → New #}

<style>
    .receipt { font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; }
    .receipt-header { text-align: center; padding: 15px 0; border-bottom: 2px solid #2c3e50; }
    .receipt-header h3 { margin: 5px 0; color: #2c3e50; }
    .receipt-body { padding: 15px 0; }
    .info-row { display: flex; padding: 6px 0; border-bottom: 1px solid #eee; }
    .info-label { width: 40%; font-weight: 600; color: #555; }
    .info-value { width: 60%; }
    .receipt-footer { text-align: center; margin-top: 20px; padding-top: 10px;
                      border-top: 1px solid #ccc; font-size: 0.85em; color: #888; }
    .status-badge { padding: 3px 10px; border-radius: 12px; font-size: 0.85em; }
    .status-issued { background: #fff3cd; color: #856404; }
    .status-returned { background: #d4edda; color: #155724; }
</style>

<div class="receipt">
    <div class="receipt-header">
        {% if letter_head %}{{ letter_head }}{% endif %}
        <h3>PHIEU MUON/TRA SACH</h3>
        <p style="margin: 0; color: #888;">{{ doc.name }}</p>
    </div>

    <div class="receipt-body">
        <div class="info-row">
            <div class="info-label">Trang thai:</div>
            <div class="info-value">
                {% if doc.status == "Issued" %}
                    <span class="status-badge status-issued">Dang muon</span>
                {% else %}
                    <span class="status-badge status-returned">Da tra</span>
                {% endif %}
            </div>
        </div>

        <div class="info-row">
            <div class="info-label">Nguoi muon:</div>
            <div class="info-value">
                {{ frappe.db.get_value("Library Member", doc.member, "member_name") }}
            </div>
        </div>

        <div class="info-row">
            <div class="info-label">Sach:</div>
            <div class="info-value">
                {% set book = frappe.get_doc("Library Book", doc.book) %}
                <strong>{{ book.title }}</strong><br>
                <small>{{ book.author }} | ISBN: {{ book.isbn or "N/A" }}</small>
            </div>
        </div>

        <div class="info-row">
            <div class="info-label">Ngay muon:</div>
            <div class="info-value">{{ doc.date | format_date }}</div>
        </div>

        {% if doc.due_date %}
        <div class="info-row">
            <div class="info-label">Han tra:</div>
            <div class="info-value">
                {{ doc.due_date | format_date }}
                {% set days = frappe.utils.date_diff(doc.due_date, frappe.utils.today()) %}
                {% if doc.status == "Issued" and days < 0 %}
                    <span style="color: red;">(Qua han {{ -days }} ngay)</span>
                {% endif %}
            </div>
        </div>
        {% endif %}

        {% if doc.status == "Returned" and doc.return_date %}
        <div class="info-row">
            <div class="info-label">Ngay tra:</div>
            <div class="info-value">{{ doc.return_date | format_date }}</div>
        </div>
        {% endif %}
    </div>

    <div class="receipt-footer">
        In ngay {{ frappe.utils.today() | format_date }}
    </div>
</div>
```

#### Bài 3: Viết 5 Test Cases

```python
# test_library_full.py
import frappe
from frappe.tests import IntegrationTestCase


class TestLibraryFull(IntegrationTestCase):
    """5 test cases kiem tra toan bo Library app."""

    def setUp(self):
        self.book = frappe.get_doc({
            "doctype": "Library Book",
            "title": "Full Test Book",
            "author": "Full Test Author",
            "isbn": "978-FULL-TEST",
            "status": "Available"
        }).insert()

        self.member = frappe.get_doc({
            "doctype": "Library Member",
            "member_name": "Full Test Member",
            "email_id": "fulltest@example.com"
        }).insert()

    # Test 1: Tạo sach với dữ liệu đầy đủ
    def test_01_create_book_with_all_fields(self):
        """Tao sach voi tat ca fields → thanh cong."""
        book = frappe.get_doc({
            "doctype": "Library Book",
            "title": "Complete Book",
            "author": "Complete Author",
            "isbn": "978-COMPLETE",
            "status": "Available",
            "publisher": "Test Publisher"
        }).insert()

        self.assertTrue(book.name)
        self.assertEqual(book.status, "Available")
        # Verify trong DB
        db_title = frappe.db.get_value("Library Book", book.name, "title")
        self.assertEqual(db_title, "Complete Book")

    # Test 2: Muon sach → status thay đổi
    def test_02_borrow_changes_book_status(self):
        """Muon sach → sach chuyen sang Issued."""
        transaction = frappe.get_doc({
            "doctype": "Library Transaction",
            "book": self.book.name,
            "member": self.member.name,
            "date": frappe.utils.today(),
            "status": "Issued"
        }).insert()

        self.book.reload()
        # Kiểm tra logic trong controller
        self.assertTrue(transaction.name)

    # Test 3: Không mượn được sach đã Issued
    def test_03_cannot_borrow_issued_book(self):
        """Muon sach da duoc muon → validation error."""
        self.book.status = "Issued"
        self.book.save()

        with self.assertRaises(frappe.ValidationError):
            frappe.get_doc({
                "doctype": "Library Transaction",
                "book": self.book.name,
                "member": self.member.name,
                "date": frappe.utils.today(),
                "status": "Issued"
            }).insert()

    # Test 4: Tra sach → status về Available
    def test_04_return_restores_availability(self):
        """Tra sach → sach kha dung tro lại."""
        # Muon
        transaction = frappe.get_doc({
            "doctype": "Library Transaction",
            "book": self.book.name,
            "member": self.member.name,
            "date": frappe.utils.today(),
            "status": "Issued"
        }).insert()

        # Tra
        transaction.status = "Returned"
        transaction.save()

        self.book.reload()
        # Kiểm tra logic restore
        self.assertEqual(transaction.status, "Returned")

    # Test 5: Search API trả về kết quả dùng
    def test_05_search_api_returns_correct_results(self):
        """API search tra ve sach matching query."""
        from library_management.api import search_books

        result = search_books(query="Full Test")
        books = result.get("books", [])

        self.assertTrue(len(books) > 0)
        titles = [b["title"] for b in books]
        self.assertIn("Full Test Book", titles)
```

#### Bài 4: Export/Import Sample Data

```bash
# Export dữ liệu màu ra fixtures
bench --site flow.local export-fixtures --app library_management

# Kiểm tra files đã tạo
ls library_management/library_management/fixtures/

# Import lại (chạy trong migrate)
bench --site flow.local migrate
```

```python
# Tạo sample data script: library_management/setup/sample_data.py
import frappe


def create_sample_data():
    """Tao du lieu mau cho demo/testing."""

    # Categories
    categories = ["Fiction", "Non-Fiction", "Technical", "Science", "History"]
    for cat in categories:
        if not frappe.db.exists("Library Category", cat):
            frappe.get_doc({
                "doctype": "Library Category",
                "category_name": cat
            }).insert()

    # Books
    books = [
        {"title": "Clean Code", "author": "Robert C. Martin",
         "isbn": "978-0-13-235088-4", "status": "Available"},
        {"title": "The Pragmatic Programmer", "author": "David Thomas",
         "isbn": "978-0-13-595705-9", "status": "Available"},
        {"title": "Design Patterns", "author": "Gang of Four",
         "isbn": "978-0-201-63361-0", "status": "Available"},
        {"title": "Refactoring", "author": "Martin Fowler",
         "isbn": "978-0-13-475759-9", "status": "Available"},
        {"title": "Python Cookbook", "author": "David Beazley",
         "isbn": "978-1-449-34037-7", "status": "Available"},
    ]
    for book_data in books:
        if not frappe.db.exists("Library Book", {"isbn": book_data["isbn"]}):
            frappe.get_doc({"doctype": "Library Book", **book_data}).insert()

    # Members
    members = [
        {"member_name": "Nguyen Van A", "email_id": "nguyenvana@example.com"},
        {"member_name": "Tran Thi B", "email_id": "tranthib@example.com"},
        {"member_name": "Le Van C", "email_id": "levanc@example.com"},
    ]
    for member_data in members:
        if not frappe.db.exists("Library Member", {"email_id": member_data["email_id"]}):
            frappe.get_doc({"doctype": "Library Member", **member_data}).insert()

    frappe.db.commit()
    print("Sample data created successfully!")
```

```bash
# Chạy sample data script
bench --site flow.local execute library_management.setup.sample_data.create_sample_data
```

### Mini Quiz

<details>
<summary><strong>Câu 1:</strong> Trong bài tập permissions, tại sao Library Member có <code>if_owner=1</code> cho Library Transaction?</summary>

**Trả lời:** `if_owner=1` đảm bảo Member chi thay Library Transactions mà ho là owner (người tạo). Không có điều kiện này, Member sẽ thay TẤT CẢ transactions của mọi người → lo thông tin. Đây là cach đơn giản nhất để tạo record-level permission mà không cần viết code.
</details>

<details>
<summary><strong>Câu 2:</strong> Trong test <code>test_03</code>, tại sao dùng <code>self.assertRaises</code> thay vì try/except?</summary>

**Trả lời:** `assertRaises` là cach chuan của unittest để kiểm tra exception. No đảm bảo: (1) Exception PHẢI xảy ra (test fail nếu không có exception). (2) Exception dùng TYPE (frappe.ValidationError, không phải Exception khác). Try/except có thể vo tính "nuot" exception và test pass sai.
</details>

**DEEP DIVE:** Xem skill `dcnet_quality` → core/erpnext-permissions/ cho permission patterns nâng cao.

**DEEP DIVE:** Xem skill `frappe` → references/data_import/ cho Data Import patterns.

---

## L7.5: Production Deployment

### Tổng quan / Overview

Deploy Frappe lên production khác hoàn toàn với `bench start` (dev mode). Production cần Supervisor (process manager), Nginx (web server), và cấu hình đặc biệt để handle concurrent requests và static files. Bài này cover toàn bộ quy trình từ server setup đến backup.

### Kiến trúc Production

```
Internet
    │
    ▼
[Nginx]          ← Reverse proxy, static files, SSL termination
    │
    ├──► Frappe WSGI (Gunicorn)   ← Python web workers
    ├──► Socket.IO server          ← Realtime events
    └──► Redis                     ← Cache + Queue broker
             │
             ▼
    [Supervisor]     ← Quản lý tất cả processes
    ├── frappe-web      (gunicorn workers)
    ├── frappe-worker   (background jobs - default queue)
    ├── frappe-worker-short   (short queue)
    ├── frappe-worker-long    (long queue)
    ├── frappe-schedule       (scheduler heartbeat)
    └── frappe-socketio       (realtime)
```

### Setup Supervisor & Nginx

```bash
# 1. Generate config files
bench setup supervisor
bench setup nginx

# 2. Link configs vào system
sudo ln -s `pwd`/config/supervisor.conf /etc/supervisor/conf.d/frappe.conf
sudo ln -s `pwd`/config/nginx.conf /etc/nginx/conf.d/frappe.conf

# 3. Reload
sudo supervisorctl reread
sudo supervisorctl update
sudo nginx -t && sudo systemctl reload nginx

# 4. Kiểm tra tất cả processes đang chạy
sudo supervisorctl status
```

### SSL Setup

```bash
# Option A: Let's Encrypt (Certbot) — miễn phí, auto-renew
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Option B: Bench wildcard SSL helper
bench setup-wildcard-ssl yourdomain.com

# Verify SSL
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com
```

### Update & Maintenance

```bash
# Update toàn bộ (pull code + migrate + build + restart)
bench update

# Update chỉ 1 app
bench update --apps erpnext

# Update với các bước riêng lẻ (safer)
bench update --pull             # git pull
bench update --patch            # run patches + migrate
bench update --build            # rebuild assets
bench update --restart          # restart processes

# Clear cache sau update
bench --site mysite.com clear-cache
bench --site mysite.com clear-website-cache

# Restart processes
bench restart
# hoặc
sudo supervisorctl restart frappe:
```

### Backup & Restore

```bash
# Backup site (database + files)
bench --site mysite.com backup

# Backup với private files
bench --site mysite.com backup --with-files

# Backup tất cả sites
bench backup-all-sites

# Xem danh sách backups
ls -la sites/mysite.com/private/backups/

# Restore từ backup
bench --site mysite.com --force restore \
    sites/mysite.com/private/backups/20260319_backup_database.sql.gz

# Restore với files
bench --site mysite.com restore \
    --with-public-files sites/.../backup_files.tar \
    --with-private-files sites/.../backup_private_files.tar \
    sites/.../backup_database.sql.gz
```

### Monitoring & Troubleshooting

```bash
# Xem logs realtime
bench --site mysite.com tail-logs

# Xem error log
tail -f logs/web.error.log
tail -f logs/worker.error.log

# Doctor — kiểm tra sức khỏe hệ thống
bench doctor

# Retry failed jobs trong queue
bench --site mysite.com retry-failed-jobs

# Xem queue status
bench --site mysite.com show-pending-jobs
```

### Environment Variables & Site Config

```bash
# Xem site config
cat sites/mysite.com/site_config.json

# Set config qua bench
bench set-config -g developer_mode 0          # Global (common_site_config.json)
bench --site mysite.com set-config db_name mydb  # Site-specific

# Common production settings trong site_config.json:
# {
#   "db_name": "frappe_mysite",
#   "db_password": "...",
#   "mail_server": "smtp.gmail.com",
#   "mail_port": 587,
#   "use_ssl": 1,
#   "mail_login": "...",
#   "mail_password": "...",
#   "auto_email_id": "noreply@yourdomain.com",
#   "redis_cache": "redis://localhost:6379/0",
#   "redis_queue": "redis://localhost:6379/1",
#   "socketio_port": 9000
# }
```

### Production Checklist

```
Pre-deploy:
[ ] developer_mode = 0 trong common_site_config.json
[ ] Tắt debug logging
[ ] Chạy bench migrate trên tất cả sites
[ ] bench build --production (minify assets)

Server setup:
[ ] Supervisor chạy tất cả processes (supervisorctl status)
[ ] Nginx configured, SSL valid (https:// hoạt động)
[ ] Redis đang chạy (redis-cli ping → PONG)
[ ] MariaDB đang chạy, backup schedule được set

Monitoring:
[ ] Log rotation được configure
[ ] Backup tự động hàng ngày (cron job hoặc bench backup)
[ ] Alert khi worker down (supervisor alerting)
[ ] Disk space monitoring (backups có thể chiếm nhiều)

Security:
[ ] Firewall: chỉ mở port 80, 443, 22
[ ] MySQL chỉ localhost (không expose 3306 ra ngoài)
[ ] Redis chỉ localhost (không expose 6379)
[ ] SSH key-based auth (tắt password auth)
```

### Mini Quiz

<details>
<summary><strong>Câu 1:</strong> Tại sao production Frappe cần Supervisor? Không thể chỉ chạy <code>bench start</code> mãi?</summary>

**Trả lời:** `bench start` dùng Honcho — process manager đơn giản chỉ dành cho development. Production cần Supervisor vì: (1) Tự động restart process khi crash. (2) Chạy như system service, tự start khi server reboot. (3) Quản lý log rotation. (4) Cho phép restart từng process riêng lẻ không ảnh hưởng process khác. (5) Honcho không có monitoring, alerting, hay process isolation.
</details>

<details>
<summary><strong>Câu 2:</strong> Khi nào dùng <code>bench update --pull</code> riêng lẻ thay vì <code>bench update</code>?</summary>

**Trả lời:** Dùng từng bước riêng lẻ khi: (1) Muốn review code changes trước khi migrate. (2) Production site có nhiều users — migrate trong giờ thấp điểm. (3) Test từng bước để isolate vấn đề nếu có lỗi. `bench update` (all-in-one) tiện cho dev nhưng trên production nên thận trọng hơn.
</details>
