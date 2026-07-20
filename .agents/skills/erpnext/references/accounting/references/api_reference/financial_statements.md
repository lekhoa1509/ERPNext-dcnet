# API Reference: financial_statements.py

**Language**: Python

**Source**: `report/financial_statements.py`

---

## Functions

### get_period_list(from_fiscal_year, to_fiscal_year, period_start_date, period_end_date, filter_based_on, periodicity, accumulated_values = False, company = None, reset_period_on_fy_change = True, ignore_fiscal_year = False)

Get a list of dict {"from_date": from_date, "to_date": to_date, "key": key, "label": label}
Periodicity can be (Yearly, Quarterly, Monthly)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| from_fiscal_year | None | - | - |
| to_fiscal_year | None | - | - |
| period_start_date | None | - | - |
| period_end_date | None | - | - |
| filter_based_on | None | - | - |
| periodicity | None | - | - |
| accumulated_values | None | False | - |
| company | None | None | - |
| reset_period_on_fy_change | None | True | - |
| ignore_fiscal_year | None | False | - |

**Returns**: (none)



### get_fiscal_year_data(from_fiscal_year, to_fiscal_year)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| from_fiscal_year | None | - | - |
| to_fiscal_year | None | - | - |

**Returns**: (none)



### validate_fiscal_year(fiscal_year, from_fiscal_year, to_fiscal_year)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fiscal_year | None | - | - |
| from_fiscal_year | None | - | - |
| to_fiscal_year | None | - | - |

**Returns**: (none)



### validate_dates(from_date, to_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| from_date | None | - | - |
| to_date | None | - | - |

**Returns**: (none)



### get_months(start_date, end_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| start_date | None | - | - |
| end_date | None | - | - |

**Returns**: (none)



### get_label(periodicity, from_date, to_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| periodicity | None | - | - |
| from_date | None | - | - |
| to_date | None | - | - |

**Returns**: (none)



### get_data(company, root_type, balance_must_be, period_list, filters = None, accumulated_values = 1, only_current_fiscal_year = True, ignore_closing_entries = False, ignore_accumulated_values_for_fy = False, total = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| root_type | None | - | - |
| balance_must_be | None | - | - |
| period_list | None | - | - |
| filters | None | None | - |
| accumulated_values | None | 1 | - |
| only_current_fiscal_year | None | True | - |
| ignore_closing_entries | None | False | - |
| ignore_accumulated_values_for_fy | None | False | - |
| total | None | True | - |

**Returns**: (none)



### get_appropriate_currency(company, filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| filters | None | None | - |

**Returns**: (none)



### calculate_values(accounts_by_name, gl_entries_by_account, period_list, accumulated_values, ignore_accumulated_values_for_fy)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| accounts_by_name | None | - | - |
| gl_entries_by_account | None | - | - |
| period_list | None | - | - |
| accumulated_values | None | - | - |
| ignore_accumulated_values_for_fy | None | - | - |

**Returns**: (none)



### accumulate_values_into_parents(accounts, accounts_by_name, period_list)

accumulate children's values in parent accounts

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| accounts | None | - | - |
| accounts_by_name | None | - | - |
| period_list | None | - | - |

**Returns**: (none)



### prepare_data(accounts, balance_must_be, period_list, company_currency, accumulated_values)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| accounts | None | - | - |
| balance_must_be | None | - | - |
| period_list | None | - | - |
| company_currency | None | - | - |
| accumulated_values | None | - | - |

**Returns**: (none)



### filter_out_zero_value_rows(data, parent_children_map, show_zero_values = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| parent_children_map | None | - | - |
| show_zero_values | None | False | - |

**Returns**: (none)



### add_total_row(out, root_type, balance_must_be, period_list, company_currency)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| out | None | - | - |
| root_type | None | - | - |
| balance_must_be | None | - | - |
| period_list | None | - | - |
| company_currency | None | - | - |

**Returns**: (none)



### get_accounts(company, root_type)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| root_type | None | - | - |

**Returns**: (none)



### filter_accounts(accounts, depth = 20)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| accounts | None | - | - |
| depth | None | 20 | - |

**Returns**: (none)



### sort_accounts(accounts, is_root = False, key = 'name')

Sort root types as Asset, Liability, Equity, Income, Expense

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| accounts | None | - | - |
| is_root | None | False | - |
| key | None | 'name' | - |

**Returns**: (none)



### set_gl_entries_by_account(company, from_date, to_date, filters, gl_entries_by_account, root_lft = None, root_rgt = None, root_type = None, ignore_closing_entries = False, ignore_opening_entries = False, group_by_account = False, ignore_reporting_currency = True)

Returns a dict like { "account": [gl entries], ... }

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| from_date | None | - | - |
| to_date | None | - | - |
| filters | None | - | - |
| gl_entries_by_account | None | - | - |
| root_lft | None | None | - |
| root_rgt | None | None | - |
| root_type | None | None | - |
| ignore_closing_entries | None | False | - |
| ignore_opening_entries | None | False | - |
| group_by_account | None | False | - |
| ignore_reporting_currency | None | True | - |

**Returns**: (none)



### get_accounting_entries(doctype, from_date, to_date, filters, root_lft = None, root_rgt = None, root_type = None, ignore_closing_entries = None, period_closing_voucher = None, ignore_opening_entries = False, group_by_account = False, ignore_reporting_currency = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| from_date | None | - | - |
| to_date | None | - | - |
| filters | None | - | - |
| root_lft | None | None | - |
| root_rgt | None | None | - |
| root_type | None | None | - |
| ignore_closing_entries | None | None | - |
| period_closing_voucher | None | None | - |
| ignore_opening_entries | None | False | - |
| group_by_account | None | False | - |
| ignore_reporting_currency | None | True | - |

**Returns**: (none)



### get_account_filter_query(root_lft, root_rgt, root_type, gl_entry)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| root_lft | None | - | - |
| root_rgt | None | - | - |
| root_type | None | - | - |
| gl_entry | None | - | - |

**Returns**: (none)



### apply_additional_conditions(doctype, query, from_date, ignore_closing_entries, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| query | None | - | - |
| from_date | None | - | - |
| ignore_closing_entries | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_cost_centers_with_children(cost_centers)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cost_centers | None | - | - |

**Returns**: (none)



### get_columns(periodicity, period_list, accumulated_values = 1, company = None, cash_flow = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| periodicity | None | - | - |
| period_list | None | - | - |
| accumulated_values | None | 1 | - |
| company | None | None | - |
| cash_flow | None | False | - |

**Returns**: (none)



### get_filtered_list_for_consolidated_report(filters, period_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| period_list | None | - | - |

**Returns**: (none)



### compute_growth_view_data(data, columns)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| columns | None | - | - |

**Returns**: (none)



### compute_margin_view_data(data, columns, accumulated_values)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| columns | None | - | - |
| accumulated_values | None | - | - |

**Returns**: (none)



### get_all_parents(account, parent_children_map)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account | None | - | - |
| parent_children_map | None | - | - |

**Returns**: (none)



### add_to_list(parent, level)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| parent | None | - | - |
| level | None | - | - |

**Returns**: (none)



### compare_accounts(a, b)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| a | None | - | - |
| b | None | - | - |

**Returns**: (none)


