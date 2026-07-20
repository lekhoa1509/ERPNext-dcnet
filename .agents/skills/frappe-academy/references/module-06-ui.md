# Module 6: Desk UI & frappe-ui

> **Mục tiêu / Objective:** Tùy chỉnh giao diện Frappe Desk — Form, List View, Reports, Dashboard, Workspace.
> **Yêu cầu / Prerequisites:** Module 1-5 (DocType, Controllers, Hooks, API)
> **Thời lượng / Duration:** ~8 giờ thực hành

---

## L6.1: Form Customization

### Tổng quan / Overview

Form là giao diện chính để xem và chính sửa document trong Frappe Desk. Client Script cho phép tùy chỉnh form mà không cần sửa source code của DocType goc. Ban có thể thêm buttons, an/hiện fields, thiết lập dependencies, và tùy chỉnh sidebar — tất cả bang JavaScript chạy trên browser.

### Khái niệm chính / Key Concepts

#### 1. Custom Buttons

```javascript
// File: library_management/library_management/doctype/library_book/library_book.js
// Hoac: Client Script (Setup → Client Script)

frappe.ui.form.on("Library Book", {
    refresh: function(frm) {
        // Button đơn giản
        if (frm.doc.status === "Available" && !frm.is_new()) {
            frm.add_custom_button(__("Issue Book"), function() {
                issue_book(frm);
            });
        }

        // Button trong nhóm (dropdown)
        if (frm.doc.status === "Issued") {
            frm.add_custom_button(__("Return"), function() {
                return_book(frm);
            }, __("Actions"));  // "Actions" là ten nhóm

            frm.add_custom_button(__("Extend Due Date"), function() {
                extend_due_date(frm);
            }, __("Actions"));
        }

        // Primary button (xanh, nổi bật)
        if (frm.doc.status === "Available") {
            frm.page.set_primary_action(__("Quick Issue"), function() {
                quick_issue_dialog(frm);
            });
        }

        // Secondary button
        frm.page.set_secondary_action(__("Print Label"), function() {
            print_book_label(frm);
        });
    }
});

function issue_book(frm) {
    // Dialog để chọn member
    let d = new frappe.ui.Dialog({
        title: __("Issue Book"),
        fields: [
            {
                label: __("Member"),
                fieldname: "member",
                fieldtype: "Link",
                options: "Library Member",
                reqd: 1,
                get_query: function() {
                    return {
                        filters: { "status": "Active" }
                    };
                }
            },
            {
                label: __("Due Date"),
                fieldname: "due_date",
                fieldtype: "Date",
                default: frappe.datetime.add_days(frappe.datetime.nowdate(), 14)
            }
        ],
        primary_action_label: __("Issue"),
        primary_action: function(values) {
            frappe.call({
                method: "library_management.api.borrow_book",
                args: {
                    book_name: frm.doc.name,
                    member_name: values.member
                },
                callback: function(r) {
                    if (r.message) {
                        frappe.msgprint(r.message.message);
                        frm.reload_doc();
                    }
                }
            });
            d.hide();
        }
    });
    d.show();
}
```

#### 2. An/hiện Fields và Field Dependencies

```javascript
frappe.ui.form.on("Library Book", {
    refresh: function(frm) {
        // An field bang code
        frm.toggle_display("internal_notes", frappe.user.has_role("Librarian"));

        // An nhiều fields cũng luc
        frm.toggle_display(["isbn", "publisher", "edition"],
            frm.doc.book_type === "Physical"
        );

        // Read-only dua trên trạng thái
        if (frm.doc.status === "Issued") {
            frm.set_df_property("title", "read_only", 1);
            frm.set_df_property("author", "read_only", 1);
        }
    },

    // Field dependency — Khi book_type thay đổi
    book_type: function(frm) {
        // Hiện URL field chi khi là ebook
        frm.toggle_display("ebook_url", frm.doc.book_type === "E-Book");
        frm.toggle_reqd("ebook_url", frm.doc.book_type === "E-Book");

        // Thay đổi options của field
        if (frm.doc.book_type === "E-Book") {
            frm.set_df_property("format", "options", "PDF\nEPUB\nMOBI");
        } else {
            frm.set_df_property("format", "options", "Hardcover\nPaperback");
        }
    },

    // Validate trước khi save
    validate: function(frm) {
        if (frm.doc.book_type === "E-Book" && !frm.doc.ebook_url) {
            frappe.msgprint(__("E-Book URL is required for E-Books"));
            frappe.validated = false;
        }
    }
});
```

#### 3. Form Dashboard

```javascript
frappe.ui.form.on("Library Book", {
    refresh: function(frm) {
        // Thêm info vao dashboard (phia trên form)
        if (!frm.is_new()) {
            // Đếm giao dịch liên quan
            frappe.call({
                method: "frappe.client.get_count",
                args: {
                    doctype: "Library Transaction",
                    filters: { book: frm.doc.name }
                },
                callback: function(r) {
                    if (r.message) {
                        frm.dashboard.add_indicator(
                            __("Total Transactions: {0}", [r.message]),
                            r.message > 10 ? "green" : "blue"
                        );
                    }
                }
            });

            // Thêm comment section custom
            frm.dashboard.add_comment(__("Last borrowed by: {0}",
                [frm.doc.last_borrower || "N/A"]), "blue", true);
        }
    }
});

// Dashboard connections (hiển thị linked documents)
// Trong Python controller:
class LibraryBook(Document):
    def on_doctype_update():
        # Tự động hiện link toi Library Transaction trên dashboard
        frappe.db.add_index("Library Transaction", ["book"])
```

