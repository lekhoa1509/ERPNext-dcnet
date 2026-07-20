# Module 2 Exercises: DocType Mastery
# Bài tập Module 2: Làm chủ DocType

> **Điều kiện tiên quyết / Prerequisites:** Hoàn thành Module 1 — app `frappe_learn` đã cài vào site `flow.local`, module "Library" đã tạo.
>
> **Environment / Môi trường:**
> - Container: `devcontainer-frappe-1`
> - Bench path: `/workspace/development/frappe-bench`
> - Site: `flow.local`
> - App path: `apps/frappe_learn/frappe_learn/library/`
> - Prefix for all commands:
>   ```bash
>   docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && <command>"
>   ```

---

## Exercise 2.1: Tạo DocType "Book" / Create DocType "Book"

### Mục tiêu / Objective
Tạo DocType đầu tiên — "Book" với các trường cơ bản. Hiểu cách Frappe tạo database table từ DocType definition.
Create your first DocType — "Book" with basic fields. Understand how Frappe creates database tables from DocType definitions.

### Bước thực hiện / Steps

**Step 1:** Tạo thư mục cho DocType / Create DocType directory
```bash
docker exec devcontainer-frappe-1 bash -c "mkdir -p /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/library/doctype/book"
docker exec devcontainer-frappe-1 bash -c "touch /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/library/doctype/__init__.py"
docker exec devcontainer-frappe-1 bash -c "touch /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/library/doctype/book/__init__.py"
```

**Step 2:** Tạo file `book.json` — DocType definition / Create DocType JSON
Tạo file `apps/frappe_learn/frappe_learn/library/doctype/book/book.json`:

```json
{
  "actions": [],
  "autoname": "format:BOOK-{####}",
  "creation": "2026-03-17 10:00:00.000000",
  "doctype": "DocType",
  "engine": "InnoDB",
  "field_order": [
    "title",
    "author",
    "isbn",
    "column_break_1",
    "status",
    "publisher",
    "publication_date",
    "section_break_1",
    "description"
  ],
  "fields": [
    {
      "fieldname": "title",
      "fieldtype": "Data",
      "in_list_view": 1,
      "in_standard_filter": 1,
      "label": "Title",
      "reqd": 1
    },
    {
      "fieldname": "author",
      "fieldtype": "Data",
      "in_list_view": 1,
      "in_standard_filter": 1,
      "label": "Author"
    },
    {
      "fieldname": "isbn",
      "fieldtype": "Data",
      "in_list_view": 1,
      "label": "ISBN",
      "unique": 1
    },
    {
      "fieldname": "column_break_1",
      "fieldtype": "Column Break"
    },
    {
      "default": "Available",
      "fieldname": "status",
      "fieldtype": "Select",
      "in_list_view": 1,
      "in_standard_filter": 1,
      "label": "Status",
      "options": "Available\nBorrowed\nLost"
    },
    {
      "fieldname": "publisher",
      "fieldtype": "Data",
      "label": "Publisher"
    },
    {
      "fieldname": "publication_date",
      "fieldtype": "Date",
      "label": "Publication Date"
    },
    {
      "fieldname": "section_break_1",
      "fieldtype": "Section Break",
      "label": "Details"
    },
    {
      "fieldname": "description",
      "fieldtype": "Text Editor",
      "label": "Description"
    }
  ],
  "links": [],
  "modified": "2026-03-17 10:00:00.000000",
  "modified_by": "Administrator",
  "module": "Library",
  "name": "Book",
  "naming_rule": "Expression",
  "owner": "Administrator",
  "permissions": [
    {
      "create": 1,
      "delete": 1,
      "email": 1,
      "export": 1,
      "print": 1,
      "read": 1,
      "report": 1,
      "role": "System Manager",
      "share": 1,
      "write": 1
    }
  ],
  "quick_entry": 0,
  "sort_field": "creation",
  "sort_order": "DESC",
  "title_field": "title",
  "track_changes": 1
}
```

**Step 3:** Tạo file Python controller / Create Python controller
Tạo file `apps/frappe_learn/frappe_learn/library/doctype/book/book.py`:

