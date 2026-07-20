# How To: Csv Export Import

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test CSV export and import functionality with company_field column

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

### Step 1: 'Test CSV export and import functionality with company_field column'

```python
'Test CSV export and import functionality with company_field column'
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

### Step 9: Assign original_count = len(...)

```python
original_count = len(tdr.doctypes_to_delete)
```

### Step 10: Call self.assertGreater()

```python
self.assertGreater(original_count, 0)
```

### Step 11: Call tdr.export_to_delete_template_method()

```python
tdr.export_to_delete_template_method()
```

### Step 12: Assign csv_content = frappe.response.get(...)

```python
csv_content = frappe.response.get('result')
```

### Step 13: Call self.assertIsNotNone()

```python
self.assertIsNotNone(csv_content)
```

### Step 14: Call self.assertIn()

```python
self.assertIn('doctype_name', csv_content)
```

### Step 15: Call self.assertIn()

```python
self.assertIn('company_field', csv_content)
```

### Step 16: Assign tdr2 = frappe.new_doc(...)

```python
tdr2 = frappe.new_doc('Transaction Deletion Record')
```

### Step 17: Assign tdr2.company = company

```python
tdr2.company = company
```

### Step 18: Call tdr2.insert()

```python
tdr2.insert()
```

### Step 19: Assign result = tdr2.import_to_delete_template_method(...)

```python
result = tdr2.import_to_delete_template_method(csv_content)
```

### Step 20: Call tdr2.reload()

```python
tdr2.reload()
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(len(tdr2.doctypes_to_delete), original_count)
```

### Step 22: Call self.assertGreaterEqual()

```python
self.assertGreaterEqual(result['imported'], 1)
```

### Step 23: Call self.assertIsNotNone()

```python
self.assertIsNotNone(row.company_field, 'Task should have company_field set after import')
```


## Complete Example

```python
# Setup
self._clear_all_deletion_cache_flags()
create_company('Dunder Mifflin Paper Co')

# Workflow
'Test CSV export and import functionality with company_field column'
company = 'Dunder Mifflin Paper Co'
create_task(company)
tdr = frappe.new_doc('Transaction Deletion Record')
tdr.company = company
tdr.insert()
tdr.generate_to_delete_list()
tdr.reload()
original_count = len(tdr.doctypes_to_delete)
self.assertGreater(original_count, 0)
tdr.export_to_delete_template_method()
csv_content = frappe.response.get('result')
self.assertIsNotNone(csv_content)
self.assertIn('doctype_name', csv_content)
self.assertIn('company_field', csv_content)
tdr2 = frappe.new_doc('Transaction Deletion Record')
tdr2.company = company
tdr2.insert()
result = tdr2.import_to_delete_template_method(csv_content)
tdr2.reload()
self.assertEqual(len(tdr2.doctypes_to_delete), original_count)
self.assertGreaterEqual(result['imported'], 1)
for row in tdr2.doctypes_to_delete:
    if row.doctype_name == 'Task':
        self.assertIsNotNone(row.company_field, 'Task should have company_field set after import')
```

## Next Steps


---

*Source: test_transaction_deletion_record.py:133 | Complexity: Advanced | Last updated: 2026-02-04*