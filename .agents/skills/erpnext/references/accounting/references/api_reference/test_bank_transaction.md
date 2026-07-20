# API Reference: test_bank_transaction.py

**Language**: Python

**Source**: `doctype/bank_transaction/test_bank_transaction.py`

---

## Classes

### TestBankTransaction

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_linked_payments(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reconcile(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cancel_voucher(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_debit_credit_output(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_already_reconciled(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_clear_sales_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_matching_loan_repayment(self)

**Decorators**: `@if_lending_app_installed`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_bank_account(bank_name = 'Citi Bank', gl_account = '_Test Bank - _TC', bank_account_name = 'Checking Account')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bank_name | None | 'Citi Bank' | - |
| gl_account | None | '_Test Bank - _TC' | - |
| bank_account_name | None | 'Checking Account' | - |

**Returns**: (none)



### create_gl_account(gl_account_name = '_Test Bank - _TC')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| gl_account_name | None | '_Test Bank - _TC' | - |

**Returns**: (none)



### add_transactions(bank_account = '_Test Bank - _TC')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bank_account | None | '_Test Bank - _TC' | - |

**Returns**: (none)



### add_vouchers(gl_account = '_Test Bank - _TC')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| gl_account | None | '_Test Bank - _TC' | - |

**Returns**: (none)



### create_loan_and_repayment()

**Returns**: (none)


