# API Reference: path_resolver.py

**Language**: Python

**Source**: `website/path_resolver.py`

---

## Classes

### PathResolver

**Inherits from**: (none)

#### Methods

##### __init__(self, path, http_status_code = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| path | None | - | - |
| http_status_code | None | None | - |


##### resolve(self)

Return endpoint and a renderer instance that can render the endpoint.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_valid_path(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_custom_page_renderers()

**Decorators**: `@staticmethod`




## Functions

### resolve_redirect(path, query_string = None)

Resolve redirects from hooks

Example:

                website_redirect = [
                                # absolute location
                                {"source": "/from", "target": "https://mysite/from"},

                                # relative location
                                {"source": "/from", "target": "/main"},

                                # use regex
                                {"source": r"/from/(.*)", "target": r"/main/"}
                                # use r as a string prefix if you use regex groups or want to escape any string literal
                ]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |
| query_string | None | None | - |

**Returns**: (none)



### resolve_path(path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |

**Returns**: (none)



### resolve_from_map(path)

transform dynamic route to a static one from hooks and route defined in doctype

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |

**Returns**: (none)



### get_website_rules()

Get website route rules from hooks and DocType route

**Returns**: (none)



### validate_path(path: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | str | - | - |

**Returns**: (none)



### raise_redirect(redirect_location, status_code = 301, forward_query_params = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| redirect_location | None | - | - |
| status_code | None | 301 | - |
| forward_query_params | None | False | - |

**Returns**: (none)



### _get()

**Returns**: (none)


