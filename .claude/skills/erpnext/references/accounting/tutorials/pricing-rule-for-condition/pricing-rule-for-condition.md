# How To: Pricing Rule For Condition

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test pricing rule for condition

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
make_pricing_rule(selling=1, margin_type='Percentage', condition="customer=='_Test Customer 1' and is_return==0", discount_percentage=10)
```

### Step 3: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(do_not_submit=True, customer='_Test Customer 2', is_return=0)
```

### Step 4: Assign unknown.price_list_rate = 1000

```python
si.items[0].price_list_rate = 1000
```

### Step 5: Call si.submit()

```python
si.submit()
```

### Step 6: Assign item = value

```python
item = si.items[0]
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(item.rate, 100)
```

### Step 8: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(do_not_submit=True, customer='_Test Customer 1', is_return=1, qty=-1)
```

### Step 9: Assign unknown.price_list_rate = 1000

```python
si.items[0].price_list_rate = 1000
```

### Step 10: Call si.submit()

```python
si.submit()
```

### Step 11: Assign item = value

```python
item = si.items[0]
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(item.rate, 100)
```

### Step 13: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(do_not_submit=True, customer='_Test Customer 1', is_return=0)
```

### Step 14: Assign unknown.price_list_rate = 1000

```python
si.items[0].price_list_rate = 1000
```

### Step 15: Call si.submit()

```python
si.submit()
```

### Step 16: Assign item = value

```python
item = si.items[0]
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(item.rate, 900)
```


## Complete Example

```python
# Setup
delete_existing_pricing_rules()
setup_pricing_rule_data()
self.enterClassContext(self.change_settings('Selling Settings', validate_selling_price=0))

# Workflow
frappe.delete_doc_if_exists('Pricing Rule', '_Test Pricing Rule')
make_pricing_rule(selling=1, margin_type='Percentage', condition="customer=='_Test Customer 1' and is_return==0", discount_percentage=10)
si = create_sales_invoice(do_not_submit=True, customer='_Test Customer 2', is_return=0)
si.items[0].price_list_rate = 1000
si.submit()
item = si.items[0]
self.assertEqual(item.rate, 100)
si = create_sales_invoice(do_not_submit=True, customer='_Test Customer 1', is_return=1, qty=-1)
si.items[0].price_list_rate = 1000
si.submit()
item = si.items[0]
self.assertEqual(item.rate, 100)
si = create_sales_invoice(do_not_submit=True, customer='_Test Customer 1', is_return=0)
si.items[0].price_list_rate = 1000
si.submit()
item = si.items[0]
self.assertEqual(item.rate, 900)
```

## Next Steps


---

*Source: test_pricing_rule.py:576 | Complexity: Advanced | Last updated: 2026-02-03*