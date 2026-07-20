# API Reference: serial_and_batch_bundle.py

**Language**: Python

**Source**: `doctype/serial_and_batch_bundle/serial_and_batch_bundle.py`

---

## Classes

### SerialNoExistsInFutureTransactionError

**Inherits from**: frappe.ValidationError



### BatchNegativeStockError

**Inherits from**: frappe.ValidationError



### SerialNoDuplicateError

**Inherits from**: frappe.ValidationError



### SerialNoWarehouseError

**Inherits from**: frappe.ValidationError



### SerialandBatchBundle

**Inherits from**: Document

#### Methods

##### autoname(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_serial_no_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_voucher_detail_no(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### allow_existing_serial_nos(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### reset_serial_batch_bundle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_batch_no(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_serial_nos_inventory(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_serial_nos_duplicate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### throw_error_message(self, message, exception = frappe.ValidationError)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| message | None | - | - |
| exception | None | frappe.ValidationError | - |


##### set_incoming_rate(self, parent = None, row = None, save = False, allow_negative_stock = False, prev_sle = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| parent | None | None | - |
| row | None | None | - |
| save | None | False | - |
| allow_negative_stock | None | False | - |
| prev_sle | None | None | - |


##### set_valuation_rate_for_return_entry(self, return_against, row, save = False, prev_sle = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| return_against | None | - | - |
| row | None | - | - |
| save | None | False | - |
| prev_sle | None | None | - |


##### validate_returned_serial_batch_no(self, return_against, row, original_inv_details)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| return_against | None | - | - |
| row | None | - | - |
| original_inv_details | None | - | - |


##### get_valuation_rate_for_return_entry(self, return_against)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| return_against | None | - | - |


##### calculate_total_qty(self, save = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| save | None | True | - |


##### get_serial_nos(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_valuation_rate(self, valuation_rate = None, save = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| valuation_rate | None | None | - |
| save | None | False | - |


##### set_incoming_rate_for_outward_transaction(self, row = None, save = False, allow_negative_stock = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | None | - |
| save | None | False | - |
| allow_negative_stock | None | False | - |


##### validate_negative_batch(self, batch_no, available_qty)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| batch_no | None | - | - |
| available_qty | None | - | - |


##### is_stock_reco_for_valuation_adjustment(self, available_qty)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| available_qty | None | - | - |


##### get_sle_for_outward_transaction(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_return_against(self, parent = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| parent | None | None | - |


##### set_incoming_rate_for_inward_transaction(self, row = None, save = False, prev_sle = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | None | - |
| save | None | False | - |
| prev_sle | None | None | - |


##### set_serial_and_batch_values(self, parent, row, qty_field = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| parent | None | - | - |
| row | None | - | - |
| qty_field | None | None | - |


##### validate_voucher_no(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_future_entries_exists(self, is_cancelled = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| is_cancelled | None | False | - |


##### get_serial_nos_for_validate(self, is_cancelled = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| is_cancelled | None | False | - |


##### get_skip_serial_nos_for_stock_reconciliation(self, is_cancelled = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| is_cancelled | None | False | - |


##### reset_qty(self, row, qty_field = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| qty_field | None | None | - |


##### validate_quantity(self, row, qty_field = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| qty_field | None | None | - |


##### get_qty_field(self, row, qty_field = None) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| qty_field | None | None | - |

**Returns**: `str`


##### set_is_outward(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_warehouse(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate_qty_and_amount(self, save = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| save | None | False | - |


##### calculate_outgoing_rate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_serial_and_batch_no(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_serial_batch_no(self, serial_batches)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| serial_batches | None | - | - |


##### validate_incorrect_serial_nos(self, serial_nos)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| serial_nos | None | - | - |


##### validate_incorrect_batch_nos(self, batch_nos)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| batch_nos | None | - | - |


##### validate_serial_and_batch_no_for_returned(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_orignal_document_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_duplicate_serial_and_batch_no(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delink_serial_and_batch_bundle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### child_table(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delink_refernce_from_voucher(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delink_reference_from_batch(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_serial_and_batch_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_docstatus(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_child_details(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_source_document_no(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_serial_and_batch_inventory(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_batch_inventory(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_batch_quantity(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### throw_negative_batch(self, batch_no, available_qty, precision)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| batch_no | None | - | - |
| available_qty | None | - | - |
| precision | None | - | - |


