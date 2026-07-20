# How To: Only One Deletion Allowed Globally

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test that only one deletion can be submitted at a time (global enforcement)

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

### Step 1: 'Test that only one deletion can be submitted at a time (global enforcement)'

```python
'Test that only one deletion can be submitted at a time (global enforcement)'
```

### Step 2: Assign company1 = 'Dunder Mifflin Paper Co'

```python
company1 = 'Dunder Mifflin Paper Co'
```

### Step 3: Assign company2 = 'Sabre Corporation'

```python
company2 = 'Sabre Corporation'
```

### Step 4: Call create_company()

```python
create_company(company2)
```

### Step 5: Assign tdr1 = frappe.new_doc(...)

```python
tdr1 = frappe.new_doc('Transaction Deletion Record')
```

### Step 6: Assign tdr1.company = company1

```python
tdr1.company = company1
```

### Step 7: Call tdr1.insert()

```python
tdr1.insert()
```

### Step 8: Call tdr1.append()

```python
tdr1.append('doctypes_to_delete', {'doctype_name': 'Task', 'company_field': 'company'})
```

### Step 9: Call tdr1.save()

```python
tdr1.save()
```

### Step 10: Call tdr1.submit()

```python
tdr1.submit()
```

### Step 11: Assign tdr2 = frappe.new_doc(...)

```python
tdr2 = frappe.new_doc('Transaction Deletion Record')
```

### Step 12: Assign tdr2.company = company2

```python
tdr2.company = company2
```

### Step 13: Call tdr2.insert()

```python
tdr2.insert()
```

### Step 14: Call tdr2.append()

```python
tdr2.append('doctypes_to_delete', {'doctype_name': 'Lead', 'company_field': 'company'})
```

### Step 15: Call tdr2.save()

```python
tdr2.save()
```

### Step 16: Call self.assertIn()

```python
self.assertIn('already', str(context.exception).lower())
```

### Step 17: Call self.assertIn()

```python
self.assertIn(tdr1.name, str(context.exception))
```

### Step 18: Call tdr1.cancel()

```python
tdr1.cancel()
```

### Step 19: Call tdr2.submit()

```python
tdr2.submit()
```


## Complete Example

```python
# Setup
self._clear_all_deletion_cache_flags()
create_company('Dunder Mifflin Paper Co')

# Workflow
'Test that only one deletion can be submitted at a time (global enforcement)'
company1 = 'Dunder Mifflin Paper Co'
company2 = 'Sabre Corporation'
create_company(company2)
tdr1 = frappe.new_doc('Transaction Deletion Record')
tdr1.company = company1
tdr1.insert()
tdr1.append('doctypes_to_delete', {'doctype_name': 'Task', 'company_field': 'company'})
tdr1.save()
tdr1.submit()
try:
    tdr2 = frappe.new_doc('Transaction Deletion Record')
    tdr2.company = company2
    tdr2.insert()
    tdr2.append('doctypes_to_delete', {'doctype_name': 'Lead', 'company_field': 'company'})
    tdr2.save()
    with self.assertRaises(frappe.ValidationError) as context:
        tdr2.submit()
    self.assertIn('already', str(context.exception).lower())
    self.assertIn(tdr1.name, str(context.exception))
finally:
    tdr1.cancel()
```

## Next Steps


---

*Source: test_transaction_deletion_record.py:352 | Complexity: Advanced | Last updated: 2026-02-04*