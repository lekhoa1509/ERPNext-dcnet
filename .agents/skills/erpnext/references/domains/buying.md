<!-- Source: erpnext_buying skill -->

# ERPNext Buying Module

## Overview

The ERPNext Buying module provides comprehensive purchasing and procurement functionality for managing supplier relationships, purchase orders, quotations, and procurement workflows. This module is essential for businesses that need to manage their supply chain, vendor relationships, and purchasing processes.

**Source Path:** `erpnext/buying`
**Files Analyzed:** 54 (51 Python, 3 JavaScript)
**Framework:** Frappe/ERPNext v16

## When to Use This Skill

Use this skill when working with:

### Primary Use Cases
- **Purchase Order Management**: Creating, updating, and managing purchase orders
- **Supplier Management**: Setting up suppliers, supplier groups, and supplier contacts
- **Request for Quotation (RFQ)**: Creating RFQs and collecting supplier quotations
- **Supplier Quotation**: Managing and comparing quotations from suppliers
- **Procurement Tracking**: Monitoring purchase order status, pending receipts, and billing
- **Subcontracting**: Managing subcontracting orders and raw material transfers
- **Supplier Scorecard**: Evaluating supplier performance with scoring criteria

### Trigger Conditions
- User asks about "purchase order", "PO", "buying", "procurement"
- Questions about supplier setup, supplier quotation, or RFQ
- Need to understand PO → PR → PI workflow
- Implementing supplier evaluation or scorecard
- Working with Material Request to Purchase Order conversion
- Drop shipping or inter-company purchase scenarios
- Subcontracting workflow questions

### Related Modules
- **Stock Module**: Purchase Receipt (PR) - receiving goods
- **Accounts Module**: Purchase Invoice (PI) - billing and payments
- **Manufacturing**: Subcontracting Orders
- **Selling**: Inter-company transactions, drop shipping

---

## Key Concepts

### Buying Workflow

```
Material Request → Request for Quotation → Supplier Quotation
                            ↓
                     Purchase Order
                            ↓
              ┌─────────────┴─────────────┐
              ↓                           ↓
       Purchase Receipt            Purchase Invoice
       (Stock Module)              (Accounts Module)
              ↓                           ↓
              └─────────────┬─────────────┘
                            ↓
                     Payment Entry
```

### Purchase Order Status Flow

| Status | Description |
|--------|-------------|
| Draft | PO is created but not submitted |
| To Receive and Bill | PO submitted, awaiting receipt and invoice |
| To Bill | Goods received, awaiting invoice |
| To Receive | Invoiced, awaiting goods receipt |
| Completed | Fully received and billed |
| Closed | Manually closed |
| On Hold | Temporarily on hold |
| Cancelled | PO cancelled |

### Core DocTypes

| DocType | Purpose | Controller |
|---------|---------|------------|
| **Purchase Order** | Confirmed order to supplier | `BuyingController` |
| **Supplier** | Vendor master data | `TransactionBase` |
| **Supplier Quotation** | Price quotes from suppliers | `BuyingController` |
| **Request for Quotation** | RFQ sent to multiple suppliers | `BuyingController` |
| **Supplier Scorecard** | Supplier performance evaluation | `Document` |
| **Buying Settings** | Module configuration | `Document` |

---

## Quick Reference

### Creating a Purchase Order

```python
# Create Purchase Order programmatically
import frappe

po = frappe.new_doc("Purchase Order")
po.supplier = "Supplier Name"
po.company = "Your Company"
po.schedule_date = frappe.utils.add_days(frappe.utils.today(), 7)

# Add items
po.append("items", {
    "item_code": "ITEM-001",
    "qty": 10,
    "rate": 100,
    "warehouse": "Stores - TC"
})

po.insert()
po.submit()
```

### Creating PO from Material Request

```python
# From codebase - Material Request to Purchase Order
from erpnext.stock.doctype.material_request.material_request import make_purchase_order

mr = frappe.get_doc("Material Request", "MR-00001")
po = make_purchase_order(mr.name)
po.supplier = "_Test Supplier"
po.save()
po.submit()
```

### Creating Purchase Receipt from PO

```python
# From codebase - PO to Purchase Receipt
from erpnext.buying.doctype.purchase_order.purchase_order import make_purchase_receipt

po = frappe.get_doc("Purchase Order", "PO-00001")
pr = make_purchase_receipt(po.name)
pr.insert()
pr.submit()
```

### Creating Purchase Invoice from PO

