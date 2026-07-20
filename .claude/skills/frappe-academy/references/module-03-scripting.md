# Module 3: Client & Server Scripting

> **Mục tiêu:** Viết Client Scripts (frontend JS) và Server Scripts (backend Python) để thêm business logic. Nắm vững nhưng SAI LẦM PHỔ BIẾN nhất khi viết scripts.
> **Thời lượng:** 6 lessons | **Độ khó:** Intermediate
> **Yêu cầu:** Hoàn thành Module 2, có Library Book/Member/Transaction DocTypes

---

## L3.1: Client Script Basics

### Tổng quan
Client Scripts chạy trên browser (JavaScript), điều khiển hành vì form — an/hiện fields, validate trước khi save, thêm custom buttons, fetch data từ server. Có 2 cach viết: (1) trong file `.js` của DocType, (2) tạo "Client Script" DocType qua UI. Bài này day cach 1 — viết trong file, là cach chuyên nghiệp.

### Key Concepts

#### 1. Event-driven Model

```javascript
// library_book.js — Client Script cho DocType "Library Book"

frappe.ui.form.on("Library Book", {
    // === FORM EVENTS ===

    // Khi form load lần đầu (chưa có data)
    setup(frm) {
        // Setup 1 lần duy nhất — set queries, default values
        console.log("setup: form initialized");
    },

    // Khi form load xong data
    onload(frm) {
        // Form đã có data — có thể đọc frm.đọc.field
        console.log("onload: data loaded");
    },

    // Mỗi lần form render (load + sau save + sau route change)
    refresh(frm) {
        // ⭐ Event DUNG NHIEU NHAT
        // Thêm custom buttons, update UI, conditional display
        console.log("refresh: form rendered");
    },

    // Trước khi save (client-side validation)
    validate(frm) {
        // Return false để cancel save
        // frappe.throw("Error") để hiện error + cancel
        console.log("validate: before save");
    },

    // Sau khi save thành cong
    after_save(frm) {
        console.log("after_save: saved successfully");
    },

    // Khi form data thay đổi (bất kỳ field nào)
    onload_post_render(frm) {
        console.log("onload_post_render: form fully rendered");
    },

    // === FIELD EVENTS ===

    // Khi field "status" thay đổi
    status(frm) {
        console.log("status changed to:", frm.doc.status);
    },

    // Khi field "author" thay đổi
    author(frm) {
        if (frm.doc.author) {
            frappe.show_alert(`Author: ${frm.doc.author}`);
        }
    }
});
```

#### 2. `frm` Object — Toàn bộ form API

```javascript
// frm là Form object — entry point cho mọi thu

// === DOC DATA ===
frm.doc                    // Document data (JS object)
frm.doc.name               // Document name
frm.doc.status             // Giá trị field "status"
frm.doc.items              // Child table rows (array)
frm.doc.__islocal          // True nếu document chưa save (new)

// === FORM STATE ===
frm.is_new()               // True nếu document mới
frm.is_dirty()             // True nếu có thay đổi chưa save
frm.doc.docstatus           // 0=Draft, 1=Submitted, 2=Cancelled

// === SET VALUES ===
frm.set_value("status", "Borrowed")     // Set field value (trigger change event)
frm.doc.status = "Borrowed"              // Direct set (KHÔNG trigger events)

// === UI CONTROL ===
frm.set_df_property("status", "read_only", 1)   // Set field property
frm.toggle_display("description", false)          // An field
frm.toggle_reqd("isbn", true)                     // Bat bước
frm.toggle_enable("author", false)                // Disable

// === REFRESH ===
frm.refresh_fields()       // Refresh UI sau khi thay đổi frm.đọc
frm.reload_doc()           // Reload từ server
frm.dirty()                // Danh đầu form đã thay đổi (hiện nut Save)
```

#### 3. Event Execution Order

```
New Document:    setup → onload → refresh → onload_post_render
Existing Doc:    setup → onload → refresh → onload_post_render
Field Change:    field_event → form.on_change (frm)
Save:            validate → (server save) → after_save → refresh
```

### Code Examples

```javascript
// library_book.js — Ví dụ thuc te

frappe.ui.form.on("Library Book", {
    refresh(frm) {
        // Highlight status bang màu
        if (frm.doc.status === "Borrowed") {
            frm.dashboard.set_headline_alert(
                '<div class="alert alert-warning">This book is currently borrowed</div>'
            );
        }

        // An ISBN field nếu đã submit
        if (frm.doc.docstatus === 1) {
            frm.toggle_enable("isbn", false);
        }
    },

    validate(frm) {
        // Validate ISBN format (13 digits)
        if (frm.doc.isbn && !/^\d{13}$/.test(frm.doc.isbn.replace(/-/g, ""))) {
            frappe.throw(__("ISBN must be 13 digits"));
            // frappe.throw tự động return false + hiện error dialog
        }
    },

    status(frm) {
        // Khi đổi status → bắt buộc ghi notes
        if (frm.doc.status === "Lost" || frm.doc.status === "Damaged") {
            frm.toggle_reqd("description", true);
            frappe.show_alert({
                message: __("Please describe the issue in Description"),
                indicator: "orange"
            });
        } else {
            frm.toggle_reqd("description", false);
        }
    }
});
```

