# How To: Subscription Cancellation Invoices With Prorata False

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test subscription cancellation invoices with prorata false

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

### Step 1: Assign settings = frappe.get_single(...)

```python
settings = frappe.get_single('Subscription Settings')
```

### Step 2: Assign to_prorate = value

```python
to_prorate = settings.prorate
```

### Step 3: Assign settings.prorate = 0

```python
settings.prorate = 0
```

### Step 4: Call settings.save()

```python
settings.save()
```

### Step 5: Assign subscription = create_subscription(...)

```python
subscription = create_subscription()
```

### Step 6: Call subscription.cancel_subscription()

```python
subscription.cancel_subscription()
```

### Step 7: Assign invoice = subscription.get_current_invoice(...)

```python
invoice = subscription.get_current_invoice()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(invoice.grand_total, 900)
```

### Step 9: Assign settings.prorate = to_prorate

```python
settings.prorate = to_prorate
```

### Step 10: Call settings.save()

```python
settings.save()
```


## Complete Example

```python
# Setup
make_plans()
create_parties()
reset_settings()
frappe.db.set_value('Company', '_Test Company', 'accounts_frozen_till_date', None)

# Workflow
settings = frappe.get_single('Subscription Settings')
to_prorate = settings.prorate
settings.prorate = 0
settings.save()
subscription = create_subscription()
subscription.cancel_subscription()
invoice = subscription.get_current_invoice()
self.assertEqual(invoice.grand_total, 900)
settings.prorate = to_prorate
settings.save()
```

## Next Steps


---

*Source: test_subscription.py:224 | Complexity: Advanced | Last updated: 2026-02-03*