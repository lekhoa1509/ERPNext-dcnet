# Module 8: ERPNext Development (Capstone)
# Mô-đun 8: Phát triển trên ERPNext (Dự án tổng hợp)

> **Container:** `devcontainer-frappe-1`
> **Bench path:** `/workspace/development/frappe-bench`
> **Site:** `flow.local`
> **Prefix command:** `docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local ..."`

---

## Prerequisites / Yêu cầu trước khi bắt đầu

- Completed Modules 1-7 (full frappe_learn app)
- ERPNext installed and configured on `flow.local`
- Understanding of Frappe DocTypes, Controllers, Client Scripts, Tests, and Fixtures
- Đã hoàn thành Module 1-7 (app frappe_learn hoàn chỉnh)
- ERPNext đã cài và cấu hình trên `flow.local`

---

## Capstone Project: Equipment Rental System / Dự án: Hệ thống cho thuê thiết bị

In this module, you will build a complete "Equipment Rental" feature on top of ERPNext, using real ERPNext DocTypes (Item, Customer) and creating a custom DocType with workflow, reports, and dashboards.

Trong module này, bạn sẽ xây dựng chức năng "Cho thuê thiết bị" trên ERPNext, sử dụng các DocType ERPNext thật (Item, Customer) và tạo DocType tùy chỉnh với workflow, báo cáo, và dashboard.

---

## Exercise 8.1: ERPNext Exploration / Khám phá ERPNext

### Objective / Mục tiêu
Explore the ERPNext installation, understand the core DocTypes (Company, Item, Customer), and learn how ERPNext modules are structured.

Khám phá ERPNext, hiểu các DocType cốt lõi (Company, Item, Customer), và học cách các module ERPNext được tổ chức.

### Instructions / Hướng dẫn

**Step 1:** List all installed ERPNext modules

```bash
docker exec -it devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console"
```

```python
# List all installed apps
print("Installed apps:")
for app in frappe.get_installed_apps():
    print(f"  - {app}")

# List all modules
print("\nAll modules:")
modules = frappe.get_all("Module Def", fields=["name", "app_name"], order_by="app_name, name")
for m in modules:
    print(f"  [{m.app_name}] {m.name}")
```

**Step 2:** Explore core ERPNext DocTypes

```python
# Count DocTypes per module
from collections import Counter
doctypes = frappe.get_all("DocType", fields=["name", "module"], limit_page_length=0)
module_counts = Counter(dt.module for dt in doctypes)
print("\nDocTypes per module (top 15):")
for module, count in module_counts.most_common(15):
    print(f"  {module}: {count} DocTypes")

# List key DocTypes
print("\n--- Key DocTypes ---")
key_doctypes = ["Company", "Item", "Customer", "Supplier", "Sales Order",
                "Purchase Order", "Stock Entry", "Sales Invoice", "Payment Entry"]
for dt_name in key_doctypes:
    meta = frappe.get_meta(dt_name)
    field_count = len(meta.fields)
    print(f"  {dt_name}: {field_count} fields, module={meta.module}")
```

**Step 3:** Understand the Company structure

```python
# List companies
companies = frappe.get_all("Company", fields=["name", "abbr", "default_currency"])
for c in companies:
    print(f"Company: {c.name} ({c.abbr}) - Currency: {c.default_currency}")

# If no company exists, note that we need to create one
if not companies:
    print("No company found. Create one via Setup Wizard or bench console.")
```

**Step 4:** Explore Item DocType (our rental items will be Items)

```python
# Understand Item fields
meta = frappe.get_meta("Item")
print("\nItem DocType key fields:")
for field in meta.fields:
    if field.reqd or field.fieldname in ["item_code", "item_name", "item_group",
        "stock_uom", "is_stock_item", "is_fixed_asset", "description"]:
        print(f"  {field.fieldname} ({field.fieldtype}) - {'Required' if field.reqd else 'Optional'}")

# List Item Groups
groups = frappe.get_all("Item Group", fields=["name", "parent_item_group"], limit=20)
print("\nItem Groups:")
for g in groups:
    print(f"  {g.name} (parent: {g.parent_item_group or 'Root'})")
```

**Step 5:** Explore Customer DocType

```python
# Customer fields
meta = frappe.get_meta("Customer")
print("\nCustomer key fields:")
for field in meta.fields:
    if field.reqd or field.fieldname in ["customer_name", "customer_type",
        "customer_group", "territory", "default_currency"]:
        print(f"  {field.fieldname} ({field.fieldtype})")

# List Customer Groups
groups = frappe.get_all("Customer Group", pluck="name")
print(f"\nCustomer Groups: {groups}")
```

### Expected Output / Kết quả mong đợi

- List of all installed apps (frappe, erpnext, frappe_learn, etc.)
- Count of DocTypes per module
- Company structure with abbreviation and currency
- Item DocType field structure (for linking rental items)
- Customer DocType field structure (for linking rental customers)

### Verification / Kiểm tra

```bash
# Verify ERPNext is installed
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local list-apps"

# Verify Company exists
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local execute frappe.client.get_count --args '{\"doctype\": \"Company\"}'"
```

<details>
<summary>Hint 1: Setting up ERPNext data / Gợi ý 1: Thiết lập dữ liệu ERPNext</summary>

If ERPNext has no data yet, create a basic setup:

```python
# Create Company (if not exists)
if not frappe.db.exists("Company", "DCNET Test"):
    company = frappe.get_doc({
        "doctype": "Company",
        "company_name": "DCNET Test",
        "abbr": "DCT",
        "default_currency": "VND",
        "country": "Vietnam",
        "chart_of_accounts": "Standard"
    })
    company.insert()

# Create Item Group for rentals
if not frappe.db.exists("Item Group", "Rental Equipment"):
    ig = frappe.get_doc({
        "doctype": "Item Group",
        "item_group_name": "Rental Equipment",
        "parent_item_group": "All Item Groups"
    })
    ig.insert()

frappe.db.commit()
```

