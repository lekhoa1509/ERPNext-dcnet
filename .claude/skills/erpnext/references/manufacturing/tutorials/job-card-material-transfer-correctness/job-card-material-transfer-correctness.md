# How To: Job Card Material Transfer Correctness

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: 1. Test if only current Job Card Items are pulled in a Stock Entry against a Job Card
2. Test impact of changing 'For Qty' in such a Stock Entry

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

### Step 1: "\n\t\t1. Test if only current Job Card Items are pulled in a Stock Entry against a Job Card\n\t\t2. Test impact of changing 'For Qty' in such a Stock Entry\n\t\t"

```python
"\n\t\t1. Test if only current Job Card Items are pulled in a Stock Entry against a Job Card\n\t\t2. Test impact of changing 'For Qty' in such a Stock Entry\n\t\t"
```

### Step 2: Call create_bom_with_multiple_operations()

```python
create_bom_with_multiple_operations()
```

### Step 3: Assign work_order = make_wo_with_transfer_against_jc(...)

```python
work_order = make_wo_with_transfer_against_jc()
```

### Step 4: Assign job_card_name = frappe.db.get_value(...)

```python
job_card_name = frappe.db.get_value('Job Card', {'work_order': work_order.name, 'operation': 'Test Operation A'})
```

### Step 5: Assign job_card = frappe.get_doc(...)

```python
job_card = frappe.get_doc('Job Card', job_card_name)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(len(job_card.items), 1)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(job_card.items[0].item_code, '_Test Item')
```

### Step 8: Assign transfer_entry = make_stock_entry_from_jc(...)

```python
transfer_entry = make_stock_entry_from_jc(job_card_name)
```

### Step 9: Call transfer_entry.insert()

```python
transfer_entry.insert()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(len(transfer_entry.items), 1)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(transfer_entry.items[0].item_code, '_Test Item')
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(transfer_entry.items[0].qty, 4)
```

### Step 13: Assign transfer_entry.fg_completed_qty = 2

```python
transfer_entry.fg_completed_qty = 2
```

### Step 14: Call transfer_entry.get_items()

```python
transfer_entry.get_items()
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(len(transfer_entry.items), 1)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(transfer_entry.items[0].item_code, '_Test Item')
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(transfer_entry.items[0].qty, 2)
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
"\n\t\t1. Test if only current Job Card Items are pulled in a Stock Entry against a Job Card\n\t\t2. Test impact of changing 'For Qty' in such a Stock Entry\n\t\t"
create_bom_with_multiple_operations()
work_order = make_wo_with_transfer_against_jc()
job_card_name = frappe.db.get_value('Job Card', {'work_order': work_order.name, 'operation': 'Test Operation A'})
job_card = frappe.get_doc('Job Card', job_card_name)
self.assertEqual(len(job_card.items), 1)
self.assertEqual(job_card.items[0].item_code, '_Test Item')
transfer_entry = make_stock_entry_from_jc(job_card_name)
transfer_entry.insert()
self.assertEqual(len(transfer_entry.items), 1)
self.assertEqual(transfer_entry.items[0].item_code, '_Test Item')
self.assertEqual(transfer_entry.items[0].qty, 4)
transfer_entry.fg_completed_qty = 2
transfer_entry.get_items()
self.assertEqual(len(transfer_entry.items), 1)
self.assertEqual(transfer_entry.items[0].item_code, '_Test Item')
self.assertEqual(transfer_entry.items[0].qty, 2)
```

## Next Steps


---

*Source: test_job_card.py:365 | Complexity: Advanced | Last updated: 2026-02-04*