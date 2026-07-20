# How To: Inter Company Transfer

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test inter company transfer

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

### Step 1: Assign se = make_serialized_item(...)

```python
se = make_serialized_item(self, target_warehouse='_Test Warehouse - _TC')
```

### Step 2: Assign serial_nos = get_serial_nos_from_bundle(...)

```python
serial_nos = get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)
```

### Step 3: Call create_delivery_note()

```python
create_delivery_note(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]])
```

### Step 4: Assign serial_no = frappe.get_doc(...)

```python
serial_no = frappe.get_doc('Serial No', serial_nos[0])
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(serial_no.warehouse, None)
```

### Step 6: Assign wh = create_warehouse(...)

```python
wh = create_warehouse('_Test Warehouse', company='_Test Company 1')
```

### Step 7: Call make_purchase_receipt()

```python
make_purchase_receipt(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]], company='_Test Company 1', warehouse=wh)
```

### Step 8: Call serial_no.reload()

```python
serial_no.reload()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(serial_no.warehouse, wh)
```


## Complete Example

```python
# Workflow
se = make_serialized_item(self, target_warehouse='_Test Warehouse - _TC')
serial_nos = get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)
create_delivery_note(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]])
serial_no = frappe.get_doc('Serial No', serial_nos[0])
self.assertEqual(serial_no.warehouse, None)
wh = create_warehouse('_Test Warehouse', company='_Test Company 1')
make_purchase_receipt(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]], company='_Test Company 1', warehouse=wh)
serial_no.reload()
self.assertEqual(serial_no.warehouse, wh)
```

## Next Steps


---

*Source: test_serial_no.py:48 | Complexity: Advanced | Last updated: 2026-02-04*