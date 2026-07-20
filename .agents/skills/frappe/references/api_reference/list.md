# API Reference: list.py

**Language**: Python

**Source**: `www/list.py`

---

## Functions

### get_list_data(doctype: str, txt: str | None = None, limit_start: int = 0, fields: list | None = None, cmd: str | None = None, limit: int = 20, web_form_name: str | None = None)

Return processed HTML page for a standard listing.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| txt | str | None | None | - |
| limit_start | int | 0 | - |
| fields | list | None | None | - |
| cmd | str | None | None | - |
| limit | int | 20 | - |
| web_form_name | str | None | None | - |

**Returns**: (none)



### prepare_filters(doctype, controller, kwargs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| controller | None | - | - |
| kwargs | None | - | - |

**Returns**: (none)



### get_list_context(context, doctype, web_form_name = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | None | - | - |
| doctype | None | - | - |
| web_form_name | None | None | - |

**Returns**: (none)



### get_list(doctype, txt, filters, limit_start, limit_page_length = 20, ignore_permissions = False, fields = None, order_by = None, or_filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| txt | None | - | - |
| filters | None | - | - |
| limit_start | None | - | - |
| limit_page_length | None | 20 | - |
| ignore_permissions | None | False | - |
| fields | None | None | - |
| order_by | None | None | - |
| or_filters | None | None | - |

**Returns**: (none)



### update_context_from_module(module, list_context)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| module | None | - | - |
| list_context | None | - | - |

**Returns**: (none)


