# API Reference: company.py

**Language**: Python

**Source**: `doctype/company/company.py`

---

## Classes

### Company

**Inherits from**: NestedSet

#### Methods

##### onload(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_if_transactions_exist(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### cant_change_valuation_method(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_inventory_account_settings(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_abbr(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_default_tax_template(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_default_accounts(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_advance_account_currency(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_currency(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_default_warehouses(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_default_accounts(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_default_departments(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_coa_input(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_perpetual_inventory(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_provisional_account_for_non_stock_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_country_change(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_chart_of_accounts(self)

If parent company is set, chart of accounts will be based on that company

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_parent_company(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_reporting_currency(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_pending_reposts(self, old_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| old_doc | None | - | - |


##### set_default_accounts(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _set_default_account(self, fieldname, account_type)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | None | - | - |
| account_type | None | - | - |


##### set_mode_of_payment_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_default_cost_center(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### after_rename(self, olddn, newdn, merge = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| olddn | None | - | - |
| newdn | None | - | - |
| merge | None | False | - |


##### abbreviate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

Trash accounts and cost centers for this company if no gl entry exists

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_parent_changed(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_name_with_abbr(name, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |
| company | None | - | - |

**Returns**: (none)



### install_country_fixtures(company, country)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| country | None | - | - |

**Returns**: (none)



### update_company_current_month_sales(company)

Update Company's Total Monthly Sales.

Postgres compatibility:
- Avoid MariaDB-only DATE_FORMAT().
- Use a date range for the current month instead (portable + index-friendly).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |

**Returns**: (none)



### update_company_monthly_sales(company)

Cache past year monthly sales of every company based on sales invoices

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |

**Returns**: (none)



### update_transactions_annual_history(company, commit = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| commit | None | False | - |

**Returns**: (none)



### cache_companies_monthly_sales_history()

**Returns**: (none)



### get_children(doctype, parent = None, company = None, is_root = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| parent | None | None | - |
| company | None | None | - |
| is_root | None | False | - |

**Returns**: (none)



### add_node()

**Returns**: (none)



### get_all_transactions_annual_history(company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |

**Returns**: (none)



### get_timeline_data(doctype, name)

returns timeline data based on linked records in dashboard

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |

**Returns**: (none)



### get_default_company_address(name, sort_key = 'is_primary_address', existing_address = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |
| sort_key | None | 'is_primary_address' | - |
| existing_address | None | None | - |

**Returns**: (none)



### get_billing_shipping_address(name, billing_address = None, shipping_address = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |
| billing_address | None | None | - |
| shipping_address | None | None | - |

**Returns**: (none)



### create_transaction_deletion_request(company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |

**Returns**: (none)


