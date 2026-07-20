# How To: Item Defaults

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test item defaults

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `json`
- `frappe`
- `frappe.custom.doctype.property_setter.property_setter`
- `frappe.test_runner`
- `frappe.tests`
- `frappe.utils`
- `erpnext.controllers.item_variant`
- `erpnext.stock.doctype.item.item`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.get_item_details`
- `erpnext.assets.doctype.asset.test_asset`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `time`
- `erpnext.stock.stock_balance`
- `erpnext.stock.stock_ledger`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.dashboard.item_dashboard`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.controllers.queries`
- `erpnext.stock.doctype.warehouse.test_warehouse`

**Setup Required:**
```python
super().setUp()
frappe.flags.attribute_values = None
```

## Step-by-Step Guide

### Step 1: Call frappe.delete_doc_if_exists()

```python
frappe.delete_doc_if_exists('Item', 'Test Item With Defaults', force=1)
```

### Step 2: Call make_item()

```python
make_item('Test Item With Defaults', {'item_group': '_Test Item Group', 'brand': '_Test Brand With Item Defaults', 'item_defaults': [{'company': '_Test Company', 'default_warehouse': '_Test Warehouse 2 - _TC', 'expense_account': '_Test Account Stock Expenses - _TC', 'default_cogs_account': '_Test Account Cost for Goods Sold - _TC', 'buying_cost_center': '_Test Write Off Cost Center - _TC'}]})
```

### Step 3: Assign sales_item_check = value

```python
sales_item_check = {'item_code': 'Test Item With Defaults', 'warehouse': '_Test Warehouse 2 - _TC', 'income_account': '_Test Account Sales - _TC', 'expense_account': '_Test Account Cost for Goods Sold - _TC', 'cost_center': '_Test Cost Center 2 - _TC'}
```

### Step 4: Assign sales_item_details = get_item_details(...)

```python
sales_item_details = get_item_details(ItemDetailsCtx({'item_code': 'Test Item With Defaults', 'company': '_Test Company', 'price_list': '_Test Price List', 'currency': '_Test Currency', 'doctype': 'Sales Invoice', 'conversion_rate': 1, 'price_list_currency': '_Test Currency', 'plc_conversion_rate': 1, 'customer': '_Test Customer'}))
```

### Step 5: Assign purchase_item_check = value

```python
purchase_item_check = {'item_code': 'Test Item With Defaults', 'warehouse': '_Test Warehouse 2 - _TC', 'expense_account': '_Test Account Stock Expenses - _TC', 'income_account': '_Test Account Sales - _TC', 'cost_center': '_Test Write Off Cost Center - _TC'}
```

### Step 6: Assign purchase_item_details = get_item_details(...)

```python
purchase_item_details = get_item_details(ItemDetailsCtx({'item_code': 'Test Item With Defaults', 'company': '_Test Company', 'price_list': '_Test Price List', 'currency': '_Test Currency', 'doctype': 'Purchase Invoice', 'conversion_rate': 1, 'price_list_currency': '_Test Currency', 'plc_conversion_rate': 1, 'supplier': '_Test Supplier'}))
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(value, sales_item_details.get(key))
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(value, purchase_item_details.get(key))
```


## Complete Example

```python
# Setup
super().setUp()
frappe.flags.attribute_values = None

# Workflow
frappe.delete_doc_if_exists('Item', 'Test Item With Defaults', force=1)
make_item('Test Item With Defaults', {'item_group': '_Test Item Group', 'brand': '_Test Brand With Item Defaults', 'item_defaults': [{'company': '_Test Company', 'default_warehouse': '_Test Warehouse 2 - _TC', 'expense_account': '_Test Account Stock Expenses - _TC', 'default_cogs_account': '_Test Account Cost for Goods Sold - _TC', 'buying_cost_center': '_Test Write Off Cost Center - _TC'}]})
sales_item_check = {'item_code': 'Test Item With Defaults', 'warehouse': '_Test Warehouse 2 - _TC', 'income_account': '_Test Account Sales - _TC', 'expense_account': '_Test Account Cost for Goods Sold - _TC', 'cost_center': '_Test Cost Center 2 - _TC'}
sales_item_details = get_item_details(ItemDetailsCtx({'item_code': 'Test Item With Defaults', 'company': '_Test Company', 'price_list': '_Test Price List', 'currency': '_Test Currency', 'doctype': 'Sales Invoice', 'conversion_rate': 1, 'price_list_currency': '_Test Currency', 'plc_conversion_rate': 1, 'customer': '_Test Customer'}))
for key, value in sales_item_check.items():
    self.assertEqual(value, sales_item_details.get(key))
purchase_item_check = {'item_code': 'Test Item With Defaults', 'warehouse': '_Test Warehouse 2 - _TC', 'expense_account': '_Test Account Stock Expenses - _TC', 'income_account': '_Test Account Sales - _TC', 'cost_center': '_Test Write Off Cost Center - _TC'}
purchase_item_details = get_item_details(ItemDetailsCtx({'item_code': 'Test Item With Defaults', 'company': '_Test Company', 'price_list': '_Test Price List', 'currency': '_Test Currency', 'doctype': 'Purchase Invoice', 'conversion_rate': 1, 'price_list_currency': '_Test Currency', 'plc_conversion_rate': 1, 'supplier': '_Test Supplier'}))
for key, value in purchase_item_check.items():
    self.assertEqual(value, purchase_item_details.get(key))
```

## Next Steps


---

*Source: test_item.py:296 | Complexity: Advanced | Last updated: 2026-02-04*