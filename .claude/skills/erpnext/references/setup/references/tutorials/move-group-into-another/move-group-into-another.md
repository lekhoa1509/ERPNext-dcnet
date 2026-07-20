# How To: Move Group Into Another

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test move group into another

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

### Step 2: Assign group_b = frappe.get_doc(...)

```python
group_b = frappe.get_doc('Item Group', '_Test Item Group B')
```

### Step 3: Assign unknown = value

```python
lft, rgt = (group_b.lft, group_b.rgt)
```

### Step 4: Assign group_b.parent_item_group = '_Test Item Group C'

```python
group_b.parent_item_group = '_Test Item Group C'
```

### Step 5: Call group_b.save()

```python
group_b.save()
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
self.assertEqual(old_lft - new_lft, rgt - lft + 1)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(new_rgt - old_rgt, 0)
```

### Step 10: Call self._move_it_back()

```python
self._move_it_back()
```


## Complete Example

```python
# Workflow
old_lft, old_rgt = frappe.db.get_value('Item Group', '_Test Item Group C', ['lft', 'rgt'])
group_b = frappe.get_doc('Item Group', '_Test Item Group B')
lft, rgt = (group_b.lft, group_b.rgt)
group_b.parent_item_group = '_Test Item Group C'
group_b.save()
self.test_basic_tree()
new_lft, new_rgt = frappe.db.get_value('Item Group', '_Test Item Group C', ['lft', 'rgt'])
self.assertEqual(old_lft - new_lft, rgt - lft + 1)
self.assertEqual(new_rgt - old_rgt, 0)
self._move_it_back()
```

## Next Steps


---

*Source: test_item_group.py:66 | Complexity: Advanced | Last updated: 2026-02-04*