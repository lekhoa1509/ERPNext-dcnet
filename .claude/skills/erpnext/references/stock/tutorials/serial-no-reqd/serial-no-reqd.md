# How To: Serial No Reqd

**Difficulty**: Advanced
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test serial no reqd

## Prerequisites

**Required Modules:**
- `frappe.permissions`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.controllers.accounts_controller`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.material_request.material_request`
- `erpnext.stock.doctype.material_request.test_material_request`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.serial_no.serial_no`
- `erpnext.stock.doctype.stock_entry.stock_entry`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.doctype.stock_ledger_entry.stock_ledger_entry`
- `erpnext.stock.doctype.stock_reconciliation.stock_reconciliation`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.stock.stock_ledger`
- `erpnext.stock.doctype.batch.test_batch`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.reorder_item`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.doctype.batch.batch`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.stock.doctype.batch.test_batch`
- `erpnext.stock.doctype.batch.test_batch`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.repost_item_valuation.repost_item_valuation`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.controllers.stock_controller`
- `erpnext.stock.doctype.batch.test_batch`
- `erpnext.stock.reorder_item`
- `erpnext.stock.reorder_item`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`
- `erpnext.stock.doctype.stock_entry.stock_entry`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.stock.utils`


## Step-by-Step Guide

### Step 1: Assign se = frappe.copy_doc(...)

```python
se = frappe.copy_doc(self.globalTestRecords['Stock Entry'][0])
```

### Step 2: Assign unknown.item_code = '_Test Serialized Item'

```python
se.get('items')[0].item_code = '_Test Serialized Item'
```

### Step 3: Assign unknown.qty = 2

```python
se.get('items')[0].qty = 2
```

### Step 4: Assign unknown.transfer_qty = 2

```python
se.get('items')[0].transfer_qty = 2
```

### Step 5: Assign bundle_id = make_serial_batch_bundle(...)

```python
bundle_id = make_serial_batch_bundle(frappe._dict({'item_code': se.get('items')[0].item_code, 'warehouse': se.get('items')[0].t_warehouse, 'company': se.company, 'qty': 2, 'voucher_type': 'Stock Entry', 'posting_date': se.posting_date, 'posting_time': se.posting_time, 'do_not_save': True}))
```

### Step 6: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, bundle_id.make_serial_and_batch_bundle)
```


## Complete Example

```python
# Workflow
se = frappe.copy_doc(self.globalTestRecords['Stock Entry'][0])
se.get('items')[0].item_code = '_Test Serialized Item'
se.get('items')[0].qty = 2
se.get('items')[0].transfer_qty = 2
bundle_id = make_serial_batch_bundle(frappe._dict({'item_code': se.get('items')[0].item_code, 'warehouse': se.get('items')[0].t_warehouse, 'company': se.company, 'qty': 2, 'voucher_type': 'Stock Entry', 'posting_date': se.posting_date, 'posting_time': se.posting_time, 'do_not_save': True}))
self.assertRaises(frappe.ValidationError, bundle_id.make_serial_and_batch_bundle)
```

## Next Steps


---

*Source: test_stock_entry.py:596 | Complexity: Advanced | Last updated: 2026-02-04*