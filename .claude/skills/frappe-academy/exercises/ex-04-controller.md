# Module 4 Exercises: Controllers & Hooks
# Bài tập Module 4: Controllers và Hooks

> **Điều kiện tiên quyết / Prerequisites:** Hoàn thành Module 2 và 3 — các DocType đã tạo, Client/Server Scripts đã test.
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
>
> **Controller vs Script:**
> | | Controller (Python file) | Server Script (DB record) |
> |---|---|---|
> | **Vị trí** | `doctype/xxx/xxx.py` | Lưu trong database |
> | **Import** | Có thể import bất kỳ module nào | KHÔNG import |
> | **Self** | Dùng `self.field` | Dùng `doc.field` |
> | **Deploy** | Cần restart bench | Áp dụng ngay |
> | **Dùng khi** | Logic phức tạp, production code | Prototype nhanh, config |

---

## Exercise 4.1: Controller validate() — Kiểm tra dữ liệu / Data Validation

### Mục tiêu / Objective
Viết controller `validate()` cho Library Transaction kiểm tra: book tồn tại, member tồn tại, sách còn "Available" (cho Borrow).
Write a controller `validate()` for Library Transaction that checks: book exists, member exists, book is "Available" (for Borrow).

### Bước thực hiện / Steps

**Step 1:** Tắt Server Script "Update Book Status" để tránh conflict / Disable overlapping Server Script

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
ss = frappe.db.get_value("Server Script", {"name": "Update Book Status on Transaction"}, "name")
if ss:
    frappe.db.set_value("Server Script", ss, "disabled", 1)
    print(f"Disabled Server Script: {ss}")
    print("(Logic sẽ được chuyển vào controller)")
frappe.db.commit()
EOF
```

**Step 2:** Cập nhật file `library_transaction.py` / Update controller file

Sửa file `apps/frappe_learn/frappe_learn/library/doctype/library_transaction/library_transaction.py`:

```python
# Copyright (c) 2026, DCNET and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, today, add_days


class LibraryTransaction(Document):
    def validate(self):
        """Validate before save — runs on both save and submit."""
        self.validate_book()
        self.validate_member()
        self.validate_dates()
        if self.transaction_type == "Borrow":
            self.validate_book_available()
            self.set_due_date_if_empty()

    def validate_book(self):
        """Check that the linked Book exists."""
        if not self.book:
            frappe.throw(_("Book is required"), title=_("Missing Book"))

        if not frappe.db.exists("Book", self.book):
            frappe.throw(
                _("Book {0} does not exist").format(self.book),
                title=_("Invalid Book")
            )

    def validate_member(self):
        """Check that the linked Library Member exists and is active."""
        if not self.member:
            frappe.throw(_("Member is required"), title=_("Missing Member"))

        if not frappe.db.exists("Library Member", self.member):
            frappe.throw(
                _("Library Member {0} does not exist").format(self.member),
                title=_("Invalid Member")
            )

        # Check member is active
        is_active = frappe.db.get_value("Library Member", self.member, "active")
        if not is_active:
            frappe.throw(
                _("Library Member {0} is not active").format(self.member),
                title=_("Inactive Member")
            )

    def validate_dates(self):
        """Validate transaction dates are logical."""
        if self.transaction_date and self.due_date:
            if getdate(self.due_date) < getdate(self.transaction_date):
                frappe.throw(
                    _("Due Date cannot be before Transaction Date"),
                    title=_("Invalid Date")
                )

        if self.transaction_type == "Return" and self.return_date:
            if getdate(self.return_date) < getdate(self.transaction_date):
                frappe.throw(
                    _("Return Date cannot be before Transaction Date"),
                    title=_("Invalid Date")
                )

    def validate_book_available(self):
        """For Borrow transactions, check that the book is Available."""
        book_status = frappe.db.get_value("Book", self.book, "status")
        if book_status != "Available":
            book_title = frappe.db.get_value("Book", self.book, "title")
            frappe.throw(
                _("Book '{0}' is currently {1}. Only Available books can be borrowed.").format(
                    book_title, book_status
                ),
                title=_("Book Not Available")
            )

    def set_due_date_if_empty(self):
        """Auto-set due_date to 14 days from transaction_date if not provided."""
        if not self.due_date and self.transaction_date:
            self.due_date = add_days(self.transaction_date, 14)
            frappe.msgprint(
                _("Due date auto-set to {0} (14 days from transaction date)").format(self.due_date),
                alert=True
            )
```

**Step 3:** Restart bench để áp dụng thay đổi controller / Restart to apply

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local clear-cache"
```

> **Lưu ý:** Trong development mode, Frappe tự động reload Python files. Trong production, cần `bench restart`.

**Step 4:** Test validate / Test validation

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
import frappe
from frappe.utils import today, add_days

