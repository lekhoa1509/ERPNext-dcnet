# How To: Add Lead To Prospect And Address Linking

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test add lead to prospect and address linking

## Prerequisites

**Required Modules:**
- `unittest`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.crm.doctype.lead.lead`
- `erpnext.crm.doctype.lead.test_lead`
- `erpnext.crm.doctype.prospect.prospect`


## Step-by-Step Guide

### Step 1: Assign lead_doc = make_lead(...)

```python
lead_doc = make_lead()
```

### Step 2: Assign address_doc = make_address(...)

```python
address_doc = make_address(address_title=lead_doc.name)
```

### Step 3: Call address_doc.append()

```python
address_doc.append('links', {'link_doctype': lead_doc.doctype, 'link_name': lead_doc.name})
```

### Step 4: Call address_doc.save()

```python
address_doc.save()
```

### Step 5: Assign prospect_doc = make_prospect(...)

```python
prospect_doc = make_prospect()
```

### Step 6: Call add_lead_to_prospect()

```python
add_lead_to_prospect(lead_doc.name, prospect_doc.name)
```

### Step 7: Call prospect_doc.reload()

```python
prospect_doc.reload()
```

### Step 8: Assign lead_exists_in_prosoect = False

```python
lead_exists_in_prosoect = False
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(lead_exists_in_prosoect, True)
```

### Step 10: Call address_doc.reload()

```python
address_doc.reload()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(address_doc.has_link('Prospect', prospect_doc.name), True)
```

### Step 12: Assign lead_exists_in_prosoect = True

```python
lead_exists_in_prosoect = True
```


## Complete Example

```python
# Workflow
lead_doc = make_lead()
address_doc = make_address(address_title=lead_doc.name)
address_doc.append('links', {'link_doctype': lead_doc.doctype, 'link_name': lead_doc.name})
address_doc.save()
prospect_doc = make_prospect()
add_lead_to_prospect(lead_doc.name, prospect_doc.name)
prospect_doc.reload()
lead_exists_in_prosoect = False
for rec in prospect_doc.get('leads'):
    if rec.lead == lead_doc.name:
        lead_exists_in_prosoect = True
self.assertEqual(lead_exists_in_prosoect, True)
address_doc.reload()
self.assertEqual(address_doc.has_link('Prospect', prospect_doc.name), True)
```

## Next Steps


---

*Source: test_prospect.py:14 | Complexity: Advanced | Last updated: 2026-02-04*