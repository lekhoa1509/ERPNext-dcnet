# How To: Progress Tracking

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test that deleted checkbox is marked when DocType deletion completes

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

### Step 1: 'Test that deleted checkbox is marked when DocType deletion completes'

```python
'Test that deleted checkbox is marked when DocType deletion completes'
```

### Step 2: Assign company = 'Dunder Mifflin Paper Co'

```python
company = 'Dunder Mifflin Paper Co'
```

### Step 3: Call create_task()

```python
create_task(company)
```

### Step 4: Assign tdr = create_and_submit_transaction_deletion_doc(...)

```python
tdr = create_and_submit_transaction_deletion_doc(company)
```

### Step 5: Call tdr.reload()

```python
tdr.reload()
```

### Step 6: Assign task_row = None

```python
task_row = None
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(task_row.deleted, 1, 'Task should be marked as deleted')
```

### Step 8: Assign task_row = doctype

```python
task_row = doctype
```


## Complete Example

```python
# Setup
self._clear_all_deletion_cache_flags()
create_company('Dunder Mifflin Paper Co')

# Workflow
'Test that deleted checkbox is marked when DocType deletion completes'
company = 'Dunder Mifflin Paper Co'
create_task(company)
tdr = create_and_submit_transaction_deletion_doc(company)
tdr.reload()
task_row = None
for doctype in tdr.doctypes_to_delete:
    if doctype.doctype_name == 'Task':
        task_row = doctype
        break
if task_row:
    self.assertEqual(task_row.deleted, 1, 'Task should be marked as deleted')
```

## Next Steps


---

*Source: test_transaction_deletion_record.py:172 | Complexity: Advanced | Last updated: 2026-02-04*