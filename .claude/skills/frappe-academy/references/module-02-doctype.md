# Module 2: DocType Mastery

> **Mục tiêu:** Thành thạo DocType — từ khai báo, field types, naming rules, child tables, đến workflow. DocType là trung tâm của mọi thứ trong Frappe.
> **Thời lượng:** 6 lessons | **Độ khó:** Beginner-Intermediate
> **Yêu cầu:** Hoàn thành Module 1, app `frappe_learn` đã cài trên site

---

## L2.1: DocType là gì?

### Tổng quan
DocType là đơn vị cơ bản nhất trong Frappe — nó đồng thời là **Model** (database table), **View** (form UI), và **Controller** (Python logic). Khi bạn tạo 1 DocType, Frappe tự động tạo table trong DB, REST API, form view, list view, và permission system. So sánh với Django: DocType = Model + ModelForm + ModelAdmin gộp lại.

### Key Concepts

#### 1. DocType = Model + View + Controller

```
DocType "Library Book"
       │
       ├── Model (Auto-generated)
       │   └── Database table: `tabLibrary Book`
       │       ├── name (VARCHAR) — primary key
       │       ├── title (VARCHAR)
       │       ├── author (VARCHAR)
       │       ├── isbn (VARCHAR)
       │       ├── status (VARCHAR)
       │       └── ... standard fields (owner, creation, modified, etc.)
       │
       ├── View (Auto-generated)
       │   ├── Form View: /app/library-book/BOOK-001
       │   ├── List View: /app/library-book
       │   └── Report View: /app/query-report/...
       │
       └── Controller (Optional)
           └── library_book.py → class LibraryBook(Document)
               ├── validate()
               ├── before_save()
               ├── on_update()
               └── on_trash()
```

#### 2. DocType Files

```
my_app/library/doctype/library_book/
├── library_book.json       # ⭐ DocType definition (metadata)
│                           #    fields, permissions, naming, settings
├── library_book.py         # Controller (Python class)
├── library_book.js         # Client Script (form behavior)
├── library_book_list.js    # List View customization (optional)
├── library_book_calendar.js # Calendar View (optional)
├── library_book_dashboard.py # Dashboard links (optional)
├── test_library_book.py    # Unit tests
└── __init__.py
```

#### 3. Standard Fields (Tự động co)
Mỗi DocType tự động có các fields sau — KHÔNG cần khai báo:

| Field | Type | Mô tả |
|-------|------|-------|
| `name` | VARCHAR(140) | Primary key (unique ID) |
| `owner` | VARCHAR(140) | User tạo document |
| `creation` | DATETIME | Thoi gian tạo |
| `modified` | DATETIME | Thoi gian sửa cuoi |
| `modified_by` | VARCHAR(140) | User sửa cuoi |
| `docstatus` | INT | 0=Draft, 1=Submitted, 2=Cancelled |
| `idx` | INT | Sort order |
| `_user_tags` | TEXT | User tags |
| `_comments` | TEXT | Comments |
| `_assign` | TEXT | Assigned users |
| `_liked_by` | TEXT | Users liked |

#### 4. DocType Types

| Type | `is_submittable` | `istable` | `issingle` | Mô tả |
|------|:-:|:-:|:-:|-------|
| **Normal** | 0 | 0 | 0 | CRUD cơ bản (VD: Customer, Item) |
| **Submittable** | 1 | 0 | 0 | Có workflow Draft→Submit→Cancel (VD: Sales Order, Invoice) |
| **Child Table** | 0 | 1 | 0 | Rows trong parent DocType (VD: Sales Order Item) |
| **Single** | 0 | 0 | 1 | Chi có 1 record — dùng cho Settings (VD: System Settings) |
| **Virtual** | — | — | — | Không có DB table, data từ code |

### Code Examples

```bash
# Tạo DocType bang bench (trong devcontainer)
cd /workspace/development/frappe-bench

# Cach 1: Tạo qua UI
# Truy cập http://flow.local:8000/app/doctype/new
# Điền ten "Library Book", thêm fields, Save

# Cach 2: Tạo bang code (tạo file JSON + Python)
# Xem phần Hands-on (L2.6) để có hướng dẫn chi tiết

# Xem DocType metadata từ console
bench --site flow.local console
```

```python
# Trong bench console:

# Xem DocType definition
meta = frappe.get_meta("Sales Order")
print(meta.fields)  # Tat ca fields
print(meta.get_field("customer"))  # 1 field cu the
print(meta.is_submittable)  # True

# Xem table structure
frappe.db.sql("DESCRIBE `tabSales Order`", as_dict=True)

# Tạo document mới
doc = frappe.get_doc({
    "doctype": "ToDo",
    "description": "Test from console",
    "status": "Open"
})
doc.insert()
frappe.db.commit()
print(f"Created: {doc.name}")

# Đọc document
doc = frappe.get_doc("ToDo", doc.name)
print(doc.description)

# Sửa document
doc.status = "Closed"
doc.save()
frappe.db.commit()

# Xóa document
frappe.delete_doc("ToDo", doc.name)
frappe.db.commit()
```

