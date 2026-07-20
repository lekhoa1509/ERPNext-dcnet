# How To: Item Shortage Report

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test item shortage report

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.report.item_shortage_report.item_shortage_report`


## Step-by-Step Guide

### Step 1: Assign item = value

```python
item = make_item().name
```

### Step 2: Assign so = make_sales_order(...)

```python
so = make_sales_order(item_code=item)
```

### Step 3: Assign unknown = frappe.db.get_value(...)

```python
reserved_qty, projected_qty = frappe.db.get_value('Bin', {'item_code': item, 'warehouse': so.items[0].warehouse}, ['reserved_qty', 'projected_qty'])
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(reserved_qty, so.items[0].qty)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(projected_qty, -so.items[0].qty)
```

### Step 6: Assign filters = value

```python
filters = {'company': so.company}
```

### Step 7: Assign report_data = value

```python
report_data = item_shortage_report(filters)[1]
```

### Step 8: Assign item_code_list = value

```python
item_code_list = [row.get('item_code') for row in report_data]
```

### Step 9: Call self.assertIn()

```python
self.assertIn(item, item_code_list)
```

### Step 10: Assign filters = value

```python
filters = {'company': so.company, 'warehouse': [so.items[0].warehouse]}
```

### Step 11: Assign report_data = value

```python
report_data = item_shortage_report(filters)[1]
```

### Step 12: Assign item_code_list = value

```python
item_code_list = [row.get('item_code') for row in report_data]
```

### Step 13: Call self.assertIn()

```python
self.assertIn(item, item_code_list)
```

### Step 14: Assign filters = value

```python
filters = {'company': so.company, 'warehouse': ['Work In Progress - _TC']}
```

### Step 15: Assign report_data = value

```python
report_data = item_shortage_report(filters)[1]
```

### Step 16: Assign item_code_list = value

```python
item_code_list = [row.get('item_code') for row in report_data]
```

### Step 17: Call self.assertNotIn()

```python
self.assertNotIn(item, item_code_list)
```


## Complete Example

```python
# Workflow
item = make_item().name
so = make_sales_order(item_code=item)
reserved_qty, projected_qty = frappe.db.get_value('Bin', {'item_code': item, 'warehouse': so.items[0].warehouse}, ['reserved_qty', 'projected_qty'])
self.assertEqual(reserved_qty, so.items[0].qty)
self.assertEqual(projected_qty, -so.items[0].qty)
filters = {'company': so.company}
report_data = item_shortage_report(filters)[1]
item_code_list = [row.get('item_code') for row in report_data]
self.assertIn(item, item_code_list)
filters = {'company': so.company, 'warehouse': [so.items[0].warehouse]}
report_data = item_shortage_report(filters)[1]
item_code_list = [row.get('item_code') for row in report_data]
self.assertIn(item, item_code_list)
filters = {'company': so.company, 'warehouse': ['Work In Progress - _TC']}
report_data = item_shortage_report(filters)[1]
item_code_list = [row.get('item_code') for row in report_data]
self.assertNotIn(item, item_code_list)
```

## Next Steps


---

*Source: test_item_shortage_report.py:15 | Complexity: Advanced | Last updated: 2026-02-04*