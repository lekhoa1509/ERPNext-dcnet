# API Reference: tax_withholding_entry.py

**Language**: Python

**Source**: `doctype/tax_withholding_entry/tax_withholding_entry.py`

---

## Classes

### TaxWithholdingEntry

**Inherits from**: Document

#### Methods

##### set_status(self, status = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| status | None | None | - |


##### get_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_adjustments(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_tax_withheld_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_taxable_different(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_withholding_different(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _process_tax_withholding_adjustments(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _adjust_against_old_entries(self, field_type: str) → set

Find old entries that need adjustment and update them.
The logic reads like: "Match up old incomplete entries with this new entry"

Args:
                field_type: Either "taxable" or "withholding" - determines which fields to use

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| field_type | str | - | - |

**Returns**: `set`


##### _get_values_to_update(self, old_entry, proportion: float, field_type: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| old_entry | None | - | - |
| proportion | float | - | - |
| field_type | str | - | - |


##### _get_balance_values_to_update(self, old_entry, proportion: float, field_type: str)

Calculate the balance amounts for both taxable and withholding fields for partial adjustments

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| old_entry | None | - | - |
| proportion | float | - | - |
| field_type | str | - | - |


##### _clear_old_references(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _handle_return_invoice_cancellation(self, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| filters | None | - | - |




### TaxWithholdingController

**Inherits from**: (none)

#### Methods

##### __init__(self, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### _get_category_details(self)

