# API Reference: backups.py

**Language**: Python

**Source**: `utils/backups.py`

---

## Classes

### BackupGenerator

This class contains methods to perform On Demand Backup

To initialize, specify (db_name, user, password, db_file_name=None, db_host="127.0.0.1")
If specifying db_file_name, also append ".sql.gz"

**Inherits from**: (none)

#### Methods

##### __init__(self, db_name, user, password, backup_path = None, backup_path_db = None, backup_path_files = None, backup_path_private_files = None, db_socket = None, db_host = None, db_port = None, db_type = None, backup_path_conf = None, ignore_conf = False, compress_files = False, include_doctypes = '', exclude_doctypes = '', verbose = False, old_backup_metadata = False, rollback_callback = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| db_name | None | - | - |
| user | None | - | - |
| password | None | - | - |
| backup_path | None | None | - |
| backup_path_db | None | None | - |
| backup_path_files | None | None | - |
| backup_path_private_files | None | None | - |
| db_socket | None | None | - |
| db_host | None | None | - |
| db_port | None | None | - |
| db_type | None | None | - |
| backup_path_conf | None | None | - |
| ignore_conf | None | False | - |
| compress_files | None | False | - |
| include_doctypes | None | '' | - |
| exclude_doctypes | None | '' | - |
| verbose | None | False | - |
| old_backup_metadata | None | False | - |
| rollback_callback | None | None | - |


##### setup_backup_directory(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _set_existing_tables(self)

Ensure self._existing_tables is set.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### setup_backup_tables(self)

Set self.backup_includes, self.backup_excludes based on include_doctypes, exclude_doctypes

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_backup_tables_from_config(self)

Set self.backup_includes, self.backup_excludes based on site config

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### site_config_backup_path(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_backup(self, older_than = 24, ignore_files = False, force = False)

Takes a new dump if existing file is old
and sends the link to the file as email

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| older_than | None | 24 | - |
| ignore_files | None | False | - |
| force | None | False | - |


##### set_backup_file_name(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### backup_encryption(self)

Encrypt all the backups created using gpg.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_recent_backup(self, older_than, partial = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| older_than | None | - | - |
| partial | None | False | - |


##### zip_files(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_summary(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### print_summary(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### backup_files(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### copy_site_config(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### take_dump(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### send_email(self)

Sends the link to backup file located at erpnext/backups

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_to_rollback(self, func: Callable) → None

Adds the given callable to the rollback CallbackManager stack

:param func: The callable to add to the rollback stack
:return: Nothing

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| func | Callable | - | - |

**Returns**: `None`


##### delete_if_step_fails(self, step: Callable)

Deletes the given path if the given step fails

:param step: The step to execute
:param paths: The paths to delete
:return: Nothing

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| step | Callable | - | - |




## Functions

### _get_tables(doctypes: list[str], existing_tables: list[str]) → list[str]

Return a list of tables for the given doctypes that exist in the database.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctypes | list[str] | - | - |
| existing_tables | list[str] | - | - |

**Returns**: `list[str]`



### fetch_latest_backups(partial = False) → dict

Fetch paths of the latest backup taken in the last 30 days.

Note: Only for System Managers

Return:
        dict: relative Backup Paths

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| partial | None | False | - |

**Returns**: `dict`



### scheduled_backup(older_than = 6, ignore_files = False, backup_path = None, backup_path_db = None, backup_path_files = None, backup_path_private_files = None, backup_path_conf = None, ignore_conf = False, include_doctypes = '', exclude_doctypes = '', compress = False, force = False, verbose = False, old_backup_metadata = False, rollback_callback = None)

this function is called from scheduler
deletes backups older than 7 days
takes backup

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| older_than | None | 6 | - |
| ignore_files | None | False | - |
| backup_path | None | None | - |
| backup_path_db | None | None | - |
| backup_path_files | None | None | - |
| backup_path_private_files | None | None | - |
| backup_path_conf | None | None | - |
| ignore_conf | None | False | - |
| include_doctypes | None | '' | - |
| exclude_doctypes | None | '' | - |
| compress | None | False | - |
| force | None | False | - |
| verbose | None | False | - |
| old_backup_metadata | None | False | - |
| rollback_callback | None | None | - |

**Returns**: (none)



### new_backup(older_than = 6, ignore_files = False, backup_path = None, backup_path_db = None, backup_path_files = None, backup_path_private_files = None, backup_path_conf = None, ignore_conf = False, include_doctypes = '', exclude_doctypes = '', compress = False, force = False, verbose = False, old_backup_metadata = False, rollback_callback = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| older_than | None | 6 | - |
| ignore_files | None | False | - |
| backup_path | None | None | - |
| backup_path_db | None | None | - |
| backup_path_files | None | None | - |
| backup_path_private_files | None | None | - |
| backup_path_conf | None | None | - |
| ignore_conf | None | False | - |
| include_doctypes | None | '' | - |
| exclude_doctypes | None | '' | - |
| compress | None | False | - |
| force | None | False | - |
| verbose | None | False | - |
| old_backup_metadata | None | False | - |
| rollback_callback | None | None | - |

**Returns**: (none)



### delete_temp_backups(older_than = 24)

Cleans up the backup_link_path directory by deleting older files

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| older_than | None | 24 | - |

**Returns**: (none)



### is_file_old(file_path, older_than = 24) → bool

Return True if file exists and is older than specified hours.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| file_path | None | - | - |
| older_than | None | 24 | - |

**Returns**: `bool`



### get_backup_path()

**Returns**: (none)



### get_backup_encryption_key()

**Returns**: (none)



### get_or_generate_backup_encryption_key()

**Returns**: (none)



### decrypt_backup(file_path: str, passphrase: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| file_path | str | - | - |
| passphrase | str | - | - |

**Returns**: (none)



### backup(with_files = False, backup_path_db = None, backup_path_files = None, backup_path_private_files = None, backup_path_conf = None)

Backup

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| with_files | None | False | - |
| backup_path_db | None | None | - |
| backup_path_files | None | None | - |
| backup_path_private_files | None | None | - |
| backup_path_conf | None | None | - |

**Returns**: (none)



### backup_time(file_path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| file_path | None | - | - |

**Returns**: (none)



### get_latest(file_pattern)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| file_pattern | None | - | - |

**Returns**: (none)



### old_enough(file_path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| file_path | None | - | - |

**Returns**: (none)


