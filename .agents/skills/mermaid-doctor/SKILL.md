---
name: mermaid-doctor
description: |
  Validate and auto-fix Mermaid diagrams in Markdown files.
  Diagnose and repair common parsing errors in stateDiagram, erDiagram, flowchart, sequenceDiagram.

  Use when:
  - User reports "Mermaid diagram error", "parse error on line X"
  - User asks "/mermaid-doctor <file_path>"
  - Markdown files with mermaid blocks fail to render
  - Need to validate all diagrams in a file
  - User asks about Mermaid syntax rules

allowed-tools: Read, Grep, Glob, Edit, Bash
---

# Mermaid Doctor Skill

Auto-diagnose and fix Mermaid diagram errors in Markdown files.

## Quick Reference

```bash
# Fix single file
/mermaid-doctor docs/modules/fitting/FITTING_DIAGRAMS.md

# Validate without fixing
/mermaid-doctor --validate-only docs/erpnext-flows/ACCOUNTING_WORKFLOW.md

# Fix all diagrams in directory
/mermaid-doctor docs/modules/**/*_DIAGRAMS.md
```

---

## Topic Routing

| Error Type | Reference File | When to Read |
|------------|----------------|--------------|
| CRLF line endings | [common-errors.md](references/common-errors.md) | "Parse error", truncated text |
| Unicode in state IDs | [common-errors.md](references/common-errors.md) | stateDiagram errors |
| Unicode in ERD | [common-errors.md](references/common-errors.md) | erDiagram errors |
| Special chars in flowchart | [common-errors.md](references/common-errors.md) | `:`, `=`, `{`, `}` errors |
| Unbalanced code fences | [common-errors.md](references/common-errors.md) | Multiple diagrams fail |
| Official Mermaid syntax | [official-syntax.md](references/official-syntax.md) | Syntax questions |
| Advanced debugging | [debugging.md](references/debugging.md) | Complex multi-error files |
| Validation checklists | [validation-rules.md](references/validation-rules.md) | Pre-commit validation |

---

## Fix Workflow

### Step 1: Analyze File
```bash
# Check line endings
file <path>  # Should show "ASCII text" not "with CRLF"

# Count code fences (must be even)
grep -c '```' <path>

# Find Unicode in mermaid blocks
grep -n '[^\x00-\x7F]' <path>
```

### Step 2: Identify Issues (Priority Order)

1. **CRLF Line Endings** - Fix first, affects all diagrams
2. **Unbalanced Code Fences** - Check fence count is even
3. **ERD Duplicate Relationships** - Merge same entity-pair relationships
4. **Sequence Diagram Special Chars** - Remove `"` `+` `;;` from messages/notes
5. **Unicode in State IDs** - Replace with ASCII + labels
4. **Unicode in ERD Descriptions** - Remove or translate
5. **Special Chars in Flowchart** - Quote labels with `""`

### Step 3: Apply Fixes

See [references/common-errors.md](references/common-errors.md) for detailed fix instructions.

**Quick CRLF fix:**
```bash
perl -pi -e 's/\r\n/\n/g' <path>
```

### Step 4: Validate
```bash
# Use Mermaid Live Editor: https://mermaid.live/edit
```

---

## Quick Fixes Summary

| Error | Quick Fix |
|-------|-----------|
| Parse error on line X | Check CRLF: `perl -pi -e 's/\r\n/\n/g' file` |
| Unexpected character in state | Replace Unicode IDs with ASCII |
| Unexpected token ':' | Quote label: `["Label: Text"]` |
| Unexpected token '/' or ';' | Quote label: `["text/with/slash"]` |
| got 'IDENTIFYING' in ERD | Merge duplicate entity-pair relationships |
| got '+' in sequenceDiagram | Remove `"` `+` `;;` from messages/notes |
| Document as code block | Check fence count is even |

---

## State ID Mapping

| Vietnamese | ASCII ID |
|------------|----------|
| Moi | NEW |
| Da xac nhan | CONFIRMED |
| Dang xu ly | IN_PROGRESS |
| Hoan thanh | COMPLETED |
| Huy | CANCELLED |
| Vang mat | NO_SHOW |
| Cho duyet | PENDING_APPROVAL |

---

## Validation Checklist

- [ ] Line endings are LF (not CRLF)
- [ ] Code fence count is even
- [ ] State diagrams use ASCII IDs
- [ ] ERD has no Unicode in descriptions
- [ ] Flowchart labels with special chars are quoted

**Special chars requiring quotes:** `:` `=` `/` `;` `{` `}` `<` `>` `-` (at start) `@`

---

## Configuration

### Git (Prevent CRLF)
```bash
git config --global core.autocrlf input
echo "*.md text eol=lf" >> .gitattributes
```

### VS Code
```json
{ "files.eol": "\n" }
```

---

## References

- [references/common-errors.md](references/common-errors.md) - Detailed error fixes
- [references/official-syntax.md](references/official-syntax.md) - Mermaid syntax reference
- [references/debugging.md](references/debugging.md) - Advanced debugging
- [references/validation-rules.md](references/validation-rules.md) - Validation checklists
- https://mermaid.live/edit - Live Editor
- https://mermaid.js.org/ - Official Docs

---

**Version:** 2.0 | **Refactored:** 2026-01-16
