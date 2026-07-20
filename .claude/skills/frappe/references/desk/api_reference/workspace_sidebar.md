# API Reference: workspace_sidebar.py

**Language**: Python

**Source**: `doctype/workspace_sidebar/workspace_sidebar.py`

---

## Classes

### WorkspaceSidebar

**Inherits from**: Document

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_can_read_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_save(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### export_sidebar(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### after_rename(self, old, new, merge)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| old | None | - | - |
| new | None | - | - |
| merge | None | - | - |


##### is_item_allowed(self, name, item_type, allowed_workspaces)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | None | - | - |
| item_type | None | - | - |
| allowed_workspaces | None | - | - |


##### get_cached(self, cache_key, fallback_fn)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| cache_key | None | - | - |
| fallback_fn | None | - | - |


##### set_module(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_module_from_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_allowed_modules(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### delete_file(app, title)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | None | - | - |
| title | None | - | - |

**Returns**: (none)



### is_workspace_manager()

**Returns**: (none)



### create_workspace_sidebar_for_workspaces()

**Returns**: (none)



### add_sidebar_items(sidebar_title, sidebar_items)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sidebar_title | None | - | - |
| sidebar_items | None | - | - |

**Returns**: (none)



### add_to_my_workspace(workspace)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| workspace | None | - | - |

**Returns**: (none)



### auto_generate_sidebar_from_module()

Auto generate sidebar from module

**Returns**: (none)



### get_module_info(module_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| module_name | None | - | - |

**Returns**: (none)



### choose_top_doctypes(doctype_names)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype_names | None | - | - |

**Returns**: (none)



### create_sidebar_items(module_info)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| module_info | None | - | - |

**Returns**: (none)



### add_section_breaks(label, idx)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| label | None | - | - |
| idx | None | - | - |

**Returns**: (none)


