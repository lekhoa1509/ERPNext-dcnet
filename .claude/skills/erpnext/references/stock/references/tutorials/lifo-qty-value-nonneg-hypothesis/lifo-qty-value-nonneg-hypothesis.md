# How To: Lifo Qty Value Nonneg Hypothesis

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test lifo qty value nonneg hypothesis

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `json`
- `frappe`
- `frappe.tests`
- `hypothesis`
- `hypothesis`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.valuation`

**Setup Required:**
```python
self.stack = LIFOValuation([])
```

## Step-by-Step Guide

### Step 1: Assign self.stack = LIFOValuation(...)

```python
self.stack = LIFOValuation([])
```

### Step 2: Assign total_qty = 0.0

```python
total_qty = 0.0
```

### Step 3: Assign total_value = 0.0

```python
total_value = 0.0
```

### Step 4: Call self.assertTotalQty()

```python
self.assertTotalQty(total_qty)
```

### Step 5: Call self.assertTotalValue()

```python
self.assertTotalValue(total_value)
```

### Step 6: Call self.stack.add_stock()

```python
self.stack.add_stock(qty, rate)
```

### Step 7: Assign qty = abs(...)

```python
qty = abs(qty)
```

### Step 8: Assign consumed = self.stack.remove_stock(...)

```python
consumed = self.stack.remove_stock(qty)
```

### Step 9: Call self.assertAlmostEqual()

```python
self.assertAlmostEqual(qty, sum((q for q, _ in consumed)), msg=f'incorrect consumption {consumed}')
```


## Complete Example

```python
# Setup
self.stack = LIFOValuation([])

# Workflow
self.stack = LIFOValuation([])
total_qty = 0.0
total_value = 0.0
for qty, rate in stock_stack:
    if round_off_if_near_zero(qty) == 0 or total_qty + qty < 0 or abs(qty) < 0.1:
        continue
    if qty > 0:
        self.stack.add_stock(qty, rate)
        total_qty += qty
        total_value += qty * rate
    else:
        qty = abs(qty)
        consumed = self.stack.remove_stock(qty)
        self.assertAlmostEqual(qty, sum((q for q, _ in consumed)), msg=f'incorrect consumption {consumed}')
        total_qty -= qty
        total_value -= sum((q * r for q, r in consumed))
    self.assertTotalQty(total_qty)
    self.assertTotalValue(total_value)
```

## Next Steps


---

*Source: test_valuation.py:294 | Complexity: Advanced | Last updated: 2026-02-04*