# API Reference: test_serial_no.py

**Language**: Python

**Source**: `doctype/serial_no/test_serial_no.py`

---

## Classes

### TestSerialNo

**Inherits from**: IntegrationTestCase

#### Methods

##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cannot_create_direct(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_inter_company_transfer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_inter_company_transfer_intermediate_cancellation(self)

Receive into and Deliver Serial No from one company.
Then Receive into and Deliver from second company.
Try to cancel intermediate receipts/deliveries to test if it is blocked.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_inter_company_transfer_fallback_on_cancel(self)

Test Serial No state changes on cancellation.
If Delivery cancelled, it should fall back on last Receipt in the same company.
If Receipt is cancelled, it should be Inactive in the same company.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_correct_serial_no_incoming_rate(self)

Check correct consumption rate based on serial no record.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auto_fetch(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_auto_serial_nos(kwargs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kwargs | None | - | - |

**Returns**: (none)


