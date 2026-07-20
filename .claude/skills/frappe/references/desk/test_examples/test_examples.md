# Test Example Extraction Report

**Total Examples**: 76  
**High Value Examples** (confidence > 0.7): 76  
**Average Complexity**: 0.59  

## Examples by Category

- **instantiation**: 8
- **method_call**: 32
- **workflow**: 36

## Examples by Language

- **Python**: 76

## Extracted Examples

### test_fetch_setup

**Category**: workflow  
**Description**: Workflow: test fetch setup  
**Expected**: self.assertEqual(todo.assigned_by_full_name, frappe.db.get_value('User', todo.assigned_by, 'full_name'))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.db.delete('ToDo')
todo_meta = frappe.get_meta('ToDo')
todo_meta.get('fields', dict(fieldname='assigned_by_full_name'))[0].fetch_from = ''
todo_meta.save()
frappe.clear_cache(doctype='ToDo')
todo = frappe.get_doc(doctype='ToDo', description='test todo', assigned_by='Administrator').insert()
self.assertFalse(todo.assigned_by_full_name)
todo_meta = frappe.get_meta('ToDo')
todo_meta.get('fields', dict(fieldname='assigned_by_full_name'))[0].fetch_from = 'assigned_by.full_name'
todo_meta.save()
todo.reload()
todo.save()
self.assertEqual(todo.assigned_by_full_name, frappe.db.get_value('User', todo.assigned_by, 'full_name'))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/todo/test_todo.py:30*

### test_doc_read_access

**Category**: workflow  
**Description**: Workflow: test doc read access  
**Expected**: self.assertFalse(todo1.has_permission('write'))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
todo1 = create_new_todo('Test1', 'testperm@example.com')
test_user = frappe.get_doc('User', 'test4@example.com')
todo2 = create_new_todo('Test2', 'test4@example.com')
frappe.set_user('test4@example.com')
todo3 = create_new_todo('Test3', 'test4@example.com')
self.assertFalse(todo1.has_permission('read'))
self.assertFalse(todo1.has_permission('write'))
self.assertTrue(todo2.has_permission('read'))
self.assertTrue(todo2.has_permission('write'))
self.assertTrue(todo3.has_permission('read'))
self.assertTrue(todo3.has_permission('write'))
frappe.set_user('Administrator')
test_user.add_roles('Website Manager')
add_permission('ToDo', 'Website Manager')
frappe.set_user('test4@example.com')
self.assertTrue(todo1.has_permission('read'))
self.assertFalse(todo1.has_permission('write'))
frappe.set_user('Administrator')
test_user.remove_roles('Website Manager')
reset_perms('ToDo')
clear_permissions_cache('ToDo')
frappe.db.rollback()
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/todo/test_todo.py:70*

### test_fetch_if_empty

**Category**: workflow  
**Description**: Workflow: test fetch if empty  
**Expected**: self.assertEqual(todo.assigned_by_full_name, frappe.db.get_value('User', todo.assigned_by, 'full_name'))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.db.delete('ToDo')
todo_meta = frappe.get_meta('ToDo')
field = todo_meta.get('fields', dict(fieldname='assigned_by_full_name'))[0]
field.fetch_from = 'assigned_by.full_name'
field.fetch_if_empty = 1
todo_meta.save()
frappe.clear_cache(doctype='ToDo')
todo = frappe.get_doc(doctype='ToDo', description='test todo', assigned_by='Administrator', assigned_by_full_name='Admin').insert()
self.assertEqual(todo.assigned_by_full_name, 'Admin')
todo.meta.get('fields', dict(fieldname='assigned_by_full_name'))[0].fetch_if_empty = 0
todo.meta.save()
todo.reload()
todo.save()
self.assertEqual(todo.assigned_by_full_name, frappe.db.get_value('User', todo.assigned_by, 'full_name'))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/todo/test_todo.py:111*

### test_fetch_setup

**Category**: workflow  
**Description**: Workflow: test fetch setup  
**Expected**: self.assertEqual(todo.assigned_by_full_name, frappe.db.get_value('User', todo.assigned_by, 'full_name'))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.db.delete('ToDo')
todo_meta = frappe.get_meta('ToDo')
todo_meta.get('fields', dict(fieldname='assigned_by_full_name'))[0].fetch_from = ''
todo_meta.save()
frappe.clear_cache(doctype='ToDo')
todo = frappe.get_doc(doctype='ToDo', description='test todo', assigned_by='Administrator').insert()
self.assertFalse(todo.assigned_by_full_name)
todo_meta = frappe.get_meta('ToDo')
todo_meta.get('fields', dict(fieldname='assigned_by_full_name'))[0].fetch_from = 'assigned_by.full_name'
todo_meta.save()
todo.reload()
todo.save()
self.assertEqual(todo.assigned_by_full_name, frappe.db.get_value('User', todo.assigned_by, 'full_name'))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/todo/test_todo.py:30*

### test_doc_read_access

**Category**: workflow  
**Description**: Workflow: test doc read access  
**Expected**: self.assertFalse(todo1.has_permission('write'))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
todo1 = create_new_todo('Test1', 'testperm@example.com')
test_user = frappe.get_doc('User', 'test4@example.com')
todo2 = create_new_todo('Test2', 'test4@example.com')
frappe.set_user('test4@example.com')
todo3 = create_new_todo('Test3', 'test4@example.com')
self.assertFalse(todo1.has_permission('read'))
self.assertFalse(todo1.has_permission('write'))
self.assertTrue(todo2.has_permission('read'))
self.assertTrue(todo2.has_permission('write'))
self.assertTrue(todo3.has_permission('read'))
self.assertTrue(todo3.has_permission('write'))
frappe.set_user('Administrator')
test_user.add_roles('Website Manager')
add_permission('ToDo', 'Website Manager')
frappe.set_user('test4@example.com')
self.assertTrue(todo1.has_permission('read'))
self.assertFalse(todo1.has_permission('write'))
frappe.set_user('Administrator')
test_user.remove_roles('Website Manager')
reset_perms('ToDo')
clear_permissions_cache('ToDo')
frappe.db.rollback()
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/todo/test_todo.py:70*

### test_fetch_if_empty

**Category**: workflow  
**Description**: Workflow: test fetch if empty  
**Expected**: self.assertEqual(todo.assigned_by_full_name, frappe.db.get_value('User', todo.assigned_by, 'full_name'))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.db.delete('ToDo')
todo_meta = frappe.get_meta('ToDo')
field = todo_meta.get('fields', dict(fieldname='assigned_by_full_name'))[0]
field.fetch_from = 'assigned_by.full_name'
field.fetch_if_empty = 1
todo_meta.save()
frappe.clear_cache(doctype='ToDo')
todo = frappe.get_doc(doctype='ToDo', description='test todo', assigned_by='Administrator', assigned_by_full_name='Admin').insert()
self.assertEqual(todo.assigned_by_full_name, 'Admin')
todo.meta.get('fields', dict(fieldname='assigned_by_full_name'))[0].fetch_if_empty = 0
todo.meta.save()
todo.reload()
todo.save()
self.assertEqual(todo.assigned_by_full_name, frappe.db.get_value('User', todo.assigned_by, 'full_name'))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/todo/test_todo.py:111*

### test_assign

**Category**: workflow  
**Description**: Workflow: test assign  
**Expected**: self.assertEqual(ev._assign, json.dumps(['test@example.com']))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.delete('Event')
make_test_objects('Event', reset=True)
self.test_user = 'test1@example.com'