```python
# Copyright (c) 2026, DCNET and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Book(Document):
    pass
```

**Step 4:** Chạy migrate / Run migrate
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local migrate"
```

**Step 5:** Tạo bản ghi thử nghiệm / Create test record
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
book = frappe.get_doc({
    "doctype": "Book",
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "isbn": "9780132350884",
    "status": "Available",
    "publisher": "Prentice Hall",
    "publication_date": "2008-08-01"
})
book.insert()
frappe.db.commit()
print(f"Created: {book.name} - {book.title}")
EOF
```

### Kết quả mong đợi / Expected Output
- Table `tabBook` được tạo trong database
- DocType "Book" xuất hiện trong desk tại `/app/book`
- Bản ghi "Clean Code" được tạo với name `BOOK-0001`
- List view hiển thị các cột: Title, Author, ISBN, Status

### Kiểm tra / Verification
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
count = frappe.db.count("Book")
print(f"Book count: {count}")
book = frappe.get_last_doc("Book")
print(f"Last book: {book.name} - {book.title} by {book.author}")
print(f"Status: {book.status}, ISBN: {book.isbn}")
EOF
```

<details>
<summary>Gợi ý / Hints</summary>

- Mỗi DocType = 1 JSON file (schema) + 1 Python file (controller) + 1 database table
- `autoname: "format:BOOK-{####}"` tạo tên tự động: BOOK-0001, BOOK-0002...
- `in_list_view: 1` để trường hiển thị trong danh sách
- `in_standard_filter: 1` để trường xuất hiện trong filter sidebar
- `unique: 1` tạo UNIQUE constraint trong database
- `title_field` quyết định tên hiển thị trong Link field và breadcrumb
- Column Break / Section Break là layout elements, không lưu vào database
- Nếu migrate lỗi, kiểm tra JSON syntax với `python -m json.tool book.json`
- Bạn cũng có thể tạo DocType qua UI: `/app/doctype/new-doctype-1` — nhưng code-first là best practice

</details>

---

## Exercise 2.2: Tạo DocType "Library Member" / Create DocType "Library Member"

### Mục tiêu / Objective
Tạo DocType "Library Member" để quản lý thành viên thư viện. Luyện tập thêm với các field types khác nhau.
Create "Library Member" DocType to manage library members. Practice with different field types.

### Bước thực hiện / Steps

**Step 1:** Tạo thư mục / Create directory
```bash
docker exec devcontainer-frappe-1 bash -c "mkdir -p /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/library/doctype/library_member"
docker exec devcontainer-frappe-1 bash -c "touch /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/library/doctype/library_member/__init__.py"
```

**Step 2:** Tạo file `library_member.json` / Create DocType JSON
Tạo file `apps/frappe_learn/frappe_learn/library/doctype/library_member/library_member.json`:

```json
{
  "actions": [],
  "autoname": "format:MEM-{####}",
  "creation": "2026-03-17 10:00:00.000000",
  "doctype": "DocType",
  "engine": "InnoDB",
  "field_order": [
    "full_name",
    "email",
    "phone",
    "column_break_1",
    "membership_date",
    "member_type",
    "active",
    "section_break_1",
    "address"
  ],
  "fields": [
    {
      "fieldname": "full_name",
      "fieldtype": "Data",
      "in_list_view": 1,
      "in_standard_filter": 1,
      "label": "Full Name",
      "reqd": 1
    },
    {
      "fieldname": "email",
      "fieldtype": "Data",
      "in_list_view": 1,
      "label": "Email",
      "options": "Email"
    },
    {
      "fieldname": "phone",
      "fieldtype": "Data",
      "label": "Phone",
      "options": "Phone"
    },
    {
      "fieldname": "column_break_1",
      "fieldtype": "Column Break"
    },
    {
      "default": "Today",
      "fieldname": "membership_date",
      "fieldtype": "Date",
      "in_list_view": 1,
      "label": "Membership Date"
    },
    {
      "default": "General",
      "fieldname": "member_type",
      "fieldtype": "Select",
      "in_list_view": 1,
      "in_standard_filter": 1,
      "label": "Member Type",
      "options": "Student\nTeacher\nGeneral"
    },
    {
      "default": "1",
      "fieldname": "active",
      "fieldtype": "Check",
      "label": "Active"
    },
    {
      "fieldname": "section_break_1",
      "fieldtype": "Section Break",
      "label": "Contact Details"
    },
    {
      "fieldname": "address",
      "fieldtype": "Small Text",
      "label": "Address"
    }
  ],
  "links": [],
  "modified": "2026-03-17 10:00:00.000000",
  "modified_by": "Administrator",
  "module": "Library",
  "name": "Library Member",
  "naming_rule": "Expression",
  "owner": "Administrator",
  "permissions": [
    {
      "create": 1,
      "delete": 1,
      "email": 1,
      "export": 1,
      "print": 1,
      "read": 1,
      "report": 1,
      "role": "System Manager",
      "share": 1,
      "write": 1
    }
  ],
  "quick_entry": 0,
  "sort_field": "creation",
  "sort_order": "DESC",
  "title_field": "full_name",
  "track_changes": 1
}
```

**Step 3:** Tạo Python controller / Create Python controller
Tạo file `apps/frappe_learn/frappe_learn/library/doctype/library_member/library_member.py`:

```python
# Copyright (c) 2026, DCNET and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LibraryMember(Document):
    pass
