# /doc - Generate Documentation

Document: $ARGUMENTS

## Purpose
Create clear documentation for analysis, code, or processes.

## Documentation Types

### 1. Analysis Documentation
- Executive summary
- Methodology
- Key findings
- Recommendations

### 2. Technical Documentation
- Code comments
- README files
- API documentation
- Data dictionaries

### 3. Process Documentation
- Step-by-step guides
- Runbooks
- FAQs

## Output Formats

### Analysis Report
```markdown
# [Analysis Title]

## Executive Summary
[2-3 sentences summarizing key findings and recommendations]

## Background
[Context and business question]

## Methodology
[Data sources, approach, timeframe]

## Key Findings
### Finding 1
[Description with supporting data/visualization]

### Finding 2
[Description with supporting data/visualization]

## Recommendations
1. [Action item with expected impact]
2. [Action item with expected impact]

## Appendix
- Data sources
- SQL queries
- Assumptions
```

### Data Dictionary
```markdown
# Data Dictionary: [Table/Dataset Name]

## Overview
[Description of the dataset]

## Fields
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| id | INT | Primary key | 12345 |
| created_at | TIMESTAMP | Record creation time | 2024-01-15 10:30:00 |

## Relationships
- Joins to [other_table] on [field]

## Notes
- [Important information about the data]
```

## Examples
- `/doc this SQL query`
- `/doc the analysis we just completed`
- `/doc data dictionary for users table`

## After Completion
Update CLAUDE.md with new knowledge:
1. Add documentation references to "## Documentation" section
2. Update data dictionaries in "## Data Sources" section
3. Link to generated reports or guides
