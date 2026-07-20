# API Reference: share_transfer.py

**Language**: Python

**Source**: `doctype/share_transfer/share_transfer.py`

---

## Classes

### ShareDontExists

**Inherits from**: ValidationError



### ShareTransfer

**Inherits from**: Document

#### Methods

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


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### basic_validations(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### share_exists(self, shareholder)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| shareholder | None | - | - |


##### folio_no_validation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### autoname_folio(self, shareholder, is_company = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| shareholder | None | - | - |
| is_company | None | False | - |


##### remove_shares(self, shareholder)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| shareholder | None | - | - |


##### return_share_balance_entry(self, from_no, to_no, rate)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| from_no | None | - | - |
| to_no | None | - | - |
| rate | None | - | - |


##### get_shareholder_doc(self, shareholder)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| shareholder | None | - | - |


##### get_company_shareholder(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### make_jv_entry(company, account, amount, payment_account, credit_applicant_type, credit_applicant, debit_applicant_type, debit_applicant)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| account | None | - | - |
| amount | None | - | - |
| payment_account | None | - | - |
| credit_applicant_type | None | - | - |
| credit_applicant | None | - | - |
| debit_applicant_type | None | - | - |
| debit_applicant | None | - | - |

**Returns**: (none)


