# How To: Get Doctype References By Dlink Field

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test get doctype references by dlink field

## Prerequisites

**Required Modules:**
- `random`
- `string`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.database`
- `frappe.desk.form`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Assign references = linked_with.get_references_across_doctypes_by_dynamic_link_field(...)

```python
references = linked_with.get_references_across_doctypes_by_dynamic_link_field(to_doctypes=['Parent DocType'], limit_link_doctypes=['Parent DocType', 'Child DocType1', 'Child DocType2'])
```

### Step 2: Call self.assertFalse()

```python
self.assertFalse(references)
```

### Step 3: Assign parent_record = frappe.get_doc.insert(...)

```python
parent_record = frappe.get_doc({'doctype': 'Parent DocType'}).insert()
```

### Step 4: Assign child_record = frappe.get_doc.insert(...)

```python
child_record = frappe.get_doc({'doctype': 'Child DocType1', 'reference_doctype': 'Parent DocType', 'reference_name': parent_record.name}).insert()
```

### Step 5: Assign references = linked_with.get_references_across_doctypes_by_dynamic_link_field(...)

```python
references = linked_with.get_references_across_doctypes_by_dynamic_link_field(to_doctypes=['Parent DocType'], limit_link_doctypes=['Parent DocType', 'Child DocType1', 'Child DocType2'])
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(len(references['Parent DocType']), 1)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(references['Parent DocType'][0]['doctype'], 'Child DocType1')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(references['Parent DocType'][0]['doctype_fieldname'], 'reference_doctype')
```

### Step 9: Call child_record.delete()

```python
child_record.delete()
```

### Step 10: Call parent_record.delete()

```python
parent_record.delete()
```


## Complete Example

```python
# Workflow
references = linked_with.get_references_across_doctypes_by_dynamic_link_field(to_doctypes=['Parent DocType'], limit_link_doctypes=['Parent DocType', 'Child DocType1', 'Child DocType2'])
self.assertFalse(references)
parent_record = frappe.get_doc({'doctype': 'Parent DocType'}).insert()
child_record = frappe.get_doc({'doctype': 'Child DocType1', 'reference_doctype': 'Parent DocType', 'reference_name': parent_record.name}).insert()
references = linked_with.get_references_across_doctypes_by_dynamic_link_field(to_doctypes=['Parent DocType'], limit_link_doctypes=['Parent DocType', 'Child DocType1', 'Child DocType2'])
self.assertEqual(len(references['Parent DocType']), 1)
self.assertEqual(references['Parent DocType'][0]['doctype'], 'Child DocType1')
self.assertEqual(references['Parent DocType'][0]['doctype_fieldname'], 'reference_doctype')
child_record.delete()
parent_record.delete()
```

## Next Steps


---

*Source: test_linked_with.py:95 | Complexity: Advanced | Last updated: 2026-02-04*