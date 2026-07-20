# API Reference: test_exchange_rate_revaluation.py

**Language**: Python

**Source**: `doctype/exchange_rate_revaluation/test_exchange_rate_revaluation.py`

---

## Classes

### TestExchangeRateRevaluation

**Inherits from**: AccountsTestMixin, IntegrationTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_system_and_company_settings(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_01_revaluation_of_forex_balance(self)

Test Forex account balance and Journal creation post Revaluation

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'allow_multi_currency_invoices_against_single_party_account': 1, 'allow_stale': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_02_accounts_only_with_base_currency_balance(self)

Test Revaluation on Forex account with balance only in base currency

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'allow_multi_currency_invoices_against_single_party_account': 1, 'allow_stale': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_03_accounts_only_with_account_currency_balance(self)

Test Revaluation on Forex account with balance only in account currency

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'allow_multi_currency_invoices_against_single_party_account': 1, 'allow_stale': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_04_get_account_details_function(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'allow_multi_currency_invoices_against_single_party_account': 1, 'allow_stale': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