#### 4. Sidebar Customization

```javascript
frappe.ui.form.on("Library Book", {
    refresh: function(frm) {
        // Thêm link vao sidebar
        frm.sidebar.add_user_action(__("View Transactions")).on("click", function() {
            frappe.set_route("List", "Library Transaction", {
                book: frm.doc.name
            });
        });

        // Thêm HTML custom vao sidebar
        if (frm.doc.cover_image) {
            frm.sidebar.image_wrapper = $(
                `<div class="sidebar-image">
                    <img src="${frm.doc.cover_image}" style="max-width:100%;border-radius:8px;">
                </div>`
            );
            frm.sidebar.$el.prepend(frm.sidebar.image_wrapper);
        }
    }
});
```

### Mini Quiz

<details>
<summary><strong>Câu 1:</strong> Su khác biết giua <code>frm.add_custom_button</code> và <code>frm.page.set_primary_action</code>?</summary>

**Trả lời:** `add_custom_button` thêm button vao thành menu phía trên (có thể nhóm trong dropdown). `set_primary_action` thay thế button chính (xanh) ở goc trên ben phải — chi có 1 primary action tại 1 thoi điểm. Primary action được nhin thay nổi bật nhất, nên dùng cho hành động chính của document.
</details>

<details>
<summary><strong>Câu 2:</strong> Làm sao để field "ebook_url" BAT BUOC chi khi <code>book_type</code> là "E-Book"?</summary>

**Trả lời:** Dùng `frm.toggle_reqd("ebook_url", frm.doc.book_type === "E-Book")` trong handler của field `book_type` VA trong `refresh`. Toggle_reqd thay đổi property "mandatory" của field. Can đặt trong cả 2 nơi để đảm bảo: (1) khi form load, (2) khi user thay đổi book_type.
</details>

<details>
<summary><strong>Câu 3:</strong> Khi nào nên dùng Client Script (UI) vs Controller (Python) để validate form?</summary>

**Trả lời:** Client Script validate cho UX nhanh (user thay lỗi ngày trước khi save). Controller validate cho BẢO MẬT (server-side, không the bypass). Nên dùng CA HAI: client script cho trải nghiệm tot, controller cho đảm bảo data integrity. API calls có thể bypass client validation nên server validation là bắt buộc.
</details>

**DEEP DIVE:** Xem skill `frappe` → references/desk/ để hiểu thêm về Frappe Desk API.

**DEEP DIVE:** Xem skill `dcnet_quality` → syntax/erpnext-syntax-clientscripts/ cho client script patterns chuan.

---

## L6.2: List View & Report Builder

### Tổng quan / Overview

List View là giao diện hiển thị danh sách documents. Ban có thể tùy chỉnh cột hiển thị, màu sac indicators, formatters, bulk actions, và thêm sidebar filters. Report Builder là công cụ drag-and-drop để tạo báo cáo nhanh từ List View.

### Khái niệm chính / Key Concepts

#### 1. List View Customization

```javascript
// File: library_book/library_book_list.js

frappe.listview_settings["Library Book"] = {
    // Cột hiển thị (mac dinh Frappe chọn 4-7 cột)
    // Không can khai báo — Frappe từ chọn dua trên field order
    // Nhưng có thể override bang add_fields
    add_fields: ["status", "author", "isbn", "book_type"],

    // Indicator màu theo trạng thái
    get_indicator: function(doc) {
        // Return: [label, color, fieldname]
        const status_map = {
            "Available": [__("Available"), "green", "status"],
            "Issued": [__("Issued"), "orange", "status"],
            "Lost": [__("Lost"), "red", "status"],
            "Reserved": [__("Reserved"), "blue", "status"]
        };
        return status_map[doc.status] || [doc.status, "grey", "status"];
    },

    // Row formatters — tùy chỉnh hiển thị cột
    formatters: {
        title: function(value, field, doc) {
            // Thêm icon trước tieu de
            const icon = doc.book_type === "E-Book" ? "📱" : "📚";
            return `${icon} ${value}`;
        },
        isbn: function(value) {
            if (!value) return "";
            return `<code>${value}</code>`;
        }
    },

    // Hanh dòng hàng loạt (bulk actions)
    onload: function(listview) {
        // Thêm bulk action
        listview.page.add_action_item(__("Mark as Lost"), function() {
            const selected = listview.get_checked_items();
            if (selected.length === 0) {
                frappe.msgprint(__("Please select at least one book"));
                return;
            }

            frappe.confirm(
                __("Mark {0} books as Lost?", [selected.length]),
                function() {
                    frappe.call({
                        method: "library_management.api.bulk_mark_lost",
                        args: { books: selected.map(d => d.name) },
                        callback: function() {
                            listview.refresh();
                        }
                    });
                }
            );
        });

        // Thêm sidebar filter custom
        listview.page.add_field({
            label: __("Book Type"),
            fieldtype: "Select",
            fieldname: "book_type_filter",
            options: "\nPhysical\nE-Book",
            change: function() {
                const value = this.get_value();
                if (value) {
                    listview.filter_area.add(["Library Book", "book_type", "=", value]);
                }
            }
        });
    },

    // Primary action khi click button phía trên
    primary_action: function() {
        frappe.new_doc("Library Book");
    },

    // Hiển thị khi không có data
    get_no_result_message: function() {
        return `<div class="text-center text-muted" style="padding: 40px;">
            <p><strong>${__("No books found")}</strong></p>
            <p>${__("Click the + button to add your first book")}</p>
        </div>`;
    },

    // Refresh mọi 30 giay (cho dashboard-like list)
    // refresh_interval: 30  // Don vi: giay (không khuyen dùng cho list bình thường)
};
```

