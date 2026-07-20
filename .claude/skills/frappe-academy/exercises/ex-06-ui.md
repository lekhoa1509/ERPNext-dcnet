# Module 6: Desk UI / Giao diện Desk
# Mô-đun 6: Tùy chỉnh giao diện người dùng Desk

> **Container:** `devcontainer-frappe-1`
> **Bench path:** `/workspace/development/frappe-bench`
> **Site:** `flow.local`
> **App path:** `/workspace/development/frappe-bench/apps/frappe_learn`
> **Prefix command:** `docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local ..."`

---

## Prerequisites / Yêu cầu trước khi bắt đầu

- Completed Modules 1-5 (frappe_learn app with Book, Library Member, Library Transaction DocTypes)
- API module (api.py) from Module 5 working
- Sample data: at least 10 Books, 5 Members, 10 Transactions
- Đã hoàn thành Module 1-5 (app frappe_learn với các DocType và api.py)
- Dữ liệu mẫu: ít nhất 10 Book, 5 Member, 10 Transaction

---

## Exercise 6.1: Form Customization / Tùy chỉnh Form

### Objective / Mục tiêu
Add a dashboard section to the Book form showing total borrows and current borrower information using Client Script.

Thêm phần dashboard vào form Book hiển thị tổng số lần mượn và thông tin người đang mượn bằng Client Script.

### Instructions / Hướng dẫn

**Step 1:** Create a Client Script for the Book DocType.

File: `frappe_learn/frappe_learn/library/doctype/book/book.js`

If you created the DocType via the UI, this file may already exist. If not, create it.

```javascript
frappe.ui.form.on('Book', {
    refresh: function(frm) {
        // Add dashboard section
        if (!frm.is_new()) {
            frm.dashboard.add_section(
                frappe.render_template('book_dashboard', {
                    loading: true
                }),
                __("Borrowing Info")
            );

            // Fetch borrowing stats
            frappe.call({
                method: 'frappe.client.get_count',
                args: {
                    doctype: 'Library Transaction',
                    filters: {
                        book: frm.doc.name,
                        type: 'Borrow',
                        docstatus: 1
                    }
                },
                callback: function(r) {
                    let total_borrows = r.message || 0;

                    // Get current borrower if status is Borrowed
                    if (frm.doc.status === 'Borrowed') {
                        frappe.call({
                            method: 'frappe.client.get_list',
                            args: {
                                doctype: 'Library Transaction',
                                filters: {
                                    book: frm.doc.name,
                                    type: 'Borrow',
                                    docstatus: 1
                                },
                                fields: ['library_member', 'transaction_date'],
                                order_by: 'transaction_date desc',
                                limit_page_length: 1
                            },
                            callback: function(r2) {
                                let borrower = r2.message && r2.message[0];
                                update_dashboard(frm, total_borrows, borrower);
                            }
                        });
                    } else {
                        update_dashboard(frm, total_borrows, null);
                    }
                }
            });

            // Add custom button to borrow
            if (frm.doc.status === 'Available') {
                frm.add_custom_button(__('Borrow'), function() {
                    show_borrow_dialog(frm);
                }, __('Actions'));
            }

            // Add custom button to return
            if (frm.doc.status === 'Borrowed') {
                frm.add_custom_button(__('Return'), function() {
                    return_book(frm);
                }, __('Actions'));
            }
        }
    }
});

function update_dashboard(frm, total_borrows, borrower) {
    let html = `
        <div class="row">
            <div class="col-sm-4">
                <div class="stat-label">${__('Total Borrows')}</div>
                <div class="stat-value text-primary">${total_borrows}</div>
            </div>
            <div class="col-sm-4">
                <div class="stat-label">${__('Current Status')}</div>
                <div class="stat-value ${frm.doc.status === 'Available' ? 'text-success' : 'text-danger'}">
                    ${__(frm.doc.status)}
                </div>
            </div>
            <div class="col-sm-4">
                <div class="stat-label">${__('Current Borrower')}</div>
                <div class="stat-value">
                    ${borrower
                        ? `<a href="/app/library-member/${borrower.library_member}">${borrower.library_member}</a>
                           <br><small class="text-muted">${__('Since')} ${frappe.datetime.str_to_user(borrower.transaction_date)}</small>`
                        : '<span class="text-muted">—</span>'}
                </div>
            </div>
        </div>
    `;

    frm.dashboard.set_headline_alert(html);
}

function show_borrow_dialog(frm) {
    let d = new frappe.ui.Dialog({
        title: __('Borrow Book'),
        fields: [
            {
                fieldname: 'library_member',
                fieldtype: 'Link',
                label: __('Library Member'),
                options: 'Library Member',
                reqd: 1
            }
        ],
        primary_action_label: __('Borrow'),
        primary_action: function(values) {
            frappe.call({
                method: 'frappe_learn.frappe_learn.api.borrow_book',
                args: {
                    book: frm.doc.name,
                    member: values.library_member
                },
                callback: function(r) {
                    if (r.message) {
                        frappe.show_alert({
                            message: __('Book borrowed successfully'),
                            indicator: 'green'
                        });
                        frm.reload_doc();
                    }
                }
            });
            d.hide();
        }
    });
    d.show();
}

function return_book(frm) {
    frappe.confirm(
        __('Are you sure you want to return this book?'),
        function() {
            // Create return transaction
            frappe.call({
                method: 'frappe.client.insert',
                args: {
                    doc: {
                        doctype: 'Library Transaction',
                        book: frm.doc.name,
                        type: 'Return',
                        transaction_date: frappe.datetime.get_today()
                    }
                },
                callback: function(r) {
                    if (r.message) {
                        // Update book status
                        frappe.call({
                            method: 'frappe.client.set_value',
                            args: {
                                doctype: 'Book',
                                name: frm.doc.name,
                                fieldname: 'status',
                                value: 'Available'
                            },
                            callback: function() {
                                frappe.show_alert({
                                    message: __('Book returned successfully'),
                                    indicator: 'green'
                                });
                                frm.reload_doc();
                            }
                        });
                    }
                }
            });
        }
    );
}
```