Nếu ERPNext chưa có dữ liệu, tạo Company và Item Group trước.
</details>

<details>
<summary>Hint 2: ERPNext module structure / Gợi ý 2: Cấu trúc module ERPNext</summary>

ERPNext modules are organized by business domain:
- **Stock**: Item, Warehouse, Stock Entry, Delivery Note, Purchase Receipt
- **Selling**: Customer, Sales Order, Quotation, Sales Invoice
- **Buying**: Supplier, Purchase Order, Purchase Invoice
- **Accounts**: Journal Entry, Payment Entry, GL Entry
- **Setup**: Company, Currency, UOM, Employee

Your custom app (frappe_learn) can link to ANY ERPNext DocType.

Các module ERPNext tổ chức theo lĩnh vực: Stock, Selling, Buying, Accounts, Setup.
App tùy chỉnh có thể liên kết đến BẤT KỲ DocType ERPNext nào.
</details>

---

## Exercise 8.2: Custom Fields / Trường tùy chỉnh

### Objective / Mục tiêu
Add custom fields to the Item DocType: `custom_rental_available` (Check) and `custom_rental_rate` (Currency) to mark items as rentable.

Thêm trường tùy chỉnh vào DocType Item: `custom_rental_available` (Check) và `custom_rental_rate` (Currency) để đánh dấu item có thể cho thuê.

### Instructions / Hướng dẫn

**Step 1:** Create custom fields via Python (recommended for version control)

File: `frappe_learn/frappe_learn/setup/install.py` (create or update)

```python
import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def after_install():
    """Run after app installation."""
    create_rental_custom_fields()


def create_rental_custom_fields():
    """Add rental-related custom fields to Item DocType."""
    custom_fields = {
        "Item": [
            {
                "fieldname": "custom_rental_section",
                "fieldtype": "Section Break",
                "label": "Rental Information",
                "insert_after": "description",
                "collapsible": 1
            },
            {
                "fieldname": "custom_rental_available",
                "fieldtype": "Check",
                "label": "Available for Rental",
                "insert_after": "custom_rental_section",
                "default": "0",
                "description": "Check if this item can be rented out"
            },
            {
                "fieldname": "custom_rental_cb",
                "fieldtype": "Column Break",
                "insert_after": "custom_rental_available"
            },
            {
                "fieldname": "custom_rental_rate",
                "fieldtype": "Currency",
                "label": "Rental Rate (per day)",
                "insert_after": "custom_rental_cb",
                "depends_on": "eval:doc.custom_rental_available",
                "mandatory_depends_on": "eval:doc.custom_rental_available",
                "description": "Daily rental rate in VND"
            },
            {
                "fieldname": "custom_rental_deposit",
                "fieldtype": "Currency",
                "label": "Rental Deposit",
                "insert_after": "custom_rental_rate",
                "depends_on": "eval:doc.custom_rental_available",
                "description": "Required deposit amount"
            }
        ]
    }

    create_custom_fields(custom_fields, update=True)
    frappe.db.commit()
    print("Rental custom fields created on Item DocType.")
```

**Step 2:** Register the install hook in hooks.py

Add to `frappe_learn/hooks.py`:

```python
after_install = "frappe_learn.frappe_learn.setup.install.after_install"
```

**Step 3:** Run the setup manually (since app is already installed)

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local execute frappe_learn.frappe_learn.setup.install.create_rental_custom_fields"
```

**Step 4:** Also export as fixtures for version control

Add to `frappe_learn/hooks.py` fixtures:

```python
fixtures = [
    # ... existing fixtures ...
    {
        "dt": "Custom Field",
        "filters": [["name", "like", "Item-custom_rental%"]]
    }
]
```

Export:

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local export-fixtures --doctype 'Custom Field'"
```

**Step 5:** Create test rental items

```bash
docker exec -it devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console"
```

```python
# Create rental items
rental_items = [
    {
        "item_code": "RENT-GOLF-001",
        "item_name": "Golf Club Set - Premium",
        "item_group": "Rental Equipment",  # Create this group first if needed
        "stock_uom": "Nos",
        "is_stock_item": 1,
        "custom_rental_available": 1,
        "custom_rental_rate": 500000,  # 500,000 VND/day
        "custom_rental_deposit": 5000000  # 5,000,000 VND
    },
    {
        "item_code": "RENT-GOLF-002",
        "item_name": "Golf Cart",
        "item_group": "Rental Equipment",
        "stock_uom": "Nos",
        "is_stock_item": 1,
        "custom_rental_available": 1,
        "custom_rental_rate": 1000000,
        "custom_rental_deposit": 10000000
    },
    {
        "item_code": "RENT-GOLF-003",
        "item_name": "Golf Bag - Standard",
        "item_group": "Rental Equipment",
        "stock_uom": "Nos",
        "is_stock_item": 1,
        "custom_rental_available": 1,
        "custom_rental_rate": 200000,
        "custom_rental_deposit": 2000000
    }
]

for item_data in rental_items:
    if not frappe.db.exists("Item", item_data["item_code"]):
        item = frappe.get_doc({"doctype": "Item", **item_data})
        item.insert()
        print(f"Created: {item_data['item_name']}")
    else:
        print(f"Already exists: {item_data['item_code']}")

frappe.db.commit()
```

### Expected Output / Kết quả mong đợi

- Item form shows a new "Rental Information" section (collapsible)
- When "Available for Rental" is checked, Rental Rate and Deposit fields appear
- Custom fields are visible at `http://localhost:8080/app/item/RENT-GOLF-001`
- Fields are exported as fixtures in `fixtures/custom_field.json`

### Verification / Kiểm tra

```bash
# Check custom fields exist
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local execute frappe.client.get_list --args '{\"doctype\": \"Custom Field\", \"filters\": {\"dt\": \"Item\", \"fieldname\": [\"like\", \"custom_rental%\"]}, \"fields\": [\"fieldname\", \"fieldtype\", \"label\"]}'"

# Check rental items exist
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local execute frappe.client.get_list --args '{\"doctype\": \"Item\", \"filters\": {\"custom_rental_available\": 1}, \"fields\": [\"item_code\", \"item_name\", \"custom_rental_rate\"]}'"
```