```

**Step 4:** Migrate và tạo dữ liệu mẫu / Migrate and create sample data
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local migrate"
```

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
members = [
    {"full_name": "Nguyen Van A", "email": "a@example.com", "member_type": "Student"},
    {"full_name": "Tran Thi B", "email": "b@example.com", "member_type": "Teacher"},
    {"full_name": "Le Van C", "email": "c@example.com", "member_type": "General"},
]
for m in members:
    doc = frappe.get_doc({"doctype": "Library Member", **m})
    doc.insert()
    print(f"Created: {doc.name} - {doc.full_name} ({doc.member_type})")
frappe.db.commit()
EOF
```

### Kết quả mong đợi / Expected Output
- Table `tabLibrary Member` được tạo
- 3 thành viên được tạo: MEM-0001, MEM-0002, MEM-0003
- Truy cập `/app/library-member` thấy danh sách thành viên
- Email field có validation tự động (nhờ `options: "Email"`)
- Membership Date mặc định là ngày hôm nay (nhờ `default: "Today"`)

### Kiểm tra / Verification
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
count = frappe.db.count("Library Member")
print(f"Library Member count: {count}")
members = frappe.get_all("Library Member", fields=["name", "full_name", "member_type"])
for m in members:
    print(f"  {m.name}: {m.full_name} ({m.member_type})")
EOF
```

<details>
<summary>Gợi ý / Hints</summary>

- `options: "Email"` trên Data field tạo email validation và mailto link
- `options: "Phone"` trên Data field tạo phone validation và tel link
- `default: "Today"` là Frappe special value — tự động điền ngày hiện tại
- `default: "1"` cho Check field = checked by default
- `title_field: "full_name"` làm cho Link field hiển thị tên thay vì MEM-0001
- DocType name phải CHÍNH XÁC khớp với folder name (convert: "Library Member" → `library_member/`)
- Frappe tự động tạo URL slug: "Library Member" → `/app/library-member`

</details>

---

## Exercise 2.3: Tạo Child DocType "Book Copy" / Create Child DocType "Book Copy"

### Mục tiêu / Objective
Tạo Child DocType "Book Copy" và thêm nó như child table vào DocType "Book". Hiểu sự khác biệt giữa regular DocType và Child DocType.
Create Child DocType "Book Copy" and add it as a child table to "Book" DocType. Understand the difference between regular and child DocTypes.

### Bước thực hiện / Steps

**Step 1:** Tạo thư mục cho Child DocType / Create directory
```bash
docker exec devcontainer-frappe-1 bash -c "mkdir -p /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/library/doctype/book_copy"
docker exec devcontainer-frappe-1 bash -c "touch /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/library/doctype/book_copy/__init__.py"
```

