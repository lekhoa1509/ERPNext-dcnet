import { ref, computed } from "vue/dist/vue.esm-bundler.js";
import { call } from "../../utils.js";

// TIÊU CHÍ LỌC — mirror MISA "Thẻ chăm sóc" filter field list
export const CARE_FILTER_DEFS = [
  { field: "name", label: "Mã thẻ chăm sóc", type: "text" },
  { field: "customer_name", label: "Khách hàng", type: "text" },
  { field: "tax_id", label: "Mã số thuế", type: "text" },
  { field: "mobile_no", label: "Điện thoại", type: "text" },
  { field: "email_id", label: "Email", type: "text" },
  { field: "address", label: "Địa chỉ", type: "text" },
  { field: "layout", label: "Bố cục", type: "text" },
  { field: "owner", label: "Chủ sở hữu", type: "text" },
  { field: "item_type", label: "Loại hàng hóa", type: "text" },
  { field: "item", label: "Hàng hóa", type: "text" },
  { field: "customer", label: "Mã khách hàng", type: "text" },
  { field: "dissatisfaction_reason", label: "Lý do không hài lòng", type: "text" },
  { field: "description", label: "Mô tả", type: "text" },
  { field: "satisfaction_level", label: "Mức độ hài lòng", type: "select",
    options: ["Rất hài lòng", "Hài lòng", "Bình thường", "Không hài lòng"] },
  { field: "status", label: "Tình trạng chăm sóc", type: "select",
    options: ["Chưa chăm sóc", "Đang chăm sóc", "Đã chăm sóc"] },
  { field: "care_date", label: "Ngày chăm sóc", type: "date" },
  { field: "modified", label: "Ngày sửa", type: "date" },
  { field: "creation", label: "Ngày tạo", type: "date" },
  { field: "ward", label: "Phường/Xã", type: "text" },
  { field: "country", label: "Quốc gia", type: "text" },
];

const SELECT_FIELDS = ["satisfaction_level", "status"];
const DATE_FIELDS = ["care_date", "modified", "creation"];

