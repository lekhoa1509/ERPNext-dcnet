# How To: Parse Full Name

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test parse full name

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

### Step 1: Assign unknown = parse_full_name(...)

```python
first, middle, last = parse_full_name('John')
```

### Step 2: Call self.assertEqual()

```python
self.assertEqual(first, 'John')
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(middle, None)
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(last, None)
```

### Step 5: Assign unknown = parse_full_name(...)

```python
first, middle, last = parse_full_name('John Doe')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(first, 'John')
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(middle, None)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(last, 'Doe')
```

### Step 9: Assign unknown = parse_full_name(...)

```python
first, middle, last = parse_full_name('John Michael Doe')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(first, 'John')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(middle, 'Michael')
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(last, 'Doe')
```


## Complete Example

```python
# Workflow
first, middle, last = parse_full_name('John')
self.assertEqual(first, 'John')
self.assertEqual(middle, None)
self.assertEqual(last, None)
first, middle, last = parse_full_name('John Doe')
self.assertEqual(first, 'John')
self.assertEqual(middle, None)
self.assertEqual(last, 'Doe')
first, middle, last = parse_full_name('John Michael Doe')
self.assertEqual(first, 'John')
self.assertEqual(middle, 'Michael')
self.assertEqual(last, 'Doe')
```

## Next Steps


---

*Source: test_customer.py:359 | Complexity: Advanced | Last updated: 2026-02-04*