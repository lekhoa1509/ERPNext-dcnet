# API Reference: point_of_sale.py

**Language**: Python

**Source**: `page/point_of_sale/point_of_sale.py`

---

## Functions

### search_by_term(search_term, warehouse, price_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| search_term | None | - | - |
| warehouse | None | - | - |
| price_list | None | - | - |

**Returns**: (none)



### filter_result_items(result, pos_profile)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| result | None | - | - |
| pos_profile | None | - | - |

**Returns**: (none)



### get_parent_item_group(pos_profile)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pos_profile | None | - | - |

**Returns**: (none)



### get_items(start, page_length, price_list, item_group, pos_profile, search_term = '')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| start | None | - | - |
| page_length | None | - | - |
| price_list | None | - | - |
| item_group | None | - | - |
| pos_profile | None | - | - |
| search_term | None | '' | - |

**Returns**: (none)



### search_for_serial_or_batch_or_barcode_number(search_value: str) → dict[str, str | None]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| search_value | str | - | - |

**Returns**: `dict[str, str | None]`



### get_conditions(search_term)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| search_term | None | - | - |

**Returns**: (none)



### add_search_fields_condition(search_term)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| search_term | None | - | - |

**Returns**: (none)



### get_item_group_condition(pos_profile)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pos_profile | None | - | - |

**Returns**: (none)



### item_group_query(doctype, txt, searchfield, start, page_len, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| txt | None | - | - |
| searchfield | None | - | - |
| start | None | - | - |
| page_len | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### check_opening_entry(user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |

**Returns**: (none)



### create_opening_voucher(pos_profile, company, balance_details)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pos_profile | None | - | - |
| company | None | - | - |
| balance_details | None | - | - |

**Returns**: (none)



### get_past_order_list(search_term, status, limit = 20)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| search_term | None | - | - |
| status | None | - | - |
| limit | None | 20 | - |

**Returns**: (none)



### set_customer_info(fieldname, customer, value = '')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fieldname | None | - | - |
| customer | None | - | - |
| value | None | '' | - |

**Returns**: (none)



### get_pos_profile_data(pos_profile)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pos_profile | None | - | - |

**Returns**: (none)



### add_doctype_to_results(doctype, results)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| results | None | - | - |

**Returns**: (none)



### order_results_by_posting_date(results)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| results | None | - | - |

**Returns**: (none)



### get_invoice_filters(doctype, status, name = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| status | None | - | - |
| name | None | None | - |

**Returns**: (none)



### get_customer_recent_transactions(customer)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| customer | None | - | - |

**Returns**: (none)



### __sort(p)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| p | None | - | - |

**Returns**: (none)


