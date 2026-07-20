# How To: Supplier Default Payment Terms

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test supplier default payment terms

## Prerequisites

**Required Modules:**
- `frappe`
- `erpnext.accounts.party`
- `erpnext.controllers.website_list_for_contact`
- `erpnext.exceptions`
- `frappe.tests`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.accounts.party`


## Step-by-Step Guide

### Step 1: Call frappe.db.set_value()

```python
frappe.db.set_value('Supplier', '_Test Supplier With Template 1', 'payment_terms', '_Test Payment Term Template 3')
```

### Step 2: Assign due_date = get_due_date(...)

```python
due_date = get_due_date('2016-01-22', 'Supplier', '_Test Supplier With Template 1')
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(due_date, '2016-02-21')
```

### Step 4: Assign due_date = get_due_date(...)

```python
due_date = get_due_date('2017-01-22', 'Supplier', '_Test Supplier With Template 1')
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(due_date, '2017-02-21')
```

### Step 6: Call frappe.db.set_value()

```python
frappe.db.set_value('Supplier', '_Test Supplier With Template 1', 'payment_terms', '_Test Payment Term Template 1')
```

### Step 7: Assign due_date = get_due_date(...)

```python
due_date = get_due_date('2016-01-22', 'Supplier', '_Test Supplier With Template 1')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(due_date, '2016-02-29')
```

### Step 9: Assign due_date = get_due_date(...)

```python
due_date = get_due_date('2017-01-22', 'Supplier', '_Test Supplier With Template 1')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(due_date, '2017-02-28')
```

### Step 11: Call frappe.db.set_value()

```python
frappe.db.set_value('Supplier', '_Test Supplier With Template 1', 'payment_terms', '')
```

### Step 12: Call frappe.db.set_value()

```python
frappe.db.set_value('Supplier Group', '_Test Supplier Group', 'payment_terms', '_Test Payment Term Template 3')
```

### Step 13: Assign due_date = get_due_date(...)

```python
due_date = get_due_date('2016-01-22', 'Supplier', '_Test Supplier With Template 1')
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(due_date, '2016-02-21')
```

### Step 15: Call frappe.db.set_value()

```python
frappe.db.set_value('Supplier Group', '_Test Supplier Group', 'payment_terms', '_Test Payment Term Template 1')
```

### Step 16: Assign due_date = get_due_date(...)

```python
due_date = get_due_date('2016-01-22', 'Supplier', '_Test Supplier With Template 1')
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(due_date, '2016-02-29')
```

### Step 18: Assign due_date = get_due_date(...)

```python
due_date = get_due_date('2017-01-22', 'Supplier', '_Test Supplier With Template 1')
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(due_date, '2017-02-28')
```

### Step 20: Call frappe.db.set_value()

```python
frappe.db.set_value('Supplier Group', '_Test Supplier Group', 'payment_terms', '')
```

### Step 21: Call frappe.db.set_value()

```python
frappe.db.set_value('Supplier', '_Test Supplier', 'payment_terms', '')
```

### Step 22: Assign due_date = get_due_date(...)

```python
due_date = get_due_date('2016-01-22', 'Supplier', '_Test Supplier')
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(due_date, '2016-01-22')
```

### Step 24: Assign due_date = get_due_date(...)

```python
due_date = get_due_date('2017-01-22', 'Supplier', '_Test Supplier')
```

### Step 25: Call self.assertEqual()

```python
self.assertEqual(due_date, '2017-01-22')
```


## Complete Example

```python
# Workflow
frappe.db.set_value('Supplier', '_Test Supplier With Template 1', 'payment_terms', '_Test Payment Term Template 3')
due_date = get_due_date('2016-01-22', 'Supplier', '_Test Supplier With Template 1')
self.assertEqual(due_date, '2016-02-21')
due_date = get_due_date('2017-01-22', 'Supplier', '_Test Supplier With Template 1')
self.assertEqual(due_date, '2017-02-21')
frappe.db.set_value('Supplier', '_Test Supplier With Template 1', 'payment_terms', '_Test Payment Term Template 1')
due_date = get_due_date('2016-01-22', 'Supplier', '_Test Supplier With Template 1')
self.assertEqual(due_date, '2016-02-29')
due_date = get_due_date('2017-01-22', 'Supplier', '_Test Supplier With Template 1')
self.assertEqual(due_date, '2017-02-28')
frappe.db.set_value('Supplier', '_Test Supplier With Template 1', 'payment_terms', '')
frappe.db.set_value('Supplier Group', '_Test Supplier Group', 'payment_terms', '_Test Payment Term Template 3')
due_date = get_due_date('2016-01-22', 'Supplier', '_Test Supplier With Template 1')
self.assertEqual(due_date, '2016-02-21')
frappe.db.set_value('Supplier Group', '_Test Supplier Group', 'payment_terms', '_Test Payment Term Template 1')
due_date = get_due_date('2016-01-22', 'Supplier', '_Test Supplier With Template 1')
self.assertEqual(due_date, '2016-02-29')
due_date = get_due_date('2017-01-22', 'Supplier', '_Test Supplier With Template 1')
self.assertEqual(due_date, '2017-02-28')
frappe.db.set_value('Supplier Group', '_Test Supplier Group', 'payment_terms', '')
frappe.db.set_value('Supplier', '_Test Supplier', 'payment_terms', '')
due_date = get_due_date('2016-01-22', 'Supplier', '_Test Supplier')
self.assertEqual(due_date, '2016-01-22')
due_date = get_due_date('2017-01-22', 'Supplier', '_Test Supplier')
self.assertEqual(due_date, '2017-01-22')
```

## Next Steps


---

*Source: test_supplier.py:42 | Complexity: Advanced | Last updated: 2026-02-04*