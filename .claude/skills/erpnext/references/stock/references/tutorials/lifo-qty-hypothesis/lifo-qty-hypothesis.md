# How To: Lifo Qty Hypothesis

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test lifo qty hypothesis

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

### Step 2: Assign total_qty = 0

```python
total_qty = 0
```

### Step 3: Call self.assertTotalQty()

```python
self.assertTotalQty(total_qty)
```

### Step 4: Call self.stack.add_stock()

```python
self.stack.add_stock(qty, rate)
```

### Step 5: Assign qty = abs(...)

```python
qty = abs(qty)
```

### Step 6: Assign consumed = self.stack.remove_stock(...)

```python
consumed = self.stack.remove_stock(qty)
```

### Step 7: Call self.assertAlmostEqual()

```python
self.assertAlmostEqual(qty, sum((q for q, _ in consumed)), msg=f'incorrect consumption {consumed}')
```


## Complete Example

```python
# Setup
self.stack = LIFOValuation([])

# Workflow
self.stack = LIFOValuation([])
total_qty = 0
for qty, rate in stock_stack:
    if round_off_if_near_zero(qty) == 0:
        continue
    if qty > 0:
        self.stack.add_stock(qty, rate)
        total_qty += qty
    else:
        qty = abs(qty)
        consumed = self.stack.remove_stock(qty)
        self.assertAlmostEqual(qty, sum((q for q, _ in consumed)), msg=f'incorrect consumption {consumed}')
        total_qty -= qty
    self.assertTotalQty(total_qty)
```

## Next Steps


---

*Source: test_valuation.py:274 | Complexity: Intermediate | Last updated: 2026-02-04*