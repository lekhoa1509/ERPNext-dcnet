# How To: Naming Series Validation

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test naming series validation

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

### Step 1: Assign dns = frappe.get_doc(...)

```python
dns = frappe.get_doc('Document Naming Settings')
```

### Step 2: Assign existing_series = value

```python
existing_series = dns.get_transactions_and_prefixes()['prefixes']
```

### Step 3: Assign valid = value

```python
valid = ['SINV-', 'SI-.{field}.', 'SI-#.###', '', *existing_series]
```

### Step 4: Assign invalid = value

```python
invalid = ['$INV-', 'WINDOWS\\NAMING']
```

### Step 5: Call self.assertRaises()

```python
self.assertRaises(InvalidNamingSeriesError, NamingSeries(series).validate)
```

### Step 6: Call NamingSeries.validate()

```python
NamingSeries(series).validate()
```

### Step 7: Call self.fail()

```python
self.fail(f'{series} should be valid\n{e}')
```


## Complete Example

```python
# Setup
frappe.db.delete('Note')

# Workflow
dns = frappe.get_doc('Document Naming Settings')
existing_series = dns.get_transactions_and_prefixes()['prefixes']
valid = ['SINV-', 'SI-.{field}.', 'SI-#.###', '', *existing_series]
invalid = ['$INV-', 'WINDOWS\\NAMING']
for series in valid:
    if series.strip():
        try:
            NamingSeries(series).validate()
        except Exception as e:
            self.fail(f'{series} should be valid\n{e}')
for series in invalid:
    self.assertRaises(InvalidNamingSeriesError, NamingSeries(series).validate)
```

## Next Steps


---

*Source: test_naming.py:327 | Complexity: Advanced | Last updated: 2026-02-04*