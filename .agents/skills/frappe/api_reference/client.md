# API Reference: client.py

**Language**: Python

**Source**: `utils/telemetry/pulse/client.py`

---

## Classes

### EventQueue

**Inherits from**: (none)

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### length(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add(self, event, interval = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| event | None | - | - |
| interval | None | None | - |


##### _is_ratelimited(self, event, interval)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| event | None | - | - |
| interval | None | - | - |


##### _get_event_key(self, event)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| event | None | - | - |


##### _update_ratelimit(self, event, interval)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| event | None | - | - |
| interval | None | - | - |


##### _queue_event(self, event)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| event | None | - | - |


##### batch_process(self, fn, batch_size = 100, max_batches = 10, max_retries = 3, backoff_seconds = 1)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fn | None | - | - |
| batch_size | None | 100 | - |
| max_batches | None | 10 | - |
| max_retries | None | 3 | - |
| backoff_seconds | None | 1 | - |


##### collect(self, batch_size = 100)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| batch_size | None | 100 | - |


##### _requeue_events(self, events)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| events | None | - | - |


##### _decode_event(self, event_json)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| event_json | None | - | - |


##### get_events(self, limit = 20)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| limit | None | 20 | - |


##### get_last_sent_events(self, limit = 20)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| limit | None | 20 | - |




## Functions

### is_enabled() → bool

**Returns**: `bool`



### capture(event_name, site = None, app = None, user = None, captured_at = None, properties = None, interval = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| event_name | None | - | - |
| site | None | None | - |
| app | None | None | - |
| user | None | None | - |
| captured_at | None | None | - |
| properties | None | None | - |
| interval | None | None | - |

**Returns**: (none)



### bulk_capture(events)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| events | None | - | - |

**Returns**: (none)



### send_queued_events()

**Returns**: (none)



### post(events)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| events | None | - | - |

**Returns**: (none)



### _create_session()

**Returns**: (none)



### _get_ingest_url()

**Returns**: (none)



### get_debug_info(fetch_events = None, fetch_rate_limited_events = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fetch_events | None | None | - |
| fetch_rate_limited_events | None | None | - |

**Returns**: (none)


