# Advanced Mermaid Debugging Techniques

> For complex multi-error files and hard-to-find issues.

---

## Technique 1: Binary Search for Error Location

When dealing with large files:

```bash
# Step 1: Split file in half
head -n 150 original.md > half1.md
tail -n +151 original.md > half2.md

# Step 2: Test each half
# If half1 has error, split again
head -n 75 half1.md > quarter1.md
tail -n +76 half1.md > quarter2.md

# Continue until you isolate the problematic diagram
```

---

## Technique 2: Diagram Extraction & Validation

```javascript
function extractAndValidateDiagrams(filePath) {
    const content = readFile(filePath);
    const diagrams = [];

    // Extract all mermaid blocks with metadata
    const regex = /```mermaid\n([\s\S]*?)\n```/g;
    let match;

    while ((match = regex.exec(content)) !== null) {
        const diagram = {
            content: match[1],
            startLine: content.substring(0, match.index).split('\n').length,
            endLine: content.substring(0, match.index + match[0].length).split('\n').length,
            type: detectDiagramType(match[1])
        };

        diagrams.push(diagram);
    }

    // Validate each diagram
    return diagrams.map(d => ({
        ...d,
        validation: validateDiagram(d.content, d.type)
    }));
}

function detectDiagramType(content) {
    const firstLine = content.trim().split('\n')[0];

    if (/^(flowchart|graph)\s+(TB|TD|BT|RL|LR)/.test(firstLine)) return 'flowchart';
    if (/^stateDiagram-v2/.test(firstLine)) return 'stateDiagram-v2';
    if (/^erDiagram/.test(firstLine)) return 'erDiagram';
    if (/^sequenceDiagram/.test(firstLine)) return 'sequenceDiagram';
    if (/^gantt/.test(firstLine)) return 'gantt';
    if (/^classDiagram/.test(firstLine)) return 'classDiagram';

    return 'unknown';
}
```

---

## Technique 3: Character-Level Analysis

```javascript
function analyzeProblematicCharacters(diagram, diagramType) {
    const issues = [];

    // Check for CRLF
    if (diagram.includes('\r\n')) {
        issues.push({
            type: 'line_endings',
            message: 'CRLF line endings detected',
            fix: "Convert to LF: perl -pi -e 's/\\r\\n/\\n/g'"
        });
    }

    // Check for Unicode in IDs (stateDiagram)
    if (diagramType === 'stateDiagram-v2') {
        const stateIdRegex = /^\s*(\S+)\s*-->/gm;
        let match;
        while ((match = stateIdRegex.exec(diagram)) !== null) {
            const stateId = match[1];
            if (/[^\x00-\x7F]/.test(stateId) && stateId !== '[*]') {
                issues.push({
                    type: 'unicode_state_id',
                    stateId: stateId,
                    message: `State ID contains Unicode: ${stateId}`,
                    fix: 'Replace with ASCII ID and add label'
                });
            }
        }
    }

    // Check for problematic characters in ERD
    if (diagramType === 'erDiagram') {
        const attributeRegex = /^\s*\w+\s+\w+\s+"([^"]*)"/gm;
        let match;
        while ((match = attributeRegex.exec(diagram)) !== null) {
            const description = match[1];
            if (/[^\x00-\x7F]/.test(description)) {
                issues.push({
                    type: 'unicode_erd_description',
                    description: description,
                    message: `ERD description contains Unicode: "${description}"`,
                    fix: 'Remove description or use ASCII'
                });
            }
        }
    }

    // Check for reserved words (flowchart)
    if (diagramType === 'flowchart') {
        if (/\bend\b/g.test(diagram)) {
            issues.push({
                type: 'reserved_word',
                word: 'end',
                message: 'Reserved word "end" found (must be capitalized)',
                fix: 'Replace "end" with "End" or "END"'
            });
        }

        // Check for problematic node IDs starting with o/x
        const nodeRegex = /---([ox])\w+/g;
        let match;
        while ((match = nodeRegex.exec(diagram)) !== null) {
            issues.push({
                type: 'problematic_node_id',
                nodeId: match[0],
                message: `Node starting with "${match[1]}" creates edge`,
                fix: `Add space: "--- ${match[1]}..." or capitalize`
            });
        }
    }

    return issues;
}
```

