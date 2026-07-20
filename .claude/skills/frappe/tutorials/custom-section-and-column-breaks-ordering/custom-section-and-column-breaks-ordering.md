# How To: Custom Section And Column Breaks Ordering

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test custom section and column breaks ordering

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.custom.doctype.custom_field.custom_field`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc({'doctype': 'DocType', 'name': 'Test Custom Breaks Ordering', 'custom': 1, 'module': 'Core', 'fields': [{'fieldname': 'section1', 'fieldtype': 'Section Break', 'label': 'Section 1'}, {'fieldname': 'field1', 'fieldtype': 'Data', 'label': 'Field 1'}, {'fieldname': 'field2', 'fieldtype': 'Data', 'label': 'Field 2'}, {'fieldname': 'section2', 'fieldtype': 'Section Break', 'label': 'Section 2'}, {'fieldname': 'column21', 'fieldtype': 'Column Break', 'label': 'Column 2.1'}, {'fieldname': 'field3', 'fieldtype': 'Data', 'label': 'Field 3'}, {'fieldname': 'column22', 'fieldtype': 'Column Break', 'label': 'Column 2.2'}, {'fieldname': 'field4', 'fieldtype': 'Data', 'label': 'Field 4'}]})
```

### Step 2: Call doc.insert()

```python
doc.insert()
```

### Step 3: Assign custom_section = frappe.get_doc(...)

```python
custom_section = frappe.get_doc({'doctype': 'Custom Field', 'dt': 'Test Custom Breaks Ordering', 'fieldname': 'custom_section', 'fieldtype': 'Section Break', 'insert_after': 'section1', 'label': 'Custom Section'})
```

### Step 4: Call custom_section.insert()

```python
custom_section.insert()
```

### Step 5: Assign custom_column = frappe.get_doc(...)

```python
custom_column = frappe.get_doc({'doctype': 'Custom Field', 'dt': 'Test Custom Breaks Ordering', 'fieldname': 'custom_column_insert', 'fieldtype': 'Column Break', 'insert_after': 'column21', 'label': 'Custom Column Insert'})
```

### Step 6: Call custom_column.insert()

```python
custom_column.insert()
```

### Step 7: Assign custom_column = frappe.get_doc(...)

```python
custom_column = frappe.get_doc({'doctype': 'Custom Field', 'dt': 'Test Custom Breaks Ordering', 'fieldname': 'custom_column_end', 'fieldtype': 'Column Break', 'insert_after': 'section2', 'label': 'Custom Column End'})
```

### Step 8: Call custom_column.insert()

```python
custom_column.insert()
```

### Step 9: Assign updated_meta = frappe.get_meta(...)

```python
updated_meta = frappe.get_meta('Test Custom Breaks Ordering', cached=False)
```

### Step 10: Assign field_names = value

```python
field_names = [field.fieldname for field in updated_meta.fields]
```

### Step 11: Assign expected_order = value

```python
expected_order = ['section1', 'field1', 'field2', 'custom_section', 'section2', 'column21', 'field3', 'custom_column_insert', 'column22', 'field4', 'custom_column_end']
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(field_names, expected_order)
```


## Complete Example

```python
# Workflow
doc = frappe.get_doc({'doctype': 'DocType', 'name': 'Test Custom Breaks Ordering', 'custom': 1, 'module': 'Core', 'fields': [{'fieldname': 'section1', 'fieldtype': 'Section Break', 'label': 'Section 1'}, {'fieldname': 'field1', 'fieldtype': 'Data', 'label': 'Field 1'}, {'fieldname': 'field2', 'fieldtype': 'Data', 'label': 'Field 2'}, {'fieldname': 'section2', 'fieldtype': 'Section Break', 'label': 'Section 2'}, {'fieldname': 'column21', 'fieldtype': 'Column Break', 'label': 'Column 2.1'}, {'fieldname': 'field3', 'fieldtype': 'Data', 'label': 'Field 3'}, {'fieldname': 'column22', 'fieldtype': 'Column Break', 'label': 'Column 2.2'}, {'fieldname': 'field4', 'fieldtype': 'Data', 'label': 'Field 4'}]})
doc.insert()
custom_section = frappe.get_doc({'doctype': 'Custom Field', 'dt': 'Test Custom Breaks Ordering', 'fieldname': 'custom_section', 'fieldtype': 'Section Break', 'insert_after': 'section1', 'label': 'Custom Section'})
custom_section.insert()
custom_column = frappe.get_doc({'doctype': 'Custom Field', 'dt': 'Test Custom Breaks Ordering', 'fieldname': 'custom_column_insert', 'fieldtype': 'Column Break', 'insert_after': 'column21', 'label': 'Custom Column Insert'})
custom_column.insert()
custom_column = frappe.get_doc({'doctype': 'Custom Field', 'dt': 'Test Custom Breaks Ordering', 'fieldname': 'custom_column_end', 'fieldtype': 'Column Break', 'insert_after': 'section2', 'label': 'Custom Column End'})
custom_column.insert()
updated_meta = frappe.get_meta('Test Custom Breaks Ordering', cached=False)
field_names = [field.fieldname for field in updated_meta.fields]
expected_order = ['section1', 'field1', 'field2', 'custom_section', 'section2', 'column21', 'field3', 'custom_column_insert', 'column22', 'field4', 'custom_column_end']
self.assertEqual(field_names, expected_order)
```

## Next Steps


---

*Source: test_custom_field.py:87 | Complexity: Advanced | Last updated: 2026-02-04*