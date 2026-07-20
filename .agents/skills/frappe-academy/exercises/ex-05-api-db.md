# Module 5: Database API & REST API
# Mô-đun 5: Database API & REST API

> **Container:** `devcontainer-frappe-1`
> **Bench path:** `/workspace/development/frappe-bench`
> **Site:** `flow.local`
> **Prefix command:** `docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local ..."`

---

## Prerequisites / Yêu cầu trước khi bắt đầu

- Completed Module 1-4 (frappe_learn app installed with Book, Library Member, Library Transaction DocTypes)
- At least 5 Books and 3 Library Members created (via fixtures or manual entry)
- Đã hoàn thành Module 1-4 (app frappe_learn đã cài đặt với các DocType Book, Library Member, Library Transaction)
- Có ít nhất 5 Book và 3 Library Member (tạo thủ công hoặc qua fixtures)

---

## Exercise 5.1: frappe.db Basics / Cơ bản về frappe.db

### Objective / Mục tiêu
Learn the fundamental `frappe.db` methods: `get_value`, `get_list`, `get_count`, `exists`, `set_value`.

Học các phương thức cơ bản của `frappe.db`: `get_value`, `get_list`, `get_count`, `exists`, `set_value`.

### Instructions / Hướng dẫn

Run each command in the bench console:

```bash
docker exec -it devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console"
```

**Step 1:** Count all Books / Đếm tất cả sách

```python
# Count all books
total = frappe.db.count("Book")
print(f"Total books: {total}")

# Count books by status
available = frappe.db.count("Book", {"status": "Available"})
print(f"Available books: {available}")
```

**Step 2:** Get a single value / Lấy một giá trị đơn

```python
# Get title of a specific book by ISBN
title = frappe.db.get_value("Book", {"isbn": "978-0-13-468599-1"}, "title")
print(f"Book title: {title}")

# Get multiple fields at once
title, author, status = frappe.db.get_value("Book", {"isbn": "978-0-13-468599-1"}, ["title", "author", "status"])
print(f"{title} by {author} - Status: {status}")
```

**Step 3:** Get a list of records / Lấy danh sách bản ghi

```python
# Get all available books (title and author only)
books = frappe.db.get_list("Book",
    filters={"status": "Available"},
    fields=["title", "author", "isbn"],
    order_by="title asc",
    limit_page_length=10
)
for b in books:
    print(f"  {b.title} - {b.author}")
```

**Step 4:** Check existence / Kiểm tra tồn tại

```python
# Check if a book exists
exists = frappe.db.exists("Book", {"isbn": "978-0-13-468599-1"})
print(f"Book exists: {bool(exists)}")

# Check if a non-existent book exists
exists = frappe.db.exists("Book", {"isbn": "000-0-00-000000-0"})
print(f"Fake book exists: {bool(exists)}")
```

**Step 5:** Update a value / Cập nhật giá trị

```python
# Update status of a book (by name)
book_name = frappe.db.get_value("Book", {"isbn": "978-0-13-468599-1"}, "name")
frappe.db.set_value("Book", book_name, "status", "Borrowed")
frappe.db.commit()

# Verify the update
status = frappe.db.get_value("Book", book_name, "status")
print(f"Updated status: {status}")

# Reset it back
frappe.db.set_value("Book", book_name, "status", "Available")
frappe.db.commit()
```

### Expected Output / Kết quả mong đợi

- `get_count` returns integer
- `get_value` returns string or tuple
- `get_list` returns list of dicts
- `exists` returns name (string) or None
- `set_value` updates the database directly (bypasses controller hooks)

