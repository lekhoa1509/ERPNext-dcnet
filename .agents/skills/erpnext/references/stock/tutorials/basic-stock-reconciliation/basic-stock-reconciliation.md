# How To: Basic Stock Reconciliation

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Ledger (same wh): [+30, reco reset >> 50, -10]
Bal: 40

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

### Step 1: '\n\t\tLedger (same wh): [+30, reco reset >> 50, -10]\n\t\tBal: 40\n\t\t'

```python
'\n\t\tLedger (same wh): [+30, reco reset >> 50, -10]\n\t\tBal: 40\n\t\t'
```

### Step 2: Assign sle = value

```python
sle = [frappe._dict(name='Flask Item', actual_qty=30, qty_after_transaction=30, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-01', voucher_type='Stock Entry', voucher_no='001', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=0, qty_after_transaction=50, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-02', voucher_type='Stock Reconciliation', voucher_no='002', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=-10, qty_after_transaction=40, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-03', voucher_type='Stock Entry', voucher_no='003', has_serial_no=False, serial_no=None)]
```

### Step 3: Assign slots = FIFOSlots.generate(...)

```python
slots = FIFOSlots(self.filters, sle).generate()
```

### Step 4: Assign result = value

```python
result = slots['Flask Item']
```

### Step 5: Assign queue = value

```python
queue = result['fifo_queue']
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(result['qty_after_transaction'], result['total_qty'])
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(result['total_qty'], 40.0)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(queue[0][0], 20.0)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(queue[1][0], 20.0)
```


## Complete Example

```python
# Setup
self.filters = frappe._dict(company='_Test Company', to_date='2021-12-10', ranges=['30', '60', '90'])

# Workflow
'\n\t\tLedger (same wh): [+30, reco reset >> 50, -10]\n\t\tBal: 40\n\t\t'
sle = [frappe._dict(name='Flask Item', actual_qty=30, qty_after_transaction=30, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-01', voucher_type='Stock Entry', voucher_no='001', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=0, qty_after_transaction=50, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-02', voucher_type='Stock Reconciliation', voucher_no='002', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=-10, qty_after_transaction=40, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-03', voucher_type='Stock Entry', voucher_no='003', has_serial_no=False, serial_no=None)]
slots = FIFOSlots(self.filters, sle).generate()
result = slots['Flask Item']
queue = result['fifo_queue']
self.assertEqual(result['qty_after_transaction'], result['total_qty'])
self.assertEqual(result['total_qty'], 40.0)
self.assertEqual(queue[0][0], 20.0)
self.assertEqual(queue[1][0], 20.0)
```

## Next Steps


---

*Source: test_stock_ageing.py:128 | Complexity: Advanced | Last updated: 2026-02-04*