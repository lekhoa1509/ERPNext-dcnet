# API Reference: integration_test_case.py

**Language**: Python

**Source**: `tests/classes/integration_test_case.py`

---

## Classes

### IntegrationTestCase

Integration test class for Frappe tests.

Key features:
- Automatic database setup and teardown
- Utilities for managing database connections
- Context managers for query counting and Redis call monitoring
- Lazy loading of test record dependencies

Note: If you override `setUpClass`, make sure to call `super().setUpClass()`
to maintain the functionality of this base class.

**Inherits from**: UnitTestCase

#### Methods

##### setUpClass(cls) → None

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |

**Returns**: `None`


##### tearDownClass(cls) → None

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |

**Returns**: `None`


##### setUp(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### tearDown(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### primary_connection(self) → AbstractContextManager[None]

Switch to primary DB connection

This is used for simulating multiple users performing actions by simulating two DB connections

**Decorators**: `@contextmanager`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `AbstractContextManager[None]`


##### secondary_connection(self) → AbstractContextManager[None]

Switch to secondary DB connection.

**Decorators**: `@contextmanager`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `AbstractContextManager[None]`


##### _rollback_connections(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### assertQueryCount(self, count: int, query_type: tuple[str] | None = None)

**Decorators**: `@contextmanager`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| count | int | - | - |
| query_type | tuple[str] | None | None | - |


##### assertRedisCallCounts(self, count: int) → AbstractContextManager[None]

**Decorators**: `@contextmanager`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| count | int | - | - |

**Returns**: `AbstractContextManager[None]`


##### assertRowsRead(self, count: int) → AbstractContextManager[None]

**Decorators**: `@contextmanager`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| count | int | - | - |

**Returns**: `AbstractContextManager[None]`




## Functions

### _commit_watcher()

**Returns**: (none)



### _rollback_db()

**Returns**: (none)



### _restore_ctx_locals(flags)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| flags | None | - | - |

**Returns**: (none)



### _sql_with_count()

**Returns**: (none)



### execute_command_and_count()

**Returns**: (none)



### _sql_with_count()

**Returns**: (none)


