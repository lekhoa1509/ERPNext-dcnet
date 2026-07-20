# How To: Exchange Rate Via Exchangerate Host

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, mock, workflow, integration

## Overview

Workflow: test exchange rate via exchangerate host

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `unittest`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.setup.utils`

**Setup Required:**
```python
# Fixtures: mock_get
```

## Step-by-Step Guide

### Step 1: Call save_new_records()

```python
save_new_records(self.globalTestRecords['Currency Exchange'])
```

### Step 2: Assign settings = frappe.get_single(...)

```python
settings = frappe.get_single('Currency Exchange Settings')
```

### Step 3: Assign settings.service_provider = 'exchangerate.host'

```python
settings.service_provider = 'exchangerate.host'
```

### Step 4: Assign settings.access_key = '12345667890'

```python
settings.access_key = '12345667890'
```

### Step 5: Call settings.save()

```python
settings.save()
```

### Step 6: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('Accounts Settings', 'allow_stale', 1)
```

### Step 7: Assign exchange_rate = get_exchange_rate(...)

```python
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-01', 'for_buying')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(flt(exchange_rate, 3), 60.0)
```

### Step 9: Assign exchange_rate = get_exchange_rate(...)

```python
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-15', 'for_buying')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(exchange_rate, 65.1)
```

### Step 11: Assign exchange_rate = get_exchange_rate(...)

```python
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-30', 'for_selling')
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(exchange_rate, 62.9)
```

### Step 13: Call self.clear_cache()

```python
self.clear_cache()
```

### Step 14: Assign exchange_rate = get_exchange_rate(...)

```python
exchange_rate = get_exchange_rate('USD', 'INR', '2015-12-15', 'for_selling')
```

### Step 15: Call self.assertFalse()

```python
self.assertFalse(exchange_rate == 60)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(flt(exchange_rate, 3), 66.999)
```

### Step 17: Assign exchange_rate = get_exchange_rate(...)

```python
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-20', 'for_buying')
```

### Step 18: Call self.assertFalse()

```python
self.assertFalse(exchange_rate == 60)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(flt(exchange_rate, 3), 65.1)
```

### Step 20: Assign settings = frappe.get_single(...)

```python
settings = frappe.get_single('Currency Exchange Settings')
```

### Step 21: Assign settings.service_provider = 'frankfurter.dev'

```python
settings.service_provider = 'frankfurter.dev'
```

### Step 22: Call settings.save()

```python
settings.save()
```


## Complete Example

```python
# Setup
# Fixtures: mock_get

# Workflow
save_new_records(self.globalTestRecords['Currency Exchange'])
settings = frappe.get_single('Currency Exchange Settings')
settings.service_provider = 'exchangerate.host'
settings.access_key = '12345667890'
settings.save()
frappe.db.set_single_value('Accounts Settings', 'allow_stale', 1)
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-01', 'for_buying')
self.assertEqual(flt(exchange_rate, 3), 60.0)
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-15', 'for_buying')
self.assertEqual(exchange_rate, 65.1)
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-30', 'for_selling')
self.assertEqual(exchange_rate, 62.9)
self.clear_cache()
exchange_rate = get_exchange_rate('USD', 'INR', '2015-12-15', 'for_selling')
self.assertFalse(exchange_rate == 60)
self.assertEqual(flt(exchange_rate, 3), 66.999)
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-20', 'for_buying')
self.assertFalse(exchange_rate == 60)
self.assertEqual(flt(exchange_rate, 3), 65.1)
settings = frappe.get_single('Currency Exchange Settings')
settings.service_provider = 'frankfurter.dev'
settings.save()
```

## Next Steps


---

*Source: test_currency_exchange.py:116 | Complexity: Advanced | Last updated: 2026-02-04*