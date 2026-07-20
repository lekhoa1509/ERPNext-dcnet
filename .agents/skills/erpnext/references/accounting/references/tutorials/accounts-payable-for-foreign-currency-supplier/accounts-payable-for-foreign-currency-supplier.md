# How To: Accounts Payable For Foreign Currency Supplier

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test accounts payable for foreign currency supplier

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.accounts.report.accounts_payable.accounts_payable`
- `erpnext.accounts.test.accounts_mixin`


## Step-by-Step Guide

### Step 1: Assign pi = self.create_purchase_invoice(...)

```python
pi = self.create_purchase_invoice(do_not_submit=True)
```

### Step 2: Assign pi.currency = 'USD'

```python
pi.currency = 'USD'
```

### Step 3: Assign pi.conversion_rate = 80

```python
pi.conversion_rate = 80
```

### Step 4: Assign pi.credit_to = value

```python
pi.credit_to = self.creditors_usd
```

### Step 5: Assign pi = pi.save.submit(...)

```python
pi = pi.save().submit()
```

### Step 6: Assign filters = value

```python
filters = {'company': self.company, 'party_type': 'Supplier', 'party': [self.supplier], 'report_date': today(), 'range': '30, 60, 90, 120', 'in_party_currency': 1}
```

### Step 7: Assign data = execute(...)

```python
data = execute(filters)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(data[1][0].get('outstanding'), 300)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(data[1][0].get('currency'), 'USD')
```


## Complete Example

```python
# Workflow
pi = self.create_purchase_invoice(do_not_submit=True)
pi.currency = 'USD'
pi.conversion_rate = 80
pi.credit_to = self.creditors_usd
pi = pi.save().submit()
filters = {'company': self.company, 'party_type': 'Supplier', 'party': [self.supplier], 'report_date': today(), 'range': '30, 60, 90, 120', 'in_party_currency': 1}
data = execute(filters)
self.assertEqual(data[1][0].get('outstanding'), 300)
self.assertEqual(data[1][0].get('currency'), 'USD')
```

## Next Steps


---

*Source: test_accounts_payable.py:21 | Complexity: Advanced | Last updated: 2026-02-03*