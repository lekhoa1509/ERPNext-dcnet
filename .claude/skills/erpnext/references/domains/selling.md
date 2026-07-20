<!-- Source: erpnext_selling skill -->

# ERPNext Selling Module

## Description

Comprehensive reference for ERPNext's Selling module, covering the complete sales cycle from quotation to delivery. This skill synthesizes knowledge from codebase analysis including API documentation, test examples, and real-world usage patterns.

**Source Path:** `/Users/vovanduc/Code/dcnet/erpnext/erpnext/selling`
**Files Analyzed:** 71
**Languages:** Python (85.9%), JavaScript (14.1%)
**Confidence Level:** High (extracted from actual codebase)

---

## When to Use This Skill

Use this skill when working with ERPNext selling functionality:

### Primary Use Cases

| Scenario | Description |
|----------|-------------|
| **Sales Order Management** | Create, update, close, or cancel Sales Orders; handle delivery and billing status |
| **Quotation Workflow** | Convert Quotations to Sales Orders; manage validity dates; track lost quotations |
| **Customer Management** | Create customers from leads; manage credit limits; handle customer groups |
| **Product Bundles** | Configure product bundles; understand packed item behavior in transactions |
| **Point of Sale** | POS operations, item search, cart management, payment processing |
| **Sales Reports** | Sales analytics, quotation trends, customer acquisition reports |
| **Stock Reservation** | Reserved qty calculations, over-delivery handling, packing list scenarios |

### Trigger Keywords

- Sales Order, SO, Quotation, Customer, Product Bundle
- Delivery Note, Sales Invoice, POS, Point of Sale
- Credit Limit, Reserved Qty, Over Delivery
- Quotation to Sales Order conversion
- `make_sales_order`, `make_delivery_note`, `make_sales_invoice`

---

## Key Concepts

### Sales Order Status Flow

```
Draft → Submitted → To Deliver and Bill → To Deliver → To Bill → Completed
                                      ↓
                                   Closed/Cancelled
```

**Status Definitions:**
- **To Deliver and Bill**: Items need both delivery and billing
- **To Deliver**: Items are billed but not yet delivered
- **To Bill**: Items are delivered but not yet billed
- **Completed**: Fully delivered and billed
- **Closed**: Manually closed (releases reserved stock)

### Document Creation Flow

```
Quotation → Sales Order → Delivery Note → Sales Invoice → Payment Entry
                      ↘ Purchase Order (for drop shipping)
                      ↘ Work Order (for manufacturing)
                      ↘ Pick List (for warehouse operations)
```

### Reserved Quantity Logic

When a Sales Order is submitted:
1. Reserved qty increases in Bin for the warehouse
2. On partial delivery, reserved qty decreases proportionally
3. On cancellation or closing, reserved qty is released
4. Over-delivery allowance is configurable per item

---

## Quick Reference

### Core DocTypes

| DocType | Purpose | Key Fields |
|---------|---------|------------|
| **Sales Order** | Confirmed sales commitment | customer, items, delivery_date, status |
| **Quotation** | Price quote to customer/lead | quotation_to, party_name, valid_till |
| **Customer** | Customer master | customer_name, customer_group, territory |
| **Product Bundle** | Non-stock item containing stock items | new_item_code, items |
| **Selling Settings** | Module configuration | customer_group, territory, price_list |

### Essential Functions

#### Sales Order Operations

```python
# Create Sales Order from Quotation
from erpnext.selling.doctype.quotation.quotation import make_sales_order
so = make_sales_order(quotation_name)
so.insert()
so.submit()

# Create Delivery Note from Sales Order
from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note
dn = make_delivery_note(sales_order_name)
dn.insert()
dn.submit()

# Create Sales Invoice from Sales Order
from erpnext.selling.doctype.sales_order.sales_order import make_sales_invoice
si = make_sales_invoice(sales_order_name)
si.insert()
si.submit()

# Close/Unclose Sales Orders
from erpnext.selling.doctype.sales_order.sales_order import close_or_unclose_sales_orders
close_or_unclose_sales_orders(["SO-00001", "SO-00002"], "Closed")
```

#### Customer Operations

