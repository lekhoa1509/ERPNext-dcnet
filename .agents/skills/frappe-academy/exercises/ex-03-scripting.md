# Module 3 Exercises: Client & Server Scripting
# Bài tập Module 3: Client Script và Server Script

> **Điều kiện tiên quyết / Prerequisites:** Hoàn thành Module 2 — các DocType Book, Library Member, Library Transaction đã tạo và có dữ liệu mẫu.
>
> **Environment / Môi trường:**
> - Container: `devcontainer-frappe-1`
> - Bench path: `/workspace/development/frappe-bench`
> - Site: `flow.local`
> - Prefix for all commands:
>   ```bash
>   docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && <command>"
>   ```
>
> **Lưu ý quan trọng / Important Notes:**
> - Client Script chạy trên BROWSER (JavaScript) — tương tác với UI
> - Server Script chạy trên SERVER (Python-like) — xử lý dữ liệu
> - Client Script: **KHÔNG dùng** `frappe.db.*` — phải dùng `frappe.call()`
> - Server Script: **KHÔNG dùng** `import` — dùng `frappe.utils.X()` trực tiếp
> - Server Script: **KHÔNG dùng** `self.` — dùng `doc.field`

---

## Exercise 3.1: Client Script — Auto-fill due_date / Tự động điền due_date

### Mục tiêu / Objective
Tạo Client Script tự động tính `due_date` = `transaction_date` + 14 ngày khi chọn `transaction_type` = "Borrow".
Create a Client Script that auto-calculates `due_date` = `transaction_date` + 14 days when `transaction_type` is "Borrow".

### Bước thực hiện / Steps

**Step 1:** Tạo Client Script qua bench console / Create via console

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
# Xóa script cũ nếu có
existing = frappe.db.get_value("Client Script", {"dt": "Library Transaction", "name": ("like", "%Auto Due Date%")}, "name")
if existing:
    frappe.delete_doc("Client Script", existing, force=True)

script = frappe.get_doc({
    "doctype": "Client Script",
    "name": "Library Transaction - Auto Due Date",
    "dt": "Library Transaction",
    "view": "Form",
    "enabled": 1,
    "script": """
frappe.ui.form.on('Library Transaction', {
    transaction_type: function(frm) {
        if (frm.doc.transaction_type === 'Borrow' && frm.doc.transaction_date) {
            let due_date = frappe.datetime.add_days(frm.doc.transaction_date, 14);
            frm.set_value('due_date', due_date);
            frappe.show_alert({
                message: __('Due date set to {0} (14 days from transaction date)', [due_date]),
                indicator: 'blue'
            });
        }
    },
    transaction_date: function(frm) {
        if (frm.doc.transaction_type === 'Borrow' && frm.doc.transaction_date) {
            let due_date = frappe.datetime.add_days(frm.doc.transaction_date, 14);
            frm.set_value('due_date', due_date);
        }
    }
});
"""
})
script.insert()
frappe.db.commit()
print(f"Created Client Script: {script.name}")
EOF
```

**Step 2:** Clear cache để áp dụng / Clear cache to apply
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local clear-cache"
```

**Step 3:** Test trong browser / Test in browser
1. Mở `/app/library-transaction/new-library-transaction-1`
2. Chọn `Transaction Type` = "Borrow"
3. Nhập `Transaction Date` = hôm nay
4. **Kết quả:** `Due Date` tự động được điền = ngày hôm nay + 14

### Kết quả mong đợi / Expected Output
- Khi chọn "Borrow", due_date tự động tính = transaction_date + 14 ngày
- Khi thay đổi transaction_date, due_date tự động cập nhật
- Hiển thị alert "Due date set to..." màu xanh
- Khi chọn "Return", due_date KHÔNG bị thay đổi

### Kiểm tra / Verification
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
cs = frappe.get_all("Client Script", filters={"dt": "Library Transaction"}, fields=["name", "enabled"])
for s in cs:
    print(f"Client Script: {s.name} (enabled={s.enabled})")
