# How To: Sales Order Creation

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test sales order creation

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext`
- `erpnext.stock.doctype.item.test_item`
- `blanket_order`


## Step-by-Step Guide

### Step 1: Assign bo = make_blanket_order(...)

```python
bo = make_blanket_order(blanket_order_type='Selling')
```

### Step 2: Assign frappe.flags.args.doctype = 'Sales Order'

```python
frappe.flags.args.doctype = 'Sales Order'
```

### Step 3: Assign so = make_order(...)

```python
so = make_order(bo.name)
```

### Step 4: Assign so.currency = get_company_currency(...)

```python
so.currency = get_company_currency(so.company)
```

### Step 5: Assign so.delivery_date = today(...)

```python
so.delivery_date = today()
```

### Step 6: Assign unknown.qty = 10

```python
so.items[0].qty = 10
```

### Step 7: Call so.submit()

```python
so.submit()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(so.doctype, 'Sales Order')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(len(so.get('items')), len(bo.get('items')))
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(so.items[0].rate, bo.items[0].rate)
```

### Step 11: Assign bo = frappe.get_doc(...)

```python
bo = frappe.get_doc('Blanket Order', bo.name)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(so.items[0].qty, bo.items[0].ordered_qty)
```

### Step 13: Assign frappe.flags.args.doctype = 'Sales Order'

```python
frappe.flags.args.doctype = 'Sales Order'
```

### Step 14: Assign so1 = make_order(...)

```python
so1 = make_order(bo.name)
```

### Step 15: Assign so1.currency = get_company_currency(...)

```python
so1.currency = get_company_currency(so1.company)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(so1.items[0].qty, bo.items[0].qty - bo.items[0].ordered_qty)
```


## Complete Example

```python
# Workflow
bo = make_blanket_order(blanket_order_type='Selling')
frappe.flags.args.doctype = 'Sales Order'
so = make_order(bo.name)
so.currency = get_company_currency(so.company)
so.delivery_date = today()
so.items[0].qty = 10
so.submit()
self.assertEqual(so.doctype, 'Sales Order')
self.assertEqual(len(so.get('items')), len(bo.get('items')))
self.assertEqual(so.items[0].rate, bo.items[0].rate)
bo = frappe.get_doc('Blanket Order', bo.name)
self.assertEqual(so.items[0].qty, bo.items[0].ordered_qty)
frappe.flags.args.doctype = 'Sales Order'
so1 = make_order(bo.name)
so1.currency = get_company_currency(so1.company)
self.assertEqual(so1.items[0].qty, bo.items[0].qty - bo.items[0].ordered_qty)
```

## Next Steps


---

*Source: test_blanket_order.py:17 | Complexity: Advanced | Last updated: 2026-02-04*