# API Reference: test_supplier_quotation.py

**Language**: Python

**Source**: `doctype/supplier_quotation/test_supplier_quotation.py`

---

## Classes

### TestPurchaseOrder

**Inherits from**: IntegrationTestCase

#### Methods

##### test_update_child_supplier_quotation_add_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_supplier_quotation_child_rate_disallow(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_supplier_quotation_child_remove_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_supplier_quotation_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_supplier_quotation_zero_qty(self)

Test if RFQ with zero qty (Unit Price Item) is conditionally allowed.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_purchase_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_map_purchase_order_from_zero_qty_supplier_quotation(self)

**Decorators**: `@IntegrationTestCase.change_settings('Buying Settings', {'allow_zero_qty_in_supplier_quotation': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



