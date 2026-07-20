# How To: Or Filters

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test OR filter conditions.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `itertools`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.permissions`
- `frappe.query_builder`
- `frappe.query_builder.functions`
- `frappe.tests`
- `frappe.tests.classes.context_managers`
- `frappe.tests.test_db_query`
- `frappe.tests.test_helpers`
- `frappe.tests.test_query_builder`
- `frappe.utils.nestedset`
- `frappe.permissions`
- `frappe.permissions`
- `frappe.core.page.permission_manager.permission_manager`
- `frappe.desk.doctype.dashboard_settings.dashboard_settings`
- `frappe.share`
- `frappe.share`
- `frappe.core.page.permission_manager.permission_manager`
- `frappe.share`
- `frappe.permissions`
- `frappe.core.page.permission_manager.permission_manager`
- `frappe.permissions`
- `frappe.database.query`

**Setup Required:**
```python
setup_for_tests()
```

## Step-by-Step Guide

### Step 1: 'Test OR filter conditions.'

```python
'Test OR filter conditions.'
```

### Step 2: Call self.assertQueryEqual()

```python
self.assertQueryEqual(frappe.qb.get_query('DocType', fields=['name'], or_filters={'name': 'User', 'module': 'Core'}).get_sql(), "SELECT `name` FROM `tabDocType` WHERE `name`='User' OR `module`='Core'")
```

### Step 3: Call self.assertQueryEqual()

```python
self.assertQueryEqual(frappe.qb.get_query('DocType', fields=['name'], or_filters=[['name', '=', 'User'], ['module', '=', 'Core']]).get_sql(), "SELECT `name` FROM `tabDocType` WHERE `name`='User' OR `module`='Core'")
```

### Step 4: Assign query = "SELECT `name` FROM `tabDocType` WHERE `name` LIKE 'User%' OR `module` IN ('Core','Custom')"

```python
query = "SELECT `name` FROM `tabDocType` WHERE `name` LIKE 'User%' OR `module` IN ('Core','Custom')"
```

### Step 5: Assign query, query = query.replace(...)

```python
query = query = query.replace('LIKE', 'ILIKE' if frappe.db.db_type == 'postgres' else 'LIKE')
```

### Step 6: Call self.assertQueryEqual()

```python
self.assertQueryEqual(frappe.qb.get_query('DocType', fields=['name'], or_filters={'name': ('like', 'User%'), 'module': ('in', ['Core', 'Custom'])}).get_sql(), query)
```

### Step 7: Call self.assertQueryEqual()

```python
self.assertQueryEqual(frappe.qb.get_query('DocType', fields=['name'], filters={'issingle': 0}, or_filters={'name': 'User', 'module': 'Core'}).get_sql(), "SELECT `name` FROM `tabDocType` WHERE `issingle`=0 AND (`name`='User' OR `module`='Core')")
```

### Step 8: Call self.assertQueryEqual()

```python
self.assertQueryEqual(frappe.qb.get_query('DocType', fields=['name'], filters={'issingle': 0, 'custom': 0}, or_filters={'name': 'User', 'module': 'Core'}).get_sql(), "SELECT `name` FROM `tabDocType` WHERE `issingle`=0 AND `custom`=0 AND (`name`='User' OR `module`='Core')")
```

### Step 9: Call self.assertQueryEqual()

```python
self.assertQueryEqual(frappe.qb.get_query('DocType', or_filters=['User', 'Role', 'Note']).get_sql(), "SELECT `name` FROM `tabDocType` WHERE `name` IN ('User','Role','Note')")
```

### Step 10: Call self.assertQueryEqual()

```python
self.assertQueryEqual(frappe.qb.get_query('DocType', fields=['name'], or_filters={'idx': ('>', 5), 'issingle': ('=', 1)}).get_sql(), 'SELECT `name` FROM `tabDocType` WHERE `idx`>5 OR `issingle`=1')
```

### Step 11: Call self.assertQueryEqual()

```python
self.assertQueryEqual(frappe.qb.get_query('DocType', fields=['name'], or_filters=[['DocType', 'name', '=', 'User'], ['DocType', 'name', '=', 'Role']]).get_sql(), "SELECT `name` FROM `tabDocType` WHERE `name`='User' OR `name`='Role'")
```

### Step 12: Call self.assertQueryEqual()

```python
self.assertQueryEqual(frappe.qb.get_query('DocType', fields=['name'], or_filters={'name': ('!=', 'User'), 'module': ('!=', 'Core')}).get_sql(), "SELECT `name` FROM `tabDocType` WHERE `name`<>'User' OR `module`<>'Core'")
```

### Step 13: Call self.assertQueryEqual()

```python
self.assertQueryEqual(frappe.qb.get_query('DocType', fields=['name'], filters={'custom': 0}, or_filters={}).get_sql(), 'SELECT `name` FROM `tabDocType` WHERE `custom`=0')
```

### Step 14: Call self.assertQueryEqual()

```python
self.assertQueryEqual(frappe.qb.get_query('DocType', fields=['name'], or_filters={'name': ('not in', ['User', 'Role']), 'module': ('=', 'Core')}).get_sql(), "SELECT `name` FROM `tabDocType` WHERE `name` NOT IN ('User','Role') OR `module`='Core'")
```

### Step 15: Assign query = "SELECT `name`,`module` FROM `tabDocType` WHERE `name` LIKE 'User%' OR `issingle`=1 OR `custom`=0"

```python
query = "SELECT `name`,`module` FROM `tabDocType` WHERE `name` LIKE 'User%' OR `issingle`=1 OR `custom`=0"
```

### Step 16: Assign query, query = query.replace(...)

```python
query = query = query.replace('LIKE', 'ILIKE' if frappe.db.db_type == 'postgres' else 'LIKE')
```

### Step 17: Call self.assertQueryEqual()

```python
self.assertQueryEqual(frappe.qb.get_query('DocType', fields=['name', 'module'], or_filters=[['name', 'like', 'User%'], ['issingle', '=', 1], ['custom', '=', 0]]).get_sql(), query)
```


## Complete Example

```python
# Setup
setup_for_tests()

