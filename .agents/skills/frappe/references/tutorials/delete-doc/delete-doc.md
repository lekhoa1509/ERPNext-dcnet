# How To: Delete Doc

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test delete doc

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.custom.doctype.property_setter.property_setter`
- `frappe.desk.page.setup_wizard.install_fixtures`
- `frappe.tests`
- `frappe.tests.utils`
- `frappe.utils`


## Step-by-Step Guide

### Step 1: Call self.insert_test_events()

```python
self.insert_test_events()
```

### Step 2: Assign event_name = value

```python
event_name = frappe.get_all('Event')[0].name
```

### Step 3: Assign event = frappe.get_doc(...)

```python
event = frappe.get_doc('Event', event_name)
```

### Step 4: Assign test_subject = value

```python
test_subject = event.subject
```

### Step 5: Assign results = global_search.search(...)

```python
results = global_search.search(test_subject)
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue(any((r['name'] == event_name for r in results)), msg='Failed to search document by exact name')
```

### Step 7: Call frappe.delete_doc()

```python
frappe.delete_doc('Event', event_name)
```

### Step 8: Call global_search.sync_global_search()

```python
global_search.sync_global_search()
```

### Step 9: Call frappe.db.commit()

```python
frappe.db.commit()
```

### Step 10: Assign results = global_search.search(...)

```python
results = global_search.search(test_subject)
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(all((r['name'] != event_name for r in results)), msg='Deleted documents appearing in global search.')
```


## Complete Example

```python
# Workflow
self.insert_test_events()
event_name = frappe.get_all('Event')[0].name
event = frappe.get_doc('Event', event_name)
test_subject = event.subject
results = global_search.search(test_subject)
self.assertTrue(any((r['name'] == event_name for r in results)), msg='Failed to search document by exact name')
frappe.delete_doc('Event', event_name)
global_search.sync_global_search()
frappe.db.commit()
results = global_search.search(test_subject)
self.assertTrue(all((r['name'] != event_name for r in results)), msg='Deleted documents appearing in global search.')
```

## Next Steps


---

*Source: test_global_search.py:89 | Complexity: Advanced | Last updated: 2026-02-04*