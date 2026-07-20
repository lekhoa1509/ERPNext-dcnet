# API Reference: bin.py

**Language**: Python

**Source**: `doctype/bin/bin.py`

---

## Classes

### Bin

**Inherits from**: Document

#### Methods

##### recalculate_qty(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_save(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_projected_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_reserved_qty_for_production_plan(self, skip_project_qty_update = False, update_qty = True)

Update qty reserved for production from Production Plan tables
in open production plan

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| skip_project_qty_update | None | False | - |
| update_qty | None | True | - |


##### update_reserved_qty_for_for_sub_assembly(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_reserved_qty_for_production(self)

Update qty reserved for production from Production Item tables
in open work orders

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_reserved_qty_for_sub_contracting(self, subcontract_doctype = 'Subcontracting Order', update_qty = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| subcontract_doctype | None | 'Subcontracting Order' | - |
| update_qty | None | True | - |


##### update_reserved_stock(self)

Update `Reserved Stock` on change in Reserved Qty of Stock Reservation Entry

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### on_doctype_update()

**Returns**: (none)



### get_bin_details(bin_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bin_name | None | - | - |

**Returns**: (none)



### update_qty(bin_name, args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bin_name | None | - | - |
| args | None | - | - |

**Returns**: (none)



### get_actual_qty(item_code, warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |

**Returns**: (none)


