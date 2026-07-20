import { ref, computed, watch } from "vue/dist/vue.esm-bundler.js";
import { call } from "../../utils.js";
import { QUOTATION_COLUMNS } from "../../constants.js";

const QT_COLUMN_SETTINGS_KEY = "dcnet_crm_columns";

export function useQuotations(ctx) {
  // ── List view column customization ──────────────────────────
  const quotationVisibleFields = ref(QUOTATION_COLUMNS.filter((item) => item.default).map((item) => item.field));
  const quotationColumnDialogOpen = ref(false);
  const quotationColumnSearch = ref("");
  const quotationColumnDraft = ref([]);

  // Column choice is remembered per user (Frappe's built-in "User Settings",
  // same mechanism Desk list views use), not just per browser/localStorage.
  async function loadQuotationColumnSettings() {
    try {
      const settings = await frappe.model.user_settings.get("Quotation");
      const saved = settings?.[QT_COLUMN_SETTINGS_KEY];
      if (Array.isArray(saved) && saved.length) {
        const valid = new Set(QUOTATION_COLUMNS.map((item) => item.field));
        const filtered = saved.filter((field) => valid.has(field));
        if (filtered.length) quotationVisibleFields.value = filtered;
      }
    } catch {
      // Keep the defaults if settings can't be loaded.
    }
  }
  loadQuotationColumnSettings();

  function openQuotationColumnDialog() {
    quotationColumnDraft.value = [...quotationVisibleFields.value];
    quotationColumnSearch.value = "";
    quotationColumnDialogOpen.value = true;
  }

  function cancelQuotationColumnDialog() {
    quotationColumnDialogOpen.value = false;
    quotationColumnSearch.value = "";
    quotationColumnDraft.value = [];
  }

  function toggleQuotationDraftColumn(field) {
    quotationColumnDraft.value = quotationColumnDraft.value.includes(field)
      ? quotationColumnDraft.value.filter((item) => item !== field)
      : [...quotationColumnDraft.value, field];
  }

  function removeQuotationDraftColumn(field) {
    quotationColumnDraft.value = quotationColumnDraft.value.filter((item) => item !== field);
  }

  function resetQuotationDraftColumns() {
    quotationColumnDraft.value = QUOTATION_COLUMNS.filter((item) => item.default).map((item) => item.field);
  }

  function saveQuotationColumns() {
    quotationVisibleFields.value = [...quotationColumnDraft.value];
    frappe.model.user_settings.save("Quotation", QT_COLUMN_SETTINGS_KEY, quotationVisibleFields.value);
    cancelQuotationColumnDialog();
  }

  // ── Drag-to-resize table columns ────────────────────────────
  const quotationColumnWidths = ref({});

  function startQuotationColumnResize(event, field, defaultWidth) {
    event.preventDefault();
    const startX = event.clientX;
    const startWidth = parseInt(quotationColumnWidths.value[field] || defaultWidth || "150px", 10) || 150;

    function onMove(moveEvent) {
      const next = Math.max(60, startWidth + (moveEvent.clientX - startX));
      quotationColumnWidths.value = { ...quotationColumnWidths.value, [field]: `${next}px` };
    }
    function onUp() {
      document.removeEventListener("mousemove", onMove);
      document.removeEventListener("mouseup", onUp);
    }
    document.addEventListener("mousemove", onMove);
    document.addEventListener("mouseup", onUp);
  }

  // ── Full CRM Quotation detail page ──────────────────────────
  const quotationDetailName = ref("");
  const quotationDetail = ref(null);
  const quotationDetailLoading = ref(false);
  const quotationDetailTab = ref("info");
  const quotationDetailFieldSearch = ref("");
  const quotationDetailShowEmpty = ref(true);
  const quotationNoteText = ref("");
  const quotationNoteSaving = ref(false);
  const quotationAttachmentUploading = ref(false);

  async function loadQuotationDetailPage(name) {
    const target = name !== undefined ? name : quotationDetailName.value;
    if (!target) return ctx.navigate("quotations");
    quotationDetailLoading.value = true;
    quotationDetail.value = null;
    try {
      quotationDetail.value = await call("get_quotation_detail", { name: target });
      quotationDetailName.value = target;
    } catch (error) {
      frappe.msgprint(error.message || "Không thể tải chi tiết báo giá.");
    } finally {
      quotationDetailLoading.value = false;
    }
  }

  function openQuotationDetail(row) {
    if (!row?.name) return;
    quotationDetailName.value = row.name;
    quotationDetailTab.value = "info";
    ctx.route.value = "quotation-detail";
    frappe.route_options = { view: "quotation-detail", quotation: row.name };
    const url = new URL(window.location.href);
    url.hash = "";
    url.searchParams.set("view", "quotation-detail");
    url.searchParams.set("quotation", row.name);
    url.searchParams.delete("customer");
    url.searchParams.delete("opportunity");
    url.searchParams.delete("order");
    window.history.replaceState(window.history.state, "", url);
    window.sessionStorage.setItem("dcnet-crm-view", "quotation-detail");
    window.setTimeout(() => {
      document.querySelectorAll(".body-sidebar .standard-sidebar-item").forEach((item) => {
        item.classList.remove("active-sidebar");
      });
      const container = [...document.querySelectorAll(".body-sidebar .sidebar-item-container")]
        .find((item) => item.getAttribute("item-name") === "Báo giá");
      container?.querySelector(".standard-sidebar-item")?.classList.add("active-sidebar");
    }, 50);
    loadQuotationDetailPage(row.name);
  }

  function backToQuotationList() {
    ctx.navigate("quotations");
  }

  function quotationDetailTabCount(tab) {
    const detail = quotationDetail.value || {};
    if (tab === "items") return detail.items?.length || 0;
    if (tab === "notes") return detail.comments?.length || 0;
    if (tab === "attachments") return detail.attachments?.length || 0;
    if (tab === "orders") return detail.orders?.length || 0;
    if (tab === "activities") return detail.activities?.filter((row) => row.status !== "Closed").length || 0;
    if (tab === "completed") return detail.activities?.filter((row) => row.status === "Closed").length || 0;
    return 0;
  }

  function quotationDetailTotal(field) {
    return (quotationDetail.value?.items || []).reduce(
      (total, item) => total + (parseFloat(item[field]) || 0),
      0,
    );
  }

  function showQuotationDetailField(label, value) {
    const keyword = quotationDetailFieldSearch.value.trim().toLocaleLowerCase("vi");
    if (keyword && !String(label || "").toLocaleLowerCase("vi").includes(keyword)) return false;
    return quotationDetailShowEmpty.value || (value !== null && value !== undefined && value !== "");
  }

  function notifyQuotationDetailAction(label) {
    frappe.show_alert({ message: `${label} đang chờ cấu hình luồng xử lý.`, indicator: "blue" }, 4);
  }

  function openQuotationTagDialog() {
    const name = quotationDetailName.value;
    if (!name) return;
    frappe.prompt(
      [{ fieldname: "tag", fieldtype: "Data", label: __("Tên thẻ"), reqd: 1 }],
      async (values) => {
        try {
          await call("add_quotation_tag", { name, tag: values.tag }, "POST");
          frappe.show_alert({ message: __("Đã thêm thẻ"), indicator: "green" });
        } catch (error) {
          frappe.msgprint(error.message || __("Không thể thêm thẻ."));
        }
      },
      __("Thêm thẻ"),
      __("Lưu"),
    );
  }

  const qtStockDialogOpen = ref(false);
  const qtStockRows = ref([]);
  const qtStockLoading = ref(false);
  const qtStockPage = ref(1);
  const qtStockPageLength = ref(10);

  async function openQuotationStockLookup() {
    const name = quotationDetailName.value;
    if (!name) return;
    qtStockDialogOpen.value = true;
    qtStockPage.value = 1;
    qtStockLoading.value = true;
    try {
      qtStockRows.value = await call("get_quotation_stock_levels", { name });
    } catch (error) {
      frappe.msgprint(error.message || "Không thể tra cứu số lượng tồn.");
      qtStockRows.value = [];
    } finally {
      qtStockLoading.value = false;
    }
  }

  async function toggleQuotationApprovalRequest() {
    if (!quotationDetail.value || !quotationDetailName.value) return;
    const requested = quotationDetail.value.document.custom_approval_requested ? 0 : 1;
    try {
      await call("set_quotation_approval_requested", {
        name: quotationDetailName.value,
        requested,
      }, "POST");
      await loadQuotationDetailPage();
      frappe.show_alert({
        message: requested ? "Đã gửi yêu cầu duyệt" : "Đã thu hồi yêu cầu duyệt",
        indicator: "green",
      }, 3);
    } catch (error) {
      frappe.msgprint(error.message || "Không thể cập nhật yêu cầu duyệt.");
    }
  }

  async function saveQuotationNote() {
    const content = quotationNoteText.value.trim();
    if (!content || quotationNoteSaving.value || !quotationDetailName.value) return;
    quotationNoteSaving.value = true;
    try {
      await call("add_note", {
        resource: "quotations",
        name: quotationDetailName.value,
        content,
      }, "POST");
      quotationNoteText.value = "";
      await loadQuotationDetailPage();
      frappe.show_alert({ message: "Đã thêm nội dung", indicator: "green" }, 3);
    } catch (error) {
      frappe.msgprint(error.message || "Không thể thêm nội dung.");
    } finally {
      quotationNoteSaving.value = false;
    }
  }

  async function uploadQuotationAttachment(event) {
    const file = event?.target?.files?.[0];
    if (event?.target) event.target.value = "";
    if (!file || !quotationDetailName.value || quotationAttachmentUploading.value) return;
    quotationAttachmentUploading.value = true;
    try {
      const formData = new FormData();
      formData.append("file", file, file.name);
      formData.append("is_private", 1);
      formData.append("doctype", "Quotation");
      formData.append("docname", quotationDetailName.value);
      const response = await window.fetch("/api/method/upload_file", {
        method: "POST",
        headers: { "X-Frappe-CSRF-Token": frappe.csrf_token },
        body: formData,
      });
      if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        throw new Error(data?._server_messages || data?.exception || "Tải tệp thất bại");
      }
      await loadQuotationDetailPage();
      frappe.show_alert({ message: "Đã đính kèm tệp", indicator: "green" }, 3);
    } catch (error) {
      frappe.msgprint(error.message || "Không thể đính kèm tệp.");
    } finally {
      quotationAttachmentUploading.value = false;
    }
  }

  function createOrderFromQuotation() {
    const detail = quotationDetail.value;
    if (!detail?.can_create_order || detail.document?.quotation_to !== "Customer") return;
    ctx.createSalesOrder(
      detail.document.party_name,
      detail.document.customer_name || detail.document.party_name,
      detail.document.opportunity || "",
      detail,
    );
  }

  function createQuotationActivity() {
    if (!quotationDetail.value?.can_create_activity) return;
    frappe.prompt([
      { fieldname: "description", label: "Nội dung công việc", fieldtype: "Data", reqd: 1 },
      { fieldname: "date", label: "Hạn hoàn thành", fieldtype: "Date", default: frappe.datetime.get_today() },
      {
        fieldname: "priority",
        label: "Mức độ ưu tiên",
        fieldtype: "Select",
        options: "Low\nMedium\nHigh\nUrgent",
        default: "Medium",
      },
    ], async (values) => {
      try {
        await call("create_quotation_activity", {
          name: quotationDetailName.value,
          activity: values,
        }, "POST");
        quotationDetailTab.value = "activities";
        await loadQuotationDetailPage();
        frappe.show_alert({ message: "Đã tạo công việc", indicator: "green" }, 3);
      } catch (error) {
        frappe.msgprint(error.message || "Không thể tạo công việc.");
      }
    }, "Thêm công việc", "Tạo");
  }

  function openQuotationActivity(row) {
    if (row?.name) ctx.openActivityRecord(row.name);
  }

  // ── Quotation list detail panel (Hàng hóa) ──────────────────
  const qtDetailItems = ref([]);
  const qtDetailLoading = ref(false);
  const qtExpandedItem = ref(-1);
  const qtItemsSearchOpen = ref(false);
  const qtItemsSearch = ref("");

  const qtDetailItemsFiltered = computed(() => {
    const keyword = qtItemsSearch.value.trim().toLocaleLowerCase("vi");
    if (!keyword) return qtDetailItems.value;
    return qtDetailItems.value.filter((item) => (
      String(item.item_code || "").toLocaleLowerCase("vi").includes(keyword)
      || String(item.item_name || "").toLocaleLowerCase("vi").includes(keyword)
    ));
  });

  function toggleQuotationDetailItem(idx) {
    qtExpandedItem.value = qtExpandedItem.value === idx ? -1 : idx;
  }

  function toggleQuotationItemsSearch() {
    qtItemsSearchOpen.value = !qtItemsSearchOpen.value;
    if (!qtItemsSearchOpen.value) qtItemsSearch.value = "";
  }

  async function loadQuotationDetail(name) {
    qtExpandedItem.value = -1;
    if (!name) { qtDetailItems.value = []; return; }
    qtDetailLoading.value = true;
    try {
      const items = await call("get_quotation_items", { name });
      qtDetailItems.value = items || [];
    } catch {
      qtDetailItems.value = [];
    } finally {
      qtDetailLoading.value = false;
    }
  }

  // Auto-select the first row on the Quotation list so the "Hàng hóa" preview
  // panel has something to show as soon as the list loads, matching the
  // reference UI where an item is always visible without an explicit click.
  watch(ctx.rows, (rows) => {
    if (ctx.route.value !== "quotations") return;
    if (!rows.length) return;
    if (ctx.selected.value) return;
    ctx.selected.value = rows[0];
    loadQuotationDetail(rows[0].name);
  });

  function quotationStatusClass(status) {
    const map = {
      Draft: "draft", Open: "open", Ordered: "ordered",
      Expired: "expired", Lost: "lost", Cancelled: "cancelled",
    };
    return map[status] || "draft";
  }

  function importQuotations() {
    frappe.new_doc("Data Import", { reference_doctype: "Quotation", import_type: "Insert New Records" });
  }

  // ── Quotation list filter state ─────────────────────────────
  const qtFilterOpen = ref(true);
  const qtItemsPanelOpen = ref(true);
  const qtQuickStatsOpen = ref(false);
  const qtQuickStats = ref(null);
  const qtQuickStatsLoading = ref(false);

  async function toggleQuotationQuickStats() {
    qtQuickStatsOpen.value = !qtQuickStatsOpen.value;
    if (!qtQuickStatsOpen.value) return;
    qtFilterOpen.value = false;
    if (qtQuickStats.value) return;
    qtQuickStatsLoading.value = true;
    try {
      qtQuickStats.value = await call("get_quotation_quick_stats");
    } catch (error) {
      frappe.msgprint(error.message || "Không thể tải thống kê.");
    } finally {
      qtQuickStatsLoading.value = false;
    }
  }
  const qtSavedFilterActive = ref("");
  const quotationsEnabledFilters = ref([]);
  const qtShowMoreFilters = ref(false);
  const qtFilterCriteriaSearch = ref("");
  const quotationsFilterValues = ref({});
  const qtSortField = ref("");
  const qtSortDirection = ref("desc");

  function toggleQuotationSort(field) {
    if (qtSortField.value !== field) {
      qtSortField.value = field;
      qtSortDirection.value = "desc";
    } else {
      qtSortDirection.value = qtSortDirection.value === "desc" ? "asc" : "desc";
    }
    ctx.loadRows();
  }

  const QT_SAVED_FILTERS = [
    { key: "quote_month", label: "Báo giá tháng này" },
    { key: "quote_week", label: "Báo giá tuần này" },
    { key: "valid_active", label: "Còn hiệu lực" },
  ];

  const QT_FILTER_CRITERIA = [
    { key: "tag", field: "status", label: "Thẻ" },
    { key: "name", field: "name", label: "Số báo giá" },
    { key: "transaction_date", field: "transaction_date", label: "Ngày báo giá" },
    { key: "valid_till", field: "valid_till", label: "Hiệu lực đến ngày" },
    { key: "customer_name", field: "customer_name", label: "Khách hàng" },
    { key: "contact_display", field: "contact_display", label: "Liên hệ" },
    { key: "grand_total", field: "grand_total", label: "Tổng tiền" },
    { key: "status", field: "status", label: "Tình trạng" },
    { key: "terms", field: "terms", label: "Mô tả" },
  ];

  // Extra criteria only revealed behind "Xem thêm" in the filter panel.
  const QT_FILTER_CRITERIA_MORE = [
    { key: "net_total", field: "net_total", label: "Thành tiền" },
    { key: "total_taxes_and_charges", field: "total_taxes_and_charges", label: "Tiền thuế" },
    { key: "discount_amount", field: "discount_amount", label: "Tiền chiết khấu" },
    { key: "company", field: "company", label: "Đơn vị" },
    { key: "owner", field: "owner", label: "Người tạo" },
    { key: "modified", field: "modified", label: "Cập nhật cuối" },
  ];

  const qtSavedFilterDates = computed(() => {
    const key = qtSavedFilterActive.value;
    if (!key) return {};
    const now = new Date();
    const y = now.getFullYear();
    const m = String(now.getMonth() + 1).padStart(2, "0");
    const dow = now.getDay();
    const monday = new Date(now);
    monday.setDate(now.getDate() - ((dow + 6) % 7));
    const mondayStr = monday.toISOString().split("T")[0];
    const todayStr = now.toISOString().split("T")[0];
    const monthStart = `${y}-${m}-01`;
    if (key === "quote_month") return { transaction_date: [">=", monthStart] };
    if (key === "quote_week") return { transaction_date: [">=", mondayStr] };
    if (key === "valid_active") return { valid_till: [">=", todayStr] };
    return {};
  });

  function activateQuotationSavedFilter(key) {
    qtSavedFilterActive.value = qtSavedFilterActive.value === key ? "" : key;
    ctx.loadRows();
  }

  function toggleQuotationsFilter(field) {
    const idx = quotationsEnabledFilters.value.indexOf(field);
    if (idx >= 0) {
      quotationsEnabledFilters.value.splice(idx, 1);
      const vals = { ...quotationsFilterValues.value };
      delete vals[field];
      quotationsFilterValues.value = vals;
    } else {
      quotationsEnabledFilters.value.push(field);
    }
    ctx.loadRows();
  }

  // ── Item picker for Báo giá ──────────────────────────────────
  const qtItemPickerOpen = ref(false);
  const qtItemPickerSearch = ref("");
  const qtItemPickerPage = ref(1);
  const qtItemPickerPageLength = ref(20);
  const qtItemPickerSelected = ref([]);
  const qtItemPickerCategoryFilter = ref("");

  const qtItemPickerFiltered = computed(() => {
    let list = qtItemList.value;
    const cat = qtItemPickerCategoryFilter.value;
    if (cat) list = list.filter((i) => i.item_group === cat);
    const kw = qtItemPickerSearch.value.trim().toLowerCase();
    if (kw) list = list.filter((i) =>
      (i.name || "").toLowerCase().includes(kw) ||
      (i.item_name || "").toLowerCase().includes(kw)
    );
    return list;
  });
  const qtItemPickerPageCount = computed(() =>
    Math.max(Math.ceil(qtItemPickerFiltered.value.length / qtItemPickerPageLength.value), 1)
  );
  const qtItemPickerRows = computed(() => {
    const start = (qtItemPickerPage.value - 1) * qtItemPickerPageLength.value;
    return qtItemPickerFiltered.value.slice(start, start + qtItemPickerPageLength.value);
  });
  const qtItemPickerCategories = computed(() => {
    const cats = new Set(qtItemList.value.map((i) => i.item_group).filter(Boolean));
    return [...cats].sort();
  });

  async function openQTItemPicker() {
    if (!qtItemList.value.length) {
      if (qtFormOptions.value.items?.length) {
        qtItemList.value = qtFormOptions.value.items;
      } else {
        try {
          const opts = await call("get_quotation_form_options", { customer: createQTContext.value.customer || "" });
          qtFormOptions.value = opts;
          qtItemList.value = opts.items || [];
        } catch {}
      }
    }
    qtItemPickerSearch.value = "";
    qtItemPickerPage.value = 1;
    qtItemPickerSelected.value = [];
    qtItemPickerCategoryFilter.value = "";
    qtItemPickerOpen.value = true;
  }

  function closeQTItemPicker() {
    qtItemPickerOpen.value = false;
    qtItemPickerSelected.value = [];
  }

  function toggleQTItemPickerRow(name) {
    const idx = qtItemPickerSelected.value.indexOf(name);
    if (idx >= 0) qtItemPickerSelected.value.splice(idx, 1);
    else qtItemPickerSelected.value.push(name);
  }

  function confirmQTItemPicker() {
    const toAdd = qtItemPickerSelected.value
      .map((name) => qtItemList.value.find((i) => i.name === name))
      .filter(Boolean);
    // Remove empty placeholder rows
    createQTItems.value = createQTItems.value.filter((i) => i.item_code || i.item_name);
    for (const item of toAdd) {
      const existing = createQTItems.value.find((r) => r.item_code === item.name);
      if (existing && qtAutoIncreaseQty.value) {
        existing.qty = (parseFloat(existing.qty) || 0) + 1;
        updateQTItemAmount(existing);
      } else if (!existing) {
        const row = _qtBlankItem();
        row.item_code = item.name;
        row.item_name = item.item_name || item.name;
        row.uom = item.stock_uom || "Cái";
        createQTItems.value.push(row);
      }
    }
    closeQTItemPicker();
  }

  // ── Internal "Thêm Báo giá" form (create-quotation) ─────────
  const createQTSaving = ref(false);
  const createQTContext = ref({ customer: "", customerName: "", opportunity: "" });
  const createQTForm = ref({});
  const createQTItems = ref([]);
  const qtFormOptions = ref({
    items: [], customers: [], opportunities: [], contacts: [],
    price_lists: [], payment_terms: [], territories: [],
    campaigns: [], taxes_templates: [],
  });

  // Reload contacts/opportunities + fill tax id when the customer is picked
  function onQTCustomerChange(val) {
    createQTForm.value.contact_person = "";
    createQTForm.value.opportunity = "";
    const cust = (qtFormOptions.value.customers || []).find((c) => c.name === val);
    createQTForm.value.tax_id = cust && cust.tax_id ? cust.tax_id : "";
    if (!val) return;
    call("get_quotation_form_options", { customer: val })
      .then((opts) => { qtFormOptions.value = opts; qtItemList.value = opts.items || []; })
      .catch(() => {});
  }
  const qtItemList = ref([]);
  const qtCurrentUser = ref(
    (typeof frappe !== "undefined" && frappe.session && (frappe.session.user_fullname || frappe.session.user)) || ""
  );
  const qtAutoIncreaseQty = ref(false);

  function _qtBlankItem() {
    return {
      item_code: "", item_name: "", description: "",
      a_end: "", z_end: "", account_id: "",
      uom: "Cái", qty: 1,
      price_list_rate: 0, discount_percentage: 0, rate: 0, amount: 0,
      tax_rate: 0,
    };
  }

  function openCreateQuotation(customer, custDisplayName, opportunity) {
    if (customer === undefined) customer = "";
    if (custDisplayName === undefined) custDisplayName = "";
    if (opportunity === undefined) opportunity = "";
    const today = new Date().toISOString().split("T")[0];
    createQTContext.value = { customer, customerName: custDisplayName, opportunity };

    call("get_quotation_form_options", { customer: customer || "" })
      .then((opts) => { qtFormOptions.value = opts; qtItemList.value = opts.items || []; })
      .catch(() => {});

    createQTForm.value = {
      customer,
      contact_person: "",
      opportunity,
      order_type: "Sales",
      transaction_date: today,
      valid_till: "",
      status: "Draft",
      installation_zone: "Nam",
      payment_terms_template: "",
      tax_id: "",
      email_id: "",
      note: "",
      implementation_time: "",
      sla: "",
      selling_price_list: "",
      currency: "VND",
      taxes_and_charges: "",
      territory: "",
      campaign: "",
      title: "",
      company: (frappe.defaults && frappe.defaults.get_user_default && frappe.defaults.get_user_default("Company")) || "",
      shared_flag: false,
    };
    createQTItems.value = [];
    ctx.route.value = "create-quotation";
    const url = new URL(window.location.href);
    url.hash = "";
    url.searchParams.set("view", "create-quotation");
    if (customer) url.searchParams.set("customer", customer);
    else url.searchParams.delete("customer");
    url.searchParams.delete("opportunity");
    window.history.replaceState(window.history.state, "", url);
    window.sessionStorage.setItem("dcnet-crm-view", "create-quotation");
    window.setTimeout(() => {
      document.querySelectorAll(".body-sidebar .standard-sidebar-item").forEach((item) => {
        item.classList.remove("active-sidebar");
      });
      const container = [...document.querySelectorAll(".body-sidebar .sidebar-item-container")]
        .find((item) => item.getAttribute("item-name") === "Báo giá");
      container?.querySelector(".standard-sidebar-item")?.classList.add("active-sidebar");
    }, 50);
  }

  function backToQuotations() {
    if (createQTContext.value.customer) {
      ctx.customerName.value = createQTContext.value.customer;
      ctx.route.value = "customer-detail";
    } else {
      ctx.route.value = "quotations";
    }
    const url = new URL(window.location.href);
    url.hash = "";
    const view = createQTContext.value.customer ? "customer-detail" : "quotations";
    url.searchParams.set("view", view);
    if (createQTContext.value.customer) url.searchParams.set("customer", createQTContext.value.customer);
    else url.searchParams.delete("customer");
    url.searchParams.delete("opportunity");
    window.history.replaceState(window.history.state, "", url);
    window.sessionStorage.setItem("dcnet-crm-view", view);
    window.setTimeout(() => {
      document.querySelectorAll(".body-sidebar .standard-sidebar-item").forEach((item) => {
        item.classList.remove("active-sidebar");
      });
      const label = createQTContext.value.customer ? "Khách hàng" : "Báo giá";
      const container = [...document.querySelectorAll(".body-sidebar .sidebar-item-container")]
        .find((item) => item.getAttribute("item-name") === label);
      container?.querySelector(".standard-sidebar-item")?.classList.add("active-sidebar");
    }, 50);
  }

  function addQTItem() { createQTItems.value.push(_qtBlankItem()); }
  function removeQTItem(idx) { createQTItems.value.splice(idx, 1); }
  function clearQTItems() { createQTItems.value = [_qtBlankItem()]; }

  function autoFillQTItemByCode(item) {
    const found = (qtFormOptions.value.items || []).find((i) => i.name === item.item_code);
    if (found) {
      if (!item.item_name) item.item_name = found.item_name || found.name;
      if (!item.uom || item.uom === "Cái") item.uom = found.stock_uom || "Cái";
    }
  }

  function updateQTItemAmount(item) {
    item.amount = Math.round((parseFloat(item.qty) || 0) * (parseFloat(item.rate) || 0));
  }
  function updateQTItemRate(item) {
    const plr = parseFloat(item.price_list_rate) || 0;
    const disc = parseFloat(item.discount_percentage) || 0;
    if (plr) item.rate = Math.round(plr * (1 - disc / 100));
    updateQTItemAmount(item);
  }
  function qtItemPreTotal(item) {
    return Math.round((parseFloat(item.price_list_rate) || 0) * (parseFloat(item.qty) || 0));
  }
  function qtItemDiscount(item) {
    return Math.round(qtItemPreTotal(item) * ((parseFloat(item.discount_percentage) || 0) / 100));
  }
  function qtItemTax(item) {
    return Math.round((parseFloat(item.amount) || 0) * ((parseFloat(item.tax_rate) || 0) / 100));
  }
  function qtSubtotal() { return createQTItems.value.reduce((s, i) => s + qtItemPreTotal(i), 0); }
  function qtTotalDiscount() { return createQTItems.value.reduce((s, i) => s + qtItemDiscount(i), 0); }
  function qtGrandTotal() { return createQTItems.value.reduce((s, i) => s + (parseFloat(i.amount) || 0), 0); }
  function qtTotalQty() { return createQTItems.value.reduce((s, i) => s + (parseFloat(i.qty) || 0), 0); }
  function qtTotalTax() { return createQTItems.value.reduce((s, i) => s + qtItemTax(i), 0); }

  async function saveCreateQuotation(addAnother) {
    if (createQTSaving.value) return;
    if (!createQTForm.value.customer) { frappe.msgprint("Vui lòng chọn khách hàng."); return; }
    if (!createQTForm.value.transaction_date) { frappe.msgprint("Vui lòng nhập ngày báo giá."); return; }
    const validItems = createQTItems.value.filter((i) => i.item_code && (parseFloat(i.qty) || 0) > 0);
    if (!validItems.length) { frappe.msgprint("Vui lòng thêm ít nhất một hàng hóa."); return; }
    createQTSaving.value = true;
    try {
      const result = await call("create_quotation", {
        data: { ...createQTForm.value, items: validItems },
      }, "POST");
      frappe.show_alert({ message: `Đã tạo báo giá ${result.name}`, indicator: "green" }, 5);
      if (addAnother) {
        openCreateQuotation(
          createQTContext.value.customer,
          createQTContext.value.customerName,
          createQTContext.value.opportunity,
        );
      } else {
        backToQuotations();
        if (ctx.route.value === "quotations") ctx.loadRows();
      }
    } catch (error) {
      frappe.msgprint(error.message || "Không thể lưu báo giá.");
    } finally {
      createQTSaving.value = false;
    }
  }

  return {
    quotationDetailName, quotationDetail, quotationDetailLoading,
    quotationDetailTab, quotationDetailFieldSearch, quotationDetailShowEmpty,
    quotationNoteText, quotationNoteSaving, quotationAttachmentUploading,
    loadQuotationDetailPage, openQuotationDetail, backToQuotationList,
    quotationDetailTabCount, quotationDetailTotal, showQuotationDetailField,
    notifyQuotationDetailAction, toggleQuotationApprovalRequest, saveQuotationNote, uploadQuotationAttachment,
    openQuotationTagDialog,
    qtStockDialogOpen, qtStockRows, qtStockLoading, qtStockPage, qtStockPageLength, openQuotationStockLookup,
    createOrderFromQuotation, createQuotationActivity, openQuotationActivity,
    qtDetailItems, qtDetailLoading, qtExpandedItem, qtDetailItemsFiltered,
    qtItemsSearchOpen, qtItemsSearch, toggleQuotationItemsSearch,
    toggleQuotationDetailItem, loadQuotationDetail,
    quotationStatusClass, importQuotations,
    qtFilterOpen, qtItemsPanelOpen, qtShowMoreFilters, qtFilterCriteriaSearch, qtSavedFilterActive,
    qtQuickStatsOpen, qtQuickStats, qtQuickStatsLoading, toggleQuotationQuickStats,
    qtSortField, qtSortDirection, toggleQuotationSort,
    quotationsEnabledFilters, quotationsFilterValues, qtSavedFilterDates,
    QT_SAVED_FILTERS, QT_FILTER_CRITERIA, QT_FILTER_CRITERIA_MORE,
    activateQuotationSavedFilter, toggleQuotationsFilter,
    createQTSaving, createQTContext, createQTForm, createQTItems,
    qtFormOptions, qtItemList, qtCurrentUser, qtAutoIncreaseQty,
    onQTCustomerChange,
    openCreateQuotation, backToQuotations,
    addQTItem, removeQTItem, clearQTItems,
    autoFillQTItemByCode, updateQTItemAmount, updateQTItemRate,
    qtItemPreTotal, qtItemDiscount, qtItemTax,
    qtSubtotal, qtTotalDiscount, qtGrandTotal, qtTotalQty, qtTotalTax,
    saveCreateQuotation,
    qtItemPickerOpen, qtItemPickerSearch, qtItemPickerPage, qtItemPickerPageLength,
    qtItemPickerSelected, qtItemPickerCategoryFilter,
    qtItemPickerFiltered, qtItemPickerPageCount, qtItemPickerRows, qtItemPickerCategories,
    openQTItemPicker, closeQTItemPicker, toggleQTItemPickerRow, confirmQTItemPicker,
    quotationVisibleFields, quotationColumnDialogOpen, quotationColumnSearch, quotationColumnDraft,
    openQuotationColumnDialog, cancelQuotationColumnDialog, toggleQuotationDraftColumn,
    removeQuotationDraftColumn, resetQuotationDraftColumns, saveQuotationColumns,
    quotationColumnWidths, startQuotationColumnResize,
  };
}
