# How To: Repack Entry Same Item Overproduce

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Under consume item and have more repacked item qty (same warehouse).
Ledger:
Item    | Qty  | Voucher
------------------------
Item 1  | 500  | 001
Item 1  | -50  | 002 (repack)
Item 1  | 100  | 002 (repack)

Case most likely for batch items. Test time bucket computation.

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

### Step 1: '\n\t\tUnder consume item and have more repacked item qty (same warehouse).\n\t\tLedger:\n\t\tItem\t| Qty  | Voucher\n\t\t------------------------\n\t\tItem 1  | 500  | 001\n\t\tItem 1  | -50  | 002 (repack)\n\t\tItem 1  | 100  | 002 (repack)\n\n\t\tCase most likely for batch items. Test time bucket computation.\n\t\t'

```python
'\n\t\tUnder consume item and have more repacked item qty (same warehouse).\n\t\tLedger:\n\t\tItem\t| Qty  | Voucher\n\t\t------------------------\n\t\tItem 1  | 500  | 001\n\t\tItem 1  | -50  | 002 (repack)\n\t\tItem 1  | 100  | 002 (repack)\n\n\t\tCase most likely for batch items. Test time bucket computation.\n\t\t'
```

### Step 2: Assign sle = value

```python
sle = [frappe._dict(name='Flask Item', actual_qty=500, qty_after_transaction=500, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-03', voucher_type='Stock Entry', voucher_no='001', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=-50, qty_after_transaction=450, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-04', voucher_type='Stock Entry', voucher_no='002', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=100, qty_after_transaction=550, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-04', voucher_type='Stock Entry', voucher_no='002', has_serial_no=False, serial_no=None)]
```

### Step 3: Assign slots = FIFOSlots.generate(...)

```python
slots = FIFOSlots(self.filters, sle).generate()
```

### Step 4: Assign item_result = value

```python
item_result = slots['Flask Item']
```

### Step 5: Assign queue = value

```python
queue = item_result['fifo_queue']
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(item_result['total_qty'], 550.0)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(queue[0][0], 450.0)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(queue[1][0], 50.0)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(queue[2][0], 50.0)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(sum([i[0] for i in queue]), 550.0)
```


## Complete Example

```python
# Setup
self.filters = frappe._dict(company='_Test Company', to_date='2021-12-10', ranges=['30', '60', '90'])

# Workflow
'\n\t\tUnder consume item and have more repacked item qty (same warehouse).\n\t\tLedger:\n\t\tItem\t| Qty  | Voucher\n\t\t------------------------\n\t\tItem 1  | 500  | 001\n\t\tItem 1  | -50  | 002 (repack)\n\t\tItem 1  | 100  | 002 (repack)\n\n\t\tCase most likely for batch items. Test time bucket computation.\n\t\t'
sle = [frappe._dict(name='Flask Item', actual_qty=500, qty_after_transaction=500, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-03', voucher_type='Stock Entry', voucher_no='001', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=-50, qty_after_transaction=450, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-04', voucher_type='Stock Entry', voucher_no='002', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=100, qty_after_transaction=550, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-04', voucher_type='Stock Entry', voucher_no='002', has_serial_no=False, serial_no=None)]
slots = FIFOSlots(self.filters, sle).generate()
item_result = slots['Flask Item']
queue = item_result['fifo_queue']
self.assertEqual(item_result['total_qty'], 550.0)
self.assertEqual(queue[0][0], 450.0)
self.assertEqual(queue[1][0], 50.0)
self.assertEqual(queue[2][0], 50.0)
self.assertEqual(sum([i[0] for i in queue]), 550.0)
```

## Next Steps


---

*Source: test_stock_ageing.py:511 | Complexity: Advanced | Last updated: 2026-02-04*