```python
# Create Quotation from Customer
from erpnext.selling.doctype.customer.customer import make_quotation
quotation = make_quotation(customer_name)

# Check Credit Limit
from erpnext.selling.doctype.customer.customer import check_credit_limit
check_credit_limit(customer, company, ignore_outstanding_sales_order=False)

# Get Credit Limit
from erpnext.selling.doctype.customer.customer import get_credit_limit
limit = get_credit_limit(customer, company)

# Get Customer Outstanding
from erpnext.selling.doctype.customer.customer import get_customer_outstanding
outstanding = get_customer_outstanding(customer, company)
```

#### Update Sales Order Items (after submit)

```python
from erpnext.controllers.accounts_controller import update_child_qty_rate
import json

# Prepare items data
trans_item = json.dumps([
    {
        'item_code': 'ITEM-001',
        'rate': 100,
        'qty': 5,
        'docname': so.items[0].name  # existing row
    },
    {
        'item_code': 'ITEM-002',  # new item
        'rate': 200,
        'qty': 3
    }
])

update_child_qty_rate('Sales Order', trans_item, so.name)
```

---

## Code Examples

### 1. Complete Sales Cycle (From Codebase Tests)

**Create Sales Order and Track Status**

```python
# Create a basic sales order
so = make_sales_order(
    item_code='_Test Item',
    qty=10,
    rate=100,
    customer='_Test Customer'
)

# Check initial status
assert so.status == 'To Deliver and Bill'

# Create partial delivery
dn = make_delivery_note(so.name)
dn.items[0].qty = 5
dn.insert()
dn.submit()

# Reload and verify
so.load_from_db()
assert so.items[0].delivered_qty == 5
assert so.status == 'To Deliver and Bill'

# Complete delivery
dn2 = make_delivery_note(so.name)
dn2.insert()
dn2.submit()

so.load_from_db()
assert so.items[0].delivered_qty == 10
assert so.status == 'To Bill'
```

*Source: test_sales_order.py*

### 2. Sales Returns with Sales Order Link

```python
from erpnext.accounts.doctype.sales_invoice.sales_invoice import make_sales_return
from erpnext.stock.doctype.delivery_note.test_delivery_note import create_delivery_note

# Original flow
so = make_sales_order()
dn = create_dn_against_so(so.name, 6)
si = make_sales_invoice(so.name)
si.update_stock = 1
si.items[0].qty = 3
si.insert()
si.submit()

# Create delivery note return
dn_return = create_delivery_note(
    is_return=1,
    return_against=dn.name,
    qty=-3,
    do_not_submit=True
)
dn_return.items[0].against_sales_order = so.name
dn_return.items[0].so_detail = so.items[0].name
dn_return.submit()

# Create invoice return
si_return = make_sales_return(si.name)
si_return.update_billed_amount_in_sales_order = 1
si_return.submit()

# Verify SO reflects returns
so.load_from_db()
assert so.items[0].delivered_qty == 5  # 6 + 3 - 3 - 1
```

*Source: test_sales_order.py:271*

### 3. Over-Delivery with Allowance

```python
from erpnext.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry

# Setup stock
make_stock_entry(target='_Test Warehouse - _TC', qty=10, rate=100)

# Configure over-delivery allowance
frappe.db.set_value('Item', '_Test Item', 'over_delivery_receipt_allowance', 50)
frappe.db.set_value('Item', '_Test Item', 'over_billing_allowance', 20)

# Create sales order for 10 qty
existing_reserved_qty = get_reserved_qty()
so = make_sales_order(qty=10)

# Reserved qty should increase
assert get_reserved_qty() == existing_reserved_qty + 10

# Deliver 12 items (over-delivery)
si = make_sales_invoice(so.name)
si.update_stock = 1
si.items[0].qty = 12
si.insert()
si.submit()

# Verify over-delivery processed correctly
so.load_from_db()
assert so.items[0].delivered_qty == 12
assert so.per_delivered == 100  # Marked as 100% delivered
assert get_reserved_qty() == existing_reserved_qty  # Reserved qty released
```

*Source: test_sales_order.py:353*