### Mini Quiz

<details>
<summary>Q1: DocType "Sales Order" có `is_submittable=1`. Document có thể ở những trạng thái nao?</summary>

**A:** 3 trạng thái theo `docstatus`: **0 = Draft** (đang soạn), **1 = Submitted** (đã xác nhận, không sửa được fields fields), **2 = Cancelled** (da huy). Luong: Draft -> Submit -> Cancel. KHÔNG THỂ quay lại từ Cancel về Draft — phải tạo document mới (Amend).
</details>

<details>
<summary>Q2: Bạn muốn lưu Settings cho app (chi 1 record duy nhất). Dùng DocType type nao?</summary>

**A:** **Single DocType** (`issingle=1`). Ví dụ: "Library Settings" với fields nhu `max_borrow_days`, `late_fee_per_day`. Truy cập: `frappe.get_single("Library Settings")`. Trong DB, Single DocType lưu trong table `tabSingles` (không tạo table riêng).
</details>

### Skill References

- **DEEP DIVE:** Xem skill `frappe` -> `references/domains/` để hiểu các domain-specific DocType patterns
- **DEEP DIVE:** Xem skill `erpnext` để hiểu cach ERPNext to chuc DocTypes theo business modules

---

## L2.2: Field Types

### Tổng quan
Frappe có ~35 field types khác nhau, từ cơ bản (Data, Int) đến phức tạp (Dynamic Link, Table MultiSelect). Chọn dùng field type rat quan trọng — nó quyết định UI rendering, validation, storage, và search behavior. Bài này cover tất cả field types quan trọng và khi nào nên dùng.

### Key Concepts

#### 1. Field Types Reference

**Text & String Fields:**

| Type | DB Column | UI | Khi nào dùng |
|------|-----------|-------|-------------|
| `Data` | VARCHAR(140) | Text input | Ten, ma, thông tin ngan |
| `Small Text` | TEXT | Textarea (nhỏ) | Ghi chu ngan |
| `Text` | LONGTEXT | Textarea | Nội dùng dai |
| `Text Editor` | LONGTEXT | Rich text (Quill) | Nội dùng có format HTML |
| `Code` | LONGTEXT | Code editor (CodeMirror) | JSON, Python, JS |
| `Password` | VARCHAR(140) | Password input | Mật khẩu (encrypted) |
| `Read Only` | VARCHAR(140) | Read-only text | Hiển thị, không sửa |
| `HTML` | — | Raw HTML | Custom UI trong form |
| `Markdown Editor` | LONGTEXT | Markdown + preview | Documentation |

**Number Fields:**

| Type | DB Column | UI | Khi nào dùng |
|------|-----------|-------|-------------|
| `Int` | INT(11) | Number input | Số nguyen (số lượng, đếm) |
| `Float` | DECIMAL(21,9) | Number input | Số thap phần (ty le) |
| `Currency` | DECIMAL(21,9) | Number + currency symbol | Tiền tệ (gia, thành tiền) |
| `Percent` | DECIMAL(21,9) | Number + % | Phần tram (chiết khấu, thue) |
| `Rating` | DECIMAL(21,9) | Star rating | Danh gia |
| `Duration` | DECIMAL(21,9) | Duration picker | Thoi gian |

**Link & Relationship Fields:**

| Type | DB Column | UI | Khi nào dùng |
|------|-----------|-------|-------------|
| `Link` | VARCHAR(140) | Autocomplete | Liên kết đến DocType khác |
| `Dynamic Link` | VARCHAR(140) | Autocomplete (dynamic) | Link đến nhiều DocTypes |
| `Table` | — | Child table | Danh sach rows (1-to-many) |
| `Table MultiSelect` | — | Tag-style multi select | Chọn nhiều items từ DocType |

**Date & Time Fields:**

| Type | DB Column | UI | Khi nào dùng |
|------|-----------|-------|-------------|
| `Date` | DATE | Date picker | Ngay (không gio) |
| `Datetime` | DATETIME(6) | Date + time picker | Ngay và gio |
| `Time` | TIME(6) | Time picker | Chi gio |

**Selection Fields:**

| Type | DB Column | UI | Khi nào dùng |
|------|-----------|-------|-------------|
| `Select` | VARCHAR(140) | Dropdown | Chọn 1 từ danh sách cố định |
| `Check` | INT(1) | Checkbox | Boolean (0/1) |
| `Autocomplete` | VARCHAR(140) | Autocomplete text | Nhập + gợi ý (không bắt buộc match) |

