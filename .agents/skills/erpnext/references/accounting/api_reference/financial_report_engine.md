# API Reference: financial_report_engine.py

**Language**: Python

**Source**: `doctype/financial_report_template/financial_report_engine.py`

---

## Classes

### PeriodValue

Represents financial data for a single period

**Inherits from**: (none)

#### Methods

##### get_value(self, balance_type: str) → float

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| balance_type | str | - | - |

**Returns**: `float`


##### copy(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### AccountData

Account data across all periods

**Inherits from**: (none)

#### Methods

##### add_period(self, period_value: PeriodValue) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| period_value | PeriodValue | - | - |

**Returns**: `None`


##### get_period(self, period_key: str) → PeriodValue | None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| period_key | str | - | - |

**Returns**: `PeriodValue | None`


##### get_values_by_type(self, balance_type: str) → list[float]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| balance_type | str | - | - |

**Returns**: `list[float]`


##### get_ordered_values(self, period_keys: list[str], balance_type: str) → list[float]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| period_keys | list[str] | - | - |
| balance_type | str | - | - |

**Returns**: `list[float]`


##### has_periods(self) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `bool`


##### accumulate_values(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### unaccumulate_values(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### copy(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### reverse_values(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`




### RowData

Represents a processed template row with calculated values

**Inherits from**: (none)



### SegmentData

Represents a segment with its rows and metadata

**Inherits from**: (none)

#### Methods

##### id(self) → str

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `str`




### SectionData

Represents a horizontal section containing multiple column segments

**Inherits from**: (none)

#### Methods

##### id(self) → str

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `str`




### ReportContext

Context object that flows through the pipeline

**Inherits from**: (none)

#### Methods

##### get_result(self) → tuple[list[dict], list[dict]]

Get final formatted columns and data

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `tuple[list[dict], list[dict]]`




### FormattingRule

Rule for applying formatting to rows

**Inherits from**: (none)

#### Methods

##### applies_to(self, row_data: RowData) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row_data | RowData | - | - |

**Returns**: `bool`


##### get_properties(self, row_data: RowData) → dict[str, Any]

Get the format properties, handling both static and dynamic cases

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row_data | RowData | - | - |

**Returns**: `dict[str, Any]`




### FinancialReportEngine

**Inherits from**: (none)

#### Methods

##### execute(self, filters: dict[str, Any]) → tuple[list[dict], list[dict]]

Execute the complete report generation

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| filters | dict[str, Any] | - | - |

**Returns**: `tuple[list[dict], list[dict]]`


##### _validate_filters(self, filters: dict[str, Any]) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| filters | dict[str, Any] | - | - |

**Returns**: `None`


##### _initialize_context(self, filters: dict[str, Any]) → ReportContext

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| filters | dict[str, Any] | - | - |

**Returns**: `ReportContext`


##### collect_financial_data(self, context: ReportContext) → ReportContext

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| context | ReportContext | - | - |

**Returns**: `ReportContext`


##### process_calculations(self, context: ReportContext) → ReportContext

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| context | ReportContext | - | - |

**Returns**: `ReportContext`


##### format_report_data(self, context: ReportContext) → ReportContext

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| context | ReportContext | - | - |

**Returns**: `ReportContext`


##### apply_view_transformation(self, context: ReportContext) → ReportContext

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| context | ReportContext | - | - |

**Returns**: `ReportContext`


##### generate_chart_data(self, context: ReportContext) → dict[str, Any]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| context | ReportContext | - | - |

**Returns**: `dict[str, Any]`




### DataCollector

Data collector that fetches all data in optimized queries

**Inherits from**: (none)

#### Methods

##### __init__(self, filters: dict[str, Any], periods: list[dict])

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| filters | dict[str, Any] | - | - |
| periods | list[dict] | - | - |


##### add_account_request(self, row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |


##### collect_all_data(self) → dict[str, Any]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `dict[str, Any]`


##### _parse_account_filter(company, report_row) → list[dict]

Find accounts matching filter criteria.

Example:

- Input: '["account_type", "=", "Cash"]'
- Output: [{"name": "Cash - COMP", "account_name": "Cash", "account_number": "1001"}]

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| report_row | None | - | - |

**Returns**: `list[dict]`


##### get_filtered_accounts(company: str, account_rows: list) → list[str]

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | str | - | - |
| account_rows | list | - | - |

**Returns**: `list[str]`




### FinancialQueryBuilder

Centralized query builder for financial data

**Inherits from**: (none)

#### Methods

##### __init__(self, filters: dict[str, Any], periods: list[dict])

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| filters | dict[str, Any] | - | - |
| periods | list[dict] | - | - |


##### fetch_account_balances(self, accounts: list[dict]) → dict[str, AccountData]

