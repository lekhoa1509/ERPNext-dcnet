# How To: Bom Stock Report

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test bom stock report

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.exceptions`
- `frappe.tests`
- `frappe.utils`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`
- `erpnext.manufacturing.report.bom_stock_report.bom_stock_report`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`


## Step-by-Step Guide

### Step 1: Assign filters = frappe._dict(...)

```python
filters = frappe._dict({'bom': self.bom.name, 'warehouse': 'Stores - _TC', 'qty_to_produce': 0})
```

### Step 2: Call self.assertRaises()

```python
self.assertRaises(ValidationError, bom_stock_report, filters)
```

### Step 3: Assign data = bom_stock_report(...)

```python
data = bom_stock_report(frappe._dict({'bom': self.bom.name, 'warehouse': 'Stores - _TC', 'qty_to_produce': 1}))
```

### Step 4: Assign expected_data = get_expected_data(...)

```python
expected_data = get_expected_data(self.bom, 'Stores - _TC', 1)
```

### Step 5: Call self.assertSetEqual()

```python
self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))
```

### Step 6: Assign data = bom_stock_report(...)

```python
data = bom_stock_report(frappe._dict({'bom': self.bom.name, 'warehouse': self.warehouse, 'qty_to_produce': 1}))
```

### Step 7: Assign expected_data = get_expected_data(...)

```python
expected_data = get_expected_data(self.bom, self.warehouse, 1)
```

### Step 8: Call self.assertSetEqual()

```python
self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))
```


## Complete Example

```python
# Workflow
filters = frappe._dict({'bom': self.bom.name, 'warehouse': 'Stores - _TC', 'qty_to_produce': 0})
self.assertRaises(ValidationError, bom_stock_report, filters)
data = bom_stock_report(frappe._dict({'bom': self.bom.name, 'warehouse': 'Stores - _TC', 'qty_to_produce': 1}))
expected_data = get_expected_data(self.bom, 'Stores - _TC', 1)
self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))
data = bom_stock_report(frappe._dict({'bom': self.bom.name, 'warehouse': self.warehouse, 'qty_to_produce': 1}))
expected_data = get_expected_data(self.bom, self.warehouse, 1)
self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))
```

## Next Steps


---

*Source: test_bom_stock_report.py:26 | Complexity: Advanced | Last updated: 2026-02-04*