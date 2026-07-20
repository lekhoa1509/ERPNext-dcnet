# API Reference: test_shipment.py

**Language**: Python

**Source**: `doctype/shipment/test_shipment.py`

---

## Classes

### TestShipment

**Inherits from**: IntegrationTestCase

#### Methods

##### test_shipment_from_delivery_note(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_total_weight(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_test_delivery_note()

**Returns**: (none)



### create_test_shipment(delivery_notes = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| delivery_notes | None | None | - |

**Returns**: (none)



### get_shipment_customer_contact(customer_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| customer_name | None | - | - |

**Returns**: (none)



### get_shipment_customer_address(customer_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| customer_name | None | - | - |

**Returns**: (none)



### get_shipment_customer()

**Returns**: (none)



### get_shipment_company_address(company_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company_name | None | - | - |

**Returns**: (none)



### get_shipment_company()

**Returns**: (none)



### get_shipment_item(company_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company_name | None | - | - |

**Returns**: (none)



### create_shipment_address(address_title, company_name, postal_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| address_title | None | - | - |
| company_name | None | - | - |
| postal_code | None | - | - |

**Returns**: (none)



### create_customer_contact(fname, lname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fname | None | - | - |
| lname | None | - | - |

**Returns**: (none)



### create_shipment_customer(customer_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| customer_name | None | - | - |

**Returns**: (none)



### create_material_receipt(item, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | None | - | - |
| company | None | - | - |

**Returns**: (none)



### create_shipment_item(item_name, company_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_name | None | - | - |
| company_name | None | - | - |

**Returns**: (none)


