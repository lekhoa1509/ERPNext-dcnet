# API Reference: functions.py

**Language**: Python

**Source**: `query_builder/functions.py`

---

## Classes

### Concat_ws

**Inherits from**: Function

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### Locate

**Inherits from**: Function

#### Methods

##### __init__(self, needle, haystack)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| needle | None | - | - |
| haystack | None | - | - |




### Strpos

**Inherits from**: Function

#### Methods

##### __init__(self, needle, haystack)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| needle | None | - | - |
| haystack | None | - | - |




### Instr

**Inherits from**: Function

#### Methods

##### __init__(self, needle, haystack)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| needle | None | - | - |
| haystack | None | - | - |




### Timestamp

**Inherits from**: Function

#### Methods

##### __init__(self, term: str, time = None, alias = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| term | str | - | - |
| time | None | None | - |
| alias | None | None | - |




### Round

**Inherits from**: Function

#### Methods

##### __init__(self, term, decimal = 0)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| term | None | - | - |
| decimal | None | 0 | - |




### Truncate

**Inherits from**: Function

#### Methods

##### __init__(self, term, decimal)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| term | None | - | - |
| decimal | None | - | - |




### _PostgresTimestamp

**Inherits from**: ArithmeticExpression

#### Methods

##### __init__(self, datepart, timepart, alias = None)

Postgres would need both datepart and timepart to be a string for concatenation

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| datepart | None | - | - |
| timepart | None | - | - |
| alias | None | None | - |




### YearWeek

**Inherits from**: Function

#### Methods

##### __init__(self, term)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| term | None | - | - |




### _PostgresUnixTimestamp

**Inherits from**: Extract

#### Methods

##### __init__(self, field, alias = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| field | None | - | - |
| alias | None | None | - |




### Cast_

**Inherits from**: Function

#### Methods

##### __init__(self, value, as_type, alias = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| value | None | - | - |
| as_type | None | - | - |
| alias | None | None | - |


##### get_special_params_sql(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### SqlFunctions

**Inherits from**: Enum



## Functions

### _aggregate(function, dt, fieldname, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| function | None | - | - |
| dt | None | - | - |
| fieldname | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### _max(dt, fieldname, filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |
| fieldname | None | - | - |
| filters | None | None | - |

**Returns**: (none)



### _min(dt, fieldname, filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |
| fieldname | None | - | - |
| filters | None | None | - |

**Returns**: (none)



### _avg(dt, fieldname, filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |
| fieldname | None | - | - |
| filters | None | None | - |

**Returns**: (none)



### _sum(dt, fieldname, filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |
| fieldname | None | - | - |
| filters | None | None | - |

**Returns**: (none)


