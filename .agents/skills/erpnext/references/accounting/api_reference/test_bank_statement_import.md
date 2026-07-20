# API Reference: test_bank_statement_import.py

**Language**: Python

**Source**: `doctype/bank_statement_import/test_bank_statement_import.py`

---

## Classes

### TestBankStatementImport

Unit tests for Bank Statement Import functions

**Inherits from**: unittest.TestCase

#### Methods

##### test_preprocess_mt940_content_with_long_statement_number(self)

Test that statement numbers longer than 5 digits are truncated to last 5 digits

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_preprocess_mt940_content_with_normal_statement_number(self)

Test that statement numbers with 5 or fewer digits are unchanged

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_preprocess_mt940_content_without_sequence_number(self)

Test statement number truncation without sequence number

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_preprocess_mt940_content_multiple_occurrences(self)

Test multiple statement numbers in the same content

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_preprocess_mt940_content_edge_cases(self)

Test edge cases like empty content and content without :28C: tags

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_preprocess_mt940_content_with_full_mt940_document(self)

Test preprocessing with complete MT940 document

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_is_mt940_format_detection(self)

Test MT940 format detection function

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_preprocess_mt940_content_boundary_conditions(self)

Test boundary conditions for statement number length

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_preprocess_mt940_content_real_world_case(self)

Test with real-world MT940 content that was failing in production

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_preprocess_mt940_content_whitespace_variants(self)

Test handling of whitespace and different line endings

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



