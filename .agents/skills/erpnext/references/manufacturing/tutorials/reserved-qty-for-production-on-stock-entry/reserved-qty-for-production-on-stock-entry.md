# How To: Reserved Qty For Production On Stock Entry

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test reserved qty for production on stock entry

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

### Step 1: Call test_stock_entry.make_stock_entry()

```python
test_stock_entry.make_stock_entry(item_code='_Test Item', target=self.warehouse, qty=100, basic_rate=100)
```

### Step 2: Call test_stock_entry.make_stock_entry()

```python
test_stock_entry.make_stock_entry(item_code='_Test Item Home Desktop 100', target=self.warehouse, qty=100, basic_rate=100)
```

### Step 3: Call self.test_reserved_qty_for_production_submit()

```python
self.test_reserved_qty_for_production_submit()
```

### Step 4: Assign s = frappe.get_doc(...)

```python
s = frappe.get_doc(make_stock_entry(self.wo_order.name, 'Material Transfer for Manufacture', 2))
```

### Step 5: Call s.submit()

```python
s.submit()
```

### Step 6: Assign bin1_on_start_production = get_bin(...)

```python
bin1_on_start_production = get_bin(self.item, self.warehouse)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(cint(self.bin1_at_start.reserved_qty_for_production), cint(bin1_on_start_production.reserved_qty_for_production))
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(cint(self.bin1_at_start.projected_qty), cint(bin1_on_start_production.projected_qty) + 2)
```

### Step 9: Assign s = frappe.get_doc(...)

```python
s = frappe.get_doc(make_stock_entry(self.wo_order.name, 'Manufacture', 2))
```

### Step 10: Assign bin1_on_end_production = get_bin(...)

```python
bin1_on_end_production = get_bin(self.item, self.warehouse)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(cint(bin1_on_end_production.reserved_qty_for_production), cint(bin1_on_start_production.reserved_qty_for_production))
```


## Complete Example

```python
# Setup
self.warehouse = '_Test Warehouse 2 - _TC'
self.item = '_Test Item'
prepare_data_for_backflush_based_on_materials_transferred()

# Workflow
test_stock_entry.make_stock_entry(item_code='_Test Item', target=self.warehouse, qty=100, basic_rate=100)
test_stock_entry.make_stock_entry(item_code='_Test Item Home Desktop 100', target=self.warehouse, qty=100, basic_rate=100)
self.test_reserved_qty_for_production_submit()
s = frappe.get_doc(make_stock_entry(self.wo_order.name, 'Material Transfer for Manufacture', 2))
s.submit()
bin1_on_start_production = get_bin(self.item, self.warehouse)
self.assertEqual(cint(self.bin1_at_start.reserved_qty_for_production), cint(bin1_on_start_production.reserved_qty_for_production))
self.assertEqual(cint(self.bin1_at_start.projected_qty), cint(bin1_on_start_production.projected_qty) + 2)
s = frappe.get_doc(make_stock_entry(self.wo_order.name, 'Manufacture', 2))
bin1_on_end_production = get_bin(self.item, self.warehouse)
self.assertEqual(cint(bin1_on_end_production.reserved_qty_for_production), cint(bin1_on_start_production.reserved_qty_for_production))
```

## Next Steps


---

*Source: test_work_order.py:200 | Complexity: Advanced | Last updated: 2026-02-04*