### Mini Quiz

<details>
<summary>Q1: Phân biệt `frm.set_value("status", "X")` và `frm.doc.status = "X"`. Khi nào dùng cái nao?</summary>

**A:** `frm.set_value()` — set value VA trigger field change event (gọi `status(frm)` callback). `frm.doc.status = "X"` — chi set value, KHÔNG trigger events. Dùng `set_value` khi mượn cascade logic. Dùng direct set khi chi mượn thay đổi data (VD: trong validate, trước khi save).
</details>

<details>
<summary>Q2: Bạn muốn ẩn field "cover_image" khi category = "Reference". Viết code ở đầu và như nào?</summary>

**A:** Trong 2 cho: `refresh` (cho luc load) và `category` (cho luc thay đổi):
```javascript
frappe.ui.form.on("Library Book", {
    refresh(frm) {
        frm.toggle_display("cover_image", frm.doc.category !== "Reference");
    },
    category(frm) {
        frm.toggle_display("cover_image", frm.doc.category !== "Reference");
    }
});
```
</details>

### Skill References

- **DEEP DIVE:** Xem skill `dcnet_quality` -> `syntax/erpnext-syntax-clientscripts/` cho FULL coding rules
- **DEEP DIVE:** Xem skill `frappe` -> `references/desk/` cho Desk UI API reference

---

## L3.2: Client Script Advanced

### Tổng quan
Nâng cao: filter Link fields (set_query), thêm custom buttons, gọi server API từ client (frappe.call), xử lý child table events. Đây là nhưng kỹ thuật dùng hàng ngày khi customize ERPNext forms.

### Key Concepts

#### 1. frm.set_query() — Filter Link Fields

```javascript
frappe.ui.form.on("Library Transaction", {
    setup(frm) {
        // Chi hiện books có status = "Available" trong dropdown
        frm.set_query("book", "items", function(doc, cdt, cdn) {
            return {
                filters: {
                    status: "Available"
                }
            };
        });

        // Filter member theo type
        frm.set_query("member", function() {
            return {
                filters: {
                    status: "Active",
                    member_type: ["in", ["Student", "Faculty"]]
                }
            };
        });
    }
});
```

#### 2. frm.add_custom_button() — Thêm nut tùy chỉnh

```javascript
frappe.ui.form.on("Library Transaction", {
    refresh(frm) {
        // Chi hiện nut khi document đã Submit
        if (frm.doc.docstatus === 1 && frm.doc.transaction_type === "Borrow") {

            // Nut đơn giản
            frm.add_custom_button(__("Return Books"), function() {
                frappe.confirm(
                    __("Mark all books as returned?"),
                    function() {
                        // Gọi server method
                        frappe.call({
                            method: "frappe_learn.library.doctype.library_transaction.library_transaction.return_books",
                            args: { transaction_name: frm.doc.name },
                            callback: function(r) {
                                if (r.message) {
                                    frappe.show_alert({
                                        message: __("Books returned successfully"),
                                        indicator: "green"
                                    });
                                    frm.reload_doc();
                                }
                            }
                        });
                    }
                );
            }, __("Actions"));  // Nhóm nut vao dropdown "Actions"

            // Nut trong nhóm
            frm.add_custom_button(__("Extend Due Date"), function() {
                // Hiện dialog để nhập ngày mới
                let d = new frappe.ui.Dialog({
                    title: __("Extend Due Date"),
                    fields: [
                        {
                            fieldname: "new_date",
                            fieldtype: "Date",
                            label: __("New Due Date"),
                            reqd: 1,
                            default: frappe.datetime.add_days(frappe.datetime.nowdate(), 7)
                        }
                    ],
                    primary_action_label: __("Extend"),
                    primary_action(values) {
                        frappe.call({
                            method: "frappe_learn.api.extend_due_date",
                            args: {
                                transaction: frm.doc.name,
                                new_date: values.new_date
                            },
                            callback: function(r) {
                                d.hide();
                                frm.reload_doc();
                            }
                        });
                    }
                });
                d.show();
            }, __("Actions"));
        }

        // Nut tạo document liên quan
        if (!frm.is_new()) {
            frm.add_custom_button(__("New Transaction"), function() {
                frappe.new_doc("Library Transaction", {
                    member: frm.doc.member
                });
            }, __("Create"));
        }
    }
});
```

#### 3. frappe.call() — Gọi Server từ Client

```javascript
// Cach 1: Gọi whitelisted method
frappe.call({
    method: "frappe_learn.api.get_book_availability",
    args: {
        book_name: "BOOK-0001"
    },
    async: true,           // default true
    freeze: true,          // Hiện loading overlay
    freeze_message: __("Checking availability..."),
    callback: function(r) {
        // r.message = return value từ server
        if (r.message) {
            console.log("Available:", r.message.available);
        }
    },
    error: function(r) {
        // Xử lý lỗi
        frappe.msgprint(__("Error checking availability"));
    }
});

// Cach 2: Promise-based (modern)
let result = await frappe.call({
    method: "frappe_learn.api.get_book_availability",
    args: { book_name: "BOOK-0001" }
});
console.log(result.message);

// Cach 3: Gọi đọc method
frappe.xcall(
    "frappe_learn.library.doctype.library_transaction.library_transaction.return_books",
    { transaction_name: frm.doc.name }
).then(r => {
    console.log(r);
});
```

