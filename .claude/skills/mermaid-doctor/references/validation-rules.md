# Mermaid Validation Rules & Checklists

> Pre-commit validation checklists and common pitfalls by diagram type.

---

## Common Pitfalls (from Official Docs)

### Flowchart Pitfalls

1. **Lowercase "end" keyword**
   ```mermaid
   flowchart TD
       A --> end  %% BREAKS SYNTAX
       A --> End  %% Works
   ```

2. **Node IDs starting with o/x**
   ```mermaid
   flowchart TD
       A---oB  %% Creates circle edge (unintended)
       A--- oB %% Space prevents issue
       A---OB  %% Capitalization prevents issue
   ```

3. **Missing direction**
   ```mermaid
   flowchart      %% No direction - ERROR
   flowchart TD   %% Has direction - OK
   ```

---

### State Diagram Pitfalls

1. **Unicode in state IDs**
   ```mermaid
   stateDiagram-v2
       Đã_xác_nhận --> Hoàn_thành  %% Unicode IDs - ERROR
       CONFIRMED --> COMPLETED      %% ASCII IDs - OK
   ```

2. **Transitions between composite internals**
   ```mermaid
   stateDiagram-v2
       state A {
           A1
       }
       state B {
           B1
       }
       A1 --> B1  %% Cannot cross composite boundaries - ERROR
   ```

---

### ERD Pitfalls

1. **Incomplete relationship statements**
   ```mermaid
   erDiagram
       CUSTOMER ||--   %% Missing second entity - ERROR
       CUSTOMER ||--|| ORDER  %% Complete - OK
   ```

2. **Invalid cardinality**
   ```mermaid
   erDiagram
       A =>=> B   %% Invalid notation - ERROR
       A ||--o{ B %% Valid notation - OK
   ```

3. **Quotes in descriptions**
   ```mermaid
   erDiagram
       ENTITY {
           string name "Can't use quotes"  %% ERROR
           string name "Cannot use quotes" %% OK
       }
   ```

---

### Sequence Diagram Pitfalls

1. **Destroyed participant without message (v10.6.1)**
   ```
   Error: The destroyed participant does not have
   an associated destroying message
   ```
   **Solution:** Update to v10.7.0+

2. **Invalid arrow syntax**
   ```mermaid
   sequenceDiagram
       A=>B: Message   %% Invalid arrow - ERROR
       A->>B: Message  %% Valid arrow - OK
   ```

---

## Diagram-Specific Validation Checklists

### State Diagram Checklist

- [ ] Starts with `stateDiagram-v2`
- [ ] All state IDs are ASCII (no Unicode)
- [ ] Has start state `[*] -->`
- [ ] Has end state `--> [*]`
- [ ] Transitions use `-->` syntax
- [ ] Labels use `: Label text` syntax
- [ ] No transitions between different composite internals
- [ ] Comments use `%%` prefix

---

### ERD Checklist

- [ ] Starts with `erDiagram`
- [ ] Valid cardinality: `||`, `|o`, `}o`, `}|`
- [ ] Valid identification: `--` or `..`
- [ ] Entity names valid (or quoted if spaces)
- [ ] Attribute format: `type name [key] ["comment"]`
- [ ] Keys are valid: `PK`, `FK`, `UK`
- [ ] No quotes within quoted descriptions
- [ ] Type format valid (alpha + digits/dashes/underscores)
- [ ] **No duplicate relationships** between the same entity pair

---

### Flowchart Checklist

- [ ] Starts with `flowchart` or `graph`
- [ ] Direction declared: `TB`, `TD`, `BT`, `RL`, `LR`
- [ ] No lowercase `end` keywords
- [ ] Node IDs starting with `o`/`x` have space or capitals
- [ ] **Labels with special chars quoted:** `:`, `=`, `/`, `;`, `{`, `}`, `<`, `>`, `-` at start
- [ ] Link text with special chars quoted
- [ ] Valid arrow syntax: `-->`, `---`, `-.->`, `==>`
- [ ] Subgraphs properly closed with `end`

---

### Sequence Diagram Checklist

- [ ] Starts with `sequenceDiagram`
- [ ] Valid arrow types used
- [ ] Activations balanced (`activate`/`deactivate`)
- [ ] Control flow blocks closed (`end`)
- [ ] Participant types valid
- [ ] No destroyed participants without messages (v10.7.0+)
- [ ] **No `"` (double quotes)** in message text or Note content
- [ ] **No `+` (plus)** in Note content (activation marker)
- [ ] **No `;;` (double semicolon)** in messages/notes (statement separator)

---

## General Pre-Commit Checklist

### File Level
- [ ] Line endings are LF (not CRLF)
- [ ] Code fence count is even (balanced)
- [ ] No orphaned closing fences
- [ ] File does not end with ```

### Diagram Level
- [ ] Each diagram has correct type declaration
- [ ] No Unicode in identifiers (IDs)
- [ ] Special characters properly quoted
- [ ] All syntax follows diagram-specific rules

### Testing
- [ ] All diagrams render in Mermaid Live Editor
- [ ] No parse errors in console
- [ ] Visual output matches expected design

---

## Quick Validation Commands

```bash
# Check line endings
file <path>

# Count code fences (must be even)
grep -c '```' <path>

# Find Unicode characters
grep -n '[^\x00-\x7F]' <path>

# List all mermaid blocks
grep -n '```mermaid' <path>

# Check for unquoted special chars in flowcharts
grep -n '\[.*[:={}].*\]' <path> | grep -v '"\|"'
```

---

## Best Practices Summary

### DO ✅

1. **State Diagrams:**
   - Use ASCII IDs: `NEW`, `CONFIRMED`, `COMPLETED`
   - Add labels separately: `NEW: Mới`
   - Keep transitions clean

2. **ERD Diagrams:**
   - Keep entity/field names ASCII
   - Remove or simplify descriptions
   - Use external table for Vietnamese docs

3. **Line Endings:**
   - Always use Unix (LF)
   - Configure git autocrlf
   - Set editor default to LF

4. **Code Fences:**
   - Always close opened fences
   - Use consistent fence style (```)
   - Check balance before commit

### DON'T ❌

1. **State Diagrams:**
   - Don't use Unicode in state IDs: `Đã_xác_nhận`
   - Don't mix languages in IDs
   - Don't use special chars: `:`, `/`, `@`

2. **ERD Diagrams:**
   - Don't use Unicode in descriptions: `"Người thực hiện"`
   - Don't use special chars in field names
   - Don't over-complicate with too many descriptions

3. **General:**
   - Don't copy-paste from Windows editors
   - Don't leave orphaned fences
   - Don't skip validation

---

## Configuration for Prevention

### Git Settings
```bash
git config --global core.autocrlf input
git config --global core.eol lf
echo "*.md text eol=lf" >> .gitattributes
```

### VS Code Settings
```json
{
  "files.eol": "\n",
  "files.insertFinalNewline": true,
  "files.trimTrailingWhitespace": true,
  "[markdown]": {
    "files.eol": "\n"
  }
}
```

### EditorConfig
```ini
# .editorconfig
[*.md]
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
```

---

**Last Updated:** 2026-01-16