#### 2. Report Builder

```
Report Builder la tinh nang co san trong List View:
1. Vao List View cua bat ky DocType
2. Click "Edit Filters" (bieu tuong loc)
3. Click "Columns" de chon cot hien thi
4. Click "Group By" de nhom du lieu
5. Click "Sort" de sap xep
6. Click "Save" de luu thanh Report

Phu hop cho:
- Bao cao don gian, khong can code
- User tu tao bao cao theo nhu cau
- Xuat Excel/CSV nhanh

Han che:
- Khong co tinh toan phuc tap (sum, average across rows)
- Khong JOIN nhieu DocTypes
- Khong co chart tuy chinh
→ Dung Script Report cho cac truong hop nay
```

#### 3. Virtual List View (chuyển hướng từ list)

```javascript
// Redirect từ Standard List sang Report view
frappe.listview_settings["Library Transaction"] = {
    onload: function(listview) {
        // Thêm button chuyen sang report view
        listview.page.add_inner_button(__("Summary Report"), function() {
            frappe.set_route("query-report", "Library Transaction Summary");
        });
    }
};
```

### Mini Quiz

<details>
<summary><strong>Câu 1:</strong> Hàm <code>get_indicator</code> trong listview_settings trả về gi?</summary>

**Trả lời:** Trả về array `[label, color, fieldname]`. `label` là text hiển thị, `color` là màu (green, orange, red, blue, grey, etc.), `fieldname` là field dùng để xác định giá trị. Indicator hiển thị nhu badge màu ben canh record trong list.
</details>

<details>
<summary><strong>Câu 2:</strong> Khi nào nên dùng Report Builder, khi nào nên dùng Script Report?</summary>

**Trả lời:** Report Builder: báo cáo đơn giản, 1 DocType, chi filter/sort/group — user từ làm được. Script Report: báo cáo phức tạp can tính toán, JOIN nhiều DocTypes, chart tùy chỉnh, logic business — developer làm. Quy tac: nếu user mượn từ drag-and-drop → Report Builder; nếu can Python code → Script Report.
</details>

**DEEP DIVE:** Xem skill `frappe` → references/desk/ để hiểu thêm về List View API.

---

## L6.3: Script Reports

### Tổng quan / Overview

Script Report là loai report mạnh nhất trong Frappe, cho phép viết Python để truy vấn dữ liệu và JavaScript để tạo filters. Report trả về columns, data, và optional chart/message. Đây là cach tạo báo cáo kinh doanh phức tạp nhu doanh thu, tồn kho, công nợ trong ERPNext.

### Khái niệm chính / Key Concepts

#### 1. Cấu trúc file / File Structure

```
library_management/
  library_management/
    report/
      library_usage_report/
        __init__.py                    # File rong (required)
        library_usage_report.json      # Report definition
        library_usage_report.py        # Python logic (columns + data)
        library_usage_report.js        # JavaScript filters
```

#### 2. Report Definition (JSON)

```json
{
    "name": "Library Usage Report",
    "doctype": "Library Transaction",
    "report_type": "Script Report",
    "ref_doctype": "Library Transaction",
    "is_standard": "Yes",
    "module": "Library Management",
    "roles": [
        {"role": "Librarian"},
        {"role": "Library Member"}
    ]
}
```

#### 3. Python Report Logic

