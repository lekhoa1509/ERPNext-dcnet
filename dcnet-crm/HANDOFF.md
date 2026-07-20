# DCNET CRM Handoff

> Last updated: 2026-07-13 (dashboard soft-bento redesign; KPI/funnel/stage-composition UI; quick-action cascade fix; `Bàn làm việc` routes to dashboard; duplicate `Tất cả` sidebar entry removed; module docs normalized)
>
> Previously: 2026-06-20 (Activities workspace; SO action modal; Notification Log; activity permission model; CRM page roles; customer assignment design note)
>
> Read this file before continuing any work in `dcnet-crm`.

## 1. Goal

Build a standalone Frappe app named `dcnet_crm` that customizes the CRM user
experience without modifying `dcnet_apps` or ERPNext source code.

The app reuses standard Frappe/ERPNext DocTypes and adds:

- A custom Vue workspace at `/desk/dcnet-crm`.
- Permission-aware server APIs.
- An ERPNext Workspace Sidebar owned by `dcnet_crm`.
- Internal customer profile screens inspired by the supplied CRM screenshots.

The repository/folder intended to be pushed independently is `dcnet-crm`.

## 2. Non-Negotiable Rules

1. Do not add CRM code to `dcnet_apps`.
2. Do not edit ERPNext core for this CRM customization.
3. Reuse standard DocTypes whenever possible; do not duplicate CRM data.
4. Official business scope comes from
   `docs/feature/FEATURE_SPECIFICATION.md`.
5. Screenshots/MISA videos are UX references only. Do not invent business
   features that are absent from the specification.
6. All reads and writes must respect Frappe permissions.
7. Customer profile tabs must remain inside `/desk/dcnet-crm`; do not route
   Customer or Contact editing to their standard DocType forms.
8. Sidebar links must navigate in the same browser tab.
9. Do not add a second custom sidebar inside the Vue application. The visible
   sidebar is the native Frappe `Workspace Sidebar`.
10. Document UI changes in `docs/customization/`.
11. If a relation is not specified, show an empty state and record a clarify
    item instead of inventing a data model.
12. Preserve unrelated dirty worktree changes.

## 3. App and Data Ownership

| UI/domain | Standard data source |
|---|---|
| Lead | `Lead` |
| Opportunity | `Opportunity` |
| Customer | `Customer` |
| Contact | `Contact` + `Dynamic Link` |
| Address | `Address` + `Dynamic Link` |
| Quotation | `Quotation` |
| Order | `Sales Order` |
| Invoice/return | `Sales Invoice`, separated by `is_return` |
| Task | `ToDo` |
| Meeting/call | `Event` + `Event Participants` |
| Notes/timeline | `Comment`, `Communication`, `ToDo` |
| Attachments | `File` |
| Care card (Thẻ chăm sóc) | `CRM Care Card` (custom DocType, owned by `dcnet_crm`) |
| Service account | `DCNET Service Account` (custom DocType, owned by `dcnet_crm`) |

`dcnet_crm` depends only on `frappe` and `erpnext`.

Two custom DocTypes (`CRM Care Card`, `DCNET Service Account`) live **inside
`dcnet_crm`** — this is the sanctioned exception to "reuse standard DocTypes":
both model CRM-specific concepts with no ERPNext equivalent. Never put them in
`dcnet_apps`.

## 4. Main Files

- `frontend/src/main.js`: thin entry (~39 lines) — mounts the app only. ← **REFACTORED**
- `frontend/src/app.js`: Vue workspace root — routing, view switch, shared `ctx`. ← **NEW**
- `frontend/src/features/*`: per-feature `composable.js` + `template.js` modules
  (leads, contacts, customers, opportunities, orders, quotations, accounts,
  activities, dashboard). The monolithic `main.js` was split into these. ← **NEW**
- `frontend/src/components/SearchSelect.js`: reusable searchable link-field control. ← **NEW**
- `frontend/src/constants.js` / `frontend/src/utils.js`: shared constants + `call()` helper.
- `frontend/src/styles.css`: full CRM workspace styling.
- `frontend/src/utils-vn-address.js`: Vietnam Provinces API client with module-level cache. ← **NEW**
- `frontend/src/features/contacts/composable-create.js`: create-contact logic (VN address cascade). ← **NEW**
- `frontend/src/features/contacts/template-create.js`: create-contact MISA-style markup. ← **NEW**
- `frontend/src/features/contacts/template-detail.js`: contact-detail view/edit markup. ← **NEW**
  (detail state lives in `composable-create.js` `useCreateContact`)
- `frontend/src/features/quotations/composable.js`: quotation list logic (items panel + filters). ← **NEW**
- `frontend/src/features/quotations/template.js`: quotation list markup (MISA-style). ← **NEW**
- `frontend/src/features/customers/composable-create.js`: create-customer logic.
- `frontend/src/features/customers/template-create.js`: create-customer HTML template.
- `frontend/src/features/customers/composable.js`: customer detail logic (edit).
- `frontend/src/features/customers/template.js`: customer detail HTML template.
- `dcnet_crm/api.py`: permission-aware APIs and data mapping.
- `dcnet_crm/install.py`: page roles and Workspace Sidebar synchronization.
- `dcnet_crm/hooks.py`: Frappe app metadata and page bundle registration.
- `dcnet_crm/workspace_sidebar/crm.json`: sidebar fixture.
- `dcnet_crm/public/dist/crm.bundle.js`: generated frontend bundle.
- `dcnet_core/erpnext/accounts/custom/address.py`: ERPNextAddress override. ← **MODIFIED**
- `docs/customization/ui/2026-06-13-dcnet-crm-customer-workspace.md`:
  customization log.
- `docs/modules/dcnet-crm/SPEC_MAPPING.md`: specification mapping.

## 5. Routing and Sidebar

The Vue page uses `/desk/dcnet-crm?view=...`.

Known views:

- `dashboard`
- `leads`
- `lead-detail&lead={Lead.name}`  ← **NEW**
- `contacts`
- `create-contact`  ← **NEW**
- `contact-detail&contact={Contact.name}`  ← **NEW**
- `customers`
- `customer-detail&customer={Customer.name}`
- `opportunities`
- `opportunity-detail&opportunity={Opportunity.name}`  ← **NEW**
- `create-sales-order&customer={Customer.name}`        ← **NEW**
- `quotations`  ← **list view implemented (2026-06-17)**
- `create-quotation&customer={Customer.name}`  ← **NEW**
- `orders`
- `activities`  ← **NEW** — standalone Activities workspace
- `care`  ← **NEW (2026-06-25)** — Thẻ chăm sóc list; internal `careView` state
  ('list' | 'detail') switches to the detail/edit/new form (no separate route)

Important implementation details:

- `syncRouteUrl()` keeps the view in the URL and `sessionStorage`.
- `syncNativeSidebarActive()` highlights the matching native sidebar entry.
- The native `Bàn làm việc` sidebar entry routes to `view=dashboard`; there is
  no separate `Tất cả` entry.
- Customer names/codes open the internal customer detail route.
- The Vue app must not render its own left navigation.
- **CRITICAL — race condition:** Do NOT call `frappe.set_route("dcnet-crm")` when already
  on dcnet-crm. It triggers `readRoute` which reads the old URL and resets `route.value`.
  Instead: set `route.value` directly + call `syncRouteUrl()` + `syncNativeSidebarActive()`.
  This pattern is used in `openCreateSO()` and `backToOpportunities()`.

## 6. Customer List

Implemented:

- Dense Customer table.
- Smart-search style input.
- Configurable visible columns.
- Filters.
- Pagination.
- Excel import entry.
- Right-side activity/order/contact preview.
- Toolbar activity button toggles the preview panel.
- Toolbar filter button toggles the filter panel.
- The table expands into the space of either hidden panel and becomes full
  width when both panels are hidden.
- The Activity preview uses the same standard `ToDo` and `Event` records as
  the Customer profile Activity tab.
- The Purchase preview combines related `Quotation`, `Sales Order` and
  `Sales Invoice` records.
- The Contact preview lists Contacts linked to the Customer through
  `Dynamic Link`.
- Do not render an extra selected-Customer summary card above these previews.
- The Customer title dropdown contains standard saved-view entries only; the
  two AI prediction entries from the UX reference are intentionally omitted.
- `Tất cả khách hàng` clears the saved-view constraint.
- `Khách hàng của tôi` filters by `Customer.account_manager` and the current
  Frappe user.
- Partner/CTV and team views remain disabled until their Customer Group and
  employee-team mappings are approved.
- The Customer settings button opens a draft column-customization drawer.
- Column search, select/remove, clear all, default, cancel and save are
  supported. Only Save changes the table.
- Saved Customer columns persist in browser local storage under
  `dcnet-crm-customer-columns`.
- Clicking customer code or name opens the internal profile.

The list reads standard `Customer` records through `get_list()`.

## 6.1 Contact List

Implemented:

- Dense Contact table based on standard `Contact` fields.
- Search, pagination, Excel import and configurable visible columns.
- Permission-aware filters.
- Right-side activity/purchase preview.
- The activity and filter toolbar buttons independently toggle their matching
  panels, using the same responsive grid behavior as the Customer list.

The standalone Contact list remains inside `/desk/dcnet-crm?view=contacts`.

## 6.2 Quotation List (Báo giá)  ← NEW (2026-06-17)

MISA-style "Tất cả báo giá" list at `?view=quotations`. Reuses the
`orders-list-layout` shell (main table + "Hàng hóa" detail panel + "Bộ lọc"
filter panel) and the `orders-*`/`odp-*`/`ofp-*` CSS, so it stays visually
consistent with the Orders list.

- Source files: `frontend/src/features/quotations/{composable,template}.js`.
- Composable `useQuotations(ctx)` owns: items panel state
  (`qtDetailItems`, `loadQuotationDetail`), amount mask, saved filters
  (`QT_SAVED_FILTERS`) and criteria (`QT_FILTER_CRITERIA`).
