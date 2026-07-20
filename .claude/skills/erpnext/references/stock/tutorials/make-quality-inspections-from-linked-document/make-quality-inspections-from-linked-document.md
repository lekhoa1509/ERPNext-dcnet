# How To: Make Quality Inspections From Linked Document

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test make quality inspections from linked document

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.controllers.stock_controller`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`


## Step-by-Step Guide

### Step 1: Assign dn = create_delivery_note(...)

```python
dn = create_delivery_note(item_code='_Test Item with QA', do_not_submit=True)
```

### Step 2: Assign quality_inspections = make_quality_inspections(...)

```python
quality_inspections = make_quality_inspections(dn.doctype, dn.name, dn.items, inspection_type)
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(len(dn.items), len(quality_inspections))
```

### Step 4: Call dn.delete()

```python
dn.delete()
```

### Step 5: Assign inspection_type = 'Incoming'

```python
inspection_type = 'Incoming'
```

### Step 6: Assign inspection_type = 'Outgoing'

```python
inspection_type = 'Outgoing'
```

### Step 7: Assign item.sample_size = value

```python
item.sample_size = item.qty
```

### Step 8: Call frappe.delete_doc()

```python
frappe.delete_doc('Quality Inspection', qi)
```


## Complete Example

```python
# Workflow
dn = create_delivery_note(item_code='_Test Item with QA', do_not_submit=True)
if dn.doctype in ['Purchase Receipt', 'Purchase Invoice', 'Subcontracting Receipt']:
    inspection_type = 'Incoming'
else:
    inspection_type = 'Outgoing'
for item in dn.items:
    item.sample_size = item.qty
quality_inspections = make_quality_inspections(dn.doctype, dn.name, dn.items, inspection_type)
self.assertEqual(len(dn.items), len(quality_inspections))
for qi in quality_inspections:
    frappe.delete_doc('Quality Inspection', qi)
dn.delete()
```

## Next Steps


---

*Source: test_quality_inspection.py:137 | Complexity: Advanced | Last updated: 2026-02-04*