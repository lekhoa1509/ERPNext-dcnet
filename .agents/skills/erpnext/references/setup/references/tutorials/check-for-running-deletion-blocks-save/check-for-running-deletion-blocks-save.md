# How To: Check For Running Deletion Blocks Save

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test that check_for_running_deletion_job blocks saves when cache flag exists

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `frappe`
- `frappe.tests`
- `erpnext.setup.doctype.company.company`
- `erpnext.setup.doctype.transaction_deletion_record.transaction_deletion_record`
- `erpnext.setup.doctype.transaction_deletion_record.transaction_deletion_record`
- `erpnext.setup.doctype.transaction_deletion_record.transaction_deletion_record`
- `erpnext.setup.doctype.transaction_deletion_record.transaction_deletion_record`

**Setup Required:**
```python
self._clear_all_deletion_cache_flags()
create_company('Dunder Mifflin Paper Co')
```

## Step-by-Step Guide

### Step 1: 'Test that check_for_running_deletion_job blocks saves when cache flag exists'

```python
'Test that check_for_running_deletion_job blocks saves when cache flag exists'
```

### Step 2: Assign company = 'Dunder Mifflin Paper Co'

```python
company = 'Dunder Mifflin Paper Co'
```

### Step 3: Call frappe.cache.set_value()

```python
frappe.cache.set_value('deletion_running_doctype:Task', 'TDR-00001', expires_in_sec=60)
```

### Step 4: Assign new_task = frappe.new_doc(...)

```python
new_task = frappe.new_doc('Task')
```

### Step 5: Assign new_task.company = company

```python
new_task.company = company
```

### Step 6: Assign new_task.subject = 'Should be blocked'

```python
new_task.subject = 'Should be blocked'
```

### Step 7: Assign error_message = str(...)

```python
error_message = str(context.exception)
```

### Step 8: Call self.assertIn()

```python
self.assertIn('currently deleting', error_message)
```

### Step 9: Call self.assertIn()

```python
self.assertIn('TDR-00001', error_message)
```

### Step 10: Call frappe.cache.delete_value()

```python
frappe.cache.delete_value('deletion_running_doctype:Task')
```

### Step 11: Call check_for_running_deletion_job()

```python
check_for_running_deletion_job(new_task)
```


## Complete Example

```python
# Setup
self._clear_all_deletion_cache_flags()
create_company('Dunder Mifflin Paper Co')

# Workflow
'Test that check_for_running_deletion_job blocks saves when cache flag exists'
from erpnext.setup.doctype.transaction_deletion_record.transaction_deletion_record import check_for_running_deletion_job
company = 'Dunder Mifflin Paper Co'
frappe.cache.set_value('deletion_running_doctype:Task', 'TDR-00001', expires_in_sec=60)
try:
    new_task = frappe.new_doc('Task')
    new_task.company = company
    new_task.subject = 'Should be blocked'
    with self.assertRaises(frappe.ValidationError) as context:
        check_for_running_deletion_job(new_task)
    error_message = str(context.exception)
    self.assertIn('currently deleting', error_message)
    self.assertIn('TDR-00001', error_message)
finally:
    frappe.cache.delete_value('deletion_running_doctype:Task')
```

## Next Steps


---

*Source: test_transaction_deletion_record.py:304 | Complexity: Advanced | Last updated: 2026-02-04*