# API Reference: test_api.py

**Language**: Python

**Source**: `tests/test_api.py`

---

## Classes

### ThreadWithReturnValue

**Inherits from**: Thread

#### Methods

##### __init__(self, group = None, target = None, name = None, args = (), kwargs = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| group | None | None | - |
| target | None | None | - |
| name | None | None | - |
| args | None | () | - |
| kwargs | None | None | - |


##### run(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### join(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### FrappeAPITestCase

**Inherits from**: IntegrationTestCase

#### Methods

##### site_url(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### resource(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### method(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### doctype_path(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_path(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### sid(self) → str

**Decorators**: `@cached_property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `str`


##### get(self, path: str, params: dict | None = None) → TestResponse

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| path | str | - | - |
| params | dict | None | None | - |

**Returns**: `TestResponse`


##### post(self, path, data) → TestResponse

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| path | None | - | - |
| data | None | - | - |

**Returns**: `TestResponse`


##### put(self, path, data) → TestResponse

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| path | None | - | - |
| data | None | - | - |

**Returns**: `TestResponse`


##### patch(self, path, data) → TestResponse

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| path | None | - | - |
| data | None | - | - |

**Returns**: `TestResponse`


##### delete(self, path) → TestResponse

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| path | None | - | - |

**Returns**: `TestResponse`


##### tearDown(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`




### TestResourceAPI

**Inherits from**: FrappeAPITestCase

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### tearDownClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### test_unauthorized_call(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_list(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_list_expand(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_doc_expand(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_list_limit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_list_dict(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_list_debug(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_list_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_create_document(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_document(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_delete_document(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_run_doc_method(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestMethodAPI

**Inherits from**: FrappeAPITestCase

#### Methods

##### test_ping(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_user_info(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auth_cycle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_404s(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_logs(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_array_response(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestReadOnlyMode

During migration if read only mode can be enabled.
Test if reads work well and writes are blocked

**Inherits from**: FrappeAPITestCase

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### test_reads(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_blocked_writes(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestWSGIApp

**Inherits from**: FrappeAPITestCase

#### Methods

##### test_request_hooks(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestAPIResponse

**Inherits from**: FrappeAPITestCase

#### Methods

##### test_generate_pdf(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_binary_and_csv_response(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_download_private_file_with_unique_url(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_login_redirects(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### suppress_stdout()

Supress stdout for tests which expectedly make noise
but that you don't need in tests

**Returns**: (none)



### make_request(target: str, args: tuple | None = None, kwargs: dict | None = None, site: str | None = None) → TestResponse

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| target | str | - | - |
| args | tuple | None | None | - |
| kwargs | dict | None | None | - |
| site | str | None | None | - |

**Returns**: `TestResponse`



### patch_request_header(key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | None | - | - |

**Returns**: (none)



### before_request()

**Returns**: (none)



### after_request()

**Returns**: (none)



### generate_admin_keys()

**Returns**: (none)



### test()

**Returns**: (none)



### test_array(data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |

**Returns**: (none)



### get_message(resp, msg_type)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| resp | None | - | - |
| msg_type | None | - | - |

**Returns**: (none)



### download_template(file_type)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| file_type | None | - | - |

**Returns**: (none)