Get tax withholding category details for the current document

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _get_category_names(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _generate_withholding_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _create_entries_for_category(self, category)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| category | None | - | - |


##### _create_under_withheld_entry(self, category)

Create an under withheld entry when threshold is not crossed

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| category | None | - | - |


##### _create_threshold_exemption_entry(self, category)

Create entry for amount below threshold (tax on excess)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| category | None | - | - |


##### _get_open_entries_for_category(self, category)

Get historical under withheld and over withheld entries for processing

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| category | None | - | - |


##### _categorize_historical_entries(self, entries, linked_payments, open_entries)

Categorize historical entries into under withheld and over withheld

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| entries | None | - | - |
| linked_payments | None | - | - |
| open_entries | None | - | - |


##### _process_ldc_entries(self, under_entries, over_entries, category)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| under_entries | None | - | - |
| over_entries | None | - | - |
| category | None | - | - |


##### _update_taxable_amounts(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _update_amount_for_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _update_item_wise_tax_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _evaluate_thresholds(self)

Evaluate if thresholds are crossed for each category

Thresholds are crossed when:
- Single transaction threshold is exceeded
- Cumulative threshold is exceeded
- Threshold check is manually overridden

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _is_threshold_crossed_for_category(self, category)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| category | None | - | - |


##### _check_historical_threshold_status(self, category)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| category | None | - | - |


##### _get_unused_threshold(self, category)

Calculate unused threshold amount for tax on excess scenarios

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| category | None | - | - |


##### _base_threshold_query(self, category)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| category | None | - | - |


##### _get_historical_entries(self, category)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| category | None | - | - |


##### _get_linked_payments(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _create_default_entry(self, category)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| category | None | - | - |


##### update_tax_rows(self)

Update tax rows in the parent document based on withholding entries

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _create_tax_row(self, account_head, tax_amount)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| account_head | None | - | - |
| tax_amount | None | - | - |


##### _set_item_wise_tax_for_tds(self, tax_row, account_head, category_withholding_map, for_update = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| tax_row | None | - | - |
| account_head | None | - | - |
| category_withholding_map | None | - | - |
| for_update | None | False | - |


##### _get_category_withholding_map(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _calculate_account_wise_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _remove_zero_tax_rows(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _adjust_under_over_withheld(self, under_entries: deque, over_entries: deque, category: dict)

Merge under withheld and over withheld entries based on the tax rate and constraint.
If only under and over entries are available, they will be processed against current document.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| under_entries | deque | - | - |
| over_entries | deque | - | - |
| category | dict | - | - |


##### _merge_entries(self, under_entries: deque, over_entries: deque, category: dict, tax_rate: float | None = None, constraint: float = inf, default_obj: dict | None = None)

Merge under withheld and over withheld entries based on the tax rate and constraint.
If only under and over entries are available, they will be processed against current document.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| under_entries | deque | - | - |
| over_entries | deque | - | - |
| category | dict | - | - |
| tax_rate | float | None | None | - |
| constraint | float | inf | - |
| default_obj | dict | None | None | - |


##### _process_under_withheld_entries(self, under_entries, category, tax_rate, constraint, default_obj, merged_entries)

Process remaining Under Withheld Entries - adjust against current document

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| under_entries | None | - | - |
| category | None | - | - |
| tax_rate | None | - | - |
| constraint | None | - | - |
| default_obj | None | - | - |
| merged_entries | None | - | - |


##### _process_over_withheld_entries(self, over_entries, category, tax_rate, constraint, default_obj, merged_entries)

Process remaining Over Withheld Entries - adjust existing over-withheld amounts

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| over_entries | None | - | - |
| category | None | - | - |
| tax_rate | None | - | - |
| constraint | None | - | - |
| default_obj | None | - | - |
| merged_entries | None | - | - |


##### _create_base_entry(self, source_entry, category, tax_rate, default_obj)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| source_entry | None | - | - |
| category | None | - | - |
| tax_rate | None | - | - |
| default_obj | None | - | - |


##### _should_include_entry(self, entry)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| entry | None | - | - |


##### compute_withheld_amount(self, taxable_amount, tax_rate, round_off_tax_amount = False)

Calculate the withholding amount based on taxable amount and rate

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| taxable_amount | None | - | - |
| tax_rate | None | - | - |
| round_off_tax_amount | None | False | - |


##### _process_withholding_entries(self)

Final processing - update tax rows and validate

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


##### _is_tax_withholding_applicable(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _clear_existing_tax_amounts(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate_taxes_and_totals(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_conversion_rate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### PurchaseTaxWithholding

Tax withholding controller for Purchase Invoices

**Inherits from**: TaxWithholdingController

#### Methods

##### __init__(self, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |




### SalesTaxWithholding

Tax withholding controller for Sales Invoices (TCS)

**Inherits from**: TaxWithholdingController

#### Methods

##### __init__(self, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |




### PaymentTaxWithholding

Tax withholding controller for Payment Entries

**Inherits from**: TaxWithholdingController

#### Methods

##### __init__(self, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### _get_category_names(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _update_taxable_amounts(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_conversion_rate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate_taxes_and_totals(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _get_open_entries_for_category(self, category)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| category | None | - | - |


##### _is_threshold_crossed_for_category(self, category)

For payment entries if apply_tds is checked, return True

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| category | None | - | - |


##### _get_unused_threshold(self, category)

Always withhold Tax and whenever tax gets deducted adjust it

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| category | None | - | - |




### JournalTaxWithholding

Tax withholding controller for Journal Entries

**Inherits from**: TaxWithholdingController

#### Methods

##### __init__(self, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### _setup_party_info(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _setup_direction_fields(self)

For Supplier (TDS): party has credit, TDS reduces credit
For Customer (TCS): party has debit, TCS increases debit

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _get_category_names(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _update_taxable_amounts(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _calculate_net_total(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_conversion_rate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate_taxes_and_totals(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_tax_rows(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _should_apply_tds(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _reset_existing_tds(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _update_party_amount(self, amount, is_reversal = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| amount | None | - | - |
| is_reversal | None | False | - |


##### _create_or_update_tds_row(self, account_head, tax_amount)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| account_head | None | - | - |
| tax_amount | None | - | - |


##### _cleanup_duplicate_tds_rows(self, current_tax_row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| current_tax_row | None | - | - |


##### _recalculate_totals(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _is_tax_withholding_applicable(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _get_linked_payments(self)

Journal Entry doesn't have advances like invoices

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### _reset_idx(docs_to_reset_idx)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docs_to_reset_idx | None | - | - |

**Returns**: (none)