<details>
<summary>Hint 1: create_custom_fields() / Gợi ý 1</summary>

`create_custom_fields` is the standard ERPNext way to add fields programmatically:

```python
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

# Structure: { "DocType": [ {field_dict}, ... ] }
create_custom_fields({"Item": [...]}, update=True)
```

Key parameters in field dict:
- `fieldname`: Must start with `custom_` for custom fields
- `insert_after`: Field after which to insert (position matters!)
- `depends_on`: JS expression for conditional visibility
- `mandatory_depends_on`: JS expression for conditional mandatory

Tên trường phải bắt đầu bằng `custom_`. `insert_after` xác định vị trí. `depends_on` điều kiện hiển thị.
</details>

<details>
<summary>Hint 2: Custom Field naming / Gợi ý 2: Đặt tên Custom Field</summary>

Custom Field names in database follow the pattern:
- `{DocType}-{fieldname}` (e.g., `Item-custom_rental_available`)
- The `fieldname` in the DocType is just `custom_rental_available`

When filtering fixtures:
```python
{"dt": "Custom Field", "filters": [["name", "like", "Item-custom_rental%"]]}
```

Tên Custom Field trong DB: `{DocType}-{fieldname}`. Trong DocType chỉ dùng `fieldname`.
</details>

---

## Exercise 8.3: Custom DocType — Equipment Rental / DocType tùy chỉnh — Cho thuê thiết bị

### Objective / Mục tiêu
Create an "Equipment Rental" DocType linked to Item and Customer, with a workflow (Draft -> Reserved -> Rented -> Returned) and proper controllers.

Tạo DocType "Equipment Rental" liên kết với Item và Customer, có workflow (Draft -> Reserved -> Rented -> Returned) và controller phù hợp.

### Instructions / Hướng dẫn

**Step 1:** Create the DocType

You can create via UI (preferred for learning) or via code. Here's the code approach.

Create the directory structure:

```bash
docker exec devcontainer-frappe-1 bash -c "mkdir -p /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/library/doctype/equipment_rental"
```

File: `frappe_learn/frappe_learn/library/doctype/equipment_rental/equipment_rental.json`

```json
{
    "name": "Equipment Rental",
    "doctype": "DocType",
    "module": "Library",
    "engine": "InnoDB",
    "naming_rule": "By \"Naming Series\" field",
    "autoname": "naming_series:",
    "is_submittable": 1,
    "creation": "2026-03-17 10:00:00.000000",
    "modified": "2026-03-17 10:00:00.000000",
    "modified_by": "Administrator",
    "owner": "Administrator",
    "fields": [
        {
            "fieldname": "naming_series",
            "fieldtype": "Select",
            "label": "Series",
            "options": "RENT-.YYYY.-",
            "default": "RENT-.YYYY.-",
            "reqd": 1
        },
        {
            "fieldname": "customer",
            "fieldtype": "Link",
            "label": "Customer",
            "options": "Customer",
            "reqd": 1,
            "in_list_view": 1,
            "in_standard_filter": 1
        },
        {
            "fieldname": "customer_name",
            "fieldtype": "Data",
            "label": "Customer Name",
            "fetch_from": "customer.customer_name",
            "read_only": 1
        },
        {
            "fieldname": "cb_1",
            "fieldtype": "Column Break"
        },
        {
            "fieldname": "rental_date",
            "fieldtype": "Date",
            "label": "Rental Date",
            "reqd": 1,
            "default": "Today"
        },
        {
            "fieldname": "return_date",
            "fieldtype": "Date",
            "label": "Expected Return Date",
            "reqd": 1
        },
        {
            "fieldname": "actual_return_date",
            "fieldtype": "Date",
            "label": "Actual Return Date",
            "depends_on": "eval:doc.workflow_state=='Returned'"
        },
        {
            "fieldname": "rental_status",
            "fieldtype": "Select",
            "label": "Rental Status",
            "options": "\nDraft\nReserved\nRented\nReturned\nCancelled",
            "default": "Draft",
            "in_list_view": 1,
            "in_standard_filter": 1,
            "read_only": 1
        },
        {
            "fieldname": "sb_items",
            "fieldtype": "Section Break",
            "label": "Rental Items"
        },
        {
            "fieldname": "item",
            "fieldtype": "Link",
            "label": "Item",
            "options": "Item",
            "reqd": 1,
            "in_list_view": 1,
            "get_query": "() => { return { filters: { custom_rental_available: 1 } }; }"
        },
        {
            "fieldname": "item_name",
            "fieldtype": "Data",
            "label": "Item Name",
            "fetch_from": "item.item_name",
            "read_only": 1
        },
        {
            "fieldname": "cb_2",
            "fieldtype": "Column Break"
        },
        {
            "fieldname": "rental_rate",
            "fieldtype": "Currency",
            "label": "Rental Rate (per day)",
            "fetch_from": "item.custom_rental_rate",
            "reqd": 1
        },
        {
            "fieldname": "deposit_amount",
            "fieldtype": "Currency",
            "label": "Deposit Amount",
            "fetch_from": "item.custom_rental_deposit"
        },
        {
            "fieldname": "quantity",
            "fieldtype": "Int",
            "label": "Quantity",
            "default": 1,
            "reqd": 1
        },
        {
            "fieldname": "sb_totals",
            "fieldtype": "Section Break",
            "label": "Totals"
        },
        {
            "fieldname": "total_days",
            "fieldtype": "Int",
            "label": "Total Days",
            "read_only": 1
        },
        {
            "fieldname": "total_amount",
            "fieldtype": "Currency",
            "label": "Total Amount",
            "read_only": 1,
            "in_list_view": 1
        },
        {
            "fieldname": "cb_3",
            "fieldtype": "Column Break"
        },
        {
            "fieldname": "deposit_paid",
            "fieldtype": "Check",
            "label": "Deposit Paid"
        },
        {
            "fieldname": "payment_status",
            "fieldtype": "Select",
            "label": "Payment Status",
            "options": "\nUnpaid\nPartially Paid\nPaid",
            "default": "Unpaid",
            "read_only": 1
        },
        {
            "fieldname": "sb_notes",
            "fieldtype": "Section Break",
            "label": "Notes"
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
            "options": "Equipment Rental",
            "read_only": 1,
            "no_copy": 1,
            "print_hide": 1
        }
    ],
    "permissions": [
        {
            "role": "System Manager",
            "read": 1, "write": 1, "create": 1, "delete": 1,
            "submit": 1, "cancel": 1, "amend": 1,
            "report": 1, "export": 1, "import": 1, "share": 1, "print": 1, "email": 1
        },
        {
            "role": "Librarian",
            "read": 1, "write": 1, "create": 1,
            "submit": 1, "cancel": 1, "amend": 1,
            "report": 1, "print": 1, "email": 1
        },
        {
            "role": "Library Admin",
            "read": 1, "write": 1, "create": 1, "delete": 1,
            "submit": 1, "cancel": 1, "amend": 1,
            "report": 1, "export": 1, "import": 1, "share": 1, "print": 1, "email": 1
        }
    ],
    "sort_field": "modified",
    "sort_order": "DESC",
    "title_field": "customer_name",
    "search_fields": "customer, item, rental_status",
    "track_changes": 1
}
```

