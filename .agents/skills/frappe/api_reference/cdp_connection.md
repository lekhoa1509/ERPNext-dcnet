# API Reference: cdp_connection.py

**Language**: Python

**Source**: `utils/pdf_generator/cdp_connection.py`

---

## Classes

### CDPSocketClient

Manages WebSocket communications with Chrome DevTools Protocol.
Ensures robust error handling and consistent logging.

**Inherits from**: (none)

#### Methods

##### __init__(self, websocket_url)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| websocket_url | None | - | - |


##### connect(self)

Open the WebSocket connection and start listening for messages.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _connect(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _listen(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _handle_message(self, response)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| response | None | - | - |


##### disconnect(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _disconnect(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### send(self, method, params = None, session_id = None, return_future = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| method | None | - | - |
| params | None | None | - |
| session_id | None | None | - |
| return_future | None | False | - |


##### _send(self, method, params = None, session_id = None, wait_future_fulfill = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| method | None | - | - |
| params | None | None | - |
| session_id | None | None | - |
| wait_future_fulfill | None | True | - |


##### _destructure_response(self, response)

Destructure the response to extract useful information.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| response | None | - | - |


##### start_listener(self, method, callback, session_id = None, target_id = None, frame_id = None)

Register a listener for a specific CDP event with optional filtering.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| method | None | - | - |
| callback | None | - | - |
| session_id | None | None | - |
| target_id | None | None | - |
| frame_id | None | None | - |


##### wait_for_event(self, event, timeout = 3)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| event | None | - | - |
| timeout | None | 3 | - |


##### remove_listener(self, method, event)

Remove a listener for a specific CDP event.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| method | None | - | - |
| event | None | - | - |



