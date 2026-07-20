# How To: Job Card Partial Material Transfer

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test partial material transfer against Job Card

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `typing`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `frappe.utils.data`
- `erpnext.manufacturing.doctype.job_card.job_card`
- `erpnext.manufacturing.doctype.job_card.job_card`
- `erpnext.manufacturing.doctype.work_order.test_work_order`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.manufacturing.doctype.workstation.test_workstation`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.tests.utils`
- `erpnext.manufacturing.doctype.operation.test_operation`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.stock.doctype.material_request.material_request`
- `erpnext.manufacturing.doctype.routing.test_routing`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.manufacturing.doctype.routing.test_routing`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.warehouse.test_warehouse`

**Setup Required:**
```python
self.make_employees()
self.make_bom_for_jc_tests()
self.transfer_material_against: Literal['Work Order', 'Job Card'] = 'Work Order'
self.source_warehouse = None
self._work_order = None
```

## Step-by-Step Guide

### Step 1: 'Test partial material transfer against Job Card'

```python
'Test partial material transfer against Job Card'
```

### Step 2: Assign self.transfer_material_against = 'Job Card'

```python
self.transfer_material_against = 'Job Card'
```

### Step 3: Assign self.source_warehouse = 'Stores - _TC'

```python
self.source_warehouse = 'Stores - _TC'
```

### Step 4: Call self.generate_required_stock()

```python
self.generate_required_stock(self.work_order)
```

### Step 5: Assign job_card = frappe.get_last_doc(...)

```python
job_card = frappe.get_last_doc('Job Card', {'work_order': self.work_order.name})
```

### Step 6: Assign transfer_entry = make_stock_entry_from_jc(...)

```python
transfer_entry = make_stock_entry_from_jc(job_card.name)
```

### Step 7: Assign transfer_entry.fg_completed_qty = 1

```python
transfer_entry.fg_completed_qty = 1
```

### Step 8: Call transfer_entry.get_items()

```python
transfer_entry.get_items()
```

### Step 9: Call transfer_entry.insert()

```python
transfer_entry.insert()
```

### Step 10: Call transfer_entry.submit()

```python
transfer_entry.submit()
```

### Step 11: Call job_card.reload()

```python
job_card.reload()
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(job_card.transferred_qty, 1)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(transfer_entry.items[0].qty, 5)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(transfer_entry.items[1].qty, 3)
```

### Step 15: Assign transfer_entry_2 = make_stock_entry_from_jc(...)

```python
transfer_entry_2 = make_stock_entry_from_jc(job_card.name)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(transfer_entry_2.fg_completed_qty, 1)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(transfer_entry_2.items[0].qty, 5)
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(transfer_entry_2.items[1].qty, 3)
```

### Step 19: Call transfer_entry_2.insert()

```python
transfer_entry_2.insert()
```

### Step 20: Call transfer_entry_2.submit()

```python
transfer_entry_2.submit()
```

### Step 21: Call job_card.reload()

```python
job_card.reload()
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(job_card.transferred_qty, 2)
```

### Step 23: Call transfer_entry_2.cancel()

```python
transfer_entry_2.cancel()
```

### Step 24: Call transfer_entry.cancel()

```python
transfer_entry.cancel()
```

### Step 25: Call job_card.reload()

```python
job_card.reload()
```

### Step 26: Call self.assertEqual()

```python
self.assertEqual(job_card.transferred_qty, 0.0)
```


## Complete Example

```python
# Setup
self.make_employees()
self.make_bom_for_jc_tests()
self.transfer_material_against: Literal['Work Order', 'Job Card'] = 'Work Order'
self.source_warehouse = None
self._work_order = None

# Workflow
'Test partial material transfer against Job Card'
self.transfer_material_against = 'Job Card'
self.source_warehouse = 'Stores - _TC'
self.generate_required_stock(self.work_order)
job_card = frappe.get_last_doc('Job Card', {'work_order': self.work_order.name})
transfer_entry = make_stock_entry_from_jc(job_card.name)
transfer_entry.fg_completed_qty = 1
transfer_entry.get_items()
transfer_entry.insert()
transfer_entry.submit()
job_card.reload()
self.assertEqual(job_card.transferred_qty, 1)
self.assertEqual(transfer_entry.items[0].qty, 5)
self.assertEqual(transfer_entry.items[1].qty, 3)
transfer_entry_2 = make_stock_entry_from_jc(job_card.name)
self.assertEqual(transfer_entry_2.fg_completed_qty, 1)
self.assertEqual(transfer_entry_2.items[0].qty, 5)
self.assertEqual(transfer_entry_2.items[1].qty, 3)
transfer_entry_2.insert()
transfer_entry_2.submit()
job_card.reload()
self.assertEqual(job_card.transferred_qty, 2)
transfer_entry_2.cancel()
transfer_entry.cancel()
job_card.reload()
self.assertEqual(job_card.transferred_qty, 0.0)
```

## Next Steps


---

*Source: test_job_card.py:325 | Complexity: Advanced | Last updated: 2026-02-04*