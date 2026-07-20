# How To: Payment Against Invoice

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test payment against invoice

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

### Step 1: Assign si = self.create_sales_invoice(...)

```python
si = self.create_sales_invoice(qty=1, rate=200)
```

### Step 2: Assign pe = self.create_payment_entry.save.submit(...)

```python
pe = self.create_payment_entry(amount=55).save().submit()
```

### Step 3: Call self.create_payment_entry.save.submit()

```python
self.create_payment_entry(amount=35).save().submit()
```

### Step 4: Assign pr = self.create_payment_reconciliation(...)

```python
pr = self.create_payment_reconciliation()
```

### Step 5: Call pr.get_unreconciled_entries()

```python
pr.get_unreconciled_entries()
```

### Step 6: Assign invoices = value

```python
invoices = [x.as_dict() for x in pr.get('invoices')]
```

### Step 7: Assign payments = value

```python
payments = [x.as_dict() for x in pr.get('payments')]
```

### Step 8: Call pr.allocate_entries()

```python
pr.allocate_entries(frappe._dict({'invoices': invoices, 'payments': payments}))
```

### Step 9: Call pr.reconcile()

```python
pr.reconcile()
```

### Step 10: Call si.reload()

```python
si.reload()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(si.status, 'Partly Paid')
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(len(pr.get('invoices')), 1)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(pr.get('invoices')[0].get('outstanding_amount'), 110)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(pr.get('payments'), [])
```

### Step 15: Call pe.reload()

```python
pe.reload()
```

### Step 16: Call pe.cancel()

```python
pe.cancel()
```

### Step 17: Call pr.get_unreconciled_entries()

```python
pr.get_unreconciled_entries()
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(len(pr.get('invoices')), 1)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(len(pr.get('payments')), 0)
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(pr.get('invoices')[0].get('outstanding_amount'), 165)
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(flt(row.get('difference_amount')), 0.0)
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
si = self.create_sales_invoice(qty=1, rate=200)
pe = self.create_payment_entry(amount=55).save().submit()
self.create_payment_entry(amount=35).save().submit()
pr = self.create_payment_reconciliation()
pr.get_unreconciled_entries()
invoices = [x.as_dict() for x in pr.get('invoices')]
payments = [x.as_dict() for x in pr.get('payments')]
pr.allocate_entries(frappe._dict({'invoices': invoices, 'payments': payments}))
for row in pr.allocation:
    self.assertEqual(flt(row.get('difference_amount')), 0.0)
pr.reconcile()
si.reload()
self.assertEqual(si.status, 'Partly Paid')
self.assertEqual(len(pr.get('invoices')), 1)
self.assertEqual(pr.get('invoices')[0].get('outstanding_amount'), 110)
self.assertEqual(pr.get('payments'), [])
pe.reload()
pe.cancel()
pr.get_unreconciled_entries()
self.assertEqual(len(pr.get('invoices')), 1)
self.assertEqual(len(pr.get('payments')), 0)
self.assertEqual(pr.get('invoices')[0].get('outstanding_amount'), 165)
```

## Next Steps


---

*Source: test_payment_reconciliation.py:447 | Complexity: Advanced | Last updated: 2026-02-03*