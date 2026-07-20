# API Reference: test_bulk_update.py

**Language**: Python

**Source**: `desk/doctype/bulk_update/test_bulk_update.py`

---

## Classes

### TestBulkUpdate

**Inherits from**: IntegrationTestCase

#### Methods

##### setUpClass(cls) → None

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |

**Returns**: `None`


##### wait_for_assertion(self, assertion)

Wait till an assertion becomes True

**Decorators**: `@timeout()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| assertion | None | - | - |


##### test_bulk_submit_in_background(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bulk_update_parent_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bulk_update_child_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### check_docstatus(docs, status)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docs | None | - | - |
| status | None | - | - |

**Returns**: (none)



### check_field_values(docs, expected)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docs | None | - | - |
| expected | None | - | - |

**Returns**: (none)



### check_child_field(docs, expected)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docs | None | - | - |
| expected | None | - | - |

**Returns**: (none)


