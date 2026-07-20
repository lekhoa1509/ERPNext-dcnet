# How To: Subscription Cancellation Invoices With Prorata True

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test subscription cancellation invoices with prorata true

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

### Step 3: Assign settings.prorate = 1

```python
settings.prorate = 1
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

### Step 8: Assign diff = flt(...)

```python
diff = flt(date_diff(nowdate(), subscription.current_invoice_start) + 1)
```

### Step 9: Assign plan_days = flt(...)

```python
plan_days = flt(date_diff(subscription.current_invoice_end, subscription.current_invoice_start) + 1)
```

### Step 10: Assign prorate_factor = flt(...)

```python
prorate_factor = flt(diff / plan_days)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(flt(invoice.grand_total, 2), flt(prorate_factor * 900, 2))
```

### Step 12: Assign settings.prorate = to_prorate

```python
settings.prorate = to_prorate
```

### Step 13: Call settings.save()

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
settings.prorate = 1
settings.save()
subscription = create_subscription()
subscription.cancel_subscription()
invoice = subscription.get_current_invoice()
diff = flt(date_diff(nowdate(), subscription.current_invoice_start) + 1)
plan_days = flt(date_diff(subscription.current_invoice_end, subscription.current_invoice_start) + 1)
prorate_factor = flt(diff / plan_days)
self.assertEqual(flt(invoice.grand_total, 2), flt(prorate_factor * 900, 2))
settings.prorate = to_prorate
settings.save()
```

## Next Steps


---

*Source: test_subscription.py:239 | Complexity: Advanced | Last updated: 2026-02-03*