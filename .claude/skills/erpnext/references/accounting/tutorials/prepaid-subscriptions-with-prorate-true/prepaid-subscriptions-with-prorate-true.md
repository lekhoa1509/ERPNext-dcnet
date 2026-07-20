# How To: Prepaid Subscriptions With Prorate True

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test prepaid subscriptions with prorate true

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
subscription = create_subscription(generate_invoice_at='Beginning of the current subscription period')
```

### Step 6: Call subscription.process()

```python
subscription.process()
```

### Step 7: Call subscription.cancel_subscription()

```python
subscription.cancel_subscription()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(len(subscription.invoices), 1)
```

### Step 9: Assign current_inv = subscription.get_current_invoice(...)

```python
current_inv = subscription.get_current_invoice()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(current_inv.status, 'Unpaid')
```

### Step 11: Assign prorate_factor = 1

```python
prorate_factor = 1
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(flt(current_inv.grand_total, 2), flt(prorate_factor * 900, 2))
```

### Step 13: Assign settings.prorate = to_prorate

```python
settings.prorate = to_prorate
```

### Step 14: Call settings.save()

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
subscription = create_subscription(generate_invoice_at='Beginning of the current subscription period')
subscription.process()
subscription.cancel_subscription()
self.assertEqual(len(subscription.invoices), 1)
current_inv = subscription.get_current_invoice()
self.assertEqual(current_inv.status, 'Unpaid')
prorate_factor = 1
self.assertEqual(flt(current_inv.grand_total, 2), flt(prorate_factor * 900, 2))
settings.prorate = to_prorate
settings.save()
```

## Next Steps


---

*Source: test_subscription.py:378 | Complexity: Advanced | Last updated: 2026-02-03*