# How To: 05 Unreconcile Order

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test 05 unreconcile order

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

### Step 1: Assign so = self.create_sales_order(...)

```python
so = self.create_sales_order()
```

### Step 2: Assign pe = self.create_payment_entry(...)

```python
pe = self.create_payment_entry()
```

### Step 3: Assign pe.paid_amount = 100

```python
pe.paid_amount = 100
```

### Step 4: Call pe.append()

```python
pe.append('references', {'reference_doctype': so.doctype, 'reference_name': so.name, 'allocated_amount': 100})
```

### Step 5: Call pe.save.submit()

```python
pe.save().submit()
```

### Step 6: Call so.reload()

```python
so.reload()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(so.advance_paid, 100)
```

### Step 8: Assign unreconcile = frappe.get_doc(...)

```python
unreconcile = frappe.get_doc({'doctype': 'Unreconcile Payment', 'company': self.company, 'voucher_type': pe.doctype, 'voucher_no': pe.name})
```

### Step 9: Call unreconcile.add_references()

```python
unreconcile.add_references()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(len(unreconcile.allocations), 1)
```

### Step 11: Assign allocations = value

```python
allocations = [x.reference_name for x in unreconcile.allocations]
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual([so.name], allocations)
```

### Step 13: Call unreconcile.save.submit()

```python
unreconcile.save().submit()
```

### Step 14: Call so.reload()

```python
so.reload()
```

### Step 15: Call pe.reload()

```python
pe.reload()
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(so.advance_paid, 0)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(len(pe.references), 0)
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(pe.unallocated_amount, 100)
```

### Step 19: Call pe.cancel()

```python
pe.cancel()
```

### Step 20: Call so.reload()

```python
so.reload()
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(so.advance_paid, 0)
```


## Complete Example

```python
# Workflow
so = self.create_sales_order()
pe = self.create_payment_entry()
pe.paid_amount = 100
pe.append('references', {'reference_doctype': so.doctype, 'reference_name': so.name, 'allocated_amount': 100})
pe.save().submit()
so.reload()
self.assertEqual(so.advance_paid, 100)
unreconcile = frappe.get_doc({'doctype': 'Unreconcile Payment', 'company': self.company, 'voucher_type': pe.doctype, 'voucher_no': pe.name})
unreconcile.add_references()
self.assertEqual(len(unreconcile.allocations), 1)
allocations = [x.reference_name for x in unreconcile.allocations]
self.assertEqual([so.name], allocations)
unreconcile.save().submit()
so.reload()
pe.reload()
self.assertEqual(so.advance_paid, 0)
self.assertEqual(len(pe.references), 0)
self.assertEqual(pe.unallocated_amount, 100)
pe.cancel()
so.reload()
self.assertEqual(so.advance_paid, 0)
```

## Next Steps


---

*Source: test_unreconcile_payment.py:335 | Complexity: Advanced | Last updated: 2026-02-03*