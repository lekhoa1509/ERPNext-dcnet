# API Reference: test_currency_exchange.py

**Language**: Python

**Source**: `doctype/currency_exchange/test_currency_exchange.py`

---

## Classes

### TestCurrencyExchange

**Inherits from**: IntegrationTestCase

#### Methods

##### clear_cache(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_exchange_rate(self, mock_get)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| mock_get | None | - | - |


##### test_exchange_rate_via_exchangerate_host(self, mock_get)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| mock_get | None | - | - |


##### test_exchange_rate_strict(self, mock_get)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| mock_get | None | - | - |


##### test_exchange_rate_strict_switched(self, mock_get)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| mock_get | None | - | - |




### PatchResponse

**Inherits from**: (none)

#### Methods

##### __init__(self, json_data, status_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| json_data | None | - | - |
| status_code | None | - | - |


##### raise_for_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### json(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### save_new_records(test_records)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| test_records | None | - | - |

**Returns**: (none)



### patched_requests_get()

**Returns**: (none)


