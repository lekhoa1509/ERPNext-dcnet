# API Reference: terms.py

**Language**: Python

**Source**: `query_builder/terms.py`

---

## Classes

### NamedParameterWrapper

Utility class to hold parameter values and keys

**Inherits from**: (none)

#### Methods

##### __init__(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### get_sql(self, param_value: Any) → str

Return SQL for a parameter, while adding the real value in a dict.

Args:
        param_value (Any): Value of the parameter

Return:
        str: parameter used in the SQL query

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| param_value | Any | - | - |

**Returns**: `str`


##### get_parameters(self) → dict[str, Any]

Get dict with parameters and values.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `dict[str, Any]`




### ParameterizedValueWrapper

Class to monkey patch ValueWrapper

Adds functionality to parameterize queries when a `param wrapper` is passed in get_sql()

**Inherits from**: ValueWrapper

#### Methods

##### get_sql(self, quote_char: str | None = None, secondary_quote_char: str = "'", param_wrapper: NamedParameterWrapper | None = None) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| quote_char | str | None | None | - |
| secondary_quote_char | str | "'" | - |
| param_wrapper | NamedParameterWrapper | None | None | - |

**Returns**: `str`




### SQLiteParameterizedValueWrapper

**Inherits from**: ParameterizedValueWrapper, SQLLiteValueWrapper



### ParameterizedFunction

Class to monkey patch pypika.terms.Functions

Only to pass `param_wrapper` in `get_function_sql`.

**Inherits from**: Function

#### Methods

##### get_sql(self) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `str`




### SubQuery

**Inherits from**: Criterion

#### Methods

##### __init__(self, subq: QueryBuilder, alias: str | None = None) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| subq | QueryBuilder | - | - |
| alias | str | None | None | - |

**Returns**: `None`


##### get_sql(self) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `str`