**Step 2:** Tạo file `book_copy.json` / Create Child DocType JSON
Tạo file `apps/frappe_learn/frappe_learn/library/doctype/book_copy/book_copy.json`:

```json
{
  "actions": [],
  "creation": "2026-03-17 10:00:00.000000",
  "doctype": "DocType",
  "engine": "InnoDB",
  "field_order": [
    "copy_number",
    "condition",
    "location"
  ],
  "fields": [
    {
      "fieldname": "copy_number",
      "fieldtype": "Int",
      "in_list_view": 1,
      "label": "Copy Number",
      "reqd": 1
    },
    {
      "default": "Good",
      "fieldname": "condition",
      "fieldtype": "Select",
      "in_list_view": 1,
      "label": "Condition",
      "options": "New\nGood\nFair\nPoor\nDamaged"
    },
    {
      "fieldname": "location",
      "fieldtype": "Data",
      "in_list_view": 1,
      "label": "Location"
    }
  ],
  "istable": 1,
  "links": [],
  "modified": "2026-03-17 10:00:00.000000",
  "modified_by": "Administrator",
  "module": "Library",
  "name": "Book Copy",
  "naming_rule": "Random",
  "owner": "Administrator",
  "permissions": [],
  "sort_field": "creation",
  "sort_order": "DESC"
}
```

**Step 3:** Tạo Python controller cho Child DocType / Create child Python controller
Tạo file `apps/frappe_learn/frappe_learn/library/doctype/book_copy/book_copy.py`:

```python
# Copyright (c) 2026, DCNET and contributors
# For license information, please see license.txt

from frappe.model.document import Document


class BookCopy(Document):
    pass
```

**Step 4:** Cập nhật `book.json` — thêm child table field / Update book.json with child table
Thêm field sau vào mảng `fields` trong `book.json` (trước `description`), và cập nhật `field_order`:

Thêm vào `field_order` (trước `section_break_1`):
```
"copies_section",
"copies"
```

Thêm vào `fields` (trước `section_break_1` field):
```json
{
    "fieldname": "copies_section",
    "fieldtype": "Section Break",
    "label": "Copies"
},
{
    "fieldname": "copies",
    "fieldtype": "Table",
    "label": "Book Copies",
    "options": "Book Copy"
}
```

**Step 5:** Migrate và test / Migrate and test
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local migrate"
```

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
# Thêm copies vào book đã tạo trước đó
book = frappe.get_last_doc("Book")
book.append("copies", {
    "copy_number": 1,
    "condition": "New",
    "location": "Shelf A-01"
})
book.append("copies", {
    "copy_number": 2,
    "condition": "Good",
    "location": "Shelf A-02"
})
book.save()
frappe.db.commit()
print(f"Book: {book.title}")
print(f"Copies: {len(book.copies)}")
for c in book.copies:
    print(f"  Copy #{c.copy_number}: {c.condition} at {c.location}")
EOF
```

### Kết quả mong đợi / Expected Output
- Table `tabBook Copy` được tạo trong database
- DocType "Book Copy" có `istable: 1` — nghĩa là chỉ xuất hiện như child table, KHÔNG có list view riêng
- Book form hiển thị bảng "Book Copies" với 3 cột: Copy Number, Condition, Location
- 2 bản ghi copy được tạo trong book "Clean Code"

