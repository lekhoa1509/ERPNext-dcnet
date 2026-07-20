# API Reference: test_landed_cost_voucher.py

**Language**: Python

**Source**: `doctype/landed_cost_voucher/test_landed_cost_voucher.py`

---

## Classes

### TestLandedCostVoucher

**Inherits from**: IntegrationTestCase

#### Methods

##### test_landed_cost_voucher(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### assertPurchaseReceiptLCVGLEntries(self, pr)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| pr | None | - | - |


##### test_landed_cost_voucher_stock_impact(self)

Test impact of LCV on future stock balances.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_landed_cost_voucher_for_zero_purchase_rate(self)

Test impact of LCV on future stock balances.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_landed_cost_voucher_against_purchase_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_landed_cost_voucher_for_serialized_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_serialized_lcv_delivered(self)

In some cases you'd want to deliver before you can know all the
landed costs, this should be allowed for serial nos too.

Case:
                - receipt a serial no @ X rate
                - delivery the serial no @ X rate
                - add LCV to receipt X + Y
                - LCV should be successful
                - delivery should reflect X+Y valuation.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_landed_cost_voucher_for_odd_numbers(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_multiple_landed_cost_voucher_against_pr(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_multi_currency_lcv(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_asset_lcv(self)

Check if LCV for an Asset updates the Assets Net Purchase Amount correctly.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_landed_cost_voucher_with_serial_batch_for_legacy_pr(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_do_not_validate_landed_cost_voucher_with_serial_batch_for_legacy_pr(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_do_not_validate_against_landed_cost_voucher_for_serial_for_legacy_pr(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_lcv_for_work_order_scr(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### make_landed_cost_voucher()

**Returns**: (none)



### create_landed_cost_voucher(receipt_document_type, receipt_document, company, charges = 50)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| receipt_document_type | None | - | - |
| receipt_document | None | - | - |
| company | None | - | - |
| charges | None | 50 | - |

**Returns**: (none)



### distribute_landed_cost_on_items(lcv)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| lcv | None | - | - |

**Returns**: (none)


