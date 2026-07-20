# How To: Save Customization Length Field Property

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test save customization length field property

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `json`
- `frappe`
- `frappe.core.doctype.doctype.doctype`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.tests`
- `frappe.tests.utils`

**Setup Required:**
```python
self.insert_custom_field()
frappe.db.delete('Property Setter', dict(doc_type='Event'))
frappe.db.commit()
frappe.clear_cache(doctype='Event')
```

## Step-by-Step Guide

### Step 1: Assign d = self.get_customize_form(...)

```python
d = self.get_customize_form('Notification Log')
```

### Step 2: Assign new_document_length = 255

```python
new_document_length = 255
```

### Step 3: Assign document_name = value

```python
document_name = d.get('fields', {'fieldname': 'document_name'})[0]
```

### Step 4: Assign document_name.length = new_document_length

```python
document_name.length = new_document_length
```

### Step 5: Call d.run_method()

```python
d.run_method('save_customization')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Property Setter', {'doc_type': 'Notification Log', 'property': 'length', 'field_name': 'document_name'}, 'value'), str(new_document_length))
```

### Step 7: Assign length = value

```python
length = frappe.db.sql("SELECT character_maximum_length\n\t\t\tFROM information_schema.columns\n\t\t\tWHERE table_name = 'tabNotification Log'\n\t\t\tAND column_name = 'document_name'")[0][0]
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(length, new_document_length)
```


## Complete Example

```python
# Setup
self.insert_custom_field()
frappe.db.delete('Property Setter', dict(doc_type='Event'))
frappe.db.commit()
frappe.clear_cache(doctype='Event')

# Workflow
d = self.get_customize_form('Notification Log')
new_document_length = 255
document_name = d.get('fields', {'fieldname': 'document_name'})[0]
document_name.length = new_document_length
d.run_method('save_customization')
self.assertEqual(frappe.db.get_value('Property Setter', {'doc_type': 'Notification Log', 'property': 'length', 'field_name': 'document_name'}, 'value'), str(new_document_length))
length = frappe.db.sql("SELECT character_maximum_length\n\t\t\tFROM information_schema.columns\n\t\t\tWHERE table_name = 'tabNotification Log'\n\t\t\tAND column_name = 'document_name'")[0][0]
self.assertEqual(length, new_document_length)
```

## Next Steps


---

*Source: test_customize_form.py:231 | Complexity: Advanced | Last updated: 2026-02-04*