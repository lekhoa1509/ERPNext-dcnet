# How To: 04 Due Date Filter

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test 04 due date filter

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

### Step 3: Assign transaction_date = nowdate(...)

```python
transaction_date = nowdate()
```

### Step 4: Assign so = make_sales_order(...)

```python
so = make_sales_order(transaction_date=add_months(transaction_date, -1), delivery_date=add_days(transaction_date, -15), item=item.item_code, qty=10, rate=100000, do_not_save=True)
```

### Step 5: Assign so.po_no = ''

```python
so.po_no = ''
```

### Step 6: Assign so.taxes_and_charges = ''

```python
so.taxes_and_charges = ''
```

### Step 7: Assign so.taxes = ''

```python
so.taxes = ''
```

### Step 8: Assign so.payment_terms_template = value

```python
so.payment_terms_template = self.template.name
```

### Step 9: Call so.save()

```python
so.save()
```

### Step 10: Call so.submit()

```python
so.submit()
```

### Step 11: Assign sinv = make_sales_invoice(...)

```python
sinv = make_sales_invoice(so.name)
```

### Step 12: Assign sinv.taxes_and_charges = ''

```python
sinv.taxes_and_charges = ''
```

### Step 13: Assign sinv.taxes = ''

```python
sinv.taxes = ''
```

### Step 14: Assign unknown.qty = 6

```python
sinv.items[0].qty = 6
```

### Step 15: Call sinv.insert()

```python
sinv.insert()
```

### Step 16: Call sinv.submit()

```python
sinv.submit()
```

### Step 17: Assign first_due_date = add_days(...)

```python
first_due_date = add_days(add_months(transaction_date, -1), 15)
```

### Step 18: Assign unknown = execute(...)

```python
columns, data, message, chart = execute(frappe._dict({'company': '_Test Company', 'item': item.item_code, 'from_due_date': add_months(transaction_date, -1), 'to_due_date': first_due_date}))
```

### Step 19: Assign expected_value = value

```python
expected_value = [{'name': so.name, 'customer': so.customer, 'submitted': datetime.date.fromisoformat(add_months(transaction_date, -1)), 'status': 'Completed', 'payment_term': None, 'description': '_Test 50-50', 'due_date': datetime.date.fromisoformat(first_due_date), 'invoice_portion': 50.0, 'currency': 'INR', 'base_payment_amount': 500000.0, 'paid_amount': 500000.0, 'invoices': ',' + sinv.name}]
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(len(data), 1)
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(data, expected_value)
```


## Complete Example

```python
# Workflow
self.create_payment_terms_template()
item = create_item(item_code='_Test Excavator 1', is_stock_item=0)
transaction_date = nowdate()
so = make_sales_order(transaction_date=add_months(transaction_date, -1), delivery_date=add_days(transaction_date, -15), item=item.item_code, qty=10, rate=100000, do_not_save=True)
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
first_due_date = add_days(add_months(transaction_date, -1), 15)
columns, data, message, chart = execute(frappe._dict({'company': '_Test Company', 'item': item.item_code, 'from_due_date': add_months(transaction_date, -1), 'to_due_date': first_due_date}))
expected_value = [{'name': so.name, 'customer': so.customer, 'submitted': datetime.date.fromisoformat(add_months(transaction_date, -1)), 'status': 'Completed', 'payment_term': None, 'description': '_Test 50-50', 'due_date': datetime.date.fromisoformat(first_due_date), 'invoice_portion': 50.0, 'currency': 'INR', 'base_payment_amount': 500000.0, 'paid_amount': 500000.0, 'invoices': ',' + sinv.name}]
self.assertEqual(len(data), 1)
self.assertEqual(data, expected_value)
```

## Next Steps


---

*Source: test_payment_terms_status_for_sales_order.py:355 | Complexity: Advanced | Last updated: 2026-02-04*