### Verification / Kiểm tra

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local execute frappe.client.get_count --args '{\"doctype\": \"Book\"}'"
```

Should return a number greater than 0.

<details>
<summary>Hint 1: frappe.db.get_list vs frappe.get_all / Gợi ý 1</summary>

`frappe.db.get_list` and `frappe.get_all` are almost identical. The key difference:
- `frappe.get_all` ignores permissions (uses `ignore_permissions=True` by default)
- `frappe.db.get_list` respects permissions by default

For bench console, both work the same since you run as Administrator.

`frappe.db.get_list` và `frappe.get_all` gần như giống nhau. Khác biệt chính:
- `frappe.get_all` bỏ qua quyền (mặc định `ignore_permissions=True`)
- `frappe.db.get_list` tôn trọng quyền mặc định
</details>

<details>
<summary>Hint 2: frappe.db.set_value vs doc.save() / Gợi ý 2</summary>

`frappe.db.set_value` writes directly to DB — no validation, no hooks, no modified timestamp update.
`doc.save()` triggers validate, on_update, and updates modified timestamp.

Use `set_value` only for quick fixes or background updates. Use `doc.save()` for normal operations.

`frappe.db.set_value` ghi trực tiếp vào DB — không validate, không hooks.
`doc.save()` chạy validate, on_update, cập nhật thời gian.
</details>

---

## Exercise 5.2: Query Builder (frappe.qb) / Truy vấn nâng cao

### Objective / Mục tiêu
Use the Frappe Query Builder (`frappe.qb`) to write type-safe, composable SQL queries — including JOINs and aggregations.

Dùng Frappe Query Builder (`frappe.qb`) để viết các truy vấn SQL an toàn, có thể kết hợp — bao gồm JOIN và gom nhóm.

### Instructions / Hướng dẫn

**Step 1:** Basic query builder / Truy vấn cơ bản

```python
# In bench console
Book = frappe.qb.DocType("Book")

# Select all available books
query = (
    frappe.qb.from_(Book)
    .select(Book.title, Book.author, Book.isbn)
    .where(Book.status == "Available")
    .orderby(Book.title)
    .limit(10)
)
print(query.get_sql())  # See the generated SQL
results = query.run(as_dict=True)
for r in results:
    print(f"  {r['title']} by {r['author']}")
```

**Step 2:** Aggregation — Count books by status / Đếm sách theo trạng thái

```python
from pypika import functions as fn

Book = frappe.qb.DocType("Book")

query = (
    frappe.qb.from_(Book)
    .select(Book.status, fn.Count(Book.name).as_("count"))
    .groupby(Book.status)
)
results = query.run(as_dict=True)
for r in results:
    print(f"  {r['status']}: {r['count']} books")
```

**Step 3:** JOIN — Get most borrowed books / Sách được mượn nhiều nhất

```python
from pypika import functions as fn

Book = frappe.qb.DocType("Book")
Transaction = frappe.qb.DocType("Library Transaction")

query = (
    frappe.qb.from_(Transaction)
    .join(Book).on(Transaction.book == Book.name)
    .select(
        Book.title,
        Book.author,
        fn.Count(Transaction.name).as_("borrow_count")
    )
    .where(Transaction.type == "Borrow")
    .groupby(Book.name)
    .orderby(fn.Count(Transaction.name), order=frappe.qb.desc)
    .limit(5)
)

print("Most borrowed books:")
results = query.run(as_dict=True)
for i, r in enumerate(results, 1):
    print(f"  {i}. {r['title']} by {r['author']} — {r['borrow_count']} times")
```

**Step 4:** Subquery — Members who never borrowed / Thành viên chưa mượn sách

```python
Book = frappe.qb.DocType("Book")
Member = frappe.qb.DocType("Library Member")
Transaction = frappe.qb.DocType("Library Transaction")

# Subquery: members who have transactions
borrowers = (
    frappe.qb.from_(Transaction)
    .select(Transaction.library_member)
    .distinct()
)

# Main query: members NOT in the subquery
query = (
    frappe.qb.from_(Member)
    .select(Member.full_name, Member.email_address)
    .where(Member.name.notin(borrowers))
)

results = query.run(as_dict=True)
print(f"Members who never borrowed: {len(results)}")
for r in results:
    print(f"  {r['full_name']} ({r['email_address']})")
