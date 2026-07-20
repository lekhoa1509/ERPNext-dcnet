# How To: Change Applicable For In Promotional Scheme

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test change applicable for in promotional scheme

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `erpnext.accounts.doctype.promotional_scheme.promotional_scheme`
- `erpnext.selling.doctype.sales_order.test_sales_order`


## Step-by-Step Guide

### Step 1: Assign ps = make_promotional_scheme(...)

```python
ps = make_promotional_scheme()
```

### Step 2: Assign price_rules = frappe.get_all(...)

```python
price_rules = frappe.get_all('Pricing Rule', filters={'promotional_scheme': ps.name})
```

### Step 3: Call self.assertTrue()

```python
self.assertTrue(len(price_rules), 1)
```

### Step 4: Assign so = make_sales_order(...)

```python
so = make_sales_order(qty=5, currency='USD', do_not_save=True)
```

### Step 5: Call so.set_missing_values()

```python
so.set_missing_values()
```

### Step 6: Call so.save()

```python
so.save()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(price_rules[0].name, so.pricing_rules[0].pricing_rule)
```

### Step 8: Assign ps.applicable_for = 'Customer'

```python
ps.applicable_for = 'Customer'
```

### Step 9: Call ps.append()

```python
ps.append('customer', {'customer': '_Test Customer'})
```

### Step 10: Call self.assertRaises()

```python
self.assertRaises(TransactionExists, ps.save)
```

### Step 11: Call frappe.delete_doc()

```python
frappe.delete_doc('Sales Order', so.name)
```

### Step 12: Call frappe.delete_doc()

```python
frappe.delete_doc('Promotional Scheme', ps.name)
```

### Step 13: Assign price_rules = frappe.get_all(...)

```python
price_rules = frappe.get_all('Pricing Rule', filters={'promotional_scheme': ps.name})
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(price_rules, [])
```


## Complete Example

```python
# Workflow
ps = make_promotional_scheme()
price_rules = frappe.get_all('Pricing Rule', filters={'promotional_scheme': ps.name})
self.assertTrue(len(price_rules), 1)
so = make_sales_order(qty=5, currency='USD', do_not_save=True)
so.set_missing_values()
so.save()
self.assertEqual(price_rules[0].name, so.pricing_rules[0].pricing_rule)
ps.applicable_for = 'Customer'
ps.append('customer', {'customer': '_Test Customer'})
self.assertRaises(TransactionExists, ps.save)
frappe.delete_doc('Sales Order', so.name)
frappe.delete_doc('Promotional Scheme', ps.name)
price_rules = frappe.get_all('Pricing Rule', filters={'promotional_scheme': ps.name})
self.assertEqual(price_rules, [])
```

## Next Steps


---

*Source: test_promotional_scheme.py:72 | Complexity: Advanced | Last updated: 2026-02-03*