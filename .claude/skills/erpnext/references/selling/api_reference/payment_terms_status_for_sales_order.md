# API Reference: payment_terms_status_for_sales_order.py

**Language**: Python

**Source**: `report/payment_terms_status_for_sales_order/payment_terms_status_for_sales_order.py`

---

## Functions

### get_columns()

**Returns**: (none)



### get_descendants_of(doctype, group_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| group_name | None | - | - |

**Returns**: (none)



### get_customers_or_items(doctype, txt, searchfield, start, page_len, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| txt | None | - | - |
| searchfield | None | - | - |
| start | None | - | - |
| page_len | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_conditions(filters)

Convert filter options to conditions used in query

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### build_filter_criterions(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### get_so_with_invoices(filters)

Get Sales Order with payment terms template with their associated Invoices

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### set_payment_terms_statuses(sales_orders, invoices, filters)

compute status for payment terms with associated sales invoice using FIFO

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sales_orders | None | - | - |
| invoices | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### prepare_chart(s_orders)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| s_orders | None | - | - |

**Returns**: (none)



### filter_on_calculated_status(filters, sales_orders)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| sales_orders | None | - | - |

**Returns**: (none)



### filter_for_immediate_upcoming_term(filters, sales_orders)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| sales_orders | None | - | - |

**Returns**: (none)



### execute(filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |

**Returns**: (none)


