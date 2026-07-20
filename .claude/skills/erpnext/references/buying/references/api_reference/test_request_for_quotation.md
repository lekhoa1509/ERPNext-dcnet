# API Reference: test_request_for_quotation.py

**Language**: Python

**Source**: `doctype/request_for_quotation/test_request_for_quotation.py`

---

## Classes

### TestRequestforQuotation

**Inherits from**: IntegrationTestCase

#### Methods

##### test_rfq_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_rfq_zero_qty(self)

Test if RFQ with zero qty (Unit Price Item) is conditionally allowed.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_quote_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_supplier_quotation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_supplier_quotation_with_taxes(self)

Test automatic tax addition when supplier quotation is created from RFQ taxes_and_charges are set

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_supplier_quotation_with_special_characters(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_supplier_quotation_from_portal(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_multi_uom_supplier_quotation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_rfq_from_opportunity(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_link(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_pdf(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_portal_user_with_new_supplier(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_supplier_quotation_from_zero_qty_rfq(self)

**Decorators**: `@IntegrationTestCase.change_settings('Buying Settings', {'allow_zero_qty_in_request_for_quotation': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_supplier_quotation_from_zero_qty_rfq_in_portal(self)

**Decorators**: `@IntegrationTestCase.change_settings('Buying Settings', {'allow_zero_qty_in_request_for_quotation': 1, 'allow_zero_qty_in_supplier_quotation': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### make_request_for_quotation() → 'RequestforQuotation'

:param supplier_data: List containing supplier data

**Returns**: `'RequestforQuotation'`



### get_supplier_data()

**Returns**: (none)


