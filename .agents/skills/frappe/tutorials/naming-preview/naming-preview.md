# How To: Naming Preview

**Difficulty**: Advanced
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test naming preview

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.core.doctype.document_naming_settings.document_naming_settings`
- `frappe.model.naming`
- `frappe.tests`
- `frappe.utils`


## Step-by-Step Guide

### Step 1: Assign self.dns.transaction_type = value

```python
self.dns.transaction_type = self.ns_doctype
```

### Step 2: Assign self.dns.try_naming_series = 'AXBZ.####'

```python
self.dns.try_naming_series = 'AXBZ.####'
```

### Step 3: Assign serieses = self.dns.preview_series.split(...)

```python
serieses = self.dns.preview_series().split('\n')
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(['AXBZ0001', 'AXBZ0002', 'AXBZ0003'], serieses)
```

### Step 5: Assign self.dns.try_naming_series = 'AXBZ-.{currency}.-'

```python
self.dns.try_naming_series = 'AXBZ-.{currency}.-'
```

### Step 6: Assign serieses = self.dns.preview_series.split(...)

```python
serieses = self.dns.preview_series().split('\n')
```


## Complete Example

```python
# Workflow
self.dns.transaction_type = self.ns_doctype
self.dns.try_naming_series = 'AXBZ.####'
serieses = self.dns.preview_series().split('\n')
self.assertEqual(['AXBZ0001', 'AXBZ0002', 'AXBZ0003'], serieses)
self.dns.try_naming_series = 'AXBZ-.{currency}.-'
serieses = self.dns.preview_series().split('\n')
```

## Next Steps


---

*Source: test_document_naming_settings.py:46 | Complexity: Advanced | Last updated: 2026-02-04*