**Step 2:** Create the controller

File: `frappe_learn/frappe_learn/library/doctype/equipment_rental/equipment_rental.py`

```python
# Copyright (c) 2026, DCNET and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import date_diff, getdate, today


class EquipmentRental(Document):
    def validate(self):
        self.validate_dates()
        self.validate_item_available()
        self.calculate_totals()

    def validate_dates(self):
        """Ensure return date is after rental date."""
        if self.return_date and self.rental_date:
            if getdate(self.return_date) <= getdate(self.rental_date):
                frappe.throw(
                    _("Expected Return Date must be after Rental Date"),
                    title=_("Invalid Date Range")
                )

    def validate_item_available(self):
        """Check if the item is marked as available for rental."""
        if self.item:
            is_rental = frappe.db.get_value("Item", self.item, "custom_rental_available")
            if not is_rental:
                frappe.throw(
                    _("Item {0} is not available for rental").format(self.item),
                    title=_("Item Not Rentable")
                )

    def calculate_totals(self):
        """Calculate total days and total amount."""
        if self.rental_date and self.return_date:
            self.total_days = date_diff(self.return_date, self.rental_date)
            if self.total_days < 1:
                self.total_days = 1

        if self.total_days and self.rental_rate and self.quantity:
            self.total_amount = self.rental_rate * self.total_days * self.quantity

    def on_submit(self):
        """When rental is submitted, update status to Reserved."""
        self.db_set("rental_status", "Reserved")

    def on_cancel(self):
        """When rental is cancelled."""
        self.db_set("rental_status", "Cancelled")

    @frappe.whitelist()
    def mark_as_rented(self):
        """Mark the rental as active (equipment handed over)."""
        if self.docstatus != 1:
            frappe.throw(_("Rental must be submitted before marking as rented"))
        if self.rental_status != "Reserved":
            frappe.throw(_("Only reserved rentals can be marked as rented"))

        self.db_set("rental_status", "Rented")
        frappe.msgprint(_("Equipment marked as rented"), indicator="green", alert=True)

    @frappe.whitelist()
    def mark_as_returned(self):
        """Mark the rental as returned."""
        if self.rental_status != "Rented":
            frappe.throw(_("Only rented equipment can be returned"))

        self.db_set("rental_status", "Returned")
        self.db_set("actual_return_date", today())

        # Check for late return
        if getdate(today()) > getdate(self.return_date):
            late_days = date_diff(today(), self.return_date)
            late_fee = self.rental_rate * late_days * self.quantity
            frappe.msgprint(
                _("Equipment returned {0} days late. Late fee: {1}").format(
                    late_days, frappe.utils.fmt_money(late_fee, currency="VND")
                ),
                indicator="orange",
                alert=True
            )
        else:
            frappe.msgprint(_("Equipment returned on time!"), indicator="green", alert=True)
```

**Step 3:** Create the Client Script

File: `frappe_learn/frappe_learn/library/doctype/equipment_rental/equipment_rental.js`

```javascript
frappe.ui.form.on('Equipment Rental', {
    refresh: function(frm) {
        // Add workflow action buttons
        if (frm.doc.docstatus === 1) {
            if (frm.doc.rental_status === 'Reserved') {
                frm.add_custom_button(__('Mark as Rented'), function() {
                    frappe.call({
                        method: 'mark_as_rented',
                        doc: frm.doc,
                        callback: function(r) {
                            frm.reload_doc();
                        }
                    });
                }, __('Actions'));
            }

            if (frm.doc.rental_status === 'Rented') {
                frm.add_custom_button(__('Mark as Returned'), function() {
                    frappe.call({
                        method: 'mark_as_returned',
                        doc: frm.doc,
                        callback: function(r) {
                            frm.reload_doc();
                        }
                    });
                }, __('Actions'));
            }
        }

        // Status indicator
        if (frm.doc.rental_status === 'Rented') {
            frm.dashboard.set_headline_alert(
                `<div class="alert alert-warning">
                    <strong>${__('Equipment is currently rented out')}</strong>
                    — Due: ${frappe.datetime.str_to_user(frm.doc.return_date)}
                </div>`
            );
        }
    },

    item: function(frm) {
        // Fetch rental rate when item changes
        if (frm.doc.item) {
            frappe.db.get_value('Item', frm.doc.item, ['custom_rental_rate', 'custom_rental_deposit'])
                .then(r => {
                    if (r.message) {
                        frm.set_value('rental_rate', r.message.custom_rental_rate);
                        frm.set_value('deposit_amount', r.message.custom_rental_deposit);
                    }
                });
        }
    },

    rental_date: function(frm) {
        frm.trigger('calculate_totals');
    },

    return_date: function(frm) {
        frm.trigger('calculate_totals');
    },

    rental_rate: function(frm) {
        frm.trigger('calculate_totals');
    },

    quantity: function(frm) {
        frm.trigger('calculate_totals');
    },

    calculate_totals: function(frm) {
        if (frm.doc.rental_date && frm.doc.return_date) {
            let days = frappe.datetime.get_diff(frm.doc.return_date, frm.doc.rental_date);
            if (days < 1) days = 1;
            frm.set_value('total_days', days);

            if (frm.doc.rental_rate && frm.doc.quantity) {
                frm.set_value('total_amount', frm.doc.rental_rate * days * frm.doc.quantity);
            }
        }
    }
});
```

