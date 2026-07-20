# How To: Update After Submit

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test update after submit

## Prerequisites

**Required Modules:**
- `inspect`
- `contextlib`
- `copy`
- `datetime`
- `unittest.mock`
- `frappe`
- `frappe.app`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.core.doctype.user.user`
- `frappe.desk.doctype.note.note`
- `frappe.model.document`
- `frappe.model.naming`
- `frappe.tests`
- `frappe.utils`
- `frappe.website.serve`
- `frappe.desk.doctype.event.event`
- `pathlib`
- `frappe.modules.utils`
- `frappe.model.document`


## Step-by-Step Guide

### Step 1: Assign d = self.test_insert(...)

```python
d = self.test_insert()
```

### Step 2: Assign d.starts_on = '2014-09-09'

```python
d.starts_on = '2014-09-09'
```

### Step 3: Call self.assertRaises()

```python
self.assertRaises(frappe.UpdateAfterSubmitError, d.validate_update_after_submit)
```

### Step 4: Assign d.meta.get_field.allow_on_submit = 1

```python
d.meta.get_field('starts_on').allow_on_submit = 1
```

### Step 5: Call d.validate_update_after_submit()

```python
d.validate_update_after_submit()
```

### Step 6: Assign d.meta.get_field.allow_on_submit = 0

```python
d.meta.get_field('starts_on').allow_on_submit = 0
```

### Step 7: Call d.reload()

```python
d.reload()
```

### Step 8: Assign d.starts_on = '2014-01-01'

```python
d.starts_on = '2014-01-01'
```

### Step 9: Call d.validate_update_after_submit()

```python
d.validate_update_after_submit()
```


## Complete Example

```python
# Workflow
d = self.test_insert()
d.starts_on = '2014-09-09'
self.assertRaises(frappe.UpdateAfterSubmitError, d.validate_update_after_submit)
d.meta.get_field('starts_on').allow_on_submit = 1
d.validate_update_after_submit()
d.meta.get_field('starts_on').allow_on_submit = 0
d.reload()
d.starts_on = '2014-01-01'
d.validate_update_after_submit()
```

## Next Steps


---

*Source: test_document.py:245 | Complexity: Advanced | Last updated: 2026-02-04*