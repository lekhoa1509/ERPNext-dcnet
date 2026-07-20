# How To: Doctype And Role Domainification

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test if doctype is hidden if the doctype's restrict to domain is not included
in active domains

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.core.doctype.domain_settings.domain_settings`
- `frappe.core.page.permission_manager.permission_manager`
- `frappe.desk.doctype.desktop_icon.desktop_icon`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: "\n\t\ttest if doctype is hidden if the doctype's restrict to domain is not included\n\t\tin active domains\n\t\t"

```python
"\n\t\ttest if doctype is hidden if the doctype's restrict to domain is not included\n\t\tin active domains\n\t\t"
```

### Step 2: Assign test_doctype = self.new_doctype(...)

```python
test_doctype = self.new_doctype('Test Domainification')
```

### Step 3: Call test_doctype.insert()

```python
test_doctype.insert()
```

### Step 4: Assign test_role = frappe.get_doc.insert(...)

```python
test_role = frappe.get_doc({'doctype': 'Role', 'role_name': '_Test Role'}).insert()
```

### Step 5: Assign results = get_roles_and_doctypes(...)

```python
results = get_roles_and_doctypes()
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue('Test Domainification' in [d.get('value') for d in results.get('doctypes')])
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue('_Test Role' in [d.get('value') for d in results.get('roles')])
```

### Step 8: Call self.add_active_domain()

```python
self.add_active_domain('_Test Domain 2')
```

### Step 9: Assign test_doctype.restrict_to_domain = '_Test Domain 2'

```python
test_doctype.restrict_to_domain = '_Test Domain 2'
```

### Step 10: Call test_doctype.save()

```python
test_doctype.save()
```

### Step 11: Assign test_role.restrict_to_domain = '_Test Domain 2'

```python
test_role.restrict_to_domain = '_Test Domain 2'
```

### Step 12: Call test_role.save()

```python
test_role.save()
```

### Step 13: Assign results = get_roles_and_doctypes(...)

```python
results = get_roles_and_doctypes()
```

### Step 14: Call self.assertTrue()

```python
self.assertTrue('Test Domainification' in [d.get('value') for d in results.get('doctypes')])
```

### Step 15: Call self.assertTrue()

```python
self.assertTrue('_Test Role' in [d.get('value') for d in results.get('roles')])
```

### Step 16: Call self.remove_from_active_domains()

```python
self.remove_from_active_domains('_Test Domain 2')
```

### Step 17: Assign results = get_roles_and_doctypes(...)

```python
results = get_roles_and_doctypes()
```

### Step 18: Call self.assertTrue()

```python
self.assertTrue('Test Domainification' not in [d.get('value') for d in results.get('doctypes')])
```

### Step 19: Call self.assertTrue()

```python
self.assertTrue('_Test Role' not in [d.get('value') for d in results.get('roles')])
```


## Complete Example

```python
# Workflow
"\n\t\ttest if doctype is hidden if the doctype's restrict to domain is not included\n\t\tin active domains\n\t\t"
test_doctype = self.new_doctype('Test Domainification')
test_doctype.insert()
test_role = frappe.get_doc({'doctype': 'Role', 'role_name': '_Test Role'}).insert()
results = get_roles_and_doctypes()
self.assertTrue('Test Domainification' in [d.get('value') for d in results.get('doctypes')])
self.assertTrue('_Test Role' in [d.get('value') for d in results.get('roles')])
self.add_active_domain('_Test Domain 2')
test_doctype.restrict_to_domain = '_Test Domain 2'
test_doctype.save()
test_role.restrict_to_domain = '_Test Domain 2'
test_role.save()
results = get_roles_and_doctypes()
self.assertTrue('Test Domainification' in [d.get('value') for d in results.get('doctypes')])
self.assertTrue('_Test Role' in [d.get('value') for d in results.get('roles')])
self.remove_from_active_domains('_Test Domain 2')
results = get_roles_and_doctypes()
self.assertTrue('Test Domainification' not in [d.get('value') for d in results.get('doctypes')])
self.assertTrue('_Test Role' not in [d.get('value') for d in results.get('roles')])
```

## Next Steps


---

*Source: test_domainification.py:81 | Complexity: Advanced | Last updated: 2026-02-04*