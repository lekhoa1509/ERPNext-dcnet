# API Reference: print_utils.py

**Language**: Python

**Source**: `utils/print_utils.py`

---

## Functions

### get_print(doctype = None, name = None, print_format = None, style = None, as_pdf = False, doc = None, output = None, no_letterhead = 0, password = None, pdf_options = None, letterhead = None, pdf_generator: Literal['wkhtmltopdf', 'chrome'] | None = None)

Get Print Format for given document.
:param doctype: DocType of document.
:param name: Name of document.
:param print_format: Print Format name. Default 'Standard',
:param style: Print Format style.
:param as_pdf: Return as PDF. Default False.
:param password: Password to encrypt the pdf with. Default None
:param pdf_generator: PDF generator to use. Default 'wkhtmltopdf'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | None | - |
| name | None | None | - |
| print_format | None | None | - |
| style | None | None | - |
| as_pdf | None | False | - |
| doc | None | None | - |
| output | None | None | - |
| no_letterhead | None | 0 | - |
| password | None | None | - |
| pdf_options | None | None | - |
| letterhead | None | None | - |
| pdf_generator | Literal['wkhtmltopdf', 'chrome'] | None | None | - |

**Returns**: (none)



### attach_print(doctype, name, file_name = None, print_format = None, style = None, html = None, doc = None, lang = None, print_letterhead = True, password = None, letterhead = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| file_name | None | None | - |
| print_format | None | None | - |
| style | None | None | - |
| html | None | None | - |
| doc | None | None | - |
| lang | None | None | - |
| print_letterhead | None | True | - |
| password | None | None | - |
| letterhead | None | None | - |

**Returns**: (none)



### setup_chromium()

Setup Chromium at the bench level.

**Returns**: (none)



### find_or_download_chromium_executable()

Finds the Chromium executable or downloads if not found.

**Returns**: (none)



### download_chromium()

**Returns**: (none)



### get_chromium_download_url()

**Returns**: (none)



### make_chromium_executable(executable)

Make the Chromium executable.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| executable | None | - | - |

**Returns**: (none)



### calculate_platform()

Determines the host platform and returns it as a string.
Includes logic for Linux ARM, Linux x64, macOS (Intel and ARM), and Windows (32-bit and 64-bit).

Returns:
        str: The detected platform string (e.g., 'linux64', 'mac-arm64', etc.).

**Returns**: (none)



### get_linux_distribution_info()

Retrieve Linux distribution information using the `distro` library.

**Returns**: (none)



### parse_float_and_unit(input_text, default_unit = 'px')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| input_text | None | - | - |
| default_unit | None | 'px' | - |

**Returns**: (none)



### convert_uom(number: float, from_uom: Literal['px', 'mm', 'cm', 'in'] = 'px', to_uom: Literal['px', 'mm', 'cm', 'in'] = 'px', only_number: bool = False) → float

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| number | float | - | - |
| from_uom | Literal['px', 'mm', 'cm', 'in'] | 'px' | - |
| to_uom | Literal['px', 'mm', 'cm', 'in'] | 'px' | - |
| only_number | bool | False | - |

**Returns**: `float`


