# API Reference: redis_wrapper.py

**Language**: Python

**Source**: `utils/redis_wrapper.py`

---

## Classes

### RedisearchWrapper

**Inherits from**: Search

#### Methods

##### sugadd(self, key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |


##### suglen(self, key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |


##### sugdel(self, key, string)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |
| string | None | - | - |


##### sugget(self, key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |




### RedisWrapper

Redis client that will automatically prefix conf.db_name

**Inherits from**: redis.Redis

#### Methods

##### connected(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### __call__(self)

WARNING: Added for backward compatibility to support frappe.cache().method(...)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_key(self, key, user = None, shared = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |
| user | None | None | - |
| shared | None | False | - |


##### set_value(self, key, val, user = None, expires_in_sec = None, shared = False)

Sets cache value.

:param key: Cache key
:param val: Value to be cached
:param user: Prepends key with User
:param expires_in_sec: Expire value of this key in X seconds

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |
| val | None | - | - |
| user | None | None | - |
| expires_in_sec | None | None | - |
| shared | None | False | - |


##### get_value(self, key, generator = None, user = None, expires = False, shared = False)

Return cache value. If not found and generator function is
        given, call the generator.

:param key: Cache key.
:param generator: Function to be called to generate a value if `None` is returned.
:param expires: If the key is supposed to be with an expiry, don't store it in frappe.local

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |
| generator | None | None | - |
| user | None | None | - |
| expires | None | False | - |
| shared | None | False | - |


##### expire_key(self, key, time)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |
| time | None | - | - |


##### get_all(self, key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |


##### get_keys(self, key)

Return keys starting with `key`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |


##### delete_keys(self, key)

Delete keys with wildcard `*`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |


##### delete_key(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delete_value(self, keys, user = None, make_keys = True, shared = False)

Delete value, list of values.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| keys | None | - | - |
| user | None | None | - |
| make_keys | None | True | - |
| shared | None | False | - |


##### lpush(self, key, value)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |
| value | None | - | - |


##### rpush(self, key, value)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |
| value | None | - | - |


##### lpop(self, key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |


##### rpop(self, key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |


##### llen(self, key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |


##### lrange(self, key, start, stop)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |
| start | None | - | - |
| stop | None | - | - |


##### ltrim(self, key, start, stop)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |
| start | None | - | - |
| stop | None | - | - |


##### hset(self, name: str, key: str, value, shared: bool = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | str | - | - |
| key | str | - | - |
| value | None | - | - |
| shared | bool | False | - |


##### hexists(self, name: str, key: str, shared: bool = False) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | str | - | - |
| key | str | - | - |
| shared | bool | False | - |

**Returns**: `bool`


##### exists(self) → int

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `int`


##### hgetall(self, name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | None | - | - |


##### hget(self, name, key, generator = None, shared = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | None | - | - |
| key | None | - | - |
| generator | None | None | - |
| shared | None | False | - |


##### hdel(self, name: str, keys: str | list | tuple, shared = False, pipeline: redis.client.Pipeline | None = None)

A wrapper around redis' HDEL command

:param name: The hash name
:param keys: the keys to delete
:param shared: shared frappe key or not
:param pipeline: A redis.client.Pipeline object, if this transaction is to be run in a pipeline

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | str | - | - |
| keys | str | list | tuple | - | - |
| shared | None | False | - |
| pipeline | redis.client.Pipeline | None | None | - |


##### hdel_names(self, names: list | tuple, key: str)

A function to call HDEL on multiple hash names with a common key, run in a single pipeline

:param names: The hash names
:param key: The common key

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| names | list | tuple | - | - |
| key | str | - | - |


##### hdel_keys(self, name_starts_with, key)

Delete hash names with wildcard `*` and key

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name_starts_with | None | - | - |
| key | None | - | - |


##### hkeys(self, name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | None | - | - |


##### sadd(self, name)

Add a member/members to a given set

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | None | - | - |


##### srem(self, name)

Remove a specific member/list of members from the set.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | None | - | - |


##### sismember(self, name, value)

Return True or False based on if a given value is present in the set.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | None | - | - |
| value | None | - | - |


##### spop(self, name)

Remove and returns a random member from the set.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | None | - | - |


##### srandmember(self, name, count = None)

Return a random member from the set.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | None | - | - |
| count | None | None | - |


##### smembers(self, name)

Return all members of the set.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | None | - | - |


##### ft(self, index_name = 'idx')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| index_name | None | 'idx' | - |




### _TrackedConnection

**Inherits from**: redis.Connection

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _enable_client_tracking(self, conn)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| conn | None | - | - |




### ClientCache

A subset of RedisWrapper that keeps "local" cache across requests.

Main reason for doing this is improving performance while reading things like hooks, schema.
This feature is internal to Frappe Framework and is subjected to change without any notice.
There aren't many use cases for such aggressive caching outside of core Framework.

This is an implementation of Redis' "client side caching" concept:
        - https://redis.io/docs/latest/develop/reference/client-side-caching/

Usage/Notes:
        - Cache keys that do not change often: Think hours-days, not minutes.
        - Cache keys that are read frequently, e.g. every request or at least >10% of the requests.
        - Cache values are not huge, consider avg size of ~4kb per value. You can deviate here and
          there but not go crazy with caching large values in this cache.
        - We have hardcoded 10 minutes "local" ttl and max 1024 keys.
                You're not supposed to work with these numbers, not change them.
        - Same keys can be accessed with `frappe.cache` too, but that won't implement invalidation.
        - Invalidate things as usual using `delete_value`. Local invalidation should be instant.
          Do not expect sub-second invalidation guarantees across processes.
          If you need that kind of guarantees, don't use this cache.
        - When redis connection isn't available or any unknown exceptions are encountered, this
          cache automatically turns itself off and falls back to behaviour that is equivalent to
          default Redis cache behaviour.
        - Never use `frappe.cache`'s request local cache along with client-side cache. Two
          different copies of same key are a big source of data races.
        - This cache uses simple FIFO eviction policy. Make sure your access patterns don't cause
          the worst case behaviour for this policy. E.g. looping over `maxsize` items repeatedly.

**Inherits from**: (none)

#### Methods

##### __init__(self, maxsize: int = 1024, ttl = 10 * 60, monitor: RedisWrapper | None = None) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| maxsize | int | 1024 | - |
| ttl | None | 10 * 60 | - |
| monitor | RedisWrapper | None | None | - |

**Returns**: `None`


##### get_value(self, key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |


##### set_value(self, key, val)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |
| val | None | - | - |


##### get_doc(self, doctype: str, name: str | None = None)

Utility to fetch and store documents in client cache.

Use sparingly, this should ideally be used for settings and doctypes that have few known
number of documents.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |
| name | str | None | None | - |


##### ensure_max_size(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delete_value(self, key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |


##### delete_keys(self, pattern)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| pattern | None | - | - |


##### run_invalidator_thread(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### erase_persistent_caches(self)

Send signal to clear all worker-specific caches

This can include cached controller resolution, @site_cache and any other similar persistent
cache.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _handle_invalidation(self, message)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| message | None | - | - |


##### _handle_persistent_cache_invalidation(self, message)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| message | None | - | - |


##### _exception_handler(self, exc, pubsub, pubsub_thread)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| exc | None | - | - |
| pubsub | None | - | - |
| pubsub_thread | None | - | - |


##### clear_cache(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### statistics(self) → CacheStatistics

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `CacheStatistics`


##### reset_statistics(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### setup_cache() → RedisWrapper

**Returns**: `RedisWrapper`



### get_sentinel_connection(sentinels: list[tuple[str, int]], sentinel_username = None, sentinel_password = None, master_username = None, master_password = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sentinels | list[tuple[str, int]] | - | - |
| sentinel_username | None | None | - |
| sentinel_password | None | None | - |
| master_username | None | None | - |
| master_password | None | None | - |

**Returns**: (none)