### 4. Product Bundle Reserved Quantity

```python
# Create stock for bundle components
make_stock_entry(
    target='_Test Warehouse - _TC',
    item='_Test Item',
    qty=10,
    rate=100
)
make_stock_entry(
    target='_Test Warehouse - _TC',
    item='_Test Item Home Desktop 100',
    qty=10,
    rate=100
)

# Track initial reserved qty
existing_qty_item1 = get_reserved_qty('_Test Item')
existing_qty_item2 = get_reserved_qty('_Test Item Home Desktop 100')

# Create SO with product bundle
so = make_sales_order(item_code='_Test Product Bundle Item', qty=10)

# Bundle reserves component items, not bundle itself
# If bundle has 5x Item1 and 2x Item2 per unit:
assert get_reserved_qty('_Test Item') == existing_qty_item1 + 50
assert get_reserved_qty('_Test Item Home Desktop 100') == existing_qty_item2 + 20

# Partial delivery releases proportionally
dn = create_dn_against_so(so.name, qty=5)  # 50% delivery
assert get_reserved_qty('_Test Item') == existing_qty_item1 + 25
assert get_reserved_qty('_Test Item Home Desktop 100') == existing_qty_item2 + 10

# Close SO releases all reserved qty
so.update_status('Closed')
assert get_reserved_qty('_Test Item') == existing_qty_item1
assert get_reserved_qty('_Test Item Home Desktop 100') == existing_qty_item2
```

*Source: test_sales_order.py:384*

### 5. Quotation to Sales Order Conversion

```python
# Quotation with alternatives
quotation = frappe.get_doc({
    'doctype': 'Quotation',
    'quotation_to': 'Customer',
    'party_name': '_Test Customer',
    'items': [
        {'item_code': 'Item A', 'qty': 5, 'rate': 100},
        {'item_code': 'Item B', 'qty': 5, 'rate': 90, 'is_alternative': 1}
    ]
})
quotation.insert()
quotation.submit()

# Convert to Sales Order (only non-alternative items by default)
from erpnext.selling.doctype.quotation.quotation import make_sales_order
so = make_sales_order(quotation.name)
so.insert()

# Quotation marked as ordered
quotation.load_from_db()
assert quotation.status == 'Ordered'
```

*Source: quotation.py - can_map_row() logic*

### 6. Point of Sale Item Search

```python
from erpnext.selling.page.point_of_sale.point_of_sale import (
    get_items,
    search_by_term,
    search_for_serial_or_batch_or_barcode_number
)

# Search items for POS
items = get_items(
    start=0,
    page_length=40,
    price_list='Standard Selling',
    item_group='All Item Groups',
    pos_profile='My POS Profile',
    search_term='golf'
)

# Search by barcode/serial/batch
result = search_for_serial_or_batch_or_barcode_number('BARCODE123')
# Returns: {'item_code': 'ITEM-001', 'batch_no': None, 'serial_no': None}

# Search with warehouse and price list
items = search_by_term(
    search_term='TaylorMade',
    warehouse='Stores - TC',
    price_list='Standard Selling'
)
```

*Source: point_of_sale.py*

### 7. Sales Order Analysis Report

```python
from erpnext.selling.report.sales_order_analysis.sales_order_analysis import execute

# Run analysis report
columns, data, message, chart = execute({
    'company': '_Test Company',
    'from_date': '2021-06-01',
    'to_date': '2021-06-30',
    'status': ['To Deliver and Bill']  # Filter by status
})

# Report data structure
for row in data:
    print(f"SO: {row['sales_order']}")
    print(f"Status: {row['status']}")
    print(f"Qty: {row['qty']}, Delivered: {row['delivered_qty']}")
    print(f"Pending: {row['pending_qty']}, To Bill: {row['qty_to_bill']}")
    print(f"Delay Days: {row['delay_days']}")
```

*Source: test_sales_order_analysis.py*

---

## API Reference

### Sales Order (`doctype/sales_order/sales_order.py`)

**Class: SalesOrder** (inherits SellingController)

