# API Reference: test_packed_item.py

**Language**: Python

**Source**: `doctype/packed_item/test_packed_item.py`

---

## Classes

### TestPackedItem

Test impact on Packed Items table in various scenarios.

**Inherits from**: IntegrationTestCase

#### Methods

##### setUpClass(cls) → None

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |

**Returns**: `None`


##### test_adding_bundle_item(self)

Test impact on packed items if bundle item row is added.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_updating_bundle_item(self)

Test impact on packed items if bundle item row is updated.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_recurring_bundle_item(self)

Test impact on packed items if same bundle item is added and removed.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bundle_item_cumulative_price(self)

Test if Bundle Item rate is cumulative from packed items.

**Decorators**: `@IntegrationTestCase.change_settings('Selling Settings', {'editable_bundle_item_rates': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_newly_mapped_doc_packed_items(self)

Test impact on packed items in newly mapped DN from SO.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reposting_packed_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### assertReturns(self, original, returned)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| original | None | - | - |
| returned | None | - | - |


##### test_returning_full_bundles(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_returning_partial_bundles(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_returning_partial_bundle_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_product_bundle(quantities: list[int] | None = None, warehouse: str | None = None) → tuple[str, list[str]]

Get a new product_bundle for use in tests.

Create 10x required stock if warehouse is specified.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| quantities | list[int] | None | None | - |
| warehouse | str | None | None | - |

**Returns**: `tuple[str, list[str]]`



### sort_function(p)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| p | None | - | - |

**Returns**: (none)


