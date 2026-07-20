# API Reference: test_commands.py

**Language**: Python

**Source**: `commands/test_commands.py`

---

## Classes

### BaseTestCommands

**Inherits from**: IntegrationTestCase

#### Methods

##### setUpClass(cls) → None

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |

**Returns**: `None`


##### execute(self, command, kwargs = None)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| command | None | - | - |
| kwargs | None | None | - |


##### setup_test_site(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### _formatMessage(self, msg, standardMsg)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| msg | None | - | - |
| standardMsg | None | - | - |




### TestCommands

**Inherits from**: BaseTestCommands

#### Methods

##### test_execute(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_restore(self)

**Decorators**: `@skipIf(frappe.conf.db_type == 'sqlite', 'Not for SQLite for now')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_partial_restore(self)

**Decorators**: `@skipIf(frappe.conf.db_type == 'sqlite', 'Not for SQLite for now')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_recorder(self)

**Decorators**: `@skipIf(frappe.conf.db_type == 'sqlite', 'Not for SQLite for now')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_remove_from_installed_apps(self)

**Decorators**: `@unittest.skip('Poorly written, relied on app name being absent in apps.txt')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_list_apps(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_show_config(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_bench_relative_path(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_frappe_site_env(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_version(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_set_password(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bench_drop_site_should_archive_site(self)

**Decorators**: `@skipIf(not (frappe.conf.root_password and frappe.conf.admin_password and (frappe.conf.db_type != 'sqlite')), 'DB Root password and Admin password not set in config')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_force_install_app(self)

**Decorators**: `@skipIf(not (frappe.conf.root_password and frappe.conf.admin_password and (frappe.conf.db_type != 'sqlite')), 'DB Root password and Admin password not set in config')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_set_global_conf(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_different_db_username(self)

**Decorators**: `@skipIf(frappe.conf.db_type == 'sqlite', 'Not for SQLite for now')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_existing_db_username(self)

**Decorators**: `@skipIf(frappe.conf.db_type == 'sqlite', 'Not for SQLite for now')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestBackups

**Inherits from**: BaseTestCommands

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backup_no_options(self)

Take a backup without any options

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backup_extract_restore(self)

Restore a backup after extracting

**Decorators**: `@skipIf(not frappe.conf.db_type == 'mariadb', 'Only for MariaDB')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_old_backup_restore(self)

Restore a backup after extracting

**Decorators**: `@skipIf(not frappe.conf.db_type == 'mariadb', 'Only for MariaDB')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backup_fails_with_exit_code(self)

Provide incorrect options to check if exit code is 1

**Decorators**: `@skipIf(frappe.conf.db_type == 'sqlite', 'Not for SQLite for now')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backup_with_files(self)

Take a backup with files (--with-files)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_clear_log_table(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backup_with_custom_path(self)

Backup to a custom path (--backup-path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backup_with_different_file_paths(self)

Backup with different file paths (--backup-path-db, --backup-path-files, --backup-path-private-files, --backup-path-conf)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backup_compress_files(self)

Take a compressed backup (--compress)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backup_verbose(self)

Take a verbose backup (--verbose)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backup_only_specific_doctypes(self)

Take a backup with (include) backup options set in the site config `frappe.conf.backup.includes`

**Decorators**: `@skipIf(frappe.conf.db_type == 'sqlite', 'Not for SQLite for now')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backup_excluding_specific_doctypes(self)

Take a backup with (exclude) backup options set (`frappe.conf.backup.excludes`, `--exclude`)

**Decorators**: `@skipIf(frappe.conf.db_type == 'sqlite', 'Not for SQLite for now')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_selective_backup_priority_resolution(self)

Take a backup with conflicting backup options set (`frappe.conf.excludes`, `--include`)

**Decorators**: `@skipIf(frappe.conf.db_type == 'sqlite', 'Not for SQLite for now')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_dont_backup_conf(self)

Take a backup ignoring frappe.conf.backup settings (with --ignore-backup-conf option)

**Decorators**: `@skipIf(frappe.conf.db_type == 'sqlite', 'Not for SQLite for now')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestRemoveApp

**Inherits from**: IntegrationTestCase

#### Methods

##### test_delete_modules(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_dry_run(self)

Check if dry run in not destructive.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestSiteMigration

**Inherits from**: BaseTestCommands

#### Methods

##### test_migrate_cli(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestAddNewUser

**Inherits from**: BaseTestCommands

#### Methods

##### test_create_user(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestBenchBuild

**Inherits from**: IntegrationTestCase

#### Methods

##### test_build_assets_size_check(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestDBUtils

**Inherits from**: BaseTestCommands

#### Methods

##### test_db_add_index(self)

**Decorators**: `@skipIf(not frappe.conf.db_type == 'mariadb', 'Only for MariaDB')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestSchedulerUtils

**Inherits from**: BaseTestCommands

#### Methods

##### test_ready_for_migrate(self)

**Decorators**: `@retry(retry=retry_if_exception_type(AssertionError), stop=stop_after_attempt(3), wait=wait_fixed(3), reraise=True)`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestCommandUtils

**Inherits from**: IntegrationTestCase

#### Methods

##### test_bench_helper(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestDBCli

**Inherits from**: BaseTestCommands

#### Methods

##### test_db_cli(self)

**Decorators**: `@timeout(10)`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_db_cli_with_sql(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestSchedulerCLI

**Inherits from**: BaseTestCommands

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### tearDownClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### test_scheduler_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_scheduler_enable_disable(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_scheduler_pause_resume(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestCLIImplementation

**Inherits from**: BaseTestCommands

#### Methods

##### test_missing_commands(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestGunicornWorker

**Inherits from**: IntegrationTestCase

#### Methods

##### spawn_gunicorn(self, args = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| args | None | None | - |


##### kill_gunicorn(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_gunicorn_ping_sync(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_gunicorn_ping_gthread(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_gunicorn_idle_cpu_usage(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestRQWorker

**Inherits from**: IntegrationTestCase

#### Methods

##### spawn_rq(self, args = None, pool = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| args | None | None | - |
| pool | None | False | - |


##### kill_rq(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_total_usage(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_rq_idle_cpu_usage(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_rq_pool_idle_cpu_usage(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### clean(value) → str

Strip and convert bytes to str.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| value | None | - | - |

**Returns**: `str`



### missing_in_backup(doctypes: list, file: os.PathLike) → list

Return list of missing doctypes in the backup.

Args:
        doctypes (list): List of DocTypes to be checked
        file (str): Path of the database file

Return:
        doctypes(list): doctypes that are missing in backup

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctypes | list | - | - |
| file | os.PathLike | - | - |

**Returns**: `list`



### exists_in_backup(doctypes: list, file: os.PathLike) → bool

Check if the list of doctypes exist in the database.sql.gz file supplied.

Args:
        doctypes (list): List of DocTypes to be checked
        file (str): Path of the database file

Return True if all tables exist.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctypes | list | - | - |
| file | os.PathLike | - | - |

**Returns**: `bool`



### maintain_locals()

**Returns**: (none)



### pass_test_context(f)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| f | None | - | - |

**Returns**: (none)



### cli(cmd: Command, args: list | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cmd | Command | - | - |
| args | list | None | None | - |

**Returns**: (none)



### decorated_function()

**Returns**: (none)



### get_total_usage()

**Returns**: (none)


