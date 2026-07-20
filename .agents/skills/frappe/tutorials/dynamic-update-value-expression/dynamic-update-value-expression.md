# How To: Dynamic Update Value Expression

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test dynamic expression evaluation in workflow update_value field

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `unittest.mock`
- `responses`
- `frappe`
- `frappe.model.workflow`
- `frappe.tests`
- `frappe.tests.utils`
- `frappe.utils`
- `frappe.tests.ui_test_helpers`
- `frappe.tests.ui_test_helpers`

**Setup Required:**
```python
self.patcher = patch('frappe.attach_print', return_value={})
self.patcher.start()
frappe.db.delete('Workflow Action')
self.workflow = create_todo_workflow()
create_domain_workflow()
```

## Step-by-Step Guide

### Step 1: 'Test dynamic expression evaluation in workflow update_value field'

```python
'Test dynamic expression evaluation in workflow update_value field'
```

### Step 2: Assign unknown.update_field = 'assigned_by'

```python
self.workflow.states[1].update_field = 'assigned_by'
```

### Step 3: Assign unknown.update_value = 'frappe.session.user'

```python
self.workflow.states[1].update_value = 'frappe.session.user'
```

### Step 4: Assign unknown.evaluate_as_expression = 1

```python
self.workflow.states[1].evaluate_as_expression = 1
```

### Step 5: Call self.workflow.save()

```python
self.workflow.save()
```

### Step 6: Assign todo = create_new_todo(...)

```python
todo = create_new_todo()
```

### Step 7: Call apply_workflow()

```python
apply_workflow(todo, 'Approve')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(todo.assigned_by, frappe.session.user)
```


## Complete Example

```python
# Setup
self.patcher = patch('frappe.attach_print', return_value={})
self.patcher.start()
frappe.db.delete('Workflow Action')
self.workflow = create_todo_workflow()
create_domain_workflow()

# Workflow
'Test dynamic expression evaluation in workflow update_value field'
self.workflow.states[1].update_field = 'assigned_by'
self.workflow.states[1].update_value = 'frappe.session.user'
self.workflow.states[1].evaluate_as_expression = 1
self.workflow.save()
todo = create_new_todo()
apply_workflow(todo, 'Approve')
self.assertEqual(todo.assigned_by, frappe.session.user)
```

## Next Steps


---

*Source: test_workflow.py:133 | Complexity: Advanced | Last updated: 2026-02-04*