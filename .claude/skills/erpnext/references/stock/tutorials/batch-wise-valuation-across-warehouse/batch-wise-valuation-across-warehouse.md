# How To: Batch Wise Valuation Across Warehouse

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test batch wise valuation across warehouse

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `json`
- `time`
- `uuid`
- `frappe`
- `frappe.core.page.permission_manager.permission_manager`
- `frappe.custom.doctype.property_setter.property_setter`
- `frappe.query_builder.functions`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.gl_entry.gl_entry`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.landed_cost_voucher.test_landed_cost_voucher`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.doctype.stock_ledger_entry.stock_ledger_entry`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.stock.stock_ledger`
- `erpnext.stock.tests.test_utils`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.stock.doctype.repost_item_valuation.repost_item_valuation`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.utils`
- `erpnext.stock.doctype.item.test_item`

**Setup Required:**
```python
items = create_items()
reset('Stock Entry')
frappe.db.sql('delete from `tabStock Ledger Entry` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)
frappe.db.sql('delete from `tabBin` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)
```

## Step-by-Step Guide

### Step 1: Assign unknown = setup_item_valuation_test(...)

```python
item_code, warehouses, batches = setup_item_valuation_test()
```

### Step 2: Assign source = value

```python
source = warehouses[0]
```

### Step 3: Assign target = value

```python
target = warehouses[1]
```

### Step 4: Assign unrelated_batch = make_stock_entry(...)

```python
unrelated_batch = make_stock_entry(item_code=item_code, target=source, batch_no=batches[1], qty=5, rate=10)
```

### Step 5: Call self.assertSLEs()

```python
self.assertSLEs(unrelated_batch, [{'actual_qty': 5, 'stock_value_difference': 10 * 5}])
```

### Step 6: Assign reciept = make_stock_entry(...)

```python
reciept = make_stock_entry(item_code=item_code, target=source, batch_no=batches[0], qty=5, rate=10)
```

### Step 7: Call self.assertSLEs()

```python
self.assertSLEs(reciept, [{'actual_qty': 5, 'stock_value_difference': 10 * 5}])
```

### Step 8: Assign transfer = make_stock_entry(...)

```python
transfer = make_stock_entry(item_code=item_code, source=source, target=target, batch_no=batches[0], qty=5)
```

### Step 9: Call self.assertSLEs()

```python
self.assertSLEs(transfer, [{'actual_qty': -5, 'stock_value_difference': -10 * 5, 'warehouse': source}, {'actual_qty': 5, 'stock_value_difference': 10 * 5, 'warehouse': target}])
```

### Step 10: Assign backdated_receipt = make_stock_entry(...)

```python
backdated_receipt = make_stock_entry(item_code=item_code, target=source, batch_no=batches[0], qty=5, rate=20, posting_date=add_days(today(), -1))
```

### Step 11: Call self.assertSLEs()

```python
self.assertSLEs(backdated_receipt, [{'actual_qty': 5, 'stock_value_difference': 20 * 5}])
```

### Step 12: Call self.assertSLEs()

```python
self.assertSLEs(transfer, [{'actual_qty': -5, 'stock_value_difference': -15 * 5, 'warehouse': source, 'stock_value': 15 * 5 + 10 * 5}, {'actual_qty': 5, 'stock_value_difference': 15 * 5, 'warehouse': target, 'stock_value': 15 * 5}])
```

### Step 13: Assign transfer_unrelated = make_stock_entry(...)

```python
transfer_unrelated = make_stock_entry(item_code=item_code, source=source, target=target, batch_no=batches[1], qty=5)
```

### Step 14: Call self.assertSLEs()

```python
self.assertSLEs(transfer_unrelated, [{'actual_qty': -5, 'stock_value_difference': -10 * 5, 'warehouse': source, 'stock_value': 15 * 5}, {'actual_qty': 5, 'stock_value_difference': 10 * 5, 'warehouse': target, 'stock_value': 15 * 5 + 10 * 5}])
```


## Complete Example

```python
# Setup
items = create_items()
reset('Stock Entry')
frappe.db.sql('delete from `tabStock Ledger Entry` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)
frappe.db.sql('delete from `tabBin` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)

# Workflow
item_code, warehouses, batches = setup_item_valuation_test()
source = warehouses[0]
target = warehouses[1]
unrelated_batch = make_stock_entry(item_code=item_code, target=source, batch_no=batches[1], qty=5, rate=10)
self.assertSLEs(unrelated_batch, [{'actual_qty': 5, 'stock_value_difference': 10 * 5}])
reciept = make_stock_entry(item_code=item_code, target=source, batch_no=batches[0], qty=5, rate=10)
self.assertSLEs(reciept, [{'actual_qty': 5, 'stock_value_difference': 10 * 5}])
transfer = make_stock_entry(item_code=item_code, source=source, target=target, batch_no=batches[0], qty=5)
self.assertSLEs(transfer, [{'actual_qty': -5, 'stock_value_difference': -10 * 5, 'warehouse': source}, {'actual_qty': 5, 'stock_value_difference': 10 * 5, 'warehouse': target}])
backdated_receipt = make_stock_entry(item_code=item_code, target=source, batch_no=batches[0], qty=5, rate=20, posting_date=add_days(today(), -1))
self.assertSLEs(backdated_receipt, [{'actual_qty': 5, 'stock_value_difference': 20 * 5}])
self.assertSLEs(transfer, [{'actual_qty': -5, 'stock_value_difference': -15 * 5, 'warehouse': source, 'stock_value': 15 * 5 + 10 * 5}, {'actual_qty': 5, 'stock_value_difference': 15 * 5, 'warehouse': target, 'stock_value': 15 * 5}])
transfer_unrelated = make_stock_entry(item_code=item_code, source=source, target=target, batch_no=batches[1], qty=5)
self.assertSLEs(transfer_unrelated, [{'actual_qty': -5, 'stock_value_difference': -10 * 5, 'warehouse': source, 'stock_value': 15 * 5}, {'actual_qty': 5, 'stock_value_difference': 10 * 5, 'warehouse': target, 'stock_value': 15 * 5 + 10 * 5}])
```

## Next Steps


---

*Source: test_stock_ledger_entry.py:589 | Complexity: Advanced | Last updated: 2026-02-04*