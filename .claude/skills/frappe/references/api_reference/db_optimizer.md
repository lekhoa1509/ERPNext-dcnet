# API Reference: db_optimizer.py

**Language**: Python

**Source**: `core/doctype/recorder/db_optimizer.py`

---

## Classes

### DBColumn

**Inherits from**: (none)

#### Methods

##### from_frappe_ouput(cls, data) → 'DBColumn'

Parse DBColumn from output of describe-database-table command in Frappe

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| data | None | - | - |

**Returns**: `'DBColumn'`




### DBIndex

**Inherits from**: (none)

#### Methods

##### __eq__(self, other: 'DBIndex') → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| other | 'DBIndex' | - | - |

**Returns**: `bool`


##### __repr__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### from_frappe_ouput(cls, data, table) → 'DBIndex'

Parse DBIndex from output of describe-database-table command in Frappe

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| data | None | - | - |
| table | None | - | - |

**Returns**: `'DBIndex'`




### ColumnStat

**Inherits from**: (none)

#### Methods

##### __post_init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### from_frappe_ouput(cls, data) → 'ColumnStat'

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| data | None | - | - |

**Returns**: `'ColumnStat'`




### DBTable

**Inherits from**: (none)

#### Methods

##### __post_init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_cardinality(self, column_stats: list[ColumnStat]) → None

Estimate cardinality using mysql.column_stat

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| column_stats | list[ColumnStat] | - | - |

**Returns**: `None`


##### from_frappe_ouput(cls, data) → 'DBTable'

Parse DBTable from output of describe-database-table command in Frappe

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| data | None | - | - |

**Returns**: `'DBTable'`


##### has_column(self, column: str) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| column | str | - | - |

**Returns**: `bool`




### DBOptimizer

**Inherits from**: (none)

#### Methods

##### __post_init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tables_examined(self) → list[str]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `list[str]`


##### update_table_data(self, table: DBTable)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| table | DBTable | - | - |


##### _convert_to_db_index(self, column: str) → DBIndex

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| column | str | - | - |

**Returns**: `DBIndex`


##### _remove_existing_indexes(self, potential_indexes: list[DBIndex]) → list[DBIndex]

Given list of potential index candidates remove the ones that already exist.

This also removes multi-column indexes for parts that are applicable to query.
Example: If multi-col index A+B+C exists and query utilizes A+B then
A+B are removed from potential indexes.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| potential_indexes | list[DBIndex] | - | - |

**Returns**: `list[DBIndex]`


##### potential_indexes(self) → list[DBIndex]

Get all columns that can potentially be indexed to speed up this query.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `list[DBIndex]`


##### suggest_index(self) → DBIndex | None

Suggest best possible column to index given query and table stats.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `DBIndex | None`


##### index_score(self, index: DBIndex) → float

Score an index from 0 to 1 based on usefulness.

A score of 0.5 indicates on average this index will read 50% of the table. (e.g. checkboxes)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| index | DBIndex | - | - |

**Returns**: `float`




## Functions

### remove_maximum_indexes(idx: list[DBIndex])

Try to remove entire index from potential indexes, if not possible, reduce one part and try again until no parts are left.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| idx | list[DBIndex] | - | - |

**Returns**: (none)


