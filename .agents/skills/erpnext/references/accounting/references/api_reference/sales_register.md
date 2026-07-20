# API Reference: sales_register.py

**Language**: Python

**Source**: `report/sales_register/sales_register.py`

---

## Functions

### execute(filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |

**Returns**: (none)



### _execute(filters, additional_table_columns = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| additional_table_columns | None | None | - |

**Returns**: (none)



### get_columns(invoice_list, additional_table_columns, include_payments = False)

return columns based on filters

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| invoice_list | None | - | - |
| additional_table_columns | None | - | - |
| include_payments | None | False | - |

**Returns**: (none)



### get_account_columns(invoice_list, include_payments)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| invoice_list | None | - | - |
| include_payments | None | - | - |

**Returns**: (none)



### get_invoices(filters, additional_query_columns)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| additional_query_columns | None | - | - |

**Returns**: (none)



### get_conditions(filters, query, doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| query | None | - | - |
| doctype | None | - | - |

**Returns**: (none)



### get_payments(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### get_invoice_income_map(invoice_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| invoice_list | None | - | - |

**Returns**: (none)



### get_internal_invoice_map(invoice_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| invoice_list | None | - | - |

**Returns**: (none)



### get_invoice_tax_map(invoice_list, invoice_income_map, income_accounts, include_payments = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| invoice_list | None | - | - |
| invoice_income_map | None | - | - |
| income_accounts | None | - | - |
| include_payments | None | False | - |

**Returns**: (none)



### get_invoice_so_dn_map(invoice_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| invoice_list | None | - | - |

**Returns**: (none)



### get_invoice_cc_wh_map(invoice_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| invoice_list | None | - | - |

**Returns**: (none)



### get_mode_of_payments(invoice_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| invoice_list | None | - | - |

**Returns**: (none)


