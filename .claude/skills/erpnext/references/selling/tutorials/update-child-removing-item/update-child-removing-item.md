# How To: Update Child Removing Item

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test update child removing item

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

### Step 1: Assign qo = make_quotation(...)

```python
qo = make_quotation(qty=10)
```

### Step 2: Assign sales_order = make_sales_order(...)

```python
sales_order = make_sales_order(qo.name)
```

### Step 3: Assign sales_order.delivery_date = nowdate(...)

```python
sales_order.delivery_date = nowdate()
```

### Step 4: Assign trans_item = json.dumps(...)

```python
trans_item = json.dumps([{'item_code': qo.items[0].item_code, 'rate': qo.items[0].rate, 'qty': qo.items[0].qty, 'docname': qo.items[0].name}, {'item_code': '_Test Item 2', 'rate': 100, 'qty': 7}])
```

### Step 5: Call update_child_qty_rate()

```python
update_child_qty_rate('Quotation', trans_item, qo.name)
```

### Step 6: Call sales_order.submit()

```python
sales_order.submit()
```

### Step 7: Call qo.reload()

```python
qo.reload()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(qo.status, 'Partially Ordered')
```

### Step 9: Assign trans_item = json.dumps(...)

```python
trans_item = json.dumps([{'item_code': '_Test Item 2', 'rate': 100, 'qty': 7}])
```

### Step 10: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, update_child_qty_rate, 'Quotation', trans_item, qo.name)
```

### Step 11: Assign trans_item = json.dumps(...)

```python
trans_item = json.dumps([{'item_code': qo.items[0].item_code, 'rate': qo.items[0].rate, 'qty': qo.items[0].qty, 'docname': qo.items[0].name}])
```

### Step 12: Call update_child_qty_rate()

```python
update_child_qty_rate('Quotation', trans_item, qo.name)
```

### Step 13: Call qo.reload()

```python
qo.reload()
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(len(qo.get('items')), 1)
```


## Complete Example

```python
# Workflow
qo = make_quotation(qty=10)
sales_order = make_sales_order(qo.name)
sales_order.delivery_date = nowdate()
trans_item = json.dumps([{'item_code': qo.items[0].item_code, 'rate': qo.items[0].rate, 'qty': qo.items[0].qty, 'docname': qo.items[0].name}, {'item_code': '_Test Item 2', 'rate': 100, 'qty': 7}])
update_child_qty_rate('Quotation', trans_item, qo.name)
sales_order.submit()
qo.reload()
self.assertEqual(qo.status, 'Partially Ordered')
trans_item = json.dumps([{'item_code': '_Test Item 2', 'rate': 100, 'qty': 7}])
self.assertRaises(frappe.ValidationError, update_child_qty_rate, 'Quotation', trans_item, qo.name)
trans_item = json.dumps([{'item_code': qo.items[0].item_code, 'rate': qo.items[0].rate, 'qty': qo.items[0].qty, 'docname': qo.items[0].name}])
update_child_qty_rate('Quotation', trans_item, qo.name)
qo.reload()
self.assertEqual(len(qo.get('items')), 1)
```

## Next Steps


---

*Source: test_quotation.py:75 | Complexity: Advanced | Last updated: 2026-02-04*