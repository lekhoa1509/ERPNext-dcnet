# API Reference: email_digest.py

**Language**: Python

**Source**: `doctype/email_digest/email_digest.py`

---

## Classes

### EmailDigest

**Inherits from**: Document

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_users(self)

get list of users

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### send(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_msg_html(self)

Build email digest content

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_title(self, context)

Set digest title

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| context | None | - | - |


##### set_style(self, context)

Set standard digest style

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| context | None | - | - |


##### get_notifications(self)

Get notifications for user

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_calendar_events(self)

Get calendar events for given user

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_todo_list(self, user_id = None)

Get to-do list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user_id | None | None | - |


##### get_todo_count(self, user_id = None)

Get count of Todo

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user_id | None | None | - |


##### get_issue_list(self, user_id = None)

Get issue list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user_id | None | None | - |


##### get_issue_count(self)

Get count of Issue

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_project_list(self, user_id = None)

Get project list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user_id | None | None | - |


##### get_project_count(self)

Get count of Project

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_accounting_cards(self, context)

Create accounting cards if checked

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| context | None | - | - |


##### get_income(self)

Get income for given period

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_income_year_to_date(self)

Get income to date

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_expense_year_to_date(self)

Get income to date

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_year_to_date_balance(self, root_type, fieldname)

Get income to date

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| root_type | None | - | - |
| fieldname | None | - | - |


##### get_bank_balance(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_credit_balance(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_payables(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_invoiced_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_expenses_booked(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_period_amounts(self, accounts, fieldname)

Get amounts for current and past periods

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| accounts | None | - | - |
| fieldname | None | - | - |


##### get_sales_orders_to_bill(self)

Get value not billed

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_sales_orders_to_deliver(self)

Get value not delivered

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_purchase_orders_to_receive(self)

Get value not received

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_purchase_orders_to_bill(self)

Get purchase not billed

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_type_balance(self, fieldname, account_type, root_type = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | None | - | - |
| account_type | None | - | - |
| root_type | None | None | - |


##### get_roots(self, root_type)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| root_type | None | - | - |


##### get_root_type_accounts(self, root_type)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| root_type | None | - | - |


##### get_purchase_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_sales_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_pending_purchase_orders(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_pending_sales_orders(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_sales_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_purchase_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_new_quotations(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_pending_quotations(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_summary_of_pending(self, doc_type, fieldname, getfield)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc_type | None | - | - |
| fieldname | None | - | - |
| getfield | None | - | - |


##### get_summary_of_pending_quotations(self, fieldname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | None | - | - |


##### get_summary_of_doc(self, doc_type, fieldname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc_type | None | - | - |
| fieldname | None | - | - |


##### get_total_on(self, doc_type, from_date, to_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc_type | None | - | - |
| from_date | None | - | - |
| to_date | None | - | - |


##### get_from_to_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_dates(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_next_sending(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### onload(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### fmt_money(self, value, absol = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| value | None | - | - |
| absol | None | True | - |


##### get_purchase_orders_items_overdue_list(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### send()

**Returns**: (none)



### get_digest_msg(name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: (none)



### get_incomes_expenses_for_period(account, from_date, to_date)

Get amounts for current and past periods

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account | None | - | - |
| from_date | None | - | - |
| to_date | None | - | - |

**Returns**: (none)



### get_count_for_period(account, fieldname, from_date, to_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account | None | - | - |
| fieldname | None | - | - |
| from_date | None | - | - |
| to_date | None | - | - |

**Returns**: (none)



### get_future_date_for_calendaer_event(frequency)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| frequency | None | - | - |

**Returns**: (none)


