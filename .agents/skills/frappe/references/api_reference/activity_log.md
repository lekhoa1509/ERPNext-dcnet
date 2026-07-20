# API Reference: activity_log.py

**Language**: Python

**Source**: `core/doctype/activity_log/activity_log.py`

---

## Classes

### ActivityLog

**Inherits from**: Document

#### Methods

##### before_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_ip_address(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### clear_old_logs(days = None)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| days | None | None | - |




## Functions

### on_doctype_update()

Add indexes in `tabActivity Log`

**Returns**: (none)



### add_authentication_log(subject, user, operation = 'Login', status = 'Success')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| subject | None | - | - |
| user | None | - | - |
| operation | None | 'Login' | - |
| status | None | 'Success' | - |

**Returns**: (none)