# --- Test 1: Borrow sách Available → OK ---
print("=== Test 1: Valid Borrow ===")
book = frappe.db.get_value("Book", {"status": "Available"}, "name")
member = frappe.db.get_value("Library Member", {"active": 1}, "name")
if book and member:
    try:
        txn = frappe.get_doc({
            "doctype": "Library Transaction",
            "book": book,
            "member": member,
            "transaction_type": "Borrow",
            "transaction_date": today()
        })
        txn.insert()
        frappe.db.commit()
        print(f"PASSED: Created {txn.name}, due_date auto-set: {txn.due_date}")
    except Exception as e:
        print(f"FAILED: {e}")
else:
    print("SKIPPED: No available book or active member")

# --- Test 2: Borrow sách đã Borrowed → FAIL ---
print("\n=== Test 2: Borrow unavailable book ===")
borrowed_book = frappe.db.get_value("Book", {"status": "Borrowed"}, "name")
if borrowed_book and member:
    try:
        txn2 = frappe.get_doc({
            "doctype": "Library Transaction",
            "book": borrowed_book,
            "member": member,
            "transaction_type": "Borrow",
            "transaction_date": today()
        })
        txn2.insert()
        print(f"FAILED: Should have thrown error, created {txn2.name}")
    except frappe.ValidationError as e:
        print(f"PASSED: Correctly rejected - {e}")
    except Exception as e:
        print(f"PASSED (other error): {e}")
else:
    print("SKIPPED: No borrowed book found")

# --- Test 3: Due date trước transaction date → FAIL ---
print("\n=== Test 3: Invalid dates ===")
book3 = frappe.db.get_value("Book", {"status": "Available"}, "name")
if book3 and member:
    try:
        txn3 = frappe.get_doc({
            "doctype": "Library Transaction",
            "book": book3,
            "member": member,
            "transaction_type": "Borrow",
            "transaction_date": today(),
            "due_date": add_days(today(), -7)  # 7 days in the past
        })
        txn3.insert()
        print(f"FAILED: Should have thrown error")
    except frappe.ValidationError as e:
        print(f"PASSED: Correctly rejected - {e}")
    except Exception as e:
        print(f"PASSED (other error): {e}")
else:
    print("SKIPPED: No available book")

frappe.db.rollback()
EOF
```

### Kết quả mong đợi / Expected Output
- Test 1 PASSED: Borrow sách Available thành công, due_date tự động set
- Test 2 PASSED: Borrow sách đã Borrowed bị reject với thông báo "Book Not Available"
- Test 3 PASSED: Due date trước transaction date bị reject

### Kiểm tra / Verification
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
# Kiểm tra controller class có đúng methods không
from frappe_learn.library.doctype.library_transaction.library_transaction import LibraryTransaction
methods = [m for m in dir(LibraryTransaction) if not m.startswith('_')]
required = ['validate', 'validate_book', 'validate_member', 'validate_dates', 'validate_book_available']
for r in required:
    print(f"  {'OK' if r in methods else 'MISSING'}: {r}")
EOF
```

<details>
<summary>Gợi ý / Hints</summary>

- `validate()` chạy TRƯỚC khi save vào DB — là nơi tốt nhất để kiểm tra dữ liệu
- `validate()` chạy cho CẢ save (Draft) và submit — dùng `self.docstatus` để phân biệt nếu cần
- `frappe.throw(message, title)` — raise `frappe.ValidationError` và hiển thị lỗi trên UI
- `_("text")` — translation function, giúp message hỗ trợ đa ngôn ngữ
- `frappe.db.get_value("DocType", name, "field")` — lấy 1 field nhanh (1 SQL query)
- `frappe.db.exists("DocType", name)` — kiểm tra record tồn tại (return name hoặc None)
- **Best practice:** Tách validate thành nhiều method nhỏ (validate_X, validate_Y) để dễ đọc và test
- Controller method có thể modify `self.field` — thay đổi sẽ tự động lưu vào DB
- KHÔNG nên `frappe.db.set_value()` trong `validate()` — thay đổi doc hiện tại dùng `self.field = value`

</details>

---

## Exercise 4.2: Controller on_submit() — Auto-update Book Status / Tự động cập nhật khi submit

### Mục tiêu / Objective
Viết `on_submit()` tự động cập nhật Book.status khi transaction được submit, và ghi log.
Write `on_submit()` to auto-update Book.status when transaction is submitted, and log the action.

### Bước thực hiện / Steps

**Step 1:** Thêm `on_submit()` vào controller / Add on_submit() to controller

Thêm vào cuối class `LibraryTransaction` trong file `library_transaction.py`:

