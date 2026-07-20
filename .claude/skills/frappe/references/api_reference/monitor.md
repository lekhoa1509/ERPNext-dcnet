# API Reference: monitor.py

**Language**: Python

**Source**: `monitor.py`

---

## Classes

### Monitor

**Inherits from**: (none)

#### Methods

##### __init__(self, transaction_type, method, kwargs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| transaction_type | None | - | - |
| method | None | - | - |
| kwargs | None | - | - |


##### collect_request_meta(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### collect_job_meta(self, method, kwargs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| method | None | - | - |
| kwargs | None | - | - |


##### add_custom_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### dump(self, response = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| response | None | None | - |


##### store(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### start(transaction_type = 'request', method = None, kwargs = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| transaction_type | None | 'request' | - |
| method | None | None | - |
| kwargs | None | None | - |

**Returns**: (none)



### stop(response = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| response | None | None | - |

**Returns**: (none)



### add_data_to_monitor() → None

Add additional custom key-value pairs along with monitor log.
Note: Key-value pairs should be simple JSON exportable types.

**Returns**: `None`



### get_trace_id() → str | None

Get unique ID for current transaction.

**Returns**: `str | None`



### log_file()

**Returns**: (none)



### flush()

**Returns**: (none)