**File & Media Fields:**

| Type | DB Column | UI | Khi nào dùng |
|------|-----------|-------|-------------|
| `Attach` | TEXT | File upload | 1 file |
| `Attach Image` | TEXT | Image upload + preview | 1 anh |
| `Image` | TEXT | Image display | Hiển thị anh (read-only) |

**Layout Fields (không lưu DB):**

| Type | Mô tả |
|------|-------|
| `Section Break` | Bat đầu section mọi (co label) |
| `Column Break` | Chia cột trong section |
| `Tab Break` | Tạo tab mới (Frappe v14+) |

#### 2. Link Field — Quan trọng nhất

```json
// Trong DocType JSON:
{
    "fieldname": "customer",
    "fieldtype": "Link",
    "options": "Customer",    // Ten DocType liên kết
    "label": "Customer",
    "reqd": 1                 // Bat bước
}
```

Link field tự động:
- Tạo autocomplete UI với search
- Validate giá trị tồn tại trong target DocType
- Tạo relationship để truy vấn

```python
# Lấy giá trị qua Link
doc = frappe.get_doc("Sales Order", "SO-001")
customer_name = doc.customer  # Tra ve `name` cua Customer

# Lấy thêm thông tin từ linked DocType
customer_doc = frappe.get_doc("Customer", doc.customer)
print(customer_doc.customer_name)

# Hoặc dùng fetch_from (tự động copy field)
# Trong DocType JSON, field "customer_name" co:
#   "fetch_from": "customer.customer_name"
# → Tự động fill khi chọn customer
```

#### 3. Dynamic Link — Liên kết linh hoạt

```json
// Khi không biết trước link đến DocType nao
// Ví dụ: field "party" có thể là Customer HOẶC Supplier
[
    {
        "fieldname": "party_type",
        "fieldtype": "Link",
        "options": "DocType",
        "label": "Party Type"
    },
    {
        "fieldname": "party",
        "fieldtype": "Dynamic Link",
        "options": "party_type",     // Field chưa ten DocType
        "label": "Party"
    }
]
// Nếu party_type = "Customer" → party autocomplete từ Customer
// Nếu party_type = "Supplier" → party autocomplete từ Supplier
```

#### 4. Table Field — Child Table

```json
{
    "fieldname": "items",
    "fieldtype": "Table",
    "options": "Library Transaction Item",  // Ten Child DocType
    "label": "Items"
}
```

### Code Examples

```python
# Trong bench console — khao sat field types

# Xem tất cả fields của 1 DocType
meta = frappe.get_meta("Sales Order")
for f in meta.fields:
    print(f"{f.fieldname:30s} {f.fieldtype:20s} {f.options or ''}")

# Đếm số field types dùng trong ERPNext
from collections import Counter
all_fields = frappe.db.sql("""
    SELECT fieldtype, COUNT(*) as cnt
    FROM `tabDocField`
    GROUP BY fieldtype
    ORDER BY cnt DESC
""", as_dict=True)
for f in all_fields[:10]:
    print(f"{f.fieldtype:20s} {f.cnt}")

# Xem field có fetch_from
fields_with_fetch = frappe.db.sql("""
    SELECT parent, fieldname, fetch_from
    FROM `tabDocField`
    WHERE fetch_from IS NOT NULL AND fetch_from != ''
    LIMIT 10
""", as_dict=True)
for f in fields_with_fetch:
    print(f"{f.parent}.{f.fieldname} ← {f.fetch_from}")
```

### Mini Quiz

<details>
<summary>Q1: Bạn muốn lưu gia sản phẩm (VND). Dùng field type nao: Float, Currency, hay Int?</summary>

**A:** **Currency**. No lưu dang DECIMAL(21,9) và tự động format theo currency của hệ thống (VD: "2.500.000d"). Float không có currency formatting. Int mất phần thap phần.
</details>

<details>
<summary>Q2: Field "party" có thể link đến Customer hoặc Supplier. Dùng field type nao?</summary>

**A:** **Dynamic Link**. Can 2 fields: (1) `party_type` — Link field tro đến DocType, (2) `party` — Dynamic Link field với `options` = "party_type". Khi chọn party_type = "Customer", field party sẽ autocomplete từ Customer list.
</details>

<details>
<summary>Q3: Section Break, Column Break, Tab Break có lưu data trong database không?</summary>

**A:** **KHÔNG**. Đây là layout fields — chi ảnh hưởng cach hiển thị form, không tạo column trong database. Chung giúp to chuc form UI đẹp hon.
</details>

### Skill References

- **DEEP DIVE:** Xem skill `frappe` -> `references/desk/` để hiểu cach form rendering hoat dong
- **DEEP DIVE:** Xem skill `dcnet_quality` -> `syntax/erpnext-syntax-controllers/` để hiểu cach xử lý fields trong controller

