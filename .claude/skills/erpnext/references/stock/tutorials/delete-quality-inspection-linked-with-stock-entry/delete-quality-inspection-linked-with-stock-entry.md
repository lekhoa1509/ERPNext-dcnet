# How To: Delete Quality Inspection Linked With Stock Entry

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test delete quality inspection linked with stock entry

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

### Step 1: Assign item_code = value

```python
item_code = create_item('_Test Cicuular Dependecy Item with QA').name
```

### Step 2: Assign se = make_stock_entry(...)

```python
se = make_stock_entry(item_code=item_code, target='_Test Warehouse - _TC', qty=1, basic_rate=100, do_not_submit=True)
```

### Step 3: Assign se.inspection_required = 1

```python
se.inspection_required = 1
```

### Step 4: Call se.save()

```python
se.save()
```

### Step 5: Assign qa = create_quality_inspection(...)

```python
qa = create_quality_inspection(item_code=item_code, reference_type='Stock Entry', reference_name=se.name, do_not_submit=True)
```

### Step 6: Call se.reload()

```python
se.reload()
```

### Step 7: Assign unknown.quality_inspection = value

```python
se.items[0].quality_inspection = qa.name
```

### Step 8: Call se.save()

```python
se.save()
```

### Step 9: Call qa.delete()

```python
qa.delete()
```

### Step 10: Call se.reload()

```python
se.reload()
```

### Step 11: Assign qc = value

```python
qc = se.items[0].quality_inspection
```

### Step 12: Call self.assertFalse()

```python
self.assertFalse(qc)
```

### Step 13: Call se.delete()

```python
se.delete()
```


## Complete Example

```python
# Workflow
item_code = create_item('_Test Cicuular Dependecy Item with QA').name
se = make_stock_entry(item_code=item_code, target='_Test Warehouse - _TC', qty=1, basic_rate=100, do_not_submit=True)
se.inspection_required = 1
se.save()
qa = create_quality_inspection(item_code=item_code, reference_type='Stock Entry', reference_name=se.name, do_not_submit=True)
se.reload()
se.items[0].quality_inspection = qa.name
se.save()
qa.delete()
se.reload()
qc = se.items[0].quality_inspection
self.assertFalse(qc)
se.delete()
```

## Next Steps


---

*Source: test_quality_inspection.py:253 | Complexity: Advanced | Last updated: 2026-02-04*