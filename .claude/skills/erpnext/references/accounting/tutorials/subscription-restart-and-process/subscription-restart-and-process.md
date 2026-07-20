# How To: Subscription Restart And Process

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test subscription restart and process

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

### Step 3: Assign settings.grace_period = 0

```python
settings.grace_period = 0
```

### Step 4: Assign settings.cancel_after_grace = 0

```python
settings.cancel_after_grace = 0
```

### Step 5: Call settings.save()

```python
settings.save()
```

### Step 6: Assign subscription = create_subscription(...)

```python
subscription = create_subscription(start_date='2018-01-01')
```

### Step 7: Call subscription.process()

```python
subscription.process(posting_date='2018-01-31')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(subscription.status, 'Unpaid')
```

### Step 9: Call subscription.cancel_subscription()

```python
subscription.cancel_subscription()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(subscription.status, 'Cancelled')
```

### Step 11: Call subscription.restart_subscription()

```python
subscription.restart_subscription()
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(subscription.status, 'Active')
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(len(subscription.invoices), 1)
```

### Step 14: Call subscription.process()

```python
subscription.process()
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(subscription.status, 'Unpaid')
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(len(subscription.invoices), 1)
```

### Step 17: Call subscription.process()

```python
subscription.process()
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(subscription.status, 'Unpaid')
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(len(subscription.invoices), 1)
```

### Step 20: Assign settings.cancel_after_grace = default_grace_period_action

```python
settings.cancel_after_grace = default_grace_period_action
```

### Step 21: Call settings.save()

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
settings.grace_period = 0
settings.cancel_after_grace = 0
settings.save()
subscription = create_subscription(start_date='2018-01-01')
subscription.process(posting_date='2018-01-31')
self.assertEqual(subscription.status, 'Unpaid')
subscription.cancel_subscription()
self.assertEqual(subscription.status, 'Cancelled')
subscription.restart_subscription()
self.assertEqual(subscription.status, 'Active')
self.assertEqual(len(subscription.invoices), 1)
subscription.process()
self.assertEqual(subscription.status, 'Unpaid')
self.assertEqual(len(subscription.invoices), 1)
subscription.process()
self.assertEqual(subscription.status, 'Unpaid')
self.assertEqual(len(subscription.invoices), 1)
settings.cancel_after_grace = default_grace_period_action
settings.save()
```

## Next Steps


---

*Source: test_subscription.py:283 | Complexity: Advanced | Last updated: 2026-02-03*