# How To: Child Field Syntax

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test child field syntax

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `itertools`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.permissions`
- `frappe.query_builder`
- `frappe.query_builder.functions`
- `frappe.tests`
- `frappe.tests.classes.context_managers`
- `frappe.tests.test_db_query`
- `frappe.tests.test_helpers`
- `frappe.tests.test_query_builder`
- `frappe.utils.nestedset`
- `frappe.permissions`
- `frappe.permissions`
- `frappe.core.page.permission_manager.permission_manager`
- `frappe.desk.doctype.dashboard_settings.dashboard_settings`
- `frappe.share`
- `frappe.share`
- `frappe.core.page.permission_manager.permission_manager`
- `frappe.share`
- `frappe.permissions`
- `frappe.core.page.permission_manager.permission_manager`
- `frappe.permissions`
- `frappe.database.query`

**Setup Required:**
```python
setup_for_tests()
```

## Step-by-Step Guide

### Step 1: Assign note1 = frappe.get_doc.insert(...)

```python
note1 = frappe.get_doc(doctype='Note', title='Note 1', seen_by=[{'user': 'Administrator'}]).insert()
```

### Step 2: Assign note2 = frappe.get_doc.insert(...)

```python
note2 = frappe.get_doc(doctype='Note', title='Note 2', seen_by=[{'user': 'Administrator'}, {'user': 'Guest'}]).insert()
```

### Step 3: Assign result = frappe.qb.get_query.run(...)

```python
result = frappe.qb.get_query('Note', filters={'name': ['in', [note1.name, note2.name]]}, fields=['name', {'seen_by': ['*']}], order_by='title asc').run(as_dict=1)
```

### Step 4: Call self.assertTrue()

```python
self.assertTrue(isinstance(result[0].seen_by, list))
```

### Step 5: Call self.assertTrue()

```python
self.assertTrue(isinstance(result[1].seen_by, list))
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(len(result[0].seen_by), 1)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(len(result[1].seen_by), 2)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(result[0].seen_by[0].user, 'Administrator')
```

### Step 9: Assign result = frappe.qb.get_query.run(...)

```python
result = frappe.qb.get_query('Note', filters={'name': ['in', [note1.name, note2.name]]}, fields=['name', {'seen_by': ['user']}], order_by='title asc').run(as_dict=1)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(len(result[0].seen_by[0].keys()), 1)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(result[1].seen_by[1].user, 'Guest')
```

### Step 12: Call note1.delete()

```python
note1.delete()
```

### Step 13: Call note2.delete()

```python
note2.delete()
```


## Complete Example

```python
# Setup
setup_for_tests()

# Workflow
note1 = frappe.get_doc(doctype='Note', title='Note 1', seen_by=[{'user': 'Administrator'}]).insert()
note2 = frappe.get_doc(doctype='Note', title='Note 2', seen_by=[{'user': 'Administrator'}, {'user': 'Guest'}]).insert()
result = frappe.qb.get_query('Note', filters={'name': ['in', [note1.name, note2.name]]}, fields=['name', {'seen_by': ['*']}], order_by='title asc').run(as_dict=1)
self.assertTrue(isinstance(result[0].seen_by, list))
self.assertTrue(isinstance(result[1].seen_by, list))
self.assertEqual(len(result[0].seen_by), 1)
self.assertEqual(len(result[1].seen_by), 2)
self.assertEqual(result[0].seen_by[0].user, 'Administrator')
result = frappe.qb.get_query('Note', filters={'name': ['in', [note1.name, note2.name]]}, fields=['name', {'seen_by': ['user']}], order_by='title asc').run(as_dict=1)
self.assertEqual(len(result[0].seen_by[0].keys()), 1)
self.assertEqual(result[1].seen_by[1].user, 'Guest')
note1.delete()
note2.delete()
```

## Next Steps


---

*Source: test_query.py:819 | Complexity: Advanced | Last updated: 2026-02-04*