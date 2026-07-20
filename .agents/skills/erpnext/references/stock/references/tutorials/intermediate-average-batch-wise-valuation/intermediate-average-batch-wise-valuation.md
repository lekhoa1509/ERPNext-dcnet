# How To: Intermediate Average Batch Wise Valuation

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: A batch has moving average up until posting time,
check if same is respected when backdated entry is inserted in middle

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

### Step 1: 'A batch has moving average up until posting time,\n\t\tcheck if same is respected when backdated entry is inserted in middle'

```python
'A batch has moving average up until posting time,\n\t\tcheck if same is respected when backdated entry is inserted in middle'
```

### Step 2: Assign unknown = setup_item_valuation_test(...)

```python
item_code, warehouses, batches = setup_item_valuation_test()
```

### Step 3: Assign warehouse = value

```python
warehouse = warehouses[0]
```

### Step 4: Assign batch = value

```python
batch = batches[0]
```

### Step 5: Assign yesterday = make_stock_entry(...)

```python
yesterday = make_stock_entry(item_code=item_code, target=warehouse, batch_no=batch, qty=1, rate=10, posting_date=add_days(today(), -1))
```

### Step 6: Call self.assertSLEs()

```python
self.assertSLEs(yesterday, [{'actual_qty': 1, 'stock_value_difference': 10}])
```

### Step 7: Assign tomorrow = make_stock_entry(...)

```python
tomorrow = make_stock_entry(item_code=item_code, target=warehouse, batch_no=batches[0], qty=1, rate=30, posting_date=add_days(today(), 1))
```

### Step 8: Call self.assertSLEs()

```python
self.assertSLEs(tomorrow, [{'actual_qty': 1, 'stock_value_difference': 30}])
```

### Step 9: Assign create_today = make_stock_entry(...)

```python
create_today = make_stock_entry(item_code=item_code, target=warehouse, batch_no=batches[0], qty=1, rate=20)
```

### Step 10: Call self.assertSLEs()

```python
self.assertSLEs(create_today, [{'actual_qty': 1, 'stock_value_difference': 20}])
```

### Step 11: Assign consume_today = make_stock_entry(...)

```python
consume_today = make_stock_entry(item_code=item_code, source=warehouse, batch_no=batches[0], qty=1)
```

### Step 12: Call self.assertSLEs()

```python
self.assertSLEs(consume_today, [{'actual_qty': -1, 'stock_value_difference': -15}])
```

### Step 13: Assign consume_tomorrow = make_stock_entry(...)

```python
consume_tomorrow = make_stock_entry(item_code=item_code, source=warehouse, batch_no=batches[0], qty=2, posting_date=add_days(today(), 2))
```

### Step 14: Call self.assertSLEs()

```python
self.assertSLEs(consume_tomorrow, [{'stock_value_difference': -(30 + 15), 'stock_value': 0, 'qty_after_transaction': 0}])
```


## Complete Example

```python
# Setup
items = create_items()
reset('Stock Entry')
frappe.db.sql('delete from `tabStock Ledger Entry` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)
frappe.db.sql('delete from `tabBin` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)

# Workflow
'A batch has moving average up until posting time,\n\t\tcheck if same is respected when backdated entry is inserted in middle'
item_code, warehouses, batches = setup_item_valuation_test()
warehouse = warehouses[0]
batch = batches[0]
yesterday = make_stock_entry(item_code=item_code, target=warehouse, batch_no=batch, qty=1, rate=10, posting_date=add_days(today(), -1))
self.assertSLEs(yesterday, [{'actual_qty': 1, 'stock_value_difference': 10}])
tomorrow = make_stock_entry(item_code=item_code, target=warehouse, batch_no=batches[0], qty=1, rate=30, posting_date=add_days(today(), 1))
self.assertSLEs(tomorrow, [{'actual_qty': 1, 'stock_value_difference': 30}])
create_today = make_stock_entry(item_code=item_code, target=warehouse, batch_no=batches[0], qty=1, rate=20)
self.assertSLEs(create_today, [{'actual_qty': 1, 'stock_value_difference': 20}])
consume_today = make_stock_entry(item_code=item_code, source=warehouse, batch_no=batches[0], qty=1)
self.assertSLEs(consume_today, [{'actual_qty': -1, 'stock_value_difference': -15}])
consume_tomorrow = make_stock_entry(item_code=item_code, source=warehouse, batch_no=batches[0], qty=2, posting_date=add_days(today(), 2))
self.assertSLEs(consume_tomorrow, [{'stock_value_difference': -(30 + 15), 'stock_value': 0, 'qty_after_transaction': 0}])
```

## Next Steps


---

*Source: test_stock_ledger_entry.py:678 | Complexity: Advanced | Last updated: 2026-02-04*