EOF
```

<details>
<summary>Gợi ý / Hints</summary>

- `frappe.ui.form.on('DocType', { fieldname: function(frm) {} })` là pattern chính của Client Script
- `frm.set_value(fieldname, value)` — set giá trị và trigger change event
- `frappe.datetime.add_days(date, days)` — utility JS để cộng ngày
- `frappe.show_alert({message, indicator})` — hiển thị toast notification (indicator: blue, green, red, orange)
- Client Script chạy SAU khi user thay đổi field — không chạy khi load form
- Để chạy khi load form, dùng event `refresh` hoặc `onload`
- **DEBUG:** Mở Browser DevTools (F12) → Console tab để xem lỗi JavaScript

</details>

---

## Exercise 3.2: Client Script — Filter Available Books / Lọc sách còn trong kho

### Mục tiêu / Objective
Tạo Client Script lọc danh sách Book chỉ hiển thị sách có status "Available" khi tạo Borrow transaction.
Create a Client Script that filters the Book list to show only "Available" books when creating a Borrow transaction.

### Bước thực hiện / Steps

**Step 1:** Tạo Client Script / Create Client Script

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
existing = frappe.db.get_value("Client Script", {"dt": "Library Transaction", "name": ("like", "%Filter Books%")}, "name")
if existing:
    frappe.delete_doc("Client Script", existing, force=True)

script = frappe.get_doc({
    "doctype": "Client Script",
    "name": "Library Transaction - Filter Books",
    "dt": "Library Transaction",
    "view": "Form",
    "enabled": 1,
    "script": """
frappe.ui.form.on('Library Transaction', {
    refresh: function(frm) {
        // Set filter on Book link field
        frm.set_query('book', function() {
            if (frm.doc.transaction_type === 'Borrow') {
                return {
                    filters: {
                        status: 'Available'
                    }
                };
            }
            // For Return, show only Borrowed books
            if (frm.doc.transaction_type === 'Return') {
                return {
                    filters: {
                        status: 'Borrowed'
                    }
                };
            }
            return {};
        });
    },
    transaction_type: function(frm) {
        // Clear book selection when transaction type changes
        frm.set_value('book', '');
        // Re-trigger refresh to update filters
        frm.trigger('refresh');

        if (frm.doc.transaction_type === 'Borrow') {
            frappe.show_alert({
                message: __('Only available books are shown'),
                indicator: 'blue'
            });
        } else if (frm.doc.transaction_type === 'Return') {
            frappe.show_alert({
                message: __('Only borrowed books are shown'),
                indicator: 'orange'
            });
        }
    }
});
"""
})
script.insert()
frappe.db.commit()
print(f"Created Client Script: {script.name}")
EOF
```

**Step 2:** Clear cache / Clear cache
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local clear-cache"
```

**Step 3:** Test trong browser / Test in browser
1. Mở `/app/library-transaction/new-library-transaction-1`
2. Chọn `Transaction Type` = "Borrow"
3. Click vào field `Book` → chỉ hiển thị sách có status "Available"
4. Đổi `Transaction Type` = "Return"
5. Click vào field `Book` → chỉ hiển thị sách có status "Borrowed"

### Kết quả mong đợi / Expected Output
- Khi transaction_type = "Borrow": Book dropdown chỉ hiện sách "Available"
- Khi transaction_type = "Return": Book dropdown chỉ hiện sách "Borrowed"
- Khi đổi transaction_type, book field được clear
- Alert hiển thị thông báo filter đang áp dụng

### Kiểm tra / Verification
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
# Đếm sách theo trạng thái để xác nhận filter
for status in ["Available", "Borrowed", "Lost"]:
    count = frappe.db.count("Book", {"status": status})
    print(f"Books with status '{status}': {count}")

cs_count = frappe.db.count("Client Script", {"dt": "Library Transaction", "enabled": 1})
print(f"\nActive Client Scripts for Library Transaction: {cs_count}")
EOF
```

