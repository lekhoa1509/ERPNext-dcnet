# How To: Repack No Change In Valuation

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test repack no change in valuation

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

### Step 1: Call make_stock_entry()

```python
make_stock_entry(item_code='_Test Item', target='_Test Warehouse - _TC', qty=50, basic_rate=100)
```

### Step 2: Call make_stock_entry()

```python
make_stock_entry(item_code='_Test Item Home Desktop 100', target='_Test Warehouse - _TC', qty=50, basic_rate=100)
```

### Step 3: Assign repack = frappe.copy_doc(...)

```python
repack = frappe.copy_doc(self.globalTestRecords['Stock Entry'][3])
```

### Step 4: Assign repack.posting_date = nowdate(...)

```python
repack.posting_date = nowdate()
```

### Step 5: Assign repack.posting_time = nowtime(...)

```python
repack.posting_time = nowtime()
```

### Step 6: Call repack.set_stock_entry_type()

```python
repack.set_stock_entry_type()
```

### Step 7: Call repack.insert()

```python
repack.insert()
```

### Step 8: Call repack.submit()

```python
repack.submit()
```

### Step 9: Call self.check_stock_ledger_entries()

```python
self.check_stock_ledger_entries('Stock Entry', repack.name, [['_Test Item', '_Test Warehouse - _TC', -50.0], ['_Test Item Home Desktop 100', '_Test Warehouse - _TC', 1]])
```

### Step 10: Assign gl_entries = frappe.db.sql(...)

```python
gl_entries = frappe.db.sql("select account, debit, credit\n\t\t\tfrom `tabGL Entry` where voucher_type='Stock Entry' and voucher_no=%s\n\t\t\torder by account desc", repack.name, as_dict=1)
```

### Step 11: Call self.assertFalse()

```python
self.assertFalse(gl_entries)
```


## Complete Example

```python
# Workflow
make_stock_entry(item_code='_Test Item', target='_Test Warehouse - _TC', qty=50, basic_rate=100)
make_stock_entry(item_code='_Test Item Home Desktop 100', target='_Test Warehouse - _TC', qty=50, basic_rate=100)
repack = frappe.copy_doc(self.globalTestRecords['Stock Entry'][3])
repack.posting_date = nowdate()
repack.posting_time = nowtime()
repack.set_stock_entry_type()
repack.insert()
repack.submit()
self.check_stock_ledger_entries('Stock Entry', repack.name, [['_Test Item', '_Test Warehouse - _TC', -50.0], ['_Test Item Home Desktop 100', '_Test Warehouse - _TC', 1]])
gl_entries = frappe.db.sql("select account, debit, credit\n\t\t\tfrom `tabGL Entry` where voucher_type='Stock Entry' and voucher_no=%s\n\t\t\torder by account desc", repack.name, as_dict=1)
self.assertFalse(gl_entries)
```

## Next Steps


---

*Source: test_stock_entry.py:432 | Complexity: Advanced | Last updated: 2026-02-04*