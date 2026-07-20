# API Reference: profit_and_loss_statement.py

**Language**: Python

**Source**: `report/profit_and_loss_statement/profit_and_loss_statement.py`

---

## Functions

### execute(filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |

**Returns**: (none)



### get_report_summary(period_list, periodicity, income, expense, net_profit_loss, currency, filters, consolidated = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| period_list | None | - | - |
| periodicity | None | - | - |
| income | None | - | - |
| expense | None | - | - |
| net_profit_loss | None | - | - |
| currency | None | - | - |
| filters | None | - | - |
| consolidated | None | False | - |

**Returns**: (none)



### get_net_profit_loss(income, expense, period_list, company, currency = None, consolidated = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| income | None | - | - |
| expense | None | - | - |
| period_list | None | - | - |
| company | None | - | - |
| currency | None | None | - |
| consolidated | None | False | - |

**Returns**: (none)



### get_chart_data(filters, columns, income, expense, net_profit_loss, currency)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| columns | None | - | - |
| income | None | - | - |
| expense | None | - | - |
| net_profit_loss | None | - | - |
| currency | None | - | - |

**Returns**: (none)


