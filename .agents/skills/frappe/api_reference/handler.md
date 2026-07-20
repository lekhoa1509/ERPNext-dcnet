# API Reference: handler.py

**Language**: Python

**Source**: `handler.py`

---

## Functions

### handle()

handle request

**Returns**: (none)



### execute_cmd(cmd, from_async = False)

execute a request as python module

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cmd | None | - | - |
| from_async | None | False | - |

**Returns**: (none)



### run_server_script(server_script)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| server_script | None | - | - |

**Returns**: (none)



### is_valid_http_method(method)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| method | None | - | - |

**Returns**: (none)



### logout()

**Returns**: (none)



### web_logout()

**Returns**: (none)



### upload_file()

**Returns**: (none)



### check_write_permission(doctype: str | None = None, name: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | None | None | - |
| name | str | None | None | - |

**Returns**: (none)



### download_file(file_url: str)

Download file using token and REST API. Valid session or
token is required to download private files.

Method : GET
Endpoints : download_file, frappe.core.doctype.file.file.download_file
URL Params : file_name = /path/to/file relative to site path

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| file_url | str | - | - |

**Returns**: (none)



### get_attr(cmd)

get method object from cmd

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cmd | None | - | - |

**Returns**: (none)



### run_doc_method(method, docs = None, dt = None, dn = None, arg = None, args = None)

run a whitelisted controller method

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| method | None | - | - |
| docs | None | None | - |
| dt | None | None | - |
| dn | None | None | - |
| arg | None | None | - |
| args | None | None | - |

**Returns**: (none)


