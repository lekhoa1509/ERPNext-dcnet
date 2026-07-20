# How To: Bom Stock Calculated

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test bom stock calculated

## Prerequisites

**Required Modules:**
- `frappe.tests`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`
- `erpnext.manufacturing.report.bom_stock_calculated.bom_stock_calculated`
- `erpnext.stock.doctype.item.test_item`


## Step-by-Step Guide

### Step 1: Assign qty_to_make = 10

```python
qty_to_make = 10
```

### Step 2: Assign data = value

```python
data = bom_stock_calculated_report(filters={'qty_to_make': qty_to_make, 'bom': self.boms[0].name})[1]
```

### Step 3: Assign expected_data = get_expected_data(...)

```python
expected_data = get_expected_data(self.boms[0], qty_to_make)
```

### Step 4: Call self.assertSetEqual()

```python
self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))
```

### Step 5: Assign data = value

```python
data = bom_stock_calculated_report(filters={'qty_to_make': qty_to_make, 'bom': self.boms[1].name})[1]
```

### Step 6: Assign expected_data = get_expected_data(...)

```python
expected_data = get_expected_data(self.boms[1], qty_to_make)
```

### Step 7: Call self.assertSetEqual()

```python
self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))
```

### Step 8: Assign data = value

```python
data = bom_stock_calculated_report(filters={'qty_to_make': qty_to_make, 'bom': self.boms[2].name})[1]
```

### Step 9: Assign expected_data = get_expected_data(...)

```python
expected_data = get_expected_data(self.boms[2], qty_to_make)
```

### Step 10: Call self.assertSetEqual()

```python
self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))
```


## Complete Example

```python
# Workflow
qty_to_make = 10
data = bom_stock_calculated_report(filters={'qty_to_make': qty_to_make, 'bom': self.boms[0].name})[1]
expected_data = get_expected_data(self.boms[0], qty_to_make)
self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))
data = bom_stock_calculated_report(filters={'qty_to_make': qty_to_make, 'bom': self.boms[1].name})[1]
expected_data = get_expected_data(self.boms[1], qty_to_make)
self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))
data = bom_stock_calculated_report(filters={'qty_to_make': qty_to_make, 'bom': self.boms[2].name})[1]
expected_data = get_expected_data(self.boms[2], qty_to_make)
self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))
```

## Next Steps


---

*Source: test_bom_stock_calculated.py:18 | Complexity: Advanced | Last updated: 2026-02-04*