---

## L2.3: Naming Rules

### Tổng quan
Mỗi document trong Frappe có 1 `name` — là primary key duy nhất. Frappe hỗ trợ nhiều cach đặt ten tự động (autoname). Chọn dùng naming rule ảnh hưởng đến UX, performance, và data management. Bài này giai thich tất cả autoname options và uu nhược điểm.

### Key Concepts

#### 1. Autoname Options

| Option | Ví dụ `name` | Khi nào dùng |
|--------|------------|-------------|
| `hash` | `a1b2c3d4e5` | Internal records, không cần đọc name |
| `autoincrement` | `1`, `2`, `3` | Don gian, nhanh, nhưng không đẹp |
| `naming_series:PREFIX-.####` | `BOOK-0001` | Business documents (SO, PO, INV) |
| `field:title` | `Harry Potter` | Name = giá trị của 1 field (phải unique) |
| `format:LIB-{title}-{##}` | `LIB-Fiction-01` | Pattern phức tạp |
| `Prompt` | User nhập | Khi user mượn từ đặt ten |
| Python override | Bat ky | Logic phức tạp trong controller |

#### 2. naming_series — Phổ biến nhất cho business docs

```json
// Trong DocType JSON:
{
    "autoname": "naming_series:",
    "fields": [
        {
            "fieldname": "naming_series",
            "fieldtype": "Select",
            "options": "BOOK-.YYYY.-.####\nBOOK-.####\nLIB-.####",
            "label": "Series",
            "default": "BOOK-.YYYY.-.####"
        }
    ]
}
```

**Naming Series Patterns:**

| Pattern | Ví dụ | Mô tả |
|---------|-------|-------|
| `####` | `0001` | Số từ tăng, 4 chữ số |
| `.YYYY.` | `2026` | Nam hiện tại |
| `.YY.` | `26` | Nam 2 chữ số |
| `.MM.` | `03` | Thang |
| `.DD.` | `17` | Ngay |
| `BOOK-.YYYY.-.####` | `BOOK-2026-0001` | Phoi hop |

#### 3. field-based naming

```json
// name = giá trị của field "title"
{
    "autoname": "field:title"
}
// Document với title "Harry Potter" → name = "Harry Potter"
// ⚠️ Nếu trung → lỗi! Phải đảm bảo unique
```

#### 4. format-based naming

```json
// Pattern phức tạp hon
{
    "autoname": "format:LIB-{category}-{##}"
}
// category = "Fiction" → name = "LIB-Fiction-01", "LIB-Fiction-02"
```

#### 5. Python override (trong controller)

```python
# library_book.py
class LibraryBook(Document):
    def autoname(self):
        """Custom naming logic"""
        # Ví dụ: ISBN làm ten
        if self.isbn:
            self.name = f"BOOK-{self.isbn}"
        else:
            # Fallback về naming series
            from frappe.model.naming import set_name_by_naming_series
            set_name_by_naming_series(self)
```

#### 6. Amend (chi cho Submittable DocTypes)

```
Khi Cancel + Amend 1 Submittable doc:
Original:  SO-2026-0001
Amended:   SO-2026-0001-1    (them suffix -1)
Amended 2: SO-2026-0001-2   (them suffix -2)
```

### Code Examples

```python
# Trong bench console:

# Xem naming rule của 1 DocType
meta = frappe.get_meta("Sales Order")
print(f"autoname: {meta.autoname}")
# → "naming_series:"

# Xem naming series options
ns_field = meta.get_field("naming_series")
print(f"options: {ns_field.options}")

# Xem current counter cho 1 series
current = frappe.db.get_value("Series", "SO-.YYYY.-", "current")
print(f"SO-.YYYY.- current: {current}")

# Test naming manually
from frappe.model.naming import make_autoname
name = make_autoname("BOOK-.YYYY.-.####")
print(f"Generated name: {name}")

# Test format naming
from frappe.model.naming import make_autoname
name = make_autoname("format:LIB-{##}", doc=None)
print(f"Generated name: {name}")
```

### Mini Quiz

<details>
<summary>Q1: Naming series "PO-.YYYY.-.####" sẽ tạo name như nào vao tháng 3/2026?</summary>

**A:** `PO-2026-0001`, `PO-2026-0002`, etc. `.YYYY.` thay bang năm hiện tại, `.####` là số từ tăng 4 chữ số. Counter reset mọi năm vì có `.YYYY.` trong pattern.
</details>

<details>
<summary>Q2: Dùng `field:email` làm autoname. Có vấn đề gì có thể xảy ra?</summary>

**A:** 2 vấn đề chính: (1) **Duplicate** — 2 records cũng email sẽ lỗi. (2) **Rename cascade** — nếu user sửa email, name cũng phải thay đổi, ảnh hưởng tất cả Link fields tro đến document này. Tốt hơn nên dùng `hash` hoặc `naming_series` và đặt email là field bình thường với `unique=1`.
</details>

