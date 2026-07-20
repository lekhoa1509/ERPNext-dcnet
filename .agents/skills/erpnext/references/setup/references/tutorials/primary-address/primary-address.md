# How To: Primary Address

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test primary address

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts`
- `erpnext.setup.doctype.company.company`
- `erpnext.setup.demo`


## Step-by-Step Guide

### Step 1: Assign company = '_Test Company'

```python
company = '_Test Company'
```

### Step 2: Assign secondary = frappe.get_doc(...)

```python
secondary = frappe.get_doc({'address_title': 'Non Primary', 'doctype': 'Address', 'address_type': 'Billing', 'address_line1': 'Something', 'city': 'Mumbai', 'state': 'Maharashtra', 'country': 'India', 'is_primary_address': 1, 'pincode': '400098', 'links': [{'link_doctype': 'Company', 'link_name': company}]})
```

### Step 3: Call secondary.insert()

```python
secondary.insert()
```

### Step 4: Call self.addCleanup()

```python
self.addCleanup(secondary.delete)
```

### Step 5: Assign primary = frappe.copy_doc(...)

```python
primary = frappe.copy_doc(secondary)
```

### Step 6: Assign primary.is_primary_address = 1

```python
primary.is_primary_address = 1
```

### Step 7: Call primary.insert()

```python
primary.insert()
```

### Step 8: Call self.addCleanup()

```python
self.addCleanup(primary.delete)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(get_default_company_address(company), primary.name)
```


## Complete Example

```python
# Workflow
company = '_Test Company'
secondary = frappe.get_doc({'address_title': 'Non Primary', 'doctype': 'Address', 'address_type': 'Billing', 'address_line1': 'Something', 'city': 'Mumbai', 'state': 'Maharashtra', 'country': 'India', 'is_primary_address': 1, 'pincode': '400098', 'links': [{'link_doctype': 'Company', 'link_name': company}]})
secondary.insert()
self.addCleanup(secondary.delete)
primary = frappe.copy_doc(secondary)
primary.is_primary_address = 1
primary.insert()
self.addCleanup(primary.delete)
self.assertEqual(get_default_company_address(company), primary.name)
```

## Next Steps


---

*Source: test_company.py:140 | Complexity: Advanced | Last updated: 2026-02-04*