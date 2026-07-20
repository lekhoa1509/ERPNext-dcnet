# How To: Replace Bom

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test replace bom

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `erpnext.manufacturing.doctype.bom_update_log.test_bom_update_log`
- `erpnext.manufacturing.doctype.bom_update_tool.bom_update_tool`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`
- `erpnext.stock.doctype.item.test_item`


## Step-by-Step Guide

### Step 1: Assign current_bom = 'BOM-_Test Item Home Desktop Manufactured-001'

```python
current_bom = 'BOM-_Test Item Home Desktop Manufactured-001'
```

### Step 2: Assign bom_doc = frappe.copy_doc(...)

```python
bom_doc = frappe.copy_doc(self.globalTestRecords['BOM'][0])
```

### Step 3: Assign unknown.item_code = '_Test Item'

```python
bom_doc.items[1].item_code = '_Test Item'
```

### Step 4: Call bom_doc.insert()

```python
bom_doc.insert()
```

### Step 5: Assign boms = frappe._dict(...)

```python
boms = frappe._dict(current_bom=current_bom, new_bom=bom_doc.name)
```

### Step 6: Call enqueue_replace_bom()

```python
enqueue_replace_bom(boms=boms)
```

### Step 7: Call self.assertFalse()

```python
self.assertFalse(frappe.db.exists('BOM Item', {'bom_no': current_bom, 'docstatus': 1}))
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(frappe.db.exists('BOM Item', {'bom_no': bom_doc.name, 'docstatus': 1}))
```


## Complete Example

```python
# Workflow
current_bom = 'BOM-_Test Item Home Desktop Manufactured-001'
bom_doc = frappe.copy_doc(self.globalTestRecords['BOM'][0])
bom_doc.items[1].item_code = '_Test Item'
bom_doc.insert()
boms = frappe._dict(current_bom=current_bom, new_bom=bom_doc.name)
enqueue_replace_bom(boms=boms)
self.assertFalse(frappe.db.exists('BOM Item', {'bom_no': current_bom, 'docstatus': 1}))
self.assertTrue(frappe.db.exists('BOM Item', {'bom_no': bom_doc.name, 'docstatus': 1}))
```

## Next Steps


---

*Source: test_bom_update_tool.py:24 | Complexity: Advanced | Last updated: 2026-02-04*