# API Reference: tax_withholding_category.py

**Language**: Python

**Source**: `doctype/tax_withholding_category/tax_withholding_category.py`

---

## Classes

### TaxWithholdingCategory

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_dates(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_companies_and_accounts(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_thresholds(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_applicable_tax_row(self, posting_date, tax_withholding_group)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| posting_date | None | - | - |
| tax_withholding_group | None | - | - |


##### get_company_account(self, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| company | None | - | - |




### TaxWithholdingDetails

**Inherits from**: (none)

#### Methods

##### __init__(self, tax_withholding_categories: list[str], tax_withholding_group: str, posting_date: str, party_type: str, party: str, company: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| tax_withholding_categories | list[str] | - | - |
| tax_withholding_group | str | - | - |
| posting_date | str | - | - |
| party_type | str | - | - |
| party | str | - | - |
| company | str | - | - |


##### get(self) → list

Fetches tax withholding categories based on the provided parameters.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `list`


##### get_ldc_details(self)

Fetches the Lower Deduction Certificate (LDC) details for the given party.
Assumes that only one LDC per category can be valid at a time.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_valid_ldc_records(self, tax_id)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| tax_id | None | - | - |


##### get_ldc_utilization_by_category(self, ldc_names, tax_id)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| ldc_names | None | - | - |
| tax_id | None | - | - |




## Functions

### get_tax_id_for_party(party_type, party)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| party_type | None | - | - |
| party | None | - | - |

**Returns**: (none)


