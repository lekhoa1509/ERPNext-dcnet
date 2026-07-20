# API Reference: stock_entry_utils.py

**Language**: Python

**Source**: `doctype/stock_entry/stock_entry_utils.py`

---

## Functions

### make_stock_entry() → 'StockEntry'

**Returns**: `'StockEntry'`



### make_stock_entry()

Helper function to make a Stock Entry

:item_code: Item to be moved
:qty: Qty to be moved
:company: Company Name (optional)
:from_warehouse: Optional
:to_warehouse: Optional
:rate: Optional
:serial_no: Optional
:batch_no: Optional
:posting_date: Optional
:posting_time: Optional
:purpose: Optional
:do_not_save: Optional flag
:do_not_submit: Optional flag

**Returns**: (none)



### process_serial_numbers(serial_nos_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| serial_nos_list | None | - | - |

**Returns**: (none)


