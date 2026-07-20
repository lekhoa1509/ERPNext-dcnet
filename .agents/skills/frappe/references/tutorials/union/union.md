# How To: Union

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test union

## Prerequisites

**Required Modules:**
- `unittest`
- `collections.abc`
- `datetime`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.query_builder`
- `frappe.query_builder.builder`
- `frappe.query_builder.custom`
- `frappe.query_builder.functions`
- `frappe.query_builder.utils`
- `frappe.tests`
- `frappe.query_builder.terms`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder.utils`


## Step-by-Step Guide

### Step 1: Assign user = frappe.qb.DocType(...)

```python
user = frappe.qb.DocType('User')
```

### Step 2: Assign role = frappe.qb.DocType(...)

```python
role = frappe.qb.DocType('Role')
```

### Step 3: Assign users = frappe.qb.from_.select(...)

```python
users = frappe.qb.from_(user).select(user.name)
```

### Step 4: Assign roles = frappe.qb.from_.select(...)

```python
roles = frappe.qb.from_(role).select(role.name)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(set(users.run() + roles.run()), set((users + roles).run()))
```


## Complete Example

```python
# Workflow
user = frappe.qb.DocType('User')
role = frappe.qb.DocType('Role')
users = frappe.qb.from_(user).select(user.name)
roles = frappe.qb.from_(role).select(role.name)
self.assertEqual(set(users.run() + roles.run()), set((users + roles).run()))
```

## Next Steps


---

*Source: test_query_builder.py:499 | Complexity: Intermediate | Last updated: 2026-02-04*