**Step 4:** Create `__init__.py` and List View

File: `frappe_learn/frappe_learn/library/doctype/equipment_rental/__init__.py`

```python
```

File: `frappe_learn/frappe_learn/library/doctype/equipment_rental/equipment_rental_list.js`

```javascript
frappe.listview_settings['Equipment Rental'] = {
    get_indicator: function(doc) {
        const status_map = {
            'Draft': [__('Draft'), 'gray', 'rental_status,=,Draft'],
            'Reserved': [__('Reserved'), 'blue', 'rental_status,=,Reserved'],
            'Rented': [__('Rented'), 'orange', 'rental_status,=,Rented'],
            'Returned': [__('Returned'), 'green', 'rental_status,=,Returned'],
            'Cancelled': [__('Cancelled'), 'red', 'rental_status,=,Cancelled']
        };
        return status_map[doc.rental_status] || [__(doc.rental_status), 'gray', ''];
    },

    add_fields: ['rental_status', 'customer_name', 'item_name', 'total_amount']
};
```

**Step 5:** Migrate and test

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local migrate && bench build --app frappe_learn && bench --site flow.local clear-cache"
```

### Expected Output / Kết quả mong đợi

- Equipment Rental DocType visible at `http://localhost:8080/app/equipment-rental`
- Form shows: Customer, Item (filtered to rental items), dates, rates, totals
- Workflow: Save (Draft) -> Submit (Reserved) -> Mark as Rented -> Mark as Returned
- List view shows colored status indicators
- Totals calculated automatically when dates/rate change

### Verification / Kiểm tra

```bash
# Verify DocType exists
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local execute frappe.client.get_count --args '{\"doctype\": \"Equipment Rental\"}'"

# Create a test rental
docker exec -it devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console"
```

```python
rental = frappe.get_doc({
    "doctype": "Equipment Rental",
    "customer": frappe.get_all("Customer", limit=1)[0].name if frappe.get_all("Customer", limit=1) else None,
    "item": "RENT-GOLF-001",
    "rental_date": frappe.utils.today(),
    "return_date": frappe.utils.add_days(frappe.utils.today(), 3),
    "quantity": 1
})
rental.insert()
print(f"Created rental: {rental.name}, Total: {rental.total_amount}")
rental.submit()
print(f"Submitted. Status: {rental.rental_status}")
rental.mark_as_rented()
rental.reload()
print(f"Rented. Status: {rental.rental_status}")
rental.mark_as_returned()
rental.reload()
print(f"Returned. Status: {rental.rental_status}, Return date: {rental.actual_return_date}")
```

<details>
<summary>Hint: DocType JSON structure / Gợi ý: Cấu trúc JSON của DocType</summary>

When creating DocType via code, the JSON must have ALL required keys. The most common missing ones:
- `engine`: "InnoDB"
- `sort_field` and `sort_order`
- `permissions` array (at least System Manager)
- `amended_from` field (required for submittable DocTypes)

For submittable DocTypes (`is_submittable: 1`):
- Must have `amended_from` Link field
- Uses `docstatus`: 0=Draft, 1=Submitted, 2=Cancelled

DocType JSON phải có tất cả key bắt buộc. DocType submittable cần trường `amended_from`.
</details>

---

## Exercise 8.4: Reports & Dashboard / Báo cáo & Dashboard

### Objective / Mục tiêu
Create a Script Report for rental revenue and Number Cards for active rentals. Add them to the Library workspace.

Tạo Script Report cho doanh thu cho thuê và Number Card cho các đơn thuê đang hoạt động. Thêm vào workspace Library.

### Instructions / Hướng dẫn

**Step 1:** Create the Rental Revenue Report

```bash
docker exec devcontainer-frappe-1 bash -c "mkdir -p /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/library/report/rental_revenue"
```

File: `frappe_learn/frappe_learn/library/report/rental_revenue/__init__.py`

```python
```

File: `frappe_learn/frappe_learn/library/report/rental_revenue/rental_revenue.json`

```json
{
    "name": "Rental Revenue",
    "doctype": "Report",
    "module": "Library",
    "ref_doctype": "Equipment Rental",
    "report_name": "Rental Revenue",
    "report_type": "Script Report",
    "is_standard": "Yes",
    "creation": "2026-03-17 10:00:00.000000",
    "modified": "2026-03-17 10:00:00.000000",
    "modified_by": "Administrator",
    "owner": "Administrator",
    "disabled": 0,
    "prepared_report": 0,
    "add_total_row": 1,
    "columns": [],
    "filters": [],
    "roles": [
        {"role": "System Manager"},
        {"role": "Library Admin"}
    ]
}
```

File: `frappe_learn/frappe_learn/library/report/rental_revenue/rental_revenue.py`

