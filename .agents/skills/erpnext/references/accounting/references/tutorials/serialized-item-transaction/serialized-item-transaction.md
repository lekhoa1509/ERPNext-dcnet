# How To: Serialized Item Transaction

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test serialized item transaction

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
pos = create_pos_invoice(company='_Test Company', debit_to='Debtors - _TC', account_for_change_amount='Cash - _TC', warehouse='Stores - _TC', income_account='Sales - _TC', expense_account='Cost of Goods Sold - _TC', cost_center='Main - _TC', item=se.get('items')[0].item_code, rate=1000, serial_no=[serial_nos[0]], do_not_save=1)
```

### Step 4: Call pos.append()

```python
pos.append('payments', {'mode_of_payment': 'Bank Draft', 'amount': 1000})
```

### Step 5: Call pos.insert()

```python
pos.insert()
```

### Step 6: Call pos.submit()

```python
pos.submit()
```

### Step 7: Assign pos2 = create_pos_invoice(...)

```python
pos2 = create_pos_invoice(company='_Test Company', debit_to='Debtors - _TC', account_for_change_amount='Cash - _TC', warehouse='Stores - _TC', income_account='Sales - _TC', expense_account='Cost of Goods Sold - _TC', cost_center='Main - _TC', item=se.get('items')[0].item_code, rate=1000, serial_no=[serial_nos[0]], do_not_save=1)
```

### Step 8: Call pos2.append()

```python
pos2.append('payments', {'mode_of_payment': 'Bank Draft', 'amount': 1000})
```

### Step 9: Call pos2.insert()

```python
pos2.insert()
```

### Step 10: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, pos2.submit)
```


## Complete Example

```python
# Workflow
from erpnext.stock.doctype.stock_entry.test_stock_entry import make_serialized_item
se = make_serialized_item(self, company='_Test Company', target_warehouse='Stores - _TC', cost_center='Main - _TC', expense_account='Cost of Goods Sold - _TC')
serial_nos = get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)
pos = create_pos_invoice(company='_Test Company', debit_to='Debtors - _TC', account_for_change_amount='Cash - _TC', warehouse='Stores - _TC', income_account='Sales - _TC', expense_account='Cost of Goods Sold - _TC', cost_center='Main - _TC', item=se.get('items')[0].item_code, rate=1000, serial_no=[serial_nos[0]], do_not_save=1)
pos.append('payments', {'mode_of_payment': 'Bank Draft', 'amount': 1000})
pos.insert()
pos.submit()
pos2 = create_pos_invoice(company='_Test Company', debit_to='Debtors - _TC', account_for_change_amount='Cash - _TC', warehouse='Stores - _TC', income_account='Sales - _TC', expense_account='Cost of Goods Sold - _TC', cost_center='Main - _TC', item=se.get('items')[0].item_code, rate=1000, serial_no=[serial_nos[0]], do_not_save=1)
pos2.append('payments', {'mode_of_payment': 'Bank Draft', 'amount': 1000})
pos2.insert()
self.assertRaises(frappe.ValidationError, pos2.submit)
```

## Next Steps


---

*Source: test_pos_invoice.py:447 | Complexity: Advanced | Last updated: 2026-02-03*