# How To: Generate To Delete List

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test automatic generation of To Delete list

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `erpnext.setup.doctype.company.company`
- `erpnext.setup.doctype.transaction_deletion_record.transaction_deletion_record`
- `erpnext.setup.doctype.transaction_deletion_record.transaction_deletion_record`
- `erpnext.setup.doctype.transaction_deletion_record.transaction_deletion_record`
- `erpnext.setup.doctype.transaction_deletion_record.transaction_deletion_record`


## Step-by-Step Guide

### Step 1: 'Test automatic generation of To Delete list'

```python
'Test automatic generation of To Delete list'
```

### Step 2: Assign company = 'Dunder Mifflin Paper Co'

```python
company = 'Dunder Mifflin Paper Co'
```

### Step 3: Call create_task()

```python
create_task(company)
```

### Step 4: Assign tdr = frappe.new_doc(...)

```python
tdr = frappe.new_doc('Transaction Deletion Record')
```

### Step 5: Assign tdr.company = company

```python
tdr.company = company
```

### Step 6: Call tdr.insert()

```python
tdr.insert()
```

### Step 7: Call tdr.generate_to_delete_list()

```python
tdr.generate_to_delete_list()
```

### Step 8: Call tdr.reload()

```python
tdr.reload()
```

### Step 9: Call self.assertGreater()

```python
self.assertGreater(len(tdr.doctypes_to_delete), 0)
```

### Step 10: Assign task_in_list = any(...)

```python
task_in_list = any((d.doctype_name == 'Task' for d in tdr.doctypes_to_delete))
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(task_in_list, 'Task should be in To Delete list')
```


## Complete Example

```python
# Workflow
'Test automatic generation of To Delete list'
company = 'Dunder Mifflin Paper Co'
create_task(company)
tdr = frappe.new_doc('Transaction Deletion Record')
tdr.company = company
tdr.insert()
tdr.generate_to_delete_list()
tdr.reload()
self.assertGreater(len(tdr.doctypes_to_delete), 0)
task_in_list = any((d.doctype_name == 'Task' for d in tdr.doctypes_to_delete))
self.assertTrue(task_in_list, 'Task should be in To Delete list')
```

## Next Steps


---

*Source: test_transaction_deletion_record.py:91 | Complexity: Advanced | Last updated: 2026-02-04*