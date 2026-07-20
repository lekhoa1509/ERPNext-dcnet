# How To: Doctypes Contain Company Field

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test that all DocTypes in To Delete list have a valid company link field

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

### Step 1: 'Test that all DocTypes in To Delete list have a valid company link field'

```python
'Test that all DocTypes in To Delete list have a valid company link field'
```

### Step 2: Assign tdr = create_and_submit_transaction_deletion_doc(...)

```python
tdr = create_and_submit_transaction_deletion_doc('Dunder Mifflin Paper Co')
```

### Step 3: Assign field_found = False

```python
field_found = False
```

### Step 4: Assign doctype_fields = value

```python
doctype_fields = frappe.get_meta(doctype_row.doctype_name).as_dict()['fields']
```

### Step 5: Call self.assertTrue()

```python
self.assertTrue(field_found, f"DocType {doctype_row.doctype_name} should have company field '{doctype_row.company_field}'")
```

### Step 6: Assign field_found = True

```python
field_found = True
```


## Complete Example

```python
# Workflow
'Test that all DocTypes in To Delete list have a valid company link field'
tdr = create_and_submit_transaction_deletion_doc('Dunder Mifflin Paper Co')
for doctype_row in tdr.doctypes_to_delete:
    if doctype_row.company_field:
        field_found = False
        doctype_fields = frappe.get_meta(doctype_row.doctype_name).as_dict()['fields']
        for doctype_field in doctype_fields:
            if doctype_field['fieldname'] == doctype_row.company_field and doctype_field['fieldtype'] == 'Link' and (doctype_field['options'] == 'Company'):
                field_found = True
                break
        self.assertTrue(field_found, f"DocType {doctype_row.doctype_name} should have company field '{doctype_row.company_field}'")
```

## Next Steps


---

*Source: test_transaction_deletion_record.py:36 | Complexity: Intermediate | Last updated: 2026-02-04*