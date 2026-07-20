# API Reference: address.py

**Language**: Python

**Source**: `contacts/doctype/address/address.py`

---

## Classes

### Address

**Inherits from**: Document

#### Methods

##### __setup__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### autoname(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### link_address(self)

Link address based on owner

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_preferred_address(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_display(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### has_link(self, doctype, name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| name | None | - | - |


##### has_common_link(self, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |




## Functions

### get_preferred_address(doctype, name, preferred_key = 'is_primary_address')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| preferred_key | None | 'is_primary_address' | - |

**Returns**: (none)



### get_default_address(doctype: str, name: str | None, sort_key: str = 'is_primary_address') → str | None

Return default Address name for the given doctype, name.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | str | None | - | - |
| sort_key | str | 'is_primary_address' | - |

**Returns**: `str | None`



### get_address_display(address_dict: dict | str | None) → str | None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| address_dict | dict | str | None | - | - |

**Returns**: `str | None`



### render_address(address: dict | str | None, check_permissions = True) → str | None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| address | dict | str | None | - | - |
| check_permissions | None | True | - |

**Returns**: `str | None`



### get_territory_from_address(address)

Tries to match city, state and country of address to existing territory

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| address | None | - | - |

**Returns**: (none)



### get_list_context(context = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | None | None | - |

**Returns**: (none)



### get_address_list(doctype, txt, filters, limit_start, limit_page_length = 20, order_by = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| txt | None | - | - |
| filters | None | - | - |
| limit_start | None | - | - |
| limit_page_length | None | 20 | - |
| order_by | None | None | - |

**Returns**: (none)



### has_website_permission(doc, ptype, user, verbose = False)

Return True if there is a related lead or contact related to this document.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| ptype | None | - | - |
| user | None | - | - |
| verbose | None | False | - |

**Returns**: (none)



### get_address_templates(address)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| address | None | - | - |

**Returns**: (none)



### get_company_address(company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |

**Returns**: (none)



### address_query(doctype, txt, searchfield, start, page_len, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| txt | None | - | - |
| searchfield | None | - | - |
| start | None | - | - |
| page_len | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_condensed_address(doc, no_title = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| no_title | None | False | - |

**Returns**: (none)



### update_preferred_address(address, field)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| address | None | - | - |
| field | None | - | - |

**Returns**: (none)



### get_address_display_list(doctype: str, name: str) → list[dict]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | str | - | - |

**Returns**: `list[dict]`