### Kiểm tra / Verification
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
book = frappe.get_last_doc("Book")
print(f"Book '{book.title}' has {len(book.copies)} copies")
copies_in_db = frappe.db.count("Book Copy", {"parent": book.name})
print(f"Copies in DB for {book.name}: {copies_in_db}")
EOF
```

<details>
<summary>Gợi ý / Hints</summary>

- **Child DocType** có `"istable": 1` — khác với regular DocType
- Child DocType KHÔNG có permissions riêng — kế thừa từ parent
- Child DocType KHÔNG có `autoname` — dùng `naming_rule: "Random"` (hash-based)
- Mỗi child row tự động có các field: `parent`, `parenttype`, `parentfield`, `idx`
- `options: "Book Copy"` trong Table field chỉ đến tên Child DocType
- `book.append("copies", {...})` là cách chuẩn để thêm child row
- `in_list_view: 1` cho child field = hiển thị trực tiếp trong bảng (không cần mở dialog)
- Child table có giới hạn mặc định 500 rows — có thể tăng trong site_config

</details>

---

## Exercise 2.4: Tạo DocType "Library Transaction" / Create DocType "Library Transaction"

### Mục tiêu / Objective
Tạo DocType "Library Transaction" với Link fields — liên kết với Book và Library Member. Hiểu cách Frappe xử lý relationships giữa các DocType.
Create "Library Transaction" DocType with Link fields — connecting Book and Library Member. Understand how Frappe handles relationships between DocTypes.

### Bước thực hiện / Steps

**Step 1:** Tạo thư mục / Create directory
```bash
docker exec devcontainer-frappe-1 bash -c "mkdir -p /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/library/doctype/library_transaction"
docker exec devcontainer-frappe-1 bash -c "touch /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/library/doctype/library_transaction/__init__.py"
```

**Step 2:** Tạo file `library_transaction.json` / Create DocType JSON
Tạo file `apps/frappe_learn/frappe_learn/library/doctype/library_transaction/library_transaction.json`:

```json
{
  "actions": [],
  "autoname": "format:TXN-{####}",
  "creation": "2026-03-17 10:00:00.000000",
  "doctype": "DocType",
  "engine": "InnoDB",
  "field_order": [
    "book",
    "book_title",
    "member",
    "member_name",
    "column_break_1",
    "transaction_type",
    "transaction_date",
    "due_date",
    "return_date",
    "section_break_1",
    "notes",
    "amended_from"
  ],
  "fields": [
    {
      "fieldname": "book",
      "fieldtype": "Link",
      "in_list_view": 1,
      "in_standard_filter": 1,
      "label": "Book",
      "options": "Book",
      "reqd": 1
    },
    {
      "fetch_from": "book.title",
      "fieldname": "book_title",
      "fieldtype": "Data",
      "in_list_view": 1,
      "label": "Book Title",
      "read_only": 1
    },
    {
      "fieldname": "member",
      "fieldtype": "Link",
      "in_list_view": 1,
      "in_standard_filter": 1,
      "label": "Member",
      "options": "Library Member",
      "reqd": 1
    },
    {
      "fetch_from": "member.full_name",
      "fieldname": "member_name",
      "fieldtype": "Data",
      "in_list_view": 1,
      "label": "Member Name",
      "read_only": 1
    },
    {
      "fieldname": "column_break_1",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "transaction_type",
      "fieldtype": "Select",
      "in_list_view": 1,
      "in_standard_filter": 1,
      "label": "Transaction Type",
      "options": "Borrow\nReturn",
      "reqd": 1
    },
    {
      "default": "Today",
      "fieldname": "transaction_date",
      "fieldtype": "Date",
      "in_list_view": 1,
      "label": "Transaction Date",
      "reqd": 1
    },
    {
      "depends_on": "eval:doc.transaction_type=='Borrow'",
      "fieldname": "due_date",
      "fieldtype": "Date",
      "label": "Due Date"
    },
    {
      "depends_on": "eval:doc.transaction_type=='Return'",
      "fieldname": "return_date",
      "fieldtype": "Date",
      "label": "Return Date"
    },
    {
      "fieldname": "section_break_1",
      "fieldtype": "Section Break",
      "label": "Additional Information"
    },
    {
      "fieldname": "notes",
      "fieldtype": "Small Text",
      "label": "Notes"
    },
    {
      "fieldname": "amended_from",
      "fieldtype": "Link",
      "label": "Amended From",
      "no_copy": 1,
      "options": "Library Transaction",
      "print_hide": 1,
      "read_only": 1
    }
  ],
  "is_submittable": 1,
  "links": [],
  "modified": "2026-03-17 10:00:00.000000",
  "modified_by": "Administrator",
  "module": "Library",
  "name": "Library Transaction",
  "naming_rule": "Expression",
  "owner": "Administrator",
  "permissions": [
    {
      "create": 1,
      "delete": 1,
      "email": 1,
      "export": 1,
      "print": 1,
      "read": 1,
      "report": 1,
      "role": "System Manager",
      "share": 1,
      "submit": 1,
      "write": 1,
      "cancel": 1,
      "amend": 1
    }
  ],
  "quick_entry": 0,
  "sort_field": "creation",
  "sort_order": "DESC",
  "track_changes": 1
}
```

**Step 3:** Tạo Python controller / Create Python controller
Tạo file `apps/frappe_learn/frappe_learn/library/doctype/library_transaction/library_transaction.py`:

```python
# Copyright (c) 2026, DCNET and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LibraryTransaction(Document):
    pass
