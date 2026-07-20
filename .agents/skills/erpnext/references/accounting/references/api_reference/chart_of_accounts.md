# API Reference: chart_of_accounts.py

**Language**: Python

**Source**: `doctype/account/chart_of_accounts/chart_of_accounts.py`

---

## Functions

### create_charts(company, chart_template = None, existing_company = None, custom_chart = None, from_coa_importer = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| chart_template | None | None | - |
| existing_company | None | None | - |
| custom_chart | None | None | - |
| from_coa_importer | None | None | - |

**Returns**: (none)



### add_suffix_if_duplicate(account_name, account_number, accounts)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account_name | None | - | - |
| account_number | None | - | - |
| accounts | None | - | - |

**Returns**: (none)



### identify_is_group(child)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| child | None | - | - |

**Returns**: (none)



### get_chart(chart_template, existing_company = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| chart_template | None | - | - |
| existing_company | None | None | - |

**Returns**: (none)



### get_charts_for_country(country, with_standard = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| country | None | - | - |
| with_standard | None | False | - |

**Returns**: (none)



### get_account_tree_from_existing_company(existing_company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| existing_company | None | - | - |

**Returns**: (none)



### build_account_tree(tree, parent, all_accounts)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| tree | None | - | - |
| parent | None | - | - |
| all_accounts | None | - | - |

**Returns**: (none)



### validate_bank_account(coa, bank_account)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| coa | None | - | - |
| bank_account | None | - | - |

**Returns**: (none)



### build_tree_from_json(chart_template, chart_data = None, from_coa_importer = False)

get chart template from its folder and parse the json to be rendered as tree

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| chart_template | None | - | - |
| chart_data | None | None | - |
| from_coa_importer | None | False | - |

**Returns**: (none)



### get_chart_metadata_fields()

**Returns**: (none)



### _get_chart_name(content)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| content | None | - | - |

**Returns**: (none)



### _import_accounts(children, parent)

recursively called to form a parent-child based list of dict from chart template

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| children | None | - | - |
| parent | None | - | - |

**Returns**: (none)



### _import_accounts(children, parent, root_type, root_account = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| children | None | - | - |
| parent | None | - | - |
| root_type | None | - | - |
| root_account | None | False | - |

**Returns**: (none)



### _get_account_names(account_master)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account_master | None | - | - |

**Returns**: (none)


