# How To: Renaming Of Invoice Using Invoice Number Field

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test renaming of invoice using invoice number field

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `erpnext.accounts.doctype.accounting_dimension.test_accounting_dimension`
- `erpnext.accounts.doctype.opening_invoice_creation_tool.opening_invoice_creation_tool`


## Step-by-Step Guide

### Step 1: Assign company = '_Test Opening Invoice Company'

```python
company = '_Test Opening Invoice Company'
```

### Step 2: Assign unknown = value

```python
party_1, party_2 = (make_customer('Customer A'), make_customer('Customer B'))
```

### Step 3: Call self.make_invoices()

```python
self.make_invoices(company=company, party_1=party_1, party_2=party_2, invoice_number='TEST-NEW-INV-11')
```

### Step 4: Assign sales_inv1 = unknown.get(...)

```python
sales_inv1 = frappe.get_all('Sales Invoice', filters={'customer': 'Customer A'})[0].get('name')
```

### Step 5: Assign sales_inv2 = unknown.get(...)

```python
sales_inv2 = frappe.get_all('Sales Invoice', filters={'customer': 'Customer B'})[0].get('name')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(sales_inv1, 'TEST-NEW-INV-11')
```

### Step 7: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc('Sales Invoice', inv)
```

### Step 8: Call doc.cancel()

```python
doc.cancel()
```


## Complete Example

```python
# Workflow
company = '_Test Opening Invoice Company'
party_1, party_2 = (make_customer('Customer A'), make_customer('Customer B'))
self.make_invoices(company=company, party_1=party_1, party_2=party_2, invoice_number='TEST-NEW-INV-11')
sales_inv1 = frappe.get_all('Sales Invoice', filters={'customer': 'Customer A'})[0].get('name')
sales_inv2 = frappe.get_all('Sales Invoice', filters={'customer': 'Customer B'})[0].get('name')
self.assertEqual(sales_inv1, 'TEST-NEW-INV-11')
for inv in [sales_inv1, sales_inv2]:
    doc = frappe.get_doc('Sales Invoice', inv)
    doc.cancel()
```

## Next Steps


---

*Source: test_opening_invoice_creation_tool.py:124 | Complexity: Advanced | Last updated: 2026-02-03*