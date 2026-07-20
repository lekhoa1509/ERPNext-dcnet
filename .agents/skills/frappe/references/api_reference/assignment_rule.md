# API Reference: assignment_rule.py

**Language**: Python

**Source**: `automation/doctype/assignment_rule/assignment_rule.py`

---

## Classes

### AssignmentRule

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### clear_cache(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_document_types(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_assignment_days(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### apply_unassign(self, doc, assignments)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |
| assignments | None | - | - |


##### apply_assign(self, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### do_assignment(self, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### clear_assignment(self, doc)

Clear assignments

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### close_assignments(self, doc)

Close assignments

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### get_user(self, doc)

Get the next user for assignment

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### get_user_round_robin(self)

Get next user based on round robin

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_user_load_balancing(self)

Assign to the user with least number of open assignments

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_user_based_on_field(self, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### safe_eval(self, fieldname, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | None | - | - |
| doc | None | - | - |


##### get_assignment_days(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_rule_not_applicable_today(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_assignments(doc) → list[dict]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: `list[dict]`



### bulk_apply(doctype, docnames)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| docnames | None | - | - |

**Returns**: (none)



### reopen_closed_assignment(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### apply(doc = None, method = None, doctype = None, name = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | None | - |
| method | None | None | - |
| doctype | None | None | - |
| name | None | None | - |

**Returns**: (none)



### update_due_date(doc, state = None)

Run on_update on every Document (via hooks.py)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| state | None | None | - |

**Returns**: (none)



### get_assignment_rules() → list[str]

**Returns**: `list[str]`



### get_repeated(values: Iterable) → list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| values | Iterable | - | - |

**Returns**: `list`