<details>
<summary>Gợi ý / Hints</summary>

- `frm.set_query(fieldname, function)` — set dynamic filter cho Link field
- Return object: `{ filters: { field: value } }` — Frappe tự động apply filter khi user mở dropdown
- `frm.set_value('book', '')` — clear field value
- `frm.trigger('refresh')` — manually trigger refresh event
- Filter chỉ áp dụng cho DROPDOWN — user vẫn có thể nhập tên trực tiếp (bypass filter)
- Để ép buộc chỉ chọn từ dropdown, thêm `frm.set_df_property('book', 'only_select', 1)`
- Filter có thể dùng các operator: `['field', '=', 'value']`, `['field', 'in', ['a','b']]`, `['field', '!=', 'value']`

</details>

---

## Exercise 3.3: Client Script — Custom Button "Mark as Returned" / Nút "Đánh dấu đã trả"

### Mục tiêu / Objective
Thêm custom button "Mark as Returned" trên form Library Transaction. Khi click, tự động tạo transaction Return mới.
Add a custom button "Mark as Returned" on the Library Transaction form. When clicked, auto-create a new Return transaction.

### Bước thực hiện / Steps

**Step 1:** Tạo Client Script / Create Client Script

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
existing = frappe.db.get_value("Client Script", {"dt": "Library Transaction", "name": ("like", "%Mark as Returned%")}, "name")
if existing:
    frappe.delete_doc("Client Script", existing, force=True)

script = frappe.get_doc({
    "doctype": "Client Script",
    "name": "Library Transaction - Mark as Returned",
    "dt": "Library Transaction",
    "view": "Form",
    "enabled": 1,
    "script": """
frappe.ui.form.on('Library Transaction', {
    refresh: function(frm) {
        // Chỉ hiện button khi: đã submit (docstatus=1), transaction_type=Borrow
        if (frm.doc.docstatus === 1 && frm.doc.transaction_type === 'Borrow') {
            frm.add_custom_button(__('Mark as Returned'), function() {
                frappe.confirm(
                    __('Create a Return transaction for book {0}?', [frm.doc.book_title || frm.doc.book]),
                    function() {
                        // Tạo Return transaction mới
                        frappe.call({
                            method: 'frappe.client.insert',
                            args: {
                                doc: {
                                    doctype: 'Library Transaction',
                                    book: frm.doc.book,
                                    member: frm.doc.member,
                                    transaction_type: 'Return',
                                    transaction_date: frappe.datetime.get_today(),
                                    return_date: frappe.datetime.get_today(),
                                    notes: 'Return for ' + frm.doc.name
                                }
                            },
                            callback: function(r) {
                                if (r.message) {
                                    frappe.show_alert({
                                        message: __('Return transaction {0} created', [r.message.name]),
                                        indicator: 'green'
                                    });
                                    frappe.set_route('Form', 'Library Transaction', r.message.name);
                                }
                            }
                        });
                    }
                );
            }, __('Actions'));
        }
    }
});
"""
})
script.insert()
frappe.db.commit()
print(f"Created Client Script: {script.name}")
EOF
```

**Step 2:** Clear cache / Clear cache
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local clear-cache"
```

**Step 3:** Test trong browser / Test in browser
1. Mở một Library Transaction đã submit với type "Borrow"
2. Tìm dropdown button "Actions" ở góc trên phải
3. Click "Mark as Returned"
4. Confirm dialog hiển thị → click "Yes"
5. **Kết quả:** Chuyển sang form Return transaction mới

### Kết quả mong đợi / Expected Output
- Button "Mark as Returned" chỉ hiện trên submitted Borrow transactions
- Click button → hiện confirm dialog
- Confirm → tạo Return transaction mới với cùng book và member
- Redirect sang form của Return transaction mới
- Alert xanh: "Return transaction TXN-XXXX created"

