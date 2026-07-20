# How To: Get Customer Group Details

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test get customer group details

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.party`
- `erpnext.exceptions`
- `erpnext.selling.doctype.customer.customer`
- `erpnext.tests.utils`
- `erpnext.accounts.party`
- `erpnext.accounts.party`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.controllers.accounts_controller`
- `erpnext.selling.doctype.sales_order.test_sales_order`


## Step-by-Step Guide

### Step 1: Assign doc = frappe.new_doc(...)

```python
doc = frappe.new_doc('Customer Group')
```

### Step 2: Assign doc.customer_group_name = '_Testing Customer Group'

```python
doc.customer_group_name = '_Testing Customer Group'
```

### Step 3: Assign doc.payment_terms = '_Test Payment Term Template 3'

```python
doc.payment_terms = '_Test Payment Term Template 3'
```

### Step 4: Assign doc.accounts = value

```python
doc.accounts = []
```

### Step 5: Assign doc.default_price_list = 'Standard Buying'

```python
doc.default_price_list = 'Standard Buying'
```

### Step 6: Assign doc.credit_limits = value

```python
doc.credit_limits = []
```

### Step 7: Assign test_account_details = value

```python
test_account_details = {'company': '_Test Company', 'account': 'Creditors - _TC'}
```

### Step 8: Assign test_credit_limits = value

```python
test_credit_limits = {'company': '_Test Company', 'credit_limit': 350000}
```

### Step 9: Call doc.append()

```python
doc.append('accounts', test_account_details)
```

### Step 10: Call doc.append()

```python
doc.append('credit_limits', test_credit_limits)
```

### Step 11: Call doc.insert()

```python
doc.insert()
```

### Step 12: Assign c_doc = frappe.new_doc(...)

```python
c_doc = frappe.new_doc('Customer')
```

### Step 13: Assign c_doc.customer_name = 'Testing Customer'

```python
c_doc.customer_name = 'Testing Customer'
```

### Step 14: Assign c_doc.customer_group = '_Testing Customer Group'

```python
c_doc.customer_group = '_Testing Customer Group'
```

### Step 15: Assign c_doc.payment_terms, c_doc.default_price_list = ''

```python
c_doc.payment_terms = c_doc.default_price_list = ''
```

### Step 16: Assign c_doc.accounts = value

```python
c_doc.accounts = []
```

### Step 17: Assign c_doc.credit_limits = value

```python
c_doc.credit_limits = []
```

### Step 18: Call c_doc.insert()

```python
c_doc.insert()
```

### Step 19: Call c_doc.get_customer_group_details()

```python
c_doc.get_customer_group_details()
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(c_doc.payment_terms, '_Test Payment Term Template 3')
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(c_doc.accounts[0].company, '_Test Company')
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(c_doc.accounts[0].account, 'Creditors - _TC')
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(c_doc.credit_limits[0].company, '_Test Company')
```

### Step 24: Call self.assertEqual()

```python
self.assertEqual(c_doc.credit_limits[0].credit_limit, 350000)
```

### Step 25: Call c_doc.delete()

```python
c_doc.delete()
```

### Step 26: Call doc.delete()

```python
doc.delete()
```


## Complete Example

```python
# Workflow
doc = frappe.new_doc('Customer Group')
doc.customer_group_name = '_Testing Customer Group'
doc.payment_terms = '_Test Payment Term Template 3'
doc.accounts = []
doc.default_price_list = 'Standard Buying'
doc.credit_limits = []
test_account_details = {'company': '_Test Company', 'account': 'Creditors - _TC'}
test_credit_limits = {'company': '_Test Company', 'credit_limit': 350000}
doc.append('accounts', test_account_details)
doc.append('credit_limits', test_credit_limits)
doc.insert()
c_doc = frappe.new_doc('Customer')
c_doc.customer_name = 'Testing Customer'
c_doc.customer_group = '_Testing Customer Group'
c_doc.payment_terms = c_doc.default_price_list = ''
c_doc.accounts = []
c_doc.credit_limits = []
c_doc.insert()
c_doc.get_customer_group_details()
self.assertEqual(c_doc.payment_terms, '_Test Payment Term Template 3')
self.assertEqual(c_doc.accounts[0].company, '_Test Company')
self.assertEqual(c_doc.accounts[0].account, 'Creditors - _TC')
self.assertEqual(c_doc.credit_limits[0].company, '_Test Company')
self.assertEqual(c_doc.credit_limits[0].credit_limit, 350000)
c_doc.delete()
doc.delete()
```

## Next Steps


---

*Source: test_customer.py:28 | Complexity: Advanced | Last updated: 2026-02-04*