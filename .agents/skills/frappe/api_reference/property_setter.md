# API Reference: property_setter.py

**Language**: Python

**Source**: `custom/doctype/property_setter/property_setter.py`

---

## Classes

### PropertySetter

**Inherits from**: Document

#### Methods

##### autoname(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


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


##### validate_fieldtype_change(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_permission_log_options(self, event = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| event | None | None | - |




## Functions

### make_property_setter(doctype, fieldname, property, value, property_type, for_doctype = False, validate_fields_for_doctype = True, is_system_generated = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| fieldname | None | - | - |
| property | None | - | - |
| value | None | - | - |
| property_type | None | - | - |
| for_doctype | None | False | - |
| validate_fields_for_doctype | None | True | - |
| is_system_generated | None | True | - |

**Returns**: (none)



### delete_property_setter(doc_type, property = None, field_name = None, row_name = None)

delete other property setters on this, if this is new

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc_type | None | - | - |
| property | None | None | - |
| field_name | None | None | - |
| row_name | None | None | - |

**Returns**: (none)


