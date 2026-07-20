# How To: Job Card

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test job card

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `collections`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.manufacturing.doctype.job_card.job_card`
- `erpnext.manufacturing.doctype.job_card.job_card`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.serial_no.serial_no`
- `erpnext.stock.doctype.stock_entry`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.utils`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.manufacturing.doctype.operation.test_operation`
- `erpnext.manufacturing.doctype.workstation.test_workstation`
- `erpnext.manufacturing.doctype.workstation_type.test_workstation_type`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.manufacturing.doctype.routing.test_routing`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`

**Setup Required:**
```python
self.warehouse = '_Test Warehouse 2 - _TC'
self.item = '_Test Item'
prepare_data_for_backflush_based_on_materials_transferred()
```

## Step-by-Step Guide

### Step 1: Assign stock_entries = value

```python
stock_entries = []
```

### Step 2: Assign bom = frappe.get_doc(...)

```python
bom = frappe.get_doc('BOM', {'docstatus': 1, 'with_operations': 1, 'company': '_Test Company'})
```

### Step 3: Assign work_order = make_wo_order_test_record(...)

```python
work_order = make_wo_order_test_record(item=bom.item, qty=1, bom_no=bom.name, source_warehouse='_Test Warehouse - _TC')
```

### Step 4: Assign ste = frappe.get_doc(...)

```python
ste = frappe.get_doc(make_stock_entry(work_order.name, 'Material Transfer for Manufacture', 1))
```

### Step 5: Call ste.submit()

```python
ste.submit()
```

### Step 6: Call stock_entries.append()

```python
stock_entries.append(ste)
```

### Step 7: Assign job_cards = frappe.get_all(...)

```python
job_cards = frappe.get_all('Job Card', filters={'work_order': work_order.name}, order_by='creation asc')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(len(job_cards), len(bom.operations))
```

### Step 9: Assign ste1 = frappe.get_doc(...)

```python
ste1 = frappe.get_doc(make_stock_entry(work_order.name, 'Manufacture', 1))
```

### Step 10: Call ste1.submit()

```python
ste1.submit()
```

### Step 11: Call stock_entries.append()

```python
stock_entries.append(ste1)
```

### Step 12: Call stock_entries.reverse()

```python
stock_entries.reverse()
```

### Step 13: Assign stock_entry_doc = test_stock_entry.make_stock_entry(...)

```python
stock_entry_doc = test_stock_entry.make_stock_entry(item_code=row.item_code, target='_Test Warehouse - _TC', qty=row.required_qty, basic_rate=100)
```

### Step 14: Call stock_entries.append()

```python
stock_entries.append(stock_entry_doc)
```

### Step 15: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc('Job Card', job_card)
```

### Step 16: Assign unknown.completed_qty = 1

```python
doc.time_logs[0].completed_qty = 1
```

### Step 17: Call doc.submit()

```python
doc.submit()
```

### Step 18: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc('Job Card', job_card)
```

### Step 19: Call self.assertRaises()

```python
self.assertRaises(JobCardCancelError, doc.cancel)
```

### Step 20: Call stock_entry.cancel()

```python
stock_entry.cancel()
```

### Step 21: Call doc.append()

```python
doc.append('time_logs', {'from_time': row.from_time, 'to_time': row.to_time, 'time_in_mins': row.time_in_mins, 'completed_qty': 0})
```


## Complete Example

```python
# Setup
self.warehouse = '_Test Warehouse 2 - _TC'
self.item = '_Test Item'
prepare_data_for_backflush_based_on_materials_transferred()

# Workflow
stock_entries = []
bom = frappe.get_doc('BOM', {'docstatus': 1, 'with_operations': 1, 'company': '_Test Company'})
work_order = make_wo_order_test_record(item=bom.item, qty=1, bom_no=bom.name, source_warehouse='_Test Warehouse - _TC')
for row in work_order.required_items:
    stock_entry_doc = test_stock_entry.make_stock_entry(item_code=row.item_code, target='_Test Warehouse - _TC', qty=row.required_qty, basic_rate=100)
    stock_entries.append(stock_entry_doc)
ste = frappe.get_doc(make_stock_entry(work_order.name, 'Material Transfer for Manufacture', 1))
ste.submit()
stock_entries.append(ste)
job_cards = frappe.get_all('Job Card', filters={'work_order': work_order.name}, order_by='creation asc')
self.assertEqual(len(job_cards), len(bom.operations))
for _i, job_card in enumerate(job_cards):
    doc = frappe.get_doc('Job Card', job_card)
    for row in doc.scheduled_time_logs:
        doc.append('time_logs', {'from_time': row.from_time, 'to_time': row.to_time, 'time_in_mins': row.time_in_mins, 'completed_qty': 0})
    doc.time_logs[0].completed_qty = 1
    doc.submit()
ste1 = frappe.get_doc(make_stock_entry(work_order.name, 'Manufacture', 1))
ste1.submit()
stock_entries.append(ste1)
for job_card in job_cards:
    doc = frappe.get_doc('Job Card', job_card)
    self.assertRaises(JobCardCancelError, doc.cancel)
stock_entries.reverse()
for stock_entry in stock_entries:
    stock_entry.cancel()
```

## Next Steps


---

*Source: test_work_order.py:462 | Complexity: Advanced | Last updated: 2026-02-04*