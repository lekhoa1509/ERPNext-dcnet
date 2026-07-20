# Module 5: Database API & REST API

> **Mục tiêu / Objective:** Thành thạo các API truy vấn database và xây dựng REST endpoints trong Frappe.
> **Yêu cầu / Prerequisites:** Module 1-4 (DocType, Controllers, Hooks)
> **Thời lượng / Duration:** ~8 giờ thực hành

---

## L5.1: frappe.db — Database API Cơ Bản

### Tổng quan / Overview

`frappe.db` là lớp trừu tượng (abstraction layer) để tương tác với database mà không cần viết SQL trực tiếp. Đây là cach phổ biến nhất để đọc/ghi dữ liệu trong Frappe, hỗ trợ cả MariaDB và PostgreSQL. Hiểu rõ các method này giúp bạn viết code hiệu quả và bảo mật hơn so với raw SQL.

### Khái niệm chính / Key Concepts

#### 1. Đọc dữ liệu / Reading Data

```python
# get_value — Lấy 1 hoặc nhiều field của 1 record
# Trả về giá trị don (string/int) nếu 1 field, tuple nếu nhiều fields
name = frappe.db.get_value("Library Book", "BOOK-001", "title")
title, author = frappe.db.get_value("Library Book", "BOOK-001", ["title", "author"])

# get_value với filters (dict)
title = frappe.db.get_value("Library Book", {"isbn": "978-0-13-468599-1"}, "title")

# get_list — Lấy danh sách records với filters, fields, order, limit
# Trả về list of dicts: [{"name": "...", "title": "..."}]
books = frappe.db.get_list("Library Book",
    filters={"status": "Available"},
    fields=["name", "title", "author"],
    order_by="title asc",
    limit_page_length=20,
    limit_start=0  # offset cho pagination
)

# get_all — Giong get_list nhưng KHÔNG giới hạn số lượng (limit=0)
# Chu y: Có thể chậm với bang lớn
all_books = frappe.db.get_all("Library Book",
    filters={"status": "Available"},
    fields=["name", "title"]
)

# get_count — Đếm số record
total = frappe.db.get_count("Library Book")
available = frappe.db.get_count("Library Book", filters={"status": "Available"})

# exists — Kiểm tra record tồn tại (trả về name hoặc None)
if frappe.db.exists("Library Book", "BOOK-001"):
    print("Book exists")

# exists với filters
if frappe.db.exists("Library Book", {"isbn": "978-0-13-468599-1"}):
    print("ISBN found")
```

#### 2. Ghi dữ liệu / Writing Data

```python
# set_value — Cập nhật 1 field (KHÔNG trigger controller events)
frappe.db.set_value("Library Book", "BOOK-001", "status", "Issued")

# set_value nhiều fields cũng luc
frappe.db.set_value("Library Book", "BOOK-001", {
    "status": "Issued",
    "last_issued_date": frappe.utils.today()
})

# QUAN TRỌNG: set_value vs save()
# - set_value: Ghi trực tiếp DB, KHÔNG chạy validate/before_save/on_update
# - đọc.save(): Chạy FULL controller lifecycle
# Dùng set_value khi can update nhanh mà KHÔNG can business logic
```

#### 3. Raw SQL

```python
# sql — Chạy raw SQL (chi dùng khi can thiet)
# Trả về list of tuples mac dinh
result = frappe.db.sql("""
    SELECT name, title, author
    FROM `tabLibrary Book`
    WHERE status = %s AND creation > %s
    ORDER BY title
""", ("Available", "2026-01-01"))

# as_dict=True — Trả về list of dicts (thường dùng hon)
result = frappe.db.sql("""
    SELECT name, title, author
    FROM `tabLibrary Book`
    WHERE status = %s
""", ("Available",), as_dict=True)

# as_list=True — Trả về list of lists
result = frappe.db.sql("""
    SELECT COUNT(*) as count, status
    FROM `tabLibrary Book`
    GROUP BY status
""", as_list=True)

# BẢO MẬT: LUON dùng parameterized queries (%s)
# KHÔNG BAO GIỜ làm thế này:
# frappe.db.sql(f"SELECT * FROM `tabLibrary Book` WHERE name = '{user_input}'")  # SQL INJECTION!
```

#### 4. Phân biệt get_value vs get_đọc

```python
# get_value: Chi lấy field(s), nhe, KHÔNG load full document
title = frappe.db.get_value("Library Book", "BOOK-001", "title")

# get_đọc: Load TOAN BO document (tất cả fields + child tables + permissions)
doc = frappe.get_doc("Library Book", "BOOK-001")
# đọc có thể .save(), .submit(), .cancel(), truy cập child tables, etc.

# Quy tac:
# - Chi can đọc data? → get_value / get_list (nhanh hơn)
# - Can modify và save? → get_đọc (chạy full lifecycle)
# - Can child table data? → get_đọc (get_value không lấy child tables)
```

#### 5. Filters nâng cao

```python
# Filter operators
books = frappe.db.get_list("Library Book",
    filters={
        "status": ["in", ["Available", "Reserved"]],
        "creation": [">=", "2026-01-01"],
        "title": ["like", "%Python%"],
        "author": ["not in", ["Unknown"]],
        "price": ["between", [100000, 500000]],
        "description": ["is", "set"],       # NOT NULL va NOT ""
        # "description": ["is", "not set"], # NULL hoặc ""
    },
    fields=["name", "title", "author", "status"]
)

# or_filters — Điều kiện OR
books = frappe.db.get_list("Library Book",
    filters={"status": "Available"},
    or_filters=[
        {"author": ["like", "%Nguyen%"]},
        {"author": ["like", "%Tran%"]}
    ],
    fields=["name", "title", "author"]
)
```