```python
# From codebase - PO to Purchase Invoice
from erpnext.buying.doctype.purchase_order.purchase_order import make_purchase_invoice

po = frappe.get_doc("Purchase Order", "PO-00001")
pi = make_purchase_invoice(po.name)

# Optional: Update stock directly with PI
pi.update_stock = 1
pi.insert()
pi.submit()
```

### RFQ to Supplier Quotation Workflow

```python
# Create RFQ and send to suppliers
rfq = frappe.new_doc("Request for Quotation")
rfq.transaction_date = frappe.utils.today()
rfq.company = "Your Company"

# Add suppliers
rfq.append("suppliers", {
    "supplier": "Supplier A",
    "email_id": "supplier_a@example.com"
})

# Add items
rfq.append("items", {
    "item_code": "ITEM-001",
    "qty": 100,
    "warehouse": "Stores - TC"
})

rfq.insert()
rfq.submit()

# Send RFQ to suppliers
rfq.send_to_supplier()
```

### Creating Supplier Quotation from RFQ

```python
# From codebase - RFQ to Supplier Quotation
from erpnext.buying.doctype.request_for_quotation.request_for_quotation import (
    make_supplier_quotation_from_rfq
)

sq = make_supplier_quotation_from_rfq(
    source_name="RFQ-00001",
    for_supplier="Supplier A"
)
sq.insert()
```

### Supplier Quotation to Purchase Order

```python
# From codebase - SQ to PO
from erpnext.buying.doctype.supplier_quotation.supplier_quotation import make_purchase_order

po = make_purchase_order(source_name="SQ-00001")
po.insert()
po.submit()
```

### Updating PO Items (After Partial Receipt)

```python
# From codebase test - Update child items
import json
from erpnext.controllers.accounts_controller import update_child_qty_rate

po = frappe.get_doc("Purchase Order", "PO-00001")
first_item = po.get("items")[0]

trans_item = json.dumps([{
    "item_code": first_item.item_code,
    "rate": 200,  # New rate
    "qty": 7,     # New qty
    "docname": first_item.name
}])

update_child_qty_rate("Purchase Order", trans_item, po.name)
```

### Close/Reopen Purchase Orders

```python
# From codebase - Bulk close/reopen POs
from erpnext.buying.doctype.purchase_order.purchase_order import close_or_unclose_purchase_orders

# Close multiple POs
close_or_unclose_purchase_orders(
    names=["PO-00001", "PO-00002"],
    status="Closed"
)

# Reopen
close_or_unclose_purchase_orders(
    names=["PO-00001"],
    status="Submitted"
)
```

### Subcontracting Order

```python
# From codebase - Create Subcontracting Order from PO
from erpnext.buying.doctype.purchase_order.purchase_order import make_subcontracting_order

sco = make_subcontracting_order(
    source_name="PO-00001",
    save=True,
    submit=True
)
```

### Supplier Scorecard

```python
# Create and calculate supplier scorecard
from erpnext.buying.doctype.supplier_scorecard.supplier_scorecard import (
    make_all_scorecards,
    refresh_scorecards
)

# Generate scorecards for a supplier
make_all_scorecards("Supplier Name")

# Refresh all scorecards (scheduled job)
refresh_scorecards()
```

---

## API Reference Summary

### Purchase Order (`purchase_order.py`)

**Class:** `PurchaseOrder` (inherits `BuyingController`)

| Method | Description |
|--------|-------------|
| `validate()` | Validates PO data before save |
| `on_submit()` | Updates ordered qty, links to SO |
| `on_cancel()` | Reverses ordered qty updates |
| `get_last_purchase_rate()` | Gets last purchase rates for items |
| `update_ordered_qty()` | Updates requested qty in Material Request |
| `update_status(status)` | Updates PO status |
| `can_update_items()` | Checks if items can be updated |
| `has_drop_ship_item()` | Checks for drop ship items |
| `auto_create_subcontracting_order()` | Auto-creates SCO on submit |

**Key Functions:**

| Function | Decorator | Description |
|----------|-----------|-------------|
| `make_purchase_receipt()` | `@frappe.whitelist()` | Creates PR from PO |
| `make_purchase_invoice()` | `@frappe.whitelist()` | Creates PI from PO |
| `make_subcontracting_order()` | `@frappe.whitelist()` | Creates SCO from PO |
| `make_inter_company_sales_order()` | `@frappe.whitelist()` | Creates SO for inter-company |
| `close_or_unclose_purchase_orders()` | `@frappe.whitelist()` | Bulk close/open POs |
| `item_last_purchase_rate()` | `@frappe.whitelist()` | Gets last purchase rate |

### Supplier (`supplier.py`)

**Class:** `Supplier` (inherits `TransactionBase`)

