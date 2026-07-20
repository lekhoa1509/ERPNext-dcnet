# API Reference: budget.py

**Language**: Python

**Source**: `doctype/budget/budget.py`

---

## Classes

### BudgetError

**Inherits from**: frappe.ValidationError



### DuplicateBudgetError

**Inherits from**: frappe.ValidationError



### Budget

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_budget_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_fiscal_year(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_fiscal_year_company(self, fiscal_year, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fiscal_year | None | - | - |
| company | None | - | - |


##### set_fiscal_year_dates(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_duplicate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_null_value(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_applicable_for(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_existing_expenses(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_save(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### allocate_budget(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _should_skip_allocation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _should_recalculate_manual_distribution(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _is_only_budget_amount_changed(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _recalculate_manual_distribution(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### should_regenerate_budget_distribution(self)

Check whether budget distribution should be recalculated.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _regenerate_distribution(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_budget_periods(self)

Return list of (start_date, end_date) tuples based on frequency.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_period_end(self, start_date, frequency)

Return the correct end date for a given frequency.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| start_date | None | - | - |
| frequency | None | - | - |


##### get_month_increment(self, frequency)

Return how many months to move forward for the next period.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| frequency | None | - | - |


##### add_allocated_amount(self, row, row_percent)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| row_percent | None | - | - |


##### validate_distribution_totals(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### validate_expense_against_budget(params, expense_amount = 0)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| params | None | - | - |
| expense_amount | None | 0 | - |

**Returns**: (none)



### validate_budget_records(params, budget_records, expense_amount)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| params | None | - | - |
| budget_records | None | - | - |
| expense_amount | None | - | - |

**Returns**: (none)



### compare_expense_with_budget(params, budget_amount, action_for, action, budget_against, amount = 0)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| params | None | - | - |
| budget_amount | None | - | - |
| action_for | None | - | - |
| action | None | - | - |
| budget_against | None | - | - |
| amount | None | 0 | - |

**Returns**: (none)



### get_expense_breakup(params, currency, budget_against)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| params | None | - | - |
| currency | None | - | - |
| budget_against | None | - | - |

**Returns**: (none)



### get_actions(params, budget)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| params | None | - | - |
| budget | None | - | - |

**Returns**: (none)



### get_requested_amount(params)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| params | None | - | - |

**Returns**: (none)



### get_ordered_amount(params)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| params | None | - | - |

**Returns**: (none)



### get_other_condition(params, for_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| params | None | - | - |
| for_doc | None | - | - |

**Returns**: (none)



### get_actual_expense(params)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| params | None | - | - |

**Returns**: (none)



### get_accumulated_monthly_budget(budget_name, posting_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| budget_name | None | - | - |
| posting_date | None | - | - |

**Returns**: (none)



### get_item_details(params)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| params | None | - | - |

**Returns**: (none)



### get_expense_cost_center(doctype, params)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| params | None | - | - |

**Returns**: (none)



### get_fiscal_year_date_range(from_fiscal_year, to_fiscal_year)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| from_fiscal_year | None | - | - |
| to_fiscal_year | None | - | - |

**Returns**: (none)



### revise_budget(budget_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| budget_name | None | - | - |

**Returns**: (none)


