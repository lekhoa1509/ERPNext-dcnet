# How To: Update Child Quotation Add Item

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test update child quotation add item

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

### Step 1: Assign item_1 = make_item(...)

```python
item_1 = make_item('_Test Item')
```

### Step 2: Assign item_2 = make_item(...)

```python
item_2 = make_item('_Test Item 1')
```

### Step 3: Assign item_list = value

```python
item_list = [{'item_code': item_1.item_code, 'warehouse': '', 'qty': 10, 'rate': 300}, {'item_code': item_2.item_code, 'warehouse': '', 'qty': 5, 'rate': 400}]
```

### Step 4: Assign qo = make_quotation(...)

```python
qo = make_quotation(item_list=item_list)
```

### Step 5: Assign first_item = value

```python
first_item = qo.get('items')[0]
```

### Step 6: Assign second_item = value

```python
second_item = qo.get('items')[1]
```

### Step 7: Assign trans_item = json.dumps(...)

```python
trans_item = json.dumps([{'item_code': first_item.item_code, 'rate': first_item.rate, 'qty': 11, 'docname': first_item.name}, {'item_code': second_item.item_code, 'rate': second_item.rate, 'qty': second_item.qty, 'docname': second_item.name, 'description': 'test'}, {'item_code': '_Test Item 2', 'rate': 100, 'qty': 7}])
```

### Step 8: Call update_child_qty_rate()

```python
update_child_qty_rate('Quotation', trans_item, qo.name)
```

### Step 9: Call qo.reload()

```python
qo.reload()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(qo.get('items')[0].qty, 11)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(qo.get('items')[-1].rate, 100)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(qo.get('items')[1].description, 'test')
```


## Complete Example

```python
# Workflow
from erpnext.stock.doctype.item.test_item import make_item
item_1 = make_item('_Test Item')
item_2 = make_item('_Test Item 1')
item_list = [{'item_code': item_1.item_code, 'warehouse': '', 'qty': 10, 'rate': 300}, {'item_code': item_2.item_code, 'warehouse': '', 'qty': 5, 'rate': 400}]
qo = make_quotation(item_list=item_list)
first_item = qo.get('items')[0]
second_item = qo.get('items')[1]
trans_item = json.dumps([{'item_code': first_item.item_code, 'rate': first_item.rate, 'qty': 11, 'docname': first_item.name}, {'item_code': second_item.item_code, 'rate': second_item.rate, 'qty': second_item.qty, 'docname': second_item.name, 'description': 'test'}, {'item_code': '_Test Item 2', 'rate': 100, 'qty': 7}])
update_child_qty_rate('Quotation', trans_item, qo.name)
qo.reload()
self.assertEqual(qo.get('items')[0].qty, 11)
self.assertEqual(qo.get('items')[-1].rate, 100)
self.assertEqual(qo.get('items')[1].description, 'test')
```

## Next Steps


---

*Source: test_quotation.py:17 | Complexity: Advanced | Last updated: 2026-02-04*