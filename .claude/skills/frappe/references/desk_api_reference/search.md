# API Reference: search.py

**Language**: Python

**Source**: `search.py`

---

## Classes

### LinkSearchResults

**Inherits from**: TypedDict



## Functions

### sanitize_searchfield(searchfield: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| searchfield | str | - | - |

**Returns**: (none)



### search_link(doctype: str, txt: str, query: str | None = None, filters: str | dict | list | None = None, page_length: int = 10, searchfield: str | None = None, reference_doctype: str | None = None, ignore_user_permissions: bool = False) → list[LinkSearchResults]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| txt | str | - | - |
| query | str | None | None | - |
| filters | str | dict | list | None | None | - |
| page_length | int | 10 | - |
| searchfield | str | None | None | - |
| reference_doctype | str | None | None | - |
| ignore_user_permissions | bool | False | - |

**Returns**: `list[LinkSearchResults]`



### search_widget(doctype: str, txt: str, query: str | None = None, searchfield: str | None = None, start: int = 0, page_length: int = 10, filters: str | None | dict | list = None, filter_fields = None, as_dict: bool = False, reference_doctype: str | None = None, ignore_user_permissions: bool = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| txt | str | - | - |
| query | str | None | None | - |
| searchfield | str | None | None | - |
| start | int | 0 | - |
| page_length | int | 10 | - |
| filters | str | None | dict | list | None | - |
| filter_fields | None | None | - |
| as_dict | bool | False | - |
| reference_doctype | str | None | None | - |
| ignore_user_permissions | bool | False | - |

**Returns**: (none)



### validate_ignore_user_permissions(form_doctype, link_fieldname, link_doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| form_doctype | None | - | - |
| link_fieldname | None | - | - |
| link_doctype | None | - | - |

**Returns**: (none)



### get_std_fields_list(meta, key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| meta | None | - | - |
| key | None | - | - |

**Returns**: (none)



### build_for_autosuggest(res: list[tuple], doctype: str) → list[LinkSearchResults]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| res | list[tuple] | - | - |
| doctype | str | - | - |

**Returns**: `list[LinkSearchResults]`



### scrub_custom_query(query, key, txt)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| query | None | - | - |
| key | None | - | - |
| txt | None | - | - |

**Returns**: (none)



### relevance_sorter(key, query, as_dict)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | None | - | - |
| query | None | - | - |
| as_dict | None | - | - |

**Returns**: (none)



### get_names_for_mentions(search_term)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| search_term | None | - | - |

**Returns**: (none)



### get_users_for_mentions()

**Returns**: (none)



### get_user_groups()

**Returns**: (none)



### get_link_title(doctype, docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| docname | None | - | - |

**Returns**: (none)



### _throw(message)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| message | None | - | - |

**Returns**: (none)



### to_string(parts)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| parts | None | - | - |

**Returns**: (none)


