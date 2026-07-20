# How To: Repack With Additional Costs

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test repack with additional costs

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

### Step 3: Assign repack = make_stock_entry(...)

```python
repack = make_stock_entry(company=company, purpose='Repack', do_not_save=True)
```

### Step 4: Assign repack.posting_date = nowdate(...)

```python
repack.posting_date = nowdate()
```

### Step 5: Assign repack.posting_time = nowtime(...)

```python
repack.posting_time = nowtime()
```

### Step 6: Assign default_expense_account = frappe.get_value(...)

```python
default_expense_account = frappe.get_value('Company', company, 'default_expense_account')
```

### Step 7: Assign items = get_multiple_items(...)

```python
items = get_multiple_items()
```

### Step 8: Assign repack.items = value

```python
repack.items = []
```

### Step 9: Call repack.set()

```python
repack.set('additional_costs', [{'expense_account': default_expense_account, 'description': 'Actual Operating Cost', 'amount': 1000}, {'expense_account': default_expense_account, 'description': 'Additional Operating Cost', 'amount': 200}])
```

### Step 10: Call repack.set_stock_entry_type()

```python
repack.set_stock_entry_type()
```

### Step 11: Call repack.insert()

```python
repack.insert()
```

### Step 12: Call repack.submit()

```python
repack.submit()
```

### Step 13: Assign stock_in_hand_account = get_inventory_account(...)

```python
stock_in_hand_account = get_inventory_account(repack.company, repack.get('items')[1].t_warehouse)
```

### Step 14: Assign rm_stock_value_diff = abs(...)

```python
rm_stock_value_diff = abs(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Stock Entry', 'voucher_no': repack.name, 'item_code': '_Test Item'}, 'stock_value_difference'))
```

### Step 15: Assign fg_stock_value_diff = abs(...)

```python
fg_stock_value_diff = abs(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Stock Entry', 'voucher_no': repack.name, 'item_code': '_Test Item Home Desktop 100'}, 'stock_value_difference'))
```

### Step 16: Assign stock_value_diff = flt(...)

```python
stock_value_diff = flt(fg_stock_value_diff - rm_stock_value_diff, 2)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(stock_value_diff, 1200)
```

### Step 18: Call self.check_gl_entries()

```python
self.check_gl_entries('Stock Entry', repack.name, sorted([[stock_in_hand_account, 1200, 0.0], ['Cost of Goods Sold - TCP1', 0.0, 1200.0]]))
```

### Step 19: Call repack.append()

```python
repack.append('items', item)
```


## Complete Example

```python
# Workflow
company = frappe.db.get_value('Warehouse', 'Stores - TCP1', 'company')
make_stock_entry(item_code='_Test Item', target='Stores - TCP1', company=company, qty=50, basic_rate=100, expense_account='Stock Adjustment - TCP1')
repack = make_stock_entry(company=company, purpose='Repack', do_not_save=True)
repack.posting_date = nowdate()
repack.posting_time = nowtime()
default_expense_account = frappe.get_value('Company', company, 'default_expense_account')
items = get_multiple_items()
repack.items = []
for item in items:
    repack.append('items', item)
repack.set('additional_costs', [{'expense_account': default_expense_account, 'description': 'Actual Operating Cost', 'amount': 1000}, {'expense_account': default_expense_account, 'description': 'Additional Operating Cost', 'amount': 200}])
repack.set_stock_entry_type()
repack.insert()
repack.submit()
stock_in_hand_account = get_inventory_account(repack.company, repack.get('items')[1].t_warehouse)
rm_stock_value_diff = abs(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Stock Entry', 'voucher_no': repack.name, 'item_code': '_Test Item'}, 'stock_value_difference'))
fg_stock_value_diff = abs(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Stock Entry', 'voucher_no': repack.name, 'item_code': '_Test Item Home Desktop 100'}, 'stock_value_difference'))
stock_value_diff = flt(fg_stock_value_diff - rm_stock_value_diff, 2)
self.assertEqual(stock_value_diff, 1200)
self.check_gl_entries('Stock Entry', repack.name, sorted([[stock_in_hand_account, 1200, 0.0], ['Cost of Goods Sold - TCP1', 0.0, 1200.0]]))
```

## Next Steps


---

*Source: test_stock_entry.py:463 | Complexity: Advanced | Last updated: 2026-02-04*