```

**Step 4:** Migrate và tạo dữ liệu / Migrate and create data
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local migrate"
```

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
book = frappe.get_last_doc("Book")
member = frappe.get_last_doc("Library Member")

txn = frappe.get_doc({
    "doctype": "Library Transaction",
    "book": book.name,
    "member": member.name,
    "transaction_type": "Borrow",
    "transaction_date": frappe.utils.today(),
    "due_date": frappe.utils.add_days(frappe.utils.today(), 14)
})
txn.insert()
txn.submit()
frappe.db.commit()
print(f"Created transaction: {txn.name}")
print(f"  Book: {txn.book_title}")
print(f"  Member: {txn.member_name}")
print(f"  Type: {txn.transaction_type}")
print(f"  Due: {txn.due_date}")
print(f"  DocStatus: {txn.docstatus} (1=Submitted)")
EOF
```

### Kết quả mong đợi / Expected Output
- DocType "Library Transaction" được tạo với `is_submittable: 1`
- Form có nút Submit (vì `is_submittable`)
- `book_title` tự động fill khi chọn Book (nhờ `fetch_from`)
- `member_name` tự động fill khi chọn Member (nhờ `fetch_from`)
- `due_date` chỉ hiện khi `transaction_type == "Borrow"` (nhờ `depends_on`)
- `return_date` chỉ hiện khi `transaction_type == "Return"` (nhờ `depends_on`)
- Transaction được submit thành công (docstatus = 1)

### Kiểm tra / Verification
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
txn = frappe.get_last_doc("Library Transaction")
print(f"Transaction: {txn.name}")
print(f"DocStatus: {txn.docstatus}")
print(f"Book title auto-fetched: {bool(txn.book_title)}")
print(f"Member name auto-fetched: {bool(txn.member_name)}")
# Verify link integrity
book_exists = frappe.db.exists("Book", txn.book)
member_exists = frappe.db.exists("Library Member", txn.member)
print(f"Book link valid: {bool(book_exists)}")
print(f"Member link valid: {bool(member_exists)}")
EOF
```

<details>
<summary>Gợi ý / Hints</summary>

- **`is_submittable: 1`** tạo DocType có workflow: Draft (0) → Submitted (1) → Cancelled (2)
- Submitted doc KHÔNG thể edit trực tiếp — phải Cancel rồi Amend
- `amended_from` field là BẮT BUỘC cho submittable DocType — Frappe dùng nó để track amendments
- **`fetch_from: "book.title"`** tự động copy giá trị khi chọn Link — giống VLOOKUP trong Excel
- **`depends_on: "eval:doc.transaction_type=='Borrow'"`** ẩn/hiện field theo điều kiện
- Link field `options` phải CHÍNH XÁC là tên DocType (case-sensitive)
- Permissions cho submittable: cần thêm `submit`, `cancel`, `amend` ngoài CRUD cơ bản
- `frappe.utils.add_days(date, n)` là utility function hay dùng để tính ngày

</details>

---

## Exercise 2.5: Tạo Workflow cho Library Transaction / Create Workflow for Library Transaction

### Mục tiêu / Objective
Tạo Workflow với nhiều trạng thái và transitions cho Library Transaction. Hiểu cách Frappe Workflow hoạt động.
Create a Workflow with multiple states and transitions for Library Transaction. Understand how Frappe Workflow works.

### Bước thực hiện / Steps

