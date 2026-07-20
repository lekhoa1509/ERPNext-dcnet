# How To: Nested Filters

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test nested filter conditions with AND/OR logic.

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

### Step 1: 'Test nested filter conditions with AND/OR logic.'

```python
'Test nested filter conditions with AND/OR logic.'
```

### Step 2: Assign User = frappe.qb.DocType(...)

```python
User = frappe.qb.DocType('User')
```

### Step 3: Assign filters_and = value

```python
filters_and = [['email', '=', 'admin@example.com'], 'and', ['first_name', '=', 'Admin']]
```

### Step 4: Assign expected_sql_and = frappe.qb.from_.select.where.get_sql(...)

```python
expected_sql_and = frappe.qb.from_(User).select(User.name).where((User.email == 'admin@example.com') & (User.first_name == 'Admin')).get_sql()
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(frappe.qb.get_query('User', filters=filters_and).get_sql(), expected_sql_and)
```

### Step 6: Assign filters_or = value

```python
filters_or = [['email', '=', 'admin@example.com'], 'or', ['email', '=', 'guest@example.com']]
```

### Step 7: Assign expected_sql_or = frappe.qb.from_.select.where.get_sql(...)

```python
expected_sql_or = frappe.qb.from_(User).select(User.name).where((User.email == 'admin@example.com') | (User.email == 'guest@example.com')).get_sql()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(frappe.qb.get_query('User', filters=filters_or).get_sql(), expected_sql_or)
```

### Step 9: Assign filters_mixed = value

```python
filters_mixed = [['first_name', '=', 'Admin'], 'and', [['email', '=', 'admin@example.com'], 'or', ['email', '=', 'guest@example.com']]]
```

### Step 10: Assign expected_sql_mixed = frappe.qb.from_.select.where.get_sql(...)

```python
expected_sql_mixed = frappe.qb.from_(User).select(User.name).where((User.first_name == 'Admin') & ((User.email == 'admin@example.com') | (User.email == 'guest@example.com'))).get_sql()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(frappe.qb.get_query('User', filters=filters_mixed).get_sql(), expected_sql_mixed)
```

### Step 12: Assign filters_nested = value

```python
filters_nested = [[['first_name', '=', 'Admin'], 'and', ['enabled', '=', 1]], 'or', [['first_name', '=', 'Guest'], 'and', ['enabled', '=', 0]]]
```

### Step 13: Assign expected_sql_nested = frappe.qb.from_.select.where.get_sql(...)

```python
expected_sql_nested = frappe.qb.from_(User).select(User.name).where((User.first_name == 'Admin') & (User.enabled == 1) | (User.first_name == 'Guest') & (User.enabled == 0)).get_sql()
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(frappe.qb.get_query('User', filters=filters_nested).get_sql(), expected_sql_nested)
```

### Step 15: Assign filters_single_group = value

```python
filters_single_group = [[['first_name', '=', 'Admin'], 'and', ['enabled', '=', 1]]]
```

### Step 16: Assign expected_sql_single_group = frappe.qb.from_.select.where.get_sql(...)

```python
expected_sql_single_group = frappe.qb.from_(User).select(User.name).where((User.first_name == 'Admin') & (User.enabled == 1)).get_sql()
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(frappe.qb.get_query('User', filters=filters_single_group).get_sql(), expected_sql_single_group)
```

### Step 18: Assign filters_complex = value

```python
filters_complex = [['creation', '>', '2023-01-01'], 'and', [['email', 'like', '%@example.com'], 'or', [['first_name', 'in', ['Admin', 'Guest']], 'and', ['enabled', '!=', 1]]]]
```

### Step 19: Assign expected_sql_complex = frappe.qb.from_.select.where.get_sql(...)

```python
expected_sql_complex = frappe.qb.from_(User).select(User.name).where((User.creation > '2023-01-01') & ((User.email.ilike('%@example.com') if frappe.db.db_type == 'postgres' else User.email.like('%@example.com')) | User.first_name.isin(['Admin', 'Guest']) & (User.enabled != 1))).get_sql()
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(frappe.qb.get_query('User', filters=filters_complex).get_sql(), expected_sql_complex)
```


## Complete Example

```python
# Setup
setup_for_tests()

# Workflow
'Test nested filter conditions with AND/OR logic.'
User = frappe.qb.DocType('User')
filters_and = [['email', '=', 'admin@example.com'], 'and', ['first_name', '=', 'Admin']]
expected_sql_and = frappe.qb.from_(User).select(User.name).where((User.email == 'admin@example.com') & (User.first_name == 'Admin')).get_sql()
self.assertEqual(frappe.qb.get_query('User', filters=filters_and).get_sql(), expected_sql_and)
filters_or = [['email', '=', 'admin@example.com'], 'or', ['email', '=', 'guest@example.com']]
expected_sql_or = frappe.qb.from_(User).select(User.name).where((User.email == 'admin@example.com') | (User.email == 'guest@example.com')).get_sql()
self.assertEqual(frappe.qb.get_query('User', filters=filters_or).get_sql(), expected_sql_or)
filters_mixed = [['first_name', '=', 'Admin'], 'and', [['email', '=', 'admin@example.com'], 'or', ['email', '=', 'guest@example.com']]]
expected_sql_mixed = frappe.qb.from_(User).select(User.name).where((User.first_name == 'Admin') & ((User.email == 'admin@example.com') | (User.email == 'guest@example.com'))).get_sql()
self.assertEqual(frappe.qb.get_query('User', filters=filters_mixed).get_sql(), expected_sql_mixed)
filters_nested = [[['first_name', '=', 'Admin'], 'and', ['enabled', '=', 1]], 'or', [['first_name', '=', 'Guest'], 'and', ['enabled', '=', 0]]]
expected_sql_nested = frappe.qb.from_(User).select(User.name).where((User.first_name == 'Admin') & (User.enabled == 1) | (User.first_name == 'Guest') & (User.enabled == 0)).get_sql()
self.assertEqual(frappe.qb.get_query('User', filters=filters_nested).get_sql(), expected_sql_nested)
filters_single_group = [[['first_name', '=', 'Admin'], 'and', ['enabled', '=', 1]]]
expected_sql_single_group = frappe.qb.from_(User).select(User.name).where((User.first_name == 'Admin') & (User.enabled == 1)).get_sql()
self.assertEqual(frappe.qb.get_query('User', filters=filters_single_group).get_sql(), expected_sql_single_group)
filters_complex = [['creation', '>', '2023-01-01'], 'and', [['email', 'like', '%@example.com'], 'or', [['first_name', 'in', ['Admin', 'Guest']], 'and', ['enabled', '!=', 1]]]]
expected_sql_complex = frappe.qb.from_(User).select(User.name).where((User.creation > '2023-01-01') & ((User.email.ilike('%@example.com') if frappe.db.db_type == 'postgres' else User.email.like('%@example.com')) | User.first_name.isin(['Admin', 'Guest']) & (User.enabled != 1))).get_sql()
self.assertEqual(frappe.qb.get_query('User', filters=filters_complex).get_sql(), expected_sql_complex)
```

## Next Steps


---

*Source: test_query.py:571 | Complexity: Advanced | Last updated: 2026-02-04*