**Step 2:** Add CSS styling (optional but recommended)

Create file: `frappe_learn/frappe_learn/public/css/library.css`

```css
.stat-label {
    font-size: 11px;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 4px;
}

.stat-value {
    font-size: 18px;
    font-weight: 600;
}
```

Add to `frappe_learn/hooks.py`:

```python
app_include_css = "/assets/frappe_learn/css/library.css"
```

**Step 3:** Build and test

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench build --app frappe_learn && bench --site flow.local clear-cache"
```

### Expected Output / Kết quả mong đợi

- Book form shows a dashboard section at the top with:
  - Total Borrows count
  - Current Status (color-coded: green for Available, red for Borrowed)
  - Current Borrower (with link to member, if borrowed)
- "Borrow" button appears when status is Available
- "Return" button appears when status is Borrowed
- Borrow dialog lets you select a Library Member

### Verification / Kiểm tra

1. Open browser: `http://localhost:8080/app/book/{book_name}`
2. Verify dashboard section is visible at the top of the form
3. Click "Actions > Borrow" — select a member — verify status changes to "Borrowed"
4. Verify "Actions > Return" appears — click it — verify status changes back to "Available"

```bash
# Verify JS file exists
docker exec devcontainer-frappe-1 bash -c "ls -la /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/library/doctype/book/book.js"
```

<details>
<summary>Hint 1: frm.dashboard methods / Gợi ý 1: Các phương thức frm.dashboard</summary>

Key dashboard methods:
- `frm.dashboard.add_section(html, label)` — Add a custom section
- `frm.dashboard.set_headline_alert(html)` — Set alert banner
- `frm.dashboard.add_indicator(label, color)` — Add status indicator
- `frm.dashboard.add_comment(text, alert_class)` — Add comment

Các phương thức dashboard quan trọng: add_section, set_headline_alert, add_indicator, add_comment.
</details>

<details>
<summary>Hint 2: Custom buttons / Gợi ý 2: Nút tùy chỉnh</summary>

Custom button patterns:
```javascript
// Simple button
frm.add_custom_button(__('Do Something'), function() { ... });

// Button in group
frm.add_custom_button(__('Action'), function() { ... }, __('Group Name'));

// Primary button (blue)
frm.page.set_primary_action(__('Submit'), function() { ... });

// Remove button
frm.remove_custom_button(__('Do Something'));
```

Các mẫu nút tùy chỉnh: nút đơn, nút trong nhóm, nút chính (xanh), xóa nút.
</details>

---

## Exercise 6.2: List View Customization / Tùy chỉnh List View

