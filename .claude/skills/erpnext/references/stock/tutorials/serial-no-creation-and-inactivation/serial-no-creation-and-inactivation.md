# How To: Serial No Creation And Inactivation

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test serial no creation and inactivation

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.utils`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_reconciliation.stock_reconciliation`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.stock_ledger`
- `erpnext.stock.tests.test_utils`
- `erpnext.stock.utils`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.batch.batch`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.stock_ledger`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.stock_ledger`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.batch.batch`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.batch.batch`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.batch.batch`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.batch.batch`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`


## Step-by-Step Guide

### Step 1: Assign item = create_item(...)

```python
item = create_item('_TestItemCreatedWithStockReco', is_stock_item=1)
```

### Step 2: Assign item_code = value

```python
item_code = item.name
```

### Step 3: Assign warehouse = '_Test Warehouse - _TC'

```python
warehouse = '_Test Warehouse - _TC'
```

### Step 4: Assign sr = create_stock_reconciliation(...)

```python
sr = create_stock_reconciliation(item_code=item.name, warehouse=warehouse, serial_no=['SR-CREATED-SR-NO'], qty=1, do_not_submit=True, rate=100)
```

### Step 5: Call sr.save()

```python
sr.save()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(cstr(sr.items[0].current_serial_no), '')
```

### Step 7: Call sr.submit()

```python
sr.submit()
```

### Step 8: Assign active_sr_no = frappe.get_all(...)

```python
active_sr_no = frappe.get_all('Serial No', filters={'item_code': item_code, 'warehouse': warehouse, 'status': 'Active'})
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(len(active_sr_no), 1)
```

### Step 10: Call sr.cancel()

```python
sr.cancel()
```

### Step 11: Assign active_sr_no = frappe.get_all(...)

```python
active_sr_no = frappe.get_all('Serial No', filters={'item_code': item_code, 'warehouse': warehouse, 'status': 'Active'})
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(len(active_sr_no), 0)
```

### Step 13: Assign item.has_serial_no = 1

```python
item.has_serial_no = 1
```

### Step 14: Call item.save()

```python
item.save()
```

### Step 15: Call frappe.get_doc.insert()

```python
frappe.get_doc({'doctype': 'Serial No', 'item_code': item_code, 'serial_no': 'SR-CREATED-SR-NO'}).insert()
```


## Complete Example

```python
# Workflow
item = create_item('_TestItemCreatedWithStockReco', is_stock_item=1)
if not item.has_serial_no:
    item.has_serial_no = 1
    item.save()
item_code = item.name
warehouse = '_Test Warehouse - _TC'
if not frappe.db.exists('Serial No', 'SR-CREATED-SR-NO'):
    frappe.get_doc({'doctype': 'Serial No', 'item_code': item_code, 'serial_no': 'SR-CREATED-SR-NO'}).insert()
sr = create_stock_reconciliation(item_code=item.name, warehouse=warehouse, serial_no=['SR-CREATED-SR-NO'], qty=1, do_not_submit=True, rate=100)
sr.save()
self.assertEqual(cstr(sr.items[0].current_serial_no), '')
sr.submit()
active_sr_no = frappe.get_all('Serial No', filters={'item_code': item_code, 'warehouse': warehouse, 'status': 'Active'})
self.assertEqual(len(active_sr_no), 1)
sr.cancel()
active_sr_no = frappe.get_all('Serial No', filters={'item_code': item_code, 'warehouse': warehouse, 'status': 'Active'})
self.assertEqual(len(active_sr_no), 0)
```

## Next Steps


---

*Source: test_stock_reconciliation.py:608 | Complexity: Advanced | Last updated: 2026-02-04*