| Method | Description |
|--------|-------------|
| `onload()` | Loads address and contacts |
| `validate()` | Validates supplier data |
| `autoname()` | Auto-generates supplier name |
| `get_supplier_group_details()` | Gets supplier group settings |
| `create_primary_contact()` | Creates primary contact |
| `create_primary_address()` | Creates primary address |
| `validate_internal_supplier()` | Validates internal supplier setup |

### Request for Quotation (`request_for_quotation.py`)

**Class:** `RequestforQuotation` (inherits `BuyingController`)

| Method | Description |
|--------|-------------|
| `send_to_supplier()` | Sends RFQ email to suppliers |
| `get_supplier_email_preview()` | Previews email content |
| `update_supplier_contact()` | Creates/updates supplier contact |
| `update_rfq_supplier_status()` | Updates supplier response status |

**Key Functions:**

| Function | Description |
|----------|-------------|
| `make_supplier_quotation_from_rfq()` | Creates SQ from RFQ |
| `send_supplier_emails()` | Sends emails to all suppliers |
| `get_pdf()` | Generates PDF for supplier |

### Supplier Quotation (`supplier_quotation.py`)

**Class:** `SupplierQuotation` (inherits `BuyingController`)

| Method | Description |
|--------|-------------|
| `validate_valid_till()` | Validates quotation validity date |
| `update_rfq_supplier_status()` | Updates RFQ with SQ status |

**Key Functions:**

| Function | Description |
|----------|-------------|
| `make_purchase_order()` | Creates PO from SQ |
| `make_purchase_invoice()` | Creates PI from SQ |
| `make_quotation()` | Creates Sales Quotation from SQ |
| `set_expired_status()` | Marks expired quotations |

### Supplier Scorecard (`supplier_scorecard.py`)

**Class:** `SupplierScorecard` (inherits `Document`)

| Method | Description |
|--------|-------------|
| `validate_standings()` | Validates standing thresholds |
| `validate_criteria_weights()` | Ensures weights sum to 100 |
| `calculate_total_score()` | Calculates supplier score |
| `update_standing()` | Updates supplier standing |

**Key Functions:**

| Function | Description |
|----------|-------------|
| `refresh_scorecards()` | Scheduled job to refresh all |
| `make_all_scorecards()` | Creates scorecard periods |
| `make_default_records()` | Creates default criteria |

---

## Reports

| Report | File | Description |
|--------|------|-------------|
| **Purchase Order Analysis** | `purchase_order_analysis.py` | Pending/completed PO analysis |
| **Purchase Order Trends** | `purchase_order_trends.py` | PO trends over time |
| **Purchase Analytics** | `purchase_analytics.py` | Supplier/item purchase analytics |
| **Procurement Tracker** | `procurement_tracker.py` | Track MR → PO → PR → PI |
| **Item-wise Purchase History** | `item_wise_purchase_history.py` | Purchase history by item |
| **Supplier Quotation Comparison** | `supplier_quotation_comparison.py` | Compare supplier prices |
| **Requested Items to Order** | `requested_items_to_order_and_receive.py` | Pending MR items |
| **Subcontract Order Summary** | `subcontract_order_summary.py` | SCO status summary |
| **Subcontracted Items to Receive** | `subcontracted_item_to_be_received.py` | Pending SCO items |

---

## Configuration (Buying Settings)

**DocType:** `Buying Settings`

| Setting | Description |
|---------|-------------|
| `supp_master_name` | Supplier naming series |
| `supplier_group` | Default supplier group |
| `buying_price_list` | Default buying price list |
| `maintain_same_rate` | Enforce same rate across transactions |
| `allow_multiple_items` | Allow multiple same items in PO |
| `subcontract_fetch_exploded` | Fetch BOM exploded items |
| `backflush_raw_materials` | Auto backflush raw materials |
| `over_billing_allowance` | Allowed over-billing percentage |
| `allow_unit_price_items` | Allow items with 0 qty (unit price) |

---

## Design Patterns Detected

| Pattern | Count | Description |
|---------|-------|-------------|
| **Factory** | 5 | Document mapping/creation functions |
| **Observer** | 5 | Event hooks (on_submit, on_cancel) |
| **Strategy** | 1 | Configurable validation strategies |

---

## Test Examples

### Complete PO Workflow Test

