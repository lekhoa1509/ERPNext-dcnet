# How To: Lifo Values

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test lifo values

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe.tests`
- `hypothesis`
- `hypothesis`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.valuation`


## Step-by-Step Guide

### Step 1: Assign in1 = self._make_stock_entry(...)

```python
in1 = self._make_stock_entry(1, 1)
```

### Step 2: Call self.assertStockQueue()

```python
self.assertStockQueue(in1, [[1, 1]])
```

### Step 3: Assign in2 = self._make_stock_entry(...)

```python
in2 = self._make_stock_entry(2, 2)
```

### Step 4: Call self.assertStockQueue()

```python
self.assertStockQueue(in2, [[1, 1], [2, 2]])
```

### Step 5: Assign out1 = self._make_stock_entry(...)

```python
out1 = self._make_stock_entry(-1)
```

### Step 6: Call self.assertStockQueue()

```python
self.assertStockQueue(out1, [[1, 1], [1, 2]])
```

### Step 7: Assign in3 = self._make_stock_entry(...)

```python
in3 = self._make_stock_entry(3, 3)
```

### Step 8: Call self.assertStockQueue()

```python
self.assertStockQueue(in3, [[1, 1], [1, 2], [3, 3]])
```

### Step 9: Assign out2 = self._make_stock_entry(...)

```python
out2 = self._make_stock_entry(-4)
```

### Step 10: Call self.assertStockQueue()

```python
self.assertStockQueue(out2, [[1, 1]])
```

### Step 11: Assign in4 = self._make_stock_entry(...)

```python
in4 = self._make_stock_entry(4, 4)
```

### Step 12: Call self.assertStockQueue()

```python
self.assertStockQueue(in4, [[1, 1], [4, 4]])
```

### Step 13: Assign out3 = self._make_stock_entry(...)

```python
out3 = self._make_stock_entry(-5)
```

### Step 14: Call self.assertStockQueue()

```python
self.assertStockQueue(out3, [])
```

### Step 15: Assign in5 = self._make_stock_entry(...)

```python
in5 = self._make_stock_entry(5, 5)
```

### Step 16: Call self.assertStockQueue()

```python
self.assertStockQueue(in5, [[5, 5]])
```

### Step 17: Assign out5 = self._make_stock_entry(...)

```python
out5 = self._make_stock_entry(-5)
```

### Step 18: Call self.assertStockQueue()

```python
self.assertStockQueue(out5, [])
```


## Complete Example

```python
# Workflow
in1 = self._make_stock_entry(1, 1)
self.assertStockQueue(in1, [[1, 1]])
in2 = self._make_stock_entry(2, 2)
self.assertStockQueue(in2, [[1, 1], [2, 2]])
out1 = self._make_stock_entry(-1)
self.assertStockQueue(out1, [[1, 1], [1, 2]])
in3 = self._make_stock_entry(3, 3)
self.assertStockQueue(in3, [[1, 1], [1, 2], [3, 3]])
out2 = self._make_stock_entry(-4)
self.assertStockQueue(out2, [[1, 1]])
in4 = self._make_stock_entry(4, 4)
self.assertStockQueue(in4, [[1, 1], [4, 4]])
out3 = self._make_stock_entry(-5)
self.assertStockQueue(out3, [])
in5 = self._make_stock_entry(5, 5)
self.assertStockQueue(in5, [[5, 5]])
out5 = self._make_stock_entry(-5)
self.assertStockQueue(out5, [])
```

## Next Steps


---

*Source: test_valuation.py:352 | Complexity: Advanced | Last updated: 2026-02-04*