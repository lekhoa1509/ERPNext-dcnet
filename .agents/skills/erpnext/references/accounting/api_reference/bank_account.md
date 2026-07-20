# API Reference: bank_account.py

**Language**: Python

**Source**: `doctype/bank_account/bank_account.py`

---

## Classes

### BankAccount

**Inherits from**: Document

#### Methods

##### onload(self)

Load address and contacts in `__onload`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### autoname(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_is_company_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_default_bank_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_party_bank_account(party_type, party)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| party_type | None | - | - |
| party | None | - | - |

**Returns**: (none)



### get_default_company_bank_account(company, party_type, party)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| party_type | None | - | - |
| party | None | - | - |

**Returns**: (none)



### get_bank_account_details(bank_account)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bank_account | None | - | - |

**Returns**: (none)


