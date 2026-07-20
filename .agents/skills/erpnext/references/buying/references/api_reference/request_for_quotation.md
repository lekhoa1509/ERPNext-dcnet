# API Reference: request_for_quotation.py

**Language**: Python

**Source**: `doctype/request_for_quotation/request_for_quotation.py`

---

## Classes

### RequestforQuotation

**Inherits from**: BuyingController

#### Methods

##### before_validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_has_unit_price_items(self)

If permitted in settings and any item has 0 qty, the RFQ has unit price items.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_data_for_supplier(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_duplicate_supplier(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_supplier_list(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_email_id(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_email_id(self, args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| args | None | - | - |


##### on_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_print(self, settings = None)

Use the first suppliers data to render the print preview.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| settings | None | None | - |


##### on_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_supplier_email_preview(self, supplier)

Returns formatted email preview as string.

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| supplier | None | - | - |


##### send_to_supplier(self)

Sends RFQ mail to involved suppliers.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_link(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_supplier_part_no(self, supplier)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| supplier | None | - | - |


##### update_supplier_contact(self, rfq_supplier, link)

Create a new user for the supplier if not set in contact

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| rfq_supplier | None | - | - |
| link | None | - | - |


##### link_supplier_contact(self, rfq_supplier, user)

If no Contact, create a new contact against Supplier. If Contact exists, check if email and user id set.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| rfq_supplier | None | - | - |
| user | None | - | - |


##### update_user_in_supplier(self, supplier, user)

Update user in Supplier.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| supplier | None | - | - |
| user | None | - | - |


##### create_user(self, rfq_supplier, link)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| rfq_supplier | None | - | - |
| link | None | - | - |


##### supplier_rfq_mail(self, data, update_password_link, rfq_link, preview = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| data | None | - | - |
| update_password_link | None | - | - |
| rfq_link | None | - | - |
| preview | None | False | - |


##### send_email(self, data, sender, subject, message, attachments)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| data | None | - | - |
| sender | None | - | - |
| subject | None | - | - |
| message | None | - | - |
| attachments | None | - | - |


##### get_attachments(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_rfq_supplier_status(self, sup_name = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sup_name | None | None | - |




## Functions

### send_supplier_emails(rfq_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rfq_name | None | - | - |

**Returns**: (none)



### check_portal_enabled(reference_doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| reference_doctype | None | - | - |

**Returns**: (none)



### get_list_context(context = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | None | None | - |

**Returns**: (none)



### make_supplier_quotation_from_rfq(source_name, target_doc = None, for_supplier = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |
| for_supplier | None | None | - |

**Returns**: (none)



### create_supplier_quotation(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### add_items(sq_doc, supplier, items)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sq_doc | None | - | - |
| supplier | None | - | - |
| items | None | - | - |

**Returns**: (none)



### create_rfq_items(sq_doc, supplier, data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sq_doc | None | - | - |
| supplier | None | - | - |
| data | None | - | - |

**Returns**: (none)



### get_pdf(name: str, supplier: str, print_format: str | None = None, language: str | None = None, letterhead: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | str | - | - |
| supplier | str | - | - |
| print_format | str | None | None | - |
| language | str | None | None | - |
| letterhead | str | None | None | - |

**Returns**: (none)



### get_item_from_material_requests_based_on_supplier(source_name, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### get_supplier_tag()

**Returns**: (none)



### get_rfq_containing_supplier(doctype, txt, searchfield, start, page_len, filters)

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



### postprocess(source, target_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target_doc | None | - | - |

**Returns**: (none)


