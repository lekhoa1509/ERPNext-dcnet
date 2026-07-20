# How To: Circular Linking

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test circular linking

## Prerequisites

**Required Modules:**
- `typing`
- `frappe`
- `frappe.core.doctype.communication.communication`
- `frappe.core.doctype.communication.email`
- `frappe.email.doctype.email_queue.email_queue`
- `frappe.tests`
- `frappe.contacts.doctype.contact.contact`
- `frappe.email.doctype.email_account.email_account`
- `frappe.desk.form.load`


## Step-by-Step Guide

### Step 1: Assign a = frappe.get_doc.insert(...)

```python
a = frappe.get_doc({'doctype': 'Communication', 'communication_type': 'Communication', 'content': 'This was created to test circular linking: Communication A'}).insert(ignore_permissions=True)
```

### Step 2: Assign b = frappe.get_doc.insert(...)

```python
b = frappe.get_doc({'doctype': 'Communication', 'communication_type': 'Communication', 'content': 'This was created to test circular linking: Communication B', 'reference_doctype': 'Communication', 'reference_name': a.name}).insert(ignore_permissions=True)
```

### Step 3: Assign c = frappe.get_doc.insert(...)

```python
c = frappe.get_doc({'doctype': 'Communication', 'communication_type': 'Communication', 'content': 'This was created to test circular linking: Communication C', 'reference_doctype': 'Communication', 'reference_name': b.name}).insert(ignore_permissions=True)
```

### Step 4: Assign a = frappe.get_doc(...)

```python
a = frappe.get_doc('Communication', a.name)
```

### Step 5: Assign a.reference_doctype = 'Communication'

```python
a.reference_doctype = 'Communication'
```

### Step 6: Assign a.reference_name = value

```python
a.reference_name = c.name
```

### Step 7: Call self.assertRaises()

```python
self.assertRaises(frappe.CircularLinkingError, a.save)
```


## Complete Example

```python
# Workflow
a = frappe.get_doc({'doctype': 'Communication', 'communication_type': 'Communication', 'content': 'This was created to test circular linking: Communication A'}).insert(ignore_permissions=True)
b = frappe.get_doc({'doctype': 'Communication', 'communication_type': 'Communication', 'content': 'This was created to test circular linking: Communication B', 'reference_doctype': 'Communication', 'reference_name': a.name}).insert(ignore_permissions=True)
c = frappe.get_doc({'doctype': 'Communication', 'communication_type': 'Communication', 'content': 'This was created to test circular linking: Communication C', 'reference_doctype': 'Communication', 'reference_name': b.name}).insert(ignore_permissions=True)
a = frappe.get_doc('Communication', a.name)
a.reference_doctype = 'Communication'
a.reference_name = c.name
self.assertRaises(frappe.CircularLinkingError, a.save)
```

## Next Steps


---

*Source: test_communication.py:73 | Complexity: Intermediate | Last updated: 2026-02-04*