- Columns match the screenshot: Thẻ (status badge), Số báo giá, Ngày báo giá,
  Hiệu lực đến, Khách hàng, Liên hệ.
- Footer aggregates (current page): Tổng số, Thành tiền (`net_total`),
  Tiền thuế (`total_taxes_and_charges`), Tiền chiết khấu (`discount_amount`),
  Tổng tiền (`grand_total`).
- "Nhập từ Excel" → standard `Quotation` Data Import. "+ Thêm" / row open →
  standard `Quotation` form (no internal create form yet).
- Backend: `RESOURCE_CONFIG["quotations"]` extended; new GET
  `get_quotation_items(name)` returns line items for the detail panel.
- The right "Hàng hóa" panel mirrors the Orders detail panel; expanding a line
  shows đơn giá sau CK / thành tiền / mô tả.

## 6.3 Quotation Create Form (Thêm Báo giá)  ← NEW (2026-06-17)

MISA-style "Thêm Báo giá" form mở trực tiếp tại `?view=create-quotation`,
không popup. Tái sử dụng layout `opportunity-form-page` + items table
`so-items-table` của form Đơn hàng để giữ phong cách nhất quán.

- Source: `frontend/src/features/quotations/{composable,template}.js`.
- Sections:
  1. Thông tin chi tiết — Số báo giá (mã tự sinh), Ngày báo giá *,
     Cơ hội, Tình trạng, Chu kỳ thanh toán *, Khu vực lắp đặt dịch vụ *,
     Khách hàng *, Hiệu lực đến ngày, Liên hệ, Mã số thuế, Email KH.
  2. Thông tin mô tả — Mô tả, Thời gian triển khai, Cam kết chất lượng (SLA).
  3. Thông tin hàng hóa — bảng items 17 cột (STT, Mã, Tên, Mô tả, A-End,
     Z-End, ĐVT, SL, Đơn giá, Thành tiền, Tỷ lệ CK, Tiền CK, Đơn giá sau CK,
     Thành tiền sau CK, Thuế suất, Tiền thuế, Tổng tiền) + dòng Tổng cộng.
  4. Thông tin hệ thống — Người thực hiện, Công ty, Dùng chung.
- Header: "← Quay lại", "Hủy", "Lưu và thêm", "Lưu" (primary).
- Đổi mẫu báo giá qua dropdown trong header (`order_type`).
- Backend: `create_quotation` insert Quotation chuẩn ERPNext, để
  `set_missing_values` chạy (KHÔNG dùng `flags.ignore_validate`); custom
  fields (`custom_a_end`, `custom_z_end`, `custom_dcnet_account_id`,
  `custom_installation_zone`, `custom_contract_duration`, `custom_internal_notes`,
  `custom_implementation_time`, `custom_sla`, `custom_is_shared`,
  `custom_opportunity`) chỉ set khi DocType meta đã có field tương ứng —
  giữ nguyên rule "không bịa data model".
- Nút "+ Thêm" trong list `quotations` mở form này thay vì
  `frappe.new_doc("Quotation")`.

## 6.4 Contact Create Form (Thêm Liên hệ)  ← NEW (2026-06-17)

MISA-style "Thêm Liên hệ" form mở trực tiếp tại `?view=create-contact`,
tái sử dụng layout `ccf-page`/`ccf-card`/`ccf-grid`/`ccf-section` của form
Khách hàng để giữ phong cách nhất quán.

- Source: `frontend/src/features/contacts/{composable-create,template-create}.js`.
- Sections theo mẫu MISA:
  1. **Thông tin chung** — Mã liên hệ (mã tự sinh), Xưng hô, Họ và đệm, Tên *,
     Họ và tên (auto-ghép), Chức danh, Phòng ban, Tổ chức (link Customer),
     Phân loại KH, Không gọi điện, Không gửi Email, Điện thoại khác,
     ĐT di động, Email cá nhân, ĐT cơ quan, Nguồn gốc, Email cơ quan, Zalo.
  2. **Thông tin địa chỉ** — Quốc gia, Tỉnh/Thành phố (cascade 2025),
     Phường/Xã, Mã vùng, Số nhà Đường phố.
  3. **Thông tin địa chỉ giao hàng** — cùng cascade + nút "Sao chép địa chỉ".
  4. **Thông tin mô tả** — Mô tả.
  5. **Thông tin hệ thống** — Dùng chung.
- Header: "← Quay lại", "Hủy", "Lưu và thêm", "Lưu" (primary).
- Backend: `create_contact_standalone` tạo Contact chuẩn, map field Contact
  chuẩn (first/last/middle_name, salutation, designation, company_name,
  department, mobile_no, phone, email_id). Các trường UI-only (Zalo, email
  cá nhân, nguồn gốc, không gọi điện...) hiển thị đúng MISA nhưng chưa có
  custom field → không lưu (ghi nhận pending). Address liên kết Contact +
  Customer cùng một lần.
- `get_contact_create_options` query đúng doctype `Salutation` và `Gender`
  (không lấy từ meta.options như cũ).

## 6.5 Contact Detail / Edit (Chi tiết Liên hệ)  ← NEW (2026-06-17)

Click một liên hệ trong danh sách (route `contacts`) mở trang chi tiết
`?view=contact-detail&contact={name}` ngay trong `dcnet-crm`, layout giống y
form Thêm Liên hệ nhưng ở chế độ xem; nút "Sửa" bật chế độ chỉnh sửa trực tiếp.

- Source: `frontend/src/features/contacts/template-detail.js`; state + logic
  nằm trong `useCreateContact` (`composable-create.js`):
  `loadContactDetail`, `openContactDetail`, `startContactEdit`,
  `cancelContactEdit`, `saveContactDetail`, `backToContacts`.
- Header: "← Quay lại"; khi xem hiện "Sửa" (nếu `can_write`); khi sửa hiện
  "Hủy" + "Lưu".
- Field readonly khi xem, đổi sang input/select khi sửa. Địa chỉ dùng cascade
  VN 2025 (tự match tỉnh từ text khi mở).
- Backend: `get_contact_detail` (đọc) + `update_contact_standalone` (ghi,
  đồng bộ Customer link + Address). Chỉ field Contact/Address CHUẨN; các field
  MISA UI-only (Zalo, email cá nhân...) hiển thị "—" khi xem.
- `openDocument` cho route `contacts` gọi `openContactDetail` thay vì chỉ
  `selectRow`.

## 6.6 Lead Detail + Create/Edit Form (Tiềm năng)  ← NEW (2026-06-25)

Clicking a Lead row opens a MISA-style detail page at `?view=lead-detail&lead={name}`.
A full create/edit form (`leadFormOpen` overlay) handles "+ Thêm" and "Sửa".

- Source: `frontend/src/features/leads/{composable,template}.js`
  (`useLeads(ctx)` composable).
- Reuses `Lead` (standard DocType). Status flow uses standard `Lead.status`.
- Form sections (MISA layout): Thông tin chung, Thông tin doanh nghiệp
  (MST, tài khoản ngân hàng, ngày thành lập, loại hình, lĩnh vực),
  Thông tin địa chỉ, Mô tả, Thông tin hệ thống (Dùng chung).
- Mandatory: Tên (`first_name`), ĐT di động (`mobile_no`).
- "Nhập từ Excel" → standard `Lead` Data Import.

**Lead Custom Fields** (defined in `install.py LEAD_CUSTOM_FIELDS`, synced by
`ensure_lead_custom_fields()` in after_install/after_migrate):
`custom_lead_type`, `custom_zalo`, `custom_work_email`, `custom_tax_id`,
`custom_bank_account`, `custom_bank_name`, `custom_founding_date`,
`custom_business_type`, `custom_sector`, `custom_district`, `custom_ward`,
`custom_full_address`, `custom_is_shared`.

**Server methods:**
- `get_lead_detail(name)` — GET. Document + `can_write`.
- `get_lead_form_options()` — GET. salutations, sources, industries, countries, companies.
- `save_lead(lead)` — POST. Creates a standard Lead.
- `update_lead(name, data)` — POST. Updates Lead (used by both detail edit + form edit).

## 7. Customer Profile

The profile has a fixed summary panel and these tabs:

- Thong tin chi tiet
- Lien he
- Hoat dong
- Ban hang
- Ho tro
- Marketing
- Ghi chu va dinh kem
- Trao doi is visible in the reference but is not implemented yet.

### 7.1 Detail Tab

Implemented inline view/edit for:

- Customer fields.
- Primary Contact.
- Primary billing Address (with Vietnam 2025 province/ward cascade dropdowns).

The header `Sua` button switches to `Huy` and `Luu`. It must not call:

```javascript
frappe.set_route("Form", "Customer", ...)
```

Server method: `update_customer_details`.

Contact email and phone values are stored through standard child tables:

- `Contact Email`
- `Contact Phone`

**Address ERPNext field mapping:**
- `state` = Tỉnh/Thành phố (province name from 2025 list)
- `county` = Phường/Xã (ward name)
- `city` = auto-filled from state or county (ERPNext mandatory, not user-facing)
- `address_line1` = Số nhà/đường phố (ERPNext mandatory, auto-filled from ward+province when blank)

**Optimistic lock fix:** `_update_customer_contact` and `_update_customer_address` previously called
`customer.save()` causing a `TimestampMismatchError` when the address `on_update` hook
also updated the Customer record. Fixed: both functions now use
`frappe.db.set_value(..., update_modified=False)` to set `customer_primary_contact` /
`customer_primary_address` without changing the Customer's `modified` timestamp.
`address.py on_update` also uses `update_modified=False` when syncing `primary_address` display.

### 7.2 Contact Tab

Implemented:

