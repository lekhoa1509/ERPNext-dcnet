# How To: Dont Enforce Free Item Qty

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test dont enforce free item qty

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

### Step 2: Assign test_record = value

```python
test_record = {'doctype': 'Pricing Rule', 'title': '_Test Pricing Rule', 'apply_on': 'Item Code', 'currency': 'USD', 'items': [{'item_code': '_Test Item'}], 'selling': 1, 'rate_or_discount': 'Discount Percentage', 'rate': 0, 'min_qty': 0, 'max_qty': 7, 'discount_percentage': 17.5, 'price_or_product_discount': 'Product', 'same_item': 0, 'free_item': '_Test Item 2', 'free_qty': 1, 'company': '_Test Company'}
```

### Step 3: Assign pricing_rule = frappe.get_doc.insert(...)

```python
pricing_rule = frappe.get_doc(test_record.copy()).insert()
```

### Step 4: Assign so = make_sales_order(...)

```python
so = make_sales_order(item_code='_Test Item', qty=1, do_not_submit=True)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(so.items[1].is_free_item, 1)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(so.items[1].item_code, '_Test Item 2')
```

### Step 7: Call so.items.pop()

```python
so.items.pop(1)
```

### Step 8: Call so.save()

```python
so.save()
```

### Step 9: Call so.reload()

```python
so.reload()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(len(so.items), 2)
```

### Step 11: Assign pricing_rule.dont_enforce_free_item_qty = 1

```python
pricing_rule.dont_enforce_free_item_qty = 1
```

### Step 12: Call pricing_rule.save()

```python
pricing_rule.save()
```

### Step 13: Call so.items.pop()

```python
so.items.pop(1)
```

### Step 14: Call so.save()

```python
so.save()
```

### Step 15: Call so.reload()

```python
so.reload()
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(len(so.items), 1)
```


## Complete Example

```python
# Setup
delete_existing_pricing_rules()
setup_pricing_rule_data()
self.enterClassContext(self.change_settings('Selling Settings', validate_selling_price=0))

# Workflow
frappe.delete_doc_if_exists('Pricing Rule', '_Test Pricing Rule')
test_record = {'doctype': 'Pricing Rule', 'title': '_Test Pricing Rule', 'apply_on': 'Item Code', 'currency': 'USD', 'items': [{'item_code': '_Test Item'}], 'selling': 1, 'rate_or_discount': 'Discount Percentage', 'rate': 0, 'min_qty': 0, 'max_qty': 7, 'discount_percentage': 17.5, 'price_or_product_discount': 'Product', 'same_item': 0, 'free_item': '_Test Item 2', 'free_qty': 1, 'company': '_Test Company'}
pricing_rule = frappe.get_doc(test_record.copy()).insert()
so = make_sales_order(item_code='_Test Item', qty=1, do_not_submit=True)
self.assertEqual(so.items[1].is_free_item, 1)
self.assertEqual(so.items[1].item_code, '_Test Item 2')
so.items.pop(1)
so.save()
so.reload()
self.assertEqual(len(so.items), 2)
pricing_rule.dont_enforce_free_item_qty = 1
pricing_rule.save()
so.items.pop(1)
so.save()
so.reload()
self.assertEqual(len(so.items), 1)
```

## Next Steps


---

*Source: test_pricing_rule.py:480 | Complexity: Advanced | Last updated: 2026-02-03*