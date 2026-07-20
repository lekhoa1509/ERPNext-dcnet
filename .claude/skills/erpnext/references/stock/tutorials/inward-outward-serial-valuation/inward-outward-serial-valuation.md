# How To: Inward Outward Serial Valuation

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test inward outward serial valuation

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

### Step 1: Assign serial_item_code = 'New Serial No Valuation 1'

```python
serial_item_code = 'New Serial No Valuation 1'
```

### Step 2: Call make_item()

```python
make_item(serial_item_code, {'has_serial_no': 1, 'serial_no_series': 'TEST-SER-VAL-.#####', 'is_stock_item': 1})
```

### Step 3: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(item_code=serial_item_code, warehouse='_Test Warehouse - _TC', qty=1, rate=500)
```

### Step 4: Assign serial_no1 = value

```python
serial_no1 = get_serial_nos_from_bundle(pr.items[0].serial_and_batch_bundle)[0]
```

### Step 5: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(item_code=serial_item_code, warehouse='_Test Warehouse - _TC', qty=1, rate=300)
```

### Step 6: Assign serial_no2 = value

```python
serial_no2 = get_serial_nos_from_bundle(pr.items[0].serial_and_batch_bundle)[0]
```

### Step 7: Assign dn = create_delivery_note(...)

```python
dn = create_delivery_note(item_code=serial_item_code, warehouse='_Test Warehouse - _TC', qty=1, rate=1500, serial_no=[serial_no2])
```

### Step 8: Assign stock_value_difference = frappe.db.get_value(...)

```python
stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': dn.name, 'is_cancelled': 0, 'voucher_type': 'Delivery Note'}, 'stock_value_difference')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(flt(stock_value_difference, 2), -300)
```

### Step 10: Assign dn = create_delivery_note(...)

```python
dn = create_delivery_note(item_code=serial_item_code, warehouse='_Test Warehouse - _TC', qty=1, rate=1500, serial_no=[serial_no1])
```

### Step 11: Assign stock_value_difference = frappe.db.get_value(...)

```python
stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': dn.name, 'is_cancelled': 0, 'voucher_type': 'Delivery Note'}, 'stock_value_difference')
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(flt(stock_value_difference, 2), -500)
```


## Complete Example

```python
# Workflow
from erpnext.stock.doctype.delivery_note.test_delivery_note import create_delivery_note
from erpnext.stock.doctype.purchase_receipt.test_purchase_receipt import make_purchase_receipt
serial_item_code = 'New Serial No Valuation 1'
make_item(serial_item_code, {'has_serial_no': 1, 'serial_no_series': 'TEST-SER-VAL-.#####', 'is_stock_item': 1})
pr = make_purchase_receipt(item_code=serial_item_code, warehouse='_Test Warehouse - _TC', qty=1, rate=500)
serial_no1 = get_serial_nos_from_bundle(pr.items[0].serial_and_batch_bundle)[0]
pr = make_purchase_receipt(item_code=serial_item_code, warehouse='_Test Warehouse - _TC', qty=1, rate=300)
serial_no2 = get_serial_nos_from_bundle(pr.items[0].serial_and_batch_bundle)[0]
dn = create_delivery_note(item_code=serial_item_code, warehouse='_Test Warehouse - _TC', qty=1, rate=1500, serial_no=[serial_no2])
stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': dn.name, 'is_cancelled': 0, 'voucher_type': 'Delivery Note'}, 'stock_value_difference')
self.assertEqual(flt(stock_value_difference, 2), -300)
dn = create_delivery_note(item_code=serial_item_code, warehouse='_Test Warehouse - _TC', qty=1, rate=1500, serial_no=[serial_no1])
stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': dn.name, 'is_cancelled': 0, 'voucher_type': 'Delivery Note'}, 'stock_value_difference')
self.assertEqual(flt(stock_value_difference, 2), -500)
```

## Next Steps


---

*Source: test_serial_and_batch_bundle.py:82 | Complexity: Advanced | Last updated: 2026-02-04*