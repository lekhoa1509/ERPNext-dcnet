# How To: Move Group Into Another

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test move group into another

## Prerequisites

**Required Modules:**
- `unittest.mock`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.desk.treeview`
- `frappe.query_builder`
- `frappe.query_builder.functions`
- `frappe.tests`
- `frappe.utils`
- `frappe.utils.nestedset`


## Step-by-Step Guide

### Step 1: Assign unknown = frappe.db.get_value(...)

```python
old_lft, old_rgt = frappe.db.get_value(TEST_DOCTYPE, 'Parent 2', ['lft', 'rgt'])
```

### Step 2: Assign parent_1 = frappe.get_doc(...)

```python
parent_1 = frappe.get_doc(TEST_DOCTYPE, 'Parent 1')
```

### Step 3: Assign unknown = value

```python
lft, rgt = (parent_1.lft, parent_1.rgt)
```

### Step 4: Assign parent_1.parent_test_tree_doctype = 'Parent 2'

```python
parent_1.parent_test_tree_doctype = 'Parent 2'
```

### Step 5: Call parent_1.save()

```python
parent_1.save()
```

### Step 6: Call self.test_basic_tree()

```python
self.test_basic_tree()
```

### Step 7: Assign unknown = frappe.db.get_value(...)

```python
new_lft, new_rgt = frappe.db.get_value(TEST_DOCTYPE, 'Parent 2', ['lft', 'rgt'])
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(old_lft - new_lft, rgt - lft + 1)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(new_rgt - old_rgt, 0)
```

### Step 10: Call self.nsu.move_it_back()

```python
self.nsu.move_it_back()
```

### Step 11: Call self.test_basic_tree()

```python
self.test_basic_tree()
```


## Complete Example

```python
# Workflow
old_lft, old_rgt = frappe.db.get_value(TEST_DOCTYPE, 'Parent 2', ['lft', 'rgt'])
parent_1 = frappe.get_doc(TEST_DOCTYPE, 'Parent 1')
lft, rgt = (parent_1.lft, parent_1.rgt)
parent_1.parent_test_tree_doctype = 'Parent 2'
parent_1.save()
self.test_basic_tree()
new_lft, new_rgt = frappe.db.get_value(TEST_DOCTYPE, 'Parent 2', ['lft', 'rgt'])
self.assertEqual(old_lft - new_lft, rgt - lft + 1)
self.assertEqual(new_rgt - old_rgt, 0)
self.nsu.move_it_back()
self.test_basic_tree()
```

## Next Steps


---

*Source: test_nestedset.py:151 | Complexity: Advanced | Last updated: 2026-02-04*