# How To: Consolidation Round Off Error 3

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test consolidation round off error 3

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

### Step 1: Call make_stock_entry()

```python
make_stock_entry(to_warehouse='_Test Warehouse - _TC', item_code='_Test Item', rate=8000, qty=10)
```

### Step 2: Assign unknown = init_user_and_profile(...)

```python
test_user, pos_profile = init_user_and_profile()
```

### Step 3: Assign opening_entry = create_opening_entry(...)

```python
opening_entry = create_opening_entry(pos_profile, test_user.name)
```

### Step 4: Assign item_rates = value

```python
item_rates = [69, 59, 29]
```

### Step 5: Assign closing_entry = make_closing_entry_from_opening(...)

```python
closing_entry = make_closing_entry_from_opening(opening_entry)
```

### Step 6: Call closing_entry.insert()

```python
closing_entry.insert()
```

### Step 7: Call closing_entry.submit()

```python
closing_entry.submit()
```

### Step 8: Call inv.load_from_db()

```python
inv.load_from_db()
```

### Step 9: Assign consolidated_invoice = frappe.get_doc(...)

```python
consolidated_invoice = frappe.get_doc('Sales Invoice', inv.consolidated_invoice)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(consolidated_invoice.status, 'Return')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(consolidated_invoice.rounding_adjustment, -0.002)
```

### Step 12: Assign inv = create_pos_invoice(...)

```python
inv = create_pos_invoice(is_return=1, do_not_save=1)
```

### Step 13: Assign inv.items = value

```python
inv.items = []
```

### Step 14: Call inv.append()

```python
inv.append('taxes', {'account_head': '_Test Account VAT - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'VAT', 'doctype': 'Sales Taxes and Charges', 'rate': 15, 'included_in_print_rate': 1})
```

### Step 15: Assign inv.payments = value

```python
inv.payments = []
```

### Step 16: Call inv.append()

```python
inv.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': -157})
```

### Step 17: Assign inv.paid_amount = value

```python
inv.paid_amount = -157
```

### Step 18: Call inv.save()

```python
inv.save()
```

### Step 19: Call inv.submit()

```python
inv.submit()
```

### Step 20: Call inv.append()

```python
inv.append('items', {'item_code': '_Test Item', 'warehouse': '_Test Warehouse - _TC', 'qty': -1, 'rate': rate, 'income_account': 'Sales - _TC', 'expense_account': 'Cost of Goods Sold - _TC', 'cost_center': '_Test Cost Center - _TC'})
```


## Complete Example

```python
# Setup
frappe.db.sql('delete from `tabPOS Invoice`')

# Workflow
make_stock_entry(to_warehouse='_Test Warehouse - _TC', item_code='_Test Item', rate=8000, qty=10)
test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
item_rates = [69, 59, 29]
for _i in [1, 2]:
    inv = create_pos_invoice(is_return=1, do_not_save=1)
    inv.items = []
    for rate in item_rates:
        inv.append('items', {'item_code': '_Test Item', 'warehouse': '_Test Warehouse - _TC', 'qty': -1, 'rate': rate, 'income_account': 'Sales - _TC', 'expense_account': 'Cost of Goods Sold - _TC', 'cost_center': '_Test Cost Center - _TC'})
    inv.append('taxes', {'account_head': '_Test Account VAT - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'VAT', 'doctype': 'Sales Taxes and Charges', 'rate': 15, 'included_in_print_rate': 1})
    inv.payments = []
    inv.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': -157})
    inv.paid_amount = -157
    inv.save()
    inv.submit()
closing_entry = make_closing_entry_from_opening(opening_entry)
closing_entry.insert()
closing_entry.submit()
inv.load_from_db()
consolidated_invoice = frappe.get_doc('Sales Invoice', inv.consolidated_invoice)
self.assertEqual(consolidated_invoice.status, 'Return')
self.assertEqual(consolidated_invoice.rounding_adjustment, -0.002)
```

## Next Steps


---

*Source: test_pos_invoice_merge_log.py:320 | Complexity: Advanced | Last updated: 2026-02-03*