# API Reference: stock_ledger.py

**Language**: Python

**Source**: `stock_ledger.py`

---

## Classes

### NegativeStockError

**Inherits from**: frappe.ValidationError



### SerialNoExistsInFutureTransaction

**Inherits from**: frappe.ValidationError



### update_entries_after

update valution rate and qty after transaction
from the current time-bucket onwards

:param args: args as dict

        args = {
                "item_code": "ABC",
                "warehouse": "XYZ",
                "posting_date": "2012-12-12",
                "posting_time": "12:00"
        }

**Inherits from**: (none)

#### Methods

##### __init__(self, args, allow_zero_rate = False, allow_negative_stock = None, via_landed_cost_voucher = False, verbose = 1)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| args | None | - | - |
| allow_zero_rate | None | False | - |
| allow_negative_stock | None | None | - |
| via_landed_cost_voucher | None | False | - |
| verbose | None | 1 | - |


##### get_reserved_stock(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_precision(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### initialize_previous_data(self, args)

Get previous sl entries for current item for each related warehouse
and assigns into self.data dict

:Data Structure:

self.data = {
        warehouse1: {
                'previus_sle': {},
                'qty_after_transaction': 10,
                'valuation_rate': 100,
                'stock_value': 1000,
                'prev_stock_value': 1000,
                'stock_queue': '[[10, 100]]',
                'stock_value_difference': 1000
        }
}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| args | None | - | - |


##### build(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_distinct_item_warehouses_for_repack(self, sle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |


##### has_stock_reco_with_serial_batch(self, sle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |


##### process_sle_against_current_timestamp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_sle_against_current_voucher(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_future_entries_to_fix(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_dependent_entries_to_fix(self, entries_to_fix, sle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| entries_to_fix | None | - | - |
| sle | None | - | - |


##### update_distinct_item_warehouses(self, dependant_sle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| dependant_sle | None | - | - |


##### is_dependent_voucher_reposted(self, dependant_sle) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| dependant_sle | None | - | - |

**Returns**: `bool`


##### get_dependent_voucher_detail_nos(self, key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |


##### validate_previous_sle_qty(self, sle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |


##### process_sle(self, sle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |


##### get_serialized_values(self, sle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |


##### reset_actual_qty_for_stock_reco(self, sle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |


##### update_serial_no_status(self, sle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |


##### calculate_valuation_for_serial_batch_bundle(self, sle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |


##### update_serial_batch_no_valuation(self, sle, doc, prev_sle = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |
| doc | None | - | - |
| prev_sle | None | None | - |


##### get_outgoing_rate_for_batched_item(self, sle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |


##### validate_negative_stock(self, sle)

validate negative stock for entries current datetime onwards
will not consider cancelled entries

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |


##### get_dynamic_incoming_outgoing_rate(self, sle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |


##### has_landed_cost_based_on_pi(self, sle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |


##### get_incoming_outgoing_rate_from_transaction(self, sle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |


##### update_outgoing_rate_on_transaction(self, sle)

Update outgoing rate in Stock Entry, Delivery Note, Sales Invoice and Sales Return
In case of Stock Entry, also calculate FG Item rate and total incoming/outgoing amount

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |


##### update_rate_on_stock_entry(self, sle, outgoing_rate)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |
| outgoing_rate | None | - | - |


##### is_manufacture_entry_with_sabb(self, sle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |


##### recalculate_amounts_in_stock_entry(self, voucher_no, voucher_detail_no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| voucher_no | None | - | - |
| voucher_detail_no | None | - | - |


##### update_rate_on_delivery_and_sales_return(self, sle, outgoing_rate)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |
| outgoing_rate | None | - | - |


##### update_rate_on_purchase_receipt(self, sle, outgoing_rate)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |
| outgoing_rate | None | - | - |


##### update_rate_on_subcontracting_receipt(self, sle, outgoing_rate)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |
| outgoing_rate | None | - | - |


##### update_rate_on_stock_reconciliation(self, sle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |


##### get_incoming_value_for_serial_nos(self, sle, serial_nos)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |
| serial_nos | None | - | - |


##### get_moving_average_values(self, sle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |


##### update_queue_values(self, sle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |


##### is_return_purchase_entry(self, sle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |


##### update_batched_values(self, sle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |


##### check_if_allow_zero_valuation_rate(self, voucher_type, voucher_detail_no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| voucher_type | None | - | - |
| voucher_detail_no | None | - | - |


