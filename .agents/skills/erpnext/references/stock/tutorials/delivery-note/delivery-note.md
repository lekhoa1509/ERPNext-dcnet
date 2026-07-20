# How To: Delivery Note

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test automatic batch selection for outgoing items

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

### Step 1: 'Test automatic batch selection for outgoing items'

```python
'Test automatic batch selection for outgoing items'
```

### Step 2: Assign batch_qty = 15

```python
batch_qty = 15
```

### Step 3: Assign receipt = self.test_purchase_receipt(...)

```python
receipt = self.test_purchase_receipt(batch_qty)
```

### Step 4: Assign item_code = 'ITEM-BATCH-1'

```python
item_code = 'ITEM-BATCH-1'
```

### Step 5: Assign batch_no = get_batch_from_bundle(...)

```python
batch_no = get_batch_from_bundle(receipt.items[0].serial_and_batch_bundle)
```

### Step 6: Assign bundle_id = value

```python
bundle_id = SerialBatchCreation({'item_code': item_code, 'warehouse': receipt.items[0].warehouse, 'actual_qty': batch_qty, 'voucher_type': 'Stock Entry', 'batches': frappe._dict({batch_no: batch_qty}), 'type_of_transaction': 'Outward', 'company': receipt.company, 'do_not_submit': 1}).make_serial_and_batch_bundle().name
```

### Step 7: Assign delivery_note = frappe.get_doc.insert(...)

```python
delivery_note = frappe.get_doc(doctype='Delivery Note', customer='_Test Customer', company=receipt.company, items=[dict(item_code=item_code, qty=batch_qty, rate=10, warehouse=receipt.items[0].warehouse, serial_and_batch_bundle=bundle_id)]).insert()
```

### Step 8: Call delivery_note.submit()

```python
delivery_note.submit()
```

### Step 9: Call receipt.load_from_db()

```python
receipt.load_from_db()
```

### Step 10: Call delivery_note.load_from_db()

```python
delivery_note.load_from_db()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(get_batch_from_bundle(delivery_note.items[0].serial_and_batch_bundle), batch_no)
```


## Complete Example

```python
# Workflow
'Test automatic batch selection for outgoing items'
batch_qty = 15
receipt = self.test_purchase_receipt(batch_qty)
item_code = 'ITEM-BATCH-1'
batch_no = get_batch_from_bundle(receipt.items[0].serial_and_batch_bundle)
bundle_id = SerialBatchCreation({'item_code': item_code, 'warehouse': receipt.items[0].warehouse, 'actual_qty': batch_qty, 'voucher_type': 'Stock Entry', 'batches': frappe._dict({batch_no: batch_qty}), 'type_of_transaction': 'Outward', 'company': receipt.company, 'do_not_submit': 1}).make_serial_and_batch_bundle().name
delivery_note = frappe.get_doc(doctype='Delivery Note', customer='_Test Customer', company=receipt.company, items=[dict(item_code=item_code, qty=batch_qty, rate=10, warehouse=receipt.items[0].warehouse, serial_and_batch_bundle=bundle_id)]).insert()
delivery_note.submit()
receipt.load_from_db()
delivery_note.load_from_db()
self.assertEqual(get_batch_from_bundle(delivery_note.items[0].serial_and_batch_bundle), batch_no)
```

## Next Steps


---

*Source: test_batch.py:156 | Complexity: Advanced | Last updated: 2026-02-04*