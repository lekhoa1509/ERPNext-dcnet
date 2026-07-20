# How To: Bom Tree Representation

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test bom tree representation

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

### Step 1: Assign bom_tree = value

```python
bom_tree = {'Assembly': {'SubAssembly1': {'ChildPart1': {}, 'ChildPart2': {}}, 'SubAssembly2': {'ChildPart3': {}}, 'SubAssembly3': {'SubSubAssy1': {'ChildPart4': {}}}, 'ChildPart5': {}, 'ChildPart6': {}, 'SubAssembly4': {'SubSubAssy2': {'ChildPart7': {}}}}}
```

### Step 2: Assign parent_bom = create_nested_bom(...)

```python
parent_bom = create_nested_bom(bom_tree, prefix='')
```

### Step 3: Assign created_tree = parent_bom.get_tree_representation(...)

```python
created_tree = parent_bom.get_tree_representation()
```

### Step 4: Assign reqd_order = value

```python
reqd_order = level_order_traversal(bom_tree)[1:]
```

### Step 5: Assign created_order = created_tree.level_order_traversal(...)

```python
created_order = created_tree.level_order_traversal()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(len(reqd_order), len(created_order))
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(reqd_item, created_item.item_code)
```


## Complete Example

```python
# Workflow
bom_tree = {'Assembly': {'SubAssembly1': {'ChildPart1': {}, 'ChildPart2': {}}, 'SubAssembly2': {'ChildPart3': {}}, 'SubAssembly3': {'SubSubAssy1': {'ChildPart4': {}}}, 'ChildPart5': {}, 'ChildPart6': {}, 'SubAssembly4': {'SubSubAssy2': {'ChildPart7': {}}}}}
parent_bom = create_nested_bom(bom_tree, prefix='')
created_tree = parent_bom.get_tree_representation()
reqd_order = level_order_traversal(bom_tree)[1:]
created_order = created_tree.level_order_traversal()
self.assertEqual(len(reqd_order), len(created_order))
for reqd_item, created_item in zip(reqd_order, created_order, strict=False):
    self.assertEqual(reqd_item, created_item.item_code)
```

## Next Steps


---

*Source: test_bom.py:321 | Complexity: Intermediate | Last updated: 2026-02-04*