# API Reference: test_stock_ageing.py

**Language**: Python

**Source**: `report/stock_ageing/test_stock_ageing.py`

---

## Classes

### TestStockAgeing

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### test_normal_inward_outward_queue(self)

Reference: Case 1 in stock_ageing_fifo_logic.md (same wh)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_insufficient_balance(self)

Reference: Case 3 in stock_ageing_fifo_logic.md (same wh)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_basic_stock_reconciliation(self)

Ledger (same wh): [+30, reco reset >> 50, -10]
Bal: 40

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sequential_stock_reco_same_warehouse(self)

Test back to back stock recos (same warehouse).
Ledger: [reco opening >> +1000, reco reset >> 400, -10]
Bal: 390

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sequential_stock_reco_different_warehouse(self)

Ledger:
WH      | Voucher | Qty
-------------------
WH1 | Reco        | 1000
WH2 | Reco        | 400
WH1 | SE          | -10

Bal: WH1 bal + WH2 bal = 990 + 400 = 1390

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_repack_entry_same_item_split_rows(self)

Split consumption rows and have single repacked item row (same warehouse).
Ledger:
Item    | Qty | Voucher
------------------------
Item 1  | 500 | 001
Item 1  | -50 | 002 (repack)
Item 1  | -50 | 002 (repack)
Item 1  | 100 | 002 (repack)

Case most likely for batch items. Test time bucket computation.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_repack_entry_same_item_overconsume(self)

Over consume item and have less repacked item qty (same warehouse).
Ledger:
Item    | Qty  | Voucher
------------------------
Item 1  | 500  | 001
Item 1  | -100 | 002 (repack)
Item 1  | 50   | 002 (repack)

Case most likely for batch items. Test time bucket computation.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_repack_entry_same_item_overconsume_with_split_rows(self)

Over consume item and have less repacked item qty (same warehouse).
Ledger:
Item    | Qty  | Voucher
------------------------
Item 1  | 20   | 001
Item 1  | -50  | 002 (repack)
Item 1  | -50  | 002 (repack)
Item 1  | 50   | 002 (repack)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_repack_entry_same_item_overproduce(self)

Under consume item and have more repacked item qty (same warehouse).
Ledger:
Item    | Qty  | Voucher
------------------------
Item 1  | 500  | 001
Item 1  | -50  | 002 (repack)
Item 1  | 100  | 002 (repack)

Case most likely for batch items. Test time bucket computation.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_repack_entry_same_item_overproduce_with_split_rows(self)

Over consume item and have less repacked item qty (same warehouse).
Ledger:
Item    | Qty  | Voucher
------------------------
Item 1  | 20   | 001
Item 1  | -50  | 002 (repack)
Item 1  | 50  | 002 (repack)
Item 1  | 50   | 002 (repack)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_negative_stock_same_voucher(self)

Test negative stock scenario in transfer bucket via repack entry (same wh).
Ledger:
Item    | Qty  | Voucher
------------------------
Item 1  | -50  | 001
Item 1  | -50  | 001
Item 1  | 30   | 001
Item 1  | 80   | 001

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_precision(self)

Test if final balance qty is rounded off correctly.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_ageing_stock_valuation(self)

Test stock valuation for each time bucket.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### generate_item_and_item_wh_wise_slots(filters, sle)

Return results with and without 'show_warehouse_wise_stock'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| sle | None | - | - |

**Returns**: (none)


