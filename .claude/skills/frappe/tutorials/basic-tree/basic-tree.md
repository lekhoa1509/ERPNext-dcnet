# How To: Basic Tree

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test basic tree

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

### Step 1: Assign min_lft = 1

```python
min_lft = 1
```

### Step 2: Assign max_rgt = value

```python
max_rgt = frappe.qb.from_(TEST_DOCTYPE).select(Max(Field('rgt'))).run(pluck=True)[0]
```

### Step 3: Assign unknown = frappe.db.get_value(...)

```python
lft, rgt, parent_test_tree_doctype = frappe.db.get_value(TEST_DOCTYPE, record['some_fieldname'], ['lft', 'rgt', 'parent_test_tree_doctype'])
```

### Step 4: Call self.assertTrue()

```python
self.assertTrue(lft)
```

### Step 5: Call self.assertTrue()

```python
self.assertTrue(rgt)
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue(lft < rgt)
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue(parent_lft < parent_rgt)
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(lft > parent_lft)
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue(rgt < parent_rgt)
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue(lft >= min_lft)
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(rgt <= max_rgt)
```

### Step 12: Assign no_of_children = self.nsu.get_no_of_children(...)

```python
no_of_children = self.nsu.get_no_of_children(record['some_fieldname'])
```

### Step 13: Call self.assertTrue()

```python
self.assertTrue(rgt == lft + 1 + 2 * no_of_children, msg=(record, no_of_children, self.nsu.get_no_of_children(record['some_fieldname'])))
```

### Step 14: Assign no_of_children = self.nsu.get_no_of_children(...)

```python
no_of_children = self.nsu.get_no_of_children(parent_test_tree_doctype)
```

### Step 15: Call self.assertTrue()

```python
self.assertTrue(parent_rgt == parent_lft + 1 + 2 * no_of_children)
```

### Step 16: Assign unknown = frappe.db.get_value(...)

```python
parent_lft, parent_rgt = frappe.db.get_value(TEST_DOCTYPE, parent_test_tree_doctype, ['lft', 'rgt'])
```

### Step 17: Assign parent_lft = value

```python
parent_lft = min_lft - 1
```

### Step 18: Assign parent_rgt = value

```python
parent_rgt = max_rgt + 1
```


## Complete Example

```python
# Workflow
global records
min_lft = 1
max_rgt = frappe.qb.from_(TEST_DOCTYPE).select(Max(Field('rgt'))).run(pluck=True)[0]
for record in records:
    lft, rgt, parent_test_tree_doctype = frappe.db.get_value(TEST_DOCTYPE, record['some_fieldname'], ['lft', 'rgt', 'parent_test_tree_doctype'])
    if parent_test_tree_doctype:
        parent_lft, parent_rgt = frappe.db.get_value(TEST_DOCTYPE, parent_test_tree_doctype, ['lft', 'rgt'])
    else:
        parent_lft = min_lft - 1
        parent_rgt = max_rgt + 1
    self.assertTrue(lft)
    self.assertTrue(rgt)
    self.assertTrue(lft < rgt)
    self.assertTrue(parent_lft < parent_rgt)
    self.assertTrue(lft > parent_lft)
    self.assertTrue(rgt < parent_rgt)
    self.assertTrue(lft >= min_lft)
    self.assertTrue(rgt <= max_rgt)
    no_of_children = self.nsu.get_no_of_children(record['some_fieldname'])
    self.assertTrue(rgt == lft + 1 + 2 * no_of_children, msg=(record, no_of_children, self.nsu.get_no_of_children(record['some_fieldname'])))
    no_of_children = self.nsu.get_no_of_children(parent_test_tree_doctype)
    self.assertTrue(parent_rgt == parent_lft + 1 + 2 * no_of_children)
```

## Next Steps


---

*Source: test_nestedset.py:101 | Complexity: Advanced | Last updated: 2026-02-04*