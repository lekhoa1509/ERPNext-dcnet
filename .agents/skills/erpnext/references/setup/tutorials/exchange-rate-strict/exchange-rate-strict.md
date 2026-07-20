# How To: Exchange Rate Strict

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, mock, workflow, integration

## Overview

Workflow: test exchange rate strict

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

### Step 1: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('Accounts Settings', 'allow_stale', 0)
```

### Step 2: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('Accounts Settings', 'stale_days', 1)
```

### Step 3: Assign exchange_rate = get_exchange_rate(...)

```python
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-01', 'for_buying')
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(exchange_rate, 60.0)
```

### Step 5: Call self.clear_cache()

```python
self.clear_cache()
```

### Step 6: Assign exchange_rate = get_exchange_rate(...)

```python
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-15', 'for_buying')
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(flt(exchange_rate, 3), 65.1)
```

### Step 8: Assign exchange_rate = get_exchange_rate(...)

```python
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-30', 'for_selling')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(exchange_rate, 62.9)
```

### Step 10: Call self.clear_cache()

```python
self.clear_cache()
```

### Step 11: Assign exchange_rate = get_exchange_rate(...)

```python
exchange_rate = get_exchange_rate('USD', 'INR', '2015-12-15', 'for_buying')
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(flt(exchange_rate, 3), 66.999)
```


## Complete Example

```python
# Setup
# Fixtures: mock_get

# Workflow
frappe.db.set_single_value('Accounts Settings', 'allow_stale', 0)
frappe.db.set_single_value('Accounts Settings', 'stale_days', 1)
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-01', 'for_buying')
self.assertEqual(exchange_rate, 60.0)
self.clear_cache()
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-15', 'for_buying')
self.assertEqual(flt(exchange_rate, 3), 65.1)
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-30', 'for_selling')
self.assertEqual(exchange_rate, 62.9)
self.clear_cache()
exchange_rate = get_exchange_rate('USD', 'INR', '2015-12-15', 'for_buying')
self.assertEqual(flt(exchange_rate, 3), 66.999)
```

## Next Steps


---

*Source: test_currency_exchange.py:152 | Complexity: Advanced | Last updated: 2026-02-04*