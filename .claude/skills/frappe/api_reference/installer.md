# API Reference: installer.py

**Language**: Python

**Source**: `installer.py`

---

## Functions

### _is_scheduler_enabled(site) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| site | None | - | - |

**Returns**: `bool`



### _new_site(db_name, site, db_root_username = None, db_root_password = None, admin_password = None, verbose = False, install_apps = None, source_sql = None, force = False, db_password = None, db_type = None, db_socket = None, db_host = None, db_port = None, db_user = None, setup_db = True, rollback_callback = None, mariadb_user_host_login_scope = None)

Install a new Frappe site

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| db_name | None | - | - |
| site | None | - | - |
| db_root_username | None | None | - |
| db_root_password | None | None | - |
| admin_password | None | None | - |
| verbose | None | False | - |
| install_apps | None | None | - |
| source_sql | None | None | - |
| force | None | False | - |
| db_password | None | None | - |
| db_type | None | None | - |
| db_socket | None | None | - |
| db_host | None | None | - |
| db_port | None | None | - |
| db_user | None | None | - |
| setup_db | None | True | - |
| rollback_callback | None | None | - |
| mariadb_user_host_login_scope | None | None | - |

**Returns**: (none)



### install_db(root_login = None, root_password = None, db_name = None, source_sql = None, admin_password = None, verbose = True, force = 0, site_config = None, db_password = None, db_type = None, db_socket = None, db_host = None, db_port = None, db_user = None, setup = True, rollback_callback = None, mariadb_user_host_login_scope = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| root_login | None | None | - |
| root_password | None | None | - |
| db_name | None | None | - |
| source_sql | None | None | - |
| admin_password | None | None | - |
| verbose | None | True | - |
| force | None | 0 | - |
| site_config | None | None | - |
| db_password | None | None | - |
| db_type | None | None | - |
| db_socket | None | None | - |
| db_host | None | None | - |
| db_port | None | None | - |
| db_user | None | None | - |
| setup | None | True | - |
| rollback_callback | None | None | - |
| mariadb_user_host_login_scope | None | None | - |

**Returns**: (none)



### find_org(org_repo: str) → tuple[str, str]

find the org a repo is in

find_org()
ref -> https://github.com/frappe/bench/blob/develop/bench/utils/__init__.py#L390

:param org_repo:
:type org_repo: str

:raises InvalidRemoteException: if the org is not found

:return: organisation and repository
:rtype: Tuple[str, str]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| org_repo | str | - | - |

**Returns**: `tuple[str, str]`



### fetch_details_from_tag(_tag: str) → tuple[str, str, str]

parse org, repo, tag from string

fetch_details_from_tag()
ref -> https://github.com/frappe/bench/blob/develop/bench/utils/__init__.py#L403

:param _tag: input string
:type _tag: str

:return: organisation, repostitory, tag
:rtype: Tuple[str, str, str]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| _tag | str | - | - |

**Returns**: `tuple[str, str, str]`



### parse_app_name(name: str) → str

parse repo name from name

__setup_details_from_git()
ref -> https://github.com/frappe/bench/blob/develop/bench/app.py#L114


:param name: git tag
:type name: str

:return: repository name
:rtype: str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | str | - | - |

**Returns**: `str`



### install_app(name, verbose = False, set_as_patched = True, force = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |
| verbose | None | False | - |
| set_as_patched | None | True | - |
| force | None | False | - |

**Returns**: (none)



### add_to_installed_apps(app_name, rebuild_website = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app_name | None | - | - |
| rebuild_website | None | True | - |

**Returns**: (none)



### remove_from_installed_apps(app_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app_name | None | - | - |

**Returns**: (none)



### remove_app(app_name, dry_run = False, yes = False, no_backup = False, force = False)

Remove app and all linked to the app's module with the app from a site.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app_name | None | - | - |
| dry_run | None | False | - |
| yes | None | False | - |
| no_backup | None | False | - |
| force | None | False | - |

**Returns**: (none)



### _delete_modules(modules: list[str], dry_run: bool) → list[str]

Delete modules belonging to the app and all related doctypes.

Note: All record linked linked to Module Def are also deleted.

Return: list of deleted doctypes.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| modules | list[str] | - | - |
| dry_run | bool | - | - |

**Returns**: `list[str]`



### _delete_linked_documents(module_name: str, doctype_linkfield_map: dict[str, str], dry_run: bool) → None

