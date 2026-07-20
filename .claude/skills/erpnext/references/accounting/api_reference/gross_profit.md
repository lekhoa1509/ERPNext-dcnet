# API Reference: gross_profit.py

**Language**: Python

**Source**: `report/gross_profit/gross_profit.py`

---

## Classes

### GrossProfitGenerator

**Inherits from**: (none)

#### Methods

##### __init__(self, filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| filters | None | None | - |


##### process(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_return_invoices(self, row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |


##### get_average_rate_based_on_group_by(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_average_based_on_payment_term_portion(self, new_row, row, invoice_portion, aggr = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| new_row | None | - | - |
| row | None | - | - |
| invoice_portion | None | - | - |
| aggr | None | False | - |


##### is_not_invoice_row(self, row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |


##### set_average_rate(self, new_row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| new_row | None | - | - |


##### set_average_gross_profit(self, new_row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| new_row | None | - | - |


##### get_returned_invoice_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### skip_row(self, row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |


##### get_buying_amount_from_product_bundle(self, row, product_bundle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| product_bundle | None | - | - |


##### calculate_buying_amount_from_sle(self, row, my_sle, parenttype, parent, item_row, item_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| my_sle | None | - | - |
| parenttype | None | - | - |
| parent | None | - | - |
| item_row | None | - | - |
| item_code | None | - | - |


##### get_buying_amount(self, row, item_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| item_code | None | - | - |


##### get_buying_amount_from_so_dn(self, sales_order, so_detail, item_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sales_order | None | - | - |
| so_detail | None | - | - |
| item_code | None | - | - |


##### get_average_buying_rate(self, row, item_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| item_code | None | - | - |


##### get_last_purchase_rate(self, item_code, row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item_code | None | - | - |
| row | None | - | - |


##### load_invoice_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_delivery_notes(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### group_items_by_invoice(self)

Turns list of Sales Invoice Items to a tree of Sales Invoices with their Items as children.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_invoice_row(self, row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |


##### get_bundle_item_row(self, row, item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| item | None | - | - |


##### get_stock_ledger_entries(self, item_code, warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item_code | None | - | - |
| warehouse | None | - | - |


##### load_product_bundle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### load_non_stock_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### execute(filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |

**Returns**: (none)



### get_data_when_grouped_by_invoice(columns, gross_profit_data, filters, group_wise_columns, data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| columns | None | - | - |
| gross_profit_data | None | - | - |
| filters | None | - | - |
| group_wise_columns | None | - | - |
| data | None | - | - |

**Returns**: (none)



### get_data_when_not_grouped_by_invoice(gross_profit_data, filters, group_wise_columns, data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| gross_profit_data | None | - | - |
| filters | None | - | - |
| group_wise_columns | None | - | - |
| data | None | - | - |

**Returns**: (none)



### get_columns(group_wise_columns, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| group_wise_columns | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_column_names()

**Returns**: (none)


