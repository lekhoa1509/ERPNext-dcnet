# How To: Subscription Cancellation And Process

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test subscription cancellation and process

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

### Step 2: Assign default_grace_period_action = value

```python
default_grace_period_action = settings.cancel_after_grace
```

### Step 3: Assign settings.cancel_after_grace = 1

```python
settings.cancel_after_grace = 1
```

### Step 4: Call settings.save()

```python
settings.save()
```

### Step 5: Assign subscription = create_subscription(...)

```python
subscription = create_subscription(start_date='2018-01-01')
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
self.assertEqual(subscription.status, 'Cancelled')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(len(subscription.invoices), 1)
```

### Step 10: Call subscription.process()

```python
subscription.process()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(subscription.status, 'Cancelled')
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(len(subscription.invoices), 1)
```

### Step 13: Call subscription.process()

```python
subscription.process()
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(subscription.status, 'Cancelled')
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(len(subscription.invoices), 1)
```

### Step 16: Assign settings.cancel_after_grace = default_grace_period_action

```python
settings.cancel_after_grace = default_grace_period_action
```

### Step 17: Call settings.save()

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
default_grace_period_action = settings.cancel_after_grace
settings.cancel_after_grace = 1
settings.save()
subscription = create_subscription(start_date='2018-01-01')
subscription.process()
subscription.cancel_subscription()
self.assertEqual(subscription.status, 'Cancelled')
self.assertEqual(len(subscription.invoices), 1)
subscription.process()
self.assertEqual(subscription.status, 'Cancelled')
self.assertEqual(len(subscription.invoices), 1)
subscription.process()
self.assertEqual(subscription.status, 'Cancelled')
self.assertEqual(len(subscription.invoices), 1)
settings.cancel_after_grace = default_grace_period_action
settings.save()
```

## Next Steps


---

*Source: test_subscription.py:258 | Complexity: Advanced | Last updated: 2026-02-03*