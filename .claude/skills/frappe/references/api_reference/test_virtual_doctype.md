# API Reference: test_virtual_doctype.py

**Language**: Python

**Source**: `tests/test_virtual_doctype.py`

---

## Classes

### VirtualDoctypeTest

This is a virtual doctype controller for test/demo purposes.

- It uses a JSON file on disk as "backend".
- Key is docname and value is the document itself.

Example:
{
        "doc1": {"name": "doc1", ...}
        "doc2": {"name": "doc2", ...}
}

**Inherits from**: Document

#### Methods

##### get_current_data() → dict[str, dict]

Read data from disk

**Decorators**: `@staticmethod`

**Returns**: `dict[str, dict]`


##### update_data(data: dict[str, dict]) → None

Flush updated data to disk

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | dict[str, dict] | - | - |

**Returns**: `None`


##### db_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### load_from_db(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### db_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delete(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_list()

**Decorators**: `@staticmethod`


##### get_count()

**Decorators**: `@staticmethod`


##### get_stats()

**Decorators**: `@staticmethod`




### TestVirtualDoctypes

**Inherits from**: IntegrationTestCase

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_insert_update_and_load_from_desk(self)

Insert, update, reload and assert changes

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_multiple_doc_insert_and_get_list(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_count(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_delete_doc(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_controller_validity(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