```python
# library_usage_report.py
import frappe
from frappe import _
from frappe.utils import getdate, add_months, today


def execute(filters=None):
    """Ham chinh — Frappe goi ham nay de lay du lieu report.

    Returns:
        columns (list): Dinh nghia cot
        data (list): Du lieu (list of dicts hoac list of lists)
        message (str, optional): Thong bao hien phia tren report
        chart (dict, optional): Chart config
    """
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    message = get_message(data)

    return columns, data, message, chart


def get_columns():
    """Dinh nghia cot report.

    Moi cot co the la:
    - Dict voi day du thong tin
    - String voi format: "Label:fieldtype:width"
    """
    return [
        {
            "label": _("Member"),
            "fieldname": "member",
            "fieldtype": "Link",
            "options": "Library Member",
            "width": 200
        },
        {
            "label": _("Member Name"),
            "fieldname": "member_name",
            "fieldtype": "Data",
            "width": 180
        },
        {
            "label": _("Total Borrowed"),
            "fieldname": "total_borrowed",
            "fieldtype": "Int",
            "width": 120
        },
        {
            "label": _("Currently Issued"),
            "fieldname": "currently_issued",
            "fieldtype": "Int",
            "width": 120
        },
        {
            "label": _("Returned"),
            "fieldname": "returned",
            "fieldtype": "Int",
            "width": 100
        },
        {
            "label": _("Overdue"),
            "fieldname": "overdue",
            "fieldtype": "Int",
            "width": 100
        },
        {
            "label": _("Fine Amount"),
            "fieldname": "fine_amount",
            "fieldtype": "Currency",
            "width": 120
        }
    ]


def get_data(filters):
    """Lay du lieu report."""

    conditions = ""
    values = {}

    if filters.get("from_date"):
        conditions += " AND lt.date >= %(from_date)s"
        values["from_date"] = filters["from_date"]

    if filters.get("to_date"):
        conditions += " AND lt.date <= %(to_date)s"
        values["to_date"] = filters["to_date"]

    if filters.get("member"):
        conditions += " AND lt.member = %(member)s"
        values["member"] = filters["member"]

    data = frappe.db.sql("""
        SELECT
            lt.member,
            lm.member_name,
            COUNT(lt.name) as total_borrowed,
            SUM(CASE WHEN lt.status = 'Issued' THEN 1 ELSE 0 END) as currently_issued,
            SUM(CASE WHEN lt.status = 'Returned' THEN 1 ELSE 0 END) as returned,
            SUM(CASE
                WHEN lt.status = 'Issued' AND lt.due_date < CURDATE()
                THEN 1 ELSE 0
            END) as overdue,
            SUM(CASE
                WHEN lt.status = 'Issued' AND lt.due_date < CURDATE()
                THEN DATEDIFF(CURDATE(), lt.due_date) * 10000
                ELSE 0
            END) as fine_amount
        FROM `tabLibrary Transaction` lt
        LEFT JOIN `tabLibrary Member` lm ON lt.member = lm.name
        WHERE 1=1 {conditions}
        GROUP BY lt.member
        ORDER BY total_borrowed DESC
    """.format(conditions=conditions), values, as_dict=True)

    return data


def get_chart(data):
    """Tao chart tu data."""
    if not data:
        return None

    # Bar chart — Top 10 members
    top_members = data[:10]

    return {
        "data": {
            "labels": [d.member_name or d.member for d in top_members],
            "datasets": [
                {
                    "name": _("Borrowed"),
                    "values": [d.total_borrowed for d in top_members]
                },
                {
                    "name": _("Overdue"),
                    "values": [d.overdue for d in top_members]
                }
            ]
        },
        "type": "bar",  # bar, line, pie, donut, percentage
        "colors": ["#7CD6FD", "#FF5858"],
        "barOptions": {
            "stacked": False
        }
    }


def get_message(data):
    """Thong bao tong hop hien phia tren report."""
    if not data:
        return _("No data found")

    total_members = len(data)
    total_overdue = sum(d.overdue or 0 for d in data)
    total_fine = sum(d.fine_amount or 0 for d in data)

    if total_overdue > 0:
        return _(
            "<b>{0}</b> members | <span style='color:red'><b>{1}</b> overdue books</span>"
            " | Total fine: <b>{2}</b>"
        ).format(total_members, total_overdue, frappe.format_value(total_fine, {"fieldtype": "Currency"}))

    return _("<b>{0}</b> members with borrowing activity").format(total_members)
```

#### 4. JavaScript Filters

```javascript
// library_usage_report.js
frappe.query_reports["Library Usage Report"] = {
    filters: [
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            default: frappe.datetime.add_months(frappe.datetime.nowdate(), -1),
            reqd: 1
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            default: frappe.datetime.nowdate(),
            reqd: 1
        },
        {
            fieldname: "member",
            label: __("Member"),
            fieldtype: "Link",
            options: "Library Member"
        }
    ],

    // Formatter cho tung cell
    formatter: function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);

        // To do overdue
        if (column.fieldname === "overdue" && data.overdue > 0) {
            value = `<span style="color: red; font-weight: bold;">${value}</span>`;
        }

        // To do fine
        if (column.fieldname === "fine_amount" && data.fine_amount > 0) {
            value = `<span style="color: red;">${value}</span>`;
        }

        return value;
    },

    // Tinh tong cho cột so
    get_datatable_options(options) {
        return Object.assign(options, {
            checkboxColumn: false,
            // Thêm row tong ở cuoi
        });
    },

    // Chạy sau khi report render xong
    after_datatable_render: function(datatable) {
        // Custom logic sau khi render
    }
};
```

#### 5. So sánh các loai Report

