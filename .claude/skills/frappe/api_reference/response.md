# API Reference: response.py

**Language**: Python

**Source**: `utils/response.py`

---

## Functions

### report_error(status_code)

Build error. Show traceback in developer mode

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| status_code | None | - | - |

**Returns**: (none)



### is_traceback_allowed()

**Returns**: (none)



### _link_error_with_message_log(error_log, exception, message_logs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| error_log | None | - | - |
| exception | None | - | - |
| message_logs | None | - | - |

**Returns**: (none)



### build_response(response_type = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| response_type | None | None | - |

**Returns**: (none)



### as_csv()

**Returns**: (none)



### as_txt()

**Returns**: (none)



### as_raw()

**Returns**: (none)



### as_json()

**Returns**: (none)



### as_pdf()

**Returns**: (none)



### as_binary()

**Returns**: (none)



### make_logs()

make strings for msgprint and errprint

**Returns**: (none)



### _make_logs_v1()

**Returns**: (none)



### _make_logs_v2()

**Returns**: (none)



### json_handler(obj)

serialize non-serializable data for json

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| obj | None | - | - |

**Returns**: (none)



### as_page()

print web page

**Returns**: (none)



### redirect()

**Returns**: (none)



### download_backup(path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |

**Returns**: (none)



### download_private_file(path: str) → Response

Checks permissions and sends back private file

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | str | - | - |

**Returns**: `Response`



### send_private_file(path: str) → Response

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | str | - | - |

**Returns**: `Response`



### handle_session_stopped()

**Returns**: (none)


