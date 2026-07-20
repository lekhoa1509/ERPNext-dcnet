# API Reference: asset_value_adjustment.py

**Language**: Python

**Source**: `doctype/asset_value_adjustment/asset_value_adjustment.py`

---

## Classes

### AssetValueAdjustment

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_difference_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_current_asset_value(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_asset_revaluation_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_entry_for_asset_value_decrease(self, fixed_asset_account, entry_template)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fixed_asset_account | None | - | - |
| entry_template | None | - | - |


##### get_entry_for_asset_value_increase(self, fixed_asset_account, entry_template)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fixed_asset_account | None | - | - |
| entry_template | None | - | - |


##### update_accounting_dimensions(self, credit_entry, debit_entry)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| credit_entry | None | - | - |
| debit_entry | None | - | - |


##### cancel_asset_revaluation_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_asset(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_asset_value_after_depreciation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_adjusted_salvage_value_amount(self, row, difference_amount)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| difference_amount | None | - | - |


##### get_adjustment_note(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_value_of_accounting_dimensions(asset_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_name | None | - | - |

**Returns**: (none)