from frappe.desk.form.assign_to import add
ev = frappe.get_doc(self.globalTestRecords['Event'][0]).insert()
add({'assign_to': ['test@example.com'], 'doctype': 'Event', 'name': ev.name, 'description': 'Test Assignment'})
ev = frappe.get_doc('Event', ev.name)
self.assertEqual(ev._assign, json.dumps(['test@example.com']))
add({'assign_to': [self.test_user], 'doctype': 'Event', 'name': ev.name, 'description': 'Test Assignment'})
ev = frappe.get_doc('Event', ev.name)
self.assertEqual(set(json.loads(ev._assign)), {'test@example.com', self.test_user})
todo = frappe.get_doc('ToDo', {'reference_type': ev.doctype, 'reference_name': ev.name, 'allocated_to': self.test_user})
todo.status = 'Cancelled'
todo.save()
ev = frappe.get_doc('Event', ev.name)
self.assertEqual(ev._assign, json.dumps(['test@example.com']))
ev.delete()
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/event/test_event.py:65*

### test_yearly_repeat

**Category**: workflow  
**Description**: Workflow: test yearly repeat  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.delete('Event')
make_test_objects('Event', reset=True)
self.test_user = 'test1@example.com'

ev = frappe.get_doc({'doctype': 'Event', 'subject': '_Test Event', 'starts_on': '2014-02-01', 'event_type': 'Public', 'repeat_this_event': 1, 'repeat_on': 'Yearly'}).insert()

def test_record_matched(e):
    return e.name == ev.name
applicable_dates = [(date(2014, 2, 1), date(2014, 2, 1)), (date(2015, 2, 1), date(2015, 2, 1)), (date(2016, 2, 1), date(2016, 2, 1))]
for start_date, end_date in applicable_dates:
    event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
    with self.subTest(start_date=start_date, end_date=end_date):
        self.assertTrue(find(event_list, test_record_matched), f'Event not found between {start_date} and {end_date}')
unapplicable_dates = [(date(2014, 1, 20), date(2014, 1, 20)), (date(2015, 1, 20), date(2015, 1, 20))]
for start_date, end_date in unapplicable_dates:
    event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
    with self.subTest(start_date=start_date, end_date=end_date):
        self.assertFalse(find(event_list, test_record_matched), f'Event found between {start_date} and {end_date}')
ev.starts_on = date(2016, 2, 29)
ev.save()
applicable_dates = [(date(2016, 2, 29), date(2016, 2, 29)), (date(2024, 2, 28), date(2024, 2, 29))]
for start_date, end_date in applicable_dates:
    event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
    with self.subTest(start_date=start_date, end_date=end_date):
        self.assertTrue(find(event_list, test_record_matched), f'Event not found between {start_date} and {end_date}')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/event/test_event.py:111*

### test_quaterly_repeat

**Category**: workflow  
**Description**: Workflow: test quaterly repeat  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.delete('Event')
make_test_objects('Event', reset=True)
self.test_user = 'test1@example.com'

ev = frappe.get_doc({'doctype': 'Event', 'subject': '_Test Event', 'starts_on': '2023-02-17', 'repeat_till': '2024-02-17', 'event_type': 'Public', 'repeat_this_event': 1, 'repeat_on': 'Quarterly'}).insert()

def test_record_matched(e):
    return e.name == ev.name
applicable_dates = [(date(2023, 2, 17), date(2023, 2, 17)), (date(2023, 5, 17), date(2023, 5, 17)), (date(2023, 8, 17), date(2023, 8, 17)), (date(2023, 11, 17), date(2023, 11, 17))]
for start_date, end_date in applicable_dates:
    event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
    with self.subTest(start_date=start_date, end_date=end_date):
        self.assertTrue(find(event_list, test_record_matched), f'Event not found between {start_date} and {end_date}')
unapplicable_dates = [(date(2022, 11, 17), date(2022, 11, 17)), (date(2024, 2, 17), date(2024, 2, 17)), (date(2023, 12, 17), date(2023, 12, 17)), (date(2023, 3, 17), date(2023, 3, 17))]
for start_date, end_date in unapplicable_dates:
    event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
    with self.subTest(start_date=start_date, end_date=end_date):
        self.assertFalse(find(event_list, test_record_matched), f'Event found between {start_date} and {end_date}')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/event/test_event.py:196*

### test_half_yearly_repeat

**Category**: workflow  
**Description**: Workflow: test half yearly repeat  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.delete('Event')
make_test_objects('Event', reset=True)
self.test_user = 'test1@example.com'

ev = frappe.get_doc({'doctype': 'Event', 'subject': '_Test Event', 'starts_on': '2023-02-17', 'repeat_till': '2024-02-17', 'event_type': 'Public', 'repeat_this_event': 1, 'repeat_on': 'Half Yearly'}).insert()

def test_record_matched(e):
    return e.name == ev.name
applicable_dates = [(date(2023, 2, 17), date(2023, 2, 17)), (date(2023, 8, 17), date(2023, 8, 17))]
for start_date, end_date in applicable_dates:
    event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
    with self.subTest(start_date=start_date, end_date=end_date):
        self.assertTrue(find(event_list, test_record_matched), f'Event not found between {start_date} and {end_date}')
unapplicable_dates = [(date(2022, 8, 17), date(2022, 8, 17)), (date(2024, 2, 17), date(2024, 2, 17)), (date(2023, 12, 17), date(2023, 12, 17)), (date(2023, 5, 17), date(2023, 5, 17))]
for start_date, end_date in unapplicable_dates:
    event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
    with self.subTest(start_date=start_date, end_date=end_date):
        self.assertFalse(find(event_list, test_record_matched), f'Event found between {start_date} and {end_date}')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/event/test_event.py:244*

### test_daily_repeat

**Category**: workflow  
**Description**: Workflow: test daily repeat  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.delete('Event')
make_test_objects('Event', reset=True)
self.test_user = 'test1@example.com'

ev = frappe.get_doc({'doctype': 'Event', 'subject': '_Test Event', 'starts_on': '2023-02-17', 'repeat_till': '2024-02-17', 'event_type': 'Public', 'repeat_this_event': 1, 'repeat_on': 'Daily'}).insert()

def test_record_matched(e):
    return e.name == ev.name
applicable_dates = [(date(2023, 2, 17), date(2023, 2, 17)), (date(2024, 1, 1), date(2024, 1, 1))]
for start_date, end_date in applicable_dates:
    event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
    with self.subTest(start_date=start_date, end_date=end_date):
        self.assertTrue(find(event_list, test_record_matched), f'Event not found between {start_date} and {end_date}')
unapplicable_dates = [(date(2024, 2, 17), date(2024, 2, 17)), (date(2022, 8, 17), date(2022, 8, 17)), (date(2024, 2, 18), date(2024, 2, 18))]
for start_date, end_date in unapplicable_dates:
    event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
    with self.subTest(start_date=start_date, end_date=end_date):
        self.assertFalse(find(event_list, test_record_matched), f'Event found between {start_date} and {end_date}')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/event/test_event.py:290*

### test_weekly_repeat

**Category**: workflow  
**Description**: Workflow: test weekly repeat  
**Expected**: self.assertEqual(len(event_list), 3)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.delete('Event')
make_test_objects('Event', reset=True)
self.test_user = 'test1@example.com'

ev = frappe.get_doc({'doctype': 'Event', 'subject': '_Test Event', 'starts_on': '2025-04-15 16:00:00', 'repeat_till': '2025-05-06 23:59:59', 'tuesday': 1, 'wednesday': 1, 'friday': 1, 'event_type': 'Public', 'repeat_this_event': 1, 'repeat_on': 'Weekly'}).insert()

def test_record_matched(e):
    return e.name == ev.name
