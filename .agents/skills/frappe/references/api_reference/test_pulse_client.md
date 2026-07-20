# API Reference: test_pulse_client.py

**Language**: Python

**Source**: `utils/telemetry/pulse/test_pulse_client.py`

---

## Classes

### TestPulseClient

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestEventQueue

**Inherits from**: TestPulseClient

#### Methods

##### test_queue_operations(self)

Test queue add, collect, and FIFO behavior

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_queue_size_limit(self)

Test that queue respects size limit

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_requeue_events(self)

Test requeueing events preserves order

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestRateLimiting

**Inherits from**: TestPulseClient

#### Methods

##### test_ratelimit_basic(self)

Test basic rate limiting functionality

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_ratelimit_different_events(self)

Test that rate limiting is per-event

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_ratelimit_expiry(self)

Test that rate limit expires after interval

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestBatchProcessing

**Inherits from**: TestPulseClient

#### Methods

##### test_batch_process_success(self)

Test successful batch processing

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_batch_process_with_failure_and_retry(self)

Test batch processing with failure and retry

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_batch_process_max_retries_exceeded(self)

Test batch processing when max retries is exceeded

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestCapture

**Inherits from**: TestPulseClient

#### Methods

##### test_capture_when_disabled(self, mock_enabled)

Test that capture does nothing when disabled

**Decorators**: `@patch('frappe.utils.telemetry.pulse.client.is_enabled')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| mock_enabled | None | - | - |


##### test_capture_basic(self, mock_enabled)

Test basic event capture

**Decorators**: `@patch('frappe.utils.telemetry.pulse.client.is_enabled')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| mock_enabled | None | - | - |


##### test_capture_anonymizes_user(self, mock_enabled)

Test that user is anonymized

**Decorators**: `@patch('frappe.utils.telemetry.pulse.client.is_enabled')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| mock_enabled | None | - | - |




### TestUtils

**Inherits from**: TestPulseClient

#### Methods

##### test_parse_interval(self)

Test parsing various interval formats

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_anonymize_user(self)

Test user anonymization

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestEventQueueDecoding

**Inherits from**: TestPulseClient

#### Methods

##### test_decode_valid_event(self)

Test decoding valid event JSON

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_decode_invalid_json(self)

Test decoding invalid JSON

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestEventKey

**Inherits from**: TestPulseClient

#### Methods

##### test_event_key_generation_and_uniqueness(self)

Test event key generation and uniqueness for rate limiting

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### process_fn(events)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| events | None | - | - |

**Returns**: (none)



### failing_fn(events)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| events | None | - | - |

**Returns**: (none)



### always_failing_fn(events)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| events | None | - | - |

**Returns**: (none)


