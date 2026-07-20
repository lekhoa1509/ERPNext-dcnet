# How To: Pos Qty For Item

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test if quantity is calculated correctly for an item in POS Closing Entry

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

### Step 1: '\n\t\tTest if quantity is calculated correctly for an item in POS Closing Entry\n\t\t'

```python
'\n\t\tTest if quantity is calculated correctly for an item in POS Closing Entry\n\t\t'
```

### Step 2: Assign unknown = init_user_and_profile(...)

```python
test_user, pos_profile = init_user_and_profile()
```

### Step 3: Assign opening_entry = create_opening_entry(...)

```python
opening_entry = create_opening_entry(pos_profile, test_user.name)
```

### Step 4: Assign test_item_qty = get_test_item_qty(...)

```python
test_item_qty = get_test_item_qty(pos_profile)
```

### Step 5: Assign pos_inv1 = create_pos_invoice(...)

```python
pos_inv1 = create_pos_invoice(rate=3500, do_not_submit=1)
```

### Step 6: Call pos_inv1.append()

```python
pos_inv1.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3500})
```

### Step 7: Call pos_inv1.save()

```python
pos_inv1.save()
```

### Step 8: Call pos_inv1.submit()

```python
pos_inv1.submit()
```

### Step 9: Assign pos_inv2 = create_pos_invoice(...)

```python
pos_inv2 = create_pos_invoice(rate=3200, do_not_submit=1)
```

### Step 10: Call pos_inv2.append()

```python
pos_inv2.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3200})
```

### Step 11: Call pos_inv2.save()

```python
pos_inv2.save()
```

### Step 12: Call pos_inv2.submit()

```python
pos_inv2.submit()
```

### Step 13: Assign pos_return = make_sales_return(...)

```python
pos_return = make_sales_return(pos_inv2.name)
```

### Step 14: Assign pos_return.paid_amount = value

```python
pos_return.paid_amount = pos_return.grand_total
```

### Step 15: Call pos_return.save()

```python
pos_return.save()
```

### Step 16: Call pos_return.submit()

```python
pos_return.submit()
```

### Step 17: Assign pcv_doc = make_closing_entry_from_opening(...)

```python
pcv_doc = make_closing_entry_from_opening(opening_entry)
```

### Step 18: Call pcv_doc.submit()

```python
pcv_doc.submit()
```

### Step 19: Assign opening_entry = create_opening_entry(...)

```python
opening_entry = create_opening_entry(pos_profile, test_user.name)
```

### Step 20: Assign test_item_qty_after_sales = get_test_item_qty(...)

```python
test_item_qty_after_sales = get_test_item_qty(pos_profile)
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(test_item_qty_after_sales, test_item_qty - 1)
```


## Complete Example

```python
# Workflow
'\n\t\tTest if quantity is calculated correctly for an item in POS Closing Entry\n\t\t'
from erpnext.accounts.doctype.pos_invoice.pos_invoice import make_sales_return
test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
test_item_qty = get_test_item_qty(pos_profile)
pos_inv1 = create_pos_invoice(rate=3500, do_not_submit=1)
pos_inv1.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3500})
pos_inv1.save()
pos_inv1.submit()
pos_inv2 = create_pos_invoice(rate=3200, do_not_submit=1)
pos_inv2.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3200})
pos_inv2.save()
pos_inv2.submit()
pos_return = make_sales_return(pos_inv2.name)
pos_return.paid_amount = pos_return.grand_total
pos_return.save()
pos_return.submit()
pcv_doc = make_closing_entry_from_opening(opening_entry)
pcv_doc.submit()
opening_entry = create_opening_entry(pos_profile, test_user.name)
test_item_qty_after_sales = get_test_item_qty(pos_profile)
self.assertEqual(test_item_qty_after_sales, test_item_qty - 1)
```

## Next Steps


---

*Source: test_pos_closing_entry.py:90 | Complexity: Advanced | Last updated: 2026-02-03*