```
+------------------+------------------+------------------+------------------+
| Tinh nang        | Report Builder   | Query Report     | Script Report    |
+------------------+------------------+------------------+------------------+
| Code can         | Khong            | Chi SQL          | Python + JS      |
| Join tables      | Khong            | Co               | Co               |
| Chart            | Khong            | Khong            | Co               |
| Tinh toan phuc   | Khong            | Han che (SQL)    | Co (Python)      |
| tap              |                  |                  |                  |
| Filter UI        | Tu dong          | Tu dong          | Tu dinh nghia JS |
| Ai tao           | User             | Developer        | Developer        |
| Luu standard     | Khong            | Co               | Co               |
+------------------+------------------+------------------+------------------+
```

### Mini Quiz

<details>
<summary><strong>Câu 1:</strong> Hàm <code>execute()</code> trong Script Report trả về nhưng gi?</summary>

**Trả lời:** Trả về tuple `(columns, data, message, chart)`. `columns`: list định nghĩa cột. `data`: list of dicts chưa dữ liệu. `message`: HTML string (optional) hiện phía trên report. `chart`: dict config chart (optional) hiện phía trên data table.
</details>

<details>
<summary><strong>Câu 2:</strong> Trong định nghĩa column, su khác biết giua <code>fieldtype: "Link"</code> và <code>fieldtype: "Data"</code> là gì?</summary>

**Trả lời:** `Link` tạo hyperlink — click vao sẽ mo document do (can có `options` chỉ định DocType). `Data` chi hiện text bình thường, không click được. Dùng `Link` cho ID/name fields để user có thể navigate nhanh, `Data` cho display-only text.
</details>

<details>
<summary><strong>Câu 3:</strong> Tại sao nên dùng <code>frappe.db.sql</code> thay vì <code>frappe.db.get_list</code> trong Script Report?</summary>

**Trả lời:** Script Report thường can JOIN nhiều bang, GROUP BY, aggregate functions (SUM, COUNT, CASE WHEN) — nhưng thư `get_list` không hỗ trợ. `frappe.db.sql` cho phép viết SQL tuy y. Tuy nhien, với query đơn giản trên 1 bang, `get_list` van dùng được và ẩn toàn hơn (tự động handle permissions).
</details>

**DEEP DIVE:** Xem skill `frappe` → references/desk/ để hiểu thêm về Report API.

**DEEP DIVE:** Xem skill `erpnext` → references/ cho ERPNext Script Report patterns thuc te.

---

## L6.4: Workspace & Dashboard

### Tổng quan / Overview

Workspace là "trang chu" của mọi module trong Frappe Desk, chưa shortcuts, Number Cards, Charts, và các khoi nội dùng. Dashboard tổng hợp data từ nhiều nguồn thành các con số và biểu đồ truc quan. Hiểu cach cấu hình Workspace giúp tạo trải nghiệm người dùng chuyên nghiệp.

### Khái niệm chính / Key Concepts

#### 1. Workspace JSON Structure

```json
{
    "name": "Library Management",
    "module": "Library Management",
    "label": "Library Management",
    "category": "Modules",
    "icon": "book",
    "is_standard": 1,
    "public": 1,

    "content": "[{\"id\":\"heading1\",\"type\":\"header\",\"data\":{\"text\":\"Library Overview\",\"col\":12}},{\"id\":\"nc_row\",\"type\":\"number_card\",\"data\":{\"number_card_name\":\"Total Books\",\"col\":4}},{\"id\":\"nc_row2\",\"type\":\"number_card\",\"data\":{\"number_card_name\":\"Active Members\",\"col\":4}},{\"id\":\"nc_row3\",\"type\":\"number_card\",\"data\":{\"number_card_name\":\"Books Issued\",\"col\":4}},{\"id\":\"spacer1\",\"type\":\"spacer\",\"data\":{\"col\":12}},{\"id\":\"chart1\",\"type\":\"chart\",\"data\":{\"chart_name\":\"Monthly Borrowing Trends\",\"col\":12}},{\"id\":\"heading2\",\"type\":\"header\",\"data\":{\"text\":\"Quick Access\",\"col\":12}},{\"id\":\"shortcut1\",\"type\":\"shortcut\",\"data\":{\"shortcut_name\":\"Library Book\",\"col\":4}},{\"id\":\"shortcut2\",\"type\":\"shortcut\",\"data\":{\"shortcut_name\":\"Library Transaction\",\"col\":4}},{\"id\":\"shortcut3\",\"type\":\"shortcut\",\"data\":{\"shortcut_name\":\"Library Usage Report\",\"col\":4}}]",

    "shortcuts": [
        {
            "label": "Library Book",
            "type": "DocType",
            "link_to": "Library Book",
            "color": "#7C7C7C",
            "stats_filter": "{\"status\": \"Available\"}"
        },
        {
            "label": "Library Transaction",
            "type": "DocType",
            "link_to": "Library Transaction"
        },
        {
            "label": "Library Usage Report",
            "type": "Report",
            "link_to": "Library Usage Report",
            "dependencies": "Library Transaction"
        }
    ],

    "number_cards": [
        {"label": "Total Books"},
        {"label": "Active Members"},
        {"label": "Books Issued"}
    ],

    "charts": [
        {"label": "Monthly Borrowing Trends"}
    ]
}
```

