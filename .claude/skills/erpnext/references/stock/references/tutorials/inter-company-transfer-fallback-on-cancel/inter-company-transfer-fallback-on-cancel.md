# How To: Inter Company Transfer Fallback On Cancel

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test Serial No state changes on cancellation.
If Delivery cancelled, it should fall back on last Receipt in the same company.
If Receipt is cancelled, it should be Inactive in the same company.

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

### Step 1: '\n\t\tTest Serial No state changes on cancellation.\n\t\tIf Delivery cancelled, it should fall back on last Receipt in the same company.\n\t\tIf Receipt is cancelled, it should be Inactive in the same company.\n\t\t'

```python
'\n\t\tTest Serial No state changes on cancellation.\n\t\tIf Delivery cancelled, it should fall back on last Receipt in the same company.\n\t\tIf Receipt is cancelled, it should be Inactive in the same company.\n\t\t'
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

### Step 5: Assign dn = create_delivery_note(...)

```python
dn = create_delivery_note(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]])
```

### Step 6: Assign wh = create_warehouse(...)

```python
wh = create_warehouse('_Test Warehouse', company='_Test Company 1')
```

### Step 7: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]], company='_Test Company 1', warehouse=wh, cost_center='_Test Company 1 - _TC1')
```

### Step 8: Assign dn_2 = create_delivery_note(...)

```python
dn_2 = create_delivery_note(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]], company='_Test Company 1', warehouse=wh, cost_center='_Test Company 1 - _TC1')
```

### Step 9: Call sn_doc.reload()

```python
sn_doc.reload()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(sn_doc.warehouse, None)
```

### Step 11: Call dn_2.cancel()

```python
dn_2.cancel()
```

### Step 12: Call sn_doc.reload()

```python
sn_doc.reload()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(sn_doc.warehouse, wh)
```

### Step 14: Call pr.cancel()

```python
pr.cancel()
```

### Step 15: Call sn_doc.reload()

```python
sn_doc.reload()
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(sn_doc.warehouse, None)
```

### Step 17: Call dn.cancel()

```python
dn.cancel()
```

### Step 18: Call sn_doc.reload()

```python
sn_doc.reload()
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(sn_doc.warehouse, '_Test Warehouse - _TC')
```


## Complete Example

```python
# Workflow
'\n\t\tTest Serial No state changes on cancellation.\n\t\tIf Delivery cancelled, it should fall back on last Receipt in the same company.\n\t\tIf Receipt is cancelled, it should be Inactive in the same company.\n\t\t'
se = make_serialized_item(self, target_warehouse='_Test Warehouse - _TC')
serial_nos = get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)
sn_doc = frappe.get_doc('Serial No', serial_nos[0])
dn = create_delivery_note(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]])
wh = create_warehouse('_Test Warehouse', company='_Test Company 1')
pr = make_purchase_receipt(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]], company='_Test Company 1', warehouse=wh, cost_center='_Test Company 1 - _TC1')
dn_2 = create_delivery_note(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]], company='_Test Company 1', warehouse=wh, cost_center='_Test Company 1 - _TC1')
sn_doc.reload()
self.assertEqual(sn_doc.warehouse, None)
dn_2.cancel()
sn_doc.reload()
self.assertEqual(sn_doc.warehouse, wh)
pr.cancel()
sn_doc.reload()
self.assertEqual(sn_doc.warehouse, None)
dn.cancel()
sn_doc.reload()
self.assertEqual(sn_doc.warehouse, '_Test Warehouse - _TC')
```

## Next Steps


---

*Source: test_serial_no.py:133 | Complexity: Advanced | Last updated: 2026-02-04*