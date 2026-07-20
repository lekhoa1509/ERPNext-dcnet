# API Reference: test_tax_withholding_details.py

**Language**: Python

**Source**: `report/tax_withholding_details/test_tax_withholding_details.py`

---

## Classes

### TestTaxWithholdingDetails

**Inherits from**: AccountsTestMixin, IntegrationTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tax_withholding_for_customers(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_single_account_for_multiple_categories(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_date_filters_in_multiple_tax_withholding_rules(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_expected_values(self, result, expected_values)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| result | None | - | - |
| expected_values | None | - | - |


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_tax_accounts()

**Returns**: (none)



### create_tax_category(category = 'TCS', rate = 0.075, account = 'TCS - _TC', cumulative_threshold = 0)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| category | None | 'TCS' | - |
| rate | None | 0.075 | - |
| account | None | 'TCS - _TC' | - |
| cumulative_threshold | None | 0 | - |

**Returns**: (none)



### create_tcs_payment_entry()

**Returns**: (none)



### create_tcs_journal_entry()

**Returns**: (none)


