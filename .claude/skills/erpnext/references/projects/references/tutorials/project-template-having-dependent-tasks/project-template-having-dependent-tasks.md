# How To: Project Template Having Dependent Tasks

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test project template having dependent tasks

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

### Step 1: Assign project_name = 'Test Project with Template - Dependent Tasks'

```python
project_name = 'Test Project with Template - Dependent Tasks'
```

### Step 2: Call frappe.db.sql()

```python
frappe.db.sql(' delete from tabTask where project = %s  ', project_name)
```

### Step 3: Call frappe.delete_doc()

```python
frappe.delete_doc('Project', project_name)
```

### Step 4: Assign task1 = task_exists(...)

```python
task1 = task_exists('Test Template Task for Dependency')
```

### Step 5: Assign task2 = task_exists(...)

```python
task2 = task_exists('Test Template Task with Dependency')
```

### Step 6: Assign template = make_project_template(...)

```python
template = make_project_template('Test Project with Template - Dependent Tasks', [task1, task2])
```

### Step 7: Assign project = get_project(...)

```python
project = get_project(project_name, template)
```

### Step 8: Assign tasks = frappe.get_all(...)

```python
tasks = frappe.get_all('Task', ['subject', 'exp_end_date', 'depends_on_tasks', 'name'], dict(project=project.name), order_by='creation asc')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(tasks[1].subject, 'Test Template Task with Dependency')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(getdate(tasks[1].exp_end_date), calculate_end_date(project, 2, 2))
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(tasks[1].depends_on_tasks.find(tasks[0].name) >= 0)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(tasks[0].subject, 'Test Template Task for Dependency')
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(getdate(tasks[0].exp_end_date), calculate_end_date(project, 3, 1))
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(len(tasks), 2)
```

### Step 15: Assign task1 = create_task(...)

```python
task1 = create_task(subject='Test Template Task for Dependency', is_template=1, begin=3, duration=1)
```

### Step 16: Assign task2 = create_task(...)

```python
task2 = create_task(subject='Test Template Task with Dependency', depends_on=task1.name, is_template=1, begin=2, duration=2)
```


## Complete Example

```python
# Workflow
project_name = 'Test Project with Template - Dependent Tasks'
frappe.db.sql(' delete from tabTask where project = %s  ', project_name)
frappe.delete_doc('Project', project_name)
task1 = task_exists('Test Template Task for Dependency')
if not task1:
    task1 = create_task(subject='Test Template Task for Dependency', is_template=1, begin=3, duration=1)
task2 = task_exists('Test Template Task with Dependency')
if not task2:
    task2 = create_task(subject='Test Template Task with Dependency', depends_on=task1.name, is_template=1, begin=2, duration=2)
template = make_project_template('Test Project with Template - Dependent Tasks', [task1, task2])
project = get_project(project_name, template)
tasks = frappe.get_all('Task', ['subject', 'exp_end_date', 'depends_on_tasks', 'name'], dict(project=project.name), order_by='creation asc')
self.assertEqual(tasks[1].subject, 'Test Template Task with Dependency')
self.assertEqual(getdate(tasks[1].exp_end_date), calculate_end_date(project, 2, 2))
self.assertTrue(tasks[1].depends_on_tasks.find(tasks[0].name) >= 0)
self.assertEqual(tasks[0].subject, 'Test Template Task for Dependency')
self.assertEqual(getdate(tasks[0].exp_end_date), calculate_end_date(project, 3, 1))
self.assertEqual(len(tasks), 2)
```

## Next Steps


---

*Source: test_project.py:130 | Complexity: Advanced | Last updated: 2026-02-04*