# How To: Pricing Rule With Margin And Discount

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test pricing rule with margin and discount

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

### Step 1: Call frappe.delete_doc_if_exists()

```python
frappe.delete_doc_if_exists('Pricing Rule', '_Test Pricing Rule')
```

### Step 2: Call make_pricing_rule()

```python
make_pricing_rule(selling=1, margin_type='Percentage', margin_rate_or_amount=10, discount_percentage=10)
```

### Step 3: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(do_not_save=True)
```

### Step 4: Assign unknown.price_list_rate = 1000

```python
si.items[0].price_list_rate = 1000
```

### Step 5: Assign si.payment_schedule = value

```python
si.payment_schedule = []
```

### Step 6: Call si.insert()

```python
si.insert(ignore_permissions=True)
```

### Step 7: Assign item = value

```python
item = si.items[0]
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(item.margin_rate_or_amount, 10)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(item.rate_with_margin, 1100)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(item.discount_percentage, 10)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(item.discount_amount, 110)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(item.rate, 990)
```


## Complete Example

```python
# Setup
delete_existing_pricing_rules()
setup_pricing_rule_data()
self.enterClassContext(self.change_settings('Selling Settings', validate_selling_price=0))

# Workflow
frappe.delete_doc_if_exists('Pricing Rule', '_Test Pricing Rule')
make_pricing_rule(selling=1, margin_type='Percentage', margin_rate_or_amount=10, discount_percentage=10)
si = create_sales_invoice(do_not_save=True)
si.items[0].price_list_rate = 1000
si.payment_schedule = []
si.insert(ignore_permissions=True)
item = si.items[0]
self.assertEqual(item.margin_rate_or_amount, 10)
self.assertEqual(item.rate_with_margin, 1100)
self.assertEqual(item.discount_percentage, 10)
self.assertEqual(item.discount_amount, 110)
self.assertEqual(item.rate, 990)
```

## Next Steps


---

*Source: test_pricing_rule.py:380 | Complexity: Advanced | Last updated: 2026-02-03*