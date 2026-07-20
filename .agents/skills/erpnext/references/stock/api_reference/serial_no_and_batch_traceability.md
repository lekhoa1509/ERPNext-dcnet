# API Reference: serial_no_and_batch_traceability.py

**Language**: Python

**Source**: `report/serial_no_and_batch_traceability/serial_no_and_batch_traceability.py`

---

## Classes

### ReportData

**Inherits from**: (none)

#### Methods

##### __init__(self, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| filters | None | - | - |


##### validate_filters(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### parse_batch_details(self, sabb_data_details, data, direction, indent = 0)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sabb_data_details | None | - | - |
| data | None | - | - |
| direction | None | - | - |
| indent | None | 0 | - |


##### prepare_source_data(self, data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| data | None | - | - |


##### get_data_from_sabb(self, row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |


##### set_backward_data(self, sabb_data, qty = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sabb_data | None | - | - |
| qty | None | None | - |


##### get_serial_no_batches(self, name = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | None | None | - |


##### get_doctype(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_materials(self, sabb_data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sabb_data | None | - | - |


##### set_forward_data(self, value, sabb_data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| value | None | - | - |
| sabb_data | None | - | - |


##### add_direct_outward_entry(self, row, batch_details)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| batch_details | None | - | - |


##### get_sabb_entries(self, value, type_of_transaction = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| value | None | - | - |
| type_of_transaction | None | None | - |


##### process_manufacture_or_repack_entry(self, row, batch_details)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| batch_details | None | - | - |


##### get_finished_item_from_stock_entry(self, reference_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| reference_name | None | - | - |


##### get_serial_batch_no(self, serial_and_batch_bundle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| serial_and_batch_bundle | None | - | - |


##### get_columns(self, has_serial_no = None, has_batch_no = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| has_serial_no | None | None | - |
| has_batch_no | None | None | - |




## Functions

### execute(filters: dict | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | dict | None | None | - |

**Returns**: (none)



### check_has_serial_no_in_data(data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |

**Returns**: (none)


