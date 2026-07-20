# How To: Item Price With Selling Uom Pricing Rule

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test item price with selling uom pricing rule

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

### Step 1: Assign properties = value

```python
properties = {'item_code': 'Item UOM other than Stock', 'stock_uom': 'Nos', 'sales_uom': 'Box', 'uoms': [dict(uom='Box', conversion_factor=10)]}
```

### Step 2: Assign item = make_item(...)

```python
item = make_item(properties=properties)
```

### Step 3: Call make_item_price()

```python
make_item_price('Item UOM other than Stock', '_Test Price List', 100)
```

### Step 4: Assign pricing_rule_record = value

```python
pricing_rule_record = {'doctype': 'Pricing Rule', 'title': '_Test Item UOM other than Stock Rule', 'apply_on': 'Item Code', 'items': [{'item_code': 'Item UOM other than Stock', 'uom': 'Box'}], 'selling': 1, 'currency': 'INR', 'rate_or_discount': 'Rate', 'rate': 101, 'company': '_Test Company'}
```

### Step 5: Assign rule = frappe.get_doc(...)

```python
rule = frappe.get_doc(pricing_rule_record)
```

### Step 6: Call rule.insert()

```python
rule.insert()
```

### Step 7: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(do_not_save=True, item_code='Item UOM other than Stock', uom='Box', conversion_factor=10)
```

### Step 8: Assign si.selling_price_list = '_Test Price List'

```python
si.selling_price_list = '_Test Price List'
```

### Step 9: Call si.save()

```python
si.save()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(si.items[0].price_list_rate, 101)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(si.items[0].rate, 101)
```

### Step 12: Call si.delete()

```python
si.delete()
```

### Step 13: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(do_not_save=True, item_code='Item UOM other than Stock', uom='Nos')
```

### Step 14: Assign si.selling_price_list = '_Test Price List'

```python
si.selling_price_list = '_Test Price List'
```

### Step 15: Call si.save()

```python
si.save()
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(si.items[0].price_list_rate, 100)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(si.items[0].rate, 100)
```

### Step 18: Call si.delete()

```python
si.delete()
```

### Step 19: Call rule.delete()

```python
rule.delete()
```

### Step 20: Call frappe.get_doc.delete()

```python
frappe.get_doc('Item Price', {'item_code': 'Item UOM other than Stock'}).delete()
```

### Step 21: Call item.delete()

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
properties = {'item_code': 'Item UOM other than Stock', 'stock_uom': 'Nos', 'sales_uom': 'Box', 'uoms': [dict(uom='Box', conversion_factor=10)]}
item = make_item(properties=properties)
make_item_price('Item UOM other than Stock', '_Test Price List', 100)
pricing_rule_record = {'doctype': 'Pricing Rule', 'title': '_Test Item UOM other than Stock Rule', 'apply_on': 'Item Code', 'items': [{'item_code': 'Item UOM other than Stock', 'uom': 'Box'}], 'selling': 1, 'currency': 'INR', 'rate_or_discount': 'Rate', 'rate': 101, 'company': '_Test Company'}
rule = frappe.get_doc(pricing_rule_record)
rule.insert()
si = create_sales_invoice(do_not_save=True, item_code='Item UOM other than Stock', uom='Box', conversion_factor=10)
si.selling_price_list = '_Test Price List'
si.save()
self.assertEqual(si.items[0].price_list_rate, 101)
self.assertEqual(si.items[0].rate, 101)
si.delete()
si = create_sales_invoice(do_not_save=True, item_code='Item UOM other than Stock', uom='Nos')
si.selling_price_list = '_Test Price List'
si.save()
self.assertEqual(si.items[0].price_list_rate, 100)
self.assertEqual(si.items[0].rate, 100)
si.delete()
rule.delete()
frappe.get_doc('Item Price', {'item_code': 'Item UOM other than Stock'}).delete()
item.delete()
```

## Next Steps


---

*Source: test_pricing_rule.py:751 | Complexity: Advanced | Last updated: 2026-02-03*