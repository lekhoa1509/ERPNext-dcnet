# API Reference: general_ledger.py

**Language**: Python

**Source**: `report/general_ledger/general_ledger.py`

---

## Functions

### execute(filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |

**Returns**: (none)



### validate_filters(filters, account_details)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| account_details | None | - | - |

**Returns**: (none)



### validate_party(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### set_account_currency(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### get_result(filters, account_details)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| account_details | None | - | - |

**Returns**: (none)



### get_gl_entries(filters, accounting_dimensions)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| accounting_dimensions | None | - | - |

**Returns**: (none)



### get_conditions(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### get_party_name_map()

**Returns**: (none)



### get_accounts_with_children(accounts)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| accounts | None | - | - |

**Returns**: (none)



### set_bill_no(gl_entries)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| gl_entries | None | - | - |

**Returns**: (none)



### get_translated_labels_for_totals()

**Returns**: (none)



### get_data_with_opening_closing(filters, account_details, accounting_dimensions, gl_entries)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| account_details | None | - | - |
| accounting_dimensions | None | - | - |
| gl_entries | None | - | - |

**Returns**: (none)



### get_totals_dict()

**Returns**: (none)



### get_group_by_field(group_by)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| group_by | None | - | - |

**Returns**: (none)



### initialize_gle_map(gl_entries, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| gl_entries | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_accountwise_gle(filters, accounting_dimensions, gl_entries, gle_map)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| accounting_dimensions | None | - | - |
| gl_entries | None | - | - |
| gle_map | None | - | - |

**Returns**: (none)



### get_account_type_map(company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |

**Returns**: (none)



### get_result_as_list(data, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_supplier_invoice_details()

**Returns**: (none)



### get_balance(row, balance, debit_field, credit_field)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| row | None | - | - |
| balance | None | - | - |
| debit_field | None | - | - |
| credit_field | None | - | - |

**Returns**: (none)



### get_columns(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### wrap_in_quotes(label)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| label | None | - | - |

**Returns**: (none)



### add_total_to_data(totals, key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| totals | None | - | - |
| key | None | - | - |

**Returns**: (none)



### update_value_in_dict(data, key, gle, show_net_values = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| key | None | - | - |
| gle | None | - | - |
| show_net_values | None | False | - |

**Returns**: (none)


