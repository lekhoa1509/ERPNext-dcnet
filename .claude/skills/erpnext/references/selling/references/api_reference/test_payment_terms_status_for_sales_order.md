# API Reference: test_payment_terms_status_for_sales_order.py

**Language**: Python

**Source**: `report/payment_terms_status_for_sales_order/test_payment_terms_status_for_sales_order.py`

---

## Classes

### TestPaymentTermsStatusForSalesOrder

**Inherits from**: IntegrationTestCase

#### Methods

##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_payment_terms_template(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_01_payment_terms_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_exchange_rate(self, date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| date | None | - | - |


##### test_02_alternate_currency(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', allow_multi_currency_invoices_against_single_party_account=1)`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_03_group_filters(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_04_due_date_filter(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