#### 4. Child Table Events

```javascript
// Events cho child table "Library Transaction Item"
frappe.ui.form.on("Library Transaction Item", {
    // Khi thêm row mới
    items_add(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        // Set default due date = 14 ngày sau
        frappe.model.set_value(cdt, cdn, "due_date",
            frappe.datetime.add_days(frappe.datetime.nowdate(), 14)
        );
    },

    // Khi xóa row
    items_remove(frm, cdt, cdn) {
        // Recalculate something
        frm.trigger("calculate_totals");
    },

    // Khi field "book" trong row thay đổi
    book(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.book) {
            // Fetch thêm thông tin từ book
            frappe.call({
                method: "frappe.client.get_value",
                args: {
                    doctype: "Library Book",
                    filters: { name: row.book },
                    fieldname: ["title", "author", "status"]
                },
                callback: function(r) {
                    if (r.message) {
                        frappe.model.set_value(cdt, cdn, "book_title", r.message.title);
                        if (r.message.status !== "Available") {
                            frappe.throw(__(`Book ${r.message.title} is not available (${r.message.status})`));
                        }
                    }
                }
            });
        }
    }
});
```

### Code Examples

```javascript
// Full client script cho Library Transaction
// File: frappe_learn/library/doctype/library_transaction/library_transaction.js

frappe.ui.form.on("Library Transaction", {
    setup(frm) {
        // Filter: chi hiện sach Available khi Borrow
        frm.set_query("book", "items", function(doc) {
            if (doc.transaction_type === "Borrow") {
                return { filters: { status: "Available" } };
            }
            return {};
        });

        // Filter: chi hiện members Active
        frm.set_query("member", function() {
            return { filters: { status: "Active" } };
        });
    },

    refresh(frm) {
        // Nut Return cho Borrow transactions đã Submit
        if (frm.doc.docstatus === 1 && frm.doc.transaction_type === "Borrow") {
            frm.add_custom_button(__("Return Books"), function() {
                frappe.call({
                    method: "frappe_learn.api.return_books",
                    args: { transaction_name: frm.doc.name },
                    freeze: true,
                    callback: function(r) {
                        frm.reload_doc();
                    }
                });
            });
        }
    },

    validate(frm) {
        // Không cho mượn qua 5 sach 1 lần
        if (frm.doc.transaction_type === "Borrow" && frm.doc.items.length > 5) {
            frappe.throw(__("Cannot borrow more than 5 books at once"));
        }
    },

    transaction_type(frm) {
        // Clear items khi đổi type
        frm.clear_table("items");
        frm.refresh_field("items");
    }
});
```

### Mini Quiz

<details>
<summary>Q1: `frm.set_query("book", "items", fn)` — tham số "items" là gì?</summary>

**A:** "items" là **fieldname của child table** trong parent DocType. Khi set_query có 3 tham số: `(link_fieldname, child_table_fieldname, filter_function)` — nó filter Link field "book" **ben trong** child table "items". Nếu không có tham số thứ 2, nó filter Link field trên parent form.
</details>

<details>
<summary>Q2: Làm sao để set value cho 1 field trong child table row?</summary>

**A:** Dùng `frappe.model.set_value(cdt, cdn, fieldname, value)`. `cdt` = child DocType name, `cdn` = child row name. KHÔNG dùng `frm.set_value()` cho child rows. Hoặc: `row.fieldname = value` + `frm.refresh_field("items")`.
</details>

### Skill References

- **DEEP DIVE:** Xem skill `dcnet_quality` -> `syntax/erpnext-syntax-clientscripts/` cho TẤT CẢ coding rules và patterns
- **DEEP DIVE:** Xem skill `frappe` -> `references/desk_api_reference/` cho Dialog, MessageBox, API reference

---

## L3.3: Server Script Basics

### Tổng quan
Server Scripts chạy trên server (Python), truy cập trực tiếp database và system. Có 2 cach viết: (1) Controller methods trong `.py` file, (2) "Server Script" DocType qua UI (sandbox). Bài này day cach 2 — Server Script DocType — thích hợp cho quick customizations và non-developers.

### Key Concepts

#### 1. Server Script Types

| Type | Trigger | Return | Khi nào dùng |
|------|---------|--------|------------|
| **Before Insert** | Trước insert (đọc mới) | — | Validate, set defaults |
| **Before Save** | Trước save (new + existing) | — | Validate, calculate |
| **After Save** | Sau save | — | Side effects (email, log) |
| **Before Submit** | Trước submit | — | Final validation |
| **After Submit** | Sau submit | — | Trigger workflows |
| **Before Cancel** | Trước cancel | — | Check dependencies |
| **After Cancel** | Sau cancel | — | Reverse effects |
| **API** | HTTP request | Value | Custom endpoint |

#### 2. Server Script Context

```python
# Bien có sẵn trong Server Script (KHÔNG CAN import):
# đọc        — Document hiện tại (không có cho API type)
# frappe     — Frappe module (frappe.db, frappe.utils, etc.)
# utils      — frappe.utils shortcut
# get_list   — frappe.get_list shortcut
# get_all    — frappe.get_all shortcut
# get_đọc    — frappe.get_đọc shortcut
# get_value  — frappe.db.get_value shortcut
# throw      — frappe.throw shortcut
```

