# Design QA Proposals — Mắt Bão Auto-Attach PDF+XML

## Session 2026-05-07 10:55

QA surfaces reviewed: EInvoice Inward form view, list view, Notification Log.
Test environment: `http://hts.localhost:8003` (local mirror, `feature/matbao-auto-attach-pdf-xml`).
Console errors during QA: 1 pre-existing (socketio `Invalid namespace` — local mirror port mismatch, unrelated to this feature).

---

### [DQ-1] Bulk action button placement — 3-dot menu vs selection dropdown

**Surface:** EInvoice Inward list view  
**Tier:** 4 — flow change (not auto-fixed)  
**Severity:** Low — functional, just suboptimal UX

**Observation:**  
"Tải file đính kèm cho HĐ đã chọn" is placed in the page 3-dot menu ("Thực đơn → Hành động") via `listview.page.add_inner_button(label, fn, __("Hành động"))`. Users must discover it there.

The Frappe list view also shows a red "Hành động" button when rows are selected (selection bulk action bar). The expected UX pattern for row-selection actions is to appear there, not in the page-level 3-dot menu.

**Root cause:**  
`listview.page.add_inner_button(label, fn, group)` adds to the page-level inner button group, which is accessible from the 3-dot menu. To add to the selection bulk action bar, Frappe requires a different approach (e.g., overriding `onload` to inject into `listview.bulk_actions` or using `listview.page.add_action_item`).

**Proposed fix:**  
In `einvoice_inward_list.js`, change from `listview.page.add_inner_button` to inject into the bulk action bar. In Frappe v15, the selection bar appears at the bottom of the list when rows are checked. The right pattern for a "works on selected rows" action is:

```javascript
onload(listview) {
    listview.page.add_action_item(__("Tải file đính kèm"), function () {
        const checked = listview.get_checked_items();
        // ... same logic
    });
    // realtime listener
}
```

Or alternatively, keep the current `add_inner_button` (it works, just less discoverable) and add UX hint text in the listview empty state or a tooltip on the rows.

**Decision:** Defer to vNext unless UX testing shows users can't find the action.

---

### [DQ-2] `attach_status` field not visible in form view default layout

**Surface:** EInvoice Inward form view  
**Tier:** 3 — spacing/label/cosmetic auto-fix candidate, but involves DocType JSON  
**Severity:** Low — status is reflected in list view formatter but hidden in form

**Observation:**  
The form shows all invoice data sections (Nguồn dữ liệu, Thông tin hóa đơn, Nhà cung cấp, etc.) but the `attach_status`, `pdf_file`, `xml_file`, `attach_error`, `attach_retry_count` fields are not visible in the default form layout. They are custom fields but appear to be in a section that's scrolled past or collapsed.

**Proposed fix:**  
Add a visible "Đính kèm" section in the form after "Xử lý" with:
- `attach_status` (read-only, labeled "Trạng thái đính kèm")
- `pdf_file` (read-only link)
- `xml_file` (read-only link)
- `attach_error` (read-only, hidden when empty)
- `attach_retry_count` (hidden — internal use only)

This requires updating the DocType JSON via `bench --site erp.htsfood.com migrate` after editing.

**Decision:** Defer to vNext. Current UX relies on list view `attach_status` formatter + form "Tải lại" button presence as implicit status indicator.

---

### [DQ-3] Realtime button state — "Đang tải" indicator has no dismissal

**Surface:** EInvoice Inward form view (active download in progress)  
**Tier:** 4 — flow change  
**Severity:** Low

**Observation:**  
When `attach_status = "Đang tải"`, the form shows a blue dashboard indicator "Đang tải file đính kèm...". This indicator disappears on `frm.reload_doc()` (triggered by realtime event). However, if the batch fails before the realtime event fires (e.g., worker crashes), the "Đang tải" indicator stays permanently until the user manually refreshes the page.

**Root cause:**  
The "Đang tải" state is set optimistically (before the background job starts) but the indicator has no timeout/auto-dismiss logic. If the worker never publishes the `einvoice_attach_progress` event (crash, queue overflow), the form is stuck.

**Proposed fix:**  
Add a client-side timeout in `onload`: if 60 seconds pass after a realtime subscription is registered and no event fires for this document, auto-reload the form. This would refresh the status from DB (which would show "Lỗi" if the worker failed).

**Decision:** Defer to vNext — timeout logic adds complexity; acceptable for MVP since workers are stable in production and `attach_retry_count < 5` provides recovery via daily scheduler.

---

### [DQ-4] Notification Log subject text hardcodes "Mắt Bão"

**Surface:** Notification Log after batch completion  
**Tier:** 4 — business logic, not auto-fixed  
**Severity:** Low

**Observation:**  
`_create_notification` in `services/attach.py` creates notifications with subject:
```
"Tải file Mắt Bão: {n_ok}/{n_total} thành công, {n_fail} lỗi"
```

This hardcodes "Mắt Bão" in the subject. If the feature is extended to other providers (Viettel, MISA), the subject will be misleading.

**Proposed fix:**  
Change to a provider-agnostic subject:
```python
subject = f"Đính kèm file HĐĐT: {n_ok}/{n_total} thành công, {n_fail} lỗi"
```

**Decision:** Minor — fix in next batch of provider extension work.
