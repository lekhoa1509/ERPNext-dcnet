# API Reference: test_caching.py

**Language**: Python

**Source**: `tests/test_caching.py`

---

## Classes

### TestCachingUtils

**Inherits from**: IntegrationTestCase

#### Methods

##### test_request_cache(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestSiteCache

**Inherits from**: FrappeAPITestCase

#### Methods

##### test_site_cache(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestRedisCache

**Inherits from**: FrappeAPITestCase

#### Methods

##### test_redis_cache(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_redis_cache_without_params(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_redis_cache_diff_args(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_global_clear_cache(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_user_cache(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestDocumentCache

**Inherits from**: FrappeAPITestCase

#### Methods

##### setUp(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### test_caching(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cache_invalidation_set_value(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestRedisWrapper

**Inherits from**: FrappeAPITestCase

#### Methods

##### test_delete_keys(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_hash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_user_cache_clear(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_doctype_cache_clear(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backward_compat_cache(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestHttpCache

**Inherits from**: FrappeAPITestCase

#### Methods

##### test_http_headers(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### request_specific_api(a: list | tuple | dict | int, b: int) → int

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| a | list | tuple | dict | int | - | - |
| b | int | - | - |

**Returns**: `int`



### ping() → str

**Returns**: `str`



### ping_with_ttl() → str

**Returns**: `str`



### same_output_received()

**Returns**: (none)



### calculate_area(radius: float) → float

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| radius | float | - | - |

**Returns**: `float`



### calculate_area(radius: float) → float

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| radius | float | - | - |

**Returns**: `float`



### calculate_area(radius: float) → float

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| radius | float | - | - |

**Returns**: `float`



### calculate_area(radius: float) → float

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| radius | float | - | - |

**Returns**: `float`



### calculate_area(radius: float) → float

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| radius | float | - | - |

**Returns**: `float`


