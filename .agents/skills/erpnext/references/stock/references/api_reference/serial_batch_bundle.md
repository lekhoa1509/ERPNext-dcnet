# API Reference: serial_batch_bundle.py

**Language**: Python

**Source**: `serial_batch_bundle.py`

---

## Classes

### SerialBatchBundle

**Inherits from**: (none)

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### process_serial_and_batch_bundle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_item_details(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### process_serial_no(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_material_transfer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_serial_batch_no_bundle_for_material_transfer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_serial_batch_no_bundle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_actual_qty(self, sn_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sn_doc | None | - | - |


##### validate_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_serial_and_batch_bundle(self, sn_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sn_doc | None | - | - |


##### child_doctype(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_rejected_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_packed_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### process_batch_no(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_item_and_warehouse(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delink_serial_and_batch_bundle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### post_process(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### cancel_serial_and_batch_bundle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_pos_or_asset_repair_transaction(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### submit_serial_and_batch_bundle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_warehouse_and_status_in_serial_nos(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_status_for_serial_nos(self, sle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |


##### update_serial_no_status_warehouse(self, sle, serial_nos)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |
| serial_nos | None | - | - |


##### update_serial_no_status_for_stock_reco(self, serial_nos)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| serial_nos | None | - | - |


##### set_batch_no_in_serial_nos(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### SerialNoValuation

**Inherits from**: DeprecatedSerialNoValuation

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate_stock_value_change(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_serial_no_wise_incoming_rate(self, serial_nos)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| serial_nos | None | - | - |


##### get_serial_nos(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate_valuation_rate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_rejected_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_incoming_rate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_incoming_rate_of_serial_no(self, serial_no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| serial_no | None | - | - |




### BatchNoValuation

**Inherits from**: DeprecatedBatchNoValuation

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate_avg_rate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_batch_stock_before_date(self) → list[dict]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `list[dict]`


##### prepare_batches(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_batch_nos(self) → list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `list`


##### set_stock_value_difference(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate_valuation_rate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_incoming_rate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_actual_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### SerialBatchCreation

**Inherits from**: (none)

#### Methods

##### __init__(self, args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| args | None | - | - |


##### set(self, args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| args | None | - | - |


##### get(self, key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |


##### set_item_details(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_other_details(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### duplicate_package(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### remove_returned_serial_nos(self, package)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| package | None | - | - |


##### make_serial_and_batch_bundle(self, serial_nos = None, batch_nos = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| serial_nos | None | None | - |
| batch_nos | None | None | - |


##### add_serial_nos_for_batch_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_serial_and_batch_entries(self, serial_nos = None, batch_nos = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| serial_nos | None | None | - |
| batch_nos | None | None | - |


##### validate_qty(self, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### set_auto_serial_batch_entries_for_outward(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_auto_serial_batch_entries_for_inward(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_serial_no_if_not_exists(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_serial_nos(self, serial_nos)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| serial_nos | None | - | - |


##### set_serial_batch_entries(self, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### create_batch(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_auto_created_serial_nos(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_serial_nos(serial_and_batch_bundle, serial_nos = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| serial_and_batch_bundle | None | - | - |
| serial_nos | None | None | - |

**Returns**: (none)



### get_batches_from_bundle(serial_and_batch_bundle, batches = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| serial_and_batch_bundle | None | - | - |
| batches | None | None | - |

**Returns**: (none)



### get_serial_nos_from_bundle(serial_and_batch_bundle, serial_nos = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| serial_and_batch_bundle | None | - | - |
| serial_nos | None | None | - |

**Returns**: (none)



### get_serial_or_batch_nos(bundle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bundle | None | - | - |

**Returns**: (none)



### is_rejected(voucher_type, voucher_detail_no, warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_type | None | - | - |
| voucher_detail_no | None | - | - |
| warehouse | None | - | - |

**Returns**: (none)



### get_batch_nos(serial_and_batch_bundle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| serial_and_batch_bundle | None | - | - |

**Returns**: (none)



### get_empty_batches_based_work_order(work_order, item_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| work_order | None | - | - |
| item_code | None | - | - |

**Returns**: (none)



### get_batches_from_work_order(work_order, item_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| work_order | None | - | - |
| item_code | None | - | - |

**Returns**: (none)



### get_batches_from_stock_entries(work_order, item_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| work_order | None | - | - |
| item_code | None | - | - |

**Returns**: (none)



### set_batch_details_from_package(ids, batches)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ids | None | - | - |
| batches | None | - | - |

**Returns**: (none)



### get_serial_or_batch_items(items)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| items | None | - | - |

**Returns**: (none)



### get_serial_nos_batch(serial_nos)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| serial_nos | None | - | - |

**Returns**: (none)



### update_batch_qty(voucher_type, voucher_no, docstatus, via_landed_cost_voucher = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_type | None | - | - |
| voucher_no | None | - | - |
| docstatus | None | - | - |
| via_landed_cost_voucher | None | False | - |

**Returns**: (none)



### get_batch_current_qty(batch)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| batch | None | - | - |

**Returns**: (none)



### throw_negative_batch_validation(batch_no, qty)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| batch_no | None | - | - |
| qty | None | - | - |

**Returns**: (none)



### get_batchwise_qty(voucher_type, voucher_no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_type | None | - | - |
| voucher_no | None | - | - |

**Returns**: (none)



### get_serial_batch_list_from_item(item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | None | - | - |

**Returns**: (none)



### get_latest_based_on_posting_datetime()

**Returns**: (none)



### get_latest_based_on_creation(latest_posting)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| latest_posting | None | - | - |

**Returns**: (none)



### get_series(partial_series, digits)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| partial_series | None | - | - |
| digits | None | - | - |

**Returns**: (none)


