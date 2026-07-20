# API Reference: sms_settings.py

**Language**: Python

**Source**: `core/doctype/sms_settings/sms_settings.py`

---

## Classes

### SMSSettings

**Inherits from**: Document



## Functions

### validate_receiver_nos(receiver_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| receiver_list | None | - | - |

**Returns**: (none)



### get_contact_number(contact_name, ref_doctype, ref_name)

Return mobile number of the given contact.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| contact_name | None | - | - |
| ref_doctype | None | - | - |
| ref_name | None | - | - |

**Returns**: (none)



### send_sms(receiver_list, msg, sender_name = '', success_msg = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| receiver_list | None | - | - |
| msg | None | - | - |
| sender_name | None | '' | - |
| success_msg | None | True | - |

**Returns**: (none)



### send_via_gateway(arg)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| arg | None | - | - |

**Returns**: (none)



### get_headers(sms_settings = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sms_settings | None | None | - |

**Returns**: (none)



### send_request(gateway_url, params, headers = None, use_post = False, use_json = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| gateway_url | None | - | - |
| params | None | - | - |
| headers | None | None | - |
| use_post | None | False | - |
| use_json | None | False | - |

**Returns**: (none)



### create_sms_log(args, sent_to)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |
| sent_to | None | - | - |

**Returns**: (none)