```python
# Copyright (c) 2026, DCNET and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    message = get_summary(data)
    chart = get_chart(data)
    return columns, data, message, chart


def get_columns():
    return [
        {"label": _("Rental ID"), "fieldname": "name", "fieldtype": "Link",
         "options": "Equipment Rental", "width": 150},
        {"label": _("Customer"), "fieldname": "customer_name", "fieldtype": "Data", "width": 150},
        {"label": _("Item"), "fieldname": "item_name", "fieldtype": "Data", "width": 200},
        {"label": _("Rental Date"), "fieldname": "rental_date", "fieldtype": "Date", "width": 120},
        {"label": _("Return Date"), "fieldname": "return_date", "fieldtype": "Date", "width": 120},
        {"label": _("Days"), "fieldname": "total_days", "fieldtype": "Int", "width": 80},
        {"label": _("Rate/Day"), "fieldname": "rental_rate", "fieldtype": "Currency", "width": 120},
        {"label": _("Total"), "fieldname": "total_amount", "fieldtype": "Currency", "width": 130},
        {"label": _("Status"), "fieldname": "rental_status", "fieldtype": "Data", "width": 100}
    ]


def get_data(filters):
    conditions = {"docstatus": 1}

    if filters:
        if filters.get("from_date"):
            conditions["rental_date"] = [">=", filters["from_date"]]
        if filters.get("to_date"):
            conditions["rental_date"] = ["<=", filters["to_date"]]
        if filters.get("customer"):
            conditions["customer"] = filters["customer"]
        if filters.get("rental_status"):
            conditions["rental_status"] = filters["rental_status"]

    data = frappe.get_all("Equipment Rental",
        filters=conditions,
        fields=["name", "customer_name", "item_name", "rental_date", "return_date",
                "total_days", "rental_rate", "total_amount", "rental_status"],
        order_by="rental_date desc"
    )

    return data


def get_summary(data):
    if not data:
        return _("No rental data found.")

    total_revenue = sum(d.total_amount or 0 for d in data)
    active = len([d for d in data if d.rental_status == "Rented"])
    returned = len([d for d in data if d.rental_status == "Returned"])

    return _(
        "Total Revenue: <b>{0}</b> | "
        "Active Rentals: <b>{1}</b> | "
        "Completed: <b>{2}</b>"
    ).format(
        frappe.utils.fmt_money(total_revenue, currency="VND"),
        active, returned
    )


def get_chart(data):
    if not data:
        return None

    # Group by month
    from collections import defaultdict
    monthly = defaultdict(float)
    for d in data:
        if d.rental_date:
            month_key = str(d.rental_date)[:7]  # YYYY-MM
            monthly[month_key] += d.total_amount or 0

    sorted_months = sorted(monthly.keys())

    return {
        "data": {
            "labels": sorted_months,
            "datasets": [
                {
                    "name": _("Revenue"),
                    "values": [monthly[m] for m in sorted_months]
                }
            ]
        },
        "type": "bar",
        "colors": ["#449CF0"]
    }
```

File: `frappe_learn/frappe_learn/library/report/rental_revenue/rental_revenue.js`

```javascript
frappe.query_reports["Rental Revenue"] = {
    filters: [
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            default: frappe.datetime.add_months(frappe.datetime.get_today(), -1)
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            default: frappe.datetime.get_today()
        },
        {
            fieldname: "customer",
            label: __("Customer"),
            fieldtype: "Link",
            options: "Customer"
        },
        {
            fieldname: "rental_status",
            label: __("Status"),
            fieldtype: "Select",
            options: "\nReserved\nRented\nReturned"
        }
    ],

    formatter: function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
        if (column.fieldname === "rental_status") {
            const colors = {
                "Reserved": "blue",
                "Rented": "orange",
                "Returned": "green"
            };
            const color = colors[data.rental_status] || "gray";
            value = `<span class="indicator-pill ${color}">${value}</span>`;
        }
        return value;
    }
};
```

**Step 2:** Create Number Cards for rentals

```bash
docker exec devcontainer-frappe-1 bash -c "mkdir -p /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/library/number_card/active_rentals"
docker exec devcontainer-frappe-1 bash -c "mkdir -p /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/library/number_card/total_rental_revenue"
```

File: `frappe_learn/frappe_learn/library/number_card/active_rentals/active_rentals.json`

```json
{
    "name": "Active Rentals",
    "doctype": "Number Card",
    "document_type": "Equipment Rental",
    "module": "Library",
    "label": "Active Rentals",
    "function": "Count",
    "aggregate_function_based_on": "",
    "filters_json": "[[\"Equipment Rental\",\"rental_status\",\"=\",\"Rented\"],[\"Equipment Rental\",\"docstatus\",\"=\",1]]",
    "is_standard": 1,
    "is_public": 1,
    "show_percentage_stats": 0,
    "stats_time_interval": "Daily",
    "color": "#ECAD4B",
    "type": "Document Type",
    "creation": "2026-03-17 10:00:00.000000",
    "modified": "2026-03-17 10:00:00.000000",
    "modified_by": "Administrator",
    "owner": "Administrator"
}
```

File: `frappe_learn/frappe_learn/library/number_card/total_rental_revenue/total_rental_revenue.json`

```json
{
    "name": "Total Rental Revenue",
    "doctype": "Number Card",
    "document_type": "Equipment Rental",
    "module": "Library",
    "label": "Total Rental Revenue",
    "function": "Sum",
    "aggregate_function_based_on": "total_amount",
    "filters_json": "[[\"Equipment Rental\",\"docstatus\",\"=\",1]]",
    "is_standard": 1,
    "is_public": 1,
    "show_percentage_stats": 0,
    "stats_time_interval": "Monthly",
    "color": "#29CD42",
    "type": "Document Type",
    "creation": "2026-03-17 10:00:00.000000",
    "modified": "2026-03-17 10:00:00.000000",
    "modified_by": "Administrator",
    "owner": "Administrator"
}
```

**Step 3:** Build, migrate, and test

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local migrate && bench build --app frappe_learn && bench --site flow.local clear-cache"
```

### Expected Output / Kết quả mong đợi

- Rental Revenue report at `http://localhost:8080/app/query-report/Rental Revenue`
  - Table with all rental details
  - Bar chart showing monthly revenue
  - Summary line with total revenue, active rentals, completed count
