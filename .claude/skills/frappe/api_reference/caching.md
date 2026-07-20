# API Reference: caching.py

**Language**: Python

**Source**: `utils/caching.py`

---

## Functions

### __generate_request_cache_key(args: tuple, kwargs: dict) → tuple

Generate a key for the cache.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | tuple | - | - |
| kwargs | dict | - | - |

**Returns**: `tuple`



### request_cache(func: Callable) → Callable

Decorator to cache function calls mid-request.

Cache is stored in `frappe.local.request_cache`.

The cache only persists for the current request and is cleared when the request is over.

The function is called just once per request with the same set of (kw)arguments.

---
Usage:
```
        from frappe.utils.caching import request_cache

        @request_cache
        def calculate_pi(num_terms=0):
            import math, time

            print(f"{num_terms = }")
            time.sleep(10)
            return math.pi

        calculate_pi(10)  # will calculate value
        calculate_pi(10)  # will return value from cache
```

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| func | Callable | - | - |

**Returns**: `Callable`



### site_cache(ttl: int | None = None, maxsize: int | None = None) → Callable

Decorator to cache method calls across requests.

The cache is stored in `frappe.utils.caching._SITE_CACHE`.

The cache persists on the parent process.

It offers a light-weight cache for the current process without the additional
overhead of serializing / deserializing Python objects.

Note: This cache isn't shared among workers. If you need to share data across
workers, use redis (frappe.cache API) instead.

---
Usage:
```
        from frappe.utils.caching import site_cache

        @site_cache
        def calculate_pi():
            import math, time

            precision = get_precision("Math Constant", "Pi") # depends on site data
            return round(math.pi, precision)

        calculate_pi(10) # will calculate value
        calculate_pi(10) # will return value from cache
        calculate_pi.clear_cache() # clear this function's cache for all sites
        calculate_pi(10) # will calculate value
```

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ttl | int | None | None | - |
| maxsize | int | None | None | - |

**Returns**: `Callable`



### redis_cache(ttl: int | None = 3600, user: str | bool | None = None, shared: bool = False) → Callable

Decorator to cache method calls and its return values in Redis

args:
        ttl: time to expiry in seconds, defaults to 1 hour
        user: `true` should cache be specific to session user.
        shared: `true` should cache be shared across sites

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ttl | int | None | 3600 | - |
| user | str | bool | None | None | - |
| shared | bool | False | - |

**Returns**: `Callable`



### http_cache() → Callable

Decorator to send cache-control response from whitelisted endpoints.

Reference: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control

args:
        public: Results can be cached by proxy if set to True, otherwise only client (browser) can
                        cache results.
        max_age: Cache Time-To-Live
        stale_while_revalidate: Duration for which stale response can be served while revalidation
                                                        occurs.

**Returns**: `Callable`



### deprecated_local_cache(namespace, key, generator, regenerate_if_none = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| namespace | None | - | - |
| key | None | - | - |
| generator | None | - | - |
| regenerate_if_none | None | False | - |

**Returns**: (none)



### wrapper()

**Returns**: (none)



### time_cache_wrapper(func: Callable | None = None) → Callable

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| func | Callable | None | None | - |

**Returns**: `Callable`



### wrapper(func: Callable | None = None) → Callable

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| func | Callable | None | None | - |

**Returns**: `Callable`



### outer(func: Callable) → Callable

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| func | Callable | - | - |

**Returns**: `Callable`



### clear_cache()

Clear cache for this function for all sites if not specified.

**Returns**: (none)



### site_cache_wrapper()

**Returns**: (none)



### clear_cache()

**Returns**: (none)



### redis_cache_wrapper()

**Returns**: (none)



### inner()

**Returns**: (none)


