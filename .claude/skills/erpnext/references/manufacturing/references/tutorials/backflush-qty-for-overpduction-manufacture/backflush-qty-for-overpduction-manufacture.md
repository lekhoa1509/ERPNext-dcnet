# How To: Backflush Qty For Overpduction Manufacture

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test backflush qty for overpduction manufacture

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

### Step 1: Assign cancel_stock_entry = value

```python
cancel_stock_entry = []
```

### Step 2: Call allow_overproduction()

```python
allow_overproduction('overproduction_percentage_for_work_order', 30)
```

### Step 3: Assign wo_order = make_wo_order_test_record(...)

```python
wo_order = make_wo_order_test_record(planned_start_date=now(), qty=100)
```

### Step 4: Assign ste1 = test_stock_entry.make_stock_entry(...)

```python
ste1 = test_stock_entry.make_stock_entry(item_code='_Test Item', target='_Test Warehouse - _TC', qty=120, basic_rate=5000.0)
```

### Step 5: Assign ste2 = test_stock_entry.make_stock_entry(...)

```python
ste2 = test_stock_entry.make_stock_entry(item_code='_Test Item Home Desktop 100', target='_Test Warehouse - _TC', qty=240, basic_rate=1000.0)
```

### Step 6: Call cancel_stock_entry.extend()

```python
cancel_stock_entry.extend([ste1.name, ste2.name])
```

### Step 7: Assign s = frappe.get_doc(...)

```python
s = frappe.get_doc(make_stock_entry(wo_order.name, 'Material Transfer for Manufacture', 60))
```

### Step 8: Call s.submit()

```python
s.submit()
```

### Step 9: Call cancel_stock_entry.append()

```python
cancel_stock_entry.append(s.name)
```

### Step 10: Assign s = frappe.get_doc(...)

```python
s = frappe.get_doc(make_stock_entry(wo_order.name, 'Manufacture', 60))
```

### Step 11: Call s.submit()

```python
s.submit()
```

### Step 12: Call cancel_stock_entry.append()

```python
cancel_stock_entry.append(s.name)
```

### Step 13: Assign s = frappe.get_doc(...)

```python
s = frappe.get_doc(make_stock_entry(wo_order.name, 'Material Transfer for Manufacture', 60))
```

### Step 14: Call s.submit()

```python
s.submit()
```

### Step 15: Call cancel_stock_entry.append()

```python
cancel_stock_entry.append(s.name)
```

### Step 16: Assign s1 = frappe.get_doc(...)

```python
s1 = frappe.get_doc(make_stock_entry(wo_order.name, 'Manufacture', 50))
```

### Step 17: Call s1.submit()

```python
s1.submit()
```

### Step 18: Call cancel_stock_entry.append()

```python
cancel_stock_entry.append(s1.name)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(s1.items[0].qty, 50)
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(s1.items[1].qty, 100)
```

### Step 21: Call cancel_stock_entry.reverse()

```python
cancel_stock_entry.reverse()
```

### Step 22: Call allow_overproduction()

```python
allow_overproduction('overproduction_percentage_for_work_order', 0)
```

### Step 23: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc('Stock Entry', ste)
```

### Step 24: Call doc.cancel()

```python
doc.cancel()
```


## Complete Example

```python
# Setup
self.warehouse = '_Test Warehouse 2 - _TC'
self.item = '_Test Item'
prepare_data_for_backflush_based_on_materials_transferred()

# Workflow
cancel_stock_entry = []
allow_overproduction('overproduction_percentage_for_work_order', 30)
wo_order = make_wo_order_test_record(planned_start_date=now(), qty=100)
ste1 = test_stock_entry.make_stock_entry(item_code='_Test Item', target='_Test Warehouse - _TC', qty=120, basic_rate=5000.0)
ste2 = test_stock_entry.make_stock_entry(item_code='_Test Item Home Desktop 100', target='_Test Warehouse - _TC', qty=240, basic_rate=1000.0)
cancel_stock_entry.extend([ste1.name, ste2.name])
s = frappe.get_doc(make_stock_entry(wo_order.name, 'Material Transfer for Manufacture', 60))
s.submit()
cancel_stock_entry.append(s.name)
s = frappe.get_doc(make_stock_entry(wo_order.name, 'Manufacture', 60))
s.submit()
cancel_stock_entry.append(s.name)
s = frappe.get_doc(make_stock_entry(wo_order.name, 'Material Transfer for Manufacture', 60))
s.submit()
cancel_stock_entry.append(s.name)
s1 = frappe.get_doc(make_stock_entry(wo_order.name, 'Manufacture', 50))
s1.submit()
cancel_stock_entry.append(s1.name)
self.assertEqual(s1.items[0].qty, 50)
self.assertEqual(s1.items[1].qty, 100)
cancel_stock_entry.reverse()
for ste in cancel_stock_entry:
    doc = frappe.get_doc('Stock Entry', ste)
    doc.cancel()
allow_overproduction('overproduction_percentage_for_work_order', 0)
```

## Next Steps


---

*Source: test_work_order.py:249 | Complexity: Advanced | Last updated: 2026-02-04*