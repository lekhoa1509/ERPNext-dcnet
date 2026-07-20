# API Reference: weasyprint.py

**Language**: Python

**Source**: `utils/weasyprint.py`

---

## Classes

### PrintFormatGenerator

Generate a PDF of a Document, with repeatable header and footer if letterhead is provided.

This generator draws its inspiration and, also a bit of its implementation, from this
discussion in the library github issues: https://github.com/Kozea/WeasyPrint/issues/92

**Inherits from**: (none)

#### Methods

##### __init__(self, print_format, doc, letterhead = None)

Parameters
----------
print_format: str
        Name of the Print Format
doc: str
        Document to print
letterhead: str
        Letter Head to apply (optional)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| print_format | None | - | - |
| doc | None | - | - |
| letterhead | None | None | - |


##### build_context(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_html_preview(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_main_html(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_header_footer_html(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### render_pdf(self)

Return a bytes sequence of the rendered PDF.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _compute_overlay_element(self, element: str)

Parameters
----------
element: str
        Either 'header' or 'footer'

Returns
-------
element_body: BlockBox
        A Weasyprint pre-rendered representation of an html element
element_height: float
        The height of this element, which will be then translated in a html height

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| element | str | - | - |


##### _apply_overlay_on_main(self, main_doc, header_body = None, footer_body = None)

Insert the header and the footer in the main document.

Parameters
----------
main_doc: Document
        The top level representation for a PDF page in Weasyprint.
header_body: BlockBox
        A representation for an html element in Weasyprint.
footer_body: BlockBox
        A representation for an html element in Weasyprint.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| main_doc | None | - | - |
| header_body | None | None | - |
| footer_body | None | None | - |


##### _make_header_footer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_layout(self, print_format)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| print_format | None | - | - |


##### set_field_renderers(self, layout)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| layout | None | - | - |


##### process_margin_texts(self, layout)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| layout | None | - | - |


##### get_element(boxes, element)

Given a set of boxes representing the elements of a PDF page in a DOM-like way, find the
box which is named `element`.

Look at the notes of the class for more details on Weasyprint insides.

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| boxes | None | - | - |
| element | None | - | - |




## Functions

### download_pdf(doctype, name, print_format, letterhead = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| print_format | None | - | - |
| letterhead | None | None | - |

**Returns**: (none)



### get_html(doctype, name, print_format, letterhead = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| print_format | None | - | - |
| letterhead | None | None | - |

**Returns**: (none)



### import_weasyprint()

**Returns**: (none)


