# How To: Normal Inward Outward Queue

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Reference: Case 1 in stock_ageing_fifo_logic.md (same wh)

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

### Step 1: 'Reference: Case 1 in stock_ageing_fifo_logic.md (same wh)'

```python
'Reference: Case 1 in stock_ageing_fifo_logic.md (same wh)'
```

### Step 2: Assign sle = value

```python
sle = [frappe._dict(name='Flask Item', actual_qty=30, qty_after_transaction=30, stock_value_difference=30, warehouse='WH 1', posting_date='2021-12-01', voucher_type='Stock Entry', voucher_no='001', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=20, qty_after_transaction=50, stock_value_difference=20, warehouse='WH 1', posting_date='2021-12-02', voucher_type='Stock Entry', voucher_no='002', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=-10, qty_after_transaction=40, stock_value_difference=-10, warehouse='WH 1', posting_date='2021-12-03', voucher_type='Stock Entry', voucher_no='003', has_serial_no=False, serial_no=None)]
```

### Step 3: Assign slots = FIFOSlots.generate(...)

```python
slots = FIFOSlots(self.filters, sle).generate()
```

### Step 4: Call self.assertTrue()

```python
self.assertTrue(slots['Flask Item']['fifo_queue'])
```

### Step 5: Assign result = value

```python
result = slots['Flask Item']
```

### Step 6: Assign queue = value

```python
queue = result['fifo_queue']
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(result['qty_after_transaction'], result['total_qty'])
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(queue[0][0], 20.0)
```

### Step 9: Assign data = format_report_data(...)

```python
data = format_report_data(self.filters, slots, self.filters['to_date'])
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(data[0][8], 40.0)
```


## Complete Example

```python
# Setup
self.filters = frappe._dict(company='_Test Company', to_date='2021-12-10', ranges=['30', '60', '90'])

# Workflow
'Reference: Case 1 in stock_ageing_fifo_logic.md (same wh)'
sle = [frappe._dict(name='Flask Item', actual_qty=30, qty_after_transaction=30, stock_value_difference=30, warehouse='WH 1', posting_date='2021-12-01', voucher_type='Stock Entry', voucher_no='001', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=20, qty_after_transaction=50, stock_value_difference=20, warehouse='WH 1', posting_date='2021-12-02', voucher_type='Stock Entry', voucher_no='002', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=-10, qty_after_transaction=40, stock_value_difference=-10, warehouse='WH 1', posting_date='2021-12-03', voucher_type='Stock Entry', voucher_no='003', has_serial_no=False, serial_no=None)]
slots = FIFOSlots(self.filters, sle).generate()
self.assertTrue(slots['Flask Item']['fifo_queue'])
result = slots['Flask Item']
queue = result['fifo_queue']
self.assertEqual(result['qty_after_transaction'], result['total_qty'])
self.assertEqual(queue[0][0], 20.0)
data = format_report_data(self.filters, slots, self.filters['to_date'])
self.assertEqual(data[0][8], 40.0)
```

## Next Steps


---

*Source: test_stock_ageing.py:14 | Complexity: Advanced | Last updated: 2026-02-04*