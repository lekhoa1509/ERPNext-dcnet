# API Reference: server_script.py

**Language**: Python

**Source**: `core/doctype/server_script/server_script.py`

---

## Classes

### ServerScript

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### clear_cache(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_code_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### scheduled_jobs(self) → list[dict[str, str]]

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `list[dict[str, str]]`


##### sync_scheduled_job_type(self)

Create or update Scheduled Job Type documents for Scheduler Event Server Scripts

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_if_compilable_in_restricted_context(self)

Check compilation errors and send them back as warnings.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### execute_method(self) → dict

Specific to API endpoint Server Scripts.

Raise:
        frappe.DoesNotExistError: If self.script_type is not API.
        frappe.PermissionError: If self.allow_guest is unset for API accessed by Guest user.

Return:
        dict: Evaluate self.script with frappe.utils.safe_exec.safe_exec and return the flags set in its safe globals.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `dict`


##### execute_doc(self, doc: Document)

Specific to Document Event triggered Server Scripts

Args:
        doc (Document): Executes script with for a certain document's events

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | Document | - | - |


##### execute_scheduled_method(self)

Specific to Scheduled Jobs via Server Scripts

Raises:
        frappe.DoesNotExistError: If script type is not a scheduler event

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_permission_query_conditions(self, user: str) → list[str]

Specific to Permission Query Server Scripts.

Args:
        user (str): Take user email to execute script and return list of conditions.

Return:
        list: Return list of conditions defined by rules in self.script.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user | str | - | - |

**Returns**: `list[str]`


##### execute_workflow_task(self, doc: Document)

Specific to Workflow Tasks via Workflow Action Master

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | Document | - | - |




## Functions

### get_autocompletion_items()

Generate a list of autocompletion strings from the context dict
that is used while executing a Server Script.

e.g., ["frappe.utils.cint", "frappe.get_all", ...]

**Returns**: (none)



### execute_api_server_script(script: ServerScript)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| script | ServerScript | - | - |

**Returns**: (none)



### enabled() → bool | None

**Returns**: `bool | None`



### get_scheduled_job() → 'ScheduledJobType'

**Returns**: `'ScheduledJobType'`