| Method | Description |
|--------|-------------|
| `can_update_items()` | Returns True if items can be modified after submit |
| `update_status(status)` | Update SO status (e.g., 'Closed', 'Draft') |
| `update_reserved_qty(so_item_rows)` | Recalculate reserved qty for specified items |
| `create_stock_reservation_entries()` | Create stock reservations for items |
| `cancel_stock_reservation_entries()` | Cancel stock reservations |
| `has_unreserved_stock()` | Returns True if any item has unreserved stock |
| `check_credit_limit()` | Validate customer credit limit |

**Whitelisted Functions:**

| Function | Description |
|----------|-------------|
| `make_material_request(source_name)` | Create Material Request from SO |
| `make_delivery_note(source_name)` | Create Delivery Note from SO |
| `make_sales_invoice(source_name)` | Create Sales Invoice from SO |
| `make_purchase_order(source_name, selected_items)` | Create PO for drop shipping |
| `make_work_orders(items, sales_order, company)` | Create Work Orders for manufacturing |
| `create_pick_list(source_name)` | Create Pick List from SO |
| `close_or_unclose_sales_orders(names, status)` | Bulk close/unclose SOs |

### Quotation (`doctype/quotation/quotation.py`)

**Class: Quotation** (inherits SellingController)

| Method | Description |
|--------|-------------|
| `get_ordered_status()` | Check if quotation is fully/partially ordered |
| `is_fully_ordered()` | Returns True if all items are in Sales Orders |
| `declare_enquiry_lost(reasons, competitors)` | Mark quotation as lost |
| `set_has_alternative_item()` | Mark rows with alternative items |

**Whitelisted Functions:**

| Function | Description |
|----------|-------------|
| `make_sales_order(source_name)` | Convert Quotation to Sales Order |
| `make_sales_invoice(source_name)` | Create Sales Invoice directly |
| `create_customer_from_lead(lead_name)` | Create Customer from Lead |

### Customer (`doctype/customer/customer.py`)

**Class: Customer** (inherits TransactionBase)

| Method | Description |
|--------|-------------|
| `update_lead_status()` | Update lead to 'Converted' status |
| `create_primary_contact()` | Create primary contact from customer data |
| `create_primary_address()` | Create primary address from customer data |
| `set_loyalty_program()` | Auto-assign loyalty program |
| `get_customer_group_details()` | Get default values from customer group |

**Whitelisted Functions:**

| Function | Description |
|----------|-------------|
| `make_quotation(source_name)` | Create Quotation for customer |
| `make_opportunity(source_name)` | Create Opportunity for customer |
| `make_payment_entry(source_name)` | Create Payment Entry for customer |
| `check_credit_limit(customer, company)` | Validate credit limit |
| `get_credit_limit(customer, company)` | Get customer's credit limit |
| `get_customer_outstanding(customer, company)` | Get outstanding amount |
| `parse_full_name(full_name)` | Split name into first/middle/last |

### Product Bundle (`doctype/product_bundle/product_bundle.py`)

**Class: ProductBundle** (inherits Document)

| Method | Description |
|--------|-------------|
| `validate_main_item()` | Ensure main item is not a stock item |
| `validate_child_items()` | Validate bundle component items |

**Important:** Product Bundle items (parent) must be non-stock items. Child items must be stock items.

---

## Design Patterns Detected

*From codebase analysis (confidence > 0.7)*

| Pattern | Count | Usage |
|---------|-------|-------|
| **Factory** | 11 | Document creation functions (make_sales_order, make_delivery_note, etc.) |
| **Observer** | 5 | Status updates triggering related document updates |
| **Command** | 1 | Batch operations (close_or_unclose_sales_orders) |

---

## Reports Reference

| Report | Path | Description |
|--------|------|-------------|
| **Sales Order Analysis** | `report/sales_order_analysis/` | SO status, delivery, billing analysis |
| **Quotation Trends** | `report/quotation_trends/` | Quotation trends over time |
| **Lost Quotations** | `report/lost_quotations/` | Analysis by lost reason/competitor |
| **Customer Credit Balance** | `report/customer_credit_balance/` | Credit limit utilization |
| **Inactive Customers** | `report/inactive_customers/` | Customers without recent transactions |
| **Sales Analytics** | `report/sales_analytics/` | Sales by customer/item/territory |
| **Item Wise Sales History** | `report/item_wise_sales_history/` | Historical sales by item |
| **Payment Terms Status** | `report/payment_terms_status_for_sales_order/` | Payment schedule tracking |
| **Sales Funnel** | `page/sales_funnel/` | Visual sales pipeline |

