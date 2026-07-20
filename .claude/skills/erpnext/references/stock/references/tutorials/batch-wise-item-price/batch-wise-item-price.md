# How To: Batch Wise Item Price

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test batch wise item price

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe.exceptions`
- `frappe.tests`
- `frappe.utils`
- `frappe.utils.data`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.stock.doctype.batch.batch`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.serial_and_batch_bundle.serial_and_batch_bundle`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.get_item_details`
- `erpnext.stock.serial_batch_bundle`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.batch.batch`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`


## Step-by-Step Guide

### Step 1: Assign batch1 = create_batch(...)

```python
batch1 = create_batch('_Test Batch Price Item', 200, 1)
```

### Step 2: Assign batch2 = create_batch(...)

```python
batch2 = create_batch('_Test Batch Price Item', 300, 1)
```

### Step 3: Assign batch3 = create_batch(...)

```python
batch3 = create_batch('_Test Batch Price Item', 400, 0)
```

### Step 4: Assign company = '_Test Company with perpetual inventory'

```python
company = '_Test Company with perpetual inventory'
```

### Step 5: Assign currency = frappe.get_cached_value(...)

```python
currency = frappe.get_cached_value('Company', company, 'default_currency')
```

### Step 6: Assign ctx = ItemDetailsCtx(...)

```python
ctx = ItemDetailsCtx({'item_code': '_Test Batch Price Item', 'company': company, 'price_list': '_Test Price List', 'currency': currency, 'doctype': 'Sales Invoice', 'conversion_rate': 1, 'price_list_currency': '_Test Currency', 'plc_conversion_rate': 1, 'customer': '_Test Customer', 'name': None})
```

### Step 7: Call ctx.update()

```python
ctx.update({'batch_no': batch1})
```

### Step 8: Assign details = get_item_details(...)

```python
details = get_item_details(ctx)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(details.get('price_list_rate'), 200)
```

### Step 10: Call ctx.update()

```python
ctx.update({'batch_no': batch2})
```

### Step 11: Assign details = get_item_details(...)

```python
details = get_item_details(ctx)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(details.get('price_list_rate'), 300)
```

### Step 13: Call ctx.update()

```python
ctx.update({'batch_no': batch3})
```

### Step 14: Assign details = get_item_details(...)

```python
details = get_item_details(ctx)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(details.get('price_list_rate'), 400)
```

### Step 16: Call frappe.get_doc.insert()

```python
frappe.get_doc({'doctype': 'Item', 'is_stock_item': 1, 'item_code': '_Test Batch Price Item', 'item_group': 'Products', 'has_batch_no': 1, 'create_new_batch': 1}).insert(ignore_permissions=True)
```


## Complete Example

```python
# Workflow
if not frappe.db.get_value('Item', '_Test Batch Price Item'):
    frappe.get_doc({'doctype': 'Item', 'is_stock_item': 1, 'item_code': '_Test Batch Price Item', 'item_group': 'Products', 'has_batch_no': 1, 'create_new_batch': 1}).insert(ignore_permissions=True)
batch1 = create_batch('_Test Batch Price Item', 200, 1)
batch2 = create_batch('_Test Batch Price Item', 300, 1)
batch3 = create_batch('_Test Batch Price Item', 400, 0)
company = '_Test Company with perpetual inventory'
currency = frappe.get_cached_value('Company', company, 'default_currency')
ctx = ItemDetailsCtx({'item_code': '_Test Batch Price Item', 'company': company, 'price_list': '_Test Price List', 'currency': currency, 'doctype': 'Sales Invoice', 'conversion_rate': 1, 'price_list_currency': '_Test Currency', 'plc_conversion_rate': 1, 'customer': '_Test Customer', 'name': None})
ctx.update({'batch_no': batch1})
details = get_item_details(ctx)
self.assertEqual(details.get('price_list_rate'), 200)
ctx.update({'batch_no': batch2})
details = get_item_details(ctx)
self.assertEqual(details.get('price_list_rate'), 300)
ctx.update({'batch_no': batch3})
details = get_item_details(ctx)
self.assertEqual(details.get('price_list_rate'), 400)
```

## Next Steps


---

*Source: test_batch.py:440 | Complexity: Advanced | Last updated: 2026-02-04*