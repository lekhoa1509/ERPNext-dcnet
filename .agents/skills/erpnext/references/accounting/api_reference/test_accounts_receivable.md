# API Reference: test_accounts_receivable.py

**Language**: Python

**Source**: `report/accounts_receivable/test_accounts_receivable.py`

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


##### create_sales_invoice(self, no_payment_schedule = False, do_not_submit = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| no_payment_schedule | None | False | - |
| do_not_submit | None | False | - |


##### create_payment_entry(self, docname, do_not_submit = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| docname | None | - | - |
| do_not_submit | None | False | - |


##### create_credit_note(self, docname, do_not_submit = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| docname | None | - | - |
| do_not_submit | None | False | - |


##### test_pos_receivable(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_accounts_receivable_with_payment(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_accounts_receivable_without_payment(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_allow_multi_currency_invoices_against_single_party_account(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'allow_multi_currency_invoices_against_single_party_account': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_accounts_receivable_with_partial_payment(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cr_note_flag_to_update_self(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_againt_po_in_receivable_report(self)

Payments made against Purchase Order will show up as outstanding amount

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_exchange_revaluation_for_party(self)

Exchange Revaluation for party on Receivable/Payable should be included

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'allow_multi_currency_invoices_against_single_party_account': 1, 'allow_stale': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_against_credit_note(self)

Payment against credit/debit note should be considered against the parent invoice

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_group_by_party(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_future_payments(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_person(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cost_center_filter(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_customer_group_filter(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_multi_customer_group_filter(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_party_account_filter(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_usd_customer_filter(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_multi_select_party_filter(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_report_output_if_party_is_missing(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_future_payments_on_foreign_currency(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_accounts_receivable_output_for_minor_outstanding(self)

AR/AP should report miniscule outstanding of 0.01. Or else there will be slight difference with General Ledger/Trial Balance

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cost_center_on_report_output(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



