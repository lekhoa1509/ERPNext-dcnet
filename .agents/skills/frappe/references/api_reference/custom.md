# API Reference: custom.py

**Language**: Python

**Source**: `query_builder/custom.py`

---

## Classes

### GROUP_CONCAT

**Inherits from**: DistinctOptionFunction

#### Methods

##### __init__(self, column: str, alias: str | None = None)

[ Implements the group concat function read more about it at https://www.geeksforgeeks.org/mysql-group_concat-function ]
Args:
        column (str): [ name of the column you want to concat]
        alias (Optional[str], optional): [ is this an alias? ]. Defaults to None.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| column | str | - | - |
| alias | str | None | None | - |




### STRING_AGG

**Inherits from**: DistinctOptionFunction

#### Methods

##### __init__(self, column: str, separator: str = ',', alias: str | None = None)

[ Implements the group concat function read more about it at https://docs.microsoft.com/en-us/sql/t-sql/functions/string-agg-transact-sql?view=sql-server-ver15 ]

Args:
        column (str): [ name of the column you want to concat ]
        separator (str, optional): [separator to be used]. Defaults to ",".
        alias (Optional[str], optional): [description]. Defaults to None.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| column | str | - | - |
| separator | str | ',' | - |
| alias | str | None | None | - |




### MATCH

**Inherits from**: DistinctOptionFunction

#### Methods

##### __init__(self, column: str)

[ Implementation of Match Against read more about it https://dev.mysql.com/doc/refman/8.0/en/fulltext-search.html#function_match ]

Args:
        column (str):[ column to search in ]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| column | str | - | - |


##### get_function_sql(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### Against(self, text: str)

[ Text that has to be searched against ]

Args:
        text (str): [ the text string that we match it against ]

**Decorators**: `@builder`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| text | str | - | - |




### TO_TSVECTOR

**Inherits from**: DistinctOptionFunction

#### Methods

##### __init__(self, column: str)

[ Implementation of TO_TSVECTOR read more about it https://www.postgresql.org/docs/9.1/textsearch-controls.html]

Args:
        column (str): [ column to search in ]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| column | str | - | - |


##### get_function_sql(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### Against(self, text: str)

[ Text that has to be searched against ]

Args:
        text (str): [ the text string that we match it against ]

**Decorators**: `@builder`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| text | str | - | - |




### ConstantColumn

**Inherits from**: Term

#### Methods

##### __init__(self, value: str) → None

Return a pseudo column with the given constant `value` in all the rows.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| value | str | - | - |

**Returns**: `None`


##### get_sql(self, quote_char: str | None = None) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| quote_char | str | None | None | - |

**Returns**: `str`




### MonthName

**Inherits from**: Function

#### Methods

##### __init__(self, field, alias = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| field | None | - | - |
| alias | None | None | - |




### Quarter

**Inherits from**: Function

#### Methods

##### __init__(self, field, alias = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| field | None | - | - |
| alias | None | None | - |




### Month

**Inherits from**: Function

#### Methods

##### __init__(self, field, alias = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| field | None | - | - |
| alias | None | None | - |



