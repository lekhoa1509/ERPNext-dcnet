# API Reference: test_stock_reconciliation.py

**Language**: Python

**Source**: `doctype/stock_reconciliation/test_stock_reconciliation.py`

---

## Classes

### TestStockReconciliation

**Inherits from**: IntegrationTestCase, StockTestMixin

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reco_for_fifo(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reco_for_moving_average(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _test_reco_sle_gle(self, valuation_method)

**Decorators**: `@IntegrationTestCase.change_settings('Stock Settings', {'allow_negative_stock': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| valuation_method | None | - | - |


##### test_get_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_stock_reco_for_serialized_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_stock_reco_for_batch_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_stock_reco_for_serial_and_batch_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_stock_reco_for_serial_and_batch_item_with_future_dependent_entry(self)

Behaviour: 1) Create Stock Reconciliation, which will be the origin document
of a new batch having a serial no
2) Create a Stock Entry that adds a serial no to the same batch following this
Stock Reconciliation
3) Cancel Stock Entry
Expected Result: 3) Serial No only in the Stock Entry is Inactive and Batch qty decreases

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_customer_provided_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backdated_stock_reco_qty_reposting(self)

Test if a backdated stock reco recalculates future qty until next reco.
-------------------------------------------
Var             | Doc   |       Qty     | Balance
-------------------------------------------
PR5     | PR    |   10  |  10   (posting date: today-4) [backdated]
SR5             | Reco  |       0       |       8       (posting date: today-4) [backdated]
PR1             | PR    |       10      |       18      (posting date: today-3)
PR2             | PR    |       1       |       19      (posting date: today-2)
SR4             | Reco  |       0       |       6       (posting date: today-1) [backdated]
PR3             | PR    |       1       |       7       (posting date: today) # can't post future PR

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backdated_stock_reco_future_negative_stock(self)

Test if a backdated stock reco causes future negative stock and is blocked.
-------------------------------------------
Var             | Doc   |       Qty     | Balance
-------------------------------------------
PR1             | PR    |       10      |       10              (posting date: today-2)
SR3             | Reco  |       0       |       1               (posting date: today-1) [backdated & blocked]
DN2             | DN    |       -2      |       8(-1)   (posting date: today)

**Decorators**: `@IntegrationTestCase.change_settings('Stock Settings', {'allow_negative_stock': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backdated_stock_reco_cancellation_future_negative_stock(self)

Test if a backdated stock reco cancellation that causes future negative stock is blocked.
-------------------------------------------
Var | Doc  | Qty | Balance
-------------------------------------------
SR  | Reco | 100 | 100     (posting date: today-1) (shouldn't be cancelled after DN)
DN  | DN   | 100 |   0     (posting date: today)

**Decorators**: `@IntegrationTestCase.change_settings('Stock Settings', {'allow_negative_stock': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_intermediate_sr_bin_update(self)

Bin should show correct qty even for backdated entries.

-------------------------------------------
| creation | Var | Doc  | Qty | balance qty
-------------------------------------------
|  1       | SR  | Reco | 10  | 10     (posting date: today+10)
|  3       | SR2 | Reco | 11  | 11     (posting date: today+11)
|  2       | DN  | DN   | 5   | 6 <-- assert in BIN  (posting date: today+12)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_valid_batch(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_serial_no_cancellation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_serial_no_creation_and_inactivation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_serial_no_batch_no_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backdated_stock_reco_entry(self)

**Decorators**: `@IntegrationTestCase.change_settings('Stock Reposting Settings', {'item_based_reposting': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_stock_reconciliation_while_reposting(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_stock_zero_for_serial_batch_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backdated_purchase_receipt_with_stock_reco(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_balance_qty_for_batch_with_backdated_stock_reco_and_future_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_stock_reco_and_backdated_purchase_receipt(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_not_reconcile_all_batch(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_not_reconcile_all_serial_nos(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_stock_reco_with_legacy_batch(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_skip_reposting_for_entries_after_stock_reco(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_stock_reco_for_negative_batch(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_stock_reco_batch_item_current_valuation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_stock_reco_recalculate_qty_for_backdated_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_serial_no_backdated_stock_reco(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_change_valuation_of_batch_using_backdated_stock_reco(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sabb_cancel_on_stock_reco_cancellation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_batch_item_with_batch(item_name, batch_id)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_name | None | - | - |
| batch_id | None | - | - |

**Returns**: (none)



### insert_existing_sle(warehouse, item_code = '_Test Item')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| warehouse | None | - | - |
| item_code | None | '_Test Item' | - |

**Returns**: (none)



### create_batch_or_serial_no_items()

**Returns**: (none)



### create_stock_reconciliation()

**Returns**: (none)



### set_valuation_method(item_code, valuation_method)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| valuation_method | None | - | - |

**Returns**: (none)



### assertBalance(doc, qty_after_transaction)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| qty_after_transaction | None | - | - |

**Returns**: (none)


