# How To: Repair Cost Exceeds Available Amount

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test that repair cost cannot exceed available amount from Purchase Invoice.

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

### Step 1: 'Test that repair cost cannot exceed available amount from Purchase Invoice.'

```python
'Test that repair cost cannot exceed available amount from Purchase Invoice.'
```

### Step 2: Assign asset_repair1 = create_asset_repair(...)

```python
asset_repair1 = create_asset_repair(capitalize_repair_cost=1, item='_Test Non Stock Item', submit=1)
```

### Step 3: Assign pi_name = value

```python
pi_name = asset_repair1.invoices[0].purchase_invoice
```

### Step 4: Assign expense_account = value

```python
expense_account = asset_repair1.invoices[0].expense_account
```

### Step 5: Assign asset_repair2 = frappe.new_doc(...)

```python
asset_repair2 = frappe.new_doc('Asset Repair')
```

### Step 6: Call asset_repair2.update()

```python
asset_repair2.update({'asset': asset_repair1.asset, 'asset_name': asset_repair1.asset_name, 'failure_date': nowdate(), 'description': 'Second Repair', 'company': asset_repair1.company, 'capitalize_repair_cost': 1})
```

### Step 7: Call asset_repair2.append()

```python
asset_repair2.append('invoices', {'purchase_invoice': pi_name, 'expense_account': expense_account, 'repair_cost': 10})
```

### Step 8: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, asset_repair2.save)
```


## Complete Example

```python
# Workflow
'Test that repair cost cannot exceed available amount from Purchase Invoice.'
asset_repair1 = create_asset_repair(capitalize_repair_cost=1, item='_Test Non Stock Item', submit=1)
pi_name = asset_repair1.invoices[0].purchase_invoice
expense_account = asset_repair1.invoices[0].expense_account
asset_repair2 = frappe.new_doc('Asset Repair')
asset_repair2.update({'asset': asset_repair1.asset, 'asset_name': asset_repair1.asset_name, 'failure_date': nowdate(), 'description': 'Second Repair', 'company': asset_repair1.company, 'capitalize_repair_cost': 1})
asset_repair2.append('invoices', {'purchase_invoice': pi_name, 'expense_account': expense_account, 'repair_cost': 10})
self.assertRaises(frappe.ValidationError, asset_repair2.save)
```

## Next Steps


---

*Source: test_asset_repair.py:179 | Complexity: Advanced | Last updated: 2026-02-04*