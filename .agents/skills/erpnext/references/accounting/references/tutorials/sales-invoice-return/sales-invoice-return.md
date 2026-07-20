# How To: Sales Invoice Return

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test sales invoice return

## Prerequisites

**Required Modules:**
- `unittest`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.loyalty_program.loyalty_program`
- `erpnext.accounts.party`


## Step-by-Step Guide

### Step 1: Call frappe.db.set_value()

```python
frappe.db.set_value('Customer', 'Test Loyalty Customer', 'loyalty_program', 'Test Single Loyalty')
```

### Step 2: Assign si_original = create_sales_invoice_record(...)

```python
si_original = create_sales_invoice_record(2)
```

### Step 3: Assign si_original.conversion_rate = flt(...)

```python
si_original.conversion_rate = flt(1)
```

### Step 4: Call si_original.insert()

```python
si_original.insert()
```

### Step 5: Call si_original.submit()

```python
si_original.submit()
```

### Step 6: Assign earned_points = get_points_earned(...)

```python
earned_points = get_points_earned(si_original)
```

### Step 7: Assign lpe_original = frappe.get_doc(...)

```python
lpe_original = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_original.name, 'customer': si_original.customer})
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(lpe_original.loyalty_points, earned_points)
```

### Step 9: Assign si_return = create_sales_invoice_record(...)

```python
si_return = create_sales_invoice_record(-1)
```

### Step 10: Assign si_return.conversion_rate = flt(...)

```python
si_return.conversion_rate = flt(1)
```

### Step 11: Assign si_return.is_return = 1

```python
si_return.is_return = 1
```

### Step 12: Assign si_return.return_against = value

```python
si_return.return_against = si_original.name
```

### Step 13: Call si_return.insert()

```python
si_return.insert()
```

### Step 14: Call si_return.submit()

```python
si_return.submit()
```

### Step 15: Assign si_original = frappe.get_doc(...)

```python
si_original = frappe.get_doc('Sales Invoice', lpe_original.invoice)
```

### Step 16: Assign earned_points = get_points_earned(...)

```python
earned_points = get_points_earned(si_original)
```

### Step 17: Assign lpe_after_return = frappe.get_doc(...)

```python
lpe_after_return = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_original.name, 'customer': si_original.customer})
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(lpe_after_return.loyalty_points, earned_points)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(True, lpe_original.loyalty_points > lpe_after_return.loyalty_points)
```

### Step 20: Call d.cancel()

```python
d.cancel()
```

### Step 21: Call frappe.get_doc.cancel()

```python
frappe.get_doc('Sales Invoice', d.name).cancel()
```


## Complete Example

```python
# Workflow
frappe.db.set_value('Customer', 'Test Loyalty Customer', 'loyalty_program', 'Test Single Loyalty')
si_original = create_sales_invoice_record(2)
si_original.conversion_rate = flt(1)
si_original.insert()
si_original.submit()
earned_points = get_points_earned(si_original)
lpe_original = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_original.name, 'customer': si_original.customer})
self.assertEqual(lpe_original.loyalty_points, earned_points)
si_return = create_sales_invoice_record(-1)
si_return.conversion_rate = flt(1)
si_return.is_return = 1
si_return.return_against = si_original.name
si_return.insert()
si_return.submit()
si_original = frappe.get_doc('Sales Invoice', lpe_original.invoice)
earned_points = get_points_earned(si_original)
lpe_after_return = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_original.name, 'customer': si_original.customer})
self.assertEqual(lpe_after_return.loyalty_points, earned_points)
self.assertEqual(True, lpe_original.loyalty_points > lpe_after_return.loyalty_points)
for d in [si_return, si_original]:
    try:
        d.cancel()
    except frappe.TimestampMismatchError:
        frappe.get_doc('Sales Invoice', d.name).cancel()
```

## Next Steps


---

*Source: test_loyalty_program.py:148 | Complexity: Advanced | Last updated: 2026-02-03*