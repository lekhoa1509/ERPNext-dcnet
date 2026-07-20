import { ref, computed, watch } from "vue/dist/vue.esm-bundler.js";
import { call, exportResource, formatValue } from "../../utils.js";
import { OPPORTUNITY_COLUMNS } from "../../constants.js";

export function useOpportunities(ctx) {
  const opportunityMoreOpen = ref(false);
  const opportunityDetailMoreOpen = ref(false);
  const opportunityActivityOpen = ref(true);
  const opportunityFilterOpen = ref(true);
  const opportunityTab = ref("activity");
  const opportunityPanelScope = ref("opportunity");
  const opportunityCustomerDetail = ref(null);
  const opportunityCustomerLoading = ref(false);
  let opportunityCustomerRequestId = 0;
  const opportunityVisibleFields = ref(OPPORTUNITY_COLUMNS.map((item) => item.field));
  const opportunityColumnDialogOpen = ref(false);
  const opportunityColumnSearch = ref("");
  const opportunityColumnDraft = ref([]);
  const opportunityEnabledFilters = ref([]);
  const opportunityFilterValues = ref({});
  const opportunityFormOpen = ref(false);
  const opportunitySaving = ref(false);
  const leaveFormConfirmOpen = ref(false);
  const pendingNavigationView = ref("");
  const itemPickerOpen = ref(false);
  const itemPickerSearch = ref("");
  const itemPickerPage = ref(1);
  const itemPickerPageLength = ref(10);
  const itemPickerSelected = ref([]);
  const itemPickerCategoryFilter = ref("");
  const opportunityFormOptions = ref({
    customers: [], contacts: [], sources: [], opportunity_types: [], sales_stages: [],
    companies: [], territories: [], countries: [], items: [], default_company: "",
  });
  const opportunityForm = ref({});
  const opportunityDetailName = ref("");
  const opportunityDetail = ref(null);
  const opportunityDetailTab = ref("overview");
  const opportunitySalesSection = ref("stage_history");
  const opportunityNotesSection = ref("notes");
  const opportunityNotesCollapsed = ref(false);
  const opportunityDetailEditing = ref(false);
  const opportunityDetailSaving = ref(false);
  const opportunityDetailForm = ref({});
  const opportunityDetailFieldSearch = ref("");
  const opportunityDetailShowEmpty = ref(true);
  const opportunityDetailComment = ref("");
  const opportunityAttachmentUploading = ref(false);
  const oppActivityPanelTab = ref("activity");
  const opportunitySummaryFieldOptions = [
    { field: "contact_display", label: "Liên hệ", value: (doc) => doc.contact_display || doc.contact_person || "— Không chọn —" },
    { field: "opportunity_amount", label: "Số tiền", cls: "blue", value: (doc) => formatMoney(doc.opportunity_amount) },
    { field: "sales_stage", label: "Giai đoạn", value: (doc) => doc.sales_stage || "—" },
    { field: "probability", label: "Tỷ lệ thành công", value: (doc) => `${doc.probability || 0}%` },
    {
      field: "expected_revenue",
      label: "Doanh số kỳ vọng",
      cls: "blue",
      value: (doc) => formatMoney((doc.opportunity_amount || 0) * (doc.probability || 0) / 100),
    },
    { field: "expected_closing", label: "Ngày kỳ vọng", value: (doc) => doc.expected_closing || "—" },
    { field: "opportunity_owner", label: "Người thực hiện", value: (doc) => doc.opportunity_owner || "—" },
    { field: "opportunity_type", label: "Loại", value: (doc) => doc.opportunity_type || "—" },
    { field: "source", label: "Nguồn", value: (doc) => doc.source || "—" },
  ];
  const opportunitySummaryDefaultFields = opportunitySummaryFieldOptions.map((item) => item.field);
  // Extra fields the summary picker also offers, mirroring everything shown in the
  // "Thông tin chi tiết" tab — not selected by default, only available to add.
  opportunitySummaryFieldOptions.push(
    { field: "customer_name", label: "Khách hàng", value: (doc) => doc.customer_name || doc.party_name || "—" },
    { field: "customer_group", label: "Loại khách hàng", value: (doc) => doc.customer_group || "—" },
    { field: "contact_email", label: "Email liên hệ", value: (doc) => doc.contact_email || "—" },
    { field: "contact_mobile", label: "SĐT liên hệ", value: (doc) => doc.contact_mobile || "—" },
    { field: "title", label: "Tên cơ hội", value: (doc) => doc.title || "—" },
    { field: "custom_item_category", label: "Loại hàng hóa", value: (doc) => doc.custom_item_category || "—" },
    { field: "territory", label: "Khu vực lắp đặt dịch vụ", value: (doc) => doc.territory || "—" },
    { field: "campaign_name", label: "Chiến dịch", value: (doc) => doc.campaign_name || "—" },
    { field: "lost_reasons", label: "Lý do thắng/thua", value: (doc) => (doc.lost_reasons || []).join(", ") || "—" },
    { field: "custom_result_other_reason", label: "Lý do khác", value: (doc) => doc.custom_result_other_reason || "—" },
    { field: "custom_shipping_address", label: "Địa chỉ", value: (doc) => doc.custom_shipping_address || "—" },
    { field: "custom_shipping_country", label: "Quốc gia", value: (doc) => doc.custom_shipping_country || "—" },
    { field: "custom_shipping_state", label: "Tỉnh/Thành phố", value: (doc) => doc.custom_shipping_state || "—" },
    { field: "custom_shipping_county", label: "Quận/Huyện", value: (doc) => doc.custom_shipping_county || "—" },
    { field: "custom_branch", label: "Đơn vị", value: (doc) => doc.custom_branch || "—" },
    { field: "custom_sales_process", label: "Quy trình bán hàng", value: (doc) => doc.custom_sales_process || "—" },
    { field: "custom_related_person", label: "Người liên quan", value: (doc) => doc.custom_related_person || "—" },
    { field: "custom_referral_partner", label: "Đối tác/CTV giới thiệu", value: (doc) => doc.custom_referral_partner || "—" },
    { field: "custom_opportunity_code", label: "Mã cơ hội", value: (doc) => doc.custom_opportunity_code || "—" },
    { field: "owner_full_name", label: "Người tạo", value: (doc) => doc.owner_full_name || "—" },
    { field: "creation", label: "Ngày tạo", value: (doc) => formatValue(doc.creation, "creation") },
  );
  const opportunitySummaryFields = ref(loadOpportunitySummaryFields());
  const opportunitySummaryDialogOpen = ref(false);
  const opportunitySummarySearch = ref("");
  const opportunitySummaryDraft = ref([]);

  const opportunityLinkedCustomerName = computed(() => {
    const doc = ctx.detail.value?.document || {};
    return doc.opportunity_from === "Customer" ? (doc.party_name || "") : "";
  });

  const opportunityPanelDetail = computed(() => (
    opportunityPanelScope.value === "customer"
      ? opportunityCustomerDetail.value
      : ctx.detail.value
  ));

  function normalisePanelActivities(detail, scope) {
    if (!detail) return [];
    const timeline = (detail.timeline || []).map((row) => ({
      ...row,
      panel_key: `${scope}-timeline-${row.name}`,
      panel_title: row.subject || row.description || (scope === "customer" ? "Hoạt động khách hàng" : "Hoạt động cơ hội"),
      panel_content: row.content || row.description || row.subject || "",
      panel_date: row.creation || row.communication_date || row.modified || "",
      panel_icon: row.activity_type === "communication" ? "email" : "contact",
    }));
    const activities = (detail.activities || []).map((row) => ({
      ...row,
      panel_key: `${scope}-activity-${row.activity_doctype || row.type || "activity"}-${row.name}`,
      panel_title: row.subject || row.description || row.activity_type || row.activity_doctype || "Hoạt động",
      panel_content: row.description || row.subject || "",
      panel_date: row.date || row.starts_on || row.creation || row.modified || "",
      panel_icon: row.activity_doctype === "Event" ? "calendar" : "task",
    }));
    return [...timeline, ...activities].sort((left, right) => (
      String(right.panel_date || "").localeCompare(String(left.panel_date || ""))
    ));
  }

  const opportunityPanelActivities = computed(() => normalisePanelActivities(
    opportunityPanelDetail.value,
    opportunityPanelScope.value,
  ));

  const opportunityPanelPurchases = computed(() => {
    const detail = opportunityPanelDetail.value || {};
    const records = [
      ...(detail.quotations || []).map((row) => ({
        ...row, record_label: "Báo giá", record_doctype: "Quotation", record_date: row.transaction_date,
      })),
      ...(detail.orders || []).map((row) => ({
        ...row, record_label: "Đơn hàng", record_doctype: "Sales Order", record_date: row.transaction_date,
      })),
      ...(detail.invoices || []).map((row) => ({
        ...row, record_label: "Hóa đơn", record_doctype: "Sales Invoice", record_date: row.posting_date,
      })),
    ];
    return records.sort((left, right) => String(right.record_date || "").localeCompare(String(left.record_date || "")));
  });

  const opportunityPanelContacts = computed(() => opportunityPanelDetail.value?.contacts || []);
  const opportunityPanelItems = computed(() => ctx.detail.value?.items || []);

  async function loadOpportunityLinkedCustomer() {
    const customerName = opportunityLinkedCustomerName.value;
    const requestId = ++opportunityCustomerRequestId;
    opportunityCustomerDetail.value = null;
    if (!customerName) {
      opportunityCustomerLoading.value = false;
      return;
    }
    opportunityCustomerLoading.value = true;
    try {
      const customerDetail = await call("get_customer_workspace", { name: customerName });
      if (requestId === opportunityCustomerRequestId && customerName === opportunityLinkedCustomerName.value) {
        opportunityCustomerDetail.value = customerDetail;
      }
    } catch (error) {
      if (requestId === opportunityCustomerRequestId) {
        frappe.msgprint(error.message || __("Không thể tải dữ liệu khách hàng liên kết."));
      }
    } finally {
      if (requestId === opportunityCustomerRequestId) opportunityCustomerLoading.value = false;
    }
  }

  function setOpportunityPanelScope(scope) {
    if (scope === "customer" && !opportunityLinkedCustomerName.value) return;
    opportunityPanelScope.value = scope;
    opportunityTab.value = "activity";
  }

  watch(
    () => ctx.detail.value?.document?.name,
    () => {
      opportunityCustomerRequestId += 1;
      opportunityCustomerDetail.value = null;
      opportunityCustomerLoading.value = false;
      if (opportunityPanelScope.value === "customer") loadOpportunityLinkedCustomer();
    },
  );

  watch(opportunityPanelScope, (scope) => {
    if (scope === "customer" && !opportunityCustomerDetail.value) loadOpportunityLinkedCustomer();
  });
  const opportunityDetailMoreActions = [
    { key: "handoff", label: "Bàn giao công việc", icon: "handoff" },
    { key: "approval", label: "Gửi phê duyệt", icon: "document" },
    { key: "purchase-request", label: "Yêu cầu mua hàng", icon: "order" },
    { key: "care-card", label: "Sinh thẻ tư vấn", icon: "care" },
    { key: "amis-chat", label: "Gửi qua AMIS Chat", icon: "message" },
    { separator: true, key: "sep-1" },
    { key: "summary", label: "Tùy chỉnh tóm tắt", icon: "sliders" },
    { key: "history", label: "Nhật ký", icon: "history" },
    { separator: true, key: "sep-2" },
    { key: "print", label: "In", icon: "print" },
    { key: "clone", label: "Nhân bản", icon: "copy" },
    { key: "share", label: "Chia sẻ", icon: "share" },
    { key: "delete", label: "Xóa", icon: "trash", danger: true },
    { separator: true, key: "sep-3" },
    { key: "back-view", label: "Quay lại giao diện", icon: "arrow-left" },
  ];

  function formatMoney(value) {
    return new Intl.NumberFormat("vi-VN").format(Number(value || 0));
  }

  function loadOpportunitySummaryFields() {
    try {
      const raw = window.localStorage.getItem("dcnet-crm-opportunity-summary-fields");
      const parsed = JSON.parse(raw || "[]");
      const allowed = new Set(opportunitySummaryFieldOptions.map((item) => item.field));
      const fields = Array.isArray(parsed) ? parsed.filter((field) => allowed.has(field)) : [];
      return fields.length ? fields : [...opportunitySummaryDefaultFields];
    } catch {
      return [...opportunitySummaryDefaultFields];
    }
  }

  const opportunitySummaryRows = computed(() => {
    const doc = opportunityDetail.value?.document || {};
    return opportunitySummaryFieldOptions
      .filter((item) => opportunitySummaryFields.value.includes(item.field))
      .map((item) => ({
        ...item,
        display: item.value(doc),
      }));
  });
  const availableOpportunitySummaryFields = computed(() => {
    const keyword = opportunitySummarySearch.value.trim().toLocaleLowerCase("vi");
    return opportunitySummaryFieldOptions.filter((item) => (
      !opportunitySummaryDraft.value.includes(item.field)
      && (!keyword || item.label.toLocaleLowerCase("vi").includes(keyword))
    ));
  });
  const selectedOpportunitySummaryFields = computed(() => opportunitySummaryDraft.value
    .map((field) => opportunitySummaryFieldOptions.find((item) => item.field === field))
    .filter(Boolean));

  const opportunitySalesMenu = computed(() => {
    const detail = opportunityDetail.value || {};
    const tabs = [
      { key: "orders", label: "Đơn hàng", icon: "cart", count: detail.orders?.length || 0 },
      { key: "quotations", label: "Báo giá", icon: "quotation", count: detail.quotations?.length || 0 },
      { key: "stage_history", label: "Lịch sử giai đoạn", icon: "history", count: detail.stage_history?.length || 0 },
      { key: "purchase_requests", label: "Yêu cầu mua hàng", icon: "order", count: detail.purchase_requests?.length || 0 },
    ];
    return tabs;
  });

  const opportunitySalesCount = computed(() => {
    const detail = opportunityDetail.value || {};
    return (detail.orders?.length || 0)
      + (detail.quotations?.length || 0)
      + (detail.stage_history?.length || 0)
      + (detail.purchase_requests?.length || 0);
  });

  const opportunityDetailTabs = computed(() => {
    const detail = opportunityDetail.value || {};
    const tabs = [
      { key: "overview", label: "Tổng quan" },
      { key: "info", label: "Thông tin chi tiết" },
      { key: "items", label: "Hàng hóa", count: detail.items?.length || 0 },
      { key: "notes", label: "Ghi chú & đính kèm", count: detail.attachments?.length || 0 },
      { key: "contacts", label: "Liên hệ", count: detail.contacts?.length || 0 },
      { key: "sales", label: "Bán hàng", count: opportunitySalesCount.value },
      { key: "activities", label: "Hoạt động", count: detail.activities?.length || 0 },
      { key: "chat", label: "Trao đổi", count: detail.comments?.length || 0 },
    ];
    if (ctx.boot.value?.show_unready_features) tabs.push({ key: "support", label: "Hỗ trợ" });
    return tabs;
  });

  const opportunityFormDirty = computed(() => {
    const f = opportunityForm.value;
    if (!f || !opportunityFormOpen.value) return false;
    if (f.party_name) return true;
    if (f.title) return true;
    if (f.opportunity_type) return true;
    if (f.notes) return true;
    if (f.items && f.items.some((item) => item.item_code || item.item_name)) return true;
    return false;
  });

  const itemPickerFiltered = computed(() => {
    const kw = itemPickerSearch.value.trim().toLocaleLowerCase("vi");
    const cat = itemPickerCategoryFilter.value;
    return (opportunityFormOptions.value.items || []).filter((item) => {
      if (cat && item.item_group !== cat) return false;
      if (!kw) return true;
      return (item.name || "").toLocaleLowerCase("vi").includes(kw)
        || (item.item_name || "").toLocaleLowerCase("vi").includes(kw);
    });
  });
  const itemPickerPageCount = computed(() => Math.ceil(itemPickerFiltered.value.length / itemPickerPageLength.value) || 1);
  const itemPickerRows = computed(() => {
    const start = (itemPickerPage.value - 1) * itemPickerPageLength.value;
    return itemPickerFiltered.value.slice(start, start + itemPickerPageLength.value);
  });
  const itemPickerCategories = computed(() => {
    const cats = new Set((opportunityFormOptions.value.items || []).map((i) => i.item_group).filter(Boolean));
    return [...cats].sort((a, b) => a.localeCompare(b, "vi"));
  });

  async function loadOpportunityDetail(name) {
    const targetName = name !== undefined ? name : opportunityDetailName.value;
    if (!targetName) return ctx.navigate("opportunities");
    ctx.loading.value = true;
    opportunityDetail.value = null;
    try {
      opportunityDetail.value = await call("get_opportunity_detail", { name: targetName });
      opportunityDetailName.value = targetName;
      if (!opportunityFormOptions.value.sales_stages?.length) {
        opportunityFormOptions.value = await call("get_opportunity_form_options");
      }
    } catch (error) {
      frappe.msgprint(error.message || __("Không thể tải chi tiết cơ hội."));
    } finally {
      ctx.loading.value = false;
    }
  }

  function openOpportunityDetail(row) {
    if (!row?.name) return;
    opportunityDetailName.value = row.name;
    opportunityDetailTab.value = "overview";
    opportunitySalesSection.value = "stage_history";
    opportunityDetailEditing.value = false;
    ctx.route.value = "opportunity-detail";
    frappe.route_options = { view: "opportunity-detail", opportunity: row.name };
    frappe.set_route("dcnet-crm").then(() => {
      const url = new URL(window.location.href);
      url.hash = "";
      url.searchParams.set("view", "opportunity-detail");
      url.searchParams.set("opportunity", row.name);
      url.searchParams.delete("customer");
      window.history.replaceState(window.history.state, "", url);
    });
    if (!opportunityFormOptions.value.sales_stages?.length) {
      call("get_opportunity_form_options").then(opts => { opportunityFormOptions.value = opts; });
    }
  }

  function backToOpportunities() {
    ctx.navigate("opportunities");
  }

  function emptyOpportunityItem() {
    return {
      item_code: "", item_name: "", description: "",
      custom_installation_point_a_end: "", custom_installation_point_z_end: "",
      qty: 1, uom: "", rate: 0,
      custom_discount_percentage: 0, custom_discount_amount: 0,
      custom_net_rate: 0, custom_net_amount: 0,
    };
  }

  function calcItemDiscount(item) {
    const amount = (item.qty || 0) * (item.rate || 0);
    const pct = Math.min(100, Math.max(0, item.custom_discount_percentage || 0));
    item.custom_discount_amount = Math.round(amount * pct / 100 * 100) / 100;
    item.custom_net_rate = (item.rate || 0) * (1 - pct / 100);
    item.custom_net_amount = item.custom_net_rate * (item.qty || 0);
  }

  async function openOpportunityForm(customer = "", custDisplayName = "", contactPerson = "") {
    const closing = new Date();
    closing.setDate(closing.getDate() + 15);
    opportunityForm.value = {
      party_name: customer || "",
      contact_person: contactPerson || "",
      customer_group: "",
      utm_source: "",
      title: custDisplayName ? `Cơ hội - ${custDisplayName}` : "",
      opportunity_type: "",
      probability: 10,
      sales_stage: opportunityFormOptions.value.sales_stages[0]?.name || "",
      expected_closing: closing.toISOString().slice(0, 10),
      territory: "",
      company: opportunityFormOptions.value.default_company || opportunityFormOptions.value.companies[0]?.name || "",
      transaction_date: new Date().toISOString().slice(0, 10),
      notes: "",
      custom_auto_increase_duplicate_qty: 0,
      custom_shipping_country: "Vietnam",
      custom_shipping_state: "",
      custom_shipping_county: "",
      custom_shipping_ward: "",
      custom_shipping_address_line1: "",
      custom_shipping_pincode: "",
      custom_shipping_address: "",
      custom_is_shared: 0,
      custom_opportunity_code: "",
      custom_referral_partner: "",
      items: [],
    };
    opportunityFormOpen.value = true;
    try {
      if (!opportunityFormOptions.value.customers.length) {
        opportunityFormOptions.value = await call("get_opportunity_form_options");
      }
      if (!opportunityFormOpen.value) return;
      if (customer) {
        const matched = (opportunityFormOptions.value.customers || []).find((item) => item.name === customer);
        opportunityForm.value.customer_group ||= matched?.customer_group || "";
        opportunityForm.value.territory ||= matched?.territory || "";
      }
      opportunityForm.value.sales_stage ||= opportunityFormOptions.value.sales_stages[0]?.name || "";
      opportunityForm.value.company ||= opportunityFormOptions.value.default_company
        || opportunityFormOptions.value.companies[0]?.name
        || "";
    } catch (error) {
      frappe.msgprint(error.message || __("Không thể tải dữ liệu tạo cơ hội."));
    }
  }

  function closeOpportunityForm() {
    opportunityFormOpen.value = false;
    opportunityForm.value = {};
  }

  function addOpportunityItem() {
    opportunityForm.value.items.push(emptyOpportunityItem());
  }

  function clearOpportunityItems() {
    opportunityForm.value.items = [];
  }

  function removeOpportunityItem(index) {
    opportunityForm.value.items.splice(index, 1);
  }

  function openItemPicker() {
    itemPickerSearch.value = "";
    itemPickerPage.value = 1;
    itemPickerSelected.value = [];
    itemPickerCategoryFilter.value = "";
    itemPickerOpen.value = true;
  }

  function closeItemPicker() {
    itemPickerOpen.value = false;
    itemPickerSelected.value = [];
  }

  function toggleItemPickerRow(name) {
    const idx = itemPickerSelected.value.indexOf(name);
    if (idx >= 0) itemPickerSelected.value.splice(idx, 1);
    else itemPickerSelected.value.push(name);
  }

  function confirmItemPicker() {
    const toAdd = itemPickerSelected.value
      .map((name) => opportunityFormOptions.value.items.find((i) => i.name === name))
      .filter(Boolean);
    for (const item of toAdd) {
      const existing = opportunityForm.value.items.find((r) => r.item_code === item.name);
      if (existing && opportunityForm.value.custom_auto_increase_duplicate_qty) {
        existing.qty = (existing.qty || 0) + 1;
        calcItemDiscount(existing);
      } else {
        const row = emptyOpportunityItem();
        row.item_code = item.name;
        row.item_name = item.item_name || item.name;
        row.uom = item.stock_uom || "";
        opportunityForm.value.items.push(row);
      }
    }
    closeItemPicker();
  }

  function selectOpportunityItem(row) {
    const item = opportunityFormOptions.value.items.find((option) => option.name === row.item_code);
    if (!item) return;
    if (opportunityForm.value.custom_auto_increase_duplicate_qty) {
      const duplicate = opportunityForm.value.items.find(
        (current) => current !== row && current.item_code === row.item_code,
      );
      if (duplicate) {
        duplicate.qty = Number(duplicate.qty || 0) + Number(row.qty || 1);
        opportunityForm.value.items = opportunityForm.value.items.filter(
          (current) => current !== row,
        );
        return;
      }
    }
    row.item_name = item.item_name || item.name;
    row.uom = item.stock_uom || "";
    calcItemDiscount(row);
  }

  async function saveOpportunity(addAnother) {
    if (addAnother === undefined) addAnother = false;
    if (opportunitySaving.value) return;
    opportunitySaving.value = true;
    try {
      const result = await call("save_opportunity", { opportunity: opportunityForm.value }, "POST");
      frappe.show_alert({ message: __("Đã tạo cơ hội {0}", [result.name]), indicator: "green" });
      if (addAnother) await openOpportunityForm();
      else {
        closeOpportunityForm();
        await ctx.loadRows();
      }
    } catch (error) {
      frappe.msgprint(error.message || __("Không thể tạo cơ hội."));
    } finally {
      opportunitySaving.value = false;
    }
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

  function uploadOpportunityAttachment() {
    const name = opportunityDetailName.value;
    if (!name || opportunityAttachmentUploading.value) return;
    if (!frappe.ui?.FileUploader) {
      frappe.msgprint({ title: __("Đính kèm"), message: __("Bộ tải tệp chưa sẵn sàng. Vui lòng tải lại trang."), indicator: "orange" });
      return;
    }
    opportunityAttachmentUploading.value = true;
    new frappe.ui.FileUploader({
      doctype: "Opportunity",
      docname: name,
      allow_multiple: true,
      on_success: async () => {
        await loadOpportunityDetail(name);
        opportunityAttachmentUploading.value = false;
        frappe.show_alert({ message: __("Đã tải tệp đính kèm"), indicator: "green" });
      },
      on_error: () => { opportunityAttachmentUploading.value = false; },
    });
    window.setTimeout(() => { opportunityAttachmentUploading.value = false; }, 1000);
  }

  function addOpportunityAttachmentLink() {
    const name = opportunityDetailName.value;
    if (!name) return;
    frappe.prompt(
      [
        { fieldname: "url", fieldtype: "Data", label: "Liên kết (URL)", default: "https://", reqd: 1 },
        { fieldname: "title", fieldtype: "Data", label: "Tên hiển thị" },
      ],
      async (values) => {
        try {
          await call("add_opportunity_attachment_link", {
            name,
            url: values.url.trim(),
            title: values.title || "",
          }, "POST");
          await loadOpportunityDetail(name);
          frappe.show_alert({ message: __("Đã thêm liên kết."), indicator: "green" });
        } catch (err) {
          frappe.msgprint(err.message || __("Không thể thêm liên kết."));
        }
      },
      "Thêm liên kết",
      "Thêm"
    );
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

  function showOpportunityDetailField(label, value) {
    const keyword = opportunityDetailFieldSearch.value.trim().toLocaleLowerCase("vi");
    const matchesSearch = !keyword || label.toLocaleLowerCase("vi").includes(keyword);
    const hasValue = value !== null && value !== undefined && String(value).trim() !== "" && String(value).trim() !== "-";
    return matchesSearch && (opportunityDetailShowEmpty.value || hasValue || opportunityDetailEditing.value);
  }

  async function setOpportunityStage(stage) {
    if (!opportunityDetail.value || opportunityDetailSaving.value) return;
    if (opportunityDetail.value.document.sales_stage === stage) return;
    opportunityDetailSaving.value = true;
    try {
      await call("update_opportunity", {
        name: opportunityDetailName.value,
        data: { sales_stage: stage },
      }, "POST");
      await loadOpportunityDetail(opportunityDetailName.value);
    } catch (error) {
      frappe.msgprint(error.message || __("Không thể cập nhật giai đoạn."));
    } finally {
      opportunityDetailSaving.value = false;
    }
  }

  // "Kết thúc thắng"/"Kết thúc thất bại" collect a final amount/date + the reason(s)
  // for the outcome before saving. The reason picker (Table MultiSelect) is filtered
  // to the matching custom_reason_type on the shared "Opportunity Lost Reason" master
  // so Won and Lost each only ever see their own reason list.
  function openOpportunityClosingDialog(stage) {
    if (!opportunityDetail.value) return;
    // The Table MultiSelect control resolves its Link field via frappe.get_meta(options)
    // synchronously — if the browser has never loaded this child doctype's metadata
    // (our SPA never opens a classic Form for it), that lookup silently fails with
    // "Table MultiSelect requires a Table with atleast one Link field". Force-load it first.
    frappe.model.with_doctype("Opportunity Lost Reason Detail", () => {
      buildOpportunityClosingDialog(stage);
    });
  }

  function buildOpportunityClosingDialog(stage) {
    const doc = opportunityDetail.value.document;
    const reasonType = stage === "Kết thúc thắng" ? "Thắng" : "Thua";
    const existingReasons = (doc.lost_reasons || []).map((reason) => ({ lost_reason: reason }));
    const dialog = new frappe.ui.Dialog({
      title: __("Chi tiết kết quả"),
      fields: [
        { fieldname: "opportunity_amount", fieldtype: "Currency", label: __("Số tiền"), default: doc.opportunity_amount },
        { fieldname: "sales_stage_display", fieldtype: "Data", label: __("Giai đoạn"), default: stage, read_only: 1 },
        {
          fieldname: "expected_closing", fieldtype: "Date", label: __("Ngày kỳ vọng/kết thúc"),
          reqd: 1, default: doc.expected_closing || frappe.datetime.get_today(),
        },
        {
          fieldname: "lost_reasons", fieldtype: "Table MultiSelect", label: __("Lý do thắng/thua"),
          options: "Opportunity Lost Reason Detail", reqd: 1, default: existingReasons,
          get_query: () => ({ filters: { custom_reason_type: reasonType } }),
        },
        {
          fieldname: "custom_result_other_reason", fieldtype: "Small Text", label: __("Lý do khác"),
          default: doc.custom_result_other_reason || "",
        },
      ],
      primary_action_label: __("Lưu"),
      primary_action: async (values) => {
        try {
          await call("update_opportunity", {
            name: opportunityDetailName.value,
            data: {
              sales_stage: stage,
              opportunity_amount: values.opportunity_amount,
              expected_closing: values.expected_closing,
              lost_reasons: values.lost_reasons || [],
              custom_result_other_reason: values.custom_result_other_reason || "",
            },
          }, "POST");
          dialog.hide();
          await loadOpportunityDetail(opportunityDetailName.value);
        } catch (error) {
          frappe.msgprint(error.message || __("Không thể cập nhật kết quả cơ hội."));
        }
      },
      secondary_action_label: __("Hủy"),
    });
    dialog.show();
  }

  // Progressive pipeline coloring: stages up to & including the current one are
  // "done"/"cur" (colored), later stages are "future" (white). Win/Lose mark all done.
  const _STAGE_ORDER = [
    "Kinh doanh lập yêu cầu",
    "P.TH check thông tin",
    "Thực hiện khảo sát",
    "Kinh doanh báo giá cho KH",
  ];
  function oppStageState(label, idx) {
    const stage = opportunityDetail.value?.document?.sales_stage || "";
    let cur = _STAGE_ORDER.indexOf(stage);
    if (stage === "Kết thúc thắng" || stage === "Kết thúc thất bại") cur = _STAGE_ORDER.length;
    if (idx === cur) return "cur";
    if (cur >= 0 && idx < cur) return "done";
    return "future";
  }

  function getStageClass(stage, currentStage) {
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

  function confirmLeaveForm() {
    leaveFormConfirmOpen.value = false;
    const key = pendingNavigationView.value;
    pendingNavigationView.value = "";
    closeOpportunityForm();
    ctx.navigate(key);
  }

  function cancelLeaveForm() {
    leaveFormConfirmOpen.value = false;
    pendingNavigationView.value = "";
  }

  function toggleOpportunityFilter(field) {
    const fields = opportunityEnabledFilters.value;
    opportunityEnabledFilters.value = fields.includes(field)
      ? fields.filter((item) => item !== field)
      : [...fields, field];
    if (!opportunityEnabledFilters.value.includes(field)) {
      delete opportunityFilterValues.value[field];
      ctx.loadRows();
    }
  }

  function openOpportunityColumnDialog() {
    opportunityColumnDraft.value = [...opportunityVisibleFields.value];
    opportunityColumnSearch.value = "";
    opportunityColumnDialogOpen.value = true;
  }

  function cancelOpportunityColumnDialog() {
    opportunityColumnDialogOpen.value = false;
    opportunityColumnSearch.value = "";
    opportunityColumnDraft.value = [];
  }

  function toggleOpportunityDraftColumn(field) {
    opportunityColumnDraft.value = opportunityColumnDraft.value.includes(field)
      ? opportunityColumnDraft.value.filter((item) => item !== field)
      : [...opportunityColumnDraft.value, field];
  }

  function removeOpportunityDraftColumn(field) {
    opportunityColumnDraft.value = opportunityColumnDraft.value.filter((item) => item !== field);
  }

  function resetOpportunityDraftColumns() {
    opportunityColumnDraft.value = OPPORTUNITY_COLUMNS.map((item) => item.field);
  }

  function saveOpportunityColumns() {
    opportunityVisibleFields.value = [...opportunityColumnDraft.value];
    cancelOpportunityColumnDialog();
  }

  function importOpportunities() {
    frappe.new_doc("Data Import", { reference_doctype: "Opportunity", import_type: "Insert New Records" });
  }

  function notifyOpportunityAction(label) {
    frappe.msgprint({
      title: __(label),
      message: __("Chức năng này đang chờ cấu hình luồng xử lý/API theo spec."),
      indicator: "blue",
    });
  }

  function currentOpportunityDoc() {
    return opportunityDetail.value?.document || ctx.selected.value || null;
  }

  function requireOpportunityDoc(actionLabel = "thao tác") {
    const doc = currentOpportunityDoc();
    if (!doc?.name) {
      frappe.msgprint({
        title: __("Chưa chọn cơ hội"),
        message: __("Vui lòng chọn một cơ hội trước khi thực hiện {0}.", [actionLabel]),
        indicator: "orange",
      });
      return null;
    }
    return doc;
  }

  function closeOpportunityDetailMoreMenu() {
    opportunityDetailMoreOpen.value = false;
  }

  function toggleOpportunityDetailMoreMenu() {
    opportunityDetailMoreOpen.value = !opportunityDetailMoreOpen.value;
  }

  function openOpportunityTagDialog() {
    const doc = requireOpportunityDoc("thêm thẻ");
    if (!doc) return;
    frappe.prompt(
      [{ fieldname: "tag", fieldtype: "Data", label: __("Tên thẻ"), reqd: 1 }],
      async (values) => {
        try {
          await call("add_opportunity_tag", { name: doc.name, tag: values.tag }, "POST");
          frappe.show_alert({ message: __("Đã thêm thẻ"), indicator: "green" });
          if (opportunityDetailName.value) await loadOpportunityDetail();
        } catch (error) {
          frappe.msgprint(error.message || __("Không thể thêm thẻ."));
        }
      },
      __("Thêm thẻ"),
      __("Lưu"),
    );
  }

  function openOpportunitySummaryDialog() {
    opportunitySummaryDraft.value = [...opportunitySummaryFields.value];
    opportunitySummarySearch.value = "";
    opportunitySummaryDialogOpen.value = true;
  }

  function cancelOpportunitySummaryDialog() {
    opportunitySummaryDialogOpen.value = false;
    opportunitySummarySearch.value = "";
    opportunitySummaryDraft.value = [];
  }

  function addOpportunitySummaryField(field) {
    if (!opportunitySummaryDraft.value.includes(field)) opportunitySummaryDraft.value.push(field);
  }

  function removeOpportunitySummaryField(field) {
    opportunitySummaryDraft.value = opportunitySummaryDraft.value.filter((item) => item !== field);
  }

  function resetOpportunitySummaryFields() {
    opportunitySummaryDraft.value = [...opportunitySummaryDefaultFields];
  }

  function saveOpportunitySummaryFields() {
    opportunitySummaryFields.value = opportunitySummaryDraft.value.length
      ? [...opportunitySummaryDraft.value]
      : [...opportunitySummaryDefaultFields];
    window.localStorage.setItem(
      "dcnet-crm-opportunity-summary-fields",
      JSON.stringify(opportunitySummaryFields.value),
    );
    opportunitySummaryDialogOpen.value = false;
    frappe.show_alert({ message: __("Đã cập nhật tóm tắt"), indicator: "green" });
  }

  function callOpportunityPhone() {
    const doc = requireOpportunityDoc("gọi điện");
    if (!doc) return;
    const phone = doc.contact_mobile || doc.mobile_no || doc.phone || "";
    if (!phone) {
      frappe.msgprint({ title: __("Gọi điện"), message: __("Cơ hội này chưa có số điện thoại liên hệ."), indicator: "orange" });
      return;
    }
    window.location.href = `tel:${String(phone).replace(/\s+/g, "")}`;
  }

  function emailOpportunity() {
    const doc = requireOpportunityDoc("gửi email");
    if (!doc) return;
    const email = doc.contact_email || doc.email_id || "";
    if (!email) {
      frappe.msgprint({ title: __("Gửi email"), message: __("Cơ hội này chưa có email liên hệ."), indicator: "orange" });
      return;
    }
    window.location.href = `mailto:${email}?subject=${encodeURIComponent(doc.title || doc.name)}`;
  }

  function createOpportunityActivity(kind = "Nhiệm vụ") {
    const doc = requireOpportunityDoc(`thêm ${kind}`);
    if (!doc) return;
    opportunityDetailTab.value = "activities";
    if (kind === "Lịch hẹn" || kind === "Cuộc gọi") {
      frappe.new_doc("Event", {
        subject: `${kind} - ${doc.title || doc.name}`,
        event_category: kind === "Cuộc gọi" ? "Call" : "Event",
        starts_on: new Date().toISOString().slice(0, 16).replace("T", " "),
      });
      return;
    }
    createOpportunityTask();
  }

  function createOpportunityTask() {
    const doc = requireOpportunityDoc("tạo công việc");
    if (!doc) return;
    frappe.new_doc("ToDo", {
      reference_type: "Opportunity",
      reference_name: doc.name,
      description: `Theo dõi cơ hội ${doc.title || doc.name}`,
    });
  }

  function analyzeOpportunityWithAi() {
    const doc = requireOpportunityDoc("phân tích");
    if (!doc) return;
    const items = opportunityDetail.value?.items?.length || 0;
    const activities = opportunityDetail.value?.activities?.length || 0;
    const comments = opportunityDetail.value?.comments?.length || 0;
    const amount = formatMoney(doc.opportunity_amount);
    const expected = formatMoney((doc.opportunity_amount || 0) * (doc.probability || 0) / 100);
    frappe.msgprint({
      title: __("Phân tích cơ hội"),
      message: `
        <div style="line-height:1.8">
          <b>${doc.title || doc.name}</b><br>
          Giai đoạn: ${doc.sales_stage || "—"}<br>
          Giá trị: ${amount}; xác suất: ${doc.probability || 0}%; doanh số kỳ vọng: ${expected}.<br>
          Hàng hóa: ${items}; hoạt động: ${activities}; trao đổi: ${comments}.<br>
          Gợi ý: kiểm tra hàng hóa, cập nhật lịch hẹn tiếp theo và gửi phê duyệt khi thông tin đã đủ.
        </div>
      `,
      indicator: "blue",
    });
  }

  function copyOpportunityLink(label = "Đã sao chép liên kết cơ hội") {
    const text = window.location.href;
    if (navigator.clipboard?.writeText) {
      navigator.clipboard.writeText(text).then(() => {
        frappe.show_alert({ message: __(label), indicator: "green" });
      }).catch(() => {
        window.prompt(__("Sao chép liên kết"), text);
      });
      return;
    }
    window.prompt(__("Sao chép liên kết"), text);
  }

  function requestOpportunityApproval() {
    const doc = requireOpportunityDoc("gửi phê duyệt");
    if (!doc) return;
    frappe.confirm(__("Gửi cơ hội {0} vào luồng phê duyệt?", [doc.name]), async () => {
      try {
        await call("request_opportunity_approval", { name: doc.name }, "POST");
        frappe.show_alert({ message: __("Đã gửi phê duyệt"), indicator: "green" });
        await loadOpportunityDetail(doc.name);
      } catch (error) {
        frappe.msgprint(error.message || __("Không thể gửi phê duyệt."));
      }
    });
  }

  function openOpportunityHandoffDialog() {
    const doc = requireOpportunityDoc("bàn giao công việc");
    if (!doc) return;
    const dialog = new frappe.ui.Dialog({
      title: __("Bàn giao công việc"),
      fields: [
        { fieldname: "assigned_to", fieldtype: "Link", options: "User", label: __("Người nhận"), reqd: 1 },
        { fieldname: "due_date", fieldtype: "Date", label: __("Hạn hoàn thành") },
        {
          fieldname: "description",
          fieldtype: "Small Text",
          label: __("Nội dung"),
          default: `Bàn giao theo dõi cơ hội ${doc.title || doc.name}`,
        },
      ],
      primary_action_label: __("Bàn giao"),
      async primary_action(values) {
        try {
          await call("create_opportunity_handoff", { name: doc.name, ...values }, "POST");
          dialog.hide();
          frappe.show_alert({ message: __("Đã tạo công việc bàn giao"), indicator: "green" });
          await loadOpportunityDetail(doc.name);
        } catch (error) {
          frappe.msgprint(error.message || __("Không thể bàn giao công việc."));
        }
      },
    });
    dialog.show();
  }

  async function createOpportunityPurchaseRequest() {
    const doc = requireOpportunityDoc("yêu cầu mua hàng");
    if (!doc) return;
    try {
      const result = await call("create_purchase_request_from_opportunity", { name: doc.name }, "POST");
      frappe.show_alert({ message: __("Đã tạo yêu cầu mua hàng {0}", [result.name]), indicator: "green" });
      frappe.set_route("Form", "Purchase Request", result.name);
    } catch (error) {
      frappe.msgprint(error.message || __("Không thể tạo yêu cầu mua hàng."));
    }
  }

  async function createOpportunityCareCard() {
    const doc = requireOpportunityDoc("sinh thẻ tư vấn");
    if (!doc) return;
    try {
      const result = await call("create_care_card_from_opportunity", { name: doc.name }, "POST");
      frappe.show_alert({ message: __("Đã tạo thẻ tư vấn {0}", [result.name]), indicator: "green" });
      frappe.set_route("Form", "CRM Care Card", result.name);
    } catch (error) {
      frappe.msgprint(error.message || __("Không thể tạo thẻ tư vấn."));
    }
  }

  async function cloneOpportunityFromDetail() {
    const doc = requireOpportunityDoc("nhân bản");
    if (!doc) return;
    await openOpportunityForm(doc.party_name, doc.customer_name || doc.party_name);
    opportunityForm.value = {
      ...opportunityForm.value,
      contact_person: doc.contact_person || "",
      title: `${doc.title || doc.name} - Bản sao`,
      opportunity_type: doc.opportunity_type || "",
      probability: doc.probability || 10,
      sales_stage: doc.sales_stage || opportunityForm.value.sales_stage,
      expected_closing: doc.expected_closing || opportunityForm.value.expected_closing,
      territory: doc.territory || "",
      company: doc.company || opportunityForm.value.company,
      notes: doc.notes || "",
      custom_is_shared: doc.custom_is_shared || 0,
      custom_referral_partner: doc.custom_referral_partner || "",
      items: (opportunityDetail.value?.items || []).map((item) => ({
        ...emptyOpportunityItem(),
        item_code: item.item_code || "",
        item_name: item.item_name || "",
        description: item.description || "",
        qty: item.qty || 1,
        uom: item.uom || "",
        rate: item.rate || 0,
        custom_discount_percentage: item.custom_discount_percentage || 0,
        custom_discount_amount: item.custom_discount_amount || 0,
        custom_net_rate: item.custom_net_rate || 0,
        custom_net_amount: item.custom_net_amount || 0,
      })),
    };
  }

  function deleteOpportunityFromDetail() {
    const doc = requireOpportunityDoc("xóa");
    if (!doc) return;
    frappe.confirm(__("Xóa cơ hội {0}? Thao tác này không thể hoàn tác.", [doc.name]), async () => {
      try {
        await frappe.call({ method: "frappe.client.delete", args: { doctype: "Opportunity", name: doc.name }, type: "POST" });
        frappe.show_alert({ message: __("Đã xóa cơ hội"), indicator: "green" });
        backToOpportunities();
        await ctx.loadRows();
      } catch (error) {
        frappe.msgprint(error.message || __("Không thể xóa cơ hội."));
      }
    });
  }

  function handleOpportunityDetailMoreAction(key) {
    closeOpportunityDetailMoreMenu();
    const doc = requireOpportunityDoc("mở menu");
    if (!doc) return;
    const actions = {
      handoff: openOpportunityHandoffDialog,
      approval: requestOpportunityApproval,
      "purchase-request": createOpportunityPurchaseRequest,
      "care-card": createOpportunityCareCard,
      "amis-chat": () => copyOpportunityLink("Đã sao chép liên kết để gửi qua chat"),
      summary: openOpportunitySummaryDialog,
      history: () => ctx.openAuditLog("Opportunity", doc.name),
      print: () => frappe.set_route("print", "Opportunity", doc.name),
      clone: cloneOpportunityFromDetail,
      share: () => copyOpportunityLink("Đã sao chép liên kết chia sẻ"),
      delete: deleteOpportunityFromDetail,
      "back-view": backToOpportunities,
    };
    actions[key]?.();
  }

  return {
    opportunityActivityOpen, opportunityFilterOpen, opportunityTab,
    opportunityPanelScope, opportunityCustomerDetail, opportunityCustomerLoading,
    opportunityLinkedCustomerName, opportunityPanelDetail, opportunityPanelActivities,
    opportunityPanelPurchases, opportunityPanelContacts, opportunityPanelItems,
    setOpportunityPanelScope,
    opportunityVisibleFields, opportunityEnabledFilters, opportunityFilterValues,
    opportunityColumnDialogOpen, opportunityColumnSearch, opportunityColumnDraft,
    opportunityFormOpen, opportunitySaving, leaveFormConfirmOpen, pendingNavigationView,
    itemPickerOpen, itemPickerSearch, itemPickerPage, itemPickerPageLength,
    itemPickerSelected, itemPickerCategoryFilter, opportunityFormOptions, opportunityForm,
    opportunityDetailName, opportunityDetail, opportunityDetailTab, opportunitySalesSection,
    opportunityNotesSection, opportunityNotesCollapsed,
    opportunityDetailEditing, opportunityDetailSaving, opportunityDetailForm, opportunityDetailComment,
    opportunityAttachmentUploading, opportunityDetailTabs,
    opportunityDetailFieldSearch, opportunityDetailShowEmpty, showOpportunityDetailField,
    oppActivityPanelTab, opportunityDetailMoreOpen, opportunityDetailMoreActions,
    opportunitySummaryRows, opportunitySalesMenu, opportunitySalesCount,
    opportunitySummaryDialogOpen, opportunitySummarySearch, opportunitySummaryDraft,
    availableOpportunitySummaryFields, selectedOpportunitySummaryFields,
    opportunityFormDirty, itemPickerFiltered, itemPickerPageCount, itemPickerRows, itemPickerCategories,
    loadOpportunityDetail, openOpportunityDetail, backToOpportunities,
    calcItemDiscount, openOpportunityForm, closeOpportunityForm,
    addOpportunityItem, clearOpportunityItems, removeOpportunityItem,
    openItemPicker, closeItemPicker, toggleItemPickerRow, confirmItemPicker, selectOpportunityItem,
    saveOpportunity, saveOpportunityDetailComment, saveOpportunityDetailEdit, uploadOpportunityAttachment,
    addOpportunityAttachmentLink,
    setOpportunityStage, openOpportunityClosingDialog, getStageClass, oppStageState,
    confirmLeaveForm, cancelLeaveForm,
    toggleOpportunityFilter,
    openOpportunityColumnDialog, cancelOpportunityColumnDialog, toggleOpportunityDraftColumn,
    removeOpportunityDraftColumn, resetOpportunityDraftColumns, saveOpportunityColumns,
    importOpportunities, notifyOpportunityAction, callOpportunityPhone, emailOpportunity,
    createOpportunityActivity, createOpportunityTask, opportunityMoreOpen,
    closeOpportunityDetailMoreMenu, toggleOpportunityDetailMoreMenu,
    handleOpportunityDetailMoreAction, openOpportunityTagDialog,
    openOpportunitySummaryDialog, cancelOpportunitySummaryDialog, addOpportunitySummaryField,
    removeOpportunitySummaryField, resetOpportunitySummaryFields, saveOpportunitySummaryFields,
    analyzeOpportunityWithAi,
    createOpportunityPurchaseRequest, exportResource,
  };
}
