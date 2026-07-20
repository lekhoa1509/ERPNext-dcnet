# API Reference: db_manager.py

**Language**: Python

**Source**: `database/db_manager.py`

---

## Classes

### DbManager

**Inherits from**: (none)

#### Methods

##### __init__(self, db: frappe.database.database.Database | None = None)

Pass root_conn here for access to all databases.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| db | frappe.database.database.Database | None | None | - |


##### get_current_host(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_user(self, user, password, host = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user | None | - | - |
| password | None | - | - |
| host | None | None | - |


##### delete_user(self, target, host = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| target | None | - | - |
| host | None | None | - |


##### create_database(self, target)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| target | None | - | - |


##### drop_database(self, target)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| target | None | - | - |


##### grant_all_privileges(self, target, user, host = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| target | None | - | - |
| user | None | - | - |
| host | None | None | - |


##### flush_privileges(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_database_list(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### restore_database(verbose: bool, target: str, source: str, user: str, password: str) → None

Function to restore the given SQL file to the target database.
:param target: The database to restore to.
:param source: The SQL dump to restore
:param user: The database username
:param password: The database password
:return: Nothing

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| verbose | bool | - | - |
| target | str | - | - |
| source | str | - | - |
| user | str | - | - |
| password | str | - | - |

**Returns**: `None`