applicable_dates = [(date(2025, 4, 15), date(2025, 4, 15)), (date(2025, 4, 22), date(2025, 4, 22)), (date(2025, 4, 29), date(2025, 4, 29)), (date(2025, 4, 30), date(2025, 4, 30)), (date(2025, 5, 2), date(2025, 5, 2))]
for start_date, end_date in applicable_dates:
    event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
    with self.subTest(start_date=start_date, end_date=end_date):
        self.assertTrue(find(event_list, test_record_matched), f'Event not found between {start_date} and {end_date}')
unapplicable_dates = [(date(2022, 8, 17), date(2022, 8, 17)), (date(2024, 2, 18), date(2024, 2, 18)), (date(2023, 5, 17), date(2023, 5, 17)), (date(2023, 5, 18), date(2023, 5, 18))]
for start_date, end_date in unapplicable_dates:
    event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
    with self.subTest(start_date=start_date, end_date=end_date):
        self.assertFalse(find(event_list, test_record_matched), f'Event found between {start_date} and {end_date}')
event_list = get_events(date(2025, 4, 29), date(2025, 5, 2), 'Administrator', for_reminder=True)
self.assertEqual(len(event_list), 3)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/event/test_event.py:333*

### test_assign

**Category**: workflow  
**Description**: Workflow: test assign  
**Expected**: self.assertEqual(ev._assign, json.dumps(['test@example.com']))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from frappe.desk.form.assign_to import add
ev = frappe.get_doc(self.globalTestRecords['Event'][0]).insert()
add({'assign_to': ['test@example.com'], 'doctype': 'Event', 'name': ev.name, 'description': 'Test Assignment'})
ev = frappe.get_doc('Event', ev.name)
self.assertEqual(ev._assign, json.dumps(['test@example.com']))
add({'assign_to': [self.test_user], 'doctype': 'Event', 'name': ev.name, 'description': 'Test Assignment'})
ev = frappe.get_doc('Event', ev.name)
self.assertEqual(set(json.loads(ev._assign)), {'test@example.com', self.test_user})
todo = frappe.get_doc('ToDo', {'reference_type': ev.doctype, 'reference_name': ev.name, 'allocated_to': self.test_user})
todo.status = 'Cancelled'
todo.save()
ev = frappe.get_doc('Event', ev.name)
self.assertEqual(ev._assign, json.dumps(['test@example.com']))
ev.delete()
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/event/test_event.py:65*

### test_yearly_repeat

**Category**: workflow  
**Description**: Workflow: test yearly repeat  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
ev = frappe.get_doc({'doctype': 'Event', 'subject': '_Test Event', 'starts_on': '2014-02-01', 'event_type': 'Public', 'repeat_this_event': 1, 'repeat_on': 'Yearly'}).insert()

def test_record_matched(e):
    return e.name == ev.name
applicable_dates = [(date(2014, 2, 1), date(2014, 2, 1)), (date(2015, 2, 1), date(2015, 2, 1)), (date(2016, 2, 1), date(2016, 2, 1))]
for start_date, end_date in applicable_dates:
    event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
    with self.subTest(start_date=start_date, end_date=end_date):
        self.assertTrue(find(event_list, test_record_matched), f'Event not found between {start_date} and {end_date}')
unapplicable_dates = [(date(2014, 1, 20), date(2014, 1, 20)), (date(2015, 1, 20), date(2015, 1, 20))]
for start_date, end_date in unapplicable_dates:
    event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
    with self.subTest(start_date=start_date, end_date=end_date):
        self.assertFalse(find(event_list, test_record_matched), f'Event found between {start_date} and {end_date}')
ev.starts_on = date(2016, 2, 29)
ev.save()
applicable_dates = [(date(2016, 2, 29), date(2016, 2, 29)), (date(2024, 2, 28), date(2024, 2, 29))]
for start_date, end_date in applicable_dates:
    event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
    with self.subTest(start_date=start_date, end_date=end_date):
        self.assertTrue(find(event_list, test_record_matched), f'Event not found between {start_date} and {end_date}')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/event/test_event.py:111*

### test_quaterly_repeat

**Category**: workflow  
**Description**: Workflow: test quaterly repeat  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
ev = frappe.get_doc({'doctype': 'Event', 'subject': '_Test Event', 'starts_on': '2023-02-17', 'repeat_till': '2024-02-17', 'event_type': 'Public', 'repeat_this_event': 1, 'repeat_on': 'Quarterly'}).insert()

def test_record_matched(e):
    return e.name == ev.name
applicable_dates = [(date(2023, 2, 17), date(2023, 2, 17)), (date(2023, 5, 17), date(2023, 5, 17)), (date(2023, 8, 17), date(2023, 8, 17)), (date(2023, 11, 17), date(2023, 11, 17))]
for start_date, end_date in applicable_dates:
    event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
    with self.subTest(start_date=start_date, end_date=end_date):
        self.assertTrue(find(event_list, test_record_matched), f'Event not found between {start_date} and {end_date}')
unapplicable_dates = [(date(2022, 11, 17), date(2022, 11, 17)), (date(2024, 2, 17), date(2024, 2, 17)), (date(2023, 12, 17), date(2023, 12, 17)), (date(2023, 3, 17), date(2023, 3, 17))]
for start_date, end_date in unapplicable_dates:
    event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
    with self.subTest(start_date=start_date, end_date=end_date):
        self.assertFalse(find(event_list, test_record_matched), f'Event found between {start_date} and {end_date}')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/event/test_event.py:196*

### test_half_yearly_repeat

**Category**: workflow  
**Description**: Workflow: test half yearly repeat  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
ev = frappe.get_doc({'doctype': 'Event', 'subject': '_Test Event', 'starts_on': '2023-02-17', 'repeat_till': '2024-02-17', 'event_type': 'Public', 'repeat_this_event': 1, 'repeat_on': 'Half Yearly'}).insert()

def test_record_matched(e):
    return e.name == ev.name
applicable_dates = [(date(2023, 2, 17), date(2023, 2, 17)), (date(2023, 8, 17), date(2023, 8, 17))]
for start_date, end_date in applicable_dates:
    event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
    with self.subTest(start_date=start_date, end_date=end_date):
        self.assertTrue(find(event_list, test_record_matched), f'Event not found between {start_date} and {end_date}')
unapplicable_dates = [(date(2022, 8, 17), date(2022, 8, 17)), (date(2024, 2, 17), date(2024, 2, 17)), (date(2023, 12, 17), date(2023, 12, 17)), (date(2023, 5, 17), date(2023, 5, 17))]
for start_date, end_date in unapplicable_dates:
    event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
    with self.subTest(start_date=start_date, end_date=end_date):
        self.assertFalse(find(event_list, test_record_matched), f'Event found between {start_date} and {end_date}')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/event/test_event.py:244*

### test_share

**Category**: workflow  
**Description**: Workflow: test share  
**Expected**: self.assertTrue(content in email.message)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
todo = get_todo()
user = get_user()
frappe.share.add('ToDo', todo.name, user, notify=1)
log_type = frappe.db.get_value('Notification Log', {'document_type': 'ToDo', 'document_name': todo.name}, 'type')
self.assertEqual(log_type, 'Share')
email = get_last_email_queue()
content = f'Subject: {frappe.utils.get_fullname(frappe.session.user)} shared a document ToDo'
self.assertTrue(content in email.message)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/notification_log/test_notification_log.py:22*

### test_share

**Category**: workflow  
**Description**: Workflow: test share  
**Expected**: self.assertTrue(content in email.message)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
todo = get_todo()
user = get_user()
frappe.share.add('ToDo', todo.name, user, notify=1)
log_type = frappe.db.get_value('Notification Log', {'document_type': 'ToDo', 'document_name': todo.name}, 'type')
self.assertEqual(log_type, 'Share')
email = get_last_email_queue()
content = f'Subject: {frappe.utils.get_fullname(frappe.session.user)} shared a document ToDo'
self.assertTrue(content in email.message)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/notification_log/test_notification_log.py:22*

