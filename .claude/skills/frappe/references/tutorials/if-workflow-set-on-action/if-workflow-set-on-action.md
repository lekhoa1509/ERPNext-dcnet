# How To: If Workflow Set On Action

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test if workflow set on action

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

### Step 1: Assign self.workflow._update_state_docstatus = True

```python
self.workflow._update_state_docstatus = True
```

### Step 2: Assign unknown.doc_status = 1

```python
self.workflow.states[1].doc_status = 1
```

### Step 3: Call self.workflow.save()

```python
self.workflow.save()
```

### Step 4: Assign todo = create_new_todo(...)

```python
todo = create_new_todo()
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(todo.docstatus, 0)
```

### Step 6: Call todo.submit()

```python
todo.submit()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(todo.docstatus, 1)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(todo.workflow_state, 'Approved')
```

### Step 9: Assign unknown.doc_status = 0

```python
self.workflow.states[1].doc_status = 0
```

### Step 10: Call self.workflow.save()

```python
self.workflow.save()
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
self.workflow._update_state_docstatus = True
self.workflow.states[1].doc_status = 1
self.workflow.save()
todo = create_new_todo()
self.assertEqual(todo.docstatus, 0)
todo.submit()
self.assertEqual(todo.docstatus, 1)
self.assertEqual(todo.workflow_state, 'Approved')
self.workflow.states[1].doc_status = 0
self.workflow.save()
```

## Next Steps


---

*Source: test_workflow.py:110 | Complexity: Advanced | Last updated: 2026-02-04*