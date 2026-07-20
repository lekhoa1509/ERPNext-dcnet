# API Reference: boilerplate.py

**Language**: Python

**Source**: `utils/boilerplate.py`

---

## Classes

### PatchCreator

**Inherits from**: (none)

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### fetch_user_inputs(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _ask_app_name(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _ask_doctype_name(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _ask_patch_meta_info(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_patch_file(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _create_parent_folder_if_not_exists(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### make_boilerplate(dest, app_name, no_git = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dest | None | - | - |
| app_name | None | - | - |
| no_git | None | False | - |

**Returns**: (none)



### _get_user_inputs(app_name)

Prompt user for various inputs related to new app and return config.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app_name | None | - | - |

**Returns**: (none)



### is_valid_email(email) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email | None | - | - |

**Returns**: `bool`



### is_valid_title(title) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| title | None | - | - |

**Returns**: `bool`



### get_license_options() → list[str]

**Returns**: `list[str]`



### get_license_text(license_name: str) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| license_name | str | - | - |

**Returns**: `str`



### copy_from_frappe(rel_path: str, new_app_path: str)

Copy files from frappe app to new app.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rel_path | str | - | - |
| new_app_path | str | - | - |

**Returns**: (none)



### _create_app_boilerplate(dest, hooks, no_git = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dest | None | - | - |
| hooks | None | - | - |
| no_git | None | False | - |

**Returns**: (none)



### _create_github_workflow_files(dest, hooks)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dest | None | - | - |
| hooks | None | - | - |

**Returns**: (none)



### _doctype_name(filename)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filename | None | - | - |

**Returns**: (none)



### _valid_filename(name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: (none)


