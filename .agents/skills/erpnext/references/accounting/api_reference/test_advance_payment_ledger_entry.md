# API Reference: test_advance_payment_ledger_entry.py

**Language**: Python

**Source**: `doctype/advance_payment_ledger_entry/test_advance_payment_ledger_entry.py`

---

## Classes

### TestAdvancePaymentLedgerEntry

Integration tests for AdvancePaymentLedgerEntry.
Use this class for testing interactions between multiple components.

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


##### create_sales_order(self, qty = 1, rate = 100, currency = 'INR', do_not_submit = False)

Helper method

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| qty | None | 1 | - |
| rate | None | 100 | - |
| currency | None | 'INR' | - |
| do_not_submit | None | False | - |


##### create_purchase_order(self, qty = 1, rate = 100, currency = 'INR', do_not_submit = False)

Helper method

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| qty | None | 1 | - |
| rate | None | 100 | - |
| currency | None | 'INR' | - |
| do_not_submit | None | False | - |


##### test_so_advance_paid_and_currency_with_payment(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_so_advance_paid_and_currency_with_journal(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_po_advance_paid_and_currency_with_payment(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_po_advance_paid_and_currency_with_journal(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



