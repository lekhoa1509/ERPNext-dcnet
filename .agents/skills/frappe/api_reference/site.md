# API Reference: site.py

**Language**: Python

**Source**: `commands/site.py`

---

## Functions

### new_site(site, db_root_username = None, db_root_password = None, admin_password = None, verbose = False, source_sql = None, force = None, no_mariadb_socket = False, mariadb_user_host_login_scope = False, install_app = None, db_name = None, db_password = None, db_type = None, db_socket = None, db_host = None, db_port = None, db_user = None, set_default = False, setup_db = True)

Create a new site

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| site | None | - | - |
| db_root_username | None | None | - |
| db_root_password | None | None | - |
| admin_password | None | None | - |
| verbose | None | False | - |
| source_sql | None | None | - |
| force | None | None | - |
| no_mariadb_socket | None | False | - |
| mariadb_user_host_login_scope | None | False | - |
| install_app | None | None | - |
| db_name | None | None | - |
| db_password | None | None | - |
| db_type | None | None | - |
| db_socket | None | None | - |
| db_host | None | None | - |
| db_port | None | None | - |
| db_user | None | None | - |
| set_default | None | False | - |
| setup_db | None | True | - |

**Returns**: (none)



### restore(context: CliCtxObj, sql_file_path, encryption_key = None, db_root_username = None, db_root_password = None, db_name = None, verbose = None, install_app = None, admin_password = None, force = None, with_public_files = None, with_private_files = None)

Restore site database from an sql file

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| sql_file_path | None | - | - |
| encryption_key | None | None | - |
| db_root_username | None | None | - |
| db_root_password | None | None | - |
| db_name | None | None | - |
| verbose | None | None | - |
| install_app | None | None | - |
| admin_password | None | None | - |
| force | None | None | - |
| with_public_files | None | None | - |
| with_private_files | None | None | - |

**Returns**: (none)



### _restore()

**Returns**: (none)



### restore_backup(sql_file_path: str, site, db_root_username, db_root_password, verbose, install_app, admin_password, force)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sql_file_path | str | - | - |
| site | None | - | - |
| db_root_username | None | - | - |
| db_root_password | None | - | - |
| verbose | None | - | - |
| install_app | None | - | - |
| admin_password | None | - | - |
| force | None | - | - |

**Returns**: (none)



### partial_restore(context: CliCtxObj, sql_file_path, verbose, encryption_key = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| sql_file_path | None | - | - |
| verbose | None | - | - |
| encryption_key | None | None | - |

**Returns**: (none)



### reinstall(context: CliCtxObj, admin_password = None, db_root_username = None, db_root_password = None, yes = False)

Reinstall site ie. wipe all data and start over

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| admin_password | None | None | - |
| db_root_username | None | None | - |
| db_root_password | None | None | - |
| yes | None | False | - |

**Returns**: (none)



### _reinstall(site, admin_password = None, db_root_username = None, db_root_password = None, yes = False, verbose = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| site | None | - | - |
| admin_password | None | None | - |
| db_root_username | None | None | - |
| db_root_password | None | None | - |
| yes | None | False | - |
| verbose | None | False | - |

**Returns**: (none)



### install_app(context: CliCtxObj, apps, force = False)

Install a new app to site, supports multiple apps

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| apps | None | - | - |
| force | None | False | - |

**Returns**: (none)



### list_apps(context: CliCtxObj, format)

List apps in site.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| format | None | - | - |

**Returns**: (none)



### add_db_index(context: CliCtxObj, doctype, column)

Adds a new DB index and creates a property setter to persist it.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| doctype | None | - | - |
| column | None | - | - |

**Returns**: (none)



### describe_database_table(context, doctype, column)

Describes various statistics about the table.
This is useful to build integration like
This includes:
1. Schema
2. Indexes
3. stats - total count of records
4. if column is specified then extra stats are generated for column:
        Distinct values count in column

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | None | - | - |
| doctype | None | - | - |
| column | None | - | - |

**Returns**: (none)



### add_system_manager(context: CliCtxObj, email, first_name, last_name, send_welcome_email, password)

