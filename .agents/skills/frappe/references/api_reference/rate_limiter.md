# API Reference: rate_limiter.py

**Language**: Python

**Source**: `rate_limiter.py`

---

## Classes

### RateLimiter

**Inherits from**: (none)

#### Methods

##### __init__(self, limit, window)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| limit | None | - | - |
| window | None | - | - |


##### apply(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### reject(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### headers(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### record_request_end(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### respond(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### apply()

**Returns**: (none)



### update()

**Returns**: (none)



### respond()

**Returns**: (none)



### rate_limit(key: str | None = None, limit: int | Callable = 5, seconds: int = 24 * 60 * 60, methods: str | list = 'ALL', ip_based: bool = True)

Decorator to rate limit an endpoint.

This will limit Number of requests per endpoint to `limit` within `seconds`.
Uses redis cache to track request counts.

:param key: Key is used to identify the requests uniqueness (Optional)
:param limit: Maximum number of requests to allow with in window time
:type limit: Callable or Integer
:param seconds: window time to allow requests
:param methods: Limit the validation for these methods.
        `ALL` is a wildcard that applies rate limit on all methods.
:type methods: string or list or tuple
:param ip_based: flag to allow ip based rate-limiting
:type ip_based: Boolean

Return: a decorator function that limit the number of requests per endpoint

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | str | None | None | - |
| limit | int | Callable | 5 | - |
| seconds | int | 24 * 60 * 60 | - |
| methods | str | list | 'ALL' | - |
| ip_based | bool | True | - |

**Returns**: (none)



### ratelimit_decorator(fn)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fn | None | - | - |

**Returns**: (none)



### wrapper()

**Returns**: (none)


