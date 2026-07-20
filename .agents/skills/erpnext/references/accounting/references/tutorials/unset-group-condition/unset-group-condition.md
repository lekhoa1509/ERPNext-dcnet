# How To: Unset Group Condition

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: If args are not set for group condition, then pricing rule should not be applied.

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

### Step 1: '\n\t\tIf args are not set for group condition, then pricing rule should not be applied.\n\t\t'

```python
'\n\t\tIf args are not set for group condition, then pricing rule should not be applied.\n\t\t'
```

### Step 2: Assign test_record = value

```python
test_record = {'doctype': 'Pricing Rule', 'title': '_Test Pricing Rule', 'apply_on': 'Item Code', 'items': [{'item_code': '_Test Item'}], 'currency': 'USD', 'selling': 1, 'rate_or_discount': 'Discount Percentage', 'rate': 0, 'discount_percentage': 10, 'applicable_for': 'Territory', 'territory': 'All Territories', 'company': '_Test Company'}
```

### Step 3: Call frappe.get_doc.insert()

```python
frappe.get_doc(test_record.copy()).insert()
```

### Step 4: Assign args = frappe._dict(...)

```python
args = frappe._dict({'item_code': '_Test Item', 'company': '_Test Company', 'price_list': '_Test Price List', 'currency': '_Test Currency', 'doctype': 'Sales Order', 'conversion_rate': 1, 'price_list_currency': '_Test Currency', 'plc_conversion_rate': 1, 'order_type': 'Sales', 'customer': '_Test Customer', 'name': None})
```

### Step 5: Assign customer = frappe.get_doc(...)

```python
customer = frappe.get_doc('Customer', '_Test Customer')
```

### Step 6: Assign territory = value

```python
territory = customer.territory
```

### Step 7: Assign customer.territory = None

```python
customer.territory = None
```

### Step 8: Call customer.save()

```python
customer.save()
```

### Step 9: Assign details = get_item_details(...)

```python
details = get_item_details(args)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(details.get('discount_percentage'), 0)
```

### Step 11: Assign customer.territory = territory

```python
customer.territory = territory
```

### Step 12: Call customer.save()

```python
customer.save()
```


## Complete Example

```python
# Setup
delete_existing_pricing_rules()
setup_pricing_rule_data()
self.enterClassContext(self.change_settings('Selling Settings', validate_selling_price=0))

# Workflow
'\n\t\tIf args are not set for group condition, then pricing rule should not be applied.\n\t\t'
from erpnext.stock.get_item_details import get_item_details
test_record = {'doctype': 'Pricing Rule', 'title': '_Test Pricing Rule', 'apply_on': 'Item Code', 'items': [{'item_code': '_Test Item'}], 'currency': 'USD', 'selling': 1, 'rate_or_discount': 'Discount Percentage', 'rate': 0, 'discount_percentage': 10, 'applicable_for': 'Territory', 'territory': 'All Territories', 'company': '_Test Company'}
frappe.get_doc(test_record.copy()).insert()
args = frappe._dict({'item_code': '_Test Item', 'company': '_Test Company', 'price_list': '_Test Price List', 'currency': '_Test Currency', 'doctype': 'Sales Order', 'conversion_rate': 1, 'price_list_currency': '_Test Currency', 'plc_conversion_rate': 1, 'order_type': 'Sales', 'customer': '_Test Customer', 'name': None})
customer = frappe.get_doc('Customer', '_Test Customer')
territory = customer.territory
customer.territory = None
customer.save()
details = get_item_details(args)
self.assertEqual(details.get('discount_percentage'), 0)
customer.territory = territory
customer.save()
```

## Next Steps


---

*Source: test_pricing_rule.py:207 | Complexity: Advanced | Last updated: 2026-02-03*