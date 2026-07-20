# API Reference: test_financial_report_engine.py

**Language**: Python

**Source**: `doctype/financial_report_template/test_financial_report_engine.py`

---

## Classes

### TestDependencyResolver

Test cases for DependencyResolver class

**Inherits from**: FinancialReportTemplateTestCase

#### Methods

##### test_resolve_basic_processing_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_resolve_simple_dependency(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_resolve_multiple_dependencies(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_resolve_chain_dependencies(self)

Test dependency resolution with chain of dependencies (A -> B -> C -> D)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_resolve_diamond_dependency_pattern(self)

Test Diamond Dependency Pattern - A → B, A → C, and both B,C → D

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_resolve_independent_formula_row_groups(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_resolve_mixed_data_sources(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_resolve_api_to_formula_dependencies(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_resolve_cross_datasource_dependencies(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_extract_from_complex_formulas(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_extract_references_with_math_functions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_extract_accurate_reference_matching(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_prevent_partial_reference_matches(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_resolve_rows_without_dependencies(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_handle_empty_reference_codes(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_resolve_include_orphaned_nodes(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_handle_valid_missing_references(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_detect_circular_dependency(self)

Test detection of circular dependency (A -> B -> C -> A)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestFormulaCalculator

Test cases for FormulaCalculator class

**Inherits from**: FinancialReportTemplateTestCase

#### Methods

##### _create_mock_report_row(self, formula: str, reference_code: str = 'TEST_ROW')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| formula | str | - | - |
| reference_code | str | 'TEST_ROW' | - |


##### test_evaluate_basic_operations(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_handle_division_by_zero(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_handle_missing_values(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_handle_invalid_reference_codes(self)

Test formula calculator handles invalid reference codes

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_handle_mismatched_period_data_lengths(self)

Test scenarios with mismatched period data

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_evaluate_complex_expressions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_evaluate_nested_function_combinations(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_calculate_financial_use_cases(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_calculate_common_financial_patterns(self)

Test patterns commonly used in financial calculations

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_handle_error_cases(self)

Test formula calculator error handling for various edge cases

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_evaluate_math_function_edge_cases(self)

Test edge cases for mathematical functions

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_prevent_security_vulnerabilities(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_build_context_validation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestFilterExpressionParser

Test cases for FilterExpressionParser class

**Inherits from**: FinancialReportTemplateTestCase

#### Methods

##### _create_mock_report_row(self, formula: str, reference_code: str = 'TEST_ROW')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| formula | str | - | - |
| reference_code | str | 'TEST_ROW' | - |


##### test_parse_simple_equality_condition(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_parse_logical_and_or_conditions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_parse_valid_operators(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_build_logical_condition_with_reduce(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_operator_value_compatibility(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_parse_complex_nested_filters(self)

Test complex nested filter expressions

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_parse_deeply_nested_conditions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_parse_different_value_types(self)

Test different value types in conditions

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_parse_special_characters_in_values(self)

Test special characters in filter values

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_parse_logical_operator_edge_cases(self)

Test edge cases for logical operators

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_build_condition_accepts_document_instance(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_parse_invalid_filter_expressions(self)

Test handling of invalid filter expressions

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_parse_malformed_logical_conditions(self)

Test malformed logical conditions

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_handle_exception_robustness(self)

Test exception handling for various inputs

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_build_condition_field_validation(self)

Test field validation behavior

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### MockReportRow

**Inherits from**: (none)

#### Methods

##### __init__(self, formula, ref_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| formula | None | - | - |
| ref_code | None | - | - |




### MockReportRow

**Inherits from**: (none)

#### Methods

##### __init__(self, formula, ref_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| formula | None | - | - |
| ref_code | None | - | - |



