# How To: Gl Entries With Periodical Inventory

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test gl entries with periodical inventory

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe`
- `frappe.query_builder.functions`
- `frappe.tests`
- `frappe.utils`
- `erpnext.assets.doctype.asset.asset`
- `erpnext.assets.doctype.asset.test_asset`
- `erpnext.assets.doctype.asset_depreciation_schedule.asset_depreciation_schedule`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`


## Step-by-Step Guide

### Step 1: Call frappe.db.set_value()

```python
frappe.db.set_value('Company', '_Test Company', 'default_expense_account', 'Cost of Goods Sold - _TC')
```

### Step 2: Assign asset_repair = create_asset_repair(...)

```python
asset_repair = create_asset_repair(capitalize_repair_cost=1, stock_consumption=1, increase_in_asset_life=1, item='_Test Non Stock Item', submit=1)
```

### Step 3: Assign gl_entries = frappe.db.sql(...)

```python
gl_entries = frappe.db.sql("\n\t\t\tselect\n\t\t\t\taccount,\n\t\t\t\tsum(debit) as debit,\n\t\t\t\tsum(credit) as credit\n\t\t\tfrom `tabGL Entry`\n\t\t\twhere\n\t\t\t\tvoucher_type='Asset Repair'\n\t\t\t\tand voucher_no=%s\n\t\t\tgroup by\n\t\t\t\taccount\n\t\t", asset_repair.name, as_dict=1)
```

### Step 4: Call self.assertTrue()

```python
self.assertTrue(gl_entries)
```

### Step 5: Assign fixed_asset_account = get_asset_account(...)

```python
fixed_asset_account = get_asset_account('fixed_asset_account', asset=asset_repair.asset, company=asset_repair.company)
```

### Step 6: Assign default_expense_account = frappe.get_cached_value(...)

```python
default_expense_account = frappe.get_cached_value('Company', asset_repair.company, 'default_expense_account')
```

### Step 7: Assign pi_expense_accounts = value

```python
pi_expense_accounts = [pi.expense_account for pi in asset_repair.invoices]
```

### Step 8: Assign expected_values = value

```python
expected_values = {fixed_asset_account: [650, 0], pi_expense_accounts[0]: [0, 250], default_expense_account: [0, 100], pi_expense_accounts[1]: [0, 300]}
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(expected_values[d.account][0], d.debit)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(expected_values[d.account][1], d.credit)
```


## Complete Example

```python
# Workflow
frappe.db.set_value('Company', '_Test Company', 'default_expense_account', 'Cost of Goods Sold - _TC')
asset_repair = create_asset_repair(capitalize_repair_cost=1, stock_consumption=1, increase_in_asset_life=1, item='_Test Non Stock Item', submit=1)
gl_entries = frappe.db.sql("\n\t\t\tselect\n\t\t\t\taccount,\n\t\t\t\tsum(debit) as debit,\n\t\t\t\tsum(credit) as credit\n\t\t\tfrom `tabGL Entry`\n\t\t\twhere\n\t\t\t\tvoucher_type='Asset Repair'\n\t\t\t\tand voucher_no=%s\n\t\t\tgroup by\n\t\t\t\taccount\n\t\t", asset_repair.name, as_dict=1)
self.assertTrue(gl_entries)
fixed_asset_account = get_asset_account('fixed_asset_account', asset=asset_repair.asset, company=asset_repair.company)
default_expense_account = frappe.get_cached_value('Company', asset_repair.company, 'default_expense_account')
pi_expense_accounts = [pi.expense_account for pi in asset_repair.invoices]
expected_values = {fixed_asset_account: [650, 0], pi_expense_accounts[0]: [0, 250], default_expense_account: [0, 100], pi_expense_accounts[1]: [0, 300]}
for d in gl_entries:
    self.assertEqual(expected_values[d.account][0], d.debit)
    self.assertEqual(expected_values[d.account][1], d.credit)
```

## Next Steps


---

*Source: test_asset_repair.py:279 | Complexity: Advanced | Last updated: 2026-02-04*