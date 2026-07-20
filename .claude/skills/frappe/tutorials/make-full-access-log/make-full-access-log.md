# How To: Make Full Access Log

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test make full access log

## Prerequisites

**Required Modules:**
- `base64`
- `os`
- `requests`
- `frappe`
- `frappe.core.doctype.access_log.access_log`
- `frappe.core.doctype.data_import.data_import`
- `frappe.core.doctype.user.user`
- `frappe.tests`
- `frappe.utils`


## Step-by-Step Guide

### Step 1: Assign self.maxDiff = None

```python
self.maxDiff = None
```

### Step 2: Call make_access_log()

```python
make_access_log(doctype=self.test_doctype, document=self.test_document, report_name=self.test_report_name, page=self.test_html_template, file_type=self.test_file_type, method=self.test_method, filters=self.test_filters)
```

### Step 3: Assign last_doc = frappe.get_last_doc(...)

```python
last_doc = frappe.get_last_doc('Access Log')
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(last_doc.filters, cstr(self.test_filters))
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(self.test_doctype, last_doc.export_from)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(self.test_document, last_doc.reference_document)
```


## Complete Example

```python
# Workflow
self.maxDiff = None
make_access_log(doctype=self.test_doctype, document=self.test_document, report_name=self.test_report_name, page=self.test_html_template, file_type=self.test_file_type, method=self.test_method, filters=self.test_filters)
last_doc = frappe.get_last_doc('Access Log')
self.assertEqual(last_doc.filters, cstr(self.test_filters))
self.assertEqual(self.test_doctype, last_doc.export_from)
self.assertEqual(self.test_document, last_doc.reference_document)
```

## Next Steps


---

*Source: test_access_log.py:116 | Complexity: Intermediate | Last updated: 2026-02-04*