#### 3. Before Save Script

```python
# Server Script: Before Save on "Library Book"
# DocType: Library Book
# Script Type: Before Save

# Validate ISBN format
if doc.isbn:
    isbn_clean = doc.isbn.replace("-", "")
    if len(isbn_clean) != 13 or not isbn_clean.isdigit():
        frappe.throw("ISBN must be 13 digits")

# Auto-set title case
if doc.title:
    doc.title = doc.title.title()

# Auto-set author from ISBN (example)
if doc.isbn and not doc.author:
    doc.author = "Unknown"
```

#### 4. After Save Script

```python
# Server Script: After Save on "Library Transaction"
# DocType: Library Transaction
# Script Type: After Save

# Update book status khi tạo transaction
if doc.transaction_type == "Borrow":
    for item in doc.items:
        frappe.db.set_value("Library Book", item.book, "status", "Borrowed")

elif doc.transaction_type == "Return":
    for item in doc.items:
        frappe.db.set_value("Library Book", item.book, "status", "Available")
```

#### 5. API Script

```python
# Server Script Type: API
# API Method: get_available_books
# URL: /api/method/get_available_books

# Trong script:
books = frappe.get_all("Library Book",
    filters={"status": "Available"},
    fields=["name", "title", "author", "category"],
    order_by="title asc"
)
frappe.response["message"] = books
```

```javascript
// Gọi từ client:
frappe.call({
    method: "get_available_books",
    callback: function(r) {
        console.log(r.message);  // List of available books
    }
});
```

### Code Examples

```python
# === Ví dụ 1: Validate trước Save ===
# Type: Before Save | DocType: Library Member

# Không cho email trung
existing = frappe.db.exists("Library Member", {
    "email": doc.email,
    "name": ["!=", doc.name]  # Tru chinh no
})
if existing:
    frappe.throw(f"Email {doc.email} already registered by {existing}")

# === Ví dụ 2: Auto-calculate sau Save ===
# Type: After Save | DocType: Library Transaction

# Đếm số sach đang mượn của member
borrowed_count = frappe.db.count("Library Transaction",
    filters={
        "member": doc.member,
        "transaction_type": "Borrow",
        "docstatus": 1
    }
)
# Cập nhật member record
frappe.db.set_value("Library Member", doc.member,
    "books_borrowed", borrowed_count)

# === Vi du 3: API endpoint ===
# Type: API | Method: check_member_eligibility

member_name = frappe.form_dict.get("member")
if not member_name:
    frappe.throw("Member is required")

member = frappe.get_doc("Library Member", member_name)

# Kiểm tra điều kiện
eligible = True
reasons = []

if member.status != "Active":
    eligible = False
    reasons.append("Member is not active")

# Đếm sach đang mượn
borrowed = frappe.db.count("Library Transaction Item", {
    "parent": ["in", frappe.get_all("Library Transaction",
        filters={"member": member_name, "transaction_type": "Borrow", "docstatus": 1},
        pluck="name"
    )],
    "status": "Borrowed"
})

if borrowed >= 5:
    eligible = False
    reasons.append(f"Already borrowed {borrowed} books (max 5)")

frappe.response["message"] = {
    "eligible": eligible,
    "reasons": reasons,
    "current_borrowed": borrowed
}
```

### Mini Quiz

<details>
<summary>Q1: Server Script "Before Save" và "After Save" — khác nhau thế nào về kha nang thay đổi đọc?</summary>

**A:** **Before Save** — có thể thay đổi `doc.field` và thay đổi SẼ ĐƯỢC LƯU (vi chưa save vao DB). **After Save** — đọc ĐÃ LƯU vao DB rồi, thay đổi `doc.field` SẼ KHÔNG được lưu. Nếu mượn thay đổi sau save, dùng `frappe.db.set_value()` (update trực tiếp DB).
</details>

<details>
<summary>Q2: Trong Server Script, làm sao để trả về error và dùng save?</summary>

**A:** Dùng `frappe.throw("Error message")`. No raise exception, dùng save, và hiện error message cho user. Có thể dùng `frappe.throw("Message", frappe.ValidationError)` để chỉ định error type.
</details>

### Skill References

- **DEEP DIVE:** Xem skill `dcnet_quality` -> `syntax/erpnext-syntax-serverscripts/` cho FULL Server Script coding rules
- **DEEP DIVE:** Xem skill `frappe` -> `references/api_reference/` cho frappe.db, frappe.utils API

---

## L3.4: Server Script GOTCHAS

### Tổng quan
Day là bai QUAN TRỌNG NHẤT trong Module 3. Server Scripts chạy trong sandbox — nhiều thư KHÔNG ĐƯỢC PHEP làm. Vì pham sẽ gay lỗi runtime hoặc bảo mật. Bài này liet ke TẤT CẢ rules phải nhỏ khi viết Server Scripts và Client Scripts.

### Key Concepts

#### 1. SERVER SCRIPT — NHỮNG ĐIỀU CẤM

