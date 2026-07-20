# How To: Advance Payment Unlink On Order Cancellation

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test advance payment unlink on order cancellation

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `frappe`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.stock.doctype.item.test_item`

**Setup Required:**
```python
self.ple = qb.DocType('Payment Ledger Entry')
self.create_company()
self.create_item()
self.create_customer()
self.clear_old_entries()
```

## Step-by-Step Guide

### Step 1: Assign transaction_date = nowdate(...)

```python
transaction_date = nowdate()
```

### Step 2: Assign amount = 100

```python
amount = 100
```

### Step 3: Assign so = self.create_sales_order.save.submit(...)

```python
so = self.create_sales_order(qty=1, rate=amount, posting_date=transaction_date).save().submit()
```

### Step 4: Call get_payment_entry.save.submit()

```python
get_payment_entry(so.doctype, so.name).save().submit()
```

### Step 5: Call so.reload()

```python
so.reload()
```

### Step 6: Call so.cancel()

```python
so.cancel()
```

### Step 7: Assign entries = frappe.db.get_list(...)

```python
entries = frappe.db.get_list('Payment Ledger Entry', filters={'against_voucher_type': so.doctype, 'against_voucher_no': so.name, 'delinked': 0})
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(entries, [])
```

### Step 9: Call so.delete()

```python
so.delete()
```

### Step 10: Call self.assertRaises()

```python
self.assertRaises(frappe.DoesNotExistError, frappe.get_doc, so.doctype, so.name)
```


## Complete Example

```python
# Setup
self.ple = qb.DocType('Payment Ledger Entry')
self.create_company()
self.create_item()
self.create_customer()
self.clear_old_entries()

# Workflow
transaction_date = nowdate()
amount = 100
so = self.create_sales_order(qty=1, rate=amount, posting_date=transaction_date).save().submit()
get_payment_entry(so.doctype, so.name).save().submit()
so.reload()
so.cancel()
entries = frappe.db.get_list('Payment Ledger Entry', filters={'against_voucher_type': so.doctype, 'against_voucher_no': so.name, 'delinked': 0})
self.assertEqual(entries, [])
so.delete()
self.assertRaises(frappe.DoesNotExistError, frappe.get_doc, so.doctype, so.name)
```

## Next Steps


---

*Source: test_payment_ledger_entry.py:518 | Complexity: Advanced | Last updated: 2026-02-03*