### Objective / Mục tiêu
Customize the Book list view with color indicators based on status: green for Available, red for Borrowed, gray for Lost.

Tùy chỉnh Book list view với chỉ báo màu sắc theo trạng thái: xanh cho Available, đỏ cho Borrowed, xám cho Lost.

### Instructions / Hướng dẫn

**Step 1:** Create the list view customization file.

File: `frappe_learn/frappe_learn/library/doctype/book/book_list.js`

```javascript
frappe.listview_settings['Book'] = {
    // Add status indicator colors
    get_indicator: function(doc) {
        // Returns [label, color, field_name, field_value]
        const status_map = {
            'Available': [__('Available'), 'green', 'status,=,Available'],
            'Borrowed': [__('Borrowed'), 'red', 'status,=,Borrowed'],
            'Lost': [__('Lost'), 'gray', 'status,=,Lost'],
            'Damaged': [__('Damaged'), 'orange', 'status,=,Damaged']
        };
        return status_map[doc.status] || [__(doc.status), 'blue', `status,=,${doc.status}`];
    },

    // Add extra columns to list
    add_fields: ['status', 'author', 'isbn'],

    // Set default filters
    filters: [['status', '!=', 'Lost']],

    // Customize row button
    button: {
        show: function(doc) {
            return doc.status === 'Available';
        },
        get_label: function() {
            return __('Quick Borrow');
        },
        get_description: function(doc) {
            return __('Borrow {0}', [doc.title || doc.name]);
        },
        action: function(doc) {
            frappe.prompt(
                {
                    fieldname: 'library_member',
                    fieldtype: 'Link',
                    label: __('Library Member'),
                    options: 'Library Member',
                    reqd: 1
                },
                function(values) {
                    frappe.call({
                        method: 'frappe_learn.frappe_learn.api.borrow_book',
                        args: {
                            book: doc.name,
                            member: values.library_member
                        },
                        callback: function(r) {
                            if (r.message) {
                                frappe.show_alert({
                                    message: __('Book borrowed successfully'),
                                    indicator: 'green'
                                });
                                cur_list.refresh();
                            }
                        }
                    });
                },
                __('Quick Borrow'),
                __('Borrow')
            );
        }
    },

    // Format row data
    formatters: {
        title: function(value, field, doc) {
            if (doc.status === 'Borrowed') {
                return `<span class="text-danger font-weight-bold">${value}</span>`;
            }
            return value;
        }
    },

    // Hide sidebar?
    hide_name_column: true
};
```

**Step 2:** Build assets

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench build --app frappe_learn && bench --site flow.local clear-cache"
```

### Expected Output / Kết quả mong đợi

- Book list shows colored status indicators:
  - Green dot + "Available" for available books
  - Red dot + "Borrowed" for borrowed books
  - Gray dot + "Lost" for lost books
  - Orange dot + "Damaged" for damaged books
- "Quick Borrow" button appears for Available books
- Borrowed book titles appear in bold red
- Lost books are filtered out by default

### Verification / Kiểm tra

1. Open browser: `http://localhost:8080/app/book`
2. Verify colored indicators next to each book
3. Verify "Quick Borrow" button on Available books
4. Remove the "Lost" filter — verify Lost books appear with gray indicator

```bash
# Verify list JS file exists
docker exec devcontainer-frappe-1 bash -c "ls -la /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/library/doctype/book/book_list.js"
```

<details>
<summary>Hint: get_indicator return format / Gợi ý: Định dạng trả về của get_indicator</summary>

The `get_indicator` function must return an array of 3 elements:
```javascript
[label, color, filter_string]
```

Available colors: `green`, `blue`, `orange`, `red`, `gray`, `yellow`, `purple`, `pink`, `cyan`.

The `filter_string` format is `"field,operator,value"` — when user clicks the indicator, it filters the list by that condition.

Hàm `get_indicator` phải trả về mảng 3 phần tử: [nhãn, màu, chuỗi_bộ_lọc].
Các màu có sẵn: green, blue, orange, red, gray, yellow, purple, pink, cyan.
</details>

---

## Exercise 6.3: Script Report / Báo cáo Script

### Objective / Mục tiêu
Create a "Library Overdue Books" Script Report showing: book title, member name, borrow date, due date, and days overdue. With a date range filter.

