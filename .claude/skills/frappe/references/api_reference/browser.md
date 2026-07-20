# API Reference: browser.py

**Language**: Python

**Source**: `utils/pdf_generator/browser.py`

---

## Classes

### Browser

**Inherits from**: (none)

#### Methods

##### __init__(self, generator, print_format, html, options)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| generator | None | - | - |
| print_format | None | - | - |
| html | None | - | - |
| options | None | - | - |


##### open(self, generator)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| generator | None | - | - |


##### create_browser_context(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_html(self, html)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| html | None | - | - |


##### set_options(self, options)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| options | None | - | - |


##### new_page(self, page_type)

# create a new page in the browser inside browser context
----
TODO: Implement Deterministic rendering for headless-chrome via DevTools Protocol ( waiting for macos support )
https://docs.google.com/document/d/1PppegrpXhOzKKAuNlP6XOEnviXFGUiX2hop00Cxcv4o/edit?tab=t.0#bookmark=id.dukbomwxpb3j

NOTE: In theory this will make it faster but more importantly use less cpu, ram etc.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| page_type | None | - | - |


##### setup_body_page(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### close_page(self, type)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| type | None | - | - |


##### is_page_no_used(self, soup)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| soup | None | - | - |


##### prepare_header_footer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### try_async_header_footer_pdf(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _get_converted_num(self, num_str, unit = 'px')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| num_str | None | - | - |
| unit | None | 'px' | - |


##### _parse_pdf_options_from_html(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _set_default_page_size(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### prepare_options_for_pdf(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_rendered_header_footer(self, content, type, head, styles, css)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| content | None | - | - |
| type | None | - | - |
| head | None | - | - |
| styles | None | - | - |
| css | None | - | - |


##### update_header_footer_page(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_header_footer_page_pd(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _open_header_footer_pages(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### close(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### PageSize

**Inherits from**: (none)

#### Methods

##### get(cls, name)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| name | None | - | - |



