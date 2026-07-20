# How To: Consolidated Invoice Item Taxes

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test consolidated invoice item taxes

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

### Step 3: Assign inv = create_pos_invoice(...)

```python
inv = create_pos_invoice(qty=1, rate=100, do_not_save=True)
```

### Step 4: Call inv.append()

```python
inv.append('taxes', {'account_head': '_Test Account VAT - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'VAT', 'doctype': 'Sales Taxes and Charges', 'rate': 9})
```

### Step 5: Call inv.insert()

```python
inv.insert()
```

### Step 6: Assign unknown.amount = value

```python
inv.payments[0].amount = inv.grand_total
```

### Step 7: Call inv.save()

```python
inv.save()
```

### Step 8: Call inv.submit()

```python
inv.submit()
```

### Step 9: Assign inv2 = create_pos_invoice(...)

```python
inv2 = create_pos_invoice(qty=1, rate=100, do_not_save=True)
```

### Step 10: Assign unknown.item_code = '_Test Item 2'

```python
inv2.get('items')[0].item_code = '_Test Item 2'
```

### Step 11: Call inv2.append()

```python
inv2.append('taxes', {'account_head': '_Test Account VAT - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'VAT', 'doctype': 'Sales Taxes and Charges', 'rate': 5})
```

### Step 12: Call inv2.insert()

```python
inv2.insert()
```

### Step 13: Assign unknown.amount = value

```python
inv2.payments[0].amount = inv.grand_total
```

### Step 14: Call inv2.save()

```python
inv2.save()
```

### Step 15: Call inv2.submit()

```python
inv2.submit()
```

### Step 16: Assign closing_entry = make_closing_entry_from_opening(...)

```python
closing_entry = make_closing_entry_from_opening(opening_entry)
```

### Step 17: Call closing_entry.insert()

```python
closing_entry.insert()
```

### Step 18: Call closing_entry.submit()

```python
closing_entry.submit()
```

### Step 19: Call inv.load_from_db()

```python
inv.load_from_db()
```

### Step 20: Assign consolidated_invoice = frappe.get_doc(...)

```python
consolidated_invoice = frappe.get_doc('Sales Invoice', inv.consolidated_invoice)
```

### Step 21: Assign expected_item_wise_tax_details = value

```python
expected_item_wise_tax_details = [{'item_row': consolidated_invoice.items[0].name, 'tax_row': consolidated_invoice.taxes[0].name, 'rate': 9.0, 'amount': 9.0, 'taxable_amount': 100.0}, {'item_row': consolidated_invoice.items[1].name, 'tax_row': consolidated_invoice.taxes[0].name, 'rate': 5.0, 'amount': 5.0, 'taxable_amount': 100.0}]
```

### Step 22: Assign actual = value

```python
actual = [{'item_row': d.item_row, 'tax_row': d.tax_row, 'rate': d.rate, 'amount': d.amount, 'taxable_amount': d.taxable_amount} for d in consolidated_invoice.get('item_wise_tax_details')]
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(actual, expected_item_wise_tax_details)
```


## Complete Example

```python
# Workflow
test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
inv = create_pos_invoice(qty=1, rate=100, do_not_save=True)
inv.append('taxes', {'account_head': '_Test Account VAT - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'VAT', 'doctype': 'Sales Taxes and Charges', 'rate': 9})
inv.insert()
inv.payments[0].amount = inv.grand_total
inv.save()
inv.submit()
inv2 = create_pos_invoice(qty=1, rate=100, do_not_save=True)
inv2.get('items')[0].item_code = '_Test Item 2'
inv2.append('taxes', {'account_head': '_Test Account VAT - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'VAT', 'doctype': 'Sales Taxes and Charges', 'rate': 5})
inv2.insert()
inv2.payments[0].amount = inv.grand_total
inv2.save()
inv2.submit()
closing_entry = make_closing_entry_from_opening(opening_entry)
closing_entry.insert()
closing_entry.submit()
inv.load_from_db()
consolidated_invoice = frappe.get_doc('Sales Invoice', inv.consolidated_invoice)
expected_item_wise_tax_details = [{'item_row': consolidated_invoice.items[0].name, 'tax_row': consolidated_invoice.taxes[0].name, 'rate': 9.0, 'amount': 9.0, 'taxable_amount': 100.0}, {'item_row': consolidated_invoice.items[1].name, 'tax_row': consolidated_invoice.taxes[0].name, 'rate': 5.0, 'amount': 5.0, 'taxable_amount': 100.0}]
actual = [{'item_row': d.item_row, 'tax_row': d.tax_row, 'rate': d.rate, 'amount': d.amount, 'taxable_amount': d.taxable_amount} for d in consolidated_invoice.get('item_wise_tax_details')]
self.assertEqual(actual, expected_item_wise_tax_details)
```

## Next Steps


---

*Source: test_pos_invoice_merge_log.py:119 | Complexity: Advanced | Last updated: 2026-02-03*