# How To: Filter Posting Date

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test filter posting date

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `frappe`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `frappe.utils.data`
- `erpnext`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.party`
- `erpnext.accounts.utils`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.accounts.doctype.account.test_account`

**Setup Required:**
```python
self.create_company()
self.create_item()
self.create_customer()
self.create_account()
self.create_cost_center()
self.clear_old_entries()
```

## Step-by-Step Guide

### Step 1: Assign date1 = nowdate(...)

```python
date1 = nowdate()
```

### Step 2: Assign date2 = add_days(...)

```python
date2 = add_days(nowdate(), -1)
```

### Step 3: Assign amount = 100

```python
amount = 100
```

### Step 4: Call self.create_sales_invoice()

```python
self.create_sales_invoice(qty=1, rate=amount, posting_date=date1)
```

### Step 5: Assign si2 = self.create_sales_invoice(...)

```python
si2 = self.create_sales_invoice(qty=1, rate=amount, posting_date=date2, do_not_save=True, do_not_submit=True)
```

### Step 6: Assign si2.set_posting_time = 1

```python
si2.set_posting_time = 1
```

### Step 7: Assign si2.posting_date = date2

```python
si2.posting_date = date2
```

### Step 8: Call si2.save.submit()

```python
si2.save().submit()
```

### Step 9: Call self.create_payment_entry.save.submit()

```python
self.create_payment_entry(amount=amount, posting_date=date1).save().submit()
```

### Step 10: Call self.create_payment_entry.save.submit()

```python
self.create_payment_entry(amount=amount, posting_date=date2).save().submit()
```

### Step 11: Assign pr = self.create_payment_reconciliation(...)

```python
pr = self.create_payment_reconciliation()
```

### Step 12: Assign pr.from_invoice_date, pr.to_invoice_date = date1

```python
pr.from_invoice_date = pr.to_invoice_date = date1
```

### Step 13: Assign pr.from_payment_date, pr.to_payment_date = date1

```python
pr.from_payment_date = pr.to_payment_date = date1
```

### Step 14: Call pr.get_unreconciled_entries()

```python
pr.get_unreconciled_entries()
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(len(pr.get('invoices')), 1)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(len(pr.get('payments')), 1)
```

### Step 17: Assign pr.from_invoice_date = date2

```python
pr.from_invoice_date = date2
```

### Step 18: Assign pr.to_invoice_date = date1

```python
pr.to_invoice_date = date1
```

### Step 19: Assign pr.from_payment_date = date2

```python
pr.from_payment_date = date2
```

### Step 20: Assign pr.to_payment_date = date1

```python
pr.to_payment_date = date1
```

### Step 21: Call pr.get_unreconciled_entries()

```python
pr.get_unreconciled_entries()
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(len(pr.get('invoices')), 2)
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(len(pr.get('payments')), 2)
```


## Complete Example

```python
# Setup
self.create_company()
self.create_item()
self.create_customer()
self.create_account()
self.create_cost_center()
self.clear_old_entries()

# Workflow
date1 = nowdate()
date2 = add_days(nowdate(), -1)
amount = 100
self.create_sales_invoice(qty=1, rate=amount, posting_date=date1)
si2 = self.create_sales_invoice(qty=1, rate=amount, posting_date=date2, do_not_save=True, do_not_submit=True)
si2.set_posting_time = 1
si2.posting_date = date2
si2.save().submit()
self.create_payment_entry(amount=amount, posting_date=date1).save().submit()
self.create_payment_entry(amount=amount, posting_date=date2).save().submit()
pr = self.create_payment_reconciliation()
pr.from_invoice_date = pr.to_invoice_date = date1
pr.from_payment_date = pr.to_payment_date = date1
pr.get_unreconciled_entries()
self.assertEqual(len(pr.get('invoices')), 1)
self.assertEqual(len(pr.get('payments')), 1)
pr.from_invoice_date = date2
pr.to_invoice_date = date1
pr.from_payment_date = date2
pr.to_payment_date = date1
pr.get_unreconciled_entries()
self.assertEqual(len(pr.get('invoices')), 2)
self.assertEqual(len(pr.get('payments')), 2)
```

## Next Steps


---

*Source: test_payment_reconciliation.py:357 | Complexity: Advanced | Last updated: 2026-02-03*