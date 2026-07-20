# API Reference: test_pos_invoice_merge_log.py

**Language**: Python

**Source**: `doctype/pos_invoice_merge_log/test_pos_invoice_merge_log.py`

---

## Classes

### TestPOSInvoiceMergeLog

**Inherits from**: IntegrationTestCase

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


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


##### test_consolidated_invoice_creation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_consolidated_credit_note_creation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_consolidated_invoice_item_taxes(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_consolidation_round_off_error_1(self)

Test round off error in consolidated invoice creation if POS Invoice has inclusive tax

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_consolidation_round_off_error_2(self)

Test the same case as above but with an Unpaid POS Invoice

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_consolidation_round_off_error_3(self)

**Decorators**: `@IntegrationTestCase.change_settings('System Settings', {'number_format': '#,###.###', 'currency_precision': 3, 'float_precision': 3})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_consolidation_rounding_adjustment(self)

Test if the rounding adjustment is calculated correctly

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_serial_no_case_1(self)

Create a POS Invoice with serial no
Create a Return Invoice with serial no
Create a POS Invoice with serial no again
Consolidate the invoices

The first POS Invoice should be consolidated with a separate single Merge Log
The second and third POS Invoice should be consolidated with a single Merge Log

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_separate_consolidated_invoice_for_different_accounting_dimensions(self)

Creating 3 POS Invoices where first POS Invoice has different Cost Center than the other two.
Consolidate the Invoices.
Check whether the first POS Invoice is consolidated with a separate Sales Invoice than the other two.
Check whether the second and third POS Invoice are consolidated with the same Sales Invoice.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_company_in_pos_invoice_merge_log(self)

Test if the company is fetched from POS Closing Entry

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