### Mini Quiz

<details>
<summary><strong>Câu 1:</strong> Su khác biết chính giua <code>frappe.db.get_list</code> và <code>frappe.db.get_all</code> là gì?</summary>

**Trả lời:** `get_list` có `limit_page_length` mac dinh là 20 records, trong khi `get_all` trả về TẤT CẢ records (limit=0). Dùng `get_all` cẩn thận với bang lớn vì có thể gay chậm.
</details>

<details>
<summary><strong>Câu 2:</strong> Tại sao KHÔNG nên dùng <code>frappe.db.set_value</code> trong môi trường hop thay cho <code>đọc.save()</code>?</summary>

**Trả lời:** `set_value` ghi trực tiếp vao database mà KHÔNG chạy các controller hooks nhu `validate()`, `before_save()`, `on_update()`. Nếu business logic can được thuc thi (VD: tính toán field, kiểm tra điều kiện), phải dùng `doc.save()`.
</details>

<details>
<summary><strong>Câu 3:</strong> Code sau có lỗi gi? <code>frappe.db.sql(f"SELECT * FROM `tabItem` WHERE name = '{name}'")</code></summary>

**Trả lời:** **SQL Injection vulnerability!** Bien `name` được chen trực tiếp vao chuỗi SQL. Can dùng parameterized query: `frappe.db.sql("SELECT * FROM `tabItem` WHERE name = %s", (name,))`.
</details>

**DEEP DIVE:** Xem skill `frappe` → references/api_reference/ để hiểu thêm về toàn bộ Frappe API.

**DEEP DIVE:** Xem skill `dcnet_quality` → core/erpnext-database/ cho database best practices và anti-patterns.

---

## L5.2: Query Builder — frappe.qb (Pypika)

### Tổng quan / Overview

`frappe.qb` là Query Builder dua trên thư viện Pypika, cho phép xây dựng SQL queries bang Python objects thay vì chuỗi SQL. Query Builder ẩn toàn hơn raw SQL (không lo SQL injection), dễ đọc hơn, và hỗ trợ auto-complete trong IDE. Đây là cach được khuyến dùng cho các truy vấn phức tạp.

### Khái niệm chính / Key Concepts

#### 1. Query cơ bản

```python
# Khai bao DocType reference
Book = frappe.qb.DocType("Library Book")
Member = frappe.qb.DocType("Library Member")

# SELECT cơ bản
query = (
    frappe.qb.from_(Book)
    .select(Book.name, Book.title, Book.author, Book.status)
    .where(Book.status == "Available")
    .orderby(Book.title)
    .limit(20)
)
# Chạy query
result = query.run(as_dict=True)

# Xem SQL được generate (debug)
print(query.get_sql())
# → SELECT name, title, author, status FROM `tabLibrary Book`
#   WHERE status = 'Available' ORDER BY title LIMIT 20
```

#### 2. Filters và Conditions

```python
Book = frappe.qb.DocType("Library Book")

# Nhiều điều kiện (AND)
query = (
    frappe.qb.from_(Book)
    .select(Book.name, Book.title)
    .where(Book.status == "Available")
    .where(Book.author.like("%Nguyen%"))
    .where(Book.creation >= "2026-01-01")
)

# OR conditions
from pypika import Criterion
query = (
    frappe.qb.from_(Book)
    .select(Book.name, Book.title)
    .where(
        Criterion.any([
            Book.author.like("%Nguyen%"),
            Book.author.like("%Tran%")
        ])
    )
)

# IN operator
query = (
    frappe.qb.from_(Book)
    .select(Book.name, Book.title)
    .where(Book.status.isin(["Available", "Reserved"]))
)

# BETWEEN
query = (
    frappe.qb.from_(Book)
    .select(Book.name, Book.title, Book.price)
    .where(Book.price.between(100000, 500000))
)

# IS NULL / IS NOT NULL
query = (
    frappe.qb.from_(Book)
    .select(Book.name, Book.title)
    .where(Book.description.isnotnull())
)
```

#### 3. JOIN

```python
Book = frappe.qb.DocType("Library Book")
Transaction = frappe.qb.DocType("Library Transaction")
Member = frappe.qb.DocType("Library Member")

# INNER JOIN — Sach dang được mượn và thông tin người mượn
query = (
    frappe.qb.from_(Transaction)
    .join(Book).on(Transaction.book == Book.name)
    .join(Member).on(Transaction.member == Member.name)
    .select(
        Book.title,
        Member.member_name,
        Transaction.date,
        Transaction.status
    )
    .where(Transaction.status == "Issued")
    .orderby(Transaction.date, order=frappe.qb.desc)
)

# LEFT JOIN — Tất cả sach, ke cả chưa bao gio được mượn
query = (
    frappe.qb.from_(Book)
    .left_join(Transaction).on(
        (Transaction.book == Book.name) &
        (Transaction.status == "Issued")
    )
    .select(
        Book.name, Book.title,
        Transaction.member.as_("current_borrower")
    )
)
```

#### 4. GROUP BY và Aggregate Functions

```python
from pypika import functions as fn

Book = frappe.qb.DocType("Library Book")
Transaction = frappe.qb.DocType("Library Transaction")

# Đếm số sach theo trạng thái
query = (
    frappe.qb.from_(Book)
    .select(Book.status, fn.Count(Book.name).as_("count"))
    .groupby(Book.status)
)

# Thống kê mượn sach theo tháng
query = (
    frappe.qb.from_(Transaction)
    .select(
        fn.Month(Transaction.date).as_("month"),
        fn.Year(Transaction.date).as_("year"),
        fn.Count(Transaction.name).as_("total_transactions")
    )
    .where(Transaction.status == "Issued")
    .groupby(fn.Year(Transaction.date), fn.Month(Transaction.date))
    .orderby(fn.Year(Transaction.date), fn.Month(Transaction.date))
)

# HAVING
query = (
    frappe.qb.from_(Transaction)
    .select(
        Transaction.member,
        fn.Count(Transaction.name).as_("borrow_count")
    )
    .where(Transaction.status == "Issued")
    .groupby(Transaction.member)
    .having(fn.Count(Transaction.name) > 5)
)
```

