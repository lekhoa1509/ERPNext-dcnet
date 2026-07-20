# How To: Item Price With Pricing Rule

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test item price with pricing rule

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

### Step 1: Assign item = make_item(...)

```python
item = make_item('Water Flask')
```

### Step 2: Call make_item_price()

```python
make_item_price('Water Flask', '_Test Price List', 100)
```

### Step 3: Assign pricing_rule_record = value

```python
pricing_rule_record = {'doctype': 'Pricing Rule', 'title': '_Test Water Flask Rule', 'apply_on': 'Item Code', 'items': [{'item_code': 'Water Flask'}], 'selling': 1, 'currency': 'INR', 'rate_or_discount': 'Rate', 'rate': 0, 'margin_type': 'Percentage', 'margin_rate_or_amount': 2, 'company': '_Test Company'}
```

### Step 4: Assign rule = frappe.get_doc(...)

```python
rule = frappe.get_doc(pricing_rule_record)
```

### Step 5: Call rule.insert()

```python
rule.insert()
```

### Step 6: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(do_not_save=True, item_code='Water Flask')
```

### Step 7: Assign si.selling_price_list = '_Test Price List'

```python
si.selling_price_list = '_Test Price List'
```

### Step 8: Call si.save()

```python
si.save()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(si.items[0].price_list_rate, 100)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(si.items[0].margin_rate_or_amount, 2)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(si.items[0].rate_with_margin, 102)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(si.items[0].rate, 102)
```

### Step 13: Call si.delete()

```python
si.delete()
```

### Step 14: Call rule.delete()

```python
rule.delete()
```

### Step 15: Call frappe.get_doc.delete()

```python
frappe.get_doc('Item Price', {'item_code': 'Water Flask'}).delete()
```

### Step 16: Call item.delete()

```python
item.delete()
```


## Complete Example

```python
# Setup
delete_existing_pricing_rules()
setup_pricing_rule_data()
self.enterClassContext(self.change_settings('Selling Settings', validate_selling_price=0))

# Workflow
item = make_item('Water Flask')
make_item_price('Water Flask', '_Test Price List', 100)
pricing_rule_record = {'doctype': 'Pricing Rule', 'title': '_Test Water Flask Rule', 'apply_on': 'Item Code', 'items': [{'item_code': 'Water Flask'}], 'selling': 1, 'currency': 'INR', 'rate_or_discount': 'Rate', 'rate': 0, 'margin_type': 'Percentage', 'margin_rate_or_amount': 2, 'company': '_Test Company'}
rule = frappe.get_doc(pricing_rule_record)
rule.insert()
si = create_sales_invoice(do_not_save=True, item_code='Water Flask')
si.selling_price_list = '_Test Price List'
si.save()
self.assertEqual(si.items[0].price_list_rate, 100)
self.assertEqual(si.items[0].margin_rate_or_amount, 2)
self.assertEqual(si.items[0].rate_with_margin, 102)
self.assertEqual(si.items[0].rate, 102)
si.delete()
rule.delete()
frappe.get_doc('Item Price', {'item_code': 'Water Flask'}).delete()
item.delete()
```

## Next Steps


---

*Source: test_pricing_rule.py:655 | Complexity: Advanced | Last updated: 2026-02-03*