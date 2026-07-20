# API Reference: test_pos_closing_entry.py

**Language**: Python

**Source**: `doctype/pos_closing_entry/test_pos_closing_entry.py`

---

## Classes

### TestPOSClosingEntry

**Inherits from**: IntegrationTestCase

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### tearDownClass(cls)

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


##### test_pos_closing_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_pos_closing_without_item_code(self)

Test if POS Closing Entry is created without item code

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_pos_qty_for_item(self)

Test if quantity is calculated correctly for an item in POS Closing Entry

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cancelling_of_pos_closing_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_pos_closing_for_required_accounting_dimension_in_pos_profile(self)

test case to check whether we can create POS Closing Entry without mandatory accounting dimension

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_merging_into_sales_invoice_for_batched_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_closing_entries_with_sales_invoice(self)

**Decorators**: `@IntegrationTestCase.change_settings('POS Settings', {'invoice_type': 'Sales Invoice'})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_invoice_in_pos_invoice_mode(self)

Test Sales Invoice and Return Sales Invoice creation during POS Invoice mode.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_pos_invoice_in_sales_invoice_mode(self)

Test POS Invoice and Return POS Invoice creation during Sales Invoice mode.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### init_user_and_profile()

**Returns**: (none)



### get_test_item_qty(pos_profile)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pos_profile | None | - | - |

**Returns**: (none)



### create_multiple_sales_invoices(pos_profile)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pos_profile | None | - | - |

**Returns**: (none)



### create_multiple_pos_invoices(pos_profile)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pos_profile | None | - | - |

**Returns**: (none)


