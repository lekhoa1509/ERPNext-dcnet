# API Reference: stock_ledger_entry.py

**Language**: Python

**Source**: `doctype/stock_ledger_entry/stock_ledger_entry.py`

---

## Classes

### StockFreezeError

**Inherits from**: frappe.ValidationError



### BackDatedStockTransaction

**Inherits from**: frappe.ValidationError



### InventoryDimensionNegativeStockError

**Inherits from**: frappe.ValidationError



### StockLedgerEntry

**Inherits from**: Document

#### Methods

##### autoname(self)

Temporarily name doc for fast insertion
name will be changed using autoname options (in a scheduled job)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_posting_datetime(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_inventory_dimension_negative_stock(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_available_qty_after_prev_transaction(self, dimensions)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| dimensions | None | - | - |


##### throw_validation_error(self, diff, dimensions)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| diff | None | - | - |
| dimensions | None | - | - |


##### _get_inventory_dimensions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_mandatory(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_serial_batch_no_bundle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### throw_error_message(self, message, exception = frappe.ValidationError)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| message | None | - | - |
| exception | None | frappe.ValidationError | - |


##### check_stock_frozen_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### scrub_posting_time(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_batch(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_and_set_fiscal_year(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### block_transactions_against_group_warehouse(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_with_last_transaction_posting_time(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### on_doctype_update()

**Returns**: (none)


