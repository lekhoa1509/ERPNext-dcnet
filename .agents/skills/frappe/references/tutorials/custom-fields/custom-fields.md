# How To: Custom Fields

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test custom fields

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils.testutils`


## Step-by-Step Guide

### Step 1: Call add_custom_field()

```python
add_custom_field('Event', 'test_ref_doc', 'Link', 'DocType')
```

### Step 2: Call add_custom_field()

```python
add_custom_field('Event', 'test_ref_name', 'Dynamic Link', 'test_ref_doc')
```

### Step 3: Assign unsub = frappe.get_doc.insert(...)

```python
unsub = frappe.get_doc({'doctype': 'Email Unsubscribe', 'email': 'test@example.com', 'global_unsubscribe': 1}).insert()
```

### Step 4: Assign event = frappe.get_doc.insert(...)

```python
event = frappe.get_doc({'doctype': 'Event', 'subject': 'test-for-delete-2', 'starts_on': '2014-01-01', 'event_type': 'Public', 'test_ref_doc': unsub.doctype, 'test_ref_name': unsub.name}).insert()
```

### Step 5: Call self.assertRaises()

```python
self.assertRaises(frappe.LinkExistsError, unsub.delete)
```

### Step 6: Assign event.test_ref_doc = None

```python
event.test_ref_doc = None
```

### Step 7: Assign event.test_ref_name = None

```python
event.test_ref_name = None
```

### Step 8: Call event.save()

```python
event.save()
```

### Step 9: Call unsub.delete()

```python
unsub.delete()
```

### Step 10: Call clear_custom_fields()

```python
clear_custom_fields('Event')
```

### Step 11: Call frappe.db.commit()

```python
frappe.db.commit()
```


## Complete Example

```python
# Workflow
from frappe.utils.testutils import add_custom_field, clear_custom_fields
add_custom_field('Event', 'test_ref_doc', 'Link', 'DocType')
add_custom_field('Event', 'test_ref_name', 'Dynamic Link', 'test_ref_doc')
unsub = frappe.get_doc({'doctype': 'Email Unsubscribe', 'email': 'test@example.com', 'global_unsubscribe': 1}).insert()
event = frappe.get_doc({'doctype': 'Event', 'subject': 'test-for-delete-2', 'starts_on': '2014-01-01', 'event_type': 'Public', 'test_ref_doc': unsub.doctype, 'test_ref_name': unsub.name}).insert()
self.assertRaises(frappe.LinkExistsError, unsub.delete)
event.test_ref_doc = None
event.test_ref_name = None
event.save()
unsub.delete()
clear_custom_fields('Event')
frappe.db.commit()
```

## Next Steps


---

*Source: test_dynamic_links.py:53 | Complexity: Advanced | Last updated: 2026-02-04*