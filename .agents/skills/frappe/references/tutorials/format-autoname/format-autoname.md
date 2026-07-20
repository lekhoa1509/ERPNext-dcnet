# How To: Format Autoname

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test if braced params are replaced in format autoname

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

### Step 1: '\n\t\tTest if braced params are replaced in format autoname\n\t\t'

```python
'\n\t\tTest if braced params are replaced in format autoname\n\t\t'
```

### Step 2: Assign doctype = new_doctype.insert(...)

```python
doctype = new_doctype(autoname='format:TODO-{MM}-{some_fieldname}-{##}').insert()
```

### Step 3: Assign description = 'Format'

```python
description = 'Format'
```

### Step 4: Assign doc = frappe.new_doc(...)

```python
doc = frappe.new_doc(doctype.name)
```

### Step 5: Assign doc.some_fieldname = description

```python
doc.some_fieldname = description
```

### Step 6: Call doc.insert()

```python
doc.insert()
```

### Step 7: Assign series = getseries(...)

```python
series = getseries('', 2)
```

### Step 8: Assign series = value

```python
series = int(series) - 1
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(doc.name, f"TODO-{now_datetime().strftime('%m')}-{description}-{series:02}")
```


## Complete Example

```python
# Setup
frappe.db.delete('Note')

# Workflow
'\n\t\tTest if braced params are replaced in format autoname\n\t\t'
doctype = new_doctype(autoname='format:TODO-{MM}-{some_fieldname}-{##}').insert()
description = 'Format'
doc = frappe.new_doc(doctype.name)
doc.some_fieldname = description
doc.insert()
series = getseries('', 2)
series = int(series) - 1
self.assertEqual(doc.name, f"TODO-{now_datetime().strftime('%m')}-{description}-{series:02}")
```

## Next Steps


---

*Source: test_naming.py:93 | Complexity: Advanced | Last updated: 2026-02-04*