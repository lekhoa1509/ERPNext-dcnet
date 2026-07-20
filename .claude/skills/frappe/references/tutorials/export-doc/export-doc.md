# How To: Export Doc

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test export doc

## Prerequisites

**Required Modules:**
- `os`
- `re`
- `unittest`
- `typing`
- `frappe`
- `frappe.tests`
- `frappe.printing.doctype.print_format.print_format`


## Step-by-Step Guide

### Step 1: Assign doc.standard = 'Yes'

```python
doc.standard = 'Yes'
```

### Step 2: Assign _before = value

```python
_before = frappe.conf.developer_mode
```

### Step 3: Assign frappe.conf.developer_mode = True

```python
frappe.conf.developer_mode = True
```

### Step 4: Assign export_path = doc.export_doc(...)

```python
export_path = doc.export_doc()
```

### Step 5: Assign frappe.conf.developer_mode = _before

```python
frappe.conf.developer_mode = _before
```

### Step 6: Assign exported_doc_path = value

```python
exported_doc_path = f'{export_path}.json'
```

### Step 7: Call doc.reload()

```python
doc.reload()
```

### Step 8: Assign doc_dict = doc.as_dict(...)

```python
doc_dict = doc.as_dict(no_nulls=True, convert_dates_to_str=True)
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue(os.path.exists(exported_doc_path))
```

### Step 10: Call self.addCleanup()

```python
self.addCleanup(os.remove, exported_doc_path)
```

### Step 11: Assign exported_doc = frappe.parse_json(...)

```python
exported_doc = frappe.parse_json(f.read())
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(value, doc_dict[key])
```


## Complete Example

```python
# Workflow
doc: PrintFormat = frappe.get_doc('Print Format', self.globalTestRecords['Print Format'][0]['name'])
doc.standard = 'Yes'
_before = frappe.conf.developer_mode
frappe.conf.developer_mode = True
export_path = doc.export_doc()
frappe.conf.developer_mode = _before
exported_doc_path = f'{export_path}.json'
doc.reload()
doc_dict = doc.as_dict(no_nulls=True, convert_dates_to_str=True)
self.assertTrue(os.path.exists(exported_doc_path))
with open(exported_doc_path) as f:
    exported_doc = frappe.parse_json(f.read())
for key, value in exported_doc.items():
    if key in doc_dict:
        with self.subTest(key=key):
            self.assertEqual(value, doc_dict[key])
self.addCleanup(os.remove, exported_doc_path)
```

## Next Steps


---

*Source: test_print_format.py:39 | Complexity: Advanced | Last updated: 2026-02-04*