# Contract + PAKD form UX redesign

> **Phase 7 (Commission UX gaps)** added 2026-05-12 after Playwright QA — see §14 at bottom. Phases 1–6 are complete and verified visually; Phase 7 captures 4 new business-logic gaps surfaced by user review.


**Date:** 2026-05-12
**Scope:** `dcnet_contract` + `dcnet_pakd` + `vn_accounting` (sidebar/dashboard) + `vn_help` + `vn_translation`
**Ship mode:** One bundled feature branch (all 6 work-streams together)
**Affected forms:** DCNET Contract, Phuong An Kinh Doanh
**Status:** Design — awaiting user review before invoking writing-plans

---

## 1. Context

The DCNET Contract (`HD-...`) and PAKD (`PAKD-...`) forms have evolved through many rounds of point-fix feedback. Recent fixes addressed label translations, auto-sync from Contract → PAKD, drift detection, related-transactions section, billing-schedule color coding. But the underlying form layout, section organization, and inline guidance are still not intuitive:

- Sections aren't grouped by business mental model — Status sits at #12 of 13 on Contract, #5 of 5 on PAKD
- Almost no fields have descriptions — users guess what they mean
- The Contract → PAKD → Billing Schedule → Sales Invoice → Payment relationship isn't visually obvious
- vn_accounting workspace surfaces Contract/PAKD as flat list links — no portfolio health view

This redesign is a holistic UX pass anchored in real business decisions, not visual polish.

## 2. Personas + business decisions

All 4 personas in scope:

| Persona | Primary form | Business decision the form must enable |
|---|---|---|
| Sales rep / NVKD | PAKD (creates), Contract (references) | "Will my commission post? Was my PAKD approved/rejected and why?" |
| Sales director / GĐKD | PAKD (reviews + approves) | "Is this PAKD's margin acceptable to approve?" |
| Accountant / Kế toán | Contract (operates billing schedule + invoices) | "Which billings due/overdue this period, what's outstanding?" |
| Accounting manager / KTT | Both (cross-contract audit) | "Drift between PAKD and Contract? Revenue at risk? Period close ready?" |

## 3. Decisions locked during brainstorming

| Decision | Choice |
|---|---|
| Ship mode | One bundled feature branch (all 6 work-streams) |
| Header style | Role-agnostic, single card showing all key info per form |
| Reminder button | Email-only Frappe-native reminder, ships in Round 1 |
| Snapshot semantics | Card subtitle shows "Thông tin KH chốt lúc ký HD: {contract_date}" |
| Bên A / Bên B section | Closed by default |
| Kỹ thuật auto-collapse | Auto-collapse based on `service_type` (FTTH HGD / VTTB / Thi công → closed; others → open) |
| Margin thresholds | New DCNET PAKD Settings DocType (margin_green_threshold, margin_amber_threshold) |
| DCNET PAKD Settings | Appears under vn_accounting sidebar "Cài đặt" group |

## 4. Work-stream 1 — At-a-glance summary header

A new top-of-form HTML section before any other section. Frappe HTML field rendered by JS on `refresh()`. One server endpoint per form returns aggregates.

### Server endpoints

```
dcnet_contract.api.get_summary_kpis(contract_name) -> dict
dcnet_pakd.api.get_summary_kpis(pakd_name) -> dict
```

Returns: status info, KPI values, next-action prompt + button payload.

### Schema change

Add ONE Section Break (`fieldname=summary_section`, no label, `print_hide=1`) + ONE HTML field (`fieldname=summary_card`, `read_only=1`) at the top of `field_order` for each form. No new DocTypes, no migration.

