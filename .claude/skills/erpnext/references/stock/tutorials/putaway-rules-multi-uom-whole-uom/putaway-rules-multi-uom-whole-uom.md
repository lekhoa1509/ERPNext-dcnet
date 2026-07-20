# How To: Putaway Rules Multi Uom Whole Uom

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test if whole UOMs are handled.

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

### Step 1: 'Test if whole UOMs are handled.'

```python
'Test if whole UOMs are handled.'
```

### Step 2: Assign item = frappe.get_doc(...)

```python
item = frappe.get_doc('Item', '_Rice')
```

### Step 3: Call frappe.db.set_value()

```python
frappe.db.set_value('UOM', 'Bag', 'must_be_whole_number', 1)
```

### Step 4: Assign rule_1 = create_putaway_rule(...)

```python
rule_1 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_1, capacity=1, uom='Bag')
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(rule_1.stock_capacity, 1000)
```

### Step 6: Assign rule_2 = create_putaway_rule(...)

```python
rule_2 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_2, capacity=500)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(rule_2.stock_capacity, 500)
```

### Step 8: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(item_code='_Rice', qty=2, uom='Bag', stock_uom='Kg', conversion_factor=1000, apply_putaway_rule=1, do_not_submit=1)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(len(pr.items), 1)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(pr.items[0].qty, 1)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(pr.items[0].warehouse, self.warehouse_1)
```

### Step 12: Call self.assertUnchangedItemsOnResave()

```python
self.assertUnchangedItemsOnResave(pr)
```

### Step 13: Call pr.delete()

```python
pr.delete()
```

### Step 14: Call rule_1.delete()

```python
rule_1.delete()
```

### Step 15: Call rule_2.delete()

```python
rule_2.delete()
```

### Step 16: Call item.append()

```python
item.append('uoms', {'uom': 'Bag', 'conversion_factor': 1000})
```

### Step 17: Call item.save()

```python
item.save()
```


## Complete Example

```python
# Workflow
'Test if whole UOMs are handled.'
item = frappe.get_doc('Item', '_Rice')
if not frappe.db.get_value('UOM Conversion Detail', {'parent': '_Rice', 'uom': 'Bag'}):
    item.append('uoms', {'uom': 'Bag', 'conversion_factor': 1000})
    item.save()
frappe.db.set_value('UOM', 'Bag', 'must_be_whole_number', 1)
rule_1 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_1, capacity=1, uom='Bag')
self.assertEqual(rule_1.stock_capacity, 1000)
rule_2 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_2, capacity=500)
self.assertEqual(rule_2.stock_capacity, 500)
pr = make_purchase_receipt(item_code='_Rice', qty=2, uom='Bag', stock_uom='Kg', conversion_factor=1000, apply_putaway_rule=1, do_not_submit=1)
self.assertEqual(len(pr.items), 1)
self.assertEqual(pr.items[0].qty, 1)
self.assertEqual(pr.items[0].warehouse, self.warehouse_1)
self.assertUnchangedItemsOnResave(pr)
pr.delete()
rule_1.delete()
rule_2.delete()
```

## Next Steps


---

*Source: test_putaway_rule.py:146 | Complexity: Advanced | Last updated: 2026-02-04*