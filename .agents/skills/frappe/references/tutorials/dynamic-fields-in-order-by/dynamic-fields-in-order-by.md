# How To: Dynamic Fields In Order By

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test dynamic field support in ORDER BY clause.

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

### Step 1: 'Test dynamic field support in ORDER BY clause.'

```python
'Test dynamic field support in ORDER BY clause.'
```

### Step 2: Assign note1 = frappe.get_doc.insert(...)

```python
note1 = frappe.get_doc(doctype='Note', title='Order Test Note 1', seen_by=[{'user': 'Administrator'}]).insert()
```

### Step 3: Assign note2 = frappe.get_doc.insert(...)

```python
note2 = frappe.get_doc(doctype='Note', title='Order Test Note 2', seen_by=[{'user': 'Guest'}]).insert()
```

### Step 4: Assign query = frappe.qb.get_query(...)

```python
query = frappe.qb.get_query('DocType', fields=['name', 'module.app_name'], order_by='module.app_name DESC', limit=5)
```

### Step 5: Assign result = query.run(...)

```python
result = query.run(as_dict=True)
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue(len(result) > 0)
```

### Step 7: Assign sql = query.get_sql(...)

```python
sql = query.get_sql()
```

### Step 8: Call self.assertIn()

```python
self.assertIn('LEFT JOIN', sql)
```

### Step 9: Call self.assertIn()

```python
self.assertIn('tabModule Def', sql)
```

### Step 10: Call self.assertIn()

```python
self.assertIn('ORDER BY', sql)
```

### Step 11: Assign query = frappe.qb.get_query(...)

```python
query = frappe.qb.get_query('Note', fields=['name', 'seen_by.user'], filters={'name': ['in', [note1.name, note2.name]]}, order_by='seen_by.user ASC')
```

### Step 12: Assign result = query.run(...)

```python
result = query.run(as_dict=True)
```

### Step 13: Call self.assertTrue()

```python
self.assertTrue(len(result) >= 2)
```

### Step 14: Assign sql = query.get_sql(...)

```python
sql = query.get_sql()
```

### Step 15: Call self.assertIn()

```python
self.assertIn('LEFT JOIN', sql)
```

### Step 16: Call self.assertIn()

```python
self.assertIn('tabNote Seen By', sql)
```

### Step 17: Call note1.delete()

```python
note1.delete()
```

### Step 18: Call note2.delete()

```python
note2.delete()
```

### Step 19: Call self.fail()

```python
self.fail(f'Dynamic link field in ORDER BY failed: {e}')
```

### Step 20: Call self.fail()

```python
self.fail(f'Dynamic child field in ORDER BY failed: {e}')
```


## Complete Example

```python
# Setup
setup_for_tests()

# Workflow
'Test dynamic field support in ORDER BY clause.'
try:
    query = frappe.qb.get_query('DocType', fields=['name', 'module.app_name'], order_by='module.app_name DESC', limit=5)
    result = query.run(as_dict=True)
    self.assertTrue(len(result) > 0)
    sql = query.get_sql()
    self.assertIn('LEFT JOIN', sql)
    self.assertIn('tabModule Def', sql)
    self.assertIn('ORDER BY', sql)
except Exception as e:
    self.fail(f'Dynamic link field in ORDER BY failed: {e}')
note1 = frappe.get_doc(doctype='Note', title='Order Test Note 1', seen_by=[{'user': 'Administrator'}]).insert()
note2 = frappe.get_doc(doctype='Note', title='Order Test Note 2', seen_by=[{'user': 'Guest'}]).insert()
try:
    query = frappe.qb.get_query('Note', fields=['name', 'seen_by.user'], filters={'name': ['in', [note1.name, note2.name]]}, order_by='seen_by.user ASC')
    result = query.run(as_dict=True)
    self.assertTrue(len(result) >= 2)
    sql = query.get_sql()
    self.assertIn('LEFT JOIN', sql)
    self.assertIn('tabNote Seen By', sql)
except Exception as e:
    self.fail(f'Dynamic child field in ORDER BY failed: {e}')
finally:
    note1.delete()
    note2.delete()
```

## Next Steps


---

*Source: test_query.py:1355 | Complexity: Advanced | Last updated: 2026-02-04*