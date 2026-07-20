# How To: Get Item Details

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test get item details

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

### Step 1: Call frappe.db.sql()

```python
frappe.db.sql('delete from `tabItem Price`')
```

### Step 2: Call frappe.db.sql()

```python
frappe.db.sql('delete from `tabBin`')
```

### Step 3: Assign to_check = value

```python
to_check = {'item_code': '_Test Item', 'item_name': '_Test Item', 'description': '_Test Item 1', 'warehouse': '_Test Warehouse - _TC', 'income_account': 'Sales - _TC', 'expense_account': '_Test Account Cost for Goods Sold - _TC', 'cost_center': '_Test Cost Center - _TC', 'qty': 1.0, 'price_list_rate': 100.0, 'base_price_list_rate': 0.0, 'discount_percentage': 0.0, 'rate': 0.0, 'base_rate': 0.0, 'amount': 0.0, 'base_amount': 0.0, 'batch_no': None, 'uom': '_Test UOM', 'conversion_factor': 1.0, 'reserved_qty': 1, 'actual_qty': 5, 'projected_qty': 14}
```

### Step 4: Call make_test_objects()

```python
make_test_objects('Item Price')
```

### Step 5: Call make_test_objects()

```python
make_test_objects('Bin', [{'item_code': '_Test Item', 'warehouse': '_Test Warehouse - _TC', 'reserved_qty': 1, 'actual_qty': 5, 'ordered_qty': 10, 'projected_qty': 14}])
```

### Step 6: Assign company = '_Test Company'

```python
company = '_Test Company'
```

### Step 7: Assign currency = frappe.get_cached_value(...)

```python
currency = frappe.get_cached_value('Company', company, 'default_currency')
```

### Step 8: Assign details = get_item_details(...)

```python
details = get_item_details(ItemDetailsCtx({'item_code': '_Test Item', 'company': company, 'price_list': '_Test Price List', 'currency': currency, 'doctype': 'Sales Order', 'conversion_rate': 1, 'price_list_currency': currency, 'plc_conversion_rate': 1, 'order_type': 'Sales', 'customer': '_Test Customer', 'conversion_factor': 1, 'price_list_uom_dependant': 1, 'ignore_pricing_rule': 1}))
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(value, details.get(key), key)
```


## Complete Example

```python
# Setup
super().setUp()
frappe.flags.attribute_values = None

# Workflow
frappe.db.sql('delete from `tabItem Price`')
frappe.db.sql('delete from `tabBin`')
to_check = {'item_code': '_Test Item', 'item_name': '_Test Item', 'description': '_Test Item 1', 'warehouse': '_Test Warehouse - _TC', 'income_account': 'Sales - _TC', 'expense_account': '_Test Account Cost for Goods Sold - _TC', 'cost_center': '_Test Cost Center - _TC', 'qty': 1.0, 'price_list_rate': 100.0, 'base_price_list_rate': 0.0, 'discount_percentage': 0.0, 'rate': 0.0, 'base_rate': 0.0, 'amount': 0.0, 'base_amount': 0.0, 'batch_no': None, 'uom': '_Test UOM', 'conversion_factor': 1.0, 'reserved_qty': 1, 'actual_qty': 5, 'projected_qty': 14}
make_test_objects('Item Price')
make_test_objects('Bin', [{'item_code': '_Test Item', 'warehouse': '_Test Warehouse - _TC', 'reserved_qty': 1, 'actual_qty': 5, 'ordered_qty': 10, 'projected_qty': 14}])
company = '_Test Company'
currency = frappe.get_cached_value('Company', company, 'default_currency')
details = get_item_details(ItemDetailsCtx({'item_code': '_Test Item', 'company': company, 'price_list': '_Test Price List', 'currency': currency, 'doctype': 'Sales Order', 'conversion_rate': 1, 'price_list_currency': currency, 'plc_conversion_rate': 1, 'order_type': 'Sales', 'customer': '_Test Customer', 'conversion_factor': 1, 'price_list_uom_dependant': 1, 'ignore_pricing_rule': 1}))
for key, value in to_check.items():
    self.assertEqual(value, details.get(key), key)
```

## Next Steps


---

*Source: test_item.py:91 | Complexity: Advanced | Last updated: 2026-02-04*