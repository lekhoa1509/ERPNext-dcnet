# How To: Serial No Case 1

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Create a POS Invoice with serial no
Create a Return Invoice with serial no
Create a POS Invoice with serial no again
Consolidate the invoices

The first POS Invoice should be consolidated with a separate single Merge Log
The second and third POS Invoice should be consolidated with a single Merge Log

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `frappe`
- `frappe.tests`
- `erpnext.accounts.doctype.mode_of_payment.test_mode_of_payment`
- `erpnext.accounts.doctype.pos_closing_entry.pos_closing_entry`
- `erpnext.accounts.doctype.pos_closing_entry.test_pos_closing_entry`
- `erpnext.accounts.doctype.pos_invoice.pos_invoice`
- `erpnext.accounts.doctype.pos_invoice.test_pos_invoice`
- `erpnext.accounts.doctype.pos_opening_entry.test_pos_opening_entry`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.accounts.doctype.cost_center.test_cost_center`

**Setup Required:**
```python
frappe.db.sql('delete from `tabPOS Invoice`')
```

## Step-by-Step Guide

### Step 1: '\n\t\tCreate a POS Invoice with serial no\n\t\tCreate a Return Invoice with serial no\n\t\tCreate a POS Invoice with serial no again\n\t\tConsolidate the invoices\n\n\t\tThe first POS Invoice should be consolidated with a separate single Merge Log\n\t\tThe second and third POS Invoice should be consolidated with a single Merge Log\n\t\t'

```python
'\n\t\tCreate a POS Invoice with serial no\n\t\tCreate a Return Invoice with serial no\n\t\tCreate a POS Invoice with serial no again\n\t\tConsolidate the invoices\n\n\t\tThe first POS Invoice should be consolidated with a separate single Merge Log\n\t\tThe second and third POS Invoice should be consolidated with a single Merge Log\n\t\t'
```

### Step 2: Assign se = make_serialized_item(...)

```python
se = make_serialized_item(self)
```

### Step 3: Assign serial_no = value

```python
serial_no = get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)[0]
```

### Step 4: Assign unknown = init_user_and_profile(...)

```python
test_user, pos_profile = init_user_and_profile()
```

### Step 5: Assign opening_entry = create_opening_entry(...)

```python
opening_entry = create_opening_entry(pos_profile, test_user.name)
```

### Step 6: Assign pos_inv = create_pos_invoice(...)

```python
pos_inv = create_pos_invoice(item_code='_Test Serialized Item With Series', serial_no=[serial_no], qty=1, rate=100, do_not_submit=1)
```

### Step 7: Call pos_inv.append()

```python
pos_inv.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 100})
```

### Step 8: Call pos_inv.save()

```python
pos_inv.save()
```

### Step 9: Call pos_inv.submit()

```python
pos_inv.submit()
```

### Step 10: Assign pos_inv_cn = make_sales_return(...)

```python
pos_inv_cn = make_sales_return(pos_inv.name)
```

### Step 11: Assign pos_inv_cn.paid_amount = value

```python
pos_inv_cn.paid_amount = -100
```

### Step 12: Call pos_inv_cn.submit()

```python
pos_inv_cn.submit()
```

### Step 13: Assign pos_inv2 = create_pos_invoice(...)

```python
pos_inv2 = create_pos_invoice(item_code='_Test Serialized Item With Series', serial_no=[serial_no], qty=1, rate=100, do_not_submit=1)
```

### Step 14: Call pos_inv2.append()

```python
pos_inv2.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 100})
```

### Step 15: Call pos_inv2.save()

```python
pos_inv2.save()
```

### Step 16: Call pos_inv2.submit()

```python
pos_inv2.submit()
```

### Step 17: Assign closing_entry = make_closing_entry_from_opening(...)

```python
closing_entry = make_closing_entry_from_opening(opening_entry)
```

### Step 18: Call closing_entry.insert()

```python
closing_entry.insert()
```

### Step 19: Call closing_entry.submit()

```python
closing_entry.submit()
```

### Step 20: Call pos_inv.load_from_db()

```python
pos_inv.load_from_db()
```

### Step 21: Call pos_inv2.load_from_db()

```python
pos_inv2.load_from_db()
```

### Step 22: Call self.assertNotEqual()

```python
self.assertNotEqual(pos_inv.consolidated_invoice, pos_inv2.consolidated_invoice)
```


## Complete Example

```python
# Setup
frappe.db.sql('delete from `tabPOS Invoice`')

# Workflow
'\n\t\tCreate a POS Invoice with serial no\n\t\tCreate a Return Invoice with serial no\n\t\tCreate a POS Invoice with serial no again\n\t\tConsolidate the invoices\n\n\t\tThe first POS Invoice should be consolidated with a separate single Merge Log\n\t\tThe second and third POS Invoice should be consolidated with a single Merge Log\n\t\t'
from erpnext.stock.doctype.stock_entry.test_stock_entry import make_serialized_item
se = make_serialized_item(self)
serial_no = get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)[0]
test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
pos_inv = create_pos_invoice(item_code='_Test Serialized Item With Series', serial_no=[serial_no], qty=1, rate=100, do_not_submit=1)
pos_inv.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 100})
pos_inv.save()
pos_inv.submit()
pos_inv_cn = make_sales_return(pos_inv.name)
pos_inv_cn.paid_amount = -100
pos_inv_cn.submit()
pos_inv2 = create_pos_invoice(item_code='_Test Serialized Item With Series', serial_no=[serial_no], qty=1, rate=100, do_not_submit=1)
pos_inv2.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 100})
pos_inv2.save()
pos_inv2.submit()
closing_entry = make_closing_entry_from_opening(opening_entry)
closing_entry.insert()
closing_entry.submit()
pos_inv.load_from_db()
pos_inv2.load_from_db()
self.assertNotEqual(pos_inv.consolidated_invoice, pos_inv2.consolidated_invoice)
```

## Next Steps


---

*Source: test_pos_invoice_merge_log.py:406 | Complexity: Advanced | Last updated: 2026-02-03*