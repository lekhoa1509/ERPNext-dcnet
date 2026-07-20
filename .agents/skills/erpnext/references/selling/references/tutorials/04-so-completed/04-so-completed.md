# How To: 04 So Completed

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test 04 so completed

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.selling.report.sales_order_analysis.sales_order_analysis`
- `erpnext.stock.doctype.item.test_item`


## Step-by-Step Guide

### Step 1: Assign transaction_date = '2021-06-01'

```python
transaction_date = '2021-06-01'
```

### Step 2: Assign unknown = self.create_sales_order(...)

```python
item, so = self.create_sales_order(transaction_date)
```

### Step 3: Call self.create_sales_invoice()

```python
self.create_sales_invoice(so)
```

### Step 4: Call self.create_delivery_note()

```python
self.create_delivery_note(so)
```

### Step 5: Assign unknown = execute(...)

```python
columns, data, message, chart = execute({'company': '_Test Company', 'from_date': '2021-06-01', 'to_date': '2021-06-30', 'status': ['Completed']})
```

### Step 6: Assign expected_value = value

```python
expected_value = {'status': 'Completed', 'sales_order': so.name, 'delay_days': frappe.utils.date_diff(frappe.utils.datetime.date.today(), so.delivery_date), 'qty': 10, 'delivered_qty': 10, 'pending_qty': 0, 'qty_to_bill': 0, 'billed_qty': 10, 'time_taken_to_deliver': 86400}
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(len(data), 1)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(data[0][key], val)
```


## Complete Example

```python
# Workflow
transaction_date = '2021-06-01'
item, so = self.create_sales_order(transaction_date)
self.create_sales_invoice(so)
self.create_delivery_note(so)
columns, data, message, chart = execute({'company': '_Test Company', 'from_date': '2021-06-01', 'to_date': '2021-06-30', 'status': ['Completed']})
expected_value = {'status': 'Completed', 'sales_order': so.name, 'delay_days': frappe.utils.date_diff(frappe.utils.datetime.date.today(), so.delivery_date), 'qty': 10, 'delivered_qty': 10, 'pending_qty': 0, 'qty_to_bill': 0, 'billed_qty': 10, 'time_taken_to_deliver': 86400}
self.assertEqual(len(data), 1)
for key, val in expected_value.items():
    with self.subTest(key=key, val=val):
        self.assertEqual(data[0][key], val)
```

## Next Steps


---

*Source: test_sales_order_analysis.py:134 | Complexity: Advanced | Last updated: 2026-02-04*