# How To: Invalid Expression Raises Error

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test that invalid expression raises proper error

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

### Step 1: 'Test that invalid expression raises proper error'

```python
'Test that invalid expression raises proper error'
```

### Step 2: Assign unknown.update_field = 'description'

```python
self.workflow.states[1].update_field = 'description'
```

### Step 3: Assign unknown.update_value = 'invalid_syntax(('

```python
self.workflow.states[1].update_value = 'invalid_syntax(('
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


## Complete Example

```python
# Setup
self.patcher = patch('frappe.attach_print', return_value={})
self.patcher.start()
frappe.db.delete('Workflow Action')
self.workflow = create_todo_workflow()
create_domain_workflow()

# Workflow
'Test that invalid expression raises proper error'
self.workflow.states[1].update_field = 'description'
self.workflow.states[1].update_value = 'invalid_syntax(('
self.workflow.states[1].evaluate_as_expression = 1
self.workflow.save()
todo = create_new_todo()
with self.assertRaises(frappe.ValidationError):
    apply_workflow(todo, 'Approve')
```

## Next Steps


---

*Source: test_workflow.py:172 | Complexity: Intermediate | Last updated: 2026-02-04*