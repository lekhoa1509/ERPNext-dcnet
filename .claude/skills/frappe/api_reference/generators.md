# API Reference: generators.py

**Language**: Python

**Source**: `tests/utils/generators.py`

---

## Classes

### TestRecordManager

**Inherits from**: (none)

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_records(self, index_doctype) → list['Document']

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| index_doctype | None | - | - |

**Returns**: `list['Document']`


##### add(self, index_doctype, records: list['Document'])

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| index_doctype | None | - | - |
| records | list['Document'] | - | - |


##### remove(self, index_doctype)

Remove all records for the specified doctype from the log.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| index_doctype | None | - | - |


##### _append_to_log(self, index_doctype, records: list['Document'])

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| index_doctype | None | - | - |
| records | list['Document'] | - | - |


##### _read_log(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _remove_from_log(self, index_doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| index_doctype | None | - | - |




## Functions

### get_modules(doctype) → tuple[str, ModuleType]

Get the modules for the specified doctype

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: `tuple[str, ModuleType]`



### get_missing_records_doctypes(doctype, visited = None) → list[str]

Get the dependencies for the specified doctype in a depth-first manner

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| visited | None | None | - |

**Returns**: `list[str]`



### get_missing_records_module_overrides(module) → [list, list]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| module | None | - | - |

**Returns**: `[list, list]`



### load_test_records_for(index_doctype) → dict[str, Any]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| index_doctype | None | - | - |

**Returns**: `dict[str, Any]`



### _generate_all_records_towards(index_doctype, reset = False, commit = False) → Generator[tuple[str, int]]

Generate test records for the given doctype and its dependencies.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| index_doctype | None | - | - |
| reset | None | False | - |
| commit | None | False | - |

**Returns**: `Generator[tuple[str, int]]`



### _generate_records_for(index_doctype: str, reset: bool = False, commit: bool = False, initial_doctype: str | None = None) → Generator[tuple[str, 'Document']]

Create and yield test records for a specific doctype.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| index_doctype | str | - | - |
| reset | bool | False | - |
| commit | bool | False | - |
| initial_doctype | str | None | None | - |

**Returns**: `Generator[tuple[str, 'Document']]`



### _sync_records(index_doctype: str, test_records: dict[str, list], reset: bool = False, commit: bool = False) → Generator[tuple[str, 'Document']]

Generate test objects for a register doctype from provided records, with caching and persistence.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| index_doctype | str | - | - |
| test_records | dict[str, list] | - | - |
| reset | bool | False | - |
| commit | bool | False | - |

**Returns**: `Generator[tuple[str, 'Document']]`



### _try_create(record, reset = False, commit = False) → tuple['Document', bool]

Create a single test document from the given record data.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| record | None | - | - |
| reset | None | False | - |
| commit | None | False | - |

**Returns**: `tuple['Document', bool]`



### print_mandatory_fields(doctype, initial_doctype)

Print mandatory fields for the specified doctype

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| initial_doctype | None | - | - |

**Returns**: (none)



### _clear_test_log()

**Returns**: (none)



### make_test_records(doctype, force = False, commit = False)

Generate test records for the given doctype and its dependencies.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| force | None | False | - |
| commit | None | False | - |

**Returns**: (none)



### make_test_records_for_doctype(doctype, force = False, commit = False)

Create test records for a specific doctype.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| force | None | False | - |
| commit | None | False | - |

**Returns**: (none)



### make_test_objects(doctype = None, test_records = None, reset = False, commit = False)

Generate test objects from provided records, with caching and persistence.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | None | - |
| test_records | None | None | - |
| reset | None | False | - |
| commit | None | False | - |

**Returns**: (none)



### _transform_legacy_json_records(test_records, doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| test_records | None | - | - |
| doctype | None | - | - |

**Returns**: (none)



### _load(do_create = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| do_create | None | True | - |

**Returns**: (none)



### revert_naming(d)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| d | None | - | - |

**Returns**: (none)


