# How To: Employee Status Left

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test employee status left

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

### Step 1: Assign employee1 = make_employee(...)

```python
employee1 = make_employee('test_employee_1@company.com')
```

### Step 2: Assign employee2 = make_employee(...)

```python
employee2 = make_employee('test_employee_2@company.com')
```

### Step 3: Assign employee1_doc = frappe.get_doc(...)

```python
employee1_doc = frappe.get_doc('Employee', employee1)
```

### Step 4: Assign employee2_doc = frappe.get_doc(...)

```python
employee2_doc = frappe.get_doc('Employee', employee2)
```

### Step 5: Call employee2_doc.reload()

```python
employee2_doc.reload()
```

### Step 6: Assign employee2_doc.reports_to = value

```python
employee2_doc.reports_to = employee1_doc.name
```

### Step 7: Call employee2_doc.save()

```python
employee2_doc.save()
```

### Step 8: Call employee1_doc.reload()

```python
employee1_doc.reload()
```

### Step 9: Assign employee1_doc.status = 'Left'

```python
employee1_doc.status = 'Left'
```

### Step 10: Call self.assertRaises()

```python
self.assertRaises(InactiveEmployeeStatusError, employee1_doc.save)
```


## Complete Example

```python
# Workflow
employee1 = make_employee('test_employee_1@company.com')
employee2 = make_employee('test_employee_2@company.com')
employee1_doc = frappe.get_doc('Employee', employee1)
employee2_doc = frappe.get_doc('Employee', employee2)
employee2_doc.reload()
employee2_doc.reports_to = employee1_doc.name
employee2_doc.save()
employee1_doc.reload()
employee1_doc.status = 'Left'
self.assertRaises(InactiveEmployeeStatusError, employee1_doc.save)
```

## Next Steps


---

*Source: test_employee.py:15 | Complexity: Advanced | Last updated: 2026-02-04*