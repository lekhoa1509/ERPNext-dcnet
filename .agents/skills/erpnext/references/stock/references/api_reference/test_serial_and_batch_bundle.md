# API Reference: test_serial_and_batch_bundle.py

**Language**: Python

**Source**: `doctype/serial_and_batch_bundle/test_serial_and_batch_bundle.py`

---

## Classes

### TestSerialandBatchBundle

**Inherits from**: IntegrationTestCase

#### Methods

##### test_naming_for_sabb(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_inward_outward_serial_valuation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_inward_outward_batch_valuation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_old_batch_valuation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_old_serial_no_valuation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_batch_not_belong_to_serial_no(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auto_delete_draft_serial_and_batch_bundle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_serial_and_batch_bundle_company(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auto_cancel_serial_and_batch(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_batch_duplicate_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_serial_no_duplicate_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_duplicate_serial_and_batch_bundle(self)

**Decorators**: `@IntegrationTestCase.change_settings('Stock Settings', {'auto_create_serial_and_batch_bundle_for_outward': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_serial_no_valuation_for_legacy_ledgers(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_pick_serial_nos_for_batch_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auto_create_serial_and_batch_bundle_for_outward_for_batch_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_voucher_detail_no(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_batch_from_bundle(bundle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bundle | None | - | - |

**Returns**: (none)



### get_serial_nos_from_bundle(bundle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bundle | None | - | - |

**Returns**: (none)



### make_serial_batch_bundle(kwargs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kwargs | None | - | - |

**Returns**: (none)


