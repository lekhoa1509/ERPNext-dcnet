# How To: Purchase Order Creation

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test purchase order creation

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
bo = make_blanket_order(blanket_order_type='Purchasing')
```

### Step 2: Assign frappe.flags.args.doctype = 'Purchase Order'

```python
frappe.flags.args.doctype = 'Purchase Order'
```

### Step 3: Assign po = make_order(...)

```python
po = make_order(bo.name)
```

### Step 4: Assign po.currency = get_company_currency(...)

```python
po.currency = get_company_currency(po.company)
```

### Step 5: Assign po.schedule_date = today(...)

```python
po.schedule_date = today()
```

### Step 6: Assign unknown.qty = 10

```python
po.items[0].qty = 10
```

### Step 7: Call po.submit()

```python
po.submit()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(po.doctype, 'Purchase Order')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(len(po.get('items')), len(bo.get('items')))
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(po.items[0].rate, po.items[0].rate)
```

### Step 11: Assign bo = frappe.get_doc(...)

```python
bo = frappe.get_doc('Blanket Order', bo.name)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(po.items[0].qty, bo.items[0].ordered_qty)
```

### Step 13: Assign frappe.flags.args.doctype = 'Purchase Order'

```python
frappe.flags.args.doctype = 'Purchase Order'
```

### Step 14: Assign po1 = make_order(...)

```python
po1 = make_order(bo.name)
```

### Step 15: Assign po1.currency = get_company_currency(...)

```python
po1.currency = get_company_currency(po1.company)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(po1.items[0].qty, bo.items[0].qty - bo.items[0].ordered_qty)
```


## Complete Example

```python
# Workflow
bo = make_blanket_order(blanket_order_type='Purchasing')
frappe.flags.args.doctype = 'Purchase Order'
po = make_order(bo.name)
po.currency = get_company_currency(po.company)
po.schedule_date = today()
po.items[0].qty = 10
po.submit()
self.assertEqual(po.doctype, 'Purchase Order')
self.assertEqual(len(po.get('items')), len(bo.get('items')))
self.assertEqual(po.items[0].rate, po.items[0].rate)
bo = frappe.get_doc('Blanket Order', bo.name)
self.assertEqual(po.items[0].qty, bo.items[0].ordered_qty)
frappe.flags.args.doctype = 'Purchase Order'
po1 = make_order(bo.name)
po1.currency = get_company_currency(po1.company)
self.assertEqual(po1.items[0].qty, bo.items[0].qty - bo.items[0].ordered_qty)
```

## Next Steps


---

*Source: test_blanket_order.py:42 | Complexity: Advanced | Last updated: 2026-02-04*