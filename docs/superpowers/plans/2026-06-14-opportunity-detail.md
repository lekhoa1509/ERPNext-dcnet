# Opportunity Detail View Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an internal opportunity detail page inside `/desk/dcnet-crm?view=opportunity-detail&opportunity={name}` that mirrors the MISA CRM detail UI — left sidebar, 9 tabs, stage progress bar.

**Architecture:** Follows the identical pattern as `customer-detail` already in the codebase. Add `opportunityDetailName` ref + `loadOpportunityDetail` + `openOpportunityDetail` to the Vue app; add `get_opportunity_detail` API; add the `opportunity-detail` template block. Single-click on the opportunity title/code in the list navigates to detail. No new files needed — all changes go into the 3 existing files.

**Tech Stack:** Vue 3 Options API (inline template, runtime compiler), Frappe v16 Python API, esbuild bundle.

**No unit tests** — site has `allow_tests = false`. Verification is manual via `bench build` + browser.

---

## File Map

| File | Changes |
|------|---------|
| `dcnet-crm/dcnet_crm/api.py` | Add `get_opportunity_detail(name)` and `update_opportunity(name, data)` |
| `dcnet-crm/frontend/src/main.js` | Add refs, functions, route handling, full template block |
| `dcnet-crm/frontend/src/styles.css` | Add `.opp-detail-*` CSS classes |

---

## Task 1 — Backend: `get_opportunity_detail`

**File:** `dcnet-crm/dcnet_crm/api.py` — append after `get_opportunity_form_options`

- [ ] **1.1 Add `get_opportunity_detail` whitelist method**

Append to `api.py`:

```python
@frappe.whitelist(methods=["GET"])
def get_opportunity_detail(name):
    """Return all data needed to render the internal Opportunity detail page."""
    _check_permission("Opportunity", name=name)
    doc = frappe.get_doc("Opportunity", name)

    # ── Items ────────────────────────────────────────────────
    items = [
        {
            "idx": item.idx,
            "item_code": item.item_code or "",
            "item_name": item.item_name or "",
            "description": item.description or "",
            "qty": item.qty,
            "uom": item.uom or "",
            "rate": item.rate,
            "amount": item.amount,
            "custom_discount_percentage": flt(item.get("custom_discount_percentage")),
            "custom_discount_amount": flt(item.get("custom_discount_amount")),
            "custom_net_rate": flt(item.get("custom_net_rate")),
            "custom_net_amount": flt(item.get("custom_net_amount")),
            "custom_installation_point_a_end": item.get("custom_installation_point_a_end") or "",
            "custom_installation_point_z_end": item.get("custom_installation_point_z_end") or "",
        }
        for item in doc.get("items", [])
    ]

    # ── Timeline (Communications + Comments for Activity tab) ─
    timeline = _get_timeline("Opportunity", name)

    # ── Comments for Trao đổi tab ─────────────────────────────
    comments = []
    if frappe.has_permission("Comment", "read"):
        comments = frappe.get_all(
            "Comment",
            filters={
                "reference_doctype": "Opportunity",
                "reference_name": name,
                "comment_type": "Comment",
            },
            fields=["name", "comment_by", "comment_by_fullname", "content", "creation"],
            order_by="creation asc",
        )

    # ── Activities (ToDo + Events) ────────────────────────────
    activities = []
    if frappe.has_permission("ToDo", "read"):
        todos = frappe.get_list(
            "ToDo",
            filters={"reference_type": "Opportunity", "reference_name": name},
            fields=["name", "description", "date", "status", "priority", "assigned_by_full_name", "owner"],
            order_by="date asc",
        )
        for t in todos:
            t["activity_doctype"] = "ToDo"
        activities.extend(todos)

    if frappe.has_permission("Event", "read"):
        event_names = frappe.get_all(
            "Event Participants",
            filters={"reference_doctype": "Opportunity", "reference_docname": name},
            pluck="parent",
        )
        if event_names:
            events = frappe.get_list(
                "Event",
                filters={"name": ["in", list(set(event_names))]},
                fields=["name", "subject", "event_category", "starts_on", "ends_on", "status", "owner"],
                order_by="starts_on asc",
            )
            for e in events:
                e["activity_doctype"] = "Event"
            activities.extend(events)

    activities.sort(key=lambda x: str(x.get("date") or x.get("starts_on") or ""))

    # ── Contacts ──────────────────────────────────────────────
    contacts = []
    if doc.contact_person and frappe.has_permission("Contact", "read"):
        contact_names = [doc.contact_person]
        if doc.party_name and doc.opportunity_from == "Customer":
            linked = frappe.get_all(
                "Dynamic Link",
                filters={"parenttype": "Contact", "link_doctype": "Customer", "link_name": doc.party_name},
                pluck="parent",
            )
            contact_names = list(set(contact_names + linked))
        if contact_names:
            contacts = frappe.get_list(
                "Contact",
                filters={"name": ["in", contact_names]},
                fields=["name", "full_name", "email_id", "mobile_no", "designation", "company_name"],
            )

    # ── Related sales docs ────────────────────────────────────
    quotations, orders, invoices = [], [], []
    customer = doc.party_name if doc.opportunity_from == "Customer" else None

    if customer and frappe.has_permission("Quotation", "read"):
        quotations = frappe.get_list(
            "Quotation",
            filters={"party_name": customer, "opportunity": name, "docstatus": ["<", 2]},
            fields=["name", "transaction_date", "status", "grand_total", "currency"],
            order_by="transaction_date desc",
            page_length=20,
        )
    if customer and frappe.has_permission("Sales Order", "read"):
        orders = frappe.get_list(
            "Sales Order",
            filters={"customer": customer, "docstatus": ["<", 2]},
            fields=["name", "transaction_date", "status", "grand_total", "currency"],
            order_by="transaction_date desc",
            page_length=20,
        )
    if customer and frappe.has_permission("Sales Invoice", "read"):
        invoices = frappe.get_list(
            "Sales Invoice",
            filters={"customer": customer, "is_return": 0, "docstatus": ["<", 2]},
            fields=["name", "posting_date", "status", "grand_total", "outstanding_amount"],
            order_by="posting_date desc",
            page_length=20,
        )

    # ── Attachments ───────────────────────────────────────────
    attachments = []
    if frappe.has_permission("File", "read"):
        attachments = frappe.get_all(
            "File",
            filters={"attached_to_doctype": "Opportunity", "attached_to_name": name},
            fields=["name", "file_name", "file_url", "file_size", "is_private", "creation", "owner"],
            order_by="creation desc",
        )

    return {
        "document": {
            f: doc.get(f)
            for f in [
                "name", "title", "opportunity_from", "party_name", "customer_name",
                "contact_person", "contact_display", "contact_mobile", "contact_email",
                "status", "sales_stage", "probability", "opportunity_amount", "currency",
                "expected_closing", "opportunity_type", "source", "campaign_name",
                "territory", "company", "opportunity_owner", "notes",
                "custom_opportunity_code", "custom_shipping_address",
                "custom_shipping_country", "custom_shipping_state",
                "custom_shipping_county", "custom_shipping_ward",
                "custom_shipping_address_line1", "custom_shipping_pincode",
                "custom_is_shared", "custom_referral_partner",
                "creation", "modified", "owner",
            ]
        },
        "items": items,
        "timeline": timeline,
        "comments": comments,
        "activities": activities,
        "contacts": contacts,
        "quotations": quotations,
        "orders": orders,
        "invoices": invoices,
        "attachments": attachments,
    }
```

