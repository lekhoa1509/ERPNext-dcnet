# How To: Party Details

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test party details

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

### Step 1: Assign to_check = value

```python
to_check = {'selling_price_list': None, 'customer_group': '_Test Customer Group', 'contact_designation': None, 'customer_address': '_Test Address for Customer-Office', 'contact_department': None, 'contact_email': 'test_contact_customer@example.com', 'contact_mobile': None, 'sales_team': [], 'contact_display': '_Test Contact for _Test Customer', 'contact_person': '_Test Contact for _Test Customer-_Test Customer', 'territory': '_Test Territory', 'contact_phone': '+91 0000000000', 'customer_name': '_Test Customer'}
```

### Step 2: Call create_test_contact_and_address()

```python
create_test_contact_and_address()
```

### Step 3: Call frappe.db.set_value()

```python
frappe.db.set_value('Contact', '_Test Contact for _Test Customer-_Test Customer', 'is_primary_contact', 1)
```

### Step 4: Assign details = get_party_details(...)

```python
details = get_party_details('_Test Customer')
```

### Step 5: Assign val = details.get(...)

```python
val = details.get(key)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(value, val)
```

### Step 7: Assign val = None

```python
val = None
```


## Complete Example

```python
# Workflow
from erpnext.accounts.party import get_party_details
to_check = {'selling_price_list': None, 'customer_group': '_Test Customer Group', 'contact_designation': None, 'customer_address': '_Test Address for Customer-Office', 'contact_department': None, 'contact_email': 'test_contact_customer@example.com', 'contact_mobile': None, 'sales_team': [], 'contact_display': '_Test Contact for _Test Customer', 'contact_person': '_Test Contact for _Test Customer-_Test Customer', 'territory': '_Test Territory', 'contact_phone': '+91 0000000000', 'customer_name': '_Test Customer'}
create_test_contact_and_address()
frappe.db.set_value('Contact', '_Test Contact for _Test Customer-_Test Customer', 'is_primary_contact', 1)
details = get_party_details('_Test Customer')
for key, value in to_check.items():
    val = details.get(key)
    if not val and (not isinstance(val, list)):
        val = None
    self.assertEqual(value, val)
```

## Next Steps


---

*Source: test_customer.py:62 | Complexity: Intermediate | Last updated: 2026-02-04*