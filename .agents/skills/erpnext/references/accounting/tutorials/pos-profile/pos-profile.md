# How To: Pos Profile

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test pos profile

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.pos_profile.pos_profile`
- `erpnext.stock.get_item_details`
- `erpnext.accounts.doctype.pos_closing_entry.test_pos_closing_entry`
- `erpnext.accounts.doctype.pos_opening_entry.test_pos_opening_entry`
- `erpnext.accounts.doctype.pos_closing_entry.pos_closing_entry`
- `erpnext.accounts.doctype.pos_closing_entry.test_pos_closing_entry`
- `erpnext.accounts.doctype.pos_opening_entry.test_pos_opening_entry`


## Step-by-Step Guide

### Step 1: Call make_pos_profile()

```python
make_pos_profile()
```

### Step 2: Assign pos_profile = value

```python
pos_profile = get_pos_profile('_Test Company') or {}
```

### Step 3: Call frappe.db.sql()

```python
frappe.db.sql('delete from `tabPOS Profile`')
```

### Step 4: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc('POS Profile', pos_profile.get('name'))
```

### Step 5: Call doc.append()

```python
doc.append('item_groups', {'item_group': '_Test Item Group'})
```

### Step 6: Call doc.append()

```python
doc.append('customer_groups', {'customer_group': '_Test Customer Group'})
```

### Step 7: Call doc.save()

```python
doc.save()
```

### Step 8: Assign items = get_items_list(...)

```python
items = get_items_list(doc, doc.company)
```

### Step 9: Assign customers = get_customers_list(...)

```python
customers = get_customers_list(doc)
```

### Step 10: Assign products_count = frappe.db.sql(...)

```python
products_count = frappe.db.sql(" select count(name) from tabItem where item_group = '_Test Item Group'", as_list=1)
```

### Step 11: Assign customers_count = frappe.db.sql(...)

```python
customers_count = frappe.db.sql(" select count(name) from tabCustomer where customer_group = '_Test Customer Group'")
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(len(items), products_count[0][0])
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(len(customers), customers_count[0][0])
```


## Complete Example

```python
# Workflow
make_pos_profile()
pos_profile = get_pos_profile('_Test Company') or {}
if pos_profile:
    doc = frappe.get_doc('POS Profile', pos_profile.get('name'))
    doc.append('item_groups', {'item_group': '_Test Item Group'})
    doc.append('customer_groups', {'customer_group': '_Test Customer Group'})
    doc.save()
    items = get_items_list(doc, doc.company)
    customers = get_customers_list(doc)
    products_count = frappe.db.sql(" select count(name) from tabItem where item_group = '_Test Item Group'", as_list=1)
    customers_count = frappe.db.sql(" select count(name) from tabCustomer where customer_group = '_Test Customer Group'")
    self.assertEqual(len(items), products_count[0][0])
    self.assertEqual(len(customers), customers_count[0][0])
frappe.db.sql('delete from `tabPOS Profile`')
```

## Next Steps


---

*Source: test_pos_profile.py:17 | Complexity: Advanced | Last updated: 2026-02-03*