```python
    def on_submit(self):
        """After submit — update book status and log transaction."""
        self.update_book_status()
        self.log_transaction()

    def update_book_status(self):
        """Update the Book status based on transaction type."""
        if self.transaction_type == "Borrow":
            new_status = "Borrowed"
        elif self.transaction_type == "Return":
            new_status = "Available"
        else:
            return

        book = frappe.get_doc("Book", self.book)
        old_status = book.status
        book.status = new_status
        book.save(ignore_permissions=True)

        frappe.msgprint(
            _("Book '{0}' status changed: {1} → {2}").format(
                book.title, old_status, new_status
            ),
            alert=True,
            indicator="green"
        )

    def log_transaction(self):
        """Add a comment to the Book document for audit trail."""
        comment_text = _("{0} by {1} on {2}").format(
            self.transaction_type,
            self.member_name or self.member,
            self.transaction_date
        )

        frappe.get_doc("Book", self.book).add_comment(
            "Info",
            comment_text
        )

        # Also add to Error Log for debugging (remove in production)
        frappe.log_error(
            title=f"Library Transaction: {self.name}",
            message=f"Type: {self.transaction_type}, Book: {self.book}, Member: {self.member}"
        )
```

**Step 2:** Clear cache / Clear cache
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local clear-cache"
```

**Step 3:** Test on_submit / Test submission

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
import frappe
from frappe.utils import today, add_days

# Tắt workflow để test trực tiếp
wf = frappe.db.get_value("Workflow", {"document_type": "Library Transaction", "is_active": 1}, "name")
if wf:
    frappe.db.set_value("Workflow", wf, "is_active", 0)
    frappe.db.commit()

# Đảm bảo có sách Available
book = frappe.db.get_value("Book", {"status": "Available"}, "name")
if not book:
    b = frappe.get_doc({
        "doctype": "Book",
        "title": "Refactoring",
        "author": "Martin Fowler",
        "isbn": "9780134757599",
        "status": "Available"
    })
    b.insert()
    frappe.db.commit()
    book = b.name

member = frappe.db.get_value("Library Member", {"active": 1}, "name")

print(f"Book: {book}, status BEFORE: {frappe.db.get_value('Book', book, 'status')}")

# Tạo và submit Borrow transaction
txn = frappe.get_doc({
    "doctype": "Library Transaction",
    "book": book,
    "member": member,
    "transaction_type": "Borrow",
    "transaction_date": today(),
    "due_date": add_days(today(), 14)
})
txn.insert()
txn.submit()
frappe.db.commit()

print(f"Transaction: {txn.name}, docstatus: {txn.docstatus}")
print(f"Book status AFTER submit: {frappe.db.get_value('Book', book, 'status')}")

# Kiểm tra comment trên Book
comments = frappe.get_all("Comment",
    filters={"reference_doctype": "Book", "reference_name": book, "comment_type": "Info"},
    fields=["content"],
    order_by="creation desc",
    limit=1
)
if comments:
    print(f"Book comment: {comments[0].content}")

# Bật lại workflow
if wf:
    frappe.db.set_value("Workflow", wf, "is_active", 1)
    frappe.db.commit()
EOF
```

### Kết quả mong đợi / Expected Output
- Sau submit Borrow: Book.status = "Borrowed"
- Comment "Borrow by [member] on [date]" xuất hiện trên Book timeline
- Error Log ghi nhận transaction (cho audit)

### Kiểm tra / Verification
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
# Kiểm tra controller có on_submit
from frappe_learn.library.doctype.library_transaction.library_transaction import LibraryTransaction
has_on_submit = hasattr(LibraryTransaction, 'on_submit')
has_update_book = hasattr(LibraryTransaction, 'update_book_status')
has_log = hasattr(LibraryTransaction, 'log_transaction')
print(f"on_submit: {'OK' if has_on_submit else 'MISSING'}")
print(f"update_book_status: {'OK' if has_update_book else 'MISSING'}")
print(f"log_transaction: {'OK' if has_log else 'MISSING'}")
EOF
```

<details>
<summary>Gợi ý / Hints</summary>

- `on_submit()` chạy SAU khi docstatus chuyển từ 0 → 1
- Thứ tự hooks khi submit: `validate()` → `before_submit()` → `on_submit()`
- Trong `on_submit()`, `self.docstatus` đã = 1
- `book.save(ignore_permissions=True)` — cho phép save không kiểm tra permission (vì system action)
- `doc.add_comment("Info", text)` — thêm comment vào timeline của document
- `frappe.log_error(title, message)` — ghi vào Error Log (dùng cho debug, xóa trong production)
- **KHÔNG** modify `self.field` trong `on_submit()` — doc đã saved, dùng `frappe.db.set_value()` nếu cần
- Nếu cần modify current doc trong on_submit: dùng `frappe.db.set_value(self.doctype, self.name, field, value)`

</details>

---

## Exercise 4.3: Controller on_cancel() — Reverse Book Status / Hoàn tác trạng thái sách

### Mục tiêu / Objective
Viết `on_cancel()` để hoàn tác: khi cancel Borrow → Book về "Available", khi cancel Return → Book về "Borrowed".
Write `on_cancel()` to reverse: when cancelling Borrow → Book back to "Available", when cancelling Return → Book back to "Borrowed".

### Bước thực hiện / Steps

**Step 1:** Thêm `on_cancel()` vào controller / Add on_cancel() to controller

Thêm vào cuối class `LibraryTransaction` trong file `library_transaction.py`:

```python
    def on_cancel(self):
        """After cancel — reverse book status."""
        self.reverse_book_status()

    def reverse_book_status(self):
        """Reverse the Book status when transaction is cancelled."""
        if self.transaction_type == "Borrow":
            # Cancel borrow → book goes back to Available
            new_status = "Available"
        elif self.transaction_type == "Return":
            # Cancel return → book goes back to Borrowed
            new_status = "Borrowed"
        else:
            return

        book = frappe.get_doc("Book", self.book)
        old_status = book.status
        book.status = new_status
        book.save(ignore_permissions=True)

        frappe.msgprint(
            _("Book '{0}' status reverted: {1} → {2} (transaction cancelled)").format(
                book.title, old_status, new_status
            ),
            alert=True,
            indicator="orange"
        )

        # Log cancellation
        frappe.get_doc("Book", self.book).add_comment(
            "Info",
            _("Transaction {0} cancelled — {1} reversed").format(
                self.name, self.transaction_type
            )
        )
