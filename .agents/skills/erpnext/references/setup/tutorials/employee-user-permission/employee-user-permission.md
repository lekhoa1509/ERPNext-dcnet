# How To: Employee User Permission

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test employee user permission

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
employee1 = make_employee('employee_1_test@company.com', create_user_permission=1)
```

### Step 2: Assign employee2 = make_employee(...)

```python
employee2 = make_employee('employee_2_test@company.com', create_user_permission=1)
```

### Step 3: Call make_employee()

```python
make_employee('employee_3_test@company.com', create_user_permission=1)
```

### Step 4: Assign employee1_doc = frappe.get_doc(...)

```python
employee1_doc = frappe.get_doc('Employee', employee1)
```

### Step 5: Assign employee2_doc = frappe.get_doc(...)

```python
employee2_doc = frappe.get_doc('Employee', employee2)
```

### Step 6: Call employee2_doc.reload()

```python
employee2_doc.reload()
```

### Step 7: Assign employee2_doc.reports_to = value

```python
employee2_doc.reports_to = employee1_doc.name
```

### Step 8: Call employee2_doc.save()

```python
employee2_doc.save()
```

### Step 9: Call frappe.set_user()

```python
frappe.set_user(employee1_doc.user_id)
```

### Step 10: Assign Employee = frappe.qb.DocType(...)

```python
Employee = frappe.qb.DocType('Employee')
```

### Step 11: Assign qb_employee_list = frappe.qb.from_.select.where.orderby.run(...)

```python
qb_employee_list = frappe.qb.from_(Employee).select(Employee.name).where(Criterion.all(build_qb_match_conditions('Employee'))).orderby(Employee.Name).run(pluck=Employee.name)
```

### Step 12: Assign employee_list = frappe.db.get_list(...)

```python
employee_list = frappe.db.get_list('Employee', pluck='name', order_by='name')
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(qb_employee_list, employee_list)
```

### Step 14: Call frappe.set_user()

```python
frappe.set_user('Administrator')
```


## Complete Example

```python
# Workflow
employee1 = make_employee('employee_1_test@company.com', create_user_permission=1)
employee2 = make_employee('employee_2_test@company.com', create_user_permission=1)
make_employee('employee_3_test@company.com', create_user_permission=1)
employee1_doc = frappe.get_doc('Employee', employee1)
employee2_doc = frappe.get_doc('Employee', employee2)
employee2_doc.reload()
employee2_doc.reports_to = employee1_doc.name
employee2_doc.save()
frappe.set_user(employee1_doc.user_id)
Employee = frappe.qb.DocType('Employee')
qb_employee_list = frappe.qb.from_(Employee).select(Employee.name).where(Criterion.all(build_qb_match_conditions('Employee'))).orderby(Employee.Name).run(pluck=Employee.name)
employee_list = frappe.db.get_list('Employee', pluck='name', order_by='name')
self.assertEqual(qb_employee_list, employee_list)
frappe.set_user('Administrator')
```

## Next Steps


---

*Source: test_employee.py:36 | Complexity: Advanced | Last updated: 2026-02-04*