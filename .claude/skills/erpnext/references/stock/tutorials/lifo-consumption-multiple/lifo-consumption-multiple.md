# How To: Lifo Consumption Multiple

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test lifo consumption multiple

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

### Step 1: Call self.stack.add_stock()

```python
self.stack.add_stock(1, 1)
```

### Step 2: Call self.stack.add_stock()

```python
self.stack.add_stock(2, 2)
```

### Step 3: Assign consumed = self.stack.remove_stock(...)

```python
consumed = self.stack.remove_stock(1)
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(consumed, [[1, 2]])
```

### Step 5: Call self.stack.add_stock()

```python
self.stack.add_stock(3, 3)
```

### Step 6: Assign consumed = self.stack.remove_stock(...)

```python
consumed = self.stack.remove_stock(4)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(consumed, [[3, 3], [1, 2]])
```

### Step 8: Call self.stack.add_stock()

```python
self.stack.add_stock(4, 4)
```

### Step 9: Assign consumed = self.stack.remove_stock(...)

```python
consumed = self.stack.remove_stock(5)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(consumed, [[4, 4], [1, 1]])
```

### Step 11: Call self.stack.add_stock()

```python
self.stack.add_stock(5, 5)
```

### Step 12: Assign consumed = self.stack.remove_stock(...)

```python
consumed = self.stack.remove_stock(5)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(consumed, [[5, 5]])
```


## Complete Example

```python
# Setup
self.stack = LIFOValuation([])

# Workflow
self.stack.add_stock(1, 1)
self.stack.add_stock(2, 2)
consumed = self.stack.remove_stock(1)
self.assertEqual(consumed, [[1, 2]])
self.stack.add_stock(3, 3)
consumed = self.stack.remove_stock(4)
self.assertEqual(consumed, [[3, 3], [1, 2]])
self.stack.add_stock(4, 4)
consumed = self.stack.remove_stock(5)
self.assertEqual(consumed, [[4, 4], [1, 1]])
self.stack.add_stock(5, 5)
consumed = self.stack.remove_stock(5)
self.assertEqual(consumed, [[5, 5]])
```

## Next Steps


---

*Source: test_valuation.py:255 | Complexity: Advanced | Last updated: 2026-02-04*