### Contract card layout

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ ● ĐANG HOẠT ĐỘNG  ·  Định kỳ  ·  ILL                                         │
│ Khách: CÔNG TY ABC  ·  HD-2026-00156  ·  NVKD: Nguyễn A  ·  CN: HCM          │
│ Thông tin KH chốt lúc ký HD: 01/04/2026                                      │
├──────────────────────────────────────────────────────────────────────────────┤
│ Giá trị HĐ        Đã xuất HĐ      Đã thu        Còn nợ       Quá hạn        │
│  156.000.000 ₫     24.000.000 ₫    18.000.000 ₫  6.000.000 ₫   0 kỳ         │
├──────────────────────────────────────────────────────────────────────────────┤
│ Hiệu lực: 01/04/2026 → 31/03/2027 (còn 10 tháng)                             │
│ ► Việc cần làm: Xuất hoá đơn kỳ T5/2026 (đến hạn 31/05)  [Tạo hoá đơn]      │
└──────────────────────────────────────────────────────────────────────────────┘
```

### PAKD card layout

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ ● CHỜ GĐ KINH DOANH DUYỆT  ·  PAKD Định kỳ  ·  HĐ: HD-2026-00156            │
│ Khách: CÔNG TY ABC  ·  NVKD: Nguyễn A  ·  CN: HCM                           │
├──────────────────────────────────────────────────────────────────────────────┤
│ DT Hợp đồng       Tổng CP         Tổng DT DV      Hoa hồng     Biên lãi     │
│  156.000.000 ₫    120.000.000 ₫   148.000.000 ₫   8.000.000 ₫   23,1%       │
├──────────────────────────────────────────────────────────────────────────────┤
│ ⚠ Hạng mục lệch so với hợp đồng — dùng nút "Cập nhật từ hợp đồng" ở trên     │
│ ► Việc cần làm: Chờ duyệt từ GĐ KD HCM (Nguyễn B)  [Nhắc duyệt]             │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Note on drift sync:** the header shows drift indicator (text + ⚠ icon) but does NOT include a sync button. The existing "Cập nhật từ hợp đồng" button (FB-2026-00503) at the Frappe action-button area is the sync entry point — users already know that location. Header is for visibility/status; action stays where it lives today.

### Next-action decision logic (Contract)

Rules evaluated top-down — first matching rule wins. Conditions combine stored `status` field with derived conditions (overdue invoices, days-to-end, etc).

| State / condition | Next action shown | Action button |
|---|---|---|
| status=Draft | "Hoàn thành thông tin → gửi duyệt" | (none) |
| status=Active AND has overdue invoice | "Theo dõi công nợ HĐ {invoice}: còn nợ {amount}" | Mở phiếu |
| status=Active AND end_date < today+60d (derived: approaching expiry) | "Hợp đồng sắp hết hạn ({days} ngày) — chuẩn bị gia hạn" | Tạo HĐ gia hạn |
| status=Active AND has projected billing row past due_date | "Xuất hoá đơn kỳ {period} (đến hạn {date})" | Tạo hoá đơn |
| status=Active AND no immediate action | "Tự động chu kỳ tiếp theo: {date}" | (none) |
| status=Suspended | "Lý do tạm ngưng: {reason}" | Kích hoạt lại |
| status=Expired | "Hợp đồng đã hết hạn — đóng hoặc gia hạn" | Gia hạn / Đóng |
| status=Cancelled | "Đã huỷ ngày {date}" | (none) |
| status=Revised | "Đã sửa đổi sang {amended_to}" | Mở bản sửa đổi |

### Next-action decision logic (PAKD)

Rules evaluated top-down — first matching rule wins. Branches on `workflow_state` and Settings flag `commission_post_on_approval`.

| State / condition | Next action shown | Action button |
|---|---|---|
| workflow_state=Draft | "Gửi duyệt {next_role_name}" | Gửi duyệt |
| workflow_state=Pending Sales Director | "Chờ duyệt từ GĐ KD {branch}" | Nhắc duyệt |
| workflow_state=Pending General Dept | "Chờ duyệt từ Phòng Tổng hợp" | Nhắc duyệt |
| workflow_state=Pending Branch Director | "Chờ duyệt từ GĐ Chi nhánh {branch}" | Nhắc duyệt |
| workflow_state=Pending Board | "Chờ duyệt từ Ban Lãnh đạo" | Nhắc duyệt |
| workflow_state=Approved AND Settings.commission_post_on_approval=0 AND additional_salary IS NULL | "Đăng hoa hồng (AS + JE) {amount}" | Đăng hoa hồng |
| workflow_state=Approved AND additional_salary IS NOT NULL | "Đã đăng hoa hồng ngày {date} — AS:{name}" | Mở AS |
| workflow_state=Approved AND Settings.commission_post_on_approval=1 AND additional_salary IS NULL (transient state, ≤ few seconds during auto-post) | "Đang đăng hoa hồng tự động…" | (none, disabled) |
| workflow_state=Rejected | "Lý do từ chối: {rejection_reason}" | Sửa & gửi lại |

**Note on Settings.commission_post_on_approval:**
- Default `1` (auto-post on approve): "Đăng hoa hồng" button rarely visible — only briefly during async job, or if auto-post failed (showing as error).
- Set `0` (explicit click): "Đăng hoa hồng" button is the primary path for accountant to control timing.
- These are mutually exclusive states — exactly one row above will match at any time.

### Reminder mechanic ("Nhắc duyệt" button)

Frappe-native email via `frappe.sendmail()` targeting `User.email` of the user(s) holding the approver role for current `workflow_state`.

**Role lookup with fallback chain:**
1. Branch-specific role match (e.g. `Pending Sales Director` + branch=HCM → `PAKD Sales Director HCM`)
2. If branch is null or no users hold the branch-specific role → general `PAKD Sales Director` role (if defined)
3. If still no recipients → fall back to `System Manager` users (logged warning, button still works but routes to admin)
4. If no recipients at all → button click shows error toast "Không tìm thấy người duyệt cho bước này — liên hệ quản trị viên"

**Multi-recipient behavior:**
- Email goes to ALL users holding the matching role (CC list)
- Single email, multiple TO recipients — not N separate emails

**Rate limit (anti-spam):**
- Server-side: new DocType `DCNET PAKD Reminder Log` (single-table audit) records `pakd`, `sent_by`, `sent_at`, `recipients`. Reminder rejected with toast if a reminder for the same PAKD was sent within last 24h, UNLESS sent_by is different user (so escalating to a different person is allowed).
- Client-side: button disabled for 60s after click (sessionStorage); prevents accidental double-click only.

**Email content:**
- Subject: "PAKD chờ duyệt: {pakd_name} — {customer_name}"
- Body: HTML template stored in DCNET PAKD Settings as Text Editor field `reminder_email_template` (admin-editable). Variables: `{{pakd_url}}`, `{{customer_name}}`, `{{total_revenue}}`, `{{days_waiting}}`, `{{reminded_by}}`.

### Empty-state behavior (fresh draft, no data)

When the Contract is brand-new (no items, no billing_schedule, no contract_date) or PAKD is brand-new (no items, no commission_lines):
- KPI strip (middle row) **hidden** — would show meaningless zeros
- Top row shows: status pill (`Draft`) + service info (if filled) + customer name (if filled)
- "Việc cần làm" row shows: `"Hoàn thành thông tin → gửi duyệt"` with no button (for Contract) or `"Chọn Hợp đồng và điền hạng mục"` (for PAKD when contract_ref is empty)
- Effective-dates row hidden when contract_date/acceptance_date are null

Card transitions from empty-state to full layout the moment the form saves with grand_total > 0 (Contract) or total_revenue_contract > 0 (PAKD).

### Performance constraint

`get_summary_kpis` must complete in **< 300ms** for contracts with ≤120 billing rows (covers 5-year monthly recurring + some headroom). Implementation requirements:
- Single SQL aggregate per data class (one SUM for SI, one SUM for PE, one COUNT for overdue billing rows) — NOT Python iteration over child docs
- Endpoint is `@frappe.whitelist()` cacheable=True with cache key = `(doctype, name, modified)` so unchanged docs hit Redis on re-render
- Cache invalidates via Frappe's standard on_save / on_submit / on_cancel hooks
- If endpoint exceeds 500ms in test seeds: profile + index recommendation before merge

### Acceptance criteria

- [ ] Open any Contract/PAKD: summary card renders within 1 second of refresh() (server endpoint < 300ms, JS render < 100ms)
- [ ] All 5 KPIs accurate vs `tabSales Invoice` + `tabPayment Entry` sums (test against seeded data with known values)
- [ ] "Next action" prompt + button changes correctly across all 9 Contract states + 9 PAKD states (integration tests cover every row of the decision tables)
- [ ] Drift indicator on PAKD card shows ⚠ when `_check_contract_drift()` returns drifted=true; does NOT show a button (sync stays at existing FB-503 location)
- [ ] "Nhắc duyệt" button sends ONE email to all recipients holding the matched role (or falls back per the chain); button disabled 60s after click; server rejects duplicate reminder within 24h from same user
- [ ] Card hidden on viewport width < 768px (replaced by compact 1-row pill showing only status + "Việc cần làm" text)
- [ ] Print Format `Hop Dong Chuan` does NOT include the card (print_hide=1 on header section + Section Break)
- [ ] Empty-state behavior fires correctly on fresh Draft (verified against new Contract / new PAKD with contract_ref selected but no items)

## 5. Work-stream 2 — Contract form section reorganization

### Final structure (13 → 8 sections + header)

| # | Section (new) | Fields | Notes |
|---|---|---|---|
| 0 | Tóm tắt hợp đồng | (header card from §4) | NEW |
| 1 | Thông tin cơ bản | customer, sales_person, department, company, branch, contract_no_external, project_category, service_type, package_name, installation_address | unchanged content |
| 2 | Loại hợp đồng & thời hạn | contract_type, payment_mode, package_term_months, contract_date, acceptance_date, end_date, appendix_no, appendix_date | merges contract_type_section + dates_section |
| 3 | Hạng mục & tổng giá trị | items, unit_price_total, setup_fee, grand_total, currency | merges financials_section + totals_section |
| 4 | Lịch thu tiền | billing_schedule (FB-504 color coding intact) | promoted from #10 to #4 |
| 5 | Kỹ thuật [collapsible, auto by service_type] | bandwidth, sla_restore_hours, point_a, point_b | unchanged content |
| 6 | Bên A / Bên B [collapsible, closed by default] | customer_info_* + company_representative_* | merges customer_info + company_info |
| 7 | Tham chiếu & bản mẫu [collapsible] | shadow_sales_order, template_ref, template_version, amended_from | merges references + template + audit |
| 8 | Văn bản hợp đồng [collapsible] | contract_html | unchanged |

`status_section` deleted — status field stays in DB but moves to header card.

### Auto-collapse logic

- Section 5 (Kỹ thuật) — auto-collapse if `service_type ∈ {FTTH HGD, VTTB, Thi công}`, auto-expand if `service_type ∈ {P2P, MPLS, ILL, FTTH DN, IT Managed}`
- Section 6 (Bên A / Bên B) — always closed by default
- Section 8 (Văn bản hợp đồng) — closed by default

### Print Format impact

`Hop Dong Chuan` reads from individual fields, not section structure. Section reorganization is **expected** to be invisible to print output — but this must be verified, not assumed.

**Regression test (mandatory before merge):**
1. BEFORE the change, render `Hop Dong Chuan` for 3 sample contracts:
   - 1 Recurring/ILL contract (P2P-style)
   - 1 One-off VTTB contract
   - 1 Recurring FTTH HGD contract (uses CMND fields)
2. Save rendered HTML to `tests/snapshots/hop_dong_chuan_{name}_before.html`
3. After the change, re-render for the same 3 contracts
4. Whitespace-normalized diff must show ZERO differences. Any diff is a regression — fix before merge.

Same procedure applies to DOCX/PDF export (compare extracted text content).

### Acceptance criteria

- [ ] All 8 sections render in proposed order on existing Contracts (manual QA against 5 sample contracts)
- [ ] Auto-collapse fires correctly per service_type (integration test: 4 service types — FTTH HGD, P2P, VTTB, FTTH DN)
- [ ] `Hop Dong Chuan` Print Format passes whitespace-normalized snapshot diff (regression test above, 3 sample contracts)
- [ ] DOCX export passes extracted-text diff
- [ ] Submitting existing Contract after reorg: no validation errors from reordered field_order
- [ ] All 4 Contract roles (DCNET Sales Rep, DCNET Sales Manager, Accounts Manager, System Manager) see correct fields per permission rules — no regression in role-based visibility

## 6. Work-stream 3 — PAKD form section reorganization

### Final structure (5 → 4 sections + header)

| # | Section (new) | Fields | Notes |
|---|---|---|---|
| 0 | Tóm tắt PAKD | (header card from §4) | NEW |
| 1 | Thông tin chung | pakd_type, contract_ref, contract_no_external, channel, customer, customer_name, sales_person, sales_person_name, department, branch, company, service_type, project_category | new section description |
| 2 | Hạng mục Hợp đồng | items | unchanged (FB-505 description stays) |
| 3 | Tổng tính toán & biên lãi | total_revenue_contract, total_add_costs, total_manager_services, total_license_fee, total_sales_commission, total_cost, total_revenue_service, **margin_pct** | renamed; adds margin display |
| 4 | Hoa hồng & lương bổ sung | commission_lines, additional_salary, **rejection_reason** | merges section_commission + lifts additional_salary; adds rejection reason |

`section_status` deleted.

### New field — `rejection_reason`

Add to PAKD DocType JSON (in section 4 "Hoa hồng & lương bổ sung"):

```json
{
  "fieldname": "rejection_reason",
  "fieldtype": "Small Text",
  "label": "Lý do từ chối",
  "read_only": 1,
  "depends_on": "eval:doc.workflow_state==='Rejected'",
  "description": "Lý do được nhập khi PAKD bị từ chối ở bước duyệt. Hiển thị trong thẻ Tóm tắt."
}
```

Populated by the workflow Reject action via a Frappe dialog prompt — the rejecting user types the reason, value saves to this field. The header card reads from this field for the Rejected state row.

Implementation: extend the workflow Reject action (or attach a `before_save` hook when `workflow_state` transitions to `Rejected`) — exact wiring sorted in plan phase.

### New computed field `margin_pct`

```python
margin_pct = round(
    (total_revenue_service - total_cost) / total_revenue_service * 100,
    1
) if total_revenue_service else 0
```

Display color logic:
- Green if `margin_pct >= margin_green_threshold` (from DCNET PAKD Settings, default 25)
- Amber if `margin_amber_threshold <= margin_pct < margin_green_threshold`
- Red if `margin_pct < margin_amber_threshold` (default 15)

### Workflow approval buttons

Frappe Workflow auto-renders approve/reject buttons in top button bar per `workflow_state` and current user role. No custom buttons needed for approve action itself — header card's "Việc cần làm" + "Nhắc duyệt" handles visibility/nudge.

### Acceptance criteria

- [ ] 4 sections render in proposed order
- [ ] `margin_pct` computes correctly and color-codes per Settings thresholds (test 3 cases: above green threshold, between thresholds, below amber threshold)
- [ ] Section 1 description visible on form load
- [ ] `rejection_reason` field persists when PAKD is Rejected via workflow action with dialog prompt
- [ ] `rejection_reason` is read-only after save (cannot be edited without re-rejecting)
- [ ] All 7 PAKD roles still see correct fields per permission rules — no regression
- [ ] Workflow Action approve/reject still fires from native Frappe top button

## 7. Work-stream 4 — Inline guidance plan

### Pattern 1 — Section header descriptions

Every section gets a 1-sentence header description (Frappe Section Break `description` field). Full text list in [Appendix A](#appendix-a-section-descriptions).

### Pattern 2 — Priority field descriptions

Round 1 must-have descriptions for fields where the label alone leaves ambiguity. **10 Contract fields + 11 PAKD fields**. Full text list in [Appendix B](#appendix-b-field-descriptions).

### Pattern 3 — Auto-computed vs manually-entered visual chip

JS renders small chip below label:
- `read_only: 1` and not `fetch_from` → "tự tính"
- `fetch_from: X` → "từ {X source doc}"
- Manually-entered → no chip (authoritative input)

Implementation: helper function in shared JS bundle (e.g. `dcnet_contract/public/js/field_chips.bundle.js`) called from each form's `refresh()`.

Edge case: when JS auto-fills a manually-editable field on trigger (e.g. customer event populates customer_address), show 1-time toast: "Đã điền từ hồ sơ KH — có thể chỉnh sửa".

### Pattern 4 — Help-icon (?) for complex semantics

7 fields get (?) icons opening Frappe Dialog with markdown from vn_help:

**Contract:** payment_mode, service_type, template_ref + template_outdated, shadow_sales_order
**PAKD:** pakd_type, channel, total_revenue_service

Implementation: JS reads vn_help slug from a `help_article` data attribute set on the field's `description`, opens via existing vn_help dialog API.

### Acceptance criteria

- [ ] All 12 section headers display description on form open
- [ ] 10 Contract + 11 PAKD priority fields have descriptions visible
- [ ] All read_only fields display correct chip
- [ ] 7 (?) help-icon fields open dialog with markdown content from vn_help
- [ ] vi.csv contains all new strings (English source + Vietnamese)
- [ ] No labels/descriptions reference English DocType names — only business language

## 8. Work-stream 5 — vn_accounting portfolio view

### Workspace sidebar additions

| Group | Item label | Type | Filter / Target | Status |
|---|---|---|---|---|
| Hợp đồng | HĐ đang hoạt động | DocType | status=Active | NEW item |
| Hợp đồng | HĐ sắp hết hạn | Report | uses **existing** `contract_expiry_report` (filter to <60d if not already) | NEW item, existing report |
| Hợp đồng | HĐ tạm ngưng | DocType | status=Suspended | NEW item |
| Hợp đồng | Công nợ theo HĐ | Report | uses **existing** `outstanding_receivables_by_contract` | NEW item, existing report |
| Hợp đồng | Kỳ thu tiền quá hạn | Report | Billing Schedule rows where state=Overdue, grouped by contract | NEW item, **NEW Script Report** |
| PAKD | PAKD chờ duyệt | DocType | workflow_state IN [Pending Sales Director, Pending General Dept, Pending Branch Director, Pending Board] | NEW item |
| PAKD | PAKD đã duyệt — chưa đăng hoa hồng | DocType | workflow_state=Approved AND additional_salary IS NULL | NEW item |
| Cài đặt | DCNET Contract Settings | DocType | (Single — **confirmed exists** at `dcnet_contract/doctype/dcnet_contract_settings/`) | existing |
| **Cài đặt** | **DCNET PAKD Settings** | DocType | (Single — NEW DocType) | **NEW** |
| **Cài đặt** | DCNET PAKD Reminder Log | DocType (List) | Audit log for "Nhắc duyệt" actions (rate-limit data source) | **NEW** (admin-only visibility, hidden in Cài đặt subsection or via role filter) |

Sidebar items follow sticky `route_options` pattern. Reports use `link_type=Report`.

### Number Cards on vn-accounting-dashboard

| Card | Computation | Drill-through |
|---|---|---|
| Số HĐ đang hoạt động | count(DCNET Contract, status=Active) | → HĐ đang hoạt động list |
| Tổng DT chưa thu | sum(Sales Invoice.outstanding_amount, contract linked) | → `outstanding_receivables_by_contract` |
| Số kỳ quá hạn | count(Billing Schedule rows, state=Overdue) | → Kỳ thu tiền quá hạn report |
| HĐ sắp hết hạn (<60d) | count(Contract, status=Active AND end_date < today+60d) | → HĐ sắp hết hạn report |
| PAKD chờ duyệt | count(PAKD, workflow_state IN pending states) | → PAKD chờ duyệt list |

Each card has Frappe Number Card `description` explaining what it counts.

### Charts on vn-accounting-dashboard

| Chart | Type | X / Y | Filter |
|---|---|---|---|
| Doanh thu HĐ theo tháng | Bar | month × sum(grand_total) | last 12 months, status=Active |
| Top 10 HĐ giá trị lớn | Bar (horizontal) | contract name × grand_total | status=Active, top 10 |
| HĐ theo trạng thái | Pie | status × count | all |
| PAKD theo bước duyệt | Bar | workflow_state × count | non-final states |

All charts use `chart_type ∈ {Count, Sum}` only. Never "Report" type.

### DCNET PAKD Settings DocType (Single)

| Field | Type | Default | Purpose |
|---|---|---|---|
| margin_green_threshold | Percent | 25 | Above this = green margin display |
| margin_amber_threshold | Percent | 15 | Between green and this = amber; below = red |
| default_commission_channel | Select (Staff/Board) | Staff | Default channel for new PAKDs |
| commission_post_on_approval | Check | 1 | If 1, AS posts immediately on Approve; else requires explicit click |
| reminder_email_template | Text Editor | (default template) | HTML body for "Nhắc duyệt" emails |
| reminder_throttle_hours | Int | 24 | Hours between reminders from same user for same PAKD |

Permissions:
- System Manager, Accounts Manager, DCNET Sales Manager: read + write
- PAKD Sales Director (HCM/HN), PAKD Board: read

### DCNET PAKD Reminder Log DocType

Per-row audit. Append-only.

| Field | Type | Purpose |
|---|---|---|
| pakd | Link → Phuong An Kinh Doanh | Which PAKD |
| sent_by | Link → User | Who clicked "Nhắc duyệt" |
| sent_at | Datetime | When |
| recipients | Long Text | Comma-separated emails (audit only) |
| workflow_state_at_send | Data | Snapshot of PAKD workflow_state at reminder time |

Permissions:
- System Manager, Accounts Manager: read
- Everyone else: no access (insert handled by server endpoint with ignore_permissions=True)

Used by the rate-limit query: `SELECT 1 FROM tabDCNET PAKD Reminder Log WHERE pakd=%s AND sent_by=%s AND sent_at > NOW() - INTERVAL <throttle_hours> HOUR LIMIT 1`.

### Acceptance criteria

- [ ] All 8 new sidebar items (6 list/report + 2 Cài đặt) appear under correct groups, route correctly with filters
- [ ] 1 new Script Report (Kỳ thu tiền quá hạn) returns correct rows for test seeds
- [ ] Reused reports (contract_expiry_report, outstanding_receivables_by_contract) accessible via new sidebar entries
- [ ] 5 Number Cards render on dashboard with correct values (verified against direct SQL counts)
- [ ] 4 charts render without errors (no Report-type charts — all Count or Sum)
- [ ] DCNET PAKD Settings opens via sidebar "Cài đặt > DCNET PAKD Settings"; only authorized roles see write actions
- [ ] DCNET PAKD Reminder Log writes correctly when "Nhắc duyệt" is clicked; rate limit enforced via SQL query against this table
- [ ] All sidebar items follow sticky route_options pattern (per `reference_frappe_sidebar_sticky.md`) — F5 keeps user on vn_accounting sidebar
- [ ] Sidebar fixture sync via after_migrate hook does NOT mutate ERPNext-owned workspace JSONs (per `frappe.md` "Custom app .save() on Workspace Sidebar" rule — insert child rows directly, never parent.save())

## 9. Work-stream 6 — vn_help article gap fill

### Contract articles (7 files)

| File | Topic |
|---|---|
| contract/contract-overview.md | Vòng đời hợp đồng, 8 trạng thái và ý nghĩa |
| contract/pakd-vs-contract.md | Khi nào dùng Hợp đồng vs PAKD |
| contract/billing-schedule.md | Lịch thu tiền: cách sinh ra, 6 trạng thái dòng |
| contract/template-engine.md | Mẫu hợp đồng: Apply, Outdated, re-apply |
| contract/payment-modes.md | Prepay / Monthly / OneOff với ví dụ |
| contract/service-types.md | 8 loại dịch vụ — khi nào dùng, trường nào cần |
| contract/shadow-sales-order.md | Đơn bán hàng nội bộ cho HĐ one-off |

### PAKD articles (6 files)

| File | Topic |
|---|---|
| pakd/pakd-overview.md | PAKD là gì, vòng đời 7 trạng thái |
| pakd/pakd-types.md | 3 loại PAKD với ví dụ tính toán |
| pakd/approval-flow.md | 4 bước duyệt, ai phụ trách bước nào |
| pakd/commission-flow.md | Hoa hồng tính như thế nào, AS sinh ra khi nào |
| pakd/channel-staff-vs-board.md | Channel Staff vs Board |
| pakd/drift-resolution.md | Khi PAKD lệch so với HĐ — cách giải quyết |

### vn_help registry updates

- `doctype_mapping`:
  - DCNET Contract → contract/contract-overview.md
  - Phuong An Kinh Doanh → pakd/pakd-overview.md
- `report_mapping`:
  - HĐ sắp hết hạn → contract/contract-overview.md#expiration
  - Kỳ thu tiền quá hạn → contract/billing-schedule.md#overdue
  - PAKD chờ duyệt → pakd/approval-flow.md

All articles follow vn_help authoring standard (YAML frontmatter, no DocType name references, business-language only).

### Acceptance criteria

- [ ] All 13 markdown articles exist with valid frontmatter
- [ ] 7 (?) help-icon fields open the matched article
- [ ] doctype_mapping resolves correctly for both DocTypes
- [ ] Articles render with proper formatting
- [ ] No article references English DocType names or ERPNext/Frappe terminology

## 10. Implementation order recommendation

Single bundled feature branch, but internally staged by work-stream commit so reviewer can read commit-by-commit. PR description structured by work-stream §. Atomic commits per acceptance criterion where possible.

> **Note on bundling vs. multi-session rule #17:** the rule warns that pure-fix mode with >50 findings degenerates as agents play it safe. This design has ~60+ verifiable acceptance items. Mitigation: each work-stream gets its own commit + its own QA gate; final merge only after every § gate passes. Reviewer can revert work-stream commits independently if any one fails review.

### Phase order (each phase = 1+ commits)

1. **Backend foundation** — `get_summary_kpis` endpoints + DCNET PAKD Settings DocType + DCNET PAKD Reminder Log DocType + `rejection_reason` PAKD field + email-reminder service
   - **`bench restart` REQUIRED after this phase** (new Python modules + new endpoints) — gunicorn caches modules, won't see new code without restart. Live testing of subsequent phases depends on this.
   - Worker queue check: reminder email uses `frappe.sendmail()` synchronously; no `frappe.enqueue` needed, so no Procfile worker check needed
2. **DocType JSONs** — field_order changes + section descriptions + field descriptions + new HTML header sections + new field `rejection_reason`
   - Run `bench migrate` after each JSON edit; verify form opens without errors
3. **JS rendering** — header card renderer + auto/manual chips + (?) help icons + auto-collapse logic by service_type
   - `bench build --app dcnet_contract && bench build --app dcnet_pakd` after each bundle change
4. **vn_help articles** (13 markdown files + registry updates) — can be authored in parallel with phase 3 since content is independent
5. **Workspace sidebar** — 6 new sidebar items + Cài đặt group additions (DCNET PAKD Settings, DCNET PAKD Reminder Log) — fixture sync via after_migrate hook per `frappe.md` "Settings DocType + after_migrate re-apply" rule
6. **Dashboard** — 5 Number Cards + 4 charts on vn-accounting-dashboard
   - Use `chart_type ∈ {Count, Sum}` only — never "Report" type per memory rule
7. **vi.csv translations** — all new English source strings translated; dedup check against existing 13.9k entries before adding
8. **Print Format snapshot regression test** — capture 3 sample contracts BEFORE phase 2, re-render AFTER phase 3, whitespace-normalized diff must be clean
9. **Integration tests** — Contract state machine (9 states), PAKD state machine (9 conditions), KPI aggregation math, reminder rate limit, role permission regression
10. **Manual QA across 4 personas** — sales rep flow, sales director approval flow, accountant invoice creation flow, KTT portfolio audit flow

### Post-merge verification

- `bench --site dcnet.localhost clear-cache` + browser hard refresh
- `pgrep -f "frappe serve.*8001"` shows a PID newer than mtime of edited Python files (sanity check that bench restart actually happened — per `multi-session.md` rule #28)
- `bench --site dcnet.localhost list-apps` includes dcnet_contract, dcnet_pakd, vn_accounting, vn_help, vn_translation

## 11. Hard constraints

Inherited from project rules:

- **Inline guidance mandatory** — every field/section/button needs contextual help
- **English source labels + VN via vi.csv** — never hardcode VN with diacritics in source
- **VN accounting terminology binds to TT99/2025** — verify all new report/sidebar names against the regulation
- **No technical jargon in user-facing labels** — "Hợp đồng" not "DCNET Contract" in display
- **No hardcoded TK or business numbers** — margin thresholds via Settings DocType

## 12. Anti-goals

- Don't reorganize fields for fashion — every move must trace to a persona pain
- Don't rewrite shipped features (auto-sync, drift detection, related transactions, color rows)
- Don't add new DocTypes/fields/columns unless current ones can't answer the persona's question (exception: DCNET PAKD Settings, justified by anti-hardcoding rule)
- Don't ship in 1 shot regardless of bundling — staged QA within the branch by work-stream

## 13. Success criteria

A user opening a Contract or PAKD form for the first time should:

- Understand within 30 seconds what the form is for and what fields are required to fill
- Know where to find related info without hunting
- See visual distinction between manually-entered, auto-computed, and synced data
- Not need to ask "what does this field mean?" — description or (?) icon answers it
- See an at-a-glance health summary on the vn_accounting sidebar/dashboard for their contract portfolio

---

## Appendix A — Section descriptions

| Form | Section | Header description |
|---|---|---|
| Contract | Thông tin cơ bản | Phần định danh hợp đồng — khách hàng, NVKD, công ty và loại dịch vụ chính. |
| Contract | Loại hợp đồng & thời hạn | Recurring = thu định kỳ. One-off = thu 1 lần. Ngày kết thúc tự tính từ Ngày kích hoạt + Thời hạn gói. |
| Contract | Hạng mục & tổng giá trị | Mỗi hạng mục có đơn giá × số lượng = giá trị/kỳ. Tổng giá trị = tổng các hạng mục + phí lắp đặt. |
| Contract | Lịch thu tiền | Tự sinh từ Ngày kích hoạt + Hình thức thanh toán + Thời hạn gói. Mỗi dòng tương ứng 1 hoá đơn dự kiến. Màu nền cho biết trạng thái. |
| Contract | Kỹ thuật | Thông tin kỹ thuật dùng cho cung cấp dịch vụ — KHÔNG in trên hợp đồng giấy. |
| Contract | Bên A / Bên B | Thông tin pháp lý IN TRÊN hợp đồng giấy. Chốt lúc ký HĐ — không tự cập nhật khi hồ sơ KH thay đổi. |
| Contract | Tham chiếu & bản mẫu | Liên kết tới các bản ghi liên quan: đơn bán hàng nội bộ (one-off), mẫu hợp đồng, bản sửa đổi trước. |
| Contract | Văn bản hợp đồng | Nội dung văn bản đầy đủ — dùng để xuất DOCX/PDF. Được tự động điền khi bấm 'Apply Template'. |
| PAKD | Thông tin chung | Hầu hết trường tự đồng bộ từ Hợp đồng. Khi Hợp đồng thay đổi, bấm Cập nhật từ hợp đồng ở Hạng mục để đồng bộ lại. |
| PAKD | Hạng mục Hợp đồng | (existing FB-505 description — keep) |
| PAKD | Tổng tính toán & biên lãi | Các tổng tính tự động từ Hạng mục, hệ số chi phí và tỷ lệ hoa hồng. Biên lãi % = (DT dịch vụ − Chi phí) / DT dịch vụ. |
| PAKD | Hoa hồng & lương bổ sung | Dòng hoa hồng sinh ra khi PAKD được duyệt. Lương bổ sung là bản ghi HRMS sẽ chi trả hoa hồng cho NVKD. |

## Appendix B — Field descriptions

### Contract priority fields

| Field | Description |
|---|---|
| service_type | Loại dịch vụ — chọn để hiển thị trường phù hợp (P2P/MPLS cần điểm A-B; FTTH HGD cần CMND…). |
| project_category | Phân loại doanh thu nội bộ — phục vụ báo cáo theo danh mục, KHÔNG in trên HĐ. |
| contract_type | Recurring = thu định kỳ (T/Q). One-off = thu 1 lần khi giao hàng/thi công. |
| payment_mode | Prepay = thu trước kỳ. Monthly = thu sau kỳ. OneOff = chỉ áp dụng cho HĐ One-off. |
| package_term_months | Số tháng. End date = acceptance_date + N tháng (tự tính). |
| acceptance_date | Ngày kích hoạt dịch vụ / nghiệm thu — Lịch thu tiền tính từ ngày này. |
| end_date | (read-only) Tự tính = Ngày kích hoạt + Thời hạn gói. |
| template_ref | Mẫu HĐ — tự điền Loại HĐ, Hình thức TT, Thời hạn, Hạng mục từ template. |
| shadow_sales_order | (one-off only) Đơn bán hàng nội bộ — quản lý xuất kho qua ERPNext. |
| setup_fee | Phí thu 1 lần khi kích hoạt — KHÔNG nhân với chu kỳ. |

### PAKD priority fields

| Field | Description |
|---|---|
| pakd_type | Recurring Telecom = qty×price. Monthly FTTH Rollup = DT thực tế hàng tháng (đa hộ). One-off = bán/thi công. |
| channel | Staff = NVKD tự bán. Board = HĐ do Ban LĐ giới thiệu (có thể áp tỷ lệ hoa hồng khác). |
| contract_ref | Hợp đồng nguồn — đa số trường ở dưới fetch từ đây. |
| total_revenue_contract | DT theo điều khoản HĐ. |
| total_add_costs | CP ngoài đơn giá (vận chuyển, chi phí thi công khác). |
| total_manager_services | Phí DV quản lý — chi cho cấp quản lý theo công thức. |
| total_license_fee | Phí GPVT — áp dụng dịch vụ telecom. |
| total_sales_commission | Hoa hồng NVKD = f(DT dịch vụ, channel). |
| total_cost | = CP ngoài + DV quản lý + GPVT + Hoa hồng. |
| total_revenue_service | = DT HĐ − GPVT − DV quản lý (DT ròng). |
| additional_salary | (read-only) Bản ghi HRMS chi hoa hồng cho NVKD — tự tạo khi PAKD duyệt. |

---

## 14. Phase 7 — Commission UX gaps (post-QA findings)

**Status:** SPEC ONLY — not yet implemented. Each item has business-decision dependencies + Doctype changes.

### 14.1 Preview commission lines on Draft PAKD (Q1)

**Gap:** `commission_lines` table is empty until PAKD `workflow_state=Approved` (per `_generate_commission_lines()` in `on_update`). User cannot see projected commission breakdown while drafting/reviewing the PAKD.

**Fix:**
- Move `_generate_commission_lines()` from `on_update` (Approved-only) to `validate()` (every save)
- Rows persist in `commission_lines` table with `state="Pending"` — semantically already means "preview, not yet paid"
- On Approved: rows stay "Pending" (no semantic change needed)
- On Payment Entry submit: matching kỳ × component rows flip to "Posted"
- On PAKD Rejected/Cancelled: clear `commission_lines`

**Acceptance:**
- [ ] Draft PAKD with Hạng mục filled → commission_lines auto-populates immediately on save
- [ ] Recurring Telecom HĐ with 12-tháng billing schedule → 12 kỳ × 4 components ≈ 48 dòng visible in section "Hoa hồng & lương bổ sung"
- [ ] Each preview row shows: kỳ, component, amount, state=Pending (no AS/JE/PE links yet)
- [ ] On re-save with changed items → preview re-computes correctly (delete + re-insert all Pending rows; preserve Posted)

### 14.2 Workflow allow_edit expansion (Q2)

**Gap:** Workflow `PAKD Approval` state `Draft` has `allow_edit="PAKD Sales Rep"` ONLY. Combined with DocType permission `if_owner=1`, this blocks edits from:
- Other PAKD Sales Reps (not owner)
- System Manager (does not hold PAKD Sales Rep role)
- Accounts Manager (does not hold PAKD Sales Rep role)

Administrator passes by virtue of System Manager + bypass logic, but other admin-level users get blocked.

**Fix:** Update Workflow `PAKD Approval` state `Draft` `allow_edit` to: `"PAKD Sales Rep,System Manager,Accounts Manager"` (comma-separated allows multiple).

**Acceptance:**
- [ ] Login as System Manager (not the doc owner) → can edit + save Draft PAKD
- [ ] Login as Accounts Manager → same
- [ ] Login as PAKD Sales Rep (not owner) → still blocked (workflow constraint kept for sales reps)
- [ ] Login as PAKD Sales Rep (owner) → can edit (existing behavior preserved)

### 14.3 In-PAKD rate adjustment + clearer % display (Q3)

**Gap A:** Commission rate is centrally managed in `PAKD Commission Rule Template`. User wants per-PAKD override visible/editable inline in the PAKD form.

**Gap B:** "Tỷ lệ hoa hồng 100% của doanh thu" hiển thị gây hiểu lầm. Audit found `Monthly FTTH Rollup Standard` template has `Sales Commission rate=100%` — dead data, because engine for FTTH bypasses the rule template and uses PAKD Item `salary_coefficient` instead. Other templates (Recurring Telecom, One-off) have correct small % values (6%, 10%, 2.2%).

**Fix A (in-PAKD rate override):**
- Add new section "Tỷ lệ hoa hồng áp dụng" between "Hạng mục" and "Tổng tính toán & biên lãi"
- Show one row per component (Manager Services / Add Costs / License Fee / Sales Commission) with:
  - Component name (read-only)
  - Rate from rule template (read-only display, e.g. "6.0%")
  - Override rate (Percent, editable) — empty by default, when filled overrides the template rate
  - Note: "Để trống = dùng mẫu chuẩn"
- On `validate()`, engine uses override rate if set, else falls back to rule template rate
- Override stored as `commission_overrides` child table on PAKD: `(component, override_rate)`

**Fix B (clarity):**
- Delete the 100% rate from `Monthly FTTH Rollup Standard` template (it's dead data; engine doesn't use it)
- Change PAKD Item field `salary_coefficient` from Float to Percent (with description: "Tỷ lệ % của Doanh thu thực tế trả cho NVKD, vd: 5 = 5%")
- Update engine to divide by 100 when reading salary_coefficient (mirror the rule template handling)
- Add a computed display field `effective_commission_pct` on PAKD: `(total_sales_commission / total_revenue_contract * 100)` — shown in totals section so user sees the actual % NVKD gets

**Acceptance:**
- [ ] Open PAKD → see "Tỷ lệ hoa hồng áp dụng" section with 4 rows (per component) showing template rates
- [ ] Override one rate → save → recompute uses override
- [ ] Clear override → recompute uses template
- [ ] FTTH PAKD → salary_coefficient displays as percent (e.g. "5%"), not float 0.05 or 5.0
- [ ] Effective commission % computed correctly and visible in totals section
- [ ] Delete `Monthly FTTH Rollup Standard` rule template's 100% row (or hide the rule template entirely for FTTH type)

### 14.4 External commission (Q4) — for customer's manager, NOT NVKD

**Gap:** Current `Sales Commission` only supports paying internal Employee (`pakd.sales_person`) via Additional Salary → HRMS. No support for "kickback" / commission paid to customer's procurement manager (external person), which has different:
- Recipient (external, not Employee)
- Account (Chi phí dịch vụ hoặc Chi phí khác, NOT 334 Phải trả lương NV)
- Tax (PIT withholding 10% or 20% at source)
- Payment method (Cash/Bank transfer, NOT through Payroll)

**Business decision (locked):**
- DCNET **NOT using HRMS module** for now → internal NVKD commission should also bypass Additional Salary, post directly via JE
- All commission posting uses Journal Entry with `party_type="Employee"` + `party=sales_person` against an account like `334 — Phải trả người lao động`
- External commission gets a SECOND JE with different account + party type

**Fix:**

**14.4.A — Bypass HRMS for NVKD commission**
- New Settings field on `PAKD Settings`:
  - `use_hrms_for_commission` (Check, default `0`)
  - `account_employee_payable` (Link → Account, default lookup for "334 Phải trả người lao động")
- When `use_hrms_for_commission=0`:
  - Skip `push_to_additional_salary()`
  - Post JE: DR `account_employee_payable` (party_type=Employee, party=sales_person) / CR ... wait, this is the OPPOSITE direction
  - Actually CORRECT JE: DR `expense account (642 - Chi phí lương)` / CR `account_employee_payable (334)` with party=Employee
  - Then when actually paying NVKD: separate Payment Entry pays down 334
- When `use_hrms_for_commission=1`: existing behavior (Additional Salary → Payroll)

**14.4.B — External commission feature (the 6 points + user's refinements)**

1. PAKD field group additions (new section "Hoa hồng ngoài (khách hàng giới thiệu)" between Sales Commission and totals):
   - `external_commission_recipient_name` (Data) — tên người nhận
   - `external_commission_recipient_id` (Data) — CMND/CCCD or tax ID for tax withholding
   - `external_commission_amount` (Currency) — số tiền hoa hồng (manual entry OR computed)
   - `external_commission_rate` (Percent, optional) — nếu muốn tính theo % thay vì nhập số trực tiếp
   - `external_commission_tax_pct` (Percent, default from Settings) — thuế TNCN khấu trừ tại nguồn, default 10%
   - `external_commission_account` (Link → Account, default from Settings) — TK hạch toán, e.g. `6427` or `642`
   - `external_commission_note` (Small Text) — lý do/tham chiếu
2. Rule template enhancement: add new `External Commission` component option (alongside the existing 4) — drives `external_commission_amount` computation when rate is set on rule template
3. Hạch toán riêng (JE) — separate from NVKD JE:
   - DR `external_commission_account` (e.g. 6427) / CR `338 - Phải trả khác` (party_type=Customer or Contact, party=recipient_name)
   - Withholding: DR `338` / CR `3335 - Thuế TNCN phải nộp` for the tax_pct portion
4. Payment Entry to pay external: reference_type="Phuong An Kinh Doanh" (or just manual reference), reference_name=PAKD.name
5. UI — render as a card in section "Hoa hồng ngoài":
   - Recipient name + ID
   - Gross amount + tax_pct + net to pay
   - JE link (once posted)
   - Payment Entry link (once paid)
6. Tax compliance:
   - PIT withholding required for individual recipients (>= 2tr/lần from 2026)
   - System auto-flag for review when amount > threshold
   - Year-end PIT report includes external commissions for non-employees

**14.4.C — Channel field becomes meaningful**
- Currently `channel` (Staff/Board) just labels but doesn't drive different rates
- Update rule template to add `scope_channel` (Select Staff/Board/All)
- Engine resolution prefers `scope_channel` match (Board > Staff > All for ties on other dimensions)
- This handles the "BLD-introduced HĐ pays lower commission" scenario

**Acceptance:**
- [ ] Settings has `use_hrms_for_commission` toggle + `account_employee_payable` field
- [ ] When toggle off: NVKD commission posts as JE (DR 642 / CR 334 with party=Employee), no Additional Salary record
- [ ] Payment Entry can pay down 334 for an employee, marks PAKD Commission Line state=Posted
- [ ] PAKD form has "Hoa hồng ngoài" section with all 7 fields
- [ ] External commission JE posts with correct accounts (DR custom expense, CR 338) + tax withholding entries
- [ ] `commission_lines` table now has rows for NVKD AND for external — visually distinct by component column
- [ ] Rule template's `scope_channel` filters which rate applies for Staff vs Board PAKDs

### 14.5 Implementation order (Phase 7)

1. **14.2 Workflow allow_edit** — 10 LOC, ~30 min — unblocks editing immediately
2. **14.1 Preview commission lines** — move method call site, ~30 LOC + tests, ~1h
3. **14.3 Rate clarity** — fix 100% in seed data + field type change + label/description — ~1h
4. **14.4.A Bypass HRMS** — Settings field + engine branching + new JE posting logic — ~2-3h
5. **14.3 In-PAKD rate override** — new child table + JS UI + engine override logic — ~2-3h
6. **14.4.B External commission feature** — new fields + new JE + payment + UI section — multi-session
7. **14.4.C Channel-aware rates** — small rule template change + engine update — ~1h

Recommend bundling 14.1+14.2+14.3 as a single "Commission UX polish" PR (fast wins), then 14.4.A as standalone (changes hạch toán direction), then 14.4.B as a focused multi-session task (biggest scope, needs careful spec).
