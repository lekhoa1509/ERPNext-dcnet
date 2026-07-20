# How To: Inward Outward Batch Valuation

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test inward outward batch valuation

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.serial_and_batch_bundle.serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.serial_batch_bundle`
- `erpnext.stock.serial_batch_bundle`
- `erpnext.stock.serial_batch_bundle`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`


## Step-by-Step Guide

### Step 1: Assign batch_item_code = 'New Batch No Valuation 1'

```python
batch_item_code = 'New Batch No Valuation 1'
```

### Step 2: Call make_item()

```python
make_item(batch_item_code, {'has_batch_no': 1, 'create_new_batch': 1, 'batch_number_series': 'TEST-BATTCCH-VAL-.#####', 'is_stock_item': 1})
```

### Step 3: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(item_code=batch_item_code, warehouse='_Test Warehouse - _TC', qty=10, rate=500)
```

### Step 4: Assign batch_no1 = get_batch_from_bundle(...)

```python
batch_no1 = get_batch_from_bundle(pr.items[0].serial_and_batch_bundle)
```

### Step 5: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(item_code=batch_item_code, warehouse='_Test Warehouse - _TC', qty=10, rate=300)
```

### Step 6: Assign batch_no2 = get_batch_from_bundle(...)

```python
batch_no2 = get_batch_from_bundle(pr.items[0].serial_and_batch_bundle)
```

### Step 7: Assign dn = create_delivery_note(...)

```python
dn = create_delivery_note(item_code=batch_item_code, warehouse='_Test Warehouse - _TC', qty=10, rate=1500, batch_no=batch_no2)
```

### Step 8: Assign stock_value_difference = frappe.db.get_value(...)

```python
stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': dn.name, 'is_cancelled': 0, 'voucher_type': 'Delivery Note'}, 'stock_value_difference')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(flt(stock_value_difference, 2), -3000)
```

### Step 10: Assign dn = create_delivery_note(...)

```python
dn = create_delivery_note(item_code=batch_item_code, warehouse='_Test Warehouse - _TC', qty=10, rate=1500, batch_no=batch_no1)
```

### Step 11: Assign stock_value_difference = frappe.db.get_value(...)

```python
stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': dn.name, 'is_cancelled': 0, 'voucher_type': 'Delivery Note'}, 'stock_value_difference')
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(flt(stock_value_difference, 2), -5000)
```


## Complete Example

```python
# Workflow
from erpnext.stock.doctype.delivery_note.test_delivery_note import create_delivery_note
from erpnext.stock.doctype.purchase_receipt.test_purchase_receipt import make_purchase_receipt
batch_item_code = 'New Batch No Valuation 1'
make_item(batch_item_code, {'has_batch_no': 1, 'create_new_batch': 1, 'batch_number_series': 'TEST-BATTCCH-VAL-.#####', 'is_stock_item': 1})
pr = make_purchase_receipt(item_code=batch_item_code, warehouse='_Test Warehouse - _TC', qty=10, rate=500)
batch_no1 = get_batch_from_bundle(pr.items[0].serial_and_batch_bundle)
pr = make_purchase_receipt(item_code=batch_item_code, warehouse='_Test Warehouse - _TC', qty=10, rate=300)
batch_no2 = get_batch_from_bundle(pr.items[0].serial_and_batch_bundle)
dn = create_delivery_note(item_code=batch_item_code, warehouse='_Test Warehouse - _TC', qty=10, rate=1500, batch_no=batch_no2)
stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': dn.name, 'is_cancelled': 0, 'voucher_type': 'Delivery Note'}, 'stock_value_difference')
self.assertEqual(flt(stock_value_difference, 2), -3000)
dn = create_delivery_note(item_code=batch_item_code, warehouse='_Test Warehouse - _TC', qty=10, rate=1500, batch_no=batch_no1)
stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': dn.name, 'is_cancelled': 0, 'voucher_type': 'Delivery Note'}, 'stock_value_difference')
self.assertEqual(flt(stock_value_difference, 2), -5000)
```

## Next Steps


---

*Source: test_serial_and_batch_bundle.py:140 | Complexity: Advanced | Last updated: 2026-02-04*