- Dense table matching the supplied screenshot.
- Pagination.
- Full create modal.
- Quick-create modal.
- Inline edit modal when clicking a contact name.
- Select existing Contact modal.
- Existing Contact is linked using `Dynamic Link`.

Server methods:

- `save_customer_contact`
- `search_customer_contacts`
- `link_customer_contact`

Do not route Contact edits from this tab to the standard Contact form.

### 7.3 Activity Tab

Implemented:

- Table columns: activity name, type, due date, status, end date, performer.
- Pagination.
- Create/edit task modal.
- Create/edit meeting modal.
- Create/edit call modal.

Mapping:

- Task -> `ToDo`.
- Meeting -> `Event.event_category = "Meeting"`.
- Call -> `Event.event_category = "Call"`.
- Customer and assigned User are stored in `Event Participants`.

Server method: `save_customer_activity`.

Tested with transaction rollback for all three activity types.

### 7.4 Sales Tab

Left menu implemented:

- Orders -> `Sales Order`
- Sales returns -> `Sales Invoice.is_return = 1`
- Opportunities -> `Opportunity`
- Quotations -> `Quotation`
- Invoices -> `Sales Invoice.is_return = 0`
- Purchased items -> aggregate submitted `Sales Invoice Item`
- Dealer/Subsidiary -> empty state only

The Dealer/Subsidiary relation is not defined in the specification. Do not
invent a field or DocType until clarified.

The `Sinh don hang` and `Them Don hang` actions currently use standard
`frappe.new_doc("Sales Order", { customer })`. This remains in the same site,
but opens the standard Sales Order creation flow.

## 7.5 Opportunity Detail Page  ← NEW (2026-06-15)

Clicking an Opportunity row opens a MISA-style full-detail page at
`?view=opportunity-detail&opportunity={name}`.

**Layout:**
- Left sidebar: sticky summary card (customer, value, closing date, owner,
  type, source, stage) — **no** "+ Thêm thẻ" tag button.
- Header: back button, Opportunity name, status badge, Edit/Save/Cancel
  buttons, stage chevron bar, "🛒 Sinh đơn hàng" button.
- Main content: tab bar + tab content area.

**Stage chevron bar:**
- MISA-style clip-path arrows. Colors: amber (in-progress), navy (upcoming),
  green (Thắng/Won), red (Thua/Lost).
- Stages are rendered as `<button>` elements. Clicking any stage calls
  `setOpportunityStage(stage)` which calls `update_opportunity` API and
  updates `opportunityDetail.value.document.sales_stage` optimistically.
- Win/loss buttons show 🏆 / 🚩 icons.

**9 tabs:**
1. Tổng quan — 2-column overview: left (stage, value, dates, owner) + right
   (recent comments, next activity, last email).
2. Thông tin chi tiết — inline edit for all Opportunity header fields.
3. Hàng hóa — Opportunity Item child table (read-only display).
4. Ghi chú & đính kèm — text notes + file attachments list.
5. Liên hệ — linked Contacts.
6. Bán hàng — linked Sales Orders, Quotations, Sales Invoices by customer.
7. Hoạt động — ToDo/Event timeline.
8. Trao đổi — Communications (email/comments).
9. Hỗ trợ — empty state for now.

**State refs:**
- `opportunityDetailName` — name of the currently opened Opportunity.
- `opportunityDetail` — object `{ document, items, timeline, comments,
  activities, contacts, quotations, orders, invoices, attachments, can_write }`.
- `opportunityDetailTab` — active tab index.
- `opportunityDetailEditing` — boolean for edit mode.
- `opportunityDetailForm` — shallow copy of `document` fields for editing.

**Server method:** `get_opportunity_detail(name)` — GET whitelisted.
Returns all the above sub-objects in one call.

**Server method:** `update_opportunity(name, data)` — POST whitelisted.
Allowed field set: `sales_stage`, `probability`, `expected_closing`,
`opportunity_amount`, `currency`, `opportunity_type`, `source`, `territory`,
`campaign`, `contact_person`, `company`.

**Known issue — Sales Order field-level permission:**
`frappe.get_list("Sales Order", filters={"opportunity": name})` is blocked by
field-level permission even for Administrator. Fix already applied: filter
Sales Orders by **customer only** (no `opportunity` filter).

## 7.6 Opportunity List

Implemented:

- Dedicated dense Opportunity workspace at `?view=opportunities`.
- Standard Opportunity columns for title, contact, amount, sales stage,
  expected closing date, type, owner and creation date.
- Search, pagination, filters, Excel import and panel visibility controls.
- Right preview tabs: Activity, Customer, Contact and Items.
- Opportunity items are read from the standard `Opportunity Item` child table.
- Activity notes use the standard Opportunity timeline.

## 7.7 "Sinh đơn hàng" — Inline Sales Order Creation  ← UPDATED (2026-06-15)

Triggered from:
- "🛒 Sinh đơn hàng" button on Opportunity detail header.
- "Thêm đơn hàng" / customer order button on Customer profile Sales tab.

Route: `?view=create-sales-order&customer={Customer.name}`

**DO NOT** call `frappe.set_route("dcnet-crm")` to navigate here — use
`openCreateSO()` which sets `route.value` directly to avoid the race condition.

**UI:** The form uses **100% the same layout as the Opportunity create form**
(`opportunity-form-page` full-page overlay). Only the fields and sections differ.
The layout consists of:
- `opportunity-form-page` — absolute overlay, z-index 900, `#f3f5f9` background.
- `opportunity-form-header` — white header with "← Quay lại", title "Sinh đơn hàng",
  order-type dropdown (`.so-type-badge` / `.so-type-sel`), Hủy and Lưu buttons.
- `opportunity-form-card` — white scrollable card, same padding as Opportunity form.

**Form sections (6):**

1. *Thông tin chung (2-column `opportunity-form-grid`, 17 fields):*
   Khách hàng*, Liên hệ, Cơ hội, Ngày đặt hàng*, Hạn giao hàng,
   Số HĐ/PO KH, Ngày ký HĐ, Thời hạn HĐ (tháng), Ngày hết hạn HĐ (disabled),
   Khu vực lắp đặt, Chiến dịch, Bảng giá, Tiền tệ,
   Điều khoản thanh toán, Phí & Thuế, Khu vực, Công ty.

2. *Thông tin hàng hóa (15-column `opportunity-items-table so-items-table`):*
   STT | Mã hàng | Tên hàng | Mô tả | A-End | Z-End | ĐVT | SL |
   Đơn giá | Thành tiền | Tỷ lệ CK | Tiền CK | Đơn giá sau CK | Thành tiền sau CK | Thuế suất

   - Thay đổi Đơn giá/CK% → `updateSOItemRate()` tính lại Đơn giá.
   - Thay đổi Đơn giá/SL → `updateSOItemAmount()` tính lại Thành tiền.
   - Row total footer: Tổng SL | Thành tiền | Tiền CK | Thành tiền sau CK.
   - Empty state: nút "＋ Thêm dòng". When rows exist: "＋ Thêm dòng" button below table.

3. *Thông tin mô tả:*
   Tiêu đề / Diễn giải (input), Ghi chú (textarea) — dùng `opportunity-notes` label layout.

4. *Tình trạng thực hiện đơn hàng (2-column grid):*
   Tình trạng*, Tình trạng ghi doanh số (disabled=Bản nhập), Ngày ghi doanh số,
   Chu kỳ thanh toán, Hạn thanh toán, Ngày nghiệm thu tính cước (disabled).

5. *Thông tin hóa đơn (2-column grid):*
   Khách hàng HĐ, Người mua hàng, Quốc gia, Tỉnh/Thành phố, Địa chỉ (full-width).

6. *Thông tin giao hàng (2-column grid):*
   Người nhận hàng, Điện thoại, Quốc gia, Tỉnh/Thành phố, Địa chỉ (full-width).

**State refs:**
- `createSOContext` — `{ customer, customerName, opportunity }`.
- `createSOForm` — all header fields including: customer, contact_person, opportunity,
  order_type, transaction_date, delivery_date, po_no, po_date, contract_duration,
  contract_expiry, installation_zone, campaign, selling_price_list, currency,
  payment_terms_template, taxes_and_charges, territory, company, title, note,
  execution_status, revenue_recognition_date, revenue_status, payment_due_date,
  acceptance_date, billing_customer, billing_address, shipping_recipient, shipping_address.
- `createSOItems` — array of `{ item_code, item_name, description, a_end, z_end, uom, qty, price_list_rate, discount_percentage, rate, amount, tax_rate }`.
- `createSOSaving` — boolean.

**Helper functions:**
- `_soBlankItem()` — blank item row with all 15 columns.
- `openCreateSO(customer, custDisplayName, opportunity)` — initializes state
  and navigates to `create-sales-order` view.
- `addSOItem()`, `removeSOItem(idx)`, `clearSOItems()`.
- `updateSOItemAmount(item)`, `updateSOItemRate(item)`.
- `soItemPreTotal(item)`, `soItemDiscount(item)`.
- `soSubtotal()`, `soTotalDiscount()`, `soGrandTotal()`, `soTotalQty()`.
- `saveCreateSO()` — calls `create_sales_order` API, then navigates back to
  customer-detail (or orders if no customer context).

**Server method:** `create_sales_order(data)` — POST whitelisted.
Creates a real ERPNext `Sales Order` document. The SO is visible in
Selling → Sales Order in the standard ERPNext UI. Supported fields:
customer, company, currency, selling_price_list, territory,
payment_terms_template, taxes_and_charges, order_type, po_no, po_date,
transaction_date, delivery_date, contact_person, opportunity, title, note.
Each item: item_code, item_name, description, qty, uom, price_list_rate,
discount_percentage, rate, warehouse, delivery_date.

