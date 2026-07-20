# API Reference: tax_withholding_details.py

**Language**: Python

**Source**: `report/tax_withholding_details/tax_withholding_details.py`

---

## Functions

### execute(filters = None)

Generate Tax Withholding Details report

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |

**Returns**: (none)



### validate_filters(filters)

Validate report filters

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### get_tax_withholding_data(filters)

Process entries into final report format

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### get_party_details(entries)

Fetch party details in batch for all entries

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| entries | None | - | - |

**Returns**: (none)



### get_columns(filters)

Generate report columns based on filters

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### get_tax_withholding_entries(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### get_additional_doc_info(entries)

Fetch additional document information in batch

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| entries | None | - | - |

**Returns**: (none)



### _fetch_doc_info(doctype_name, voucher_set, doc_info)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype_name | None | - | - |
| voucher_set | None | - | - |
| doc_info | None | - | - |

**Returns**: (none)