Fetch account balances for all periods with optimization.
Steps: get opening balances → fetch GL entries → calculate running totals

- accounts: list of accounts with details

```
{
    "name": "Cash - COMP",
    "account_name": "Cash",
    "account_number": "1001",
}
```

Returns:
    dict: {account: AccountData}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| accounts | list[dict] | - | - |

**Returns**: `dict[str, AccountData]`


##### _get_opening_balances(self, accounts: list[str]) → dict[str, dict[str, dict[str, float]]]

Return opening balances for *all accounts* defaulting to zero.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| accounts | list[str] | - | - |

**Returns**: `dict[str, dict[str, dict[str, float]]]`


##### _get_closing_balances(self, account_names: list[str], closing_voucher: str) → dict[str, float]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| account_names | list[str] | - | - |
| closing_voucher | str | - | - |

**Returns**: `dict[str, float]`


##### _rebase_closing_balances(self, closing_data: dict[str, float], closing_date: str) → dict[str, dict[str, dict[str, float]]]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| closing_data | dict[str, float] | - | - |
| closing_date | str | - | - |

**Returns**: `dict[str, dict[str, dict[str, float]]]`


##### _get_opening_balances_from_gl(self, accounts: list[str]) → dict

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| accounts | list[str] | - | - |

**Returns**: `dict`


##### _get_gap_movements(self, account_names: list[str], from_date: str, to_date: str) → dict[str, float]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| account_names | list[str] | - | - |
| from_date | str | - | - |
| to_date | str | - | - |

**Returns**: `dict[str, float]`


##### _get_gl_movements(self, account_names: list[str]) → list[dict]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| account_names | list[str] | - | - |

**Returns**: `list[dict]`


##### _calculate_running_balances(self, balances_data: dict, gl_data: list[dict]) → dict

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| balances_data | dict | - | - |
| gl_data | list[dict] | - | - |

**Returns**: `dict`


##### _handle_balance_accumulation(self, balances_data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| balances_data | None | - | - |


##### _apply_standard_filters(self, query, table)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| query | None | - | - |
| table | None | - | - |


##### _execute_with_permissions(self, query, doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| query | None | - | - |
| doctype | None | - | - |


##### _get_account_meta(self, account: str) → dict[str, Any]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| account | str | - | - |

**Returns**: `dict[str, Any]`




### FilterExpressionParser

Direct filter expression to SQL condition builder

**Inherits from**: (none)

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### build_conditions(self, report_rows, table)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| report_rows | None | - | - |
| table | None | - | - |


##### build_condition(self, report_row, table)

Build SQL condition directly from filter formula.

Supports:
1. Simple condition: ["field", "operator", "value"]
   Example: ["account_type", "=", "Income"]

2. Complex logical conditions:
   {"and": [condition1, condition2, ...]}  # All conditions must be true
   {"or": [condition1, condition2, ...]}   # Any condition can be true

   Example:
   {
         "and": [
           ["account_type", "=", "Income"],
           {"or": [
                 ["category", "=", "Direct Income"],
                 ["category", "=", "Indirect Income"]
           ]}
         ]
   }

Returns:
        SQL condition object or None if invalid

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| report_row | None | - | - |
| table | None | - | - |


##### _build_from_parsed(self, parsed, table)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| parsed | None | - | - |
| table | None | - | - |


##### _build_simple_condition(self, condition_list: list[str, str, str | float], table)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| condition_list | list[str, str, str | float] | - | - |
| table | None | - | - |


##### _build_logical_condition(self, condition_dict: dict, table)

Build SQL condition from logical {"and/or": [...]} format

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| condition_dict | dict | - | - |
| table | None | - | - |




### FormulaFieldExtractor

Extract field values from filter formulas without SQL execution

**Inherits from**: (none)

#### Methods

##### __init__(self, field_name: str, exclude_operators: list[str] | None = None)

Initialize field extractor.

Args:
    field_name: The field to extract values for (e.g., "account_category")
    exclude_operators: List of operators to exclude (e.g., ["like"])

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| field_name | str | - | - |
| exclude_operators | list[str] | None | None | - |


##### extract_from_rows(self, rows: list) → set

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| rows | list | - | - |

**Returns**: `set`


##### _extract_recursive(self, parsed, values: set)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| parsed | None | - | - |
| values | set | - | - |




### FormulaFieldUpdater

Update field values in filter formulas

**Inherits from**: (none)

#### Methods

##### __init__(self, field_name: str, value_mapping: dict[str, str], exclude_operators: list[str] | None = None)

Initialize field updater.

Args:
    field_name: The field to update values for (e.g., "account_category")
    value_mapping: Mapping of old values to new values (e.g., {"Old Name": "New Name"})
    exclude_operators: List of operators to exclude from updates (e.g., ["like", "not like"])

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| field_name | str | - | - |
| value_mapping | dict[str, str] | - | - |
| exclude_operators | list[str] | None | None | - |


