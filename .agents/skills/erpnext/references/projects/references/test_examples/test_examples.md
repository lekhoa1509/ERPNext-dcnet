# Test Example Extraction Report

**Total Examples**: 44  
**High Value Examples** (confidence > 0.7): 44  
**Average Complexity**: 0.74  

## Examples by Category

- **instantiation**: 12
- **method_call**: 2
- **workflow**: 30

## Examples by Language

- **Python**: 44

## Extracted Examples

### test_project_total_costing_and_billing_amount

**Category**: workflow  
**Description**: Workflow: test project total costing and billing amount  
**Expected**: self.assertEqual(project.total_billable_amount, 8000)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.projects.doctype.timesheet.test_timesheet import make_timesheet
from erpnext.setup.doctype.employee.test_employee import make_employee
project_name = 'Test Project Costing'
employee = make_employee('employee@frappe.io')
project = make_project({'project_name': project_name})
timesheet = make_timesheet(employee=employee, is_billable=1, currency='USD', project=project.name, simulate=True, exchange_rate=80)
timesheet.reload()
project.reload()
self.assertEqual(project.total_costing_amount, 3200)
self.assertEqual(project.total_billable_amount, 8000)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/project/test_project.py:22*

### test_project_with_template_having_no_parent_and_depend_tasks

