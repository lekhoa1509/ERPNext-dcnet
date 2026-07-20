# How To: Bom Recursion 1St Level

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: BOM should not allow BOM item again in child

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

### Step 1: 'BOM should not allow BOM item again in child'

```python
'BOM should not allow BOM item again in child'
```

### Step 2: Assign item_code = value

```python
item_code = make_item(properties={'is_stock_item': 1}).name
```

### Step 3: Assign bom = frappe.new_doc(...)

```python
bom = frappe.new_doc('BOM')
```

### Step 4: Assign bom.item = item_code

```python
bom.item = item_code
```

### Step 5: Call bom.append()

```python
bom.append('items', frappe._dict(item_code=item_code))
```

### Step 6: Call bom.save()

```python
bom.save()
```

### Step 7: Assign unknown.bom_no = value

```python
bom.items[0].bom_no = bom.name
```

### Step 8: Call bom.save()

```python
bom.save()
```


## Complete Example

```python
# Workflow
'BOM should not allow BOM item again in child'
item_code = make_item(properties={'is_stock_item': 1}).name
bom = frappe.new_doc('BOM')
bom.item = item_code
bom.append('items', frappe._dict(item_code=item_code))
bom.save()
with self.assertRaises(BOMRecursionError):
    bom.items[0].bom_no = bom.name
    bom.save()
```

## Next Steps


---

*Source: test_bom.py:388 | Complexity: Advanced | Last updated: 2026-02-04*