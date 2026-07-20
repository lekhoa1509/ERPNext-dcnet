# How To: Convert To Sub Assembly

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test convert to sub assembly

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
doc = make_bom_creator(name='Bicycle BOM', company='_Test Company', item_code=final_product, qty=1, rm_cosy_as_per='Valuation Rate', currency='INR', plc_conversion_rate=1, conversion_rate=1)
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
self.assertEqual(doc.items[0].is_expandable, 0)
```

### Step 7: Call add_sub_assembly()

```python
add_sub_assembly(convert_to_sub_assembly=1, parent=doc.name, fg_item=final_product, fg_reference_id=doc.items[0].name, bom_item={'item_code': 'Pedal Assembly', 'qty': 2, 'items': [{'item_code': 'Pedal Body', 'qty': 2}, {'item_code': 'Pedal Axle', 'qty': 2}]})
```

### Step 8: Call doc.reload()

```python
doc.reload()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(doc.items[0].is_expandable, 1)
```

### Step 10: Assign fg_valuation_rate = 0

```python
fg_valuation_rate = 0
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(doc.raw_material_cost, fg_valuation_rate)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(row.fg_item, 'Pedal Assembly')
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(row.qty, 2.0)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(row.fg_reference_id, doc.items[0].name)
```


## Complete Example

```python
# Workflow
final_product = 'Bicycle'
make_item(final_product, {'item_group': 'Raw Material', 'stock_uom': 'Nos'})
doc = make_bom_creator(name='Bicycle BOM', company='_Test Company', item_code=final_product, qty=1, rm_cosy_as_per='Valuation Rate', currency='INR', plc_conversion_rate=1, conversion_rate=1)
add_item(parent=doc.name, fg_item=final_product, fg_reference_id=doc.name, item_code='Pedal Assembly', qty=2)
doc.reload()
self.assertEqual(doc.items[0].is_expandable, 0)
add_sub_assembly(convert_to_sub_assembly=1, parent=doc.name, fg_item=final_product, fg_reference_id=doc.items[0].name, bom_item={'item_code': 'Pedal Assembly', 'qty': 2, 'items': [{'item_code': 'Pedal Body', 'qty': 2}, {'item_code': 'Pedal Axle', 'qty': 2}]})
doc.reload()
self.assertEqual(doc.items[0].is_expandable, 1)
fg_valuation_rate = 0
for row in doc.items:
    if row.fg_item == final_product:
        fg_valuation_rate += row.amount
    if not row.is_expandable:
        self.assertEqual(row.fg_item, 'Pedal Assembly')
        self.assertEqual(row.qty, 2.0)
        self.assertEqual(row.fg_reference_id, doc.items[0].name)
self.assertEqual(doc.raw_material_cost, fg_valuation_rate)
```

## Next Steps


---

*Source: test_bom_creator.py:119 | Complexity: Advanced | Last updated: 2026-02-04*