#### 5. Khi nào dùng gì? / When to Use What?

```
+------------------+------------------------+------------------------------------+
| Method           | Khi nao dung           | Vi du                              |
+------------------+------------------------+------------------------------------+
| frappe.db.       | Truy van don gian,     | Lay ten, status cua 1 record      |
|   get_value/list | 1 bang, khong join     |                                    |
+------------------+------------------------+------------------------------------+
| frappe.qb        | Truy van phuc tap,     | JOIN nhieu bang, GROUP BY,         |
| (Query Builder)  | JOIN, subquery,        | aggregate, subquery                |
|                  | type-safe              |                                    |
+------------------+------------------------+------------------------------------+
| frappe.db.sql    | SQL dac biet ma qb     | CTE, UNION, stored procedure,     |
| (Raw SQL)        | khong ho tro, hoac     | database-specific syntax           |
|                  | migration scripts      |                                    |
+------------------+------------------------+------------------------------------+
```

### Mini Quiz

<details>
<summary><strong>Câu 1:</strong> Ưu điểm chính của <code>frappe.qb</code> số với <code>frappe.db.sql</code> là gì?</summary>

**Trả lời:** (1) Type-safe — không lo SQL injection vì parameters được escape tự động. (2) IDE auto-complete cho field names. (3) Để đọc và maintain hơn raw SQL strings. (4) Tự động xử lý table prefix (`tab`).
</details>

<details>
<summary><strong>Câu 2:</strong> Viết query builder để lấy 5 tac gia có nhiều sach nhất.</summary>

**Trả lời:**
```python
from pypika import functions as fn
Book = frappe.qb.DocType("Library Book")
query = (
    frappe.qb.from_(Book)
    .select(Book.author, fn.Count(Book.name).as_("book_count"))
    .groupby(Book.author)
    .orderby(fn.Count(Book.name), order=frappe.qb.desc)
    .limit(5)
)
result = query.run(as_dict=True)
```
</details>

**DEEP DIVE:** Xem skill `frappe` → references/api_reference/ để hiểu thêm về Query Builder API.

---

## L5.3: Transactions & Caching

### Tổng quan / Overview

Frappe quản lý database transactions tự động trong mọi web request, nhưng có nhưng trường hợp bạn cần kiem soat thủ công. Redis caching giúp giảm tại cho database bang cach lưu kết quả truy vấn thường dùng. Hiểu dùng về transactions và caching là yeu to quan trọng để xây dựng ứng dụng hiệu suất cao.

### Khái niệm chính / Key Concepts

#### 1. Transaction Management

```python
# Frappe tự động commit SAU MOI web request thành cong
# Va tự động rollback nếu có exception
# → Ban KHÔNG can gọi commit() trong hầu hết trường hợp

# Khi nào CẦN commit thủ công?
# 1. Background jobs (bench execute, scheduled tasks)
# 2. Khi can đảm bảo data được ghi trước khi tiếp tục

# Commit thủ công
def long_running_task():
    for i in range(1000):
        doc = frappe.get_doc({
            "doctype": "Library Book",
            "title": f"Book {i}"
        })
        doc.insert()

        # Commit mọi 100 records để tránh mất het data nếu fail
        if i % 100 == 0:
            frappe.db.commit()

# Rollback — Huy tất cả thay đổi chưa commit
try:
    doc1 = frappe.get_doc({"doctype": "Library Book", "title": "Book A"})
    doc1.insert()
    doc2 = frappe.get_doc({"doctype": "Library Book", "title": "Book B"})
    doc2.insert()
    # Nếu đọc2.insert() fail, cả đọc1 cũng bi rollback (cũng transaction)
except Exception:
    frappe.db.rollback()
    frappe.log_error("Transaction failed")
```

#### 2. Savepoints

```python
# Savepoint — Diem lưu tam trong transaction
# Cho phép rollback 1 phần mà không mất toàn bộ transaction

def process_books(book_list):
    for book_data in book_list:
        # Tạo savepoint trước mọi book
        frappe.db.savepoint("before_book")
        try:
            doc = frappe.get_doc({"doctype": "Library Book", **book_data})
            doc.insert()
        except Exception as e:
            # Chi rollback book này, các book trước van OK
            frappe.db.rollback(save_point="before_book")
            frappe.log_error(f"Failed to insert book: {e}")

    # Commit tất cả books thành cong
    frappe.db.commit()
```

#### 3. Redis Cache

```python
# frappe.cache() trả về Redis client wrapper
cache = frappe.cache()

# set_value / get_value — Lưu/đọc giá trị đơn giản
cache.set_value("total_books", 1500)
total = cache.get_value("total_books")  # → 1500

# TTL (Time To Live) — Tự động hết hạn
cache.set_value("daily_stats", stats_data, expires_in_sec=3600)  # 1 gio

# delete_key — Xóa cache
cache.delete_key("total_books")

# hset / hget — Hash (nhóm các giá trị liên quan)
cache.hset("book_cache", "BOOK-001", {"title": "Python Guide", "status": "Available"})
book = cache.hget("book_cache", "BOOK-001")

# delete_keys — Xóa theo pattern
cache.delete_keys("book_cache*")
```

#### 4. Document Cache

