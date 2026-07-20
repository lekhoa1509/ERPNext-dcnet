# How To: Workflow Condition

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test condition in transition

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

### Step 1: 'Test condition in transition'

```python
'Test condition in transition'
```

### Step 2: Assign unknown.condition = 'doc.status == "Closed"'

```python
self.workflow.transitions[0].condition = 'doc.status == "Closed"'
```

### Step 3: Call self.workflow.save()

```python
self.workflow.save()
```

### Step 4: Call self.assertRaises()

```python
self.assertRaises(WorkflowTransitionError, self.test_approve)
```

### Step 5: Assign unknown.condition = ''

```python
self.workflow.transitions[0].condition = ''
```

### Step 6: Call self.workflow.save()

```python
self.workflow.save()
```


## Complete Example

```python
# Workflow
'Test condition in transition'
self.workflow.transitions[0].condition = 'doc.status == "Closed"'
self.workflow.save()
self.assertRaises(WorkflowTransitionError, self.test_approve)
self.workflow.transitions[0].condition = ''
self.workflow.save()
```

## Next Steps


---

*Source: test_workflow.py:64 | Complexity: Intermediate | Last updated: 2026-02-04*