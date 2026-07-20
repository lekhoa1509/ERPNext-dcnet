# API Reference: test_process_statement_of_accounts.py

**Language**: Python

**Source**: `doctype/process_statement_of_accounts/test_process_statement_of_accounts.py`

---

## Classes

### TestProcessStatementOfAccounts

**Inherits from**: AccountsTestMixin, IntegrationTestCase

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_process_soa_for_gl(self)

Tests the utils for Statement of Accounts(General Ledger)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_process_soa_for_ar(self)

Tests the utils for Statement of Accounts(Accounts Receivable)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auto_email_for_process_soa_ar(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_ageing_summary(self, ageing, expected_ageing)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| ageing | None | - | - |
| expected_ageing | None | - | - |


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_process_soa()

**Returns**: (none)


