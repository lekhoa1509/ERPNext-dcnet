# How To: Gross Profit

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test gross profit

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

### Step 1: Assign item_doc = make_item(...)

```python
item_doc = make_item('_Test Item for Gross Profit', {'is_stock_item': 1})
```

### Step 2: Assign item_code = value

```python
item_code = item_doc.name
```

### Step 3: Call make_stock_entry()

```python
make_stock_entry(item_code=item_code, qty=10, rate=100, target='_Test Warehouse - _TC')
```

### Step 4: Assign selling_price_list = value

```python
selling_price_list = frappe.get_all('Price List', filters={'selling': 1}, limit=1)[0].name
```

### Step 5: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('Stock Settings', 'auto_insert_price_list_rate_if_missing', 1)
```

### Step 6: Call insert_item_price()

```python
insert_item_price(ItemDetailsCtx({'item_code': item_code, 'price_list': selling_price_list, 'price_list_rate': 300, 'rate': 300, 'conversion_factor': 1, 'discount_amount': 0.0, 'currency': frappe.db.get_value('Price List', selling_price_list, 'currency'), 'uom': item_doc.stock_uom}))
```

### Step 7: Assign quotation = make_quotation(...)

```python
quotation = make_quotation(item_code=item_code, qty=1, rate=300, selling_price_list=selling_price_list)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(quotation.items[0].valuation_rate, 100)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(quotation.items[0].gross_profit, 200)
```

### Step 10: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('Stock Settings', 'auto_insert_price_list_rate_if_missing', 0)
```


## Complete Example

```python
# Workflow
from erpnext.stock.doctype.item.test_item import make_item
from erpnext.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry
from erpnext.stock.get_item_details import ItemDetailsCtx, insert_item_price
item_doc = make_item('_Test Item for Gross Profit', {'is_stock_item': 1})
item_code = item_doc.name
make_stock_entry(item_code=item_code, qty=10, rate=100, target='_Test Warehouse - _TC')
selling_price_list = frappe.get_all('Price List', filters={'selling': 1}, limit=1)[0].name
frappe.db.set_single_value('Stock Settings', 'auto_insert_price_list_rate_if_missing', 1)
insert_item_price(ItemDetailsCtx({'item_code': item_code, 'price_list': selling_price_list, 'price_list_rate': 300, 'rate': 300, 'conversion_factor': 1, 'discount_amount': 0.0, 'currency': frappe.db.get_value('Price List', selling_price_list, 'currency'), 'uom': item_doc.stock_uom}))
quotation = make_quotation(item_code=item_code, qty=1, rate=300, selling_price_list=selling_price_list)
self.assertEqual(quotation.items[0].valuation_rate, 100)
self.assertEqual(quotation.items[0].gross_profit, 200)
frappe.db.set_single_value('Stock Settings', 'auto_insert_price_list_rate_if_missing', 0)
```

## Next Steps


---

*Source: test_quotation.py:190 | Complexity: Advanced | Last updated: 2026-02-04*