**CSS selectors (new pattern):**
Reuses all `.opportunity-form-*`, `.opportunity-items-*`, `.opportunity-section-heading`,
`.opportunity-notes`, `.item-stt-cell`, `.item-row-del`, `.item-calc-cell`,
`.items-total-row`, `.item-action-btns` classes from the Opportunity form.
SO-specific additions in `styles.css`:
- `.so-type-badge`, `.so-type-sel` — order type dropdown in header.
- `.so-items-table` — extends `min-width: 2200px` and adds `th:nth-child(15) { width: 110px }` for Thuế suất column.

### Internal Opportunity Create Form

- The Opportunity `Thêm` action opens a full-page form inside `dcnet_crm`.
- Initialize the Opportunity form model before setting `opportunityFormOpen`;
  the template reads `items.length` immediately when the form mounts.
- Implemented standard fields: Customer, Contact, title, Opportunity Type,
  probability, expected closing date, Sales Stage, Territory, Company,
  Opportunity Items and notes.
- Save and Save-and-add use `save_opportunity` with Frappe permission checks.
- Opportunity Items use the standard `Opportunity Item` child table.
- Source, A-End/Z-End installation points, detailed Vietnamese delivery
  address, shared flag, custom opportunity code and Partner/CTV referral are
  visible as disabled placeholders because no approved Custom Field mapping
  exists yet.

## 7.12 Vietnam 2025 Address — Province/Ward Cascade Dropdowns  ← NEW (2026-06-17)

Vietnam's 2025 administrative reform eliminated all districts (quận/huyện).
Address structure is now **Province → Ward** (2 levels only, 63 → 34 provinces).

### API client: `utils-vn-address.js`

```javascript
import { fetchVnProvinces, fetchVnWards } from "../../utils-vn-address.js";
```

- `fetchVnProvinces()` → `GET https://provinces.open-api.vn/api/v2/p/` — returns 34 provinces.
- `fetchVnWards(provinceCode)` → `GET /p/{code}?depth=2` — returns wards for that province.
- Module-level caching: provinces cached after first fetch, wards cached per province code.

### Create form (`composable-create.js`)

**New refs:**
- `vnProvinces`, `vnBillingWards`, `vnShippingWards` — lists from API.
- `vnLoadingBillingWards`, `vnLoadingShippingWards` — spinner state.
- `billingProvinceCode`, `shippingProvinceCode` — selected province code (drives cascade).
- `_pendingBillingWard`, `_pendingShippingWard` — ward name to auto-select after wards load
  (used when MST lookup fires before wards API resolves).

**Watchers:** `billingProvinceCode` and `shippingProvinceCode` each fire an async watcher that:
1. Clears `state`/`county` on the form.
2. Fetches wards for the new code.
3. Auto-selects the pending ward (if set) after wards load.

**MST lookup fills BOTH billing and shipping address simultaneously.**

**Province matching:** `_matchProvince(rawName)` normalizes and fuzzy-matches old province names
(e.g. "Đồng Tháp") against the 2025 list. If no match, province is saved as raw text.

**MST regex:** supports branch MST format `XXXXXXXXXX-XXX` (with hyphen).
Pattern: `^\d{10}(-\d{3})?$` — in both frontend and `api.py`.

### MST duplicate detection

`lookup_taxpayer` in `api.py` now checks `frappe.db.get_value("Customer", {"tax_id": ...})`
after a successful GDT lookup. If a match is found, it adds `existing_customer: {name, customer_name}`
to the response. Frontend sets `taxLookupStatus = "duplicate"` and blocks save with a msgprint.

### MST inactive status warning

If GDT returns a status that does NOT include "đang hoạt động", `taxLookupStatus` is set to
`"found-inactive"`. The AVA banner turns red and shows the status text. Clicking Lưu triggers
`frappe.confirm` — user can still proceed or cancel.

**`taxLookupStatus` values:**
| Value | Meaning | Save allowed? |
|-------|---------|--------------|
| `"found"` | Active in GDT, not in DB | Yes |
| `"found-inactive"` | Found in GDT but not active | Yes (after confirm) |
| `"not-found"` | Not on GDT | Yes |
| `"duplicate"` | Already in ERPNext DB | **No** |
| `"error"` | Network/API error | Yes |

### Detail edit form (`composable.js`)

**New refs:** `editVnProvinces`, `editVnWards`, `editVnLoadingWards`, `editProvinceCode`.

`beginCustomerEdit()` loads provinces and fuzzy-matches the current `address.state` to
pre-select the province dropdown. Ward is loaded after province resolves, then
the existing `county` value is matched and restored.

`cancelCustomerEdit()` resets `editProvinceCode` and `editVnWards`.

### ERPNext mandatory field auto-fill (`_update_customer_address` in `api.py`)

`Address.city` and `Address.address_line1` are mandatory in ERPNext but not user-facing in CRM.
Defaults:
```python
if not address_doc.city:
    address_doc.city = address_doc.state or address_doc.county or "-"
if not address_doc.address_line1:
    parts = [p for p in [address_doc.county, address_doc.state] if p and p != "-"]
    address_doc.address_line1 = ", ".join(parts) if parts else "-"
```

### `address.py` (dcnet_core)

`ERPNextAddress` subclass at `dcnet_core/erpnext/accounts/custom/address.py`.

**Defensive `getattr`:** `is_your_company_address` is a custom field that may not be in DB yet.
Always use `getattr(self, "is_your_company_address", None)` — never `self.is_your_company_address`.

**`on_update` — `update_modified=False`:** When updating `primary_address` display text on
linked Customer records, `frappe.db.set_value(..., update_modified=False)` prevents changing
the Customer's `modified` timestamp (which would cause optimistic-lock conflicts for any
ongoing `update_customer_details` request).

## 7.13 Activities Workspace — Standalone "Hoạt động" View  ← NEW (2026-06-20)

Route: `?view=activities`. Accessible from sidebar "Hoạt động" link.

### Data model

Activities are stored as standard `ToDo` records with two custom fields (defined in `install.py`):
- `custom_related_users` (Small Text) — JSON array of `[{name: "email", full_name: "..."}]`
- `custom_task_type` (Data) — free-text label, one of the 15 known task types

### Permission model (role-based scoping)

`get_activity_list` uses raw SQL with an OR condition:
- Users with roles in `_ACTIVITY_FULL_ACCESS_ROLES` (`System Manager`, `Administrator`, `Sales Manager`, `Sales Master Manager`) → see all ToDos.
- Other users → see only ToDos where `owner = current_user` OR `custom_related_users LIKE '%current_user%'`.

`_user_can_access_todo(todo, perm)` helper (used in `get_activity_detail` and `update_activity`):
1. Checks `frappe.has_permission("ToDo", perm, doc=todo)` first (standard Frappe).
2. Falls back to scanning `custom_related_users` JSON for the current user's email.
This allows related users (e.g. KT) to read/update without requiring a `DocShare` record.

### SO Action Modal

Clicking action items (Đề nghị xuất hóa đơn, Giao hàng, etc.) in the Order detail page no longer calls `create_so_action` directly. Instead it opens a modal form (`soa-*` CSS classes) where the user fills:
- **Tiêu đề** (freetext, overrides auto-generated description)
- **Hạn hoàn thành** (date)
- **Mức độ ưu tiên** (Low / Medium / High)
- **Trạng thái** (Open / Replied / Closed)
- **Người liên quan** (multi-user picker with avatar + checkmark, `onUserFocus` / `toggleRelatedUser` pattern)
- **Loại nhiệm vụ** (searchable dropdown from `_MODAL_TASK_TYPES` list)

On confirm, calls `create_so_action(so_name, action, extra=JSON)` where `extra` contains all form fields.

`action="activity"` is also accepted — creates a plain ToDo without triggering any SO workflow.

### `create_so_action` — `extra` dict

```python
# extra keys consumed by create_so_action:
{
  "title": str,           # overrides auto-description if non-blank
  "task_type": str,       # stored in custom_task_type + used as label when no SO action label
  "date": str,            # ISO date, defaults to today
  "priority": str,        # "Low" | "Medium" | "High"
  "status": str,          # "Open" | "Replied" | "Closed"
  "related_users": [{"name": "email@...", "full_name": "..."}]
}
```

### Task type parsing — `_ACTIVITY_TASK_TYPES` frozenset

`api.py` defines `_ACTIVITY_TASK_TYPES` (frozenset of 15 Vietnamese labels). When building
the activity list/detail from a ToDo's `description` field, task type is extracted by scanning
all `" - "`-split parts for a known type — NOT by positional index. This handles both
old format (`"Đề nghị xuất hóa đơn - SAL-ORD-..."`) and new format (`"2026-06-20 - Đề nghị xuất hóa đơn - ..."`).

```python
_ACTIVITY_TASK_TYPES = frozenset([
    "Đề nghị xuất hóa đơn", "Giao hàng", "Đề nghị trả hàng", "Yêu cầu mua hàng",
    "Gửi báo giá", "Nhắc cước đến hạn", "Check TT DVVT", "Khảo sát DVVT",
    "Triển khai DVVT", "Lập PAKD", "Nghiệm thu DVVT", "Hỗ trợ kỹ thuật",
    "Chăm sóc khách hàng", "Họp tư vấn", "Khác",
])
```

### Notifications — `Notification Log`

When `create_so_action` or `update_activity` assigns related users, each user receives:
1. **DocShare** — `frappe.share.add("ToDo", name, user_email, read=1, flags={"ignore_share_permission": True})` so they can open the standard ToDo if needed.
2. **Notification Log** insert — persistent bell icon entry. Clicking navigates to CRM page (not standard ToDo form) via `document_type="Page"`, `document_name="dcnet-crm"`.

`_send_todo_notification(user_email, subject, todo_name)` helper encapsulates this.
Frappe automatically pushes a realtime badge update when `Notification Log` is inserted.

### CRM Page roles