```

**Step 2:** Clear cache / Clear cache
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local clear-cache"
```

**Step 3:** Test on_cancel / Test cancellation

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
import frappe
from frappe.utils import today, add_days

# Tắt workflow
wf = frappe.db.get_value("Workflow", {"document_type": "Library Transaction", "is_active": 1}, "name")
if wf:
    frappe.db.set_value("Workflow", wf, "is_active", 0)
    frappe.db.commit()

# Tạo sách mới để test
book = frappe.get_doc({
    "doctype": "Book",
    "title": "Test Cancel Book",
    "author": "Test Author",
    "isbn": "9781234567890",
    "status": "Available"
})
book.insert()
frappe.db.commit()
print(f"1. Book created: {book.name}, status: {book.status}")

member = frappe.db.get_value("Library Member", {"active": 1}, "name")

# Borrow → status becomes Borrowed
txn = frappe.get_doc({
    "doctype": "Library Transaction",
    "book": book.name,
    "member": member,
    "transaction_type": "Borrow",
    "transaction_date": today(),
    "due_date": add_days(today(), 14)
})
txn.insert()
txn.submit()
frappe.db.commit()
print(f"2. After Borrow submit: Book status = {frappe.db.get_value('Book', book.name, 'status')}")

# Cancel Borrow → status should revert to Available
txn.reload()
txn.cancel()
frappe.db.commit()
print(f"3. After Borrow cancel: Book status = {frappe.db.get_value('Book', book.name, 'status')}")
print(f"   Transaction docstatus: {txn.docstatus} (2=Cancelled)")

status = frappe.db.get_value("Book", book.name, "status")
print(f"\nFINAL TEST: {'PASSED' if status == 'Available' else 'FAILED'} — Book status is '{status}'")

# Bật lại workflow
if wf:
    frappe.db.set_value("Workflow", wf, "is_active", 1)
    frappe.db.commit()
EOF
```

### Kết quả mong đợi / Expected Output
- Step 1: Book status = "Available"
- Step 2: After Borrow submit → status = "Borrowed"
- Step 3: After cancel → status = "Available" (reverted)
- Comment "Transaction cancelled" xuất hiện trên Book timeline
- Transaction docstatus = 2 (Cancelled)

### Kiểm tra / Verification
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
from frappe_learn.library.doctype.library_transaction.library_transaction import LibraryTransaction
required = ['validate', 'on_submit', 'on_cancel', 'update_book_status', 'reverse_book_status']
for m in required:
    print(f"  {'OK' if hasattr(LibraryTransaction, m) else 'MISSING'}: {m}")
EOF
```

<details>
<summary>Gợi ý / Hints</summary>

- `on_cancel()` chạy SAU khi docstatus chuyển từ 1 → 2
- Thứ tự hooks khi cancel: `before_cancel()` → `on_cancel()`
- **QUAN TRỌNG:** `on_cancel()` phải hoàn tác CHÍNH XÁC những gì `on_submit()` đã làm
- Nếu không hoàn tác, data sẽ không nhất quán (VD: sách vẫn "Borrowed" dù transaction đã cancel)
- Document đã cancel KHÔNG thể edit hay submit lại — phải tạo mới (Amend)
- `self.docstatus` trong `on_cancel()` đã = 2
- Frappe tự động thêm "Cancelled" label trên cancelled documents
- **Pattern chuẩn:** `on_submit` ↔ `on_cancel` luôn đi đôi — làm gì khi submit thì undo khi cancel

</details>

---

## Exercise 4.4: hooks.py — doc_events Notification / Thông báo qua hooks

### Mục tiêu / Objective
Thêm `doc_events` trong hooks.py để gửi notification khi Library Transaction được tạo. Hiểu cách hooks.py dùng cho cross-app integration.
Add `doc_events` in hooks.py to send a notification when a Library Transaction is created. Understand hooks.py for cross-app integration.

### Bước thực hiện / Steps

**Step 1:** Tạo file notification utility / Create notification utility

