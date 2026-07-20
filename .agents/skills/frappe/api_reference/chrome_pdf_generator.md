# API Reference: chrome_pdf_generator.py

**Language**: Python

**Source**: `utils/pdf_generator/chrome_pdf_generator.py`

---

## Classes

### ChromePDFGenerator

**Inherits from**: (none)

#### Methods

##### add_browser(self, browser)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| browser | None | - | - |


##### remove_browser(self, browser)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| browser | None | - | - |


##### __new__(cls)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### __init__(self)

Initialize only once.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _initialize_chromium(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _verify_chromium_installation(self)

Ensures Chromium is available and executable, raising clearer errors if not.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### start_chromium_process(self, debug = False)

Launches Chromium in headless mode with robust logging and error handling.
chrome switches
https://peter.sh/experiments/chromium-command-line-switches/

NOTE: dbus issue in docker
  https://source.chromium.org/chromium/chromium/src/+/main:content/app/content_main.cc;l=229-241?q=DBUS_SESSION_BUS_ADDRESS&ss=chromium

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| debug | None | False | - |


##### _start_chromium_process(self, command_args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| command_args | None | - | - |


##### _set_devtools_url(self)

Monitor Chromium's stderr for the DevTools WebSocket URL
----------------
other approch: if we choose port using find_available_port we can avoid this entirely and fetch_devtools_url() method.

NOTE:   1) in current approch output to stderr is pretty consistent.
                2) other approch may seem reliable but it is slow compared to this in testing.

TODO:
final approch can be decided later after testing in production.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _close_browser(self)

Close the headless Chromium browser.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### fetch_devtools_url(self, port)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| port | None | - | - |



