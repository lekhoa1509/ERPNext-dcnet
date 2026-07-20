# API Reference: test_repost_item_valuation.py

**Language**: Python

**Source**: `doctype/repost_item_valuation/test_repost_item_valuation.py`

---

## Classes

### TestRepostItemValuation

**Inherits from**: IntegrationTestCase, StockTestMixin

#### Methods

##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_repost_time_slot(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_clear_old_logs(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_create_item_wise_repost_item_valuation_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_deduplication(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_stock_freeze_validation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_prevention_of_cancelled_transaction_riv(self)

**Decorators**: `@IntegrationTestCase.change_settings('Stock Reposting Settings', {'item_based_reposting': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_queue_progress_serialization(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_gl_repost_progress(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_gl_complete_gl_reposting(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_duplicate_ple_on_repost(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_account_freeze_validation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_create_repost_entry_for_cancelled_document(self)

**Decorators**: `@IntegrationTestCase.change_settings('Stock Reposting Settings', {'item_based_reposting': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_repost_item_valuation_for_closing_stock_balance(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_remove_attached_file(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### _assert_status(doc, status)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| status | None | - | - |

**Returns**: (none)


