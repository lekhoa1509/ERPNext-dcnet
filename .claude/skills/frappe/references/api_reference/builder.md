# API Reference: builder.py

**Language**: Python

**Source**: `query_builder/builder.py`

---

## Classes

### Base

**Inherits from**: (none)

#### Methods

##### functions(name: str) → Function

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | str | - | - |

**Returns**: `Function`


##### DocType(table_name: str) → Table

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| table_name | str | - | - |

**Returns**: `Table`


##### into(cls, table) → QueryBuilder

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| table | None | - | - |

**Returns**: `QueryBuilder`


##### update(cls, table) → QueryBuilder

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| table | None | - | - |

**Returns**: `QueryBuilder`




### MariaDB

**Inherits from**: Base, MySQLQuery

#### Methods

##### _builder(cls) → 'MySQLQueryBuilder'

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |

**Returns**: `'MySQLQueryBuilder'`


##### from_(cls, table)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| table | None | - | - |




### Postgres

**Inherits from**: Base, PostgreSQLQuery

#### Methods

##### _builder(cls) → 'PostgreSQLQueryBuilder'

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |

**Returns**: `'PostgreSQLQueryBuilder'`


##### Field(cls, field_name)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| field_name | None | - | - |


##### from_(cls, table)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| table | None | - | - |




### SQLite

**Inherits from**: Base, SQLLiteQuery

#### Methods

##### _builder(cls) → 'SQLLiteQueryBuilder'

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |

**Returns**: `'SQLLiteQueryBuilder'`


##### from_(cls, table)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| table | None | - | - |



