# How To: 02 Deferred Accounting Valiations

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test 02 deferred accounting valiations

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
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debit_to, parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100, do_not_submit=True)
```

### Step 2: Assign unknown.enable_deferred_revenue = True

```python
si.items[0].enable_deferred_revenue = True
```

### Step 3: Assign unknown.deferred_revenue_account = value

```python
si.items[0].deferred_revenue_account = self.deferred_revenue
```

### Step 4: Assign unknown.service_start_date = nowdate(...)

```python
si.items[0].service_start_date = nowdate()
```

### Step 5: Assign unknown.service_end_date = add_days(...)

```python
si.items[0].service_end_date = add_days(nowdate(), 90)
```

### Step 6: Call si.save.submit()

```python
si.save().submit()
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


## Complete Example

```python
# Workflow
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debit_to, parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100, do_not_submit=True)
si.items[0].enable_deferred_revenue = True
si.items[0].deferred_revenue_account = self.deferred_revenue
si.items[0].service_start_date = nowdate()
si.items[0].service_end_date = add_days(nowdate(), 90)
si.save().submit()
ral = frappe.new_doc('Repost Accounting Ledger')
ral.company = self.company
ral.append('vouchers', {'voucher_type': si.doctype, 'voucher_no': si.name})
self.assertRaises(frappe.ValidationError, ral.save)
```

## Next Steps


---

*Source: test_repost_accounting_ledger.py:102 | Complexity: Advanced | Last updated: 2026-02-03*