#### 2. Number Cards

```json
// number_card/total_books/total_books.json
// TYPE 1: Standard — count/sum/average trên 1 DocType
{
    "name": "Total Books",
    "label": "Total Books",
    "document_type": "Library Book",
    "function": "Count",
    "is_standard": 1,
    "module": "Library Management",
    "type": "Document Type",
    "filters_json": "[]",
    "show_percentage_stats": 1,
    "stats_time_interval": "Monthly",
    "color": "#29CD42"
}
```

```json
// TYPE 2: Custom — gọi API Python để tính giá trị
{
    "name": "Overdue Books",
    "label": "Overdue Books",
    "is_standard": 1,
    "module": "Library Management",
    "type": "Custom",
    "method": "library_management.api.get_overdue_count",
    "filters_json": "[]",
    "color": "#FF5858",
    "show_full_number": 1
}
```

```python
# API cho Custom Number Card
@frappe.whitelist()
def get_overdue_count():
    """Dem sach qua han — dung cho Number Card."""
    count = frappe.db.count("Library Transaction",
        filters={
            "status": "Issued",
            "due_date": ["<", frappe.utils.today()]
        }
    )
    return {
        "value": count,
        "fieldtype": "Int"  # Hoac "Currency" cho so tien
    }
```

#### 3. Dashboard Charts

```json
// dashboard_chart/monthly_borrowing_trends/monthly_borrowing_trends.json
// TYPE 1: Count — Đếm record theo thoi gian
{
    "name": "Monthly Borrowing Trends",
    "chart_name": "Monthly Borrowing Trends",
    "chart_type": "Count",
    "document_type": "Library Transaction",
    "based_on": "date",
    "time_interval": "Monthly",
    "timespan": "Last Year",
    "is_standard": 1,
    "module": "Library Management",
    "type": "Line",
    "color": "#7CD6FD",
    "filters_json": "{}",
    "width": "Full"
}
```

```json
// TYPE 2: Report — Tu Script Report
{
    "name": "Book Category Distribution",
    "chart_name": "Book Category Distribution",
    "chart_type": "Report",
    "report_name": "Library Book Summary",
    "is_standard": 1,
    "module": "Library Management",
    "type": "Donut",
    "color": "#7C7C7C",
    "use_report_chart": 1,
    "filters_json": "{}",
    "width": "Half"
}
```

#### 4. Content Blocks (trong Workspace content JSON)

```javascript
// Các loai block trong Workspace content:

// 1. Header
{"type": "header", "data": {"text": "Section Title", "col": 12}}

// 2. Number Card (tham chiếu ten Number Card)
{"type": "number_card", "data": {"number_card_name": "Total Books", "col": 4}}

// 3. Chart (tham chiếu ten Dashboard Chart)
{"type": "chart", "data": {"chart_name": "Monthly Trends", "col": 12}}

// 4. Shortcut (tham chiếu ten Shortcut)
{"type": "shortcut", "data": {"shortcut_name": "Library Book", "col": 4}}

// 5. Spacer (khoảng trống)
{"type": "spacer", "data": {"col": 12}}

// 6. Card (nhóm links)
{
    "type": "card",
    "data": {
        "card_name": "Settings",
        "col": 4
    }
}

// col: 1-12 (hệ thống grid 12 cột, giong Bootstrap)
// col: 4 = 1/3 man hinh, col: 6 = 1/2 man hinh, col: 12 = full width
```

### Mini Quiz

<details>
<summary><strong>Câu 1:</strong> Su khác biết giua Number Card type "Document Type" và type "Custom"?</summary>

**Trả lời:** "Document Type" (Standard): Frappe tự động Count/Sum/Average trên 1 DocType với filters — không cần code Python. "Custom": Gọi API Python method để tính giá trị — dùng cho logic phức tạp (VD: đếm sach qua han can so sánh ngày). Custom method trả về `{"value": number, "fieldtype": "Int/Currency"}`.
</details>

<details>
<summary><strong>Câu 2:</strong> <code>filters_json</code> trong Number Card và Dashboard Chart có format khác nhau như thế nào?</summary>

**Trả lời:** Number Card dùng array-of-arrays: `[["DocType","field","op","value"]]`. Dashboard Chart dùng object: `{"key": "value"}`. Đây là su không nhất quán trong Frappe — can nhỏ dùng format cho tung loai để tránh lỗi.
</details>

**DEEP DIVE:** Xem skill `frappe` → references/desk/ để hiểu thêm về Workspace API.

**DEEP DIVE:** Xem skill `erpnext` → references/ cho ERPNext Dashboard patterns thuc te.

---

## L6.5: Hands-on — Library Dashboard

### Tổng quan / Overview

Thực hành tổng hợp: Xây dựng dashboard hoàn chỉnh cho thư viện gom Number Cards, Charts, Script Report, và Workspace. Ket hop tất cả kiến thức từ L6.1-L6.4 để tạo trải nghiệm quản lý truc quan.