##### get_fallback_rate(self, sle) → float

When exact incoming rate isn't available use any of other "average" rates as fallback.
This should only get used for negative stock.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |

**Returns**: `float`


##### get_sle_before_datetime(self, args)

get previous stock ledger entry before current time-bucket

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| args | None | - | - |


##### get_sle_after_datetime(self, args)

get Stock Ledger Entries after a particular datetime, for reposting

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| args | None | - | - |


##### raise_exceptions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_bin_data(self, sle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |


##### update_bin(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### make_sl_entries(sl_entries, allow_negative_stock = False, via_landed_cost_voucher = False)

Create SL entries from SL entry dicts

args:
        - allow_negative_stock: disable negative stock valiations if true
        - via_landed_cost_voucher: landed cost voucher cancels and reposts
        entries of purchase document. This flag is used to identify if
        cancellation and repost is happening via landed cost voucher, in
        such cases certain validations need to be ignored (like negative
                        stock)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sl_entries | None | - | - |
| allow_negative_stock | None | False | - |
| via_landed_cost_voucher | None | False | - |

**Returns**: (none)



### repost_current_voucher(args, allow_negative_stock = False, via_landed_cost_voucher = False, cancelled = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |
| allow_negative_stock | None | False | - |
| via_landed_cost_voucher | None | False | - |
| cancelled | None | False | - |

**Returns**: (none)



### get_args_for_future_sle(row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| row | None | - | - |

**Returns**: (none)



### validate_serial_no(sle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sle | None | - | - |

**Returns**: (none)



### validate_cancellation(kargs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kargs | None | - | - |

**Returns**: (none)



### set_as_cancel(voucher_type, voucher_no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_type | None | - | - |
| voucher_no | None | - | - |

**Returns**: (none)



### make_entry(args, allow_negative_stock = False, via_landed_cost_voucher = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |
| allow_negative_stock | None | False | - |
| via_landed_cost_voucher | None | False | - |

**Returns**: (none)



### repost_future_sle(args = None, voucher_type = None, voucher_no = None, allow_negative_stock = None, via_landed_cost_voucher = False, doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | None | - |
| voucher_type | None | None | - |
| voucher_no | None | None | - |
| allow_negative_stock | None | None | - |
| via_landed_cost_voucher | None | False | - |
| doc | None | None | - |

**Returns**: (none)



### get_reposting_data(file_path) → dict

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| file_path | None | - | - |

**Returns**: `dict`



### validate_item_warehouse(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### update_args_in_repost_item_valuation(doc, index, args, distinct_item_warehouses, affected_transactions)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| index | None | - | - |
| args | None | - | - |
| distinct_item_warehouses | None | - | - |
| affected_transactions | None | - | - |

**Returns**: (none)



### get_reposting_file_name(dt, dn)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |
| dn | None | - | - |

**Returns**: (none)



### create_json_gz_file(data, doc, file_name = None) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| doc | None | - | - |
| file_name | None | None | - |

**Returns**: `str`



### create_file(doc, compressed_content)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| compressed_content | None | - | - |

**Returns**: (none)



### get_items_to_be_repost(voucher_type = None, voucher_no = None, doc = None, reposting_data = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_type | None | None | - |
| voucher_no | None | None | - |
| doc | None | None | - |
| reposting_data | None | None | - |

**Returns**: (none)



### get_distinct_item_warehouse(args = None, doc = None, reposting_data = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | None | - |
| doc | None | None | - |
| reposting_data | None | None | - |

**Returns**: (none)



### parse_distinct_items_and_warehouses(distinct_items_and_warehouses)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| distinct_items_and_warehouses | None | - | - |

**Returns**: (none)



### get_affected_transactions(doc, reposting_data = None) → set[tuple[str, str]]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| reposting_data | None | None | - |

**Returns**: `set[tuple[str, str]]`



### get_current_index(doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | None | - |

**Returns**: (none)



### get_previous_sle_of_current_voucher(args, operator = '<', exclude_current_voucher = False)

get stock ledger entries filtered by specific posting datetime conditions

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |
| operator | None | '<' | - |
| exclude_current_voucher | None | False | - |

**Returns**: (none)



### get_previous_sle(args, for_update = False, extra_cond = None)

get the last sle on or before the current time-bucket,
to get actual qty before transaction, this function
is called from various transaction like stock entry, reco etc