- [ ] **1.2 Add `update_opportunity` for Thông tin chi tiết edit**

Append to `api.py`:

```python
@frappe.whitelist(methods=["POST"])
def update_opportunity(name, data):
    """Update editable fields on an Opportunity (called from detail page Sửa mode)."""
    _check_permission("Opportunity", "write", name=name)
    if isinstance(data, str):
        data = json.loads(data)

    ALLOWED = {
        "title", "party_name", "contact_person", "sales_stage", "probability",
        "expected_closing", "opportunity_type", "source", "territory", "company",
        "opportunity_owner", "notes",
        "custom_shipping_country", "custom_shipping_state", "custom_shipping_county",
        "custom_shipping_ward", "custom_shipping_address_line1", "custom_shipping_pincode",
        "custom_shipping_address", "custom_is_shared", "custom_referral_partner",
    }
    doc = frappe.get_doc("Opportunity", name)
    for k, v in data.items():
        if k in ALLOWED:
            doc.set(k, v)
    doc.save(ignore_permissions=False)
    frappe.db.commit()
    return {"name": doc.name, "modified": str(doc.modified)}
```

- [ ] **1.3 Verify Python syntax**

```bash
docker exec devcontainer-frappe-1 bash -lc \
  'cd /workspace/development/frappe-bench && python -m py_compile apps/dcnet-crm/dcnet_crm/api.py && echo OK'
```
Expected: `OK`

- [ ] **1.4 Commit**

```bash
git add dcnet-crm/dcnet_crm/api.py
git commit -m "feat(dcnet-crm): add get_opportunity_detail and update_opportunity APIs"
```

---

## Task 2 — Vue: refs, state, routing

**File:** `dcnet-crm/frontend/src/main.js`

- [ ] **2.1 Add `opportunity-detail` to `syncNativeSidebarActive` labels map**

In `syncNativeSidebarActive` (around line 352), add to the `labels` object:
```javascript
"opportunity-detail": "Cơ hội",
```

- [ ] **2.2 Add `opportunity-detail` to `readRoute` known views**

In `readRoute` (around line 389), change the route assignment so `opportunity-detail` is recognised:
```javascript
route.value = RESOURCES[key] || ["dashboard", "customer-detail", "opportunity-detail"].includes(key)
  ? key
  : "dashboard";
// Add: clear back to opportunities if no name given
if (route.value === "opportunity-detail" && !opportunityDetailName.value) route.value = "opportunities";
```

Also update `syncRouteUrl` to pass `opportunity` param for the detail route. In `syncRouteUrl` (around line 340), after the `customer` param handling add:
```javascript
// After the existing customer param lines:
if (name && view === "opportunity-detail") url.searchParams.set("opportunity", name);
else if (view !== "opportunity-detail") url.searchParams.delete("opportunity");
```

And in `readRoute` read the opportunity param:
```javascript
opportunityDetailName.value = params.get("opportunity") || frappe.route_options?.opportunity || "";
```

- [ ] **2.3 Add refs for opportunity detail**

After the `opportunityFormOptions` ref block (around line 192), add:

```javascript
const opportunityDetailName = ref("");
const opportunityDetail = ref(null);
const opportunityDetailTab = ref("overview");
const opportunityDetailEditing = ref(false);
const opportunityDetailSaving = ref(false);
const opportunityDetailForm = ref({});
const opportunityDetailComment = ref("");
```

- [ ] **2.4 Add `loadOpportunityDetail` function**

After `backToCustomers` function (around line 520):

```javascript
async function loadOpportunityDetail(name = opportunityDetailName.value) {
  if (!name) return navigate("opportunities");
  loading.value = true;
  opportunityDetail.value = null;
  try {
    opportunityDetail.value = await call("get_opportunity_detail", { name });
    opportunityDetailName.value = name;
  } catch (error) {
    frappe.msgprint(error.message || __("Không thể tải chi tiết cơ hội."));
  } finally {
    loading.value = false;
  }
}

function openOpportunityDetail(row) {
  if (!row?.name) return;
  opportunityDetailName.value = row.name;
  opportunityDetailTab.value = "overview";
  opportunityDetailEditing.value = false;
  route.value = "opportunity-detail";
  frappe.route_options = { view: "opportunity-detail", opportunity: row.name };
  frappe.set_route("dcnet-crm").then(() => syncRouteUrl("opportunity-detail", row.name));
}

function backToOpportunities() {
  navigate("opportunities");
}

async function saveOpportunityDetailComment() {
  const content = opportunityDetailComment.value.trim();
  if (!content || !opportunityDetailName.value) return;
  await call("add_note", {
    resource: "opportunities",
    name: opportunityDetailName.value,
    content,
  }, "POST");
  opportunityDetailComment.value = "";
  await loadOpportunityDetail();
}

async function saveOpportunityDetailEdit() {
  if (opportunityDetailSaving.value) return;
  opportunityDetailSaving.value = true;
  try {
    await call("update_opportunity", {
      name: opportunityDetailName.value,
      data: opportunityDetailForm.value,
    }, "POST");
    opportunityDetailEditing.value = false;
    await loadOpportunityDetail();
  } catch (error) {
    frappe.msgprint(error.message || __("Không thể lưu cơ hội."));
  } finally {
    opportunityDetailSaving.value = false;
  }
}
```

- [ ] **2.5 Wire `openOpportunityDetail` to the opportunity table row**

In the opportunity table template (around line 1942–1945), change the title/contact link cell to call `openOpportunityDetail`:

```html
<a v-if="column.field === 'title' || column.field === 'name'"
   href="#" class="opp-link"
   @click.prevent.stop="openOpportunityDetail(row)">
  {{ formatValue(row[column.field], column.field) }}
</a>
```