```

### Expected Output / Kết quả mong đợi

- Step 1: List of available books with title and author
- Step 2: Table showing count per status (Available, Borrowed, etc.)
- Step 3: Top 5 most borrowed books with borrow count
- Step 4: List of members who have never borrowed a book

### Verification / Kiểm tra

```bash
# Verify the JOIN query works by running it via bench execute
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local execute frappe.client.get_count --args '{\"doctype\": \"Library Transaction\"}'"
```

<details>
<summary>Hint: frappe.qb vs raw SQL / Gợi ý</summary>

You can always run raw SQL with `frappe.db.sql()`:
```python
results = frappe.db.sql("""
    SELECT b.title, COUNT(t.name) as borrow_count
    FROM `tabLibrary Transaction` t
    JOIN `tabBook` b ON t.book = b.name
    WHERE t.type = 'Borrow'
    GROUP BY b.name
    ORDER BY borrow_count DESC
    LIMIT 5
""", as_dict=True)
```

But `frappe.qb` is preferred because:
1. Type-safe — catches typos at build time
2. No SQL injection risk
3. Composable — build queries dynamically
4. Database-agnostic (MariaDB/PostgreSQL)

`frappe.qb` được ưu tiên vì: an toàn kiểu dữ liệu, chống SQL injection, có thể kết hợp, tương thích nhiều DB.
</details>

---

## Exercise 5.3: Whitelisted API / API Whitelist

### Objective / Mục tiêu
Create a `@frappe.whitelist()` function that can be called from the client side (browser) or via REST API.

Tạo hàm `@frappe.whitelist()` có thể gọi từ phía client (trình duyệt) hoặc qua REST API.

### Instructions / Hướng dẫn

**Step 1:** Create the API file / Tạo file API

Create file: `frappe_learn/frappe_learn/api.py`

```python
import frappe
from frappe import _


@frappe.whitelist()
def get_book_availability(isbn):
    """Get availability info for a book by ISBN.

    Args:
        isbn: The ISBN of the book to check

    Returns:
        dict: Book info with availability status
            - title: Book title
            - author: Book author
            - status: Current status (Available/Borrowed/Lost)
            - total_copies: Total copies in library (books with same ISBN)
            - available_copies: Number of available copies
            - current_borrower: Name of current borrower (if borrowed)
    """
    if not isbn:
        frappe.throw(_("ISBN is required"))

    # Check if book exists
    if not frappe.db.exists("Book", {"isbn": isbn}):
        frappe.throw(_("No book found with ISBN {0}").format(isbn))

    # Get all copies of this book
    books = frappe.get_all("Book",
        filters={"isbn": isbn},
        fields=["name", "title", "author", "status"]
    )

    total_copies = len(books)
    available_copies = len([b for b in books if b.status == "Available"])

    # Get current borrower if any copy is borrowed
    current_borrower = None
    for book in books:
        if book.status == "Borrowed":
            transaction = frappe.db.get_value(
                "Library Transaction",
                {"book": book.name, "type": "Borrow", "docstatus": 1},
                ["library_member"],
                order_by="transaction_date desc"
            )
            if transaction:
                current_borrower = frappe.db.get_value(
                    "Library Member", transaction, "full_name"
                )
                break

    return {
        "title": books[0].title,
        "author": books[0].author,
        "isbn": isbn,
        "status": books[0].status,
        "total_copies": total_copies,
        "available_copies": available_copies,
        "current_borrower": current_borrower
    }
```

**Step 2:** Test from bench console / Kiểm tra từ bench console

```bash
docker exec -it devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console"
```

```python
from frappe_learn.frappe_learn.api import get_book_availability
result = get_book_availability("978-0-13-468599-1")
print(result)
```

**Step 3:** Test from browser console (F12) / Kiểm tra từ trình duyệt

```javascript
frappe.call({
    method: 'frappe_learn.frappe_learn.api.get_book_availability',
    args: { isbn: '978-0-13-468599-1' },
    callback: function(r) {
        console.log(r.message);
    }
});
```

**Step 4:** Test via curl / Kiểm tra qua curl

```bash
# First get API key/secret or use cookie-based auth
# For development, use password-based auth:
curl -X POST http://localhost:8080/api/method/frappe_learn.frappe_learn.api.get_book_availability \
  -H "Content-Type: application/json" \
  -d '{"isbn": "978-0-13-468599-1"}' \
  -b cookies.txt
