# How To: Work Order With Non Stock Item

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test work order with non stock item

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

### Step 1: Assign items = value

```python
items = {'Finished Good Test Item For non stock': 1, '_Test FG Item': 1, '_Test FG Non Stock Item': 0}
```

### Step 2: Assign fg_item = 'Finished Good Test Item For non stock'

```python
fg_item = 'Finished Good Test Item For non stock'
```

### Step 3: Call test_stock_entry.make_stock_entry()

```python
test_stock_entry.make_stock_entry(item_code='_Test FG Item', target='_Test Warehouse - _TC', qty=1, basic_rate=100)
```

### Step 4: Assign wo = make_wo_order_test_record(...)

```python
wo = make_wo_order_test_record(production_item=fg_item)
```

### Step 5: Assign se = frappe.get_doc(...)

```python
se = frappe.get_doc(make_stock_entry(wo.name, 'Material Transfer for Manufacture', 1))
```

### Step 6: Call se.insert()

```python
se.insert()
```

### Step 7: Call se.submit()

```python
se.submit()
```

### Step 8: Assign ste = frappe.get_doc(...)

```python
ste = frappe.get_doc(make_stock_entry(wo.name, 'Manufacture', 1))
```

### Step 9: Call ste.insert()

```python
ste.insert()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(len(ste.additional_costs), 1)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(ste.total_additional_costs, 1000)
```

### Step 12: Call make_item()

```python
make_item(item, {'is_stock_item': is_stock_item})
```

### Step 13: Call frappe.get_doc.insert()

```python
frappe.get_doc({'doctype': 'Item Price', 'item_code': '_Test FG Non Stock Item', 'price_list_rate': 1000, 'price_list': '_Test Price List India'}).insert(ignore_permissions=True)
```

### Step 14: Assign bom = make_bom(...)

```python
bom = make_bom(item=fg_item, rate=1000, raw_materials=['_Test FG Item', '_Test FG Non Stock Item'], do_not_save=True)
```

### Step 15: Assign bom.rm_cost_as_per = 'Price List'

```python
bom.rm_cost_as_per = 'Price List'
```

### Step 16: Assign bom.buying_price_list = '_Test Price List India'

```python
bom.buying_price_list = '_Test Price List India'
```

### Step 17: Assign bom.currency = 'INR'

```python
bom.currency = 'INR'
```

### Step 18: Call bom.save()

```python
bom.save()
```


## Complete Example

```python
# Setup
self.warehouse = '_Test Warehouse 2 - _TC'
self.item = '_Test Item'
prepare_data_for_backflush_based_on_materials_transferred()

# Workflow
items = {'Finished Good Test Item For non stock': 1, '_Test FG Item': 1, '_Test FG Non Stock Item': 0}
for item, is_stock_item in items.items():
    make_item(item, {'is_stock_item': is_stock_item})
if not frappe.db.get_value('Item Price', {'item_code': '_Test FG Non Stock Item'}):
    frappe.get_doc({'doctype': 'Item Price', 'item_code': '_Test FG Non Stock Item', 'price_list_rate': 1000, 'price_list': '_Test Price List India'}).insert(ignore_permissions=True)
fg_item = 'Finished Good Test Item For non stock'
test_stock_entry.make_stock_entry(item_code='_Test FG Item', target='_Test Warehouse - _TC', qty=1, basic_rate=100)
if not frappe.db.get_value('BOM', {'item': fg_item, 'docstatus': 1}):
    bom = make_bom(item=fg_item, rate=1000, raw_materials=['_Test FG Item', '_Test FG Non Stock Item'], do_not_save=True)
    bom.rm_cost_as_per = 'Price List'
    bom.buying_price_list = '_Test Price List India'
    bom.currency = 'INR'
    bom.save()
wo = make_wo_order_test_record(production_item=fg_item)
se = frappe.get_doc(make_stock_entry(wo.name, 'Material Transfer for Manufacture', 1))
se.insert()
se.submit()
ste = frappe.get_doc(make_stock_entry(wo.name, 'Manufacture', 1))
ste.insert()
self.assertEqual(len(ste.additional_costs), 1)
self.assertEqual(ste.total_additional_costs, 1000)
```

## Next Steps


---

*Source: test_work_order.py:414 | Complexity: Advanced | Last updated: 2026-02-04*