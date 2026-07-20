# API Reference: website_search.py

**Language**: Python

**Source**: `search/website_search.py`

---

## Classes

### WebsiteSearch

Wrapper for WebsiteSearch

**Inherits from**: FullTextSearch

#### Methods

##### get_schema(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_fields_to_search(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_id(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_items_to_index(self)

Get all routes to be indexed, this includes the static pages in www/ and routes from published documents.

Return:
        self (object): FullTextSearch Instance

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_document_to_index(self, route: str) → frappe._dict | None

Render a page and parse it using `BeautifulSoup`.

Args:
        path: route of the page to be parsed

Return a dictionary with title, path and content.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| route | str | - | - |

**Returns**: `frappe._dict | None`


##### parse_result(self, result)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| result | None | - | - |




## Functions

### slugs_with_web_view(_items_to_index)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| _items_to_index | None | - | - |

**Returns**: (none)



### get_static_pages_from_all_apps()

**Returns**: (none)



### update_index_for_path(path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |

**Returns**: (none)



### remove_document_from_index(path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |

**Returns**: (none)



### build_index_for_all_routes()

**Returns**: (none)