- [ ] **2.6 Update `watch(route)` block to load opportunity detail**

In the `watch(route, ...)` callback (around line 1140), add a branch:
```javascript
else if (value === "opportunity-detail") await loadOpportunityDetail();
```

- [ ] **2.7 Expose new functions in template return**

Add to the `return { ... }` object at the bottom of `setup()`:
```javascript
backToOpportunities, loadOpportunityDetail, openOpportunityDetail,
opportunityDetail, opportunityDetailComment, opportunityDetailEditing,
opportunityDetailForm, opportunityDetailName, opportunityDetailSaving,
opportunityDetailTab, saveOpportunityDetailComment, saveOpportunityDetailEdit,
```

---

## Task 3 — Vue Template: opportunity-detail shell + left sidebar + tabs

**File:** `dcnet-crm/frontend/src/main.js` — add inside the root `<template>` after the `opportunities` workspace block (around line 2014)

- [ ] **3.1 Add the opportunity-detail template block**

After the closing `</main>` of `route === 'opportunities'` (around line 2034), add:

```html
<main v-else-if="route === 'opportunity-detail'" class="opp-detail-page">
  <!-- HEADER -->
  <header class="opp-detail-header">
    <button class="opp-back-btn" @click="backToOpportunities">←</button>
    <span class="opp-detail-code">{{ opportunityDetail?.document?.custom_opportunity_code || opportunityDetail?.document?.name || opportunityDetailName }}</span>
    <div class="opp-detail-stage-badge" v-if="opportunityDetail?.document?.sales_stage">
      <span class="opp-stage-dot">●</span>
      {{ opportunityDetail.document.sales_stage }}
    </div>
    <button class="icon-button opp-refresh-btn" @click="loadOpportunityDetail()"><CRMIcon name="refresh" /></button>
    <div class="opp-detail-header-spacer"></div>
    <template v-if="!opportunityDetailEditing">
      <button class="crm-button" @click="opportunityDetailEditing = true; opportunityDetailForm = { ...opportunityDetail.document }">✏ Sửa</button>
    </template>
    <template v-else>
      <button class="crm-button" :disabled="opportunityDetailSaving" @click="opportunityDetailEditing = false">Hủy</button>
      <button class="crm-button primary" :disabled="opportunityDetailSaving" @click="saveOpportunityDetailEdit">{{ opportunityDetailSaving ? 'Đang lưu...' : 'Lưu' }}</button>
    </template>
    <button class="crm-button primary" @click="openRelated('Sales Order', { name: null })">📄 Sinh đơn hàng</button>
  </header>

  <div v-if="loading" class="crm-empty" style="margin-top:40px">Đang tải...</div>
  <div v-else-if="!opportunityDetail" class="crm-empty" style="margin-top:40px">Không tìm thấy cơ hội.</div>
  <div v-else class="opp-detail-body">

    <!-- LEFT SIDEBAR -->
    <aside class="opp-detail-sidebar">
      <div class="opp-detail-sidebar-customer">
        <h3>{{ opportunityDetail.document.customer_name || opportunityDetail.document.party_name || '—' }}</h3>
        <small>{{ opportunityDetail.document.party_name }}</small>
        <div class="opp-sidebar-tag">+ Thêm thẻ</div>
      </div>
      <div class="opp-detail-sidebar-actions">
        <button class="act-btn" title="Gọi điện"><CRMIcon name="phone" /></button>
        <button class="act-btn" title="Tạo công việc" @click="opportunityDetailTab = 'activities'"><CRMIcon name="task" /></button>
        <button class="act-btn" title="Tạo lịch"><CRMIcon name="calendar" /></button>
        <button class="act-btn" title="Gửi email"><CRMIcon name="email" /></button>
      </div>
      <div class="opp-detail-sidebar-stats">
        <div class="opp-stat-row">
          <span class="opp-stat-label">Liên hệ</span>
          <span class="opp-stat-value">{{ opportunityDetail.document.contact_display || '— Không chọn —' }}</span>
        </div>
        <div class="opp-stat-row">
          <span class="opp-stat-label">Số tiền</span>
          <span class="opp-stat-value blue">{{ formatValue(opportunityDetail.document.opportunity_amount, 'opportunity_amount') }}</span>
        </div>
        <div class="opp-stat-row">
          <span class="opp-stat-label">Giai đoạn</span>
          <span class="opp-stat-value">{{ opportunityDetail.document.sales_stage || '—' }}</span>
        </div>
        <div class="opp-stat-row">
          <span class="opp-stat-label">Tỷ lệ thành công</span>
          <span class="opp-stat-value">{{ opportunityDetail.document.probability || 0 }}%</span>
        </div>
        <div class="opp-stat-row">
          <span class="opp-stat-label">Doanh số kỳ vọng</span>
          <span class="opp-stat-value blue">{{ formatValue((opportunityDetail.document.opportunity_amount || 0) * (opportunityDetail.document.probability || 0) / 100, 'opportunity_amount') }}</span>
        </div>
        <div class="opp-stat-row">
          <span class="opp-stat-label">Ngày kỳ vọng</span>
          <span class="opp-stat-value">{{ formatValue(opportunityDetail.document.expected_closing, 'expected_closing') }}</span>
        </div>
        <div class="opp-stat-row">
          <span class="opp-stat-label">Người thực hiện</span>
          <span class="opp-stat-value">{{ opportunityDetail.document.opportunity_owner || '—' }}</span>
        </div>
        <div class="opp-stat-row">
          <span class="opp-stat-label">Loại</span>
          <span class="opp-stat-value">{{ opportunityDetail.document.opportunity_type || '—' }}</span>
        </div>
        <div class="opp-stat-row">
          <span class="opp-stat-label">Nguồn</span>
          <span class="opp-stat-value">{{ opportunityDetail.document.source || '—' }}</span>
        </div>
      </div>
    </aside>

    <!-- MAIN: TABS + CONTENT -->
    <div class="opp-detail-main">
      <nav class="opp-detail-tabs">
        <button :class="{ active: opportunityDetailTab === 'overview' }" @click="opportunityDetailTab = 'overview'">Tổng quan</button>
        <button :class="{ active: opportunityDetailTab === 'info' }" @click="opportunityDetailTab = 'info'">Thông tin chi tiết</button>
        <button :class="{ active: opportunityDetailTab === 'items' }" @click="opportunityDetailTab = 'items'">Hàng hóa</button>
        <button :class="{ active: opportunityDetailTab === 'notes' }" @click="opportunityDetailTab = 'notes'">Ghi chú & đính kèm</button>
        <button :class="{ active: opportunityDetailTab === 'contacts' }" @click="opportunityDetailTab = 'contacts'">Liên hệ</button>
        <button :class="{ active: opportunityDetailTab === 'sales' }" @click="opportunityDetailTab = 'sales'">Bán hàng</button>
        <button :class="{ active: opportunityDetailTab === 'activities' }" @click="opportunityDetailTab = 'activities'">
          Hoạt động <span v-if="opportunityDetail.activities.length" class="opp-tab-badge">{{ opportunityDetail.activities.length }}</span>
        </button>
        <button :class="{ active: opportunityDetailTab === 'chat' }" @click="opportunityDetailTab = 'chat'">
          Trao đổi <span v-if="opportunityDetail.comments.length" class="opp-tab-badge">{{ opportunityDetail.comments.length }}</span>
        </button>
        <button :class="{ active: opportunityDetailTab === 'support' }" @click="opportunityDetailTab = 'support'">Hỗ trợ</button>
      </nav>

      <div class="opp-detail-tab-content">
        <!-- TAB: TỔNG QUAN -->
        <template v-if="opportunityDetailTab === 'overview'">
          <div class="opp-overview-main">
            <!-- Stage progress -->
            <div class="opp-stage-progress">
              <div class="opp-stage-track">
                <div v-for="(stage, idx) in (opportunityDetail.stageOptions || ['Kinh doanh lập yêu cầu','P.TH check thông tin','Thực hiện khảo sát','Kinh doanh báo giá cho KH'])"
                     :key="stage"
                     :class="['opp-stage-step', getStageClass(stage, opportunityDetail.document.sales_stage, idx)]">
                  {{ stage }}
                </div>
                <div :class="['opp-stage-step', 'win', opportunityDetail.document.sales_stage === 'Kết thúc thắng' ? 'active-win' : '']">✓ Hoàn thành</div>
                <div :class="['opp-stage-step', 'lose', opportunityDetail.document.sales_stage === 'Kết thúc thất bại' ? 'active-lose' : '']">✗ Thất bại</div>
              </div>
            </div>

            <!-- Stat cards -->
            <div class="opp-stat-cards">
              <div class="opp-stat-card">
                <div class="opp-sc-label">💰 SỐ TIỀN</div>
                <div class="opp-sc-value">{{ formatValue(opportunityDetail.document.opportunity_amount, 'opportunity_amount') }}</div>
              </div>
              <div class="opp-stat-card">
                <div class="opp-sc-label">✓ TỶ LỆ THÀNH CÔNG</div>
                <div class="opp-sc-value">{{ opportunityDetail.document.probability || 0 }}%</div>
              </div>
              <div class="opp-stat-card">
                <div class="opp-sc-label">📈 DOANH SỐ KỲ VỌNG</div>
                <div class="opp-sc-value">{{ formatValue((opportunityDetail.document.opportunity_amount || 0) * (opportunityDetail.document.probability || 0) / 100, 'opportunity_amount') }}</div>
              </div>
              <div class="opp-stat-card">
                <div class="opp-sc-label">📅 NGÀY KỲ VỌNG / KẾT THÚC</div>
                <div class="opp-sc-value">{{ formatValue(opportunityDetail.document.expected_closing, 'expected_closing') }}</div>
              </div>
            </div>

            <!-- Hàng hóa section -->
            <div class="opp-section-card">
              <div class="opp-section-header">
                <h4>Hàng hóa</h4>
                <button class="crm-button" @click="opportunityDetailTab = 'items'">→</button>
              </div>
              <div v-if="!opportunityDetail.items.length" class="opp-section-empty">📦 Không có dữ liệu</div>
              <table v-else class="opp-mini-table">
                <thead><tr><th>Tên hàng hóa</th><th>SL</th><th>Thành tiền</th></tr></thead>
                <tbody>
                  <tr v-for="item in opportunityDetail.items.slice(0, 5)" :key="item.idx">
                    <td>{{ item.item_name || item.item_code }}</td>
                    <td>{{ item.qty }}</td>
                    <td>{{ formatValue(item.custom_net_amount || item.amount, 'opportunity_amount') }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Nội dung trao đổi section -->
            <div class="opp-section-card">
              <div class="opp-section-header">
                <h4>Nội dung trao đổi</h4>
                <button class="crm-button" @click="opportunityDetailTab = 'chat'">→</button>
              </div>
              <div v-if="!opportunityDetail.comments.length" class="opp-section-empty">💬 Chưa có trao đổi nào</div>
              <div v-else class="opp-comment-list">
                <div v-for="c in opportunityDetail.comments.slice(-3)" :key="c.name" class="opp-comment-item">
                  <div class="opp-comment-avatar">{{ (c.comment_by_fullname || c.comment_by || '?')[0].toUpperCase() }}</div>
                  <div class="opp-comment-body">
                    <strong>{{ c.comment_by_fullname || c.comment_by }}</strong>
                    <p v-html="c.content"></p>
                    <small>{{ formatValue(c.creation, 'creation') }}</small>
                  </div>
                </div>
              </div>
              <div class="opp-comment-input">
                <input v-model="opportunityDetailComment" placeholder="Nhập nội dung..." @keyup.enter="saveOpportunityDetailComment">
                <button class="crm-button primary" :disabled="!opportunityDetailComment.trim()" @click="saveOpportunityDetailComment">➤</button>
              </div>
            </div>
          </div>

          <!-- Right activity panel -->
          <div class="opp-overview-right">
            <div class="opp-activity-panel">
              <div class="opp-activity-tabs">
                <button class="atab active">Hoạt động</button>
              </div>
              <div class="opp-activity-list">
                <div v-for="item in opportunityDetail.timeline.slice(0, 10)" :key="item.name" class="opp-timeline-item">
                  <div class="opp-tl-avatar">{{ (item.owner || 'A')[0].toUpperCase() }}</div>
                  <div class="opp-tl-body">
                    <strong>{{ item.subject || item.description || 'Hoạt động' }}</strong>
                    <p>{{ stripHtml(item.content || item.description || '') }}</p>
                    <small>{{ formatValue(item.creation, 'creation') }}</small>
                  </div>
                </div>
                <p v-if="!opportunityDetail.timeline.length" class="crm-empty">Chưa có hoạt động.</p>
              </div>
            </div>
          </div>
        </template>

        <!-- TAB: THÔNG TIN CHI TIẾT -->
        <template v-else-if="opportunityDetailTab === 'info'">
          <div class="opp-info-grid">
            <div class="opp-info-section">
              <h4>Thông tin cơ bản</h4>
              <div class="opp-field-row">
                <label>Tiêu đề</label>
                <span v-if="!opportunityDetailEditing">{{ opportunityDetail.document.title || '—' }}</span>
                <input v-else v-model="opportunityDetailForm.title">
              </div>
              <div class="opp-field-row">
                <label>Khách hàng</label>
                <span>{{ opportunityDetail.document.customer_name || opportunityDetail.document.party_name || '—' }}</span>
              </div>
              <div class="opp-field-row">
                <label>Liên hệ</label>
                <span v-if="!opportunityDetailEditing">{{ opportunityDetail.document.contact_display || '—' }}</span>
                <input v-else v-model="opportunityDetailForm.contact_person">
              </div>
              <div class="opp-field-row">
                <label>Email liên hệ</label>
                <span>{{ opportunityDetail.document.contact_email || '—' }}</span>
              </div>
              <div class="opp-field-row">
                <label>SĐT liên hệ</label>
                <span>{{ opportunityDetail.document.contact_mobile || '—' }}</span>
              </div>
            </div>
            <div class="opp-info-section">
              <h4>Thông tin kinh doanh</h4>
              <div class="opp-field-row">
                <label>Giai đoạn</label>
                <span v-if="!opportunityDetailEditing">{{ opportunityDetail.document.sales_stage || '—' }}</span>
                <select v-else v-model="opportunityDetailForm.sales_stage">
                  <option v-for="s in (opportunityFormOptions.sales_stages || [])" :key="s.name" :value="s.name">{{ s.name }}</option>
                </select>
              </div>
              <div class="opp-field-row">
                <label>Xác suất (%)</label>
                <span v-if="!opportunityDetailEditing">{{ opportunityDetail.document.probability || 0 }}%</span>
                <input v-else type="number" min="0" max="100" v-model.number="opportunityDetailForm.probability">
              </div>
              <div class="opp-field-row">
                <label>Ngày kỳ vọng</label>
                <span v-if="!opportunityDetailEditing">{{ formatValue(opportunityDetail.document.expected_closing, 'expected_closing') }}</span>
                <input v-else type="date" v-model="opportunityDetailForm.expected_closing">
              </div>
              <div class="opp-field-row">
                <label>Loại cơ hội</label>
                <span v-if="!opportunityDetailEditing">{{ opportunityDetail.document.opportunity_type || '—' }}</span>
                <select v-else v-model="opportunityDetailForm.opportunity_type">
                  <option v-for="t in (opportunityFormOptions.opportunity_types || [])" :key="t.name" :value="t.name">{{ t.name }}</option>
                </select>
              </div>
              <div class="opp-field-row">
                <label>Nguồn gốc</label>
                <span v-if="!opportunityDetailEditing">{{ opportunityDetail.document.source || '—' }}</span>
                <select v-else v-model="opportunityDetailForm.source">
                  <option v-for="s in (opportunityFormOptions.sources || [])" :key="s.name" :value="s.name">{{ s.name }}</option>
                </select>
              </div>
              <div class="opp-field-row">
                <label>Khu vực</label>
                <span v-if="!opportunityDetailEditing">{{ opportunityDetail.document.territory || '—' }}</span>
                <select v-else v-model="opportunityDetailForm.territory">
                  <option v-for="t in (opportunityFormOptions.territories || [])" :key="t.name" :value="t.name">{{ t.name }}</option>
                </select>
              </div>
              <div class="opp-field-row">
                <label>Người thực hiện</label>
                <span v-if="!opportunityDetailEditing">{{ opportunityDetail.document.opportunity_owner || '—' }}</span>
                <input v-else v-model="opportunityDetailForm.opportunity_owner">
              </div>
            </div>
            <div class="opp-info-section" style="grid-column: 1 / -1">
              <h4>Ghi chú</h4>
              <div class="opp-field-row">
                <span v-if="!opportunityDetailEditing" style="white-space:pre-wrap">{{ opportunityDetail.document.notes || '—' }}</span>
                <textarea v-else v-model="opportunityDetailForm.notes" rows="4" style="width:100%"></textarea>
              </div>
            </div>
          </div>
        </template>

        <!-- TAB: HÀNG HÓA -->
        <template v-else-if="opportunityDetailTab === 'items'">
          <div v-if="!opportunityDetail.items.length" class="crm-empty" style="margin-top:40px">📦 Chưa có hàng hóa nào.</div>
          <div v-else class="opp-items-wrap">
            <table class="opp-items-table">
              <thead>
                <tr>
                  <th>STT</th><th>Mã HH</th><th>Tên HH</th><th>ĐVT</th>
                  <th>SL</th><th>Đơn giá</th><th>Thành tiền</th>
                  <th>Tỷ lệ CK</th><th>Tiền CK</th><th>Đơn giá sau CK</th><th>Thành tiền sau CK</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, idx) in opportunityDetail.items" :key="item.idx">
                  <td>{{ idx + 1 }}</td>
                  <td>{{ item.item_code }}</td>
                  <td>{{ item.item_name }}</td>
                  <td>{{ item.uom }}</td>
                  <td>{{ item.qty }}</td>
                  <td>{{ formatValue(item.rate, 'opportunity_amount') }}</td>
                  <td>{{ formatValue(item.amount, 'opportunity_amount') }}</td>
                  <td>{{ item.custom_discount_percentage }}%</td>
                  <td>{{ formatValue(item.custom_discount_amount, 'opportunity_amount') }}</td>
                  <td>{{ formatValue(item.custom_net_rate, 'opportunity_amount') }}</td>
                  <td>{{ formatValue(item.custom_net_amount, 'opportunity_amount') }}</td>
                </tr>
              </tbody>
              <tfoot>
                <tr class="opp-items-total">
                  <td colspan="6" style="text-align:right;font-weight:600">Tổng cộng:</td>
                  <td>{{ formatValue(opportunityDetail.items.reduce((s,i) => s + (i.amount||0), 0), 'opportunity_amount') }}</td>
                  <td></td>
                  <td>{{ formatValue(opportunityDetail.items.reduce((s,i) => s + (i.custom_discount_amount||0), 0), 'opportunity_amount') }}</td>
                  <td></td>
                  <td>{{ formatValue(opportunityDetail.items.reduce((s,i) => s + (i.custom_net_amount||0), 0), 'opportunity_amount') }}</td>
                </tr>
              </tfoot>
            </table>
          </div>
        </template>

        <!-- TAB: GHI CHÚ & ĐÍNH KÈM -->
        <template v-else-if="opportunityDetailTab === 'notes'">
          <div class="opp-notes-wrap">
            <div class="opp-section-card">
              <div class="opp-section-header"><h4>Ghi chú</h4></div>
              <div style="padding:14px">
                <p v-if="opportunityDetail.document.notes" style="white-space:pre-wrap">{{ opportunityDetail.document.notes }}</p>
                <p v-else class="crm-empty">Chưa có ghi chú.</p>
              </div>
            </div>
            <div class="opp-section-card" style="margin-top:12px">
              <div class="opp-section-header"><h4>File đính kèm ({{ opportunityDetail.attachments.length }})</h4></div>
              <div v-if="!opportunityDetail.attachments.length" class="opp-section-empty">📎 Chưa có file đính kèm.</div>
              <div v-else style="padding:8px 14px">
                <div v-for="f in opportunityDetail.attachments" :key="f.name" class="opp-attachment-row">
                  <span>📎 {{ f.file_name }}</span>
                  <a :href="f.file_url" target="_blank" class="crm-button" style="font-size:11px;padding:2px 8px">Tải về</a>
                </div>
              </div>
            </div>
          </div>
        </template>

        <!-- TAB: LIÊN HỆ -->
        <template v-else-if="opportunityDetailTab === 'contacts'">
          <div v-if="!opportunityDetail.contacts.length" class="crm-empty" style="margin-top:40px">Chưa có liên hệ nào.</div>
          <table v-else class="customer-table">
            <thead><tr><th>Họ tên</th><th>Email</th><th>SĐT</th><th>Chức vụ</th><th>Công ty</th></tr></thead>
            <tbody>
              <tr v-for="c in opportunityDetail.contacts" :key="c.name">
                <td>{{ c.full_name }}</td>
                <td>{{ c.email_id || '—' }}</td>
                <td>{{ c.mobile_no || '—' }}</td>
                <td>{{ c.designation || '—' }}</td>
                <td>{{ c.company_name || '—' }}</td>
              </tr>
            </tbody>
          </table>
        </template>

        <!-- TAB: BÁN HÀNG -->
        <template v-else-if="opportunityDetailTab === 'sales'">
          <div class="opp-sales-wrap">
            <div class="opp-section-card">
              <div class="opp-section-header"><h4>Báo giá ({{ opportunityDetail.quotations.length }})</h4></div>
              <div v-if="!opportunityDetail.quotations.length" class="opp-section-empty">Chưa có báo giá.</div>
              <div v-else>
                <button v-for="q in opportunityDetail.quotations" :key="q.name" class="profile-record-row" @click="openRelated('Quotation', q)">
                  <span><strong>{{ q.name }}</strong><small>{{ formatValue(q.transaction_date, 'transaction_date') }}</small></span>
                  <span><b>{{ formatValue(q.grand_total, 'grand_total') }}</b><small>{{ q.status }}</small></span>
                </button>
              </div>
            </div>
            <div class="opp-section-card" style="margin-top:12px">
              <div class="opp-section-header"><h4>Đơn hàng ({{ opportunityDetail.orders.length }})</h4></div>
              <div v-if="!opportunityDetail.orders.length" class="opp-section-empty">Chưa có đơn hàng.</div>
              <div v-else>
                <button v-for="o in opportunityDetail.orders" :key="o.name" class="profile-record-row" @click="openRelated('Sales Order', o)">
                  <span><strong>{{ o.name }}</strong><small>{{ formatValue(o.transaction_date, 'transaction_date') }}</small></span>
                  <span><b>{{ formatValue(o.grand_total, 'grand_total') }}</b><small>{{ o.status }}</small></span>
                </button>
              </div>
            </div>
            <div class="opp-section-card" style="margin-top:12px">
              <div class="opp-section-header"><h4>Hóa đơn ({{ opportunityDetail.invoices.length }})</h4></div>
              <div v-if="!opportunityDetail.invoices.length" class="opp-section-empty">Chưa có hóa đơn.</div>
              <div v-else>
                <button v-for="inv in opportunityDetail.invoices" :key="inv.name" class="profile-record-row" @click="openRelated('Sales Invoice', inv)">
                  <span><strong>{{ inv.name }}</strong><small>{{ formatValue(inv.posting_date, 'posting_date') }}</small></span>
                  <span><b>{{ formatValue(inv.grand_total, 'grand_total') }}</b><small>Còn nợ {{ formatValue(inv.outstanding_amount, 'grand_total') }}</small></span>
                </button>
              </div>
            </div>
          </div>
        </template>

        <!-- TAB: HOẠT ĐỘNG -->
        <template v-else-if="opportunityDetailTab === 'activities'">
          <div v-if="!opportunityDetail.activities.length" class="crm-empty" style="margin-top:40px">Chưa có hoạt động nào.</div>
          <table v-else class="customer-table">
            <thead><tr><th>Tên</th><th>Loại</th><th>Ngày</th><th>Trạng thái</th><th>Người thực hiện</th></tr></thead>
            <tbody>
              <tr v-for="a in opportunityDetail.activities" :key="a.name">
                <td>{{ a.subject || a.description || a.name }}</td>
                <td>{{ a.activity_doctype === 'Event' ? (a.event_category || 'Sự kiện') : 'Công việc' }}</td>
                <td>{{ formatValue(a.date || a.starts_on, 'expected_closing') }}</td>
                <td>{{ a.status || '—' }}</td>
                <td>{{ a.assigned_by_full_name || a.owner || '—' }}</td>
              </tr>
            </tbody>
          </table>
        </template>

        <!-- TAB: TRAO ĐỔI -->
        <template v-else-if="opportunityDetailTab === 'chat'">
          <div class="opp-chat-wrap">
            <div class="opp-chat-messages">
              <div v-if="!opportunityDetail.comments.length" class="crm-empty">Chưa có trao đổi nào.</div>
              <div v-for="c in opportunityDetail.comments" :key="c.name" class="opp-comment-item">
                <div class="opp-comment-avatar">{{ (c.comment_by_fullname || c.comment_by || '?')[0].toUpperCase() }}</div>
                <div class="opp-comment-body">
                  <strong>{{ c.comment_by_fullname || c.comment_by }}</strong>
                  <p v-html="c.content"></p>
                  <small>{{ formatValue(c.creation, 'creation') }}</small>
                </div>
              </div>
            </div>
            <div class="opp-chat-input">
              <input v-model="opportunityDetailComment" placeholder="Nhập nội dung trao đổi..." @keyup.enter="saveOpportunityDetailComment">
              <button class="crm-button primary" :disabled="!opportunityDetailComment.trim()" @click="saveOpportunityDetailComment">Gửi</button>
            </div>
          </div>
        </template>

        <!-- TAB: HỖ TRỢ -->
        <template v-else-if="opportunityDetailTab === 'support'">
          <div class="crm-empty" style="margin-top:40px">🛠 Tính năng hỗ trợ đang được phát triển.</div>
        </template>
      </div>
    </div>
  </div>
</main>
```

