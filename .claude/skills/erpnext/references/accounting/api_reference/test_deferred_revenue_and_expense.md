# API Reference: test_deferred_revenue_and_expense.py

**Language**: Python

**Source**: `report/deferred_revenue_and_expense/test_deferred_revenue_and_expense.py`

---

## Classes

### TestDeferredRevenueAndExpense

**Inherits from**: IntegrationTestCase, AccountsTestMixin

#### Methods

##### clear_old_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### setup_deferred_accounts_and_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


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


##### test_deferred_revenue(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'book_deferred_entries_based_on': 'Months'})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_deferred_expense(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'book_deferred_entries_based_on': 'Months'})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_zero_months(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'book_deferred_entries_based_on': 'Months'})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_zero_amount(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'book_deferred_entries_based_on': 'Months', 'book_deferred_entries_via_journal_entry': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



