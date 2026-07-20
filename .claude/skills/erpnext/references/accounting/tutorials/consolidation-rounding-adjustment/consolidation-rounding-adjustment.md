# How To: Consolidation Rounding Adjustment

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test if the rounding adjustment is calculated correctly

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

### Step 1: '\n\t\tTest if the rounding adjustment is calculated correctly\n\t\t'

```python
'\n\t\tTest if the rounding adjustment is calculated correctly\n\t\t'
```

### Step 2: Call make_stock_entry()

```python
make_stock_entry(to_warehouse='_Test Warehouse - _TC', item_code='_Test Item', rate=8000, qty=10)
```

### Step 3: Assign unknown = init_user_and_profile(...)

```python
test_user, pos_profile = init_user_and_profile()
```

### Step 4: Assign opening_entry = create_opening_entry(...)

```python
opening_entry = create_opening_entry(pos_profile, test_user.name)
```

### Step 5: Assign inv = create_pos_invoice(...)

```python
inv = create_pos_invoice(qty=1, rate=69.5, do_not_save=True)
```

### Step 6: Call inv.append()

```python
inv.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 70})
```

### Step 7: Call inv.insert()

```python
inv.insert()
```

### Step 8: Call inv.submit()

```python
inv.submit()
```

### Step 9: Assign inv2 = create_pos_invoice(...)

```python
inv2 = create_pos_invoice(qty=1, rate=59.5, do_not_save=True)
```

### Step 10: Call inv2.append()

```python
inv2.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 60})
```

### Step 11: Call inv2.insert()

```python
inv2.insert()
```

### Step 12: Call inv2.submit()

```python
inv2.submit()
```

### Step 13: Assign closing_entry = make_closing_entry_from_opening(...)

```python
closing_entry = make_closing_entry_from_opening(opening_entry)
```

### Step 14: Call closing_entry.insert()

```python
closing_entry.insert()
```

### Step 15: Call closing_entry.submit()

```python
closing_entry.submit()
```

### Step 16: Call inv.load_from_db()

```python
inv.load_from_db()
```

### Step 17: Assign consolidated_invoice = frappe.get_doc(...)

```python
consolidated_invoice = frappe.get_doc('Sales Invoice', inv.consolidated_invoice)
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(consolidated_invoice.rounding_adjustment, 1)
```


## Complete Example

```python
# Setup
frappe.db.sql('delete from `tabPOS Invoice`')

# Workflow
'\n\t\tTest if the rounding adjustment is calculated correctly\n\t\t'
make_stock_entry(to_warehouse='_Test Warehouse - _TC', item_code='_Test Item', rate=8000, qty=10)
test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
inv = create_pos_invoice(qty=1, rate=69.5, do_not_save=True)
inv.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 70})
inv.insert()
inv.submit()
inv2 = create_pos_invoice(qty=1, rate=59.5, do_not_save=True)
inv2.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 60})
inv2.insert()
inv2.submit()
closing_entry = make_closing_entry_from_opening(opening_entry)
closing_entry.insert()
closing_entry.submit()
inv.load_from_db()
consolidated_invoice = frappe.get_doc('Sales Invoice', inv.consolidated_invoice)
self.assertEqual(consolidated_invoice.rounding_adjustment, 1)
```

## Next Steps


---

*Source: test_pos_invoice_merge_log.py:374 | Complexity: Advanced | Last updated: 2026-02-03*