# How To: 06 Repost Purchase Receipt

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test 06 repost purchase receipt

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `frappe`
- `frappe`
- `frappe.query_builder.functions`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.accounts.doctype.payment_request.payment_request`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.test.accounts_mixin`
- `erpnext.accounts.utils`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.accounts.doctype.account.test_account`

**Setup Required:**
```python
self.create_company()
self.create_customer()
self.create_item()
update_repost_settings()
```

## Step-by-Step Guide

### Step 1: Assign provisional_account = create_account(...)

```python
provisional_account = create_account(account_name='Provision Account', parent_account='Current Liabilities - _TC', company=self.company)
```

### Step 2: Assign another_provisional_account = create_account(...)

```python
another_provisional_account = create_account(account_name='Another Provision Account', parent_account='Current Liabilities - _TC', company=self.company)
```

### Step 3: Assign company = frappe.get_doc(...)

```python
company = frappe.get_doc('Company', self.company)
```

### Step 4: Assign company.enable_provisional_accounting_for_non_stock_items = 1

```python
company.enable_provisional_accounting_for_non_stock_items = 1
```

### Step 5: Assign company.default_provisional_account = provisional_account

```python
company.default_provisional_account = provisional_account
```

### Step 6: Call company.save()

```python
company.save()
```

### Step 7: Assign test_cc = value

```python
test_cc = company.cost_center
```

### Step 8: Assign default_expense_account = value

```python
default_expense_account = company.service_expense_account
```

### Step 9: Assign item = make_item(...)

```python
item = make_item(properties={'is_stock_item': 0})
```

### Step 10: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(company=self.company, item_code=item.name, rate=1000.0, qty=1.0)
```

### Step 11: Assign pr_gl_entries = get_gl_entries(...)

```python
pr_gl_entries = get_gl_entries(pr.doctype, pr.name, skip_cancelled=True)
```

### Step 12: Assign expected_pr_gles = value

```python
expected_pr_gles = [{'account': provisional_account, 'debit': 0.0, 'credit': 1000.0, 'cost_center': test_cc}, {'account': default_expense_account, 'debit': 1000.0, 'credit': 0.0, 'cost_center': test_cc}]
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(expected_pr_gles, pr_gl_entries)
```

### Step 14: Call frappe.db.set_value()

```python
frappe.db.set_value('Purchase Receipt Item', pr.items[0].name, 'provisional_expense_account', another_provisional_account)
```

### Step 15: Assign repost_doc = frappe.new_doc(...)

```python
repost_doc = frappe.new_doc('Repost Accounting Ledger')
```

### Step 16: Assign repost_doc.company = value

```python
repost_doc.company = self.company
```

### Step 17: Assign repost_doc.delete_cancelled_entries = True

```python
repost_doc.delete_cancelled_entries = True
```

### Step 18: Call repost_doc.append()

```python
repost_doc.append('vouchers', {'voucher_type': pr.doctype, 'voucher_no': pr.name})
```

### Step 19: Call repost_doc.save.submit()

```python
repost_doc.save().submit()
```

### Step 20: Assign pr_gles_after_repost = get_gl_entries(...)

```python
pr_gles_after_repost = get_gl_entries(pr.doctype, pr.name, skip_cancelled=True)
```

### Step 21: Assign expected_pr_gles_after_repost = value

```python
expected_pr_gles_after_repost = [{'account': default_expense_account, 'debit': 1000.0, 'credit': 0.0, 'cost_center': test_cc}, {'account': another_provisional_account, 'debit': 0.0, 'credit': 1000.0, 'cost_center': test_cc}]
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(len(pr_gles_after_repost), len(expected_pr_gles_after_repost))
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(expected_pr_gles_after_repost, pr_gles_after_repost)
```

### Step 24: Call repost_doc.cancel()

```python
repost_doc.cancel()
```

### Step 25: Call repost_doc.delete()

```python
repost_doc.delete()
```

### Step 26: Call pr.reload()

```python
pr.reload()
```

### Step 27: Call pr.cancel()

```python
pr.cancel()
```

### Step 28: Assign company.enable_provisional_accounting_for_non_stock_items = 0

```python
company.enable_provisional_accounting_for_non_stock_items = 0
```

### Step 29: Assign company.default_provisional_account = None

```python
company.default_provisional_account = None
```

### Step 30: Call company.save()

```python
company.save()
```


## Complete Example

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
update_repost_settings()

# Workflow
from erpnext.accounts.doctype.account.test_account import create_account
provisional_account = create_account(account_name='Provision Account', parent_account='Current Liabilities - _TC', company=self.company)
another_provisional_account = create_account(account_name='Another Provision Account', parent_account='Current Liabilities - _TC', company=self.company)
company = frappe.get_doc('Company', self.company)
company.enable_provisional_accounting_for_non_stock_items = 1
company.default_provisional_account = provisional_account
company.save()
test_cc = company.cost_center
default_expense_account = company.service_expense_account
item = make_item(properties={'is_stock_item': 0})
pr = make_purchase_receipt(company=self.company, item_code=item.name, rate=1000.0, qty=1.0)
pr_gl_entries = get_gl_entries(pr.doctype, pr.name, skip_cancelled=True)
expected_pr_gles = [{'account': provisional_account, 'debit': 0.0, 'credit': 1000.0, 'cost_center': test_cc}, {'account': default_expense_account, 'debit': 1000.0, 'credit': 0.0, 'cost_center': test_cc}]
self.assertEqual(expected_pr_gles, pr_gl_entries)
frappe.db.set_value('Purchase Receipt Item', pr.items[0].name, 'provisional_expense_account', another_provisional_account)
repost_doc = frappe.new_doc('Repost Accounting Ledger')
repost_doc.company = self.company
repost_doc.delete_cancelled_entries = True
repost_doc.append('vouchers', {'voucher_type': pr.doctype, 'voucher_no': pr.name})
repost_doc.save().submit()
pr_gles_after_repost = get_gl_entries(pr.doctype, pr.name, skip_cancelled=True)
expected_pr_gles_after_repost = [{'account': default_expense_account, 'debit': 1000.0, 'credit': 0.0, 'cost_center': test_cc}, {'account': another_provisional_account, 'debit': 0.0, 'credit': 1000.0, 'cost_center': test_cc}]
self.assertEqual(len(pr_gles_after_repost), len(expected_pr_gles_after_repost))
self.assertEqual(expected_pr_gles_after_repost, pr_gles_after_repost)
repost_doc.cancel()
repost_doc.delete()
pr.reload()
pr.cancel()
company.enable_provisional_accounting_for_non_stock_items = 0
company.default_provisional_account = None
company.save()
```

## Next Steps


---

*Source: test_repost_accounting_ledger.py:214 | Complexity: Advanced | Last updated: 2026-02-03*