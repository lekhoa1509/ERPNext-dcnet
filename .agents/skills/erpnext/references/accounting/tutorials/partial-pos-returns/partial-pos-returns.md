# How To: Partial Pos Returns

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test partial pos returns

## Prerequisites

**Required Modules:**
- `copy`
- `frappe`
- `frappe`
- `frappe.tests`
- `erpnext.accounts.doctype.mode_of_payment.test_mode_of_payment`
- `erpnext.accounts.doctype.pos_invoice.pos_invoice`
- `erpnext.accounts.doctype.pos_profile.test_pos_profile`
- `erpnext.accounts.doctype.sales_invoice.sales_invoice`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.accounts.doctype.pos_closing_entry.test_pos_closing_entry`
- `erpnext.accounts.doctype.pos_opening_entry.test_pos_opening_entry`
- `time`
- `time`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.accounts.doctype.loyalty_program.loyalty_program`
- `erpnext.accounts.doctype.loyalty_program.test_loyalty_program`
- `erpnext.accounts.doctype.loyalty_program.loyalty_program`
- `erpnext.accounts.doctype.pos_closing_entry.test_pos_closing_entry`
- `erpnext.accounts.doctype.pos_invoice_merge_log.pos_invoice_merge_log`
- `erpnext.accounts.doctype.pos_closing_entry.test_pos_closing_entry`
- `erpnext.accounts.doctype.pos_invoice_merge_log.pos_invoice_merge_log`
- `erpnext.accounts.doctype.pos_closing_entry.test_pos_closing_entry`
- `erpnext.accounts.doctype.pos_invoice_merge_log.pos_invoice_merge_log`
- `erpnext.stock.doctype.serial_and_batch_bundle.serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.stock.doctype.serial_and_batch_bundle.serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.stock.doctype.serial_and_batch_bundle.serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.stock.serial_batch_bundle`
- `erpnext.accounts.doctype.pricing_rule.test_pricing_rule`
- `erpnext.accounts.doctype.pos_invoice_merge_log.test_pos_invoice_merge_log`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.accounts.doctype.pos_invoice.pos_invoice`
- `erpnext.accounts.doctype.pos_invoice_merge_log.test_pos_invoice_merge_log`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.stock.doctype.item.test_item`


## Step-by-Step Guide

### Step 1: Assign se = make_serialized_item(...)

```python
se = make_serialized_item(self, company='_Test Company', target_warehouse='Stores - _TC', cost_center='Main - _TC', expense_account='Cost of Goods Sold - _TC')
```

### Step 2: Assign serial_nos = get_serial_nos_from_bundle(...)

```python
serial_nos = get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)
```

### Step 3: Assign pos = create_pos_invoice(...)

```python
pos = create_pos_invoice(company='_Test Company', debit_to='Debtors - _TC', account_for_change_amount='Cash - _TC', warehouse='Stores - _TC', income_account='Sales - _TC', expense_account='Cost of Goods Sold - _TC', cost_center='Main - _TC', item=se.get('items')[0].item_code, serial_no=serial_nos, qty=2, rate=1000, do_not_save=1)
```

### Step 4: Call pos.append()

```python
pos.append('payments', {'mode_of_payment': 'Cash', 'amount': 2000, 'default': 1})
```

### Step 5: Call pos.insert()

```python
pos.insert()
```

### Step 6: Call pos.submit()

```python
pos.submit()
```

### Step 7: Call pos.reload()

```python
pos.reload()
```

### Step 8: Assign pos_return1 = make_sales_return(...)

```python
pos_return1 = make_sales_return(pos.name)
```

### Step 9: Assign unknown.qty = value

```python
pos_return1.get('items')[0].qty = -1
```

### Step 10: Call pos_return1.set()

```python
pos_return1.set('payments', [])
```

### Step 11: Call pos_return1.append()

```python
pos_return1.append('payments', {'mode_of_payment': 'Cash', 'amount': -1000, 'default': 1})
```

