# How To: Add To Transit Entry

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test add to transit entry

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

### Step 1: Assign item_code = '_Test Transit Item'

```python
item_code = '_Test Transit Item'
```

### Step 2: Assign company = '_Test Company'

```python
company = '_Test Company'
```

### Step 3: Call create_warehouse()

```python
create_warehouse('Test From Warehouse')
```

### Step 4: Call create_warehouse()

```python
create_warehouse('Test Transit Warehouse')
```

### Step 5: Call create_warehouse()

```python
create_warehouse('Test To Warehouse')
```

### Step 6: Call create_item()

```python
create_item(item_code=item_code, is_stock_item=1, is_purchase_item=1, company=company)
```

### Step 7: Call make_stock_entry()

```python
make_stock_entry(item_code=item_code, target='Test From Warehouse - _TC', qty=10, basic_rate=100, expense_account='Stock Adjustment - _TC', cost_center='Main - _TC')
```

### Step 8: Assign transit_entry = make_stock_entry(...)

```python
transit_entry = make_stock_entry(item_code=item_code, source='Test From Warehouse - _TC', target='Test Transit Warehouse - _TC', add_to_transit=1, stock_entry_type='Material Transfer', purpose='Material Transfer', qty=10, basic_rate=100, expense_account='Stock Adjustment - _TC', cost_center='Main - _TC')
```

### Step 9: Assign end_transit_entry = make_stock_in_entry(...)

```python
end_transit_entry = make_stock_in_entry(transit_entry.name)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(end_transit_entry.stock_entry_type, 'Material Transfer')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(end_transit_entry.purpose, 'Material Transfer')
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(transit_entry.name, end_transit_entry.outgoing_stock_entry)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(transit_entry.name, end_transit_entry.items[0].against_stock_entry)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(transit_entry.items[0].name, end_transit_entry.items[0].ste_detail)
```


## Complete Example

```python
# Workflow
from erpnext.stock.doctype.warehouse.test_warehouse import create_warehouse
item_code = '_Test Transit Item'
company = '_Test Company'
create_warehouse('Test From Warehouse')
create_warehouse('Test Transit Warehouse')
create_warehouse('Test To Warehouse')
create_item(item_code=item_code, is_stock_item=1, is_purchase_item=1, company=company)
make_stock_entry(item_code=item_code, target='Test From Warehouse - _TC', qty=10, basic_rate=100, expense_account='Stock Adjustment - _TC', cost_center='Main - _TC')
transit_entry = make_stock_entry(item_code=item_code, source='Test From Warehouse - _TC', target='Test Transit Warehouse - _TC', add_to_transit=1, stock_entry_type='Material Transfer', purpose='Material Transfer', qty=10, basic_rate=100, expense_account='Stock Adjustment - _TC', cost_center='Main - _TC')
end_transit_entry = make_stock_in_entry(transit_entry.name)
self.assertEqual(end_transit_entry.stock_entry_type, 'Material Transfer')
self.assertEqual(end_transit_entry.purpose, 'Material Transfer')
self.assertEqual(transit_entry.name, end_transit_entry.outgoing_stock_entry)
self.assertEqual(transit_entry.name, end_transit_entry.items[0].against_stock_entry)
self.assertEqual(transit_entry.items[0].name, end_transit_entry.items[0].ste_detail)
```

## Next Steps


---

*Source: test_stock_entry.py:189 | Complexity: Advanced | Last updated: 2026-02-04*