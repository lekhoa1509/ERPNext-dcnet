# API Reference: local.py

**Language**: Python

**Source**: `utils/local.py`

---

## Classes

### Local

For internal use only. Do not use this class directly.

**Inherits from**: (none)

#### Methods

##### __getattribute__(self, name: str) → Any

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | str | - | - |

**Returns**: `Any`


##### __iter__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### __setattr__(self, name: str, value: Any) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | str | - | - |
| value | Any | - | - |

**Returns**: `None`


##### __delattr__(self, name: str) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | str | - | - |

**Returns**: `None`


##### __call__(self, name: str) → 'LocalProxy'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | str | - | - |

**Returns**: `'LocalProxy'`




### LocalProxy

**Inherits from**: WerkzeugLocalProxy

#### Methods

##### __getattr__(self, name: str) → Any

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | str | - | - |

**Returns**: `Any`


##### __setattr__(self, name: str, value: str) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | str | - | - |
| value | str | - | - |

**Returns**: `None`


##### __delattr__(self, name: str) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | str | - | - |

**Returns**: `None`


##### __getitem__(self, key: str) → Any

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | str | - | - |

**Returns**: `Any`


##### __setitem__(self, key: str, value: str) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | str | - | - |
| value | str | - | - |

**Returns**: `None`


##### __delitem__(self, key: str) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | str | - | - |

**Returns**: `None`


##### __bool__(self) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `bool`


##### __contains__(self, key: str) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | str | - | - |

**Returns**: `bool`


##### __str__(self) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `str`




## Functions

### release_local(local)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| local | None | - | - |

**Returns**: (none)



### _get_current_object() → Any

**Returns**: `Any`


