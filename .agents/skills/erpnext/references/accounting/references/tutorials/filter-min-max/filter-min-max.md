# How To: Filter Min Max

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test filter min max

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

### Step 1: Call self.create_sales_invoice()

```python
self.create_sales_invoice(qty=1, rate=300)
```

### Step 2: Call self.create_sales_invoice()

```python
self.create_sales_invoice(qty=1, rate=400)
```

### Step 3: Call self.create_sales_invoice()

```python
self.create_sales_invoice(qty=1, rate=500)
```

### Step 4: Call self.create_payment_entry.save.submit()

```python
self.create_payment_entry(amount=300).save().submit()
```

### Step 5: Call self.create_payment_entry.save.submit()

```python
self.create_payment_entry(amount=400).save().submit()
```

### Step 6: Call self.create_payment_entry.save.submit()

```python
self.create_payment_entry(amount=500).save().submit()
```

### Step 7: Assign pr = self.create_payment_reconciliation(...)

```python
pr = self.create_payment_reconciliation()
```

### Step 8: Assign pr.minimum_invoice_amount = 400

```python
pr.minimum_invoice_amount = 400
```

### Step 9: Assign pr.maximum_invoice_amount = 500

```python
pr.maximum_invoice_amount = 500
```

### Step 10: Assign pr.minimum_payment_amount = 300

```python
pr.minimum_payment_amount = 300
```

### Step 11: Assign pr.maximum_payment_amount = 600

```python
pr.maximum_payment_amount = 600
```

### Step 12: Call pr.get_unreconciled_entries()

```python
pr.get_unreconciled_entries()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(len(pr.get('invoices')), 2)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(len(pr.get('payments')), 3)
```

### Step 15: Assign pr.minimum_invoice_amount = 300

```python
pr.minimum_invoice_amount = 300
```

### Step 16: Assign pr.maximum_invoice_amount = 600

```python
pr.maximum_invoice_amount = 600
```

### Step 17: Assign pr.minimum_payment_amount = 400

```python
pr.minimum_payment_amount = 400
```

### Step 18: Assign pr.maximum_payment_amount = 500

```python
pr.maximum_payment_amount = 500
```

### Step 19: Call pr.get_unreconciled_entries()

```python
pr.get_unreconciled_entries()
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(len(pr.get('invoices')), 3)
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(len(pr.get('payments')), 2)
```

### Step 22: Assign pr.minimum_invoice_amount, pr.maximum_invoice_amount, pr.minimum_payment_amount, pr.maximum_payment_amount = 0

```python
pr.minimum_invoice_amount = pr.maximum_invoice_amount = pr.minimum_payment_amount = pr.maximum_payment_amount = 0
```

### Step 23: Call pr.get_unreconciled_entries()

```python
pr.get_unreconciled_entries()
```

### Step 24: Call self.assertEqual()

```python
self.assertEqual(len(pr.get('invoices')), 3)
```

### Step 25: Call self.assertEqual()

```python
self.assertEqual(len(pr.get('payments')), 3)
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
self.create_sales_invoice(qty=1, rate=300)
self.create_sales_invoice(qty=1, rate=400)
self.create_sales_invoice(qty=1, rate=500)
self.create_payment_entry(amount=300).save().submit()
self.create_payment_entry(amount=400).save().submit()
self.create_payment_entry(amount=500).save().submit()
pr = self.create_payment_reconciliation()
pr.minimum_invoice_amount = 400
pr.maximum_invoice_amount = 500
pr.minimum_payment_amount = 300
pr.maximum_payment_amount = 600
pr.get_unreconciled_entries()
self.assertEqual(len(pr.get('invoices')), 2)
self.assertEqual(len(pr.get('payments')), 3)
pr.minimum_invoice_amount = 300
pr.maximum_invoice_amount = 600
pr.minimum_payment_amount = 400
pr.maximum_payment_amount = 500
pr.get_unreconciled_entries()
self.assertEqual(len(pr.get('invoices')), 3)
self.assertEqual(len(pr.get('payments')), 2)
pr.minimum_invoice_amount = pr.maximum_invoice_amount = pr.minimum_payment_amount = pr.maximum_payment_amount = 0
pr.get_unreconciled_entries()
self.assertEqual(len(pr.get('invoices')), 3)
self.assertEqual(len(pr.get('payments')), 3)
```

## Next Steps


---

*Source: test_payment_reconciliation.py:324 | Complexity: Advanced | Last updated: 2026-02-03*