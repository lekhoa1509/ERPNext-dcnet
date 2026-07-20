# API Reference: web_page.py

**Language**: Python

**Source**: `website/doctype/web_page/web_page.py`

---

## Classes

### WebPage

**Inherits from**: WebsiteGenerator

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_context(self, context)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| context | None | - | - |


##### render_dynamic(self, context)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| context | None | - | - |


##### set_breadcrumbs(self, context)

Build breadcrumbs template

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| context | None | - | - |


##### set_title_and_header(self, context)

Extract and set title and header from content or context.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| context | None | - | - |


##### set_page_blocks(self, context)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| context | None | - | - |


##### add_hero(self, context)

Add a hero element if specified in content or hooks.
Hero elements get full page width.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| context | None | - | - |


##### check_for_redirect(self, context)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| context | None | - | - |


##### set_metatags(self, context)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| context | None | - | - |


##### validate_dates(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### check_publish_status()

**Returns**: (none)



### get_web_blocks_html(blocks)

Convert a list of blocks into Raw HTML and extract out their scripts for deduplication.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| blocks | None | - | - |

**Returns**: (none)



### extract_script_and_style_tags(html)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| html | None | - | - |

**Returns**: (none)



### get_dynamic_web_pages() → dict[str, str]

**Returns**: `dict[str, str]`


