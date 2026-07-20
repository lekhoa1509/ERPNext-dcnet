# API Reference: number_card.py

**Language**: Python

**Source**: `doctype/number_card/number_card.py`

---

## Classes

### NumberCard

**Inherits from**: Document

#### Methods

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


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_permission_query_conditions(user = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | None | - |

**Returns**: (none)



### has_permission(doc, ptype, user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| ptype | None | - | - |
| user | None | - | - |

**Returns**: (none)



### get_result(doc, filters, to_date = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| filters | None | - | - |
| to_date | None | None | - |

**Returns**: (none)



### get_percentage_difference(doc, filters, result)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| filters | None | - | - |
| result | None | - | - |

**Returns**: (none)



### calculate_previous_result(doc, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### create_number_card(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### get_cards_for_user(doctype, txt, searchfield, start, page_len, filters)

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



### create_report_number_card(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### add_card_to_dashboard(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)