Tạo file `apps/frappe_learn/frappe_learn/library/notifications.py`:

```python
# Copyright (c) 2026, DCNET and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def send_borrow_notification(doc, method):
    """
    Send notification when a Library Transaction is created.

    This function is called via hooks.py doc_events.
    Parameters:
        doc: the Library Transaction document
        method: the event name (e.g., "after_insert")
    """
    if doc.transaction_type != "Borrow":
        return

    # Get member email
    member_email = frappe.db.get_value("Library Member", doc.member, "email")
    book_title = doc.book_title or frappe.db.get_value("Book", doc.book, "title")

    # Log the notification (in production, use frappe.sendmail)
    frappe.log_error(
        title=f"Library Notification: {doc.name}",
        message=(
            f"Transaction: {doc.name}\n"
            f"Type: {doc.transaction_type}\n"
            f"Book: {book_title}\n"
            f"Member: {doc.member_name or doc.member}\n"
            f"Email: {member_email}\n"
            f"Due Date: {doc.due_date}\n"
            f"\nIn production, an email would be sent to: {member_email}"
        )
    )

    frappe.msgprint(
        _("Notification logged for {0} — Book: {1}, Due: {2}").format(
            doc.member_name or doc.member,
            book_title,
            doc.due_date
        ),
        alert=True,
        indicator="blue"
    )


def on_transaction_update(doc, method):
    """
    Called when a Library Transaction is updated.
    Can be used for audit trail or sync.
    """
    frappe.logger("library").info(
        f"Library Transaction {doc.name} updated: "
        f"type={doc.transaction_type}, status={doc.docstatus}"
    )
```

**Step 2:** Cập nhật hooks.py / Update hooks.py

Sửa file `apps/frappe_learn/frappe_learn/hooks.py`, thêm (hoặc bỏ comment) section `doc_events`:

```python
# Document Events
# ---------------
doc_events = {
    "Library Transaction": {
        "after_insert": "frappe_learn.library.notifications.send_borrow_notification",
        "on_update": "frappe_learn.library.notifications.on_transaction_update",
    }
}
```

**Step 3:** Clear cache để áp dụng hooks mới / Clear cache

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local clear-cache"
```

**Step 4:** Test notification / Test

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
import frappe
from frappe.utils import today, add_days

# Tắt workflow
wf = frappe.db.get_value("Workflow", {"document_type": "Library Transaction", "is_active": 1}, "name")
if wf:
    frappe.db.set_value("Workflow", wf, "is_active", 0)
    frappe.db.commit()

book = frappe.db.get_value("Book", {"status": "Available"}, "name")
member = frappe.db.get_value("Library Member", {"active": 1}, "name")

if book and member:
    txn = frappe.get_doc({
        "doctype": "Library Transaction",
        "book": book,
        "member": member,
        "transaction_type": "Borrow",
        "transaction_date": today(),
        "due_date": add_days(today(), 14)
    })
    txn.insert()
    frappe.db.commit()
    print(f"Created: {txn.name}")

    # Kiểm tra Error Log có notification không
    log = frappe.get_all("Error Log",
        filters={"title": ("like", f"%Library Notification: {txn.name}%")},
        fields=["title", "error"],
        limit=1
    )
    if log:
        print(f"\nNotification Log:")
        print(f"  Title: {log[0].title}")
        print(f"  Content: {log[0].error[:200]}")
        print(f"\nTEST PASSED: Notification was sent via hooks.py doc_events!")
    else:
        print("TEST FAILED: No notification log found")

# Bật lại workflow
if wf:
    frappe.db.set_value("Workflow", wf, "is_active", 1)
    frappe.db.commit()
EOF
```

### Kết quả mong đợi / Expected Output
- Khi tạo Library Transaction (Borrow), notification được log trong Error Log
- Log chứa thông tin: transaction name, book title, member name, email, due date
- `on_transaction_update` ghi vào frappe logger (file log)

### Kiểm tra / Verification
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
# Verify hooks registration
hooks = frappe.get_hooks("doc_events")
lt_hooks = hooks.get("Library Transaction", {})
print("Library Transaction doc_events in hooks:")
for event, handlers in lt_hooks.items():
    print(f"  {event}: {handlers}")
