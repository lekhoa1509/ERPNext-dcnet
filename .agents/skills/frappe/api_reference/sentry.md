# API Reference: sentry.py

**Language**: Python

**Source**: `utils/sentry.py`

---

## Classes

### FrappeIntegration

**Inherits from**: Integration

#### Methods

##### setup_once()

**Decorators**: `@staticmethod`




## Functions

### set_scope(scope)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scope | None | - | - |

**Returns**: (none)



### set_sentry_context()

**Returns**: (none)



### before_send(event, hint)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| event | None | - | - |
| hint | None | - | - |

**Returns**: (none)



### capture_exception(message: str | None = None) → None

Function to upload exception data to entry

:param message: A message to be sent if we can't find an exception

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| message | str | None | None | - |

**Returns**: `None`



### sql(self, query, values = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| query | None | - | - |
| values | None | None | - |

**Returns**: (none)



### connect(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: (none)