##### get_batchwise_available_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_available_qty_from_stock_ledger(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_available_qty_from_sabb(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_voucher_no_docstatus(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_serial_batch(self, data)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| data | None | - | - |


##### delete_serial_batch_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### download_blank_csv_template(content)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| content | None | - | - |

**Returns**: (none)



### upload_csv_file(item_code, file_path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| file_path | None | - | - |

**Returns**: (none)



### get_serial_batch_from_csv(item_code, file_path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| file_path | None | - | - |

**Returns**: (none)



### parse_csv_file_to_get_serial_batch(reader)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| reader | None | - | - |

**Returns**: (none)



### get_serial_batch_from_data(item_code, kwargs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| kwargs | None | - | - |

**Returns**: (none)



### create_serial_nos(item_code, serial_nos)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| serial_nos | None | - | - |

**Returns**: (none)



### make_serial_nos(item_code, serial_nos)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| serial_nos | None | - | - |

**Returns**: (none)



### make_batch_nos(item_code, batch_nos)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| batch_nos | None | - | - |

**Returns**: (none)



### item_query(doctype, txt, searchfield, start, page_len, filters, as_dict = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| txt | None | - | - |
| searchfield | None | - | - |
| start | None | - | - |
| page_len | None | - | - |
| filters | None | - | - |
| as_dict | None | False | - |

**Returns**: (none)



### get_serial_batch_ledgers(item_code = None, docstatus = None, voucher_no = None, name = None, child_row = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | None | - |
| docstatus | None | None | - |
| voucher_no | None | None | - |
| name | None | None | - |
| child_row | None | None | - |

**Returns**: (none)



### get_filters_for_bundle(item_code = None, docstatus = None, voucher_no = None, name = None, child_row = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | None | - |
| docstatus | None | None | - |
| voucher_no | None | None | - |
| name | None | None | - |
| child_row | None | None | - |

**Returns**: (none)



### get_reference_serial_and_batch_bundle(child_row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| child_row | None | - | - |

**Returns**: (none)



### add_serial_batch_ledgers(entries, child_row, doc, warehouse, do_not_save = False) → object

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| entries | None | - | - |
| child_row | None | - | - |
| doc | None | - | - |
| warehouse | None | - | - |
| do_not_save | None | False | - |

**Returns**: `object`



### create_serial_batch_no_ledgers(entries, child_row, parent_doc, warehouse = None, do_not_save = False) → object

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| entries | None | - | - |
| child_row | None | - | - |
| parent_doc | None | - | - |
| warehouse | None | None | - |
| do_not_save | None | False | - |

**Returns**: `object`



### combine_datetime(date, time = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | None | - | - |
| time | None | None | - |

**Returns**: (none)



### get_batch(item_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |

**Returns**: (none)



### get_type_of_transaction(parent_doc, child_row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| parent_doc | None | - | - |
| child_row | None | - | - |

**Returns**: (none)



### update_serial_batch_no_ledgers(bundle, entries, child_row, parent_doc, warehouse = None) → object

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bundle | None | - | - |
| entries | None | - | - |
| child_row | None | - | - |
| parent_doc | None | - | - |
| warehouse | None | None | - |

**Returns**: `object`



### update_serial_or_batch(bundle_id, serial_no = None, batch_no = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bundle_id | None | - | - |
| serial_no | None | None | - |
| batch_no | None | None | - |

**Returns**: (none)



### get_serial_and_batch_ledger()

**Returns**: (none)



### get_auto_data()

**Returns**: (none)



### get_available_batches_qty(available_batches)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| available_batches | None | - | - |

**Returns**: (none)



### get_available_serial_nos(kwargs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kwargs | None | - | - |

**Returns**: (none)



### get_serial_nos_based_on_filters(filters, fields, order_by, kwargs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| fields | None | - | - |
| order_by | None | - | - |
| kwargs | None | - | - |

**Returns**: (none)



### get_serial_nos_from_sre(kwargs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kwargs | None | - | - |

**Returns**: (none)



### get_non_expired_batches(batches)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| batches | None | - | - |

**Returns**: (none)



### get_serial_nos_based_on_posting_date(kwargs, ignore_serial_nos)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kwargs | None | - | - |
| ignore_serial_nos | None | - | - |