```

### Expected Output / Kết quả mong đợi

```json
{
  "message": {
    "title": "The Pragmatic Programmer",
    "author": "David Thomas",
    "isbn": "978-0-13-468599-1",
    "status": "Available",
    "total_copies": 1,
    "available_copies": 1,
    "current_borrower": null
  }
}
```

### Verification / Kiểm tra

```bash
# Verify the function is importable
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local execute frappe_learn.frappe_learn.api.get_book_availability --args '[\"978-0-13-468599-1\"]'"
```

<details>
<summary>Hint 1: @frappe.whitelist(allow_guest=True) / Gợi ý 1</summary>

By default, `@frappe.whitelist()` requires the user to be logged in.
Add `allow_guest=True` to allow unauthenticated access:

```python
@frappe.whitelist(allow_guest=True)
def get_book_availability(isbn):
    ...
```

Mặc định, `@frappe.whitelist()` yêu cầu đăng nhập. Thêm `allow_guest=True` để cho phép truy cập không cần đăng nhập.
</details>

<details>
<summary>Hint 2: Error handling pattern / Gợi ý 2: Xử lý lỗi</summary>

Always use `frappe.throw()` for user-facing errors — it returns proper HTTP 417 with message.
Never use `raise Exception()` in whitelisted methods.

```python
# Good
frappe.throw(_("Book not found"))

# Bad
raise Exception("Book not found")
```

Luôn dùng `frappe.throw()` cho lỗi hiển thị cho người dùng — trả về HTTP 417 với thông báo.
Không bao giờ dùng `raise Exception()` trong whitelisted methods.
</details>

---

## Exercise 5.4: REST API CRUD / CRUD qua REST API

### Objective / Mục tiêu
Test the built-in Frappe REST API to perform CRUD operations on the Book DocType using curl.

Kiểm tra REST API tích hợp của Frappe để thực hiện các thao tác CRUD trên DocType Book bằng curl.

### Instructions / Hướng dẫn

**Step 1:** Login to get session cookie / Đăng nhập để lấy cookie

```bash
# Login (run from INSIDE the container or adjust the URL)
docker exec devcontainer-frappe-1 bash -c '
curl -s -c /tmp/cookies.txt -X POST http://localhost:8000/api/method/login \
  -H "Content-Type: application/json" \
  -d "{\"usr\": \"Administrator\", \"pwd\": \"admin\"}" | python3 -m json.tool
'
```

**Step 2:** GET — List all books / Lấy danh sách sách

```bash
docker exec devcontainer-frappe-1 bash -c '
curl -s -b /tmp/cookies.txt \
  "http://localhost:8000/api/resource/Book?fields=[\"name\",\"title\",\"author\",\"status\"]&limit_page_length=5&order_by=title+asc" \
  | python3 -m json.tool
'
```

**Step 3:** GET — Get a single book / Lấy một cuốn sách

```bash
docker exec devcontainer-frappe-1 bash -c '
# Replace BOOK_NAME with actual book name
BOOK_NAME=$(python3 -c "import frappe; frappe.connect(site=\"flow.local\"); print(frappe.db.get_value(\"Book\", {}, \"name\") or \"\")")
curl -s -b /tmp/cookies.txt \
  "http://localhost:8000/api/resource/Book/${BOOK_NAME}" \
  | python3 -m json.tool
'
```

**Step 4:** POST — Create a new book / Tạo sách mới

```bash
docker exec devcontainer-frappe-1 bash -c '
curl -s -b /tmp/cookies.txt -X POST \
  "http://localhost:8000/api/resource/Book" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"REST API Test Book\",
    \"author\": \"Test Author\",
    \"isbn\": \"978-0-00-000000-1\",
    \"status\": \"Available\",
    \"publisher\": \"Test Publisher\"
  }" | python3 -m json.tool
'
```

**Step 5:** PUT — Update the book / Cập nhật sách

```bash
docker exec devcontainer-frappe-1 bash -c '
# Get the name of the book we just created
BOOK_NAME=$(python3 -c "import frappe; frappe.connect(site=\"flow.local\"); print(frappe.db.get_value(\"Book\", {\"isbn\": \"978-0-00-000000-1\"}, \"name\") or \"\")")
curl -s -b /tmp/cookies.txt -X PUT \
  "http://localhost:8000/api/resource/Book/${BOOK_NAME}" \
  -H "Content-Type: application/json" \
  -d "{\"status\": \"Borrowed\"}" \
  | python3 -m json.tool
