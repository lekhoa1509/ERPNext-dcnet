# API Reference: customer.py

**Language**: Python

**Source**: `doctype/customer/customer.py`

---

## Classes

### Customer

**Inherits from**: TransactionBase

#### Methods

##### onload(self)

Load address and contacts in `__onload`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### load_dashboard_info(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### autoname(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_customer_name(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### after_insert(self)

If customer created from Lead, update customer id in quotations, opportunities

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_customer_group_details(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_customer_group_change(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_default_bank_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_internal_customer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_role_for_user(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_customer_groups(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_primary_contact(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_primary_address(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_lead_status(self)

If Customer created from Lead, update lead status to "Converted"
update Customer link in Quotation, Opportunity

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### link_address_and_contact(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### copy_communication(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_name_with_customer_group(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_credit_limit_on_change(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_rename(self, olddn, newdn, merge = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| olddn | None | - | - |
| newdn | None | - | - |
| merge | None | False | - |


##### after_rename(self, olddn, newdn, merge = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| olddn | None | - | - |
| newdn | None | - | - |
| merge | None | False | - |


##### set_loyalty_program(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### make_quotation(source_name, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### make_opportunity(source_name, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### make_payment_entry(source_name, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### _set_missing_values(source, target)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |

**Returns**: (none)



### get_loyalty_programs(doc)

returns applicable loyalty programs for a customer

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### get_nested_links(link_doctype, link_name, ignore_permissions = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| link_doctype | None | - | - |
| link_name | None | - | - |
| ignore_permissions | None | False | - |

**Returns**: (none)



### check_credit_limit(customer, company, ignore_outstanding_sales_order = False, extra_amount = 0)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| customer | None | - | - |
| company | None | - | - |
| ignore_outstanding_sales_order | None | False | - |
| extra_amount | None | 0 | - |

**Returns**: (none)



### send_emails(customer, customer_outstanding, credit_limit, credit_controller_users_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| customer | None | - | - |
| customer_outstanding | None | - | - |
| credit_limit | None | - | - |
| credit_controller_users_list | None | - | - |

**Returns**: (none)



### get_customer_outstanding(customer, company, ignore_outstanding_sales_order = False, cost_center = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| customer | None | - | - |
| company | None | - | - |
| ignore_outstanding_sales_order | None | False | - |
| cost_center | None | None | - |

**Returns**: (none)



### get_credit_limit(customer, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| customer | None | - | - |
| company | None | - | - |

**Returns**: (none)



### make_contact(args, is_primary_contact = 1)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |
| is_primary_contact | None | 1 | - |

**Returns**: (none)



### make_address(args, is_primary_address = 1, is_shipping_address = 1)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |
| is_primary_address | None | 1 | - |
| is_shipping_address | None | 1 | - |

**Returns**: (none)



### get_customer_primary(doctype, txt, searchfield, start, page_len, filters)

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



### parse_full_name(full_name: str) → tuple[str, str | None, str | None]

Parse full name into first name, middle name and last name

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| full_name | str | - | - |

**Returns**: `tuple[str, str | None, str | None]`



### set_missing_values(source, target)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |

**Returns**: (none)



### set_missing_values(source, target)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |

**Returns**: (none)



### set_missing_values(source, target)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |

**Returns**: (none)


