# API Reference: stock_reposting_settings.py

**Language**: Python

**Source**: `doctype/stock_reposting_settings/stock_reposting_settings.py`

---

## Classes

### StockRepostingSettings

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_save(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### reset_parallel_reposting_settings(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_minimum_reposting_time_slot(self)

Ensure that timeslot for reposting is at least 12 hours.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### convert_to_item_wh_reposting(self)

Convert Transaction reposting to Item Warehouse based reposting if Item Based Reposting has enabled.

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_reposting_entries()

**Returns**: (none)



### get_stock_ledgers(vouchers)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| vouchers | None | - | - |

**Returns**: (none)



### create_repost_item_valuation(item_code, warehouse, posting_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |
| posting_date | None | - | - |

**Returns**: (none)


