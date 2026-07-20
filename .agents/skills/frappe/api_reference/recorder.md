# API Reference: recorder.py

**Language**: Python

**Source**: `recorder.py`

---

## Classes

### RecorderConfig

**Inherits from**: (none)

#### Methods

##### __post_init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### store(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### retrieve(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### delete()

**Decorators**: `@staticmethod`




### Recorder

**Inherits from**: (none)

#### Methods

##### __init__(self, force = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| force | None | False | - |


##### register(self, data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| data | None | - | - |


##### cleanup(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### process_profiler(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### dump(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _patch_sql(self, db: 'Database')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| db | 'Database' | - | - |


##### _unpatch_sql(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### record_sql()

**Returns**: (none)



### get_current_stack_frames()

**Returns**: (none)



### post_process()

post process all recorded values.

Any processing that can be done later should be done here to avoid overhead while
profiling. As of now following values are post-processed:
        - `EXPLAIN` output of queries.
        - SQLParse reformatting of queries
        - Mark duplicates

**Returns**: (none)



### mark_duplicates(request)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| request | None | - | - |

**Returns**: (none)



### normalize_query(query: str) → str

Attempt to normalize query by removing variables.
This gives a different view of similar duplicate queries.

Example:
        These two are distinct queries:
                `select * from user where name = 'x'`
                `select * from user where name = 'z'`

        But their "normalized" form would be same:
                `select * from user where name = ?`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| query | str | - | - |

**Returns**: `str`



### record(force = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| force | None | False | - |

**Returns**: (none)



### dump()

**Returns**: (none)



### do_not_record(function)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| function | None | - | - |

**Returns**: (none)



### administrator_only(function)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| function | None | - | - |

**Returns**: (none)



### status()

**Returns**: (none)



### start(record_jobs: bool = True, record_requests: bool = True, record_sql: bool = True, profile: bool = False, capture_stack: bool = True, explain: bool = True, request_filter: str = '/', jobs_filter: str = '')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| record_jobs | bool | True | - |
| record_requests | bool | True | - |
| record_sql | bool | True | - |
| profile | bool | False | - |
| capture_stack | bool | True | - |
| explain | bool | True | - |
| request_filter | str | '/' | - |
| jobs_filter | str | '' | - |

**Returns**: (none)



### stop()

**Returns**: (none)



### get(uuid = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| uuid | None | None | - |

**Returns**: (none)



### export_data()

**Returns**: (none)



### delete()

**Returns**: (none)



### record_queries(func: Callable)

Decorator to profile a specific function using recorder.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| func | Callable | - | - |

**Returns**: (none)



### import_data(file: str) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| file | str | - | - |

**Returns**: `None`



### wrapper()

**Returns**: (none)



### wrapper()

**Returns**: (none)



### wrapped()

**Returns**: (none)


