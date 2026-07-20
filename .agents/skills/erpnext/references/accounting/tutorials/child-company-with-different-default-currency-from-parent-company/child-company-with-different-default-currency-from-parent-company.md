# How To: Child Company With Different Default Currency From Parent Company

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test child company with different default currency from parent company

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.report.consolidated_trial_balance.consolidated_trial_balance`
- `erpnext.setup.utils`
- `erpnext.accounts.report.trial_balance.test_trial_balance`
- `erpnext.accounts.utils`


## Step-by-Step Guide

### Step 1: Assign filters = frappe._dict(...)

```python
filters = frappe._dict({'company': ['Parent Group Company India', 'Child Company US'], 'fiscal_year': self.fiscal_year})
```

### Step 2: Assign report = execute(...)

```python
report = execute(filters)
```

### Step 3: Assign total_row = value

```python
total_row = report[1][-1]
```

### Step 4: Assign exchange_rate = get_exchange_rate(...)

```python
exchange_rate = get_exchange_rate('USD', 'INR')
```

### Step 5: Assign fctr = value

```python
fctr = [d for d in report[1] if d.get('account') == _('Foreign Currency Translation Reserve')]
```

### Step 6: Assign ccu_total_credit = value

```python
ccu_total_credit = 1000 * flt(exchange_rate)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(total_row['closing_debit'], total_row['closing_credit'])
```

### Step 8: Call self.assertNotEqual()

```python
self.assertNotEqual(total_row['closing_credit'], ccu_total_credit)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(total_row['closing_credit'], flt(100000 + ccu_total_credit))
```


## Complete Example

```python
# Workflow
filters = frappe._dict({'company': ['Parent Group Company India', 'Child Company US'], 'fiscal_year': self.fiscal_year})
report = execute(filters)
total_row = report[1][-1]
exchange_rate = get_exchange_rate('USD', 'INR')
fctr = [d for d in report[1] if d.get('account') == _('Foreign Currency Translation Reserve')]
if not fctr:
    raise ForeignCurrencyTranslationReserveNotFoundError
ccu_total_credit = 1000 * flt(exchange_rate)
self.assertEqual(total_row['closing_debit'], total_row['closing_credit'])
self.assertNotEqual(total_row['closing_credit'], ccu_total_credit)
self.assertEqual(total_row['closing_credit'], flt(100000 + ccu_total_credit))
```

## Next Steps


---

*Source: test_consolidated_trial_balance.py:75 | Complexity: Advanced | Last updated: 2026-02-03*