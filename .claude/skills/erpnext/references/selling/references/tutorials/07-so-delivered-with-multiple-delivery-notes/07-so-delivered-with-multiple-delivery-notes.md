# How To: 07 So Delivered With Multiple Delivery Notes

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test 07 so delivered with multiple delivery notes

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

### Step 3: Assign dn1 = self.create_delivery_note(...)

```python
dn1 = self.create_delivery_note(so, do_not_save=True)
```

### Step 4: Assign unknown.qty = 5

```python
dn1.items[0].qty = 5
```

### Step 5: Assign dn1 = dn1.save.submit(...)

```python
dn1 = dn1.save().submit()
```

### Step 6: Assign dn2 = self.create_delivery_note(...)

```python
dn2 = self.create_delivery_note(so, do_not_save=True)
```

### Step 7: Assign unknown.qty = 5

```python
dn2.items[0].qty = 5
```

### Step 8: Assign dn2 = dn2.save.submit(...)

```python
dn2 = dn2.save().submit()
```

### Step 9: Assign unknown = execute(...)

```python
columns, data, message, chart = execute({'company': '_Test Company', 'from_date': '2021-06-01', 'to_date': '2021-06-30', 'sales_order': [so.name]})
```

### Step 10: Assign expected_value = value

```python
expected_value = {'status': 'To Bill', 'sales_order': so.name, 'delay_days': frappe.utils.date_diff(frappe.utils.datetime.date.today(), so.delivery_date), 'qty': 10, 'delivered_qty': 10, 'pending_qty': 0, 'qty_to_bill': 10, 'billed_qty': 0, 'time_taken_to_deliver': 86400}
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(len(data), 1)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(data[0][key], val)
```


## Complete Example

```python
# Workflow
transaction_date = '2021-06-01'
item, so = self.create_sales_order(transaction_date)
dn1 = self.create_delivery_note(so, do_not_save=True)
dn1.items[0].qty = 5
dn1 = dn1.save().submit()
dn2 = self.create_delivery_note(so, do_not_save=True)
dn2.items[0].qty = 5
dn2 = dn2.save().submit()
columns, data, message, chart = execute({'company': '_Test Company', 'from_date': '2021-06-01', 'to_date': '2021-06-30', 'sales_order': [so.name]})
expected_value = {'status': 'To Bill', 'sales_order': so.name, 'delay_days': frappe.utils.date_diff(frappe.utils.datetime.date.today(), so.delivery_date), 'qty': 10, 'delivered_qty': 10, 'pending_qty': 0, 'qty_to_bill': 10, 'billed_qty': 0, 'time_taken_to_deliver': 86400}
self.assertEqual(len(data), 1)
for key, val in expected_value.items():
    with self.subTest(key=key, val=val):
        self.assertEqual(data[0][key], val)
```

## Next Steps


---

*Source: test_sales_order_analysis.py:220 | Complexity: Advanced | Last updated: 2026-02-04*