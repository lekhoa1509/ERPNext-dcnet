# How To: Closing Entries With Sales Invoice

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test closing entries with sales invoice

## Prerequisites

- [ ] Setup code must be executed first

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

**Setup Required:**
```python
frappe.db.sql('delete from `tabPOS Opening Entry`')
make_stock_entry(target='_Test Warehouse - _TC', qty=2, basic_rate=100)
```

## Step-by-Step Guide

### Step 1: Assign unknown = init_user_and_profile(...)

```python
test_user, pos_profile = init_user_and_profile()
```

### Step 2: Assign opening_entry = create_opening_entry(...)

```python
opening_entry = create_opening_entry(pos_profile, test_user.name)
```

### Step 3: Assign pos_si = create_sales_invoice(...)

```python
pos_si = create_sales_invoice(qty=10, is_created_using_pos=1, pos_profile=pos_profile.name, do_not_save=1)
```

### Step 4: Call pos_si.append()

```python
pos_si.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 1000})
```

### Step 5: Call pos_si.save()

```python
pos_si.save()
```

### Step 6: Call pos_si.submit()

```python
pos_si.submit()
```

### Step 7: Assign pos_si2 = create_sales_invoice(...)

```python
pos_si2 = create_sales_invoice(qty=5, is_created_using_pos=1, pos_profile=pos_profile.name, do_not_save=11)
```

### Step 8: Call pos_si2.append()

```python
pos_si2.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 1000})
```

### Step 9: Call pos_si2.save()

```python
pos_si2.save()
```

### Step 10: Call pos_si2.submit()

```python
pos_si2.submit()
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

### Step 15: Call self.assertEqual()

```python
self.assertEqual(pcv_doc.total_quantity, 15)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(pcv_doc.net_total, 1500)
```

### Step 17: Call pos_si2.reload()

```python
pos_si2.reload()
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(pos_si2.pos_closing_entry, pcv_doc.name)
```

### Step 19: Assign d.closing_amount = 1500

```python
d.closing_amount = 1500
```


## Complete Example

```python
# Setup
frappe.db.sql('delete from `tabPOS Opening Entry`')
make_stock_entry(target='_Test Warehouse - _TC', qty=2, basic_rate=100)

# Workflow
test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
pos_si = create_sales_invoice(qty=10, is_created_using_pos=1, pos_profile=pos_profile.name, do_not_save=1)
pos_si.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 1000})
pos_si.save()
pos_si.submit()
pos_si2 = create_sales_invoice(qty=5, is_created_using_pos=1, pos_profile=pos_profile.name, do_not_save=11)
pos_si2.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 1000})
pos_si2.save()
pos_si2.submit()
pcv_doc = make_closing_entry_from_opening(opening_entry)
payment = pcv_doc.payment_reconciliation[0]
self.assertEqual(payment.mode_of_payment, 'Cash')
for d in pcv_doc.payment_reconciliation:
    if d.mode_of_payment == 'Cash':
        d.closing_amount = 1500
pcv_doc.submit()
self.assertEqual(pcv_doc.total_quantity, 15)
self.assertEqual(pcv_doc.net_total, 1500)
pos_si2.reload()
self.assertEqual(pos_si2.pos_closing_entry, pcv_doc.name)
```

## Next Steps


---

*Source: test_pos_closing_entry.py:305 | Complexity: Advanced | Last updated: 2026-02-03*