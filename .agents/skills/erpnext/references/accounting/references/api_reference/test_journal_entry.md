# API Reference: test_journal_entry.py

**Language**: Python

**Source**: `doctype/journal_entry/test_journal_entry.py`

---

## Classes

### TestJournalEntry

**Inherits from**: IntegrationTestCase

#### Methods

##### test_journal_entry_with_against_jv(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'unlink_payment_on_cancellation_of_invoice': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_jv_against_sales_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_jv_against_purchase_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### jv_against_voucher_testcase(self, base_jv, test_voucher)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| base_jv | None | - | - |
| test_voucher | None | - | - |


##### advance_paid_testcase(self, base_jv, test_voucher, dr_or_cr)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| base_jv | None | - | - |
| test_voucher | None | - | - |
| dr_or_cr | None | - | - |


##### cancel_against_voucher_testcase(self, test_voucher)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| test_voucher | None | - | - |


##### test_jv_against_stock_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_multi_currency(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reverse_journal_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_disallow_change_in_account_currency_for_a_party(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_inter_company_jv(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_jv_with_cost_centre(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_jv_with_project(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_jv_account_and_party_balance_with_cost_centre(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_repost_accounting_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_gl_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_negative_debit_and_credit_with_same_account_head(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_toggle_debit_credit_if_negative(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_transaction_exchange_rate_on_journals(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_pay_to_recd_from(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_credit_limit_for_customer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### make_journal_entry(account1, account2, amount, cost_center = None, posting_date = None, exchange_rate = 1, save = True, submit = False, project = None, company = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account1 | None | - | - |
| account2 | None | - | - |
| amount | None | - | - |
| cost_center | None | None | - |
| posting_date | None | None | - |
| exchange_rate | None | 1 | - |
| save | None | True | - |
| submit | None | False | - |
| project | None | None | - |
| company | None | None | - |

**Returns**: (none)


