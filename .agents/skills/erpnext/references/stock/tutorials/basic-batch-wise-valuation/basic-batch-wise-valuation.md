# How To: Basic Batch Wise Valuation

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test basic batch wise valuation

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe.exceptions`
- `frappe.tests`
- `frappe.utils`
- `frappe.utils.data`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.stock.doctype.batch.batch`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.serial_and_batch_bundle.serial_and_batch_bundle`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.get_item_details`
- `erpnext.stock.serial_batch_bundle`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.batch.batch`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`


## Step-by-Step Guide

### Step 1: Assign item_code = '_TestBatchWiseVal'

```python
item_code = '_TestBatchWiseVal'
```

### Step 2: Assign warehouse = '_Test Warehouse - _TC'

```python
warehouse = '_Test Warehouse - _TC'
```

### Step 3: Call self.make_batch_item()

```python
self.make_batch_item(item_code)
```

### Step 4: Assign rates = value

```python
rates = [42, 420]
```

### Step 5: Assign batches = value

```python
batches = {}
```

### Step 6: Assign unknown = list(...)

```python
LOW, HIGH = list(batches.keys())
```

### Step 7: Assign consumption_plan = value

```python
consumption_plan = [(HIGH, 1), (LOW, 2), (HIGH, 2), (HIGH, 4), (LOW, 6)]
```

### Step 8: Assign stock_value = value

```python
stock_value = sum(rates) * 10
```

### Step 9: Assign qty_after_transaction = 20

```python
qty_after_transaction = 20
```

### Step 10: Assign se = make_stock_entry(...)

```python
se = make_stock_entry(item_code=item_code, qty=10, rate=rate, target=warehouse)
```

### Step 11: Assign batch_no = get_batch_from_bundle(...)

```python
batch_no = get_batch_from_bundle(se.items[0].serial_and_batch_bundle)
```

### Step 12: Assign unknown = rate

```python
batches[batch_no] = rate
```

### Step 13: Assign se = make_stock_entry(...)

```python
se = make_stock_entry(item_code=item_code, source=warehouse, qty=qty, batch_no=batch)
```

### Step 14: Assign sle = frappe.get_last_doc(...)

```python
sle = frappe.get_last_doc('Stock Ledger Entry', {'is_cancelled': 0, 'voucher_no': se.name})
```

### Step 15: Assign stock_value_difference = value

```python
stock_value_difference = sle.actual_qty * batches[get_batch_from_bundle(sle.serial_and_batch_bundle)]
```

### Step 16: Call self.assertAlmostEqual()

```python
self.assertAlmostEqual(sle.stock_value_difference, stock_value_difference)
```

### Step 17: Call self.assertAlmostEqual()

```python
self.assertAlmostEqual(sle.stock_value, stock_value)
```

### Step 18: Call self.assertAlmostEqual()

```python
self.assertAlmostEqual(sle.qty_after_transaction, qty_after_transaction)
```

### Step 19: Call self.assertAlmostEqual()

```python
self.assertAlmostEqual(sle.valuation_rate, stock_value / qty_after_transaction)
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(json.loads(sle.stock_queue), [])
```


## Complete Example

```python
# Workflow
item_code = '_TestBatchWiseVal'
warehouse = '_Test Warehouse - _TC'
self.make_batch_item(item_code)
rates = [42, 420]
batches = {}
for rate in rates:
    se = make_stock_entry(item_code=item_code, qty=10, rate=rate, target=warehouse)
    batch_no = get_batch_from_bundle(se.items[0].serial_and_batch_bundle)
    batches[batch_no] = rate
LOW, HIGH = list(batches.keys())
consumption_plan = [(HIGH, 1), (LOW, 2), (HIGH, 2), (HIGH, 4), (LOW, 6)]
stock_value = sum(rates) * 10
qty_after_transaction = 20
for batch, qty in consumption_plan:
    se = make_stock_entry(item_code=item_code, source=warehouse, qty=qty, batch_no=batch)
    sle = frappe.get_last_doc('Stock Ledger Entry', {'is_cancelled': 0, 'voucher_no': se.name})
    stock_value_difference = sle.actual_qty * batches[get_batch_from_bundle(sle.serial_and_batch_bundle)]
    self.assertAlmostEqual(sle.stock_value_difference, stock_value_difference)
    stock_value += stock_value_difference
    self.assertAlmostEqual(sle.stock_value, stock_value)
    qty_after_transaction += sle.actual_qty
    self.assertAlmostEqual(sle.qty_after_transaction, qty_after_transaction)
    self.assertAlmostEqual(sle.valuation_rate, stock_value / qty_after_transaction)
    self.assertEqual(json.loads(sle.stock_queue), [])
```

## Next Steps


---

*Source: test_batch.py:490 | Complexity: Advanced | Last updated: 2026-02-04*