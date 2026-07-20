# API Reference: account_closing_balance.py

**Language**: Python

**Source**: `doctype/account_closing_balance/account_closing_balance.py`

---

## Classes

### AccountClosingBalance

**Inherits from**: Document



## Functions

### make_closing_entries(closing_entries, voucher_name, company, closing_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| closing_entries | None | - | - |
| voucher_name | None | - | - |
| company | None | - | - |
| closing_date | None | - | - |

**Returns**: (none)



### aggregate_with_last_account_closing_balance(entries, accounting_dimensions)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| entries | None | - | - |
| accounting_dimensions | None | - | - |

**Returns**: (none)



### generate_key(entry, accounting_dimensions)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| entry | None | - | - |
| accounting_dimensions | None | - | - |

**Returns**: (none)



### get_previous_closing_entries(company, closing_date, accounting_dimensions)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| closing_date | None | - | - |
| accounting_dimensions | None | - | - |

**Returns**: (none)



### set_amount_in_reporting_currency(cle, company, closing_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cle | None | - | - |
| company | None | - | - |
| closing_date | None | - | - |

**Returns**: (none)


