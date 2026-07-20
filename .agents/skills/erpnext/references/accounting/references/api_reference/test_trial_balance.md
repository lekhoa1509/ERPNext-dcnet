# API Reference: test_trial_balance.py

**Language**: Python

**Source**: `report/trial_balance/test_trial_balance.py`

---

## Classes

### TestTrialBalance

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_offsetting_entries_for_accounting_dimensions(self)

Checks if Trial Balance Report is balanced when filtered using a particular Accounting Dimension

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_company()

**Returns**: (none)



### create_accounting_dimension()

**Returns**: (none)



### disable_dimension()

**Returns**: (none)



### clear_dimension_defaults(dimension_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dimension_name | None | - | - |

**Returns**: (none)


