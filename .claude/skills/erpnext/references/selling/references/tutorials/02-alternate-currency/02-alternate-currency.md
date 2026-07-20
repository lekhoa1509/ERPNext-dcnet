# How To: 02 Alternate Currency

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test 02 alternate currency

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

### Step 1: Assign transaction_date = '2021-06-15'

```python
transaction_date = '2021-06-15'
```

### Step 2: Call self.create_payment_terms_template()

```python
self.create_payment_terms_template()
```

### Step 3: Call self.create_exchange_rate()

```python
self.create_exchange_rate(transaction_date)
```

### Step 4: Assign item = create_item(...)

```python
item = create_item(item_code='_Test Excavator 2', is_stock_item=0)
```

### Step 5: Assign so = make_sales_order(...)

```python
so = make_sales_order(transaction_date=transaction_date, currency='USD', delivery_date=add_days(transaction_date, -30), item=item.item_code, qty=10, rate=10000, do_not_save=True)
```

### Step 6: Assign so.po_no = ''

```python
so.po_no = ''
```

### Step 7: Assign so.taxes_and_charges = ''

```python
so.taxes_and_charges = ''
```

### Step 8: Assign so.taxes = ''

```python
so.taxes = ''
```

### Step 9: Assign so.payment_terms_template = value

```python
so.payment_terms_template = self.template.name
```

### Step 10: Call so.save()

```python
so.save()
```

### Step 11: Call so.submit()

```python
so.submit()
```

### Step 12: Assign sinv = make_sales_invoice(...)

```python
sinv = make_sales_invoice(so.name)
```

### Step 13: Assign sinv.currency = 'USD'

```python
sinv.currency = 'USD'
```

### Step 14: Assign sinv.taxes_and_charges = ''

```python
sinv.taxes_and_charges = ''
```

### Step 15: Assign sinv.taxes = ''

```python
sinv.taxes = ''
```

### Step 16: Assign unknown.qty = 6

```python
sinv.items[0].qty = 6
```

### Step 17: Call sinv.insert()

```python
sinv.insert()
```

### Step 18: Call sinv.submit()

```python
sinv.submit()
```

### Step 19: Assign unknown = execute(...)

```python
columns, data, message, chart = execute(frappe._dict({'company': '_Test Company', 'period_start_date': '2021-06-01', 'period_end_date': '2021-06-30', 'item': item.item_code}))
```

### Step 20: Assign expected_value = value

```python
expected_value = [{'name': so.name, 'customer': so.customer, 'submitted': datetime.date(2021, 6, 15), 'status': 'Completed', 'payment_term': None, 'description': '_Test 50-50', 'due_date': datetime.date(2021, 6, 30), 'invoice_portion': 50.0, 'currency': frappe.get_cached_value('Company', '_Test Company', 'default_currency'), 'base_payment_amount': 3500000.0, 'paid_amount': 3500000.0, 'invoices': ',' + sinv.name}, {'name': so.name, 'customer': so.customer, 'submitted': datetime.date(2021, 6, 15), 'status': 'Partly Paid', 'payment_term': None, 'description': '_Test 50-50', 'due_date': datetime.date(2021, 7, 15), 'invoice_portion': 50.0, 'currency': frappe.get_cached_value('Company', '_Test Company', 'default_currency'), 'base_payment_amount': 3500000.0, 'paid_amount': 700000.0, 'invoices': ',' + sinv.name}]
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(data, expected_value)
```


## Complete Example

```python
# Workflow
transaction_date = '2021-06-15'
self.create_payment_terms_template()
self.create_exchange_rate(transaction_date)
item = create_item(item_code='_Test Excavator 2', is_stock_item=0)
so = make_sales_order(transaction_date=transaction_date, currency='USD', delivery_date=add_days(transaction_date, -30), item=item.item_code, qty=10, rate=10000, do_not_save=True)
so.po_no = ''
so.taxes_and_charges = ''
so.taxes = ''
so.payment_terms_template = self.template.name
so.save()
so.submit()
sinv = make_sales_invoice(so.name)
sinv.currency = 'USD'
sinv.taxes_and_charges = ''
sinv.taxes = ''
sinv.items[0].qty = 6
sinv.insert()
sinv.submit()
columns, data, message, chart = execute(frappe._dict({'company': '_Test Company', 'period_start_date': '2021-06-01', 'period_end_date': '2021-06-30', 'item': item.item_code}))
expected_value = [{'name': so.name, 'customer': so.customer, 'submitted': datetime.date(2021, 6, 15), 'status': 'Completed', 'payment_term': None, 'description': '_Test 50-50', 'due_date': datetime.date(2021, 6, 30), 'invoice_portion': 50.0, 'currency': frappe.get_cached_value('Company', '_Test Company', 'default_currency'), 'base_payment_amount': 3500000.0, 'paid_amount': 3500000.0, 'invoices': ',' + sinv.name}, {'name': so.name, 'customer': so.customer, 'submitted': datetime.date(2021, 6, 15), 'status': 'Partly Paid', 'payment_term': None, 'description': '_Test 50-50', 'due_date': datetime.date(2021, 7, 15), 'invoice_portion': 50.0, 'currency': frappe.get_cached_value('Company', '_Test Company', 'default_currency'), 'base_payment_amount': 3500000.0, 'paid_amount': 700000.0, 'invoices': ',' + sinv.name}]
self.assertEqual(data, expected_value)
```

## Next Steps


---

*Source: test_payment_terms_status_for_sales_order.py:151 | Complexity: Advanced | Last updated: 2026-02-04*