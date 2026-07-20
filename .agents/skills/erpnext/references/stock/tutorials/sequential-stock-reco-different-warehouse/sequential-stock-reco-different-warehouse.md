# How To: Sequential Stock Reco Different Warehouse

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Ledger:
WH      | Voucher | Qty
-------------------
WH1 | Reco        | 1000
WH2 | Reco        | 400
WH1 | SE          | -10

Bal: WH1 bal + WH2 bal = 990 + 400 = 1390

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

### Step 1: '\n\t\tLedger:\n\t\tWH\t| Voucher | Qty\n\t\t-------------------\n\t\tWH1 | Reco\t  | 1000\n\t\tWH2 | Reco\t  | 400\n\t\tWH1 | SE\t  | -10\n\n\t\tBal: WH1 bal + WH2 bal = 990 + 400 = 1390\n\t\t'

```python
'\n\t\tLedger:\n\t\tWH\t| Voucher | Qty\n\t\t-------------------\n\t\tWH1 | Reco\t  | 1000\n\t\tWH2 | Reco\t  | 400\n\t\tWH1 | SE\t  | -10\n\n\t\tBal: WH1 bal + WH2 bal = 990 + 400 = 1390\n\t\t'
```

### Step 2: Assign sle = value

```python
sle = [frappe._dict(name='Flask Item', actual_qty=0, qty_after_transaction=1000, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-01', voucher_type='Stock Reconciliation', voucher_no='002', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=0, qty_after_transaction=400, stock_value_difference=0, warehouse='WH 2', posting_date='2021-12-02', voucher_type='Stock Reconciliation', voucher_no='003', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=-10, qty_after_transaction=990, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-03', voucher_type='Stock Entry', voucher_no='004', has_serial_no=False, serial_no=None)]
```

### Step 3: Assign unknown = generate_item_and_item_wh_wise_slots(...)

```python
item_wise_slots, item_wh_wise_slots = generate_item_and_item_wh_wise_slots(filters=self.filters, sle=sle)
```

### Step 4: Assign item_result = value

```python
item_result = item_wise_slots['Flask Item']
```

### Step 5: Assign queue = value

```python
queue = item_result['fifo_queue']
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(item_result['qty_after_transaction'], item_result['total_qty'])
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(item_result['total_qty'], 1390.0)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(queue[0][0], 990.0)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(queue[1][0], 400.0)
```

### Step 10: Assign item_wh_balances = value

```python
item_wh_balances = [item_wh_wise_slots.get(i).get('qty_after_transaction') for i in item_wh_wise_slots]
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(sum(item_wh_balances), item_result['qty_after_transaction'])
```


## Complete Example

```python
# Setup
self.filters = frappe._dict(company='_Test Company', to_date='2021-12-10', ranges=['30', '60', '90'])

# Workflow
'\n\t\tLedger:\n\t\tWH\t| Voucher | Qty\n\t\t-------------------\n\t\tWH1 | Reco\t  | 1000\n\t\tWH2 | Reco\t  | 400\n\t\tWH1 | SE\t  | -10\n\n\t\tBal: WH1 bal + WH2 bal = 990 + 400 = 1390\n\t\t'
sle = [frappe._dict(name='Flask Item', actual_qty=0, qty_after_transaction=1000, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-01', voucher_type='Stock Reconciliation', voucher_no='002', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=0, qty_after_transaction=400, stock_value_difference=0, warehouse='WH 2', posting_date='2021-12-02', voucher_type='Stock Reconciliation', voucher_no='003', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=-10, qty_after_transaction=990, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-03', voucher_type='Stock Entry', voucher_no='004', has_serial_no=False, serial_no=None)]
item_wise_slots, item_wh_wise_slots = generate_item_and_item_wh_wise_slots(filters=self.filters, sle=sle)
item_result = item_wise_slots['Flask Item']
queue = item_result['fifo_queue']
self.assertEqual(item_result['qty_after_transaction'], item_result['total_qty'])
self.assertEqual(item_result['total_qty'], 1390.0)
self.assertEqual(queue[0][0], 990.0)
self.assertEqual(queue[1][0], 400.0)
item_wh_balances = [item_wh_wise_slots.get(i).get('qty_after_transaction') for i in item_wh_wise_slots]
self.assertEqual(sum(item_wh_balances), item_result['qty_after_transaction'])
```

## Next Steps


---

*Source: test_stock_ageing.py:235 | Complexity: Advanced | Last updated: 2026-02-04*