`CRM_PAGE_ROLES` in `install.py`:
```python
CRM_PAGE_ROLES = ("Sales Manager", "Sales User", "System Manager", "Accounts Manager", "Accounts User")
```
`Accounts Manager` and `Accounts User` were added so KT role can access the CRM page to view and confirm activities assigned to them.

### Source files

- `frontend/src/features/activities/composable.js` — `useActivities(ctx)` composable (list state, detail state, edit form, user/tasktype pickers)
- `frontend/src/features/activities/template.js` — Activities list + detail/edit form (reuses `hd-ef-*` CSS from Customer header edit form)
- `dcnet_crm/api.py` — `get_activity_list`, `get_activity_detail`, `create_activity`, `update_activity`, `create_so_action` (updated), `_send_todo_notification`, `_user_can_access_todo`, `_ACTIVITY_TASK_TYPES`, `_ACTIVITY_FULL_ACCESS_ROLES`
- CSS selectors added for SO action modal: `.soa-overlay`, `.soa-modal`, `.soa-modal-header`, `.soa-modal-title`, `.soa-modal-actions`, `.soa-modal-body`

## 8. API Notes

Important public methods in `dcnet_crm/api.py`:

- `get_boot`
- `get_list`
- `get_document`
- `get_customer_workspace`
- `update_customer_details`
- `save_customer_contact`
- `search_customer_contacts`
- `link_customer_contact`
- `save_customer_activity`
- `add_note`
- `get_dashboard`
- `get_opportunity_detail(name)` — GET. Returns document + items + timeline +
  comments + activities + contacts + quotations + orders + invoices +
  attachments + can_write. ← **NEW**
- `update_opportunity(name, data)` — POST. Allowed field allowlist only.
  Do NOT pass arbitrary fields. ← **NEW**
- `create_sales_order(data)` — POST. Creates a real ERPNext Sales Order.
  Returns `{ name, grand_total }`. ← **NEW**
- `update_sales_order(name, data)` — POST. Updates draft or submitted SO.
  Uses explicit short-key → DocType-field mapping. Sets `ignore_validate = True`.
- `get_quotation_items(name)` — GET. Returns Quotation line items for the
  Báo giá list detail panel. ← **NEW**
- `get_contact_create_options()` — GET. Dropdowns cho form Thêm Liên hệ
  (salutations, genders, designations, departments, customers, countries). ← **NEW**
- `create_contact_standalone(data)` — POST. Tạo Contact chuẩn ERPNext, link
  Customer + Address tuỳ chọn. Trả `{ name, full_name }`. ← **NEW**
- `get_contact_detail(name)` — GET. Dữ liệu Contact + customer link + địa chỉ
  chính + `can_write` cho trang chi tiết. ← **NEW**
- `update_contact_standalone(name, data)` — POST. Cập nhật Contact + Address,
  đồng bộ Customer link. ← **NEW**
- `get_quotation_form_options(customer=None)` — GET. Dropdowns cho form
  Thêm Báo giá (items, opportunities, contacts, price_lists, payment_terms,
  territories, campaigns, taxes_templates). ← **NEW**
- `create_quotation(data)` — POST. Tạo Quotation từ form CRM nội bộ
  (mẫu báo giá DVVT). Trả `{ name, grand_total }`. ← **NEW**
- `get_or_create_service_account(customer, item_code, a_end, z_end)` — POST. Idempotent.
- `get_customer_service_accounts(customer, item_code)` — GET. For datalist suggestions.
- `get_service_accounts_list(search, page, page_length)` — GET. Paginated.
- `get_service_account_detail(account_code)` — GET. Doc + linked SO list.
- `lookup_taxpayer(tax_code)` — GET. Proxies GDT via xinvoice API. Now also checks
  `Customer.tax_id` in DB and returns `existing_customer: {name, customer_name}` if found.
  Supports branch MST format `XXXXXXXXXX-XXX` (regex `^\d{10}(-\d{3})?$`). ← **UPDATED**
- `get_customer_create_options` — GET. Returns countries, customer_groups, territories,
  industries. Uses `ignore_permissions=True` for Country lookup.
- `get_activity_list(search, page, page_length, status)` — GET. Raw SQL with role-based
  OR filter (owner OR custom_related_users). Returns paginated list + total. ← **NEW**
- `get_activity_detail(name)` — GET. Returns ToDo fields + related_users JSON parsed.
  Uses `_user_can_access_todo` — accessible even if user is only in related_users. ← **NEW**
- `create_activity(data)` — POST. Creates ToDo, assigns related users via DocShare + Notification Log. ← **NEW**
- `update_activity(name, data)` — POST. Updates ToDo. Notifies newly added related users. ← **NEW**
- `create_so_action(so_name, action, extra)` — POST. Creates SO-linked ToDo. `extra` is JSON
  dict with `title`, `task_type`, `date`, `priority`, `status`, `related_users`. ← **UPDATED**
- `create_customer(data)` — POST. Creates a standard Customer from the CRM create form. ← **NEW**
- `search_crm_users(search)` — GET. User picker (related-users / assignment lookups). ← **NEW**
- `get_lead_detail(name)` — GET. Lead document + `can_write`. ← **NEW**
- `get_lead_form_options()` — GET. salutations, sources, industries, countries, companies. ← **NEW**
- `save_lead(lead)` — POST. Creates a standard Lead. ← **NEW**
- `update_lead(name, data)` — POST. Updates a Lead. ← **NEW**
- `get_so_detail(name)` — GET. Full Sales Order document for the order detail page. ← **NEW**
- `get_so_items(name)` — GET. Sales Order line items. ← **NEW**
- `get_so_form_options(customer=None)` — GET. Dropdowns for the SO create/edit form. ← **NEW**
- `update_so_items(name, items)` — POST. Update only the SO items child table. ← **NEW**
- `get_so_stock_balance(name)` — GET. Per-warehouse stock balance for each SO item (from `Bin`). ← **NEW**
- `get_care_card_detail(name)` — GET. `CRM Care Card` doc + `customer_info` +
  three timelines: `activities` (Communication+ToDo), `purchases` (SO+SI),
  `care` (Comments on the card). Includes `can_write`. ← **NEW (2026-06-25)**
- `add_care_note(name, content)` — POST. Adds a `Comment` to a care card (feeds
  the Chăm sóc timeline). ← **NEW (2026-06-25)**
- `save_care_card(name=None, data=None)` — POST. Creates (name empty) or updates
  a `CRM Care Card`. Editable allowlist `_CARE_CARD_EDITABLE`. Returns
  `{ name }`. ← **NEW (2026-06-25)**
- `get_list(resource="care_cards", ...)` — the generic list endpoint now serves
  care cards via `RESOURCE_CONFIG["care_cards"]`. ← **NEW (2026-06-25)**

Important rules:

- Use `frappe.get_list` for permission-aware reads.
- Use `frappe.get_all` only for child/link discovery or internal aggregation
  after the parent permission has been checked.
- Check write/create permission before every mutation.
- Frappe v16 blocks SQL aggregate strings such as `sum(qty) as qty`.
  Use structured aggregate fields:

```python
{"SUM": "qty", "as": "qty"}
```

## 9. Build and Deploy

Host `node_modules` was installed for the Linux container, so host macOS
`npm run build` can fail with an incompatible `esbuild` binary. Build inside
the devcontainer:

```bash
docker exec devcontainer-frappe-1 bash -lc \
  'cd /workspace/development/frappe-bench && bench build --app dcnet_crm'

docker exec devcontainer-frappe-1 bash -lc \
  'cd /workspace/development/frappe-bench && \
   bench --site flow.local clear-cache && \
   bench --site flow.local clear-website-cache'
```

For schema/install changes:

```bash
docker exec devcontainer-frappe-1 bash -lc \
  'cd /workspace/development/frappe-bench && bench --site flow.local migrate'
```

Browser may require `Ctrl + Shift + R`.

## 10. Verification Already Performed

- Python compile for `dcnet_crm/api.py`.
- Frontend bundle build in `devcontainer-frappe-1`.
- Opportunity Custom Fields synchronized by `after_migrate`.
- Opportunity create tested with shipping fields, referral partner and
  A-End/Z-End item fields in a transaction, then rolled back.
- Asset served by HTTP matches the generated bundle SHA-256.
- `get_customer_workspace` tested against real Customer data.
- Inline Customer/Contact/Address update tested in a transaction then rolled
  back.
- Contact creation and linking tested in a transaction then rolled back.
- Task, meeting and call creation tested in a transaction then rolled back.
- Purchased-item aggregate query validated with Frappe v16 structured fields.
- **Opportunity detail page** — full 9-tab layout rendered correctly in browser.
- **Stage chevron bar** — click updates `sales_stage` via API, visual state
  updates immediately.
- **Sales Order field-level permission** — confirmed `opportunity` filter causes
  PermissionError even for Administrator; fixed by querying SO by customer only.
- **`create-sales-order` route race condition** — confirmed `frappe.set_route`
  triggers `readRoute` and resets `route.value`; fixed by not calling
  `frappe.set_route`.
- **Inline SO form** — renders correctly at `?view=create-sales-order`.
- `create_sales_order` API build succeeded (bundle 414.8 kB).
- **SO form UI rebuild** — replaced `mso-*` layout with `opportunity-form-page` overlay
  pattern (same as Opportunity create form). 6 sections, 15-column items table.
  Bundle 454.8 kB.
- **Order detail "Thông tin chi tiết" tab** — 7-section MISA-style grid view with toggle
  for empty fields. Bundle ~596 kB.
- **Left sidebar scroll fix** — `height: 100%; overflow: hidden` chain added to
  `.layout-main-section`, `.dcnet-crm-root`, `.dcnet-crm`. Sidebar now stays sticky.
- **Edit order flow** — `soEditMode` flag reuses create form for edit. `openEditSO()`,
  `cancelEditSO()`, `saveCreateSO()` edit branch all verified. Bundle ~599 kB.
