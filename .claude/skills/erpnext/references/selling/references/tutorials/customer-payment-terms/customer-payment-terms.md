# How To: Customer Payment Terms

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test customer payment terms

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

### Step 1: Call frappe.db.set_value()

```python
frappe.db.set_value('Customer', '_Test Customer With Template', 'payment_terms', '_Test Payment Term Template 3')
```

### Step 2: Assign due_date = get_due_date(...)

```python
due_date = get_due_date('2016-01-22', 'Customer', '_Test Customer With Template')
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(due_date, '2016-02-21')
```

### Step 4: Assign due_date = get_due_date(...)

```python
due_date = get_due_date('2017-01-22', 'Customer', '_Test Customer With Template')
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(due_date, '2017-02-21')
```

### Step 6: Call frappe.db.set_value()

```python
frappe.db.set_value('Customer', '_Test Customer With Template', 'payment_terms', '_Test Payment Term Template 1')
```

### Step 7: Assign due_date = get_due_date(...)

```python
due_date = get_due_date('2016-01-22', 'Customer', '_Test Customer With Template')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(due_date, '2016-02-29')
```

### Step 9: Assign due_date = get_due_date(...)

```python
due_date = get_due_date('2017-01-22', 'Customer', '_Test Customer With Template')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(due_date, '2017-02-28')
```

### Step 11: Call frappe.db.set_value()

```python
frappe.db.set_value('Customer', '_Test Customer With Template', 'payment_terms', '')
```

### Step 12: Assign due_date = get_due_date(...)

```python
due_date = get_due_date('2016-01-22', 'Customer', '_Test Customer')
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(due_date, '2016-01-22')
```

### Step 14: Assign due_date = get_due_date(...)

```python
due_date = get_due_date('2017-01-22', 'Customer', '_Test Customer')
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(due_date, '2017-01-22')
```


## Complete Example

```python
# Workflow
frappe.db.set_value('Customer', '_Test Customer With Template', 'payment_terms', '_Test Payment Term Template 3')
due_date = get_due_date('2016-01-22', 'Customer', '_Test Customer With Template')
self.assertEqual(due_date, '2016-02-21')
due_date = get_due_date('2017-01-22', 'Customer', '_Test Customer With Template')
self.assertEqual(due_date, '2017-02-21')
frappe.db.set_value('Customer', '_Test Customer With Template', 'payment_terms', '_Test Payment Term Template 1')
due_date = get_due_date('2016-01-22', 'Customer', '_Test Customer With Template')
self.assertEqual(due_date, '2016-02-29')
due_date = get_due_date('2017-01-22', 'Customer', '_Test Customer With Template')
self.assertEqual(due_date, '2017-02-28')
frappe.db.set_value('Customer', '_Test Customer With Template', 'payment_terms', '')
due_date = get_due_date('2016-01-22', 'Customer', '_Test Customer')
self.assertEqual(due_date, '2016-01-22')
due_date = get_due_date('2017-01-22', 'Customer', '_Test Customer')
self.assertEqual(due_date, '2017-01-22')
```

## Next Steps


---

*Source: test_customer.py:329 | Complexity: Advanced | Last updated: 2026-02-04*