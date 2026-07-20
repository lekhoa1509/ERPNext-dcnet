# How To: Between Filters

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test case to check between filter for date fields

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

### Step 1: 'test case to check between filter for date fields'

```python
'test case to check between filter for date fields'
```

### Step 2: Call frappe.db.delete()

```python
frappe.db.delete('Event')
```

### Step 3: Assign todays_event = create_event(...)

```python
todays_event = create_event()
```

### Step 4: Assign event1 = create_event(...)

```python
event1 = create_event(starts_on='2016-07-05 23:59:59')
```

### Step 5: Assign event2 = create_event(...)

```python
event2 = create_event(starts_on='2016-07-06 00:00:00')
```

### Step 6: Assign event3 = create_event(...)

```python
event3 = create_event(starts_on='2016-07-07 23:59:59')
```

### Step 7: Assign event4 = create_event(...)

```python
event4 = create_event(starts_on='2016-07-08 00:00:00')
```

### Step 8: Assign data = DatabaseQuery.execute(...)

```python
data = DatabaseQuery('Event').execute(filters={'starts_on': ['between', None]}, fields=['name'])
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue({'name': event1.name} not in data)
```

### Step 10: Assign data = DatabaseQuery.execute(...)

```python
data = DatabaseQuery('Event').execute(filters={'starts_on': ['between', ['2016-07-06', '2016-07-07']]}, fields=['name'])
```

### Step 11: Call self.assertIn()

```python
self.assertIn({'name': event2.name}, data)
```

### Step 12: Call self.assertIn()

```python
self.assertIn({'name': event3.name}, data)
```

### Step 13: Call self.assertNotIn()

```python
self.assertNotIn({'name': event1.name}, data)
```

### Step 14: Call self.assertNotIn()

```python
self.assertNotIn({'name': event4.name}, data)
```

### Step 15: Assign data = DatabaseQuery.execute(...)

```python
data = DatabaseQuery('Event').execute(filters={'starts_on': ['between', ['2016-07-07']]}, fields=['name'])
```

### Step 16: Call self.assertIn()

```python
self.assertIn({'name': event3.name}, data)
```

### Step 17: Call self.assertIn()

```python
self.assertIn({'name': event4.name}, data)
```

### Step 18: Call self.assertIn()

```python
self.assertIn({'name': todays_event.name}, data)
```

### Step 19: Call self.assertNotIn()

```python
self.assertNotIn({'name': event1.name}, data)
```

### Step 20: Call self.assertNotIn()

```python
self.assertNotIn({'name': event2.name}, data)
```

### Step 21: Assign data = DatabaseQuery.execute(...)

```python
data = DatabaseQuery('Event').execute(filters={'creation': ['between', ['2016-07-06', '2016-07-07']]}, fields=['name'])
```


## Complete Example

```python
# Setup
setup_for_tests()
frappe.set_user('Administrator')

# Workflow
'test case to check between filter for date fields'
frappe.db.delete('Event')
todays_event = create_event()
event1 = create_event(starts_on='2016-07-05 23:59:59')
event2 = create_event(starts_on='2016-07-06 00:00:00')
event3 = create_event(starts_on='2016-07-07 23:59:59')
event4 = create_event(starts_on='2016-07-08 00:00:00')
data = DatabaseQuery('Event').execute(filters={'starts_on': ['between', None]}, fields=['name'])
self.assertTrue({'name': event1.name} not in data)
data = DatabaseQuery('Event').execute(filters={'starts_on': ['between', ['2016-07-06', '2016-07-07']]}, fields=['name'])
self.assertIn({'name': event2.name}, data)
self.assertIn({'name': event3.name}, data)
self.assertNotIn({'name': event1.name}, data)
self.assertNotIn({'name': event4.name}, data)
data = DatabaseQuery('Event').execute(filters={'starts_on': ['between', ['2016-07-07']]}, fields=['name'])
self.assertIn({'name': event3.name}, data)
self.assertIn({'name': event4.name}, data)
self.assertIn({'name': todays_event.name}, data)
self.assertNotIn({'name': event1.name}, data)
self.assertNotIn({'name': event2.name}, data)
data = DatabaseQuery('Event').execute(filters={'creation': ['between', ['2016-07-06', '2016-07-07']]}, fields=['name'])
```

## Next Steps


---

*Source: test_db_query.py:296 | Complexity: Advanced | Last updated: 2026-02-04*