# How To: Gl Entries With Perpetual Inventory

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test gl entries with perpetual inventory

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

### Step 1: Call set_depreciation_settings_in_company()

```python
set_depreciation_settings_in_company(company='_Test Company with perpetual inventory')
```

### Step 2: Assign asset_category = frappe.get_doc(...)

```python
asset_category = frappe.get_doc('Asset Category', 'Computers')
```

### Step 3: Call asset_category.append()

```python
asset_category.append('accounts', {'company_name': '_Test Company with perpetual inventory', 'fixed_asset_account': '_Test Fixed Asset - TCP1', 'accumulated_depreciation_account': '_Test Accumulated Depreciations - TCP1', 'depreciation_expense_account': '_Test Depreciations - TCP1', 'capital_work_in_progress_account': 'CWIP Account - TCP1'})
```

### Step 4: Call asset_category.save()

```python
asset_category.save()
```

### Step 5: Assign asset_repair = create_asset_repair(...)

```python
asset_repair = create_asset_repair(capitalize_repair_cost=1, stock_consumption=1, warehouse='Stores - TCP1', company='_Test Company with perpetual inventory', pi_expense_account1='Administrative Expenses - TCP1', pi_expense_account2='Legal Expenses - TCP1', item='_Test Non Stock Item', increase_in_asset_life=1, submit=1)
```

### Step 6: Assign gl_entries = frappe.db.sql(...)

```python
gl_entries = frappe.db.sql("\n\t\t\tselect\n\t\t\t\taccount,\n\t\t\t\tsum(debit) as debit,\n\t\t\t\tsum(credit) as credit\n\t\t\tfrom `tabGL Entry`\n\t\t\twhere\n\t\t\t\tvoucher_type='Asset Repair'\n\t\t\t\tand voucher_no=%s\n\t\t\tgroup by\n\t\t\t\taccount\n\t\t", asset_repair.name, as_dict=1)
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue(gl_entries)
```

### Step 8: Assign fixed_asset_account = get_asset_account(...)

```python
fixed_asset_account = get_asset_account('fixed_asset_account', asset=asset_repair.asset, company=asset_repair.company)
```

### Step 9: Assign pi_expense_accounts = value

```python
pi_expense_accounts = [pi.expense_account for pi in asset_repair.invoices]
```

### Step 10: Assign pi_repair_costs = value

```python
pi_repair_costs = [pi.repair_cost for pi in asset_repair.invoices]
```

### Step 11: Assign stock_entry_expense_account = value

```python
stock_entry_expense_account = frappe.get_doc('Stock Entry', {'asset_repair': asset_repair.name}).get('items')[0].expense_account
```

### Step 12: Assign expected_values = value

```python
expected_values = {fixed_asset_account: [asset_repair.total_repair_cost, 0], pi_expense_accounts[0]: [0, pi_repair_costs[0]], pi_expense_accounts[1]: [0, pi_repair_costs[1]], stock_entry_expense_account: [0, 100]}
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(expected_values[d.account][0], d.debit)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(expected_values[d.account][1], d.credit)
```


## Complete Example

```python
# Workflow
set_depreciation_settings_in_company(company='_Test Company with perpetual inventory')
asset_category = frappe.get_doc('Asset Category', 'Computers')
asset_category.append('accounts', {'company_name': '_Test Company with perpetual inventory', 'fixed_asset_account': '_Test Fixed Asset - TCP1', 'accumulated_depreciation_account': '_Test Accumulated Depreciations - TCP1', 'depreciation_expense_account': '_Test Depreciations - TCP1', 'capital_work_in_progress_account': 'CWIP Account - TCP1'})
asset_category.save()
asset_repair = create_asset_repair(capitalize_repair_cost=1, stock_consumption=1, warehouse='Stores - TCP1', company='_Test Company with perpetual inventory', pi_expense_account1='Administrative Expenses - TCP1', pi_expense_account2='Legal Expenses - TCP1', item='_Test Non Stock Item', increase_in_asset_life=1, submit=1)
gl_entries = frappe.db.sql("\n\t\t\tselect\n\t\t\t\taccount,\n\t\t\t\tsum(debit) as debit,\n\t\t\t\tsum(credit) as credit\n\t\t\tfrom `tabGL Entry`\n\t\t\twhere\n\t\t\t\tvoucher_type='Asset Repair'\n\t\t\t\tand voucher_no=%s\n\t\t\tgroup by\n\t\t\t\taccount\n\t\t", asset_repair.name, as_dict=1)
self.assertTrue(gl_entries)
fixed_asset_account = get_asset_account('fixed_asset_account', asset=asset_repair.asset, company=asset_repair.company)
pi_expense_accounts = [pi.expense_account for pi in asset_repair.invoices]
pi_repair_costs = [pi.repair_cost for pi in asset_repair.invoices]
stock_entry_expense_account = frappe.get_doc('Stock Entry', {'asset_repair': asset_repair.name}).get('items')[0].expense_account
expected_values = {fixed_asset_account: [asset_repair.total_repair_cost, 0], pi_expense_accounts[0]: [0, pi_repair_costs[0]], pi_expense_accounts[1]: [0, pi_repair_costs[1]], stock_entry_expense_account: [0, 100]}
for d in gl_entries:
    self.assertEqual(expected_values[d.account][0], d.debit)
    self.assertEqual(expected_values[d.account][1], d.credit)
```

## Next Steps


---

*Source: test_asset_repair.py:212 | Complexity: Advanced | Last updated: 2026-02-04*