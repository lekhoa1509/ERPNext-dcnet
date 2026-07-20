# How To: Delete Logs

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test delete logs

## Prerequisites

**Required Modules:**
- `datetime`
- `frappe`
- `frappe.core.doctype.log_settings.log_settings`
- `frappe.tests`
- `frappe.utils`


## Step-by-Step Guide

### Step 1: Assign activity_log_count = frappe.db.count(...)

```python
activity_log_count = frappe.db.count('Activity Log', {'creation': ('<=', self.datetime.past)})
```

### Step 2: Assign error_log_count = frappe.db.count(...)

```python
error_log_count = frappe.db.count('Error Log', {'creation': ('<=', self.datetime.past)})
```

### Step 3: Assign email_queue_count = frappe.db.count(...)

```python
email_queue_count = frappe.db.count('Email Queue', {'creation': ('<=', self.datetime.past)})
```

### Step 4: Call self.assertNotEqual()

```python
self.assertNotEqual(activity_log_count, 0)
```

### Step 5: Call self.assertNotEqual()

```python
self.assertNotEqual(error_log_count, 0)
```

### Step 6: Call self.assertNotEqual()

```python
self.assertNotEqual(email_queue_count, 0)
```

### Step 7: Call run_log_clean_up()

```python
run_log_clean_up()
```

### Step 8: Assign activity_log_count = frappe.db.count(...)

```python
activity_log_count = frappe.db.count('Activity Log', {'creation': ('<', self.datetime.past)})
```

### Step 9: Assign error_log_count = frappe.db.count(...)

```python
error_log_count = frappe.db.count('Error Log', {'creation': ('<', self.datetime.past)})
```

### Step 10: Assign email_queue_count = frappe.db.count(...)

```python
email_queue_count = frappe.db.count('Email Queue', {'creation': ('<', self.datetime.past)})
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(activity_log_count, 0)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(error_log_count, 0)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(email_queue_count, 0)
```


## Complete Example

```python
# Workflow
activity_log_count = frappe.db.count('Activity Log', {'creation': ('<=', self.datetime.past)})
error_log_count = frappe.db.count('Error Log', {'creation': ('<=', self.datetime.past)})
email_queue_count = frappe.db.count('Email Queue', {'creation': ('<=', self.datetime.past)})
self.assertNotEqual(activity_log_count, 0)
self.assertNotEqual(error_log_count, 0)
self.assertNotEqual(email_queue_count, 0)
run_log_clean_up()
activity_log_count = frappe.db.count('Activity Log', {'creation': ('<', self.datetime.past)})
error_log_count = frappe.db.count('Error Log', {'creation': ('<', self.datetime.past)})
email_queue_count = frappe.db.count('Email Queue', {'creation': ('<', self.datetime.past)})
self.assertEqual(activity_log_count, 0)
self.assertEqual(error_log_count, 0)
self.assertEqual(email_queue_count, 0)
```

## Next Steps


---

*Source: test_log_settings.py:37 | Complexity: Advanced | Last updated: 2026-02-04*