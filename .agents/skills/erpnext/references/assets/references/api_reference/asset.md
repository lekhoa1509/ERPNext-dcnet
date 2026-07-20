# API Reference: asset.py

**Language**: Python

**Source**: `doctype/asset/asset.py`

---

## Classes

### Asset

**Inherits from**: AccountsController

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_save(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_asset_depreciation_schedule(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### evaluate_and_recreate_depreciation_schedule(self, existing_doc, fb_row)

Determine if depreciation schedule needs to be regenerated and recreate if necessary

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| existing_doc | None | - | - |
| fb_row | None | - | - |


##### has_asset_details_changed(self, existing_doc)

Check if core asset details that affect depreciation have changed

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| existing_doc | None | - | - |


##### has_depreciation_settings_changed(self, existing_doc, fb_row)

Check if depreciation calculation settings have changed

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| existing_doc | None | - | - |
| fb_row | None | - | - |


##### should_regenerate_depreciation_schedule(self, existing_doc, asset_details_changed, depreciation_settings_changed)

Check all conditions to determine if schedule regeneration is required

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| existing_doc | None | - | - |
| asset_details_changed | None | - | - |
| depreciation_settings_changed | None | - | - |


##### set_depr_rate_and_value_after_depreciation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### show_schedule_creation_message(self, schedules)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| schedules | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_submit(self)

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


##### after_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### after_delete(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_purchase_doc_row_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_linked_item(self, purchase_doc_type, purchase_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| purchase_doc_type | None | - | - |
| purchase_doc | None | - | - |


##### validate_asset_and_reference(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_cost_center(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_in_use_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_missing_values(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_finance_books(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_category(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_precision(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_asset_values(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_linked_purchase_documents(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_asset_qty_with_purchase_doc(self, doctype, purchase_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| purchase_doc | None | - | - |


##### validate_gross_and_purchase_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_asset_movement(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_depreciation_rate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_asset_finance_books(self, row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |


##### validate_opening_depreciation_values(self, row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |


##### validate_total_number_of_depreciations_and_frequency(self, row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |


##### validate_depreciation_start_date(self, row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |


##### set_total_booked_depreciations(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_expected_value_after_useful_life(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_cancellation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### cancel_movement_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delete_depreciation_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_status(self, status = None)

Get and update status

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| status | None | None | - |


##### get_status(self)

Returns status based on whether it is draft, submitted, scrapped or depreciated

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_value_after_depreciation(self, finance_book = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| finance_book | None | None | - |


##### get_default_finance_book_idx(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_manual_depreciation_entries(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_make_gl_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_purchase_document(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_fixed_asset_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_cwip_account(self, cwip_enabled = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| cwip_enabled | None | False | - |


##### make_gl_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_asset_capitalization_gl_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_depreciation_rate(self, args, on_validate = False)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| args | None | - | - |
| on_validate | None | False | - |


##### get_double_declining_balance_rate(self, args, rate_field_precision)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| args | None | - | - |
| rate_field_precision | None | - | - |


##### get_written_down_value_rate(self, args, rate_field_precision, on_validate)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| args | None | - | - |
| rate_field_precision | None | - | - |
| on_validate | None | - | - |




## Functions

### has_gl_entries(doctype, docname, target_account)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| docname | None | - | - |
| target_account | None | - | - |

**Returns**: (none)



### update_maintenance_status()

**Returns**: (none)



### make_post_gl_entry()

**Returns**: (none)



### get_asset_naming_series()

**Returns**: (none)



### make_sales_invoice(asset, item_code, company, sell_qty, serial_no = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset | None | - | - |
| item_code | None | - | - |
| company | None | - | - |
| sell_qty | None | - | - |
| serial_no | None | None | - |

**Returns**: (none)



### create_asset_maintenance(asset, item_code, item_name, asset_category, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset | None | - | - |
| item_code | None | - | - |
| item_name | None | - | - |
| asset_category | None | - | - |
| company | None | - | - |

**Returns**: (none)



### create_asset_repair(company, asset, asset_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| asset | None | - | - |
| asset_name | None | - | - |

**Returns**: (none)



### create_asset_capitalization(company, asset, asset_name, item_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| asset | None | - | - |
| asset_name | None | - | - |
| item_code | None | - | - |

**Returns**: (none)



### create_asset_value_adjustment(asset, asset_category, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset | None | - | - |
| asset_category | None | - | - |
| company | None | - | - |

**Returns**: (none)



### transfer_asset(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### get_item_details(item_code, asset_category, net_purchase_amount)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| asset_category | None | - | - |
| net_purchase_amount | None | - | - |

**Returns**: (none)



### get_asset_account(account_name, asset = None, asset_category = None, company = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account_name | None | - | - |
| asset | None | None | - |
| asset_category | None | None | - |
| company | None | None | - |

**Returns**: (none)



### make_journal_entry(asset_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_name | None | - | - |

**Returns**: (none)



### make_asset_movement(assets, purpose = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| assets | None | - | - |
| purpose | None | None | - |

**Returns**: (none)



### is_cwip_accounting_enabled(asset_category)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_category | None | - | - |

**Returns**: (none)



### get_asset_value_after_depreciation(asset_name, finance_book = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_name | None | - | - |
| finance_book | None | None | - |

**Returns**: (none)



### has_active_capitalization(asset)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset | None | - | - |

**Returns**: (none)



### get_values_from_purchase_doc(purchase_doc_name, item_code, doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| purchase_doc_name | None | - | - |
| item_code | None | - | - |
| doctype | None | - | - |

**Returns**: (none)



### split_asset(asset_name, split_qty)

Split an asset into two based on the given quantity.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_name | None | - | - |
| split_qty | None | - | - |

**Returns**: (none)



### validate_split_quantity(existing_asset, split_qty)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| existing_asset | None | - | - |
| split_qty | None | - | - |

**Returns**: (none)



### create_new_asset_from_split(existing_asset, split_qty)

Create a new asset from the split quantity.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| existing_asset | None | - | - |
| split_qty | None | - | - |

**Returns**: (none)



### update_existing_asset_after_split(existing_asset, remaining_qty, splitted_asset)

Update the existing asset with the remaining quantity.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| existing_asset | None | - | - |
| remaining_qty | None | - | - |
| splitted_asset | None | - | - |

**Returns**: (none)



### process_asset_split(existing_asset, split_qty, splitted_asset = None, is_new_asset = False)

Handle asset creation or update during the split.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| existing_asset | None | - | - |
| split_qty | None | - | - |
| splitted_asset | None | None | - |
| is_new_asset | None | False | - |

**Returns**: (none)



### set_split_asset_values(asset_doc, scaling_factor, split_qty, existing_asset, is_new_asset)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_doc | None | - | - |
| scaling_factor | None | - | - |
| split_qty | None | - | - |
| existing_asset | None | - | - |
| is_new_asset | None | - | - |

**Returns**: (none)



### log_asset_activity(existing_asset, asset_doc, splitted_asset, is_new_asset)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| existing_asset | None | - | - |
| asset_doc | None | - | - |
| splitted_asset | None | - | - |
| is_new_asset | None | - | - |

**Returns**: (none)



### update_finance_books(asset_doc, existing_asset, new_asset, scaling_factor, is_new_asset)

Update finance books and depreciation schedules for the asset.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_doc | None | - | - |
| existing_asset | None | - | - |
| new_asset | None | - | - |
| scaling_factor | None | - | - |
| is_new_asset | None | - | - |

**Returns**: (none)



### reschedule_depr_for_updated_asset(existing_asset, new_asset, fb_row, scaling_factor, is_new_asset)

Reschedule depreciation for an asset after a split.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| existing_asset | None | - | - |
| new_asset | None | - | - |
| fb_row | None | - | - |
| scaling_factor | None | - | - |
| is_new_asset | None | - | - |

**Returns**: (none)



### create_new_depr_schedule(current_depr_schedule_doc, existing_asset, new_asset, is_new_asset, fb_row)

Create a new depreciation schedule based on the current one.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| current_depr_schedule_doc | None | - | - |
| existing_asset | None | - | - |
| new_asset | None | - | - |
| is_new_asset | None | - | - |
| fb_row | None | - | - |

**Returns**: (none)



### update_depreciation_terms(new_depr_schedule_doc, scaling_factor)

Update depreciation terms with scaled amounts.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| new_depr_schedule_doc | None | - | - |
| scaling_factor | None | - | - |

**Returns**: (none)



### add_depr_schedule_notes(new_depr_schedule_doc, existing_asset, new_asset, is_new_asset)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| new_depr_schedule_doc | None | - | - |
| existing_asset | None | - | - |
| new_asset | None | - | - |
| is_new_asset | None | - | - |

**Returns**: (none)



### add_reference_in_jv_on_split(entry_name, new_asset_name, old_asset_name, depreciation_amount)

Add a reference to a new asset in a journal entry after a split.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| entry_name | None | - | - |
| new_asset_name | None | - | - |
| old_asset_name | None | - | - |
| depreciation_amount | None | - | - |

**Returns**: (none)



### adjust_existing_accounts(journal_entry, old_asset_name, depreciation_amount, entries_to_add)

Adjust existing accounts and prepare new entries for the new asset.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| journal_entry | None | - | - |
| old_asset_name | None | - | - |
| depreciation_amount | None | - | - |
| entries_to_add | None | - | - |

**Returns**: (none)



### adjust_account_balance(account, depreciation_amount)

Adjust the balance of an account based on the depreciation amount.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account | None | - | - |
| depreciation_amount | None | - | - |

**Returns**: (none)



### add_new_entries(journal_entry, entries_to_add, new_asset_name, depreciation_amount)

Add new entries for the new asset to the journal entry.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| journal_entry | None | - | - |
| entries_to_add | None | - | - |
| new_asset_name | None | - | - |
| depreciation_amount | None | - | - |

**Returns**: (none)


