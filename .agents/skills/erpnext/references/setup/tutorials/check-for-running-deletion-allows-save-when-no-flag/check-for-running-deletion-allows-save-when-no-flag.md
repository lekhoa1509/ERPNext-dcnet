# How To: Check For Running Deletion Allows Save When No Flag

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test that documents can be saved when no deletion is running

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

### Step 1: 'Test that documents can be saved when no deletion is running'

```python
'Test that documents can be saved when no deletion is running'
```

### Step 2: Assign company = 'Dunder Mifflin Paper Co'

```python
company = 'Dunder Mifflin Paper Co'
```

### Step 3: Call frappe.cache.delete_value()

```python
frappe.cache.delete_value('deletion_running_doctype:Task')
```

### Step 4: Assign new_task = frappe.new_doc(...)

```python
new_task = frappe.new_doc('Task')
```

### Step 5: Assign new_task.company = company

```python
new_task.company = company
```

### Step 6: Assign new_task.subject = 'Should be allowed'

```python
new_task.subject = 'Should be allowed'
```

### Step 7: Call new_task.insert()

```python
new_task.insert()
```

### Step 8: Call frappe.delete_doc()

```python
frappe.delete_doc('Task', new_task.name)
```

### Step 9: Call self.fail()

```python
self.fail(f'Should allow save when no deletion is running, but got: {e}')
```


## Complete Example

```python
# Setup
self._clear_all_deletion_cache_flags()
create_company('Dunder Mifflin Paper Co')

# Workflow
'Test that documents can be saved when no deletion is running'
company = 'Dunder Mifflin Paper Co'
frappe.cache.delete_value('deletion_running_doctype:Task')
new_task = frappe.new_doc('Task')
new_task.company = company
new_task.subject = 'Should be allowed'
try:
    new_task.insert()
    frappe.delete_doc('Task', new_task.name)
except frappe.ValidationError as e:
    self.fail(f'Should allow save when no deletion is running, but got: {e}')
```

## Next Steps


---

*Source: test_transaction_deletion_record.py:332 | Complexity: Advanced | Last updated: 2026-02-04*