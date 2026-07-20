# API Reference: logger.py

**Language**: Python

**Source**: `utils/logger.py`

---

## Classes

### SiteContextFilter

This is a filter which injects request information (if available) into the log.

**Inherits from**: logging.Filter

#### Methods

##### filter(self, record) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| record | None | - | - |

**Returns**: `bool`




## Functions

### create_handler(module, site = None, max_size = 100000, file_count = 20, stream_only = False)

Create and return a Frappe-specific logging handler.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| module | None | - | - |
| site | None | None | - |
| max_size | None | 100000 | - |
| file_count | None | 20 | - |
| stream_only | None | False | - |

**Returns**: (none)



### get_logger(module = None, with_more_info = False, allow_site = True, filter = None, max_size = 100000, file_count = 20, stream_only = stream_logging) → 'logging.Logger'

Return Application Logger for your given module.

Args:
        module (str, optional): Name of your logger and consequently your log file. Defaults to None.
        with_more_info (bool, optional): Will log the form dict using the SiteContextFilter. Defaults to False.
        allow_site ((str, bool), optional): Pass site name to explicitly log under it's logs. If True and unspecified, guesses which site the logs would be saved under. Defaults to True.
        filter (function, optional): Add a filter function for your logger. Defaults to None.
        max_size (int, optional): Max file size of each log file in bytes. Defaults to 100_000.
        file_count (int, optional): Max count of log files to be retained via Log Rotation. Defaults to 20.
        stream_only (bool, optional): Whether to stream logs only to stderr (True) or use log files (False). Defaults to False.

Return a Python logger object with Site and Bench level logging capabilities.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| module | None | None | - |
| with_more_info | None | False | - |
| allow_site | None | True | - |
| filter | None | None | - |
| max_size | None | 100000 | - |
| file_count | None | 20 | - |
| stream_only | None | stream_logging | - |

**Returns**: `'logging.Logger'`



### set_log_level(level: Literal['ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG']) → None

Use this method to set log level to something other than the default DEBUG

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| level | Literal['ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG'] | - | - |

**Returns**: `None`



### sanitized_dict(form_dict)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| form_dict | None | - | - |

**Returns**: (none)


