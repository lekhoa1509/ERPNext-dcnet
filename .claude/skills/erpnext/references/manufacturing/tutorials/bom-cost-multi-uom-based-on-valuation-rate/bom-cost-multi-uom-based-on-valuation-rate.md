# How To: Bom Cost Multi Uom Based On Valuation Rate

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test bom cost multi uom based on valuation rate

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

### Step 2: Assign bom.set_rate_of_sub_assembly_item_based_on_bom = 0

```python
bom.set_rate_of_sub_assembly_item_based_on_bom = 0
```

### Step 3: Assign bom.rm_cost_as_per = 'Valuation Rate'

```python
bom.rm_cost_as_per = 'Valuation Rate'
```

### Step 4: Assign unknown.uom = '_Test UOM 1'

```python
bom.items[0].uom = '_Test UOM 1'
```

### Step 5: Assign unknown.conversion_factor = 6

```python
bom.items[0].conversion_factor = 6
```

### Step 6: Call bom.insert()

```python
bom.insert()
```

### Step 7: Call reset_item_valuation_rate()

```python
reset_item_valuation_rate(item_code='_Test Item', warehouse_list=frappe.get_all('Warehouse', {'is_group': 0, 'company': bom.company}, pluck='name'), qty=200, rate=200)
```

### Step 8: Call bom.update_cost()

```python
bom.update_cost()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(bom.items[0].rate, 20)
```


## Complete Example

```python
# Workflow
bom = frappe.copy_doc(self.globalTestRecords['BOM'][2])
bom.set_rate_of_sub_assembly_item_based_on_bom = 0
bom.rm_cost_as_per = 'Valuation Rate'
bom.items[0].uom = '_Test UOM 1'
bom.items[0].conversion_factor = 6
bom.insert()
reset_item_valuation_rate(item_code='_Test Item', warehouse_list=frappe.get_all('Warehouse', {'is_group': 0, 'company': bom.company}, pluck='name'), qty=200, rate=200)
bom.update_cost()
self.assertEqual(bom.items[0].rate, 20)
```

## Next Steps


---

*Source: test_bom.py:191 | Complexity: Advanced | Last updated: 2026-02-04*