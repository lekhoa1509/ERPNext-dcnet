# How To: 01 Payment Terms Status

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test 01 payment terms status

## Prerequisites

**Required Modules:**
- `datetime`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.selling.report.payment_terms_status_for_sales_order.payment_terms_status_for_sales_order`
- `erpnext.stock.doctype.item.test_item`


## Step-by-Step Guide

### Step 1: Call self.create_payment_terms_template()

```python
self.create_payment_terms_template()
```

### Step 2: Assign item = create_item(...)

```python
item = create_item(item_code='_Test Excavator 1', is_stock_item=0)
```

### Step 3: Assign so = make_sales_order(...)

```python
so = make_sales_order(transaction_date='2021-06-15', delivery_date=add_days('2021-06-15', -30), item=item.item_code, qty=10, rate=100000, do_not_save=True)
```

### Step 4: Assign so.po_no = ''

```python
so.po_no = ''
```

### Step 5: Assign so.taxes_and_charges = ''

```python
so.taxes_and_charges = ''
```

### Step 6: Assign so.taxes = ''

```python
so.taxes = ''
```

### Step 7: Assign so.payment_terms_template = value

```python
so.payment_terms_template = self.template.name
```

### Step 8: Call so.save()

```python
so.save()
```

### Step 9: Call so.submit()

```python
so.submit()
```

### Step 10: Assign sinv = make_sales_invoice(...)

```python
sinv = make_sales_invoice(so.name)
```

### Step 11: Assign sinv.taxes_and_charges = ''

```python
sinv.taxes_and_charges = ''
```

### Step 12: Assign sinv.taxes = ''

```python
sinv.taxes = ''
```

### Step 13: Assign unknown.qty = 6

```python
sinv.items[0].qty = 6
```

### Step 14: Call sinv.insert()

```python
sinv.insert()
```

### Step 15: Call sinv.submit()

```python
sinv.submit()
```

### Step 16: Assign unknown = execute(...)

```python
columns, data, message, chart = execute(frappe._dict({'company': '_Test Company', 'period_start_date': '2021-06-01', 'period_end_date': '2021-06-30', 'item': item.item_code}))
```

### Step 17: Assign expected_value = value

```python
expected_value = [{'name': so.name, 'customer': so.customer, 'submitted': datetime.date(2021, 6, 15), 'status': 'Completed', 'payment_term': None, 'description': '_Test 50-50', 'due_date': datetime.date(2021, 6, 30), 'invoice_portion': 50.0, 'currency': 'INR', 'base_payment_amount': 500000.0, 'paid_amount': 500000.0, 'invoices': ',' + sinv.name}, {'name': so.name, 'customer': so.customer, 'submitted': datetime.date(2021, 6, 15), 'status': 'Partly Paid', 'payment_term': None, 'description': '_Test 50-50', 'due_date': datetime.date(2021, 7, 15), 'invoice_portion': 50.0, 'currency': 'INR', 'base_payment_amount': 500000.0, 'paid_amount': 100000.0, 'invoices': ',' + sinv.name}]
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(data, expected_value)
```


## Complete Example

```python
# Workflow
self.create_payment_terms_template()
item = create_item(item_code='_Test Excavator 1', is_stock_item=0)
so = make_sales_order(transaction_date='2021-06-15', delivery_date=add_days('2021-06-15', -30), item=item.item_code, qty=10, rate=100000, do_not_save=True)
so.po_no = ''
so.taxes_and_charges = ''
so.taxes = ''
so.payment_terms_template = self.template.name
so.save()
so.submit()
sinv = make_sales_invoice(so.name)
sinv.taxes_and_charges = ''
sinv.taxes = ''
sinv.items[0].qty = 6
sinv.insert()
sinv.submit()
columns, data, message, chart = execute(frappe._dict({'company': '_Test Company', 'period_start_date': '2021-06-01', 'period_end_date': '2021-06-30', 'item': item.item_code}))
expected_value = [{'name': so.name, 'customer': so.customer, 'submitted': datetime.date(2021, 6, 15), 'status': 'Completed', 'payment_term': None, 'description': '_Test 50-50', 'due_date': datetime.date(2021, 6, 30), 'invoice_portion': 50.0, 'currency': 'INR', 'base_payment_amount': 500000.0, 'paid_amount': 500000.0, 'invoices': ',' + sinv.name}, {'name': so.name, 'customer': so.customer, 'submitted': datetime.date(2021, 6, 15), 'status': 'Partly Paid', 'payment_term': None, 'description': '_Test 50-50', 'due_date': datetime.date(2021, 7, 15), 'invoice_portion': 50.0, 'currency': 'INR', 'base_payment_amount': 500000.0, 'paid_amount': 100000.0, 'invoices': ',' + sinv.name}]
self.assertEqual(data, expected_value)
```

## Next Steps


---

*Source: test_payment_terms_status_for_sales_order.py:60 | Complexity: Advanced | Last updated: 2026-02-04*