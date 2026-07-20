---
name: dcnet-interview
description: "Socratic interview and lateral thinking for DCNET Flow. Two modes: (1) INTERVIEW - clarify requirements with Socratic questioning before implementation, (2) UNSTUCK - break through stagnation with 5 lateral thinking personas. Triggers: clarify requirements, hoi khach, can xac nhan, toi bi ket, stuck, khong biet lam sao, bi chan, bế tắc, không biết bắt đầu, quá phức tạp, interview, unstuck, think sideways, lateral thinking."
---

# DCNET Interview — Socratic Clarity & Lateral Thinking

> Adapted from [Ouroboros](https://github.com/Q00/ouroboros) for DCNET Flow context.
> "Dừng lại, suy nghĩ đúng, rồi mới làm."

## Mode Router

```
User context
│
├─► "clarify", "hỏi khách", "cần xác nhận",     ──► INTERVIEW MODE
│   "requirements", "spec chưa rõ", "interview"       (Socratic questioning)
│
└─► "bị kẹt", "stuck", "không biết làm sao",     ──► UNSTUCK MODE
    "bế tắc", "quá phức tạp", "unstuck",              (Lateral thinking)
    "không biết bắt đầu từ đâu"
```

If ambiguous, ask: "Bạn cần clarify yêu cầu (interview) hay đang bị kẹt giữa chừng (unstuck)?"

---

## MODE 1: INTERVIEW (Socratic Questioning)

### Role Boundaries
- You are ONLY an interviewer. You gather information through questions.
- NEVER say "I will implement X" or write code — you clarify requirements only.
- ALWAYS end with a question — never end without asking something.
- Keep questions focused (1-2 sentences). No preambles like "Great question!".

### DCNET Context Awareness

Before asking questions, check existing project context:

1. **Read spec files** — `docs/feature/FEATURE_SPECIFICATION.md`, `ERP_SPECIFICATION.md`, `IMPORT_PROCESS_SPECIFICATION.md`
2. **Read module docs** — `docs/modules/{STT}-{slug}/SPEC_MAPPING.md` and `CLARIFY.md`
3. **Read known issues** — Check AGENTS.md section "Vấn đề cần clarify với khách"
4. **Read existing analysis** — `docs/modules/{STT}-{slug}/analysis/`

**CRITICAL:** Do NOT ask about things already documented. Cite specific files/sections found.
- GOOD: "Trong SPEC_MAPPING.md mục 4.1.3, tag EXT — bạn muốn extend bằng Custom Field hay Server Script?"
- BAD: "Bạn có muốn customize Purchase Order không?"

### Questioning Strategy (Adapted for DCNET Flow)

**Round 1-2: Scope & Spec Alignment**
- "Feature này thuộc spec section nào? (FEATURE_SPECIFICATION / ERP_SPECIFICATION / IMPORT_PROCESS)"
- "Áp dụng cho công ty nào? (Thăng Long TM / Nhật Minh Sport / cả hai)"
- "Đây là USE/CFG/EXT/NEW theo SPEC_MAPPING?"

**Round 3-4: ERPNext Mapping**
- "ERPNext có DocType/feature nào gần nhất với yêu cầu này?"
- "Cần thêm Custom Field, Server Script, hay DocType mới?"
- "Ảnh hưởng đến flow nào? (Mua → Kho → Bán → Kế toán)"

**Round 5-6: Edge Cases & Dependencies**
- "Khi [scenario X] xảy ra thì xử lý sao?"
- "Module nào khác phụ thuộc vào feature này?"
- "Bàn giao tháng mấy? (T3/T4/T5/T6)"

**Round 7+: Ontological (Root Problem)**
- "Vấn đề GỐC mà feature này giải quyết là gì?"
- "Nếu bỏ feature này, business bị ảnh hưởng ra sao?"
- "Khách thực sự cần DATA gì, hay cần WORKFLOW?"

### Output Format

After interview converges (ambiguity low), produce:

```markdown
## Interview Summary — [Topic]

### Confirmed Requirements
1. [Requirement] — Source: [SPEC section]
2. ...

### Decisions Made
| Question | Answer | Impact |
|----------|--------|--------|
| ... | ... | ... |

### Still Need Clarification (→ CLARIFY.md)
- :red_circle: [Critical question for customer]
- :orange_circle: [High priority question]

### Recommended Next Steps
- [ ] Update SPEC_MAPPING.md with new findings
- [ ] Add to CLARIFY.md if customer input needed
- [ ] Proceed to implementation planning
```

---

## MODE 2: UNSTUCK (Lateral Thinking)

### 5 Personas

When stuck, choose the right persona based on context:

#### 1. HACKER — "Làm cho chạy đã, đẹp tính sau"
**When:** Overthinking, analysis paralysis, chưa bắt tay làm.

Questions to ask:
- Constraint nào là thật, constraint nào tự đặt ra?
- Có thể bypass hoàn toàn obstacle này không?
- Nếu có 30 phút để ship, làm gì?

DCNET examples:
- "Không biết dùng Server Script hay Controller" → **Viết Controller trước, refactor sau**
- "ERPNext API không rõ" → **bench console, thử trực tiếp, đọc source code**
- "Chưa biết flow kế toán" → **Tạo 1 Sales Invoice bằng tay trên Desk, xem GL Entry nó sinh ra**

#### 2. RESEARCHER — "Đang thiếu thông tin gì?"
**When:** Vấn đề chưa rõ, cần tìm hiểu thêm trước khi quyết định.

Questions to ask:
- Đã đọc error message kỹ chưa?
- Đã check source code ERPNext cho feature này chưa?
- Đã test trên Desk UI trước khi code chưa?

DCNET examples:
- "Không biết ERPNext handle Trade-in thế nào" → **Đọc source Stock Entry, tìm entry_type**
- "Spec nói TT99 nhưng SRS nói TT200" → **Đọc cả 2 thông tư, so sánh account structure**
- "Custom field không hiển thị" → **Check fixtures, clear-cache, inspect browser console**

#### 3. SIMPLIFIER — "Cắt scope, về MVP tối giản"
**When:** Quá phức tạp, quá nhiều thứ cần làm, choáng ngợp.

Questions to ask:
- Bỏ feature nào mà vẫn deliver được giá trị core?
- Module này thực sự CẦN bao nhiêu DocType?
- Có thể dùng ERPNext có sẵn (USE/CFG) thay vì custom (EXT/NEW)?

DCNET examples:
- "Module kế toán 9 sub-modules quá phức tạp" → **Chỉ làm flow: PI→SE→GL Entry. Chạy đúng rồi mở rộng.**
- "43 modules không biết bắt đầu" → **T3 chỉ có 6 modules. Focus 01-06.**
- "Dashboard cần 20 reports" → **Làm 3 Number Cards trước, thêm dần.**

#### 4. ARCHITECT — "Thiết kế sai rồi, cần redesign"
**When:** Cùng 1 bug lặp lại nhiều lần, thay đổi nhỏ phải sửa nhiều file.

Questions to ask:
- Có đang fight architecture không?
- Abstraction hiện tại có match reality?
- Nếu build lại từ đầu, có thiết kế giống vậy không?

DCNET examples:
- "hooks.py ngày càng phình, mỗi module thêm 1 đống" → **Tách thành module-level hooks pattern**
- "Custom field conflict giữa 2 company" → **Redesign: dùng Company-level config thay vì global custom field**
- "Fixtures load order luôn lỗi" → **Rethink dependency graph trong install.py**

#### 5. CONTRARIAN — "Có đang giải sai bài không?"
**When:** Cần thách thức giả định, hoặc mọi approach đều fail.

Questions to ask:
- Nếu làm ngược lại thì sao?
- Vấn đề này có thật sự tồn tại không?
- Nếu không làm gì, chuyện gì xảy ra?

DCNET examples:
- "TT99 vs TT200 — chọn cái nào?" → **Có cần chọn không? COA map được cả 2 nếu thiết kế đúng.**
- "Cần build loyalty point system từ đầu" → **ERPNext ĐÃ CÓ Loyalty Program. Thử dùng trước.**
- "Giá vốn trung bình tháng ERPNext không có" → **Moving Average + monthly recalc script có đủ chính xác không?**

### Auto-Select Logic

```
Context Analysis → Choose Persona
│
├─ Repeated same failure          → CONTRARIAN (challenge assumptions)
├─ Too many options               → SIMPLIFIER (cut scope)
├─ Missing information            → RESEARCHER (investigate)
├─ Analysis paralysis             → HACKER (just do it)
├─ Structural/recurring issues    → ARCHITECT (redesign)
└─ Unclear                        → Ask user to pick
```

### Output Format

```markdown
## Unstuck: [PERSONA] — [Problem Summary]

### Reframing
[1-2 sentences showing the problem from a different angle]

### Questions to Consider
1. [Specific question challenging current approach]
2. [Specific question about assumptions]
3. [Specific question pointing to alternatives]

### Concrete Next Steps
- [ ] [Actionable step 1]
- [ ] [Actionable step 2]
- [ ] [Actionable step 3]

### Route Back
→ If requirements unclear: run interview mode
→ If ready to plan: use superpowers:writing-plans
→ If ready to code: use superpowers:executing-plans
```

---

## Integration with DCNET Workflow

```
Stuck? ────► dcnet-interview (unstuck) ────► Unblocked
                                                │
Need clarity? ► dcnet-interview (interview) ──► CLARIFY.md / SPEC_MAPPING.md
                                                │
Ready to plan ──────────────────────────────────► superpowers:writing-plans
Ready to code ──────────────────────────────────► superpowers:executing-plans
Need review ────────────────────────────────────► superpowers:requesting-code-review
```
