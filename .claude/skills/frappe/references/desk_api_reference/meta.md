# API Reference: meta.py

**Language**: Python

**Source**: `form/meta.py`

---

## Classes

### FormMeta

**Inherits from**: Meta

#### Methods

##### __init__(self, doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |


##### load_assets(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### as_dict(self, no_nulls = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| no_nulls | None | False | - |


##### add_code(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _add_code(self, path, fieldname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| path | None | - | - |
| fieldname | None | - | - |


##### add_html_templates(self, path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| path | None | - | - |


##### add_code_via_hook(self, hook, fieldname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| hook | None | - | - |
| fieldname | None | - | - |


##### add_custom_script(self)

embed all require files

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _show_missing_doctype_msg(self, df)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| df | None | - | - |


##### load_print_formats(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### load_workflows(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### load_templates(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### load_dashboard(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### load_workspaces(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### load_kanban_meta(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### load_kanban_column_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_meta(doctype, cached = True) → 'FormMeta'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| cached | None | True | - |

**Returns**: `'FormMeta'`



### get_code_files_via_hooks(hook, name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| hook | None | - | - |
| name | None | - | - |

**Returns**: (none)



### get_js(path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |

**Returns**: (none)



### _get_path(fname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fname | None | - | - |

**Returns**: (none)


