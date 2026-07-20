# /commit - Git Commit

Commit changes: $ARGUMENTS

## Purpose
Create a well-formatted git commit with proper message.

## Process

### 1. Check Status
```bash
git status
git diff --staged
```

### 2. Stage Changes
```bash
git add <files>
# or
git add -A
```

### 3. Commit with Message
Follow conventional commit format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

## Commit Types
| Type | Description |
|------|-------------|
| feat | New feature |
| fix | Bug fix |
| docs | Documentation only |
| style | Formatting, no code change |
| refactor | Code restructuring |
| test | Adding tests |
| chore | Maintenance |
| data | Data changes (queries, notebooks) |
| analysis | Analysis work |

## Examples

### Simple commit
```bash
git commit -m "feat(analysis): add monthly revenue query"
```

### Detailed commit
```bash
git commit -m "analysis(churn): complete customer churn analysis

- Added cohort analysis for Q1 2024
- Identified top 3 churn factors
- Created retention dashboard

Closes #123"
```

## Best Practices
- Keep subject line under 50 characters
- Use imperative mood ("add" not "added")
- Reference issue numbers when applicable
- Separate subject from body with blank line

## Usage
- `/commit` - Auto-generate commit message from changes
- `/commit add revenue analysis` - Commit with custom message
