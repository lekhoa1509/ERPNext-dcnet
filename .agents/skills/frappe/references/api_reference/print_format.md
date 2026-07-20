# API Reference: print_format.py

**Language**: Python

**Source**: `utils/print_format.py`

---

## Functions

### download_multi_pdf(doctype: str | dict[str, list[str]], name: str | list[str], format: str | None = None, no_letterhead: bool = False, letterhead: str | None = None, options: str | None = None)

Calls _download_multi_pdf with the given parameters and returns the response

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | dict[str, list[str]] | - | - |
| name | str | list[str] | - | - |
| format | str | None | None | - |
| no_letterhead | bool | False | - |
| letterhead | str | None | None | - |
| options | str | None | None | - |

**Returns**: (none)



### download_multi_pdf_async(doctype: str | dict[str, list[str]], name: str | list[str], format: str | None = None, no_letterhead: bool = False, letterhead: str | None = None, options: str | None = None)

Calls _download_multi_pdf with the given parameters in a background job, returns task ID

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | dict[str, list[str]] | - | - |
| name | str | list[str] | - | - |
| format | str | None | None | - |
| no_letterhead | bool | False | - |
| letterhead | str | None | None | - |
| options | str | None | None | - |

**Returns**: (none)



### _download_multi_pdf(doctype: str | dict[str, list[str]], name: str | list[str], format: str | None = None, no_letterhead: bool = False, letterhead: str | None = None, options: str | None = None, task_id: str | None = None)

Return a PDF compiled by concatenating multiple documents.

The documents can be from a single DocType or multiple DocTypes.

Note: The design may seem a little weird, but it  exists to ensure backward compatibility.
          The correct way to use this function is to pass a dict to doctype as described below

NEW FUNCTIONALITY
=================
Parameters:
doctype (dict):
        key (string): DocType name
        value (list): of strings of doc names which need to be concatenated and printed
name (string):
        name of the pdf which is generated
format:
        Print Format to be used

OLD FUNCTIONALITY - soon to be deprecated
=========================================
Parameters:
doctype (string):
        name of the DocType to which the docs belong which need to be printed
name (string or list):
        If string the name of the doc which needs to be printed
        If list the list of strings of doc names which needs to be printed
format:
        Print Format to be used

Returns:
Publishes a link to the PDF to the given task ID

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | dict[str, list[str]] | - | - |
| name | str | list[str] | - | - |
| format | str | None | None | - |
| no_letterhead | bool | False | - |
| letterhead | str | None | None | - |
| options | str | None | None | - |
| task_id | str | None | None | - |

**Returns**: (none)



### download_pdf(doctype: str, name: str, format = None, doc = None, no_letterhead = 0, language = None, letterhead = None, pdf_generator: Literal['wkhtmltopdf', 'chrome'] | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | str | - | - |
| format | None | None | - |
| doc | None | None | - |
| no_letterhead | None | 0 | - |
| language | None | None | - |
| letterhead | None | None | - |
| pdf_generator | Literal['wkhtmltopdf', 'chrome'] | None | None | - |

**Returns**: (none)



### report_to_pdf(html, orientation = 'Landscape')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| html | None | - | - |
| orientation | None | 'Landscape' | - |

**Returns**: (none)



### print_by_server(doctype, name, printer_setting, print_format = None, doc = None, no_letterhead = 0, file_path = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| printer_setting | None | - | - |
| print_format | None | None | - |
| doc | None | None | - |
| no_letterhead | None | 0 | - |
| file_path | None | None | - |

**Returns**: (none)