### Skill References

- **DEEP DIVE:** Xem skill `erpnext` để hiểu naming conventions của các business DocTypes (SO, PO, SI, PI, etc.)
- **DEEP DIVE:** Xem skill `frappe` -> `references/patterns/` để hiểu naming best practices

---

## L2.4: Child Tables

### Tổng quan
Child Tables (hay `Table` field) là cach Frappe mô hình hoa quan he 1-to-many. Ví dụ: 1 Sales Order có nhiều Items — mọi item là 1 row trong child table "Sales Order Item". Child DocType không tồn tại độc lập — nó luôn gan với parent. Bài này giai thich cach tạo, CRUD, và nhưng lưu ý quan trọng.

### Key Concepts

#### 1. Parent-Child Relationship

```
Parent DocType: Sales Order (SO-001)
    │
    ├── Child Row 1: Sales Order Item (name=hash, idx=1)
    │   ├── parenttype = "Sales Order"
    │   ├── parentfield = "items"
    │   ├── parent = "SO-001"
    │   ├── item_code = "ITEM-A"
    │   └── qty = 10
    │
    ├── Child Row 2: Sales Order Item (name=hash, idx=2)
    │   ├── parenttype = "Sales Order"
    │   ├── parentfield = "items"
    │   ├── parent = "SO-001"
    │   ├── item_code = "ITEM-B"
    │   └── qty = 5
    │
    └── ...
```

**Standard fields của Child DocType:**

| Field | Mô tả |
|-------|-------|
| `name` | Unique ID (hash) |
| `parent` | Name của parent document |
| `parenttype` | DocType của parent |
| `parentfield` | Fieldname trong parent chưa table này |
| `idx` | Thứ tự row (1, 2, 3...) |

#### 2. Tạo Child DocType

```json
// library_transaction_item.json — Child DocType
{
    "name": "Library Transaction Item",
    "istable": 1,          // ← QUAN TRỌNG: đánh dấu là child table
    "fields": [
        {
            "fieldname": "book",
            "fieldtype": "Link",
            "options": "Library Book",
            "label": "Book",
            "in_list_view": 1,    // Hiển thị trong table view
            "reqd": 1
        },
        {
            "fieldname": "return_date",
            "fieldtype": "Date",
            "label": "Return Date",
            "in_list_view": 1
        }
    ]
}
```

```json
// Trong parent DocType (Library Transaction):
{
    "fieldname": "items",
    "fieldtype": "Table",
    "options": "Library Transaction Item",  // Ten child DocType
    "label": "Books"
}
```

#### 3. CRUD Operations trên Child Rows

```python
# === THEM ROW ===
parent = frappe.get_doc("Library Transaction", "LT-001")

# Cach 1: append()
row = parent.append("items", {
    "book": "BOOK-001",
    "return_date": "2026-04-01"
})
parent.save()

# Cach 2: Khi tạo document mới
doc = frappe.get_doc({
    "doctype": "Library Transaction",
    "member": "MEM-001",
    "items": [
        {"book": "BOOK-001", "return_date": "2026-04-01"},
        {"book": "BOOK-002", "return_date": "2026-04-15"}
    ]
})
doc.insert()

# === DOC ROW ===
for item in parent.items:
    print(f"Row {item.idx}: {item.book} - due {item.return_date}")

# === SUA ROW ===
parent.items[0].return_date = "2026-05-01"
parent.save()

# === XOA ROW ===
# Xóa row đầu tiên
parent.items.pop(0)
parent.save()

# Xóa tất cả rows
parent.items = []
parent.save()

# === TIM ROW ===
# Tìm row có book = "BOOK-001"
matching = [r for r in parent.items if r.book == "BOOK-001"]
```

#### 4. Lưu ý quan trọng

```python
# ⚠️ KHÔNG query child table trực tiếp rồi modify
# SAI:
row = frappe.get_doc("Library Transaction Item", "hash-abc")
row.return_date = "2026-05-01"
row.save()  # Co the gay loi hoac khong trigger parent validation

# DUNG:
parent = frappe.get_doc("Library Transaction", "LT-001")
for item in parent.items:
    if item.name == "hash-abc":
        item.return_date = "2026-05-01"
parent.save()  # Trigger parent validate + on_update

# ⚠️ idx tự động re-index khi save parent
# Nếu xóa row 2 trong 5 rows, idx sẽ tự động thành 1,2,3,4

# ⚠️ Child DocType KHÔNG có permissions riêng
# Permission theo parent DocType
```

### Code Examples

