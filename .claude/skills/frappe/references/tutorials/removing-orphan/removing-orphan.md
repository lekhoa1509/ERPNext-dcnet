# How To: Removing Orphan

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test removing orphan

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.model.sync`
- `frappe.modules.export_file`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Assign _before = value

```python
_before = frappe.conf.developer_mode
```

### Step 2: Assign frappe.conf.developer_mode = True

```python
frappe.conf.developer_mode = True
```

### Step 3: Assign report = frappe.new_doc(...)

```python
report = frappe.new_doc('Report')
```

### Step 4: Assign args = value

```python
args = {'doctype': 'Report', 'report_name': 'Orphan Report', 'ref_doctype': 'DocType', 'is_standard': 'Yes', 'module': 'Custom'}
```

### Step 5: Call report.update()

```python
report.update(args)
```

### Step 6: Call report.save()

```python
report.save()
```

### Step 7: Call print()

```python
print(f'Created report: {report.name}')
```

### Step 8: Call delete_folder()

```python
delete_folder('Custom', 'Report', report.name)
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue(frappe.db.exists('Report', report.name))
```

### Step 10: Call self.assertFalse()

```python
self.assertFalse(frappe.db.exists('Report', report.name))
```

### Step 11: Assign frappe.conf.developer_mode = _before

```python
frappe.conf.developer_mode = _before
```

### Step 12: Call remove_orphan_entities()

```python
remove_orphan_entities()
```


## Complete Example

```python
# Workflow
_before = frappe.conf.developer_mode
frappe.conf.developer_mode = True
report = frappe.new_doc('Report')
args = {'doctype': 'Report', 'report_name': 'Orphan Report', 'ref_doctype': 'DocType', 'is_standard': 'Yes', 'module': 'Custom'}
report.update(args)
report.save()
print(f'Created report: {report.name}')
delete_folder('Custom', 'Report', report.name)
self.assertTrue(frappe.db.exists('Report', report.name))
if frappe.db.exists('Report', report.name):
    remove_orphan_entities()
self.assertFalse(frappe.db.exists('Report', report.name))
frappe.conf.developer_mode = _before
```

## Next Steps


---

*Source: test_removing_orphans.py:8 | Complexity: Advanced | Last updated: 2026-02-04*