- Number Cards:
  - "Active Rentals" (orange) — count of currently rented equipment
  - "Total Rental Revenue" (green) — sum of all rental amounts

### Verification / Kiểm tra

```bash
# Check report exists
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local execute frappe.client.get_list --args '{\"doctype\": \"Report\", \"filters\": {\"name\": \"Rental Revenue\"}, \"fields\": [\"name\", \"report_type\"]}'"

# Check number cards
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local execute frappe.client.get_list --args '{\"doctype\": \"Number Card\", \"filters\": {\"module\": \"Library\"}, \"fields\": [\"name\", \"label\", \"type\"]}'"

# Test report execution
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local execute frappe_learn.frappe_learn.library.report.rental_revenue.rental_revenue.execute --args '[{}]'"
```

<details>
<summary>Hint: Adding to workspace / Gợi ý: Thêm vào workspace</summary>

Update the Library workspace JSON (from Exercise 6.5) to include the new number cards and report shortcut. Add to the `content` JSON string:

```json
{
    "id": "nc_rental",
    "type": "number_card",
    "data": {"number_card_name": "Active Rentals", "col": 6}
},
{
    "id": "nc_revenue",
    "type": "number_card",
    "data": {"number_card_name": "Total Rental Revenue", "col": 6}
}
```

And add to `shortcuts`:
```json
{
    "label": "Rental Revenue",
    "type": "Report",
    "link_to": "Rental Revenue",
    "color": "#449CF0"
}
```

Cập nhật workspace JSON để thêm number card và shortcut mới.
</details>

---

## Exercise 8.5: Code Validation / Kiểm tra chất lượng code

### Objective / Mục tiêu
Use the dcnet_quality skill to validate all code written in this module. Review for common ERPNext anti-patterns, security issues, and best practices.

Dùng dcnet_quality skill để kiểm tra tất cả code viết trong module này. Review các anti-pattern, vấn đề bảo mật, và best practices.

### Instructions / Hướng dẫn

**Step 1:** Self-review checklist / Danh sách tự kiểm tra

Go through each file and check against these rules:

**Controller (equipment_rental.py):**

| Rule | Check |
|------|-------|
| No `import frappe` in Server Scripts (only in Python files) | N/A (this is a .py file) |
| Use `doc.field` not `self.field` in Server Scripts | N/A (this is a Controller, `self` is correct) |
| No `frappe.db.*` modifications inside `on_update` | Check: use `db_set` for status updates |
| All `@frappe.whitelist()` methods validate permissions | Check: `mark_as_rented`, `mark_as_returned` |
| Use `frappe.throw()` not `raise Exception()` | Check all error handling |
| All date comparisons use `getdate()` wrapper | Check `validate_dates`, `mark_as_returned` |
| Currency calculations handle None values | Check `calculate_totals` |

**Client Script (equipment_rental.js):**

| Rule | Check |
|------|-------|
| No `frappe.db.*` calls (use `frappe.call` or `frappe.db.get_value`) | Check |
| All user-facing strings wrapped in `__()` | Check button labels, alerts |
| `frm.reload_doc()` after server calls that modify data | Check callbacks |
| Custom buttons only added in `refresh` event | Check |
| No `cur_frm` usage (use `frm` from event handler) | Check |

**Step 2:** Run manual code review

```bash
# Check for common issues in Python files
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench/apps/frappe_learn && grep -rn 'raise Exception' frappe_learn/ || echo 'No raw Exception raises found - GOOD'"
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench/apps/frappe_learn && grep -rn 'cur_frm' frappe_learn/ || echo 'No cur_frm usage found - GOOD'"
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench/apps/frappe_learn && grep -rn 'frappe.db\.' frappe_learn/**/*.js || echo 'No frappe.db in JS found - checking...'"
```

**Step 3:** Run tests for the new DocType

Create test file: `frappe_learn/frappe_learn/library/doctype/equipment_rental/test_equipment_rental.py`

```python
# Copyright (c) 2026, DCNET and contributors
# For license information, please see license.txt

import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import today, add_days


class TestEquipmentRental(IntegrationTestCase):
    """Test cases for Equipment Rental DocType."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Ensure rental item exists
        if not frappe.db.exists("Item", "TEST-RENT-001"):
            # Create Item Group if needed
            if not frappe.db.exists("Item Group", "Rental Equipment"):
                frappe.get_doc({
                    "doctype": "Item Group",
                    "item_group_name": "Rental Equipment",
                    "parent_item_group": "All Item Groups"
                }).insert()

            frappe.get_doc({
                "doctype": "Item",
                "item_code": "TEST-RENT-001",
                "item_name": "Test Rental Item",
                "item_group": "Rental Equipment",
                "stock_uom": "Nos",
                "custom_rental_available": 1,
                "custom_rental_rate": 100000,
                "custom_rental_deposit": 500000
            }).insert()

        # Ensure customer exists
        if not frappe.db.exists("Customer", "Test Rental Customer"):
            frappe.get_doc({
                "doctype": "Customer",
                "customer_name": "Test Rental Customer",
                "customer_type": "Individual",
                "customer_group": frappe.get_all("Customer Group", limit=1)[0].name,
                "territory": frappe.get_all("Territory", limit=1)[0].name
            }).insert()

        frappe.db.commit()

    def _create_rental(self, days=3):
        """Helper to create a test rental."""
        rental = frappe.get_doc({
            "doctype": "Equipment Rental",
            "customer": "Test Rental Customer",
            "item": "TEST-RENT-001",
            "rental_date": today(),
            "return_date": add_days(today(), days),
            "quantity": 1
        })
        rental.insert()
        return rental

    def test_create_rental(self):
        """Test creating a rental calculates totals correctly."""
        rental = self._create_rental(days=5)
        self.assertEqual(rental.total_days, 5)
        self.assertEqual(rental.total_amount, 100000 * 5 * 1)  # rate * days * qty

    def test_rental_workflow(self):
        """Test the full rental lifecycle: Draft -> Reserved -> Rented -> Returned."""
        rental = self._create_rental()

        # Draft
        self.assertEqual(rental.rental_status, "Draft")
        self.assertEqual(rental.docstatus, 0)

        # Submit -> Reserved
        rental.submit()
        rental.reload()
        self.assertEqual(rental.rental_status, "Reserved")
        self.assertEqual(rental.docstatus, 1)

        # Mark as Rented
        rental.mark_as_rented()
        rental.reload()
        self.assertEqual(rental.rental_status, "Rented")

        # Mark as Returned
        rental.mark_as_returned()
        rental.reload()
        self.assertEqual(rental.rental_status, "Returned")
        self.assertIsNotNone(rental.actual_return_date)

    def test_invalid_dates(self):
        """Test that return date before rental date is rejected."""
        with self.assertRaises(frappe.exceptions.ValidationError):
            rental = frappe.get_doc({
                "doctype": "Equipment Rental",
                "customer": "Test Rental Customer",
                "item": "TEST-RENT-001",
                "rental_date": today(),
                "return_date": add_days(today(), -1),  # Before rental date
                "quantity": 1
            })
            rental.insert()

    def test_non_rental_item_rejected(self):
        """Test that non-rental items are rejected."""
        # Create a non-rental item
        if not frappe.db.exists("Item", "TEST-NORENT-001"):
            frappe.get_doc({
                "doctype": "Item",
                "item_code": "TEST-NORENT-001",
                "item_name": "Non-Rental Item",
                "item_group": "All Item Groups",
                "stock_uom": "Nos",
                "custom_rental_available": 0
            }).insert()

        with self.assertRaises(frappe.exceptions.ValidationError):
            rental = frappe.get_doc({
                "doctype": "Equipment Rental",
                "customer": "Test Rental Customer",
                "item": "TEST-NORENT-001",
                "rental_date": today(),
                "return_date": add_days(today(), 3),
                "quantity": 1
            })
            rental.insert()
```