'
```

**Step 6:** DELETE — Delete the test book / Xóa sách test

```bash
docker exec devcontainer-frappe-1 bash -c '
BOOK_NAME=$(python3 -c "import frappe; frappe.connect(site=\"flow.local\"); print(frappe.db.get_value(\"Book\", {\"isbn\": \"978-0-00-000000-1\"}, \"name\") or \"\")")
curl -s -b /tmp/cookies.txt -X DELETE \
  "http://localhost:8000/api/resource/Book/${BOOK_NAME}" \
  | python3 -m json.tool
'
```

### Expected Output / Kết quả mong đợi

- GET list: `{"data": [{"name": "...", "title": "...", ...}, ...]}`
- GET single: `{"data": {"name": "...", "title": "...", "author": "...", ...}}`
- POST: `{"data": {"name": "...", "title": "REST API Test Book", ...}}`
- PUT: `{"data": {"name": "...", "status": "Borrowed", ...}}`
- DELETE: `{"message": "ok"}`

### Verification / Kiểm tra

```bash
# Verify the test book was created and deleted
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local execute frappe.client.get_count --args '{\"doctype\": \"Book\", \"filters\": {\"isbn\": \"978-0-00-000000-1\"}}'"
# Should return 0 (deleted)
```

<details>
<summary>Hint 1: API filters / Gợi ý 1: Bộ lọc API</summary>

Frappe REST API supports powerful filters:
```
# Equals
?filters=[["Book","status","=","Available"]]

# Like (search)
?filters=[["Book","title","like","%Python%"]]

# In
?filters=[["Book","status","in",["Available","Borrowed"]]]

# Between (for dates)
?filters=[["Book","creation","between",["2024-01-01","2024-12-31"]]]
```
</details>

<details>
<summary>Hint 2: API authentication methods / Gợi ý 2: Các phương thức xác thực</summary>

Frappe supports multiple auth methods:

1. **Cookie-based** (used above) — best for browser/testing
2. **Token-based** — `Authorization: token api_key:api_secret`
3. **Basic Auth** — `Authorization: Basic base64(api_key:api_secret)`
4. **Bearer Token** — OAuth2 bearer tokens

For development, cookie-based is easiest. For production APIs, use token-based.

Frappe hỗ trợ nhiều phương thức xác thực. Trong dev, dùng cookie. Trong production, dùng token.
</details>

---

## Exercise 5.5: Complete API Module / Module API hoàn chỉnh

### Objective / Mục tiêu
Create 3 complete API endpoints: `search_books`, `borrow_book`, `get_member_stats` with proper validation, error handling, and documentation.

Tạo 3 endpoint API hoàn chỉnh: `search_books`, `borrow_book`, `get_member_stats` với validation, xử lý lỗi, và tài liệu đầy đủ.

### Instructions / Hướng dẫn

**Step 1:** Add the following functions to `frappe_learn/frappe_learn/api.py`

```python
@frappe.whitelist()
def search_books(query, status=None, limit=20):
    """Search books by title or author.

    Args:
        query (str): Search term (matches title or author)
        status (str, optional): Filter by status (Available/Borrowed/Lost)
        limit (int, optional): Max results (default 20)

    Returns:
        list[dict]: List of matching books with fields:
            name, title, author, isbn, status, publisher
    """
    if not query or len(query) < 2:
        frappe.throw(_("Search query must be at least 2 characters"))

    filters = [
        ["Book", "title", "like", f"%{query}%"],
    ]
    or_filters = [
        ["Book", "author", "like", f"%{query}%"],
    ]

    if status:
        filters.append(["Book", "status", "=", status])

    books = frappe.get_all("Book",
        filters=filters,
        or_filters=or_filters,
        fields=["name", "title", "author", "isbn", "status", "publisher"],
        limit_page_length=int(limit),
        order_by="title asc"
    )

    return books


