# How To: Customer Credit Limit

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test customer credit limit

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
so = make_sales_order(do_not_submit=True)
```

### Step 4: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, so.submit)
```

### Step 5: Assign dn = create_delivery_note(...)

```python
dn = create_delivery_note(do_not_submit=True)
```

### Step 6: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, dn.submit)
```

### Step 7: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(do_not_submit=True)
```

### Step 8: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, si.submit)
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
set_credit_limit('_Test Customer', '_Test Company', outstanding_amt - 50)
```

### Step 12: Call set_credit_limit()

```python
set_credit_limit('_Test Customer', '_Test Company', credit_limit)
```


## Complete Example

```python
# Workflow
from erpnext.accounts.doctype.sales_invoice.test_sales_invoice import create_sales_invoice
from erpnext.selling.doctype.sales_order.test_sales_order import make_sales_order
from erpnext.stock.doctype.delivery_note.test_delivery_note import create_delivery_note
outstanding_amt = self.get_customer_outstanding_amount()
credit_limit = get_credit_limit('_Test Customer', '_Test Company')
if outstanding_amt <= 0.0:
    item_qty = int((abs(outstanding_amt) + 200) / 100)
    make_sales_order(qty=item_qty)
if not credit_limit:
    set_credit_limit('_Test Customer', '_Test Company', outstanding_amt - 50)
so = make_sales_order(do_not_submit=True)
self.assertRaises(frappe.ValidationError, so.submit)
dn = create_delivery_note(do_not_submit=True)
self.assertRaises(frappe.ValidationError, dn.submit)
si = create_sales_invoice(do_not_submit=True)
self.assertRaises(frappe.ValidationError, si.submit)
if credit_limit > outstanding_amt:
    set_credit_limit('_Test Customer', '_Test Company', credit_limit)
```

## Next Steps


---

*Source: test_customer.py:256 | Complexity: Advanced | Last updated: 2026-02-04*