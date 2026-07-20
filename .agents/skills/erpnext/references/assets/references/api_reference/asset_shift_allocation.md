# API Reference: asset_shift_allocation.py

**Language**: Python

**Source**: `doctype/asset_shift_allocation/asset_shift_allocation.py`

---

## Classes

### AssetShiftAllocation

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### after_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_invalid_shift_change(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_depr_schedule(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### adjust_depr_shifts(self)

Adjust the shifts in the depreciation schedule based on the new shifts

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate_shift_factor_diff(self, shift_factors_map)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| shift_factors_map | None | - | - |


##### reduce_depr_shifts(self, factor_diff, shift_factors_map, reverse_shift_factors_map)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| factor_diff | None | - | - |
| shift_factors_map | None | - | - |
| reverse_shift_factors_map | None | - | - |


##### add_depr_shifts(self, factor_diff, shift_factors_map, reverse_shift_factors_map)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| factor_diff | None | - | - |
| shift_factors_map | None | - | - |
| reverse_shift_factors_map | None | - | - |


##### add_schedule_row(self, factor, reverse_shift_factors_map)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| factor | None | - | - |
| reverse_shift_factors_map | None | - | - |


##### get_finance_book_row(self, asset_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| asset_doc | None | - | - |


##### modify_depr_schedule(self, temp_depr_schedule)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| temp_depr_schedule | None | - | - |


##### fetch_and_set_depr_schedule(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_new_asset_depr_schedule(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