```python
# Frappe tự động cache documents trong Redis
# Khi gọi frappe.get_đọc() → check cache trước, miss thi query DB

# Xóa cache của 1 document cũ the
frappe.clear_document_cache("Library Book", "BOOK-001")

# Xóa cache của toàn bộ DocType
frappe.clear_cache(doctype="Library Book")

# Xóa TOAN BO cache (cẩn thận — ảnh hưởng performance)
frappe.clear_cache()

# Trong controller — on_update tự động clear cache cho document do
class LibraryBook(Document):
    def on_update(self):
        # Cache đã được clear tự động cho self
        # Nhưng nếu bạn tính toán aggregate data, can clear cache thủ công
        frappe.cache().delete_key("library_stats")
```

#### 5. Caching Patterns thường dùng

```python
# Pattern 1: Cache-aside (Lazy Loading)
def get_library_stats():
    """Lay thong ke thu vien, cache 5 phut."""
    cache_key = "library_stats"
    stats = frappe.cache().get_value(cache_key)

    if stats is None:
        # Cache miss — tính toán và lưu cache
        stats = {
            "total_books": frappe.db.count("Library Book"),
            "available": frappe.db.count("Library Book", {"status": "Available"}),
            "issued": frappe.db.count("Library Book", {"status": "Issued"})
        }
        frappe.cache().set_value(cache_key, stats, expires_in_sec=300)

    return stats

# Pattern 2: Invalidate cache khi data thay đổi
class LibraryTransaction(Document):
    def on_update(self):
        # Khi có giao dịch mới, stats cũ không con chính xac
        frappe.cache().delete_key("library_stats")
```

### Mini Quiz

<details>
<summary><strong>Câu 1:</strong> Tại sao bạn KHÔNG nên gọi <code>frappe.db.commit()</code> trong web request handler bình thường?</summary>

**Trả lời:** Frappe tự động commit sau mọi web request thành cong và rollback nếu có lỗi. Gọi commit() thủ công có thể dan đến tính trang dữ liệu không nhất quán nếu phần sau của request bi lỗi (vi phần trước đã commit rồi, không rollback được).
</details>

<details>
<summary><strong>Câu 2:</strong> Nếu bạn lưu thống kê "so sach kha dùng" vao cache, khi nào can xóa (invalidate) cache do?</summary>

**Trả lời:** Can invalidate khi: (1) Sach mọi được thêm, (2) Sach bi xóa, (3) Trạng thái sach thay đổi (VD: từ Available sang Issued). Tot nhất là đặt `frappe.cache().delete_key()` trong `on_update` và `on_trash` của LibraryBook và `on_update` của LibraryTransaction.
</details>

**DEEP DIVE:** Xem skill `frappe` → references/patterns/ để hiểu thêm về caching strategies.

---

## L5.4: REST API

### Tổng quan / Overview

Frappe cũng cap san REST API cho mọi DocType (Resource API) và cho phép tạo custom API endpoints bang `@frappe.whitelist()`. Client-side gọi API qua `frappe.call()`. Hiểu rõ REST API là can thiet để xây dựng mobile apps, tích hợp hệ thống ngoài, và viết client scripts hiệu quả.

### Khái niệm chính / Key Concepts

#### 1. Resource API (Built-in)

```bash
# GET — Lấy danh sách documents
curl -X GET "http://flow.local:8000/api/resource/Library Book?\
filters=[[\"status\",\"=\",\"Available\"]]&\
fields=[\"name\",\"title\",\"author\"]&\
limit_page_length=20&\
order_by=title asc" \
-H "Authorization: token api_key:api_secret"

# GET — Lay 1 document
curl -X GET "http://flow.local:8000/api/resource/Library Book/BOOK-001" \
-H "Authorization: token api_key:api_secret"

# POST — Tạo document mới
curl -X POST "http://flow.local:8000/api/resource/Library Book" \
-H "Authorization: token api_key:api_secret" \
-H "Content-Type: application/json" \
-d '{
    "title": "Python Programming",
    "author": "Guido van Rossum",
    "isbn": "978-0-13-468599-1",
    "status": "Available"
}'

# PUT — Cập nhật document
curl -X PUT "http://flow.local:8000/api/resource/Library Book/BOOK-001" \
-H "Authorization: token api_key:api_secret" \
-H "Content-Type: application/json" \
-d '{"status": "Issued"}'

# DELETE — Xóa document
curl -X DELETE "http://flow.local:8000/api/resource/Library Book/BOOK-001" \
-H "Authorization: token api_key:api_secret"
```

#### 2. Custom API Endpoints

```python
# Trong file: library_management/api.py

import frappe
from frappe import _

@frappe.whitelist()
def search_books(query, status=None, limit=20):
    """Tim kiem sach theo tieu de hoac tac gia.

    @frappe.whitelist() — Chi cho phep logged-in users goi
    Frappe tu dong validate:
    - User phai dang nhap
    - CSRF token (cho browser requests)
    """
    filters = {"title": ["like", f"%{query}%"]}
    if status:
        filters["status"] = status

    return frappe.db.get_list("Library Book",
        filters=filters,
        fields=["name", "title", "author", "status"],
        limit_page_length=int(limit)
    )


@frappe.whitelist(allow_guest=True)
def get_public_catalog():
    """Catalog cong khai — khong can dang nhap.

    allow_guest=True cho phep anonymous access.
    CHU Y: Chi dung cho data CONG KHAI, KHONG chua thong tin nhay cam.
    """
    return frappe.db.get_list("Library Book",
        filters={"status": "Available"},
        fields=["title", "author", "isbn"],
        order_by="title asc"
    )


@frappe.whitelist(methods=["POST"])
def borrow_book(book_name, member_name):
    """Muon sach — Chi chap nhan POST request.

    methods=["POST"] gioi han HTTP method duoc phep.
    """
    # Kiểm tra sach con kha dùng
    book = frappe.get_doc("Library Book", book_name)
    if book.status != "Available":
        frappe.throw(_("Book {0} is not available").format(book.title))

    # Tạo giao dịch mượn
    transaction = frappe.get_doc({
        "doctype": "Library Transaction",
        "book": book_name,
        "member": member_name,
        "date": frappe.utils.today(),
        "status": "Issued"
    })
    transaction.insert()

    # Cập nhật trạng thái sach
    book.status = "Issued"
    book.save()

    return {"message": _("Book borrowed successfully"), "transaction": transaction.name}
```

