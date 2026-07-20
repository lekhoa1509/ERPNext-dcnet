# How To: List View Comment Count

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test list view comment count

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe.desk.listview`
- `frappe.desk.reportview`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Assign frappe.form_dict.doctype = 'DocType'

```python
frappe.form_dict.doctype = 'DocType'
```

### Step 2: Assign frappe.form_dict.limit = '1'

```python
frappe.form_dict.limit = '1'
```

### Step 3: Assign frappe.form_dict.fields = value

```python
frappe.form_dict.fields = ['`tabDocType`.`name`']
```

### Step 4: Assign frappe.form_dict.with_comment_count = with_comment_count

```python
frappe.form_dict.with_comment_count = with_comment_count
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(len(get()['values'][0]), 2)
```

### Step 6: Assign frappe.form_dict.with_comment_count = with_comment_count

```python
frappe.form_dict.with_comment_count = with_comment_count
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(len(get()['values'][0]), 1)
```


## Complete Example

```python
# Workflow
frappe.form_dict.doctype = 'DocType'
frappe.form_dict.limit = '1'
frappe.form_dict.fields = ['`tabDocType`.`name`']
for with_comment_count in (1, True, '1'):
    frappe.form_dict.with_comment_count = with_comment_count
    self.assertEqual(len(get()['values'][0]), 2)
for with_comment_count in (0, False, '0', None):
    frappe.form_dict.with_comment_count = with_comment_count
    self.assertEqual(len(get()['values'][0]), 1)
```

## Next Steps


---

*Source: test_listview.py:83 | Complexity: Intermediate | Last updated: 2026-02-04*