### Kiểm tra / Verification
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
# Kiểm tra có Return transactions không
returns = frappe.get_all("Library Transaction",
    filters={"transaction_type": "Return"},
    fields=["name", "book", "member", "notes"]
)
print(f"Return transactions: {len(returns)}")
for r in returns:
    print(f"  {r.name}: book={r.book}, notes={r.notes}")
EOF
```

<details>
<summary>Gợi ý / Hints</summary>

- `frm.add_custom_button(label, callback, group)` — thêm button vào form
  - `group` (optional): gom nhiều buttons vào dropdown (VD: "Actions", "Tools")
  - Không có group: button hiện trực tiếp trên toolbar
- `frappe.confirm(message, yes_callback, no_callback)` — dialog xác nhận
- `frappe.call({method, args, callback})` — gọi server từ client
  - `frappe.client.insert` là built-in whitelist method để tạo document
  - `frappe.client.get_list`, `frappe.client.get_count` — các method khác
- `frappe.set_route('Form', 'DocType', 'name')` — chuyển trang
- `frm.doc.docstatus`: 0=Draft, 1=Submitted, 2=Cancelled
- Button chỉ hiện khi `refresh` event chạy — doc phải loaded xong
- **KHÔNG BAO GIỜ** dùng `frappe.db.sql` hay `frappe.db.get_value` trong Client Script!

</details>

---

## Exercise 3.4: Server Script — Validate ISBN Format / Kiểm tra định dạng ISBN

### Mục tiêu / Objective
Tạo Server Script kiểm tra ISBN phải đúng 13 ký tự số khi lưu Book. Hiểu cách Server Script chạy trước khi lưu dữ liệu.
Create a Server Script that validates ISBN must be exactly 13 digits when saving a Book. Understand how Server Scripts run before data is saved.

### Bước thực hiện / Steps

**Step 1:** Tạo Server Script / Create Server Script

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
existing = frappe.db.get_value("Server Script", {"name": ("like", "%Validate Book ISBN%")}, "name")
if existing:
    frappe.delete_doc("Server Script", existing, force=True)

script = frappe.get_doc({
    "doctype": "Server Script",
    "name": "Validate Book ISBN",
    "script_type": "DocType Event",
    "reference_doctype": "Book",
    "doctype_event": "Before Save",
    "disabled": 0,
    "script": """
# Server Script: Validate ISBN format on Book
# Lưu ý: KHÔNG dùng import, KHÔNG dùng self

if doc.isbn:
    # Xóa khoảng trắng và dấu gạch ngang
    clean_isbn = doc.isbn.replace('-', '').replace(' ', '').strip()

    # Kiểm tra chỉ chứa số
    if not clean_isbn.isdigit():
        frappe.throw(
            'ISBN chỉ được chứa ký tự số (ISBN must contain only digits). '
            'Current value: ' + doc.isbn,
            title='Invalid ISBN'
        )

    # Kiểm tra độ dài = 10 hoặc 13
    if len(clean_isbn) not in (10, 13):
        frappe.throw(
            'ISBN phải có 10 hoặc 13 ký tự số (ISBN must be 10 or 13 digits). '
            'Current length: ' + str(len(clean_isbn)),
            title='Invalid ISBN Length'
        )

    # Tự động lưu dạng sạch (không dấu gạch ngang)
    doc.isbn = clean_isbn

    frappe.msgprint(
        'ISBN validated: ' + doc.isbn + ' (' + str(len(doc.isbn)) + ' digits)',
        alert=True,
        indicator='green'
    )
"""
})
script.insert()
frappe.db.commit()
print(f"Created Server Script: {script.name}")
EOF
```

**Step 2:** Test với dữ liệu hợp lệ / Test with valid data

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
# Test 1: ISBN hợp lệ (13 digits)
try:
    book = frappe.get_doc({
        "doctype": "Book",
        "title": "The Pragmatic Programmer",
        "author": "David Thomas",
        "isbn": "978-0-13-595705-9",
        "status": "Available"
    })
    book.insert()
    frappe.db.commit()
    print(f"TEST 1 PASSED: Created {book.name}, ISBN cleaned to: {book.isbn}")