EOF
```

<details>
<summary>Gợi ý / Hints</summary>

- `doc_events` trong hooks.py là cách để **app A** hook vào DocType của **app B**
- Format: `doc_events = { "DocType": { "event": "module.path.function" } }`
- Function phải nhận 2 params: `(doc, method)` — doc là document, method là event name
- Events có sẵn: `before_insert`, `after_insert`, `validate`, `before_save`, `on_update`, `before_submit`, `on_submit`, `before_cancel`, `on_cancel`, `on_trash`
- **`"*"` wildcard:** `doc_events = { "*": { "on_update": "..." } }` — hook vào TẤT CẢ DocTypes
- `frappe.log_error()` ghi vào "Error Log" DocType — dùng cho debug
- `frappe.logger(module).info()` ghi vào file `logs/frappe.log` — dùng cho production logging
- Trong production, dùng `frappe.sendmail()` thay vì log_error
- hooks.py thay đổi cần `bench clear-cache` hoặc `bench restart` để áp dụng

</details>

---

## Exercise 4.5: Scheduled Job — Check Overdue Books / Kiểm tra sách quá hạn

### Mục tiêu / Objective
Tạo scheduled job chạy hàng ngày kiểm tra sách quá hạn (due_date < today và chưa trả). Hiểu cách Frappe scheduler hoạt động.
Create a daily scheduled job to check overdue books (due_date < today and not returned). Understand how the Frappe scheduler works.

### Bước thực hiện / Steps

**Step 1:** Tạo file tasks / Create tasks file

Tạo file `apps/frappe_learn/frappe_learn/library/tasks.py`:

```python
# Copyright (c) 2026, DCNET and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import today, getdate, date_diff


def check_overdue_books():
    """
    Daily scheduled job: Check for overdue book transactions.

    Finds all submitted Borrow transactions where:
    - due_date < today
    - No corresponding Return transaction exists

    Logs results and optionally sends notifications.
    """
    frappe.logger("library").info("Running overdue books check...")

    # Find overdue borrow transactions
    overdue_transactions = frappe.db.sql("""
        SELECT
            lt.name as transaction_name,
            lt.book,
            lt.member,
            lt.member_name,
            lt.due_date,
            lt.transaction_date,
            b.title as book_title,
            lm.email as member_email,
            DATEDIFF(CURDATE(), lt.due_date) as days_overdue
        FROM `tabLibrary Transaction` lt
        JOIN `tabBook` b ON b.name = lt.book
        JOIN `tabLibrary Member` lm ON lm.name = lt.member
        WHERE lt.transaction_type = 'Borrow'
            AND lt.docstatus = 1
            AND lt.due_date < %s
            AND NOT EXISTS (
                SELECT 1 FROM `tabLibrary Transaction` rt
                WHERE rt.book = lt.book
                    AND rt.member = lt.member
                    AND rt.transaction_type = 'Return'
                    AND rt.docstatus = 1
                    AND rt.transaction_date >= lt.transaction_date
            )
        ORDER BY lt.due_date ASC
    """, (today(),), as_dict=True)

    if not overdue_transactions:
        frappe.logger("library").info("No overdue books found.")
        return

    # Log summary
    summary_lines = [
        f"Overdue Books Report — {today()}",
        f"Total overdue: {len(overdue_transactions)}",
        "---"
    ]

    for txn in overdue_transactions:
        line = (
            f"Book: {txn.book_title} | "
            f"Member: {txn.member_name} ({txn.member_email}) | "
            f"Due: {txn.due_date} | "
            f"Overdue: {txn.days_overdue} days | "
            f"Transaction: {txn.transaction_name}"
        )
        summary_lines.append(line)

        # In production: send email to member
        # frappe.sendmail(
        #     recipients=[txn.member_email],
        #     subject=f"Overdue Book: {txn.book_title}",
        #     message=f"Your book '{txn.book_title}' was due on {txn.due_date}. "
        #             f"Please return it as soon as possible."
        # )

    summary = "\n".join(summary_lines)

    # Log to Error Log (visible in Desk)
    frappe.log_error(
        title=f"Overdue Books Check — {today()}",
        message=summary
    )

    frappe.logger("library").info(summary)

    return {
        "total_overdue": len(overdue_transactions),
        "transactions": overdue_transactions
    }


def weekly_library_report():
    """
    Weekly scheduled job: Generate library statistics.
    (Bonus exercise — implement if you want!)
    """
    stats = {
        "total_books": frappe.db.count("Book"),
        "available_books": frappe.db.count("Book", {"status": "Available"}),
        "borrowed_books": frappe.db.count("Book", {"status": "Borrowed"}),
        "total_members": frappe.db.count("Library Member", {"active": 1}),
        "total_transactions": frappe.db.count("Library Transaction", {"docstatus": 1}),
    }

    frappe.log_error(
        title=f"Weekly Library Report — {today()}",
        message="\n".join(f"{k}: {v}" for k, v in stats.items())
    )

    return stats
```

**Step 2:** Cập nhật hooks.py — thêm scheduler_events / Update hooks.py

Thêm vào `hooks.py`:

```python
# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "frappe_learn.library.tasks.check_overdue_books"
    ],
    "weekly": [
        "frappe_learn.library.tasks.weekly_library_report"
    ]
}
```

**Step 3:** Clear cache / Clear cache
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local clear-cache"
```

**Step 4:** Test thủ công (không đợi scheduler) / Test manually

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
import frappe
from frappe.utils import today, add_days

# Tắt workflow để test
wf = frappe.db.get_value("Workflow", {"document_type": "Library Transaction", "is_active": 1}, "name")
if wf:
    frappe.db.set_value("Workflow", wf, "is_active", 0)
    frappe.db.commit()

