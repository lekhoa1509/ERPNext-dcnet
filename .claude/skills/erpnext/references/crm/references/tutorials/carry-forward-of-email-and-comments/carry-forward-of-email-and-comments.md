# How To: Carry Forward Of Email And Comments

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test carry forward of email and comments

## Prerequisites

**Required Modules:**
- `unittest`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.crm.doctype.lead.lead`
- `erpnext.crm.doctype.lead.test_lead`
- `erpnext.crm.doctype.opportunity.opportunity`
- `erpnext.crm.utils`
- `erpnext.tests.utils`


## Step-by-Step Guide

### Step 1: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('CRM Settings', 'carry_forward_communication_and_comments', 1)
```

### Step 2: Assign lead_doc = make_lead(...)

```python
lead_doc = make_lead()
```

### Step 3: Call lead_doc.add_comment()

```python
lead_doc.add_comment('Comment', text='Test Comment 1')
```

### Step 4: Call lead_doc.add_comment()

```python
lead_doc.add_comment('Comment', text='Test Comment 2')
```

### Step 5: Call create_communication()

```python
create_communication(lead_doc.doctype, lead_doc.name, lead_doc.email_id)
```

### Step 6: Call create_communication()

```python
create_communication(lead_doc.doctype, lead_doc.name, lead_doc.email_id)
```

### Step 7: Assign opp_doc = make_opportunity(...)

```python
opp_doc = make_opportunity(opportunity_from='Lead', lead=lead_doc.name)
```

### Step 8: Assign opportunity_comment_count = frappe.db.count(...)

```python
opportunity_comment_count = frappe.db.count('Comment', {'reference_doctype': opp_doc.doctype, 'reference_name': opp_doc.name})
```

### Step 9: Assign opportunity_communication_count = len(...)

```python
opportunity_communication_count = len(get_linked_communication_list(opp_doc.doctype, opp_doc.name))
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(opportunity_comment_count, 2)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(opportunity_communication_count, 2)
```

### Step 12: Call opp_doc.add_comment()

```python
opp_doc.add_comment('Comment', text='Test Comment 3')
```

### Step 13: Call opp_doc.add_comment()

```python
opp_doc.add_comment('Comment', text='Test Comment 4')
```

### Step 14: Call create_communication()

```python
create_communication(opp_doc.doctype, opp_doc.name, opp_doc.contact_email)
```

### Step 15: Call create_communication()

```python
create_communication(opp_doc.doctype, opp_doc.name, opp_doc.contact_email)
```


## Complete Example

```python
# Workflow
frappe.db.set_single_value('CRM Settings', 'carry_forward_communication_and_comments', 1)
lead_doc = make_lead()
lead_doc.add_comment('Comment', text='Test Comment 1')
lead_doc.add_comment('Comment', text='Test Comment 2')
create_communication(lead_doc.doctype, lead_doc.name, lead_doc.email_id)
create_communication(lead_doc.doctype, lead_doc.name, lead_doc.email_id)
opp_doc = make_opportunity(opportunity_from='Lead', lead=lead_doc.name)
opportunity_comment_count = frappe.db.count('Comment', {'reference_doctype': opp_doc.doctype, 'reference_name': opp_doc.name})
opportunity_communication_count = len(get_linked_communication_list(opp_doc.doctype, opp_doc.name))
self.assertEqual(opportunity_comment_count, 2)
self.assertEqual(opportunity_communication_count, 2)
opp_doc.add_comment('Comment', text='Test Comment 3')
opp_doc.add_comment('Comment', text='Test Comment 4')
create_communication(opp_doc.doctype, opp_doc.name, opp_doc.contact_email)
create_communication(opp_doc.doctype, opp_doc.name, opp_doc.contact_email)
```

## Next Steps


---

*Source: test_opportunity.py:82 | Complexity: Advanced | Last updated: 2026-02-04*