##### update_in_rows(self, rows: list) → dict[str, dict[str, str]]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| rows | list | - | - |

**Returns**: `dict[str, dict[str, str]]`


##### _update_recursive(self, parsed)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| parsed | None | - | - |


##### _update_value(self, value)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| value | None | - | - |




### RowProcessor

Processes individual rows of the financial report template.
Handles dependency resolution and calculation order.

**Inherits from**: (none)

#### Methods

##### __init__(self, context: ReportContext)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| context | ReportContext | - | - |


##### process_all_rows(self) → list[RowData]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `list[RowData]`


##### _process_single_row(self, row, account_summary: dict, account_details: dict) → RowData

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| account_summary | dict | - | - |
| account_details | dict | - | - |

**Returns**: `RowData`


##### _process_account_row(self, row, account_summary: dict, account_details: dict) → RowData

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| account_summary | dict | - | - |
| account_details | dict | - | - |

**Returns**: `RowData`


##### _process_api_row(self, row) → RowData

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |

**Returns**: `RowData`


##### _process_formula_row(self, row) → RowData

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |

**Returns**: `RowData`


##### _process_blank_row(self, row) → RowData

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |

**Returns**: `RowData`


##### _process_column_break_row(self, row) → RowData

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |

**Returns**: `RowData`


##### _process_section_break_row(self, row) → RowData

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |

**Returns**: `RowData`




### DependencyResolver

Optimized dependency resolver with better circular reference detection

**Inherits from**: (none)

#### Methods

##### __init__(self, template)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| template | None | - | - |


##### _validate_dependencies(self)

Validate dependencies using the new validation framework

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_processing_order(self) → list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `list`


##### _topological_sort(self, formula_rows: list) → list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| formula_rows | list | - | - |

**Returns**: `list`




### FormulaCalculator

Enhanced formula calculator with better error handling

**Inherits from**: (none)

#### Methods

##### __init__(self, row_data: dict[str, list[float]], period_list: list[dict])

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row_data | dict[str, list[float]] | - | - |
| period_list | list[dict] | - | - |


##### evaluate_formula(self, report_row: dict[str, Any]) → list[float]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| report_row | dict[str, Any] | - | - |

**Returns**: `list[float]`


##### _evaluate_for_period(self, formula: str, period_index: int, negation_factor: int) → float

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| formula | str | - | - |
| period_index | int | - | - |
| negation_factor | int | - | - |

**Returns**: `float`


##### _build_context(self, period_index: int) → dict[str, Any]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| period_index | int | - | - |

**Returns**: `dict[str, Any]`




### DataFormatter

**Inherits from**: (none)

#### Methods

##### __init__(self, context: ReportContext)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| context | ReportContext | - | - |


##### format_for_display(self) → tuple[list[dict], list[dict]]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `tuple[list[dict], list[dict]]`


##### _format_rows(self) → list[dict]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `list[dict]`


##### _generate_columns(self) → list[dict]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `list[dict]`


##### _expand_segments_with_details(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### FormattingEngine

Manages formatting rules and application

**Inherits from**: (none)

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### initialize_rules(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_formatting(self, row_data: RowData) → dict[str, Any]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row_data | RowData | - | - |

**Returns**: `dict[str, Any]`




### SegmentOrganizer

Handles segment organization by `Column Break`, `Section Break` and metadata extraction

**Inherits from**: (none)

#### Methods

##### __init__(self, processed_rows: list[RowData])

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| processed_rows | list[RowData] | - | - |


##### _organize_into_sections(self, rows: list[RowData]) → list[SectionData]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| rows | list[RowData] | - | - |

**Returns**: `list[SectionData]`


##### _organize_into_segments(self, rows: list[RowData], section_label: str) → list[SegmentData]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| rows | list[RowData] | - | - |
| section_label | str | - | - |

**Returns**: `list[SegmentData]`


##### is_single_segment(self) → bool

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `bool`


##### max_rows(self, section: SectionData) → int

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| section | SectionData | - | - |

**Returns**: `int`


##### max_segments(self) → bool

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `bool`


##### section_with_max_segments(self) → SectionData

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `SectionData`


##### _should_show_row(self, row_data: RowData) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row_data | RowData | - | - |

**Returns**: `bool`




### RowFormatterBase

**Inherits from**: ABC

#### Methods

##### __init__(self, context: ReportContext, formatting_engine: FormattingEngine)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| context | ReportContext | - | - |
| formatting_engine | FormattingEngine | - | - |


##### format_row(self, segments: list[SegmentData], row_index: int) → dict[str, Any]

