# How To: Multi Currency Lcv

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test multi currency lcv

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

### Step 1: Call save_new_records()

```python
save_new_records(self.globalTestRecords['Currency Exchange'])
```

### Step 2: Assign usd_shipping = create_account(...)

```python
usd_shipping = create_account(account_name='Shipping Charges USD', parent_account='Duties and Taxes - TCP1', company='_Test Company with perpetual inventory', account_currency='USD')
```

### Step 3: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', supplier_warehouse='Stores - TCP1')
```

### Step 4: Call pr.submit()

```python
pr.submit()
```

### Step 5: Assign lcv = make_landed_cost_voucher(...)

```python
lcv = make_landed_cost_voucher(company=pr.company, receipt_document_type='Purchase Receipt', receipt_document=pr.name, charges=100, do_not_save=True)
```

### Step 6: Call lcv.append()

```python
lcv.append('taxes', {'description': 'Shipping Charges', 'expense_account': usd_shipping, 'amount': 10})
```

### Step 7: Call lcv.save()

```python
lcv.save()
```

### Step 8: Call lcv.submit()

```python
lcv.submit()
```

### Step 9: Call pr.load_from_db()

```python
pr.load_from_db()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(lcv.total_taxes_and_charges, 729)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(pr.items[0].landed_cost_voucher_amount, 729)
```

### Step 12: Assign gl_entries = frappe.get_all(...)

```python
gl_entries = frappe.get_all('GL Entry', fields=['account', 'credit', 'credit_in_account_currency'], filters={'voucher_no': pr.name, 'account': ('in', ['Shipping Charges USD - TCP1', 'Expenses Included In Valuation - TCP1'])})
```

### Step 13: Assign expected_gl_entries = value

```python
expected_gl_entries = {'Shipping Charges USD - TCP1': [629, 10], 'Expenses Included In Valuation - TCP1': [100, 100]}
```

### Step 14: Assign amounts = expected_gl_entries.get(...)

```python
amounts = expected_gl_entries.get(entry.account)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(entry.credit, amounts[0])
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(entry.credit_in_account_currency, amounts[1])
```


## Complete Example

```python
# Workflow
from erpnext.setup.doctype.currency_exchange.test_currency_exchange import save_new_records
save_new_records(self.globalTestRecords['Currency Exchange'])
usd_shipping = create_account(account_name='Shipping Charges USD', parent_account='Duties and Taxes - TCP1', company='_Test Company with perpetual inventory', account_currency='USD')
pr = make_purchase_receipt(company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', supplier_warehouse='Stores - TCP1')
pr.submit()
lcv = make_landed_cost_voucher(company=pr.company, receipt_document_type='Purchase Receipt', receipt_document=pr.name, charges=100, do_not_save=True)
lcv.append('taxes', {'description': 'Shipping Charges', 'expense_account': usd_shipping, 'amount': 10})
lcv.save()
lcv.submit()
pr.load_from_db()
self.assertEqual(lcv.total_taxes_and_charges, 729)
self.assertEqual(pr.items[0].landed_cost_voucher_amount, 729)
gl_entries = frappe.get_all('GL Entry', fields=['account', 'credit', 'credit_in_account_currency'], filters={'voucher_no': pr.name, 'account': ('in', ['Shipping Charges USD - TCP1', 'Expenses Included In Valuation - TCP1'])})
expected_gl_entries = {'Shipping Charges USD - TCP1': [629, 10], 'Expenses Included In Valuation - TCP1': [100, 100]}
for entry in gl_entries:
    amounts = expected_gl_entries.get(entry.account)
    self.assertEqual(entry.credit, amounts[0])
    self.assertEqual(entry.credit_in_account_currency, amounts[1])
```

## Next Steps


---

*Source: test_landed_cost_voucher.py:505 | Complexity: Advanced | Last updated: 2026-02-04*