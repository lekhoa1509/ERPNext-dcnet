# API Reference: depreciation_methods.py

**Language**: Python

**Source**: `doctype/asset_depreciation_schedule/depreciation_methods.py`

---

## Classes

### StraightLineMethod

**Inherits from**: Document

#### Methods

##### get_straight_line_depr_amount(self, row_idx)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row_idx | None | - | - |


##### get_fixed_depr_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_daily_prorata_based_depr_amount(self, row_idx)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row_idx | None | - | - |


##### get_daily_depr_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_shift_depr_amount(self, row_idx)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row_idx | None | - | - |


##### get_asset_shift_factors_map(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### WDVMethod

**Inherits from**: Document

#### Methods

##### get_wdv_or_dd_depr_amount(self, row_idx)

**Decorators**: `@erpnext.allow_regional`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row_idx | None | - | - |


##### calculate_wdv_or_dd_based_depreciation_amount(self, row_idx)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row_idx | None | - | - |


##### get_wdv_depr_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_fiscal_year_changed(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_daily_prorata_based_wdv_depr_amount(self, row_idx)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row_idx | None | - | - |


##### get_daily_wdv_depr_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



