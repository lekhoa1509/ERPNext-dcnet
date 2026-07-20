# API Reference: depreciation.py

**Language**: Python

**Source**: `doctype/asset/depreciation.py`

---

## Functions

### post_depreciation_entries(date = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | None | None | - |

**Returns**: (none)



### book_depreciation_entries(date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | None | - | - |

**Returns**: (none)



### get_depreciable_assets_data(date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | None | - | - |

**Returns**: (none)



### get_companies_with_frozen_limits()

**Returns**: (none)



### make_depreciation_entry_on_disposal(asset_doc, disposal_date = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_doc | None | - | - |
| disposal_date | None | None | - |

**Returns**: (none)



### get_credit_debit_accounts_for_asset(asset_category, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_category | None | - | - |
| company | None | - | - |

**Returns**: (none)



### get_depreciation_cost_center_and_series(asset)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset | None | - | - |

**Returns**: (none)



### get_depr_cost_center_and_series()

**Returns**: (none)



### make_depreciation_entry(depr_schedule_name, date = None, sch_start_idx = None, sch_end_idx = None, accounting_dimensions = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| depr_schedule_name | None | - | - |
| date | None | None | - |
| sch_start_idx | None | None | - |
| sch_end_idx | None | None | - |
| accounting_dimensions | None | None | - |

**Returns**: (none)



### _make_journal_entry_for_depreciation(depr_schedule_doc, asset, date, depr_schedule, sch_start_idx, sch_end_idx, depr_cost_center, depr_series, credit_account, debit_account, accounting_dimensions)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| depr_schedule_doc | None | - | - |
| asset | None | - | - |
| date | None | - | - |
| depr_schedule | None | - | - |
| sch_start_idx | None | - | - |
| sch_end_idx | None | - | - |
| depr_cost_center | None | - | - |
| depr_series | None | - | - |
| credit_account | None | - | - |
| debit_account | None | - | - |
| accounting_dimensions | None | - | - |

**Returns**: (none)



### setup_journal_entry_metadata(je, depr_schedule_doc, depr_series, depr_schedule, asset)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| je | None | - | - |
| depr_schedule_doc | None | - | - |
| depr_series | None | - | - |
| depr_schedule | None | - | - |
| asset | None | - | - |

**Returns**: (none)



### get_credit_and_debit_entry(credit_account, depr_schedule, asset, depr_cost_center, debit_account, dimensions)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| credit_account | None | - | - |
| depr_schedule | None | - | - |
| asset | None | - | - |
| depr_cost_center | None | - | - |
| debit_account | None | - | - |
| dimensions | None | - | - |

**Returns**: (none)



### get_credit_and_debit_accounts(accumulated_depreciation_account, depreciation_expense_account)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| accumulated_depreciation_account | None | - | - |
| depreciation_expense_account | None | - | - |

**Returns**: (none)



### set_depr_entry_posting_status_for_failed_assets(failed_asset_names)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| failed_asset_names | None | - | - |

**Returns**: (none)



### notify_depr_entry_posting_error(failed_asset_names, error_log_names)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| failed_asset_names | None | - | - |
| error_log_names | None | - | - |

**Returns**: (none)



### get_comma_separated_links(names, doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| names | None | - | - |
| doctype | None | - | - |

**Returns**: (none)



### get_message_for_depr_entry_posting_error(asset_links, error_log_links)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_links | None | - | - |
| error_log_links | None | - | - |

**Returns**: (none)



### scrap_asset(asset_name, scrap_date = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_name | None | - | - |
| scrap_date | None | None | - |

**Returns**: (none)



### validate_asset_for_scrap(asset, scrap_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset | None | - | - |
| scrap_date | None | - | - |

**Returns**: (none)



### validate_scrap_date(asset, scrap_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset | None | - | - |
| scrap_date | None | - | - |

**Returns**: (none)



### get_last_depreciation_date(asset_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_name | None | - | - |

**Returns**: (none)



### get_note_for_scrap(asset)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset | None | - | - |

**Returns**: (none)



### create_journal_entry_for_scrap(asset, scrap_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset | None | - | - |
| scrap_date | None | - | - |

**Returns**: (none)



### restore_asset(asset_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_name | None | - | - |

**Returns**: (none)



### get_note_for_restore(asset)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset | None | - | - |

**Returns**: (none)



### cancel_journal_entry_for_scrap(asset)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset | None | - | - |

**Returns**: (none)



### depreciate_asset(asset_doc, date, notes)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_doc | None | - | - |
| date | None | - | - |
| notes | None | - | - |

**Returns**: (none)



### cancel_depreciation_entries(asset_doc, date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_doc | None | - | - |
| date | None | - | - |

**Returns**: (none)



### reset_depreciation_schedule(asset_doc, notes)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_doc | None | - | - |
| notes | None | - | - |

**Returns**: (none)



### reverse_depreciation_entry_made_on_disposal(asset)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset | None | - | - |

**Returns**: (none)



### disposal_was_made_on_original_schedule_date(schedule_idx, row, disposal_date)

If asset is scrapped or sold on original schedule date,
then the depreciation entry should not be reversed.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| schedule_idx | None | - | - |
| row | None | - | - |
| disposal_date | None | - | - |

**Returns**: (none)



### disposal_happens_in_the_future(disposal_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| disposal_date | None | - | - |

**Returns**: (none)



### create_reverse_depreciation_entry(asset_name, journal_entry)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_name | None | - | - |
| journal_entry | None | - | - |

**Returns**: (none)



### update_value_after_depreciation_on_asset_restore(schedule, row, journal_entry)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| schedule | None | - | - |
| row | None | - | - |
| journal_entry | None | - | - |

**Returns**: (none)



### get_depreciation_amount_in_je(journal_entry)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| journal_entry | None | - | - |

**Returns**: (none)



### get_gl_entries_on_asset_regain(asset, selling_amount = 0, finance_book = None, voucher_type = None, voucher_no = None, date = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset | None | - | - |
| selling_amount | None | 0 | - |
| finance_book | None | None | - |
| voucher_type | None | None | - |
| voucher_no | None | None | - |
| date | None | None | - |

**Returns**: (none)



### get_gl_entries_on_asset_disposal(asset, selling_amount = 0, finance_book = None, voucher_type = None, voucher_no = None, date = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset | None | - | - |
| selling_amount | None | 0 | - |
| finance_book | None | None | - |
| voucher_type | None | None | - |
| voucher_no | None | None | - |
| date | None | None | - |

**Returns**: (none)



### get_asset_details(asset, finance_book = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset | None | - | - |
| finance_book | None | None | - |

**Returns**: (none)



### get_depreciation_accounts(asset_category, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_category | None | - | - |
| company | None | - | - |

**Returns**: (none)



### get_profit_gl_entries(asset, profit_amount, gl_entries, disposal_account, depreciation_cost_center, date = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset | None | - | - |
| profit_amount | None | - | - |
| gl_entries | None | - | - |
| disposal_account | None | - | - |
| depreciation_cost_center | None | - | - |
| date | None | None | - |

**Returns**: (none)



### get_disposal_account_and_cost_center(company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |

**Returns**: (none)



### get_value_after_depreciation_on_disposal_date(asset, disposal_date, finance_book = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset | None | - | - |
| disposal_date | None | - | - |
| finance_book | None | None | - |

**Returns**: (none)



### validate_disposal_date(reference_date, disposal_date, label)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| reference_date | None | - | - |
| disposal_date | None | - | - |
| label | None | - | - |

**Returns**: (none)


