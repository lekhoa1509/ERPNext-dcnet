# API Reference: stock_analytics.py

**Language**: Python

**Source**: `report/stock_analytics/stock_analytics.py`

---

## Functions

### execute(filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |

**Returns**: (none)



### get_columns(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### get_period_date_ranges(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### round_down_to_nearest_frequency(date: str, frequency: str) → datetime.datetime

Rounds down the date to nearest frequency unit.
example:

>>> round_down_to_nearest_frequency("2021-02-21", "Monthly")
datetime.datetime(2021, 2, 1)

>>> round_down_to_nearest_frequency("2021-08-21", "Yearly")
datetime.datetime(2021, 1, 1)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | str | - | - |
| frequency | str | - | - |

**Returns**: `datetime.datetime`



### get_period(posting_date, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| posting_date | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_periodic_data(entry, filters)

Structured as:
Item 1
        - Balance (updated and carried forward):
                        - Warehouse A : bal_qty/value
                        - Warehouse B : bal_qty/value
        - Jun 2021 (sum of warehouse quantities used in report)
                        - Warehouse A : bal_qty/value
                        - Warehouse B : bal_qty/value
        - Jul 2021 (sum of warehouse quantities used in report)
                        - Warehouse A : bal_qty/value
                        - Warehouse B : bal_qty/value
Item 2
        - Balance (updated and carried forward):
                        - Warehouse A : bal_qty/value
                        - Warehouse B : bal_qty/value
        - Jun 2021 (sum of warehouse quantities used in report)
                        - Warehouse A : bal_qty/value
                        - Warehouse B : bal_qty/value
        - Jul 2021 (sum of warehouse quantities used in report)
                        - Warehouse A : bal_qty/value
                        - Warehouse B : bal_qty/value

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| entry | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### fill_intermediate_periods(periodic_data, item_code: str, current_period: str, all_periods: list[str]) → None

There might be intermediate periods where no stock ledger entry exists, copy previous previous data.

Previous data is ONLY copied if period falls in report range and before period being processed currently.

args:
        current_period: process till this period (exclusive)
        all_periods: all periods expected in report via filters
        periodic_data: report's periodic data
        item_code: item_code being processed

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| periodic_data | None | - | - |
| item_code | str | - | - |
| current_period | str | - | - |
| all_periods | list[str] | - | - |

**Returns**: `None`



### get_data(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### get_chart_data(columns)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| columns | None | - | - |

**Returns**: (none)



### get_items(filters)

Get items based on item code, item group or brand.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### get_stock_ledger_entries(filters, items)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| items | None | - | - |

**Returns**: (none)



### apply_conditions(query, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| query | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_item_details(items, sle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| items | None | - | - |
| sle | None | - | - |

**Returns**: (none)



### _get_first_day_of_fiscal_year(date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | None | - | - |

**Returns**: (none)


