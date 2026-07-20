# How To: 01 Unreconcile Invoice

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test 01 unreconcile invoice

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

### Step 1: Assign si1 = self.create_sales_invoice(...)

```python
si1 = self.create_sales_invoice()
```

### Step 2: Assign si2 = self.create_sales_invoice(...)

```python
si2 = self.create_sales_invoice()
```

### Step 3: Assign pe = self.create_payment_entry(...)

```python
pe = self.create_payment_entry()
```

### Step 4: Call pe.append()

```python
pe.append('references', {'reference_doctype': si1.doctype, 'reference_name': si1.name, 'allocated_amount': 100})
```

### Step 5: Call pe.append()

```python
pe.append('references', {'reference_doctype': si2.doctype, 'reference_name': si2.name, 'allocated_amount': 100})
```

### Step 6: Call pe.save.submit()

```python
pe.save().submit()
```

### Step 7: [doc.reload() for doc in [si1, si2, pe]]

```python
[doc.reload() for doc in [si1, si2, pe]]
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(si1.outstanding_amount, 0)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(si2.outstanding_amount, 0)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(pe.unallocated_amount, 0)
```

### Step 11: Assign unreconcile = frappe.get_doc(...)

```python
unreconcile = frappe.get_doc({'doctype': 'Unreconcile Payment', 'company': self.company, 'voucher_type': pe.doctype, 'voucher_no': pe.name})
```

### Step 12: Call unreconcile.add_references()

```python
unreconcile.add_references()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(len(unreconcile.allocations), 2)
```

### Step 14: Assign allocations = value

```python
allocations = [x.reference_name for x in unreconcile.allocations]
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual([si1.name, si2.name], allocations)
```

### Step 16: Call unreconcile.save.submit()

```python
unreconcile.save().submit()
```

### Step 17: [doc.reload() for doc in [si1, si2, pe]]

```python
[doc.reload() for doc in [si1, si2, pe]]
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(si1.outstanding_amount, 100)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(si2.outstanding_amount, 0)
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(len(pe.references), 1)
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(pe.unallocated_amount, 100)
```

### Step 22: Call unreconcile.remove()

```python
unreconcile.remove(x)
```


## Complete Example

```python
# Workflow
si1 = self.create_sales_invoice()
si2 = self.create_sales_invoice()
pe = self.create_payment_entry()
pe.append('references', {'reference_doctype': si1.doctype, 'reference_name': si1.name, 'allocated_amount': 100})
pe.append('references', {'reference_doctype': si2.doctype, 'reference_name': si2.name, 'allocated_amount': 100})
pe.save().submit()
[doc.reload() for doc in [si1, si2, pe]]
self.assertEqual(si1.outstanding_amount, 0)
self.assertEqual(si2.outstanding_amount, 0)
self.assertEqual(pe.unallocated_amount, 0)
unreconcile = frappe.get_doc({'doctype': 'Unreconcile Payment', 'company': self.company, 'voucher_type': pe.doctype, 'voucher_no': pe.name})
unreconcile.add_references()
self.assertEqual(len(unreconcile.allocations), 2)
allocations = [x.reference_name for x in unreconcile.allocations]
self.assertEqual([si1.name, si2.name], allocations)
for x in unreconcile.allocations:
    if x.reference_name != si1.name:
        unreconcile.remove(x)
unreconcile.save().submit()
[doc.reload() for doc in [si1, si2, pe]]
self.assertEqual(si1.outstanding_amount, 100)
self.assertEqual(si2.outstanding_amount, 0)
self.assertEqual(len(pe.references), 1)
self.assertEqual(pe.unallocated_amount, 100)
```

## Next Steps


---

*Source: test_unreconcile_payment.py:67 | Complexity: Advanced | Last updated: 2026-02-03*