### Bài tập / Exercise

#### Bước 1: Number Cards (3 cards)

```python
# File: library_management/library_management/api.py (thêm vao)

@frappe.whitelist()
def get_total_books():
    """Number Card: Tong so sach."""
    count = frappe.db.count("Library Book")
    return {"value": count, "fieldtype": "Int"}


@frappe.whitelist()
def get_active_members():
    """Number Card: Thanh vien dang hoat dong (co it nhat 1 sach dang muon)."""
    result = frappe.db.sql("""
        SELECT COUNT(DISTINCT member) as count
        FROM `tabLibrary Transaction`
        WHERE status = 'Issued'
    """, as_dict=True)
    return {"value": result[0].count if result else 0, "fieldtype": "Int"}


@frappe.whitelist()
def get_books_issued():
    """Number Card: So sach dang cho muon."""
    count = frappe.db.count("Library Book", {"status": "Issued"})
    return {"value": count, "fieldtype": "Int"}
```

```json
// number_card/total_books/total_books.json
{
    "name": "Total Books",
    "label": "Total Books",
    "is_standard": 1,
    "module": "Library Management",
    "type": "Custom",
    "method": "library_management.api.get_total_books",
    "filters_json": "[]",
    "color": "#29CD42",
    "show_full_number": 1
}
```

```json
// number_card/active_members/active_members.json
{
    "name": "Active Members",
    "label": "Active Members",
    "is_standard": 1,
    "module": "Library Management",
    "type": "Custom",
    "method": "library_management.api.get_active_members",
    "filters_json": "[]",
    "color": "#7CD6FD",
    "show_full_number": 1
}
```

```json
// number_card/books_issued/books_issued.json
{
    "name": "Books Issued",
    "label": "Books Issued",
    "is_standard": 1,
    "module": "Library Management",
    "type": "Custom",
    "method": "library_management.api.get_books_issued",
    "filters_json": "[]",
    "color": "#ECAD4B",
    "show_full_number": 1
}
```

#### Bước 2: Dashboard Chart — Monthly Borrowing Trends

```json
// dashboard_chart/monthly_borrowing_trends/monthly_borrowing_trends.json
{
    "name": "Monthly Borrowing Trends",
    "chart_name": "Monthly Borrowing Trends",
    "chart_type": "Count",
    "document_type": "Library Transaction",
    "based_on": "date",
    "time_interval": "Monthly",
    "timespan": "Last Year",
    "is_standard": 1,
    "module": "Library Management",
    "type": "Line",
    "color": "#7CD6FD",
    "filters_json": "{}",
    "width": "Full"
}
```

#### Bước 3: Script Report — Overdue Books Report

```python
# report/overdue_books/overdue_books.py
import frappe
from frappe import _
from frappe.utils import today, date_diff


def execute(filters=None):
    columns = [
        {"label": _("Transaction"), "fieldname": "name", "fieldtype": "Link",
         "options": "Library Transaction", "width": 130},
        {"label": _("Book"), "fieldname": "book", "fieldtype": "Link",
         "options": "Library Book", "width": 130},
        {"label": _("Book Title"), "fieldname": "book_title",
         "fieldtype": "Data", "width": 200},
        {"label": _("Member"), "fieldname": "member", "fieldtype": "Link",
         "options": "Library Member", "width": 130},
        {"label": _("Member Name"), "fieldname": "member_name",
         "fieldtype": "Data", "width": 150},
        {"label": _("Issue Date"), "fieldname": "date",
         "fieldtype": "Date", "width": 110},
        {"label": _("Due Date"), "fieldname": "due_date",
         "fieldtype": "Date", "width": 110},
        {"label": _("Days Overdue"), "fieldname": "days_overdue",
         "fieldtype": "Int", "width": 110},
        {"label": _("Fine (VND)"), "fieldname": "fine",
         "fieldtype": "Currency", "width": 120}
    ]

    data = frappe.db.sql("""
        SELECT
            lt.name,
            lt.book,
            lb.title as book_title,
            lt.member,
            lm.member_name,
            lt.date,
            lt.due_date,
            DATEDIFF(CURDATE(), lt.due_date) as days_overdue,
            DATEDIFF(CURDATE(), lt.due_date) * 10000 as fine
        FROM `tabLibrary Transaction` lt
        LEFT JOIN `tabLibrary Book` lb ON lt.book = lb.name
        LEFT JOIN `tabLibrary Member` lm ON lt.member = lm.name
        WHERE lt.status = 'Issued'
            AND lt.due_date < CURDATE()
        ORDER BY days_overdue DESC
    """, as_dict=True)

    # Chart
    chart = None
    if data:
        # Nhóm theo số ngày qua han
        buckets = {"1-7 days": 0, "8-14 days": 0, "15-30 days": 0, "30+ days": 0}
        for row in data:
            d = row.days_overdue
            if d <= 7:
                buckets["1-7 days"] += 1
            elif d <= 14:
                buckets["8-14 days"] += 1
            elif d <= 30:
                buckets["15-30 days"] += 1
            else:
                buckets["30+ days"] += 1

        chart = {
            "data": {
                "labels": list(buckets.keys()),
                "datasets": [{"name": _("Overdue Books"), "values": list(buckets.values())}]
            },
            "type": "bar",
            "colors": ["#FF5858"]
        }

    total_fine = sum(row.fine or 0 for row in data)
    message = _("<b>{0}</b> overdue books | Total fine: <b>{1}</b> VND").format(
        len(data), f"{total_fine:,.0f}"
    ) if data else _("No overdue books!")

    return columns, data, message, chart
```

