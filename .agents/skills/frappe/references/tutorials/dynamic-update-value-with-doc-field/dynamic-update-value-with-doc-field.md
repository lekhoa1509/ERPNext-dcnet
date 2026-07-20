# How To: Dynamic Update Value With Doc Field

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test dynamic expression using doc field value

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

### Step 1: 'Test dynamic expression using doc field value'

```python
'Test dynamic expression using doc field value'
```

### Step 2: Assign unknown.update_field = 'description'

```python
self.workflow.states[1].update_field = 'description'
```

### Step 3: Assign unknown.update_value = "doc.allocated_to or 'No assignee'"

```python
self.workflow.states[1].update_value = "doc.allocated_to or 'No assignee'"
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

### Step 7: Assign todo.allocated_to = 'Administrator'

```python
todo.allocated_to = 'Administrator'
```

### Step 8: Call todo.save()

```python
todo.save()
```

### Step 9: Call apply_workflow()

```python
apply_workflow(todo, 'Approve')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(todo.description, 'Administrator')
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
'Test dynamic expression using doc field value'
self.workflow.states[1].update_field = 'description'
self.workflow.states[1].update_value = "doc.allocated_to or 'No assignee'"
self.workflow.states[1].evaluate_as_expression = 1
self.workflow.save()
todo = create_new_todo()
todo.allocated_to = 'Administrator'
todo.save()
apply_workflow(todo, 'Approve')
self.assertEqual(todo.description, 'Administrator')
```

## Next Steps


---

*Source: test_workflow.py:145 | Complexity: Advanced | Last updated: 2026-02-04*