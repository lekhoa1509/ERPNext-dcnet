# API Reference: document_page.py

**Language**: Python

**Source**: `website/page_renderers/document_page.py`

---

## Classes

### DocumentPage

**Inherits from**: BaseTemplatePage

#### Methods

##### can_render(self)

Find a document with matching `route` from all doctypes with `has_web_view`=1

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### search_in_doctypes_with_web_view(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### search_web_page_dynamic_routes(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### render(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_html(self)

**Decorators**: `@cache_html`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_context(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_condition_field(meta)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| meta | None | - | - |




## Functions

### _find_matching_document_webview(route: str) → tuple[str, str] | None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| route | str | - | - |

**Returns**: `tuple[str, str] | None`


