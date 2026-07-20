# How To: Make Customer

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test make customer

## Prerequisites

**Required Modules:**
- `unittest`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.crm.doctype.lead.lead`
- `erpnext.crm.utils`
- `erpnext.tests.utils`
- `erpnext.crm.doctype.lead.lead`
- `erpnext.crm.doctype.lead.lead`


## Step-by-Step Guide

### Step 1: Call frappe.delete_doc_if_exists()

```python
frappe.delete_doc_if_exists('Customer', '_Test Lead')
```

### Step 2: Assign customer = make_customer(...)

```python
customer = make_customer(self.leads[0].name)
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(customer.doctype, 'Customer')
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(customer.lead_name, self.leads[0].name)
```

### Step 5: Assign customer.company = '_Test Company'

```python
customer.company = '_Test Company'
```

### Step 6: Assign customer.customer_group = '_Test Customer Group'

```python
customer.customer_group = '_Test Customer Group'
```

### Step 7: Call customer.insert()

```python
customer.insert()
```

### Step 8: Assign contact = frappe.db.get_value(...)

```python
contact = frappe.db.get_value('Dynamic Link', {'parenttype': 'Contact', 'link_doctype': 'Lead', 'link_name': customer.lead_name}, 'parent')
```

### Step 9: Assign contact_doc = frappe.get_doc(...)

```python
contact_doc = frappe.get_doc('Contact', contact)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(contact_doc.has_link(customer.doctype, customer.name), True)
```


## Complete Example

```python
# Workflow
from erpnext.crm.doctype.lead.lead import make_customer
frappe.delete_doc_if_exists('Customer', '_Test Lead')
customer = make_customer(self.leads[0].name)
self.assertEqual(customer.doctype, 'Customer')
self.assertEqual(customer.lead_name, self.leads[0].name)
customer.company = '_Test Company'
customer.customer_group = '_Test Customer Group'
customer.insert()
contact = frappe.db.get_value('Dynamic Link', {'parenttype': 'Contact', 'link_doctype': 'Lead', 'link_name': customer.lead_name}, 'parent')
if contact:
    contact_doc = frappe.get_doc('Contact', contact)
    self.assertEqual(contact_doc.has_link(customer.doctype, customer.name), True)
```

## Next Steps


---

*Source: test_lead.py:20 | Complexity: Advanced | Last updated: 2026-02-04*