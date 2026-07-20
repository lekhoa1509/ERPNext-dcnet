# How To: Loyalty Points Earned Single Tier

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test loyalty points earned single tier

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
si_original = create_sales_invoice_record()
```

### Step 3: Call si_original.insert()

```python
si_original.insert()
```

### Step 4: Call si_original.submit()

```python
si_original.submit()
```

### Step 5: Assign customer = frappe.get_doc(...)

```python
customer = frappe.get_doc('Customer', {'customer_name': 'Test Loyalty Customer'})
```

### Step 6: Assign earned_points = get_points_earned(...)

```python
earned_points = get_points_earned(si_original)
```

### Step 7: Assign lpe = frappe.get_doc(...)

```python
lpe = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_original.name, 'customer': si_original.customer})
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(si_original.get('loyalty_program'), customer.loyalty_program)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(lpe.get('loyalty_program_tier'), 'Bronce')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(lpe.get('loyalty_program_tier'), customer.loyalty_program_tier)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(lpe.loyalty_points, earned_points)
```

### Step 12: Assign si_redeem = create_sales_invoice_record(...)

```python
si_redeem = create_sales_invoice_record()
```

### Step 13: Assign si_redeem.redeem_loyalty_points = 1

```python
si_redeem.redeem_loyalty_points = 1
```

### Step 14: Assign si_redeem.loyalty_points = earned_points

```python
si_redeem.loyalty_points = earned_points
```

### Step 15: Call si_redeem.insert()

```python
si_redeem.insert()
```

### Step 16: Call si_redeem.submit()

```python
si_redeem.submit()
```

### Step 17: Assign earned_after_redemption = get_points_earned(...)

```python
earned_after_redemption = get_points_earned(si_redeem)
```

### Step 18: Assign lpe_redeem = frappe.get_doc(...)

```python
lpe_redeem = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_redeem.name, 'redeem_against': lpe.name})
```

### Step 19: Assign lpe_earn = frappe.get_doc(...)

```python
lpe_earn = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_redeem.name, 'name': ['!=', lpe_redeem.name]})
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(lpe_earn.loyalty_points, earned_after_redemption)
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(lpe_redeem.loyalty_points, -1 * earned_points)
```

### Step 22: Call d.cancel()

```python
d.cancel()
```


## Complete Example

```python
# Workflow
frappe.db.set_value('Customer', 'Test Loyalty Customer', 'loyalty_program', 'Test Single Loyalty')
si_original = create_sales_invoice_record()
si_original.insert()
si_original.submit()
customer = frappe.get_doc('Customer', {'customer_name': 'Test Loyalty Customer'})
earned_points = get_points_earned(si_original)
lpe = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_original.name, 'customer': si_original.customer})
self.assertEqual(si_original.get('loyalty_program'), customer.loyalty_program)
self.assertEqual(lpe.get('loyalty_program_tier'), 'Bronce')
self.assertEqual(lpe.get('loyalty_program_tier'), customer.loyalty_program_tier)
self.assertEqual(lpe.loyalty_points, earned_points)
si_redeem = create_sales_invoice_record()
si_redeem.redeem_loyalty_points = 1
si_redeem.loyalty_points = earned_points
si_redeem.insert()
si_redeem.submit()
earned_after_redemption = get_points_earned(si_redeem)
lpe_redeem = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_redeem.name, 'redeem_against': lpe.name})
lpe_earn = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_redeem.name, 'name': ['!=', lpe_redeem.name]})
self.assertEqual(lpe_earn.loyalty_points, earned_after_redemption)
self.assertEqual(lpe_redeem.loyalty_points, -1 * earned_points)
for d in [si_redeem, si_original]:
    d.cancel()
```

## Next Steps


---

*Source: test_loyalty_program.py:23 | Complexity: Advanced | Last updated: 2026-02-03*