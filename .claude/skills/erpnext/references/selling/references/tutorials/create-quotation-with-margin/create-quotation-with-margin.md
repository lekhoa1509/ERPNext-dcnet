# How To: Create Quotation With Margin

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test create quotation with margin

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

### Step 1: Assign rate_with_margin = flt(...)

```python
rate_with_margin = flt(1500 * 18.75 / 100 + 1500)
```

### Step 2: Assign test_record = dict(...)

```python
test_record = dict(self.globalTestRecords['Quotation'][0])
```

### Step 3: Assign unknown = 1500

```python
test_record['items'][0]['price_list_rate'] = 1500
```

### Step 4: Assign unknown = 'Percentage'

```python
test_record['items'][0]['margin_type'] = 'Percentage'
```

### Step 5: Assign unknown = 18.75

```python
test_record['items'][0]['margin_rate_or_amount'] = 18.75
```

### Step 6: Assign quotation = frappe.copy_doc(...)

```python
quotation = frappe.copy_doc(test_record)
```

### Step 7: Assign quotation.transaction_date = nowdate(...)

```python
quotation.transaction_date = nowdate()
```

### Step 8: Assign quotation.valid_till = add_months(...)

```python
quotation.valid_till = add_months(quotation.transaction_date, 1)
```

### Step 9: Call quotation.insert()

```python
quotation.insert()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(quotation.get('items')[0].rate, rate_with_margin)
```

### Step 11: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, make_sales_order, quotation.name)
```

### Step 12: Call quotation.submit()

```python
quotation.submit()
```

### Step 13: Assign sales_order = make_sales_order(...)

```python
sales_order = make_sales_order(quotation.name)
```

### Step 14: Assign sales_order.naming_series = '_T-Quotation-'

```python
sales_order.naming_series = '_T-Quotation-'
```

### Step 15: Assign sales_order.transaction_date = '2016-01-01'

```python
sales_order.transaction_date = '2016-01-01'
```

### Step 16: Assign sales_order.delivery_date = '2016-01-02'

```python
sales_order.delivery_date = '2016-01-02'
```

### Step 17: Call sales_order.insert()

```python
sales_order.insert()
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(quotation.get('items')[0].rate, rate_with_margin)
```

### Step 19: Call sales_order.submit()

```python
sales_order.submit()
```

### Step 20: Assign dn = make_delivery_note(...)

```python
dn = make_delivery_note(sales_order.name)
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(quotation.get('items')[0].rate, rate_with_margin)
```

### Step 22: Call dn.save()

```python
dn.save()
```

### Step 23: Assign si = make_sales_invoice(...)

```python
si = make_sales_invoice(sales_order.name)
```

### Step 24: Call self.assertEqual()

```python
self.assertEqual(quotation.get('items')[0].rate, rate_with_margin)
```

### Step 25: Call si.save()

```python
si.save()
```


## Complete Example

```python
# Workflow
from erpnext.selling.doctype.quotation.quotation import make_sales_order
from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note, make_sales_invoice
rate_with_margin = flt(1500 * 18.75 / 100 + 1500)
test_record = dict(self.globalTestRecords['Quotation'][0])
test_record['items'][0]['price_list_rate'] = 1500
test_record['items'][0]['margin_type'] = 'Percentage'
test_record['items'][0]['margin_rate_or_amount'] = 18.75
quotation = frappe.copy_doc(test_record)
quotation.transaction_date = nowdate()
quotation.valid_till = add_months(quotation.transaction_date, 1)
quotation.insert()
self.assertEqual(quotation.get('items')[0].rate, rate_with_margin)
self.assertRaises(frappe.ValidationError, make_sales_order, quotation.name)
quotation.submit()
sales_order = make_sales_order(quotation.name)
sales_order.naming_series = '_T-Quotation-'
sales_order.transaction_date = '2016-01-01'
sales_order.delivery_date = '2016-01-02'
sales_order.insert()
self.assertEqual(quotation.get('items')[0].rate, rate_with_margin)
sales_order.submit()
dn = make_delivery_note(sales_order.name)
self.assertEqual(quotation.get('items')[0].rate, rate_with_margin)
dn.save()
si = make_sales_invoice(sales_order.name)
self.assertEqual(quotation.get('items')[0].rate, rate_with_margin)
si.save()
```

## Next Steps


---

*Source: test_quotation.py:352 | Complexity: Advanced | Last updated: 2026-02-04*