args = {
        "item_code": "ABC",
        "warehouse": "XYZ",
        "posting_date": "2012-12-12",
        "posting_time": "12:00",
        "sle": "name of reference Stock Ledger Entry"
}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |
| for_update | None | False | - |
| extra_cond | None | None | - |

**Returns**: (none)



### get_stock_ledger_entries(previous_sle, operator = None, order = 'desc', limit = None, for_update = False, debug = False, check_serial_no = True, extra_cond = None)

get stock ledger entries filtered by specific posting datetime conditions

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| previous_sle | None | - | - |
| operator | None | None | - |
| order | None | 'desc' | - |
| limit | None | None | - |
| for_update | None | False | - |
| debug | None | False | - |
| check_serial_no | None | True | - |
| extra_cond | None | None | - |

**Returns**: (none)



### get_sle_by_voucher_detail_no(voucher_detail_no, excluded_sle = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_detail_no | None | - | - |
| excluded_sle | None | None | - |

**Returns**: (none)



### get_valuation_rate(item_code, warehouse, voucher_type, voucher_no, allow_zero_rate = False, currency = None, company = None, raise_error_if_no_rate = True, batch_no = None, serial_and_batch_bundle = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |
| voucher_type | None | - | - |
| voucher_no | None | - | - |
| allow_zero_rate | None | False | - |
| currency | None | None | - |
| company | None | None | - |
| raise_error_if_no_rate | None | True | - |
| batch_no | None | None | - |
| serial_and_batch_bundle | None | None | - |

**Returns**: (none)



### update_qty_in_future_sle(args, allow_negative_stock = False)

Recalculate Qty after Transaction in future SLEs based on current SLE.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |
| allow_negative_stock | None | False | - |

**Returns**: (none)



### get_stock_reco_qty_shift(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### get_next_stock_reco(kwargs)

Returns next nearest stock reconciliaton's details.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kwargs | None | - | - |

**Returns**: (none)



### get_datetime_limit_condition(detail)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| detail | None | - | - |

**Returns**: (none)



### validate_negative_qty_in_future_sle(args, allow_negative_stock = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |
| allow_negative_stock | None | False | - |

**Returns**: (none)



### is_negative_with_precision(neg_sle, is_batch = False)

Returns whether system precision rounded qty is insufficient.
E.g: -0.0003 in precision 3 (0.000) is sufficient for the user.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| neg_sle | None | - | - |
| is_batch | None | False | - |

**Returns**: (none)



### get_future_sle_with_negative_qty(sle_args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sle_args | None | - | - |

**Returns**: (none)



### get_future_sle_with_negative_batch_qty(sle_args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sle_args | None | - | - |

**Returns**: (none)



### validate_reserved_stock(kwargs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kwargs | None | - | - |

**Returns**: (none)



### validate_reserved_serial_nos(item_code, warehouse, serial_nos)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |
| serial_nos | None | - | - |

**Returns**: (none)



### validate_reserved_batch_nos(item_code, warehouse, batch_nos)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |
| batch_nos | None | - | - |

**Returns**: (none)



### is_negative_stock_allowed() → bool

**Returns**: `bool`



### get_incoming_rate_for_inter_company_transfer(sle) → float

For inter company transfer, incoming rate is the average of the outgoing rate

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sle | None | - | - |

**Returns**: `float`



### is_internal_transfer(sle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sle | None | - | - |

**Returns**: (none)



### get_stock_value_difference(item_code, warehouse, posting_date, posting_time, voucher_no = None, voucher_detail_no = None, creation = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |
| posting_date | None | - | - |
| posting_time | None | - | - |
| voucher_no | None | None | - |
| voucher_detail_no | None | None | - |
| creation | None | None | - |

**Returns**: (none)



### is_transfer_stock_entry(voucher_no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_no | None | - | - |

**Returns**: (none)



### get_serial_from_sabb(serial_and_batch_bundle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| serial_and_batch_bundle | None | - | - |

**Returns**: (none)



### get_incoming_rate_for_serial_and_batch(item_code, row, sn_obj, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| row | None | - | - |
| sn_obj | None | - | - |
| company | None | - | - |

**Returns**: (none)



### is_repack_entry(stock_entry_id)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| stock_entry_id | None | - | - |

**Returns**: (none)



### rate_generator() → float

**Returns**: `float`


