# How To: Batched Serial No Purchase

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test batched serial no purchase

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `pypika`
- `erpnext`
- `erpnext.controllers`
- `erpnext.controllers.status_updater`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.buying.doctype.supplier.test_supplier`
- `erpnext.controllers.accounts_controller`
- `erpnext.controllers.buying_controller`
- `erpnext.stock`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.serial_and_batch_bundle.serial_and_batch_bundle`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.selling.doctype.customer.test_customer`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.stock.get_item_details`
- `erpnext.stock.utils`
- `erpnext.buying.doctype.purchase_order`
- `erpnext.buying.doctype.purchase_order`
- `erpnext.accounts.doctype.purchase_invoice.purchase_invoice`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.accounts.party`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.accounts.doctype.sales_invoice.sales_invoice`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.get_item_details`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.landed_cost_voucher.test_landed_cost_voucher`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.buying.doctype.supplier.test_supplier`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.serial_no.serial_no`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.accounts.doctype.purchase_invoice.purchase_invoice`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.landed_cost_voucher.test_landed_cost_voucher`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.report.stock_balance.stock_balance`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.landed_cost_voucher.test_landed_cost_voucher`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.stock_ledger`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.stock_ledger`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`

**Setup Required:**
```python
frappe.db.set_single_value('Buying Settings', 'allow_multiple_items', 1)
```

## Step-by-Step Guide

### Step 1: Assign item = frappe.db.exists(...)

```python
item = frappe.db.exists('Item', {'item_name': 'Batched Serialized Item'})
```

### Step 2: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(item_code=item.name, qty=5, rate=500)
```

### Step 3: Call self.assertTrue()

```python
self.assertTrue(frappe.db.get_value('Batch', {'item': item.name, 'reference_name': pr.name}))
```

### Step 4: Call pr.load_from_db()

```python
pr.load_from_db()
```

### Step 5: Call pr.cancel()

```python
pr.cancel()
```

### Step 6: Assign item = create_item(...)

```python
item = create_item('Batched Serialized Item')
```

### Step 7: Assign item.has_batch_no = 1

```python
item.has_batch_no = 1
```

### Step 8: Assign item.create_new_batch = 1

```python
item.create_new_batch = 1
```

### Step 9: Assign item.has_serial_no = 1

```python
item.has_serial_no = 1
```

### Step 10: Assign item.batch_number_series = 'BS-BATCH-.##'

```python
item.batch_number_series = 'BS-BATCH-.##'
```

### Step 11: Assign item.serial_no_series = 'BS-.####'

```python
item.serial_no_series = 'BS-.####'
```

### Step 12: Call item.save()

```python
item.save()
```

### Step 13: Assign item = frappe.get_doc(...)

```python
item = frappe.get_doc('Item', {'item_name': 'Batched Serialized Item'})
```


## Complete Example

```python
# Setup
frappe.db.set_single_value('Buying Settings', 'allow_multiple_items', 1)

# Workflow
item = frappe.db.exists('Item', {'item_name': 'Batched Serialized Item'})
if not item:
    item = create_item('Batched Serialized Item')
    item.has_batch_no = 1
    item.create_new_batch = 1
    item.has_serial_no = 1
    item.batch_number_series = 'BS-BATCH-.##'
    item.serial_no_series = 'BS-.####'
    item.save()
else:
    item = frappe.get_doc('Item', {'item_name': 'Batched Serialized Item'})
pr = make_purchase_receipt(item_code=item.name, qty=5, rate=500)
self.assertTrue(frappe.db.get_value('Batch', {'item': item.name, 'reference_name': pr.name}))
pr.load_from_db()
pr.cancel()
```

## Next Steps


---

*Source: test_purchase_receipt.py:202 | Complexity: Advanced | Last updated: 2026-02-04*