```python
# Trong bench console:

# Xem child table structure
meta = frappe.get_meta("Sales Order Item")
print(f"istable: {meta.istable}")  # True
for f in meta.fields[:5]:
    print(f"  {f.fieldname}: {f.fieldtype}")

# Đếm số rows trong 1 Sales Order
so = frappe.get_doc("Sales Order", "SO-00001")
print(f"So dong items: {len(so.items)}")

# Query child table trực tiếp (read-only)
items = frappe.db.sql("""
    SELECT parent, item_code, qty, rate, amount
    FROM `tabSales Order Item`
    WHERE parent = 'SO-00001'
    ORDER BY idx
""", as_dict=True)
for item in items:
    print(f"  {item.item_code}: {item.qty} x {item.rate} = {item.amount}")

# Tinh tong amount
total = frappe.db.sql("""
    SELECT SUM(amount) as total
    FROM `tabSales Order Item`
    WHERE parent = 'SO-00001'
""")[0][0]
print(f"Total: {total}")
```

### Mini Quiz

<details>
<summary>Q1: Child DocType có `istable=1`. No khác DocType thường ở điểm nao?</summary>

**A:** Child DocType: (1) không có form view riêng — chi hiển thị nhu rows trong parent form, (2) không có list view, (3) không có permissions riêng — theo parent, (4) có thêm standard fields: `parent`, `parenttype`, `parentfield`, `idx`, (5) `name` luôn là hash (không có autoname).
</details>

<details>
<summary>Q2: Bạn muốn thêm 1 row vao child table "items" của đọc đã tồn tại. Dùng lenh gi?</summary>

**A:** `doc.append("items", {"field1": "value1", ...})` rồi `doc.save()`. PHẢI save parent để persist. KHÔNG nên trực tiếp insert vao DB vì sẽ miss validation và events.
</details>

### Skill References

- **DEEP DIVE:** Xem skill `erpnext` để hiểu cach ERPNext dùng child tables (Sales Order Item, Purchase Order Item, etc.)
- **DEEP DIVE:** Xem skill `dcnet_quality` -> `core/` để hiểu database patterns cho child tables

---

## L2.5: Workflow

### Tổng quan
Frappe Workflow cho phép định nghĩa trạng thái (states) và chuyển đổi (transitions) cho documents — thay vì chi có Draft/Submitted/Cancelled. Ví dụ: Sales Order có thể di qua Pending Approval -> Manager Approved -> Director Approved -> Submitted. Bài này giai thich cach tạo workflow, conditions, và actions.

### Key Concepts

#### 1. Workflow Components

```
Workflow "Sales Order Approval"
    │
    ├── States (trang thai)
    │   ├── Pending Review    (doc_status=0, style=Orange)
    │   ├── Approved          (doc_status=0, style=Blue)
    │   ├── Rejected          (doc_status=0, style=Red)
    │   └── Submitted         (doc_status=1, style=Green)
    │
    ├── Transitions (chuyen doi)
    │   ├── Pending Review → Approved    (Role: Sales Manager, Action: Approve)
    │   ├── Pending Review → Rejected    (Role: Sales Manager, Action: Reject)
    │   ├── Approved → Submitted         (Role: Sales Manager, Action: Submit)
    │   └── Rejected → Pending Review    (Role: Sales User, Action: Revise)
    │
    └── Conditions (dieu kien — optional)
        └── "Approve" chi khi grand_total < 100000000
```

#### 2. Workflow DocType Definition

```python
# Tạo Workflow qua code
workflow = frappe.get_doc({
    "doctype": "Workflow",
    "workflow_name": "Library Book Approval",
    "document_type": "Library Book",        # DocType ap dung
    "is_active": 1,
    "send_email_alert": 1,

    # Workflow States
    "states": [
        {
            "state": "Pending Review",
            "doc_status": 0,
            "allow_edit": "Librarian",       # Role duoc phep sua o state nay
            "style": "Warning"               # UI style: Primary, Success, Warning, Danger, Info
        },
        {
            "state": "Approved",
            "doc_status": 0,
            "allow_edit": "Library Manager",
            "style": "Success"
        },
        {
            "state": "Rejected",
            "doc_status": 0,
            "allow_edit": "Librarian",
            "style": "Danger"
        }
    ],

    # Workflow Transitions
    "transitions": [
        {
            "state": "Pending Review",
            "action": "Approve",
            "next_state": "Approved",
            "allowed": "Library Manager",     # Role duoc phep thuc hien action
            "condition": "doc.category != ''"  # Python condition (optional)
        },
        {
            "state": "Pending Review",
            "action": "Reject",
            "next_state": "Rejected",
            "allowed": "Library Manager"
        },
        {
            "state": "Rejected",
            "action": "Revise",
            "next_state": "Pending Review",
            "allowed": "Librarian"
        }
    ]
})
workflow.insert()
```

#### 3. Workflow State Field

