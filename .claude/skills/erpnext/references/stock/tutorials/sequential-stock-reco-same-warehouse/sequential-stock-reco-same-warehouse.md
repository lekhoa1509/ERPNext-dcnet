# How To: Sequential Stock Reco Same Warehouse

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test back to back stock recos (same warehouse).
Ledger: [reco opening >> +1000, reco reset >> 400, -10]
Bal: 390

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

### Step 1: '\n\t\tTest back to back stock recos (same warehouse).\n\t\tLedger: [reco opening >> +1000, reco reset >> 400, -10]\n\t\tBal: 390\n\t\t'

```python
'\n\t\tTest back to back stock recos (same warehouse).\n\t\tLedger: [reco opening >> +1000, reco reset >> 400, -10]\n\t\tBal: 390\n\t\t'
```

### Step 2: Assign sle = value

```python
sle = [frappe._dict(name='Flask Item', actual_qty=0, qty_after_transaction=1000, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-01', voucher_type='Stock Reconciliation', voucher_no='002', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=0, qty_after_transaction=400, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-02', voucher_type='Stock Reconciliation', voucher_no='003', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=-10, qty_after_transaction=390, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-03', voucher_type='Stock Entry', voucher_no='003', has_serial_no=False, serial_no=None)]
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
self.assertEqual(result['total_qty'], 390.0)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(queue[0][0], 390.0)
```


## Complete Example

```python
# Setup
self.filters = frappe._dict(company='_Test Company', to_date='2021-12-10', ranges=['30', '60', '90'])

# Workflow
'\n\t\tTest back to back stock recos (same warehouse).\n\t\tLedger: [reco opening >> +1000, reco reset >> 400, -10]\n\t\tBal: 390\n\t\t'
sle = [frappe._dict(name='Flask Item', actual_qty=0, qty_after_transaction=1000, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-01', voucher_type='Stock Reconciliation', voucher_no='002', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=0, qty_after_transaction=400, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-02', voucher_type='Stock Reconciliation', voucher_no='003', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=-10, qty_after_transaction=390, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-03', voucher_type='Stock Entry', voucher_no='003', has_serial_no=False, serial_no=None)]
slots = FIFOSlots(self.filters, sle).generate()
result = slots['Flask Item']
queue = result['fifo_queue']
self.assertEqual(result['qty_after_transaction'], result['total_qty'])
self.assertEqual(result['total_qty'], 390.0)
self.assertEqual(queue[0][0], 390.0)
```

## Next Steps


---

*Source: test_stock_ageing.py:182 | Complexity: Advanced | Last updated: 2026-02-04*