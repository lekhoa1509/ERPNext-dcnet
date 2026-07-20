# How To: Make Boms From Bom Creator

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test make boms from bom creator

## Prerequisites

**Required Modules:**
- `random`
- `frappe`
- `frappe.tests`
- `erpnext.manufacturing.doctype.bom_creator.bom_creator`
- `erpnext.stock.doctype.item.test_item`


## Step-by-Step Guide

### Step 1: Assign final_product = 'Bicycle Test'

```python
final_product = 'Bicycle Test'
```

### Step 2: Call make_item()

```python
make_item(final_product, {'item_group': 'Raw Material', 'stock_uom': 'Nos'})
```

### Step 3: Assign doc = make_bom_creator(...)

```python
doc = make_bom_creator(name='Bicycle BOM Test', company='_Test Company', item_code=final_product, qty=1, rm_cosy_as_per='Valuation Rate', currency='INR', plc_conversion_rate=1, conversion_rate=1)
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

### Step 10: Call doc.submit()

```python
doc.submit()
```

### Step 11: Call doc.create_boms()

```python
doc.create_boms()
```

### Step 12: Call doc.reload()

```python
doc.reload()
```

### Step 13: Assign data = frappe.get_all(...)

```python
data = frappe.get_all('BOM', filters={'bom_creator': doc.name, 'docstatus': 1})
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(len(data), 2)
```

### Step 15: Call doc.create_boms()

```python
doc.create_boms()
```

### Step 16: Assign data = frappe.get_all(...)

```python
data = frappe.get_all('BOM', filters={'bom_creator': doc.name, 'docstatus': 1})
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(len(data), 2)
```


## Complete Example

```python
# Workflow
final_product = 'Bicycle Test'
make_item(final_product, {'item_group': 'Raw Material', 'stock_uom': 'Nos'})
doc = make_bom_creator(name='Bicycle BOM Test', company='_Test Company', item_code=final_product, qty=1, rm_cosy_as_per='Valuation Rate', currency='INR', plc_conversion_rate=1, conversion_rate=1)
add_item(parent=doc.name, fg_item=final_product, fg_reference_id=doc.name, item_code='Pedal Assembly', qty=2)
doc.reload()
self.assertEqual(doc.items[0].is_expandable, 0)
add_sub_assembly(convert_to_sub_assembly=1, parent=doc.name, fg_item=final_product, fg_reference_id=doc.items[0].name, bom_item={'item_code': 'Pedal Assembly', 'qty': 2, 'items': [{'item_code': 'Pedal Body', 'qty': 2}, {'item_code': 'Pedal Axle', 'qty': 2}]})
doc.reload()
self.assertEqual(doc.items[0].is_expandable, 1)
doc.submit()
doc.create_boms()
doc.reload()
data = frappe.get_all('BOM', filters={'bom_creator': doc.name, 'docstatus': 1})
self.assertEqual(len(data), 2)
doc.create_boms()
data = frappe.get_all('BOM', filters={'bom_creator': doc.name, 'docstatus': 1})
self.assertEqual(len(data), 2)
```

## Next Steps


---

*Source: test_bom_creator.py:187 | Complexity: Advanced | Last updated: 2026-02-04*