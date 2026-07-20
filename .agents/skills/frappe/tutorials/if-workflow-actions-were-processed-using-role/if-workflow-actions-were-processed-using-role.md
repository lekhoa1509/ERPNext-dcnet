# How To: If Workflow Actions Were Processed Using Role

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test if workflow actions were processed using role

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

### Step 1: Assign user = frappe.get_doc(...)

```python
user = frappe.get_doc('User', 'test2@example.com')
```

### Step 2: Call user.add_roles()

```python
user.add_roles('Test Approver', 'System Manager')
```

### Step 3: Call frappe.set_user()

```python
frappe.set_user('test2@example.com')
```

### Step 4: Assign doc = self.test_default_condition(...)

```python
doc = self.test_default_condition()
```

### Step 5: Assign workflow_actions = frappe.get_all(...)

```python
workflow_actions = frappe.get_all('Workflow Action', fields=['*'])
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(len(workflow_actions), 1)
```

### Step 7: Call self.test_approve()

```python
self.test_approve(doc)
```

### Step 8: Call user.remove_roles()

```python
user.remove_roles('Test Approver', 'System Manager')
```

### Step 9: Assign workflow_actions = frappe.get_all(...)

```python
workflow_actions = frappe.get_all('Workflow Action', fields=['*'])
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(len(workflow_actions), 1)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(workflow_actions[0].status, 'Completed')
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
user = frappe.get_doc('User', 'test2@example.com')
user.add_roles('Test Approver', 'System Manager')
frappe.set_user('test2@example.com')
doc = self.test_default_condition()
workflow_actions = frappe.get_all('Workflow Action', fields=['*'])
self.assertEqual(len(workflow_actions), 1)
self.test_approve(doc)
user.remove_roles('Test Approver', 'System Manager')
workflow_actions = frappe.get_all('Workflow Action', fields=['*'])
self.assertEqual(len(workflow_actions), 1)
self.assertEqual(workflow_actions[0].status, 'Completed')
```

## Next Steps


---

*Source: test_workflow.py:94 | Complexity: Advanced | Last updated: 2026-02-04*