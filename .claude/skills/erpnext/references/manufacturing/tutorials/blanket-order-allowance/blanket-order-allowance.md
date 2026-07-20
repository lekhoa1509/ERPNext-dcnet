# How To: Blanket Order Allowance

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test blanket order allowance

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
bo = make_blanket_order(blanket_order_type='Selling', quantity=100)
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

### Step 6: Assign unknown.qty = 110

```python
so.items[0].qty = 110
```

### Step 7: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, so.submit)
```

### Step 8: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('Selling Settings', 'blanket_order_allowance', 10)
```

### Step 9: Call so.submit()

```python
so.submit()
```

### Step 10: Assign bo = make_blanket_order(...)

```python
bo = make_blanket_order(blanket_order_type='Purchasing', quantity=100)
```

### Step 11: Assign frappe.flags.args.doctype = 'Purchase Order'

```python
frappe.flags.args.doctype = 'Purchase Order'
```

### Step 12: Assign po = make_order(...)

```python
po = make_order(bo.name)
```

### Step 13: Assign po.currency = get_company_currency(...)

```python
po.currency = get_company_currency(po.company)
```

### Step 14: Assign po.schedule_date = today(...)

```python
po.schedule_date = today()
```

### Step 15: Assign unknown.qty = 110

```python
po.items[0].qty = 110
```

### Step 16: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, po.submit)
```

### Step 17: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('Buying Settings', 'blanket_order_allowance', 10)
```

### Step 18: Call po.submit()

```python
po.submit()
```


## Complete Example

```python
# Workflow
bo = make_blanket_order(blanket_order_type='Selling', quantity=100)
frappe.flags.args.doctype = 'Sales Order'
so = make_order(bo.name)
so.currency = get_company_currency(so.company)
so.delivery_date = today()
so.items[0].qty = 110
self.assertRaises(frappe.ValidationError, so.submit)
frappe.db.set_single_value('Selling Settings', 'blanket_order_allowance', 10)
so.submit()
bo = make_blanket_order(blanket_order_type='Purchasing', quantity=100)
frappe.flags.args.doctype = 'Purchase Order'
po = make_order(bo.name)
po.currency = get_company_currency(po.company)
po.schedule_date = today()
po.items[0].qty = 110
self.assertRaises(frappe.ValidationError, po.submit)
frappe.db.set_single_value('Buying Settings', 'blanket_order_allowance', 10)
po.submit()
```

## Next Steps


---

*Source: test_blanket_order.py:67 | Complexity: Advanced | Last updated: 2026-02-04*