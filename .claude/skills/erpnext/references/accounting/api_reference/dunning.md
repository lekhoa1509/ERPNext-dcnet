# API Reference: dunning.py

**Language**: Python

**Source**: `doctype/dunning/dunning.py`

---

## Classes

### Dunning

**Inherits from**: AccountsController

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_same_currency(self)

Throw an error if invoice currency differs from dunning currency.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_overdue_payments(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_totals(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_party_details(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_dunning_level(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### update_linked_dunnings(doc, previous_outstanding_amount)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| previous_outstanding_amount | None | - | - |

**Returns**: (none)



### get_linked_dunnings_as_per_state(sales_invoice, state)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sales_invoice | None | - | - |
| state | None | - | - |

**Returns**: (none)



### get_dunning_letter_text(dunning_type: str, doc: str | dict, language: str | None = None) → dict

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dunning_type | str | - | - |
| doc | str | dict | - | - |
| language | str | None | None | - |

**Returns**: `dict`