```python
# ❌ SAI — KHÔNG ĐƯỢC import trong Server Script
from frappe.utils import nowdate, add_days
import json
import os

# ✅ DUNG — Dùng trực tiếp từ frappe namespace
today = frappe.utils.nowdate()
next_week = frappe.utils.add_days(today, 7)
data = frappe.parse_json('{"key": "value"}')

# ❌ SAI — KHÔNG ĐƯỢC dùng self
self.status = "Active"
self.validate()

# ✅ DUNG — Dùng đọc
doc.status = "Active"
# Không gọi validate() — Frappe tự động gọi

# ❌ SAI — KHÔNG ĐƯỢC dùng class/def (top-level)
class MyHelper:
    pass

def my_function():
    pass

# ✅ DUNG — Viết logic trực tiếp (procedural)
if doc.status == "Active":
    frappe.db.set_value(...)

# ❌ SAI — KHÔNG ĐƯỢC truy cập file system
open("/etc/passwd", "r")
import subprocess

# ✅ DUNG — Chi dùng Frappe API
frappe.get_doc(...)
frappe.db.sql(...)
```

#### 2. CLIENT SCRIPT — NHỮNG ĐIỀU CẤM

```javascript
// ❌ SAI — KHÔNG ĐƯỢC dùng frappe.db.* trong Client Script
let value = frappe.db.get_value("Customer", "CUST-001", "customer_name");
frappe.db.set_value("Customer", "CUST-001", "status", "Active");

// ✅ DUNG — Dùng frappe.call() để gọi server
frappe.call({
    method: "frappe.client.get_value",
    args: {
        doctype: "Customer",
        filters: { name: "CUST-001" },
        fieldname: "customer_name"
    },
    callback: function(r) {
        console.log(r.message);
    }
});

// ❌ SAI — KHÔNG ĐƯỢC dùng frappe.db.sql() từ client
frappe.db.sql("SELECT * FROM tabCustomer");

// ❌ SAI — KHÔNG async/await trong old-style event handlers
frappe.ui.form.on("My DocType", {
    async refresh(frm) {  // ⚠️ Có thể lỗi trên 1 số browsers
        let data = await frappe.call({...});
    }
});

// ✅ DUNG — Dùng callback pattern
frappe.ui.form.on("My DocType", {
    refresh(frm) {
        frappe.call({
            method: "...",
            callback: function(r) {
                // Xử lý kết quả ở day
            }
        });
    }
});
```

#### 3. CONTROLLER (.py file) — NHỮNG ĐIỀU CẤM

```python
# ❌ SAI — KHÔNG modify fields trong on_update
class LibraryBook(Document):
    def on_update(self):
        self.status = "Active"   # KHONG CO TAC DUNG — doc da save roi!
        self.save()              # GAY INFINITE LOOP!

# ✅ DUNG — Dùng frappe.db.set_value() trong on_update
class LibraryBook(Document):
    def on_update(self):
        frappe.db.set_value("Library Book", self.name, "status", "Active")

# ✅ DUNG — Modify fields trong validate (TRƯỚC save)
class LibraryBook(Document):
    def validate(self):
        self.status = "Active"   # OK — chua save, se duoc luu

# ❌ SAI — Gọi self.save() trong controller methods
class LibraryBook(Document):
    def validate(self):
        self.save()  # INFINITE LOOP! validate → save → validate → save...

# ❌ SAI — Query không có permission check
class LibraryBook(Document):
    def get_all_members(self):
        return frappe.db.sql("SELECT * FROM `tabLibrary Member`")
        # User có thể thay data không có quyền

# ✅ DUNG — Dùng frappe.get_all (co permission check)
class LibraryBook(Document):
    def get_all_members(self):
        return frappe.get_all("Library Member",
            fields=["name", "full_name"])
```

#### 4. Bang tom tat RULES

| Context | import | self | frappe.db.* | class/def | File I/O |
|---------|:------:|:----:|:-----------:|:---------:|:--------:|
| **Server Script** | NO | NO (dùng `doc`) | YES | NO | NO |
| **Client Script** | N/A | N/A | NO (dùng `frappe.call`) | YES | N/A |
| **Controller .py** | YES | YES | YES | YES | Có giới hạn |
| **Whitelisted API** | YES | N/A | YES | YES | Có giới hạn |

### Code Examples

```python
# === Server Script: DUNG CACH ===
# Type: Before Save | DocType: Library Transaction

# Validate member eligibility
member = frappe.get_doc("Library Member", doc.member)

if member.status != "Active":
    frappe.throw(f"Member {member.full_name} is not active")

# Count borrowed books (không cần import)
borrowed = frappe.db.count("Library Transaction",
    filters={
        "member": doc.member,
        "transaction_type": "Borrow",
        "docstatus": 1
    }
)

if borrowed >= 5:
    frappe.throw("Member has reached maximum borrow limit (5 books)")

# Set dates (dùng frappe.utils trực tiếp)
if not doc.transaction_date:
    doc.transaction_date = frappe.utils.nowdate()

for item in doc.items:
    if not item.due_date:
        item.due_date = frappe.utils.add_days(doc.transaction_date, 14)
```

### Mini Quiz

<details>
<summary>Q1: Tại sao KHÔNG ĐƯỢC `import` trong Server Script?</summary>