#### 3. Client-side API Calls

```javascript
// frappe.call() — Gọi API từ client scripts
// Cach 1: Gọi custom API endpoint
frappe.call({
    method: "library_management.api.search_books",
    args: {
        query: "Python",
        status: "Available",
        limit: 10
    },
    callback: function(r) {
        if (r.message) {
            console.log("Books found:", r.message);
        }
    }
});

// Cach 2: Async/await (modern — khuyen dùng)
async function searchBooks(query) {
    const result = await frappe.call({
        method: "library_management.api.search_books",
        args: { query: query }
    });
    return result.message;
}

// Cach 3: Gọi whitelisted method của DocType
frappe.call({
    method: "run_doc_method",
    args: {
        docs: cur_frm.doc,   // Document hiện tại
        method: "calculate_fine",  // Method trong controller
        // hoac:
        // method: "check_availability"
    },
    callback: function(r) {
        console.log(r.message);
    }
});

// Cach 4: frappe.xcall — Shorthand, trả về Promise
const books = await frappe.xcall(
    "library_management.api.search_books",
    { query: "Python" }
);
```

#### 4. Authentication

```python
# 1. Token-based (API Key + Secret) — Cho hệ thống ngoài
# Tạo trong: User → API Access → Generate Keys
# Header: Authorization: token api_key:api_secret

# 2. Cookie-based — Tự động khi đăng nhập qua browser
# Frappe Desk su dùng cach này, không cần config thêm

# 3. OAuth2 — Cho ứng dụng third-party
# Setup trong: Social Login Key / Connected App
# Flow: Authorization Code → Access Token → API calls

# 4. Basic Auth (username:password) — KHÔNG khuyến dùng cho production
# Chi dùng để test nhanh
# curl -X GET url -u "user@example.com:password"
```

#### 5. Error Handling trong API

```python
@frappe.whitelist()
def safe_api_endpoint(book_name):
    """API voi error handling dung cach."""
    try:
        if not frappe.db.exists("Library Book", book_name):
            # 404 — Không tìm thay
            frappe.throw(
                _("Book {0} not found").format(book_name),
                frappe.DoesNotExistError
            )

        book = frappe.get_doc("Library Book", book_name)

        if not frappe.has_permission("Library Book", "read", book):
            # 403 — Không có quyền
            frappe.throw(
                _("No permission to read this book"),
                frappe.PermissionError
            )

        return book.as_dict()

    except frappe.DoesNotExistError:
        raise  # De Frappe xu ly, tra ve HTTP 404
    except frappe.PermissionError:
        raise  # De Frappe xu ly, tra ve HTTP 403
    except Exception as e:
        frappe.log_error(f"API Error: {e}")
        frappe.throw(_("An error occurred"), frappe.ValidationError)
```

### Mini Quiz

<details>
<summary><strong>Câu 1:</strong> Su khác biết giua <code>@frappe.whitelist()</code> và <code>@frappe.whitelist(allow_guest=True)</code>?</summary>

**Trả lời:** `@frappe.whitelist()` yêu cầu user phải đăng nhập (authenticated). `@frappe.whitelist(allow_guest=True)` cho phép truy cập không cần đăng nhập — chi dùng cho data công khai nhu catalog, trang chu, etc.
</details>

<details>
<summary><strong>Câu 2:</strong> Trong Client Script, tại sao KHÔNG được dùng <code>frappe.db.get_list()</code> mà phải dùng <code>frappe.call()</code>?</summary>

**Trả lời:** Client Script chạy trên BROWSER (JavaScript), không có truy cập trực tiếp database. `frappe.db.*` là Python API chạy trên server. Từ browser, phải dùng `frappe.call()` để gửi HTTP request toi server, server sẽ thuc hiện truy vấn database và tra kết quả ve.
</details>

<details>
<summary><strong>Câu 3:</strong> Làm sao để giới hạn 1 API endpoint chi chap nhận POST requests?</summary>

**Trả lời:** Dùng `@frappe.whitelist(methods=["POST"])`. Khi client gửi GET request, Frappe sẽ trả về lỗi. Đây hữu ích cho các endpoint thay đổi dữ liệu (borrow, return, etc.) để tránh CSRF và đảm bảo idempotency.
</details>

**DEEP DIVE:** Xem skill `frappe` → references/api_reference/ để hiểu thêm về REST API patterns.

**DEEP DIVE:** Xem skill `dcnet_quality` → syntax/erpnext-syntax-whitelisted/ cho whitelisted method best practices.

**DEEP DIVE:** Xem skill `dcnet_quality` → syntax/erpnext-syntax-clientscripts/ cho client-side API call patterns.

---

## L5.5: Hands-on — Library API System

### Tổng quan / Overview

Thực hành tổng hợp: Xây dựng 5 API endpoints cho hệ thống thư viện, bao gồm tìm kiem, kiểm tra tính trang, mượn sach, tra sach, và thống kê thành vien. Mỗi endpoint ap dùng các kiến thức từ L5.1-L5.4 với error handling, permissions, và caching.

### Bài tập / Exercise

Tạo file `library_management/library_management/api.py`:

