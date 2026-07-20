# How To: Pos Closing Without Item Code

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test if POS Closing Entry is created without item code

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

### Step 1: '\n\t\tTest if POS Closing Entry is created without item code\n\t\t'

```python
'\n\t\tTest if POS Closing Entry is created without item code\n\t\t'
```

### Step 2: Assign unknown = init_user_and_profile(...)

```python
test_user, pos_profile = init_user_and_profile()
```

### Step 3: Assign opening_entry = create_opening_entry(...)

```python
opening_entry = create_opening_entry(pos_profile, test_user.name)
```

### Step 4: Assign pos_inv = create_pos_invoice(...)

```python
pos_inv = create_pos_invoice(rate=3500, do_not_submit=1, item_name='Test Item', without_item_code=1)
```

### Step 5: Call pos_inv.append()

```python
pos_inv.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3500})
```

### Step 6: Call pos_inv.save()

```python
pos_inv.save()
```

### Step 7: Call pos_inv.submit()

```python
pos_inv.submit()
```

### Step 8: Assign pcv_doc = make_closing_entry_from_opening(...)

```python
pcv_doc = make_closing_entry_from_opening(opening_entry)
```

### Step 9: Call pcv_doc.submit()

```python
pcv_doc.submit()
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue(pcv_doc.name)
```


## Complete Example

```python
# Workflow
'\n\t\tTest if POS Closing Entry is created without item code\n\t\t'
test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
pos_inv = create_pos_invoice(rate=3500, do_not_submit=1, item_name='Test Item', without_item_code=1)
pos_inv.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3500})
pos_inv.save()
pos_inv.submit()
pcv_doc = make_closing_entry_from_opening(opening_entry)
pcv_doc.submit()
self.assertTrue(pcv_doc.name)
```

## Next Steps


---

*Source: test_pos_closing_entry.py:73 | Complexity: Advanced | Last updated: 2026-02-03*