Tạo báo cáo Script "Library Overdue Books" hiển thị: tên sách, tên thành viên, ngày mượn, ngày hết hạn, số ngày quá hạn. Với bộ lọc khoảng ngày.

### Instructions / Hướng dẫn

**Step 1:** Create the report directory structure

```bash
docker exec devcontainer-frappe-1 bash -c "mkdir -p /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/library/report/library_overdue_books"
```

**Step 2:** Create `__init__.py`

File: `frappe_learn/frappe_learn/library/report/library_overdue_books/__init__.py`

```python
# Empty file
```

**Step 3:** Create the report JSON definition

File: `frappe_learn/frappe_learn/library/report/library_overdue_books/library_overdue_books.json`

```json
{
    "add_total_row": 0,
    "columns": [],
    "creation": "2026-03-17 10:00:00.000000",
    "disabled": 0,
    "docstatus": 0,
    "doctype": "Report",
    "filters": [],
    "is_standard": "Yes",
    "modified": "2026-03-17 10:00:00.000000",
    "modified_by": "Administrator",
    "module": "Library",
    "name": "Library Overdue Books",
    "owner": "Administrator",
    "prepared_report": 0,
    "ref_doctype": "Library Transaction",
    "report_name": "Library Overdue Books",
    "report_type": "Script Report",
    "roles": [
        {
            "role": "System Manager"
        }
    ]
}
```

**Step 4:** Create the Python report logic

File: `frappe_learn/frappe_learn/library/report/library_overdue_books/library_overdue_books.py`

```python
# Copyright (c) 2026, DCNET and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, date_diff, today


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    message = get_summary(data)
    chart = get_chart(data)
    return columns, data, message, chart


def get_columns():
    return [
        {
            "label": _("Book"),
            "fieldname": "book",
            "fieldtype": "Link",
            "options": "Book",
            "width": 150
        },
        {
            "label": _("Book Title"),
            "fieldname": "book_title",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("Member"),
            "fieldname": "library_member",
            "fieldtype": "Link",
            "options": "Library Member",
            "width": 150
        },
        {
            "label": _("Member Name"),
            "fieldname": "member_name",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Borrow Date"),
            "fieldname": "borrow_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": _("Due Date"),
            "fieldname": "due_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": _("Days Overdue"),
            "fieldname": "days_overdue",
            "fieldtype": "Int",
            "width": 120
        },
        {
            "label": _("Status"),
            "fieldname": "overdue_status",
            "fieldtype": "Data",
            "width": 100
        }
    ]


def get_data(filters):
    conditions = ""
    values = {}

    if filters and filters.get("from_date"):
        conditions += " AND t.transaction_date >= %(from_date)s"
        values["from_date"] = filters["from_date"]

    if filters and filters.get("to_date"):
        conditions += " AND t.transaction_date <= %(to_date)s"
        values["to_date"] = filters["to_date"]

    if filters and filters.get("library_member"):
        conditions += " AND t.library_member = %(library_member)s"
        values["library_member"] = filters["library_member"]

    # Default loan period: 14 days
    loan_period = filters.get("loan_period", 14) if filters else 14

    data = frappe.db.sql("""
        SELECT
            t.book,
            b.title as book_title,
            t.library_member,
            m.full_name as member_name,
            t.transaction_date as borrow_date,
            DATE_ADD(t.transaction_date, INTERVAL %(loan_period)s DAY) as due_date,
            DATEDIFF(CURDATE(), DATE_ADD(t.transaction_date, INTERVAL %(loan_period)s DAY)) as days_overdue
        FROM `tabLibrary Transaction` t
        JOIN `tabBook` b ON t.book = b.name
        JOIN `tabLibrary Member` m ON t.library_member = m.name
        WHERE t.type = 'Borrow'
            AND t.docstatus = 1
            AND b.status = 'Borrowed'
            AND DATEDIFF(CURDATE(), DATE_ADD(t.transaction_date, INTERVAL %(loan_period)s DAY)) > 0
            {conditions}
        ORDER BY days_overdue DESC
    """.format(conditions=conditions), {**values, "loan_period": loan_period}, as_dict=True)

    # Add status classification
    for row in data:
        if row.days_overdue > 30:
            row["overdue_status"] = "Critical"
        elif row.days_overdue > 14:
            row["overdue_status"] = "Warning"
        else:
            row["overdue_status"] = "Overdue"

    return data


def get_summary(data):
    if not data:
        return _("No overdue books found. All books are returned on time!")

    total = len(data)
    critical = len([d for d in data if d.get("overdue_status") == "Critical"])
    warning = len([d for d in data if d.get("overdue_status") == "Warning"])
    max_days = max(d.get("days_overdue", 0) for d in data) if data else 0

    return _(
        "<b>{0}</b> overdue books. "
        "<span class='text-danger'>{1} critical</span>, "
        "<span class='text-warning'>{2} warning</span>. "
        "Longest overdue: <b>{3} days</b>."
    ).format(total, critical, warning, max_days)


def get_chart(data):
    if not data:
        return None

    # Group by overdue ranges
    ranges = {"1-7 days": 0, "8-14 days": 0, "15-30 days": 0, "30+ days": 0}
    for d in data:
        days = d.get("days_overdue", 0)
        if days <= 7:
            ranges["1-7 days"] += 1
        elif days <= 14:
            ranges["8-14 days"] += 1
        elif days <= 30:
            ranges["15-30 days"] += 1
        else:
            ranges["30+ days"] += 1

    return {
        "data": {
            "labels": list(ranges.keys()),
            "datasets": [
                {
                    "name": _("Overdue Books"),
                    "values": list(ranges.values())
                }
            ]
        },
        "type": "bar",
        "colors": ["#ff5858"]
    }
```

