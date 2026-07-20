# API Reference: deferred_revenue_and_expense.py

**Language**: Python

**Source**: `report/deferred_revenue_and_expense/deferred_revenue_and_expense.py`

---

## Classes

### Deferred_Item

Helper class for processing items with deferred revenue/expense

**Inherits from**: (none)

#### Methods

##### __init__(self, item, inv, gle_entries)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item | None | - | - |
| inv | None | - | - |
| gle_entries | None | - | - |


##### report_data(self)

Generate report data for output

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_amount(self, entry)

For a given GL/Journal posting, get balance based on item type

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| entry | None | - | - |


##### get_item_total(self)

Helper method - calculate booked amount. Includes simulated postings as well

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate_amount(self, start_date, end_date)

start_date, end_date - datetime.datetime.date
return - estimated amount to post for given period
Calculated based on already booked amount and item service period

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| start_date | None | - | - |
| end_date | None | - | - |


##### calculate_monthly_amount(self, start_date, end_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| start_date | None | - | - |
| end_date | None | - | - |


##### calculate_days_amount(self, start_date, end_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| start_date | None | - | - |
| end_date | None | - | - |


##### make_dummy_gle(self, name, date, amount)

return - frappe._dict() of a dummy gle entry

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | None | - | - |
| date | None | - | - |
| amount | None | - | - |


##### simulate_future_posting(self)

simulate future posting by creating dummy gl entries. starts from the last posting date.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate_item_revenue_expense_for_period(self)

calculate item postings for each period and update period_total list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### Deferred_Invoice

**Inherits from**: (none)

#### Methods

##### __init__(self, invoice, items, filters, period_list)

Helper class for processing invoices with deferred revenue/expense items
invoice - string : invoice name
items - list : frappe._dict() with item details. Refer Deferred_Item for required fields

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| invoice | None | - | - |
| items | None | - | - |
| filters | None | - | - |
| period_list | None | - | - |


##### calculate_invoice_revenue_expense_for_period(self)

calculate deferred revenue/expense for all items in invoice

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### estimate_future(self)

create dummy GL entries for upcoming months for all items in invoice

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### report_data(self)

generate report data for invoice, includes invoice total

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### Deferred_Revenue_and_Expense_Report

**Inherits from**: (none)

#### Methods

##### __init__(self, filters = None)

Initialize deferred revenue/expense report with user provided filters or system defaults, if none is provided

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| filters | None | None | - |


##### get_period_list(self)

Figure out selected period based on filters

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_invoices(self)

Get all sales and purchase invoices which has deferred revenue/expense items

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### estimate_future(self)

For all Invoices estimate upcoming postings

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate_revenue_and_expense(self)

calculate the deferred revenue/expense for all invoices

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_columns(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### generate_report_data(self)

Generate report data for all invoices. Adds total rows for revenue and expense

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### prepare_chart(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### run(self)

Run report and generate data

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