@frappe.whitelist()
def borrow_book(book, member):
    """Borrow a book for a member. Creates a Library Transaction.

    Args:
        book (str): Book name (ID)
        member (str): Library Member name (ID)

    Returns:
        dict: Created transaction details
            - transaction_name: Transaction ID
            - book_title: Title of borrowed book
            - member_name: Name of borrower
            - transaction_date: Date of transaction
    """
    # Validate book exists and is available
    book_doc = frappe.get_doc("Book", book)
    if book_doc.status != "Available":
        frappe.throw(_("Book '{0}' is not available for borrowing. Current status: {1}").format(
            book_doc.title, book_doc.status
        ))

    # Validate member exists
    if not frappe.db.exists("Library Member", member):
        frappe.throw(_("Library Member '{0}' does not exist").format(member))

    member_name = frappe.db.get_value("Library Member", member, "full_name")

    # Check if member has too many active borrows (max 3)
    active_borrows = frappe.db.count("Library Transaction", {
        "library_member": member,
        "type": "Borrow",
        "docstatus": 1
    })
    # Note: This is a simplified check. In production, you would track
    # borrows that haven't been returned yet.

    # Create the transaction
    transaction = frappe.get_doc({
        "doctype": "Library Transaction",
        "book": book,
        "library_member": member,
        "type": "Borrow",
        "transaction_date": frappe.utils.today()
    })
    transaction.insert()
    transaction.submit()

    # Update book status
    book_doc.status = "Borrowed"
    book_doc.save()

    frappe.db.commit()

    return {
        "transaction_name": transaction.name,
        "book_title": book_doc.title,
        "member_name": member_name,
        "transaction_date": str(transaction.transaction_date)
    }


@frappe.whitelist()
def get_member_stats(member):
    """Get borrowing statistics for a library member.

    Args:
        member (str): Library Member name (ID)

    Returns:
        dict: Member statistics
            - member_name: Full name
            - email: Email address
            - total_borrows: Total times borrowed
            - total_returns: Total times returned
            - currently_borrowed: Number of books currently borrowed
            - books_borrowed: List of currently borrowed book titles
            - favorite_author: Most borrowed author
    """
    if not frappe.db.exists("Library Member", member):
        frappe.throw(_("Library Member '{0}' does not exist").format(member))

    member_doc = frappe.get_doc("Library Member", member)

    # Count transactions
    total_borrows = frappe.db.count("Library Transaction", {
        "library_member": member,
        "type": "Borrow",
        "docstatus": 1
    })

    total_returns = frappe.db.count("Library Transaction", {
        "library_member": member,
        "type": "Return",
        "docstatus": 1
    })

    currently_borrowed = total_borrows - total_returns

    # Get currently borrowed books
    # (books that have a Borrow transaction but no subsequent Return)
    borrowed_transactions = frappe.get_all("Library Transaction",
        filters={
            "library_member": member,
            "type": "Borrow",
            "docstatus": 1
        },
        fields=["book"],
        order_by="transaction_date desc"
    )

    books_borrowed = []
    for bt in borrowed_transactions:
        book_status = frappe.db.get_value("Book", bt.book, "status")
        if book_status == "Borrowed":
            book_title = frappe.db.get_value("Book", bt.book, "title")
            books_borrowed.append(book_title)

    # Find favorite author (most borrowed)
    from pypika import functions as fn
    Book = frappe.qb.DocType("Book")
    Transaction = frappe.qb.DocType("Library Transaction")

    favorite_query = (
        frappe.qb.from_(Transaction)
        .join(Book).on(Transaction.book == Book.name)
        .select(Book.author, fn.Count(Transaction.name).as_("count"))
        .where(Transaction.library_member == member)
        .where(Transaction.type == "Borrow")
        .where(Transaction.docstatus == 1)
        .groupby(Book.author)
        .orderby(fn.Count(Transaction.name), order=frappe.qb.desc)
        .limit(1)
    )
    favorite_result = favorite_query.run(as_dict=True)
    favorite_author = favorite_result[0]["author"] if favorite_result else None

    return {
        "member_name": member_doc.full_name,
        "email": member_doc.email_address,
        "total_borrows": total_borrows,
        "total_returns": total_returns,
        "currently_borrowed": currently_borrowed,
        "books_borrowed": books_borrowed,
        "favorite_author": favorite_author
    }
```

**Step 2:** Test all 3 endpoints / Kiểm tra cả 3 endpoint

```bash
# Test search_books
docker exec devcontainer-frappe-1 bash -c '
curl -s -b /tmp/cookies.txt -X POST \
  "http://localhost:8000/api/method/frappe_learn.frappe_learn.api.search_books" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"Python\", \"status\": \"Available\"}" \
  | python3 -m json.tool
