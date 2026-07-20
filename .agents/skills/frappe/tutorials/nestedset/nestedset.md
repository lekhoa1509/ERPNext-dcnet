# How To: Nestedset

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test nestedset

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

### Step 1: Call frappe.db.sql()

```python
frappe.db.sql("delete from `tabDocType` where `name` = 'Test Tree DocType'")
```

### Step 2: Call frappe.db.sql_ddl()

```python
frappe.db.sql_ddl('drop table if exists `tabTest Tree DocType`')
```

### Step 3: Call create_tree_docs()

```python
create_tree_docs()
```

### Step 4: Assign descendants_result = frappe.qb.get_query.run(...)

```python
descendants_result = frappe.qb.get_query('Test Tree DocType', fields=['name'], filters={'name': ('descendants of', 'Parent 1')}, order_by='creation desc').run(as_list=1)
```

### Step 5: Assign descendants_result = list(...)

```python
descendants_result = list(itertools.chain.from_iterable(descendants_result))
```

### Step 6: Call self.assertListEqual()

```python
self.assertListEqual(descendants_result, get_descendants_of('Test Tree DocType', 'Parent 1'))
```

### Step 7: Assign ancestors_result = frappe.qb.get_query.run(...)

```python
ancestors_result = frappe.qb.get_query('Test Tree DocType', fields=['name'], filters={'name': ('ancestors of', 'Child 2')}, order_by='creation desc').run(as_list=1)
```

### Step 8: Assign ancestors_result = list(...)

```python
ancestors_result = list(itertools.chain.from_iterable(ancestors_result))
```

### Step 9: Call self.assertListEqual()

```python
self.assertListEqual(ancestors_result, get_ancestors_of('Test Tree DocType', 'Child 2'))
```

### Step 10: Assign not_descendants_result = frappe.qb.get_query.run(...)

```python
not_descendants_result = frappe.qb.get_query('Test Tree DocType', fields=['name'], filters={'name': ('not descendants of', 'Parent 1')}, order_by='creation desc').run(as_dict=1)
```

### Step 11: Call self.assertListEqual()

```python
self.assertListEqual(not_descendants_result, frappe.db.get_all('Test Tree DocType', fields=['name'], filters={'name': ('not descendants of', 'Parent 1')}))
```

### Step 12: Assign not_ancestors_result = frappe.qb.get_query.run(...)

```python
not_ancestors_result = frappe.qb.get_query('Test Tree DocType', fields=['name'], filters={'name': ('not ancestors of', 'Child 2')}, order_by='creation desc').run(as_dict=1)
```

### Step 13: Call self.assertListEqual()

```python
self.assertListEqual(not_ancestors_result, frappe.db.get_all('Test Tree DocType', fields=['name'], filters={'name': ('not ancestors of', 'Child 2')}))
```

### Step 14: Call frappe.db.sql()

```python
frappe.db.sql("delete from `tabDocType` where `name` = 'Test Tree DocType'")
```

### Step 15: Call frappe.db.sql_ddl()

```python
frappe.db.sql_ddl('drop table if exists `tabTest Tree DocType`')
```


## Complete Example

```python
# Setup
setup_for_tests()

# Workflow
frappe.db.sql("delete from `tabDocType` where `name` = 'Test Tree DocType'")
frappe.db.sql_ddl('drop table if exists `tabTest Tree DocType`')
create_tree_docs()
descendants_result = frappe.qb.get_query('Test Tree DocType', fields=['name'], filters={'name': ('descendants of', 'Parent 1')}, order_by='creation desc').run(as_list=1)
descendants_result = list(itertools.chain.from_iterable(descendants_result))
self.assertListEqual(descendants_result, get_descendants_of('Test Tree DocType', 'Parent 1'))
ancestors_result = frappe.qb.get_query('Test Tree DocType', fields=['name'], filters={'name': ('ancestors of', 'Child 2')}, order_by='creation desc').run(as_list=1)
ancestors_result = list(itertools.chain.from_iterable(ancestors_result))
self.assertListEqual(ancestors_result, get_ancestors_of('Test Tree DocType', 'Child 2'))
not_descendants_result = frappe.qb.get_query('Test Tree DocType', fields=['name'], filters={'name': ('not descendants of', 'Parent 1')}, order_by='creation desc').run(as_dict=1)
self.assertListEqual(not_descendants_result, frappe.db.get_all('Test Tree DocType', fields=['name'], filters={'name': ('not descendants of', 'Parent 1')}))
not_ancestors_result = frappe.qb.get_query('Test Tree DocType', fields=['name'], filters={'name': ('not ancestors of', 'Child 2')}, order_by='creation desc').run(as_dict=1)
self.assertListEqual(not_ancestors_result, frappe.db.get_all('Test Tree DocType', fields=['name'], filters={'name': ('not ancestors of', 'Child 2')}))
frappe.db.sql("delete from `tabDocType` where `name` = 'Test Tree DocType'")
frappe.db.sql_ddl('drop table if exists `tabTest Tree DocType`')
```

## Next Steps


---

*Source: test_query.py:758 | Complexity: Advanced | Last updated: 2026-02-04*