- [ ] **3.2 Add `getStageClass` helper function** (after `saveOpportunityDetailEdit`):

```javascript
function getStageClass(stage, currentStage, idx) {
  const ORDERED = [
    "Kinh doanh lập yêu cầu",
    "P.TH check thông tin",
    "Thực hiện khảo sát",
    "Kinh doanh báo giá cho KH",
  ];
  const currentIdx = ORDERED.indexOf(currentStage);
  const stageIdx = ORDERED.indexOf(stage);
  if (stageIdx < currentIdx) return "done";
  if (stage === currentStage) return "active";
  return "";
}
```

---

## Task 4 — CSS

**File:** `dcnet-crm/frontend/src/styles.css` — append at end

- [ ] **4.1 Append opportunity-detail CSS**

```css
/* ── OPPORTUNITY DETAIL PAGE ──────────────────────────────── */
.opp-detail-page {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
  background: #f4f5f7;
}

.opp-detail-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 16px;
  background: #fff;
  border-bottom: 1px solid #e4e7ec;
  flex-shrink: 0;
}
.opp-back-btn {
  background: none;
  border: none;
  font-size: 20px;
  color: #667085;
  cursor: pointer;
  padding: 0 4px;
}
.opp-detail-code { font-weight: 700; font-size: 15px; color: #1a1d23; }
.opp-detail-stage-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #1a1d23;
  color: #fff;
  padding: 4px 12px;
  border-radius: 5px;
  font-size: 12px;
}
.opp-stage-dot { font-size: 10px; color: #4ade80; }
.opp-detail-header-spacer { flex: 1; }
.opp-refresh-btn { color: #667085; }

.opp-detail-body {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* LEFT SIDEBAR */
.opp-detail-sidebar {
  width: 220px;
  flex-shrink: 0;
  background: #fff;
  border-right: 1px solid #e4e7ec;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}
.opp-detail-sidebar-customer {
  padding: 14px 14px 10px;
  border-bottom: 1px solid #f0f2f5;
}
.opp-detail-sidebar-customer h3 {
  font-size: 13px;
  font-weight: 600;
  line-height: 1.4;
  margin-bottom: 3px;
}
.opp-detail-sidebar-customer small { font-size: 11px; color: #6c757d; }
.opp-sidebar-tag {
  display: inline-block;
  background: #e9f0ff;
  color: #2563eb;
  font-size: 10px;
  padding: 2px 8px;
  border-radius: 10px;
  margin-top: 6px;
  cursor: pointer;
}
.opp-detail-sidebar-actions {
  padding: 8px 14px;
  display: flex;
  gap: 6px;
  border-bottom: 1px solid #f0f2f5;
}
.opp-detail-sidebar-actions .act-btn {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 1px solid #e4e7ec;
  background: #f8f9fc;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  cursor: pointer;
  color: #344054;
}
.opp-detail-sidebar-stats {
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.opp-stat-row { display: flex; flex-direction: column; gap: 2px; }
.opp-stat-label { font-size: 10px; color: #98a1b3; text-transform: uppercase; letter-spacing: 0.4px; }
.opp-stat-value { font-size: 12px; font-weight: 500; color: #1a1d23; }
.opp-stat-value.blue { color: #2563eb; font-weight: 700; }

/* MAIN */
.opp-detail-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.opp-detail-tabs {
  display: flex;
  background: #fff;
  border-bottom: 1px solid #e4e7ec;
  padding: 0 14px;
  gap: 2px;
  overflow-x: auto;
  flex-shrink: 0;
}
.opp-detail-tabs button {
  padding: 10px 14px;
  font-size: 12px;
  font-weight: 500;
  color: #667085;
  border: none;
  background: transparent;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 5px;
}
.opp-detail-tabs button.active { color: #2563eb; border-bottom-color: #2563eb; }
.opp-tab-badge {
  background: #2563eb;
  color: #fff;
  font-size: 10px;
  padding: 1px 5px;
  border-radius: 8px;
  font-weight: 700;
}
.opp-detail-tab-content {
  flex: 1;
  overflow-y: auto;
  padding: 14px;
  display: flex;
  gap: 12px;
}

/* TỔNG QUAN */
.opp-overview-main { flex: 1; display: flex; flex-direction: column; gap: 12px; min-width: 0; }
.opp-overview-right { width: 260px; flex-shrink: 0; }

.opp-stage-progress {
  background: #fff;
  border: 1px solid #e4e7ec;
  border-radius: 8px;
  padding: 14px;
}
.opp-stage-track { display: flex; }
.opp-stage-step {
  flex: 1;
  background: #e4e7ec;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 500;
  color: #667085;
  clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 50%, calc(100% - 10px) 100%, 0 100%, 10px 50%);
  margin-right: -1px;
  padding: 0 16px;
  text-align: center;
}
.opp-stage-step:first-child {
  clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 50%, calc(100% - 10px) 100%, 0 100%);
  border-radius: 4px 0 0 4px;
}
.opp-stage-step:last-child { border-radius: 0 4px 4px 0; clip-path: none; }
.opp-stage-step.done { background: #dbeafe; color: #2563eb; }
.opp-stage-step.active { background: #2563eb; color: #fff; }
.opp-stage-step.win { background: #d1fae5; color: #059669; }
.opp-stage-step.active-win { background: #059669; color: #fff; }
.opp-stage-step.lose { background: #fee2e2; color: #dc2626; }
.opp-stage-step.active-lose { background: #dc2626; color: #fff; }

.opp-stat-cards { display: flex; gap: 10px; }
.opp-stat-card {
  flex: 1;
  background: #fff;
  border: 1px solid #e4e7ec;
  border-radius: 8px;
  padding: 14px;
}
.opp-sc-label { font-size: 10px; color: #98a1b3; text-transform: uppercase; margin-bottom: 6px; }
.opp-sc-value { font-size: 18px; font-weight: 700; color: #1a1d23; }

.opp-section-card {
  background: #fff;
  border: 1px solid #e4e7ec;
  border-radius: 8px;
  overflow: hidden;
}
.opp-section-header {
  padding: 10px 14px;
  border-bottom: 1px solid #f0f2f5;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.opp-section-header h4 { font-size: 13px; font-weight: 600; }
.opp-section-empty { padding: 24px; text-align: center; color: #98a1b3; font-size: 12px; }

.opp-mini-table { width: 100%; border-collapse: collapse; font-size: 12px; }
.opp-mini-table th, .opp-mini-table td { padding: 6px 12px; border-bottom: 1px solid #f0f2f5; text-align: left; }
.opp-mini-table th { background: #fafbfc; font-size: 11px; color: #667085; }

/* Comment / chat shared */
.opp-comment-list { padding: 8px 14px; display: flex; flex-direction: column; gap: 10px; }
.opp-comment-item { display: flex; gap: 10px; }
.opp-comment-avatar {
  width: 30px; height: 30px; border-radius: 50%;
  background: #4361ee; color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 12px; flex-shrink: 0;
}
.opp-comment-body strong { font-size: 12px; font-weight: 600; display: block; margin-bottom: 2px; }
.opp-comment-body p { font-size: 12px; color: #344054; line-height: 1.5; }
.opp-comment-body small { font-size: 11px; color: #98a1b3; }
.opp-comment-input {
  display: flex;
  gap: 8px;
  padding: 10px 14px;
  border-top: 1px solid #f0f2f5;
}
.opp-comment-input input {
  flex: 1;
  border: 1px solid #e4e7ec;
  border-radius: 6px;
  padding: 7px 12px;
  font-size: 12px;
  outline: none;
}
.opp-comment-input input:focus { border-color: #2563eb; }

/* Activity right panel */
.opp-activity-panel {
  background: #fff;
  border: 1px solid #e4e7ec;
  border-radius: 8px;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.opp-activity-tabs { display: flex; border-bottom: 1px solid #e4e7ec; flex-shrink: 0; }
.opp-activity-tabs .atab {
  flex: 1; padding: 8px;
  font-size: 11px; font-weight: 600;
  text-align: center; cursor: pointer;
  border: none; background: transparent;
  border-bottom: 2px solid transparent; color: #667085;
}
.opp-activity-tabs .atab.active { color: #2563eb; border-bottom-color: #2563eb; }
.opp-activity-list { flex: 1; overflow-y: auto; padding: 8px; }
.opp-timeline-item { display: flex; gap: 8px; padding: 8px 0; border-bottom: 1px solid #f0f2f5; }
.opp-tl-avatar {
  width: 28px; height: 28px; border-radius: 50%;
  background: #4361ee; color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 11px; flex-shrink: 0;
}
.opp-tl-body strong { font-size: 11px; font-weight: 600; display: block; margin-bottom: 2px; }
.opp-tl-body p { font-size: 11px; color: #667085; line-height: 1.4; }
.opp-tl-body small { font-size: 10px; color: #98a1b3; }

/* Thông tin chi tiết */
.opp-info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  width: 100%;
}
.opp-info-section {
  background: #fff;
  border: 1px solid #e4e7ec;
  border-radius: 8px;
  padding: 14px;
}
.opp-info-section h4 { font-size: 12px; font-weight: 700; color: #667085; text-transform: uppercase; margin-bottom: 12px; }
.opp-field-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 6px 0;
  border-bottom: 1px solid #f8f9fc;
  font-size: 12px;
}
.opp-field-row label { width: 130px; flex-shrink: 0; color: #667085; }
.opp-field-row span { color: #1a1d23; }
.opp-field-row input, .opp-field-row select, .opp-field-row textarea {
  flex: 1;
  border: 1px solid #d0d5dd;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 12px;
  outline: none;
}
.opp-field-row input:focus, .opp-field-row select:focus, .opp-field-row textarea:focus {
  border-color: #2563eb;
}

/* Hàng hóa tab */
.opp-items-wrap { width: 100%; overflow-x: auto; }
.opp-items-table { border-collapse: collapse; min-width: 900px; width: 100%; font-size: 12px; background: #fff; border-radius: 8px; overflow: hidden; }
.opp-items-table th, .opp-items-table td { padding: 8px 10px; border-bottom: 1px solid #e4e7ec; text-align: right; white-space: nowrap; }
.opp-items-table th { background: #fafbfc; font-size: 11px; color: #667085; text-align: center; border-bottom: 2px solid #d0d5dd; }
.opp-items-table td:nth-child(3) { text-align: left; }
.opp-items-total td { border-top: 2px solid #d0d5dd; border-bottom: 0; font-weight: 600; background: #fafbfc; }

/* Attachment */
.opp-attachment-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #f0f2f5;
  font-size: 12px;
}

/* Sales wrap */
.opp-sales-wrap { width: 100%; }

/* Chat */
.opp-chat-wrap { display: flex; flex-direction: column; height: 100%; min-height: 0; }
.opp-chat-messages { flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; padding-bottom: 8px; }
.opp-chat-input {
  display: flex;
  gap: 8px;
  padding-top: 10px;
  border-top: 1px solid #e4e7ec;
  flex-shrink: 0;
}
.opp-chat-input input {
  flex: 1;
  border: 1px solid #e4e7ec;
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 12px;
  outline: none;
}
.opp-chat-input input:focus { border-color: #2563eb; }

/* Notes wrap */
.opp-notes-wrap { width: 100%; }

/* Link in opportunity list */
.opp-link { color: #2563eb; text-decoration: none; font-weight: 500; }
.opp-link:hover { text-decoration: underline; }
```

