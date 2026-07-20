# How To: Amended Naming

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test amended naming

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.core.doctype.document_naming_settings.document_naming_settings`
- `frappe.model.naming`
- `frappe.tests`
- `frappe.utils`


## Step-by-Step Guide

### Step 1: Assign self.dns.amend_naming_override = value

```python
self.dns.amend_naming_override = []
```

### Step 2: Assign self.dns.default_amend_naming = 'Amend Counter'

```python
self.dns.default_amend_naming = 'Amend Counter'
```

### Step 3: Call self.dns.update_amendment_rule()

```python
self.dns.update_amendment_rule()
```

### Step 4: Assign submittable_doc = frappe.get_doc.submit(...)

```python
submittable_doc = frappe.get_doc(doctype=self.ns_doctype, some_fieldname='test doc with submit').submit()
```

### Step 5: Call submittable_doc.cancel()

```python
submittable_doc.cancel()
```

### Step 6: Assign amended_doc = frappe.get_doc.insert(...)

```python
amended_doc = frappe.get_doc(doctype=self.ns_doctype, some_fieldname='test doc with submit', amended_from=submittable_doc.name).insert()
```

### Step 7: Call self.assertIn()

```python
self.assertIn(submittable_doc.name, amended_doc.name)
```

### Step 8: Call amended_doc.delete()

```python
amended_doc.delete()
```

### Step 9: Assign self.dns.default_amend_naming = 'Default Naming'

```python
self.dns.default_amend_naming = 'Default Naming'
```

### Step 10: Call self.dns.update_amendment_rule()

```python
self.dns.update_amendment_rule()
```

### Step 11: Assign new_amended_doc = frappe.get_doc.insert(...)

```python
new_amended_doc = frappe.get_doc(doctype=self.ns_doctype, some_fieldname='test doc with submit', amended_from=submittable_doc.name).insert()
```

### Step 12: Call self.assertNotIn()

```python
self.assertNotIn(submittable_doc.name, new_amended_doc.name)
```


## Complete Example

```python
# Workflow
self.dns.amend_naming_override = []
self.dns.default_amend_naming = 'Amend Counter'
self.dns.update_amendment_rule()
submittable_doc = frappe.get_doc(doctype=self.ns_doctype, some_fieldname='test doc with submit').submit()
submittable_doc.cancel()
amended_doc = frappe.get_doc(doctype=self.ns_doctype, some_fieldname='test doc with submit', amended_from=submittable_doc.name).insert()
self.assertIn(submittable_doc.name, amended_doc.name)
amended_doc.delete()
self.dns.default_amend_naming = 'Default Naming'
self.dns.update_amendment_rule()
new_amended_doc = frappe.get_doc(doctype=self.ns_doctype, some_fieldname='test doc with submit', amended_from=submittable_doc.name).insert()
self.assertNotIn(submittable_doc.name, new_amended_doc.name)
```

## Next Steps


---

*Source: test_document_naming_settings.py:86 | Complexity: Advanced | Last updated: 2026-02-04*