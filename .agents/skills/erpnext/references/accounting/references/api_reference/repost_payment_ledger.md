# API Reference: repost_payment_ledger.py

**Language**: Python

**Source**: `doctype/repost_payment_ledger/repost_payment_ledger.py`

---

## Classes

### RepostPaymentLedger

**Inherits from**: Document

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### load_vouchers_based_on_filters(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_vouchers(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### repost_ple_for_voucher(voucher_type, voucher_no, gle_map = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_type | None | - | - |
| voucher_no | None | - | - |
| gle_map | None | None | - |

**Returns**: (none)



### start_payment_ledger_repost(docname = None)

Repost Payment Ledger Entries for Vouchers through Background Job

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docname | None | None | - |

**Returns**: (none)



### execute_repost_payment_ledger(docname)

Repost Payment Ledger Entries by background job.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docname | None | - | - |

**Returns**: (none)