except Exception as e:
    print(f"TEST 1 FAILED: {e}")

# Test 2: ISBN không hợp lệ (quá ngắn)
try:
    book2 = frappe.get_doc({
        "doctype": "Book",
        "title": "Bad ISBN Book",
        "author": "Test",
        "isbn": "12345",
        "status": "Available"
    })
    book2.insert()
    frappe.db.commit()
    print(f"TEST 2 FAILED: Should have thrown error but created {book2.name}")
except Exception as e:
    print(f"TEST 2 PASSED: Correctly rejected invalid ISBN - {e}")

# Test 3: ISBN có chữ cái
try:
    book3 = frappe.get_doc({
        "doctype": "Book",
        "title": "Letters in ISBN",
        "author": "Test",
        "isbn": "978ABC1234567",
        "status": "Available"
    })
    book3.insert()
    frappe.db.commit()
    print(f"TEST 3 FAILED: Should have thrown error but created {book3.name}")
except Exception as e:
    print(f"TEST 3 PASSED: Correctly rejected non-digit ISBN - {e}")
EOF
```

### Kết quả mong đợi / Expected Output
- TEST 1: PASSED — ISBN "978-0-13-595705-9" được clean thành "9780135957059" (13 digits)
- TEST 2: PASSED — ISBN "12345" bị reject vì chỉ có 5 ký tự
- TEST 3: PASSED — ISBN "978ABC1234567" bị reject vì chứa chữ cái
- Book không ISBN (để trống) vẫn save được (ISBN không bắt buộc)

### Kiểm tra / Verification
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
scripts = frappe.get_all("Server Script",
    filters={"reference_doctype": "Book"},
    fields=["name", "script_type", "doctype_event", "disabled"]
)
for s in scripts:
    print(f"Server Script: {s.name}")
    print(f"  Type: {s.script_type}, Event: {s.doctype_event}, Disabled: {s.disabled}")
EOF
```

<details>
<summary>Gợi ý / Hints</summary>

- Server Script có 4 loại script_type:
  - `DocType Event` — chạy khi DocType event (Before Save, After Save, Before Submit...)
  - `API` — tạo REST API endpoint
  - `Permission Query` — custom permission filter
  - `Scheduled` — chạy theo lịch (cron)
- **KHÔNG import module** trong Server Script — dùng `frappe.utils.X()` trực tiếp
- **KHÔNG dùng `self`** — dùng `doc` (biến global trong Server Script)
- `frappe.throw(message)` — raise ValidationError và hiển thị lỗi cho user
- `frappe.msgprint(message, alert=True)` — hiển thị thông báo (không block)
- `doc` trong Server Script là document đang được save — thay đổi `doc.field` sẽ lưu vào DB
- Server Script chạy trong **sandbox** — một số Python features bị hạn chế
- Để debug Server Script: xem `bench --site flow.local show-pending-events` hoặc check Error Log

</details>

---

## Exercise 3.5: Server Script — Auto-update Book Status / Tự động cập nhật trạng thái sách

### Mục tiêu / Objective
Tạo Server Script tự động cập nhật Book.status khi Library Transaction được lưu: Borrow → "Borrowed", Return → "Available".
Create a Server Script that auto-updates Book.status when a Library Transaction is saved: Borrow → "Borrowed", Return → "Available".

### Bước thực hiện / Steps

**Step 1:** Tạo Server Script / Create Server Script

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
existing = frappe.db.get_value("Server Script", {"name": ("like", "%Update Book Status%")}, "name")
if existing:
    frappe.delete_doc("Server Script", existing, force=True)

