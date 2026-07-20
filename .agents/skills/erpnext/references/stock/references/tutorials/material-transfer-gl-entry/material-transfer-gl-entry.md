# How To: Material Transfer Gl Entry

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test material transfer gl entry

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

### Step 1: Assign company = frappe.db.get_value(...)

```python
company = frappe.db.get_value('Warehouse', 'Stores - TCP1', 'company')
```

### Step 2: Assign item_code = 'Hand Sanitizer - 001'

```python
item_code = 'Hand Sanitizer - 001'
```

### Step 3: Call create_item()

```python
create_item(item_code=item_code, is_stock_item=1, is_purchase_item=1, opening_stock=1000, valuation_rate=10, company=company, warehouse='Stores - TCP1')
```

### Step 4: Assign mtn = make_stock_entry(...)

```python
mtn = make_stock_entry(item_code=item_code, source='Stores - TCP1', target='Finished Goods - TCP1', qty=45, company=company)
```

### Step 5: Call self.check_stock_ledger_entries()

```python
self.check_stock_ledger_entries('Stock Entry', mtn.name, [[item_code, 'Stores - TCP1', -45.0], [item_code, 'Finished Goods - TCP1', 45.0]])
```

### Step 6: Assign source_warehouse_account = get_inventory_account(...)

```python
source_warehouse_account = get_inventory_account(mtn.company, mtn.get('items')[0].s_warehouse)
```

### Step 7: Assign target_warehouse_account = get_inventory_account(...)

```python
target_warehouse_account = get_inventory_account(mtn.company, mtn.get('items')[0].t_warehouse)
```

### Step 8: Call mtn.cancel()

```python
mtn.cancel()
```

### Step 9: Call self.assertFalse()

```python
self.assertFalse(frappe.db.sql("select * from `tabGL Entry`\n\t\t\t\twhere voucher_type='Stock Entry' and voucher_no=%s", mtn.name, as_dict=1))
```

### Step 10: Assign stock_value_diff = abs(...)

```python
stock_value_diff = abs(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Stock Entry', 'voucher_no': mtn.name, 'warehouse': 'Stores - TCP1'}, 'stock_value_difference'))
```

### Step 11: Call self.check_gl_entries()

```python
self.check_gl_entries('Stock Entry', mtn.name, sorted([[source_warehouse_account, 0.0, stock_value_diff], [target_warehouse_account, stock_value_diff, 0.0]]))
```


## Complete Example

```python
# Workflow
company = frappe.db.get_value('Warehouse', 'Stores - TCP1', 'company')
item_code = 'Hand Sanitizer - 001'
create_item(item_code=item_code, is_stock_item=1, is_purchase_item=1, opening_stock=1000, valuation_rate=10, company=company, warehouse='Stores - TCP1')
mtn = make_stock_entry(item_code=item_code, source='Stores - TCP1', target='Finished Goods - TCP1', qty=45, company=company)
self.check_stock_ledger_entries('Stock Entry', mtn.name, [[item_code, 'Stores - TCP1', -45.0], [item_code, 'Finished Goods - TCP1', 45.0]])
source_warehouse_account = get_inventory_account(mtn.company, mtn.get('items')[0].s_warehouse)
target_warehouse_account = get_inventory_account(mtn.company, mtn.get('items')[0].t_warehouse)
if source_warehouse_account == target_warehouse_account:
    self.assertFalse(frappe.db.sql("select * from `tabGL Entry`\n\t\t\t\twhere voucher_type='Stock Entry' and voucher_no=%s", mtn.name, as_dict=1))
else:
    stock_value_diff = abs(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Stock Entry', 'voucher_no': mtn.name, 'warehouse': 'Stores - TCP1'}, 'stock_value_difference'))
    self.check_gl_entries('Stock Entry', mtn.name, sorted([[source_warehouse_account, 0.0, stock_value_diff], [target_warehouse_account, stock_value_diff, 0.0]]))
mtn.cancel()
```

## Next Steps


---

*Source: test_stock_entry.py:320 | Complexity: Advanced | Last updated: 2026-02-04*