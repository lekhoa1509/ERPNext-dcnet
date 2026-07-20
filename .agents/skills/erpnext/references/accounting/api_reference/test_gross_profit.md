# API Reference: test_gross_profit.py

**Language**: Python

**Source**: `report/gross_profit/test_gross_profit.py`

---

## Classes

### TestGrossProfit

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


##### create_bundle(self)

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


##### create_delivery_note(self, item = None, qty = 1, rate = 100, posting_date = None, do_not_save = False, do_not_submit = False)

Helper function to populate default values in Delivery Note

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item | None | None | - |
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


##### test_invoice_without_only_delivery_note(self)

Test buying amount for Invoice without `update_stock` flag set but has Delivery Note

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bundled_delivery_note_with_different_warehouses(self)

Test Delivery Note with bundled item. Packed Item from the bundle having different warehouses

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_order_connected_dn_and_inv(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_crnote_against_invoice_with_multiple_instances_of_same_item(self)

Item Qty for Sales Invoices with multiple instances of same item go in the -ve. Ideally, the credit noteshould cancel out the invoice items.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_standalone_cr_notes(self)

Standalone cr notes will be reported as usual

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_different_rates_in_si_and_dn(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_valuation_rate_without_previous_sle(self)

Test Valuation rate calculation when stock ledger is empty and invoices are against different warehouses

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_gross_profit_groupby_invoices(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_profit_for_later_period_return(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



