# API Reference: messages.py

**Language**: Python

**Source**: `utils/messages.py`

---

## Functions

### msgprint(msg: str | Sequence[str] | Sequence[Sequence[str]], title: str | None = None, raise_exception: bool | type[Exception] | Exception = False, as_table: bool = False, as_list: bool = False, indicator: Literal['blue', 'green', 'orange', 'red', 'yellow'] | None = None, alert: bool = False, primary_action: dict | None = None, is_minimizable: bool = False, wide: bool = False) → None

Print a message to the user (via HTTP response).
Messages are sent in the `__server_messages` property in the
response JSON and shown in a pop-up / modal.

:param msg: Message.
:param title: [optional] Message title. Default: "Message".
:param raise_exception: [optional] Raise given exception and show message.
:param as_table: [optional] If `msg` is a list of lists, render as HTML table.
:param as_list: [optional] If `msg` is a list, render as un-ordered list.
:param primary_action: [optional] Bind a primary server/client side action.
:param is_minimizable: [optional] Allow users to minimize the modal
:param wide: [optional] Show wide modal
:param realtime: Publish message immediately using websocket.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| msg | str | Sequence[str] | Sequence[Sequence[str]] | - | - |
| title | str | None | None | - |
| raise_exception | bool | type[Exception] | Exception | False | - |
| as_table | bool | False | - |
| as_list | bool | False | - |
| indicator | Literal['blue', 'green', 'orange', 'red', 'yellow'] | None | None | - |
| alert | bool | False | - |
| primary_action | dict | None | None | - |
| is_minimizable | bool | False | - |
| wide | bool | False | - |

**Returns**: `None`



### toast(message: str, indicator: Literal['blue', 'green', 'orange', 'red', 'yellow'] | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| message | str | - | - |
| indicator | Literal['blue', 'green', 'orange', 'red', 'yellow'] | None | None | - |

**Returns**: (none)



### clear_messages()

**Returns**: (none)



### get_message_log() → list[dict]

**Returns**: `list[dict]`



### clear_last_message()

**Returns**: (none)



### throw(msg: str | Sequence[str], exc: type[Exception] | Exception = frappe.ValidationError, title: str | None = None, is_minimizable: bool = False, wide: bool = False, as_list: bool = False, primary_action = None) → None

Throw execption and show message (`msgprint`).

:param msg: Message.
:param exc: Exception class. Default `frappe.ValidationError`
:param title: [optional] Message title. Default: "Message".
:param is_minimizable: [optional] Allow users to minimize the modal
:param wide: [optional] Show wide modal
:param as_list: [optional] If `msg` is a list, render as un-ordered list.
:param primary_action: [optional] Bind a primary server/client side action.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| msg | str | Sequence[str] | - | - |
| exc | type[Exception] | Exception | frappe.ValidationError | - |
| title | str | None | None | - |
| is_minimizable | bool | False | - |
| wide | bool | False | - |
| as_list | bool | False | - |
| primary_action | None | None | - |

**Returns**: `None`



### throw_permission_error()

**Returns**: (none)



### _raise_exception()

**Returns**: (none)