export function useCareCards(ctx) {
  const careList = ref([]);
  const careTotal = ref(0);
  const carePage = ref(1);
  const carePageLength = ref(20);
  const careSearch = ref("");
  const careListLoading = ref(false);

  const careSelectedName = ref("");
  const careDetail = ref(null);
  const careDetailLoading = ref(false);
  const careTab = ref("activities"); // activities | purchases | care

  // Detail / edit / new page
  const careView = ref("list");        // list | detail
  const careFormMode = ref("view");    // view | edit | new
  const careForm = ref({});
  const careFormSaving = ref(false);
  const careDetailTab = ref("info");   // info | notes | files | open-tasks | done-tasks | chat | advisory
  const careFieldSearch = ref("");
  const careShowEmpty = ref(true);

  // Bộ lọc panel
  const careFilterOpen = ref(false);
  const careFilterSearch = ref("");
  const careEnabledFilters = ref([]);
  const careFilterValues = ref({});

  // Add care note
  const careNoteText = ref("");
  const careNoteSaving = ref(false);

  const careFilterDefinitions = computed(() => {
    const q = (careFilterSearch.value || "").toLowerCase();
    return q ? CARE_FILTER_DEFS.filter((d) => d.label.toLowerCase().includes(q)) : CARE_FILTER_DEFS;
  });

  const carePageCount = computed(() => Math.max(1, Math.ceil(careTotal.value / carePageLength.value)));
  const carePageStart = computed(() => (careTotal.value === 0 ? 0 : (carePage.value - 1) * carePageLength.value + 1));
  const carePageEnd = computed(() => Math.min(carePage.value * carePageLength.value, careTotal.value));

  function buildCareFilters() {
    const filters = {};
    careEnabledFilters.value.forEach((field) => {
      const value = careFilterValues.value[field];
      if (value === undefined || value === null || value === "") return;
      if (SELECT_FIELDS.includes(field)) {
        filters[field] = value;
      } else if (DATE_FIELDS.includes(field)) {
        filters[field] = ["between", [`${value} 00:00:00`, `${value} 23:59:59`]];
      } else {
        filters[field] = ["like", `%${value}%`];
      }
    });
    return filters;
  }

  async function loadCareCards() {
    careListLoading.value = true;
    try {
      const res = await call("get_list", {
        resource: "care_cards",
        search: careSearch.value || "",
        filters: JSON.stringify(buildCareFilters()),
        page: carePage.value,
        page_length: carePageLength.value,
      });
      careList.value = res?.data || [];
      careTotal.value = res?.total || 0;
      // Auto-select first row so the right panel has content (MISA behaviour)
      if (careList.value.length && !careList.value.find((r) => r.name === careSelectedName.value)) {
        selectCareCard(careList.value[0].name);
      } else if (!careList.value.length) {
        careSelectedName.value = "";
        careDetail.value = null;
      }
    } catch {
      careList.value = [];
      careTotal.value = 0;
    } finally {
      careListLoading.value = false;
    }
  }

  async function selectCareCard(name) {
    if (careSelectedName.value === name && careDetail.value) return;
    careSelectedName.value = name;
    careDetail.value = null;
    careDetailLoading.value = true;
    try {
      careDetail.value = await call("get_care_card_detail", { name });
    } catch (err) {
      frappe.msgprint(err.message || "Không thể tải chi tiết thẻ chăm sóc.");
    } finally {
      careDetailLoading.value = false;
    }
  }

  const careTimeline = computed(() => {
    const d = careDetail.value;
    if (!d) return [];
    if (careTab.value === "purchases") return d.purchases || [];
    if (careTab.value === "care") return d.care || [];
    return d.activities || [];
  });

  async function addCareNote() {
    const text = (careNoteText.value || "").trim();
    if (!text || !careSelectedName.value || careNoteSaving.value) return;
    careNoteSaving.value = true;
    try {
      await call("add_care_note", { name: careSelectedName.value, content: text }, "POST");
      careNoteText.value = "";
      careTab.value = "care";
      careDetail.value = await call("get_care_card_detail", { name: careSelectedName.value });
      frappe.show_alert({ message: "Đã thêm ghi chú chăm sóc", indicator: "green" }, 3);
    } catch (err) {
      frappe.msgprint(err.message || "Không thể lưu ghi chú.");
    } finally {
      careNoteSaving.value = false;
    }
  }

  function notifyCareAction(label) {
    frappe.msgprint({
      title: __(label),
      message: __("Chức năng này đang chờ cấu hình luồng xử lý/API theo spec."),
      indicator: "blue",
    });
  }

  function importCareCards() {
    frappe.new_doc("Data Import", { reference_doctype: "CRM Care Card", import_type: "Insert New Records" });
  }

  function currentCareCard() {
    return (careDetail.value && careDetail.value.card) || careForm.value || {};
  }

  function callCareCustomer() {
    const card = currentCareCard();
    const phone = card.mobile_no || careDetail.value?.customer_info?.mobile_no;
    if (!phone) return notifyCareAction("Gọi điện");
    window.location.href = `tel:${phone}`;
  }

  function emailCareCustomer() {
    const email = currentCareCard().email_id;
    if (!email) return notifyCareAction("Gửi email");
    window.location.href = `mailto:${email}`;
  }

  function showCareNoteComposer() {
    careTab.value = "care";
  }

  function createCareOrder() {
    const customer = currentCareCard().customer;
    if (!customer) return notifyCareAction("Sinh đơn hàng");
    frappe.new_doc("Sales Order", { customer });
  }

  // ── Detail / edit / new page ──
  async function openCareDetail(name) {
    await selectCareCard(name);
    careFormMode.value = "view";
    careDetailTab.value = "info";
    careView.value = "detail";
  }

  // Cross-feature entry points used by the Sales Order detail page's
  // Hỗ trợ > Thẻ chăm sóc tab.
  async function openCareCardFromOrder(name) {
    if (!name) return;
    ctx.navigate("care");
    await openCareDetail(name);
  }

  async function createCareCardForOrder(salesOrderName) {
    if (!salesOrderName) return;
    try {
      const so = await frappe.db.get_value("Sales Order", salesOrderName, "customer").then((r) => r.message || {});
      const customerId = so.customer || "";
      let cust = {};
      if (customerId) {
        cust = await frappe.db.get_value(
          "Customer", customerId, ["customer_name", "tax_id", "mobile_no", "email_id"]
        ).then((r) => r.message || {});
      }
      careSelectedName.value = "";
      careDetail.value = null;
      careForm.value = {
        customer: customerId,
        customer_name: cust.customer_name || customerId,
        tax_id: cust.tax_id || "",
        mobile_no: cust.mobile_no || "",
        email_id: cust.email_id || "",
        country: "Việt Nam",
        layout: "Mẫu tiêu chuẩn",
        status: "Chưa chăm sóc",
        sales_order: salesOrderName,
      };
      careFormMode.value = "new";
      careDetailTab.value = "info";
      careView.value = "detail";
      ctx.navigate("care");
    } catch (error) {
      frappe.msgprint(error.message || "Không thể tạo thẻ chăm sóc.");
    }
  }

  function backToCareList() {
    careView.value = "list";
    careFormMode.value = "view";
  }

  function startCareEdit() {
    const c = (careDetail.value && careDetail.value.card) || {};
    careForm.value = { ...c };
    careFormMode.value = "edit";
  }

  function cancelCareEdit() {
    if (careFormMode.value === "new") {
      backToCareList();
    } else {
      careFormMode.value = "view";
    }
  }

  async function saveCareForm() {
    if (careFormSaving.value) return;
    if (careFormMode.value === "new" && !careForm.value.customer) {
      frappe.msgprint("Vui lòng chọn Khách hàng");
      return;
    }
    careFormSaving.value = true;
    try {
      const res = await call(
        "save_care_card",
        { name: careFormMode.value === "new" ? "" : careSelectedName.value, data: careForm.value },
        "POST"
      );
      frappe.show_alert({ message: "Đã lưu thẻ chăm sóc", indicator: "green" }, 3);
      careSelectedName.value = res.name;
      careDetail.value = await call("get_care_card_detail", { name: res.name });
      careFormMode.value = "view";
      await loadCareCards();
    } catch (err) {
      frappe.msgprint(err.message || "Không thể lưu thẻ chăm sóc.");
    } finally {
      careFormSaving.value = false;
    }
  }

  // "+ Thêm" — pick customer (Link with server search), then open the full form
  function createCareCard() {
    frappe.prompt(
      [{ fieldname: "customer", label: "Khách hàng", fieldtype: "Link", options: "Customer", reqd: 1 }],
      async (values) => {
        careSelectedName.value = "";
        careDetail.value = null;
        // Pre-fill snapshot from the chosen customer
        const cust = await frappe.db.get_value(
          "Customer", values.customer, ["customer_name", "tax_id", "mobile_no", "email_id"]
        ).then((r) => r.message || {});
        careForm.value = {
          customer: values.customer,
          customer_name: cust.customer_name || values.customer,
          tax_id: cust.tax_id || "",
          mobile_no: cust.mobile_no || "",
          email_id: cust.email_id || "",
          country: "Việt Nam",
          layout: "Mẫu tiêu chuẩn",
          status: "Chưa chăm sóc",
        };
        careFormMode.value = "new";
        careDetailTab.value = "info";
        careView.value = "detail";
      },
      "Thêm thẻ chăm sóc",
      "Tiếp tục"
    );
  }

  // field visibility for "Tìm kiếm trường" + "Hiển thị dữ liệu trống"
  function showCareField(label, value) {
    const q = (careFieldSearch.value || "").toLowerCase().trim();
    if (q && !String(label).toLowerCase().includes(q)) return false;
    if (!careShowEmpty.value && (value === null || value === undefined || value === "")) return false;
    return true;
  }

  // ── Filters ──
  function toggleCareFilter(field) {
    const set = new Set(careEnabledFilters.value);
    if (set.has(field)) {
      set.delete(field);
      delete careFilterValues.value[field];
    } else {
      set.add(field);
    }
    careEnabledFilters.value = [...set];
  }
  function isCareFilterOn(field) {
    return careEnabledFilters.value.includes(field);
  }
  function applyCareFilters() {
    carePage.value = 1;
    loadCareCards();
  }
  function clearCareFilters() {
    careEnabledFilters.value = [];
    careFilterValues.value = {};
    carePage.value = 1;
    loadCareCards();
  }

  function changeCarePage(delta) {
    const next = carePage.value + delta;
    if (next < 1 || next > carePageCount.value) return;
    carePage.value = next;
    loadCareCards();
  }
  function setCarePageLength(n) {
    carePageLength.value = Number(n) || 20;
    carePage.value = 1;
    loadCareCards();
  }

  let careSearchTimer;
  function onCareSearchInput() {
    clearTimeout(careSearchTimer);
    carePage.value = 1;
    careSearchTimer = setTimeout(loadCareCards, 300);
  }

  // ── Helpers ──
  function careStatusLabel(s) {
    return s || "—";
  }
  function careStatusClass(s) {
    if (s === "Đã chăm sóc") return "cc-badge--done";
    if (s === "Đang chăm sóc") return "cc-badge--progress";
    return "cc-badge--new";
  }
  function careKindIcon(kind) {
    if (kind === "Task" || kind === "Nhiệm vụ") return "task";
    if (kind === "Đơn hàng" || kind === "Hóa đơn") return "order";
    if (kind === "Ghi chú" || kind === "Chăm sóc") return "care";
    return "email";
  }
  function fmtDate(d) {
    if (!d) return "—";
    const s = String(d);
    const datePart = s.indexOf(" ") > 0 ? s.slice(0, s.indexOf(" ")) : s;
    const [y, m, day] = datePart.split("-");
    return y && m && day ? `${day}/${m}/${y}` : s;
  }
  function fmtMoney(v, currency) {
    if (v === null || v === undefined) return "—";
    try {
      return new Intl.NumberFormat("vi-VN").format(v) + (currency ? ` ${currency}` : " ₫");
    } catch {
      return String(v);
    }
  }

  return {
    careList, careTotal, carePage, carePageLength, careSearch, careListLoading,
    careSelectedName, careDetail, careDetailLoading, careTab,
    careView, careFormMode, careForm, careFormSaving, careDetailTab,
    careFieldSearch, careShowEmpty,
    careFilterOpen, careFilterSearch, careEnabledFilters, careFilterValues,
    careFilterDefinitions, careAllFilterDefs: CARE_FILTER_DEFS, careNoteText, careNoteSaving,
    carePageCount, carePageStart, carePageEnd, careTimeline,
    loadCareCards, selectCareCard, addCareNote, createCareCard,
    notifyCareAction, importCareCards, callCareCustomer, emailCareCustomer,
    showCareNoteComposer, createCareOrder,
    openCareDetail, backToCareList, startCareEdit, cancelCareEdit, saveCareForm, showCareField,
    openCareCardFromOrder, createCareCardForOrder,
    toggleCareFilter, isCareFilterOn, applyCareFilters, clearCareFilters,
    changeCarePage, setCarePageLength, onCareSearchInput,
    careStatusLabel, careStatusClass, careKindIcon, fmtDate, fmtMoney,
  };
}
