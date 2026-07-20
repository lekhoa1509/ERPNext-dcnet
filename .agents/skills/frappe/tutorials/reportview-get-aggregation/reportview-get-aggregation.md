# How To: Reportview Get Aggregation

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test reportview get aggregation

## Prerequisites

**Required Modules:**
- `datetime`
- `contextlib`
- `unittest.mock`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.core.page.permission_manager.permission_manager`
- `frappe.custom.doctype.property_setter.property_setter`
- `frappe.database.utils`
- `frappe.desk.reportview`
- `frappe.handler`
- `frappe.model.db_query`
- `frappe.permissions`
- `frappe.query_builder`
- `frappe.tests`
- `frappe.tests.test_helpers`
- `frappe.tests.test_query_builder`
- `frappe.utils.testutils`
- `frappe.utils`
- `frappe.desk.search`
- `frappe.core.page.permission_manager.permission_manager`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.desk.doctype.dashboard_settings.dashboard_settings`
- `frappe.desk.reportview`
- `frappe.desk`
- `frappe.types.filter`


## Step-by-Step Guide

### Step 1: Assign frappe.local.request = frappe._dict(...)

```python
frappe.local.request = frappe._dict()
```

### Step 2: Assign frappe.local.request.method = 'POST'

```python
frappe.local.request.method = 'POST'
```

### Step 3: Assign frappe.local.form_dict = frappe._dict(...)

```python
frappe.local.form_dict = frappe._dict({'doctype': 'DocType', 'fields': '["`tabDocField`.`label` as field_label","`tabDocField`.`name` as field_name"]', 'filters': '[]', 'order_by': '_aggregate_column desc', 'start': 0, 'page_length': 20, 'view': 'Report', 'with_comment_count': 0, 'group_by': 'field_label, field_name', 'aggregate_on_field': 'columns', 'aggregate_on_doctype': 'DocField', 'aggregate_function': 'sum'})
```

### Step 4: Assign response = execute_cmd(...)

```python
response = execute_cmd('frappe.desk.reportview.get')
```

### Step 5: Call self.assertListEqual()

```python
self.assertListEqual(response['keys'], ['field_label', 'field_name', '_aggregate_column'])
```


## Complete Example

```python
# Workflow
frappe.local.request = frappe._dict()
frappe.local.request.method = 'POST'
frappe.local.form_dict = frappe._dict({'doctype': 'DocType', 'fields': '["`tabDocField`.`label` as field_label","`tabDocField`.`name` as field_name"]', 'filters': '[]', 'order_by': '_aggregate_column desc', 'start': 0, 'page_length': 20, 'view': 'Report', 'with_comment_count': 0, 'group_by': 'field_label, field_name', 'aggregate_on_field': 'columns', 'aggregate_on_doctype': 'DocField', 'aggregate_function': 'sum'})
response = execute_cmd('frappe.desk.reportview.get')
self.assertListEqual(response['keys'], ['field_label', 'field_name', '_aggregate_column'])
```

## Next Steps


---

*Source: test_db_query.py:1315 | Complexity: Intermediate | Last updated: 2026-02-04*