---

## Task 5 — Build, cache clear, verify

- [ ] **5.1 Build bundle**

```bash
docker exec devcontainer-frappe-1 bash -lc \
  'cd /workspace/development/frappe-bench && bench build --app dcnet_crm 2>&1 | tail -10'
```
Expected: `Done in X.XXs.`

- [ ] **5.2 Clear cache**

```bash
docker exec devcontainer-frappe-1 bash -lc \
  'cd /workspace/development/frappe-bench && bench --site flow.local clear-cache && bench --site flow.local clear-website-cache'
```

- [ ] **5.3 Manual verification checklist**

`Ctrl+Shift+R` to reload. Then:

1. Go to `/desk/dcnet-crm?view=opportunities`
2. Click on a title in the opportunity table → should navigate to `?view=opportunity-detail&opportunity={name}`
3. Left sidebar shows customer name, stats
4. 9 tabs are visible and clickable
5. Tổng quan: stage progress bar shows current stage highlighted, stat cards, sections
6. Thông tin chi tiết: fields visible; click Sửa → inputs appear; save works
7. Hàng hóa: items table with all columns
8. Trao đổi: type a comment → Enter → comment appears
9. Back button → returns to opportunities list

- [ ] **5.4 Commit**

```bash
git add dcnet-crm/frontend/src/main.js dcnet-crm/frontend/src/styles.css dcnet-crm/dcnet_crm/api.py
git commit -m "feat(dcnet-crm): opportunity detail page — 9 tabs, MISA-style layout"
```
