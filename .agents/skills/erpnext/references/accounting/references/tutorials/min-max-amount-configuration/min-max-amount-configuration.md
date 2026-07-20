# How To: Min Max Amount Configuration

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test min max amount configuration

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

### Step 2: Assign unknown.min_amount = 10

```python
ps.price_discount_slabs[0].min_amount = 10
```

### Step 3: Assign unknown.max_amount = 1000

```python
ps.price_discount_slabs[0].max_amount = 1000
```

### Step 4: Call ps.save()

```python
ps.save()
```

### Step 5: Assign price_rules_data = frappe.db.get_value(...)

```python
price_rules_data = frappe.db.get_value('Pricing Rule', {'promotional_scheme': ps.name}, ['min_amt', 'max_amt'], as_dict=1)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(price_rules_data.min_amt, 10)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(price_rules_data.max_amt, 1000)
```

### Step 8: Call frappe.delete_doc()

```python
frappe.delete_doc('Promotional Scheme', ps.name)
```

### Step 9: Assign price_rules = frappe.get_all(...)

```python
price_rules = frappe.get_all('Pricing Rule', filters={'promotional_scheme': ps.name})
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(price_rules, [])
```


## Complete Example

```python
# Workflow
ps = make_promotional_scheme()
ps.price_discount_slabs[0].min_amount = 10
ps.price_discount_slabs[0].max_amount = 1000
ps.save()
price_rules_data = frappe.db.get_value('Pricing Rule', {'promotional_scheme': ps.name}, ['min_amt', 'max_amt'], as_dict=1)
self.assertEqual(price_rules_data.min_amt, 10)
self.assertEqual(price_rules_data.max_amt, 1000)
frappe.delete_doc('Promotional Scheme', ps.name)
price_rules = frappe.get_all('Pricing Rule', filters={'promotional_scheme': ps.name})
self.assertEqual(price_rules, [])
```

## Next Steps


---

*Source: test_promotional_scheme.py:117 | Complexity: Advanced | Last updated: 2026-02-03*