```
Khi gan Workflow cho 1 DocType, Frappe tu dong:
1. Them field "workflow_state" vao DocType
2. Hien thi action buttons tren form (Approve, Reject, etc.)
3. An nut Save/Submit/Cancel mac dinh (thay bang workflow actions)
4. Enforce permissions theo state + role
```

#### 4. Workflow trong Code

```python
# Check workflow state
doc = frappe.get_doc("Library Book", "BOOK-001")
print(doc.workflow_state)  # "Pending Review"

# Apply workflow action
from frappe.model.workflow import apply_workflow
apply_workflow(doc, "Approve")
# → doc.workflow_state = "Approved"

# Get allowed transitions cho user hiện tại
from frappe.model.workflow import get_transitions
transitions = get_transitions(doc)
for t in transitions:
    print(f"Action: {t.action} → {t.next_state}")

# Check if user có quyền thuc hiện action
from frappe.model.workflow import has_approval_access
can_approve = has_approval_access(frappe.session.user, doc)
```

### Code Examples

```python
# Trong bench console — khao sat workflows hiện co

# Xem tất cả workflows
workflows = frappe.get_all("Workflow",
    fields=["name", "document_type", "is_active"]
)
for w in workflows:
    print(f"{w.name}: {w.document_type} (active={w.is_active})")

# Xem chi tiết 1 workflow
wf = frappe.get_doc("Workflow", "Library Book Approval")
print("States:")
for s in wf.states:
    print(f"  {s.state} (docstatus={s.doc_status}, edit={s.allow_edit})")
print("Transitions:")
for t in wf.transitions:
    print(f"  {t.state} --[{t.action}]--> {t.next_state} (by {t.allowed})")
```

### Mini Quiz

<details>
<summary>Q1: Workflow state "Approved" có doc_status=0. Document đã Submit chưa?</summary>

**A:** **Chưa**. `doc_status=0` = Draft. Document đã "Approved" nhưng van ở trạng thái Draft trong hệ thống. Chi khi transition đến state có `doc_status=1` thi mọi thuc su Submit. Đây là điểm hay — workflow states là layer trên docstatus, cho phép nhiều bước trước khi Submit.
</details>

<details>
<summary>Q2: Làm sao để chi cho phép Approve khi grand_total < 100 trieu?</summary>

**A:** Thêm `condition` vao transition:
```python
{
    "state": "Pending Review",
    "action": "Approve",
    "next_state": "Approved",
    "allowed": "Sales Manager",
    "condition": "doc.grand_total < 100000000"
}
```
Condition là Python expression, có thể truy cập `doc` (document hiện tại) và `frappe.session`.
</details>

### Skill References

- **DEEP DIVE:** Xem skill `frappe` -> `documentation/workflows/` để có full workflow reference
- **DEEP DIVE:** Xem skill `erpnext` để hiểu các approval workflows có sẵn trong ERPNext

---

## L2.6: Hands-on — Library Management System

### Tổng quan
Bài tập tổng hợp: tạo 3 DocTypes cho Library Management System — Book, Member, Transaction. Ap dùng kiến thức về field types, naming, child tables, và relationships. Đây là bài tập cơ bản nhất — sẽ được mở rộng trong Module 3 và 4.

### Step-by-step

#### Bước 1: Tạo DocType "Library Book"

```bash
# Trong devcontainer, đảm bảo app frappe_learn đã cai
cd /workspace/development/frappe-bench
```

Truy cập **http://flow.local:8000/app/doctype/new** và tạo:

**DocType Settings:**
- Name: `Library Book`
- Module: `Frappe Learn`
- Naming: `naming_series:` với options `BOOK-.####`

**Fields:**

| # | Label | Fieldname | Type | Options/Settings |
|---|-------|-----------|------|-----------------|
| 1 | Series | naming_series | Select | `BOOK-.####` |
| 2 | Title | title | Data | Mandatory, In List View |
| 3 | Author | author | Data | In List View |
| 4 | ISBN | isbn | Data | Unique |
| 5 | Publisher | publisher | Data | |
| 6 | Section: Details | — | Section Break | |
| 7 | Category | category | Select | `Fiction\nNon-Fiction\nReference\nTextbook` |
| 8 | Column Break | — | Column Break | |
| 9 | Status | status | Select | `Available\nBorrowed\nLost\nDamaged` Default: Available |
| 10 | Section: Image | — | Section Break | |
| 11 | Cover Image | cover_image | Attach Image | |
| 12 | Section: Description | — | Section Break | |
| 13 | Description | description | Text Editor | |

Save DocType. Frappe tự động tạo:
- Table `tabLibrary Book` trong DB
- Form view tại `/app/library-book`
- REST API tại `/api/resource/Library Book`

#### Bước 2: Tạo DocType "Library Member"

**DocType Settings:**
- Name: `Library Member`
- Module: `Frappe Learn`
- Naming: `naming_series:` với options `MEM-.####`

