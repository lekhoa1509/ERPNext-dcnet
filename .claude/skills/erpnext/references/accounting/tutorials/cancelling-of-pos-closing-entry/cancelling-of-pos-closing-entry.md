# How To: Cancelling Of Pos Closing Entry

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test cancelling of pos closing entry

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `erpnext.accounts.doctype.accounting_dimension.test_accounting_dimension`
- `erpnext.accounts.doctype.pos_closing_entry.pos_closing_entry`
- `erpnext.accounts.doctype.pos_invoice.test_pos_invoice`
- `erpnext.accounts.doctype.pos_opening_entry.test_pos_opening_entry`
- `erpnext.accounts.doctype.pos_profile.test_pos_profile`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.selling.page.point_of_sale.point_of_sale`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.accounts.doctype.pos_invoice.pos_invoice`
- `erpnext.accounts.doctype.pos_closing_entry.test_pos_closing_entry`
- `erpnext.stock.doctype.batch.batch`
- `erpnext.accounts.doctype.sales_invoice.sales_invoice`
- `erpnext.accounts.doctype.pos_invoice.pos_invoice`


## Step-by-Step Guide

### Step 1: Assign unknown = init_user_and_profile(...)

```python
test_user, pos_profile = init_user_and_profile()
```

### Step 2: Assign opening_entry = create_opening_entry(...)

```python
opening_entry = create_opening_entry(pos_profile, test_user.name)
```

### Step 3: Assign pos_inv1 = create_pos_invoice(...)

```python
pos_inv1 = create_pos_invoice(rate=3500, do_not_submit=1)
```

### Step 4: Call pos_inv1.append()

```python
pos_inv1.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3500})
```

### Step 5: Call pos_inv1.save()

```python
pos_inv1.save()
```

### Step 6: Call pos_inv1.submit()

```python
pos_inv1.submit()
```

### Step 7: Assign pos_inv2 = create_pos_invoice(...)

```python
pos_inv2 = create_pos_invoice(rate=3200, do_not_submit=1)
```

### Step 8: Call pos_inv2.append()

```python
pos_inv2.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3200})
```

### Step 9: Call pos_inv2.save()

```python
pos_inv2.save()
```

### Step 10: Call pos_inv2.submit()

```python
pos_inv2.submit()
```

### Step 11: Assign pcv_doc = make_closing_entry_from_opening(...)

```python
pcv_doc = make_closing_entry_from_opening(opening_entry)
```

### Step 12: Assign payment = value

```python
payment = pcv_doc.payment_reconciliation[0]
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(payment.mode_of_payment, 'Cash')
```

### Step 14: Call pcv_doc.submit()

```python
pcv_doc.submit()
```

### Step 15: Call pos_inv1.load_from_db()

```python
pos_inv1.load_from_db()
```

### Step 16: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, pos_inv1.cancel)
```

### Step 17: Assign si_doc = frappe.get_doc(...)

```python
si_doc = frappe.get_doc('Sales Invoice', pos_inv1.consolidated_invoice)
```

### Step 18: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, si_doc.cancel)
```

### Step 19: Call pcv_doc.load_from_db()

```python
pcv_doc.load_from_db()
```

### Step 20: Call pcv_doc.cancel()

```python
pcv_doc.cancel()
```

### Step 21: Assign cancelled_invoice = frappe.db.get_value(...)

```python
cancelled_invoice = frappe.db.get_value('POS Invoice Merge Log', {'pos_closing_entry': pcv_doc.name}, 'consolidated_invoice')
```

### Step 22: Assign docstatus = frappe.db.get_value(...)

```python
docstatus = frappe.db.get_value('Sales Invoice', cancelled_invoice, 'docstatus')
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(docstatus, 2)
```

### Step 24: Call pos_inv1.load_from_db()

```python
pos_inv1.load_from_db()
```

### Step 25: Call self.assertEqual()

```python
self.assertEqual(pos_inv1.status, 'Paid')
```

### Step 26: Assign d.closing_amount = 6700

```python
d.closing_amount = 6700
```


## Complete Example

```python
# Workflow
test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
pos_inv1 = create_pos_invoice(rate=3500, do_not_submit=1)
pos_inv1.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3500})
pos_inv1.save()
pos_inv1.submit()
pos_inv2 = create_pos_invoice(rate=3200, do_not_submit=1)
pos_inv2.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3200})
pos_inv2.save()
pos_inv2.submit()
pcv_doc = make_closing_entry_from_opening(opening_entry)
payment = pcv_doc.payment_reconciliation[0]
self.assertEqual(payment.mode_of_payment, 'Cash')
for d in pcv_doc.payment_reconciliation:
    if d.mode_of_payment == 'Cash':
        d.closing_amount = 6700
pcv_doc.submit()
pos_inv1.load_from_db()
self.assertRaises(frappe.ValidationError, pos_inv1.cancel)
si_doc = frappe.get_doc('Sales Invoice', pos_inv1.consolidated_invoice)
self.assertRaises(frappe.ValidationError, si_doc.cancel)
pcv_doc.load_from_db()
pcv_doc.cancel()
cancelled_invoice = frappe.db.get_value('POS Invoice Merge Log', {'pos_closing_entry': pcv_doc.name}, 'consolidated_invoice')
docstatus = frappe.db.get_value('Sales Invoice', cancelled_invoice, 'docstatus')
self.assertEqual(docstatus, 2)
pos_inv1.load_from_db()
self.assertEqual(pos_inv1.status, 'Paid')
```

## Next Steps


---

*Source: test_pos_closing_entry.py:124 | Complexity: Advanced | Last updated: 2026-02-03*