**Step 5:** Create the JavaScript filter file

File: `frappe_learn/frappe_learn/library/report/library_overdue_books/library_overdue_books.js`

```javascript
frappe.query_reports["Library Overdue Books"] = {
    filters: [
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            default: frappe.datetime.add_months(frappe.datetime.get_today(), -3),
            reqd: 0
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            default: frappe.datetime.get_today(),
            reqd: 0
        },
        {
            fieldname: "library_member",
            label: __("Library Member"),
            fieldtype: "Link",
            options: "Library Member",
            reqd: 0
        },
        {
            fieldname: "loan_period",
            label: __("Loan Period (days)"),
            fieldtype: "Int",
            default: 14,
            reqd: 0
        }
    ],

    formatter: function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);

        if (column.fieldname === "days_overdue" && data && data.days_overdue > 30) {
            value = `<span style="color: red; font-weight: bold;">${value}</span>`;
        }
        if (column.fieldname === "overdue_status") {
            const colors = {
                "Critical": "red",
                "Warning": "orange",
                "Overdue": "yellow"
            };
            const color = colors[data.overdue_status] || "gray";
            value = `<span class="indicator-pill ${color}">${value}</span>`;
        }

        return value;
    }
};
```

**Step 6:** Build and migrate

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench build --app frappe_learn && bench --site flow.local migrate && bench --site flow.local clear-cache"
```

### Expected Output / Kết quả mong đợi

- Report accessible at `http://localhost:8080/app/query-report/Library Overdue Books`
- Shows table with: Book, Book Title, Member, Member Name, Borrow Date, Due Date, Days Overdue, Status
- Chart shows bar graph of overdue books grouped by range
- Summary message at the top with totals
- Days > 30 shown in bold red
- Status shown as colored pills (red=Critical, orange=Warning, yellow=Overdue)

### Verification / Kiểm tra

```bash
# Verify report files exist
docker exec devcontainer-frappe-1 bash -c "ls -la /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/library/report/library_overdue_books/"

# Test report from bench
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local execute frappe_learn.frappe_learn.library.report.library_overdue_books.library_overdue_books.execute --args '[{\"loan_period\": 14}]'"
```

<details>
<summary>Hint 1: Report return format / Gợi ý 1: Định dạng trả về báo cáo</summary>

Script Report `execute()` returns a tuple of 4 elements:
```python
return columns, data, message, chart
```

- `columns`: list of dicts with label, fieldname, fieldtype, width, options
- `data`: list of dicts (each dict = one row)
- `message`: HTML string shown above the table
- `chart`: dict with `{data: {labels, datasets}, type, colors}`

Hàm `execute()` trả về tuple 4 phần tử: columns, data, message, chart.
</details>

<details>
<summary>Hint 2: Common report issues / Gợi ý 2: Lỗi thường gặp với báo cáo</summary>

1. **Report not appearing?** Run `bench --site flow.local migrate` — the JSON file must be imported
2. **"Report not found"?** Check the JSON `name` matches the folder name (snake_case)
3. **No data?** Test the SQL query directly in bench console first
4. **Chart not showing?** Ensure `type` is one of: `bar`, `line`, `pie`, `donut`, `percentage`