### test_system_console_sql

**Category**: workflow  
**Description**: Workflow: test system console sql  
**Expected**: self.assertIn('PermissionError', system_console.output)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
system_console = frappe.get_doc('System Console')
system_console.type = 'SQL'
system_console.console = "select 'test'"
system_console.run()
self.assertIn('test', system_console.output)
system_console.console = "update `tabDocType` set is_virtual = 1 where name = 'xyz'"
system_console.run()
self.assertIn('PermissionError', system_console.output)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/system_console/test_system_console.py:25*

### test_system_console_sql

**Category**: workflow  
**Description**: Workflow: test system console sql  
**Expected**: self.assertIn('PermissionError', system_console.output)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
system_console = frappe.get_doc('System Console')
system_console.type = 'SQL'
system_console.console = "select 'test'"
system_console.run()
self.assertIn('test', system_console.output)
system_console.console = "update `tabDocType` set is_virtual = 1 where name = 'xyz'"
system_console.run()
self.assertIn('PermissionError', system_console.output)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/system_console/test_system_console.py:25*

### test_bulk_submit_in_background

**Category**: workflow  
**Description**: Workflow: test bulk submit in background  
**Expected**: self.wait_for_assertion(lambda: check_docstatus(submitted, 2))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
unsubmitted = frappe.get_all(self.doctype, {'docstatus': 0}, limit=5, pluck='name')
failed = submit_cancel_or_update_docs(self.doctype, unsubmitted, action='submit')
self.assertEqual(failed, [])

def check_docstatus(docs, status):
    frappe.db.rollback()
    matching_docs = frappe.get_all(self.doctype, {'docstatus': status, 'name': ('in', docs)}, pluck='name')
    return set(matching_docs) == set(docs)
unsubmitted = frappe.get_all(self.doctype, {'docstatus': 0}, limit=20, pluck='name')
submit_cancel_or_update_docs(self.doctype, unsubmitted, action='submit')
self.wait_for_assertion(lambda: check_docstatus(unsubmitted, 1))
submitted = frappe.get_all(self.doctype, {'docstatus': 1}, limit=20, pluck='name')
submit_cancel_or_update_docs(self.doctype, submitted, action='cancel')
self.wait_for_assertion(lambda: check_docstatus(submitted, 2))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/bulk_update/test_bulk_update.py:30*

### test_bulk_update_parent_fields

**Category**: workflow  
**Description**: Workflow: test bulk update parent fields  
**Expected**: self.wait_for_assertion(lambda: check_field_values(docnames_bg, '_Test Background'))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
docnames = frappe.get_all(self.doctype, {'docstatus': 0}, limit=5, pluck='name')
failed = submit_cancel_or_update_docs(self.doctype, docnames, action='update', data={'some_fieldname': '_Test Sync'})
self.assertEqual(failed, [])

def check_field_values(docs, expected):
    frappe.db.rollback()
    values = frappe.get_all(self.doctype, {'name': ['in', docs]}, ['name', 'some_fieldname'])
    return all((v.some_fieldname == expected for v in values))
docnames_bg = frappe.get_all(self.doctype, {'docstatus': 0}, limit=20, pluck='name')
submit_cancel_or_update_docs(self.doctype, docnames_bg, action='update', data={'some_fieldname': '_Test Background'})
self.wait_for_assertion(lambda: check_field_values(docnames_bg, '_Test Background'))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/bulk_update/test_bulk_update.py:51*

### test_bulk_update_child_fields

**Category**: workflow  
**Description**: Workflow: test bulk update child fields  
**Expected**: self.wait_for_assertion(lambda: check_child_field(docnames_bg, '_Test Child Updated'))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
doctype_doc = frappe.get_doc('DocType', self.doctype)
doctype_doc.append('fields', {'fieldname': 'child_table', 'fieldtype': 'Table', 'options': self.child_doctype})
doctype_doc.save()
frappe.db.commit()
existing_docs = frappe.get_all(self.doctype, {'docstatus': 0}, pluck='name')
for docname in existing_docs:
    doc = frappe.get_doc(self.doctype, docname)
    doc.append('child_table', {'some_fieldname': '_Test Child Value'})
    doc.save()
frappe.db.commit()
update_data = {'child_table_updates': {self.child_doctype: {'some_fieldname': '_Test Child Updated'}}}

def check_child_field(docs, expected):
    frappe.db.rollback()
    for docname in docs:
        doc = frappe.get_doc(self.doctype, docname)
        if not doc.child_table or doc.child_table[0].some_fieldname != expected:
            return False
    return True
docnames = frappe.get_all(self.doctype, {'docstatus': 0}, limit=5, pluck='name')
failed = submit_cancel_or_update_docs(self.doctype, docnames, action='update', data=update_data)
self.assertEqual(failed, [])
docnames_bg = frappe.get_all(self.doctype, {'docstatus': 0}, limit=20, pluck='name')
submit_cancel_or_update_docs(self.doctype, docnames_bg, action='update', data=update_data)
self.wait_for_assertion(lambda: check_child_field(docnames_bg, '_Test Child Updated'))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/bulk_update/test_bulk_update.py:70*

### test_bulk_submit_in_background

**Category**: workflow  
**Description**: Workflow: test bulk submit in background  
**Expected**: self.wait_for_assertion(lambda: check_docstatus(submitted, 2))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
unsubmitted = frappe.get_all(self.doctype, {'docstatus': 0}, limit=5, pluck='name')
failed = submit_cancel_or_update_docs(self.doctype, unsubmitted, action='submit')
self.assertEqual(failed, [])

def check_docstatus(docs, status):
    frappe.db.rollback()
    matching_docs = frappe.get_all(self.doctype, {'docstatus': status, 'name': ('in', docs)}, pluck='name')
    return set(matching_docs) == set(docs)
unsubmitted = frappe.get_all(self.doctype, {'docstatus': 0}, limit=20, pluck='name')
submit_cancel_or_update_docs(self.doctype, unsubmitted, action='submit')
self.wait_for_assertion(lambda: check_docstatus(unsubmitted, 1))
submitted = frappe.get_all(self.doctype, {'docstatus': 1}, limit=20, pluck='name')
submit_cancel_or_update_docs(self.doctype, submitted, action='cancel')
self.wait_for_assertion(lambda: check_docstatus(submitted, 2))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/bulk_update/test_bulk_update.py:30*

### test_bulk_update_parent_fields

**Category**: workflow  
**Description**: Workflow: test bulk update parent fields  
**Expected**: self.wait_for_assertion(lambda: check_field_values(docnames_bg, '_Test Background'))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
docnames = frappe.get_all(self.doctype, {'docstatus': 0}, limit=5, pluck='name')
failed = submit_cancel_or_update_docs(self.doctype, docnames, action='update', data={'some_fieldname': '_Test Sync'})
self.assertEqual(failed, [])

def check_field_values(docs, expected):
    frappe.db.rollback()
    values = frappe.get_all(self.doctype, {'name': ['in', docs]}, ['name', 'some_fieldname'])
    return all((v.some_fieldname == expected for v in values))
docnames_bg = frappe.get_all(self.doctype, {'docstatus': 0}, limit=20, pluck='name')
submit_cancel_or_update_docs(self.doctype, docnames_bg, action='update', data={'some_fieldname': '_Test Background'})
self.wait_for_assertion(lambda: check_field_values(docnames_bg, '_Test Background'))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/bulk_update/test_bulk_update.py:51*

### test_bulk_update_child_fields

