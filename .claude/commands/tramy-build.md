# /build - Implement Solution

Build: $ARGUMENTS

## Purpose
Write code, queries, or create artifacts based on a plan.

## Process

### 1. Review Requirements
- What exactly needs to be built?
- What inputs are available?
- What output format is expected?

### 2. Implementation
- Write clean, readable code
- Add comments for complex logic
- Handle edge cases
- Follow best practices

### 3. Validation
- Test with sample data
- Check edge cases
- Verify output format

### 4. Documentation
- Add inline comments
- Document usage
- Note any limitations

## Output Standards

### SQL Queries
```sql
-- Purpose: [What this query does]
-- Author: DA Toolkit
-- Date: [Current date]

WITH base_data AS (
    -- Step 1: [Description]
    SELECT ...
),
aggregated AS (
    -- Step 2: [Description]
    SELECT ...
)
SELECT
    column1,
    column2,
    -- Calculate metric
    SUM(value) AS total_value
FROM aggregated
GROUP BY 1, 2
ORDER BY total_value DESC;
```

### Python Code
```python
"""
Purpose: [What this script does]
Author: DA Toolkit
"""

import pandas as pd
import numpy as np

def main():
    # Step 1: Load data
    df = load_data()

    # Step 2: Transform
    df = transform_data(df)

    # Step 3: Output
    return df

if __name__ == "__main__":
    result = main()
```

## Examples
- `/build SQL query for monthly active users`
- `/build Python script to clean customer data`
- `/build cohort analysis notebook`

## After Completion
Update CLAUDE.md with new knowledge:
1. Add created files/scripts to "## Project Files" section
2. Document any reusable code patterns or utilities
3. Note important implementation details for future reference
