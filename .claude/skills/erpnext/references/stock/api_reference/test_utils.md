# API Reference: test_utils.py

**Language**: Python

**Source**: `tests/test_utils.py`

---

## Classes

### StockTestMixin

Mixin to simplfy stock ledger tests, useful for all stock transactions.

**Inherits from**: (none)

#### Methods

##### make_item(self, item_code = None, properties = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item_code | None | None | - |
| properties | None | None | - |


##### assertSLEs(self, doc, expected_sles, sle_filters = None)

Compare sorted SLEs, useful for vouchers that create multiple SLEs for same line

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |
| expected_sles | None | - | - |
| sle_filters | None | None | - |


##### assertGLEs(self, doc, expected_gles, gle_filters = None, order_by = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |
| expected_gles | None | - | - |
| gle_filters | None | None | - |
| order_by | None | None | - |




### TestStockUtilities

**Inherits from**: IntegrationTestCase, StockTestMixin

#### Methods

##### test_barcode_scanning(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_barcode_scanning_of_warehouse(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



