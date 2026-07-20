# How To: Submittable Assignment

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test submittable assignment

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.tests.utils`


## Step-by-Step Guide

### Step 1: Assign submittable_doctype = 'Assignment Test Submittable'

```python
submittable_doctype = 'Assignment Test Submittable'
```

### Step 2: Call create_test_doctype()

```python
create_test_doctype(submittable_doctype)
```

### Step 3: Assign dt = frappe.get_doc(...)

```python
dt = frappe.get_doc('DocType', submittable_doctype)
```

### Step 4: Assign dt.is_submittable = 1

```python
dt.is_submittable = 1
```

### Step 5: Call dt.save()

```python
dt.save()
```

### Step 6: Assign assignment_rule = frappe.new_doc(...)

```python
assignment_rule = frappe.new_doc('Assignment Rule')
```

### Step 7: Assign assignment_rule.name = value

```python
assignment_rule.name = f'For {submittable_doctype}'
```

### Step 8: Assign assignment_rule.document_type = submittable_doctype

```python
assignment_rule.document_type = submittable_doctype
```

### Step 9: Assign assignment_rule.rule = 'Round Robin'

```python
assignment_rule.rule = 'Round Robin'
```

### Step 10: Call assignment_rule.extend()

```python
assignment_rule.extend('assignment_days', self.days)
```

### Step 11: Call assignment_rule.append()

```python
assignment_rule.append('users', {'user': 'test@example.com'})
```

### Step 12: Assign assignment_rule.assign_condition = 'docstatus == 1'

```python
assignment_rule.assign_condition = 'docstatus == 1'
```

### Step 13: Assign assignment_rule.unassign_condition = 'docstatus == 2'

```python
assignment_rule.unassign_condition = 'docstatus == 2'
```

### Step 14: Call assignment_rule.save()

```python
assignment_rule.save()
```

### Step 15: Assign doc = frappe.new_doc(...)

```python
doc = frappe.new_doc(submittable_doctype)
```

### Step 16: Call doc.save()

```python
doc.save()
```

### Step 17: Call doc.submit()

```python
doc.submit()
```

### Step 18: Assign todos = frappe.get_all(...)

```python
todos = frappe.get_all('ToDo', filters={'reference_type': submittable_doctype, 'reference_name': doc.name, 'status': 'Open', 'allocated_to': 'test@example.com'})
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(len(todos), 1)
```

### Step 20: Call doc.cancel()

```python
doc.cancel()
```

### Step 21: Assign todos = frappe.get_all(...)

```python
todos = frappe.get_all('ToDo', filters={'reference_type': submittable_doctype, 'reference_name': doc.name, 'status': 'Cancelled', 'allocated_to': 'test@example.com'})
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(len(todos), 1)
```


## Complete Example

```python
# Workflow
submittable_doctype = 'Assignment Test Submittable'
create_test_doctype(submittable_doctype)
dt = frappe.get_doc('DocType', submittable_doctype)
dt.is_submittable = 1
dt.save()
assignment_rule = frappe.new_doc('Assignment Rule')
assignment_rule.name = f'For {submittable_doctype}'
assignment_rule.document_type = submittable_doctype
assignment_rule.rule = 'Round Robin'
assignment_rule.extend('assignment_days', self.days)
assignment_rule.append('users', {'user': 'test@example.com'})
assignment_rule.assign_condition = 'docstatus == 1'
assignment_rule.unassign_condition = 'docstatus == 2'
assignment_rule.save()
doc = frappe.new_doc(submittable_doctype)
doc.save()
doc.submit()
todos = frappe.get_all('ToDo', filters={'reference_type': submittable_doctype, 'reference_name': doc.name, 'status': 'Open', 'allocated_to': 'test@example.com'})
self.assertEqual(len(todos), 1)
doc.cancel()
todos = frappe.get_all('ToDo', filters={'reference_type': submittable_doctype, 'reference_name': doc.name, 'status': 'Cancelled', 'allocated_to': 'test@example.com'})
self.assertEqual(len(todos), 1)
```

## Next Steps


---

*Source: test_assignment_rule.py:291 | Complexity: Advanced | Last updated: 2026-02-04*