**Step 4:** Run all tests

```bash
# Run Equipment Rental tests
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local run-tests --app frappe_learn --doctype 'Equipment Rental' -v"

# Run ALL app tests
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local run-tests --app frappe_learn -v"
```

**Step 5:** Final validation summary

Create a validation report by checking all files:

```bash
docker exec devcontainer-frappe-1 bash -c '
echo "=== CODE VALIDATION REPORT ==="
echo ""
echo "1. Python files:"
find /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn -name "*.py" -not -path "*/__pycache__/*" | wc -l
echo " Python files found"

echo ""
echo "2. JavaScript files:"
find /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn -name "*.js" | wc -l
echo " JavaScript files found"

echo ""
echo "3. JSON fixtures:"
find /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn -name "*.json" -path "*/number_card/*" -o -name "*.json" -path "*/workspace/*" -o -name "*.json" -path "*/report/*" | wc -l
echo " fixture JSON files found"

echo ""
echo "4. Anti-pattern checks:"
echo -n "   raise Exception: "
grep -rn "raise Exception" /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/*.py 2>/dev/null | wc -l
echo -n "   cur_frm usage: "
grep -rn "cur_frm" /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/ 2>/dev/null | wc -l

echo ""
echo "=== END REPORT ==="
'
```

### Expected Output / Kết quả mong đợi

- All tests pass (Book tests + Equipment Rental tests)
- No `raise Exception()` in Python files
- No `cur_frm` in JavaScript files
- No `frappe.db.*` calls in Client Scripts (`.js` files)
- All whitelisted methods have proper validation
- Dates compared using `getdate()` wrapper

### Verification / Kiểm tra

```bash
# Final comprehensive test
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local run-tests --app frappe_learn -v 2>&1 | tail -20"
```

Expected output ends with:
```
----------------------------------------------------------------------
Ran X tests in Y.YYYs

OK
```

<details>
<summary>Hint: Common ERPNext code issues / Gợi ý: Các lỗi code ERPNext thường gặp</summary>

Top 5 mistakes when writing ERPNext code:

1. **Server Script: using `import`** — Server Scripts run in sandbox, use `frappe.utils.X()` directly
2. **Server Script: using `self.`** — Use `doc.field` instead
3. **Client Script: using `frappe.db.*`** — Use `frappe.call()` to call server methods
4. **Controller: modifying fields in `on_update`** — Use `frappe.db.set_value()` or `db_set()`
5. **Not using `getdate()` for date comparisons** — Raw string comparison fails

These are the #1 source of bugs in AI-generated ERPNext code.

5 lỗi thường gặp nhất: import trong Server Script, self trong Server Script, frappe.db trong Client Script, sửa field trong on_update, so sánh ngày không dùng getdate().
</details>

---

## Summary / Tóm tắt

| Exercise | Key Concept | Deliverables |
|----------|-------------|--------------|
| 8.1 | ERPNext exploration | Understanding of Company/Item/Customer structure |
| 8.2 | Custom Fields on ERPNext DocType | `install.py` with `create_custom_fields()` |
| 8.3 | Custom DocType with workflow | Equipment Rental DocType + Controller + Client Script |
| 8.4 | Script Report + Number Cards | Rental Revenue report + 2 Number Cards |
| 8.5 | Code validation + Tests | 4 test cases + validation report |

## Congratulations! / Chúc mừng!

You have completed the Frappe Academy! You now have the skills to:

- Build custom Frappe apps from scratch
- Create DocTypes with controllers and client scripts
- Write whitelisted APIs and REST endpoints
- Customize the Desk UI (forms, lists, reports, workspaces)
- Implement permissions and print formats
- Write automated tests
- Extend ERPNext with custom fields and DocTypes
- Validate code quality against ERPNext best practices

Bạn đã hoàn thành Frappe Academy! Bây giờ bạn có thể: xây dựng app Frappe, tạo DocType, viết API, tùy chỉnh giao diện, phân quyền, viết test, và mở rộng ERPNext.