```python
import frappe
from frappe import _
from frappe.utils import today, add_days, date_diff, getdate


# === API 1: Tìm kiem sach ===
@frappe.whitelist(allow_guest=True)
def search_books(query=None, author=None, status=None, page=1, page_size=20):
    """Tim kiem sach theo tieu de, tac gia, trang thai.

    Endpoint: POST /api/method/library_management.api.search_books
    Params: query (str), author (str), status (str), page (int), page_size (int)
    """
    filters = {}
    or_filters = []

    if query:
        or_filters = [
            {"title": ["like", f"%{query}%"]},
            {"isbn": ["like", f"%{query}%"]}
        ]
    if author:
        filters["author"] = ["like", f"%{author}%"]
    if status:
        filters["status"] = status

    page = int(page)
    page_size = min(int(page_size), 100)  # Gioi han toi da 100
    offset = (page - 1) * page_size

    books = frappe.db.get_list("Library Book",
        filters=filters,
        or_filters=or_filters if or_filters else None,
        fields=["name", "title", "author", "isbn", "status", "publisher"],
        limit_page_length=page_size,
        limit_start=offset,
        order_by="title asc"
    )

    total = frappe.db.count("Library Book", filters=filters)

    return {
        "books": books,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": -(-total // page_size)  # Ceiling division
    }


# === API 2: Kiểm tra tính trang sach ===
@frappe.whitelist(allow_guest=True)
def check_availability(book_name):
    """Kiem tra sach co san de muon hay khong.

    Endpoint: POST /api/method/library_management.api.check_availability
    Params: book_name (str) — ten (ID) cua sach
    """
    if not frappe.db.exists("Library Book", book_name):
        frappe.throw(_("Book {0} not found").format(book_name), frappe.DoesNotExistError)

    book = frappe.db.get_value("Library Book", book_name,
        ["name", "title", "author", "status"], as_dict=True
    )

    result = {
        "book": book,
        "available": book.status == "Available"
    }

    # Nếu dang được mượn, cho biết ngày du kien tra
    if book.status == "Issued":
        transaction = frappe.db.get_value("Library Transaction",
            filters={"book": book_name, "status": "Issued"},
            fieldname=["member", "date"],
            as_dict=True,
            order_by="date desc"
        )
        if transaction:
            result["expected_return_date"] = str(add_days(getdate(transaction.date), 14))

    return result


# === API 3: Muon sach ===
@frappe.whitelist(methods=["POST"])
def borrow_book(book_name, member_name):
    """Tao giao dich muon sach.

    Endpoint: POST /api/method/library_management.api.borrow_book
    Params: book_name (str), member_name (str)
    """
    # Validate book
    if not frappe.db.exists("Library Book", book_name):
        frappe.throw(_("Book {0} not found").format(book_name), frappe.DoesNotExistError)

    # Validate member
    if not frappe.db.exists("Library Member", member_name):
        frappe.throw(_("Member {0} not found").format(member_name), frappe.DoesNotExistError)

    # Kiểm tra sach con kha dùng
    status = frappe.db.get_value("Library Book", book_name, "status")
    if status != "Available":
        frappe.throw(_("Book is not available for borrowing"))

    # Kiểm tra member không vượt qua giới hạn mượn (VD: tối đa 5 cuon)
    active_loans = frappe.db.count("Library Transaction",
        filters={"member": member_name, "status": "Issued"}
    )
    max_loans = 5
    if active_loans >= max_loans:
        frappe.throw(_("Member has reached maximum loan limit ({0})").format(max_loans))

    # Tạo giao dịch
    transaction = frappe.get_doc({
        "doctype": "Library Transaction",
        "book": book_name,
        "member": member_name,
        "date": today(),
        "status": "Issued",
        "due_date": add_days(today(), 14)  # Han tra: 14 ngay
    })
    transaction.insert(ignore_permissions=False)

    # Cập nhật trạng thái sach
    frappe.db.set_value("Library Book", book_name, "status", "Issued")

    # Xóa cache thống kê
    frappe.cache().delete_key("library_stats")

    return {
        "message": _("Book borrowed successfully"),
        "transaction": transaction.name,
        "due_date": str(transaction.due_date)
    }


# === API 4: Tra sach ===
@frappe.whitelist(methods=["POST"])
def return_book(book_name, member_name):
    """Tra sach va tinh phat (neu tre han).

    Endpoint: POST /api/method/library_management.api.return_book
    Params: book_name (str), member_name (str)
    """
    # Tìm giao dịch mượn dang active
    transaction_name = frappe.db.get_value("Library Transaction",
        filters={
            "book": book_name,
            "member": member_name,
            "status": "Issued"
        },
        fieldname="name",
        order_by="date desc"
    )

    if not transaction_name:
        frappe.throw(_("No active loan found for this book and member"))

    transaction = frappe.get_doc("Library Transaction", transaction_name)

    # Tinh phat tre han (10,000 VND/ngày)
    fine = 0
    days_overdue = 0
    if hasattr(transaction, 'due_date') and transaction.due_date:
        days_overdue = date_diff(today(), transaction.due_date)
        if days_overdue > 0:
            fine = days_overdue * 10000  # 10,000 VND/ngay

    # Cập nhật giao dịch
    transaction.status = "Returned"
    transaction.return_date = today()
    transaction.save()

    # Cập nhật trạng thái sach
    frappe.db.set_value("Library Book", book_name, "status", "Available")

    # Xóa cache thống kê
    frappe.cache().delete_key("library_stats")

    result = {
        "message": _("Book returned successfully"),
        "transaction": transaction.name
    }

    if fine > 0:
        result["fine"] = fine
        result["days_overdue"] = days_overdue
        result["fine_message"] = _("Overdue by {0} days. Fine: {1} VND").format(
            days_overdue, f"{fine:,.0f}"
        )

    return result


# === API 5: Thống kê thành vien ===
@frappe.whitelist()
def member_statistics(member_name=None):
    """Thong ke hoat dong muon tra cua thanh vien.

    Endpoint: POST /api/method/library_management.api.member_statistics
    Params: member_name (str, optional) — neu khong truyen, lay cua user hien tai
    """
    if not member_name:
        # Tìm member liên kết với user hiện tại
        member_name = frappe.db.get_value("Library Member",
            {"email_id": frappe.session.user}, "name"
        )
        if not member_name:
            frappe.throw(_("No library member linked to current user"))

    if not frappe.db.exists("Library Member", member_name):
        frappe.throw(_("Member {0} not found").format(member_name), frappe.DoesNotExistError)

    member = frappe.db.get_value("Library Member", member_name,
        ["member_name", "email_id", "membership_date"], as_dict=True
    )

    # Thống kê tổng hợp
    total_borrowed = frappe.db.count("Library Transaction",
        filters={"member": member_name}
    )
    currently_borrowed = frappe.db.count("Library Transaction",
        filters={"member": member_name, "status": "Issued"}
    )
    total_returned = frappe.db.count("Library Transaction",
        filters={"member": member_name, "status": "Returned"}
    )

    # Sach đang mượn (chi tiết)
    active_loans = frappe.db.get_list("Library Transaction",
        filters={"member": member_name, "status": "Issued"},
        fields=["name", "book", "date", "due_date"]
    )

    # Bo sung ten sach
    for loan in active_loans:
        loan["book_title"] = frappe.db.get_value("Library Book", loan["book"], "title")
        if loan.get("due_date"):
            loan["days_remaining"] = date_diff(loan["due_date"], today())
            loan["overdue"] = loan["days_remaining"] < 0

    # Lich su mượn gan nhất (5 records)
    recent_history = frappe.db.get_list("Library Transaction",
        filters={"member": member_name, "status": "Returned"},
        fields=["name", "book", "date", "return_date"],
        order_by="return_date desc",
        limit_page_length=5
    )
    for item in recent_history:
        item["book_title"] = frappe.db.get_value("Library Book", item["book"], "title")

    return {
        "member": member,
        "statistics": {
            "total_borrowed": total_borrowed,
            "currently_borrowed": currently_borrowed,
            "total_returned": total_returned
        },
        "active_loans": active_loans,
        "recent_history": recent_history
    }
```

