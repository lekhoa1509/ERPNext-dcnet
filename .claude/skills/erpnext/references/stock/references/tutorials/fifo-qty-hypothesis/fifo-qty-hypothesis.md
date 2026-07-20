# How To: Fifo Qty Hypothesis

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test fifo qty hypothesis

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
# Fixtures: stock_queue
```

## Step-by-Step Guide

### Step 1: Assign self.queue = FIFOValuation(...)

```python
self.queue = FIFOValuation([])
```

### Step 2: Assign total_qty = 0

```python
total_qty = 0
```

### Step 3: Call self.assertTotalQty()

```python
self.assertTotalQty(total_qty)
```

### Step 4: Call self.queue.add_stock()

```python
self.queue.add_stock(qty, rate)
```

### Step 5: Assign qty = abs(...)

```python
qty = abs(qty)
```

### Step 6: Assign consumed = self.queue.remove_stock(...)

```python
consumed = self.queue.remove_stock(qty)
```

### Step 7: Call self.assertAlmostEqual()

```python
self.assertAlmostEqual(qty, sum((q for q, _ in consumed)), msg=f'incorrect consumption {consumed}')
```


## Complete Example

```python
# Setup
# Fixtures: stock_queue

# Workflow
self.queue = FIFOValuation([])
total_qty = 0
for qty, rate in stock_queue:
    if round_off_if_near_zero(qty) == 0:
        continue
    if qty > 0:
        self.queue.add_stock(qty, rate)
        total_qty += qty
    else:
        qty = abs(qty)
        consumed = self.queue.remove_stock(qty)
        self.assertAlmostEqual(qty, sum((q for q, _ in consumed)), msg=f'incorrect consumption {consumed}')
        total_qty -= qty
    self.assertTotalQty(total_qty)
```

## Next Steps


---

*Source: test_valuation.py:127 | Complexity: Intermediate | Last updated: 2026-02-04*