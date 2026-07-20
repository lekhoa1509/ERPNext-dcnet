# How To: Landed Cost Voucher For Serialized Item

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test landed cost voucher for serialized item

## Prerequisites

**Required Modules:**
- `copy`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.accounts.utils`
- `erpnext.assets.doctype.asset.test_asset`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.serial_batch_bundle`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.setup.doctype.currency_exchange.test_currency_exchange`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.serial_and_batch_bundle.serial_and_batch_bundle`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.controllers.tests.test_subcontracting_controller`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`
- `erpnext.manufacturing.doctype.work_order.test_work_order`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.subcontracting.doctype.subcontracting_order.subcontracting_order`


## Step-by-Step Guide

### Step 1: Call frappe.db.set_value()

```python
frappe.db.set_value('Item', '_Test Serialized Item', 'serial_no_series', 'SNJJ.###')
```

### Step 2: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', supplier_warehouse='Work In Progress - TCP1', get_multiple_items=True, get_taxes_and_charges=True, do_not_submit=True)
```

### Step 3: Assign unknown.item_code = '_Test Serialized Item'

```python
pr.items[0].item_code = '_Test Serialized Item'
```

### Step 4: Call pr.submit()

```python
pr.submit()
```

### Step 5: Call pr.load_from_db()

```python
pr.load_from_db()
```

### Step 6: Assign serial_no = value

```python
serial_no = get_serial_nos_from_bundle(pr.items[0].serial_and_batch_bundle)[0]
```

### Step 7: Assign sn_obj = SerialNoValuation(...)

```python
sn_obj = SerialNoValuation(sle=frappe._dict({'posting_date': today(), 'posting_time': nowtime(), 'item_code': '_Test Serialized Item', 'warehouse': 'Stores - TCP1', 'serial_nos': [serial_no]}))
```

### Step 8: Assign serial_no_rate = sn_obj.get_incoming_rate_of_serial_no(...)

```python
serial_no_rate = sn_obj.get_incoming_rate_of_serial_no(serial_no)
```

### Step 9: Call create_landed_cost_voucher()

```python
create_landed_cost_voucher('Purchase Receipt', pr.name, pr.company)
```

### Step 10: Assign sn_obj = SerialNoValuation(...)

```python
sn_obj = SerialNoValuation(sle=frappe._dict({'posting_date': today(), 'posting_time': nowtime(), 'item_code': '_Test Serialized Item', 'warehouse': 'Stores - TCP1', 'serial_nos': [serial_no]}))
```

### Step 11: Assign new_serial_no_rate = sn_obj.get_incoming_rate_of_serial_no(...)

```python
new_serial_no_rate = sn_obj.get_incoming_rate_of_serial_no(serial_no)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(new_serial_no_rate - serial_no_rate, 5.0)
```


## Complete Example

```python
# Workflow
frappe.db.set_value('Item', '_Test Serialized Item', 'serial_no_series', 'SNJJ.###')
pr = make_purchase_receipt(company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', supplier_warehouse='Work In Progress - TCP1', get_multiple_items=True, get_taxes_and_charges=True, do_not_submit=True)
pr.items[0].item_code = '_Test Serialized Item'
pr.submit()
pr.load_from_db()
serial_no = get_serial_nos_from_bundle(pr.items[0].serial_and_batch_bundle)[0]
sn_obj = SerialNoValuation(sle=frappe._dict({'posting_date': today(), 'posting_time': nowtime(), 'item_code': '_Test Serialized Item', 'warehouse': 'Stores - TCP1', 'serial_nos': [serial_no]}))
serial_no_rate = sn_obj.get_incoming_rate_of_serial_no(serial_no)
create_landed_cost_voucher('Purchase Receipt', pr.name, pr.company)
sn_obj = SerialNoValuation(sle=frappe._dict({'posting_date': today(), 'posting_time': nowtime(), 'item_code': '_Test Serialized Item', 'warehouse': 'Stores - TCP1', 'serial_nos': [serial_no]}))
new_serial_no_rate = sn_obj.get_incoming_rate_of_serial_no(serial_no)
self.assertEqual(new_serial_no_rate - serial_no_rate, 5.0)
```

## Next Steps


---

*Source: test_landed_cost_voucher.py:299 | Complexity: Advanced | Last updated: 2026-02-04*