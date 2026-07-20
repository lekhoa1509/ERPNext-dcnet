# How To: Subscription With Follow Calendar Months

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test subscription with follow calendar months

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils.data`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.accounts.doctype.subscription.subscription`

**Setup Required:**
```python
make_plans()
create_parties()
reset_settings()
frappe.db.set_value('Company', '_Test Company', 'accounts_frozen_till_date', None)
```

## Step-by-Step Guide

### Step 1: Assign subscription = frappe.new_doc(...)

```python
subscription = frappe.new_doc('Subscription')
```

### Step 2: Assign subscription.company = '_Test Company'

```python
subscription.company = '_Test Company'
```

### Step 3: Assign subscription.party_type = 'Supplier'

```python
subscription.party_type = 'Supplier'
```

### Step 4: Assign subscription.party = '_Test Supplier'

```python
subscription.party = '_Test Supplier'
```

### Step 5: Assign subscription.generate_invoice_at = 'Beginning of the current subscription period'

```python
subscription.generate_invoice_at = 'Beginning of the current subscription period'
```

### Step 6: Assign subscription.follow_calendar_months = 1

```python
subscription.follow_calendar_months = 1
```

### Step 7: Assign subscription.start_date = '2018-01-15'

```python
subscription.start_date = '2018-01-15'
```

### Step 8: Assign subscription.end_date = '2018-07-15'

```python
subscription.end_date = '2018-07-15'
```

### Step 9: Call subscription.append()

```python
subscription.append('plans', {'plan': '_Test Plan Name 4', 'qty': 1})
```

### Step 10: Call subscription.save()

```python
subscription.save()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(get_date_str(subscription.current_invoice_end), '2018-03-31')
```


## Complete Example

```python
# Setup
make_plans()
create_parties()
reset_settings()
frappe.db.set_value('Company', '_Test Company', 'accounts_frozen_till_date', None)

# Workflow
subscription = frappe.new_doc('Subscription')
subscription.company = '_Test Company'
subscription.party_type = 'Supplier'
subscription.party = '_Test Supplier'
subscription.generate_invoice_at = 'Beginning of the current subscription period'
subscription.follow_calendar_months = 1
subscription.start_date = '2018-01-15'
subscription.end_date = '2018-07-15'
subscription.append('plans', {'plan': '_Test Plan Name 4', 'qty': 1})
subscription.save()
self.assertEqual(get_date_str(subscription.current_invoice_end), '2018-03-31')
```

## Next Steps


---

*Source: test_subscription.py:400 | Complexity: Advanced | Last updated: 2026-02-03*