script = frappe.get_doc({
    "doctype": "Server Script",
    "name": "Update Book Status on Transaction",
    "script_type": "DocType Event",
    "reference_doctype": "Library Transaction",
    "doctype_event": "After Save",
    "disabled": 0,
    "script": """
# Server Script: Auto-update Book status based on transaction type
# Chạy sau khi Library Transaction được save

if doc.docstatus == 1:
    # Chỉ cập nhật khi transaction đã submit (docstatus=1)

    if doc.transaction_type == 'Borrow':
        new_status = 'Borrowed'
    elif doc.transaction_type == 'Return':
        new_status = 'Available'
    else:
        new_status = None

    if new_status:
        # Dùng frappe.db.set_value để cập nhật trực tiếp (không trigger hooks)
        frappe.db.set_value('Book', doc.book, 'status', new_status)

        frappe.msgprint(
            'Book <b>' + (doc.book_title or doc.book) + '</b> status updated to <b>' + new_status + '</b>',
            alert=True,
            indicator='green'
        )
"""
})
script.insert()
frappe.db.commit()
print(f"Created Server Script: {script.name}")
EOF
```

**Step 2:** Tắt Workflow tạm thời để test / Disable Workflow temporarily for testing

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
# Tắt workflow để test trực tiếp submit
wf = frappe.db.get_value("Workflow", {"document_type": "Library Transaction", "is_active": 1}, "name")
if wf:
    frappe.db.set_value("Workflow", wf, "is_active", 0)
    print(f"Disabled workflow: {wf}")
else:
    print("No active workflow found")
frappe.db.commit()
EOF
```

**Step 3:** Test với dữ liệu / Test with data

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
# Đảm bảo có sách Available
book = frappe.db.get_value("Book", {"status": "Available"}, "name")
if not book:
    # Tạo sách mới
    b = frappe.get_doc({
        "doctype": "Book",
        "title": "Design Patterns",
        "author": "Gang of Four",
        "isbn": "9780201633610",
        "status": "Available"
    })
    b.insert()
    frappe.db.commit()
    book = b.name
    print(f"Created book: {b.name}")

member = frappe.get_last_doc("Library Member").name

# Test 1: Borrow → Book status should become "Borrowed"
print(f"\n--- Test 1: Borrow ---")
print(f"Book status BEFORE: {frappe.db.get_value('Book', book, 'status')}")

txn = frappe.get_doc({
    "doctype": "Library Transaction",
    "book": book,
    "member": member,
    "transaction_type": "Borrow",
    "transaction_date": frappe.utils.today(),
    "due_date": frappe.utils.add_days(frappe.utils.today(), 14)
})
txn.insert()
txn.submit()
frappe.db.commit()

book_status = frappe.db.get_value("Book", book, "status")
print(f"Book status AFTER borrow: {book_status}")
print(f"TEST 1: {'PASSED' if book_status == 'Borrowed' else 'FAILED'}")

# Test 2: Return → Book status should become "Available"
print(f"\n--- Test 2: Return ---")
txn2 = frappe.get_doc({
    "doctype": "Library Transaction",
    "book": book,
    "member": member,
    "transaction_type": "Return",
    "transaction_date": frappe.utils.today(),
    "return_date": frappe.utils.today()
})
txn2.insert()
txn2.submit()
frappe.db.commit()

book_status = frappe.db.get_value("Book", book, "status")
print(f"Book status AFTER return: {book_status}")
print(f"TEST 2: {'PASSED' if book_status == 'Available' else 'FAILED'}")
EOF
```

**Step 4:** Bật lại Workflow / Re-enable Workflow

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
wf = frappe.db.get_value("Workflow", {"document_type": "Library Transaction"}, "name")
if wf:
    frappe.db.set_value("Workflow", wf, "is_active", 1)
    print(f"Re-enabled workflow: {wf}")
frappe.db.commit()
EOF
```

### Kết quả mong đợi / Expected Output
- TEST 1 PASSED: Sau khi submit Borrow transaction, Book.status = "Borrowed"
- TEST 2 PASSED: Sau khi submit Return transaction, Book.status = "Available"
- Server Script chỉ chạy khi `docstatus == 1` (submitted) — draft save không ảnh hưởng Book status

