# How To: Delete Leaf

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test delete leaf

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils.nestedset`
- `json`


## Step-by-Step Guide

### Step 1: Assign parent_item_group = frappe.db.get_value(...)

```python
parent_item_group = frappe.db.get_value('Item Group', '_Test Item Group B - 3', 'parent_item_group')
```

### Step 2: Call frappe.db.get_value()

```python
frappe.db.get_value('Item Group', parent_item_group, 'rgt')
```

### Step 3: Assign ancestors = get_ancestors_of(...)

```python
ancestors = get_ancestors_of('Item Group', '_Test Item Group B - 3')
```

### Step 4: Assign ancestors = frappe.db.sql(...)

```python
ancestors = frappe.db.sql('select name, rgt from `tabItem Group`\n\t\t\twhere name in ({})'.format(', '.join(['%s'] * len(ancestors))), tuple(ancestors), as_dict=True)
```

### Step 5: Call frappe.delete_doc()

```python
frappe.delete_doc('Item Group', '_Test Item Group B - 3')
```

### Step 6: Assign records_to_test = value

```python
records_to_test = self.globalTestRecords['Item Group'][2:]
```

### Step 7: Call self.test_basic_tree()

```python
self.test_basic_tree(records=records_to_test)
```

### Step 8: Call frappe.copy_doc.insert()

```python
frappe.copy_doc(self.globalTestRecords['Item Group'][6]).insert()
```

### Step 9: Call self.test_basic_tree()

```python
self.test_basic_tree()
```

### Step 10: Assign unknown = frappe.db.get_value(...)

```python
new_lft, new_rgt = frappe.db.get_value('Item Group', item_group.name, ['lft', 'rgt'])
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(new_rgt, item_group.rgt - 2)
```


## Complete Example

```python
# Workflow
parent_item_group = frappe.db.get_value('Item Group', '_Test Item Group B - 3', 'parent_item_group')
frappe.db.get_value('Item Group', parent_item_group, 'rgt')
ancestors = get_ancestors_of('Item Group', '_Test Item Group B - 3')
ancestors = frappe.db.sql('select name, rgt from `tabItem Group`\n\t\t\twhere name in ({})'.format(', '.join(['%s'] * len(ancestors))), tuple(ancestors), as_dict=True)
frappe.delete_doc('Item Group', '_Test Item Group B - 3')
records_to_test = self.globalTestRecords['Item Group'][2:]
del records_to_test[4]
self.test_basic_tree(records=records_to_test)
for item_group in ancestors:
    new_lft, new_rgt = frappe.db.get_value('Item Group', item_group.name, ['lft', 'rgt'])
    self.assertEqual(new_rgt, item_group.rgt - 2)
frappe.copy_doc(self.globalTestRecords['Item Group'][6]).insert()
self.test_basic_tree()
```

## Next Steps


---

*Source: test_item_group.py:125 | Complexity: Advanced | Last updated: 2026-02-04*