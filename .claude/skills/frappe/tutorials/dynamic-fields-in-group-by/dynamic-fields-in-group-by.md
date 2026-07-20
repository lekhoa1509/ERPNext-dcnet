# How To: Dynamic Fields In Group By

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test dynamic field support in GROUP BY clause.

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

### Step 1: 'Test dynamic field support in GROUP BY clause.'

```python
'Test dynamic field support in GROUP BY clause.'
```

### Step 2: Assign note = frappe.get_doc.insert(...)

```python
note = frappe.get_doc(doctype='Note', title='Group By Test Note', seen_by=[{'user': 'Administrator'}, {'user': 'Guest'}]).insert()
```

### Step 3: Assign query = frappe.qb.get_query(...)

```python
query = frappe.qb.get_query('DocType', fields=['module.app_name', 'name'], group_by='module.app_name, name')
```

### Step 4: Assign result = query.run(...)

```python
result = query.run(as_dict=True)
```

### Step 5: Call self.assertTrue()

```python
self.assertTrue(len(result) > 0)
```

### Step 6: Assign sql = query.get_sql(...)

```python
sql = query.get_sql()
```

### Step 7: Call self.assertIn()

```python
self.assertIn('LEFT JOIN', sql)
```

### Step 8: Call self.assertIn()

```python
self.assertIn('tabModule Def', sql)
```

### Step 9: Assign query = frappe.qb.get_query(...)

```python
query = frappe.qb.get_query('Note', fields=['seen_by.user', 'name'], filters={'name': note.name}, group_by='seen_by.user, name')
```

### Step 10: Assign result = query.run(...)

```python
result = query.run(as_dict=True)
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(len(result) >= 1)
```

### Step 12: Assign sql = query.get_sql(...)

```python
sql = query.get_sql()
```

### Step 13: Call self.assertIn()

```python
self.assertIn('LEFT JOIN', sql)
```

### Step 14: Call self.assertIn()

```python
self.assertIn('tabNote Seen By', sql)
```

### Step 15: Call note.delete()

```python
note.delete()
```

### Step 16: Call self.fail()

```python
self.fail(f'Dynamic link field in GROUP BY failed: {e}')
```

### Step 17: Call self.fail()

```python
self.fail(f'Dynamic child field in GROUP BY failed: {e}')
```


## Complete Example

```python
# Setup
setup_for_tests()

# Workflow
'Test dynamic field support in GROUP BY clause.'
try:
    query = frappe.qb.get_query('DocType', fields=['module.app_name', 'name'], group_by='module.app_name, name')
    result = query.run(as_dict=True)
    self.assertTrue(len(result) > 0)
    sql = query.get_sql()
    self.assertIn('LEFT JOIN', sql)
    self.assertIn('tabModule Def', sql)
except Exception as e:
    self.fail(f'Dynamic link field in GROUP BY failed: {e}')
note = frappe.get_doc(doctype='Note', title='Group By Test Note', seen_by=[{'user': 'Administrator'}, {'user': 'Guest'}]).insert()
try:
    query = frappe.qb.get_query('Note', fields=['seen_by.user', 'name'], filters={'name': note.name}, group_by='seen_by.user, name')
    result = query.run(as_dict=True)
    self.assertTrue(len(result) >= 1)
    sql = query.get_sql()
    self.assertIn('LEFT JOIN', sql)
    self.assertIn('tabNote Seen By', sql)
except Exception as e:
    self.fail(f'Dynamic child field in GROUP BY failed: {e}')
finally:
    note.delete()
```

## Next Steps


---

*Source: test_query.py:1318 | Complexity: Advanced | Last updated: 2026-02-04*