# Tạo overdue transaction (due_date = 7 ngày trước)
book = frappe.db.get_value("Book", {"status": "Available"}, "name")
member = frappe.db.get_value("Library Member", {"active": 1}, "name")

if book and member:
    txn = frappe.get_doc({
        "doctype": "Library Transaction",
        "book": book,
        "member": member,
        "transaction_type": "Borrow",
        "transaction_date": add_days(today(), -21),
        "due_date": add_days(today(), -7)  # 7 ngày quá hạn
    })
    txn.insert()
    txn.submit()
    frappe.db.commit()
    print(f"Created overdue transaction: {txn.name}, due: {txn.due_date}")

# Chạy task thủ công
from frappe_learn.library.tasks import check_overdue_books
result = check_overdue_books()
frappe.db.commit()

if result:
    print(f"\nOverdue books found: {result['total_overdue']}")
    for t in result['transactions']:
        print(f"  {t.book_title} — overdue {t.days_overdue} days — member: {t.member_name}")
else:
    print("\nNo overdue books (or function returned None)")

# Kiểm tra Error Log
log = frappe.get_all("Error Log",
    filters={"title": ("like", f"%Overdue Books Check%{today()}%")},
    fields=["title", "error"],
    limit=1
)
if log:
    print(f"\nError Log entry found: {log[0].title}")
    print(f"Content preview: {log[0].error[:300]}")
else:
    print("\nNo Error Log entry found")

# Bật lại workflow
if wf:
    frappe.db.set_value("Workflow", wf, "is_active", 1)
    frappe.db.commit()
EOF
```

**Step 5:** Test với bench execute / Test via bench execute (giống scheduler chạy)

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local execute frappe_learn.library.tasks.check_overdue_books"
```

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local execute frappe_learn.library.tasks.weekly_library_report"
```

### Kết quả mong đợi / Expected Output
- `check_overdue_books()` trả về danh sách sách quá hạn
- Error Log có entry "Overdue Books Check" với chi tiết
- `bench execute` chạy thành công, không lỗi
- `weekly_library_report()` trả về thống kê thư viện

### Kiểm tra / Verification
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
# Verify scheduler hooks registered
hooks = frappe.get_hooks("scheduler_events")
print("Scheduler Events:")
for freq, tasks in hooks.items():
    for task in tasks:
        if "frappe_learn" in task:
            print(f"  {freq}: {task}")

# Verify functions importable
try:
    from frappe_learn.library.tasks import check_overdue_books, weekly_library_report
    print("\nFunctions importable: OK")
except ImportError as e:
    print(f"\nImport error: {e}")
EOF
```

<details>
<summary>Gợi ý / Hints</summary>

- `scheduler_events` trong hooks.py định nghĩa các cron jobs
- Frequencies: `all` (mỗi 60s), `hourly`, `daily`, `weekly`, `monthly`, `cron` (custom crontab)
- **Custom cron:**
  ```python
  scheduler_events = {
      "cron": {
          "0 9 * * *": [  # 9:00 AM mỗi ngày
              "frappe_learn.library.tasks.check_overdue_books"
          ]
      }
  }
  ```
- Scheduler chạy bởi `bench schedule` process — kiểm tra: `bench doctor`
- `bench execute module.path.function` — chạy function thủ công (giống scheduler gọi)
- `bench execute` có thể truyền args: `bench execute module.func --kwargs '{"arg1": "val1"}'`
- Scheduled function KHÔNG nhận tham số — phải tự query data
- **Best practice:** Log kết quả bằng `frappe.log_error()` hoặc `frappe.logger()` để debug
- Trong production, scheduled job nên có error handling: `try/except` + `frappe.log_error()`
- `frappe.db.sql()` trong scheduled job dùng cho complex queries — nhanh hơn `frappe.get_all()` với nhiều joins

</details>

---

## Tổng kết Module 4 / Module 4 Summary

### File Structure toàn bộ / Complete File Structure

```
apps/frappe_learn/frappe_learn/
├── __init__.py
├── hooks.py                     ← doc_events + scheduler_events
├── modules.txt                  ← "Frappe Learn" + "Library"
├── patches.txt
├── frappe_learn/
│   └── __init__.py
└── library/
    ├── __init__.py
    ├── notifications.py         ← Ex 4.4: Hook notification functions
    ├── tasks.py                 ← Ex 4.5: Scheduled jobs
    └── doctype/
        ├── __init__.py
        ├── book/
        │   ├── __init__.py
        │   ├── book.json
        │   └── book.py
        ├── book_copy/
        │   ├── __init__.py
        │   ├── book_copy.json
        │   └── book_copy.py
        ├── library_member/
        │   ├── __init__.py
        │   ├── library_member.json
        │   └── library_member.py
        └── library_transaction/
            ├── __init__.py
            ├── library_transaction.json
            └── library_transaction.py  ← Ex 4.1-4.3: Controller with validate, on_submit, on_cancel
```

