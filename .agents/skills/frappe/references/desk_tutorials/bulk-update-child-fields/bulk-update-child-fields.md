# How To: Bulk Update Child Fields

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test bulk update child fields

## Prerequisites

**Required Modules:**
- `time`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.desk.doctype.bulk_update.bulk_update`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Assign doctype_doc = frappe.get_doc(...)

```python
doctype_doc = frappe.get_doc('DocType', self.doctype)
```

### Step 2: Call doctype_doc.append()

```python
doctype_doc.append('fields', {'fieldname': 'child_table', 'fieldtype': 'Table', 'options': self.child_doctype})
```

### Step 3: Call doctype_doc.save()

```python
doctype_doc.save()
```

### Step 4: Call frappe.db.commit()

```python
frappe.db.commit()
```

### Step 5: Assign existing_docs = frappe.get_all(...)

```python
existing_docs = frappe.get_all(self.doctype, {'docstatus': 0}, pluck='name')
```

### Step 6: Call frappe.db.commit()

```python
frappe.db.commit()
```

### Step 7: Assign update_data = value

```python
update_data = {'child_table_updates': {self.child_doctype: {'some_fieldname': '_Test Child Updated'}}}
```

### Step 8: Assign docnames = frappe.get_all(...)

```python
docnames = frappe.get_all(self.doctype, {'docstatus': 0}, limit=5, pluck='name')
```

### Step 9: Assign failed = submit_cancel_or_update_docs(...)

```python
failed = submit_cancel_or_update_docs(self.doctype, docnames, action='update', data=update_data)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(failed, [])
```

### Step 11: Assign docnames_bg = frappe.get_all(...)

```python
docnames_bg = frappe.get_all(self.doctype, {'docstatus': 0}, limit=20, pluck='name')
```

### Step 12: Call submit_cancel_or_update_docs()

```python
submit_cancel_or_update_docs(self.doctype, docnames_bg, action='update', data=update_data)
```

### Step 13: Call self.wait_for_assertion()

```python
self.wait_for_assertion(lambda: check_child_field(docnames_bg, '_Test Child Updated'))
```

### Step 14: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc(self.doctype, docname)
```

### Step 15: Call doc.append()

```python
doc.append('child_table', {'some_fieldname': '_Test Child Value'})
```

### Step 16: Call doc.save()

```python
doc.save()
```

### Step 17: Call frappe.db.rollback()

```python
frappe.db.rollback()
```

### Step 18: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc(self.doctype, docname)
```


## Complete Example

```python
# Workflow
doctype_doc = frappe.get_doc('DocType', self.doctype)
doctype_doc.append('fields', {'fieldname': 'child_table', 'fieldtype': 'Table', 'options': self.child_doctype})
doctype_doc.save()
frappe.db.commit()
existing_docs = frappe.get_all(self.doctype, {'docstatus': 0}, pluck='name')
for docname in existing_docs:
    doc = frappe.get_doc(self.doctype, docname)
    doc.append('child_table', {'some_fieldname': '_Test Child Value'})
    doc.save()
frappe.db.commit()
update_data = {'child_table_updates': {self.child_doctype: {'some_fieldname': '_Test Child Updated'}}}

def check_child_field(docs, expected):
    frappe.db.rollback()
    for docname in docs:
        doc = frappe.get_doc(self.doctype, docname)
        if not doc.child_table or doc.child_table[0].some_fieldname != expected:
            return False
    return True
docnames = frappe.get_all(self.doctype, {'docstatus': 0}, limit=5, pluck='name')
failed = submit_cancel_or_update_docs(self.doctype, docnames, action='update', data=update_data)
self.assertEqual(failed, [])
docnames_bg = frappe.get_all(self.doctype, {'docstatus': 0}, limit=20, pluck='name')
submit_cancel_or_update_docs(self.doctype, docnames_bg, action='update', data=update_data)
self.wait_for_assertion(lambda: check_child_field(docnames_bg, '_Test Child Updated'))
```

## Next Steps


---

*Source: test_bulk_update.py:70 | Complexity: Advanced | Last updated: 2026-02-04*