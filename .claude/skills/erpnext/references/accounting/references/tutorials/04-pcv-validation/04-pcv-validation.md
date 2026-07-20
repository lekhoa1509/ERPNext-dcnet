# How To: 04 Pcv Validation

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test 04 pcv validation

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

### Step 1: Assign gl = frappe.qb.DocType(...)

```python
gl = frappe.qb.DocType('GL Entry')
```

### Step 2: Call qb.from_.delete.where.run()

```python
qb.from_(gl).delete().where(gl.company == self.company).run()
```

### Step 3: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debit_to, parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100)
```

### Step 4: Assign fy = get_fiscal_year(...)

```python
fy = get_fiscal_year(today(), company=self.company)
```

### Step 5: Assign pcv = frappe.get_doc(...)

```python
pcv = frappe.get_doc({'doctype': 'Period Closing Voucher', 'transaction_date': today(), 'period_start_date': fy[1], 'period_end_date': today(), 'company': self.company, 'fiscal_year': fy[0], 'cost_center': self.cost_center, 'closing_account_head': self.retained_earnings, 'remarks': 'test'})
```

### Step 6: Call pcv.save.submit()

```python
pcv.save().submit()
```

### Step 7: Assign ral = frappe.new_doc(...)

```python
ral = frappe.new_doc('Repost Accounting Ledger')
```

### Step 8: Assign ral.company = value

```python
ral.company = self.company
```

### Step 9: Call ral.append()

```python
ral.append('vouchers', {'voucher_type': si.doctype, 'voucher_no': si.name})
```

### Step 10: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, ral.save)
```

### Step 11: Call pcv.reload()

```python
pcv.reload()
```

### Step 12: Call pcv.cancel()

```python
pcv.cancel()
```

### Step 13: Call pcv.delete()

```python
pcv.delete()
```


## Complete Example

```python
# Workflow
gl = frappe.qb.DocType('GL Entry')
qb.from_(gl).delete().where(gl.company == self.company).run()
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debit_to, parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100)
fy = get_fiscal_year(today(), company=self.company)
pcv = frappe.get_doc({'doctype': 'Period Closing Voucher', 'transaction_date': today(), 'period_start_date': fy[1], 'period_end_date': today(), 'company': self.company, 'fiscal_year': fy[0], 'cost_center': self.cost_center, 'closing_account_head': self.retained_earnings, 'remarks': 'test'})
pcv.save().submit()
ral = frappe.new_doc('Repost Accounting Ledger')
ral.company = self.company
ral.append('vouchers', {'voucher_type': si.doctype, 'voucher_no': si.name})
self.assertRaises(frappe.ValidationError, ral.save)
pcv.reload()
pcv.cancel()
pcv.delete()
```

## Next Steps


---

*Source: test_repost_accounting_ledger.py:125 | Complexity: Advanced | Last updated: 2026-02-03*