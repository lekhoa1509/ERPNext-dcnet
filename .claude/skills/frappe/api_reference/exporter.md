# API Reference: exporter.py

**Language**: Python

**Source**: `types/exporter.py`

---

## Classes

### TypeExporter

**Inherits from**: (none)

#### Methods

##### __init__(self, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### export_types(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _replace_or_add_code(self, new_code: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| new_code | str | - | - |


##### _generate_code(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _create_fields_code_block(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _create_imports_block(self) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `str`


##### _get_doctype_imports(self, doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |


##### _map_fieldtype(self, field) → str | None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| field | None | - | - |

**Returns**: `str | None`


##### _is_nullable(self, field) → bool

If value can be `None`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| field | None | - | - |

**Returns**: `bool`


##### _generic_parameters(self, field) → str | None

If field is container type then return element type.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| field | None | - | - |

**Returns**: `str | None`


##### _validate_code(code) → bool

Make sure whatever code Frappe adds dynamically is valid python.

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| code | None | - | - |

**Returns**: `bool`


##### _guess_indentation(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`



