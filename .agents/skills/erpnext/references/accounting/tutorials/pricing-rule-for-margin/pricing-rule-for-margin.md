# How To: Pricing Rule For Margin

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test pricing rule for margin

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `frappe`
- `frappe.tests`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.get_item_details`
- `frappe`
- `erpnext.stock.get_item_details`
- `erpnext.accounts.doctype.pricing_rule.utils`
- `erpnext.stock.get_item_details`
- `erpnext.stock.get_item_details`
- `erpnext.stock.get_item_details`

**Setup Required:**
```python
delete_existing_pricing_rules()
setup_pricing_rule_data()
self.enterClassContext(self.change_settings('Selling Settings', validate_selling_price=0))
```

## Step-by-Step Guide

### Step 1: Assign test_record = value

```python
test_record = {'doctype': 'Pricing Rule', 'title': '_Test Pricing Rule', 'apply_on': 'Item Code', 'items': [{'item_code': '_Test FG Item 2'}], 'selling': 1, 'currency': 'USD', 'rate_or_discount': 'Discount Percentage', 'rate': 0, 'margin_type': 'Percentage', 'margin_rate_or_amount': 10, 'company': '_Test Company'}
```

### Step 2: Call frappe.get_doc.insert()

```python
frappe.get_doc(test_record.copy()).insert()
```

### Step 3: Assign item_price = frappe.get_doc(...)

```python
item_price = frappe.get_doc({'doctype': 'Item Price', 'price_list': '_Test Price List 2', 'item_code': '_Test FG Item 2', 'price_list_rate': 100})
```

### Step 4: Call item_price.insert()

```python
item_price.insert(ignore_permissions=True)
```

### Step 5: Assign args = frappe._dict(...)

```python
args = frappe._dict({'item_code': '_Test FG Item 2', 'company': '_Test Company', 'price_list': '_Test Price List', 'currency': '_Test Currency', 'doctype': 'Sales Order', 'conversion_rate': 1, 'price_list_currency': '_Test Currency', 'plc_conversion_rate': 1, 'order_type': 'Sales', 'customer': '_Test Customer', 'name': None})
```

### Step 6: Assign details = get_item_details(...)

```python
details = get_item_details(args)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(details.get('margin_type'), 'Percentage')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(details.get('margin_rate_or_amount'), 10)
```


## Complete Example

```python
# Setup
delete_existing_pricing_rules()
setup_pricing_rule_data()
self.enterClassContext(self.change_settings('Selling Settings', validate_selling_price=0))

# Workflow
from erpnext.stock.get_item_details import get_item_details
test_record = {'doctype': 'Pricing Rule', 'title': '_Test Pricing Rule', 'apply_on': 'Item Code', 'items': [{'item_code': '_Test FG Item 2'}], 'selling': 1, 'currency': 'USD', 'rate_or_discount': 'Discount Percentage', 'rate': 0, 'margin_type': 'Percentage', 'margin_rate_or_amount': 10, 'company': '_Test Company'}
frappe.get_doc(test_record.copy()).insert()
item_price = frappe.get_doc({'doctype': 'Item Price', 'price_list': '_Test Price List 2', 'item_code': '_Test FG Item 2', 'price_list_rate': 100})
item_price.insert(ignore_permissions=True)
args = frappe._dict({'item_code': '_Test FG Item 2', 'company': '_Test Company', 'price_list': '_Test Price List', 'currency': '_Test Currency', 'doctype': 'Sales Order', 'conversion_rate': 1, 'price_list_currency': '_Test Currency', 'plc_conversion_rate': 1, 'order_type': 'Sales', 'customer': '_Test Customer', 'name': None})
details = get_item_details(args)
self.assertEqual(details.get('margin_type'), 'Percentage')
self.assertEqual(details.get('margin_rate_or_amount'), 10)
```

## Next Steps


---

*Source: test_pricing_rule.py:107 | Complexity: Advanced | Last updated: 2026-02-03*