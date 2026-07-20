# API Reference: test_stock_analytics.py

**Language**: Python

**Source**: `report/stock_analytics/test_stock_analytics.py`

---

## Classes

### TestStockAnalyticsReport

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### assert_single_item_report(self, movement, expected_buckets)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| movement | None | - | - |
| expected_buckets | None | - | - |


##### generate_stock(self, movement)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| movement | None | - | - |


##### compare_analytics_row(self, report_row, columns, expected_buckets)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| report_row | None | - | - |
| columns | None | - | - |
| expected_buckets | None | - | - |


##### test_get_period_date_ranges(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_period_date_ranges_yearly(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_basic_report_functionality(self)

Stock analytics report generates balance "as of" periods based on
user defined ranges. Check that this behaviour is correct.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_empty_month_in_between(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_multi_month_missings(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### stock_analytics(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)