---

## Available Reference Files

### API Documentation (`references/api_reference/`)

| File | Description | Confidence |
|------|-------------|------------|
| `sales_order.md` | Sales Order DocType and functions | High |
| `quotation.md` | Quotation DocType and conversion | High |
| `customer.md` | Customer management and credit | High |
| `product_bundle.md` | Product Bundle configuration | High |
| `selling_settings.md` | Module settings | High |
| `point_of_sale.md` | POS page functions | High |
| `pos_*.md` | POS JavaScript components | Medium |
| `sales_analytics.md` | Analytics report | High |
| `sales_funnel.md` | Sales funnel page | High |

### Test Examples (`references/test_examples/`)

**Total Examples:** 86 (High confidence: 86)
**Categories:**
- Workflow: 52 examples
- Instantiation: 28 examples
- Config: 4 examples
- Method Call: 2 examples

### Tutorials (`references/tutorials/`)

Step-by-step guides extracted from test cases:
- `01-so-to-deliver-and-bill/` - Complete SO workflow
- `so-billed-amount-against-return-entry/` - Returns handling
- `update-child-adding-new-item/` - Modify SO after submit
- `reserved-qty-for-partial-delivery-with-packing-list/` - Bundle delivery
- `customer-credit-limit/` - Credit limit validation

---

## Working with This Skill

### For Beginners

1. Start with the **Key Concepts** section to understand the document flow
2. Review **Quick Reference** for common operations
3. Use tutorials in `references/tutorials/` for step-by-step guidance

### For Intermediate Users

1. Check **Code Examples** for real-world patterns
2. Explore **API Reference** for detailed function signatures
3. Review test examples in `references/test_examples/` for edge cases

### For Advanced Users

1. Examine `references/api_reference/` for complete API documentation
2. Study design patterns for architectural understanding
3. Use `references/patterns/` for pattern implementation details

### Navigation Tips

```bash
# Find specific function
grep -r "make_sales_order" references/api_reference/

# Find test examples for a feature
grep -r "credit_limit" references/test_examples/

# List all tutorials
ls references/tutorials/
```

---

## Common Patterns & Best Practices

### 1. Always Reload After Related Doc Changes

```python
so.load_from_db()  # After DN/SI submission
```

### 2. Use Proper Status Updates

```python
# Don't manually set status
so.status = 'Closed'  # Wrong

# Use the method
so.update_status('Closed')  # Correct - handles reserved qty
```

### 3. Handle Over-Delivery Properly

```python
# Check item settings
item = frappe.get_doc('Item', item_code)
allowance = item.over_delivery_receipt_allowance or 0
```

### 4. Credit Limit Validation

```python
# Always check before SO submission
from erpnext.selling.doctype.customer.customer import check_credit_limit
try:
    check_credit_limit(customer, company)
except frappe.ValidationError as e:
    # Handle credit limit exceeded
    pass
```

---

## Troubleshooting

### Reserved Qty Not Released

**Symptom:** Reserved qty remains after SO cancelled

**Solution:**
```python
so.update_reserved_qty()
# or
so.update_status('Closed')
```

### Quotation Not Converting

**Symptom:** `make_sales_order` returns empty document

**Check:**
1. Quotation status is 'Submitted'
2. `valid_till` date has not passed
3. Items have adequate qty (not already ordered)

### Credit Limit Bypass

**Symptom:** SO submitted despite exceeded credit limit

**Check:**
1. User has 'Credit Controller' role
2. `ignore_outstanding_sales_order` setting
3. Customer-specific credit limit vs company default

---

**Generated from ERPNext Codebase Analysis**
**Last Updated:** 2026-02-04
**Analysis Depth:** Full (C2.5, C2.6, C3.1, C3.2, C3.4, C3.7, C3.9)
