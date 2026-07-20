# How To: Result For Partial Material Request

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test result for partial material request

## Prerequisites

**Required Modules:**
- `frappe.tests`
- `frappe.utils`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.selling.report.pending_so_items_for_purchase_request.pending_so_items_for_purchase_request`


## Step-by-Step Guide

### Step 1: Assign so = make_sales_order(...)

```python
so = make_sales_order()
```

### Step 2: Assign mr = make_material_request(...)

```python
mr = make_material_request(so.name)
```

### Step 3: Assign unknown.qty = 4

```python
mr.items[0].qty = 4
```

### Step 4: Assign mr.schedule_date = add_months(...)

```python
mr.schedule_date = add_months(nowdate(), 1)
```

### Step 5: Call mr.submit()

```python
mr.submit()
```

### Step 6: Assign report = execute(...)

```python
report = execute()
```

### Step 7: Assign l = len(...)

```python
l = len(report[1])
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(so.items[0].qty - mr.items[0].qty, report[1][l - 1]['pending_qty'])
```


## Complete Example

```python
# Workflow
so = make_sales_order()
mr = make_material_request(so.name)
mr.items[0].qty = 4
mr.schedule_date = add_months(nowdate(), 1)
mr.submit()
report = execute()
l = len(report[1])
self.assertEqual(so.items[0].qty - mr.items[0].qty, report[1][l - 1]['pending_qty'])
```

## Next Steps


---

*Source: test_pending_so_items_for_purchase_request.py:16 | Complexity: Advanced | Last updated: 2026-02-04*