**A:** Server Script chạy trong **sandbox** (restricted execution environment). Frappe giới hạn để bảo mật — nếu cho import từ do, user có thể `import os; os.system("rm -rf /")`. Tất cả utilities can thiet đã có sẵn qua `frappe.utils`, `frappe.db`, etc.
</details>

<details>
<summary>Q2: Tại sao `self.status = "Active"` trong `on_update` KHÔNG có tác dụng?</summary>

**A:** `on_update` chạy **SAU KHI đã save vao DB**. Thay đổi `self.field` chi thay đổi Python object trong memory, không ghi lại vao DB. Phải dùng `frappe.db.set_value("DocType", self.name, "status", "Active")` để update trực tiếp DB. Hoặc tốt hơn: đặt logic trong `validate()` — chạy TRƯỚC save.
</details>

<details>
<summary>Q3: Ban gọi `frappe.db.get_value()` trong Client Script JS. Dieu gì xảy ra?</summary>

**A:** **LỖI hoặc không hoat dong.** `frappe.db` là server-side Python API, KHÔNG tồn tại trên client JavaScript. Phải dùng `frappe.call({method: "frappe.client.get_value", args: {...}})` để gọi server và nhận kết quả qua callback.
</details>

### Skill References

- **DEEP DIVE:** Xem skill `dcnet_quality` -> `syntax/erpnext-syntax-serverscripts/` — PHẢI ĐỌC trước khi viết Server Script
- **DEEP DIVE:** Xem skill `dcnet_quality` -> `syntax/erpnext-syntax-clientscripts/` — PHẢI ĐỌC trước khi viết Client Script
- **DEEP DIVE:** Xem skill `dcnet_quality` -> `syntax/erpnext-syntax-controllers/` — PHẢI ĐỌC trước khi viết Controller
- **DEEP DIVE:** Xem skill `dcnet_quality` -> `errors/` cho error handling patterns

---

## L3.5: System Console

### Tổng quan
`bench console` là interactive Python REPL có sẵn Frappe context — database connected, site loaded, mọi API sẵn sàng dùng. Đây là công cụ để thử nghiệm nhanh trước khi viết code vao file. Bài này day cach dùng hiệu quả và nhưng kỹ thuật debug.

### Key Concepts

#### 1. Khởi động Console

```bash
# Trong devcontainer:
cd /workspace/development/frappe-bench

# Mo console cho site cũ the
bench --site flow.local console

# Trong console — sẵn sàng dùng:
>>> frappe.session.user
'Administrator'

>>> frappe.local.site
'flow.local'
```

#### 2. CRUD Operations

```python
# === CREATE ===
doc = frappe.get_doc({
    "doctype": "Library Book",
    "title": "The Pragmatic Programmer",
    "author": "Andy Hunt",
    "isbn": "9780135957059",
    "category": "Reference"
})
doc.insert()
frappe.db.commit()  # ⚠️ QUAN TRONG — phai commit trong console!
print(doc.name)

# === READ ===
# Lay 1 document
doc = frappe.get_doc("Library Book", "BOOK-0001")
print(doc.title, doc.author)

# Lấy nhiều documents
books = frappe.get_all("Library Book",
    filters={"status": "Available"},
    fields=["name", "title", "author"],
    order_by="title asc",
    limit_page_length=10
)
for b in books:
    print(f"  {b.name}: {b.title}")

# Lấy 1 giá trị
title = frappe.db.get_value("Library Book", "BOOK-0001", "title")
print(title)

# === UPDATE ===
doc = frappe.get_doc("Library Book", "BOOK-0001")
doc.status = "Borrowed"
doc.save()
frappe.db.commit()

# Update nhanh không load đọc
frappe.db.set_value("Library Book", "BOOK-0001", "status", "Available")
frappe.db.commit()

# === DELETE ===
frappe.delete_doc("Library Book", "BOOK-0001")
frappe.db.commit()
```

#### 3. Database Queries

```python
# SQL trực tiếp
results = frappe.db.sql("""
    SELECT name, title, author, status
    FROM `tabLibrary Book`
    WHERE status = 'Available'
    ORDER BY title
    LIMIT 10
""", as_dict=True)

for r in results:
    print(f"{r.name}: {r.title} by {r.author}")

# Count
count = frappe.db.count("Library Book", {"status": "Available"})
print(f"Available books: {count}")

# Exists
exists = frappe.db.exists("Library Book", {"isbn": "9780135957059"})
print(f"Book exists: {exists}")

# Get list (với permission check)
members = frappe.get_list("Library Member",
    filters={"status": "Active"},
    fields=["name", "full_name", "email"],
    limit_page_length=0  # No limit
)
print(f"Active members: {len(members)}")
```

#### 4. Debug Techniques

```python
# Xem DocType metadata
meta = frappe.get_meta("Library Book")
print("Fields:")
for f in meta.fields:
    print(f"  {f.fieldname:20s} {f.fieldtype:15s} reqd={f.reqd}")

# Xem hooks của 1 app
import frappe.utils.change_log
hooks = frappe.get_hooks()
print("doc_events:", hooks.get("doc_events", {}))

# Xem scheduled jobs
from frappe.utils.scheduler import get_jobs
jobs = frappe.get_all("Scheduled Job Type",
    fields=["name", "method", "frequency"],
    limit=20
)
for j in jobs:
    print(f"  {j.frequency:10s} {j.method}")

# Test email (dry run)
frappe.sendmail(
    recipients=["test@example.com"],
    subject="Test",
    message="Hello from console",
    now=True
)
```