**Step 1:** Tạo Workflow qua bench console / Create Workflow via console

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
# Tạo Workflow States trước (nếu chưa có)
for state in ["Pending Approval", "Approved", "Completed", "Rejected"]:
    if not frappe.db.exists("Workflow State", state):
        frappe.get_doc({
            "doctype": "Workflow State",
            "workflow_state_name": state,
            "style": "Primary" if state == "Approved" else ("Success" if state == "Completed" else ("Danger" if state == "Rejected" else "Warning"))
        }).insert()
        print(f"Created Workflow State: {state}")

# Tạo Workflow Action (nếu chưa có)
for action in ["Approve", "Reject", "Complete", "Request Approval"]:
    if not frappe.db.exists("Workflow Action Master", action):
        frappe.get_doc({
            "doctype": "Workflow Action Master",
            "workflow_action_name": action
        }).insert()
        print(f"Created Workflow Action: {action}")

frappe.db.commit()
print("Workflow prerequisites created!")
EOF
```

**Step 2:** Tạo Workflow chính / Create the main Workflow

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
# Xóa workflow cũ nếu có
if frappe.db.exists("Workflow", "Library Transaction Approval"):
    frappe.delete_doc("Workflow", "Library Transaction Approval", force=True)

workflow = frappe.get_doc({
    "doctype": "Workflow",
    "workflow_name": "Library Transaction Approval",
    "document_type": "Library Transaction",
    "is_active": 1,
    "send_email_alert": 0,
    "states": [
        {
            "state": "Draft",
            "doc_status": "0",
            "allow_edit": "System Manager",
            "is_optional_state": 0
        },
        {
            "state": "Pending Approval",
            "doc_status": "0",
            "allow_edit": "System Manager",
            "is_optional_state": 0
        },
        {
            "state": "Approved",
            "doc_status": "1",
            "allow_edit": "System Manager",
            "is_optional_state": 0
        },
        {
            "state": "Completed",
            "doc_status": "1",
            "allow_edit": "System Manager",
            "is_optional_state": 0
        },
        {
            "state": "Rejected",
            "doc_status": "0",
            "allow_edit": "System Manager",
            "is_optional_state": 0
        }
    ],
    "transitions": [
        {
            "state": "Draft",
            "action": "Request Approval",
            "next_state": "Pending Approval",
            "allowed": "System Manager"
        },
        {
            "state": "Pending Approval",
            "action": "Approve",
            "next_state": "Approved",
            "allowed": "System Manager"
        },
        {
            "state": "Pending Approval",
            "action": "Reject",
            "next_state": "Rejected",
            "allowed": "System Manager"
        },
        {
            "state": "Approved",
            "action": "Complete",
            "next_state": "Completed",
            "allowed": "System Manager"
        }
    ]
})
workflow.insert()
frappe.db.commit()
print(f"Workflow created: {workflow.name}")
print(f"States: {[s.state for s in workflow.states]}")
print(f"Transitions: {[f'{t.state} --{t.action}--> {t.next_state}' for t in workflow.transitions]}")
EOF
```

**Step 3:** Test workflow / Test the workflow

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
book = frappe.get_last_doc("Book")
member = frappe.get_last_doc("Library Member")

# Tạo transaction mới
txn = frappe.get_doc({
    "doctype": "Library Transaction",
    "book": book.name,
    "member": member.name,
    "transaction_type": "Borrow",
    "transaction_date": frappe.utils.today(),
    "due_date": frappe.utils.add_days(frappe.utils.today(), 14)
})
txn.insert()
frappe.db.commit()
print(f"1. Created: {txn.name}, State: {txn.workflow_state}")

# Request Approval
frappe.model.workflow.apply_workflow(txn, "Request Approval")
frappe.db.commit()
txn.reload()
print(f"2. After Request Approval: State: {txn.workflow_state}")

# Approve
frappe.model.workflow.apply_workflow(txn, "Approve")
frappe.db.commit()
txn.reload()
print(f"3. After Approve: State: {txn.workflow_state}, DocStatus: {txn.docstatus}")

