# How To: Promotional Scheme

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test promotional scheme

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `erpnext.accounts.doctype.promotional_scheme.promotional_scheme`
- `erpnext.selling.doctype.sales_order.test_sales_order`


## Step-by-Step Guide

### Step 1: Assign ps = make_promotional_scheme(...)

```python
ps = make_promotional_scheme(applicable_for='Customer', customer='_Test Customer')
```

### Step 2: Assign price_rules = frappe.get_all(...)

```python
price_rules = frappe.get_all('Pricing Rule', fields=['promotional_scheme_id', 'name', 'creation'], filters={'promotional_scheme': ps.name})
```

### Step 3: Call self.assertTrue()

```python
self.assertTrue(len(price_rules), 1)
```

### Step 4: Assign price_doc_details = frappe.db.get_value(...)

```python
price_doc_details = frappe.db.get_value('Pricing Rule', price_rules[0].name, ['customer', 'min_qty', 'discount_percentage'], as_dict=1)
```

### Step 5: Call self.assertTrue()

```python
self.assertTrue(price_doc_details.customer, '_Test Customer')
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue(price_doc_details.min_qty, 4)
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue(price_doc_details.discount_percentage, 20)
```

### Step 8: Assign unknown.min_qty = 6

```python
ps.price_discount_slabs[0].min_qty = 6
```

### Step 9: Call ps.append()

```python
ps.append('customer', {'customer': '_Test Customer 2'})
```

### Step 10: Call ps.save()

```python
ps.save()
```

### Step 11: Assign price_rules = frappe.get_all(...)

```python
price_rules = frappe.get_all('Pricing Rule', fields=['promotional_scheme_id', 'name'], filters={'promotional_scheme': ps.name})
```

### Step 12: Call self.assertTrue()

```python
self.assertTrue(len(price_rules), 2)
```

### Step 13: Assign price_doc_details = frappe.db.get_value(...)

```python
price_doc_details = frappe.db.get_value('Pricing Rule', price_rules[1].name, ['customer', 'min_qty', 'discount_percentage'], as_dict=1)
```

### Step 14: Call self.assertTrue()

```python
self.assertTrue(price_doc_details.customer, '_Test Customer 2')
```

### Step 15: Call self.assertTrue()

```python
self.assertTrue(price_doc_details.min_qty, 6)
```

### Step 16: Call self.assertTrue()

```python
self.assertTrue(price_doc_details.discount_percentage, 20)
```

### Step 17: Assign price_doc_details = frappe.db.get_value(...)

```python
price_doc_details = frappe.db.get_value('Pricing Rule', price_rules[0].name, ['customer', 'min_qty', 'discount_percentage'], as_dict=1)
```

### Step 18: Call self.assertTrue()

```python
self.assertTrue(price_doc_details.customer, '_Test Customer')
```

### Step 19: Call self.assertTrue()

```python
self.assertTrue(price_doc_details.min_qty, 6)
```

### Step 20: Call frappe.delete_doc()

```python
frappe.delete_doc('Promotional Scheme', ps.name)
```

### Step 21: Assign price_rules = frappe.get_all(...)

```python
price_rules = frappe.get_all('Pricing Rule', fields=['promotional_scheme_id', 'name'], filters={'promotional_scheme': ps.name})
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(price_rules, [])
```


## Complete Example

```python
# Workflow
ps = make_promotional_scheme(applicable_for='Customer', customer='_Test Customer')
price_rules = frappe.get_all('Pricing Rule', fields=['promotional_scheme_id', 'name', 'creation'], filters={'promotional_scheme': ps.name})
self.assertTrue(len(price_rules), 1)
price_doc_details = frappe.db.get_value('Pricing Rule', price_rules[0].name, ['customer', 'min_qty', 'discount_percentage'], as_dict=1)
self.assertTrue(price_doc_details.customer, '_Test Customer')
self.assertTrue(price_doc_details.min_qty, 4)
self.assertTrue(price_doc_details.discount_percentage, 20)
ps.price_discount_slabs[0].min_qty = 6
ps.append('customer', {'customer': '_Test Customer 2'})
ps.save()
price_rules = frappe.get_all('Pricing Rule', fields=['promotional_scheme_id', 'name'], filters={'promotional_scheme': ps.name})
self.assertTrue(len(price_rules), 2)
price_doc_details = frappe.db.get_value('Pricing Rule', price_rules[1].name, ['customer', 'min_qty', 'discount_percentage'], as_dict=1)
self.assertTrue(price_doc_details.customer, '_Test Customer 2')
self.assertTrue(price_doc_details.min_qty, 6)
self.assertTrue(price_doc_details.discount_percentage, 20)
price_doc_details = frappe.db.get_value('Pricing Rule', price_rules[0].name, ['customer', 'min_qty', 'discount_percentage'], as_dict=1)
self.assertTrue(price_doc_details.customer, '_Test Customer')
self.assertTrue(price_doc_details.min_qty, 6)
frappe.delete_doc('Promotional Scheme', ps.name)
price_rules = frappe.get_all('Pricing Rule', fields=['promotional_scheme_id', 'name'], filters={'promotional_scheme': ps.name})
self.assertEqual(price_rules, [])
```

## Next Steps


---

*Source: test_promotional_scheme.py:16 | Complexity: Advanced | Last updated: 2026-02-03*