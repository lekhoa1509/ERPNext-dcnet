# API Reference: process_statement_of_accounts.py

**Language**: Python

**Source**: `doctype/process_statement_of_accounts/process_statement_of_accounts.py`

---

## Classes

### ProcessStatementOfAccounts

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_company_for_table(self, doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |




## Functions

### get_report_pdf(doc, consolidated = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| consolidated | None | True | - |

**Returns**: (none)



### get_statement_dict(doc, get_statement_dict = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| get_statement_dict | None | False | - |

**Returns**: (none)



### set_ageing(doc, entry)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| entry | None | - | - |

**Returns**: (none)



### get_common_filters(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### get_gl_filters(doc, entry, tax_id, presentation_currency)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| entry | None | - | - |
| tax_id | None | - | - |
| presentation_currency | None | - | - |

**Returns**: (none)



### get_ar_filters(doc, entry)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| entry | None | - | - |

**Returns**: (none)



### get_html(doc, filters, entry, col, res, ageing)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| filters | None | - | - |
| entry | None | - | - |
| col | None | - | - |
| res | None | - | - |
| ageing | None | - | - |

**Returns**: (none)



### get_customers_based_on_territory_or_customer_group(customer_collection, collection_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| customer_collection | None | - | - |
| collection_name | None | - | - |

**Returns**: (none)



### get_customers_based_on_sales_person(sales_person)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sales_person | None | - | - |

**Returns**: (none)



### get_recipients_and_cc(customer, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| customer | None | - | - |
| doc | None | - | - |

**Returns**: (none)



### get_context(customer, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| customer | None | - | - |
| doc | None | - | - |

**Returns**: (none)



### fetch_customers(customer_collection, collection_name, primary_mandatory)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| customer_collection | None | - | - |
| collection_name | None | - | - |
| primary_mandatory | None | - | - |

**Returns**: (none)



### get_customer_emails(customer_name, primary_mandatory, billing_and_primary = True)

Returns first email from Contact Email table as a Billing email
when Is Billing Contact checked
and Primary email- email with Is Primary checked

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| customer_name | None | - | - |
| primary_mandatory | None | - | - |
| billing_and_primary | None | True | - |

**Returns**: (none)



### download_statements(document_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| document_name | None | - | - |

**Returns**: (none)



### send_emails(document_name, from_scheduler = False, posting_date = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| document_name | None | - | - |
| from_scheduler | None | False | - |
| posting_date | None | None | - |

**Returns**: (none)



### send_auto_email()

**Returns**: (none)


