# API Reference: test_delivery_trip.py

**Language**: Python

**Source**: `doctype/delivery_trip/test_delivery_trip.py`

---

## Classes

### TestDeliveryTrip

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


##### test_delivery_trip_notify_customers(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_unoptimized_route_list_without_locks(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_unoptimized_route_list_with_locks(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_optimized_route_list_without_locks(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_optimized_route_list_with_locks(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_delivery_trip_status_draft(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_delivery_trip_status_scheduled(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_delivery_trip_status_cancelled(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_delivery_trip_status_in_transit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_delivery_trip_status_completed(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_address(driver)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| driver | None | - | - |

**Returns**: (none)



### create_driver()

**Returns**: (none)



### create_delivery_notification()

**Returns**: (none)



### create_vehicle()

**Returns**: (none)



### create_delivery_trip(driver, address, contact = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| driver | None | - | - |
| address | None | - | - |
| contact | None | None | - |

**Returns**: (none)


