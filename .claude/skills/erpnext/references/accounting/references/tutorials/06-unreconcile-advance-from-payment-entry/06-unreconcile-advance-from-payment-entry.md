# How To: 06 Unreconcile Advance From Payment Entry

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test 06 unreconcile advance from payment entry

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

### Step 1: Call self.enable_advance_as_liability()

```python
self.enable_advance_as_liability()
```

### Step 2: Assign so1 = self.create_sales_order(...)

```python
so1 = self.create_sales_order()
```

### Step 3: Assign so2 = self.create_sales_order(...)

```python
so2 = self.create_sales_order()
```

### Step 4: Assign pe = self.create_payment_entry(...)

```python
pe = self.create_payment_entry()
```

### Step 5: Assign pe.paid_amount = 260

```python
pe.paid_amount = 260
```

### Step 6: Call pe.append()

```python
pe.append('references', {'reference_doctype': so1.doctype, 'reference_name': so1.name, 'allocated_amount': 150})
```

### Step 7: Call pe.append()

```python
pe.append('references', {'reference_doctype': so2.doctype, 'reference_name': so2.name, 'allocated_amount': 110})
```

### Step 8: Call pe.save.submit()

```python
pe.save().submit()
```

### Step 9: Call so1.reload()

```python
so1.reload()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(so1.advance_paid, 150)
```

### Step 11: Call so2.reload()

```python
so2.reload()
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(so2.advance_paid, 110)
```

### Step 13: Assign unreconcile = frappe.get_doc(...)

```python
unreconcile = frappe.get_doc({'doctype': 'Unreconcile Payment', 'company': self.company, 'voucher_type': pe.doctype, 'voucher_no': pe.name})
```

### Step 14: Call unreconcile.add_references()

```python
unreconcile.add_references()
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(len(unreconcile.allocations), 2)
```

### Step 16: Assign allocations = value

```python
allocations = [(x.reference_name, x.allocated_amount) for x in unreconcile.allocations]
```

### Step 17: Call self.assertListEqual()

```python
self.assertListEqual(allocations, [(so1.name, 150), (so2.name, 110)])
```

### Step 18: Call unreconcile.remove()

```python
unreconcile.remove(unreconcile.allocations[0])
```

### Step 19: Call unreconcile.save.submit()

```python
unreconcile.save().submit()
```

### Step 20: Call so1.reload()

```python
so1.reload()
```

### Step 21: Call so2.reload()

```python
so2.reload()
```

### Step 22: Call pe.reload()

```python
pe.reload()
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(so1.advance_paid, 150)
```

### Step 24: Call self.assertEqual()

```python
self.assertEqual(so2.advance_paid, 0)
```

### Step 25: Call self.assertEqual()

```python
self.assertEqual(len(pe.references), 1)
```

### Step 26: Call self.assertEqual()

```python
self.assertEqual(pe.unallocated_amount, 110)
```

### Step 27: Call self.disable_advance_as_liability()

```python
self.disable_advance_as_liability()
```


## Complete Example

```python
# Workflow
self.enable_advance_as_liability()
so1 = self.create_sales_order()
so2 = self.create_sales_order()
pe = self.create_payment_entry()
pe.paid_amount = 260
pe.append('references', {'reference_doctype': so1.doctype, 'reference_name': so1.name, 'allocated_amount': 150})
pe.append('references', {'reference_doctype': so2.doctype, 'reference_name': so2.name, 'allocated_amount': 110})
pe.save().submit()
so1.reload()
self.assertEqual(so1.advance_paid, 150)
so2.reload()
self.assertEqual(so2.advance_paid, 110)
unreconcile = frappe.get_doc({'doctype': 'Unreconcile Payment', 'company': self.company, 'voucher_type': pe.doctype, 'voucher_no': pe.name})
unreconcile.add_references()
self.assertEqual(len(unreconcile.allocations), 2)
allocations = [(x.reference_name, x.allocated_amount) for x in unreconcile.allocations]
self.assertListEqual(allocations, [(so1.name, 150), (so2.name, 110)])
unreconcile.remove(unreconcile.allocations[0])
unreconcile.save().submit()
so1.reload()
so2.reload()
pe.reload()
self.assertEqual(so1.advance_paid, 150)
self.assertEqual(so2.advance_paid, 0)
self.assertEqual(len(pe.references), 1)
self.assertEqual(pe.unallocated_amount, 110)
self.disable_advance_as_liability()
```

## Next Steps


---

*Source: test_unreconcile_payment.py:377 | Complexity: Advanced | Last updated: 2026-02-03*