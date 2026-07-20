# API Reference: tax_rule.py

**Language**: Python

**Source**: `doctype/tax_rule/tax_rule.py`

---

## Classes

### IncorrectCustomerGroup

**Inherits from**: frappe.ValidationError



### IncorrectSupplierType

**Inherits from**: frappe.ValidationError



### ConflictingTaxRule

**Inherits from**: frappe.ValidationError



### TaxRule

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_tax_template(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_filters(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_party_details(party, party_type, args = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| party | None | - | - |
| party_type | None | - | - |
| args | None | None | - |

**Returns**: (none)



### get_tax_template(posting_date, args)

Get matching tax rule

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| posting_date | None | - | - |
| args | None | - | - |

**Returns**: (none)



### get_customer_group_condition(customer_group)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| customer_group | None | - | - |

**Returns**: (none)



### cmp(a, b)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| a | None | - | - |
| b | None | - | - |

**Returns**: (none)


