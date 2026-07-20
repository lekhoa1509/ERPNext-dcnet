# How To: Update Doc

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test update doc

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

### Step 2: Assign test_subject = 'testing global search'

```python
test_subject = 'testing global search'
```

### Step 3: Assign event = frappe.get_doc(...)

```python
event = frappe.get_doc('Event', frappe.get_all('Event')[0].name)
```

### Step 4: Assign event.subject = test_subject

```python
event.subject = test_subject
```

### Step 5: Call event.save()

```python
event.save()
```

### Step 6: Call frappe.db.commit()

```python
frappe.db.commit()
```

### Step 7: Call global_search.sync_global_search()

```python
global_search.sync_global_search()
```

### Step 8: Assign results = global_search.search(...)

```python
results = global_search.search('testing global search')
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue('testing global search' in results[0].content)
```


## Complete Example

```python
# Workflow
self.insert_test_events()
test_subject = 'testing global search'
event = frappe.get_doc('Event', frappe.get_all('Event')[0].name)
event.subject = test_subject
event.save()
frappe.db.commit()
global_search.sync_global_search()
results = global_search.search('testing global search')
self.assertTrue('testing global search' in results[0].content)
```

## Next Steps


---

*Source: test_global_search.py:67 | Complexity: Advanced | Last updated: 2026-02-04*