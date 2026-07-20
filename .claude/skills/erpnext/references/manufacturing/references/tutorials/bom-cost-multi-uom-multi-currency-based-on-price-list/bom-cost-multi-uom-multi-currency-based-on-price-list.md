# How To: Bom Cost Multi Uom Multi Currency Based On Price List

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test bom cost multi uom multi currency based on price list

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

### Step 1: Call frappe.db.set_value()

```python
frappe.db.set_value('Price List', '_Test Price List', 'price_not_uom_dependent', 1)
```

### Step 2: Assign bom = frappe.copy_doc(...)

```python
bom = frappe.copy_doc(self.globalTestRecords['BOM'][2])
```

### Step 3: Assign bom.set_rate_of_sub_assembly_item_based_on_bom = 0

```python
bom.set_rate_of_sub_assembly_item_based_on_bom = 0
```

### Step 4: Assign bom.rm_cost_as_per = 'Price List'

```python
bom.rm_cost_as_per = 'Price List'
```

### Step 5: Assign bom.buying_price_list = '_Test Price List'

```python
bom.buying_price_list = '_Test Price List'
```

### Step 6: Assign unknown.uom = '_Test UOM 1'

```python
bom.items[0].uom = '_Test UOM 1'
```

### Step 7: Assign unknown.conversion_factor = 5

```python
bom.items[0].conversion_factor = 5
```

### Step 8: Call bom.insert()

```python
bom.insert()
```

### Step 9: Call bom.update_cost()

```python
bom.update_cost(update_hour_rate=False)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(bom.items[0].rate, 300)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(bom.items[1].rate, 50)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(bom.operating_cost, 100)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(bom.raw_material_cost, 450)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(bom.total_cost, 550)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(bom.items[0].base_rate, 18000)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(bom.items[1].base_rate, 3000)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(bom.base_operating_cost, 6000)
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(bom.base_raw_material_cost, 27000)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(bom.base_total_cost, 33000)
```

### Step 20: Call frappe.db.sql()

```python
frappe.db.sql("delete from `tabItem Price` where price_list='_Test Price List' and item_code=%s", item_code)
```

### Step 21: Assign item_price = frappe.new_doc(...)

```python
item_price = frappe.new_doc('Item Price')
```

### Step 22: Assign item_price.price_list = '_Test Price List'

```python
item_price.price_list = '_Test Price List'
```

### Step 23: Assign item_price.item_code = item_code

```python
item_price.item_code = item_code
```

### Step 24: Assign item_price.price_list_rate = rate

```python
item_price.price_list_rate = rate
```

### Step 25: Call item_price.insert()

```python
item_price.insert()
```


## Complete Example

```python
# Workflow
frappe.db.set_value('Price List', '_Test Price List', 'price_not_uom_dependent', 1)
for item_code, rate in (('_Test Item', 3600), ('_Test Item Home Desktop Manufactured', 3000)):
    frappe.db.sql("delete from `tabItem Price` where price_list='_Test Price List' and item_code=%s", item_code)
    item_price = frappe.new_doc('Item Price')
    item_price.price_list = '_Test Price List'
    item_price.item_code = item_code
    item_price.price_list_rate = rate
    item_price.insert()
bom = frappe.copy_doc(self.globalTestRecords['BOM'][2])
bom.set_rate_of_sub_assembly_item_based_on_bom = 0
bom.rm_cost_as_per = 'Price List'
bom.buying_price_list = '_Test Price List'
bom.items[0].uom = '_Test UOM 1'
bom.items[0].conversion_factor = 5
bom.insert()
bom.update_cost(update_hour_rate=False)
self.assertEqual(bom.items[0].rate, 300)
self.assertEqual(bom.items[1].rate, 50)
self.assertEqual(bom.operating_cost, 100)
self.assertEqual(bom.raw_material_cost, 450)
self.assertEqual(bom.total_cost, 550)
self.assertEqual(bom.items[0].base_rate, 18000)
self.assertEqual(bom.items[1].base_rate, 3000)
self.assertEqual(bom.base_operating_cost, 6000)
self.assertEqual(bom.base_raw_material_cost, 27000)
self.assertEqual(bom.base_total_cost, 33000)
```

## Next Steps


---

*Source: test_bom.py:154 | Complexity: Advanced | Last updated: 2026-02-04*