### Kiểm tra / Verification
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
# Kiểm tra toàn bộ
scripts = frappe.get_all("Server Script",
    filters={"reference_doctype": ["in", ["Book", "Library Transaction"]]},
    fields=["name", "reference_doctype", "doctype_event", "disabled"]
)
print("Server Scripts:")
for s in scripts:
    print(f"  {s.name} | {s.reference_doctype} | {s.doctype_event} | disabled={s.disabled}")

client_scripts = frappe.get_all("Client Script",
    filters={"dt": "Library Transaction"},
    fields=["name", "enabled"]
)
print(f"\nClient Scripts for Library Transaction:")
for s in client_scripts:
    print(f"  {s.name} | enabled={s.enabled}")
EOF
```

<details>
<summary>Gợi ý / Hints</summary>

- **`After Save`** chạy SAU khi document lưu vào DB — an toàn để cập nhật document khác
- **`Before Save`** chạy TRƯỚC khi lưu — dùng để validate và modify document hiện tại
- `frappe.db.set_value('DocType', name, field, value)` — cập nhật trực tiếp, KHÔNG trigger hooks của doc khác
  - Dùng khi: cập nhật 1-2 fields đơn giản
  - KHÔNG dùng khi: cần trigger validate/hooks của doc được cập nhật
- Để trigger hooks: dùng `frappe.get_doc().save()` thay vì `frappe.db.set_value()`
- `doc.docstatus` trong Server Script:
  - `0` = Draft (save)
  - `1` = Submitted (submit)
  - `2` = Cancelled (cancel)
- **QUAN TRỌNG:** After Save chạy cho CẢ save và submit — check `doc.docstatus` để phân biệt
- Server Script `After Save` KHÔNG nên `frappe.throw()` — doc đã lưu rồi, throw sẽ confuse user

</details>

---

## Tổng kết Module 3 / Module 3 Summary

| # | Script | Loại / Type | Event | Chức năng / Function |
|---|--------|-------------|-------|----------------------|
| 3.1 | Auto Due Date | Client Script | transaction_type change | Auto-fill due_date = transaction_date + 14 days |
| 3.2 | Filter Books | Client Script | refresh, transaction_type change | Filter Book dropdown by status |
| 3.3 | Mark as Returned | Client Script | refresh | Custom button to create Return transaction |
| 3.4 | Validate ISBN | Server Script | Before Save (Book) | Validate ISBN format (10 or 13 digits) |
| 3.5 | Update Book Status | Server Script | After Save (Library Transaction) | Auto-update Book status on submit |

| # | Kỹ năng / Skill | Trạng thái / Status |
|---|-----------------|---------------------|
| 3.1 | Client Script — field change handler, auto-calculate | [ ] |
| 3.2 | Client Script — set_query, dynamic Link field filter | [ ] |
| 3.3 | Client Script — add_custom_button, frappe.call, frappe.confirm | [ ] |
| 3.4 | Server Script — Before Save validation, frappe.throw | [ ] |
| 3.5 | Server Script — After Save, cross-document update | [ ] |

### Verification toàn bộ / Full Module Verification
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
print("=== Client Scripts ===")
for s in frappe.get_all("Client Script", filters={"dt": "Library Transaction"}, fields=["name", "enabled"]):
    print(f"  {'ON' if s.enabled else 'OFF'}: {s.name}")

print("\n=== Server Scripts ===")
for s in frappe.get_all("Server Script", filters={"reference_doctype": ["in", ["Book", "Library Transaction"]]}, fields=["name", "disabled", "doctype_event"]):
    print(f"  {'ON' if not s.disabled else 'OFF'}: {s.name} ({s.doctype_event})")
EOF
```

> **Tiếp theo / Next:** [Exercise 04 - Controllers & Hooks](ex-04-controller.md)
