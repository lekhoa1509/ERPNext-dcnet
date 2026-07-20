# /tramy-analyze - Business Analysis for ERP

Analyze: $ARGUMENTS

## Purpose
Phân tích nghiệp vụ, workflows, business logic, và data patterns trong hệ thống DCNET Flow.

> **Note:** Đây là command phân tích nghiệp vụ. Để planning development tasks, dùng `/plan`

## Process

### 1. Clarify the Question
- What is the business/technical question?
- What decisions will this analysis inform?
- Who is the audience?

### 2. Data Discovery
- Identify relevant data sources
- Understand data schema and relationships
- Check data quality and completeness

### 3. Exploratory Analysis
- Summary statistics
- Distributions and patterns
- Anomalies and outliers
- Key metrics

### 4. Initial Findings
- What patterns emerge?
- What hypotheses can we form?
- What additional data might be needed?

## Output Format
```
## Analysis: [Topic]

### Question
[Business/technical question being addressed]

### Data Sources
- [Source 1]: [Description, key fields]
- [Source 2]: [Description, key fields]

### Key Findings
1. [Finding 1 with supporting data]
2. [Finding 2 with supporting data]
3. [Finding 3 with supporting data]

### Data Quality Notes
- [Any issues or limitations]

### Next Steps
- [Recommended follow-up analysis or actions]
```

## Examples (ERP-specific)
- `/tramy-analyze Lead to Sales Order workflow`
- `/tramy-analyze pricing calculation logic for wholesale vs retail`
- `/tramy-analyze CRM Deal to Customer sync integration`
- `/tramy-analyze credit management approval workflow`
- `/tramy-analyze shipment tracking data flow`

## After Completion
Update CLAUDE.md with new knowledge:
1. Add discovered data sources to "## Data Sources" section
2. Add key findings to "## Project Knowledge" section
3. Document any important patterns or insights learned