### hooks.py cuối cùng / Final hooks.py

```python
app_name = "frappe_learn"
app_title = "Frappe Learn"
app_publisher = "DCNET"
app_description = "Learning exercises for Frappe Framework"
app_email = "learn@dcnet.vn"
app_license = "MIT"
app_version = "0.1.0"

# Document Events
doc_events = {
    "Library Transaction": {
        "after_insert": "frappe_learn.library.notifications.send_borrow_notification",
        "on_update": "frappe_learn.library.notifications.on_transaction_update",
    }
}

# Scheduled Tasks
scheduler_events = {
    "daily": [
        "frappe_learn.library.tasks.check_overdue_books"
    ],
    "weekly": [
        "frappe_learn.library.tasks.weekly_library_report"
    ]
}
```

| # | Kỹ năng / Skill | Trạng thái / Status |
|---|-----------------|---------------------|
| 4.1 | Controller validate() — data validation | [ ] |
| 4.2 | Controller on_submit() — cross-doc update + logging | [ ] |
| 4.3 | Controller on_cancel() — reverse/undo logic | [ ] |
| 4.4 | hooks.py doc_events — notification on insert | [ ] |
| 4.5 | Scheduled job — daily overdue check | [ ] |

### Verification toàn bộ / Full Module Verification
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
print("=== Controller Methods ===")
from frappe_learn.library.doctype.library_transaction.library_transaction import LibraryTransaction
for m in ['validate', 'on_submit', 'on_cancel', 'update_book_status', 'reverse_book_status', 'log_transaction']:
    print(f"  {'OK' if hasattr(LibraryTransaction, m) else 'MISSING'}: {m}")

print("\n=== Hooks: doc_events ===")
hooks = frappe.get_hooks("doc_events")
lt_hooks = hooks.get("Library Transaction", {})
for event, handlers in lt_hooks.items():
    for h in handlers:
        if "frappe_learn" in h:
            print(f"  {event}: {h}")

print("\n=== Hooks: scheduler_events ===")
sched = frappe.get_hooks("scheduler_events")
for freq, tasks in sched.items():
    for t in tasks:
        if "frappe_learn" in t:
            print(f"  {freq}: {t}")

print("\n=== Functions Importable ===")
try:
    from frappe_learn.library.notifications import send_borrow_notification, on_transaction_update
    from frappe_learn.library.tasks import check_overdue_books, weekly_library_report
    print("  All functions: OK")
except ImportError as e:
    print(f"  Import error: {e}")
EOF
```

### Test end-to-end / Full Integration Test

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
import frappe
from frappe.utils import today, add_days

# Tắt workflow để test
wf = frappe.db.get_value("Workflow", {"document_type": "Library Transaction", "is_active": 1}, "name")
if wf:
    frappe.db.set_value("Workflow", wf, "is_active", 0)
    frappe.db.commit()

print("=== End-to-End Integration Test ===\n")

# 1. Tạo sách mới
book = frappe.get_doc({
    "doctype": "Book",
    "title": "Integration Test Book",
    "author": "Test Author",
    "isbn": "9789999999999",
    "status": "Available"
})
book.insert()
frappe.db.commit()
print(f"1. Book created: {book.name}, status={book.status}")

# 2. Tạo member
member = frappe.db.get_value("Library Member", {"active": 1}, "name")
print(f"2. Using member: {member}")

# 3. Borrow (validate + on_submit + notification)
txn = frappe.get_doc({
    "doctype": "Library Transaction",
    "book": book.name,
    "member": member,
    "transaction_type": "Borrow",
    "transaction_date": today()
})
txn.insert()   # triggers validate() + after_insert hook (notification)
txn.submit()   # triggers on_submit() (update book status)
frappe.db.commit()
print(f"3. Borrow submitted: {txn.name}, due={txn.due_date}")
print(f"   Book status: {frappe.db.get_value('Book', book.name, 'status')}")

# 4. Cancel (on_cancel → reverse)
txn.reload()
txn.cancel()
frappe.db.commit()
print(f"4. Borrow cancelled")
print(f"   Book status: {frappe.db.get_value('Book', book.name, 'status')}")

# 5. Check overdue (scheduled task)
from frappe_learn.library.tasks import check_overdue_books
result = check_overdue_books()
frappe.db.commit()
print(f"5. Overdue check: {result['total_overdue'] if result else 0} overdue books")

status = frappe.db.get_value("Book", book.name, "status")
print(f"\n{'PASSED' if status == 'Available' else 'FAILED'}: Final book status is '{status}'")

# Bật lại workflow
if wf:
    frappe.db.set_value("Workflow", wf, "is_active", 1)
    frappe.db.commit()
EOF
```

> **Tiếp theo / Next:** Module 5 — Web Views & API (coming soon)
>
> **Quay lại / Back to:** [Exercise 01 - Setup](ex-01-setup.md) | [Exercise 02 - DocType](ex-02-doctype.md) | [Exercise 03 - Scripting](ex-03-scripting.md)