### Code Examples

```bash
# Workflow đầy đủ trong devcontainer:

docker exec -it devcontainer-frappe-1 bash -c "
cd /workspace/development/frappe-bench && bench --site flow.local console <<'PYTHON'
# Quick data exploration
print('=== Site Info ===')
print(f'Site: {frappe.local.site}')
print(f'User: {frappe.session.user}')
print(f'Apps: {frappe.get_installed_apps()}')

print('\n=== DocType Count ===')
doctypes = frappe.get_all('DocType', filters={'custom': 0}, limit_page_length=0)
print(f'Total DocTypes: {len(doctypes)}')

print('\n=== Recent Documents ===')
recent = frappe.db.sql('''
    SELECT doctype, name, modified
    FROM __global_search
    ORDER BY modified DESC
    LIMIT 5
''', as_dict=True)
for r in recent:
    print(f'  {r.doctype}: {r.name} ({r.modified})')
PYTHON
"
```

### Mini Quiz

<details>
<summary>Q1: Tại sao trong `bench console` phải gọi `frappe.db.commit()` sau khi insert/update/delete?</summary>

**A:** Bench console KHÔNG tự động commit transactions (khác với web requests — Frappe tự động commit sau mọi request thành cong). Nếu không commit, thay đổi chi tồn tại trong memory và mất khi thoat console. `frappe.db.commit()` ghi thay đổi vao database.
</details>

<details>
<summary>Q2: Phân biệt `frappe.get_all()` và `frappe.db.sql()`. Khi nào dùng cái nao?</summary>

**A:** `frappe.get_all()` — có **permission check** (chi trả về data user có quyền xem), syntax đơn giản, ẩn toàn. `frappe.db.sql()` — **KHÔNG có permission check**, chạy raw SQL, linh hoạt hơn nhưng nguy hiếm hon. Dùng `get_all` cho production code, `db.sql` cho debug/admin tasks hoặc queries phức tạp.
</details>

### Skill References

- **DEEP DIVE:** Xem skill `dcnet_quality` -> `core/` cho database API patterns và best practices
- **DEEP DIVE:** Xem skill `frappe` -> `references/api_reference/` cho full frappe.db API

---

## L3.6: Hands-on — 5 Scripts cho Library System

### Tổng quan
Thực hành viết 5 scripts cho Library Management System đã tạo ở Module 2. Mỗi script ap dùng 1 kỹ thuật khác nhau: validation, calculation, filtering, custom button, và API endpoint.

### Script 1: Validate Book ISBN (Server Script — Before Save)

```python
# Tạo Server Script qua UI: /app/server-script/new
# Name: Validate Library Book ISBN
# DocType Reference: Library Book
# Script Type: Before Save

# Validate ISBN-13 format
if doc.isbn:
    isbn_clean = doc.isbn.replace("-", "").replace(" ", "")

    if len(isbn_clean) != 13:
        frappe.throw("ISBN must be exactly 13 digits")

    if not isbn_clean.isdigit():
        frappe.throw("ISBN must contain only digits (and optional dashes)")

    # ISBN-13 checksum validation
    total = 0
    for i, digit in enumerate(isbn_clean):
        if i % 2 == 0:
            total += int(digit)
        else:
            total += int(digit) * 3

    if total % 10 != 0:
        frappe.throw("Invalid ISBN checksum. Please verify the ISBN number.")

    # Normalize: lưu không có dash
    doc.isbn = isbn_clean
```

### Script 2: Auto-calculate Late Fees (Server Script — Before Save)

```python
# Name: Calculate Late Fees
# DocType Reference: Library Transaction
# Script Type: Before Save

# Tinh phi tre cho mọi sach đã tra
if doc.transaction_type == "Return":
    total_late_fee = 0
    late_fee_per_day = 5000  # 5,000 VND/ngay

    for item in doc.items:
        if item.return_date and item.due_date:
            due = frappe.utils.getdate(item.due_date)
            returned = frappe.utils.getdate(item.return_date)

            if returned > due:
                days_late = frappe.utils.date_diff(returned, due)
                item.late_fee = days_late * late_fee_per_day
                item.status = "Overdue"
            else:
                item.late_fee = 0
                item.status = "Returned"

            total_late_fee += (item.late_fee or 0)

    doc.total_late_fee = total_late_fee

    if total_late_fee > 0:
        frappe.msgprint(
            f"Late fee: {frappe.utils.fmt_money(total_late_fee, currency='VND')}",
            title="Late Return",
            indicator="orange"
        )
```

### Script 3: Filter Members by Type (Client Script)

