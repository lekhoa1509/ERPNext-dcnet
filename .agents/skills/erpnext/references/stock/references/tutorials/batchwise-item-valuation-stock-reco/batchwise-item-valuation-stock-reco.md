# How To: Batchwise Item Valuation Stock Reco

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test batchwise item valuation stock reco

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `json`
- `time`
- `uuid`
- `frappe`
- `frappe.core.page.permission_manager.permission_manager`
- `frappe.custom.doctype.property_setter.property_setter`
- `frappe.query_builder.functions`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.gl_entry.gl_entry`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.landed_cost_voucher.test_landed_cost_voucher`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.doctype.stock_ledger_entry.stock_ledger_entry`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.stock.stock_ledger`
- `erpnext.stock.tests.test_utils`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.stock.doctype.repost_item_valuation.repost_item_valuation`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.utils`
- `erpnext.stock.doctype.item.test_item`

**Setup Required:**
```python
items = create_items()
reset('Stock Entry')
frappe.db.sql('delete from `tabStock Ledger Entry` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)
frappe.db.sql('delete from `tabBin` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)
```

## Step-by-Step Guide

### Step 1: Assign unknown = setup_item_valuation_test(...)

```python
item, warehouses, batches = setup_item_valuation_test()
```

### Step 2: Assign state = value

```python
state = {'stock_value': 0.0, 'qty': 0.0}
```

### Step 3: Assign osr1 = create_stock_reconciliation(...)

```python
osr1 = create_stock_reconciliation(warehouse=warehouses[0], item_code=item, qty=10, rate=100, batch_no=batches[1])
```

### Step 4: Assign expected_sles = value

```python
expected_sles = [{'actual_qty': 10, 'stock_value_difference': 1000}]
```

### Step 5: Call update_invariants()

```python
update_invariants(expected_sles)
```

### Step 6: Call self.assertSLEs()

```python
self.assertSLEs(osr1, expected_sles)
```

### Step 7: Assign osr2 = create_stock_reconciliation(...)

```python
osr2 = create_stock_reconciliation(warehouse=warehouses[0], item_code=item, qty=13, rate=200, batch_no=batches[0])
```

### Step 8: Assign expected_sles = value

```python
expected_sles = [{'actual_qty': -10, 'stock_value_difference': -10 * 100}, {'actual_qty': 13, 'stock_value_difference': 200 * 13}]
```

### Step 9: Call update_invariants()

```python
update_invariants(expected_sles)
```

### Step 10: Call self.assertSLEs()

```python
self.assertSLEs(osr2, expected_sles)
```

### Step 11: Assign sr1 = create_stock_reconciliation(...)

```python
sr1 = create_stock_reconciliation(warehouse=warehouses[0], item_code=item, qty=5, rate=50, batch_no=batches[1])
```

### Step 12: Assign expected_sles = value

```python
expected_sles = [{'actual_qty': -13, 'stock_value_difference': -13 * 200}, {'actual_qty': 5, 'stock_value_difference': 250}]
```

### Step 13: Call update_invariants()

```python
update_invariants(expected_sles)
```

### Step 14: Call self.assertSLEs()

```python
self.assertSLEs(sr1, expected_sles)
```

### Step 15: Assign sr2 = create_stock_reconciliation(...)

```python
sr2 = create_stock_reconciliation(warehouse=warehouses[0], item_code=item, qty=20, rate=75, batch_no=batches[0])
```

### Step 16: Assign expected_sles = value

```python
expected_sles = [{'actual_qty': -5, 'stock_value_difference': -5 * 50}, {'actual_qty': 20, 'stock_value_difference': 20 * 75}]
```

### Step 17: Call update_invariants()

```python
update_invariants(expected_sles)
```

### Step 18: Call self.assertSLEs()

```python
self.assertSLEs(sr2, expected_sles)
```

### Step 19: Assign unknown = value

```python
sle['stock_value'] = state['stock_value']
```

### Step 20: Assign unknown = value

```python
sle['qty_after_transaction'] = state['qty']
```


## Complete Example

```python
# Setup
items = create_items()
reset('Stock Entry')
frappe.db.sql('delete from `tabStock Ledger Entry` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)
frappe.db.sql('delete from `tabBin` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)

# Workflow
item, warehouses, batches = setup_item_valuation_test()
state = {'stock_value': 0.0, 'qty': 0.0}

def update_invariants(exp_sles):
    for sle in exp_sles:
        state['stock_value'] += sle['stock_value_difference']
        state['qty'] += sle['actual_qty']
        sle['stock_value'] = state['stock_value']
        sle['qty_after_transaction'] = state['qty']
osr1 = create_stock_reconciliation(warehouse=warehouses[0], item_code=item, qty=10, rate=100, batch_no=batches[1])
expected_sles = [{'actual_qty': 10, 'stock_value_difference': 1000}]
update_invariants(expected_sles)
self.assertSLEs(osr1, expected_sles)
osr2 = create_stock_reconciliation(warehouse=warehouses[0], item_code=item, qty=13, rate=200, batch_no=batches[0])
expected_sles = [{'actual_qty': -10, 'stock_value_difference': -10 * 100}, {'actual_qty': 13, 'stock_value_difference': 200 * 13}]
update_invariants(expected_sles)
self.assertSLEs(osr2, expected_sles)
sr1 = create_stock_reconciliation(warehouse=warehouses[0], item_code=item, qty=5, rate=50, batch_no=batches[1])
expected_sles = [{'actual_qty': -13, 'stock_value_difference': -13 * 200}, {'actual_qty': 5, 'stock_value_difference': 250}]
update_invariants(expected_sles)
self.assertSLEs(sr1, expected_sles)
sr2 = create_stock_reconciliation(warehouse=warehouses[0], item_code=item, qty=20, rate=75, batch_no=batches[0])
expected_sles = [{'actual_qty': -5, 'stock_value_difference': -5 * 50}, {'actual_qty': 20, 'stock_value_difference': 20 * 75}]
update_invariants(expected_sles)
self.assertSLEs(sr2, expected_sles)
```

## Next Steps


---

*Source: test_stock_ledger_entry.py:536 | Complexity: Advanced | Last updated: 2026-02-04*