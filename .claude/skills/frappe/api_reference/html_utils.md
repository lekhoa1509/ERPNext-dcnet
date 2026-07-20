# API Reference: html_utils.py

**Language**: Python

**Source**: `utils/html_utils.py`

---

## Functions

### clean_html(html)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| html | None | - | - |

**Returns**: (none)



### clean_email_html(html)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| html | None | - | - |

**Returns**: (none)



### clean_script_and_style(html)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| html | None | - | - |

**Returns**: (none)



### sanitize_html(html, linkify = False, always_sanitize = False)

Sanitize HTML tags, attributes and style to prevent XSS attacks
Based on bleach clean, bleach whitelist and html5lib's Sanitizer defaults

Does not sanitize JSON unless explicitly specified, as it could lead to future problems

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| html | None | - | - |
| linkify | None | False | - |
| always_sanitize | None | False | - |

**Returns**: (none)



### is_json(text)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| text | None | - | - |

**Returns**: (none)



### get_icon_html(icon, small = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| icon | None | - | - |
| small | None | False | - |

**Returns**: (none)



### unescape_html(value)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| value | None | - | - |

**Returns**: (none)



### attributes_filter(tag, name, value)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| tag | None | - | - |
| name | None | - | - |
| value | None | - | - |

**Returns**: (none)


