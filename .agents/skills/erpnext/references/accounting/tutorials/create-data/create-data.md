# How To: Create Data

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test create test data

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.accounts.doctype.pricing_rule.utils`


## Step-by-Step Guide

### Step 1: Call frappe.set_user()

```python
frappe.set_user('Administrator')
```

### Step 2: Assign item_price = frappe.get_list(...)

```python
item_price = frappe.get_list('Item Price', filters={'item_code': '_Test Tesla Car', 'price_list': '_Test Price List'}, fields=['name'])
```

### Step 3: Assign item = frappe.get_doc(...)

```python
item = frappe.get_doc({'description': '_Test Tesla Car', 'doctype': 'Item', 'has_batch_no': 0, 'has_serial_no': 0, 'inspection_required': 0, 'is_stock_item': 1, 'opening_stock': 100, 'is_sub_contracted_item': 0, 'item_code': '_Test Tesla Car', 'item_group': '_Test Item Group', 'item_name': '_Test Tesla Car', 'apply_warehouse_wise_reorder_level': 0, 'warehouse': 'Stores - _TC', 'valuation_rate': 5000, 'standard_rate': 5000, 'item_defaults': [{'company': '_Test Company', 'default_warehouse': 'Stores - _TC', 'default_price_list': '_Test Price List', 'expense_account': 'Cost of Goods Sold - _TC', 'buying_cost_center': 'Main - _TC', 'selling_cost_center': 'Main - _TC', 'income_account': 'Sales - _TC'}]})
```

### Step 4: Call item.insert()

```python
item.insert()
```

### Step 5: Assign item_price = frappe.get_doc(...)

```python
item_price = frappe.get_doc({'doctype': 'Item Price', 'item_code': '_Test Tesla Car', 'price_list': '_Test Price List', 'price_list_rate': 5000})
```

### Step 6: Call item_price.insert()

```python
item_price.insert()
```

### Step 7: Assign item_pricing_rule = frappe.get_doc(...)

```python
item_pricing_rule = frappe.get_doc({'doctype': 'Pricing Rule', 'title': '_Test Pricing Rule for _Test Item', 'apply_on': 'Item Code', 'items': [{'item_code': '_Test Tesla Car'}], 'warehouse': 'Stores - _TC', 'coupon_code_based': 1, 'selling': 1, 'rate_or_discount': 'Discount Percentage', 'discount_percentage': 30, 'company': '_Test Company', 'currency': 'INR', 'for_price_list': '_Test Price List'})
```

### Step 8: Call item_pricing_rule.insert()

```python
item_pricing_rule.insert()
```

### Step 9: Assign sales_partner = frappe.get_doc(...)

```python
sales_partner = frappe.get_doc({'doctype': 'Sales Partner', 'partner_name': '_Test Coupon Partner', 'commission_rate': 2, 'referral_code': 'COPART'})
```

### Step 10: Call sales_partner.insert()

```python
sales_partner.insert()
```

### Step 11: Assign pricing_rule = frappe.db.get_value(...)

```python
pricing_rule = frappe.db.get_value('Pricing Rule', {'title': '_Test Pricing Rule for _Test Item'}, ['name'])
```

### Step 12: Assign coupon_code = frappe.get_doc(...)

```python
coupon_code = frappe.get_doc({'doctype': 'Coupon Code', 'coupon_name': 'SAVE30', 'coupon_code': 'SAVE30', 'pricing_rule': pricing_rule, 'valid_from': '2014-01-01', 'maximum_use': 1, 'used': 0})
```

### Step 13: Call coupon_code.insert()

```python
coupon_code.insert()
```


## Complete Example

```python
# Workflow
frappe.set_user('Administrator')
if not frappe.db.exists('Item', '_Test Tesla Car'):
    item = frappe.get_doc({'description': '_Test Tesla Car', 'doctype': 'Item', 'has_batch_no': 0, 'has_serial_no': 0, 'inspection_required': 0, 'is_stock_item': 1, 'opening_stock': 100, 'is_sub_contracted_item': 0, 'item_code': '_Test Tesla Car', 'item_group': '_Test Item Group', 'item_name': '_Test Tesla Car', 'apply_warehouse_wise_reorder_level': 0, 'warehouse': 'Stores - _TC', 'valuation_rate': 5000, 'standard_rate': 5000, 'item_defaults': [{'company': '_Test Company', 'default_warehouse': 'Stores - _TC', 'default_price_list': '_Test Price List', 'expense_account': 'Cost of Goods Sold - _TC', 'buying_cost_center': 'Main - _TC', 'selling_cost_center': 'Main - _TC', 'income_account': 'Sales - _TC'}]})
    item.insert()
item_price = frappe.get_list('Item Price', filters={'item_code': '_Test Tesla Car', 'price_list': '_Test Price List'}, fields=['name'])
if len(item_price) == 0:
    item_price = frappe.get_doc({'doctype': 'Item Price', 'item_code': '_Test Tesla Car', 'price_list': '_Test Price List', 'price_list_rate': 5000})
    item_price.insert()
if not frappe.db.exists('Pricing Rule', {'title': '_Test Pricing Rule for _Test Item'}):
    item_pricing_rule = frappe.get_doc({'doctype': 'Pricing Rule', 'title': '_Test Pricing Rule for _Test Item', 'apply_on': 'Item Code', 'items': [{'item_code': '_Test Tesla Car'}], 'warehouse': 'Stores - _TC', 'coupon_code_based': 1, 'selling': 1, 'rate_or_discount': 'Discount Percentage', 'discount_percentage': 30, 'company': '_Test Company', 'currency': 'INR', 'for_price_list': '_Test Price List'})
    item_pricing_rule.insert()
if not frappe.db.exists('Sales Partner', '_Test Coupon Partner'):
    sales_partner = frappe.get_doc({'doctype': 'Sales Partner', 'partner_name': '_Test Coupon Partner', 'commission_rate': 2, 'referral_code': 'COPART'})
    sales_partner.insert()
if not frappe.db.exists('Coupon Code', 'SAVE30'):
    pricing_rule = frappe.db.get_value('Pricing Rule', {'title': '_Test Pricing Rule for _Test Item'}, ['name'])
    coupon_code = frappe.get_doc({'doctype': 'Coupon Code', 'coupon_name': 'SAVE30', 'coupon_code': 'SAVE30', 'pricing_rule': pricing_rule, 'valid_from': '2014-01-01', 'maximum_use': 1, 'used': 0})
    coupon_code.insert()
```

## Next Steps


---

*Source: test_coupon_code.py:12 | Complexity: Advanced | Last updated: 2026-02-03*