---

## Technique 4: Incremental Validation

```javascript
function incrementalValidation(diagram) {
    const lines = diagram.split('\n');
    const errors = [];

    // Validate line by line
    for (let i = 0; i < lines.length; i++) {
        const partialDiagram = lines.slice(0, i + 1).join('\n');

        try {
            const valid = mermaidValidate(partialDiagram);
            if (!valid) {
                errors.push({
                    line: i + 1,
                    content: lines[i],
                    message: 'Validation failed at this line'
                });
                break;
            }
        } catch (error) {
            errors.push({
                line: i + 1,
                content: lines[i],
                error: error.message
            });
            break;
        }
    }

    return errors;
}
```

---

## Technique 5: Syntax Pattern Matching

```javascript
function validateSyntaxPatterns(diagram, diagramType) {
    const validators = {
        'stateDiagram-v2': [
            {
                pattern: /^\s*stateDiagram-v2\s*$/m,
                required: true,
                message: 'Must start with stateDiagram-v2'
            },
            {
                pattern: /^\s*\[?\*\]?\s*-->/m,
                message: 'Should have start state transition'
            },
            {
                pattern: /-->\s*\[?\*\]?\s*$/m,
                message: 'Should have end state transition'
            }
        ],
        'erDiagram': [
            {
                pattern: /^\s*erDiagram\s*$/m,
                required: true,
                message: 'Must start with erDiagram'
            },
            {
                pattern: /\w+\s+(\|\|--|\|o--|o\|--|}o--|}\|--)/,
                message: 'Should have valid relationships'
            },
            {
                pattern: /\w+\s+\{[\s\S]*?\}/,
                message: 'Should have entity definitions'
            }
        ],
        'flowchart': [
            {
                pattern: /^(flowchart|graph)\s+(TB|TD|BT|RL|LR)/m,
                required: true,
                message: 'Must declare direction: TB, TD, BT, RL, or LR'
            },
            {
                pattern: /\w+\s*--+>/,
                message: 'Should have connections'
            }
        ],
        'sequenceDiagram': [
            {
                pattern: /^\s*sequenceDiagram\s*$/m,
                required: true,
                message: 'Must start with sequenceDiagram'
            },
            {
                pattern: /\w+\s*-+[>x)]]+\s*\w+:/,
                message: 'Should have message arrows'
            }
        ]
    };

    const rules = validators[diagramType] || [];
    return rules.map(rule => ({
        pattern: rule.pattern.toString(),
        matches: rule.pattern.test(diagram),
        required: rule.required || false,
        message: rule.message
    }));
}
```

---

## Diagnostic Report Template

```markdown
# Mermaid Diagnostic Report
**File:** {file_path}
**Date:** {date}

## Summary
- Total diagrams: {count}
- Valid: {valid_count}
- Errors: {error_count}

## Issues Found

### 1. Line Endings
- **Status:** {CRLF | LF}
- **Action:** {Convert CRLF to LF | OK}

### 2. Code Fences
- **Total fences:** {count}
- **Status:** {Balanced | Unbalanced}
- **Orphaned fences:** {locations}

### 3. State Diagrams
- **Count:** {count}
- **Unicode state IDs:** {list}
- **Fix:** Replace with ASCII IDs

### 4. ERD Diagrams
- **Count:** {count}
- **Unicode fields:** {list}
- **Fix:** Remove descriptions

## Validation Results

| Diagram | Type | Line | Status |
|---------|------|------|--------|
| Workflow | flowchart | 28 | Valid |
| State Machine | stateDiagram-v2 | 54 | Error |
| ERD | erDiagram | 91 | Error |

## Recommended Actions

1. Fix line endings (affects all diagrams)
2. Remove orphaned code fences
3. State diagrams: Replace Unicode IDs
4. ERD diagrams: Remove Unicode descriptions
```

---

**Last Updated:** 2026-01-16
