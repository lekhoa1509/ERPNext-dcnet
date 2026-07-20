# API Reference: test_redis.py

**Language**: Python

**Source**: `tests/test_redis.py`

---

## Classes

### TestRedisAuth

**Inherits from**: IntegrationTestCase

#### Methods

##### test_rq_gen_acllist(self)

Make sure that ACL list is genrated

**Decorators**: `@skip_if_redis_version_lt('6.0')`, `@patch.dict(frappe.conf, {'bench_id': 'test_bench', 'use_rq_auth': False})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_adding_redis_user(self)

**Decorators**: `@skip_if_redis_version_lt('6.0')`, `@patch.dict(frappe.conf, {'bench_id': 'test_bench', 'use_rq_auth': False})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_rq_namespace(self)

Make sure that user can access only their respective namespace.

**Decorators**: `@skip_if_redis_version_lt('6.0')`, `@patch.dict(frappe.conf, {'bench_id': 'test_bench', 'use_rq_auth': False})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### version_tuple(version)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| version | None | - | - |

**Returns**: (none)



### skip_if_redis_version_lt(version)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| version | None | - | - |

**Returns**: (none)



### decorator(func)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| func | None | - | - |

**Returns**: (none)



### wrapper()

**Returns**: (none)


