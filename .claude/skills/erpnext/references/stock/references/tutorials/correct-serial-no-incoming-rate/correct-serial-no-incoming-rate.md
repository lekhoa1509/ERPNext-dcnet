# How To: Correct Serial No Incoming Rate

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Check correct consumption rate based on serial no record.

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe`
- `frappe.tests`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.serial_no.serial_no`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.doctype.serial_and_batch_bundle.serial_and_batch_bundle`


## Step-by-Step Guide

### Step 1: 'Check correct consumption rate based on serial no record.'

```python
'Check correct consumption rate based on serial no record.'
```

### Step 2: Assign item_code = '_Test Serialized Item'

```python
item_code = '_Test Serialized Item'
```

### Step 3: Assign warehouse = '_Test Warehouse - _TC'

```python
warehouse = '_Test Warehouse - _TC'
```

### Step 4: Assign serial_nos = value

```python
serial_nos = ['LOWVALUATION', 'HIGHVALUATION']
```

### Step 5: Call make_stock_entry()

```python
make_stock_entry(item_code=item_code, to_warehouse=warehouse, qty=1, rate=42, serial_no=[serial_nos[0]])
```

### Step 6: Call make_stock_entry()

```python
make_stock_entry(item_code=item_code, to_warehouse=warehouse, qty=1, rate=113, serial_no=[serial_nos[1]])
```

### Step 7: Assign out = create_delivery_note(...)

```python
out = create_delivery_note(item_code=item_code, qty=1, serial_no=[serial_nos[0]], do_not_submit=True)
```

### Step 8: Assign bundle = value

```python
bundle = out.items[0].serial_and_batch_bundle
```

### Step 9: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc('Serial and Batch Bundle', bundle)
```

### Step 10: Assign unknown.serial_no = value

```python
doc.entries[0].serial_no = serial_nos[1]
```

### Step 11: Call doc.save()

```python
doc.save()
```

### Step 12: Call out.save()

```python
out.save()
```

### Step 13: Call out.submit()

```python
out.submit()
```

### Step 14: Assign value_diff = frappe.db.get_value(...)

```python
value_diff = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': out.name, 'voucher_type': 'Delivery Note'}, 'stock_value_difference')
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(value_diff, -113)
```

### Step 16: Call frappe.get_doc.insert()

```python
frappe.get_doc({'doctype': 'Serial No', 'item_code': item_code, 'serial_no': serial_no}).insert()
```


## Complete Example

```python
# Workflow
'Check correct consumption rate based on serial no record.'
item_code = '_Test Serialized Item'
warehouse = '_Test Warehouse - _TC'
serial_nos = ['LOWVALUATION', 'HIGHVALUATION']
for serial_no in serial_nos:
    if not frappe.db.exists('Serial No', serial_no):
        frappe.get_doc({'doctype': 'Serial No', 'item_code': item_code, 'serial_no': serial_no}).insert()
make_stock_entry(item_code=item_code, to_warehouse=warehouse, qty=1, rate=42, serial_no=[serial_nos[0]])
make_stock_entry(item_code=item_code, to_warehouse=warehouse, qty=1, rate=113, serial_no=[serial_nos[1]])
out = create_delivery_note(item_code=item_code, qty=1, serial_no=[serial_nos[0]], do_not_submit=True)
bundle = out.items[0].serial_and_batch_bundle
doc = frappe.get_doc('Serial and Batch Bundle', bundle)
doc.entries[0].serial_no = serial_nos[1]
doc.save()
out.save()
out.submit()
value_diff = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': out.name, 'voucher_type': 'Delivery Note'}, 'stock_value_difference')
self.assertEqual(value_diff, -113)
```

## Next Steps


---

*Source: test_serial_no.py:189 | Complexity: Advanced | Last updated: 2026-02-04*