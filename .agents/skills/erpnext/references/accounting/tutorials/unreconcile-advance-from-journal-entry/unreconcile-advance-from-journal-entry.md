# How To: Unreconcile Advance From Journal Entry

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test unreconcile advance from journal entry

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.party`
- `erpnext.accounts.test.accounts_mixin`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`


## Step-by-Step Guide

### Step 1: Assign po = create_purchase_order(...)

```python
po = create_purchase_order(company=self.company, supplier=self.supplier, item=self.item, qty=1, rate=100, transaction_date=today(), do_not_submit=False)
```

### Step 2: Assign je = frappe.get_doc(...)

```python
je = frappe.get_doc({'doctype': 'Journal Entry', 'company': self.company, 'voucher_type': 'Journal Entry', 'posting_date': po.transaction_date, 'multi_currency': True, 'accounts': [{'account': 'Creditors - _TC', 'party_type': 'Supplier', 'party': po.supplier, 'debit_in_account_currency': 100, 'is_advance': 'Yes', 'reference_type': po.doctype, 'reference_name': po.name}, {'account': 'Cash - _TC', 'credit_in_account_currency': 100}]})
```

### Step 3: Call je.save.submit()

```python
je.save().submit()
```

### Step 4: Call po.reload()

```python
po.reload()
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(po.advance_paid, 100)
```

### Step 6: Assign unreconcile = frappe.get_doc(...)

```python
unreconcile = frappe.get_doc({'doctype': 'Unreconcile Payment', 'company': self.company, 'voucher_type': je.doctype, 'voucher_no': je.name})
```

### Step 7: Call unreconcile.add_references()

```python
unreconcile.add_references()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(len(unreconcile.allocations), 1)
```

### Step 9: Assign allocations = value

```python
allocations = [x.reference_name for x in unreconcile.allocations]
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual([po.name], allocations)
```

### Step 11: Call unreconcile.save.submit()

```python
unreconcile.save().submit()
```

### Step 12: Call po.reload()

```python
po.reload()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(po.advance_paid, 0)
```


## Complete Example

```python
# Workflow
po = create_purchase_order(company=self.company, supplier=self.supplier, item=self.item, qty=1, rate=100, transaction_date=today(), do_not_submit=False)
je = frappe.get_doc({'doctype': 'Journal Entry', 'company': self.company, 'voucher_type': 'Journal Entry', 'posting_date': po.transaction_date, 'multi_currency': True, 'accounts': [{'account': 'Creditors - _TC', 'party_type': 'Supplier', 'party': po.supplier, 'debit_in_account_currency': 100, 'is_advance': 'Yes', 'reference_type': po.doctype, 'reference_name': po.name}, {'account': 'Cash - _TC', 'credit_in_account_currency': 100}]})
je.save().submit()
po.reload()
self.assertEqual(po.advance_paid, 100)
unreconcile = frappe.get_doc({'doctype': 'Unreconcile Payment', 'company': self.company, 'voucher_type': je.doctype, 'voucher_no': je.name})
unreconcile.add_references()
self.assertEqual(len(unreconcile.allocations), 1)
allocations = [x.reference_name for x in unreconcile.allocations]
self.assertEqual([po.name], allocations)
unreconcile.save().submit()
po.reload()
self.assertEqual(po.advance_paid, 0)
```

## Next Steps


---

*Source: test_unreconcile_payment.py:490 | Complexity: Advanced | Last updated: 2026-02-03*