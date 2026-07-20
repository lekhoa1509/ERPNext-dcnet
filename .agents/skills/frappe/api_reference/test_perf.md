# API Reference: test_perf.py

**Language**: Python

**Source**: `tests/test_perf.py`

---

## Classes

### TestPerformance

**Inherits from**: IntegrationTestCase

#### Methods

##### reset_request_specific_caches(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### setUp(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### test_meta_caching(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_permitted_fieldnames(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_set_value_query_count(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_controller_caching(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_value_limits(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_db_value_cache(self)

Link validation if repeated should just use db.value_cache, hence no extra queries

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_req_per_seconds_basic(self)

Ideally should be ran against gunicorn worker, though I have not seen any difference
when using werkzeug's run_simple for synchronous requests.

**Decorators**: `@retry(retry=retry_if_exception_type(AssertionError), stop=stop_after_attempt(3), wait=wait_fixed(0.5), reraise=True)`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_homepage_resolver(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_consistent_build_version(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_list_single_query(self)

get_list should only perform single query.

Note:
this test will work only as Admistrator.
other users will have permission queries - so share conditions will be added.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_no_ifnull_checks(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_no_stale_ref_sql(self)

frappe.db.sql should not hold any internal references to result set.

pymysql stores results internally. If your code reads a lot and doesn't make another
query, for that entire duration there's copy of result consuming memory in internal
attributes of pymysql.
We clear it manually, this test ensures that it actually works.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_no_cyclic_references(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_doc_cache_calls(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_local_caching(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_redis_cache_calls(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_idle_cpu_utilization_redis_pubsub(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cpu_allocation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestOverheadCalls

Test that typical redis and db calls remain same overtime.

If this tests fail on your PR, make sure you're not introducing something in hot-path of these
endpoints. Only update values if you're really sure that's the right call.
Every call increase here is an actual increase in cost!

**Inherits from**: FrappeAPITestCase

#### Methods

##### test_ping_overheads(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_ping_overheads_authenticated(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_list_view_overheads(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_doc_overheads(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### redis_cached_func()

**Returns**: (none)


