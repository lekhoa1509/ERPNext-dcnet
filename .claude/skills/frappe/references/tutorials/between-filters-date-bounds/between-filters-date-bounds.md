# How To: Between Filters Date Bounds

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test between filters date bounds

## Prerequisites

- [ ] Setup code must be executed first

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

**Setup Required:**
```python
setup_for_tests()
frappe.set_user('Administrator')
```

## Step-by-Step Guide

### Step 1: Assign date_df = frappe._dict(...)

```python
date_df = frappe._dict(fieldtype='Date')
```

### Step 2: Assign datetime_df = frappe._dict(...)

```python
datetime_df = frappe._dict(fieldtype='Datetime')
```

### Step 3: Assign today = frappe.utils.nowdate(...)

```python
today = frappe.utils.nowdate()
```

### Step 4: Assign cond = get_between_date_filter(...)

```python
cond = get_between_date_filter('', date_df)
```

### Step 5: Call self.assertQueryEqual()

```python
self.assertQueryEqual(cond, f"'{today}' AND '{today}'")
```

### Step 6: Assign start = '2021-01-01'

```python
start = '2021-01-01'
```

### Step 7: Assign cond = get_between_date_filter(...)

```python
cond = get_between_date_filter([start], date_df)
```

### Step 8: Call self.assertQueryEqual()

```python
self.assertQueryEqual(cond, f"'{start}' AND '{today}'")
```

### Step 9: Assign start = '2021-01-01'

```python
start = '2021-01-01'
```

### Step 10: Assign end = '2022-01-02'

```python
end = '2022-01-02'
```

### Step 11: Assign cond = get_between_date_filter(...)

```python
cond = get_between_date_filter([start, end], date_df)
```

### Step 12: Call self.assertQueryEqual()

```python
self.assertQueryEqual(cond, f"'{start}' AND '{end}'")
```

### Step 13: Assign start = '2021-01-01'

```python
start = '2021-01-01'
```

### Step 14: Assign cond = get_between_date_filter(...)

```python
cond = get_between_date_filter([start, start], datetime_df)
```

### Step 15: Call self.assertQueryEqual()

```python
self.assertQueryEqual(cond, f"'{start} 00:00:00.000000' AND '{start} 23:59:59.999999'")
```

### Step 16: Assign start = '2021-01-01 01:01:00'

```python
start = '2021-01-01 01:01:00'
```

### Step 17: Assign end = '2022-01-02 12:23:43'

```python
end = '2022-01-02 12:23:43'
```

### Step 18: Assign cond = get_between_date_filter(...)

```python
cond = get_between_date_filter([start, end], datetime_df)
```

### Step 19: Call self.assertQueryEqual()

```python
self.assertQueryEqual(cond, f"'{start}.000000' AND '{end}.000000'")
```


## Complete Example

```python
# Setup
setup_for_tests()
frappe.set_user('Administrator')

# Workflow
date_df = frappe._dict(fieldtype='Date')
datetime_df = frappe._dict(fieldtype='Datetime')
today = frappe.utils.nowdate()
cond = get_between_date_filter('', date_df)
self.assertQueryEqual(cond, f"'{today}' AND '{today}'")
start = '2021-01-01'
cond = get_between_date_filter([start], date_df)
self.assertQueryEqual(cond, f"'{start}' AND '{today}'")
start = '2021-01-01'
end = '2022-01-02'
cond = get_between_date_filter([start, end], date_df)
self.assertQueryEqual(cond, f"'{start}' AND '{end}'")
start = '2021-01-01'
cond = get_between_date_filter([start, start], datetime_df)
self.assertQueryEqual(cond, f"'{start} 00:00:00.000000' AND '{start} 23:59:59.999999'")
start = '2021-01-01 01:01:00'
end = '2022-01-02 12:23:43'
cond = get_between_date_filter([start, end], datetime_df)
self.assertQueryEqual(cond, f"'{start}.000000' AND '{end}.000000'")
```

## Next Steps


---

*Source: test_db_query.py:340 | Complexity: Advanced | Last updated: 2026-02-04*