# How To: If User Is Added

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test if user is added

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe.tests`
- `frappe.desk.form.load`


## Step-by-Step Guide

### Step 1: Assign ev = frappe.get_doc.insert(...)

```python
ev = frappe.get_doc({'doctype': 'Event', 'subject': 'test event for seen', 'starts_on': '2016-01-01 10:10:00', 'event_type': 'Public'}).insert()
```

### Step 2: Call frappe.set_user()

```python
frappe.set_user('test@example.com')
```

### Step 3: Call getdoc()

```python
getdoc('Event', ev.name)
```

### Step 4: Assign ev = frappe.get_doc(...)

```python
ev = frappe.get_doc('Event', ev.name)
```

### Step 5: Call self.assertTrue()

```python
self.assertTrue('test@example.com' in json.loads(ev._seen))
```

### Step 6: Call frappe.set_user()

```python
frappe.set_user('test1@example.com')
```

### Step 7: Call getdoc()

```python
getdoc('Event', ev.name)
```

### Step 8: Assign ev = frappe.get_doc(...)

```python
ev = frappe.get_doc('Event', ev.name)
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue('test@example.com' in json.loads(ev._seen))
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue('test1@example.com' in json.loads(ev._seen))
```

### Step 11: Call ev.save()

```python
ev.save()
```

### Step 12: Assign ev = frappe.get_doc(...)

```python
ev = frappe.get_doc('Event', ev.name)
```

### Step 13: Call self.assertFalse()

```python
self.assertFalse('test@example.com' in json.loads(ev._seen))
```

### Step 14: Call self.assertTrue()

```python
self.assertTrue('test1@example.com' in json.loads(ev._seen))
```


## Complete Example

```python
# Workflow
ev = frappe.get_doc({'doctype': 'Event', 'subject': 'test event for seen', 'starts_on': '2016-01-01 10:10:00', 'event_type': 'Public'}).insert()
frappe.set_user('test@example.com')
from frappe.desk.form.load import getdoc
getdoc('Event', ev.name)
ev = frappe.get_doc('Event', ev.name)
self.assertTrue('test@example.com' in json.loads(ev._seen))
frappe.set_user('test1@example.com')
getdoc('Event', ev.name)
ev = frappe.get_doc('Event', ev.name)
self.assertTrue('test@example.com' in json.loads(ev._seen))
self.assertTrue('test1@example.com' in json.loads(ev._seen))
ev.save()
ev = frappe.get_doc('Event', ev.name)
self.assertFalse('test@example.com' in json.loads(ev._seen))
self.assertTrue('test1@example.com' in json.loads(ev._seen))
```

## Next Steps


---

*Source: test_seen.py:13 | Complexity: Advanced | Last updated: 2026-02-04*