- **Service Accounts** — `DCNET Service Account` DocType, `get_or_create_service_account`
  idempotent upsert, Account column in SO items table (create/edit), Account column in
  order detail "Hàng hóa" tab + "Thông tin chi tiết" tab, "Quản lý accounts" management
  view. Bundle 661.5 kB.
- **CRM "Cập nhật" fix** — rewrote `update_sales_order` with explicit field key mapping;
  items + header fields now save correctly.
- **Warehouse validation bypass** — `ignore_validate = True` on all CRM SO saves.
- **Account badge CSS** — hardcoded hex `#eff4ff`/`#2b4acb` instead of undefined
  `--crm-primary-light` variable.

- **Vietnam address cascade** — province/ward dropdowns working in both create form and detail edit.
- **MST branch format** — `0110631368-001` style now parsed correctly in both frontend and backend.
- **MST duplicate detection** — duplicate banner shown; save blocked with msgprint.
- **MST inactive warning** — red banner + `frappe.confirm` dialog; user can still save.
- **Optimistic lock fix** — `_update_customer_contact` / `_update_customer_address` now use
  `frappe.db.set_value(update_modified=False)`; `on_update` in `address.py` also uses it.
  "Customer has been modified" error no longer occurs on detail save.
- **Address mandatory fields** — `city` and `address_line1` auto-filled when blank.
- **`address.py` AttributeError** — `getattr` defensive access prevents crash when
  `is_your_company_address` custom field not yet synced to DB.
- **CRM Care Card (2026-06-25)** — DocType created via `migrate`; `bench`-console
  verified: autoname → `CS0000001`, `fetch_from` populated customer_name + tax_id;
  `get_list("care_cards")`, `get_care_card_detail`, `save_care_card` (create +
  update with all new fields) all returned correctly; sidebar route confirmed
  `{"view": "care"}`. Frontend bundle built in container (946.6 kB).

Site tests are disabled because `flow.local` has `allow_tests = false`.
Do not silently change that site setting.

## 10.1 Opportunity Create Form

- Opens inside `/desk/dcnet-crm` and preserves the native Frappe sidebar.
- Uses standard fields for Customer, Contact, UTM Source, Opportunity Type,
  Sales Stage, Territory, Company and Opportunity Item.
- `dcnet_crm.install.ensure_opportunity_custom_fields` owns the additional
  Opportunity and Opportunity Item fields. Do not recreate them in
  `dcnet_apps`.
- Additional fields cover shipping address, shared flag, generated
  opportunity code, referral partner and A-End/Z-End installation points.
- Frontend source is in `frontend/src/main.js`; form layout is under the
  `.opportunity-form-*` selectors in `frontend/src/styles.css`.

## 11. Current Limitations and Clarifications

- Support tab is an empty state (both Customer profile and Opportunity detail).
- Marketing tab is an empty state.
- Dealer/Subsidiary has no approved relation mapping.
- Trade/sales return creation UI is not implemented; existing returns display.
- Purchased items require submitted non-return Sales Invoices.
- Notes/attachments currently display existing files; full file upload/delete
  workflow is not implemented.
- Customer care card — ✅ implemented as the `CRM Care Card` DocType + `?view=care`
  feature (see §7.16). Remaining: `item`/`sales_order`/`order_executor` edit
  fields are plain text (no autocomplete); detail tabs other than "Thông tin
  chi tiết" are empty states; "Nhập từ Excel" is a placeholder.
- `Trao doi` tab in Customer profile is not implemented.
- Zalo, Messenger, Facebook and SMS integrations require provider/credential
  clarification.
- Activities list currently shows all ToDos visible to the current user (role-filtered).
  The standalone sidebar item `Hoat dong` now routes to `?view=activities` in CRM.
- **Opportunity detail tabs 3–9** are UI shells — data binding is partial.
  Tab 1 (Tổng quan), Tab 2 (Thông tin chi tiết) and Tab 6 (Bán hàng) are the
  most complete.
- **Inline SO form** — header fields are plain text inputs, not linked-field
  controls. No auto-complete for Item Code, Contact, Territory etc.
  These are acceptable for MVP; add `frappe.call("frappe.client.get_list")`
  autocomplete when requested.
- **SO Custom Fields** — ✅ DONE (confirmed per `docs/plans/2026-06-15-confirm-so-crm.md`).
  "Thời hạn HĐ (tháng)" (`custom_contract_duration`), "Ngày hết hạn HĐ"
  (`custom_contract_expiry`), "Khu vực lắp đặt" (`custom_installation_zone`),
  "A-End/Z-End" (`custom_a_end`/`custom_z_end`), execution/revenue/payment/
  acceptance status fields are now real ERPNext Custom Fields in
  `dcnet_apps/dcnet_apps/fixtures/custom_field.json` and are persisted by both
  `create_sales_order` and `update_sales_order` (via `_set_if(...)`).
- SO form `contract_expiry` and `acceptance_date` are still rendered as `disabled`
  inputs because their auto-fill compute logic (from contract_duration / delivery
  milestone) is not implemented — the underlying Custom Fields exist and save.
- `setOpportunityStage()` calls `update_opportunity` with only `sales_stage`.
  It does not trigger any ERPNext Workflow. If a Workflow is configured on
  Opportunity, it may reject stage changes — check before enabling Workflows.

## 7.8 Order Detail — "Thông tin chi tiết" Tab  ← NEW (2026-06-16)

The first tab of the order detail page was renamed from "Thông tin chung" to "Thông tin chi tiết" and rebuilt as a comprehensive multi-section read-only view matching MISA AMIS CRM.

**Layout:** 7 collapsible sections, each using a 2-column `.sod-detail-grid` CSS Grid.

**Sections:**
1. *Thông tin chung* — 12 field pairs: Khách hàng, Tên HĐ/PO, Cơ hội, Loại đơn hàng, Ngày đặt hàng, Ngày giao hàng, Số HĐ KH, Ngày ký HĐ, Thời hạn HĐ, Ngày hết hạn HĐ, Khu vực lắp đặt, Chiến dịch.
2. *Thông tin mô tả* — full-width: Tiêu đề, Ghi chú.
3. *Thông tin hàng hóa* — inline goods table (same as Items tab) + "Loại hàng hóa" auto-derived from unique item codes.
4. *Tình trạng thực hiện đơn hàng* — Tình trạng, Tình trạng ghi DT, Ngày ghi DT, Chu kỳ TT, Hạn TT, Ngày nghiệm thu.
5. *Thông tin hóa đơn* — Khách hàng HĐ, Người mua, Địa chỉ.
6. *Thông tin giao hàng* — Người nhận, Điện thoại, Địa chỉ.
7. *Thông tin hệ thống* — Tạo bởi, Tạo lúc, Cập nhật lúc, Trạng thái.

**Toggle "Hiển thị trống":** A checkbox at the top (`soDetailShowEmpty` ref) controls whether empty rows are shown. Implemented with custom CSS toggle switch.

**CSS Grid pattern:**
- `.sod-detail-grid` — `display: grid; grid-template-columns: 1fr 1fr`
- `.sod-drow:nth-child(odd)` gets `border-right` to create vertical divider between columns without double borders.
- `.sod-drow--full` — `grid-column: 1 / -1` for full-width rows.
- `.sod-dlabel` — 168px wide, `#f7f8fc` background (MISA-style label column).

**New CSS selectors (all added to `styles.css`):**
`.sod-detail-view`, `.sod-detail-topbar`, `.sod-dtoggle-inp`, `.sod-dtoggle-track`, `.sod-dtoggle-thumb`, `.sod-section`, `.sod-section-title`, `.sod-detail-grid`, `.sod-drow`, `.sod-drow--full`, `.sod-dlabel`, `.sod-dval`, `.sod-dval-empty`, `.sod-dlink`, `.sod-dtag`, `.sod-dbool`, `.sod-info-hint`, `.sod-dstatus--check/--draft/--done/--pending`, `.sod-detail-section-goods`.

**New state ref:** `soDetailShowEmpty = ref(true)` in `orders/composable.js`.

## 7.9 Left Sidebar Scroll Fix  ← NEW (2026-06-16)

**Problem:** When scrolling down in the order detail page, the left summary sidebar scrolled away with the content instead of staying fixed.

**Root cause:** The `height: 100%` chain was broken. `.layout-main-section` used no height, `.dcnet-crm` used `min-height`, and `.dcnet-crm-root` had no height. This caused `height: 100%` on `.sod-page` to resolve to `auto`, making both columns scroll together.

**Fix applied to `styles.css`:**
- `.layout-main-section` → added `height: 100%; overflow: hidden`
- `.dcnet-crm-root` → added `height: 100%; overflow: hidden`
- `.dcnet-crm` → changed `min-height` to `height: 100%; overflow: hidden`
- `.sod-page` → added `min-height: 0; max-height: 100vh`

After this fix, `.sod-left` (sticky sidebar) stays fixed while `.sod-main` (right content) scrolls independently.

## 7.10 Edit Order Flow — MISA-style Full-Page Edit  ← NEW (2026-06-16)

Instead of inline field editing, the "Sửa" button now opens the full `create-sales-order` form page pre-filled with the existing SO's data, matching the MISA AMIS edit pattern.

**DRY pattern:** The existing `create-sales-order` route/form is reused entirely. No new route or HTML was added. A `soEditMode` flag branches the form's title, back button, save button label, and save logic.

**New state refs in `orders/composable.js`:**
- `soEditMode = ref(false)` — whether the create form is in edit mode.
- `soEditTarget = ref("")` — the SO name being edited (e.g. `"SAL-ORD-2026-00001"`).

**New functions:**
- `openEditSO(detail)` — maps all `orderDetail` fields → `createSOForm` and `createSOItems`, sets `soEditMode = true`, sets `soEditTarget = detail.name`, navigates to `create-sales-order` route.
- `cancelEditSO()` — resets `soEditMode`, navigates back to `order-detail` via `openOrderDetail({ name })`.

