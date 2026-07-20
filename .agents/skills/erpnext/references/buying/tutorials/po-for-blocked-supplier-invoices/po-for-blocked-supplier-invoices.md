# How To: Po For Blocked Supplier Invoices

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test po for blocked supplier invoices

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `frappe.utils.data`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.accounts.party`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.controllers.accounts_controller`
- `erpnext.manufacturing.doctype.blanket_order.test_blanket_order`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.material_request.material_request`
- `erpnext.stock.doctype.material_request.test_material_request`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.controllers.tests.test_subcontracting_controller`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.selling.doctype.customer.test_customer`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.accounts.doctype.purchase_invoice.purchase_invoice`
- `erpnext.stock.utils`
- `erpnext.utilities.transaction_base`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.accounts.doctype.sales_invoice.sales_invoice`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.controllers.tests.test_subcontracting_controller`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.controllers.tests.test_subcontracting_controller`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.payment_request.payment_request`
- `erpnext.accounts.doctype.purchase_invoice.purchase_invoice`


## Step-by-Step Guide

### Step 1: Assign supplier = frappe.get_doc(...)

```python
supplier = frappe.get_doc('Supplier', '_Test Supplier')
```

### Step 2: Assign supplier.on_hold = 1

```python
supplier.on_hold = 1
```

### Step 3: Assign supplier.hold_type = 'Invoices'

```python
supplier.hold_type = 'Invoices'
```

### Step 4: Call supplier.save()

```python
supplier.save()
```

### Step 5: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, create_purchase_order)
```

### Step 6: Assign supplier.on_hold = 0

```python
supplier.on_hold = 0
```

### Step 7: Call supplier.save()

```python
supplier.save()
```


## Complete Example

```python
# Workflow
supplier = frappe.get_doc('Supplier', '_Test Supplier')
supplier.on_hold = 1
supplier.hold_type = 'Invoices'
supplier.save()
self.assertRaises(frappe.ValidationError, create_purchase_order)
supplier.on_hold = 0
supplier.save()
```

## Next Steps


---

*Source: test_purchase_order.py:639 | Complexity: Intermediate | Last updated: 2026-02-04*