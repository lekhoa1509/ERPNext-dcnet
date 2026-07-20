# How To: Party Details Tax Category

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test party details tax category

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

### Step 1: Call frappe.delete_doc_if_exists()

```python
frappe.delete_doc_if_exists('Address', '_Test Address With Tax Category-Billing')
```

### Step 2: Call frappe.delete_doc_if_exists()

```python
frappe.delete_doc_if_exists('Address', '_Test Address With Tax Category-Shipping')
```

### Step 3: Assign details = get_party_details(...)

```python
details = get_party_details('_Test Customer With Tax Category')
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(details.tax_category, '_Test Tax Category 1')
```

### Step 5: Assign billing_address = frappe.get_doc.insert(...)

```python
billing_address = frappe.get_doc(doctype='Address', address_title='_Test Address With Tax Category', tax_category='_Test Tax Category 2', address_type='Billing', address_line1='Station Road', city='_Test City', country='India', links=[dict(link_doctype='Customer', link_name='_Test Customer With Tax Category')]).insert()
```

### Step 6: Assign shipping_address = frappe.get_doc.insert(...)

```python
shipping_address = frappe.get_doc(doctype='Address', address_title='_Test Address With Tax Category', tax_category='_Test Tax Category 3', address_type='Shipping', address_line1='Station Road', city='_Test City', country='India', links=[dict(link_doctype='Customer', link_name='_Test Customer With Tax Category')]).insert()
```

### Step 7: Assign settings = frappe.get_single(...)

```python
settings = frappe.get_single('Accounts Settings')
```

### Step 8: Assign rollback_setting = value

```python
rollback_setting = settings.determine_address_tax_category_from
```

### Step 9: Assign settings.determine_address_tax_category_from = 'Billing Address'

```python
settings.determine_address_tax_category_from = 'Billing Address'
```

### Step 10: Call settings.save()

```python
settings.save()
```

### Step 11: Assign details = get_party_details(...)

```python
details = get_party_details('_Test Customer With Tax Category')
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(details.tax_category, '_Test Tax Category 2')
```

### Step 13: Assign settings.determine_address_tax_category_from = 'Shipping Address'

```python
settings.determine_address_tax_category_from = 'Shipping Address'
```

### Step 14: Call settings.save()

```python
settings.save()
```

### Step 15: Assign details = get_party_details(...)

```python
details = get_party_details('_Test Customer With Tax Category')
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(details.tax_category, '_Test Tax Category 3')
```

### Step 17: Assign settings.determine_address_tax_category_from = rollback_setting

```python
settings.determine_address_tax_category_from = rollback_setting
```

### Step 18: Call settings.save()

```python
settings.save()
```

### Step 19: Call billing_address.delete()

```python
billing_address.delete()
```

### Step 20: Call shipping_address.delete()

```python
shipping_address.delete()
```


## Complete Example

```python
# Workflow
from erpnext.accounts.party import get_party_details
frappe.delete_doc_if_exists('Address', '_Test Address With Tax Category-Billing')
frappe.delete_doc_if_exists('Address', '_Test Address With Tax Category-Shipping')
details = get_party_details('_Test Customer With Tax Category')
self.assertEqual(details.tax_category, '_Test Tax Category 1')
billing_address = frappe.get_doc(doctype='Address', address_title='_Test Address With Tax Category', tax_category='_Test Tax Category 2', address_type='Billing', address_line1='Station Road', city='_Test City', country='India', links=[dict(link_doctype='Customer', link_name='_Test Customer With Tax Category')]).insert()
shipping_address = frappe.get_doc(doctype='Address', address_title='_Test Address With Tax Category', tax_category='_Test Tax Category 3', address_type='Shipping', address_line1='Station Road', city='_Test City', country='India', links=[dict(link_doctype='Customer', link_name='_Test Customer With Tax Category')]).insert()
settings = frappe.get_single('Accounts Settings')
rollback_setting = settings.determine_address_tax_category_from
settings.determine_address_tax_category_from = 'Billing Address'
settings.save()
details = get_party_details('_Test Customer With Tax Category')
self.assertEqual(details.tax_category, '_Test Tax Category 2')
settings.determine_address_tax_category_from = 'Shipping Address'
settings.save()
details = get_party_details('_Test Customer With Tax Category')
self.assertEqual(details.tax_category, '_Test Tax Category 3')
settings.determine_address_tax_category_from = rollback_setting
settings.save()
billing_address.delete()
shipping_address.delete()
```

## Next Steps


---

*Source: test_customer.py:96 | Complexity: Advanced | Last updated: 2026-02-04*