# How To: Inter Company Transfer Intermediate Cancellation

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Receive into and Deliver Serial No from one company.
Then Receive into and Deliver from second company.
Try to cancel intermediate receipts/deliveries to test if it is blocked.

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

### Step 1: '\n\t\tReceive into and Deliver Serial No from one company.\n\t\tThen Receive into and Deliver from second company.\n\t\tTry to cancel intermediate receipts/deliveries to test if it is blocked.\n\t\t'

```python
'\n\t\tReceive into and Deliver Serial No from one company.\n\t\tThen Receive into and Deliver from second company.\n\t\tTry to cancel intermediate receipts/deliveries to test if it is blocked.\n\t\t'
```

### Step 2: Assign se = make_serialized_item(...)

```python
se = make_serialized_item(self, target_warehouse='_Test Warehouse - _TC')
```

### Step 3: Assign serial_nos = get_serial_nos_from_bundle(...)

```python
serial_nos = get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)
```

### Step 4: Assign sn_doc = frappe.get_doc(...)

```python
sn_doc = frappe.get_doc('Serial No', serial_nos[0])
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(sn_doc.warehouse, '_Test Warehouse - _TC')
```

### Step 6: Assign dn = create_delivery_note(...)

```python
dn = create_delivery_note(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]])
```

### Step 7: Call sn_doc.reload()

```python
sn_doc.reload()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(sn_doc.warehouse, None)
```

### Step 9: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, se.cancel)
```

### Step 10: Assign wh = create_warehouse(...)

```python
wh = create_warehouse('_Test Warehouse', company='_Test Company 1')
```

### Step 11: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]], company='_Test Company 1', warehouse=wh)
```

### Step 12: Call sn_doc.reload()

```python
sn_doc.reload()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(sn_doc.warehouse, wh)
```

### Step 14: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, dn.cancel)
```

### Step 15: Call create_delivery_note()

```python
create_delivery_note(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]], company='_Test Company 1', warehouse=wh, cost_center='_Test Company 1 - _TC1')
```

### Step 16: Call sn_doc.reload()

```python
sn_doc.reload()
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(sn_doc.warehouse, None)
```

### Step 18: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, se.cancel)
```

### Step 19: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, dn.cancel)
```

### Step 20: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, pr.cancel)
```


## Complete Example

```python
# Workflow
'\n\t\tReceive into and Deliver Serial No from one company.\n\t\tThen Receive into and Deliver from second company.\n\t\tTry to cancel intermediate receipts/deliveries to test if it is blocked.\n\t\t'
se = make_serialized_item(self, target_warehouse='_Test Warehouse - _TC')
serial_nos = get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)
sn_doc = frappe.get_doc('Serial No', serial_nos[0])
self.assertEqual(sn_doc.warehouse, '_Test Warehouse - _TC')
dn = create_delivery_note(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]])
sn_doc.reload()
self.assertEqual(sn_doc.warehouse, None)
self.assertRaises(frappe.ValidationError, se.cancel)
wh = create_warehouse('_Test Warehouse', company='_Test Company 1')
pr = make_purchase_receipt(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]], company='_Test Company 1', warehouse=wh)
sn_doc.reload()
self.assertEqual(sn_doc.warehouse, wh)
self.assertRaises(frappe.ValidationError, dn.cancel)
create_delivery_note(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]], company='_Test Company 1', warehouse=wh, cost_center='_Test Company 1 - _TC1')
sn_doc.reload()
self.assertEqual(sn_doc.warehouse, None)
self.assertRaises(frappe.ValidationError, se.cancel)
self.assertRaises(frappe.ValidationError, dn.cancel)
self.assertRaises(frappe.ValidationError, pr.cancel)
```

## Next Steps


---

*Source: test_serial_no.py:73 | Complexity: Advanced | Last updated: 2026-02-04*