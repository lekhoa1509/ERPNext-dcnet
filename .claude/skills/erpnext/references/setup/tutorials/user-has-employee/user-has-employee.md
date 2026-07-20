# How To: User Has Employee

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test user has employee

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.utils`
- `frappe.query_builder`
- `frappe.tests`
- `erpnext`
- `erpnext.accounts.utils`
- `erpnext.setup.doctype.employee.employee`


## Step-by-Step Guide

### Step 1: Assign employee = make_employee(...)

```python
employee = make_employee('test_emp_user_creation@company.com')
```

### Step 2: Assign employee_doc = frappe.get_doc(...)

```python
employee_doc = frappe.get_doc('Employee', employee)
```

### Step 3: Assign user = value

```python
user = employee_doc.user_id
```

### Step 4: Call self.assertTrue()

```python
self.assertTrue('Employee' in frappe.get_roles(user))
```

### Step 5: Assign employee_doc.user_id = ''

```python
employee_doc.user_id = ''
```

### Step 6: Call employee_doc.save()

```python
employee_doc.save()
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue('Employee' not in frappe.get_roles(user))
```


## Complete Example

```python
# Workflow
employee = make_employee('test_emp_user_creation@company.com')
employee_doc = frappe.get_doc('Employee', employee)
user = employee_doc.user_id
self.assertTrue('Employee' in frappe.get_roles(user))
employee_doc.user_id = ''
employee_doc.save()
self.assertTrue('Employee' not in frappe.get_roles(user))
```

## Next Steps


---

*Source: test_employee.py:27 | Complexity: Intermediate | Last updated: 2026-02-04*