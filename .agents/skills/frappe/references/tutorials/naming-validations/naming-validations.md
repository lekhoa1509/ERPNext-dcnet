# How To: Naming Validations

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test naming validations

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `time`
- `uuid`
- `uuid_utils`
- `tenacity`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.model.naming`
- `frappe.query_builder.utils`
- `frappe.tests`
- `frappe.tests.test_query_builder`
- `frappe.utils`
- `datetime`
- `datetime`
- `frappe.core.doctype.doctype.test_doctype`

**Setup Required:**
```python
frappe.db.delete('Note')
```

## Step-by-Step Guide

### Step 1: Assign tag = frappe.get_doc(...)

```python
tag = frappe.get_doc({'doctype': 'Tag', '__newname': 'Tag'})
```

### Step 2: Call self.assertRaises()

```python
self.assertRaises(frappe.NameError, tag.insert)
```

### Step 3: Call self.assertRaises()

```python
self.assertRaises(frappe.NameError, make_invalid_todo)
```

### Step 4: Assign note = frappe.get_doc(...)

```python
note = frappe.get_doc({'doctype': 'Currency', 'currency_name': 'Currency'})
```

### Step 5: Call self.assertRaises()

```python
self.assertRaises(frappe.NameError, note.insert)
```

### Step 6: Assign tag = frappe.get_doc(...)

```python
tag = frappe.get_doc({'doctype': 'Tag', '__newname': 'New Tag'})
```

### Step 7: Call self.assertRaises()

```python
self.assertRaises(frappe.NameError, tag.insert)
```

### Step 8: Assign tag = frappe.get_doc(...)

```python
tag = frappe.get_doc({'doctype': 'Tag', '__newname': 'Tag<>'})
```

### Step 9: Call self.assertRaises()

```python
self.assertRaises(frappe.NameError, tag.insert)
```

### Step 10: Assign tag = frappe.get_doc(...)

```python
tag = frappe.get_doc({'doctype': 'Tag', '__newname': ''})
```

### Step 11: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, tag.insert)
```


## Complete Example

```python
# Setup
frappe.db.delete('Note')

# Workflow
tag = frappe.get_doc({'doctype': 'Tag', '__newname': 'Tag'})
self.assertRaises(frappe.NameError, tag.insert)
self.assertRaises(frappe.NameError, make_invalid_todo)
note = frappe.get_doc({'doctype': 'Currency', 'currency_name': 'Currency'})
self.assertRaises(frappe.NameError, note.insert)
tag = frappe.get_doc({'doctype': 'Tag', '__newname': 'New Tag'})
self.assertRaises(frappe.NameError, tag.insert)
tag = frappe.get_doc({'doctype': 'Tag', '__newname': 'Tag<>'})
self.assertRaises(frappe.NameError, tag.insert)
tag = frappe.get_doc({'doctype': 'Tag', '__newname': ''})
self.assertRaises(frappe.ValidationError, tag.insert)
```

## Next Steps


---

*Source: test_naming.py:276 | Complexity: Advanced | Last updated: 2026-02-04*