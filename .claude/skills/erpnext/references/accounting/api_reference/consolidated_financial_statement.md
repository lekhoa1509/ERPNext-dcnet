# API Reference: consolidated_financial_statement.py

**Language**: Python

**Source**: `report/consolidated_financial_statement/consolidated_financial_statement.py`

---

## Functions

### execute(filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |

**Returns**: (none)



### get_balance_sheet_data(fiscal_year, companies, columns, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fiscal_year | None | - | - |
| companies | None | - | - |
| columns | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### prepare_companywise_opening_balance(asset_data, liability_data, equity_data, companies)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_data | None | - | - |
| liability_data | None | - | - |
| equity_data | None | - | - |
| companies | None | - | - |

**Returns**: (none)



### get_opening_balance(account_name, data, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account_name | None | - | - |
| data | None | - | - |
| company | None | - | - |

**Returns**: (none)



### get_root_account_name(root_type, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| root_type | None | - | - |
| company | None | - | - |

**Returns**: (none)



### get_profit_loss_data(fiscal_year, companies, columns, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fiscal_year | None | - | - |
| companies | None | - | - |
| columns | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_income_expense_data(companies, fiscal_year, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| companies | None | - | - |
| fiscal_year | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_cash_flow_data(fiscal_year, companies, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fiscal_year | None | - | - |
| companies | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_account_type_based_data(account_type, companies, fiscal_year, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account_type | None | - | - |
| companies | None | - | - |
| fiscal_year | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_columns(companies, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| companies | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_data(companies, root_type, balance_must_be, fiscal_year, filters = None, ignore_closing_entries = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| companies | None | - | - |
| root_type | None | - | - |
| balance_must_be | None | - | - |
| fiscal_year | None | - | - |
| filters | None | None | - |
| ignore_closing_entries | None | False | - |

**Returns**: (none)



### get_company_currency(filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |

**Returns**: (none)



### calculate_values(accounts_by_name, gl_entries_by_account, companies, filters, fiscal_year)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| accounts_by_name | None | - | - |
| gl_entries_by_account | None | - | - |
| companies | None | - | - |
| filters | None | - | - |
| fiscal_year | None | - | - |

**Returns**: (none)



### accumulate_values_into_parents(accounts, accounts_by_name, companies)

accumulate children's values in parent accounts

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| accounts | None | - | - |
| accounts_by_name | None | - | - |
| companies | None | - | - |

**Returns**: (none)



### get_account_heads(root_type, companies, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| root_type | None | - | - |
| companies | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### update_parent_account_names(accounts)

Update parent_account_name in accounts list.

parent_name is `name` of parent account which could have other prefix
of account_number and suffix of company abbr. This function adds key called
`parent_account_name` which does not have such prefix/suffix.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| accounts | None | - | - |

**Returns**: (none)



### get_companies(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### get_subsidiary_companies(company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |

**Returns**: (none)



### get_accounts(root_type, companies)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| root_type | None | - | - |
| companies | None | - | - |

**Returns**: (none)



### prepare_data(accounts, start_date, end_date, balance_must_be, companies, company_currency, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| accounts | None | - | - |
| start_date | None | - | - |
| end_date | None | - | - |
| balance_must_be | None | - | - |
| companies | None | - | - |
| company_currency | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### set_gl_entries_by_account(from_date, to_date, root_lft, root_rgt, filters, gl_entries_by_account, accounts_by_name, accounts, ignore_closing_entries = False, root_type = None)

Returns a dict like { "account": [gl entries], ... }

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| from_date | None | - | - |
| to_date | None | - | - |
| root_lft | None | - | - |
| root_rgt | None | - | - |
| filters | None | - | - |
| gl_entries_by_account | None | - | - |
| accounts_by_name | None | - | - |
| accounts | None | - | - |
| ignore_closing_entries | None | False | - |
| root_type | None | None | - |

**Returns**: (none)



### get_account_details(account)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account | None | - | - |

**Returns**: (none)



### validate_entries(key, entry, accounts_by_name, accounts)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | None | - | - |
| entry | None | - | - |
| accounts_by_name | None | - | - |
| accounts | None | - | - |

**Returns**: (none)



### get_additional_conditions(from_date, ignore_closing_entries, filters, d)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| from_date | None | - | - |
| ignore_closing_entries | None | - | - |
| filters | None | - | - |
| d | None | - | - |

**Returns**: (none)



### add_total_row(out, root_type, balance_must_be, companies, company_currency)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| out | None | - | - |
| root_type | None | - | - |
| balance_must_be | None | - | - |
| companies | None | - | - |
| company_currency | None | - | - |

**Returns**: (none)



### filter_accounts(accounts, depth = 10)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| accounts | None | - | - |
| depth | None | 10 | - |

**Returns**: (none)



### add_to_list(parent, level)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| parent | None | - | - |
| level | None | - | - |

**Returns**: (none)


