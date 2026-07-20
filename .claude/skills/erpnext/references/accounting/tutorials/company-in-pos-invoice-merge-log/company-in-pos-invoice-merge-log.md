# How To: Company In Pos Invoice Merge Log

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test if the company is fetched from POS Closing Entry

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

### Step 1: '\n\t\tTest if the company is fetched from POS Closing Entry\n\t\t'

```python
'\n\t\tTest if the company is fetched from POS Closing Entry\n\t\t'
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
pos_inv = create_pos_invoice(rate=300, do_not_submit=1)
```

### Step 5: Call pos_inv.append()

```python
pos_inv.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 300})
```

### Step 6: Call pos_inv.save()

```python
pos_inv.save()
```

### Step 7: Call pos_inv.submit()

```python
pos_inv.submit()
```

### Step 8: Assign closing_entry = make_closing_entry_from_opening(...)

```python
closing_entry = make_closing_entry_from_opening(opening_entry)
```

### Step 9: Call closing_entry.insert()

```python
closing_entry.insert()
```

### Step 10: Call closing_entry.submit()

```python
closing_entry.submit()
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(frappe.db.exists('POS Invoice Merge Log', {'pos_closing_entry': closing_entry.name}))
```

### Step 12: Assign pos_merge_log_company = frappe.db.get_value(...)

```python
pos_merge_log_company = frappe.db.get_value('POS Invoice Merge Log', {'pos_closing_entry': closing_entry.name}, 'company')
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(pos_merge_log_company, closing_entry.company)
```


## Complete Example

```python
# Setup
frappe.db.sql('delete from `tabPOS Invoice`')

# Workflow
'\n\t\tTest if the company is fetched from POS Closing Entry\n\t\t'
test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
pos_inv = create_pos_invoice(rate=300, do_not_submit=1)
pos_inv.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 300})
pos_inv.save()
pos_inv.submit()
closing_entry = make_closing_entry_from_opening(opening_entry)
closing_entry.insert()
closing_entry.submit()
self.assertTrue(frappe.db.exists('POS Invoice Merge Log', {'pos_closing_entry': closing_entry.name}))
pos_merge_log_company = frappe.db.get_value('POS Invoice Merge Log', {'pos_closing_entry': closing_entry.name}, 'company')
self.assertEqual(pos_merge_log_company, closing_entry.company)
```

## Next Steps


---

*Source: test_pos_invoice_merge_log.py:510 | Complexity: Advanced | Last updated: 2026-02-03*