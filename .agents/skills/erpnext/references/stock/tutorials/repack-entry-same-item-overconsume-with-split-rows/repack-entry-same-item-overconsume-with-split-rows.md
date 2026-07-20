# How To: Repack Entry Same Item Overconsume With Split Rows

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Over consume item and have less repacked item qty (same warehouse).
Ledger:
Item    | Qty  | Voucher
------------------------
Item 1  | 20   | 001
Item 1  | -50  | 002 (repack)
Item 1  | -50  | 002 (repack)
Item 1  | 50   | 002 (repack)

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `frappe`
- `frappe.tests`
- `erpnext.stock.report.stock_ageing.stock_ageing`

**Setup Required:**
```python
self.filters = frappe._dict(company='_Test Company', to_date='2021-12-10', ranges=['30', '60', '90'])
```

## Step-by-Step Guide

### Step 1: '\n\t\tOver consume item and have less repacked item qty (same warehouse).\n\t\tLedger:\n\t\tItem\t| Qty  | Voucher\n\t\t------------------------\n\t\tItem 1  | 20   | 001\n\t\tItem 1  | -50  | 002 (repack)\n\t\tItem 1  | -50  | 002 (repack)\n\t\tItem 1  | 50   | 002 (repack)\n\t\t'

```python
'\n\t\tOver consume item and have less repacked item qty (same warehouse).\n\t\tLedger:\n\t\tItem\t| Qty  | Voucher\n\t\t------------------------\n\t\tItem 1  | 20   | 001\n\t\tItem 1  | -50  | 002 (repack)\n\t\tItem 1  | -50  | 002 (repack)\n\t\tItem 1  | 50   | 002 (repack)\n\t\t'
```

### Step 2: Assign sle = value

```python
sle = [frappe._dict(name='Flask Item', actual_qty=20, qty_after_transaction=20, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-03', voucher_type='Stock Entry', voucher_no='001', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=-50, qty_after_transaction=-30, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-04', voucher_type='Stock Entry', voucher_no='002', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=-50, qty_after_transaction=-80, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-04', voucher_type='Stock Entry', voucher_no='002', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=50, qty_after_transaction=-30, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-04', voucher_type='Stock Entry', voucher_no='002', has_serial_no=False, serial_no=None)]
```

### Step 3: Assign fifo_slots = FIFOSlots(...)

```python
fifo_slots = FIFOSlots(self.filters, sle)
```

### Step 4: Assign slots = fifo_slots.generate(...)

```python
slots = fifo_slots.generate()
```

### Step 5: Assign item_result = value

```python
item_result = slots['Flask Item']
```

### Step 6: Assign queue = value

```python
queue = item_result['fifo_queue']
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(item_result['total_qty'], -30.0)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(queue[0][0], -30.0)
```

### Step 9: Assign transfer_bucket = value

```python
transfer_bucket = fifo_slots.transferred_item_details['002', 'Flask Item', 'WH 1']
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(transfer_bucket[0][0], 50)
```


## Complete Example

```python
# Setup
self.filters = frappe._dict(company='_Test Company', to_date='2021-12-10', ranges=['30', '60', '90'])

# Workflow
'\n\t\tOver consume item and have less repacked item qty (same warehouse).\n\t\tLedger:\n\t\tItem\t| Qty  | Voucher\n\t\t------------------------\n\t\tItem 1  | 20   | 001\n\t\tItem 1  | -50  | 002 (repack)\n\t\tItem 1  | -50  | 002 (repack)\n\t\tItem 1  | 50   | 002 (repack)\n\t\t'
sle = [frappe._dict(name='Flask Item', actual_qty=20, qty_after_transaction=20, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-03', voucher_type='Stock Entry', voucher_no='001', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=-50, qty_after_transaction=-30, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-04', voucher_type='Stock Entry', voucher_no='002', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=-50, qty_after_transaction=-80, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-04', voucher_type='Stock Entry', voucher_no='002', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=50, qty_after_transaction=-30, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-04', voucher_type='Stock Entry', voucher_no='002', has_serial_no=False, serial_no=None)]
fifo_slots = FIFOSlots(self.filters, sle)
slots = fifo_slots.generate()
item_result = slots['Flask Item']
queue = item_result['fifo_queue']
self.assertEqual(item_result['total_qty'], -30.0)
self.assertEqual(queue[0][0], -30.0)
transfer_bucket = fifo_slots.transferred_item_details['002', 'Flask Item', 'WH 1']
self.assertEqual(transfer_bucket[0][0], 50)
```

## Next Steps


---

*Source: test_stock_ageing.py:438 | Complexity: Advanced | Last updated: 2026-02-04*