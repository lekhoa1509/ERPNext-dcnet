# API Reference: module_def.py

**Language**: Python

**Source**: `core/doctype/module_def/module_def.py`

---

## Classes

### ModuleDef

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

If in `developer_mode`, create folder for module and
add in `modules.txt` of app if missing.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_modules_folder(self)

Creates a folder `[app]/[module]` and adds `__init__.py`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_to_modules_txt(self)

Adds to `[app]/modules.txt`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

Delete module name from modules.txt

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delete_module_from_file(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_installed_apps()

**Returns**: (none)


