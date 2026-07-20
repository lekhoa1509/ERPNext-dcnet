# How To: Bom Cost With Fg Based Operating Cost

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test bom cost with fg based operating cost

## Prerequisites

**Required Modules:**
- `collections`
- `functools`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.controllers.tests.test_subcontracting_controller`
- `erpnext.manufacturing.doctype.bom.bom`
- `erpnext.manufacturing.doctype.bom_update_log.test_bom_update_log`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.manufacturing.doctype.bom.bom`
- `erpnext.manufacturing.doctype.bom.bom`
- `erpnext.manufacturing.doctype.bom.bom`
- `erpnext.controllers.tests.test_subcontracting_controller`
- `erpnext.controllers.item_variant`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`
- `erpnext.manufacturing.doctype.bom.bom`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`


## Step-by-Step Guide

### Step 1: Assign bom = frappe.copy_doc(...)

```python
bom = frappe.copy_doc(self.globalTestRecords['BOM'][4])
```

### Step 2: Call bom.insert()

```python
bom.insert()
```

### Step 3: Assign raw_material_cost = 0.0

```python
raw_material_cost = 0.0
```

### Step 4: Assign op_cost = 0.0

```python
op_cost = 0.0
```

### Step 5: Assign op_cost = value

```python
op_cost = bom.quantity * bom.operating_cost_per_bom_quantity
```

### Step 6: Assign base_raw_material_cost = value

```python
base_raw_material_cost = raw_material_cost * flt(bom.conversion_rate, bom.precision('conversion_rate'))
```

### Step 7: Assign base_op_cost = value

```python
base_op_cost = op_cost * flt(bom.conversion_rate, bom.precision('conversion_rate'))
```

### Step 8: Call self.assertAlmostEqual()

```python
self.assertAlmostEqual(bom.operating_cost, op_cost)
```

### Step 9: Call self.assertAlmostEqual()

```python
self.assertAlmostEqual(bom.raw_material_cost, raw_material_cost)
```

### Step 10: Call self.assertAlmostEqual()

```python
self.assertAlmostEqual(bom.total_cost, raw_material_cost + op_cost)
```

### Step 11: Call self.assertAlmostEqual()

```python
self.assertAlmostEqual(bom.base_operating_cost, base_op_cost)
```

### Step 12: Call self.assertAlmostEqual()

```python
self.assertAlmostEqual(bom.base_raw_material_cost, base_raw_material_cost)
```

### Step 13: Call self.assertAlmostEqual()

```python
self.assertAlmostEqual(bom.base_total_cost, base_raw_material_cost + base_op_cost)
```


## Complete Example

```python
# Workflow
bom = frappe.copy_doc(self.globalTestRecords['BOM'][4])
bom.insert()
raw_material_cost = 0.0
op_cost = 0.0
op_cost = bom.quantity * bom.operating_cost_per_bom_quantity
for row in bom.items:
    raw_material_cost += row.amount
base_raw_material_cost = raw_material_cost * flt(bom.conversion_rate, bom.precision('conversion_rate'))
base_op_cost = op_cost * flt(bom.conversion_rate, bom.precision('conversion_rate'))
self.assertAlmostEqual(bom.operating_cost, op_cost)
self.assertAlmostEqual(bom.raw_material_cost, raw_material_cost)
self.assertAlmostEqual(bom.total_cost, raw_material_cost + op_cost)
self.assertAlmostEqual(bom.base_operating_cost, base_op_cost)
self.assertAlmostEqual(bom.base_raw_material_cost, base_raw_material_cost)
self.assertAlmostEqual(bom.base_total_cost, base_raw_material_cost + base_op_cost)
```

## Next Steps


---

*Source: test_bom.py:211 | Complexity: Advanced | Last updated: 2026-02-04*