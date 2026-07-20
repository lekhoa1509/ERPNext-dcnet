# API Reference: financial_report_validation.py

**Language**: Python

**Source**: `doctype/financial_report_template/financial_report_validation.py`

---

## Classes

### ValidationIssue

Represents a single validation issue

**Inherits from**: (none)

#### Methods

##### __post_init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### __str__(self) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `str`




### ValidationResult

**Inherits from**: (none)

#### Methods

##### is_valid(self) → bool

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `bool`


##### has_warnings(self) → bool

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `bool`


##### error_count(self) → int

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `int`


##### warning_count(self) → int

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `int`


##### merge(self, other: 'ValidationResult') → 'ValidationResult'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| other | 'ValidationResult' | - | - |

**Returns**: `'ValidationResult'`


##### add_error(self, issue: ValidationIssue) → None

Add a critical error that prevents functionality

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| issue | ValidationIssue | - | - |

**Returns**: `None`


##### add_warning(self, issue: ValidationIssue) → None

Add a warning for recommendatory validation

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| issue | ValidationIssue | - | - |

**Returns**: `None`


##### notify_user(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`




### TemplateValidator

Main validator that orchestrates all validations

**Inherits from**: (none)

#### Methods

##### __init__(self, template)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| template | None | - | - |


##### validate(self) → ValidationResult

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `ValidationResult`




### Validator

**Inherits from**: ABC

#### Methods

##### validate(self, context: Any) → ValidationResult

**Decorators**: `@abstractmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| context | Any | - | - |

**Returns**: `ValidationResult`




### TemplateStructureValidator

**Inherits from**: Validator

#### Methods

##### validate(self, template) → ValidationResult

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| template | None | - | - |

**Returns**: `ValidationResult`


##### _validate_reference_codes(self, template) → ValidationResult

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| template | None | - | - |

**Returns**: `ValidationResult`


##### _validate_required_fields(self, template) → ValidationResult

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| template | None | - | - |

**Returns**: `ValidationResult`




### DependencyValidator

**Inherits from**: Validator

#### Methods

##### __init__(self, template)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| template | None | - | - |


##### validate(self, context = None) → ValidationResult

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| context | None | None | - |

**Returns**: `ValidationResult`


##### _build_dependency_graph(self) → dict[str, list[str]]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `dict[str, list[str]]`


##### _validate_circular_dependencies(self) → ValidationResult

Efficient cycle detection using DFS (Depth-First Search) with three-color algorithm:
- WHITE (0): unvisited node
- GRAY (1): currently being processed (on recursion stack)
- BLACK (2): fully processed

Example cycle detection:
A → B → C → A (cycle detected when A is GRAY and visited again)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `ValidationResult`


##### _validate_missing_dependencies(self) → ValidationResult

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `ValidationResult`


##### _get_row_idx(self, reference_code: str) → int | None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| reference_code | str | - | - |

**Returns**: `int | None`




### CalculationFormulaValidator

Validates calculation formulas used in Calculated Amount rows

**Inherits from**: Validator

#### Methods

##### __init__(self, reference_codes: set[str])

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| reference_codes | set[str] | - | - |


##### validate(self, row) → ValidationResult

Validate calculation formula for a single row

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |

**Returns**: `ValidationResult`


##### _preprocess_formula(self, formula: str) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| formula | str | - | - |

**Returns**: `str`


##### _are_parentheses_balanced(formula: str) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| formula | str | - | - |

**Returns**: `bool`


##### _test_formula_evaluation(self, formula: str, available_codes: list[str]) → str | None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| formula | str | - | - |
| available_codes | list[str] | - | - |

**Returns**: `str | None`




### AccountFilterValidator

Validates account filter expressions used in Account Data rows

**Inherits from**: Validator

#### Methods

##### __init__(self, account_fields: set | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| account_fields | set | None | None | - |


##### validate(self, row) → ValidationResult

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |

**Returns**: `ValidationResult`


##### _validate_filter_structure(self, filter_config, account_fields: set) → str | None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| filter_config | None | - | - |
| account_fields | set | - | - |

**Returns**: `str | None`




### FormulaValidator

**Inherits from**: Validator

#### Methods

##### __init__(self, template)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| template | None | - | - |


##### validate(self, row, account_fields: set) → ValidationResult

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| account_fields | set | - | - |

**Returns**: `ValidationResult`


##### _validate_custom_api(self, row) → ValidationResult

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |

**Returns**: `ValidationResult`




## Functions

### extract_reference_codes_from_formula(formula: str, available_codes: list[str]) → list[str]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| formula | str | - | - |
| available_codes | list[str] | - | - |

**Returns**: `list[str]`



### dfs(node, path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| node | None | - | - |
| path | None | - | - |

**Returns**: (none)