Báo cáo không hiện? Chạy migrate. Không tìm thấy? Kiểm tra tên trong JSON. Không có dữ liệu? Test SQL trước.
</details>

---

## Exercise 6.4: Number Cards / Thẻ số liệu

### Objective / Mục tiêu
Create 3 Number Cards: Total Books, Active Members, Books Currently Borrowed. Display them on the Library workspace.

Tạo 3 Number Card: Tổng số sách, Thành viên đang hoạt động, Sách đang cho mượn. Hiển thị trên workspace Library.

### Instructions / Hướng dẫn

**Step 1:** Create Number Card fixtures directory

```bash
docker exec devcontainer-frappe-1 bash -c "mkdir -p /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/library/number_card/total_books"
docker exec devcontainer-frappe-1 bash -c "mkdir -p /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/library/number_card/active_library_members"
docker exec devcontainer-frappe-1 bash -c "mkdir -p /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/library/number_card/books_currently_borrowed"
```

**Step 2:** Create Number Card JSON files

File: `frappe_learn/frappe_learn/library/number_card/total_books/total_books.json`

```json
{
    "name": "Total Books",
    "doctype": "Number Card",
    "document_type": "Book",
    "creation": "2026-03-17 10:00:00.000000",
    "modified": "2026-03-17 10:00:00.000000",
    "modified_by": "Administrator",
    "owner": "Administrator",
    "module": "Library",
    "label": "Total Books",
    "function": "Count",
    "aggregate_function_based_on": "",
    "filters_json": "[]",
    "is_standard": 1,
    "is_public": 1,
    "show_percentage_stats": 0,
    "stats_time_interval": "Monthly",
    "color": "#449CF0",
    "type": "Document Type"
}
```

File: `frappe_learn/frappe_learn/library/number_card/active_library_members/active_library_members.json`

```json
{
    "name": "Active Library Members",
    "doctype": "Number Card",
    "document_type": "Library Member",
    "creation": "2026-03-17 10:00:00.000000",
    "modified": "2026-03-17 10:00:00.000000",
    "modified_by": "Administrator",
    "owner": "Administrator",
    "module": "Library",
    "label": "Active Members",
    "function": "Count",
    "aggregate_function_based_on": "",
    "filters_json": "[]",
    "is_standard": 1,
    "is_public": 1,
    "show_percentage_stats": 0,
    "stats_time_interval": "Monthly",
    "color": "#29CD42",
    "type": "Document Type"
}
```

File: `frappe_learn/frappe_learn/library/number_card/books_currently_borrowed/books_currently_borrowed.json`

```json
{
    "name": "Books Currently Borrowed",
    "doctype": "Number Card",
    "document_type": "Book",
    "creation": "2026-03-17 10:00:00.000000",
    "modified": "2026-03-17 10:00:00.000000",
    "modified_by": "Administrator",
    "owner": "Administrator",
    "module": "Library",
    "label": "Books Currently Borrowed",
    "function": "Count",
    "aggregate_function_based_on": "",
    "filters_json": "[[\"Book\",\"status\",\"=\",\"Borrowed\"]]",
    "is_standard": 1,
    "is_public": 1,
    "show_percentage_stats": 0,
    "stats_time_interval": "Monthly",
    "color": "#FF5858",
    "type": "Document Type"
}
```

**Step 3:** Migrate to create the Number Cards

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local migrate && bench --site flow.local clear-cache"
```

### Expected Output / Kết quả mong đợi

- 3 Number Cards created and visible at:
  - `http://localhost:8080/app/number-card/Total Books`
  - `http://localhost:8080/app/number-card/Active Library Members`
  - `http://localhost:8080/app/number-card/Books Currently Borrowed`
- Each card shows the correct count with appropriate color
- Blue for Total Books, Green for Active Members, Red for Borrowed

### Verification / Kiểm tra

```bash
# Check Number Cards exist
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local execute frappe.client.get_list --args '{\"doctype\": \"Number Card\", \"filters\": {\"module\": \"Library\"}, \"fields\": [\"name\", \"label\"]}'"

# Verify count values
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local execute frappe.client.get_count --args '{\"doctype\": \"Book\"}'"
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local execute frappe.client.get_count --args '{\"doctype\": \"Book\", \"filters\": {\"status\": \"Borrowed\"}}'"
```

