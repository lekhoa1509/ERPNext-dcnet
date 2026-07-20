# API Reference: test_search.py

**Language**: Python

**Source**: `tests/test_search.py`

---

## Classes

### TestSearch

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_search_field_sanitizer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_only_enabled_in_mention(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_link_field_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_link_search_in_foreign_language(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_doctype_search_in_foreign_language(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_validate_and_sanitize_search_inputs(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reference_doctype(self)

search query methods should get reference_doctype if they want

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_search_relevance(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_search_with_paren(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_search_link_with_ignore_user_permissions(self)

Test that ignore_user_permissions works correctly in search_link
when the link field has ignore_user_permissions enabled

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_search_link_ignore_user_permissions_validation(self)

Test that ignore_user_permissions is validated correctly

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_data(doctype, txt, searchfield, start, page_len, filters)

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



### query_with_reference_doctype(doctype, txt, searchfield, start, page_len, filters, reference_doctype = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| txt | None | - | - |
| searchfield | None | - | - |
| start | None | - | - |
| page_len | None | - | - |
| filters | None | - | - |
| reference_doctype | None | None | - |

**Returns**: (none)



### setup_test_link_field_order(TestCase)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| TestCase | None | - | - |

**Returns**: (none)



### custom_translation(language: str, source_text: str, translated_text: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| language | str | - | - |
| source_text | str | - | - |
| translated_text | str | - | - |

**Returns**: (none)



### use_language(language: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| language | str | - | - |

**Returns**: (none)



### teardown_test_link_field_order(TestCase)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| TestCase | None | - | - |

**Returns**: (none)



### do_search(txt: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| txt | str | - | - |

**Returns**: (none)


