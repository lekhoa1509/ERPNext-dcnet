# How To: Serialized Lcv Delivered

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: In some cases you'd want to deliver before you can know all the
landed costs, this should be allowed for serial nos too.

Case:
                - receipt a serial no @ X rate
                - delivery the serial no @ X rate
                - add LCV to receipt X + Y
                - LCV should be successful
                - delivery should reflect X+Y valuation.

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

### Step 1: "In some cases you'd want to deliver before you can know all the\n\t\tlanded costs, this should be allowed for serial nos too.\n\n\t\tCase:\n\t\t                - receipt a serial no @ X rate\n\t\t                - delivery the serial no @ X rate\n\t\t                - add LCV to receipt X + Y\n\t\t                - LCV should be successful\n\t\t                - delivery should reflect X+Y valuation.\n\t\t"

```python
"In some cases you'd want to deliver before you can know all the\n\t\tlanded costs, this should be allowed for serial nos too.\n\n\t\tCase:\n\t\t                - receipt a serial no @ X rate\n\t\t                - delivery the serial no @ X rate\n\t\t                - add LCV to receipt X + Y\n\t\t                - LCV should be successful\n\t\t                - delivery should reflect X+Y valuation.\n\t\t"
```

### Step 2: Assign serial_no = 'LCV_TEST_SR_NO'

```python
serial_no = 'LCV_TEST_SR_NO'
```

### Step 3: Assign item_code = '_Test Serialized Item'

```python
item_code = '_Test Serialized Item'
```

### Step 4: Assign warehouse = 'Stores - TCP1'

```python
warehouse = 'Stores - TCP1'
```

### Step 5: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(company='_Test Company with perpetual inventory', warehouse=warehouse, qty=1, rate=200, item_code=item_code, serial_no=[serial_no])
```

### Step 6: Assign sn_obj = SerialNoValuation(...)

```python
sn_obj = SerialNoValuation(sle=frappe._dict({'posting_date': today(), 'posting_time': nowtime(), 'item_code': '_Test Serialized Item', 'warehouse': 'Stores - TCP1', 'serial_nos': [serial_no]}))
```

### Step 7: Assign serial_no_rate = sn_obj.get_incoming_rate_of_serial_no(...)

```python
serial_no_rate = sn_obj.get_incoming_rate_of_serial_no(serial_no)
```

### Step 8: Assign dn = create_delivery_note(...)

```python
dn = create_delivery_note(item_code=item_code, company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', serial_no=[serial_no], qty=1, rate=500, cost_center='Main - TCP1', expense_account='Cost of Goods Sold - TCP1')
```

### Step 9: Assign charges = 10

```python
charges = 10
```

### Step 10: Call create_landed_cost_voucher()

```python
create_landed_cost_voucher('Purchase Receipt', pr.name, pr.company, charges=charges)
```

### Step 11: Assign new_purchase_rate = value

```python
new_purchase_rate = serial_no_rate + charges
```

### Step 12: Assign stock_value_difference = frappe.db.get_value(...)

```python
stock_value_difference = frappe.db.get_value('Stock Ledger Entry', filters={'voucher_no': dn.name, 'voucher_type': dn.doctype, 'is_cancelled': 0}, fieldname='stock_value_difference')
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(stock_value_difference, -new_purchase_rate)
```

### Step 14: Call frappe.get_doc.insert()

```python
frappe.get_doc({'doctype': 'Serial No', 'item_code': item_code, 'serial_no': serial_no}).insert()
```


## Complete Example

```python
# Workflow
"In some cases you'd want to deliver before you can know all the\n\t\tlanded costs, this should be allowed for serial nos too.\n\n\t\tCase:\n\t\t                - receipt a serial no @ X rate\n\t\t                - delivery the serial no @ X rate\n\t\t                - add LCV to receipt X + Y\n\t\t                - LCV should be successful\n\t\t                - delivery should reflect X+Y valuation.\n\t\t"
serial_no = 'LCV_TEST_SR_NO'
item_code = '_Test Serialized Item'
warehouse = 'Stores - TCP1'
if not frappe.db.exists('Serial No', serial_no):
    frappe.get_doc({'doctype': 'Serial No', 'item_code': item_code, 'serial_no': serial_no}).insert()
pr = make_purchase_receipt(company='_Test Company with perpetual inventory', warehouse=warehouse, qty=1, rate=200, item_code=item_code, serial_no=[serial_no])
sn_obj = SerialNoValuation(sle=frappe._dict({'posting_date': today(), 'posting_time': nowtime(), 'item_code': '_Test Serialized Item', 'warehouse': 'Stores - TCP1', 'serial_nos': [serial_no]}))
serial_no_rate = sn_obj.get_incoming_rate_of_serial_no(serial_no)
dn = create_delivery_note(item_code=item_code, company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', serial_no=[serial_no], qty=1, rate=500, cost_center='Main - TCP1', expense_account='Cost of Goods Sold - TCP1')
charges = 10
create_landed_cost_voucher('Purchase Receipt', pr.name, pr.company, charges=charges)
new_purchase_rate = serial_no_rate + charges
stock_value_difference = frappe.db.get_value('Stock Ledger Entry', filters={'voucher_no': dn.name, 'voucher_type': dn.doctype, 'is_cancelled': 0}, fieldname='stock_value_difference')
self.assertEqual(stock_value_difference, -new_purchase_rate)
```

## Next Steps


---

*Source: test_landed_cost_voucher.py:349 | Complexity: Advanced | Last updated: 2026-02-04*