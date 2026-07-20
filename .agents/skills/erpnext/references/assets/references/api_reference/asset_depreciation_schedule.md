# API Reference: asset_depreciation_schedule.py

**Language**: Python

**Source**: `doctype/asset_depreciation_schedule/asset_depreciation_schedule.py`

---

## Classes

### AssetDepreciationSchedule

**Inherits from**: DepreciationScheduleController

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_another_asset_depr_schedule_does_not_exist(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_asset(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### cancel_depreciation_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_shift_depr_schedule(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_finance_book_row(self, fb_row = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fb_row | None | None | - |


##### fetch_asset_details(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### make_draft_asset_depr_schedule(asset_doc, row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_doc | None | - | - |
| row | None | - | - |

**Returns**: (none)



### convert_draft_asset_depr_schedules_into_active(asset_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_doc | None | - | - |

**Returns**: (none)



### cancel_asset_depr_schedules(asset_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_doc | None | - | - |

**Returns**: (none)



### reschedule_depreciation(asset_doc, notes, disposal_date = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_doc | None | - | - |
| notes | None | - | - |
| disposal_date | None | None | - |

**Returns**: (none)



### set_modified_depreciation_rate(asset_doc, row, new_schedule)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_doc | None | - | - |
| row | None | - | - |
| new_schedule | None | - | - |

**Returns**: (none)



### get_temp_depr_schedule_doc(asset_doc, fb_row, disposal_date = None, updated_depr_schedule = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_doc | None | - | - |
| fb_row | None | - | - |
| disposal_date | None | None | - |
| updated_depr_schedule | None | None | - |

**Returns**: (none)



### get_current_asset_depr(asset_doc, row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_doc | None | - | - |
| row | None | - | - |

**Returns**: (none)



### modify_depreciation_dchedule(temp_schedule_doc, updated_depr_schedule)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| temp_schedule_doc | None | - | - |
| updated_depr_schedule | None | - | - |

**Returns**: (none)



### get_asset_shift_factors_map()

**Returns**: (none)



### get_depr_schedule(asset_name, status, finance_book = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_name | None | - | - |
| status | None | - | - |
| finance_book | None | None | - |

**Returns**: (none)



### get_asset_depr_schedule_doc(asset_name, status = None, finance_book = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_name | None | - | - |
| status | None | None | - |
| finance_book | None | None | - |

**Returns**: (none)



### get_asset_depr_schedule_name(asset_name, status = None, finance_book = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_name | None | - | - |
| status | None | None | - |
| finance_book | None | None | - |

**Returns**: (none)



### is_first_day_of_the_month(date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | None | - | - |

**Returns**: (none)


