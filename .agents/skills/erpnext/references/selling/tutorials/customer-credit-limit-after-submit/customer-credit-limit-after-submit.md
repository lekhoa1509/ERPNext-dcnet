# How To: Customer Credit Limit After Submit

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test customer credit limit after submit

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.party`
- `erpnext.exceptions`
- `erpnext.selling.doctype.customer.customer`
- `erpnext.tests.utils`
- `erpnext.accounts.party`
- `erpnext.accounts.party`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.controllers.accounts_controller`
- `erpnext.selling.doctype.sales_order.test_sales_order`


## Step-by-Step Guide

### Step 1: Assign outstanding_amt = self.get_customer_outstanding_amount(...)

```python
outstanding_amt = self.get_customer_outstanding_amount()
```

### Step 2: Assign credit_limit = get_credit_limit(...)

```python
credit_limit = get_credit_limit('_Test Customer', '_Test Company')
```

### Step 3: Assign so = make_sales_order(...)

```python
so = make_sales_order(rate=100, qty=1)
```

### Step 4: Assign fields = value

```python
fields = ['name', 'item_code', 'delivery_date', 'conversion_factor', 'qty', 'rate', 'uom', 'idx']
```

### Step 5: Assign modified_item = frappe._dict(...)

```python
modified_item = frappe._dict()
```

### Step 6: Assign unknown = value

```python
modified_item['docname'] = so.items[0].name
```

### Step 7: Assign unknown = 2

```python
modified_item['qty'] = 2
```

### Step 8: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, update_child_qty_rate, so.doctype, json.dumps([modified_item]), so.name)
```

### Step 9: Assign item_qty = int(...)

```python
item_qty = int((abs(outstanding_amt) + 200) / 100)
```

### Step 10: Call make_sales_order()

```python
make_sales_order(qty=item_qty)
```

### Step 11: Call set_credit_limit()

```python
set_credit_limit('_Test Customer', '_Test Company', outstanding_amt + 100)
```

### Step 12: Assign unknown = unknown.get(...)

```python
modified_item[x] = so.items[0].get(x)
```


## Complete Example

```python
# Workflow
from erpnext.controllers.accounts_controller import update_child_qty_rate
from erpnext.selling.doctype.sales_order.test_sales_order import make_sales_order
outstanding_amt = self.get_customer_outstanding_amount()
credit_limit = get_credit_limit('_Test Customer', '_Test Company')
if outstanding_amt <= 0.0:
    item_qty = int((abs(outstanding_amt) + 200) / 100)
    make_sales_order(qty=item_qty)
if credit_limit <= 0.0:
    set_credit_limit('_Test Customer', '_Test Company', outstanding_amt + 100)
so = make_sales_order(rate=100, qty=1)
fields = ['name', 'item_code', 'delivery_date', 'conversion_factor', 'qty', 'rate', 'uom', 'idx']
modified_item = frappe._dict()
for x in fields:
    modified_item[x] = so.items[0].get(x)
modified_item['docname'] = so.items[0].name
modified_item['qty'] = 2
self.assertRaises(frappe.ValidationError, update_child_qty_rate, so.doctype, json.dumps([modified_item]), so.name)
```

## Next Steps


---

*Source: test_customer.py:286 | Complexity: Advanced | Last updated: 2026-02-04*