**Category**: workflow  
**Description**: Workflow: test project with template having no parent and depend tasks  
**Expected**: self.assertEqual(len(tasks), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
project_name = 'Test Project with Template - No Parent and Dependend Tasks'
frappe.db.sql(' delete from tabTask where project = %s ', project_name)
frappe.delete_doc('Project', project_name)
task1 = task_exists('Test Template Task with No Parent and Dependency')
if not task1:
    task1 = create_task(subject='Test Template Task with No Parent and Dependency', is_template=1, begin=5, duration=3, priority='High')
template = make_project_template('Test Project Template - No Parent and Dependend Tasks', [task1])
project = get_project(project_name, template)
tasks = frappe.get_all('Task', ['subject', 'exp_end_date', 'depends_on_tasks', 'priority'], dict(project=project.name), order_by='creation asc')
self.assertEqual(tasks[0].priority, 'High')
self.assertEqual(tasks[0].subject, 'Test Template Task with No Parent and Dependency')
self.assertEqual(getdate(tasks[0].exp_end_date), calculate_end_date(project, 5, 3))
self.assertEqual(len(tasks), 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/project/test_project.py:42*

### test_project_template_having_parent_child_tasks

**Category**: workflow  
**Description**: Workflow: test project template having parent child tasks  
**Expected**: self.assertEqual(len(tasks), 3)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
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

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/project/test_project.py:71*

### test_project_template_having_dependent_tasks

**Category**: workflow  
**Description**: Workflow: test project template having dependent tasks  
**Expected**: self.assertEqual(len(tasks), 2)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
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

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/project/test_project.py:130*

### test_project_with_template_tasks_having_common_name

**Category**: workflow  
**Description**: Workflow: test project with template tasks having common name  
**Expected**: self.assertEqual(len(project_tasks), len(template_tasks))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
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

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/project/test_project.py:184*

### test_project_having_no_tasks_complete

**Category**: workflow  
**Description**: Workflow: test project having no tasks complete  
**Expected**: self.assertEqual(project.status, 'Completed')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
project_name = 'Test Project - No Tasks Completion'
frappe.db.sql(' delete from tabTask where project = %s ', project_name)
frappe.delete_doc('Project', project_name)
project = frappe.get_doc({'doctype': 'Project', 'project_name': project_name, 'status': 'Open', 'expected_start_date': nowdate(), 'company': '_Test Company'}).insert()
tasks = frappe.get_all('Task', ['subject', 'exp_end_date', 'depends_on_tasks', 'name', 'parent_task'], dict(project=project.name), order_by='creation asc')
self.assertEqual(project.status, 'Open')
self.assertEqual(len(tasks), 0)
project.status = 'Completed'
project.save()
self.assertEqual(project.status, 'Completed')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/project/test_project.py:226*

### test_project_total_costing_and_billing_amount

**Category**: workflow  
**Description**: Workflow: test project total costing and billing amount  
**Expected**: self.assertEqual(project.total_billable_amount, 8000)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.projects.doctype.timesheet.test_timesheet import make_timesheet
from erpnext.setup.doctype.employee.test_employee import make_employee
project_name = 'Test Project Costing'
employee = make_employee('employee@frappe.io')
project = make_project({'project_name': project_name})
timesheet = make_timesheet(employee=employee, is_billable=1, currency='USD', project=project.name, simulate=True, exchange_rate=80)
timesheet.reload()
project.reload()
self.assertEqual(project.total_costing_amount, 3200)
self.assertEqual(project.total_billable_amount, 8000)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/project/test_project.py:22*

### test_project_with_template_having_no_parent_and_depend_tasks

**Category**: workflow  
**Description**: Workflow: test project with template having no parent and depend tasks  
**Expected**: self.assertEqual(len(tasks), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
project_name = 'Test Project with Template - No Parent and Dependend Tasks'
frappe.db.sql(' delete from tabTask where project = %s ', project_name)
frappe.delete_doc('Project', project_name)
task1 = task_exists('Test Template Task with No Parent and Dependency')
if not task1:
    task1 = create_task(subject='Test Template Task with No Parent and Dependency', is_template=1, begin=5, duration=3, priority='High')
template = make_project_template('Test Project Template - No Parent and Dependend Tasks', [task1])
project = get_project(project_name, template)
tasks = frappe.get_all('Task', ['subject', 'exp_end_date', 'depends_on_tasks', 'priority'], dict(project=project.name), order_by='creation asc')
self.assertEqual(tasks[0].priority, 'High')
self.assertEqual(tasks[0].subject, 'Test Template Task with No Parent and Dependency')
self.assertEqual(getdate(tasks[0].exp_end_date), calculate_end_date(project, 5, 3))
self.assertEqual(len(tasks), 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/project/test_project.py:42*

### test_project_template_having_parent_child_tasks

**Category**: workflow  
**Description**: Workflow: test project template having parent child tasks  
**Expected**: self.assertEqual(len(tasks), 3)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
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

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/project/test_project.py:71*

### test_project_template_having_dependent_tasks

**Category**: workflow  
**Description**: Workflow: test project template having dependent tasks  
**Expected**: self.assertEqual(len(tasks), 2)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
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

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/project/test_project.py:130*

### test_task_total_costing_and_billing_amount

**Category**: workflow  
**Description**: Workflow: test task total costing and billing amount  
**Expected**: self.assertEqual(task.total_billing_amount, 8000)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.projects.doctype.project.test_project import make_project
from erpnext.projects.doctype.timesheet.test_timesheet import make_timesheet
from erpnext.setup.doctype.employee.test_employee import make_employee
project_name = 'Test Project Costing'
employee = make_employee('employee@frappe.io')
project = make_project({'project_name': project_name})
task = create_task('_Test Task 1')
task.project = project.name
task.save()
timesheet = make_timesheet(employee=employee, is_billable=1, currency='USD', project=project.name, simulate=True, exchange_rate=80, task=task.name)
timesheet.reload()
project.reload()
task.reload()
self.assertEqual(task.total_costing_amount, 3200)
self.assertEqual(task.total_billing_amount, 8000)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/task/test_task.py:17*

### test_circular_reference

**Category**: workflow  
**Description**: Workflow: test circular reference  
**Expected**: self.assertRaises(CircularReferenceError, task1.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
task1 = create_task('_Test Task 1', add_days(nowdate(), -15), add_days(nowdate(), -10))
task2 = create_task('_Test Task 2', add_days(nowdate(), 11), add_days(nowdate(), 15), task1.name)
task3 = create_task('_Test Task 3', add_days(nowdate(), 11), add_days(nowdate(), 15), task2.name)
task1.reload()
task1.append('depends_on', {'task': task3.name})
self.assertRaises(CircularReferenceError, task1.save)
task1.set('depends_on', [])
task1.save()
task4 = create_task('_Test Task 4', nowdate(), add_days(nowdate(), 15), task1.name)
task3.append('depends_on', {'task': task4.name})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/task/test_task.py:43*

### test_reschedule_dependent_task

**Category**: workflow  
**Description**: Workflow: test reschedule dependent task  
**Expected**: self.assertEqual(getdate(frappe.db.get_value('Task', task3.name, 'exp_end_date')), getdate(add_days(nowdate(), 30)))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
project = frappe.get_value('Project', {'project_name': '_Test Project'})
task1 = create_task('_Test Task 1', nowdate(), add_days(nowdate(), 10))
task2 = create_task('_Test Task 2', add_days(nowdate(), 11), add_days(nowdate(), 15), task1.name)
task2.get('depends_on')[0].project = project
task2.save()
task3 = create_task('_Test Task 3', add_days(nowdate(), 11), add_days(nowdate(), 15), task2.name)
task3.get('depends_on')[0].project = project
task3.save()
task1.update({'exp_end_date': add_days(nowdate(), 20)})
task1.save()
self.assertEqual(getdate(frappe.db.get_value('Task', task2.name, 'exp_start_date')), getdate(add_days(nowdate(), 21)))
self.assertEqual(getdate(frappe.db.get_value('Task', task2.name, 'exp_end_date')), getdate(add_days(nowdate(), 25)))
self.assertEqual(getdate(frappe.db.get_value('Task', task3.name, 'exp_start_date')), getdate(add_days(nowdate(), 26)))
self.assertEqual(getdate(frappe.db.get_value('Task', task3.name, 'exp_end_date')), getdate(add_days(nowdate(), 30)))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/task/test_task.py:60*

### test_close_assignment

**Category**: workflow  
**Description**: Workflow: test close assignment  
**Expected**: self.assertEqual(todo.status, 'Closed')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
if not frappe.db.exists('Task', 'Test Close Assignment'):
    task = frappe.new_doc('Task')
    task.subject = 'Test Close Assignment'
    task.insert()

def assign():
    from frappe.desk.form import assign_to
    assign_to.add({'assign_to': ['test@example.com'], 'doctype': task.doctype, 'name': task.name, 'description': 'Close this task'})

def get_owner_and_status():
    return frappe.db.get_value('ToDo', filters={'reference_type': task.doctype, 'reference_name': task.name, 'description': 'Close this task'}, fieldname=('allocated_to', 'status'), as_dict=True)
assign()
todo = get_owner_and_status()
self.assertEqual(todo.allocated_to, 'test@example.com')
self.assertEqual(todo.status, 'Open')
task.load_from_db()
task.status = 'Completed'
task.save()
todo = get_owner_and_status()
self.assertEqual(todo.allocated_to, 'test@example.com')
self.assertEqual(todo.status, 'Closed')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/task/test_task.py:94*

### test_task_total_costing_and_billing_amount

**Category**: workflow  
**Description**: Workflow: test task total costing and billing amount  
**Expected**: self.assertEqual(task.total_billing_amount, 8000)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.projects.doctype.project.test_project import make_project
from erpnext.projects.doctype.timesheet.test_timesheet import make_timesheet
from erpnext.setup.doctype.employee.test_employee import make_employee
project_name = 'Test Project Costing'
employee = make_employee('employee@frappe.io')
project = make_project({'project_name': project_name})
task = create_task('_Test Task 1')
task.project = project.name
task.save()
timesheet = make_timesheet(employee=employee, is_billable=1, currency='USD', project=project.name, simulate=True, exchange_rate=80, task=task.name)
timesheet.reload()
project.reload()
task.reload()
self.assertEqual(task.total_costing_amount, 3200)
self.assertEqual(task.total_billing_amount, 8000)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/task/test_task.py:17*

### test_circular_reference

**Category**: workflow  
**Description**: Workflow: test circular reference  
**Expected**: self.assertRaises(CircularReferenceError, task1.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
task1 = create_task('_Test Task 1', add_days(nowdate(), -15), add_days(nowdate(), -10))
task2 = create_task('_Test Task 2', add_days(nowdate(), 11), add_days(nowdate(), 15), task1.name)
task3 = create_task('_Test Task 3', add_days(nowdate(), 11), add_days(nowdate(), 15), task2.name)
task1.reload()
task1.append('depends_on', {'task': task3.name})
self.assertRaises(CircularReferenceError, task1.save)
task1.set('depends_on', [])
task1.save()
task4 = create_task('_Test Task 4', nowdate(), add_days(nowdate(), 15), task1.name)
task3.append('depends_on', {'task': task4.name})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/task/test_task.py:43*

### test_reschedule_dependent_task

**Category**: workflow  
**Description**: Workflow: test reschedule dependent task  
**Expected**: self.assertEqual(getdate(frappe.db.get_value('Task', task3.name, 'exp_end_date')), getdate(add_days(nowdate(), 30)))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
project = frappe.get_value('Project', {'project_name': '_Test Project'})
task1 = create_task('_Test Task 1', nowdate(), add_days(nowdate(), 10))
task2 = create_task('_Test Task 2', add_days(nowdate(), 11), add_days(nowdate(), 15), task1.name)
task2.get('depends_on')[0].project = project
task2.save()
task3 = create_task('_Test Task 3', add_days(nowdate(), 11), add_days(nowdate(), 15), task2.name)
task3.get('depends_on')[0].project = project
task3.save()
task1.update({'exp_end_date': add_days(nowdate(), 20)})
task1.save()
self.assertEqual(getdate(frappe.db.get_value('Task', task2.name, 'exp_start_date')), getdate(add_days(nowdate(), 21)))
self.assertEqual(getdate(frappe.db.get_value('Task', task2.name, 'exp_end_date')), getdate(add_days(nowdate(), 25)))
self.assertEqual(getdate(frappe.db.get_value('Task', task3.name, 'exp_start_date')), getdate(add_days(nowdate(), 26)))
self.assertEqual(getdate(frappe.db.get_value('Task', task3.name, 'exp_end_date')), getdate(add_days(nowdate(), 30)))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/task/test_task.py:60*

### test_close_assignment

**Category**: workflow  
**Description**: Workflow: test close assignment  
**Expected**: self.assertEqual(todo.status, 'Closed')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
if not frappe.db.exists('Task', 'Test Close Assignment'):
    task = frappe.new_doc('Task')
    task.subject = 'Test Close Assignment'
    task.insert()

def assign():
    from frappe.desk.form import assign_to
    assign_to.add({'assign_to': ['test@example.com'], 'doctype': task.doctype, 'name': task.name, 'description': 'Close this task'})

def get_owner_and_status():
    return frappe.db.get_value('ToDo', filters={'reference_type': task.doctype, 'reference_name': task.name, 'description': 'Close this task'}, fieldname=('allocated_to', 'status'), as_dict=True)
assign()
todo = get_owner_and_status()
self.assertEqual(todo.allocated_to, 'test@example.com')
self.assertEqual(todo.status, 'Open')
task.load_from_db()
task.status = 'Completed'
task.save()
todo = get_owner_and_status()
self.assertEqual(todo.allocated_to, 'test@example.com')
self.assertEqual(todo.status, 'Closed')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/task/test_task.py:94*

### test_sales_invoice_from_timesheet

**Category**: workflow  
**Description**: Workflow: test sales invoice from timesheet  
**Expected**: self.assertEqual(item.rate, 50.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.delete('Timesheet')

emp = make_employee('test_employee_6@salary.com')
timesheet = make_timesheet(emp, simulate=True, is_billable=1)
sales_invoice = make_sales_invoice(timesheet.name, '_Test Item', '_Test Customer', currency='INR')
sales_invoice.due_date = nowdate()
sales_invoice.submit()
timesheet = frappe.get_doc('Timesheet', timesheet.name)
self.assertEqual(sales_invoice.total_billing_amount, 100)
self.assertEqual(timesheet.status, 'Billed')
self.assertEqual(sales_invoice.customer, '_Test Customer')
item = sales_invoice.items[0]
self.assertEqual(item.item_code, '_Test Item')
self.assertEqual(item.qty, 2.0)
self.assertEqual(item.rate, 50.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/timesheet/test_timesheet.py:104*

### test_timesheet_billing_based_on_project

**Category**: workflow  
**Description**: Workflow: test timesheet billing based on project  
**Expected**: self.assertEqual(ts.time_logs[0].sales_invoice, sales_invoice.name)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.delete('Timesheet')

emp = make_employee('test_employee_6@salary.com')
project = frappe.get_value('Project', {'project_name': '_Test Project'})
timesheet = make_timesheet(emp, simulate=True, is_billable=1, project=project, company='_Test Company')
sales_invoice = create_sales_invoice(do_not_save=True)
sales_invoice.project = project
sales_invoice.add_timesheet_data()
sales_invoice.submit()
ts = frappe.get_doc('Timesheet', timesheet.name)
self.assertEqual(ts.per_billed, 100)
self.assertEqual(ts.time_logs[0].sales_invoice, sales_invoice.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/timesheet/test_timesheet.py:122*

### test_timesheet_time_overlap

**Category**: workflow  
**Description**: Workflow: test timesheet time overlap  
**Expected**: self.assertRaises(frappe.ValidationError, timesheet.submit)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.delete('Timesheet')

emp = make_employee('test_employee_6@salary.com')
settings = frappe.get_single('Projects Settings')
initial_setting = settings.ignore_employee_time_overlap
settings.ignore_employee_time_overlap = 0
settings.save()
update_activity_type('_Test Activity Type')
timesheet = frappe.new_doc('Timesheet')
timesheet.employee = emp
timesheet.append('time_logs', {'billable': 1, 'activity_type': '_Test Activity Type', 'from_time': now_datetime(), 'to_time': now_datetime() + datetime.timedelta(hours=3), 'company': '_Test Company'})
timesheet.append('time_logs', {'billable': 1, 'activity_type': '_Test Activity Type', 'from_time': now_datetime(), 'to_time': now_datetime() + datetime.timedelta(hours=3), 'company': '_Test Company'})
self.assertRaises(frappe.ValidationError, timesheet.save)
settings.ignore_employee_time_overlap = 1
settings.save()
timesheet.save()
timesheet.submit()
settings.ignore_employee_time_overlap = 0
settings.save()
timesheet.append('time_logs', {'billable': 1, 'activity_type': '_Test Activity Type', 'from_time': now_datetime(), 'to_time': now_datetime() + datetime.timedelta(hours=3), 'company': '_Test Company'})
self.assertRaises(frappe.ValidationError, timesheet.submit)
settings.ignore_employee_time_overlap = initial_setting
settings.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/timesheet/test_timesheet.py:138*

### test_to_time

**Category**: workflow  
**Description**: Workflow: test to time  
**Expected**: self.assertEqual(to_time, add_to_date(from_time, hours=2, as_datetime=True))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.delete('Timesheet')

emp = make_employee('test_employee_6@salary.com')
from_time = now_datetime()
timesheet = frappe.new_doc('Timesheet')
timesheet.employee = emp
timesheet.append('time_logs', {'billable': 1, 'activity_type': '_Test Activity Type', 'from_time': from_time, 'hours': 2, 'company': '_Test Company'})
timesheet.save()
to_time = timesheet.time_logs[0].to_time
self.assertEqual(to_time, add_to_date(from_time, hours=2, as_datetime=True))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/timesheet/test_timesheet.py:223*

### test_per_billed_hours

**Category**: workflow  
**Description**: Workflow: If amounts are 0, per_billed should be calculated based on hours.  
**Expected**: self.assertEqual(ts.per_billed, 100)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.delete('Timesheet')

'If amounts are 0, per_billed should be calculated based on hours.'
ts = frappe.new_doc('Timesheet')
ts.total_billable_amount = 0
ts.total_billed_amount = 0
ts.total_billable_hours = 2
ts.total_billed_hours = 0.5
ts.calculate_percentage_billed()
self.assertEqual(ts.per_billed, 25)
ts.total_billed_hours = 2
ts.calculate_percentage_billed()
self.assertEqual(ts.per_billed, 100)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/timesheet/test_timesheet.py:244*

### test_per_billed_amount

**Category**: workflow  
**Description**: Workflow: If amounts are > 0, per_billed should be calculated based on amounts, regardless of hours.  
**Expected**: self.assertEqual(ts.per_billed, 100)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.delete('Timesheet')

'If amounts are > 0, per_billed should be calculated based on amounts, regardless of hours.'
ts = frappe.new_doc('Timesheet')
ts.total_billable_hours = 2
ts.total_billed_hours = 1
ts.total_billable_amount = 200
ts.total_billed_amount = 50
ts.calculate_percentage_billed()
self.assertEqual(ts.per_billed, 25)
ts.total_billed_hours = 3
ts.total_billable_amount = 200
ts.total_billed_amount = 200
ts.calculate_percentage_billed()
self.assertEqual(ts.per_billed, 100)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/timesheet/test_timesheet.py:259*

### test_partial_billing_and_return

**Category**: workflow  
**Description**: Workflow: Test Timesheet status transitions during partial billing, full billing,
sales return, and return cancellation.

Scenario:
1. Create a Timesheet with two billable time logs.
2. Create a Sales Invoice billing only one time log → Timesheet becomes Partially Billed.
3. Create another Sales Invoice billing the remaining time log → Timesheet becomes Billed.
4. Create a Sales Return against the second invoice → Timesheet reverts to Partially Billed.
5. Cancel the Sales Return → Timesheet returns to Billed status.

This test ensures Timesheet status is recalculated correctly
across billing and return lifecycle events.  
**Expected**: self.assertEqual(timesheet.status, 'Billed')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.delete('Timesheet')

'\n\t\tTest Timesheet status transitions during partial billing, full billing,\n\t\tsales return, and return cancellation.\n\n\t\tScenario:\n\t\t1. Create a Timesheet with two billable time logs.\n\t\t2. Create a Sales Invoice billing only one time log → Timesheet becomes Partially Billed.\n\t\t3. Create another Sales Invoice billing the remaining time log → Timesheet becomes Billed.\n\t\t4. Create a Sales Return against the second invoice → Timesheet reverts to Partially Billed.\n\t\t5. Cancel the Sales Return → Timesheet returns to Billed status.\n\n\t\tThis test ensures Timesheet status is recalculated correctly\n\t\tacross billing and return lifecycle events.\n\t\t'
emp = make_employee('test_employee_6@salary.com')
timesheet = make_timesheet(emp, simulate=True, is_billable=1, do_not_submit=True)
timesheet_detail = timesheet.append('time_logs', {})
timesheet_detail.is_billable = 1
timesheet_detail.activity_type = '_Test Activity Type'
timesheet_detail.from_time = timesheet.time_logs[0].to_time + datetime.timedelta(minutes=1)
timesheet_detail.hours = 2
timesheet_detail.to_time = timesheet_detail.from_time + datetime.timedelta(hours=timesheet_detail.hours)
timesheet.save().submit()
sales_invoice = make_sales_invoice(timesheet.name, '_Test Item', '_Test Customer', currency='INR')
sales_invoice.due_date = nowdate()
sales_invoice.timesheets.pop()
sales_invoice.submit()
timesheet_status = frappe.get_value('Timesheet', timesheet.name, 'status')
self.assertEqual(timesheet_status, 'Partially Billed')
sales_invoice2 = make_sales_invoice(timesheet.name, '_Test Item', '_Test Customer', currency='INR')
sales_invoice2.due_date = nowdate()
sales_invoice2.submit()
timesheet_status = frappe.get_value('Timesheet', timesheet.name, 'status')
self.assertEqual(timesheet_status, 'Billed')
sales_return = make_sales_return(sales_invoice2.name).submit()
timesheet_status = frappe.get_value('Timesheet', timesheet.name, 'status')
self.assertEqual(timesheet_status, 'Partially Billed')
sales_return.load_from_db()
sales_return.cancel()
timesheet.load_from_db()
self.assertEqual(timesheet.time_logs[1].sales_invoice, sales_invoice2.name)
self.assertEqual(timesheet.status, 'Billed')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/timesheet/test_timesheet.py:275*

### test_sales_invoice_from_timesheet

**Category**: workflow  
**Description**: Workflow: test sales invoice from timesheet  
**Expected**: self.assertEqual(item.rate, 50.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
emp = make_employee('test_employee_6@salary.com')
timesheet = make_timesheet(emp, simulate=True, is_billable=1)
sales_invoice = make_sales_invoice(timesheet.name, '_Test Item', '_Test Customer', currency='INR')
sales_invoice.due_date = nowdate()
sales_invoice.submit()
timesheet = frappe.get_doc('Timesheet', timesheet.name)
self.assertEqual(sales_invoice.total_billing_amount, 100)
self.assertEqual(timesheet.status, 'Billed')
self.assertEqual(sales_invoice.customer, '_Test Customer')
item = sales_invoice.items[0]
self.assertEqual(item.item_code, '_Test Item')
self.assertEqual(item.qty, 2.0)
self.assertEqual(item.rate, 50.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/timesheet/test_timesheet.py:104*

### test_timesheet_billing_based_on_project

**Category**: workflow  
**Description**: Workflow: test timesheet billing based on project  
**Expected**: self.assertEqual(ts.time_logs[0].sales_invoice, sales_invoice.name)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
emp = make_employee('test_employee_6@salary.com')
project = frappe.get_value('Project', {'project_name': '_Test Project'})
timesheet = make_timesheet(emp, simulate=True, is_billable=1, project=project, company='_Test Company')
sales_invoice = create_sales_invoice(do_not_save=True)
sales_invoice.project = project
sales_invoice.add_timesheet_data()
sales_invoice.submit()
ts = frappe.get_doc('Timesheet', timesheet.name)
self.assertEqual(ts.per_billed, 100)
self.assertEqual(ts.time_logs[0].sales_invoice, sales_invoice.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/timesheet/test_timesheet.py:122*

### test_timesheet_time_overlap

**Category**: workflow  
**Description**: Workflow: test timesheet time overlap  
**Expected**: self.assertRaises(frappe.ValidationError, timesheet.submit)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
emp = make_employee('test_employee_6@salary.com')
settings = frappe.get_single('Projects Settings')
initial_setting = settings.ignore_employee_time_overlap
settings.ignore_employee_time_overlap = 0
settings.save()
update_activity_type('_Test Activity Type')
timesheet = frappe.new_doc('Timesheet')
timesheet.employee = emp
timesheet.append('time_logs', {'billable': 1, 'activity_type': '_Test Activity Type', 'from_time': now_datetime(), 'to_time': now_datetime() + datetime.timedelta(hours=3), 'company': '_Test Company'})
timesheet.append('time_logs', {'billable': 1, 'activity_type': '_Test Activity Type', 'from_time': now_datetime(), 'to_time': now_datetime() + datetime.timedelta(hours=3), 'company': '_Test Company'})
self.assertRaises(frappe.ValidationError, timesheet.save)
settings.ignore_employee_time_overlap = 1
settings.save()
timesheet.save()
timesheet.submit()
settings.ignore_employee_time_overlap = 0
settings.save()
timesheet.append('time_logs', {'billable': 1, 'activity_type': '_Test Activity Type', 'from_time': now_datetime(), 'to_time': now_datetime() + datetime.timedelta(hours=3), 'company': '_Test Company'})
self.assertRaises(frappe.ValidationError, timesheet.submit)
settings.ignore_employee_time_overlap = initial_setting
settings.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/timesheet/test_timesheet.py:138*

### test_delayed_tasks_summary

**Category**: workflow  
**Description**: Workflow: test delayed tasks summary  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
task1 = create_task('_Test Task 98', add_days(nowdate(), -10), nowdate())
create_task('_Test Task 99', add_days(nowdate(), -10), add_days(nowdate(), -1))
task1.status = 'Completed'
task1.completed_on = add_days(nowdate(), -1)
task1.save()

filters = frappe._dict({'from_date': add_months(nowdate(), -1), 'to_date': nowdate(), 'priority': 'Low', 'status': 'Open'})
expected_data = [{'subject': '_Test Task 99', 'status': 'Open', 'priority': 'Low', 'delay': 1}, {'subject': '_Test Task 98', 'status': 'Completed', 'priority': 'Low', 'delay': -1}]
report = execute(filters)
data = next(filter(lambda x: x.subject == '_Test Task 99', report[1]))
for key in ['subject', 'status', 'priority', 'delay']:
    self.assertEqual(expected_data[0].get(key), data.get(key))
filters.status = 'Completed'
report = execute(filters)
data = next(filter(lambda x: x.subject == '_Test Task 98', report[1]))
for key in ['subject', 'status', 'priority', 'delay']:
    self.assertEqual(expected_data[1].get(key), data.get(key))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/report/delayed_tasks_summary/test_delayed_tasks_summary.py:19*

### test_delayed_tasks_summary

**Category**: workflow  
**Description**: Workflow: test delayed tasks summary  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
filters = frappe._dict({'from_date': add_months(nowdate(), -1), 'to_date': nowdate(), 'priority': 'Low', 'status': 'Open'})
expected_data = [{'subject': '_Test Task 99', 'status': 'Open', 'priority': 'Low', 'delay': 1}, {'subject': '_Test Task 98', 'status': 'Completed', 'priority': 'Low', 'delay': -1}]
report = execute(filters)
data = next(filter(lambda x: x.subject == '_Test Task 99', report[1]))
for key in ['subject', 'status', 'priority', 'delay']:
    self.assertEqual(expected_data[0].get(key), data.get(key))
filters.status = 'Completed'
report = execute(filters)
data = next(filter(lambda x: x.subject == '_Test Task 98', report[1]))
for key in ['subject', 'status', 'priority', 'delay']:
    self.assertEqual(expected_data[1].get(key), data.get(key))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/report/delayed_tasks_summary/test_delayed_tasks_summary.py:19*

### test_task_total_costing_and_billing_amount

**Category**: method_call  
**Description**: test task total costing and billing amount  
**Expected**: self.assertEqual(task.total_costing_amount, 3200)  
**Confidence**: 0.85  

```python
task.reload()
self.assertEqual(task.total_costing_amount, 3200)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/task/test_task.py:39*

### test_task_total_costing_and_billing_amount

**Category**: method_call  
**Description**: test task total costing and billing amount  
**Expected**: self.assertEqual(task.total_billing_amount, 8000)  
**Confidence**: 0.85  

```python
self.assertEqual(task.total_costing_amount, 3200)
self.assertEqual(task.total_billing_amount, 8000)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/task/test_task.py:40*

### test_duplication

**Category**: instantiation  
**Description**: Instantiate new_doc: test duplication  
**Expected**: self.assertRaises(DuplicationError, activity_cost2.insert)  
**Confidence**: 0.80  

```python
activity_cost1 = frappe.new_doc('Activity Cost')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/activity_cost/test_activity_cost.py:19*

### test_duplication

**Category**: instantiation  
**Description**: Instantiate copy_doc: test duplication  
**Expected**: self.assertRaises(DuplicationError, activity_cost2.insert)  
**Confidence**: 0.80  

```python
activity_cost2 = frappe.copy_doc(activity_cost1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/activity_cost/test_activity_cost.py:30*

### test_duplication

**Category**: instantiation  
**Description**: Instantiate new_doc: test duplication  
**Expected**: self.assertRaises(DuplicationError, activity_cost2.insert)  
**Confidence**: 0.80  

```python
activity_cost1 = frappe.new_doc('Activity Cost')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/activity_cost/test_activity_cost.py:19*

### test_duplication

**Category**: instantiation  
**Description**: Instantiate copy_doc: test duplication  
**Expected**: self.assertRaises(DuplicationError, activity_cost2.insert)  
**Confidence**: 0.80  

```python
activity_cost2 = frappe.copy_doc(activity_cost1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/doctype/activity_cost/test_activity_cost.py:30*

### test_delayed_tasks_summary

**Category**: instantiation  
**Description**: Instantiate _dict: test delayed tasks summary  
**Confidence**: 0.80  

```python
# Setup
task1 = create_task('_Test Task 98', add_days(nowdate(), -10), nowdate())
create_task('_Test Task 99', add_days(nowdate(), -10), add_days(nowdate(), -1))
task1.status = 'Completed'
task1.completed_on = add_days(nowdate(), -1)
task1.save()

filters = frappe._dict({'from_date': add_months(nowdate(), -1), 'to_date': nowdate(), 'priority': 'Low', 'status': 'Open'})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/report/delayed_tasks_summary/test_delayed_tasks_summary.py:20*

### test_delayed_tasks_summary

**Category**: instantiation  
**Description**: Instantiate execute: test delayed tasks summary  
**Confidence**: 0.80  

```python
# Setup
task1 = create_task('_Test Task 98', add_days(nowdate(), -10), nowdate())
create_task('_Test Task 99', add_days(nowdate(), -10), add_days(nowdate(), -1))
task1.status = 'Completed'
task1.completed_on = add_days(nowdate(), -1)
task1.save()

report = execute(filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/report/delayed_tasks_summary/test_delayed_tasks_summary.py:32*

### test_delayed_tasks_summary

**Category**: instantiation  
**Description**: Instantiate next: test delayed tasks summary  
**Confidence**: 0.80  

```python
# Setup
task1 = create_task('_Test Task 98', add_days(nowdate(), -10), nowdate())
create_task('_Test Task 99', add_days(nowdate(), -10), add_days(nowdate(), -1))
task1.status = 'Completed'
task1.completed_on = add_days(nowdate(), -1)
task1.save()

data = next(filter(lambda x: x.subject == '_Test Task 99', report[1]))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/report/delayed_tasks_summary/test_delayed_tasks_summary.py:33*

### test_delayed_tasks_summary

**Category**: instantiation  
**Description**: Instantiate execute: test delayed tasks summary  
**Confidence**: 0.80  

```python
# Setup
task1 = create_task('_Test Task 98', add_days(nowdate(), -10), nowdate())
create_task('_Test Task 99', add_days(nowdate(), -10), add_days(nowdate(), -1))
task1.status = 'Completed'
task1.completed_on = add_days(nowdate(), -1)
task1.save()

report = execute(filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/report/delayed_tasks_summary/test_delayed_tasks_summary.py:39*

### test_delayed_tasks_summary

**Category**: instantiation  
**Description**: Instantiate next: test delayed tasks summary  
**Confidence**: 0.80  

```python
# Setup
task1 = create_task('_Test Task 98', add_days(nowdate(), -10), nowdate())
create_task('_Test Task 99', add_days(nowdate(), -10), add_days(nowdate(), -1))
task1.status = 'Completed'
task1.completed_on = add_days(nowdate(), -1)
task1.save()

data = next(filter(lambda x: x.subject == '_Test Task 98', report[1]))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/report/delayed_tasks_summary/test_delayed_tasks_summary.py:40*

### test_delayed_tasks_summary

**Category**: instantiation  
**Description**: Instantiate _dict: test delayed tasks summary  
**Confidence**: 0.80  

```python
filters = frappe._dict({'from_date': add_months(nowdate(), -1), 'to_date': nowdate(), 'priority': 'Low', 'status': 'Open'})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/report/delayed_tasks_summary/test_delayed_tasks_summary.py:20*

### test_delayed_tasks_summary

**Category**: instantiation  
**Description**: Instantiate execute: test delayed tasks summary  
**Confidence**: 0.80  

```python
report = execute(filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/report/delayed_tasks_summary/test_delayed_tasks_summary.py:32*

### test_delayed_tasks_summary

**Category**: instantiation  
**Description**: Instantiate next: test delayed tasks summary  
**Confidence**: 0.80  

```python
data = next(filter(lambda x: x.subject == '_Test Task 99', report[1]))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/projects/report/delayed_tasks_summary/test_delayed_tasks_summary.py:33*