**Returns**: (none)



### get_bundle_wise_serial_nos(data, kwargs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| kwargs | None | - | - |

**Returns**: (none)



### get_reserved_voucher_details(kwargs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kwargs | None | - | - |

**Returns**: (none)



### get_reserved_serial_nos_for_pos(kwargs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kwargs | None | - | - |

**Returns**: (none)



### get_reserved_serial_nos_for_voucher(kwargs, reserved_entries, reserved_voucher_details)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kwargs | None | - | - |
| reserved_entries | None | - | - |
| reserved_voucher_details | None | - | - |

**Returns**: (none)



### get_other_doc_reserved_serials(kwargs, reserved_entries, reserved_voucher_details)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kwargs | None | - | - |
| reserved_entries | None | - | - |
| reserved_voucher_details | None | - | - |

**Returns**: (none)



### get_reserved_serial_nos_for_sre(kwargs) → list

Returns a list of `Serial No` reserved in Stock Reservation Entry.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kwargs | None | - | - |

**Returns**: `list`



### get_reserved_batches_for_pos(kwargs) → dict

Returns a dict of `Batch No` followed by the `Qty` reserved in POS Invoices.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kwargs | None | - | - |

**Returns**: `dict`



### get_reserved_batches_for_sre(kwargs) → dict

Returns a dict of `Batch No` followed by the `Qty` reserved in Stock Reservation Entry.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kwargs | None | - | - |

**Returns**: `dict`



### get_auto_batch_nos(kwargs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kwargs | None | - | - |

**Returns**: (none)



### get_batch_nos_from_sre(kwargs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kwargs | None | - | - |

**Returns**: (none)



### get_batches_to_be_considered(sales_order_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sales_order_name | None | - | - |

**Returns**: (none)



### filter_zero_near_batches(available_batches, kwargs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| available_batches | None | - | - |
| kwargs | None | - | - |

**Returns**: (none)



### get_qty_based_available_batches(available_batches, qty)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| available_batches | None | - | - |
| qty | None | - | - |

**Returns**: (none)



### update_available_batches(available_batches) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| available_batches | None | - | - |

**Returns**: `None`



### get_available_batches(kwargs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kwargs | None | - | - |

**Returns**: (none)



### get_voucher_wise_serial_batch_from_bundle() → dict[str, dict]

**Returns**: `dict[str, dict]`



### get_picked_batches(kwargs) → dict[str, dict]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kwargs | None | - | - |

**Returns**: `dict[str, dict]`



### get_picked_serial_nos(item_code, warehouse = None) → list[str]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | None | - |

**Returns**: `list[str]`



### get_ledgers_from_serial_batch_bundle() → list[frappe._dict]

**Returns**: `list[frappe._dict]`



### get_stock_ledgers_for_serial_nos(kwargs)

Fetch stock ledger entries based on various filters.
:param kwargs: Filters including posting_datetime, creation, warehouse, item_code, serial_nos, ignore_voucher_detail_no, voucher_no. Joins with Serial and Batch Entry table to filter based on serial numbers.
:return: List of stock ledger entries as dictionaries.
:rtype: list[dict]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kwargs | None | - | - |

**Returns**: (none)



### get_stock_ledgers_batches(kwargs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kwargs | None | - | - |

**Returns**: (none)



### get_batch_no_from_serial_no(serial_no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| serial_no | None | - | - |

**Returns**: (none)



### is_serial_batch_no_exists(item_code, type_of_transaction, serial_no = None, batch_no = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| type_of_transaction | None | - | - |
| serial_no | None | None | - |
| batch_no | None | None | - |

**Returns**: (none)



### make_serial_no(serial_no, item_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| serial_no | None | - | - |
| item_code | None | - | - |

**Returns**: (none)



### make_batch_no(batch_no, item_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| batch_no | None | - | - |
| item_code | None | - | - |

**Returns**: (none)



### is_duplicate_serial_no(bundle_id, serial_no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bundle_id | None | - | - |
| serial_no | None | - | - |

**Returns**: (none)



### parse_serial_nos(serial_no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| serial_no | None | - | - |

**Returns**: (none)



### get_stock_reco_details(voucher_detail_no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_detail_no | None | - | - |

**Returns**: (none)