**Field mapping in `openEditSO`:**
Maps all standard SO fields + custom fields: `custom_contract_duration`, `custom_contract_expiry`, `custom_installation_zone`, `custom_execution_status`, `custom_revenue_recognition_date`, `custom_revenue_status`, `custom_payment_due_date`, `custom_acceptance_date`. Items mapped with `item.net_rate || item.rate` for price, `item.custom_a_end → a_end`, `item.custom_z_end → z_end`.

**Modified `saveCreateSO()` in `composable.js`:**
```js
if (soEditMode.value) {
  await call("update_sales_order", { name: soEditTarget.value, data: { ...createSOForm.value, items: validItems } }, "POST");
  // navigate back to order-detail + loadOrderDetail(name)
} else {
  // original create flow
}
```

**Server method:** Reuses existing `update_sales_order(name, data)` — no backend changes needed.

**Template changes in `orders/template.js`:**
- Create form back button: `soEditMode ? cancelEditSO() : (...)`.
- Create form title: `soEditMode ? 'Sửa đơn hàng' : 'Sinh đơn hàng'`.
- SO name badge shown next to title when editing: `<span class="so-edit-name">{{ soEditTarget }}</span>`.
- Save button label: `soEditMode ? 'Cập nhật' : 'Lưu'`.
- Order detail header "Sửa" button simplified: removed old inline-edit `v-if`/`v-else` blocks; now always calls `openEditSO(orderDetail)`.

**CSS addition:** `.so-edit-name` — teal green badge (`#0d9488` background) showing the SO name next to the form title in edit mode.

## 7.11 Service Accounts — DCNET Service Account  ← NEW (2026-06-16)

A service account represents a unique (customer + item_code + a_end + z_end) combination,
auto-assigned to DVVT (non-Maintenance) SO line items.

### DocType: `DCNET Service Account`

- Location: `dcnet-crm/dcnet_crm/dcnet_crm/doctype/dcnet_service_account/`
- Module: `DCNET CRM`
- autoname: `field:account_code`
- Fields: `account_code` (Data, unique, reqd), `customer` (Link→Customer, reqd),
  `item_code` (Link→Item), `item_name` (Data), `a_end` (Data), `z_end` (Data),
  `uom` (Data), `is_active` (Check, default 1)
- Permissions: System Manager (full CRUD) + Sales User (no delete)
- Class name: `DCNETServiceAccount` (Frappe converts "DCNET Service Account" → folder
  `dcnet_service_account` — NOT `service_account`. Must match exactly.)

### Account code generation

Format: `Acc-0001` … `Acc-9999`, then `Acc-10000` (unbounded).
Function `_generate_next_account_code()` reads the latest `creation` row and increments.
`get_or_create_service_account(customer, item_code, a_end, z_end)` is idempotent:
returns existing if found by exact key match, creates new otherwise.

### Custom Field on SO Item

`Sales Order Item.custom_dcnet_account_id` (Data, `insert_after: custom_z_end`,
`search_index: 1`) — defined in `dcnet_apps/dcnet_apps/fixtures/custom_field.json`.
Run `bench --site flow.local migrate` after pulling to activate.

### API methods added

- `get_or_create_service_account(customer, item_code, a_end, z_end)` — idempotent upsert.
- `get_customer_service_accounts(customer, item_code=None)` — list for datalist suggestions.
- `get_service_accounts_list(search, page, page_length)` — paginated list for mgmt view.
- `get_service_account_detail(account_code)` — doc + linked SOs.

### Frontend: auto-fetch logic (`orders/composable.js`)

- `autoFetchSOItemAccount(item)` — calls `get_or_create_service_account` for an item;
  assigns `item.account_id` if response is returned. Called on:
  1. `item_code` change (via `autoFillSOItemByCode`).
  2. `a_end` / `z_end` `@change` events in form.
  3. Opening edit form (`openEditSO`) for items that have `item_code` but no `account_id`.
- `soAEndOptions`, `soZEndOptions` — ref arrays populated by `_loadSOEndpointSuggestions`
  bound to `<datalist id="so-aend-options">` / `<datalist id="so-zend-options">`.
- `openEditSO` maps `item.custom_dcnet_account_id → item.account_id` when loading items.
- `saveCreateSO` / `update_sales_order` persists `account_id → custom_dcnet_account_id`
  on each SO item row.

### Frontend: Account column visibility

The Account column is only shown for non-Maintenance orders (`order_type !== 'Maintenance'`).
Hidden via `v-if="createSOForm.order_type !== 'Maintenance'"` on `<col>`, `<th>`, and `<td>`.

### Frontend: Account badge CSS

`.item-account-badge` uses hardcoded hex colors — NOT CSS variables:
```css
background: #eff4ff; border: 1px solid #b2ccff; color: #2b4acb;
```
The CRM theme does NOT define `--crm-primary-light`. Using the variable renders the
badge as a solid blue rectangle (text invisible). Always use the hardcoded values.

### Frontend: Account column locations

1. **SO create/edit form** (DVVT items table, `so-items-table`) — after Z-End column.
   colgroup: `<col class="col-account">` (width 100px via `.so-items-table .col-account`).
2. **Order detail "Hàng hóa" tab** (`orderDetailTab === 'items'`, line ~599) — after Mô tả column.
   colgroup: extra `<col style="width:100px">` added; thead: `<th class="gt-center">Account</th>`;
   tbody: badge or `gt-muted` dash; tfoot colspan updated from 5 → 6; empty row 18 → 19.
3. **Order detail "Thông tin chi tiết" tab** (line ~873) — also has Account column in the
   secondary goods table inside that tab.

### "Quản lý accounts" tab

Route: `?view=accounts`. Sidebar entry already wired in `app.js`.
- `frontend/src/features/accounts/composable.js` — `useAccounts(ctx)` composable.
- `frontend/src/features/accounts/template.js` — search toolbar, paginated table, detail modal.
- Detail modal shows account fields + table of all linked SOs (from `get_service_account_detail`).

### CRM "Cập nhật" fix (2026-06-16)

**Root cause:** `update_sales_order` used an ALLOWED whitelist with full DocType field names
(`custom_contract_duration`) but the form sends short keys (`contract_duration`) — zero
matches, so all header fields and items were silently dropped on save.

**Fix:** Rewrote `update_sales_order` with the same explicit short-key → DocType-field mapping
used in `create_sales_order` (e.g. `_set_if(doc, data, "custom_contract_duration", src_key="contract_duration")`).
Items are now processed via the draft path (rewrite `doc.items[]`) or submitted path
(`update_child_qty_rate`).

### Warehouse validation bypass (2026-06-16)

CRM creates/updates SO as draft only; accountants submit later with warehouse selected.
All SO saves in `dcnet_crm/api.py` now set `doc.flags.ignore_validate = True` before
`doc.save()` / `doc.insert()` to bypass ERPNext's "Kho giao hàng là bắt buộc" validation.

## 7.14 SO Stock Balance Lookup — "Tra cứu số lượng tồn"  ← NEW (2026-06-25)

A popup on the Order detail page shows, for each SO line item, the ordered qty,
delivered qty and the real stock balance broken down by warehouse.

- Trigger + state live in `frontend/src/features/orders/composable.js` (~line 282):
  `openStockLookup()` calls `get_so_stock_balance`.
- **Server method:** `get_so_stock_balance(name)` — GET. Reads standard `Bin`
  records (`actual_qty`, `reserved_qty`, `projected_qty`) per warehouse for all
  item codes on the SO, aggregated per item code. Returns
  `{ name, items: [{ item_code, item_name, uom, qty, delivered_qty,
  balance_qty, warehouses: [{ warehouse, actual_qty, reserved_qty,
  projected_qty }] }] }`.
- Read-only; no stock mutation.

## 7.15 SO API Refactor — separate detail/items methods  ← NEW (2026-06-25)

The order detail / edit flow now uses granular server methods instead of one
monolithic call:
- `get_so_detail(name)` — GET. Full SO document for the detail page.
- `get_so_items(name)` — GET. SO line items (detail/edit tables).
- `get_so_form_options(customer=None)` — GET. Dropdowns for the SO create/edit form.
- `update_so_items(name, items)` — POST. Update only the items child table.
- `update_sales_order(name, data)` remains for full header+items update.

## 7.16 Thẻ chăm sóc — CRM Care Card (list + detail/edit/new)  ← NEW (2026-06-25)

MISA-style "Thẻ chăm sóc" feature at `?view=care`. The sidebar entry "Thẻ chăm
sóc" (previously a placeholder pointing at `view=customers`) now routes here.

### DocType: `CRM Care Card`

- Location: `dcnet_crm/dcnet_crm/doctype/crm_care_card/`
- Module: `DCNET CRM`. Class name `CRMCareCard`.
- **autoname:** `CS.#######` (Expression old style) → produces `CS0000001`
  (matches the MISA code format exactly).
- Snapshot fields fetched from the linked Customer via `fetch_from` +
  `fetch_if_empty`: `customer_name`, `tax_id`, `mobile_no`, `email_id`. The
  controller `validate()` also backfills these for programmatic inserts (so
  list/filter queries work even when `fetch_from` did not run).
- Fields by MISA section:
  - *Thông tin chung:* `customer` (Link, reqd), `customer_name`, `tax_id`,
    `mobile_no`, `email_id`, `status` (Select).
  - *Địa chỉ:* `province` (Tỉnh/Thành phố), `district` (Quận/Huyện), `ward`
    (Phường/Xã), `country` (default "Việt Nam"), `address`, `established_date`
    (Ngày thành lập/Ngày sinh).
  - *Hàng hóa / Đơn hàng:* `sales_order` (Link→Sales Order), `item`
    (Link→Item), `item_type` (Data), `order_executor` (Link→User).
  - *Thông tin chăm sóc:* `care_date`, `satisfaction_level` (Select),
    `dissatisfaction_reason` (depends on satisfaction = "Không hài lòng"),
    `description`.
  - *Thông tin hệ thống:* `department` (Đơn vị, Data), `layout` (Bố cục,
    default "Mẫu tiêu chuẩn"), `related_users` (Người liên quan, Small Text).
