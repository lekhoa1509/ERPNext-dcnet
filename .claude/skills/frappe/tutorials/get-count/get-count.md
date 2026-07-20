# How To: Get Count

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test get count

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

### Step 2: Assign frappe.local.request.method = 'GET'

```python
frappe.local.request.method = 'GET'
```

### Step 3: Assign frappe.local.form_dict = frappe._dict(...)

```python
frappe.local.form_dict = frappe._dict({'doctype': 'DocType', 'filters': [['DocType', 'show_title_field_in_link', '=', 1]], 'fields': [], 'distinct': 'false'})
```

### Step 4: Assign count = execute_cmd(...)

```python
count = execute_cmd('frappe.desk.reportview.get_count')
```

### Step 5: Assign frappe.local.form_dict = frappe._dict(...)

```python
frappe.local.form_dict = frappe._dict({'doctype': 'DocType', 'filters': {'show_title_field_in_link': 1}, 'distinct': 'true'})
```

### Step 6: Assign dict_filter_response = execute_cmd(...)

```python
dict_filter_response = execute_cmd('frappe.desk.reportview.get_count')
```

### Step 7: Call self.assertIsInstance()

```python
self.assertIsInstance(count, int)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(count, dict_filter_response)
```

### Step 9: Assign frappe.local.form_dict = frappe._dict(...)

```python
frappe.local.form_dict = frappe._dict({'doctype': 'DocType', 'filters': [['DocField', 'fieldtype', '=', 'Data']], 'fields': [], 'distinct': 'true'})
```

### Step 10: Assign child_filter_response = execute_cmd(...)

```python
child_filter_response = execute_cmd('frappe.desk.reportview.get_count')
```

### Step 11: Assign current_value = value

```python
current_value = frappe.db.sql("select count(distinct `tabDocType`.name) as total_count from `tabDocType` left join `tabDocField` on (`tabDocField`.parenttype = 'DocType' and `tabDocField`.parent = `tabDocType`.name) where `tabDocField`.`fieldtype` = 'Data'")[0][0]
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(child_filter_response, current_value)
```

### Step 13: Assign limit = 2

```python
limit = 2
```

### Step 14: Assign frappe.local.form_dict = frappe._dict(...)

```python
frappe.local.form_dict = frappe._dict({'doctype': 'DocType', 'filters': [['DocType', 'is_virtual', '=', 1]], 'fields': [], 'distinct': 'false', 'limit': limit})
```

### Step 15: Assign count = execute_cmd(...)

```python
count = execute_cmd('frappe.desk.reportview.get_count')
```

### Step 16: Call self.assertIsInstance()

```python
self.assertIsInstance(count, int)
```

### Step 17: Call self.assertLessEqual()

```python
self.assertLessEqual(count, limit)
```

### Step 18: Assign limit = 2

```python
limit = 2
```

### Step 19: Assign frappe.local.form_dict = frappe._dict(...)

```python
frappe.local.form_dict = frappe._dict({'doctype': 'DocType', 'fields': [], 'distinct': 'true', 'limit': limit})
```

### Step 20: Assign count = execute_cmd(...)

```python
count = execute_cmd('frappe.desk.reportview.get_count')
```

### Step 21: Call self.assertIsInstance()

```python
self.assertIsInstance(count, int)
```

### Step 22: Call self.assertLessEqual()

```python
self.assertLessEqual(count, limit)
```


## Complete Example

```python
# Workflow
frappe.local.request = frappe._dict()
frappe.local.request.method = 'GET'
frappe.local.form_dict = frappe._dict({'doctype': 'DocType', 'filters': [['DocType', 'show_title_field_in_link', '=', 1]], 'fields': [], 'distinct': 'false'})
count = execute_cmd('frappe.desk.reportview.get_count')
frappe.local.form_dict = frappe._dict({'doctype': 'DocType', 'filters': {'show_title_field_in_link': 1}, 'distinct': 'true'})
dict_filter_response = execute_cmd('frappe.desk.reportview.get_count')
self.assertIsInstance(count, int)
self.assertEqual(count, dict_filter_response)
frappe.local.form_dict = frappe._dict({'doctype': 'DocType', 'filters': [['DocField', 'fieldtype', '=', 'Data']], 'fields': [], 'distinct': 'true'})
child_filter_response = execute_cmd('frappe.desk.reportview.get_count')
current_value = frappe.db.sql("select count(distinct `tabDocType`.name) as total_count from `tabDocType` left join `tabDocField` on (`tabDocField`.parenttype = 'DocType' and `tabDocField`.parent = `tabDocType`.name) where `tabDocField`.`fieldtype` = 'Data'")[0][0]
self.assertEqual(child_filter_response, current_value)
limit = 2
frappe.local.form_dict = frappe._dict({'doctype': 'DocType', 'filters': [['DocType', 'is_virtual', '=', 1]], 'fields': [], 'distinct': 'false', 'limit': limit})
count = execute_cmd('frappe.desk.reportview.get_count')
self.assertIsInstance(count, int)
self.assertLessEqual(count, limit)
limit = 2
frappe.local.form_dict = frappe._dict({'doctype': 'DocType', 'fields': [], 'distinct': 'true', 'limit': limit})
count = execute_cmd('frappe.desk.reportview.get_count')
self.assertIsInstance(count, int)
self.assertLessEqual(count, limit)
```

## Next Steps


---

*Source: test_db_query.py:1169 | Complexity: Advanced | Last updated: 2026-02-04*