```javascript
// report/overdue_books/overdue_books.js
frappe.query_reports["Overdue Books"] = {
    filters: [],  // Không can filter — hiện tất cả sach qua han

    formatter: function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);

        if (column.fieldname === "days_overdue") {
            if (data.days_overdue > 30) {
                value = `<span style="color:red;font-weight:bold;">${value}</span>`;
            } else if (data.days_overdue > 14) {
                value = `<span style="color:orange;font-weight:bold;">${value}</span>`;
            }
        }

        return value;
    }
};
```

#### Bước 4: Workspace — Ket hop tất cả

```json
{
    "name": "Library Management",
    "module": "Library Management",
    "label": "Library Management",
    "category": "Modules",
    "icon": "book",
    "is_standard": 1,
    "public": 1,
    "content": "[{\"id\":\"h1\",\"type\":\"header\",\"data\":{\"text\":\"<span class='h4'>Library Overview</span>\",\"col\":12}},{\"id\":\"nc1\",\"type\":\"number_card\",\"data\":{\"number_card_name\":\"Total Books\",\"col\":4}},{\"id\":\"nc2\",\"type\":\"number_card\",\"data\":{\"number_card_name\":\"Active Members\",\"col\":4}},{\"id\":\"nc3\",\"type\":\"number_card\",\"data\":{\"number_card_name\":\"Books Issued\",\"col\":4}},{\"id\":\"sp1\",\"type\":\"spacer\",\"data\":{\"col\":12}},{\"id\":\"ch1\",\"type\":\"chart\",\"data\":{\"chart_name\":\"Monthly Borrowing Trends\",\"col\":12}},{\"id\":\"sp2\",\"type\":\"spacer\",\"data\":{\"col\":12}},{\"id\":\"h2\",\"type\":\"header\",\"data\":{\"text\":\"<span class='h4'>Quick Access</span>\",\"col\":12}},{\"id\":\"sc1\",\"type\":\"shortcut\",\"data\":{\"shortcut_name\":\"Library Book\",\"col\":4}},{\"id\":\"sc2\",\"type\":\"shortcut\",\"data\":{\"shortcut_name\":\"Library Transaction\",\"col\":4}},{\"id\":\"sc3\",\"type\":\"shortcut\",\"data\":{\"shortcut_name\":\"Overdue Books\",\"col\":4}}]",
    "shortcuts": [
        {
            "label": "Library Book",
            "type": "DocType",
            "link_to": "Library Book"
        },
        {
            "label": "Library Transaction",
            "type": "DocType",
            "link_to": "Library Transaction"
        },
        {
            "label": "Overdue Books",
            "type": "Report",
            "link_to": "Overdue Books",
            "dependencies": "Library Transaction"
        }
    ],
    "number_cards": [
        {"label": "Total Books"},
        {"label": "Active Members"},
        {"label": "Books Issued"}
    ],
    "charts": [
        {"label": "Monthly Borrowing Trends"}
    ]
}
```

### Kiểm tra / Verification

```bash
# Sau khi tạo xong các file, chạy:
cd /workspace/development/frappe-bench

# Migrate để tạo report, number cards, charts
bench --site flow.local migrate

# Kiểm tra workspace hiển thị
bench --site flow.local console
# >>> frappe.get_doc("Workspace", "Library Management")

# Truy cập browser: http://flow.local:8000/app/library-management
```

### Mini Quiz

<details>
<summary><strong>Câu 1:</strong> Workspace <code>content</code> là gì và tại sao nó là JSON string thay vì object?</summary>

**Trả lời:** `content` là JSON string chưa array các block (header, number_card, chart, shortcut, spacer, card). No được lưu nhu string vì Frappe Workspace editor trên UI serialize/deserialize no. Mỗi block có `id` (unique), `type`, và `data` (chưa config nhu `col` cho grid width 1-12).
</details>

<details>
<summary><strong>Câu 2:</strong> Làm sao để Number Card hiển thị số đầy đủ (VD: 2.847.500 thay vì "2.85M")?</summary>

**Trả lời:** Đặt `"show_full_number": 1` trong Number Card JSON. Mac dinh Frappe rút gọn số lớn thành dang viết tat (K, M, B). Với tien VND, số thường rat lớn nên can bat `show_full_number` để hiển thị đầy đủ.
</details>

**DEEP DIVE:** Xem skill `frappe` → references/desk/ để hiểu thêm về Workspace internals.

**DEEP DIVE:** Xem skill `erpnext` → references/ cho Dashboard patterns của ERPNext modules thuc te.
