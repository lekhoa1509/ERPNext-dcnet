# How To: Cache Flag Management

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test that cache flags can be set and cleared correctly

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

### Step 1: 'Test that cache flags can be set and cleared correctly'

```python
'Test that cache flags can be set and cleared correctly'
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

### Step 9: Call tdr._set_deletion_cache()

```python
tdr._set_deletion_cache()
```

### Step 10: Assign cached_value = frappe.cache.get_value(...)

```python
cached_value = frappe.cache.get_value('deletion_running_doctype:Task')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(cached_value, tdr.name, 'Cache flag should be set for Task')
```

### Step 12: Call tdr._clear_deletion_cache()

```python
tdr._clear_deletion_cache()
```

### Step 13: Assign cached_value = frappe.cache.get_value(...)

```python
cached_value = frappe.cache.get_value('deletion_running_doctype:Task')
```

### Step 14: Call self.assertIsNone()

```python
self.assertIsNone(cached_value, 'Cache flag should be cleared for Task')
```


## Complete Example

```python
# Setup
self._clear_all_deletion_cache_flags()
create_company('Dunder Mifflin Paper Co')

# Workflow
'Test that cache flags can be set and cleared correctly'
company = 'Dunder Mifflin Paper Co'
create_task(company)
tdr = frappe.new_doc('Transaction Deletion Record')
tdr.company = company
tdr.insert()
tdr.generate_to_delete_list()
tdr.reload()
tdr._set_deletion_cache()
cached_value = frappe.cache.get_value('deletion_running_doctype:Task')
self.assertEqual(cached_value, tdr.name, 'Cache flag should be set for Task')
tdr._clear_deletion_cache()
cached_value = frappe.cache.get_value('deletion_running_doctype:Task')
self.assertIsNone(cached_value, 'Cache flag should be cleared for Task')
```

## Next Steps


---

*Source: test_transaction_deletion_record.py:279 | Complexity: Advanced | Last updated: 2026-02-04*