Add a new system manager to a site

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| email | None | - | - |
| first_name | None | - | - |
| last_name | None | - | - |
| send_welcome_email | None | - | - |
| password | None | - | - |

**Returns**: (none)



### add_user_for_sites(context: CliCtxObj, email, first_name, last_name, user_type, send_welcome_email, password, add_role)

Add user to a site

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| email | None | - | - |
| first_name | None | - | - |
| last_name | None | - | - |
| user_type | None | - | - |
| send_welcome_email | None | - | - |
| password | None | - | - |
| add_role | None | - | - |

**Returns**: (none)



### disable_user(context: CliCtxObj, email)

Disable a user account on site.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| email | None | - | - |

**Returns**: (none)



### migrate(context: CliCtxObj, skip_failing = False, skip_search_index = False, skip_fixtures = False)

Run patches, sync schema and rebuild files/translations

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| skip_failing | None | False | - |
| skip_search_index | None | False | - |
| skip_fixtures | None | False | - |

**Returns**: (none)



### migrate_to()

Migrates site to the specified provider

**Returns**: (none)



### run_patch(context: CliCtxObj, module, force)

Run a particular patch

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| module | None | - | - |
| force | None | - | - |

**Returns**: (none)



### reload_doc(context: CliCtxObj, module, doctype, docname)

Reload schema for a DocType

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| module | None | - | - |
| doctype | None | - | - |
| docname | None | - | - |

**Returns**: (none)



### reload_doctype(context: CliCtxObj, doctype)

Reload schema for a DocType

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| doctype | None | - | - |

**Returns**: (none)



### add_to_hosts(context: CliCtxObj)

Add site to hosts

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |

**Returns**: (none)



### _use(site, sites_path = '.')

Set a default site

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| site | None | - | - |
| sites_path | None | '.' | - |

**Returns**: (none)



### use(site, sites_path = '.')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| site | None | - | - |
| sites_path | None | '.' | - |

**Returns**: (none)



### backup(context: CliCtxObj, with_files = False, backup_path = None, backup_path_db = None, backup_path_files = None, backup_path_private_files = None, backup_path_conf = None, ignore_backup_conf = False, verbose = False, compress = False, include = '', exclude = '', old_backup_metadata = False)

Backup

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| with_files | None | False | - |
| backup_path | None | None | - |
| backup_path_db | None | None | - |
| backup_path_files | None | None | - |
| backup_path_private_files | None | None | - |
| backup_path_conf | None | None | - |
| ignore_backup_conf | None | False | - |
| verbose | None | False | - |
| compress | None | False | - |
| include | None | '' | - |
| exclude | None | '' | - |
| old_backup_metadata | None | False | - |

**Returns**: (none)



### remove_from_installed_apps(context: CliCtxObj, app)

Remove app from site's installed-apps list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| app | None | - | - |

**Returns**: (none)



### uninstall(context: CliCtxObj, app, dry_run, yes, no_backup, force)

Remove app and linked modules from site

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| app | None | - | - |
| dry_run | None | - | - |
| yes | None | - | - |
| no_backup | None | - | - |
| force | None | - | - |

**Returns**: (none)



### drop_site(site, db_root_username = 'root', db_root_password = None, archived_sites_path = None, force = False, no_backup = False)

Remove a site from database and filesystem.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| site | None | - | - |
| db_root_username | None | 'root' | - |
| db_root_password | None | None | - |
| archived_sites_path | None | None | - |
| force | None | False | - |
| no_backup | None | False | - |

**Returns**: (none)



### _drop_site(site, db_root_username = None, db_root_password = None, archived_sites_path = None, force = False, no_backup = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| site | None | - | - |
| db_root_username | None | None | - |
| db_root_password | None | None | - |
| archived_sites_path | None | None | - |
| force | None | False | - |
| no_backup | None | False | - |

**Returns**: (none)



### move(dest_dir, site)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dest_dir | None | - | - |
| site | None | - | - |

**Returns**: (none)



### set_password(context: CliCtxObj, user, password = None, logout_all_sessions = False)