<details>
<summary>Hint: Number Card types / Gợi ý: Các loại Number Card</summary>

Frappe supports 3 types of Number Cards:

1. **Document Type** — counts/sums from a DocType (used above)
2. **Report** — gets value from a Script Report
3. **Custom** — calls a whitelisted method

For Custom type:
```json
{
    "type": "Custom",
    "method": "frappe_learn.frappe_learn.api.get_book_availability",
    "filters_json": "[]"
}
```

The custom method must return `{"value": number, "fieldtype": "Currency/Int/etc"}`.

Frappe hỗ trợ 3 loại Number Card: Document Type, Report, Custom. Loại Custom gọi phương thức whitelist.
</details>

---

## Exercise 6.5: Library Workspace / Workspace Thư viện

### Objective / Mục tiêu
Create a complete "Library" Workspace with: number cards row, overdue report chart, shortcuts to Book/Member/Transaction DocTypes.

Tạo Workspace "Library" hoàn chỉnh với: hàng number card, biểu đồ báo cáo quá hạn, phím tắt đến các DocType Book/Member/Transaction.

### Instructions / Hướng dẫn

**Step 1:** Create workspace directory

```bash
docker exec devcontainer-frappe-1 bash -c "mkdir -p /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/library/workspace/library"
```

**Step 2:** Create the workspace JSON

File: `frappe_learn/frappe_learn/library/workspace/library/library.json`

```json
{
    "name": "Library",
    "doctype": "Workspace",
    "creation": "2026-03-17 10:00:00.000000",
    "modified": "2026-03-17 10:00:00.000000",
    "modified_by": "Administrator",
    "owner": "Administrator",
    "module": "Library",
    "label": "Library",
    "title": "Library Management",
    "icon": "book",
    "is_standard": 1,
    "public": 1,
    "for_user": "",
    "sequence_id": 10,
    "content": "[{\"id\":\"nc_row\",\"type\":\"number_card\",\"data\":{\"number_card_name\":\"Total Books\",\"col\":4}},{\"id\":\"nc_row2\",\"type\":\"number_card\",\"data\":{\"number_card_name\":\"Active Library Members\",\"col\":4}},{\"id\":\"nc_row3\",\"type\":\"number_card\",\"data\":{\"number_card_name\":\"Books Currently Borrowed\",\"col\":4}},{\"id\":\"spacer1\",\"type\":\"spacer\",\"data\":{\"col\":12}},{\"id\":\"header1\",\"type\":\"header\",\"data\":{\"text\":\"<span class=\\\"h4\\\">Quick Access</span>\",\"col\":12,\"level\":4}},{\"id\":\"shortcut1\",\"type\":\"shortcut\",\"data\":{\"shortcut_name\":\"Book\",\"col\":4}},{\"id\":\"shortcut2\",\"type\":\"shortcut\",\"data\":{\"shortcut_name\":\"Library Member\",\"col\":4}},{\"id\":\"shortcut3\",\"type\":\"shortcut\",\"data\":{\"shortcut_name\":\"Library Transaction\",\"col\":4}},{\"id\":\"spacer2\",\"type\":\"spacer\",\"data\":{\"col\":12}},{\"id\":\"header2\",\"type\":\"header\",\"data\":{\"text\":\"<span class=\\\"h4\\\">Reports</span>\",\"col\":12,\"level\":4}},{\"id\":\"shortcut4\",\"type\":\"shortcut\",\"data\":{\"shortcut_name\":\"Library Overdue Books\",\"col\":6}}]",
    "links": [
        {
            "label": "Catalog",
            "type": "Card Break",
            "icon": "book"
        },
        {
            "label": "Book",
            "type": "Link",
            "link_type": "DocType",
            "link_to": "Book",
            "description": "Manage library books catalog"
        },
        {
            "label": "Library Member",
            "type": "Link",
            "link_type": "DocType",
            "link_to": "Library Member",
            "description": "Manage library members"
        },
        {
            "label": "Transactions",
            "type": "Card Break",
            "icon": "list"
        },
        {
            "label": "Library Transaction",
            "type": "Link",
            "link_type": "DocType",
            "link_to": "Library Transaction",
            "description": "Borrow and return books"
        },
        {
            "label": "Reports",
            "type": "Card Break",
            "icon": "chart-line"
        },
        {
            "label": "Library Overdue Books",
            "type": "Link",
            "link_type": "Report",
            "link_to": "Library Overdue Books",
            "is_query_report": 1,
            "description": "View overdue books report"
        }
    ],
    "shortcuts": [
        {
            "label": "Book",
            "type": "DocType",
            "link_to": "Book",
            "color": "#449CF0",
            "stats_filter": "",
            "format": "{} Books"
        },
        {
            "label": "Library Member",
            "type": "DocType",
            "link_to": "Library Member",
            "color": "#29CD42",
            "stats_filter": "",
            "format": "{} Members"
        },
        {
            "label": "Library Transaction",
            "type": "DocType",
            "link_to": "Library Transaction",
            "color": "#ECAD4B",
            "stats_filter": "",
            "format": "{} Transactions"
        },
        {
            "label": "Library Overdue Books",
            "type": "Report",
            "link_to": "Library Overdue Books",
            "color": "#FF5858",
            "format": "Overdue Report"
        }
    ],
    "number_cards": [
        {
            "number_card_name": "Total Books"
        },
        {
            "number_card_name": "Active Library Members"
        },
        {
            "number_card_name": "Books Currently Borrowed"
        }
    ]
}
```

