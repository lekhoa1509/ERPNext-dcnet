# How To: Consolidated Invoice Creation

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test consolidated invoice creation

## Prerequisites

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


## Step-by-Step Guide

### Step 1: Assign unknown = init_user_and_profile(...)

```python
test_user, pos_profile = init_user_and_profile()
```

### Step 2: Assign opening_entry = create_opening_entry(...)

```python
opening_entry = create_opening_entry(pos_profile, test_user.name)
```

### Step 3: Assign pos_inv = create_pos_invoice(...)

```python
pos_inv = create_pos_invoice(rate=300, do_not_submit=1)
```

### Step 4: Call pos_inv.append()

```python
pos_inv.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 300})
```

### Step 5: Call pos_inv.save()

```python
pos_inv.save()
```

### Step 6: Call pos_inv.submit()

```python
pos_inv.submit()
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

### Step 11: Assign pos_inv3 = create_pos_invoice(...)

```python
pos_inv3 = create_pos_invoice(customer='_Test Customer 2', rate=2300, do_not_submit=1)
```

### Step 12: Call pos_inv3.append()

```python
pos_inv3.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 2300})
```

### Step 13: Call pos_inv3.save()

```python
pos_inv3.save()
```

### Step 14: Call pos_inv3.submit()

```python
pos_inv3.submit()
```

### Step 15: Assign closing_entry = make_closing_entry_from_opening(...)

```python
closing_entry = make_closing_entry_from_opening(opening_entry)
```

### Step 16: Call closing_entry.insert()

```python
closing_entry.insert()
```

### Step 17: Call closing_entry.submit()

```python
closing_entry.submit()
```

### Step 18: Call pos_inv.load_from_db()

```python
pos_inv.load_from_db()
```

### Step 19: Call self.assertTrue()

```python
self.assertTrue(frappe.db.exists('Sales Invoice', pos_inv.consolidated_invoice))
```

### Step 20: Call pos_inv3.load_from_db()

```python
pos_inv3.load_from_db()
```

### Step 21: Call self.assertTrue()

```python
self.assertTrue(frappe.db.exists('Sales Invoice', pos_inv3.consolidated_invoice))
```

### Step 22: Call self.assertFalse()

```python
self.assertFalse(pos_inv.consolidated_invoice == pos_inv3.consolidated_invoice)
```


## Complete Example

```python
# Workflow
test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
pos_inv = create_pos_invoice(rate=300, do_not_submit=1)
pos_inv.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 300})
pos_inv.save()
pos_inv.submit()
pos_inv2 = create_pos_invoice(rate=3200, do_not_submit=1)
pos_inv2.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3200})
pos_inv2.save()
pos_inv2.submit()
pos_inv3 = create_pos_invoice(customer='_Test Customer 2', rate=2300, do_not_submit=1)
pos_inv3.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 2300})
pos_inv3.save()
pos_inv3.submit()
closing_entry = make_closing_entry_from_opening(opening_entry)
closing_entry.insert()
closing_entry.submit()
pos_inv.load_from_db()
self.assertTrue(frappe.db.exists('Sales Invoice', pos_inv.consolidated_invoice))
pos_inv3.load_from_db()
self.assertTrue(frappe.db.exists('Sales Invoice', pos_inv3.consolidated_invoice))
self.assertFalse(pos_inv.consolidated_invoice == pos_inv3.consolidated_invoice)
```

## Next Steps


---

*Source: test_pos_invoice_merge_log.py:41 | Complexity: Advanced | Last updated: 2026-02-03*