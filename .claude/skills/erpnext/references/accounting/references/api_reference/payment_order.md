# API Reference: payment_order.py

**Language**: Python

**Source**: `doctype/payment_order/payment_order.py`

---

## Classes

### PaymentOrder

**Inherits from**: Document

#### Methods

##### on_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_payment_status(self, cancel = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| cancel | None | False | - |




## Functions

### get_mop_query(doctype, txt, searchfield, start, page_len, filters)

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



### get_supplier_query(doctype, txt, searchfield, start, page_len, filters)

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



### make_payment_records(name, supplier, mode_of_payment = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |
| supplier | None | - | - |
| mode_of_payment | None | None | - |

**Returns**: (none)



### make_journal_entry(doc, supplier, mode_of_payment = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| supplier | None | - | - |
| mode_of_payment | None | None | - |

**Returns**: (none)


