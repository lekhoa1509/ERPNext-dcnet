# API Reference: desktop_icon.py

**Language**: Python

**Source**: `desk/doctype/desktop_icon/desktop_icon.py`

---

## Classes

### DesktopIcon

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### export_desktop_icon(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delete_desktop_icon_file(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_permitted(self, bootinfo)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| bootinfo | None | - | - |


##### check_app_permission(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### after_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_workspace_names(workspaces)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| workspaces | None | - | - |

**Returns**: (none)



### get_desktop_icons(user = None, bootinfo = None)

Return desktop icons for user

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | None | - |
| bootinfo | None | None | - |

**Returns**: (none)



### clear_desktop_icons_cache(user = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | None | - |

**Returns**: (none)



### create_desktop_icons_from_workspace()

**Returns**: (none)



### create_desktop_icons_from_installed_apps()

**Returns**: (none)



### create_desktop_icons()

**Returns**: (none)


