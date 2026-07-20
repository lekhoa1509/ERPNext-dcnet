# How To: Generated Variant Bom

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test generated variant bom

## Prerequisites

**Required Modules:**
- `collections`
- `functools`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.controllers.tests.test_subcontracting_controller`
- `erpnext.manufacturing.doctype.bom.bom`
- `erpnext.manufacturing.doctype.bom_update_log.test_bom_update_log`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.manufacturing.doctype.bom.bom`
- `erpnext.manufacturing.doctype.bom.bom`
- `erpnext.manufacturing.doctype.bom.bom`
- `erpnext.controllers.tests.test_subcontracting_controller`
- `erpnext.controllers.item_variant`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`
- `erpnext.manufacturing.doctype.bom.bom`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`


## Step-by-Step Guide

### Step 1: Assign template_item = make_item(...)

```python
template_item = make_item('_TestTemplateItem', {'has_variants': 1, 'attributes': [{'attribute': 'Test Size'}]})
```

### Step 2: Assign variant = create_variant(...)

```python
variant = create_variant(template_item.item_code, {'Test Size': 'Large'})
```

### Step 3: Call variant.insert()

```python
variant.insert(ignore_if_duplicate=True)
```

### Step 4: Assign bom_tree = value

```python
bom_tree = {template_item.item_code: {'SubAssembly1': {'ChildPart1': {}, 'ChildPart2': {}}, 'ChildPart5': {}}}
```

### Step 5: Assign template_bom = create_nested_bom(...)

```python
template_bom = create_nested_bom(bom_tree, prefix='')
```

### Step 6: Assign variant_bom = make_variant_bom(...)

```python
variant_bom = make_variant_bom(template_bom.name, template_bom.name, variant.item_code, variant_items=[])
```

### Step 7: Call variant_bom.save()

```python
variant_bom.save()
```

### Step 8: Assign reqd_order = template_bom.get_tree_representation.level_order_traversal(...)

```python
reqd_order = template_bom.get_tree_representation().level_order_traversal()
```

### Step 9: Assign created_order = variant_bom.get_tree_representation.level_order_traversal(...)

```python
created_order = variant_bom.get_tree_representation().level_order_traversal()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(len(reqd_order), len(created_order))
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(reqd_item.item_code, created_item.item_code)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(reqd_item.qty, created_item.qty)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(reqd_item.exploded_qty, created_item.exploded_qty)
```


## Complete Example

```python
# Workflow
from erpnext.controllers.item_variant import create_variant
template_item = make_item('_TestTemplateItem', {'has_variants': 1, 'attributes': [{'attribute': 'Test Size'}]})
variant = create_variant(template_item.item_code, {'Test Size': 'Large'})
variant.insert(ignore_if_duplicate=True)
bom_tree = {template_item.item_code: {'SubAssembly1': {'ChildPart1': {}, 'ChildPart2': {}}, 'ChildPart5': {}}}
template_bom = create_nested_bom(bom_tree, prefix='')
variant_bom = make_variant_bom(template_bom.name, template_bom.name, variant.item_code, variant_items=[])
variant_bom.save()
reqd_order = template_bom.get_tree_representation().level_order_traversal()
created_order = variant_bom.get_tree_representation().level_order_traversal()
self.assertEqual(len(reqd_order), len(created_order))
for reqd_item, created_item in zip(reqd_order, created_order, strict=False):
    self.assertEqual(reqd_item.item_code, created_item.item_code)
    self.assertEqual(reqd_item.qty, created_item.qty)
    self.assertEqual(reqd_item.exploded_qty, created_item.exploded_qty)
```

## Next Steps


---

*Source: test_bom.py:347 | Complexity: Advanced | Last updated: 2026-02-04*