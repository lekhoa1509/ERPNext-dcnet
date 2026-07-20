# How To: Pos Closing For Required Accounting Dimension In Pos Profile

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test case to check whether we can create POS Closing Entry without mandatory accounting dimension

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

### Step 1: '\n\t\ttest case to check whether we can create POS Closing Entry without mandatory accounting dimension\n\t\t'

```python
'\n\t\ttest case to check whether we can create POS Closing Entry without mandatory accounting dimension\n\t\t'
```

### Step 2: Call create_dimension()

```python
create_dimension()
```

### Step 3: Assign location = frappe.get_doc(...)

```python
location = frappe.get_doc('Accounting Dimension', 'Location')
```

### Step 4: Assign unknown.mandatory_for_bs = True

```python
location.dimension_defaults[0].mandatory_for_bs = True
```

### Step 5: Call location.save()

```python
location.save()
```

### Step 6: Assign pos_profile = make_pos_profile(...)

```python
pos_profile = make_pos_profile(do_not_insert=1, do_not_set_accounting_dimension=1)
```

### Step 7: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, pos_profile.insert)
```

### Step 8: Assign pos_profile.location = 'Block 1'

```python
pos_profile.location = 'Block 1'
```

### Step 9: Call pos_profile.insert()

```python
pos_profile.insert()
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue(frappe.db.exists('POS Profile', pos_profile.name))
```

### Step 11: Assign test_user = init_user_and_profile(...)

```python
test_user = init_user_and_profile(do_not_create_pos_profile=1)
```

### Step 12: Assign opening_entry = create_opening_entry(...)

```python
opening_entry = create_opening_entry(pos_profile, test_user.name)
```

### Step 13: Assign pos_inv1 = create_pos_invoice(...)

```python
pos_inv1 = create_pos_invoice(rate=350, do_not_submit=1, pos_profile=pos_profile.name)
```

### Step 14: Call pos_inv1.append()

```python
pos_inv1.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3500})
```

### Step 15: Call pos_inv1.save()

```python
pos_inv1.save()
```

### Step 16: Call pos_inv1.submit()

```python
pos_inv1.submit()
```

### Step 17: Assign accounting_dimension_department = frappe.get_doc(...)

```python
accounting_dimension_department = frappe.get_doc('Accounting Dimension', {'name': 'Department'})
```

### Step 18: Assign unknown.mandatory_for_bs = 1

```python
accounting_dimension_department.dimension_defaults[0].mandatory_for_bs = 1
```

### Step 19: Call accounting_dimension_department.save()

```python
accounting_dimension_department.save()
```

### Step 20: Assign pcv_doc = make_closing_entry_from_opening(...)

```python
pcv_doc = make_closing_entry_from_opening(opening_entry)
```

### Step 21: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, pcv_doc.submit)
```

### Step 22: Assign accounting_dimension_department = frappe.get_doc(...)

```python
accounting_dimension_department = frappe.get_doc('Accounting Dimension Detail', {'parent': 'Department'})
```

### Step 23: Assign accounting_dimension_department.mandatory_for_bs = 0

```python
accounting_dimension_department.mandatory_for_bs = 0
```

### Step 24: Call accounting_dimension_department.save()

```python
accounting_dimension_department.save()
```

### Step 25: Call disable_dimension()

```python
disable_dimension()
```


## Complete Example

```python
# Setup
frappe.db.sql('delete from `tabPOS Opening Entry`')
make_stock_entry(target='_Test Warehouse - _TC', qty=2, basic_rate=100)

# Workflow
'\n\t\ttest case to check whether we can create POS Closing Entry without mandatory accounting dimension\n\t\t'
create_dimension()
location = frappe.get_doc('Accounting Dimension', 'Location')
location.dimension_defaults[0].mandatory_for_bs = True
location.save()
pos_profile = make_pos_profile(do_not_insert=1, do_not_set_accounting_dimension=1)
self.assertRaises(frappe.ValidationError, pos_profile.insert)
pos_profile.location = 'Block 1'
pos_profile.insert()
self.assertTrue(frappe.db.exists('POS Profile', pos_profile.name))
test_user = init_user_and_profile(do_not_create_pos_profile=1)
opening_entry = create_opening_entry(pos_profile, test_user.name)
pos_inv1 = create_pos_invoice(rate=350, do_not_submit=1, pos_profile=pos_profile.name)
pos_inv1.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3500})
pos_inv1.save()
pos_inv1.submit()
accounting_dimension_department = frappe.get_doc('Accounting Dimension', {'name': 'Department'})
accounting_dimension_department.dimension_defaults[0].mandatory_for_bs = 1
accounting_dimension_department.save()
pcv_doc = make_closing_entry_from_opening(opening_entry)
self.assertRaises(frappe.ValidationError, pcv_doc.submit)
accounting_dimension_department = frappe.get_doc('Accounting Dimension Detail', {'parent': 'Department'})
accounting_dimension_department.mandatory_for_bs = 0
accounting_dimension_department.save()
disable_dimension()
```

## Next Steps


---

*Source: test_pos_closing_entry.py:167 | Complexity: Advanced | Last updated: 2026-02-03*