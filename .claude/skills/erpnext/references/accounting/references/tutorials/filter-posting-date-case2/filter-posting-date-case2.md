# How To: Filter Posting Date Case2

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Posting date should not affect outstanding amount calculation

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

### Step 1: '\n\t\tPosting date should not affect outstanding amount calculation\n\t\t'

```python
'\n\t\tPosting date should not affect outstanding amount calculation\n\t\t'
```

### Step 2: Assign from_date = add_days(...)

```python
from_date = add_days(nowdate(), -30)
```

### Step 3: Assign to_date = nowdate(...)

```python
to_date = nowdate()
```

### Step 4: Call self.create_payment_entry.submit()

```python
self.create_payment_entry(amount=25, posting_date=from_date).submit()
```

### Step 5: Call self.create_sales_invoice()

```python
self.create_sales_invoice(rate=25, qty=1, posting_date=to_date)
```

### Step 6: Assign pr = self.create_payment_reconciliation(...)

```python
pr = self.create_payment_reconciliation()
```

### Step 7: Assign pr.from_invoice_date, pr.from_payment_date = from_date

```python
pr.from_invoice_date = pr.from_payment_date = from_date
```

### Step 8: Assign pr.to_invoice_date, pr.to_payment_date = to_date

```python
pr.to_invoice_date = pr.to_payment_date = to_date
```

### Step 9: Call pr.get_unreconciled_entries()

```python
pr.get_unreconciled_entries()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(len(pr.invoices), 1)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(len(pr.payments), 1)
```

### Step 12: Assign invoices = value

```python
invoices = [x.as_dict() for x in pr.invoices]
```

### Step 13: Assign payments = value

```python
payments = [x.as_dict() for x in pr.payments]
```

### Step 14: Call pr.allocate_entries()

```python
pr.allocate_entries(frappe._dict({'invoices': invoices, 'payments': payments}))
```

### Step 15: Call pr.reconcile()

```python
pr.reconcile()
```

### Step 16: Call pr.get_unreconciled_entries()

```python
pr.get_unreconciled_entries()
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(len(pr.invoices), 0)
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(len(pr.payments), 0)
```

### Step 19: Assign pr.from_invoice_date, pr.from_payment_date = to_date

```python
pr.from_invoice_date = pr.from_payment_date = to_date
```

### Step 20: Assign pr.to_invoice_date, pr.to_payment_date = to_date

```python
pr.to_invoice_date = pr.to_payment_date = to_date
```

### Step 21: Call pr.get_unreconciled_entries()

```python
pr.get_unreconciled_entries()
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(len(pr.invoices), 0)
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
'\n\t\tPosting date should not affect outstanding amount calculation\n\t\t'
from_date = add_days(nowdate(), -30)
to_date = nowdate()
self.create_payment_entry(amount=25, posting_date=from_date).submit()
self.create_sales_invoice(rate=25, qty=1, posting_date=to_date)
pr = self.create_payment_reconciliation()
pr.from_invoice_date = pr.from_payment_date = from_date
pr.to_invoice_date = pr.to_payment_date = to_date
pr.get_unreconciled_entries()
self.assertEqual(len(pr.invoices), 1)
self.assertEqual(len(pr.payments), 1)
invoices = [x.as_dict() for x in pr.invoices]
payments = [x.as_dict() for x in pr.payments]
pr.allocate_entries(frappe._dict({'invoices': invoices, 'payments': payments}))
pr.reconcile()
pr.get_unreconciled_entries()
self.assertEqual(len(pr.invoices), 0)
self.assertEqual(len(pr.payments), 0)
pr.from_invoice_date = pr.from_payment_date = to_date
pr.to_invoice_date = pr.to_payment_date = to_date
pr.get_unreconciled_entries()
self.assertEqual(len(pr.invoices), 0)
```

## Next Steps


---

*Source: test_payment_reconciliation.py:391 | Complexity: Advanced | Last updated: 2026-02-03*