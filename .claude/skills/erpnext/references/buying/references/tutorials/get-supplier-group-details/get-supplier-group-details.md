# How To: Get Supplier Group Details

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test get supplier group details

## Prerequisites

**Required Modules:**
- `frappe`
- `erpnext.accounts.party`
- `erpnext.controllers.website_list_for_contact`
- `erpnext.exceptions`
- `frappe.tests`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.accounts.party`


## Step-by-Step Guide

### Step 1: Assign doc = frappe.new_doc(...)

```python
doc = frappe.new_doc('Supplier Group')
```

### Step 2: Assign doc.supplier_group_name = '_Testing Supplier Group'

```python
doc.supplier_group_name = '_Testing Supplier Group'
```

### Step 3: Assign doc.payment_terms = '_Test Payment Term Template 3'

```python
doc.payment_terms = '_Test Payment Term Template 3'
```

### Step 4: Assign doc.accounts = value

```python
doc.accounts = []
```

### Step 5: Assign test_account_details = value

```python
test_account_details = {'company': '_Test Company', 'account': 'Creditors - _TC'}
```

### Step 6: Call doc.append()

```python
doc.append('accounts', test_account_details)
```

### Step 7: Call doc.save()

```python
doc.save()
```

### Step 8: Assign s_doc = frappe.new_doc(...)

```python
s_doc = frappe.new_doc('Supplier')
```

### Step 9: Assign s_doc.supplier_name = 'Testing Supplier'

```python
s_doc.supplier_name = 'Testing Supplier'
```

### Step 10: Assign s_doc.supplier_group = '_Testing Supplier Group'

```python
s_doc.supplier_group = '_Testing Supplier Group'
```

### Step 11: Assign s_doc.payment_terms = ''

```python
s_doc.payment_terms = ''
```

### Step 12: Assign s_doc.accounts = value

```python
s_doc.accounts = []
```

### Step 13: Call s_doc.insert()

```python
s_doc.insert()
```

### Step 14: Call s_doc.get_supplier_group_details()

```python
s_doc.get_supplier_group_details()
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(s_doc.payment_terms, '_Test Payment Term Template 3')
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(s_doc.accounts[0].company, '_Test Company')
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(s_doc.accounts[0].account, 'Creditors - _TC')
```

### Step 18: Call s_doc.delete()

```python
s_doc.delete()
```

### Step 19: Call doc.delete()

```python
doc.delete()
```


## Complete Example

```python
# Workflow
doc = frappe.new_doc('Supplier Group')
doc.supplier_group_name = '_Testing Supplier Group'
doc.payment_terms = '_Test Payment Term Template 3'
doc.accounts = []
test_account_details = {'company': '_Test Company', 'account': 'Creditors - _TC'}
doc.append('accounts', test_account_details)
doc.save()
s_doc = frappe.new_doc('Supplier')
s_doc.supplier_name = 'Testing Supplier'
s_doc.supplier_group = '_Testing Supplier Group'
s_doc.payment_terms = ''
s_doc.accounts = []
s_doc.insert()
s_doc.get_supplier_group_details()
self.assertEqual(s_doc.payment_terms, '_Test Payment Term Template 3')
self.assertEqual(s_doc.accounts[0].company, '_Test Company')
self.assertEqual(s_doc.accounts[0].account, 'Creditors - _TC')
s_doc.delete()
doc.delete()
```

## Next Steps


---

*Source: test_supplier.py:18 | Complexity: Advanced | Last updated: 2026-02-04*