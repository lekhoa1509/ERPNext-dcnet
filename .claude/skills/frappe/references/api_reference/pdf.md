# API Reference: pdf.py

**Language**: Python

**Source**: `utils/pdf.py`

---

## Functions

### pdf_header_html(soup, head, content, styles, html_id, css, path = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| soup | None | - | - |
| head | None | - | - |
| content | None | - | - |
| styles | None | - | - |
| html_id | None | - | - |
| css | None | - | - |
| path | None | None | - |

**Returns**: (none)



### pdf_body_html(template, args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| template | None | - | - |
| args | None | - | - |

**Returns**: (none)



### _guess_template_error_line_number(template) → int | None

Guess line on which exception occurred from current traceback.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| template | None | - | - |

**Returns**: `int | None`



### pdf_footer_html(soup, head, content, styles, html_id, css, path = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| soup | None | - | - |
| head | None | - | - |
| content | None | - | - |
| styles | None | - | - |
| html_id | None | - | - |
| css | None | - | - |
| path | None | None | - |

**Returns**: (none)



### get_pdf(html, options = None, output: PdfWriter | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| html | None | - | - |
| options | None | None | - |
| output | PdfWriter | None | None | - |

**Returns**: (none)



### measure_time(func)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| func | None | - | - |

**Returns**: (none)



### get_chrome_pdf(print_format, html, options, output, pdf_generator = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| print_format | None | - | - |
| html | None | - | - |
| options | None | - | - |
| output | None | - | - |
| pdf_generator | None | None | - |

**Returns**: (none)



### get_file_data_from_writer(writer_obj)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| writer_obj | None | - | - |

**Returns**: (none)



### prepare_options(html, options)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| html | None | - | - |
| options | None | - | - |

**Returns**: (none)



### get_cookie_options()

**Returns**: (none)



### read_options_from_html(html)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| html | None | - | - |

**Returns**: (none)



### get_print_format_styles(soup: BeautifulSoup) → list[cssutils.css.Property]

Get styles purely on class 'print-format'.
Valid:
1) .print-format { ... }
2) .print-format, p { ... } | p, .print-format { ... }

Invalid (applied on child elements):
1) .print-format p { ... } | .print-format > p { ... }
2) .print-format #abc { ... }

Returns:
[cssutils.css.Property(name='margin-top', value='50mm', priority=''), ...]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| soup | BeautifulSoup | - | - |

**Returns**: `list[cssutils.css.Property]`



### inline_private_images(html) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| html | None | - | - |

**Returns**: `str`



### _get_base64_image(src)

Return base64 version of image if user has permission to view it

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| src | None | - | - |

**Returns**: (none)



### prepare_header_footer(soup: BeautifulSoup)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| soup | BeautifulSoup | - | - |

**Returns**: (none)



### cleanup(options)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| options | None | - | - |

**Returns**: (none)



### toggle_visible_pdf(soup)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| soup | None | - | - |

**Returns**: (none)



### is_wkhtmltopdf_valid()

**Returns**: (none)



### get_wkhtmltopdf_version()

**Returns**: (none)



### pdf_contains_js(file_content: bytes)

Check if a PDF file contains JavaScript.

Args:
        file_content (bytes): The content of the PDF file.

Returns:
        bool: True if the PDF contains JavaScript, False otherwise and also if the file is encrypted.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| file_content | bytes | - | - |

**Returns**: (none)



### get_host_url()

**Returns**: (none)



### wrapper()

**Returns**: (none)



### has_javascript(obj)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| obj | None | - | - |

**Returns**: (none)


