# How To: Do Not Add Ordered Items In New Sales Order

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test do not add ordered items in new sales order

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.controllers.accounts_controller`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.get_item_details`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.stock.doctype.item.test_item`


## Step-by-Step Guide

### Step 1: Assign item = make_item(...)

```python
item = make_item('_Test Item for Quotation for SO', {'is_stock_item': 1})
```

### Step 2: Assign quotation = make_quotation(...)

```python
quotation = make_quotation(qty=5, do_not_submit=True)
```

### Step 3: Call quotation.append()

```python
quotation.append('items', {'item_code': item.name, 'qty': 5, 'rate': 100, 'conversion_factor': 1, 'uom': item.stock_uom, 'warehouse': '_Test Warehouse - _TC', 'stock_uom': item.stock_uom})
```

### Step 4: Call quotation.submit()

```python
quotation.submit()
```

### Step 5: Assign sales_order = make_sales_order(...)

```python
sales_order = make_sales_order(quotation.name)
```

### Step 6: Assign sales_order.delivery_date = nowdate(...)

```python
sales_order.delivery_date = nowdate()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(len(sales_order.items), 2)
```

### Step 8: Call sales_order.remove()

```python
sales_order.remove(sales_order.items[1])
```

### Step 9: Call sales_order.submit()

```python
sales_order.submit()
```

### Step 10: Assign sales_order = make_sales_order(...)

```python
sales_order = make_sales_order(quotation.name)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(len(sales_order.items), 1)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(sales_order.items[0].item_code, item.name)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(sales_order.items[0].qty, 5.0)
```


## Complete Example

```python
# Workflow
from erpnext.selling.doctype.quotation.quotation import make_sales_order
from erpnext.stock.doctype.item.test_item import make_item
item = make_item('_Test Item for Quotation for SO', {'is_stock_item': 1})
quotation = make_quotation(qty=5, do_not_submit=True)
quotation.append('items', {'item_code': item.name, 'qty': 5, 'rate': 100, 'conversion_factor': 1, 'uom': item.stock_uom, 'warehouse': '_Test Warehouse - _TC', 'stock_uom': item.stock_uom})
quotation.submit()
sales_order = make_sales_order(quotation.name)
sales_order.delivery_date = nowdate()
self.assertEqual(len(sales_order.items), 2)
sales_order.remove(sales_order.items[1])
sales_order.submit()
sales_order = make_sales_order(quotation.name)
self.assertEqual(len(sales_order.items), 1)
self.assertEqual(sales_order.items[0].item_code, item.name)
self.assertEqual(sales_order.items[0].qty, 5.0)
```

## Next Steps


---

*Source: test_quotation.py:158 | Complexity: Advanced | Last updated: 2026-02-04*