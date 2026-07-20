# How To: Make Sales Order With Terms

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test make sales order with terms

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

### Step 1: Assign quotation = frappe.copy_doc(...)

```python
quotation = frappe.copy_doc(self.globalTestRecords['Quotation'][0])
```

### Step 2: Assign quotation.transaction_date = nowdate(...)

```python
quotation.transaction_date = nowdate()
```

### Step 3: Assign quotation.valid_till = add_months(...)

```python
quotation.valid_till = add_months(quotation.transaction_date, 1)
```

### Step 4: Call quotation.update()

```python
quotation.update({'payment_terms_template': '_Test Payment Term Template'})
```

### Step 5: Call quotation.insert()

```python
quotation.insert()
```

### Step 6: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, make_sales_order, quotation.name)
```

### Step 7: Call quotation.save()

```python
quotation.save()
```

### Step 8: Call quotation.submit()

```python
quotation.submit()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(quotation.payment_schedule[0].payment_amount, 8906.0)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(quotation.payment_schedule[0].due_date, quotation.transaction_date)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(quotation.payment_schedule[1].payment_amount, 8906.0)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(quotation.payment_schedule[1].due_date, add_days(quotation.transaction_date, 30))
```

### Step 13: Assign sales_order = make_sales_order(...)

```python
sales_order = make_sales_order(quotation.name)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(sales_order.doctype, 'Sales Order')
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(len(sales_order.get('items')), 1)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(sales_order.get('items')[0].doctype, 'Sales Order Item')
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(sales_order.get('items')[0].prevdoc_docname, quotation.name)
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(sales_order.customer, '_Test Customer')
```

### Step 19: Assign sales_order.naming_series = '_T-Quotation-'

```python
sales_order.naming_series = '_T-Quotation-'
```

### Step 20: Assign sales_order.transaction_date = nowdate(...)

```python
sales_order.transaction_date = nowdate()
```

### Step 21: Assign sales_order.delivery_date = nowdate(...)

```python
sales_order.delivery_date = nowdate()
```

### Step 22: Call sales_order.insert()

```python
sales_order.insert()
```

### Step 23: Call sales_order.set()

```python
sales_order.set('taxes', [])
```

### Step 24: Call sales_order.save()

```python
sales_order.save()
```

### Step 25: Call self.assertEqual()

```python
self.assertEqual(sales_order.payment_schedule[0].payment_amount, 8906.0)
```

### Step 26: Call self.assertEqual()

```python
self.assertEqual(sales_order.payment_schedule[0].due_date, getdate(quotation.transaction_date))
```

### Step 27: Call self.assertEqual()

```python
self.assertEqual(sales_order.payment_schedule[1].payment_amount, 8906.0)
```

### Step 28: Call self.assertEqual()

```python
self.assertEqual(sales_order.payment_schedule[1].due_date, getdate(add_days(quotation.transaction_date, 30)))
```


## Complete Example

```python
# Workflow
from erpnext.selling.doctype.quotation.quotation import make_sales_order
quotation = frappe.copy_doc(self.globalTestRecords['Quotation'][0])
quotation.transaction_date = nowdate()
quotation.valid_till = add_months(quotation.transaction_date, 1)
quotation.update({'payment_terms_template': '_Test Payment Term Template'})
quotation.insert()
self.assertRaises(frappe.ValidationError, make_sales_order, quotation.name)
quotation.save()
quotation.submit()
self.assertEqual(quotation.payment_schedule[0].payment_amount, 8906.0)
self.assertEqual(quotation.payment_schedule[0].due_date, quotation.transaction_date)
self.assertEqual(quotation.payment_schedule[1].payment_amount, 8906.0)
self.assertEqual(quotation.payment_schedule[1].due_date, add_days(quotation.transaction_date, 30))
sales_order = make_sales_order(quotation.name)
self.assertEqual(sales_order.doctype, 'Sales Order')
self.assertEqual(len(sales_order.get('items')), 1)
self.assertEqual(sales_order.get('items')[0].doctype, 'Sales Order Item')
self.assertEqual(sales_order.get('items')[0].prevdoc_docname, quotation.name)
self.assertEqual(sales_order.customer, '_Test Customer')
sales_order.naming_series = '_T-Quotation-'
sales_order.transaction_date = nowdate()
sales_order.delivery_date = nowdate()
sales_order.insert()
sales_order.set('taxes', [])
sales_order.save()
self.assertEqual(sales_order.payment_schedule[0].payment_amount, 8906.0)
self.assertEqual(sales_order.payment_schedule[0].due_date, getdate(quotation.transaction_date))
self.assertEqual(sales_order.payment_schedule[1].payment_amount, 8906.0)
self.assertEqual(sales_order.payment_schedule[1].due_date, getdate(add_days(quotation.transaction_date, 30)))
```

## Next Steps


---

*Source: test_quotation.py:289 | Complexity: Advanced | Last updated: 2026-02-04*