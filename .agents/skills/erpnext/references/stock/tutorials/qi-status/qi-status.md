# How To: Qi Status

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test qi status

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

### Step 1: Call make_stock_entry()

```python
make_stock_entry(item_code='_Test Item with QA', target='_Test Warehouse - _TC', qty=1, basic_rate=100)
```

### Step 2: Assign dn = create_delivery_note(...)

```python
dn = create_delivery_note(item_code='_Test Item with QA', do_not_submit=True)
```

### Step 3: Assign qa = create_quality_inspection(...)

```python
qa = create_quality_inspection(reference_type='Delivery Note', reference_name=dn.name, status='Accepted', do_not_save=True)
```

### Step 4: Assign unknown.manual_inspection = 1

```python
qa.readings[0].manual_inspection = 1
```

### Step 5: Call qa.save()

```python
qa.save()
```

### Step 6: Assign qa.status = 'Accepted'

```python
qa.status = 'Accepted'
```

### Step 7: Assign qa.manual_inspection = 0

```python
qa.manual_inspection = 0
```

### Step 8: Assign unknown.status = 'Rejected'

```python
qa.readings[0].status = 'Rejected'
```

### Step 9: Call qa.save()

```python
qa.save()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(qa.status, 'Rejected')
```

### Step 11: Assign qa.status = 'Rejected'

```python
qa.status = 'Rejected'
```

### Step 12: Assign qa.manual_inspection = 0

```python
qa.manual_inspection = 0
```

### Step 13: Assign unknown.status = 'Accepted'

```python
qa.readings[0].status = 'Accepted'
```

### Step 14: Call qa.save()

```python
qa.save()
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(qa.status, 'Accepted')
```

### Step 16: Assign qa.status = 'Accepted'

```python
qa.status = 'Accepted'
```

### Step 17: Assign qa.manual_inspection = 1

```python
qa.manual_inspection = 1
```

### Step 18: Assign unknown.status = 'Rejected'

```python
qa.readings[0].status = 'Rejected'
```

### Step 19: Call qa.save()

```python
qa.save()
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(qa.status, 'Accepted')
```


## Complete Example

```python
# Workflow
make_stock_entry(item_code='_Test Item with QA', target='_Test Warehouse - _TC', qty=1, basic_rate=100)
dn = create_delivery_note(item_code='_Test Item with QA', do_not_submit=True)
qa = create_quality_inspection(reference_type='Delivery Note', reference_name=dn.name, status='Accepted', do_not_save=True)
qa.readings[0].manual_inspection = 1
qa.save()
qa.status = 'Accepted'
qa.manual_inspection = 0
qa.readings[0].status = 'Rejected'
qa.save()
self.assertEqual(qa.status, 'Rejected')
qa.status = 'Rejected'
qa.manual_inspection = 0
qa.readings[0].status = 'Accepted'
qa.save()
self.assertEqual(qa.status, 'Accepted')
qa.status = 'Accepted'
qa.manual_inspection = 1
qa.readings[0].status = 'Rejected'
qa.save()
self.assertEqual(qa.status, 'Accepted')
```

## Next Steps


---

*Source: test_quality_inspection.py:187 | Complexity: Advanced | Last updated: 2026-02-04*