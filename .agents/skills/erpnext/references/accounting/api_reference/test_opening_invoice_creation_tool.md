# API Reference: test_opening_invoice_creation_tool.py

**Language**: Python

**Source**: `doctype/opening_invoice_creation_tool/test_opening_invoice_creation_tool.py`

---

## Classes

### TestOpeningInvoiceCreationTool

**Inherits from**: IntegrationTestCase

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### make_invoices(self, invoice_type = 'Sales', company = None, party_1 = None, party_2 = None, invoice_number = None, department = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| invoice_type | None | 'Sales' | - |
| company | None | None | - |
| party_1 | None | None | - |
| party_2 | None | None | - |
| invoice_number | None | None | - |
| department | None | None | - |


##### test_opening_sales_invoice_creation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_expected_values(self, invoices, expected_value, invoice_type = 'Sales')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| invoices | None | - | - |
| expected_value | None | - | - |
| invoice_type | None | 'Sales' | - |


##### test_opening_purchase_invoice_creation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_opening_sales_invoice_creation_with_missing_debit_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_renaming_of_invoice_using_invoice_number_field(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_opening_invoice_with_accounting_dimension(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_opening_invoice_creation_dict()

**Returns**: (none)



### make_company()

**Returns**: (none)



### make_customer(customer = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| customer | None | None | - |

**Returns**: (none)


