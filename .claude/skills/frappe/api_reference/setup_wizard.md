# API Reference: setup_wizard.py

**Language**: Python

**Source**: `desk/page/setup_wizard/setup_wizard.py`

---

## Functions

### get_setup_stages(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### setup_complete(args)

Calls hooks for `setup_wizard_complete`, sets home page as `desktop`
and clears cache. If wizard breaks, calls `setup_wizard_exception` hook

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### initialize_system_settings_and_user(system_settings_data, user_data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| system_settings_data | None | - | - |
| user_data | None | - | - |

**Returns**: (none)



### process_setup_stages(stages, user_input, is_background_task = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| stages | None | - | - |
| user_input | None | - | - |
| is_background_task | None | False | - |

**Returns**: (none)



### set_missing_values(task)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| task | None | - | - |

**Returns**: (none)



### enable_setup_wizard_complete(app_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app_name | None | - | - |

**Returns**: (none)



### update_global_settings(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### run_post_setup_complete(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### run_setup_success(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### get_stages_hooks(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### update_app_details_in_stages(_stages, app_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| _stages | None | - | - |
| app_name | None | - | - |

**Returns**: (none)



### get_setup_complete_hooks(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### handle_setup_exception(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### update_system_settings(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### create_or_update_user(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### set_timezone(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### parse_args(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### sanitize_input(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### add_all_roles_to(name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: (none)



### _get_default_roles() → set[str]

**Returns**: `set[str]`



### disable_future_access()

**Returns**: (none)



### load_messages(language)

Load translation messages for given language from all `setup_wizard_requires`
javascript files

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| language | None | - | - |

**Returns**: (none)



### load_languages()

**Returns**: (none)



### load_user_details()

**Returns**: (none)



### prettify_args(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### email_setup_wizard_exception(traceback, args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| traceback | None | - | - |
| args | None | - | - |

**Returns**: (none)



### log_setup_wizard_exception(traceback, args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| traceback | None | - | - |
| args | None | - | - |

**Returns**: (none)



### get_language_code(lang)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| lang | None | - | - |

**Returns**: (none)



### enable_twofactor_all_roles()

**Returns**: (none)



### make_records(records, debug = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| records | None | - | - |
| debug | None | False | - |

**Returns**: (none)



### show_document_insert_error()

**Returns**: (none)


