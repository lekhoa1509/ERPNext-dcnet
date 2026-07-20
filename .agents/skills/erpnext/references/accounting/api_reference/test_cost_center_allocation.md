# API Reference: test_cost_center_allocation.py

**Language**: Python

**Source**: `doctype/cost_center_allocation/test_cost_center_allocation.py`

---

## Classes

### TestCostCenterAllocation

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_gle_based_on_cost_center_allocation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_main_cost_center_cant_be_child(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_invalid_main_cost_center(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_if_child_cost_center_has_any_allocation_record(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_total_percentage(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_valid_from_based_on_existing_gle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_multiple_cost_center_allocation_on_same_main_cost_center(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_debit_credit_on_cost_center_allocation_for_commercial_rounding(self)

**Decorators**: `@IntegrationTestCase.change_settings('System Settings', {'rounding_method': 'Commercial Rounding'})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_cost_center_allocation(company, main_cost_center, allocation_percentages, valid_from = None, valid_upto = None, save = True, submit = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| main_cost_center | None | - | - |
| allocation_percentages | None | - | - |
| valid_from | None | None | - |
| valid_upto | None | None | - |
| save | None | True | - |
| submit | None | True | - |

**Returns**: (none)