**Step 3:** Migrate and build

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench build --app frappe_learn && bench --site flow.local migrate && bench --site flow.local clear-cache"
```

**Step 4:** Verify in browser

Navigate to: `http://localhost:8080/app/library`

### Expected Output / Kết quả mong đợi

The Library workspace should display:
1. **Top row:** 3 Number Cards side by side
   - Total Books (blue)
   - Active Members (green)
   - Books Currently Borrowed (red)
2. **Quick Access section:** 3 shortcuts
   - Book (with count)
   - Library Member (with count)
   - Library Transaction (with count)
3. **Reports section:** Shortcut to Overdue Books Report
4. **Left sidebar:** Card links organized by category (Catalog, Transactions, Reports)

### Verification / Kiểm tra

```bash
# Verify workspace exists
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local execute frappe.client.get_list --args '{\"doctype\": \"Workspace\", \"filters\": {\"module\": \"Library\"}, \"fields\": [\"name\", \"label\"]}'"

# Verify workspace file exists
docker exec devcontainer-frappe-1 bash -c "ls -la /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/library/workspace/library/library.json"
```

<details>
<summary>Hint 1: Workspace content blocks / Gợi ý 1: Các khối nội dung workspace</summary>

Workspace `content` is a JSON string of blocks. Available block types:

| Type | Description |
|------|-------------|
| `number_card` | Number Card widget |
| `chart` | Dashboard Chart widget |
| `shortcut` | Quick link to DocType/Report/Page |
| `header` | Section header (h3/h4/h5) |
| `spacer` | Empty space between sections |
| `card` | Custom card with HTML content |
| `onboarding` | Onboarding card for new users |

Each block has `id`, `type`, and `data` (with `col` for column width out of 12).

Workspace `content` là chuỗi JSON của các khối. Các loại khối: number_card, chart, shortcut, header, spacer, card.
</details>

<details>
<summary>Hint 2: Workspace not showing? / Gợi ý 2: Workspace không hiển thị?</summary>

Common issues:
1. **Not visible in sidebar?** Check `public: 1` in JSON
2. **Module not listed?** Ensure "Library" is in `modules.txt`
3. **After migrate still not showing?** Try:
   ```bash
   bench --site flow.local clear-cache
   bench --site flow.local clear-website-cache
   ```
4. **Icon not showing?** Use valid Frappe icon names (check `/assets/frappe/icons/`)

Workspace không hiện? Kiểm tra `public: 1`, "Library" trong modules.txt, và chạy clear-cache.
</details>

---

## Summary / Tóm tắt

| Exercise | Key Concept | Files Created |
|----------|-------------|---------------|
| 6.1 | Form customization + Client Script | `book.js` |
| 6.2 | List View customization | `book_list.js` |
| 6.3 | Script Report (Python + JS) | `library_overdue_books/` (4 files) |
| 6.4 | Number Cards (JSON fixtures) | 3 number card JSON files |
| 6.5 | Workspace | `workspace/library/library.json` |

**Next:** Module 7 — Advanced Topics (Permissions, Print Format, Testing, Fixtures)
