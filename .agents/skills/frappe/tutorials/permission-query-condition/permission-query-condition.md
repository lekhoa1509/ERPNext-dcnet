# How To: Permission Query Condition

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test permission query condition

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `datetime`
- `contextlib`
- `unittest.mock`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.core.page.permission_manager.permission_manager`
- `frappe.custom.doctype.property_setter.property_setter`
- `frappe.database.utils`
- `frappe.desk.reportview`
- `frappe.handler`
- `frappe.model.db_query`
- `frappe.permissions`
- `frappe.query_builder`
- `frappe.tests`
- `frappe.tests.test_helpers`
- `frappe.tests.test_query_builder`
- `frappe.utils.testutils`
- `frappe.utils`
- `frappe.desk.search`
- `frappe.core.page.permission_manager.permission_manager`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.desk.doctype.dashboard_settings.dashboard_settings`
- `frappe.desk.reportview`
- `frappe.desk`
- `frappe.types.filter`

**Setup Required:**
```python
setup_for_tests()
frappe.set_user('Administrator')
```

## Step-by-Step Guide

### Step 1: Assign self.doctype = 'Dashboard Settings'

```python
self.doctype = 'Dashboard Settings'
```

### Step 2: Assign self.user = "test'5@example.com"

```python
self.user = "test'5@example.com"
```

### Step 3: Assign permission_query_conditions = DatabaseQuery.get_permission_query_conditions(...)

```python
permission_query_conditions = DatabaseQuery.get_permission_query_conditions(self)
```

### Step 4: Call create_dashboard_settings()

```python
create_dashboard_settings(self.user)
```

### Step 5: Assign dashboard_settings = value

```python
dashboard_settings = frappe.db.sql(f'\n\t\t\t\tSELECT name\n\t\t\t\tFROM `tabDashboard Settings`\n\t\t\t\tWHERE {permission_query_conditions}\n\t\t\t', as_dict=1)[0]
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue(dashboard_settings)
```


## Complete Example

```python
# Setup
setup_for_tests()
frappe.set_user('Administrator')

# Workflow
from frappe.desk.doctype.dashboard_settings.dashboard_settings import create_dashboard_settings
self.doctype = 'Dashboard Settings'
self.user = "test'5@example.com"
permission_query_conditions = DatabaseQuery.get_permission_query_conditions(self)
create_dashboard_settings(self.user)
dashboard_settings = frappe.db.sql(f'\n\t\t\t\tSELECT name\n\t\t\t\tFROM `tabDashboard Settings`\n\t\t\t\tWHERE {permission_query_conditions}\n\t\t\t', as_dict=1)[0]
self.assertTrue(dashboard_settings)
```

## Next Steps


---

*Source: test_db_query.py:989 | Complexity: Intermediate | Last updated: 2026-02-04*