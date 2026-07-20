# How To: Material Issue Gl Entry

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test material issue gl entry

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

### Step 2: Call make_stock_entry()

```python
make_stock_entry(item_code='_Test Item', target='Stores - TCP1', company=company, qty=50, basic_rate=100, expense_account='Stock Adjustment - TCP1')
```

### Step 3: Assign mi = make_stock_entry(...)

```python
mi = make_stock_entry(item_code='_Test Item', source='Stores - TCP1', company=company, qty=40, expense_account='Stock Adjustment - TCP1')
```

### Step 4: Call self.check_stock_ledger_entries()

```python
self.check_stock_ledger_entries('Stock Entry', mi.name, [['_Test Item', 'Stores - TCP1', -40.0]])
```

### Step 5: Assign stock_in_hand_account = get_inventory_account(...)

```python
stock_in_hand_account = get_inventory_account(mi.company, 'Stores - TCP1')
```

### Step 6: Assign stock_value_diff = abs(...)

```python
stock_value_diff = abs(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Stock Entry', 'voucher_no': mi.name}, 'stock_value_difference'))
```

### Step 7: Call self.check_gl_entries()

```python
self.check_gl_entries('Stock Entry', mi.name, sorted([[stock_in_hand_account, 0.0, stock_value_diff], ['Stock Adjustment - TCP1', stock_value_diff, 0.0]]))
```

### Step 8: Call mi.cancel()

```python
mi.cancel()
```


## Complete Example

```python
# Workflow
company = frappe.db.get_value('Warehouse', 'Stores - TCP1', 'company')
make_stock_entry(item_code='_Test Item', target='Stores - TCP1', company=company, qty=50, basic_rate=100, expense_account='Stock Adjustment - TCP1')
mi = make_stock_entry(item_code='_Test Item', source='Stores - TCP1', company=company, qty=40, expense_account='Stock Adjustment - TCP1')
self.check_stock_ledger_entries('Stock Entry', mi.name, [['_Test Item', 'Stores - TCP1', -40.0]])
stock_in_hand_account = get_inventory_account(mi.company, 'Stores - TCP1')
stock_value_diff = abs(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Stock Entry', 'voucher_no': mi.name}, 'stock_value_difference'))
self.check_gl_entries('Stock Entry', mi.name, sorted([[stock_in_hand_account, 0.0, stock_value_diff], ['Stock Adjustment - TCP1', stock_value_diff, 0.0]]))
mi.cancel()
```

## Next Steps


---

*Source: test_stock_entry.py:278 | Complexity: Advanced | Last updated: 2026-02-04*