### Step 12: Assign pos_return1.paid_amount = value

```python
pos_return1.paid_amount = -1000
```

### Step 13: Call pos_return1.submit()

```python
pos_return1.submit()
```

### Step 14: Call pos_return1.reload()

```python
pos_return1.reload()
```

### Step 15: Assign bundle_id = frappe.get_doc(...)

```python
bundle_id = frappe.get_doc('Serial and Batch Bundle', pos_return1.get('items')[0].serial_and_batch_bundle)
```

### Step 16: Call bundle_id.load_from_db()

```python
bundle_id.load_from_db()
```

### Step 17: Assign serial_no = value

```python
serial_no = bundle_id.entries[0].serial_no
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(serial_no, serial_nos[0])
```

### Step 19: Assign pos_return2 = make_sales_return(...)

```python
pos_return2 = make_sales_return(pos.name)
```

### Step 20: Call pos_return2.set()

```python
pos_return2.set('payments', [])
```

### Step 21: Call pos_return2.append()

```python
pos_return2.append('payments', {'mode_of_payment': 'Cash', 'amount': -1000, 'default': 1})
```

### Step 22: Assign pos_return2.paid_amount = value

```python
pos_return2.paid_amount = -1000
```

### Step 23: Call pos_return2.submit()

```python
pos_return2.submit()
```

### Step 24: Call self.assertEqual()

```python
self.assertEqual(pos_return2.get('items')[0].qty, -1)
```

### Step 25: Assign serial_no = value

```python
serial_no = get_serial_nos_from_bundle(pos_return2.get('items')[0].serial_and_batch_bundle)[0]
```

### Step 26: Call self.assertEqual()

```python
self.assertEqual(serial_no, serial_nos[1])
```


## Complete Example

```python
# Workflow
from erpnext.stock.doctype.stock_entry.test_stock_entry import make_serialized_item
se = make_serialized_item(self, company='_Test Company', target_warehouse='Stores - _TC', cost_center='Main - _TC', expense_account='Cost of Goods Sold - _TC')
serial_nos = get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)
pos = create_pos_invoice(company='_Test Company', debit_to='Debtors - _TC', account_for_change_amount='Cash - _TC', warehouse='Stores - _TC', income_account='Sales - _TC', expense_account='Cost of Goods Sold - _TC', cost_center='Main - _TC', item=se.get('items')[0].item_code, serial_no=serial_nos, qty=2, rate=1000, do_not_save=1)
pos.append('payments', {'mode_of_payment': 'Cash', 'amount': 2000, 'default': 1})
pos.insert()
pos.submit()
pos.reload()
pos_return1 = make_sales_return(pos.name)
pos_return1.get('items')[0].qty = -1
pos_return1.set('payments', [])
pos_return1.append('payments', {'mode_of_payment': 'Cash', 'amount': -1000, 'default': 1})
pos_return1.paid_amount = -1000
pos_return1.submit()
pos_return1.reload()
bundle_id = frappe.get_doc('Serial and Batch Bundle', pos_return1.get('items')[0].serial_and_batch_bundle)
bundle_id.load_from_db()
serial_no = bundle_id.entries[0].serial_no
self.assertEqual(serial_no, serial_nos[0])
pos_return2 = make_sales_return(pos.name)
pos_return2.set('payments', [])
pos_return2.append('payments', {'mode_of_payment': 'Cash', 'amount': -1000, 'default': 1})
pos_return2.paid_amount = -1000
pos_return2.submit()
self.assertEqual(pos_return2.get('items')[0].qty, -1)
serial_no = get_serial_nos_from_bundle(pos_return2.get('items')[0].serial_and_batch_bundle)[0]
self.assertEqual(serial_no, serial_nos[1])
```

## Next Steps


---

*Source: test_pos_invoice.py:303 | Complexity: Advanced | Last updated: 2026-02-03*