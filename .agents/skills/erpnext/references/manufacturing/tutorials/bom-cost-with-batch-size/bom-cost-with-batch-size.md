# How To: Bom Cost With Batch Size

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test bom cost with batch size

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
bom = frappe.copy_doc(self.globalTestRecords['BOM'][2])
```

### Step 2: Assign bom.docstatus = 0

```python
bom.docstatus = 0
```

### Step 3: Assign op_cost = 0.0

```python
op_cost = 0.0
```

### Step 4: Call bom.save()

```python
bom.save()
```

### Step 5: Call self.assertAlmostEqual()

```python
self.assertAlmostEqual(bom.operating_cost, op_cost / 2)
```

### Step 6: Call bom.delete()

```python
bom.delete()
```

### Step 7: Assign op_row.docstatus = 0

```python
op_row.docstatus = 0
```

### Step 8: Assign op_row.batch_size = 2

```python
op_row.batch_size = 2
```

### Step 9: Assign op_row.set_cost_based_on_bom_qty = 1

```python
op_row.set_cost_based_on_bom_qty = 1
```

### Step 10: Call self.assertAlmostEqual()

```python
self.assertAlmostEqual(op_row.cost_per_unit, op_row.operating_cost / 2)
```


## Complete Example

```python
# Workflow
bom = frappe.copy_doc(self.globalTestRecords['BOM'][2])
bom.docstatus = 0
op_cost = 0.0
for op_row in bom.operations:
    op_row.docstatus = 0
    op_row.batch_size = 2
    op_row.set_cost_based_on_bom_qty = 1
    op_cost += op_row.operating_cost
bom.save()
for op_row in bom.operations:
    self.assertAlmostEqual(op_row.cost_per_unit, op_row.operating_cost / 2)
self.assertAlmostEqual(bom.operating_cost, op_cost / 2)
bom.delete()
```

## Next Steps


---

*Source: test_bom.py:135 | Complexity: Advanced | Last updated: 2026-02-04*