# API Reference: test_db_update.py

**Language**: Python

**Source**: `tests/test_db_update.py`

---

## Classes

### TestDBUpdate

**Inherits from**: IntegrationTestCase

#### Methods

##### test_db_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_index_and_unique_constraints(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_unique_indexes(self, doctype: str, field: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |
| field | str | - | - |


##### test_bigint_conversion(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_unique_index_on_install(self)

Only one unique index should be added

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_unique_index_on_alter(self)

Only one unique index should be added

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_uuid_varchar_migration(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_uuid_link_field(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_varchar_length(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestDBUpdateSanityChecks

**Inherits from**: IntegrationTestCase

#### Methods

##### test_no_unnecessary_migrates(self)

**Decorators**: `@skipIf(frappe.conf.db_type == 'sqlite', 'Not for SQLite for now')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_fieldtype_from_def(field_def)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| field_def | None | - | - |

**Returns**: (none)



### get_field_defs(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### get_other_fields_meta(meta)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| meta | None | - | - |

**Returns**: (none)



### get_table_column(doctype, fieldname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| fieldname | None | - | - |

**Returns**: (none)