```python
# From test_purchase_order.py - Complete workflow
def test_purchase_order_invoice_receipt_workflow():
    from erpnext.accounts.doctype.purchase_invoice.purchase_invoice import make_purchase_receipt

    # Create PO
    po = create_purchase_order()

    # Create PI from PO
    pi = make_pi_from_po(po.name)
    pi.submit()

    # Create PR from PI
    pr = make_purchase_receipt(pi.name)
    pr.submit()

    # Verify completion
    pi.load_from_db()
    assert pi.per_received == 100.0

    po.load_from_db()
    assert po.per_received == 100.0
    assert po.per_billed == 100.0
```

### Material Request to PO with Updates

```python
# From test_purchase_order.py - MR → PO with item updates
def test_update_child():
    mr = make_material_request(qty=10)
    po = make_purchase_order(mr.name)
    po.supplier = '_Test Supplier'
    po.items[0].qty = 4
    po.save()
    po.submit()

    # Partial receipt
    create_pr_against_po(po.name)

    # Update PO items
    trans_item = json.dumps([{
        'item_code': '_Test Item',
        'rate': 200,
        'qty': 7,
        'docname': po.items[0].name
    }])

    update_child_qty_rate('Purchase Order', trans_item, po.name)

    # Verify MR ordered qty updated
    mr.reload()
    assert mr.items[0].ordered_qty == 7
    assert mr.per_ordered == 70
```

### Return Against Purchase Order

```python
# From test_purchase_order.py - Purchase returns
def test_return_against_purchase_order():
    po = create_purchase_order()
    pr = make_pr_against_po(po.name, 6)

    # Create return receipt
    pr_return = make_purchase_receipt(
        is_return=1,
        return_against=pr.name,
        qty=-3,
        do_not_submit=True
    )
    pr_return.items[0].purchase_order = po.name
    pr_return.items[0].purchase_order_item = po.items[0].name
    pr_return.submit()

    # Verify received qty reduced
    po.load_from_db()
    assert po.get('items')[0].received_qty == 3
```

---

## Working with This Skill

### For Beginners

1. Start with understanding the basic workflow: Material Request → Purchase Order → Purchase Receipt → Purchase Invoice
2. Review the Supplier master setup and required fields
3. Understand PO status transitions
4. Practice creating simple POs programmatically

### For Intermediate Users

1. Explore RFQ → Supplier Quotation → PO workflow
2. Learn about `update_child_qty_rate()` for modifying submitted POs
3. Understand drop shipping and inter-company transactions
4. Implement supplier scorecard evaluation

### For Advanced Users

1. Customize BuyingController for specific business logic
2. Extend supplier evaluation with custom criteria
3. Implement automated procurement based on reorder levels
4. Build custom reports using buying data

### Navigation Tips

- **API Reference**: `references/api_reference/` - All class/function documentation
- **Test Examples**: `references/test_examples/` - Real-world usage patterns
- **Configuration**: `references/config_patterns/` - DocType configurations
- **Dependencies**: `references/dependencies/` - Module relationships

---

## Available Reference Files

| Directory | Content |
|-----------|---------|
| `references/api_reference/` | Complete API documentation for all modules |
| `references/documentation/` | Project README files and descriptions |
| `references/patterns/` | Detected design patterns analysis |
| `references/test_examples/` | Extracted test workflows |
| `references/config_patterns/` | Configuration file analysis |
| `references/dependencies/` | Module dependency graphs |

### Key Reference Files

| File | Description |
|------|-------------|
| `api_reference/purchase_order.md` | Purchase Order API (40+ methods) |
| `api_reference/supplier.md` | Supplier master API |
| `api_reference/request_for_quotation.md` | RFQ workflow API |
| `api_reference/supplier_quotation.md` | Supplier Quotation API |
| `api_reference/supplier_scorecard.md` | Scorecard evaluation API |
| `api_reference/buying_settings.md` | Module settings API |

---

## Integration Points

### With Stock Module

```python
# Purchase Order links to Purchase Receipt
po.items[0].received_qty  # Updated by PR
po.per_received           # Overall receipt percentage
```

### With Accounts Module

```python
# Purchase Order links to Purchase Invoice
po.items[0].billed_amt    # Updated by PI
po.per_billed             # Overall billing percentage
```

### With Manufacturing Module

```python
# Subcontracting workflow
po.is_subcontracted       # Flag for subcontracting
po.supplier_warehouse     # Raw material warehouse
po.auto_create_subcontracting_order()
```

### With Selling Module

```python
# Drop shipping
po.items[0].sales_order           # Linked SO
po.items[0].sales_order_item      # Linked SO item
po.update_delivered_qty_in_sales_order()  # Updates SO delivery
```

---

**Generated by Skill Seeker** | ERPNext Buying Module Analysis

*Last Updated: Based on ERPNext v16 codebase*
