# How To: Loyalty Points Earned Multiple Tier

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test loyalty points earned multiple tier

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
frappe.db.set_value('Customer', 'Test Loyalty Customer', 'loyalty_program', 'Test Multiple Loyalty')
```

### Step 2: Assign customer = frappe.get_doc(...)

```python
customer = frappe.get_doc('Customer', {'customer_name': 'Test Loyalty Customer'})
```

### Step 3: Assign customer.loyalty_program = value

```python
customer.loyalty_program = frappe.get_doc('Loyalty Program', {'loyalty_program_name': 'Test Multiple Loyalty'}).name
```

### Step 4: Call customer.save()

```python
customer.save()
```

### Step 5: Assign si_original = create_sales_invoice_record(...)

```python
si_original = create_sales_invoice_record()
```

### Step 6: Call si_original.insert()

```python
si_original.insert()
```

### Step 7: Call si_original.submit()

```python
si_original.submit()
```

### Step 8: Call customer.reload()

```python
customer.reload()
```

### Step 9: Assign earned_points = get_points_earned(...)

```python
earned_points = get_points_earned(si_original)
```

### Step 10: Assign lpe = frappe.get_doc(...)

```python
lpe = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_original.name, 'customer': si_original.customer})
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(si_original.get('loyalty_program'), customer.loyalty_program)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(lpe.get('loyalty_program_tier'), customer.loyalty_program_tier)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(lpe.loyalty_points, earned_points)
```

### Step 14: Assign si_redeem = create_sales_invoice_record(...)

```python
si_redeem = create_sales_invoice_record()
```

### Step 15: Assign si_redeem.redeem_loyalty_points = 1

```python
si_redeem.redeem_loyalty_points = 1
```

### Step 16: Assign si_redeem.loyalty_points = earned_points

```python
si_redeem.loyalty_points = earned_points
```

### Step 17: Call si_redeem.insert()

```python
si_redeem.insert()
```

### Step 18: Call si_redeem.submit()

```python
si_redeem.submit()
```

### Step 19: Call customer.reload()

```python
customer.reload()
```

### Step 20: Assign earned_after_redemption = get_points_earned(...)

```python
earned_after_redemption = get_points_earned(si_redeem)
```

### Step 21: Assign lpe_redeem = frappe.get_doc(...)

```python
lpe_redeem = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_redeem.name, 'redeem_against': lpe.name})
```

### Step 22: Assign lpe_earn = frappe.get_doc(...)

```python
lpe_earn = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_redeem.name, 'name': ['!=', lpe_redeem.name]})
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(lpe_earn.loyalty_points, earned_after_redemption)
```

### Step 24: Call self.assertEqual()

```python
self.assertEqual(lpe_redeem.loyalty_points, -1 * earned_points)
```

### Step 25: Call self.assertEqual()

```python
self.assertEqual(lpe_earn.loyalty_program_tier, customer.loyalty_program_tier)
```

### Step 26: Call d.cancel()

```python
d.cancel()
```


## Complete Example

```python
# Workflow
frappe.db.set_value('Customer', 'Test Loyalty Customer', 'loyalty_program', 'Test Multiple Loyalty')
customer = frappe.get_doc('Customer', {'customer_name': 'Test Loyalty Customer'})
customer.loyalty_program = frappe.get_doc('Loyalty Program', {'loyalty_program_name': 'Test Multiple Loyalty'}).name
customer.save()
si_original = create_sales_invoice_record()
si_original.insert()
si_original.submit()
customer.reload()
earned_points = get_points_earned(si_original)
lpe = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_original.name, 'customer': si_original.customer})
self.assertEqual(si_original.get('loyalty_program'), customer.loyalty_program)
self.assertEqual(lpe.get('loyalty_program_tier'), customer.loyalty_program_tier)
self.assertEqual(lpe.loyalty_points, earned_points)
si_redeem = create_sales_invoice_record()
si_redeem.redeem_loyalty_points = 1
si_redeem.loyalty_points = earned_points
si_redeem.insert()
si_redeem.submit()
customer.reload()
earned_after_redemption = get_points_earned(si_redeem)
lpe_redeem = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_redeem.name, 'redeem_against': lpe.name})
lpe_earn = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_redeem.name, 'name': ['!=', lpe_redeem.name]})
self.assertEqual(lpe_earn.loyalty_points, earned_after_redemption)
self.assertEqual(lpe_redeem.loyalty_points, -1 * earned_points)
self.assertEqual(lpe_earn.loyalty_program_tier, customer.loyalty_program_tier)
for d in [si_redeem, si_original]:
    d.cancel()
```

## Next Steps


---

*Source: test_loyalty_program.py:72 | Complexity: Advanced | Last updated: 2026-02-03*