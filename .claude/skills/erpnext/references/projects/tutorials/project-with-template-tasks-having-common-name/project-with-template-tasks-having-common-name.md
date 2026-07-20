# How To: Project With Template Tasks Having Common Name

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test project with template tasks having common name

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.utils`
- `erpnext.projects.doctype.project_template.test_project_template`
- `erpnext.projects.doctype.task.test_task`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.tests.utils`
- `erpnext.projects.doctype.timesheet.test_timesheet`
- `erpnext.setup.doctype.employee.test_employee`


## Step-by-Step Guide

### Step 1: Assign template_parent_task1 = create_task(...)

```python
template_parent_task1 = create_task(subject='Parent Task - 1', is_template=1, is_group=1)
```

### Step 2: Assign template_parent_task2 = create_task(...)

```python
template_parent_task2 = create_task(subject='Parent Task - 2', is_template=1, is_group=1)
```

### Step 3: Assign template_parent_task3 = create_task(...)

```python
template_parent_task3 = create_task(subject='Parent Task - 1', is_template=1, is_group=1)
```

### Step 4: Assign template_task1 = create_task(...)

```python
template_task1 = create_task(subject='Task - 1', is_template=1, parent_task=template_parent_task1.name)
```

### Step 5: Assign template_task2 = create_task(...)

```python
template_task2 = create_task(subject='Task - 2', is_template=1, parent_task=template_parent_task2.name)
```

### Step 6: Assign template_task3 = create_task(...)

```python
template_task3 = create_task(subject='Task - 1', is_template=1, parent_task=template_parent_task3.name)
```

### Step 7: Assign template_tasks = value

```python
template_tasks = [template_parent_task1, template_task1, template_parent_task2, template_task2, template_parent_task3, template_task3]
```

### Step 8: Assign project_template = make_project_template(...)

```python
project_template = make_project_template('Project template with common Task Subject', template_tasks)
```

### Step 9: Assign project = get_project(...)

```python
project = get_project('Project with common Task Subject', project_template)
```

### Step 10: Assign project_tasks = frappe.get_all(...)

```python
project_tasks = frappe.get_all('Task', {'project': project.name}, ['subject', 'parent_task', 'is_group'])
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(len(project_tasks), len(template_tasks))
```

### Step 12: Call self.assertIsNotNone()

```python
self.assertIsNotNone(pt.parent_task)
```


## Complete Example

```python
# Workflow
template_parent_task1 = create_task(subject='Parent Task - 1', is_template=1, is_group=1)
template_parent_task2 = create_task(subject='Parent Task - 2', is_template=1, is_group=1)
template_parent_task3 = create_task(subject='Parent Task - 1', is_template=1, is_group=1)
template_task1 = create_task(subject='Task - 1', is_template=1, parent_task=template_parent_task1.name)
template_task2 = create_task(subject='Task - 2', is_template=1, parent_task=template_parent_task2.name)
template_task3 = create_task(subject='Task - 1', is_template=1, parent_task=template_parent_task3.name)
template_tasks = [template_parent_task1, template_task1, template_parent_task2, template_task2, template_parent_task3, template_task3]
project_template = make_project_template('Project template with common Task Subject', template_tasks)
project = get_project('Project with common Task Subject', project_template)
project_tasks = frappe.get_all('Task', {'project': project.name}, ['subject', 'parent_task', 'is_group'])
self.assertEqual(len(project_tasks), len(template_tasks))
for pt in project_tasks:
    if not pt.is_group:
        self.assertIsNotNone(pt.parent_task)
```

## Next Steps


---

*Source: test_project.py:184 | Complexity: Advanced | Last updated: 2026-02-04*