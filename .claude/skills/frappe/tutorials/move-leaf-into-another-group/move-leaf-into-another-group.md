# How To: Move Leaf Into Another Group

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test move leaf into another group

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

### Step 1: Assign child_2 = frappe.get_doc(...)

```python
child_2 = frappe.get_doc(TEST_DOCTYPE, 'Child 2')
```

### Step 2: Assign unknown = frappe.db.get_value(...)

```python
parent_lft_old, parent_rgt_old = frappe.db.get_value(TEST_DOCTYPE, 'Parent 2', ['lft', 'rgt'])
```

### Step 3: Call self.assertTrue()

```python
self.assertTrue(parent_lft_old > child_2.lft and parent_rgt_old > child_2.rgt)
```

### Step 4: Assign child_2.parent_test_tree_doctype = 'Parent 2'

```python
child_2.parent_test_tree_doctype = 'Parent 2'
```

### Step 5: Call child_2.save()

```python
child_2.save()
```

### Step 6: Call self.test_basic_tree()

```python
self.test_basic_tree()
```

### Step 7: Assign unknown = frappe.db.get_value(...)

```python
parent_lft_new, parent_rgt_new = frappe.db.get_value(TEST_DOCTYPE, 'Parent 2', ['lft', 'rgt'])
```

### Step 8: Call self.assertFalse()

```python
self.assertFalse(parent_lft_new > child_2.lft and parent_rgt_new > child_2.rgt)
```


## Complete Example

```python
# Workflow
child_2 = frappe.get_doc(TEST_DOCTYPE, 'Child 2')
parent_lft_old, parent_rgt_old = frappe.db.get_value(TEST_DOCTYPE, 'Parent 2', ['lft', 'rgt'])
self.assertTrue(parent_lft_old > child_2.lft and parent_rgt_old > child_2.rgt)
child_2.parent_test_tree_doctype = 'Parent 2'
child_2.save()
self.test_basic_tree()
parent_lft_new, parent_rgt_new = frappe.db.get_value(TEST_DOCTYPE, 'Parent 2', ['lft', 'rgt'])
self.assertFalse(parent_lft_new > child_2.lft and parent_rgt_new > child_2.rgt)
```

## Next Steps


---

*Source: test_nestedset.py:173 | Complexity: Advanced | Last updated: 2026-02-04*