**Category**: workflow  
**Description**: Workflow: test bulk update child fields  
**Expected**: self.wait_for_assertion(lambda: check_child_field(docnames_bg, '_Test Child Updated'))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
doctype_doc = frappe.get_doc('DocType', self.doctype)
doctype_doc.append('fields', {'fieldname': 'child_table', 'fieldtype': 'Table', 'options': self.child_doctype})
doctype_doc.save()
frappe.db.commit()
existing_docs = frappe.get_all(self.doctype, {'docstatus': 0}, pluck='name')
for docname in existing_docs:
    doc = frappe.get_doc(self.doctype, docname)
    doc.append('child_table', {'some_fieldname': '_Test Child Value'})
    doc.save()
frappe.db.commit()
update_data = {'child_table_updates': {self.child_doctype: {'some_fieldname': '_Test Child Updated'}}}

def check_child_field(docs, expected):
    frappe.db.rollback()
    for docname in docs:
        doc = frappe.get_doc(self.doctype, docname)
        if not doc.child_table or doc.child_table[0].some_fieldname != expected:
            return False
    return True
docnames = frappe.get_all(self.doctype, {'docstatus': 0}, limit=5, pluck='name')
failed = submit_cancel_or_update_docs(self.doctype, docnames, action='update', data=update_data)
self.assertEqual(failed, [])
docnames_bg = frappe.get_all(self.doctype, {'docstatus': 0}, limit=20, pluck='name')
submit_cancel_or_update_docs(self.doctype, docnames_bg, action='update', data=update_data)
self.wait_for_assertion(lambda: check_child_field(docnames_bg, '_Test Child Updated'))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/bulk_update/test_bulk_update.py:70*

### test_dashboard_chart

**Category**: workflow  
**Description**: Workflow: test dashboard chart  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
doc = new_doctype(fields=[{'fieldname': 'title', 'fieldtype': 'Text', 'label': 'Title', 'reqd': 1}, {'fieldname': 'number', 'fieldtype': 'Int', 'label': 'Number', 'reqd': 1}, {'fieldname': 'date', 'fieldtype': 'Date', 'label': 'Date', 'reqd': 1}])
doc.insert()
self.doctype_name = doc.name

if frappe.db.exists('Dashboard Chart', 'Test Dashboard Chart'):
    frappe.delete_doc('Dashboard Chart', 'Test Dashboard Chart')
frappe.get_doc(doctype='Dashboard Chart', chart_name='Test Dashboard Chart', chart_type='Count', document_type='DocType', based_on='creation', timespan='Last Year', time_interval='Monthly', filters_json='{}', timeseries=1).insert()
cur_date = datetime.now() - relativedelta(years=1)
result = get(chart_name='Test Dashboard Chart', refresh=1)
for idx in range(13):
    month = get_last_day(cur_date)
    month = formatdate(month.strftime('%Y-%m-%d'))
    self.assertEqual(result.get('labels')[idx], get_period(month))
    cur_date += relativedelta(months=1)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/dashboard_chart/test_dashboard_chart.py:59*

### test_empty_dashboard_chart

**Category**: workflow  
**Description**: Workflow: test empty dashboard chart  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
doc = new_doctype(fields=[{'fieldname': 'title', 'fieldtype': 'Text', 'label': 'Title', 'reqd': 1}, {'fieldname': 'number', 'fieldtype': 'Int', 'label': 'Number', 'reqd': 1}, {'fieldname': 'date', 'fieldtype': 'Date', 'label': 'Date', 'reqd': 1}])
doc.insert()
self.doctype_name = doc.name

if frappe.db.exists('Dashboard Chart', 'Test Empty Dashboard Chart'):
    frappe.delete_doc('Dashboard Chart', 'Test Empty Dashboard Chart')
frappe.db.delete('Error Log')
frappe.get_doc(doctype='Dashboard Chart', chart_name='Test Empty Dashboard Chart', chart_type='Count', document_type='Error Log', based_on='creation', timespan='Last Year', time_interval='Monthly', filters_json='[]', timeseries=1).insert()
cur_date = datetime.now() - relativedelta(years=1)
result = get(chart_name='Test Empty Dashboard Chart', refresh=1)
for idx in range(13):
    month = get_last_day(cur_date)
    month = formatdate(month.strftime('%Y-%m-%d'))
    self.assertEqual(result.get('labels')[idx], get_period(month))
    cur_date += relativedelta(months=1)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/dashboard_chart/test_dashboard_chart.py:85*

### test_chart_wih_one_value

