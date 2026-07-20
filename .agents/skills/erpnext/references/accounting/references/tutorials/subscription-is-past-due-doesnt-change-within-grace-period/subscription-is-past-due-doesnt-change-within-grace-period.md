# How To: Subscription Is Past Due Doesnt Change Within Grace Period

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test subscription is past due doesnt change within grace period

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

### Step 2: Assign grace_period = value

```python
grace_period = settings.grace_period
```

### Step 3: Assign settings.grace_period = 1000

```python
settings.grace_period = 1000
```

### Step 4: Call settings.save()

```python
settings.save()
```

### Step 5: Assign subscription = create_subscription(...)

```python
subscription = create_subscription(start_date=add_days(nowdate(), -1000))
```

### Step 6: Call subscription.process()

```python
subscription.process(posting_date=subscription.current_invoice_end)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(subscription.status, 'Grace Period')
```

### Step 8: Call subscription.process()

```python
subscription.process()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(subscription.status, 'Grace Period')
```

### Step 10: Call subscription.process()

```python
subscription.process()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(subscription.status, 'Grace Period')
```

### Step 12: Call subscription.process()

```python
subscription.process()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(subscription.status, 'Grace Period')
```

### Step 14: Assign settings.grace_period = grace_period

```python
settings.grace_period = grace_period
```

### Step 15: Call settings.save()

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
grace_period = settings.grace_period
settings.grace_period = 1000
settings.save()
subscription = create_subscription(start_date=add_days(nowdate(), -1000))
subscription.process(posting_date=subscription.current_invoice_end)
self.assertEqual(subscription.status, 'Grace Period')
subscription.process()
self.assertEqual(subscription.status, 'Grace Period')
subscription.process()
self.assertEqual(subscription.status, 'Grace Period')
subscription.process()
self.assertEqual(subscription.status, 'Grace Period')
settings.grace_period = grace_period
settings.save()
```

## Next Steps


---

*Source: test_subscription.py:138 | Complexity: Advanced | Last updated: 2026-02-03*