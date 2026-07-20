# How To: Job Card Excess Material Transfer Block

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test job card excess material transfer block

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

### Step 1: Assign self.transfer_material_against = 'Job Card'

```python
self.transfer_material_against = 'Job Card'
```

### Step 2: Assign self.source_warehouse = 'Stores - _TC'

```python
self.source_warehouse = 'Stores - _TC'
```

### Step 3: Call self.generate_required_stock()

```python
self.generate_required_stock(self.work_order)
```

### Step 4: Assign job_card_name = frappe.db.get_value(...)

```python
job_card_name = frappe.db.get_value('Job Card', {'work_order': self.work_order.name})
```

### Step 5: Assign transfer_entry_1 = make_stock_entry_from_jc(...)

```python
transfer_entry_1 = make_stock_entry_from_jc(job_card_name)
```

### Step 6: Call transfer_entry_1.insert()

```python
transfer_entry_1.insert()
```

### Step 7: Call transfer_entry_1.submit()

```python
transfer_entry_1.submit()
```

### Step 8: Assign transfer_entry_2 = make_stock_entry_from_jc(...)

```python
transfer_entry_2 = make_stock_entry_from_jc(job_card_name)
```

### Step 9: Assign transfer_entry_2.fg_completed_qty = 1

```python
transfer_entry_2.fg_completed_qty = 1
```

### Step 10: Assign unknown.qty = 5

```python
transfer_entry_2.items[0].qty = 5
```

### Step 11: Assign unknown.qty = 3

```python
transfer_entry_2.items[1].qty = 3
```

### Step 12: Call transfer_entry_2.insert()

```python
transfer_entry_2.insert()
```

### Step 13: Call self.assertRaises()

```python
self.assertRaises(JobCardOverTransferError, transfer_entry_2.submit)
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
self.transfer_material_against = 'Job Card'
self.source_warehouse = 'Stores - _TC'
self.generate_required_stock(self.work_order)
job_card_name = frappe.db.get_value('Job Card', {'work_order': self.work_order.name})
transfer_entry_1 = make_stock_entry_from_jc(job_card_name)
transfer_entry_1.insert()
transfer_entry_1.submit()
transfer_entry_2 = make_stock_entry_from_jc(job_card_name)
transfer_entry_2.fg_completed_qty = 1
transfer_entry_2.items[0].qty = 5
transfer_entry_2.items[1].qty = 3
transfer_entry_2.insert()
self.assertRaises(JobCardOverTransferError, transfer_entry_2.submit)
```

## Next Steps


---

*Source: test_job_card.py:268 | Complexity: Advanced | Last updated: 2026-02-04*