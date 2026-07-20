# How To: Naming With Empty Part

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test naming with empty part

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

### Step 1: Assign webhook = frappe.new_doc(...)

```python
webhook = frappe.new_doc('Webhook')
```

### Step 2: Assign webhook.webhook_docevent = 'on_update'

```python
webhook.webhook_docevent = 'on_update'
```

### Step 3: Assign series = 'KOOH-..{webhook_docevent}.-.####'

```python
series = 'KOOH-..{webhook_docevent}.-.####'
```

### Step 4: Assign name = parse_naming_series(...)

```python
name = parse_naming_series(series, doc=webhook)
```

### Step 5: Call self.assertTrue()

```python
self.assertTrue(name.startswith('KOOH-on_update'), f'incorrect name generated {name}, missing field value')
```


## Complete Example

```python
# Setup
frappe.db.delete('Note')

# Workflow
webhook = frappe.new_doc('Webhook')
webhook.webhook_docevent = 'on_update'
series = 'KOOH-..{webhook_docevent}.-.####'
name = parse_naming_series(series, doc=webhook)
self.assertTrue(name.startswith('KOOH-on_update'), f'incorrect name generated {name}, missing field value')
```

## Next Steps


---

*Source: test_naming.py:351 | Complexity: Intermediate | Last updated: 2026-02-04*