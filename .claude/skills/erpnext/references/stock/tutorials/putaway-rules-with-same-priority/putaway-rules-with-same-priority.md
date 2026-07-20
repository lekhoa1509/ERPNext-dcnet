# How To: Putaway Rules With Same Priority

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test if rule with more free space is applied,
among two rules with same priority and capacity.

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

### Step 1: 'Test if rule with more free space is applied,\n\t\tamong two rules with same priority and capacity.'

```python
'Test if rule with more free space is applied,\n\t\tamong two rules with same priority and capacity.'
```

### Step 2: Assign rule_1 = create_putaway_rule(...)

```python
rule_1 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_1, capacity=500, uom='Kg')
```

### Step 3: Assign rule_2 = create_putaway_rule(...)

```python
rule_2 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_2, capacity=500, uom='Kg')
```

### Step 4: Assign stock_receipt = make_stock_entry(...)

```python
stock_receipt = make_stock_entry(item_code='_Rice', target=self.warehouse_1, qty=100, basic_rate=50)
```

### Step 5: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(item_code='_Rice', qty=700, apply_putaway_rule=1, do_not_submit=1)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(len(pr.items), 2)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(pr.items[0].qty, 500)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(pr.items[0].warehouse, self.warehouse_2)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(pr.items[1].qty, 200)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(pr.items[1].warehouse, self.warehouse_1)
```

### Step 11: Call stock_receipt.cancel()

```python
stock_receipt.cancel()
```

### Step 12: Call pr.delete()

```python
pr.delete()
```

### Step 13: Call rule_1.delete()

```python
rule_1.delete()
```

### Step 14: Call rule_2.delete()

```python
rule_2.delete()
```


## Complete Example

```python
# Workflow
'Test if rule with more free space is applied,\n\t\tamong two rules with same priority and capacity.'
rule_1 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_1, capacity=500, uom='Kg')
rule_2 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_2, capacity=500, uom='Kg')
stock_receipt = make_stock_entry(item_code='_Rice', target=self.warehouse_1, qty=100, basic_rate=50)
pr = make_purchase_receipt(item_code='_Rice', qty=700, apply_putaway_rule=1, do_not_submit=1)
self.assertEqual(len(pr.items), 2)
self.assertEqual(pr.items[0].qty, 500)
self.assertEqual(pr.items[0].warehouse, self.warehouse_2)
self.assertEqual(pr.items[1].qty, 200)
self.assertEqual(pr.items[1].warehouse, self.warehouse_1)
stock_receipt.cancel()
pr.delete()
rule_1.delete()
rule_2.delete()
```

## Next Steps


---

*Source: test_putaway_rule.py:71 | Complexity: Advanced | Last updated: 2026-02-04*