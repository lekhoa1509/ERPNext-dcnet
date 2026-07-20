# How To: Default Bom

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test default bom

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

### Step 1: Assign bom = frappe.get_doc(...)

```python
bom = frappe.get_doc('BOM', {'item': '_Test FG Item 2', 'is_default': 1})
```

### Step 2: Call self.assertEqual()

```python
self.assertEqual(_get_default_bom_in_item(), bom.name)
```

### Step 3: Assign bom.is_active = 0

```python
bom.is_active = 0
```

### Step 4: Call bom.save()

```python
bom.save()
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(_get_default_bom_in_item(), '')
```

### Step 6: Assign bom.is_active = 1

```python
bom.is_active = 1
```

### Step 7: Assign bom.is_default = 1

```python
bom.is_default = 1
```

### Step 8: Call bom.save()

```python
bom.save()
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue(_get_default_bom_in_item(), bom.name)
```


## Complete Example

```python
# Workflow
def _get_default_bom_in_item():
    return cstr(frappe.db.get_value('Item', '_Test FG Item 2', 'default_bom'))
bom = frappe.get_doc('BOM', {'item': '_Test FG Item 2', 'is_default': 1})
self.assertEqual(_get_default_bom_in_item(), bom.name)
bom.is_active = 0
bom.save()
self.assertEqual(_get_default_bom_in_item(), '')
bom.is_active = 1
bom.is_default = 1
bom.save()
self.assertTrue(_get_default_bom_in_item(), bom.name)
```

## Next Steps


---

*Source: test_bom.py:59 | Complexity: Advanced | Last updated: 2026-02-04*