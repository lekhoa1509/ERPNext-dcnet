# API Reference: test_query.py

**Language**: Python

**Source**: `tests/test_query.py`

---

## Classes

### TestQuery

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### ensure_system_manager(self, user_doc, should_have: bool)

Ensure user has/doesn't have System Manager role, with cleanup to restore original state.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user_doc | None | - | - |
| should_have | bool | - | - |


##### test_multiple_tables_in_filters(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_string_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_qb_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_field_validation_select(self)

Test validation for fields in SELECT clause.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_field_validation_filters(self)

Test validation for fields used in filters (WHERE clause).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_field_validation_group_by(self)

Test validation for fields in GROUP BY clause.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_field_validation_order_by(self)

Test validation for fields in ORDER BY clause.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_aliasing(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_filters(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_or_filters(self)

Test OR filter conditions.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_nested_filters(self)

Test nested filter conditions with AND/OR logic.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_invalid_nested_filters(self)

Test invalid formats for nested filters.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_implicit_join_query(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_nestedset(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_child_field_syntax(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_build_match_conditions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_ignore_permissions_for_query(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_permlevel_fields(self)

Test permission level check when querying fields

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_child_table_access_with_select_permission(self)

Test that child table fields are inaccessible if user only has select perm on parent.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_nested_permission(self)

Test permission on nested doctypes

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_is_set_is_not_set(self)

Test is set and is not set filters

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_permission_query_condition(self)

Test permission query condition being applied from hooks and server script

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_link_field_target_permission(self)

Test that accessing link_field.target_field respects target field's permlevel.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_filter_direct_field_permission(self)

Test that filtering is only allowed on permitted direct fields.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_filter_linked_field_permission(self)

Test that filtering is only allowed on permitted linked fields.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_dynamic_fields_in_group_by(self)

Test dynamic field support in GROUP BY clause.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_dynamic_fields_in_order_by(self)

Test dynamic field support in ORDER BY clause.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_multiple_dynamic_fields_group_order(self)

Test multiple dynamic fields in GROUP BY and ORDER BY.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_group_by_order_by_permission_checks(self)

Test permission checks for dynamic fields in GROUP BY and ORDER BY.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_child_table_group_by_order_by_permissions(self)

Test permission checks for child table fields in GROUP BY and ORDER BY.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_group_by_order_by_validation_errors(self)

Test validation errors for invalid GROUP BY and ORDER BY fields.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backtick_rejection_group_order(self)

Test that malformed backticks are properly rejected in GROUP BY and ORDER BY.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sql_functions_in_fields(self)

Test SQL function support in fields with various syntaxes.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_arithmetic_operators_in_fields(self)

Test arithmetic operator support in fields.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_not_equal_condition_on_none(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_field_alias_in_group_by(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_field_alias_permission_check(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_between_datetime_expansion(self)

Test that date strings are expanded to datetime ranges for Datetime fields with 'between' operator

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_timespan_datetime_expansion(self)

Test that timespan operator expands dates to datetime ranges for Datetime fields

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_share_only_access(self)

Test that shared docs grant access when user has no role permissions.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_if_owner_constraint_with_shared_docs(self)

Test that shared docs trump if_owner constraint.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_user_permission_with_shared_docs(self)

Test that shared docs grant access even when user permission doesn't match.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_role_permission_without_restrictions(self)

Test that all documents are accessible when role permissions exist without if_owner/user_perms.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_child_table_permission_uses_parent_doctype(self)

Test that child table queries use parent doctype for permission checks.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_child_table_filters_orphaned_rows(self)

Test that child table queries filter out orphaned rows (rows without valid parent).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_child_table_of_single_doctype(self)

Test querying child tables whose parent is a Single doctype.

Single doctypes don't have physical tables, so we can't join to them.
This tests that the query works correctly without the join.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_child_table_of_single_doctype_without_permission(self)

Test that permission checks work for child tables of Single doctypes.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_combined_raw_criterion_precedence(self)

Test that CombinedRawCriterion properly groups OR conditions.

When permission conditions (like permission_query_conditions) are combined with
shared docs via OR, the entire expression must be wrapped in parentheses to
ensure correct operator precedence with other WHERE filters.

Without proper grouping:
  WHERE filter=X AND perm_cond OR shared_cond  -- shared_cond ignores filter!

With proper grouping:
  WHERE filter=X AND (perm_cond OR shared_cond)  -- correct behavior

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_permission_query_conditions_with_filter(self)

Test that filters work correctly when permission_query_conditions and shares exist.

This is a regression test for the CombinedRawCriterion fix - ensures that
explicit filters are not bypassed by shared doc conditions.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_tree_docs()

**Returns**: (none)



### test_permission_hook_condition(user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |

**Returns**: (none)