Deleted all records linked with module def

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| module_name | str | - | - |
| doctype_linkfield_map | dict[str, str] | - | - |
| dry_run | bool | - | - |

**Returns**: `None`



### _get_module_linked_doctype_field_map() → dict[str, str]

Get all the doctypes which have module linked with them.

Return ordered dictionary with doctype->link field mapping.

**Returns**: `dict[str, str]`



### _delete_doctypes(doctypes: list[str], dry_run: bool) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctypes | list[str] | - | - |
| dry_run | bool | - | - |

**Returns**: `None`



### post_install(rebuild_website = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rebuild_website | None | False | - |

**Returns**: (none)



### set_all_patches_as_completed(app)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | None | - | - |

**Returns**: (none)



### init_singles()

**Returns**: (none)



### make_conf(db_name = None, db_password = None, site_config = None, db_type = None, db_socket = None, db_host = None, db_port = None, db_user = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| db_name | None | None | - |
| db_password | None | None | - |
| site_config | None | None | - |
| db_type | None | None | - |
| db_socket | None | None | - |
| db_host | None | None | - |
| db_port | None | None | - |
| db_user | None | None | - |

**Returns**: (none)



### make_site_config(db_name = None, db_password = None, site_config = None, db_type = None, db_socket = None, db_host = None, db_port = None, db_user = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| db_name | None | None | - |
| db_password | None | None | - |
| site_config | None | None | - |
| db_type | None | None | - |
| db_socket | None | None | - |
| db_host | None | None | - |
| db_port | None | None | - |
| db_user | None | None | - |

**Returns**: (none)



### update_site_config(key, value, validate = True, site_config_path = None)

Update a value in site_config

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | None | - | - |
| value | None | - | - |
| validate | None | True | - |
| site_config_path | None | None | - |

**Returns**: (none)



### _update_config_file(key: str, value, config_file: str)

Updates site or common config

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | str | - | - |
| value | None | - | - |
| config_file | str | - | - |

**Returns**: (none)



### get_site_config_path()

**Returns**: (none)



### get_conf_params(db_name = None, db_password = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| db_name | None | None | - |
| db_password | None | None | - |

**Returns**: (none)



### clear_site_locks()

**Returns**: (none)



### make_site_dirs()

**Returns**: (none)



### add_module_defs(app, ignore_if_duplicate = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | None | - | - |
| ignore_if_duplicate | None | False | - |

**Returns**: (none)



### remove_missing_apps()

**Returns**: (none)



### convert_archive_content(sql_file_path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sql_file_path | None | - | - |

**Returns**: (none)



### _guess_mariadb_version() → tuple[int] | None

**Returns**: `tuple[int] | None`



### extract_files(site_name, file_path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| site_name | None | - | - |
| file_path | None | - | - |

**Returns**: (none)



### is_downgrade(sql_file_path, verbose = False)

Check if input db backup will get downgraded on current bench

This function is only tested with mariadb.
TODO: Add postgres support

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sql_file_path | None | - | - |
| verbose | None | False | - |

**Returns**: (none)



### get_old_backup_version(sql_file_path: str) → Version | None

Return the frappe version used to create the specified database dump.

This methods supports older versions of Frappe wich used a different format.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sql_file_path | str | - | - |

**Returns**: `Version | None`



### get_backup_version(sql_file_path: str) → Version | None

Return the frappe version used to create the specified database dump.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sql_file_path | str | - | - |

**Returns**: `Version | None`



### is_partial(sql_file_path: str) → bool

Function to return whether the database dump is a partial backup or not

:param sql_file_path: path to the database dump file
:return: True if the database dump is a partial backup, False otherwise

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sql_file_path | str | - | - |

**Returns**: `bool`



### partial_restore(sql_file_path, verbose = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sql_file_path | None | - | - |
| verbose | None | False | - |

**Returns**: (none)



### validate_database_sql(path: str, _raise: bool = True) → None

Check if file has contents and if `__Auth` table exists

Args:
        path (str): Path of the decompressed SQL file
        _raise (bool, optional): Raise exception if invalid file. Defaults to True.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | str | - | - |
| _raise | bool | True | - |

**Returns**: `None`



### get_db_dump_header(file_path: str, file_bytes: int = 256) → str

Get the header of a database dump file

:param file_path: path to the database dump file
:param file_bytes: number of bytes to read from the file
:return: The first few bytes of the file as requested

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| file_path | str | - | - |
| file_bytes | int | 256 | - |

**Returns**: `str`