Set password for a user on a site

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| user | None | - | - |
| password | None | None | - |
| logout_all_sessions | None | False | - |

**Returns**: (none)



### set_admin_password(context: CliCtxObj, admin_password = None, logout_all_sessions = False)

Set Administrator password for a site

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| admin_password | None | None | - |
| logout_all_sessions | None | False | - |

**Returns**: (none)



### set_user_password(site, user, password, logout_all_sessions = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| site | None | - | - |
| user | None | - | - |
| password | None | - | - |
| logout_all_sessions | None | False | - |

**Returns**: (none)



### set_last_active_for_user(context: CliCtxObj, user = None)

Set users last active date to current datetime

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| user | None | None | - |

**Returns**: (none)



### publish_realtime(context: CliCtxObj, event, message, room, user, doctype, docname, after_commit)

Publish realtime event from bench

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| event | None | - | - |
| message | None | - | - |
| room | None | - | - |
| user | None | - | - |
| doctype | None | - | - |
| docname | None | - | - |
| after_commit | None | - | - |

**Returns**: (none)



### browse(context: CliCtxObj, site, user: str | None = None, session_end: str | None = None, user_for_audit: str | None = None)

Opens the site on web browser

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| site | None | - | - |
| user | str | None | None | - |
| session_end | str | None | None | - |
| user_for_audit | str | None | None | - |

**Returns**: (none)



### start_recording(context: CliCtxObj)

Start Frappe Recorder.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |

**Returns**: (none)



### stop_recording(context: CliCtxObj)

Stop Frappe Recorder.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |

**Returns**: (none)



### start_ngrok(context: CliCtxObj, bind_tls, use_default_authtoken)

Start a ngrok tunnel to your local development server.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| bind_tls | None | - | - |
| use_default_authtoken | None | - | - |

**Returns**: (none)



### build_search_index(context)

Rebuild search index used by global search.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | None | - | - |

**Returns**: (none)



### clear_log_table(context: CliCtxObj, doctype, days, no_backup)

If any logtype table grows too large then clearing it with DELETE query
is not feasible in reasonable time. This command copies recent data to new
table and replaces current table with new smaller table.


ref: https://mariadb.com/kb/en/big-deletes/#deleting-more-than-half-a-table

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| doctype | None | - | - |
| days | None | - | - |
| no_backup | None | - | - |

**Returns**: (none)



### trim_database(context: CliCtxObj, dry_run, format, no_backup, yes = False)

Remove database tables for deleted DocTypes.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| dry_run | None | - | - |
| format | None | - | - |
| no_backup | None | - | - |
| yes | None | False | - |

**Returns**: (none)



### get_standard_tables()

**Returns**: (none)



### trim_tables(context: CliCtxObj, dry_run, format, no_backup)

Remove columns from tables where fields are deleted from doctypes.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| dry_run | None | - | - |
| format | None | - | - |
| no_backup | None | - | - |

**Returns**: (none)



### handle_data(data: dict, format = 'json')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | dict | - | - |
| format | None | 'json' | - |

**Returns**: (none)



### add_new_user(email, first_name = None, last_name = None, user_type = 'System User', send_welcome_email = False, password = None, role = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email | None | - | - |
| first_name | None | None | - |
| last_name | None | None | - |
| user_type | None | 'System User' | - |
| send_welcome_email | None | False | - |
| password | None | None | - |
| role | None | None | - |

**Returns**: (none)



### ensure_app_not_frappe(app: str) → None

Ensure that the app name passed is not 'frappe'

:param app: Name of the app
:return: Nothing

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | str | - | - |

**Returns**: `None`



### bypass_patch(context: CliCtxObj, patch_name: str, yes: bool)

Bypass a patch permanently instead of migrating using the --skip-failing flag.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| patch_name | str | - | - |
| yes | bool | - | - |

**Returns**: (none)



### create_icons_and_sidebar(context: CliCtxObj)

Create desktop icons and workspace sidebars.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |

**Returns**: (none)



### format_app(app)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | None | - | - |

**Returns**: (none)


