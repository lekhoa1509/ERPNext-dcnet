# How To: Batch Stock Levels

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test automated batch creation from Purchase Receipt

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

### Step 1: 'Test automated batch creation from Purchase Receipt'

```python
'Test automated batch creation from Purchase Receipt'
```

### Step 2: Call self.make_batch_item()

```python
self.make_batch_item('ITEM-BATCH-1')
```

### Step 3: Assign receipt = frappe.get_doc.insert(...)

```python
receipt = frappe.get_doc(doctype='Purchase Receipt', supplier='_Test Supplier', company='_Test Company', items=[dict(item_code='ITEM-BATCH-1', qty=10, rate=10, warehouse='Stores - _TC')]).insert()
```

### Step 4: Call receipt.submit()

```python
receipt.submit()
```

### Step 5: Call receipt.load_from_db()

```python
receipt.load_from_db()
```

### Step 6: Assign batch_no = get_batch_from_bundle(...)

```python
batch_no = get_batch_from_bundle(receipt.items[0].serial_and_batch_bundle)
```

### Step 7: Assign bundle_id = value

```python
bundle_id = SerialBatchCreation({'item_code': 'ITEM-BATCH-1', 'warehouse': '_Test Warehouse - _TC', 'actual_qty': 20, 'voucher_type': 'Purchase Receipt', 'batches': frappe._dict({batch_no: 20}), 'type_of_transaction': 'Inward', 'company': receipt.company, 'do_not_submit': 1}).make_serial_and_batch_bundle().name
```

### Step 8: Assign receipt2 = frappe.get_doc.insert(...)

```python
receipt2 = frappe.get_doc(doctype='Purchase Receipt', supplier='_Test Supplier', company='_Test Company', items=[dict(item_code='ITEM-BATCH-1', qty=20, rate=10, warehouse='_Test Warehouse - _TC', serial_and_batch_bundle=bundle_id)]).insert()
```

### Step 9: Call receipt2.submit()

```python
receipt2.submit()
```

### Step 10: Call receipt.load_from_db()

```python
receipt.load_from_db()
```

### Step 11: Call receipt2.load_from_db()

```python
receipt2.load_from_db()
```

### Step 12: Call self.assertTrue()

```python
self.assertTrue(receipt.items[0].serial_and_batch_bundle)
```

### Step 13: Call self.assertTrue()

```python
self.assertTrue(receipt2.items[0].serial_and_batch_bundle)
```

### Step 14: Assign batchwise_qty = frappe._dict(...)

```python
batchwise_qty = frappe._dict({})
```

### Step 15: Assign batches = get_batch_qty(...)

```python
batches = get_batch_qty(batch_no)
```

### Step 16: Assign batch_no = get_batch_from_bundle(...)

```python
batch_no = get_batch_from_bundle(r.items[0].serial_and_batch_bundle)
```

### Step 17: Assign key = value

```python
key = (batch_no, r.items[0].warehouse)
```

### Step 18: Assign unknown = value

```python
batchwise_qty[key] = r.items[0].qty
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(d.qty, batchwise_qty[d.batch_no, d.warehouse])
```


## Complete Example

```python
# Workflow
'Test automated batch creation from Purchase Receipt'
self.make_batch_item('ITEM-BATCH-1')
receipt = frappe.get_doc(doctype='Purchase Receipt', supplier='_Test Supplier', company='_Test Company', items=[dict(item_code='ITEM-BATCH-1', qty=10, rate=10, warehouse='Stores - _TC')]).insert()
receipt.submit()
receipt.load_from_db()
batch_no = get_batch_from_bundle(receipt.items[0].serial_and_batch_bundle)
bundle_id = SerialBatchCreation({'item_code': 'ITEM-BATCH-1', 'warehouse': '_Test Warehouse - _TC', 'actual_qty': 20, 'voucher_type': 'Purchase Receipt', 'batches': frappe._dict({batch_no: 20}), 'type_of_transaction': 'Inward', 'company': receipt.company, 'do_not_submit': 1}).make_serial_and_batch_bundle().name
receipt2 = frappe.get_doc(doctype='Purchase Receipt', supplier='_Test Supplier', company='_Test Company', items=[dict(item_code='ITEM-BATCH-1', qty=20, rate=10, warehouse='_Test Warehouse - _TC', serial_and_batch_bundle=bundle_id)]).insert()
receipt2.submit()
receipt.load_from_db()
receipt2.load_from_db()
self.assertTrue(receipt.items[0].serial_and_batch_bundle)
self.assertTrue(receipt2.items[0].serial_and_batch_bundle)
batchwise_qty = frappe._dict({})
for r in [receipt, receipt2]:
    batch_no = get_batch_from_bundle(r.items[0].serial_and_batch_bundle)
    key = (batch_no, r.items[0].warehouse)
    batchwise_qty[key] = r.items[0].qty
batches = get_batch_qty(batch_no)
for d in batches:
    self.assertEqual(d.qty, batchwise_qty[d.batch_no, d.warehouse])
```

## Next Steps


---

*Source: test_batch.py:62 | Complexity: Advanced | Last updated: 2026-02-04*