**Fields:**

| # | Label | Fieldname | Type | Options/Settings |
|---|-------|-----------|------|-----------------|
| 1 | Series | naming_series | Select | `MEM-.####` |
| 2 | Full Name | full_name | Data | Mandatory, In List View |
| 3 | Email | email | Data | Mandatory, Unique |
| 4 | Phone | phone | Data | |
| 5 | Column Break | — | Column Break | |
| 6 | Member Type | member_type | Select | `Student\nFaculty\nPublic` In List View |
| 7 | Membership Date | membership_date | Date | Default: Today |
| 8 | Status | status | Select | `Active\nInactive\nSuspended` Default: Active |

#### Bước 3: Tạo Child DocType "Library Transaction Item"

**DocType Settings:**
- Name: `Library Transaction Item`
- Module: `Frappe Learn`
- **Is Child Table**: Check ✓

**Fields:**

| # | Label | Fieldname | Type | Options/Settings |
|---|-------|-----------|------|-----------------|
| 1 | Book | book | Link | Library Book, Mandatory, In List View |
| 2 | Book Title | book_title | Data | Read Only, Fetch From: `book.title` |
| 3 | Due Date | due_date | Date | In List View |
| 4 | Return Date | return_date | Date | |
| 5 | Status | status | Select | `Borrowed\nReturned\nOverdue` Default: Borrowed |

#### Bước 4: Tạo DocType "Library Transaction"

**DocType Settings:**
- Name: `Library Transaction`
- Module: `Frappe Learn`
- Naming: `naming_series:` với options `LT-.YYYY.-.####`
- **Is Submittable**: Check ✓

**Fields:**

| # | Label | Fieldname | Type | Options/Settings |
|---|-------|-----------|------|-----------------|
| 1 | Series | naming_series | Select | `LT-.YYYY.-.####` |
| 2 | Member | member | Link | Library Member, Mandatory |
| 3 | Member Name | member_name | Data | Read Only, Fetch From: `member.full_name` |
| 4 | Column Break | — | Column Break | |
| 5 | Transaction Date | transaction_date | Date | Default: Today, Mandatory |
| 6 | Transaction Type | transaction_type | Select | `Borrow\nReturn` Mandatory |
| 7 | Section: Items | — | Section Break | |
| 8 | Books | items | Table | Library Transaction Item |
| 9 | Section: Notes | — | Section Break | |
| 10 | Notes | notes | Small Text | |

#### Bước 5: Verify

```bash
# Migrate để sync
bench --site flow.local migrate

# Kiểm tra tables đã tạo
bench --site flow.local mariadb -e "SHOW TABLES LIKE 'tabLibrary%';"
# Kết quả:
# tabLibrary Book
# tabLibrary Member
# tabLibrary Transaction
# tabLibrary Transaction Item

# Test tạo document
bench --site flow.local console
```

```python
# Trong console:
# Tạo book
book = frappe.get_doc({
    "doctype": "Library Book",
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "isbn": "978-0132350884",
    "category": "Reference",
    "status": "Available"
})
book.insert()
print(f"Book: {book.name}")

# Tạo member
member = frappe.get_doc({
    "doctype": "Library Member",
    "full_name": "Nguyen Van A",
    "email": "a@dcnet.vn",
    "member_type": "Faculty"
})
member.insert()
print(f"Member: {member.name}")

# Tạo transaction với child items
txn = frappe.get_doc({
    "doctype": "Library Transaction",
    "member": member.name,
    "transaction_type": "Borrow",
    "transaction_date": frappe.utils.today(),
    "items": [
        {
            "book": book.name,
            "due_date": frappe.utils.add_days(frappe.utils.today(), 14)
        }
    ]
})
txn.insert()
txn.submit()
print(f"Transaction: {txn.name}, Status: {txn.docstatus}")

frappe.db.commit()
```

#### Kiểm tra hoàn thành

- [ ] DocType "Library Book" đã tạo, có form tại `/app/library-book`
- [ ] DocType "Library Member" đã tạo, có form tại `/app/library-member`
- [ ] DocType "Library Transaction Item" là child table (`istable=1`)
- [ ] DocType "Library Transaction" là submittable, có child table "items"
- [ ] Có thể tạo book, member, và transaction qua UI và console
- [ ] Transaction có thể Submit (docstatus = 1)

> **Tiếp theo:** Module 3 sẽ thêm Client Scripts và Server Scripts cho các DocTypes này — validate ISBN, auto-update book status, filter members, etc.

### Skill References

- **DEEP DIVE:** Xem skill `frappe` -> `references/tutorials/` để có thêm bài tập DocType nâng cao
- **DEEP DIVE:** Xem skill `frappe` -> `test_examples/` để hiểu cach viết unit tests cho DocTypes