# Complete
frappe.model.workflow.apply_workflow(txn, "Complete")
frappe.db.commit()
txn.reload()
print(f"4. After Complete: State: {txn.workflow_state}, DocStatus: {txn.docstatus}")
EOF
```

### Kết quả mong đợi / Expected Output
- Workflow "Library Transaction Approval" được tạo
- Luồng trạng thái: Draft → Pending Approval → Approved → Completed
- Nhánh phụ: Pending Approval → Rejected
- Khi Approve, docstatus tự động chuyển từ 0 (Draft) sang 1 (Submitted)
- Form hiển thị nút action tương ứng với trạng thái hiện tại

### Workflow Diagram
```
Draft --[Request Approval]--> Pending Approval
Pending Approval --[Approve]--> Approved (docstatus=1, submitted)
Pending Approval --[Reject]--> Rejected (docstatus=0, stays draft)
Approved --[Complete]--> Completed (docstatus=1, stays submitted)
```

### Kiểm tra / Verification
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
wf = frappe.get_doc("Workflow", "Library Transaction Approval")
print(f"Workflow: {wf.name}")
print(f"Active: {wf.is_active}")
print(f"Document Type: {wf.document_type}")
print(f"States ({len(wf.states)}):")
for s in wf.states:
    print(f"  - {s.state} (docstatus={s.doc_status})")
print(f"Transitions ({len(wf.transitions)}):")
for t in wf.transitions:
    print(f"  - {t.state} --[{t.action}]--> {t.next_state}")
EOF
```

<details>
<summary>Gợi ý / Hints</summary>

- Frappe Workflow THAY THẾ submit/cancel button bằng custom action buttons
- `doc_status` trong Workflow State: "0" = Draft, "1" = Submitted, "2" = Cancelled
- Mỗi state chỉ cho phép certain roles edit (field `allow_edit`)
- `workflow_state` field tự động được thêm vào DocType khi có Workflow active
- Workflow chỉ active cho 1 DocType tại 1 thời điểm — nếu có nhiều workflow, chỉ 1 cái `is_active`
- Để tắt workflow: set `is_active = 0` hoặc xóa Workflow doc
- Trong production, dùng các Role khác nhau cho mỗi transition (VD: "Librarian" approve, "Library Manager" complete)
- **Lưu ý:** Nếu đã có transaction với workflow, xóa workflow có thể gây lỗi — phải cập nhật `workflow_state` trước

</details>

---

## Tổng kết Module 2 / Module 2 Summary

Sau khi hoàn thành tất cả bài tập, bạn đã tạo:
After completing all exercises, you have created:

| DocType | Loại / Type | Fields | Đặc điểm / Features |
|---------|-------------|--------|---------------------|
| Book | Regular | title, author, isbn, status, publisher, publication_date, copies (table) | autoname, unique isbn, title_field |
| Book Copy | Child Table | copy_number, condition, location | istable=1, in Book |
| Library Member | Regular | full_name, email, phone, membership_date, member_type, active | autoname, email validation |
| Library Transaction | Submittable | book (Link), member (Link), transaction_type, dates | is_submittable, fetch_from, depends_on, Workflow |

| # | Kỹ năng / Skill | Trạng thái / Status |
|---|-----------------|---------------------|
| 2.1 | Tạo DocType cơ bản với các field types | [ ] |
| 2.2 | Tạo DocType với special field options | [ ] |
| 2.3 | Tạo Child DocType và Table field | [ ] |
| 2.4 | Tạo Submittable DocType với Link và fetch_from | [ ] |
| 2.5 | Tạo và test Workflow | [ ] |

### Verification toàn bộ / Full Module Verification
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
doctypes = ["Book", "Book Copy", "Library Member", "Library Transaction"]
for dt in doctypes:
    exists = frappe.db.exists("DocType", dt)
    count = frappe.db.count(dt) if exists else 0
    print(f"{'OK' if exists else 'MISSING'}: {dt} ({count} records)")

wf_exists = frappe.db.exists("Workflow", "Library Transaction Approval")
print(f"{'OK' if wf_exists else 'MISSING'}: Workflow 'Library Transaction Approval'")
EOF
```

> **Tiếp theo / Next:** [Exercise 03 - Client & Server Scripting](ex-03-scripting.md)
