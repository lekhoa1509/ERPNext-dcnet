# How To: Pricing Rule For Stock Qty

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test pricing rule for stock qty

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
test_record = {'doctype': 'Pricing Rule', 'title': '_Test Pricing Rule', 'apply_on': 'Item Code', 'currency': 'USD', 'items': [{'item_code': '_Test Item'}], 'selling': 1, 'rate_or_discount': 'Discount Percentage', 'rate': 0, 'min_qty': 5, 'max_qty': 7, 'discount_percentage': 17.5, 'company': '_Test Company'}
```

### Step 2: Call frappe.get_doc.insert()

```python
frappe.get_doc(test_record.copy()).insert()
```

### Step 3: Assign so = make_sales_order(...)

```python
so = make_sales_order(item_code='_Test Item', qty=1, uom='Box', do_not_submit=True)
```

### Step 4: Assign unknown.price_list_rate = 100

```python
so.items[0].price_list_rate = 100
```

### Step 5: Call so.submit()

```python
so.submit()
```

### Step 6: Assign so = frappe.get_doc(...)

```python
so = frappe.get_doc('Sales Order', so.name)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(so.items[0].discount_percentage, 17.5)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(so.items[0].rate, 82.5)
```

### Step 9: Assign so = make_sales_order(...)

```python
so = make_sales_order(item_code='_Test Item', qty=2, uom='Box', do_not_submit=True)
```

### Step 10: Assign unknown.price_list_rate = 100

```python
so.items[0].price_list_rate = 100
```

### Step 11: Call so.submit()

```python
so.submit()
```

### Step 12: Assign so = frappe.get_doc(...)

```python
so = frappe.get_doc('Sales Order', so.name)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(so.items[0].discount_percentage, 0)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(so.items[0].rate, 100)
```

### Step 15: Assign item = frappe.get_doc(...)

```python
item = frappe.get_doc('Item', '_Test Item')
```

### Step 16: Call item.append()

```python
item.append('uoms', {'uom': 'Box', 'conversion_factor': 5})
```

### Step 17: Call item.save()

```python
item.save(ignore_permissions=True)
```


## Complete Example

```python
# Setup
delete_existing_pricing_rules()
setup_pricing_rule_data()
self.enterClassContext(self.change_settings('Selling Settings', validate_selling_price=0))

# Workflow
test_record = {'doctype': 'Pricing Rule', 'title': '_Test Pricing Rule', 'apply_on': 'Item Code', 'currency': 'USD', 'items': [{'item_code': '_Test Item'}], 'selling': 1, 'rate_or_discount': 'Discount Percentage', 'rate': 0, 'min_qty': 5, 'max_qty': 7, 'discount_percentage': 17.5, 'company': '_Test Company'}
frappe.get_doc(test_record.copy()).insert()
if not frappe.db.get_value('UOM Conversion Detail', {'parent': '_Test Item', 'uom': 'box'}):
    item = frappe.get_doc('Item', '_Test Item')
    item.append('uoms', {'uom': 'Box', 'conversion_factor': 5})
    item.save(ignore_permissions=True)
so = make_sales_order(item_code='_Test Item', qty=1, uom='Box', do_not_submit=True)
so.items[0].price_list_rate = 100
so.submit()
so = frappe.get_doc('Sales Order', so.name)
self.assertEqual(so.items[0].discount_percentage, 17.5)
self.assertEqual(so.items[0].rate, 82.5)
so = make_sales_order(item_code='_Test Item', qty=2, uom='Box', do_not_submit=True)
so.items[0].price_list_rate = 100
so.submit()
so = frappe.get_doc('Sales Order', so.name)
self.assertEqual(so.items[0].discount_percentage, 0)
self.assertEqual(so.items[0].rate, 100)
```

## Next Steps


---

*Source: test_pricing_rule.py:338 | Complexity: Advanced | Last updated: 2026-02-03*