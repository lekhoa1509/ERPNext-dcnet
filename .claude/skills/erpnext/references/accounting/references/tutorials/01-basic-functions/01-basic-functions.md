# How To: 01 Basic Functions

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test 01 basic functions

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe`
- `frappe.query_builder.functions`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.accounts.doctype.payment_request.payment_request`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.test.accounts_mixin`
- `erpnext.accounts.utils`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.accounts.doctype.account.test_account`


## Step-by-Step Guide

### Step 1: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debit_to, parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100)
```

### Step 2: Assign preq = frappe.get_doc(...)

```python
preq = frappe.get_doc(make_payment_request(dt=si.doctype, dn=si.name, payment_request_type='Inward', party_type='Customer', party=si.customer))
```

### Step 3: Call preq.save.submit()

```python
preq.save().submit()
```

### Step 4: Assign ral = frappe.new_doc(...)

```python
ral = frappe.new_doc('Repost Accounting Ledger')
```

### Step 5: Assign ral.company = value

```python
ral.company = self.company
```

### Step 6: Assign ral.delete_cancelled_entries = True

```python
ral.delete_cancelled_entries = True
```

### Step 7: Call ral.append()

```python
ral.append('vouchers', {'voucher_type': si.doctype, 'voucher_no': si.name})
```

### Step 8: Call ral.append()

```python
ral.append('vouchers', {'voucher_type': preq.doctype, 'voucher_no': preq.name})
```

### Step 9: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, ral.save)
```

### Step 10: Call ral.vouchers.pop()

```python
ral.vouchers.pop()
```

### Step 11: Call preq.cancel()

```python
preq.cancel()
```

### Step 12: Call preq.delete()

```python
preq.delete()
```

### Step 13: Assign pe = get_payment_entry(...)

```python
pe = get_payment_entry(si.doctype, si.name)
```

### Step 14: Call pe.save.submit()

```python
pe.save().submit()
```

### Step 15: Call ral.append()

```python
ral.append('vouchers', {'voucher_type': pe.doctype, 'voucher_no': pe.name})
```

### Step 16: Call ral.save()

```python
ral.save()
```

### Step 17: Assign gle = frappe.db.get_all(...)

```python
gle = frappe.db.get_all('GL Entry', filters={'voucher_no': si.name, 'account': self.debit_to})
```

### Step 18: Call frappe.db.set_value()

```python
frappe.db.set_value('GL Entry', gle[0], 'debit', 90)
```

### Step 19: Assign gl = qb.DocType(...)

```python
gl = qb.DocType('GL Entry')
```

### Step 20: Assign res = qb.from_.select.where.run(...)

```python
res = qb.from_(gl).select(gl.voucher_no, Sum(gl.debit).as_('debit'), Sum(gl.credit).as_('credit')).where((gl.voucher_no == si.name) & (gl.is_cancelled == 0)).run()
```

### Step 21: Call self.assertNotEqual()

```python
self.assertNotEqual(res[0], (si.name, 100, 100))
```

### Step 22: Call ral.save.submit()

```python
ral.save().submit()
```

### Step 23: Assign res = qb.from_.select.where.run(...)

```python
res = qb.from_(gl).select(gl.voucher_no, Sum(gl.debit).as_('debit'), Sum(gl.credit).as_('credit')).where((gl.voucher_no == si.name) & (gl.is_cancelled == 0)).run()
```

### Step 24: Call self.assertEqual()

```python
self.assertEqual(res[0], (si.name, 100, 100))
```


## Complete Example

```python
# Workflow
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debit_to, parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100)
preq = frappe.get_doc(make_payment_request(dt=si.doctype, dn=si.name, payment_request_type='Inward', party_type='Customer', party=si.customer))
preq.save().submit()
ral = frappe.new_doc('Repost Accounting Ledger')
ral.company = self.company
ral.delete_cancelled_entries = True
ral.append('vouchers', {'voucher_type': si.doctype, 'voucher_no': si.name})
ral.append('vouchers', {'voucher_type': preq.doctype, 'voucher_no': preq.name})
self.assertRaises(frappe.ValidationError, ral.save)
ral.vouchers.pop()
preq.cancel()
preq.delete()
pe = get_payment_entry(si.doctype, si.name)
pe.save().submit()
ral.append('vouchers', {'voucher_type': pe.doctype, 'voucher_no': pe.name})
ral.save()
gle = frappe.db.get_all('GL Entry', filters={'voucher_no': si.name, 'account': self.debit_to})
frappe.db.set_value('GL Entry', gle[0], 'debit', 90)
gl = qb.DocType('GL Entry')
res = qb.from_(gl).select(gl.voucher_no, Sum(gl.debit).as_('debit'), Sum(gl.credit).as_('credit')).where((gl.voucher_no == si.name) & (gl.is_cancelled == 0)).run()
self.assertNotEqual(res[0], (si.name, 100, 100))
ral.save().submit()
res = qb.from_(gl).select(gl.voucher_no, Sum(gl.debit).as_('debit'), Sum(gl.credit).as_('credit')).where((gl.voucher_no == si.name) & (gl.is_cancelled == 0)).run()
self.assertEqual(res[0], (si.name, 100, 100))
```

## Next Steps


---

*Source: test_repost_accounting_ledger.py:34 | Complexity: Advanced | Last updated: 2026-02-03*