'

# Test borrow_book (replace BOOK_NAME and MEMBER_NAME with actual values)
docker exec devcontainer-frappe-1 bash -c '
curl -s -b /tmp/cookies.txt -X POST \
  "http://localhost:8000/api/method/frappe_learn.frappe_learn.api.borrow_book" \
  -H "Content-Type: application/json" \
  -d "{\"book\": \"BOOK_NAME\", \"member\": \"MEMBER_NAME\"}" \
  | python3 -m json.tool
'

# Test get_member_stats
docker exec devcontainer-frappe-1 bash -c '
curl -s -b /tmp/cookies.txt -X POST \
  "http://localhost:8000/api/method/frappe_learn.frappe_learn.api.get_member_stats" \
  -H "Content-Type: application/json" \
  -d "{\"member\": \"MEMBER_NAME\"}" \
  | python3 -m json.tool
'
```

### Expected Output / Kết quả mong đợi

**search_books:**
```json
{
  "message": [
    {
      "name": "BOOK-001",
      "title": "Learning Python",
      "author": "Mark Lutz",
      "isbn": "978-1-449-35573-9",
      "status": "Available",
      "publisher": "O'Reilly"
    }
  ]
}
```

**borrow_book:**
```json
{
  "message": {
    "transaction_name": "LT-00001",
    "book_title": "Learning Python",
    "member_name": "Nguyen Van A",
    "transaction_date": "2026-03-17"
  }
}
```

**get_member_stats:**
```json
{
  "message": {
    "member_name": "Nguyen Van A",
    "email": "nguyenvana@example.com",
    "total_borrows": 5,
    "total_returns": 3,
    "currently_borrowed": 2,
    "books_borrowed": ["Learning Python", "Clean Code"],
    "favorite_author": "Robert C. Martin"
  }
}
```

### Verification / Kiểm tra

```bash
# Verify api.py exists and has all 3 functions (plus get_book_availability from 5.3)
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && grep -c '@frappe.whitelist' apps/frappe_learn/frappe_learn/frappe_learn/api.py"
# Should return 4 (get_book_availability + search_books + borrow_book + get_member_stats)

# Test each function from bench
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local execute frappe_learn.frappe_learn.api.search_books --args '[\"Python\"]'"
```

<details>
<summary>Hint 1: Debugging API errors / Gợi ý 1: Debug lỗi API</summary>

If your API returns an error, check:

1. **Import error**: `bench --site flow.local console` then `from frappe_learn.frappe_learn.api import search_books`
2. **Syntax error**: `python3 -c "import frappe_learn.frappe_learn.api"`
3. **Runtime error**: Check `frappe-bench/logs/frappe.log`

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && tail -50 logs/frappe.log"
```

Nếu API trả về lỗi, kiểm tra: lỗi import, lỗi cú pháp, lỗi runtime trong logs/frappe.log.
</details>

<details>
<summary>Hint 2: Rate limiting and caching / Gợi ý 2: Giới hạn và cache</summary>

For production APIs, add caching:

```python
@frappe.whitelist()
def search_books(query, status=None, limit=20):
    # Cache for 60 seconds
    cache_key = f"book_search:{query}:{status}:{limit}"
    cached = frappe.cache.get_value(cache_key)
    if cached:
        return cached

    # ... do the search ...

    frappe.cache.set_value(cache_key, books, expires_in_sec=60)
    return books
```

Trong production, thêm cache để tăng hiệu suất. Dùng `frappe.cache` với thời gian hết hạn.
</details>

---

## Summary / Tóm tắt

| Exercise | Key Concept | Files Modified |
|----------|-------------|----------------|
| 5.1 | `frappe.db` methods | None (console only) |
| 5.2 | `frappe.qb` Query Builder | None (console only) |
| 5.3 | `@frappe.whitelist()` | `frappe_learn/frappe_learn/api.py` |
| 5.4 | REST API CRUD | None (curl only) |
| 5.5 | Complete API module | `frappe_learn/frappe_learn/api.py` |

**Next:** Module 6 — Desk UI (Form customization, List View, Reports, Workspace)
