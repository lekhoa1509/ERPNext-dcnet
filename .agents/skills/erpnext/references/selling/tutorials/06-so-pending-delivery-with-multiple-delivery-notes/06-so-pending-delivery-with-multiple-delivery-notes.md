# How To: 06 So Pending Delivery With Multiple Delivery Notes

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test 06 so pending delivery with multiple delivery notes

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

### Step 3: Assign sinv1 = self.create_sales_invoice(...)

```python
sinv1 = self.create_sales_invoice(so, do_not_save=True)
```

### Step 4: Assign unknown.qty = 2

```python
sinv1.items[0].qty = 2
```

### Step 5: Assign sinv1 = sinv1.save.submit(...)

```python
sinv1 = sinv1.save().submit()
```

### Step 6: Assign dn1 = self.create_delivery_note(...)

```python
dn1 = self.create_delivery_note(so, do_not_save=True)
```

### Step 7: Assign unknown.qty = 2

```python
dn1.items[0].qty = 2
```

### Step 8: Assign dn1 = dn1.save.submit(...)

```python
dn1 = dn1.save().submit()
```

### Step 9: Assign sinv2 = self.create_sales_invoice(...)

```python
sinv2 = self.create_sales_invoice(so, do_not_save=True)
```

### Step 10: Assign unknown.qty = 2

```python
sinv2.items[0].qty = 2
```

### Step 11: Assign sinv2 = sinv2.save.submit(...)

```python
sinv2 = sinv2.save().submit()
```

### Step 12: Assign dn2 = self.create_delivery_note(...)

```python
dn2 = self.create_delivery_note(so, do_not_save=True)
```

### Step 13: Assign unknown.qty = 1

```python
dn2.items[0].qty = 1
```

### Step 14: Assign dn2 = dn2.save.submit(...)

```python
dn2 = dn2.save().submit()
```

### Step 15: Assign unknown = execute(...)

```python
columns, data, message, chart = execute({'company': '_Test Company', 'from_date': '2021-06-01', 'to_date': '2021-06-30', 'sales_order': [so.name]})
```

### Step 16: Assign expected_value = value

```python
expected_value = {'status': 'To Deliver and Bill', 'sales_order': so.name, 'delay_days': frappe.utils.date_diff(frappe.utils.datetime.date.today(), so.delivery_date), 'qty': 10, 'delivered_qty': 3, 'pending_qty': 7, 'qty_to_bill': 6, 'billed_qty': 4, 'time_taken_to_deliver': 0}
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(len(data), 1)
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(data[0][key], val)
```


## Complete Example

```python
# Workflow
transaction_date = '2021-06-01'
item, so = self.create_sales_order(transaction_date)
sinv1 = self.create_sales_invoice(so, do_not_save=True)
sinv1.items[0].qty = 2
sinv1 = sinv1.save().submit()
dn1 = self.create_delivery_note(so, do_not_save=True)
dn1.items[0].qty = 2
dn1 = dn1.save().submit()
sinv2 = self.create_sales_invoice(so, do_not_save=True)
sinv2.items[0].qty = 2
sinv2 = sinv2.save().submit()
dn2 = self.create_delivery_note(so, do_not_save=True)
dn2.items[0].qty = 1
dn2 = dn2.save().submit()
columns, data, message, chart = execute({'company': '_Test Company', 'from_date': '2021-06-01', 'to_date': '2021-06-30', 'sales_order': [so.name]})
expected_value = {'status': 'To Deliver and Bill', 'sales_order': so.name, 'delay_days': frappe.utils.date_diff(frappe.utils.datetime.date.today(), so.delivery_date), 'qty': 10, 'delivered_qty': 3, 'pending_qty': 7, 'qty_to_bill': 6, 'billed_qty': 4, 'time_taken_to_deliver': 0}
self.assertEqual(len(data), 1)
for key, val in expected_value.items():
    with self.subTest(key=key, val=val):
        self.assertEqual(data[0][key], val)
```

## Next Steps


---

*Source: test_sales_order_analysis.py:174 | Complexity: Advanced | Last updated: 2026-02-04*