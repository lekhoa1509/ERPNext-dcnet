# How To: Validate Over Receipt In Warehouse

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test if overreceipt is blocked in the presence of putaway rules.

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `erpnext.stock.doctype.batch.test_batch`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.get_item_details`
- `erpnext.stock.dashboard.warehouse_capacity_dashboard`


## Step-by-Step Guide

### Step 1: 'Test if overreceipt is blocked in the presence of putaway rules.'

```python
'Test if overreceipt is blocked in the presence of putaway rules.'
```

### Step 2: Assign rule_1 = create_putaway_rule(...)

```python
rule_1 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_1, capacity=200, uom='Kg')
```

### Step 3: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(item_code='_Rice', qty=300, apply_putaway_rule=1, do_not_submit=1)
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(len(pr.items), 1)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(pr.items[0].qty, 200)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(pr.items[0].warehouse, self.warehouse_1)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(pr.items[0].putaway_rule, rule_1.name)
```

### Step 8: Assign unknown.qty = 300

```python
pr.items[0].qty = 300
```

### Step 9: Assign unknown.stock_qty = 300

```python
pr.items[0].stock_qty = 300
```

### Step 10: Assign pr.apply_putaway_rule = 0

```python
pr.apply_putaway_rule = 0
```

### Step 11: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, pr.save)
```

### Step 12: Call pr.delete()

```python
pr.delete()
```

### Step 13: Call rule_1.delete()

```python
rule_1.delete()
```


## Complete Example

```python
# Workflow
'Test if overreceipt is blocked in the presence of putaway rules.'
rule_1 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_1, capacity=200, uom='Kg')
pr = make_purchase_receipt(item_code='_Rice', qty=300, apply_putaway_rule=1, do_not_submit=1)
self.assertEqual(len(pr.items), 1)
self.assertEqual(pr.items[0].qty, 200)
self.assertEqual(pr.items[0].warehouse, self.warehouse_1)
self.assertEqual(pr.items[0].putaway_rule, rule_1.name)
pr.items[0].qty = 300
pr.items[0].stock_qty = 300
pr.apply_putaway_rule = 0
self.assertRaises(frappe.ValidationError, pr.save)
pr.delete()
rule_1.delete()
```

## Next Steps


---

*Source: test_putaway_rule.py:220 | Complexity: Advanced | Last updated: 2026-02-04*