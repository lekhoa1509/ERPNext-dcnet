# How To: Auto Fetch

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test auto fetch

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

### Step 1: Assign item_code = value

```python
item_code = make_item(properties={'has_serial_no': 1, 'has_batch_no': 1, 'create_new_batch': 1, 'serial_no_series': 'TEST.#######'}).name
```

### Step 2: Assign warehouse = '_Test Warehouse - _TC'

```python
warehouse = '_Test Warehouse - _TC'
```

### Step 3: Assign in1 = make_stock_entry(...)

```python
in1 = make_stock_entry(item_code=item_code, to_warehouse=warehouse, qty=5)
```

### Step 4: Assign in2 = make_stock_entry(...)

```python
in2 = make_stock_entry(item_code=item_code, to_warehouse=warehouse, qty=5)
```

### Step 5: Call in1.reload()

```python
in1.reload()
```

### Step 6: Call in2.reload()

```python
in2.reload()
```

### Step 7: Assign batch1 = get_batch_from_bundle(...)

```python
batch1 = get_batch_from_bundle(in1.items[0].serial_and_batch_bundle)
```

### Step 8: Assign batch2 = get_batch_from_bundle(...)

```python
batch2 = get_batch_from_bundle(in2.items[0].serial_and_batch_bundle)
```

### Step 9: Assign batch_wise_serials = value

```python
batch_wise_serials = {batch1: get_serial_nos_from_bundle(in1.items[0].serial_and_batch_bundle), batch2: get_serial_nos_from_bundle(in2.items[0].serial_and_batch_bundle)}
```

### Step 10: Assign first_fetch = get_auto_serial_nos(...)

```python
first_fetch = get_auto_serial_nos(_dict({'qty': 5, 'item_code': item_code, 'warehouse': warehouse}))
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(first_fetch, batch_wise_serials[batch1])
```

### Step 12: Assign partial_fetch = get_auto_serial_nos(...)

```python
partial_fetch = get_auto_serial_nos(_dict({'qty': 2, 'item_code': item_code, 'warehouse': warehouse}))
```

### Step 13: Call self.assertTrue()

```python
self.assertTrue(set(partial_fetch).issubset(set(first_fetch)), msg=f'{partial_fetch} should be subset of {first_fetch}')
```

### Step 14: Assign remaining = get_auto_serial_nos(...)

```python
remaining = get_auto_serial_nos(_dict({'qty': 3, 'item_code': item_code, 'warehouse': warehouse, 'ignore_serial_nos': partial_fetch}))
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(sorted(remaining + partial_fetch), first_fetch)
```

### Step 16: Call self.assertFalse()

```python
self.assertFalse(get_auto_serial_nos(_dict({'qty': 10, 'item_code': item_code, 'warehouse': 'Non Existing Warehouse'})))
```

### Step 17: Assign all_serials = value

```python
all_serials = [sr for sr_list in batch_wise_serials.values() for sr in sr_list]
```

### Step 18: Assign fetched_serials = get_auto_serial_nos(...)

```python
fetched_serials = get_auto_serial_nos(_dict({'qty': 10, 'item_code': item_code, 'warehouse': warehouse, 'batches': list(batch_wise_serials.keys())}))
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(sorted(all_serials), fetched_serials)
```

### Step 20: Call frappe.db.set_value()

```python
frappe.db.set_value('Batch', batch1, 'expiry_date', '1980-01-01')
```

### Step 21: Assign non_expired_serials = get_auto_serial_nos(...)

```python
non_expired_serials = get_auto_serial_nos(_dict({'qty': 5, 'item_code': item_code, 'warehouse': warehouse, 'batches': [batch1]}))
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(non_expired_serials, [])
```

### Step 23: Assign fetched_sr = get_auto_serial_nos(...)

```python
fetched_sr = get_auto_serial_nos(_dict({'qty': 5, 'item_code': item_code, 'warehouse': warehouse, 'batches': [batch]}))
```

### Step 24: Call self.assertEqual()

```python
self.assertEqual(fetched_sr, sorted(expected_serials))
```


## Complete Example

```python
# Workflow
item_code = make_item(properties={'has_serial_no': 1, 'has_batch_no': 1, 'create_new_batch': 1, 'serial_no_series': 'TEST.#######'}).name
warehouse = '_Test Warehouse - _TC'
in1 = make_stock_entry(item_code=item_code, to_warehouse=warehouse, qty=5)
in2 = make_stock_entry(item_code=item_code, to_warehouse=warehouse, qty=5)
in1.reload()
in2.reload()
batch1 = get_batch_from_bundle(in1.items[0].serial_and_batch_bundle)
batch2 = get_batch_from_bundle(in2.items[0].serial_and_batch_bundle)
batch_wise_serials = {batch1: get_serial_nos_from_bundle(in1.items[0].serial_and_batch_bundle), batch2: get_serial_nos_from_bundle(in2.items[0].serial_and_batch_bundle)}
first_fetch = get_auto_serial_nos(_dict({'qty': 5, 'item_code': item_code, 'warehouse': warehouse}))
self.assertEqual(first_fetch, batch_wise_serials[batch1])
partial_fetch = get_auto_serial_nos(_dict({'qty': 2, 'item_code': item_code, 'warehouse': warehouse}))
self.assertTrue(set(partial_fetch).issubset(set(first_fetch)), msg=f'{partial_fetch} should be subset of {first_fetch}')
remaining = get_auto_serial_nos(_dict({'qty': 3, 'item_code': item_code, 'warehouse': warehouse, 'ignore_serial_nos': partial_fetch}))
self.assertEqual(sorted(remaining + partial_fetch), first_fetch)
for batch, expected_serials in batch_wise_serials.items():
    fetched_sr = get_auto_serial_nos(_dict({'qty': 5, 'item_code': item_code, 'warehouse': warehouse, 'batches': [batch]}))
    self.assertEqual(fetched_sr, sorted(expected_serials))
self.assertFalse(get_auto_serial_nos(_dict({'qty': 10, 'item_code': item_code, 'warehouse': 'Non Existing Warehouse'})))
all_serials = [sr for sr_list in batch_wise_serials.values() for sr in sr_list]
fetched_serials = get_auto_serial_nos(_dict({'qty': 10, 'item_code': item_code, 'warehouse': warehouse, 'batches': list(batch_wise_serials.keys())}))
self.assertEqual(sorted(all_serials), fetched_serials)
frappe.db.set_value('Batch', batch1, 'expiry_date', '1980-01-01')
non_expired_serials = get_auto_serial_nos(_dict({'qty': 5, 'item_code': item_code, 'warehouse': warehouse, 'batches': [batch1]}))
self.assertEqual(non_expired_serials, [])
```

## Next Steps


---

*Source: test_serial_no.py:225 | Complexity: Advanced | Last updated: 2026-02-04*