**Category**: workflow  
**Description**: Workflow: test chart wih one value  
**Expected**: self.assertEqual(result.get('datasets')[0].get('values')[2], 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
doc = new_doctype(fields=[{'fieldname': 'title', 'fieldtype': 'Text', 'label': 'Title', 'reqd': 1}, {'fieldname': 'number', 'fieldtype': 'Int', 'label': 'Number', 'reqd': 1}, {'fieldname': 'date', 'fieldtype': 'Date', 'label': 'Date', 'reqd': 1}])
doc.insert()
self.doctype_name = doc.name

if frappe.db.exists('Dashboard Chart', 'Test Empty Dashboard Chart 2'):
    frappe.delete_doc('Dashboard Chart', 'Test Empty Dashboard Chart 2')
frappe.db.delete('Error Log')
frappe.get_doc(doctype='Error Log', creation='2018-06-01 00:00:00').insert()
frappe.get_doc(doctype='Dashboard Chart', chart_name='Test Empty Dashboard Chart 2', chart_type='Count', document_type='Error Log', based_on='creation', timespan='Last Year', time_interval='Monthly', filters_json='[]', timeseries=1).insert()
cur_date = datetime.now() - relativedelta(years=1)
result = get(chart_name='Test Empty Dashboard Chart 2', refresh=1)
for idx in range(13):
    month = get_last_day(cur_date)
    month = formatdate(month.strftime('%Y-%m-%d'))
    self.assertEqual(result.get('labels')[idx], get_period(month))
    cur_date += relativedelta(months=1)
self.assertEqual(result.get('datasets')[0].get('values')[2], 0)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/dashboard_chart/test_dashboard_chart.py:113*

### test_dashboard_chart

**Category**: workflow  
**Description**: Workflow: test dashboard chart  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
if frappe.db.exists('Dashboard Chart', 'Test Dashboard Chart'):
    frappe.delete_doc('Dashboard Chart', 'Test Dashboard Chart')
frappe.get_doc(doctype='Dashboard Chart', chart_name='Test Dashboard Chart', chart_type='Count', document_type='DocType', based_on='creation', timespan='Last Year', time_interval='Monthly', filters_json='{}', timeseries=1).insert()
cur_date = datetime.now() - relativedelta(years=1)
result = get(chart_name='Test Dashboard Chart', refresh=1)
for idx in range(13):
    month = get_last_day(cur_date)
    month = formatdate(month.strftime('%Y-%m-%d'))
    self.assertEqual(result.get('labels')[idx], get_period(month))
    cur_date += relativedelta(months=1)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/dashboard_chart/test_dashboard_chart.py:59*

### test_empty_dashboard_chart

**Category**: workflow  
**Description**: Workflow: test empty dashboard chart  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
if frappe.db.exists('Dashboard Chart', 'Test Empty Dashboard Chart'):
    frappe.delete_doc('Dashboard Chart', 'Test Empty Dashboard Chart')
frappe.db.delete('Error Log')
frappe.get_doc(doctype='Dashboard Chart', chart_name='Test Empty Dashboard Chart', chart_type='Count', document_type='Error Log', based_on='creation', timespan='Last Year', time_interval='Monthly', filters_json='[]', timeseries=1).insert()
cur_date = datetime.now() - relativedelta(years=1)
result = get(chart_name='Test Empty Dashboard Chart', refresh=1)
for idx in range(13):
    month = get_last_day(cur_date)
    month = formatdate(month.strftime('%Y-%m-%d'))
    self.assertEqual(result.get('labels')[idx], get_period(month))
    cur_date += relativedelta(months=1)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/dashboard_chart/test_dashboard_chart.py:85*

### test_chart_wih_one_value

**Category**: workflow  
**Description**: Workflow: test chart wih one value  
**Expected**: self.assertEqual(result.get('datasets')[0].get('values')[2], 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
if frappe.db.exists('Dashboard Chart', 'Test Empty Dashboard Chart 2'):
    frappe.delete_doc('Dashboard Chart', 'Test Empty Dashboard Chart 2')
frappe.db.delete('Error Log')
frappe.get_doc(doctype='Error Log', creation='2018-06-01 00:00:00').insert()
frappe.get_doc(doctype='Dashboard Chart', chart_name='Test Empty Dashboard Chart 2', chart_type='Count', document_type='Error Log', based_on='creation', timespan='Last Year', time_interval='Monthly', filters_json='[]', timeseries=1).insert()
cur_date = datetime.now() - relativedelta(years=1)
result = get(chart_name='Test Empty Dashboard Chart 2', refresh=1)
for idx in range(13):
    month = get_last_day(cur_date)
    month = formatdate(month.strftime('%Y-%m-%d'))
    self.assertEqual(result.get('labels')[idx], get_period(month))
    cur_date += relativedelta(months=1)
self.assertEqual(result.get('datasets')[0].get('values')[2], 0)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/dashboard_chart/test_dashboard_chart.py:113*

### test_version

**Category**: workflow  
**Description**: Workflow: test version  
**Expected**: self.assertTrue(('content', 'test note content', '1'), data['changed'])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
note = self.insert_note()
note.title = 'test note 1'
note.content = '1'
note.save(ignore_version=False)
version = frappe.get_doc('Version', dict(docname=note.name))
data = version.get_data()
self.assertTrue(('title', 'test note', 'test note 1'), data['changed'])
self.assertTrue(('content', 'test note content', '1'), data['changed'])
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/note/test_note.py:16*

### test_rows

**Category**: workflow  
**Description**: Workflow: test rows  
**Expected**: self.assertEqual(len(data.get('removed')), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
note = self.insert_note()
note.append('seen_by', {'user': 'Administrator'})
note.save(ignore_version=False)
version = frappe.get_doc('Version', dict(docname=note.name))
data = version.get_data()
self.assertEqual(len(data.get('added')), 1)
self.assertEqual(len(data.get('removed')), 0)
self.assertEqual(len(data.get('changed')), 0)
for row in data.get('added'):
    self.assertEqual(row[0], 'seen_by')
    self.assertEqual(row[1]['user'], 'Administrator')
note.seen_by[0].user = 'Guest'
note.save(ignore_version=False)
version = frappe.get_doc('Version', dict(docname=note.name))
data = version.get_data()
self.assertEqual(len(data.get('row_changed')), 1)
for row in data.get('row_changed'):
    self.assertEqual(row[0], 'seen_by')
    self.assertEqual(row[1], 0)
    self.assertEqual(row[2], note.seen_by[0].name)
    self.assertEqual(row[3], [['user', 'Administrator', 'Guest']])
note.seen_by = []
note.save(ignore_version=False)
version = frappe.get_doc('Version', dict(docname=note.name))
data = version.get_data()
self.assertEqual(len(data.get('removed')), 1)
for row in data.get('removed'):
    self.assertEqual(row[0], 'seen_by')
    self.assertEqual(row[1]['user'], 'Guest')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/note/test_note.py:28*

### test_version

**Category**: workflow  
**Description**: Workflow: test version  
**Expected**: self.assertTrue(('content', 'test note content', '1'), data['changed'])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
note = self.insert_note()
note.title = 'test note 1'
note.content = '1'
note.save(ignore_version=False)
version = frappe.get_doc('Version', dict(docname=note.name))
data = version.get_data()
self.assertTrue(('title', 'test note', 'test note 1'), data['changed'])
self.assertTrue(('content', 'test note content', '1'), data['changed'])
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/note/test_note.py:16*

### test_rows

**Category**: workflow  
**Description**: Workflow: test rows  
**Expected**: self.assertEqual(len(data.get('removed')), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
note = self.insert_note()
note.append('seen_by', {'user': 'Administrator'})
note.save(ignore_version=False)
version = frappe.get_doc('Version', dict(docname=note.name))
data = version.get_data()
self.assertEqual(len(data.get('added')), 1)
self.assertEqual(len(data.get('removed')), 0)
self.assertEqual(len(data.get('changed')), 0)
for row in data.get('added'):
    self.assertEqual(row[0], 'seen_by')
    self.assertEqual(row[1]['user'], 'Administrator')
note.seen_by[0].user = 'Guest'
note.save(ignore_version=False)
version = frappe.get_doc('Version', dict(docname=note.name))
data = version.get_data()
self.assertEqual(len(data.get('row_changed')), 1)
for row in data.get('row_changed'):
    self.assertEqual(row[0], 'seen_by')
    self.assertEqual(row[1], 0)
    self.assertEqual(row[2], note.seen_by[0].name)
    self.assertEqual(row[3], [['user', 'Administrator', 'Guest']])
note.seen_by = []
note.save(ignore_version=False)
version = frappe.get_doc('Version', dict(docname=note.name))
data = version.get_data()
self.assertEqual(len(data.get('removed')), 1)
for row in data.get('removed'):
    self.assertEqual(row[0], 'seen_by')
    self.assertEqual(row[1]['user'], 'Guest')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/note/test_note.py:28*

### test_linked_with

**Category**: method_call  
**Description**: test linked with  
**Expected**: self.assertTrue('DocType' in results)  
**Confidence**: 0.85  

```python
self.assertTrue('User' in results)
self.assertTrue('DocType' in results)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/form/test_form.py:12*

### test_linked_with

**Category**: method_call  
**Description**: test linked with  
**Expected**: self.assertTrue('DocType' in results)  
**Confidence**: 0.85  

```python
self.assertTrue('User' in results)
self.assertTrue('DocType' in results)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/form/test_form.py:12*

### test_fetch_setup

**Category**: method_call  
**Description**: test fetch setup  
**Expected**: self.assertEqual(todo.assigned_by_full_name, frappe.db.get_value('User', todo.assigned_by, 'full_name'))  
**Confidence**: 0.85  

```python
todo.save()
self.assertEqual(todo.assigned_by_full_name, frappe.db.get_value('User', todo.assigned_by, 'full_name'))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/todo/test_todo.py:49*

### test_doc_read_access

**Category**: method_call  
**Description**: test doc read access  
**Expected**: self.assertFalse(todo1.has_permission('write'))  
**Confidence**: 0.85  

```python
self.assertFalse(todo1.has_permission('read'))
self.assertFalse(todo1.has_permission('write'))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/todo/test_todo.py:83*

### test_doc_read_access

**Category**: method_call  
**Description**: test doc read access  
**Expected**: self.assertTrue(todo2.has_permission('read'))  
**Confidence**: 0.85  

```python
self.assertFalse(todo1.has_permission('write'))
self.assertTrue(todo2.has_permission('read'))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/todo/test_todo.py:84*

### test_doc_read_access

**Category**: method_call  
**Description**: test doc read access  
**Expected**: self.assertTrue(todo2.has_permission('write'))  
**Confidence**: 0.85  

```python
self.assertTrue(todo2.has_permission('read'))
self.assertTrue(todo2.has_permission('write'))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/todo/test_todo.py:87*

### test_system_console

**Category**: method_call  
**Description**: test system console  
**Expected**: self.assertEqual(system_console.output, 'hello')  
**Confidence**: 0.85  

```python
system_console.run()
self.assertEqual(system_console.output, 'hello')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/system_console/test_system_console.py:16*

### test_system_console

**Category**: method_call  
**Description**: test system console  
**Expected**: self.assertEqual(system_console.output, 'Core')  
**Confidence**: 0.85  

```python
system_console.run()
self.assertEqual(system_console.output, 'Core')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/system_console/test_system_console.py:21*

### test_system_console_sql

**Category**: method_call  
**Description**: test system console sql  
**Expected**: self.assertIn('test', system_console.output)  
**Confidence**: 0.85  

```python
system_console.run()
self.assertIn('test', system_console.output)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/system_console/test_system_console.py:29*

### test_system_console_sql

**Category**: method_call  
**Description**: test system console sql  
**Expected**: self.assertIn('PermissionError', system_console.output)  
**Confidence**: 0.85  

```python
system_console.run()
self.assertIn('PermissionError', system_console.output)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/system_console/test_system_console.py:34*

### test_system_console

**Category**: method_call  
**Description**: test system console  
**Expected**: self.assertEqual(system_console.output, 'hello')  
**Confidence**: 0.85  

```python
system_console.run()
self.assertEqual(system_console.output, 'hello')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/system_console/test_system_console.py:16*

### test_system_console

**Category**: method_call  
**Description**: test system console  
**Expected**: self.assertEqual(system_console.output, 'Core')  
**Confidence**: 0.85  

```python
system_console.run()
self.assertEqual(system_console.output, 'Core')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/system_console/test_system_console.py:21*

### test_system_console_sql

**Category**: method_call  
**Description**: test system console sql  
**Expected**: self.assertIn('test', system_console.output)  
**Confidence**: 0.85  

```python
system_console.run()
self.assertIn('test', system_console.output)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/system_console/test_system_console.py:29*

### test_system_console_sql

**Category**: method_call  
**Description**: test system console sql  
**Expected**: self.assertIn('PermissionError', system_console.output)  
**Confidence**: 0.85  

```python
system_console.run()
self.assertIn('PermissionError', system_console.output)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/system_console/test_system_console.py:34*

### test_bulk_submit_in_background

**Category**: method_call  
**Description**: test bulk submit in background  
**Expected**: self.wait_for_assertion(lambda: check_docstatus(unsubmitted, 1))  
**Confidence**: 0.85  

```python
submit_cancel_or_update_docs(self.doctype, unsubmitted, action='submit')
self.wait_for_assertion(lambda: check_docstatus(unsubmitted, 1))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/bulk_update/test_bulk_update.py:43*

### test_bulk_submit_in_background

**Category**: method_call  
**Description**: test bulk submit in background  
**Expected**: self.wait_for_assertion(lambda: check_docstatus(submitted, 2))  
**Confidence**: 0.85  

```python
submit_cancel_or_update_docs(self.doctype, submitted, action='cancel')
self.wait_for_assertion(lambda: check_docstatus(submitted, 2))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/bulk_update/test_bulk_update.py:48*

### test_bulk_update_parent_fields

**Category**: method_call  
**Description**: test bulk update parent fields  
**Expected**: self.wait_for_assertion(lambda: check_field_values(docnames_bg, '_Test Background'))  
**Confidence**: 0.85  

```python
submit_cancel_or_update_docs(self.doctype, docnames_bg, action='update', data={'some_fieldname': '_Test Background'})
self.wait_for_assertion(lambda: check_field_values(docnames_bg, '_Test Background'))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/bulk_update/test_bulk_update.py:64*

### test_bulk_update_child_fields

**Category**: method_call  
**Description**: test bulk update child fields  
**Expected**: self.wait_for_assertion(lambda: check_child_field(docnames_bg, '_Test Child Updated'))  
**Confidence**: 0.85  

```python
submit_cancel_or_update_docs(self.doctype, docnames_bg, action='update', data=update_data)
self.wait_for_assertion(lambda: check_child_field(docnames_bg, '_Test Child Updated'))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/bulk_update/test_bulk_update.py:104*

### test_period_ending

**Category**: method_call  
**Description**: test period ending  
**Expected**: self.assertEqual(get_period_ending('2019-04-30', 'Monthly'), getdate('2019-04-30'))  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
doc = new_doctype(fields=[{'fieldname': 'title', 'fieldtype': 'Text', 'label': 'Title', 'reqd': 1}, {'fieldname': 'number', 'fieldtype': 'Int', 'label': 'Number', 'reqd': 1}, {'fieldname': 'date', 'fieldtype': 'Date', 'label': 'Date', 'reqd': 1}])
doc.insert()
self.doctype_name = doc.name

self.assertEqual(get_period_ending('2019-04-10', 'Monthly'), getdate('2019-04-30'))
self.assertEqual(get_period_ending('2019-04-30', 'Monthly'), getdate('2019-04-30'))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/dashboard_chart/test_dashboard_chart.py:51*

### test_period_ending

**Category**: method_call  
**Description**: test period ending  
**Expected**: self.assertEqual(get_period_ending('2019-03-31', 'Monthly'), getdate('2019-03-31'))  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
doc = new_doctype(fields=[{'fieldname': 'title', 'fieldtype': 'Text', 'label': 'Title', 'reqd': 1}, {'fieldname': 'number', 'fieldtype': 'Int', 'label': 'Number', 'reqd': 1}, {'fieldname': 'date', 'fieldtype': 'Date', 'label': 'Date', 'reqd': 1}])
doc.insert()
self.doctype_name = doc.name

self.assertEqual(get_period_ending('2019-04-30', 'Monthly'), getdate('2019-04-30'))
self.assertEqual(get_period_ending('2019-03-31', 'Monthly'), getdate('2019-03-31'))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/dashboard_chart/test_dashboard_chart.py:52*

### test_period_ending

**Category**: method_call  
**Description**: test period ending  
**Expected**: self.assertEqual(get_period_ending('2019-04-10', 'Quarterly'), getdate('2019-06-30'))  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
doc = new_doctype(fields=[{'fieldname': 'title', 'fieldtype': 'Text', 'label': 'Title', 'reqd': 1}, {'fieldname': 'number', 'fieldtype': 'Int', 'label': 'Number', 'reqd': 1}, {'fieldname': 'date', 'fieldtype': 'Date', 'label': 'Date', 'reqd': 1}])
doc.insert()
self.doctype_name = doc.name

self.assertEqual(get_period_ending('2019-03-31', 'Monthly'), getdate('2019-03-31'))
self.assertEqual(get_period_ending('2019-04-10', 'Quarterly'), getdate('2019-06-30'))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/dashboard_chart/test_dashboard_chart.py:53*

### test_period_ending

**Category**: method_call  
**Description**: test period ending  
**Expected**: self.assertEqual(get_period_ending('2019-06-30', 'Quarterly'), getdate('2019-06-30'))  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
doc = new_doctype(fields=[{'fieldname': 'title', 'fieldtype': 'Text', 'label': 'Title', 'reqd': 1}, {'fieldname': 'number', 'fieldtype': 'Int', 'label': 'Number', 'reqd': 1}, {'fieldname': 'date', 'fieldtype': 'Date', 'label': 'Date', 'reqd': 1}])
doc.insert()
self.doctype_name = doc.name

self.assertEqual(get_period_ending('2019-04-10', 'Quarterly'), getdate('2019-06-30'))
self.assertEqual(get_period_ending('2019-06-30', 'Quarterly'), getdate('2019-06-30'))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/dashboard_chart/test_dashboard_chart.py:55*

### test_version

**Category**: method_call  
**Description**: test version  
**Expected**: self.assertTrue(('content', 'test note content', '1'), data['changed'])  
**Confidence**: 0.85  

```python
self.assertTrue(('title', 'test note', 'test note 1'), data['changed'])
self.assertTrue(('content', 'test note content', '1'), data['changed'])
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/note/test_note.py:25*

### test_rows

**Category**: method_call  
**Description**: test rows  
**Expected**: self.assertEqual(len(data.get('removed')), 0)  
**Confidence**: 0.85  

```python
self.assertEqual(len(data.get('added')), 1)
self.assertEqual(len(data.get('removed')), 0)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/note/test_note.py:38*

### test_rows

**Category**: method_call  
**Description**: test rows  
**Expected**: self.assertEqual(len(data.get('changed')), 0)  
**Confidence**: 0.85  

```python
self.assertEqual(len(data.get('removed')), 0)
self.assertEqual(len(data.get('changed')), 0)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/note/test_note.py:39*

### test_version

**Category**: method_call  
**Description**: test version  
**Expected**: self.assertTrue(('content', 'test note content', '1'), data['changed'])  
**Confidence**: 0.85  

```python
self.assertTrue(('title', 'test note', 'test note 1'), data['changed'])
self.assertTrue(('content', 'test note content', '1'), data['changed'])
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/note/test_note.py:25*

### test_rows

**Category**: method_call  
**Description**: test rows  
**Expected**: self.assertEqual(len(data.get('removed')), 0)  
**Confidence**: 0.85  

```python
self.assertEqual(len(data.get('added')), 1)
self.assertEqual(len(data.get('removed')), 0)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/note/test_note.py:38*

### test_rows

**Category**: method_call  
**Description**: test rows  
**Expected**: self.assertEqual(len(data.get('changed')), 0)  
**Confidence**: 0.85  

```python
self.assertEqual(len(data.get('removed')), 0)
self.assertEqual(len(data.get('changed')), 0)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/note/test_note.py:39*

### test_tag_count_query

**Category**: method_call  
**Description**: test tag count query  
**Expected**: self.assertDictEqual(get_stats('["_user_tags"]', 'DocType'), {'_user_tags': [['Standard', 2], ['No Tags', frappe.db.count('DocType') - 2]]})  
**Confidence**: 0.85  

```python
# Setup
frappe.db.delete('Tag')
frappe.db.sql("UPDATE `tabDocType` set _user_tags=''")

add_tag('Standard', 'DocType', 'ToDo')
self.assertDictEqual(get_stats('["_user_tags"]', 'DocType'), {'_user_tags': [['Standard', 2], ['No Tags', frappe.db.count('DocType') - 2]]})
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/tag/test_tag.py:18*

### test_tag_count_query

**Category**: method_call  
**Description**: test tag count query  
**Expected**: self.assertDictEqual(get_stats('["_user_tags"]', 'DocType', filters='[["DocField", "fieldname", "like", "%last_name%"], ["DocType", "name", "like", "%use%"]]'), {'_user_tags': [['Standard', 1], ['No Tags', 0]]})  
**Confidence**: 0.85  

```python
# Setup
frappe.db.delete('Tag')
frappe.db.sql("UPDATE `tabDocType` set _user_tags=''")

self.assertDictEqual(get_stats('["_user_tags"]', 'DocType'), {'_user_tags': [['Standard', 2], ['No Tags', frappe.db.count('DocType') - 2]]})
self.assertDictEqual(get_stats('["_user_tags"]', 'DocType', filters='[["DocField", "fieldname", "like", "%last_name%"], ["DocType", "name", "like", "%use%"]]'), {'_user_tags': [['Standard', 1], ['No Tags', 0]]})
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/tag/test_tag.py:21*

### test_tag_count_query

**Category**: method_call  
**Description**: test tag count query  
**Expected**: self.assertDictEqual(get_stats('["_user_tags"]', 'DocType'), {'_user_tags': [['Standard', 2], ['No Tags', frappe.db.count('DocType') - 2]]})  
**Confidence**: 0.85  

```python
add_tag('Standard', 'DocType', 'ToDo')
self.assertDictEqual(get_stats('["_user_tags"]', 'DocType'), {'_user_tags': [['Standard', 2], ['No Tags', frappe.db.count('DocType') - 2]]})
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/tag/test_tag.py:18*

### test_tag_count_query

**Category**: method_call  
**Description**: test tag count query  
**Expected**: self.assertDictEqual(get_stats('["_user_tags"]', 'DocType', filters='[["DocField", "fieldname", "like", "%last_name%"], ["DocType", "name", "like", "%use%"]]'), {'_user_tags': [['Standard', 1], ['No Tags', 0]]})  
**Confidence**: 0.85  

```python
self.assertDictEqual(get_stats('["_user_tags"]', 'DocType'), {'_user_tags': [['Standard', 2], ['No Tags', frappe.db.count('DocType') - 2]]})
self.assertDictEqual(get_stats('["_user_tags"]', 'DocType', filters='[["DocField", "fieldname", "like", "%last_name%"], ["DocType", "name", "like", "%use%"]]'), {'_user_tags': [['Standard', 1], ['No Tags', 0]]})
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/tag/test_tag.py:21*

### test_linked_with

**Category**: instantiation  
**Description**: Instantiate get_linked_docs: test linked with  
**Expected**: self.assertTrue('User' in results)  
**Confidence**: 0.80  

```python
results = get_linked_docs('Role', 'System Manager', linkinfo=get_linked_doctypes('Role'))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/form/test_form.py:11*

### test_linked_with

**Category**: instantiation  
**Description**: Instantiate get_linked_docs: test linked with  
**Expected**: self.assertTrue('User' in results)  
**Confidence**: 0.80  

```python
results = get_linked_docs('Role', 'System Manager', linkinfo=get_linked_doctypes('Role'))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/form/test_form.py:11*

### test_permission_query

**Category**: instantiation  
**Description**: Instantiate get_modules_from_all_apps_for_user: test permission query  
**Confidence**: 0.80  

```python
all_modules = get_modules_from_all_apps_for_user('Administrator')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/dashboard/test_dashboard.py:19*

### test_permission_query

**Category**: instantiation  
**Description**: Instantiate get_modules_from_all_apps_for_user: test permission query  
**Confidence**: 0.80  

```python
all_modules = get_modules_from_all_apps_for_user('Administrator')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/dashboard/test_dashboard.py:19*

### test_assignment

**Category**: instantiation  
**Description**: Instantiate get_value: test assignment  
**Expected**: self.assertEqual(log_type, 'Assignment')  
**Confidence**: 0.80  

```python
log_type = frappe.db.get_value('Notification Log', {'document_type': 'ToDo', 'document_name': todo.name}, 'type')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/notification_log/test_notification_log.py:17*

### test_share

**Category**: instantiation  
**Description**: Instantiate get_value: test share  
**Expected**: self.assertEqual(log_type, 'Share')  
**Confidence**: 0.80  

```python
log_type = frappe.db.get_value('Notification Log', {'document_type': 'ToDo', 'document_name': todo.name}, 'type')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/notification_log/test_notification_log.py:27*

### test_assignment

**Category**: instantiation  
**Description**: Instantiate get_value: test assignment  
**Expected**: self.assertEqual(log_type, 'Assignment')  
**Confidence**: 0.80  

```python
log_type = frappe.db.get_value('Notification Log', {'document_type': 'ToDo', 'document_name': todo.name}, 'type')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/notification_log/test_notification_log.py:17*

### test_share

**Category**: instantiation  
**Description**: Instantiate get_value: test share  
**Expected**: self.assertEqual(log_type, 'Share')  
**Confidence**: 0.80  

```python
log_type = frappe.db.get_value('Notification Log', {'document_type': 'ToDo', 'document_name': todo.name}, 'type')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/desk/doctype/notification_log/test_notification_log.py:27*

