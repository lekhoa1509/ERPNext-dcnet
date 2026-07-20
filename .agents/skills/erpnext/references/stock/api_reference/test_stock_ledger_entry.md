# API Reference: test_stock_ledger_entry.py

**Language**: Python

**Source**: `doctype/stock_ledger_entry/test_stock_ledger_entry.py`

---

## Classes

### TestStockLedgerEntry

**Inherits from**: IntegrationTestCase, StockTestMixin

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


##### test_item_cost_reposting(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_return_valuation_reposting(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_return_valuation_reposting(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reposting_of_sales_return_for_packed_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_back_dated_entry_not_allowed(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_batchwise_item_valuation_fifo(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_batchwise_item_valuation_moving_average(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_batchwise_item_valuation_stock_reco(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_batch_wise_valuation_across_warehouse(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_intermediate_average_batch_wise_valuation(self)

A batch has moving average up until posting time,
check if same is respected when backdated entry is inserted in middle

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_legacy_item_valuation_stock_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_fifo_dependent_consumption(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_fifo_multi_item_repack_consumption(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_negative_fifo_valuation(self)

When stock goes negative discard FIFO queue.
Only pervailing valuation rate should be used for making transactions in such cases.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_dependent_gl_entry_reposting(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tie_breaking(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_timestamp_clash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_previous_sle_with_clashed_timestamp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backdated_sle_with_same_timestamp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_transfer_invariants(self)

Extact stock value should be transferred.

**Decorators**: `@IntegrationTestCase.change_settings('System Settings', {'float_precision': 3, 'currency_precision': 2})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_negative_qty_with_precision(self)

Test if system precision is respected while validating negative qty.

**Decorators**: `@IntegrationTestCase.change_settings('System Settings', {'float_precision': 4})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_future_negative_qty_with_precision(self)

Ledger:
| Voucher | Qty         | Balance
-------------------
| Reco    | 559.8327| 559.8327
| SE      | -470.84     | [Backdated] (new bal: 88.9927)
| SE      | 11.007      | 570.8397 (new bal: 99.9997)
| DN      | -100        | 470.8397 (new bal: -0.0003)

Check if future negative qty is asserted as per precision 3.
-0.0003 should be considered as 0.000

**Decorators**: `@IntegrationTestCase.change_settings('System Settings', {'float_precision': 4})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestDeferredNaming

**Inherits from**: IntegrationTestCase

#### Methods

##### setUpClass(cls) → None

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |

**Returns**: `None`


##### setUp(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### tearDown(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### get_gle_sles(se)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| se | None | - | - |


##### test_deferred_naming(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_hash_naming(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_repack_entry()

**Returns**: (none)



### create_product_bundle_item(new_item_code, packed_items)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| new_item_code | None | - | - |
| packed_items | None | - | - |

**Returns**: (none)



### create_items(items = None, uoms = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| items | None | None | - |
| uoms | None | None | - |

**Returns**: (none)



### setup_item_valuation_test(valuation_method = 'FIFO', suffix = None, use_batchwise_valuation = 1, batches_list = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| valuation_method | None | 'FIFO' | - |
| suffix | None | None | - |
| use_batchwise_valuation | None | 1 | - |
| batches_list | None | None | - |

**Returns**: (none)



### create_purchase_receipt_entries_for_batchwise_item_valuation_test(pr_entry_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pr_entry_list | None | - | - |

**Returns**: (none)



### create_delivery_note_entries_for_batchwise_item_valuation_test(dn_entry_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dn_entry_list | None | - | - |

**Returns**: (none)



### fetch_sle_details_for_doc_list(doc_list, columns, as_dict = 1)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc_list | None | - | - |
| columns | None | - | - |
| as_dict | None | 1 | - |

**Returns**: (none)



### get_stock_value_from_q(q)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| q | None | - | - |

**Returns**: (none)



### create_stock_entry_entries_for_batchwise_item_valuation_test(se_entry_list, purpose)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| se_entry_list | None | - | - |
| purpose | None | - | - |

**Returns**: (none)



### get_unique_suffix()

**Returns**: (none)



### update_invariants(exp_sles)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| exp_sles | None | - | - |

**Returns**: (none)



### check_sle_details_against_expected(sle_details, expected_sle_details, detail, columns)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sle_details | None | - | - |
| expected_sle_details | None | - | - |
| detail | None | - | - |
| columns | None | - | - |

**Returns**: (none)



### _get_stock_credit(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### _day(days)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| days | None | - | - |

**Returns**: (none)



### ordered_qty_after_transaction()

**Returns**: (none)


