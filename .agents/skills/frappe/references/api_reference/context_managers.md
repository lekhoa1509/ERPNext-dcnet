# API Reference: context_managers.py

**Language**: Python

**Source**: `tests/classes/context_managers.py`

---

## Functions

### freeze_time(time_to_freeze: Any, is_utc: bool = False) → None

Temporarily: freeze time with freezegun.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| time_to_freeze | Any | - | - |
| is_utc | bool | False | - |

**Returns**: `None`



### set_user(user: str)

Temporarily: set the user.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | str | - | - |

**Returns**: (none)



### patch_hooks(overridden_hooks: dict) → None

Temporarily: patch a hook.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| overridden_hooks | dict | - | - |

**Returns**: `None`



### change_settings(commit = False) → None

Temporarily: change settings in a settings doctype.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| commit | None | False | - |

**Returns**: `None`



### switch_site(site: str) → None

Temporarily: drop current connection and switch to a different site.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| site | str | - | - |

**Returns**: `None`



### enable_safe_exec() → None

Temporarily: enable safe exec (server scripts).

**Returns**: `None`



### debug_on() → None

Temporarily: enter an interactive debugger on specified exceptions, default: (AssertionError,).

**Returns**: `None`



### timeout_context(seconds = 30, error_message = 'Operation timed out.') → None

Temporarily: timeout an operation.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| seconds | None | 30 | - |
| error_message | None | 'Operation timed out.' | - |

**Returns**: `None`



### timeout(seconds = 30, error_message = 'Operation timed out.')

Timeout decorator to ensure a test doesn't run for too long.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| seconds | None | 30 | - |
| error_message | None | 'Operation timed out.' | - |

**Returns**: (none)



### trace_fields(doc_class: type, field_name: str | None = None, forbidden_values: list | None = None, custom_validation: Callable | None = None) → 'Document'

A context manager for temporarily tracing fields in a DocType.

Can be used in two ways:
1. Tracing a single field:
   trace_fields(DocType, "field_name", forbidden_values=[...], custom_validation=...)
2. Tracing multiple fields:
   trace_fields(DocType, field1={"forbidden_values": [...], "custom_validation": ...}, ...)

Args:
    doc_class (Document): The DocType class to modify.
    field_name (str, optional): The name of the field to trace (for single field tracing).
    forbidden_values (list, optional): A list of forbidden values for the field (for single field tracing).
    custom_validation (callable, optional): A custom validation function (for single field tracing).
    **field_configs: Keyword arguments for multiple field tracing, where each key is a field name and
                     the value is a dict containing 'forbidden_values' and/or 'custom_validation'.

Yields:
    Document class

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc_class | type | - | - |
| field_name | str | None | None | - |
| forbidden_values | list | None | None | - |
| custom_validation | Callable | None | None | - |

**Returns**: `'Document'`



### patched_hooks(hook = None, default = '_KEEP_DEFAULT_LIST', app_name = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| hook | None | None | - |
| default | None | '_KEEP_DEFAULT_LIST' | - |
| app_name | None | None | - |

**Returns**: (none)



### _handle_timeout(signum, frame)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| signum | None | - | - |
| frame | None | - | - |

**Returns**: (none)



### decorator(func = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| func | None | None | - |

**Returns**: (none)



### new_init(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: (none)



### wrapper()

**Returns**: (none)


