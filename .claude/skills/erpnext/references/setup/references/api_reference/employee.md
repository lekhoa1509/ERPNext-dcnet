# API Reference: employee.py

**Language**: Python

**Source**: `doctype/employee/employee.py`

---

## Classes

### EmployeeUserDisabledError

**Inherits from**: frappe.ValidationError



### InactiveEmployeeStatusError

**Inherits from**: frappe.ValidationError



### Employee

**Inherits from**: NestedSet

#### Methods

##### autoname(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### after_rename(self, old, new, merge)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| old | None | - | - |
| new | None | - | - |
| merge | None | - | - |


##### set_employee_name(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_user_details(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_nsm_model(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_user_permissions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_user(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_email(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_preferred_email(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_for_enabled_user_id(self, enabled)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| enabled | None | - | - |


##### validate_duplicate_user_id(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_reports_to(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_preferred_email(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### reset_employee_emails_cache(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### validate_employee_role(doc, method = None, ignore_emp_check = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| method | None | None | - |
| ignore_emp_check | None | False | - |

**Returns**: (none)



### get_employee_email(employee_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| employee_doc | None | - | - |

**Returns**: (none)



### get_holiday_list_for_employee(employee, raise_exception = True, as_on = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| employee | None | - | - |
| raise_exception | None | True | - |
| as_on | None | None | - |

**Returns**: (none)



### is_holiday(employee, date = None, raise_exception = True, only_non_weekly = False, with_description = False)

Returns True if given Employee has an holiday on the given date
        :param employee: Employee `name`
        :param date: Date to check. Will check for today if None
        :param raise_exception: Raise an exception if no holiday list found, default is True
        :param only_non_weekly: Check only non-weekly holidays, default is False

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| employee | None | - | - |
| date | None | None | - |
| raise_exception | None | True | - |
| only_non_weekly | None | False | - |
| with_description | None | False | - |

**Returns**: (none)



### deactivate_sales_person(status = None, employee = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| status | None | None | - |
| employee | None | None | - |

**Returns**: (none)



### create_user(employee, user = None, email = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| employee | None | - | - |
| user | None | None | - |
| email | None | None | - |

**Returns**: (none)



### get_all_employee_emails(company)

Returns list of employee emails either based on user_id or company_email

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |

**Returns**: (none)



### get_employee_emails(employee_list)

Returns list of employee emails either based on user_id or company_email

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| employee_list | None | - | - |

**Returns**: (none)



### get_children(doctype, parent = None, company = None, is_root = False, is_tree = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| parent | None | None | - |
| company | None | None | - |
| is_root | None | False | - |
| is_tree | None | False | - |

**Returns**: (none)



### on_doctype_update()

**Returns**: (none)



### has_user_permission_for_employee(user_name, employee_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user_name | None | - | - |
| employee_name | None | - | - |

**Returns**: (none)



### has_upload_permission(doc, ptype = 'read', user = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| ptype | None | 'read' | - |
| user | None | None | - |

**Returns**: (none)


