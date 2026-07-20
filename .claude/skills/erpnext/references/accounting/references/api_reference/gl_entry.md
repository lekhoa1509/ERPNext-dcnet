# API Reference: gl_entry.py

**Language**: Python

**Source**: `doctype/gl_entry/gl_entry.py`

---

## Classes

### GLEntry

**Inherits from**: Document

#### Methods

##### autoname(self)

Temporarily name doc for fast insertion
name will be changed using autoname options (in a scheduled job)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_mandatory(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### pl_must_have_cost_center(self)

Validate that profit and loss type account GL entries have a cost center.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_dimensions_for_pl_and_bs(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_pl_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_account_details(self, adv_adj)

Account must be ledger, active and not freezed

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| adv_adj | None | - | - |


##### validate_cost_center(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_party(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_currency(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_amount_in_reporting_currency(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_and_set_fiscal_year(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### validate_balance_type(account, adv_adj = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account | None | - | - |
| adv_adj | None | False | - |

**Returns**: (none)



### update_outstanding_amt(account, party_type, party, against_voucher_type, against_voucher, on_cancel = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account | None | - | - |
| party_type | None | - | - |
| party | None | - | - |
| against_voucher_type | None | - | - |
| against_voucher | None | - | - |
| on_cancel | None | False | - |

**Returns**: (none)



### validate_frozen_account(company, account, adv_adj = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| account | None | - | - |
| adv_adj | None | None | - |

**Returns**: (none)



### update_against_account(voucher_type, voucher_no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_type | None | - | - |
| voucher_no | None | - | - |

**Returns**: (none)



### on_doctype_update()

**Returns**: (none)



### rename_gle_sle_docs()

**Returns**: (none)



### rename_temporarily_named_docs(doctype)

Rename temporarily named docs using autoname options

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)