```javascript
// File: library_transaction.js (thêm vao setup event)
// Hoặc tạo Client Script qua UI: /app/client-script/new

frappe.ui.form.on("Library Transaction", {
    setup(frm) {
        // Filter books: chi hiện Available khi Borrow
        frm.set_query("book", "items", function(doc) {
            let filters = {};
            if (doc.transaction_type === "Borrow") {
                filters.status = "Available";
            } else if (doc.transaction_type === "Return") {
                filters.status = "Borrowed";
            }
            return { filters: filters };
        });

        // Filter members: chi Active
        frm.set_query("member", function() {
            return {
                filters: {
                    status: "Active"
                }
            };
        });
    },

    // Re-filter khi đổi transaction type
    transaction_type(frm) {
        // Clear items vì filter đã thay đổi
        frm.clear_table("items");
        frm.refresh_field("items");
    }
});
```

### Script 4: Custom Button "Return Books" (Client Script + Server)

```javascript
// Client Script — thêm vao library_transaction.js

frappe.ui.form.on("Library Transaction", {
    refresh(frm) {
        // Chi hiện khi Borrow đã Submit và chưa Return het
        if (frm.doc.docstatus === 1
            && frm.doc.transaction_type === "Borrow") {

            // Check nếu con sach chưa tra
            let unreturned = (frm.doc.items || []).filter(
                row => row.status !== "Returned"
            );

            if (unreturned.length > 0) {
                frm.add_custom_button(__("Return All Books"), function() {
                    frappe.confirm(
                        __(`Return ${unreturned.length} book(s)?`),
                        function() {
                            frappe.call({
                                method: "frappe_learn.api.return_books",
                                args: {
                                    transaction_name: frm.doc.name
                                },
                                freeze: true,
                                freeze_message: __("Processing returns..."),
                                callback: function(r) {
                                    if (!r.exc) {
                                        frappe.show_alert({
                                            message: __("Books returned successfully"),
                                            indicator: "green"
                                        });
                                        frm.reload_doc();
                                    }
                                }
                            });
                        }
                    );
                }).addClass("btn-primary");
            }
        }
    }
});
```

```python
# Server side — frappe_learn/api.py

import frappe

@frappe.whitelist()
def return_books(transaction_name):
    """Mark all books in a Borrow transaction as returned"""
    txn = frappe.get_doc("Library Transaction", transaction_name)

    if txn.docstatus != 1:
        frappe.throw("Transaction must be submitted")

    if txn.transaction_type != "Borrow":
        frappe.throw("Can only return books from Borrow transactions")

    today = frappe.utils.nowdate()
    returned_count = 0

    for item in txn.items:
        if item.status != "Returned":
            # Update transaction item
            frappe.db.set_value("Library Transaction Item", item.name, {
                "status": "Returned",
                "return_date": today
            })

            # Update book status
            frappe.db.set_value("Library Book", item.book, "status", "Available")
            returned_count += 1

    frappe.db.commit()
    return {"returned": returned_count}
```

### Script 5: API — Book Availability Check (Server Script)

```python
# Server Script Type: API
# API Method: check_book_availability
# URL: /api/method/check_book_availability

book_name = frappe.form_dict.get("book")

if not book_name:
    frappe.throw("Book parameter is required")

if not frappe.db.exists("Library Book", book_name):
    frappe.throw(f"Book {book_name} not found")

book = frappe.get_doc("Library Book", book_name)

# Tìm transaction hiện tại nếu dang borrowed
current_borrower = None
if book.status == "Borrowed":
    txn = frappe.db.sql("""
        SELECT lt.member, lt.member_name, lti.due_date
        FROM `tabLibrary Transaction` lt
        JOIN `tabLibrary Transaction Item` lti ON lti.parent = lt.name
        WHERE lti.book = %s
          AND lti.status = 'Borrowed'
          AND lt.docstatus = 1
        ORDER BY lt.creation DESC
        LIMIT 1
    """, book_name, as_dict=True)

    if txn:
        current_borrower = {
            "member": txn[0].member,
            "member_name": txn[0].member_name,
            "due_date": str(txn[0].due_date)
        }

frappe.response["message"] = {
    "book": book_name,
    "title": book.title,
    "author": book.author,
    "status": book.status,
    "available": book.status == "Available",
    "current_borrower": current_borrower
}
```

```javascript
// Test từ browser console:
frappe.call({
    method: "check_book_availability",
    args: { book: "BOOK-0001" },
    callback: function(r) {
        console.log(r.message);
        // {book: "BOOK-0001", title: "Clean Code", available: true, ...}
    }
});
```

#### Kiểm tra hoàn thành

- [ ] Script 1: ISBN validation hoat dòng — nhập ISBN sai → báo lỗi
- [ ] Script 2: Late fee tự động tính khi tra sach tre
- [ ] Script 3: Book dropdown chi hiện sach Available khi Borrow
- [ ] Script 4: Nut "Return All Books" hiện và hoat dong
- [ ] Script 5: API `/api/method/check_book_availability` trả về JSON

> **Tiếp theo:** Module 4 sẽ chuyen sang Controllers — viết business logic trong `.py` files, hooks.py doc_events, và scheduled jobs.

### Skill References

- **DEEP DIVE:** Xem skill `dcnet_quality` -> `syntax/` cho TẤT CẢ 8 syntax skill files
- **DEEP DIVE:** Xem skill `dcnet_quality` -> `errors/` cho error handling trong mọi context
- **DEEP DIVE:** Xem skill `frappe` -> `test_examples/` để hiểu cach test scripts
