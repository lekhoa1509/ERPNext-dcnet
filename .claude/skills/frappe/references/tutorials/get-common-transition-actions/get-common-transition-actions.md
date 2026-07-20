# How To: Get Common Transition Actions

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test get common transition actions

## Prerequisites

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


## Step-by-Step Guide

### Step 1: Assign todo1 = create_new_todo(...)

```python
todo1 = create_new_todo()
```

### Step 2: Assign todo2 = create_new_todo(...)

```python
todo2 = create_new_todo()
```

### Step 3: Assign todo3 = create_new_todo(...)

```python
todo3 = create_new_todo()
```

### Step 4: Assign todo4 = create_new_todo(...)

```python
todo4 = create_new_todo()
```

### Step 5: Assign actions = get_common_transition_actions(...)

```python
actions = get_common_transition_actions([todo1, todo2, todo3, todo4], 'ToDo')
```

### Step 6: Call self.assertSetEqual()

```python
self.assertSetEqual(set(actions), {'Approve', 'Reject'})
```

### Step 7: Call apply_workflow()

```python
apply_workflow(todo1, 'Reject')
```

### Step 8: Call apply_workflow()

```python
apply_workflow(todo2, 'Reject')
```

### Step 9: Call apply_workflow()

```python
apply_workflow(todo3, 'Approve')
```

### Step 10: Assign actions = get_common_transition_actions(...)

```python
actions = get_common_transition_actions([todo1, todo2, todo3], 'ToDo')
```

### Step 11: Call self.assertListEqual()

```python
self.assertListEqual(actions, [])
```

### Step 12: Assign actions = get_common_transition_actions(...)

```python
actions = get_common_transition_actions([todo1, todo2], 'ToDo')
```

### Step 13: Call self.assertListEqual()

```python
self.assertListEqual(actions, ['Review'])
```


## Complete Example

```python
# Workflow
todo1 = create_new_todo()
todo2 = create_new_todo()
todo3 = create_new_todo()
todo4 = create_new_todo()
actions = get_common_transition_actions([todo1, todo2, todo3, todo4], 'ToDo')
self.assertSetEqual(set(actions), {'Approve', 'Reject'})
apply_workflow(todo1, 'Reject')
apply_workflow(todo2, 'Reject')
apply_workflow(todo3, 'Approve')
actions = get_common_transition_actions([todo1, todo2, todo3], 'ToDo')
self.assertListEqual(actions, [])
actions = get_common_transition_actions([todo1, todo2], 'ToDo')
self.assertListEqual(actions, ['Review'])
```

## Next Steps


---

*Source: test_workflow.py:75 | Complexity: Advanced | Last updated: 2026-02-04*