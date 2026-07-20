# How To: Project Template Having Parent Child Tasks

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test project template having parent child tasks

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

### Step 1: Assign project_name = 'Test Project with Template - Tasks with Parent-Child Relation'

```python
project_name = 'Test Project with Template - Tasks with Parent-Child Relation'
```

### Step 2: Call frappe.db.sql()

```python
frappe.db.sql(' delete from tabTask where project = %s ', project_name)
```

### Step 3: Call frappe.delete_doc()

```python
frappe.delete_doc('Project', project_name)
```

### Step 4: Assign task1 = task_exists(...)

```python
task1 = task_exists('Test Template Task Parent')
```

### Step 5: Assign task2 = task_exists(...)

```python
task2 = task_exists('Test Template Task Child 1')
```

### Step 6: Assign task3 = task_exists(...)

```python
task3 = task_exists('Test Template Task Child 2')
```

### Step 7: Assign template = make_project_template(...)

```python
template = make_project_template('Test Project Template  - Tasks with Parent-Child Relation', [task1, task2, task3])
```

### Step 8: Assign project = get_project(...)

```python
project = get_project(project_name, template)
```

### Step 9: Assign tasks = frappe.get_all(...)

```python
tasks = frappe.get_all('Task', ['subject', 'exp_end_date', 'depends_on_tasks', 'name', 'parent_task'], dict(project=project.name), order_by='creation asc')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(tasks[0].subject, 'Test Template Task Parent')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(getdate(tasks[0].exp_end_date), calculate_end_date(project, 1, 10))
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(tasks[1].subject, 'Test Template Task Child 1')
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(getdate(tasks[1].exp_end_date), calculate_end_date(project, 1, 3))
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(tasks[1].parent_task, tasks[0].name)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(tasks[2].subject, 'Test Template Task Child 2')
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(getdate(tasks[2].exp_end_date), calculate_end_date(project, 2, 3))
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(tasks[2].parent_task, tasks[0].name)
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(len(tasks), 3)
```

### Step 19: Assign project_name = frappe.db.get_value(...)

```python
project_name = frappe.db.get_value('Project', {'project_name': project_name}, 'name')
```

### Step 20: Assign task1 = create_task(...)

```python
task1 = create_task(subject='Test Template Task Parent', is_group=1, is_template=1, begin=1, duration=10)
```

### Step 21: Assign task2 = create_task(...)

```python
task2 = create_task(subject='Test Template Task Child 1', parent_task=task1.name, is_template=1, begin=1, duration=3)
```

### Step 22: Assign task3 = create_task(...)

```python
task3 = create_task(subject='Test Template Task Child 2', parent_task=task1.name, is_template=1, begin=2, duration=3)
```


## Complete Example

```python
# Workflow
project_name = 'Test Project with Template - Tasks with Parent-Child Relation'
if frappe.db.get_value('Project', {'project_name': project_name}, 'name'):
    project_name = frappe.db.get_value('Project', {'project_name': project_name}, 'name')
frappe.db.sql(' delete from tabTask where project = %s ', project_name)
frappe.delete_doc('Project', project_name)
task1 = task_exists('Test Template Task Parent')
if not task1:
    task1 = create_task(subject='Test Template Task Parent', is_group=1, is_template=1, begin=1, duration=10)
task2 = task_exists('Test Template Task Child 1')
if not task2:
    task2 = create_task(subject='Test Template Task Child 1', parent_task=task1.name, is_template=1, begin=1, duration=3)
task3 = task_exists('Test Template Task Child 2')
if not task3:
    task3 = create_task(subject='Test Template Task Child 2', parent_task=task1.name, is_template=1, begin=2, duration=3)
template = make_project_template('Test Project Template  - Tasks with Parent-Child Relation', [task1, task2, task3])
project = get_project(project_name, template)
tasks = frappe.get_all('Task', ['subject', 'exp_end_date', 'depends_on_tasks', 'name', 'parent_task'], dict(project=project.name), order_by='creation asc')
self.assertEqual(tasks[0].subject, 'Test Template Task Parent')
self.assertEqual(getdate(tasks[0].exp_end_date), calculate_end_date(project, 1, 10))
self.assertEqual(tasks[1].subject, 'Test Template Task Child 1')
self.assertEqual(getdate(tasks[1].exp_end_date), calculate_end_date(project, 1, 3))
self.assertEqual(tasks[1].parent_task, tasks[0].name)
self.assertEqual(tasks[2].subject, 'Test Template Task Child 2')
self.assertEqual(getdate(tasks[2].exp_end_date), calculate_end_date(project, 2, 3))
self.assertEqual(tasks[2].parent_task, tasks[0].name)
self.assertEqual(len(tasks), 3)
```

## Next Steps


---

*Source: test_project.py:71 | Complexity: Advanced | Last updated: 2026-02-04*