### Test với curl

```bash
# Test API 1: Tìm kiem sach
curl -X POST "http://flow.local:8000/api/method/library_management.api.search_books" \
  -H "Content-Type: application/json" \
  -d '{"query": "Python", "page": 1, "page_size": 10}'

# Test API 2: Kiểm tra tính trang
curl -X POST "http://flow.local:8000/api/method/library_management.api.check_availability" \
  -H "Authorization: token api_key:api_secret" \
  -H "Content-Type: application/json" \
  -d '{"book_name": "BOOK-001"}'

# Test API 3: Muon sach
curl -X POST "http://flow.local:8000/api/method/library_management.api.borrow_book" \
  -H "Authorization: token api_key:api_secret" \
  -H "Content-Type: application/json" \
  -d '{"book_name": "BOOK-001", "member_name": "MEM-001"}'

# Test API 4: Tra sach
curl -X POST "http://flow.local:8000/api/method/library_management.api.return_book" \
  -H "Authorization: token api_key:api_secret" \
  -H "Content-Type: application/json" \
  -d '{"book_name": "BOOK-001", "member_name": "MEM-001"}'

# Test API 5: Thống kê thành vien
curl -X POST "http://flow.local:8000/api/method/library_management.api.member_statistics" \
  -H "Authorization: token api_key:api_secret" \
  -H "Content-Type: application/json" \
  -d '{"member_name": "MEM-001"}'
```

### Kiểm tra đầu ra mong đổi / Expected Output

```json
// API 1 Response:
{
  "message": {
    "books": [{"name": "BOOK-001", "title": "Python Programming", ...}],
    "total": 15,
    "page": 1,
    "page_size": 10,
    "total_pages": 2
  }
}

// API 3 Response:
{
  "message": {
    "message": "Book borrowed successfully",
    "transaction": "LT-00001",
    "due_date": "2026-03-31"
  }
}
```

### Mini Quiz

<details>
<summary><strong>Câu 1:</strong> Tại sao <code>search_books</code> dùng <code>allow_guest=True</code> con <code>borrow_book</code> thi không?</summary>

**Trả lời:** Tìm kiem sach là thao tác đọc (read-only) và có thể công khai cho bất kỳ ai. Muon sach là thao tác ghi (write) can xác định người mượn, kiểm tra quyền, và tạo giao dịch — bắt buộc phải đăng nhập.
</details>

<details>
<summary><strong>Câu 2:</strong> Trong API <code>return_book</code>, tại sao lại gọi <code>frappe.cache().delete_key("library_stats")</code>?</summary>

**Trả lời:** Khi sach được tra, số lieu thống kê (so sach kha dùng, số sach đang mượn) thay đổi. Nếu không xóa cache, API thống kê sẽ trả về số lieu cũ cho đến khi cache hết hạn. Đây là cache invalidation pattern — đảm bảo data luôn nhất quán.
</details>

**DEEP DIVE:** Xem skill `dcnet_quality` → impl/erpnext-impl-whitelisted/ cho whitelisted method implementation patterns.

**DEEP DIVE:** Xem skill `dcnet_quality` → errors/ cho error handling best practices trong API.

---

## L5.6: Performance Tips — Chọn đúng API

### Tổng quan / Overview

