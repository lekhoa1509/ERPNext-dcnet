# API Reference: test_asset.py

**Language**: Python

**Source**: `doctype/asset/test_asset.py`

---

## Classes

### AssetSetup

**Inherits from**: IntegrationTestCase

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### tearDownClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |




### TestAsset

**Inherits from**: AssetSetup

#### Methods

##### test_asset_category_is_fetched(self)

Tests if the Item's Asset Category value is assigned to the Asset, if the field is empty.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_net_purchase_amount_is_mandatory(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_pr_or_pi_mandatory_if_not_existing_asset(self)

Tests if either PI or PR is present if CWIP is enabled and is_existing_asset=0.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_available_for_use_date_is_after_purchase_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_item_exists(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_validate_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_asset(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_of_grouped_asset(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_is_fixed_asset_set(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_scrap_asset(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_gle_made_by_asset_sale(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_gle_made_by_asset_sale_for_existing_asset(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_asset_with_maintenance_required_status_after_sale(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_asset_splitting(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_expense_head(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cwip_accounting(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_asset_cwip_toggling_cases(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_partial_asset_sale(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_asset_splitting_for_non_existing_asset(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestDepreciationMethods

**Inherits from**: AssetSetup

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### tearDownClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### test_schedule_for_straight_line_method(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_schedule_for_straight_line_method_with_daily_prorata_based(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_schedule_for_straight_line_method_for_existing_asset(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_schedule_for_double_declining_method(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_schedule_for_double_declining_method_for_existing_asset(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_schedule_for_prorated_straight_line_method(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_depreciation_entry_for_wdv_without_pro_rata(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_pro_rata_depreciation_entry_for_wdv(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_monthly_depreciation_by_wdv_method(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestDepreciationBasics

**Inherits from**: AssetSetup

#### Methods

##### test_depreciation_without_pro_rata(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_depreciation_with_pro_rata(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_depreciation_amount(self)

Tests if get_depreciation_amount() returns the right value.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_depr_schedule(self)

Tests if make_depr_schedule() returns the right values.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_set_accumulated_depreciation(self)

Tests if set_accumulated_depreciation() returns the right values.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_check_is_pro_rata(self)

Tests if check_is_pro_rata() returns the right value(i.e. checks if has_pro_rata is accurate).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_expected_value_after_useful_life_greater_than_purchase_amount(self)

Tests if an error is raised when expected_value_after_useful_life(110,000) > net_purchase_amount(100,000).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_depreciation_start_date(self)

Tests if an error is raised when neither depreciation_start_date nor available_for_use_date are specified.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_opening_accumulated_depreciation(self)

Tests if an error is raised when opening_accumulated_depreciation > (net_purchase_amount - expected_value_after_useful_life).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_opening_booked_depreciations(self)

Tests if an error is raised when opening_number_of_booked_depreciations is not specified when opening_accumulated_depreciation is.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_number_of_depreciations(self)

Tests if an error is raised when opening_number_of_booked_depreciations >= total_number_of_depreciations.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_depreciation_start_date_is_before_purchase_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_depreciation_start_date_is_before_available_for_use_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_finance_books_are_present_if_calculate_depreciation_is_enabled(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_post_depreciation_entries(self)

Tests if post_depreciation_entries() works as expected.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_depr_entry_posting_when_depr_expense_account_is_an_expense_account(self)

Tests if the Depreciation Expense Account gets debited and the Accumulated Depreciation Account gets credited when the former's an Expense Account.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_depr_entry_posting_when_depr_expense_account_is_an_income_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_clear_depr_schedule(self)

Tests if clear_depr_schedule() works as expected.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_clear_depr_schedule_for_multiple_finance_books(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_depreciation_schedules_are_set_up_for_multiple_finance_books(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_depreciation_entry_cancellation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_asset_expected_value_after_useful_life(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_gle_made_by_depreciation_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_expected_value_change(self)

tests if changing `expected_value_after_useful_life`
affects `value_after_depreciation`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_asset_cost_center(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_depreciation_on_final_day_of_the_month(self)

Tests if final day of the month is picked each time, if the depreciation start date is the last day of the month.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_manual_depreciation_for_existing_asset(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_manual_depreciation_for_depreciable_asset(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_manual_depreciation_with_incorrect_jv_voucher_type(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_multi_currency_asset_pr_creation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_split_asset_created_via_capitalization(self)

Test that assets created via Asset Capitalization can be split without capitalization error

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_gl_entries(doctype, docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| docname | None | - | - |

**Returns**: (none)



### create_asset_data()

**Returns**: (none)



### create_asset()

**Returns**: (none)



### create_asset_category(enable_cwip = 1)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| enable_cwip | None | 1 | - |

**Returns**: (none)



### create_fixed_asset_item(item_code = None, auto_create_assets = 1, is_grouped_asset = 0)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | None | - |
| auto_create_assets | None | 1 | - |
| is_grouped_asset | None | 0 | - |

**Returns**: (none)



### set_depreciation_settings_in_company(company = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | None | - |

**Returns**: (none)



### enable_cwip_accounting(asset_category, enable = 1)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_category | None | - | - |
| enable | None | 1 | - |

**Returns**: (none)


