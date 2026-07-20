# How To: Bom Replace For Root Bom

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: - B-Item A (Root Item)
        - B-Item B
                - B-Item C
        - B-Item D
                - B-Item E
                        - B-Item F

Create New BOM for B-Item E with B-Item G and replace it in the above BOM.

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `erpnext.manufacturing.doctype.bom_update_log.bom_update_log`
- `erpnext.manufacturing.doctype.bom_update_tool.bom_update_tool`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.stock.doctype.item.test_item`


## Step-by-Step Guide

### Step 1: '\n\t\t- B-Item A (Root Item)\n\t\t        - B-Item B\n\t\t                - B-Item C\n\t\t        - B-Item D\n\t\t                - B-Item E\n\t\t                        - B-Item F\n\n\t\tCreate New BOM for B-Item E with B-Item G and replace it in the above BOM.\n\t\t'

```python
'\n\t\t- B-Item A (Root Item)\n\t\t        - B-Item B\n\t\t                - B-Item C\n\t\t        - B-Item D\n\t\t                - B-Item E\n\t\t                        - B-Item F\n\n\t\tCreate New BOM for B-Item E with B-Item G and replace it in the above BOM.\n\t\t'
```

### Step 2: Assign items = value

```python
items = ['B-Item A', 'B-Item B', 'B-Item C', 'B-Item D', 'B-Item E', 'B-Item F', 'B-Item G']
```

### Step 3: Assign bom_tree = value

```python
bom_tree = {'B-Item A': {'B-Item B': {'B-Item C': {}}, 'B-Item D': {'B-Item E': {'B-Item F': {}}}}}
```

### Step 4: Assign root_bom = create_nested_bom(...)

```python
root_bom = create_nested_bom(bom_tree, prefix='')
```

### Step 5: Assign exploded_items = frappe.get_all(...)

```python
exploded_items = frappe.get_all('BOM Explosion Item', filters={'parent': root_bom.name}, fields=['item_code'])
```

### Step 6: Assign exploded_items = value

```python
exploded_items = [item.item_code for item in exploded_items]
```

### Step 7: Assign expected_exploded_items = value

```python
expected_exploded_items = ['B-Item C', 'B-Item F']
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(sorted(exploded_items), sorted(expected_exploded_items))
```

### Step 9: Assign old_bom = frappe.db.get_value(...)

```python
old_bom = frappe.db.get_value('BOM', {'item': 'B-Item E'}, 'name')
```

### Step 10: Assign bom_tree = value

```python
bom_tree = {'B-Item E': {'B-Item G': {}}}
```

### Step 11: Assign new_bom = create_nested_bom(...)

```python
new_bom = create_nested_bom(bom_tree, prefix='')
```

### Step 12: Call enqueue_replace_bom()

```python
enqueue_replace_bom(boms=frappe._dict(current_bom=old_bom, new_bom=new_bom.name))
```

### Step 13: Assign exploded_items = frappe.get_all(...)

```python
exploded_items = frappe.get_all('BOM Explosion Item', filters={'parent': root_bom.name}, fields=['item_code'])
```

### Step 14: Assign exploded_items = value

```python
exploded_items = [item.item_code for item in exploded_items]
```

### Step 15: Assign expected_exploded_items = value

```python
expected_exploded_items = ['B-Item C', 'B-Item G']
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(sorted(exploded_items), sorted(expected_exploded_items))
```

### Step 17: Call remove_bom()

```python
remove_bom(item_code)
```

### Step 18: Call make_item()

```python
make_item(item_code)
```


## Complete Example

```python
# Workflow
'\n\t\t- B-Item A (Root Item)\n\t\t        - B-Item B\n\t\t                - B-Item C\n\t\t        - B-Item D\n\t\t                - B-Item E\n\t\t                        - B-Item F\n\n\t\tCreate New BOM for B-Item E with B-Item G and replace it in the above BOM.\n\t\t'
from erpnext.manufacturing.doctype.bom.test_bom import create_nested_bom
from erpnext.stock.doctype.item.test_item import make_item
items = ['B-Item A', 'B-Item B', 'B-Item C', 'B-Item D', 'B-Item E', 'B-Item F', 'B-Item G']
for item_code in items:
    if not frappe.db.exists('Item', item_code):
        make_item(item_code)
for item_code in items:
    remove_bom(item_code)
bom_tree = {'B-Item A': {'B-Item B': {'B-Item C': {}}, 'B-Item D': {'B-Item E': {'B-Item F': {}}}}}
root_bom = create_nested_bom(bom_tree, prefix='')
exploded_items = frappe.get_all('BOM Explosion Item', filters={'parent': root_bom.name}, fields=['item_code'])
exploded_items = [item.item_code for item in exploded_items]
expected_exploded_items = ['B-Item C', 'B-Item F']
self.assertEqual(sorted(exploded_items), sorted(expected_exploded_items))
old_bom = frappe.db.get_value('BOM', {'item': 'B-Item E'}, 'name')
bom_tree = {'B-Item E': {'B-Item G': {}}}
new_bom = create_nested_bom(bom_tree, prefix='')
enqueue_replace_bom(boms=frappe._dict(current_bom=old_bom, new_bom=new_bom.name))
exploded_items = frappe.get_all('BOM Explosion Item', filters={'parent': root_bom.name}, fields=['item_code'])
exploded_items = [item.item_code for item in exploded_items]
expected_exploded_items = ['B-Item C', 'B-Item G']
self.assertEqual(sorted(exploded_items), sorted(expected_exploded_items))
```

## Next Steps


---

*Source: test_bom_update_log.py:60 | Complexity: Advanced | Last updated: 2026-02-04*