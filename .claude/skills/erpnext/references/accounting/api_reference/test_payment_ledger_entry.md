# API Reference: test_payment_ledger_entry.py

**Language**: Python

**Source**: `doctype/payment_ledger_entry/test_payment_ledger_entry.py`

---

## Classes

### TestPaymentLedgerEntry

**Inherits from**: IntegrationTestCase

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


##### create_company(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_customer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_sales_invoice(self, qty = 1, rate = 100, posting_date = None, do_not_save = False, do_not_submit = False)

Helper function to populate default values in sales invoice

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| qty | None | 1 | - |
| rate | None | 100 | - |
| posting_date | None | None | - |
| do_not_save | None | False | - |
| do_not_submit | None | False | - |


##### create_payment_entry(self, amount = 100, posting_date = None)

Helper function to populate default values in payment entry

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| amount | None | 100 | - |
| posting_date | None | None | - |


##### create_sales_order(self, qty = 1, rate = 100, posting_date = None, do_not_save = False, do_not_submit = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| qty | None | 1 | - |
| rate | None | 100 | - |
| posting_date | None | None | - |
| do_not_save | None | False | - |
| do_not_submit | None | False | - |


##### clear_old_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_journal_entry(self, acc1 = None, acc2 = None, amount = 0, posting_date = None, cost_center = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| acc1 | None | None | - |
| acc2 | None | None | - |
| amount | None | 0 | - |
| posting_date | None | None | - |
| cost_center | None | None | - |


##### test_payment_against_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_partial_payment_against_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cr_note_against_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_je_against_inv_and_note(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_multi_payment_unlink_on_invoice_cancellation(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'unlink_payment_on_cancellation_of_invoice': 1, 'delete_linked_ledger_entries': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_multi_je_unlink_on_invoice_cancellation(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'unlink_payment_on_cancellation_of_invoice': 1, 'delete_linked_ledger_entries': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_advance_payment_unlink_on_order_cancellation(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'unlink_payment_on_cancellation_of_invoice': 1, 'delete_linked_ledger_entries': 1, 'unlink_advance_payment_on_cancelation_of_order': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