Chọn sai API là nguyên nhân phổ biến nhất gây chậm trong Frappe. `frappe.get_doc()` load toàn bộ document kể cả child tables — dùng sai chỗ có thể chậm hơn 10-100x so với `frappe.db.get_value()`.

### Bảng so sánh chọn API

| Tình huống | Dùng | Không dùng | Lý do |
|------------|------|-----------|-------|
| Lấy 1-2 field của 1 record | `frappe.db.get_value()` | `frappe.get_doc()` | get_doc load toàn document + child tables |
| Lấy nhiều field của 1 record | `frappe.db.get_value(fields=[...])` | `frappe.get_doc()` | Vẫn nhanh hơn, chọn đúng fields |
| Cần chạy hooks (validate, on_save) | `frappe.get_doc()` + `.save()` | `frappe.db.set_value()` | Hooks không chạy với db.set_value |
| Cập nhật 1 field, không cần hooks | `frappe.db.set_value()` | `doc.save()` | set_value trực tiếp DB, không trigger lifecycle |
| Lấy danh sách nhiều records | `frappe.db.get_list()` | `frappe.get_all()` | get_list ít memory hơn |
| Cần tất cả fields + child tables | `frappe.get_all(fields=["*"])` | Nhiều get_doc trong loop | N+1 problem |
| Query phức tạp (JOIN, GROUP BY) | `frappe.db.sql()` | Nhiều API calls | 1 query hiệu quả hơn nhiều round-trips |

### N+1 Problem — Anti-pattern phổ biến nhất

```python
# ❌ SAI — N+1 queries (N = số sales orders)
orders = frappe.db.get_list("Sales Order",
    filters={"status": "To Deliver"},
    fields=["name", "customer"]
)
for order in orders:
    customer = frappe.get_doc("Customer", order.customer)  # N queries!
    print(customer.customer_name)

# ✅ ĐÚNG — 1 query dùng IN filter hoặc JOIN
customer_names = [o.customer for o in orders]
customers = frappe.db.get_list("Customer",
    filters={"name": ["in", customer_names]},
    fields=["name", "customer_name"]
)
# Tạo dict để lookup O(1)
customer_map = {c.name: c.customer_name for c in customers}

for order in orders:
    print(customer_map.get(order.customer, "Unknown"))


# ✅ ĐÚNG — Dùng frappe.qb với JOIN (Module 5.2)
from frappe.query_builder import DocType
SO = DocType("Sales Order")
Cust = DocType("Customer")

results = (
    frappe.qb.from_(SO)
    .join(Cust).on(SO.customer == Cust.name)
    .select(SO.name, SO.customer, Cust.customer_name)
    .where(SO.status == "To Deliver")
    .run(as_dict=True)
)
```

### Index Strategy

```python
# Field hay dùng trong filter cần được index
# Trong DocType JSON — thêm "search_index": 1

# ❌ Chậm — filter trên field không có index
result = frappe.db.get_list("Sales Order",
    filters={"custom_external_id": "EXT-12345"},  # Không có index → full table scan
    fields=["name"]
)

# ✅ Nhanh — sau khi thêm search_index=1 vào field custom_external_id
# Frappe tự tạo INDEX khi migrate

# Kiểm tra index trong MariaDB:
# SHOW INDEX FROM `tabSales Order`;
```

### Memory Optimization

```python
# ❌ Load toàn bộ vào memory
all_orders = frappe.db.get_list("Sales Order",
    fields=["*"],    # Tránh — load tất cả fields
    limit=0          # limit=0 = không giới hạn = có thể load 100k records!
)

# ✅ Paginate + chỉ field cần thiết
PAGE_SIZE = 100
page = 0
while True:
    batch = frappe.db.get_list("Sales Order",
        filters={"status": "Draft"},
        fields=["name", "customer", "grand_total"],
        limit=PAGE_SIZE,
        limit_start=page * PAGE_SIZE
    )
    if not batch:
        break
    process_batch(batch)
    page += 1
```

### Caching để tránh query lặp lại

```python
# Pattern: Cache-aside cho data ít thay đổi
def get_company_settings() -> dict:
    """Company settings không thay đổi thường xuyên — cache 1 giờ"""
    cache_key = f"company_settings_{frappe.defaults.get_user_default('Company')}"
    cached = frappe.cache().get_value(cache_key)
    if cached:
        return cached

    settings = frappe.db.get_value(
        "Company",
        frappe.defaults.get_user_default("Company"),
        ["default_currency", "default_letter_head", "tax_id"],
        as_dict=True
    )
    frappe.cache().set_value(cache_key, settings, expires_in_sec=3600)
    return settings


# Invalidate cache khi Company thay đổi (trong hooks.py):
# doc_events = {
#     "Company": {
#         "on_update": "myapp.utils.invalidate_company_cache"
#     }
# }
```

### Mini Quiz

<details>
<summary><strong>Câu 1:</strong> Bạn cần hiển thị tên khách hàng trong 500 Sales Orders. Cách nào đúng và tại sao?</summary>

**Trả lời:** Fetch tất cả customer names bằng 1 query `get_list("Customer", filters={"name": ["in", customer_list]})` rồi tạo dict để lookup. KHÔNG dùng `frappe.get_doc("Customer", name)` trong loop vì đó là N+1 problem (500 extra queries).
</details>

<details>
<summary><strong>Câu 2:</strong> Khi nào dùng <code>frappe.db.set_value()</code> thay vì <code>doc.save()</code>?</summary>

**Trả lời:** Dùng `set_value()` khi: (1) Chỉ update 1-2 field đơn giản, (2) Không muốn trigger validate/before_save hooks, (3) Đang trong background job cần hiệu năng cao. Dùng `doc.save()` khi cần business logic chạy (validation, computed fields, notifications).
</details>
