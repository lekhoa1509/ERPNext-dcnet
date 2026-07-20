# How To: Move Leaf Into Another Group

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test move leaf into another group

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils.nestedset`
- `json`


## Step-by-Step Guide

### Step 1: Assign unknown = frappe.db.get_value(...)

```python
old_lft, old_rgt = frappe.db.get_value('Item Group', '_Test Item Group C', ['lft', 'rgt'])
```

### Step 2: Assign group_b_3 = frappe.get_doc(...)

```python
group_b_3 = frappe.get_doc('Item Group', '_Test Item Group B - 3')
```

### Step 3: Assign unknown = value

```python
lft, rgt = (group_b_3.lft, group_b_3.rgt)
```

### Step 4: Assign group_b_3.parent_item_group = '_Test Item Group C'

```python
group_b_3.parent_item_group = '_Test Item Group C'
```

### Step 5: Call group_b_3.save()

```python
group_b_3.save()
```

### Step 6: Call self.test_basic_tree()

```python
self.test_basic_tree()
```

### Step 7: Assign unknown = frappe.db.get_value(...)

```python
new_lft, new_rgt = frappe.db.get_value('Item Group', '_Test Item Group C', ['lft', 'rgt'])
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(old_lft - new_lft, 0)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(new_rgt - old_rgt, rgt - lft + 1)
```

### Step 10: Assign group_b_3 = frappe.get_doc(...)

```python
group_b_3 = frappe.get_doc('Item Group', '_Test Item Group B - 3')
```

### Step 11: Assign group_b_3.parent_item_group = '_Test Item Group B'

```python
group_b_3.parent_item_group = '_Test Item Group B'
```

### Step 12: Call group_b_3.save()

```python
group_b_3.save()
```

### Step 13: Call self.test_basic_tree()

```python
self.test_basic_tree()
```


## Complete Example

```python
# Workflow
old_lft, old_rgt = frappe.db.get_value('Item Group', '_Test Item Group C', ['lft', 'rgt'])
group_b_3 = frappe.get_doc('Item Group', '_Test Item Group B - 3')
lft, rgt = (group_b_3.lft, group_b_3.rgt)
group_b_3.parent_item_group = '_Test Item Group C'
group_b_3.save()
self.test_basic_tree()
new_lft, new_rgt = frappe.db.get_value('Item Group', '_Test Item Group C', ['lft', 'rgt'])
self.assertEqual(old_lft - new_lft, 0)
self.assertEqual(new_rgt - old_rgt, rgt - lft + 1)
group_b_3 = frappe.get_doc('Item Group', '_Test Item Group B - 3')
group_b_3.parent_item_group = '_Test Item Group B'
group_b_3.save()
self.test_basic_tree()
```

## Next Steps


---

*Source: test_item_group.py:99 | Complexity: Advanced | Last updated: 2026-02-04*