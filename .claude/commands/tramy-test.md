# /tramy-test - Business Logic Validation

Test: $ARGUMENTS

## Purpose
Validate business rules, test công thức tính toán, verify data quality, và ensure business logic correctness trong DCNET Flow system.

> **Note:** Đây là command test business logic. Để run unit tests, dùng bench commands.

## Types of Testing

### 1. Data Quality Checks
- Completeness: Are there missing values?
- Accuracy: Do values make sense?
- Consistency: Are formats uniform?
- Timeliness: Is data fresh?
- Uniqueness: Are there duplicates?

### 2. Query Validation
- Does the query return expected row count?
- Are joins correct (no unexpected multiplication)?
- Do aggregations match known totals?
- Are filters applied correctly?

### 3. Results Verification
- Do results make business sense?
- Are edge cases handled?
- Do totals reconcile?
- Are trends consistent with expectations?

## Output Format
```
## Test Report: [What was tested]

### Summary
- Status: PASS / FAIL / WARNING
- Items tested: [Count]
- Issues found: [Count]

### Data Quality Checks
| Check | Status | Details |
|-------|--------|---------|
| Null values | PASS/FAIL | [Details] |
| Duplicates | PASS/FAIL | [Details] |
| Value ranges | PASS/FAIL | [Details] |

### Validation Results
| Test | Expected | Actual | Status |
|------|----------|--------|--------|
| Row count | X | Y | PASS/FAIL |
| Total sum | X | Y | PASS/FAIL |

### Issues Found
1. [Issue description and severity]
2. [Issue description and severity]

### Recommendations
- [Action to take]
```

## Example Queries

### Check for nulls
```sql
SELECT
    COUNT(*) AS total_rows,
    COUNT(column1) AS non_null_col1,
    COUNT(*) - COUNT(column1) AS null_col1
FROM table_name;
```

### Check for duplicates
```sql
SELECT
    id,
    COUNT(*) AS cnt
FROM table_name
GROUP BY id
HAVING COUNT(*) > 1;
```

## Examples (ERP-specific)
- `/tramy-test pricing calculation with volume discounts`
- `/tramy-test GST calculation on Sales Order`
- `/tramy-test credit limit validation for customer`
- `/tramy-test duplicate detection logic for leads`
- `/tramy-test state transitions for Purchase Order workflow`
- `/tramy-test data quality in Item Master`

## After Completion
Update CLAUDE.md with new knowledge:
1. Add data quality findings to "## Data Quality" section
2. Document known issues and their status
3. Note validation rules for future reference
