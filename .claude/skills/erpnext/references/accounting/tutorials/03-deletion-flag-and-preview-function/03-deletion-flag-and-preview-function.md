# How To: 03 Deletion Flag And Preview Function

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test 03 deletion flag and preview function

## Prerequisites

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


## Step-by-Step Guide

### Step 1: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debit_to, parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100)
```

### Step 2: Assign pe = get_payment_entry(...)

```python
pe = get_payment_entry(si.doctype, si.name)
```

### Step 3: Call pe.save.submit()

```python
pe.save().submit()
```

### Step 4: Assign ral = frappe.new_doc(...)

```python
ral = frappe.new_doc('Repost Accounting Ledger')
```

### Step 5: Assign ral.company = value

```python
ral.company = self.company
```

### Step 6: Assign ral.delete_cancelled_entries = True

```python
ral.delete_cancelled_entries = True
```

### Step 7: Call ral.append()

```python
ral.append('vouchers', {'voucher_type': si.doctype, 'voucher_no': si.name})
```

### Step 8: Call ral.append()

```python
ral.append('vouchers', {'voucher_type': pe.doctype, 'voucher_no': pe.name})
```

### Step 9: Call ral.save.submit()

```python
ral.save().submit()
```

### Step 10: Call self.assertIsNone()

```python
self.assertIsNone(frappe.db.exists('GL Entry', {'voucher_no': si.name, 'is_cancelled': 1}))
```

### Step 11: Call self.assertIsNone()

```python
self.assertIsNone(frappe.db.exists('GL Entry', {'voucher_no': pe.name, 'is_cancelled': 1}))
```


## Complete Example

```python
# Workflow
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debit_to, parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100)
pe = get_payment_entry(si.doctype, si.name)
pe.save().submit()
ral = frappe.new_doc('Repost Accounting Ledger')
ral.company = self.company
ral.delete_cancelled_entries = True
ral.append('vouchers', {'voucher_type': si.doctype, 'voucher_no': si.name})
ral.append('vouchers', {'voucher_type': pe.doctype, 'voucher_no': pe.name})
ral.save().submit()
self.assertIsNone(frappe.db.exists('GL Entry', {'voucher_no': si.name, 'is_cancelled': 1}))
self.assertIsNone(frappe.db.exists('GL Entry', {'voucher_no': pe.name, 'is_cancelled': 1}))
```

## Next Steps


---

*Source: test_repost_accounting_ledger.py:164 | Complexity: Advanced | Last updated: 2026-02-03*