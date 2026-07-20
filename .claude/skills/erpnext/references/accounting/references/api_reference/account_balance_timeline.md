# API Reference: account_balance_timeline.py

**Language**: Python

**Source**: `dashboard_chart_source/account_balance_timeline/account_balance_timeline.py`

---

## Functions

### get(chart_name = None, chart = None, no_cache = None, filters = None, from_date = None, to_date = None, timespan = None, time_interval = None, heatmap_year = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| chart_name | None | None | - |
| chart | None | None | - |
| no_cache | None | None | - |
| filters | None | None | - |
| from_date | None | None | - |
| to_date | None | None | - |
| timespan | None | None | - |
| time_interval | None | None | - |
| heatmap_year | None | None | - |

**Returns**: (none)



### build_result(account, dates, gl_entries)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account | None | - | - |
| dates | None | - | - |
| gl_entries | None | - | - |

**Returns**: (none)



### get_gl_entries(account, to_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account | None | - | - |
| to_date | None | - | - |

**Returns**: (none)



### get_dates_from_timegrain(from_date, to_date, timegrain)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| from_date | None | - | - |
| to_date | None | - | - |
| timegrain | None | - | - |

**Returns**: (none)