- **Status options (MISA):** `Chưa chăm sóc` (default) / `Đang chăm sóc` /
  `Đã chăm sóc`.
- Permissions: System Manager + Sales User (full CRUD).

### List view (`careView === 'list'`)

MISA layout = 3 columns: data grid (left) + activity timeline panel (center) +
"Bộ lọc" flyout (right, toggled). All CSS uses the `cc-*` prefix.

- Toolbar: title dropdown "Tất cả thẻ chăm sóc", "Nhập từ Excel" (placeholder),
  "+ Thêm".
- Grid columns: Mã thẻ chăm sóc (name), Khách hàng, Mã số thuế, Điện thoại,
  Email, Địa chỉ, Bố cục. Footer = total + page-size + pager.
- Clicking the **code** or **customer name** opens the detail page
  (`openCareDetail`). Clicking elsewhere on the row only selects it (loads the
  right activity panel preview).
- Activity panel: icon bar + 3 tabs **Hoạt động / Mua hàng / Chăm sóc**
  (`careTab`). "Chăm sóc" tab has a compose box → `add_care_note` (Comment).
  - *Hoạt động* = customer's `Communication` + `ToDo` records.
  - *Mua hàng* = customer's `Sales Order` + `Sales Invoice`.
  - *Chăm sóc* = `Comment` records on the care card + its own care_date/desc.
- "Bộ lọc" flyout: TIÊU CHÍ LỌC = checkbox field list (`CARE_FILTER_DEFS`);
  enabled fields render a value input; Áp dụng / Xóa lọc.

### Detail / edit / new (`careView === 'detail'`)

Header (← back, customer name title, "Thêm thẻ", and right-side Sửa / Sinh đơn
hàng / ⋯ in view mode; Hủy / Lưu in edit/new mode) + summary row + 7 tabs
(Thông tin chi tiết, Ghi chú, Tài liệu đính kèm, Công việc đang/đã hoàn thành,
Nội dung trao đổi, Thẻ tư vấn). Only "Thông tin chi tiết" is implemented; the
rest are empty states.

- "Thông tin chi tiết" has a field-search box + "Hiển thị dữ liệu trống" toggle
  (`careFieldSearch`, `careShowEmpty`, helper `showCareField(label, value)`) and
  3 sections (Thông tin chung / Thông tin chăm sóc / Thông tin hệ thống), each
  rendered view-mode (read-only spans) or edit-mode (inputs) by `careFormMode`.
- **+ Thêm:** `createCareCard()` opens `frappe.prompt` (Customer Link with
  server search), prefills snapshot from the chosen Customer, then opens the
  full form in `careFormMode = 'new'`.
- **Sửa:** `startCareEdit()` copies `careDetail.card` into `careForm`.
- **Lưu:** `saveCareForm()` → `save_care_card`.
- ⚠️ The three Link fields (`sales_order`, `item`, `order_executor`) are edited
  as **plain text inputs** — typing a value with no matching record raises a
  `LinkValidationError` shown via `frappe.msgprint`. Add autocomplete when
  requested (same MVP caveat as the SO form).

### Source files

- `frontend/src/features/care-cards/composable.js` — `useCareCards(ctx)`:
  list/detail/edit/new state, `CARE_FILTER_DEFS`, filters, `careTimeline`.
- `frontend/src/features/care-cards/template.js` — list view + detail/edit/new
  form (`cc-*` markup).
- `dcnet_crm/dcnet_crm/doctype/crm_care_card/` — DocType json + `.py`.
- `dcnet_crm/api.py` — `get_care_card_detail`, `add_care_note`,
  `save_care_card`, `RESOURCE_CONFIG["care_cards"]`.
- `dcnet_crm/install.py` — sidebar "Thẻ chăm sóc" → `{"view": "care"}`.
- `frontend/src/app.js` — imports + `useCareCards`, route `care` in the allowed
  list, loader in both watchers, `...careState` spread, `+ careCardsTemplate`.
- `frontend/src/styles.css` — `cc-*` list + `cc-det-*` / `cc-fld-*` form styles.

## 12. Recommended Next Work

**Immediate:**
1. ✅ DONE — Custom Fields for confirmed SO fields added to
   `dcnet_apps/dcnet_apps/fixtures/custom_field.json` and wired into the inline
   SO form + `create_sales_order` / `update_sales_order` API.
2. Remaining: implement auto-fill compute logic for `contract_expiry`
   (from `contract_duration`) and `acceptance_date` (from delivery milestone) so
   those two inputs no longer need to be `disabled`.

**Service Accounts — remaining:**
4. Old orders with no `custom_dcnet_account_id` show `—` in Account column. To assign accounts,
   user must open "Sửa" → "Cập nhật". Consider adding a backend migration or batch-assign button.
5. Account column in create/edit form only shows for non-Maintenance orders. Confirm
   this rule is correct with customer.
6. `get_or_create_service_account` auto-creates a DB record. If `a_end`/`z_end` are
   blank (e.g. retail items), it creates an account with empty endpoint fields. Confirm
   desired behavior — may want to skip account creation for blank endpoints.

**SO form variant — trimmed columns (in discussion):**
- Reuse the existing `create-sales-order` CRM form (do NOT fork a new route/form).
- Goal: hide a subset of fields/columns so the form fits a specific job/workflow.
- Approach: drive visibility from a flag/config rather than deleting fields, so the
  full form and the trimmed form share one template (same DRY pattern as `soEditMode`).
- Open question: which exact fields/columns to hide — pending customer confirmation.

**Thẻ chăm sóc (CRM Care Card) — remaining:**
- Autocomplete for `item` / `sales_order` / `order_executor` edit fields
  (currently plain text → LinkValidationError on bad input).
- Implement the non-"Thông tin chi tiết" detail tabs (Ghi chú, Tài liệu đính
  kèm, Công việc đang/đã hoàn thành, Nội dung trao đổi, Thẻ tư vấn).
- Wire "Nhập từ Excel" to a standard `CRM Care Card` Data Import.
- "Sinh đơn hàng" button on the detail header is a placeholder — wire to
  `openCreateSO(customer)` if desired.
- Confirm with customer the exact filter-criteria list + grid columns vs MISA.

**Opportunity detail — complete remaining tabs:**
4. Tab 3 (Hàng hóa) — display Opportunity Items with quantity/price.
5. Tab 4 (Ghi chú & đính kèm) — file upload + note create.
6. Tab 7 (Hoạt động) — reuse Customer Activity tab pattern (ToDo/Event).
7. Tab 8 (Trao đổi) — Comments/Communication list + add comment.

**Customer profile — finish remaining areas:**
8. Notes/attachments full upload flow.
9. `Trao doi` tab.
10. Ho tro, Marketing (empty states are acceptable until specs confirmed).

**Order detail improvements:**
11. Item Code autocomplete in SO create/edit form via `frappe.call("frappe.client.get_list", "Item")`.
12. Show link to created/updated SO after save ("Mở đơn hàng {name}").
13. Opportunity detail → Bán hàng tab should list SOs created from this opportunity.
14. `soDetailShowEmpty = false` default — consider persisting toggle state in `localStorage`.

**Address / MST — remaining:**
1. Shipping address cascade dropdowns in create form are wired but not yet wired in the
   detail edit form (only billing is done there). Add `editShippingProvinceCode` + watcher
   in `composable.js` when needed.
2. MST lookup fills billing + shipping address identically. If they should diverge, add
   separate pending-ward refs for each (already done for create form via `_pendingShippingWard`).
3. "Thông tin giao hàng" section in customer detail edit form — verify address fields are
   wired to `customerForm.shipping_address` (currently only billing address is cascade).

**Phân công khách hàng (Customer Assignment) — design note (2026-06-20):**

Context: Manager wants to assign/reassign customers to specific sales users without IT involvement.
Currently only System Manager / IT can configure Frappe User Permissions via Setup → User Permissions.

**Option 1 (quick, no code): ERPNext Sales Person**
- Selling → Setup → Sales Person → create salesperson hierarchy.
- Each Customer → "Sales Team" tab → add salesperson + commission %.
- Manager can edit this tab directly (no technical knowledge needed).
- Limitation: no row-level data restriction — sales user still sees all customers in lists.

**Option 2 (recommended): Build "Phân công khách hàng" UI in CRM (~2-3 hours)**
- Manager selects a sales user from dropdown.
- All customers shown as a checklist; currently assigned customers have checkmarks.
- Manager toggles assignments → click Save.
- Backend API reads/writes `User Permission` DocType (DocType = Customer, user = selected user).
- Internally uses `frappe.client.insert` / `frappe.client.delete` on User Permission — manager never sees this.
- Result: sales user's Customer list is row-restricted to their assigned customers.
- Integration: can live in `dcnet-permission` app (next to the existing Role & Permission UI)
  or as a new CRM view `?view=customer-assignment`.
- Backend scope: `get_user_customer_assignments(user)` → list of assigned Customer names;
  `set_user_customer_assignments(user, customers[])` → diff old/new, delete removed, insert added.
- Permissions: only Sales Manager / System Manager can access this page.

**General:**
Before implementing each area:
1. Check `docs/SPEC-CRM-tinh-nang.md` for business rules.
2. Map to an existing DocType first; only custom if nothing fits.
3. Record unclear requirements in `docs/plans/`.
4. Implement inside `dcnet-crm` only — never touch `dcnet_apps` or ERPNext core.
5. Build in the container + clear cache.
6. Update this file.
