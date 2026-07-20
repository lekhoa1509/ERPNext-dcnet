# API Reference: workspace.py

**Language**: Python

**Source**: `doctype/workspace/workspace.py`

---

## Classes

### Workspace

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### clear_cache(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_export(self, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delete_from_my_workspaces(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### after_delete(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_module_wise_workspaces()

**Decorators**: `@staticmethod`


##### get_link_groups(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### build_links_table_from_card(self, config)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| config | None | - | - |




## Functions

### disable_saving_as_public()

**Returns**: (none)



### get_link_type(key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | None | - | - |

**Returns**: (none)



### get_report_type(report)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| report | None | - | - |

**Returns**: (none)



### new_page(new_page)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| new_page | None | - | - |

**Returns**: (none)



### save_page(name, public, new_widgets, blocks)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |
| public | None | - | - |
| new_widgets | None | - | - |
| blocks | None | - | - |

**Returns**: (none)



### update_page(name, title, icon, indicator_color, parent, public)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |
| title | None | - | - |
| icon | None | - | - |
| indicator_color | None | - | - |
| parent | None | - | - |
| public | None | - | - |

**Returns**: (none)



### last_sequence_id(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### get_page_list(fields, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fields | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### is_workspace_manager()

**Returns**: (none)


