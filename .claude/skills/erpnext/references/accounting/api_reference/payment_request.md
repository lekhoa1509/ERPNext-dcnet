# API Reference: payment_request.py

**Language**: Python

**Source**: `doctype/payment_request/payment_request.py`

---

## Classes

### PaymentRequest

**Inherits from**: Document

#### Methods

##### on_discard(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_reference_document(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_payment_request_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_currency(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_subscription_details(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### request_phone_payment(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_request_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### payment_gateway_validation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_payment_request_url(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_payment_url(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_as_paid(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_payment_entry(self, submit = True)

create entry

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| submit | None | True | - |


##### send_email(self)

send email with payment link

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_message(self)

return message with payment gateway link

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_failed(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_as_cancelled(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_if_payment_entry_exists(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_communication_entry(self)

Make communication entry

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_subscription(self, payment_provider, gateway_controller, data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| payment_provider | None | - | - |
| gateway_controller | None | - | - |
| data | None | - | - |


##### update_reference_advance_payment_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _allocate_payment_request_to_pe_references(self, references)

Allocate the Payment Request to the Payment Entry references based on

    - Allocated Amount.
    - Outstanding Amount of Payment Request.

Payment Request is doc itself and references are the rows of Payment Entry.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| references | None | - | - |




## Functions

### _get_payment_gateway_controller()

**Returns**: (none)



### make_payment_request()

Make payment request

**Returns**: (none)



### get_amount(ref_doc, payment_account = None)

get amount based on doctype

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ref_doc | None | - | - |
| payment_account | None | None | - |

**Returns**: (none)



### get_irequest_status(payment_requests: None | list = None) → list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| payment_requests | None | list | None | - |

**Returns**: `list`



### cancel_old_payment_requests(ref_dt, ref_dn)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ref_dt | None | - | - |
| ref_dn | None | - | - |

**Returns**: (none)



### get_existing_payment_request_amount(ref_doc, statuses: list | None = None) → list

Return the total amount of Payment Requests against a reference document.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ref_doc | None | - | - |
| statuses | list | None | None | - |

**Returns**: `list`



### get_gateway_details(args)

Return gateway and payment account of default payment gateway

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### get_payment_gateway_account(filter)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filter | None | - | - |

**Returns**: (none)



### get_print_format_list(ref_doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ref_doctype | None | - | - |

**Returns**: (none)



### resend_payment_email(docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docname | None | - | - |

**Returns**: (none)



### make_payment_entry(docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docname | None | - | - |

**Returns**: (none)



### update_payment_requests_as_per_pe_references(references = None, cancel = False)

Update Payment Request's `Status` and `Outstanding Amount` based on Payment Entry Reference's `Allocated Amount`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| references | None | None | - |
| cancel | None | False | - |

**Returns**: (none)



### get_dummy_message(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### get_subscription_details(reference_doctype, reference_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| reference_doctype | None | - | - |
| reference_name | None | - | - |

**Returns**: (none)



### make_payment_order(source_name, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### validate_payment(doc, method = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| method | None | None | - |

**Returns**: (none)



### get_open_payment_requests_query(doctype, txt, searchfield, start, page_len, filters)

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



### get_irequests_of_payment_request(doc: str | None = None) → list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | str | None | None | - |

**Returns**: `list`



### validate_and_calculate_grand_total(grand_total, existing_payment_request_amount)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| grand_total | None | - | - |
| existing_payment_request_amount | None | - | - |

**Returns**: (none)



### set_missing_values(source, target)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |

**Returns**: (none)


