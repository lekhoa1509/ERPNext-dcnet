# Unstuck Reference — 5 Lateral Thinking Personas

## Persona Details

### 1. HACKER

**Mindset:** "Rules are obstacles to route around, not walls to stop at."

**Process:**
1. List every constraint being followed
2. Question each: which are real? which are assumed?
3. Look for edge cases and bypasses
4. Consider solving a different problem entirely

**Typical Reframes:**
- "Must use ERPNext workflow" → What if a simple status field + permissions is enough?
- "Need custom DocType" → What if Custom Field on existing DocType works?
- "API requires auth" → Can we cache the response?
- "Database too slow" → What if we precompute into a summary table?

---

### 2. RESEARCHER

**Mindset:** "Most blocks exist because we're missing information."

**Process:**
1. Define what's UNKNOWN (not what's known)
2. Gather evidence: source code > docs > Stack Overflow
3. Read error messages literally (they usually say what's wrong)
4. Form a hypothesis, then verify

**Investigation Checklist for DCNET:**
- [ ] Read ERPNext source code for the relevant DocType controller
- [ ] Check `docs/erpnext-flows/` for existing flow analysis
- [ ] Test manually on Desk UI first
- [ ] Run `bench console` and inspect actual data
- [ ] Check `docs/feature/` spec for exact customer wording
- [ ] Search frappe/erpnext GitHub issues

---

### 3. SIMPLIFIER

**Mindset:** "Every requirement should be questioned, every abstraction justified."

**Process:**
1. List every component involved
2. Challenge each: is it truly necessary?
3. Find the MINIMUM that solves the core problem
4. Ask: "What's the simplest thing that could possibly work?"

**Simplification Patterns for DCNET:**
| Complex | Simple |
|---------|--------|
| Custom DocType + Controller + API | Custom Field + Client Script |
| Server Script + Webhook | doc_events in hooks.py |
| Multi-level approval workflow | Single approve permission |
| Custom report page | Script Report |
| Real-time sync | Scheduled batch job |
| Custom print format | Standard with CSS override |

---

### 4. ARCHITECT

**Mindset:** "If you're fighting the architecture, the architecture is wrong."

**Process:**
1. Identify structural symptoms (same bug recurring, simple change = many files)
2. Map current structure and coupling points
3. Find root misalignment (which abstraction doesn't match reality?)
4. Propose minimal restructuring with clear migration path

**Structural Smells in DCNET:**
- hooks.py growing uncontrollably → Need module-level organization
- Same validation logic in 3 places → Missing shared utility
- Custom field naming conflicts → Need namespace convention
- install.py too complex → Need idempotent setup functions
- Fixtures load order brittle → Need dependency declaration

---

### 5. CONTRARIAN

**Mindset:** "The opposite of a great truth is often another great truth."

**Process:**
1. List every assumption (especially "obvious" ones)
2. Consider the exact opposite of each
3. Challenge the problem statement itself
4. Ask: "What happens if we do nothing?"

**Assumption Inversions for DCNET:**
| Assumption | Inversion | Insight |
|------------|-----------|---------|
| "Need custom module" | "ERPNext already has it" | Check MODULE_GAP_ANALYSIS.md first |
| "Must match spec exactly" | "Spec may be wrong" | Add to CLARIFY.md |
| "Both companies need same feature" | "Maybe only TM/NM needs it" | Check scope in spec |
| "Must build before deadline" | "Can demo with mock data" | Fixtures-first approach |
| "Code first, test later" | "Test first, code follows" | Use TDD skill |
| "Custom field solves it" | "Maybe it's a workflow issue" | Redesign process, not form |

---

## Quick Decision: Which Persona?

```
What's the symptom?
│
├─ "I've been going back and forth"     → CONTRARIAN
│   (oscillating between options)
│
├─ "There's too much to do"            → SIMPLIFIER
│   (overwhelmed by scope)
│
├─ "I don't understand how X works"    → RESEARCHER
│   (missing knowledge)
│
├─ "I keep overthinking this"          → HACKER
│   (paralyzed by perfection)
│
├─ "Every fix creates a new bug"       → ARCHITECT
│   (structural problem)
│
└─ "I literally don't know"            → RESEARCHER first,
    (no idea)                            then CONTRARIAN
```
