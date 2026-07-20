# How To: Bom Raw Material

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test bom raw material

## Prerequisites

**Required Modules:**
- `random`
- `frappe`
- `frappe.tests`
- `erpnext.manufacturing.doctype.bom_creator.bom_creator`
- `erpnext.stock.doctype.item.test_item`


## Step-by-Step Guide

### Step 1: Assign final_product = 'Bicycle'

```python
final_product = 'Bicycle'
```

### Step 2: Call make_item()

```python
make_item(final_product, {'item_group': 'Raw Material', 'stock_uom': 'Nos'})
```

### Step 3: Assign doc = make_bom_creator(...)

```python
doc = make_bom_creator(name='Bicycle BOM with Raw Material', company='_Test Company', item_code=final_product, qty=1, rm_cosy_as_per='Valuation Rate', currency='INR', plc_conversion_rate=1, conversion_rate=1)
```

### Step 4: Call add_item()

```python
add_item(parent=doc.name, fg_item=final_product, fg_reference_id=doc.name, item_code='Pedal Assembly', qty=2)
```

### Step 5: Call doc.reload()

```python
doc.reload()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(doc.items[0].item_code, 'Pedal Assembly')
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(doc.items[0].qty, 2)
```

### Step 8: Assign fg_valuation_rate = 0

```python
fg_valuation_rate = 0
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(doc.raw_material_cost, fg_valuation_rate)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(row.fg_item, 'Bicycle')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(row.fg_reference_id, doc.name)
```


## Complete Example

```python
# Workflow
final_product = 'Bicycle'
make_item(final_product, {'item_group': 'Raw Material', 'stock_uom': 'Nos'})
doc = make_bom_creator(name='Bicycle BOM with Raw Material', company='_Test Company', item_code=final_product, qty=1, rm_cosy_as_per='Valuation Rate', currency='INR', plc_conversion_rate=1, conversion_rate=1)
add_item(parent=doc.name, fg_item=final_product, fg_reference_id=doc.name, item_code='Pedal Assembly', qty=2)
doc.reload()
self.assertEqual(doc.items[0].item_code, 'Pedal Assembly')
self.assertEqual(doc.items[0].qty, 2)
fg_valuation_rate = 0
for row in doc.items:
    if row.fg_item == final_product:
        fg_valuation_rate += row.amount
    if not row.is_expandable:
        self.assertEqual(row.fg_item, 'Bicycle')
        self.assertEqual(row.fg_reference_id, doc.name)
self.assertEqual(doc.raw_material_cost, fg_valuation_rate)
```

## Next Steps


---

*Source: test_bom_creator.py:75 | Complexity: Advanced | Last updated: 2026-02-04*