**Decorators**: `@abstractmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| segments | list[SegmentData] | - | - |
| row_index | int | - | - |

**Returns**: `dict[str, Any]`


##### get_columns(self, segments: list[SegmentData], base_columns: list[dict]) → list[dict]

**Decorators**: `@abstractmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| segments | list[SegmentData] | - | - |
| base_columns | list[dict] | - | - |

**Returns**: `list[dict]`


##### _get_values(self, row_data: RowData) → dict[str, Any]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row_data | RowData | - | - |

**Returns**: `dict[str, Any]`


##### _get_period_value(self, row_data: RowData, period_index: int) → Any

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row_data | RowData | - | - |
| period_index | int | - | - |

**Returns**: `Any`




### SingleSegmentFormatter

**Inherits from**: RowFormatterBase

#### Methods

##### format_row(self, segments: list[SegmentData], row_index: int) → dict[str, Any]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| segments | list[SegmentData] | - | - |
| row_index | int | - | - |

**Returns**: `dict[str, Any]`


##### get_columns(self, segments: list[SegmentData], base_columns: list[dict]) → list[dict]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| segments | list[SegmentData] | - | - |
| base_columns | list[dict] | - | - |

**Returns**: `list[dict]`




### MultiSegmentFormatter

**Inherits from**: RowFormatterBase

#### Methods

##### format_row(self, segments: list[SegmentData], row_index: int) → dict[str, Any]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| segments | list[SegmentData] | - | - |
| row_index | int | - | - |

**Returns**: `dict[str, Any]`


##### get_columns(self, segments: list[SegmentData], base_columns: list[dict]) → list[dict]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| segments | list[SegmentData] | - | - |
| base_columns | list[dict] | - | - |

**Returns**: `list[dict]`


##### _add_segment_data(self, formatted: dict, row_data: RowData, segment: SegmentData)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| formatted | dict | - | - |
| row_data | RowData | - | - |
| segment | SegmentData | - | - |


##### _add_empty_segment(self, formatted: dict, segment: SegmentData)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| formatted | dict | - | - |
| segment | SegmentData | - | - |




### DetailRowBuilder

Builds detail rows for account breakdown

**Inherits from**: (none)

#### Methods

##### __init__(self, filters: dict, parent_row_data: RowData)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| filters | dict | - | - |
| parent_row_data | RowData | - | - |


##### build(self) → list[RowData]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `list[RowData]`


##### _create_detail_row_object(self, account_data: AccountData, parent_row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| account_data | AccountData | - | - |
| parent_row | None | - | - |




### ChartDataGenerator

**Inherits from**: (none)

#### Methods

##### __init__(self, context: ReportContext)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| context | ReportContext | - | - |


##### generate(self) → dict[str, Any]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `dict[str, Any]`




### GrowthViewTransformer

**Inherits from**: (none)

#### Methods

##### __init__(self, context: ReportContext)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| context | ReportContext | - | - |


##### transform(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### _calculate_growth(self, previous_value: float, current_value: float) → float | None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| previous_value | float | - | - |
| current_value | float | - | - |

**Returns**: `float | None`




## Functions

### get_filtered_accounts(company: str, account_rows: str | list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | str | - | - |
| account_rows | str | list | - | - |

**Returns**: (none)



### get_children_accounts(doctype: str, parent: str, company: str, filtered_accounts: list[str] | str | None = None, missed: bool = False, is_root: bool = False, include_disabled: bool = False)

Get children accounts based on the provided filters to view in tree.

Args:
    parent: The parent account to get children for.
    company: The company to filter accounts by.
    account_rows: Template rows with `Data Source` == `Account Data`.
    missed:
                - If True, only missed by filters accounts will be included.
                - If False, only filtered accounts will be included.
    is_root: Whether the parent is a root account.
    include_disabled: Whether to include disabled accounts.

Example:
```python
[
    {
        value: "Current Liabilities - WP",
        expandable: 1,
        root_type: "Liability",
        account_currency: "USD",
        parent: "Source of Funds (Liabilities) - WP",
    },
    {
        value: "Non-Current Liabilities - WP",
        expandable: 1,
        root_type: "Liability",
        account_currency: "USD",
        parent: "Source of Funds (Liabilities) - WP",
    },
]
```

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| parent | str | - | - |
| company | str | - | - |
| filtered_accounts | list[str] | str | None | None | - |
| missed | bool | False | - |
| is_root | bool | False | - |
| include_disabled | bool | False | - |

**Returns**: (none)



### _get_row_data(key: str, default: Any = '') → Any

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | str | - | - |
| default | Any | '' | - |

**Returns**: `Any`



### _get_filter_value(key: str, default: Any = '') → Any

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | str | - | - |
| default | Any | '' | - |

**Returns**: `Any`


