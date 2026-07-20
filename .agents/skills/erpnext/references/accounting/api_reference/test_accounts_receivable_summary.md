# API Reference: test_accounts_receivable_summary.py

**Language**: Python

**Source**: `report/accounts_receivable_summary/test_accounts_receivable_summary.py`

---

## Classes

### TestAccountsReceivable

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


##### test_01_receivable_summary_output(self)

Test for Invoices, Paid, Advance and Outstanding

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_02_various_filters_and_output(self)

**Decorators**: `@IntegrationTestCase.change_settings('Selling Settings', {'cust_master_name': 'Naming Series'})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



