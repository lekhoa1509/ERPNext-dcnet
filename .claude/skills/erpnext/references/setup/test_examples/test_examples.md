# Test Example Extraction Report

**Total Examples**: 68  
**High Value Examples** (confidence > 0.7): 68  
**Average Complexity**: 0.66  

## Examples by Category

- **instantiation**: 10
- **method_call**: 16
- **workflow**: 42

## Examples by Language

- **Python**: 68

## Extracted Examples

### test_employee_status_left

**Category**: workflow  
**Description**: Workflow: test employee status left  
**Expected**: self.assertRaises(InactiveEmployeeStatusError, employee1_doc.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
employee1 = make_employee('test_employee_1@company.com')
employee2 = make_employee('test_employee_2@company.com')
employee1_doc = frappe.get_doc('Employee', employee1)
employee2_doc = frappe.get_doc('Employee', employee2)
employee2_doc.reload()
employee2_doc.reports_to = employee1_doc.name
employee2_doc.save()
employee1_doc.reload()
employee1_doc.status = 'Left'
self.assertRaises(InactiveEmployeeStatusError, employee1_doc.save)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/employee/test_employee.py:15*

### test_user_has_employee

**Category**: workflow  
**Description**: Workflow: test user has employee  
**Expected**: self.assertTrue('Employee' not in frappe.get_roles(user))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
employee = make_employee('test_emp_user_creation@company.com')
employee_doc = frappe.get_doc('Employee', employee)
user = employee_doc.user_id
self.assertTrue('Employee' in frappe.get_roles(user))
employee_doc.user_id = ''
employee_doc.save()
self.assertTrue('Employee' not in frappe.get_roles(user))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/employee/test_employee.py:27*

### test_employee_user_permission

**Category**: workflow  
**Description**: Workflow: test employee user permission  
**Expected**: self.assertEqual(qb_employee_list, employee_list)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
employee1 = make_employee('employee_1_test@company.com', create_user_permission=1)
employee2 = make_employee('employee_2_test@company.com', create_user_permission=1)
make_employee('employee_3_test@company.com', create_user_permission=1)
employee1_doc = frappe.get_doc('Employee', employee1)
employee2_doc = frappe.get_doc('Employee', employee2)
employee2_doc.reload()
employee2_doc.reports_to = employee1_doc.name
employee2_doc.save()
frappe.set_user(employee1_doc.user_id)
Employee = frappe.qb.DocType('Employee')
qb_employee_list = frappe.qb.from_(Employee).select(Employee.name).where(Criterion.all(build_qb_match_conditions('Employee'))).orderby(Employee.Name).run(pluck=Employee.name)
employee_list = frappe.db.get_list('Employee', pluck='name', order_by='name')
self.assertEqual(qb_employee_list, employee_list)
frappe.set_user('Administrator')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/employee/test_employee.py:36*

### test_employee_status_left

**Category**: workflow  
**Description**: Workflow: test employee status left  
**Expected**: self.assertRaises(InactiveEmployeeStatusError, employee1_doc.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
employee1 = make_employee('test_employee_1@company.com')
employee2 = make_employee('test_employee_2@company.com')
employee1_doc = frappe.get_doc('Employee', employee1)
employee2_doc = frappe.get_doc('Employee', employee2)
employee2_doc.reload()
employee2_doc.reports_to = employee1_doc.name
employee2_doc.save()
employee1_doc.reload()
employee1_doc.status = 'Left'
self.assertRaises(InactiveEmployeeStatusError, employee1_doc.save)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/employee/test_employee.py:15*

### test_user_has_employee

**Category**: workflow  
**Description**: Workflow: test user has employee  
**Expected**: self.assertTrue('Employee' not in frappe.get_roles(user))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
employee = make_employee('test_emp_user_creation@company.com')
employee_doc = frappe.get_doc('Employee', employee)
user = employee_doc.user_id
self.assertTrue('Employee' in frappe.get_roles(user))
employee_doc.user_id = ''
employee_doc.save()
self.assertTrue('Employee' not in frappe.get_roles(user))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/employee/test_employee.py:27*

### test_employee_user_permission

**Category**: workflow  
**Description**: Workflow: test employee user permission  
**Expected**: self.assertEqual(qb_employee_list, employee_list)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
employee1 = make_employee('employee_1_test@company.com', create_user_permission=1)
employee2 = make_employee('employee_2_test@company.com', create_user_permission=1)
make_employee('employee_3_test@company.com', create_user_permission=1)
employee1_doc = frappe.get_doc('Employee', employee1)
employee2_doc = frappe.get_doc('Employee', employee2)
employee2_doc.reload()
employee2_doc.reports_to = employee1_doc.name
employee2_doc.save()
frappe.set_user(employee1_doc.user_id)
Employee = frappe.qb.DocType('Employee')
qb_employee_list = frappe.qb.from_(Employee).select(Employee.name).where(Criterion.all(build_qb_match_conditions('Employee'))).orderby(Employee.Name).run(pluck=Employee.name)
employee_list = frappe.db.get_list('Employee', pluck='name', order_by='name')
self.assertEqual(qb_employee_list, employee_list)
frappe.set_user('Administrator')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/employee/test_employee.py:36*

### test_basic_tree

**Category**: workflow  
**Description**: Workflow: test basic tree  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
min_lft = 1
max_rgt = frappe.db.sql('select max(rgt) from `tabItem Group`')[0][0]
if not records:
    records = self.globalTestRecords['Item Group'][2:]
for item_group in records:
    lft, rgt, parent_item_group = frappe.db.get_value('Item Group', item_group['item_group_name'], ['lft', 'rgt', 'parent_item_group'])
    if parent_item_group:
        parent_lft, parent_rgt = frappe.db.get_value('Item Group', parent_item_group, ['lft', 'rgt'])
    else:
        parent_lft = min_lft - 1
        parent_rgt = max_rgt + 1
    self.assertTrue(lft, 'has no lft')
    self.assertTrue(rgt, 'has no rgt')
    self.assertTrue(lft < rgt, 'lft >= rgt')
    self.assertTrue(parent_lft < parent_rgt, 'parent_lft >= parent_rgt')
    self.assertTrue(lft > parent_lft, 'lft <= parent_lft')
    self.assertTrue(rgt < parent_rgt, 'rgt >= parent_rgt')
    self.assertTrue(lft >= min_lft, 'lft < min_lft')
    self.assertTrue(rgt <= max_rgt, 'rgs > max_rgt')
    no_of_children = self._get_no_of_children(item_group['item_group_name'])
    self.assertTrue(rgt == lft + 1 + 2 * no_of_children, 'rgt is not lft + 1 + (2 * #children)')
    no_of_children = self._get_no_of_children(parent_item_group)
    self.assertTrue(parent_rgt == parent_lft + 1 + 2 * no_of_children, 'parent_rgs is not 1 + (2 * #children)')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/item_group/test_item_group.py:17*

### test_move_group_into_another

**Category**: workflow  
**Description**: Workflow: test move group into another  
**Expected**: self.assertEqual(new_rgt - old_rgt, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
old_lft, old_rgt = frappe.db.get_value('Item Group', '_Test Item Group C', ['lft', 'rgt'])
group_b = frappe.get_doc('Item Group', '_Test Item Group B')
lft, rgt = (group_b.lft, group_b.rgt)
group_b.parent_item_group = '_Test Item Group C'
group_b.save()
self.test_basic_tree()
new_lft, new_rgt = frappe.db.get_value('Item Group', '_Test Item Group C', ['lft', 'rgt'])
self.assertEqual(old_lft - new_lft, rgt - lft + 1)
self.assertEqual(new_rgt - old_rgt, 0)
self._move_it_back()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/item_group/test_item_group.py:66*

### test_move_leaf_into_another_group

**Category**: workflow  
**Description**: Workflow: test move leaf into another group  
**Expected**: self.assertEqual(new_rgt - old_rgt, rgt - lft + 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
old_lft, old_rgt = frappe.db.get_value('Item Group', '_Test Item Group C', ['lft', 'rgt'])
group_b_3 = frappe.get_doc('Item Group', '_Test Item Group B - 3')
lft, rgt = (group_b_3.lft, group_b_3.rgt)
group_b_3.parent_item_group = '_Test Item Group C'
group_b_3.save()
self.test_basic_tree()
new_lft, new_rgt = frappe.db.get_value('Item Group', '_Test Item Group C', ['lft', 'rgt'])
self.assertEqual(old_lft - new_lft, 0)
self.assertEqual(new_rgt - old_rgt, rgt - lft + 1)
group_b_3 = frappe.get_doc('Item Group', '_Test Item Group B - 3')
group_b_3.parent_item_group = '_Test Item Group B'
group_b_3.save()
self.test_basic_tree()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/item_group/test_item_group.py:99*

### test_delete_leaf

**Category**: workflow  
**Description**: Workflow: test delete leaf  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
parent_item_group = frappe.db.get_value('Item Group', '_Test Item Group B - 3', 'parent_item_group')
frappe.db.get_value('Item Group', parent_item_group, 'rgt')
ancestors = get_ancestors_of('Item Group', '_Test Item Group B - 3')
ancestors = frappe.db.sql('select name, rgt from `tabItem Group`\n\t\t\twhere name in ({})'.format(', '.join(['%s'] * len(ancestors))), tuple(ancestors), as_dict=True)
frappe.delete_doc('Item Group', '_Test Item Group B - 3')
records_to_test = self.globalTestRecords['Item Group'][2:]
del records_to_test[4]
self.test_basic_tree(records=records_to_test)
for item_group in ancestors:
    new_lft, new_rgt = frappe.db.get_value('Item Group', item_group.name, ['lft', 'rgt'])
    self.assertEqual(new_rgt, item_group.rgt - 2)
frappe.copy_doc(self.globalTestRecords['Item Group'][6]).insert()
self.test_basic_tree()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/item_group/test_item_group.py:125*

### test_basic_tree

**Category**: workflow  
**Description**: Workflow: test basic tree  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
# Fixtures: records

min_lft = 1
max_rgt = frappe.db.sql('select max(rgt) from `tabItem Group`')[0][0]
if not records:
    records = self.globalTestRecords['Item Group'][2:]
for item_group in records:
    lft, rgt, parent_item_group = frappe.db.get_value('Item Group', item_group['item_group_name'], ['lft', 'rgt', 'parent_item_group'])
    if parent_item_group:
        parent_lft, parent_rgt = frappe.db.get_value('Item Group', parent_item_group, ['lft', 'rgt'])
    else:
        parent_lft = min_lft - 1
        parent_rgt = max_rgt + 1
    self.assertTrue(lft, 'has no lft')
    self.assertTrue(rgt, 'has no rgt')
    self.assertTrue(lft < rgt, 'lft >= rgt')
    self.assertTrue(parent_lft < parent_rgt, 'parent_lft >= parent_rgt')
    self.assertTrue(lft > parent_lft, 'lft <= parent_lft')
    self.assertTrue(rgt < parent_rgt, 'rgt >= parent_rgt')
    self.assertTrue(lft >= min_lft, 'lft < min_lft')
    self.assertTrue(rgt <= max_rgt, 'rgs > max_rgt')
    no_of_children = self._get_no_of_children(item_group['item_group_name'])
    self.assertTrue(rgt == lft + 1 + 2 * no_of_children, 'rgt is not lft + 1 + (2 * #children)')
    no_of_children = self._get_no_of_children(parent_item_group)
    self.assertTrue(parent_rgt == parent_lft + 1 + 2 * no_of_children, 'parent_rgs is not 1 + (2 * #children)')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/item_group/test_item_group.py:17*

### test_move_group_into_another

**Category**: workflow  
**Description**: Workflow: test move group into another  
**Expected**: self.assertEqual(new_rgt - old_rgt, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
old_lft, old_rgt = frappe.db.get_value('Item Group', '_Test Item Group C', ['lft', 'rgt'])
group_b = frappe.get_doc('Item Group', '_Test Item Group B')
lft, rgt = (group_b.lft, group_b.rgt)
group_b.parent_item_group = '_Test Item Group C'
group_b.save()
self.test_basic_tree()
new_lft, new_rgt = frappe.db.get_value('Item Group', '_Test Item Group C', ['lft', 'rgt'])
self.assertEqual(old_lft - new_lft, rgt - lft + 1)
self.assertEqual(new_rgt - old_rgt, 0)
self._move_it_back()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/item_group/test_item_group.py:66*

### test_move_leaf_into_another_group

**Category**: workflow  
**Description**: Workflow: test move leaf into another group  
**Expected**: self.assertEqual(new_rgt - old_rgt, rgt - lft + 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
old_lft, old_rgt = frappe.db.get_value('Item Group', '_Test Item Group C', ['lft', 'rgt'])
group_b_3 = frappe.get_doc('Item Group', '_Test Item Group B - 3')
lft, rgt = (group_b_3.lft, group_b_3.rgt)
group_b_3.parent_item_group = '_Test Item Group C'
group_b_3.save()
self.test_basic_tree()
new_lft, new_rgt = frappe.db.get_value('Item Group', '_Test Item Group C', ['lft', 'rgt'])
self.assertEqual(old_lft - new_lft, 0)
self.assertEqual(new_rgt - old_rgt, rgt - lft + 1)
group_b_3 = frappe.get_doc('Item Group', '_Test Item Group B - 3')
group_b_3.parent_item_group = '_Test Item Group B'
group_b_3.save()
self.test_basic_tree()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/item_group/test_item_group.py:99*

### test_delete_leaf

**Category**: workflow  
**Description**: Workflow: test delete leaf  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
parent_item_group = frappe.db.get_value('Item Group', '_Test Item Group B - 3', 'parent_item_group')
frappe.db.get_value('Item Group', parent_item_group, 'rgt')
ancestors = get_ancestors_of('Item Group', '_Test Item Group B - 3')
ancestors = frappe.db.sql('select name, rgt from `tabItem Group`\n\t\t\twhere name in ({})'.format(', '.join(['%s'] * len(ancestors))), tuple(ancestors), as_dict=True)
frappe.delete_doc('Item Group', '_Test Item Group B - 3')
records_to_test = self.globalTestRecords['Item Group'][2:]
del records_to_test[4]
self.test_basic_tree(records=records_to_test)
for item_group in ancestors:
    new_lft, new_rgt = frappe.db.get_value('Item Group', item_group.name, ['lft', 'rgt'])
    self.assertEqual(new_rgt, item_group.rgt - 2)
frappe.copy_doc(self.globalTestRecords['Item Group'][6]).insert()
self.test_basic_tree()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/item_group/test_item_group.py:125*

### test_doctypes_contain_company_field

**Category**: workflow  
**Description**: Workflow: Test that all DocTypes in To Delete list have a valid company link field  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self._clear_all_deletion_cache_flags()
create_company('Dunder Mifflin Paper Co')

'Test that all DocTypes in To Delete list have a valid company link field'
tdr = create_and_submit_transaction_deletion_doc('Dunder Mifflin Paper Co')
for doctype_row in tdr.doctypes_to_delete:
    if doctype_row.company_field:
        field_found = False
        doctype_fields = frappe.get_meta(doctype_row.doctype_name).as_dict()['fields']
        for doctype_field in doctype_fields:
            if doctype_field['fieldname'] == doctype_row.company_field and doctype_field['fieldtype'] == 'Link' and (doctype_field['options'] == 'Company'):
                field_found = True
                break
        self.assertTrue(field_found, f"DocType {doctype_row.doctype_name} should have company field '{doctype_row.company_field}'")
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/transaction_deletion_record/test_transaction_deletion_record.py:36*

### test_generate_to_delete_list

**Category**: workflow  
**Description**: Workflow: Test automatic generation of To Delete list  
**Expected**: self.assertTrue(task_in_list, 'Task should be in To Delete list')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self._clear_all_deletion_cache_flags()
create_company('Dunder Mifflin Paper Co')

'Test automatic generation of To Delete list'
company = 'Dunder Mifflin Paper Co'
create_task(company)
tdr = frappe.new_doc('Transaction Deletion Record')
tdr.company = company
tdr.insert()
tdr.generate_to_delete_list()
tdr.reload()
self.assertGreater(len(tdr.doctypes_to_delete), 0)
task_in_list = any((d.doctype_name == 'Task' for d in tdr.doctypes_to_delete))
self.assertTrue(task_in_list, 'Task should be in To Delete list')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/transaction_deletion_record/test_transaction_deletion_record.py:91*

### test_csv_export_import

**Category**: workflow  
**Description**: Workflow: Test CSV export and import functionality with company_field column  
**Expected**: self.assertGreaterEqual(result['imported'], 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self._clear_all_deletion_cache_flags()
create_company('Dunder Mifflin Paper Co')

'Test CSV export and import functionality with company_field column'
company = 'Dunder Mifflin Paper Co'
create_task(company)
tdr = frappe.new_doc('Transaction Deletion Record')
tdr.company = company
tdr.insert()
tdr.generate_to_delete_list()
tdr.reload()
original_count = len(tdr.doctypes_to_delete)
self.assertGreater(original_count, 0)
tdr.export_to_delete_template_method()
csv_content = frappe.response.get('result')
self.assertIsNotNone(csv_content)
self.assertIn('doctype_name', csv_content)
self.assertIn('company_field', csv_content)
tdr2 = frappe.new_doc('Transaction Deletion Record')
tdr2.company = company
tdr2.insert()
result = tdr2.import_to_delete_template_method(csv_content)
tdr2.reload()
self.assertEqual(len(tdr2.doctypes_to_delete), original_count)
self.assertGreaterEqual(result['imported'], 1)
for row in tdr2.doctypes_to_delete:
    if row.doctype_name == 'Task':
        self.assertIsNotNone(row.company_field, 'Task should have company_field set after import')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/transaction_deletion_record/test_transaction_deletion_record.py:133*

### test_progress_tracking

**Category**: workflow  
**Description**: Workflow: Test that deleted checkbox is marked when DocType deletion completes  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self._clear_all_deletion_cache_flags()
create_company('Dunder Mifflin Paper Co')

'Test that deleted checkbox is marked when DocType deletion completes'
company = 'Dunder Mifflin Paper Co'
create_task(company)
tdr = create_and_submit_transaction_deletion_doc(company)
tdr.reload()
task_row = None
for doctype in tdr.doctypes_to_delete:
    if doctype.doctype_name == 'Task':
        task_row = doctype
        break
if task_row:
    self.assertEqual(task_row.deleted, 1, 'Task should be marked as deleted')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/transaction_deletion_record/test_transaction_deletion_record.py:172*

### test_cache_flag_management

**Category**: workflow  
**Description**: Workflow: Test that cache flags can be set and cleared correctly  
**Expected**: self.assertIsNone(cached_value, 'Cache flag should be cleared for Task')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self._clear_all_deletion_cache_flags()
create_company('Dunder Mifflin Paper Co')

'Test that cache flags can be set and cleared correctly'
company = 'Dunder Mifflin Paper Co'
create_task(company)
tdr = frappe.new_doc('Transaction Deletion Record')
tdr.company = company
tdr.insert()
tdr.generate_to_delete_list()
tdr.reload()
tdr._set_deletion_cache()
cached_value = frappe.cache.get_value('deletion_running_doctype:Task')
self.assertEqual(cached_value, tdr.name, 'Cache flag should be set for Task')
tdr._clear_deletion_cache()
cached_value = frappe.cache.get_value('deletion_running_doctype:Task')
self.assertIsNone(cached_value, 'Cache flag should be cleared for Task')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/transaction_deletion_record/test_transaction_deletion_record.py:279*

### test_check_for_running_deletion_blocks_save

**Category**: workflow  
**Description**: Workflow: Test that check_for_running_deletion_job blocks saves when cache flag exists  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self._clear_all_deletion_cache_flags()
create_company('Dunder Mifflin Paper Co')

'Test that check_for_running_deletion_job blocks saves when cache flag exists'
from erpnext.setup.doctype.transaction_deletion_record.transaction_deletion_record import check_for_running_deletion_job
company = 'Dunder Mifflin Paper Co'
frappe.cache.set_value('deletion_running_doctype:Task', 'TDR-00001', expires_in_sec=60)
try:
    new_task = frappe.new_doc('Task')
    new_task.company = company
    new_task.subject = 'Should be blocked'
    with self.assertRaises(frappe.ValidationError) as context:
        check_for_running_deletion_job(new_task)
    error_message = str(context.exception)
    self.assertIn('currently deleting', error_message)
    self.assertIn('TDR-00001', error_message)
finally:
    frappe.cache.delete_value('deletion_running_doctype:Task')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/transaction_deletion_record/test_transaction_deletion_record.py:304*

### test_check_for_running_deletion_allows_save_when_no_flag

**Category**: workflow  
**Description**: Workflow: Test that documents can be saved when no deletion is running  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self._clear_all_deletion_cache_flags()
create_company('Dunder Mifflin Paper Co')

'Test that documents can be saved when no deletion is running'
company = 'Dunder Mifflin Paper Co'
frappe.cache.delete_value('deletion_running_doctype:Task')
new_task = frappe.new_doc('Task')
new_task.company = company
new_task.subject = 'Should be allowed'
try:
    new_task.insert()
    frappe.delete_doc('Task', new_task.name)
except frappe.ValidationError as e:
    self.fail(f'Should allow save when no deletion is running, but got: {e}')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/transaction_deletion_record/test_transaction_deletion_record.py:332*

### test_only_one_deletion_allowed_globally

**Category**: workflow  
**Description**: Workflow: Test that only one deletion can be submitted at a time (global enforcement)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self._clear_all_deletion_cache_flags()
create_company('Dunder Mifflin Paper Co')

'Test that only one deletion can be submitted at a time (global enforcement)'
company1 = 'Dunder Mifflin Paper Co'
company2 = 'Sabre Corporation'
create_company(company2)
tdr1 = frappe.new_doc('Transaction Deletion Record')
tdr1.company = company1
tdr1.insert()
tdr1.append('doctypes_to_delete', {'doctype_name': 'Task', 'company_field': 'company'})
tdr1.save()
tdr1.submit()
try:
    tdr2 = frappe.new_doc('Transaction Deletion Record')
    tdr2.company = company2
    tdr2.insert()
    tdr2.append('doctypes_to_delete', {'doctype_name': 'Lead', 'company_field': 'company'})
    tdr2.save()
    with self.assertRaises(frappe.ValidationError) as context:
        tdr2.submit()
    self.assertIn('already', str(context.exception).lower())
    self.assertIn(tdr1.name, str(context.exception))
finally:
    tdr1.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/transaction_deletion_record/test_transaction_deletion_record.py:352*

### test_doctypes_contain_company_field

**Category**: workflow  
**Description**: Workflow: Test that all DocTypes in To Delete list have a valid company link field  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test that all DocTypes in To Delete list have a valid company link field'
tdr = create_and_submit_transaction_deletion_doc('Dunder Mifflin Paper Co')
for doctype_row in tdr.doctypes_to_delete:
    if doctype_row.company_field:
        field_found = False
        doctype_fields = frappe.get_meta(doctype_row.doctype_name).as_dict()['fields']
        for doctype_field in doctype_fields:
            if doctype_field['fieldname'] == doctype_row.company_field and doctype_field['fieldtype'] == 'Link' and (doctype_field['options'] == 'Company'):
                field_found = True
                break
        self.assertTrue(field_found, f"DocType {doctype_row.doctype_name} should have company field '{doctype_row.company_field}'")
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/transaction_deletion_record/test_transaction_deletion_record.py:36*

### test_generate_to_delete_list

**Category**: workflow  
**Description**: Workflow: Test automatic generation of To Delete list  
**Expected**: self.assertTrue(task_in_list, 'Task should be in To Delete list')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test automatic generation of To Delete list'
company = 'Dunder Mifflin Paper Co'
create_task(company)
tdr = frappe.new_doc('Transaction Deletion Record')
tdr.company = company
tdr.insert()
tdr.generate_to_delete_list()
tdr.reload()
self.assertGreater(len(tdr.doctypes_to_delete), 0)
task_in_list = any((d.doctype_name == 'Task' for d in tdr.doctypes_to_delete))
self.assertTrue(task_in_list, 'Task should be in To Delete list')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/transaction_deletion_record/test_transaction_deletion_record.py:91*

### test_coa_based_on_existing_company

**Category**: workflow  
**Description**: Workflow: test coa based on existing company  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
company = frappe.new_doc('Company')
company.company_name = 'COA from Existing Company'
company.abbr = 'CFEC'
company.default_currency = 'INR'
company.create_chart_of_accounts_based_on = 'Existing Company'
company.existing_company = '_Test Company'
company.save()
expected_results = {'Debtors - CFEC': {'account_type': 'Receivable', 'is_group': 0, 'root_type': 'Asset', 'parent_account': 'Accounts Receivable - CFEC'}, 'Cash - CFEC': {'account_type': 'Cash', 'is_group': 0, 'root_type': 'Asset', 'parent_account': 'Cash In Hand - CFEC'}}
for account, acc_property in expected_results.items():
    acc = frappe.get_doc('Account', account)
    for prop, val in acc_property.items():
        self.assertEqual(acc.get(prop), val)
self.delete_mode_of_payment('COA from Existing Company')
frappe.delete_doc('Company', 'COA from Existing Company')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/company/test_company.py:26*

### test_basic_tree

**Category**: workflow  
**Description**: Workflow: test basic tree  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
min_lft = 1
max_rgt = frappe.db.sql('select max(rgt) from `tabCompany`')[0][0]
if not records:
    records = self.globalTestRecords['Company'][2:]
for company in records:
    lft, rgt, parent_company = frappe.db.get_value('Company', company['company_name'], ['lft', 'rgt', 'parent_company'])
    if parent_company:
        parent_lft, parent_rgt = frappe.db.get_value('Company', parent_company, ['lft', 'rgt'])
    else:
        parent_lft = min_lft - 1
        parent_rgt = max_rgt + 1
    self.assertTrue(lft)
    self.assertTrue(rgt)
    self.assertTrue(lft < rgt)
    self.assertTrue(parent_lft < parent_rgt)
    self.assertTrue(lft > parent_lft)
    self.assertTrue(rgt < parent_rgt)
    self.assertTrue(lft >= min_lft)
    self.assertTrue(rgt <= max_rgt)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/company/test_company.py:112*

### test_primary_address

**Category**: workflow  
**Description**: Workflow: test primary address  
**Expected**: self.assertEqual(get_default_company_address(company), primary.name)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
company = '_Test Company'
secondary = frappe.get_doc({'address_title': 'Non Primary', 'doctype': 'Address', 'address_type': 'Billing', 'address_line1': 'Something', 'city': 'Mumbai', 'state': 'Maharashtra', 'country': 'India', 'is_primary_address': 1, 'pincode': '400098', 'links': [{'link_doctype': 'Company', 'link_name': company}]})
secondary.insert()
self.addCleanup(secondary.delete)
primary = frappe.copy_doc(secondary)
primary.is_primary_address = 1
primary.insert()
self.addCleanup(primary.delete)
self.assertEqual(get_default_company_address(company), primary.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/company/test_company.py:140*

### test_coa_based_on_existing_company

**Category**: workflow  
**Description**: Workflow: test coa based on existing company  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
company = frappe.new_doc('Company')
company.company_name = 'COA from Existing Company'
company.abbr = 'CFEC'
company.default_currency = 'INR'
company.create_chart_of_accounts_based_on = 'Existing Company'
company.existing_company = '_Test Company'
company.save()
expected_results = {'Debtors - CFEC': {'account_type': 'Receivable', 'is_group': 0, 'root_type': 'Asset', 'parent_account': 'Accounts Receivable - CFEC'}, 'Cash - CFEC': {'account_type': 'Cash', 'is_group': 0, 'root_type': 'Asset', 'parent_account': 'Cash In Hand - CFEC'}}
for account, acc_property in expected_results.items():
    acc = frappe.get_doc('Account', account)
    for prop, val in acc_property.items():
        self.assertEqual(acc.get(prop), val)
self.delete_mode_of_payment('COA from Existing Company')
frappe.delete_doc('Company', 'COA from Existing Company')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/company/test_company.py:26*

### test_basic_tree

**Category**: workflow  
**Description**: Workflow: test basic tree  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
# Fixtures: records

min_lft = 1
max_rgt = frappe.db.sql('select max(rgt) from `tabCompany`')[0][0]
if not records:
    records = self.globalTestRecords['Company'][2:]
for company in records:
    lft, rgt, parent_company = frappe.db.get_value('Company', company['company_name'], ['lft', 'rgt', 'parent_company'])
    if parent_company:
        parent_lft, parent_rgt = frappe.db.get_value('Company', parent_company, ['lft', 'rgt'])
    else:
        parent_lft = min_lft - 1
        parent_rgt = max_rgt + 1
    self.assertTrue(lft)
    self.assertTrue(rgt)
    self.assertTrue(lft < rgt)
    self.assertTrue(parent_lft < parent_rgt)
    self.assertTrue(lft > parent_lft)
    self.assertTrue(rgt < parent_rgt)
    self.assertTrue(lft >= min_lft)
    self.assertTrue(rgt <= max_rgt)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/company/test_company.py:112*

### test_primary_address

**Category**: workflow  
**Description**: Workflow: test primary address  
**Expected**: self.assertEqual(get_default_company_address(company), primary.name)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
company = '_Test Company'
secondary = frappe.get_doc({'address_title': 'Non Primary', 'doctype': 'Address', 'address_type': 'Billing', 'address_line1': 'Something', 'city': 'Mumbai', 'state': 'Maharashtra', 'country': 'India', 'is_primary_address': 1, 'pincode': '400098', 'links': [{'link_doctype': 'Company', 'link_name': company}]})
secondary.insert()
self.addCleanup(secondary.delete)
primary = frappe.copy_doc(secondary)
primary.is_primary_address = 1
primary.insert()
self.addCleanup(primary.delete)
self.assertEqual(get_default_company_address(company), primary.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/company/test_company.py:140*

### test_exchange_rate

**Category**: workflow  
**Description**: Workflow: test exchange rate  
**Expected**: self.assertEqual(flt(exchange_rate, 3), 65.1)  
**Confidence**: 0.90  
**Tags**: unittest, mock, workflow, integration  

```python
save_new_records(self.globalTestRecords['Currency Exchange'])
frappe.db.set_single_value('Accounts Settings', 'allow_stale', 1)
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-01', 'for_buying')
self.assertEqual(flt(exchange_rate, 3), 60.0)
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-15', 'for_buying')
self.assertEqual(exchange_rate, 65.1)
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-30', 'for_selling')
self.assertEqual(exchange_rate, 62.9)
self.clear_cache()
exchange_rate = get_exchange_rate('USD', 'INR', '2015-12-15', 'for_selling')
self.assertFalse(exchange_rate == 60)
self.assertEqual(flt(exchange_rate, 3), 66.999)
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-20', 'for_buying')
self.assertFalse(exchange_rate == 60)
self.assertEqual(flt(exchange_rate, 3), 65.1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/currency_exchange/test_currency_exchange.py:91*

### test_exchange_rate_via_exchangerate_host

**Category**: workflow  
**Description**: Workflow: test exchange rate via exchangerate host  
**Expected**: self.assertEqual(flt(exchange_rate, 3), 65.1)  
**Confidence**: 0.90  
**Tags**: unittest, mock, workflow, integration  

```python
save_new_records(self.globalTestRecords['Currency Exchange'])
settings = frappe.get_single('Currency Exchange Settings')
settings.service_provider = 'exchangerate.host'
settings.access_key = '12345667890'
settings.save()
frappe.db.set_single_value('Accounts Settings', 'allow_stale', 1)
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-01', 'for_buying')
self.assertEqual(flt(exchange_rate, 3), 60.0)
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-15', 'for_buying')
self.assertEqual(exchange_rate, 65.1)
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-30', 'for_selling')
self.assertEqual(exchange_rate, 62.9)
self.clear_cache()
exchange_rate = get_exchange_rate('USD', 'INR', '2015-12-15', 'for_selling')
self.assertFalse(exchange_rate == 60)
self.assertEqual(flt(exchange_rate, 3), 66.999)
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-20', 'for_buying')
self.assertFalse(exchange_rate == 60)
self.assertEqual(flt(exchange_rate, 3), 65.1)
settings = frappe.get_single('Currency Exchange Settings')
settings.service_provider = 'frankfurter.dev'
settings.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/currency_exchange/test_currency_exchange.py:116*

### test_exchange_rate_strict

**Category**: workflow  
**Description**: Workflow: test exchange rate strict  
**Expected**: self.assertEqual(flt(exchange_rate, 3), 66.999)  
**Confidence**: 0.90  
**Tags**: unittest, mock, workflow, integration  

```python
frappe.db.set_single_value('Accounts Settings', 'allow_stale', 0)
frappe.db.set_single_value('Accounts Settings', 'stale_days', 1)
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-01', 'for_buying')
self.assertEqual(exchange_rate, 60.0)
self.clear_cache()
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-15', 'for_buying')
self.assertEqual(flt(exchange_rate, 3), 65.1)
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-30', 'for_selling')
self.assertEqual(exchange_rate, 62.9)
self.clear_cache()
exchange_rate = get_exchange_rate('USD', 'INR', '2015-12-15', 'for_buying')
self.assertEqual(flt(exchange_rate, 3), 66.999)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/currency_exchange/test_currency_exchange.py:152*

### test_exchange_rate

**Category**: workflow  
**Description**: Workflow: test exchange rate  
**Expected**: self.assertEqual(flt(exchange_rate, 3), 65.1)  
**Confidence**: 0.90  
**Tags**: unittest, mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get

save_new_records(self.globalTestRecords['Currency Exchange'])
frappe.db.set_single_value('Accounts Settings', 'allow_stale', 1)
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-01', 'for_buying')
self.assertEqual(flt(exchange_rate, 3), 60.0)
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-15', 'for_buying')
self.assertEqual(exchange_rate, 65.1)
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-30', 'for_selling')
self.assertEqual(exchange_rate, 62.9)
self.clear_cache()
exchange_rate = get_exchange_rate('USD', 'INR', '2015-12-15', 'for_selling')
self.assertFalse(exchange_rate == 60)
self.assertEqual(flt(exchange_rate, 3), 66.999)
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-20', 'for_buying')
self.assertFalse(exchange_rate == 60)
self.assertEqual(flt(exchange_rate, 3), 65.1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/currency_exchange/test_currency_exchange.py:91*

### test_exchange_rate_via_exchangerate_host

**Category**: workflow  
**Description**: Workflow: test exchange rate via exchangerate host  
**Expected**: self.assertEqual(flt(exchange_rate, 3), 65.1)  
**Confidence**: 0.90  
**Tags**: unittest, mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get

save_new_records(self.globalTestRecords['Currency Exchange'])
settings = frappe.get_single('Currency Exchange Settings')
settings.service_provider = 'exchangerate.host'
settings.access_key = '12345667890'
settings.save()
frappe.db.set_single_value('Accounts Settings', 'allow_stale', 1)
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-01', 'for_buying')
self.assertEqual(flt(exchange_rate, 3), 60.0)
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-15', 'for_buying')
self.assertEqual(exchange_rate, 65.1)
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-30', 'for_selling')
self.assertEqual(exchange_rate, 62.9)
self.clear_cache()
exchange_rate = get_exchange_rate('USD', 'INR', '2015-12-15', 'for_selling')
self.assertFalse(exchange_rate == 60)
self.assertEqual(flt(exchange_rate, 3), 66.999)
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-20', 'for_buying')
self.assertFalse(exchange_rate == 60)
self.assertEqual(flt(exchange_rate, 3), 65.1)
settings = frappe.get_single('Currency Exchange Settings')
settings.service_provider = 'frankfurter.dev'
settings.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/currency_exchange/test_currency_exchange.py:116*

### test_exchange_rate_strict

**Category**: workflow  
**Description**: Workflow: test exchange rate strict  
**Expected**: self.assertEqual(flt(exchange_rate, 3), 66.999)  
**Confidence**: 0.90  
**Tags**: unittest, mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get

frappe.db.set_single_value('Accounts Settings', 'allow_stale', 0)
frappe.db.set_single_value('Accounts Settings', 'stale_days', 1)
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-01', 'for_buying')
self.assertEqual(exchange_rate, 60.0)
self.clear_cache()
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-15', 'for_buying')
self.assertEqual(flt(exchange_rate, 3), 65.1)
exchange_rate = get_exchange_rate('USD', 'INR', '2016-01-30', 'for_selling')
self.assertEqual(exchange_rate, 62.9)
self.clear_cache()
exchange_rate = get_exchange_rate('USD', 'INR', '2015-12-15', 'for_buying')
self.assertEqual(flt(exchange_rate, 3), 66.999)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/currency_exchange/test_currency_exchange.py:152*

### test_holiday_list

**Category**: workflow  
**Description**: Workflow: test holiday list  
**Expected**: self.assertEqual(holiday_list.name, fetched_holiday_list)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
today_date = getdate()
test_holiday_dates = [today_date - timedelta(days=5), today_date - timedelta(days=4)]
holiday_list = make_holiday_list('test_holiday_list', holiday_dates=[{'holiday_date': test_holiday_dates[0], 'description': 'test holiday'}, {'holiday_date': test_holiday_dates[1], 'description': 'test holiday2'}])
fetched_holiday_list = frappe.get_value('Holiday List', holiday_list.name)
self.assertEqual(holiday_list.name, fetched_holiday_list)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/holiday_list/test_holiday_list.py:14*

### test_weekly_off

**Category**: workflow  
**Description**: Workflow: test weekly off  
**Expected**: self.assertNotIn(date(2023, 3, 5), holidays)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
holiday_list = frappe.new_doc('Holiday List')
holiday_list.from_date = '2023-01-01'
holiday_list.to_date = '2023-02-28'
holiday_list.weekly_off = 'Sunday'
holiday_list.get_weekly_off_dates()
holidays = [holiday.holiday_date for holiday in holiday_list.holidays]
self.assertNotIn(date(2022, 12, 25), holidays)
self.assertIn(date(2023, 1, 1), holidays)
self.assertIn(date(2023, 1, 8), holidays)
self.assertIn(date(2023, 1, 15), holidays)
self.assertIn(date(2023, 1, 22), holidays)
self.assertIn(date(2023, 1, 29), holidays)
self.assertIn(date(2023, 2, 5), holidays)
self.assertIn(date(2023, 2, 12), holidays)
self.assertIn(date(2023, 2, 19), holidays)
self.assertIn(date(2023, 2, 26), holidays)
self.assertNotIn(date(2023, 3, 5), holidays)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/holiday_list/test_holiday_list.py:27*

### test_localized_country_names

**Category**: workflow  
**Description**: Workflow: test localized country names  
**Expected**: self.assertEqual(local_country_name('DE'), 'Deutschland')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
lang = frappe.local.lang
frappe.local.lang = 'en-gb'
self.assertEqual(local_country_name('IN'), 'India')
self.assertEqual(local_country_name('DE'), 'Germany')
frappe.local.lang = 'de'
self.assertEqual(local_country_name('DE'), 'Deutschland')
frappe.local.lang = lang
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/holiday_list/test_holiday_list.py:103*

### test_holiday_list

**Category**: workflow  
**Description**: Workflow: test holiday list  
**Expected**: self.assertEqual(holiday_list.name, fetched_holiday_list)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
today_date = getdate()
test_holiday_dates = [today_date - timedelta(days=5), today_date - timedelta(days=4)]
holiday_list = make_holiday_list('test_holiday_list', holiday_dates=[{'holiday_date': test_holiday_dates[0], 'description': 'test holiday'}, {'holiday_date': test_holiday_dates[1], 'description': 'test holiday2'}])
fetched_holiday_list = frappe.get_value('Holiday List', holiday_list.name)
self.assertEqual(holiday_list.name, fetched_holiday_list)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/holiday_list/test_holiday_list.py:14*

### test_weekly_off

**Category**: workflow  
**Description**: Workflow: test weekly off  
**Expected**: self.assertNotIn(date(2023, 3, 5), holidays)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
holiday_list = frappe.new_doc('Holiday List')
holiday_list.from_date = '2023-01-01'
holiday_list.to_date = '2023-02-28'
holiday_list.weekly_off = 'Sunday'
holiday_list.get_weekly_off_dates()
holidays = [holiday.holiday_date for holiday in holiday_list.holidays]
self.assertNotIn(date(2022, 12, 25), holidays)
self.assertIn(date(2023, 1, 1), holidays)
self.assertIn(date(2023, 1, 8), holidays)
self.assertIn(date(2023, 1, 15), holidays)
self.assertIn(date(2023, 1, 22), holidays)
self.assertIn(date(2023, 1, 29), holidays)
self.assertIn(date(2023, 2, 5), holidays)
self.assertIn(date(2023, 2, 12), holidays)
self.assertIn(date(2023, 2, 19), holidays)
self.assertIn(date(2023, 2, 26), holidays)
self.assertNotIn(date(2023, 3, 5), holidays)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/holiday_list/test_holiday_list.py:27*

### test_localized_country_names

**Category**: workflow  
**Description**: Workflow: test localized country names  
**Expected**: self.assertEqual(local_country_name('DE'), 'Deutschland')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
lang = frappe.local.lang
frappe.local.lang = 'en-gb'
self.assertEqual(local_country_name('IN'), 'India')
self.assertEqual(local_country_name('DE'), 'Germany')
frappe.local.lang = 'de'
self.assertEqual(local_country_name('DE'), 'Deutschland')
frappe.local.lang = lang
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/holiday_list/test_holiday_list.py:103*

### test_user_has_employee

**Category**: method_call  
**Description**: test user has employee  
**Expected**: self.assertTrue('Employee' not in frappe.get_roles(user))  
**Confidence**: 0.85  

```python
employee_doc.save()
self.assertTrue('Employee' not in frappe.get_roles(user))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/employee/test_employee.py:33*

### test_user_has_employee

**Category**: method_call  
**Description**: test user has employee  
**Expected**: self.assertTrue('Employee' not in frappe.get_roles(user))  
**Confidence**: 0.85  

```python
employee_doc.save()
self.assertTrue('Employee' not in frappe.get_roles(user))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/employee/test_employee.py:33*

### test_move_group_into_another

**Category**: method_call  
**Description**: test move group into another  
**Expected**: self.assertEqual(new_rgt - old_rgt, 0)  
**Confidence**: 0.85  

```python
self.assertEqual(old_lft - new_lft, rgt - lft + 1)
self.assertEqual(new_rgt - old_rgt, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/item_group/test_item_group.py:82*

### test_move_leaf_into_another_group

**Category**: method_call  
**Description**: test move leaf into another group  
**Expected**: self.assertEqual(new_rgt - old_rgt, rgt - lft + 1)  
**Confidence**: 0.85  

```python
self.assertEqual(old_lft - new_lft, 0)
self.assertEqual(new_rgt - old_rgt, rgt - lft + 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/item_group/test_item_group.py:114*

### test_primary_address

**Category**: method_call  
**Description**: test primary address  
**Expected**: self.assertEqual(get_default_company_address(company), primary.name)  
**Confidence**: 0.85  

```python
self.addCleanup(primary.delete)
self.assertEqual(get_default_company_address(company), primary.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/company/test_company.py:168*

### test_primary_address

**Category**: method_call  
**Description**: test primary address  
**Expected**: self.assertEqual(get_default_company_address(company), primary.name)  
**Confidence**: 0.85  

```python
self.addCleanup(primary.delete)
self.assertEqual(get_default_company_address(company), primary.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/company/test_company.py:168*

### test_exchange_rate

**Category**: method_call  
**Description**: test exchange rate  
**Expected**: self.assertEqual(flt(exchange_rate, 3), 66.999)  
**Confidence**: 0.85  
**Tags**: unittest, mock  

```python
self.assertFalse(exchange_rate == 60)
self.assertEqual(flt(exchange_rate, 3), 66.999)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/currency_exchange/test_currency_exchange.py:109*

### test_exchange_rate

**Category**: method_call  
**Description**: test exchange rate  
**Expected**: self.assertEqual(flt(exchange_rate, 3), 65.1)  
**Confidence**: 0.85  
**Tags**: unittest, mock  

```python
self.assertFalse(exchange_rate == 60)
self.assertEqual(flt(exchange_rate, 3), 65.1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/currency_exchange/test_currency_exchange.py:113*

### test_exchange_rate_via_exchangerate_host

**Category**: method_call  
**Description**: test exchange rate via exchangerate host  
**Expected**: self.assertEqual(flt(exchange_rate, 3), 66.999)  
**Confidence**: 0.85  
**Tags**: unittest, mock  

```python
self.assertFalse(exchange_rate == 60)
self.assertEqual(flt(exchange_rate, 3), 66.999)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/currency_exchange/test_currency_exchange.py:141*

### test_exchange_rate_via_exchangerate_host

**Category**: method_call  
**Description**: test exchange rate via exchangerate host  
**Expected**: self.assertEqual(flt(exchange_rate, 3), 65.1)  
**Confidence**: 0.85  
**Tags**: unittest, mock  

```python
self.assertFalse(exchange_rate == 60)
self.assertEqual(flt(exchange_rate, 3), 65.1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/currency_exchange/test_currency_exchange.py:145*

### test_weekly_off

**Category**: method_call  
**Description**: test weekly off  
**Expected**: self.assertIn(date(2023, 1, 1), holidays)  
**Confidence**: 0.85  

```python
self.assertNotIn(date(2022, 12, 25), holidays)
self.assertIn(date(2023, 1, 1), holidays)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/holiday_list/test_holiday_list.py:36*

### test_weekly_off

**Category**: method_call  
**Description**: test weekly off  
**Expected**: self.assertIn(date(2023, 1, 8), holidays)  
**Confidence**: 0.85  

```python
self.assertIn(date(2023, 1, 1), holidays)
self.assertIn(date(2023, 1, 8), holidays)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/holiday_list/test_holiday_list.py:37*

### test_weekly_off

**Category**: method_call  
**Description**: test weekly off  
**Expected**: self.assertIn(date(2023, 1, 15), holidays)  
**Confidence**: 0.85  

```python
self.assertIn(date(2023, 1, 8), holidays)
self.assertIn(date(2023, 1, 15), holidays)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/holiday_list/test_holiday_list.py:38*

### test_weekly_off

**Category**: method_call  
**Description**: test weekly off  
**Expected**: self.assertIn(date(2023, 1, 22), holidays)  
**Confidence**: 0.85  

```python
self.assertIn(date(2023, 1, 15), holidays)
self.assertIn(date(2023, 1, 22), holidays)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/holiday_list/test_holiday_list.py:39*

### test_renaming_vehicle

**Category**: method_call  
**Description**: test renaming vehicle  
**Expected**: self.assertEqual(new_license_plate, frappe.db.get_value('Vehicle', new_license_plate, 'license_plate'))  
**Confidence**: 0.85  

```python
frappe.rename_doc('Vehicle', license_plate, new_license_plate)
self.assertEqual(new_license_plate, frappe.db.get_value('Vehicle', new_license_plate, 'license_plate'))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/vehicle/test_vehicle.py:47*

### test_renaming_vehicle

**Category**: method_call  
**Description**: test renaming vehicle  
**Expected**: self.assertEqual(new_license_plate, frappe.db.get_value('Vehicle', new_license_plate, 'license_plate'))  
**Confidence**: 0.85  

```python
frappe.rename_doc('Vehicle', license_plate, new_license_plate)
self.assertEqual(new_license_plate, frappe.db.get_value('Vehicle', new_license_plate, 'license_plate'))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/vehicle/test_vehicle.py:47*

### test_employee_status_left

**Category**: instantiation  
**Description**: Instantiate make_employee: test employee status left  
**Expected**: self.assertRaises(InactiveEmployeeStatusError, employee1_doc.save)  
**Confidence**: 0.80  

```python
employee1 = make_employee('test_employee_1@company.com')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/employee/test_employee.py:16*

### test_employee_status_left

**Category**: instantiation  
**Description**: Instantiate make_employee: test employee status left  
**Expected**: self.assertRaises(InactiveEmployeeStatusError, employee1_doc.save)  
**Confidence**: 0.80  

```python
employee2 = make_employee('test_employee_2@company.com')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/employee/test_employee.py:17*

### test_coa_based_on_existing_company

**Category**: instantiation  
**Description**: Instantiate new_doc: test coa based on existing company  
**Confidence**: 0.80  

```python
company = frappe.new_doc('Company')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/company/test_company.py:27*

### test_coa_based_on_existing_company

**Category**: instantiation  
**Description**: Instantiate get_doc: test coa based on existing company  
**Confidence**: 0.80  

```python
acc = frappe.get_doc('Account', account)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/company/test_company.py:51*

### test_remove_department_data

**Category**: instantiation  
**Description**: Instantiate create_department: test remove department data  
**Confidence**: 0.80  

```python
doc = create_department('Test Department')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/department/test_department.py:12*

### test_remove_department_data

**Category**: instantiation  
**Description**: Instantiate create_department: test remove department data  
**Confidence**: 0.80  

```python
doc = create_department('Test Department')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/department/test_department.py:12*

### test_make_vehicle

**Category**: instantiation  
**Description**: Instantiate get_doc: test make vehicle  
**Confidence**: 0.80  

```python
vehicle = frappe.get_doc({'doctype': 'Vehicle', 'license_plate': random_string(10).upper(), 'make': 'Maruti', 'model': 'PCM', 'last_odometer': 5000, 'acquisition_date': frappe.utils.nowdate(), 'location': 'Mumbai', 'chassis_no': '1234ABCD', 'uom': 'Litre', 'vehicle_value': frappe.utils.flt(500000)})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/vehicle/test_vehicle.py:11*

### test_renaming_vehicle

**Category**: instantiation  
**Description**: Instantiate get_doc: test renaming vehicle  
**Expected**: self.assertEqual(new_license_plate, frappe.db.get_value('Vehicle', new_license_plate, 'license_plate'))  
**Confidence**: 0.80  

```python
vehicle = frappe.get_doc({'doctype': 'Vehicle', 'license_plate': license_plate, 'make': 'Skoda', 'model': 'Slavia', 'last_odometer': 5000, 'acquisition_date': frappe.utils.nowdate(), 'location': 'Mumbai', 'chassis_no': '1234EFGH', 'uom': 'Litre', 'vehicle_value': frappe.utils.flt(500000)})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/vehicle/test_vehicle.py:30*

### test_make_vehicle

**Category**: instantiation  
**Description**: Instantiate get_doc: test make vehicle  
**Confidence**: 0.80  

```python
vehicle = frappe.get_doc({'doctype': 'Vehicle', 'license_plate': random_string(10).upper(), 'make': 'Maruti', 'model': 'PCM', 'last_odometer': 5000, 'acquisition_date': frappe.utils.nowdate(), 'location': 'Mumbai', 'chassis_no': '1234ABCD', 'uom': 'Litre', 'vehicle_value': frappe.utils.flt(500000)})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/vehicle/test_vehicle.py:11*

### test_renaming_vehicle

**Category**: instantiation  
**Description**: Instantiate get_doc: test renaming vehicle  
**Expected**: self.assertEqual(new_license_plate, frappe.db.get_value('Vehicle', new_license_plate, 'license_plate'))  
**Confidence**: 0.80  

```python
vehicle = frappe.get_doc({'doctype': 'Vehicle', 'license_plate': license_plate, 'make': 'Skoda', 'model': 'Slavia', 'last_odometer': 5000, 'acquisition_date': frappe.utils.nowdate(), 'location': 'Mumbai', 'chassis_no': '1234EFGH', 'uom': 'Litre', 'vehicle_value': frappe.utils.flt(500000)})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/setup/doctype/vehicle/test_vehicle.py:30*