# Workflow
'Test OR filter conditions.'
self.assertQueryEqual(frappe.qb.get_query('DocType', fields=['name'], or_filters={'name': 'User', 'module': 'Core'}).get_sql(), "SELECT `name` FROM `tabDocType` WHERE `name`='User' OR `module`='Core'")
self.assertQueryEqual(frappe.qb.get_query('DocType', fields=['name'], or_filters=[['name', '=', 'User'], ['module', '=', 'Core']]).get_sql(), "SELECT `name` FROM `tabDocType` WHERE `name`='User' OR `module`='Core'")
query = "SELECT `name` FROM `tabDocType` WHERE `name` LIKE 'User%' OR `module` IN ('Core','Custom')"
query = query = query.replace('LIKE', 'ILIKE' if frappe.db.db_type == 'postgres' else 'LIKE')
self.assertQueryEqual(frappe.qb.get_query('DocType', fields=['name'], or_filters={'name': ('like', 'User%'), 'module': ('in', ['Core', 'Custom'])}).get_sql(), query)
self.assertQueryEqual(frappe.qb.get_query('DocType', fields=['name'], filters={'issingle': 0}, or_filters={'name': 'User', 'module': 'Core'}).get_sql(), "SELECT `name` FROM `tabDocType` WHERE `issingle`=0 AND (`name`='User' OR `module`='Core')")
self.assertQueryEqual(frappe.qb.get_query('DocType', fields=['name'], filters={'issingle': 0, 'custom': 0}, or_filters={'name': 'User', 'module': 'Core'}).get_sql(), "SELECT `name` FROM `tabDocType` WHERE `issingle`=0 AND `custom`=0 AND (`name`='User' OR `module`='Core')")
self.assertQueryEqual(frappe.qb.get_query('DocType', or_filters=['User', 'Role', 'Note']).get_sql(), "SELECT `name` FROM `tabDocType` WHERE `name` IN ('User','Role','Note')")
self.assertQueryEqual(frappe.qb.get_query('DocType', fields=['name'], or_filters={'idx': ('>', 5), 'issingle': ('=', 1)}).get_sql(), 'SELECT `name` FROM `tabDocType` WHERE `idx`>5 OR `issingle`=1')
self.assertQueryEqual(frappe.qb.get_query('DocType', fields=['name'], or_filters=[['DocType', 'name', '=', 'User'], ['DocType', 'name', '=', 'Role']]).get_sql(), "SELECT `name` FROM `tabDocType` WHERE `name`='User' OR `name`='Role'")
self.assertQueryEqual(frappe.qb.get_query('DocType', fields=['name'], or_filters={'name': ('!=', 'User'), 'module': ('!=', 'Core')}).get_sql(), "SELECT `name` FROM `tabDocType` WHERE `name`<>'User' OR `module`<>'Core'")
self.assertQueryEqual(frappe.qb.get_query('DocType', fields=['name'], filters={'custom': 0}, or_filters={}).get_sql(), 'SELECT `name` FROM `tabDocType` WHERE `custom`=0')
self.assertQueryEqual(frappe.qb.get_query('DocType', fields=['name'], or_filters={'name': ('not in', ['User', 'Role']), 'module': ('=', 'Core')}).get_sql(), "SELECT `name` FROM `tabDocType` WHERE `name` NOT IN ('User','Role') OR `module`='Core'")
query = "SELECT `name`,`module` FROM `tabDocType` WHERE `name` LIKE 'User%' OR `issingle`=1 OR `custom`=0"
query = query = query.replace('LIKE', 'ILIKE' if frappe.db.db_type == 'postgres' else 'LIKE')
self.assertQueryEqual(frappe.qb.get_query('DocType', fields=['name', 'module'], or_filters=[['name', 'like', 'User%'], ['issingle', '=', 1], ['custom', '=', 0]]).get_sql(), query)
```

## Next Steps


---

*Source: test_query.py:437 | Complexity: Advanced | Last updated: 2026-02-04*