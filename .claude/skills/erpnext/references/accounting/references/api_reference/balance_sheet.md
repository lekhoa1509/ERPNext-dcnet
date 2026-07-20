# API Reference: balance_sheet.py

**Language**: Python

**Source**: `report/balance_sheet/balance_sheet.py`

---

## Functions

### execute(filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |

**Returns**: (none)



### get_provisional_profit_loss(asset, liability, equity, period_list, company, currency = None, consolidated = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset | None | - | - |
| liability | None | - | - |
| equity | None | - | - |
| period_list | None | - | - |
| company | None | - | - |
| currency | None | None | - |
| consolidated | None | False | - |

**Returns**: (none)



### check_opening_balance(asset, liability, equity)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset | None | - | - |
| liability | None | - | - |
| equity | None | - | - |

**Returns**: (none)



### get_report_summary(period_list, asset, liability, equity, provisional_profit_loss, currency, filters, consolidated = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| period_list | None | - | - |
| asset | None | - | - |
| liability | None | - | - |
| equity | None | - | - |
| provisional_profit_loss | None | - | - |
| currency | None | - | - |
| filters | None | - | - |
| consolidated | None | False | - |

**Returns**: (none)



### get_chart_data(filters, columns, asset, liability, equity, currency)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| columns | None | - | - |
| asset | None | - | - |
| liability | None | - | - |
| equity | None | - | - |
| currency | None | - | - |

**Returns**: (none)


