# API Reference: taxes_setup.py

**Language**: Python

**Source**: `setup_wizard/operations/taxes_setup.py`

---

## Functions

### setup_taxes_and_charges(company_name: str, country: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company_name | str | - | - |
| country | str | - | - |

**Returns**: (none)



### simple_to_detailed(templates)

Convert a simple taxes object into a more detailed data structure.

Example input:

{
        "France VAT 20%": {
                "account_name": "VAT 20%",
                "tax_rate": 20,
                "default": 1
        },
        "France VAT 10%": {
                "account_name": "VAT 10%",
                "tax_rate": 10
        }
}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| templates | None | - | - |

**Returns**: (none)



### from_detailed_data(company_name, data)

Create Taxes and Charges Templates from detailed data.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company_name | None | - | - |
| data | None | - | - |

**Returns**: (none)



### update_regional_tax_settings(country, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| country | None | - | - |
| company | None | - | - |

**Returns**: (none)



### make_taxes_and_charges_template(company_name, doctype, template)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company_name | None | - | - |
| doctype | None | - | - |
| template | None | - | - |

**Returns**: (none)



### make_item_tax_template(company_name, template)

Create an Item Tax Template.

This requires a separate method because Item Tax Template is structured
differently from Sales and Purchase Tax Templates.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company_name | None | - | - |
| template | None | - | - |

**Returns**: (none)



### get_or_create_account(company_name, account)

Check if account already exists. If not, create it.
Return a tax account or None.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company_name | None | - | - |
| account | None | - | - |

**Returns**: (none)



### get_or_create_tax_group(company_name, root_type)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company_name | None | - | - |
| root_type | None | - | - |

**Returns**: (none)



### make_tax_category(tax_category)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| tax_category | None | - | - |

**Returns**: (none)


