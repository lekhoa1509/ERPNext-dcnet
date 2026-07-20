# How To: Exchange Rate

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, mock, workflow, integration

## Overview

Workflow: test exchange rate

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

### Step 2: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('Accounts Settings', 'allow_stale', 1)
```

### Step 3: Assign exchange_rate = get_exchange_rate(...)

```python
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-01', 'for_buying')
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(flt(exchange_rate, 3), 60.0)
```

### Step 5: Assign exchange_rate = get_exchange_rate(...)

```python
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-15', 'for_buying')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(exchange_rate, 65.1)
```

### Step 7: Assign exchange_rate = get_exchange_rate(...)

```python
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-30', 'for_selling')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(exchange_rate, 62.9)
```

### Step 9: Call self.clear_cache()

```python
self.clear_cache()
```

### Step 10: Assign exchange_rate = get_exchange_rate(...)

```python
exchange_rate = get_exchange_rate('USD', 'INR', '2015-12-15', 'for_selling')
```

### Step 11: Call self.assertFalse()

```python
self.assertFalse(exchange_rate == 60)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(flt(exchange_rate, 3), 66.999)
```

### Step 13: Assign exchange_rate = get_exchange_rate(...)

```python
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-20', 'for_buying')
```

### Step 14: Call self.assertFalse()

```python
self.assertFalse(exchange_rate == 60)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(flt(exchange_rate, 3), 65.1)
```


## Complete Example

```python
# Setup
# Fixtures: mock_get

# Workflow
save_new_records(self.globalTestRecords['Currency Exchange'])
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
```

## Next Steps


---

*Source: test_currency_exchange.py:91 | Complexity: Advanced | Last updated: 2026-02-04*