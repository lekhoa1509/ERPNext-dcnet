# API Reference: item_wise_sales_register.py

**Language**: Python

**Source**: `report/item_wise_sales_register/item_wise_sales_register.py`

---

## Functions

### execute(filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |

**Returns**: (none)



### _execute(filters = None, additional_table_columns = None, additional_conditions = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |
| additional_table_columns | None | None | - |
| additional_conditions | None | None | - |

**Returns**: (none)



### get_income_account(row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| row | None | - | - |

**Returns**: (none)



### get_columns(additional_table_columns, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| additional_table_columns | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### apply_conditions(query, si, sii, sip, filters, additional_conditions = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| query | None | - | - |
| si | None | - | - |
| sii | None | - | - |
| sip | None | - | - |
| filters | None | - | - |
| additional_conditions | None | None | - |

**Returns**: (none)



### apply_order_by_conditions(doctype, query, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| query | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_items(filters, additional_query_columns, additional_conditions = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| additional_query_columns | None | - | - |
| additional_conditions | None | None | - |

**Returns**: (none)



### get_delivery_notes_against_sales_order(item_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_list | None | - | - |

**Returns**: (none)



### get_grand_total(filters, doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| doctype | None | - | - |

**Returns**: (none)



### get_tax_accounts(item_list, columns, company_currency, doctype = 'Sales Invoice', tax_doctype = 'Sales Taxes and Charges')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_list | None | - | - |
| columns | None | - | - |
| company_currency | None | - | - |
| doctype | None | 'Sales Invoice' | - |
| tax_doctype | None | 'Sales Taxes and Charges' | - |

**Returns**: (none)



### get_tax_details_query(doctype, tax_doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| tax_doctype | None | - | - |

**Returns**: (none)



### add_total_row(data, filters, prev_group_by_value, item, total_row_map, group_by_field, subtotal_display_field, grand_total, tax_columns)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| filters | None | - | - |
| prev_group_by_value | None | - | - |
| item | None | - | - |
| total_row_map | None | - | - |
| group_by_field | None | - | - |
| subtotal_display_field | None | - | - |
| grand_total | None | - | - |
| tax_columns | None | - | - |

**Returns**: (none)



### get_display_value(filters, group_by_field, item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| group_by_field | None | - | - |
| item | None | - | - |

**Returns**: (none)



### get_group_by_and_display_fields(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### add_sub_total_row(item, total_row_map, group_by_value, tax_columns)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | None | - | - |
| total_row_map | None | - | - |
| group_by_value | None | - | - |
| tax_columns | None | - | - |

**Returns**: (none)


