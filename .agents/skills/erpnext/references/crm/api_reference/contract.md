# API Reference: contract.py

**Language**: Python

**Source**: `doctype/contract/contract.py`

---

## Classes

### Contract

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_missing_values(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_discard(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_update_after_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_dates(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_contract_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_fulfilment_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_fulfilment_progress(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_status(start_date, end_date)

Get a Contract's status based on the start, current and end dates

Args:
        start_date (str): The start date of the contract
        end_date (str): The end date of the contract

Returns:
        str: 'Active' if within range, otherwise 'Inactive'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| start_date | None | - | - |
| end_date | None | - | - |

**Returns**: (none)



### update_status_for_contracts()

Run the daily hook to update the statuses for all signed
and submitted Contracts

**Returns**: (none)


