# How To: Accounting Period Exempted Role

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test accounting period exempted role

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.accounting_period.accounting_period`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`


## Step-by-Step Guide

### Step 1: Assign ap = create_accounting_period(...)

```python
ap = create_accounting_period(period_name='Test Accounting Period Exempted', exempted_role='Accounts Manager', start_date='2025-12-01', end_date='2025-12-31')
```

### Step 2: Call ap.save()

```python
ap.save()
```

### Step 3: Assign users = frappe.get_all(...)

```python
users = frappe.get_all('User', filters={'email': ['like', 'test%']}, limit=1)
```

### Step 4: Assign user = None

```python
user = None
```

### Step 5: Assign user.roles = value

```python
user.roles = []
```

### Step 6: Call user.append()

```python
user.append('roles', {'role': 'Accounts User'})
```

### Step 7: Call user.save()

```python
user.save(ignore_permissions=True)
```

### Step 8: Call frappe.clear_cache()

```python
frappe.clear_cache(user=user.name)
```

### Step 9: Call frappe.set_user()

```python
frappe.set_user(user.name)
```

### Step 10: Assign posting_date = '2025-12-11'

```python
posting_date = '2025-12-11'
```

### Step 11: Assign doc = create_sales_invoice(...)

```python
doc = create_sales_invoice(do_not_save=1, posting_date=posting_date)
```

### Step 12: Call user.append()

```python
user.append('roles', {'role': 'Accounts Manager'})
```

### Step 13: Call user.save()

```python
user.save(ignore_permissions=True)
```

### Step 14: Call frappe.clear_cache()

```python
frappe.clear_cache(user=user.name)
```

### Step 15: Assign doc = create_sales_invoice(...)

```python
doc = create_sales_invoice(do_not_save=1, posting_date=posting_date)
```

### Step 16: Call doc.submit()

```python
doc.submit()
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(doc.docstatus, 1)
```

### Step 18: Assign user = frappe.get_doc(...)

```python
user = frappe.get_doc('User', users[0].name)
```

### Step 19: Assign user = frappe.get_doc(...)

```python
user = frappe.get_doc({'doctype': 'User', 'email': 'test1@example.com', 'first_name': 'Test1'})
```

### Step 20: Call user.insert()

```python
user.insert()
```

### Step 21: Call doc.submit()

```python
doc.submit()
```


## Complete Example

```python
# Workflow
ap = create_accounting_period(period_name='Test Accounting Period Exempted', exempted_role='Accounts Manager', start_date='2025-12-01', end_date='2025-12-31')
ap.save()
users = frappe.get_all('User', filters={'email': ['like', 'test%']}, limit=1)
user = None
if users[0].name:
    user = frappe.get_doc('User', users[0].name)
else:
    user = frappe.get_doc({'doctype': 'User', 'email': 'test1@example.com', 'first_name': 'Test1'})
    user.insert()
user.roles = []
user.append('roles', {'role': 'Accounts User'})
user.save(ignore_permissions=True)
frappe.clear_cache(user=user.name)
frappe.set_user(user.name)
posting_date = '2025-12-11'
doc = create_sales_invoice(do_not_save=1, posting_date=posting_date)
with self.assertRaises(frappe.ValidationError):
    doc.submit()
user.append('roles', {'role': 'Accounts Manager'})
user.save(ignore_permissions=True)
frappe.clear_cache(user=user.name)
doc = create_sales_invoice(do_not_save=1, posting_date=posting_date)
doc.submit()
self.assertEqual(doc.docstatus, 1)
```

## Next Steps


---

*Source: test_accounting_period.py:39 | Complexity: Advanced | Last updated: 2026-02-03*