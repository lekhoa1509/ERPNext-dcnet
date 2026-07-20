# API Reference: page.py

**Language**: Python

**Source**: `utils/pdf_generator/page.py`

---

## Classes

### Page

**Inherits from**: (none)

#### Methods

##### __init__(self, session, browser_context_id, page_type)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| session | None | - | - |
| browser_context_id | None | - | - |
| page_type | None | - | - |


##### send(self, method, params = None, return_future = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| method | None | - | - |
| params | None | None | - |
| return_future | None | False | - |


##### get_frame_id_on_demand(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _ensure_frame_id(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_media_emulation(self, media_type: str = 'print')

Set media emulation for the page.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| media_type | str | 'print' | - |


##### set_cookies(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### intercept_request_and_fulfill(self, url_pattern)

Starts intercepting network requests for the given target_id and URL pattern.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| url_pattern | None | - | - |


##### intercept_request_for_local_resources(self, url_pattern = '*')

Starts intercepting network requests for the given target_id and URL pattern.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| url_pattern | None | '*' | - |


##### set_tab_url(self, url)

Navigate to a URL and fulfill the request with status code 200.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| url | None | - | - |


##### evaluate(self, expression, await_promise = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| expression | None | - | - |
| await_promise | None | False | - |


##### set_content(self, html, wait_for = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| html | None | - | - |
| wait_for | None | None | - |


##### wait_for_load(self, wait_for, timeout = 60)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| wait_for | None | - | - |
| timeout | None | 60 | - |


##### get_element_height(self, selector = 'body')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| selector | None | 'body' | - |


##### add_page_size_css(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### generate_pdf(self, wait_for_pdf = True, raw = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| wait_for_pdf | None | True | - |
| raw | None | False | - |


##### get_pdf_stream_id(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_pdf_from_stream(self, stream_id, raw = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| stream_id | None | - | - |
| raw | None | False | - |


##### close(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### on_request_paused_event(future, response)

Callback for when a request is paused (intercepted).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| future | None | - | - |
| response | None | - | - |

**Returns**: (none)



### intercept_and_fulfill()

**Returns**: (none)



### on_request_paused_event(future, response)

Callback for when a request is paused (intercepted).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| future | None | - | - |
| response | None | - | - |

**Returns**: (none)



### wait_for_navigate()

**Returns**: (none)



### on_lifecycle_event(future, response)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| future | None | - | - |
| response | None | - | - |

**Returns**: (none)



### start_wait()

**Returns**: (none)


