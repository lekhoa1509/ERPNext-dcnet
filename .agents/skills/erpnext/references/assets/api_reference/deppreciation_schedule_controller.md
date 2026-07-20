# API Reference: deppreciation_schedule_controller.py

**Language**: Python

**Source**: `doctype/asset_depreciation_schedule/deppreciation_schedule_controller.py`

---

## Classes

### DepreciationScheduleController

**Inherits from**: StraightLineMethod, WDVMethod

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_depreciation_schedule(self, fb_row = None, disposal_date = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fb_row | None | None | - |
| disposal_date | None | None | - |


##### clear(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### initialize_variables(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_final_number_of_depreciations(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_final_number_of_depreciations_considering_increase_in_asset_life(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_wdv_or_dd_non_yearly_pro_rata(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _check_is_pro_rata(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _get_modified_available_for_use_date_for_existing_assets(self)

if Asset has opening booked depreciations = 3,
frequency of depreciation = 3,
available for use date = 17-07-2023,
depreciation start date = 30-06-2024
then from date should be 01-04-2024

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_total_days(self, date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| date | None | - | - |


##### _get_pro_rata_amt(self, from_date, to_date, original_schedule_date = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| from_date | None | - | - |
| to_date | None | - | - |
| original_schedule_date | None | None | - |


##### get_number_of_pending_months(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_last_booked_depreciation_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_booked_depr_for_months_count(self, last_depr_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| last_depr_date | None | - | - |


##### get_total_pending_days_or_years(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### has_fiscal_year_changed(self, row_idx)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row_idx | None | - | - |


##### get_prev_depreciation_amount(self, row_idx)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row_idx | None | - | - |


##### get_next_schedule_date(self, row_idx)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row_idx | None | - | - |


##### set_depreciation_amount_for_disposal(self, row_idx)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row_idx | None | - | - |


##### set_depreciation_amount_for_first_row(self, row_idx)

For the first row, if available for use date is mid of the month, then pro rata amount is needed

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row_idx | None | - | - |


##### set_depreciation_amount_for_last_row(self, row_idx)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row_idx | None | - | - |


##### adjust_depr_amount_for_salvage_value(self, row_idx)

Adjust depreciation amount in the last period based on the expected value after useful life

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row_idx | None | - | - |


##### validate_depreciation_amount_for_low_value_assets(self)

If net purchase amount is too low, then depreciation amount
can come zero sometimes based on the frequency and number of depreciations.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_depr_schedule_row(self, row_idx)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row_idx | None | - | - |


##### set_accumulated_depreciation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_depreciation_amount(self, row_idx)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row_idx | None | - | - |


##### _get_total_days(self, depreciation_start_date, row_idx)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| depreciation_start_date | None | - | - |
| row_idx | None | - | - |


##### get_total_days_in_current_depr_year(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_fiscal_year(self, date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| date | None | - | - |



