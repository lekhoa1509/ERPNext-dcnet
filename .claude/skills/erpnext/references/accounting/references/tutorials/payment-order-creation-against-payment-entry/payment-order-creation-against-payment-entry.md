# How To: Payment Order Creation Against Payment Entry

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test payment order creation against payment entry

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.bank_transaction.test_bank_transaction`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`


## Step-by-Step Guide

### Step 1: Assign purchase_invoice = make_purchase_invoice(...)

```python
purchase_invoice = make_purchase_invoice()
```

### Step 2: Assign payment_entry = get_payment_entry(...)

```python
payment_entry = get_payment_entry('Purchase Invoice', purchase_invoice.name, bank_account=self.gl_account)
```

### Step 3: Assign payment_entry.reference_no = '_Test_Payment_Order'

```python
payment_entry.reference_no = '_Test_Payment_Order'
```

### Step 4: Assign payment_entry.reference_date = getdate(...)

```python
payment_entry.reference_date = getdate()
```

### Step 5: Assign payment_entry.party_bank_account = value

```python
payment_entry.party_bank_account = self.bank_account
```

### Step 6: Call payment_entry.insert()

```python
payment_entry.insert()
```

### Step 7: Call payment_entry.submit()

```python
payment_entry.submit()
```

### Step 8: Assign doc = create_payment_order_against_payment_entry(...)

```python
doc = create_payment_order_against_payment_entry(payment_entry, 'Payment Entry', self.bank_account)
```

### Step 9: Assign reference_doc = value

```python
reference_doc = doc.get('references')[0]
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(reference_doc.reference_name, payment_entry.name)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(reference_doc.reference_doctype, 'Payment Entry')
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(reference_doc.supplier, '_Test Supplier')
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(reference_doc.amount, 250)
```


## Complete Example

```python
# Workflow
purchase_invoice = make_purchase_invoice()
payment_entry = get_payment_entry('Purchase Invoice', purchase_invoice.name, bank_account=self.gl_account)
payment_entry.reference_no = '_Test_Payment_Order'
payment_entry.reference_date = getdate()
payment_entry.party_bank_account = self.bank_account
payment_entry.insert()
payment_entry.submit()
doc = create_payment_order_against_payment_entry(payment_entry, 'Payment Entry', self.bank_account)
reference_doc = doc.get('references')[0]
self.assertEqual(reference_doc.reference_name, payment_entry.name)
self.assertEqual(reference_doc.reference_doctype, 'Payment Entry')
self.assertEqual(reference_doc.supplier, '_Test Supplier')
self.assertEqual(reference_doc.amount, 250)
```

## Next Steps


---

*Source: test_payment_order.py:32 | Complexity: Advanced | Last updated: 2026-02-03*