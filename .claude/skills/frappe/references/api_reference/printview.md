# API Reference: printview.py

**Language**: Python

**Source**: `www/printview.py`

---

## Classes

### PrintContext

**Inherits from**: TypedDict



## Functions

### get_context(context) → PrintContext

Build context for print

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | None | - | - |

**Returns**: `PrintContext`



### get_print_format_doc(print_format_name: str, meta: 'Meta') → 'PrintFormat' | None

Return print format document.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| print_format_name | str | - | - |
| meta | 'Meta' | - | - |

**Returns**: `'PrintFormat' | None`



### get_rendered_template(doc: 'Document', print_format: 'PrintFormat' | None = None, meta: 'Meta' = None, no_letterhead: bool | None = None, letterhead: str | None = None, trigger_print: bool = False, settings: dict | None = None) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | 'Document' | - | - |
| print_format | 'PrintFormat' | None | None | - |
| meta | 'Meta' | None | - |
| no_letterhead | bool | None | None | - |
| letterhead | str | None | None | - |
| trigger_print | bool | False | - |
| settings | dict | None | None | - |

**Returns**: `str`



### set_link_titles(doc: 'Document') → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | 'Document' | - | - |

**Returns**: `None`



### set_title_values_for_link_and_dynamic_link_fields(meta: 'Meta', doc: 'Document', parent_doc: 'Document' | None = None) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| meta | 'Meta' | - | - |
| doc | 'Document' | - | - |
| parent_doc | 'Document' | None | None | - |

**Returns**: `None`



### set_title_values_for_table_and_multiselect_fields(meta: 'Meta', doc: 'Document') → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| meta | 'Meta' | - | - |
| doc | 'Document' | - | - |

**Returns**: `None`



### convert_markdown(doc: 'Document') → None

Convert text field values to markdown if necessary.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | 'Document' | - | - |

**Returns**: `None`



### get_html_and_style(doc: str, name: str | None = None, print_format: str | None = None, no_letterhead: bool | None = None, letterhead: str | None = None, trigger_print: bool = False, style: str | None = None, settings: str | None = None) → dict[str, str | None]

Return `html` and `style` of print format, used in PDF etc.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | str | - | - |
| name | str | None | None | - |
| print_format | str | None | None | - |
| no_letterhead | bool | None | None | - |
| letterhead | str | None | None | - |
| trigger_print | bool | False | - |
| style | str | None | None | - |
| settings | str | None | None | - |

**Returns**: `dict[str, str | None]`



### get_rendered_raw_commands(doc: str, name: str | None = None, print_format: str | None = None) → dict

Return Rendered Raw Commands of print format, used to send directly to printer.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | str | - | - |
| name | str | None | None | - |
| print_format | str | None | None | - |

**Returns**: `dict`



### validate_print_permission(doc: 'Document') → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | 'Document' | - | - |

**Returns**: `None`



### validate_key(key: str, doc: 'Document') → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | str | - | - |
| doc | 'Document' | - | - |

**Returns**: `None`



### get_letter_head(doc: 'Document', no_letterhead: bool, letterhead: str | None = None) → dict

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | 'Document' | - | - |
| no_letterhead | bool | - | - |
| letterhead | str | None | None | - |

**Returns**: `dict`



### get_print_format(doctype: str, print_format: 'PrintFormat') → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| print_format | 'PrintFormat' | - | - |

**Returns**: `str`



### make_layout(doc: 'Document', meta: 'Meta', format_data = None) → list

Builds a hierarchical layout object from the fields list to be rendered
by `standard.html`

:param doc: Document to be rendered.
:param meta: Document meta object (doctype).
:param format_data: Fields sequence and properties defined by Print Format Builder.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | 'Document' | - | - |
| meta | 'Meta' | - | - |
| format_data | None | None | - |

**Returns**: `list`



### is_visible(df: 'DocField', doc: 'Document') → bool

Return True if docfield is visible in print layout and does not have print_hide set.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| df | 'DocField' | - | - |
| doc | 'Document' | - | - |

**Returns**: `bool`



### has_value(df: 'DocField', doc: 'Document') → bool

Return True if given docfield (`df`) has some value in the given document (`doc`).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| df | 'DocField' | - | - |
| doc | 'Document' | - | - |

**Returns**: `bool`



### get_print_style(style: str | None = None, print_format: 'PrintFormat' | None = None, for_legacy: bool = False) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| style | str | None | None | - |
| print_format | 'PrintFormat' | None | None | - |
| for_legacy | bool | False | - |

**Returns**: `str`



### get_font(print_settings: 'PrintSettings', print_format: 'PrintFormat' | None = None, for_legacy = False) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| print_settings | 'PrintSettings' | - | - |
| print_format | 'PrintFormat' | None | None | - |
| for_legacy | None | False | - |

**Returns**: `str`



### get_visible_columns(data: list, table_meta: 'Meta', df: 'DocField') → list['DocField']

Return list of visible columns based on print_hide and if all columns have value.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | list | - | - |
| table_meta | 'Meta' | - | - |
| df | 'DocField' | - | - |

**Returns**: `list['DocField']`



### column_has_value(data: list, fieldname: str, col_df: 'DocField') → bool

Check if at least one cell in column has non-zero and non-blank value

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | list | - | - |
| fieldname | str | - | - |
| col_df | 'DocField' | - | - |

**Returns**: `bool`



### get_new_section()

**Returns**: (none)



### append_empty_field_dict_to_page_column(page)

append empty columns dict to page layout

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| page | None | - | - |

**Returns**: (none)



### add_column(col_df: 'DocField')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| col_df | 'DocField' | - | - |

**Returns**: (none)



### get_template_from_string()

**Returns**: (none)


