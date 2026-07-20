# How To: Duplicate Serial Nos

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test duplicate serial nos

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
item = frappe.db.exists('Item', {'item_name': 'Test Serialized Item 123'})
```

### Step 2: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(item_code=item.name, qty=2, rate=500)
```

### Step 3: Call pr.load_from_db()

```python
pr.load_from_db()
```

### Step 4: Assign bundle_id = frappe.db.get_value(...)

```python
bundle_id = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Purchase Receipt', 'voucher_no': pr.name, 'item_code': item.name}, 'serial_and_batch_bundle')
```

### Step 5: Assign serial_nos = get_serial_nos_from_bundle(...)

```python
serial_nos = get_serial_nos_from_bundle(bundle_id)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(get_serial_nos_from_bundle(pr.items[0].serial_and_batch_bundle), serial_nos)
```

### Step 7: Assign bundle_id = make_serial_batch_bundle(...)

```python
bundle_id = make_serial_batch_bundle(frappe._dict({'item_code': item.item_code, 'warehouse': '_Test Warehouse 2 - _TC1', 'company': '_Test Company 1', 'qty': 2, 'voucher_type': 'Purchase Receipt', 'serial_nos': serial_nos, 'posting_date': today(), 'posting_time': nowtime(), 'do_not_save': True}))
```

### Step 8: Call self.assertRaises()

```python
self.assertRaises(SerialNoDuplicateError, bundle_id.make_serial_and_batch_bundle)
```

### Step 9: Assign dn = create_delivery_note(...)

```python
dn = create_delivery_note(item_code=item.name, qty=2, rate=1500, serial_no=serial_nos)
```

### Step 10: Call dn.load_from_db()

```python
dn.load_from_db()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(get_serial_nos_from_bundle(dn.items[0].serial_and_batch_bundle), serial_nos)
```

### Step 12: Assign posting_date = add_days(...)

```python
posting_date = add_days(today(), -3)
```

### Step 13: Assign bundle_id = make_serial_batch_bundle(...)

```python
bundle_id = make_serial_batch_bundle(frappe._dict({'item_code': item.item_code, 'warehouse': '_Test Warehouse - _TC', 'company': '_Test Company', 'qty': 2, 'rate': 500, 'voucher_type': 'Purchase Receipt', 'serial_nos': serial_nos, 'posting_date': posting_date, 'posting_time': nowtime(), 'do_not_save': True}))
```

### Step 14: Call self.assertRaises()

```python
self.assertRaises(SerialNoExistsInFutureTransactionError, bundle_id.make_serial_and_batch_bundle)
```

### Step 15: Assign bundle_id = make_serial_batch_bundle(...)

```python
bundle_id = make_serial_batch_bundle(frappe._dict({'item_code': item.item_code, 'warehouse': '_Test Warehouse 2 - _TC1', 'company': '_Test Company 1', 'qty': 2, 'rate': 500, 'voucher_type': 'Purchase Receipt', 'serial_nos': serial_nos, 'posting_date': posting_date, 'posting_time': nowtime(), 'do_not_save': True}))
```

### Step 16: Call self.assertRaises()

```python
self.assertRaises(SerialNoExistsInFutureTransactionError, bundle_id.make_serial_and_batch_bundle)
```

### Step 17: Call make_purchase_receipt()

```python
make_purchase_receipt(item_code=item.name, qty=2, rate=500, serial_no=serial_nos)
```

### Step 18: Assign item = create_item(...)

```python
item = create_item('Test Serialized Item 123')
```

### Step 19: Assign item.has_serial_no = 1

```python
item.has_serial_no = 1
```

### Step 20: Assign item.serial_no_series = 'TSI123-.####'

```python
item.serial_no_series = 'TSI123-.####'
```

### Step 21: Call item.save()

```python
item.save()
```

### Step 22: Assign item = frappe.get_doc(...)

```python
item = frappe.get_doc('Item', {'item_name': 'Test Serialized Item 123'})
```


## Complete Example

```python
# Setup
frappe.db.set_single_value('Buying Settings', 'allow_multiple_items', 1)

# Workflow
from erpnext.stock.doctype.delivery_note.test_delivery_note import create_delivery_note
item = frappe.db.exists('Item', {'item_name': 'Test Serialized Item 123'})
if not item:
    item = create_item('Test Serialized Item 123')
    item.has_serial_no = 1
    item.serial_no_series = 'TSI123-.####'
    item.save()
else:
    item = frappe.get_doc('Item', {'item_name': 'Test Serialized Item 123'})
pr = make_purchase_receipt(item_code=item.name, qty=2, rate=500)
pr.load_from_db()
bundle_id = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Purchase Receipt', 'voucher_no': pr.name, 'item_code': item.name}, 'serial_and_batch_bundle')
serial_nos = get_serial_nos_from_bundle(bundle_id)
self.assertEqual(get_serial_nos_from_bundle(pr.items[0].serial_and_batch_bundle), serial_nos)
bundle_id = make_serial_batch_bundle(frappe._dict({'item_code': item.item_code, 'warehouse': '_Test Warehouse 2 - _TC1', 'company': '_Test Company 1', 'qty': 2, 'voucher_type': 'Purchase Receipt', 'serial_nos': serial_nos, 'posting_date': today(), 'posting_time': nowtime(), 'do_not_save': True}))
self.assertRaises(SerialNoDuplicateError, bundle_id.make_serial_and_batch_bundle)
dn = create_delivery_note(item_code=item.name, qty=2, rate=1500, serial_no=serial_nos)
dn.load_from_db()
self.assertEqual(get_serial_nos_from_bundle(dn.items[0].serial_and_batch_bundle), serial_nos)
posting_date = add_days(today(), -3)
bundle_id = make_serial_batch_bundle(frappe._dict({'item_code': item.item_code, 'warehouse': '_Test Warehouse - _TC', 'company': '_Test Company', 'qty': 2, 'rate': 500, 'voucher_type': 'Purchase Receipt', 'serial_nos': serial_nos, 'posting_date': posting_date, 'posting_time': nowtime(), 'do_not_save': True}))
self.assertRaises(SerialNoExistsInFutureTransactionError, bundle_id.make_serial_and_batch_bundle)
bundle_id = make_serial_batch_bundle(frappe._dict({'item_code': item.item_code, 'warehouse': '_Test Warehouse 2 - _TC1', 'company': '_Test Company 1', 'qty': 2, 'rate': 500, 'voucher_type': 'Purchase Receipt', 'serial_nos': serial_nos, 'posting_date': posting_date, 'posting_time': nowtime(), 'do_not_save': True}))
self.assertRaises(SerialNoExistsInFutureTransactionError, bundle_id.make_serial_and_batch_bundle)
make_purchase_receipt(item_code=item.name, qty=2, rate=500, serial_no=serial_nos)
```

## Next Steps


---

*Source: test_purchase_receipt.py:222 | Complexity: Advanced | Last updated: 2026-02-04*