# How To: 01 So To Deliver And Bill

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test 01 so to deliver and bill

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

### Step 3: Assign unknown = execute(...)

```python
columns, data, message, chart = execute({'company': '_Test Company', 'from_date': '2021-06-01', 'to_date': '2021-06-30', 'status': ['To Deliver and Bill']})
```

### Step 4: Assign expected_value = value

```python
expected_value = {'status': 'To Deliver and Bill', 'sales_order': so.name, 'delay_days': frappe.utils.date_diff(frappe.utils.datetime.date.today(), so.delivery_date), 'qty': 10, 'delivered_qty': 0, 'pending_qty': 10, 'qty_to_bill': 10, 'time_taken_to_deliver': 0}
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(len(data), 1)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(data[0][key], val)
```


## Complete Example

```python
# Workflow
transaction_date = '2021-06-01'
item, so = self.create_sales_order(transaction_date)
columns, data, message, chart = execute({'company': '_Test Company', 'from_date': '2021-06-01', 'to_date': '2021-06-30', 'status': ['To Deliver and Bill']})
expected_value = {'status': 'To Deliver and Bill', 'sales_order': so.name, 'delay_days': frappe.utils.date_diff(frappe.utils.datetime.date.today(), so.delivery_date), 'qty': 10, 'delivered_qty': 0, 'pending_qty': 10, 'qty_to_bill': 10, 'time_taken_to_deliver': 0}
self.assertEqual(len(data), 1)
for key, val in expected_value.items():
    with self.subTest(key=key, val=val):
        self.assertEqual(data[0][key], val)
```

## Next Steps


---

*Source: test_sales_order_analysis.py:54 | Complexity: Intermediate | Last updated: 2026-02-04*