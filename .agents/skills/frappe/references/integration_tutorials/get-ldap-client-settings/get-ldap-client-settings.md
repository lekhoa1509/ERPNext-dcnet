# How To: Get Ldap Client Settings

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, unittest, workflow, integration

## Overview

Workflow: test get ldap client settings

## Prerequisites

**Required Modules:**
- `contextlib`
- `functools`
- `os`
- `ssl`
- `typing`
- `unittest`
- `ldap3`
- `ldap3`
- `frappe`
- `frappe.exceptions`
- `frappe.integrations.doctype.ldap_settings.ldap_settings`


## Step-by-Step Guide

### Step 1: Assign result = self.test_class.get_ldap_client_settings(...)

```python
result = self.test_class.get_ldap_client_settings()
```

### Step 2: Call self.assertIsInstance()

```python
self.assertIsInstance(result, dict)
```

### Step 3: Call self.assertTrue()

```python
self.assertTrue(result['enabled'] == self.doc['enabled'])
```

### Step 4: Assign localdoc = self.doc.copy(...)

```python
localdoc = self.doc.copy()
```

### Step 5: Assign unknown = False

```python
localdoc['enabled'] = False
```

### Step 6: Call frappe.get_doc.save()

```python
frappe.get_doc(localdoc).save()
```

### Step 7: Assign result = self.test_class.get_ldap_client_settings(...)

```python
result = self.test_class.get_ldap_client_settings()
```

### Step 8: Call self.assertFalse()

```python
self.assertFalse(result['enabled'])
```


## Complete Example

```python
# Workflow
result = self.test_class.get_ldap_client_settings()
self.assertIsInstance(result, dict)
self.assertTrue(result['enabled'] == self.doc['enabled'])
localdoc = self.doc.copy()
localdoc['enabled'] = False
frappe.get_doc(localdoc).save()
result = self.test_class.get_ldap_client_settings()
self.assertFalse(result['enabled'])
```

## Next Steps


---

*Source: test_ldap_settings.py:316 | Complexity: Advanced | Last updated: 2026-02-04*