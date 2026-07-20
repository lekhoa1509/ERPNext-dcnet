import { ref, computed, watch } from "vue/dist/vue.esm-bundler.js";
import { call, exportResource } from "../../utils.js";

const ORDER_SUMMARY_FIELDS = [
  { field: "name", label: "Số đơn hàng / hợp đồng" },
  { field: "transaction_date", label: "Ngày đặt hàng", format: "date" },
  { field: "delivery_date", label: "Ngày giao hàng", format: "date" },
  { field: "grand_total", label: "Giá trị đơn hàng", format: "currency" },
  { field: "net_total", label: "Thành tiền", format: "currency" },
  { field: "total_taxes_and_charges", label: "Tiền thuế", format: "currency" },
  { field: "discount_amount", label: "Tiền chiết khấu", format: "currency" },
  { field: "total_qty", label: "Tổng số lượng" },
  { field: "owner", label: "Người thực hiện" },
  { field: "company", label: "Đơn vị" },
  { field: "customer_name", label: "Khách hàng" },
  { field: "customer_group", label: "Nhóm khách hàng", empty: "- Không chọn -" },
  { field: "territory", label: "Khu vực", empty: "- Không chọn -" },
  { field: "order_type", label: "Loại đơn hàng" },
  { field: "po_no", label: "Số PO" },
  { field: "po_date", label: "Ngày PO", format: "date" },
  { field: "campaign", label: "Chiến dịch", empty: "- Không chọn -" },
  { field: "currency", label: "Tiền tệ" },
  { field: "selling_price_list", label: "Bảng giá", empty: "- Không chọn -" },
  { field: "payment_terms_template", label: "Điều khoản thanh toán", empty: "- Không chọn -" },
  { field: "taxes_and_charges", label: "Loại thuế", empty: "- Không chọn -" },
  { field: "display_order_status", label: "Trạng thái đơn hàng" },
  { field: "display_execution_status", label: "Tình trạng" },
  { field: "display_revenue_status", label: "Trạng thái ghi nhận DT" },
  { field: "per_billed", label: "% Đã xuất hóa đơn", format: "percent" },
  { field: "per_delivered", label: "% Đã giao hàng", format: "percent" },
  { field: "creation", label: "Ngày tạo", format: "datetime" },
  { field: "modified", label: "Ngày sửa", format: "datetime" },
];
const DEFAULT_ORDER_SUMMARY_FIELDS = ["name", "transaction_date", "grand_total", "owner", "company", "display_execution_status"];

function orderSummaryStorageKey() {
  return `dcnet-crm-order-summary-fields:${window.frappe?.session?.user || "Guest"}`;
}

function readOrderSummaryFields() {
  try {
    const stored = JSON.parse(window.localStorage.getItem(orderSummaryStorageKey()));
    if (!Array.isArray(stored)) return [...DEFAULT_ORDER_SUMMARY_FIELDS];
    const allowed = new Set(ORDER_SUMMARY_FIELDS.map((item) => item.field));
    return [...new Set(stored.filter((field) => allowed.has(field)))];
  } catch (_) {
    return [...DEFAULT_ORDER_SUMMARY_FIELDS];
  }
}

export function useOrders(ctx) {
  // ── Orders list detail panel ────────────────────────────────
  const soDetailItems = ref([]);
  const soDetailLoading = ref(false);
  const soExpandedItem = ref(-1);

  function toggleSODetailItem(idx) {
    soExpandedItem.value = soExpandedItem.value === idx ? -1 : idx;
  }

  async function loadSODetail(name) {
    soExpandedItem.value = -1;
    if (!name) { soDetailItems.value = []; return; }
    soDetailLoading.value = true;
    try {
      const items = await call("get_so_items", { name });
      soDetailItems.value = items || [];
    } catch {
      soDetailItems.value = [];
    } finally {
      soDetailLoading.value = false;
    }
  }

  // Auto-select the first row on the Orders list so the "Hàng hóa" preview
  // panel has something to show as soon as the list loads, matching the
  // same behavior already used on the Quotations list.
  watch(ctx.rows, (rows) => {
    if (ctx.route.value !== "orders") return;
    if (!rows.length) return;
    if (ctx.selected.value) return;
    ctx.selected.value = rows[0];
    loadSODetail(rows[0].name);
  });

  // ── Order detail page (MISA-style) ──────────────────────────
  const orderDetailName = ref("");
  const orderDetail = ref(null);
  const orderDetailTab = ref("items");
  const soSideCollapsed = ref(false);
  function toggleSOSidePanel() {
    soSideCollapsed.value = !soSideCollapsed.value;
  }
  const orderRelatedSection = ref("quotations");
  const ORDER_RELATED_SECTION_LABELS = {
    quotations: "Báo giá",
    delivery_notes: "Phiếu giao hàng",
    invoices: "Hóa đơn",
    payment_entries: "Thanh toán",
  };
  function orderRelatedSectionLabel(section) {
    return ORDER_RELATED_SECTION_LABELS[section] || "";
  }

  const orderCashflowSection = ref("actual_receipt");
  const ORDER_CASHFLOW_SECTION_LABELS = {
    actual_receipt: "Thực thu",
    planned_payment: "Dự kiến chi",
    actual_payment: "Thực chi",
  };
  function orderCashflowSectionLabel(section) {
    return ORDER_CASHFLOW_SECTION_LABELS[section] || "";
  }

  const orderSupportSection = ref("warranty");
  const ORDER_SUPPORT_SECTION_LABELS = {
    warranty: "Phiếu bảo hành",
    care_cards: "Thẻ chăm sóc",
    consult_cards: "Thẻ tư vấn",
  };
  function orderSupportSectionLabel(section) {
    return ORDER_SUPPORT_SECTION_LABELS[section] || "";
  }

  const orderOtherSection = ref("sales_returns");
  const ORDER_OTHER_SECTION_LABELS = {
    sales_returns: "Trả lại hàng bán",
    revenue_recognition: "Ghi nhận doanh số",
    invoices: "Hóa đơn",
    esignature: "Lịch sử ký điện tử",
    purchase_requests: "Yêu cầu mua hàng",
  };
  function orderOtherSectionLabel(section) {
    return ORDER_OTHER_SECTION_LABELS[section] || "";
  }
  function orderRevenueRequestStatusLabel(status) {
    return status === "Cancelled" ? "Đã thu hồi" : "Đề nghị ghi";
  }

  function openSOWarrantyClaimDialog() {
    const name = orderDetail.value?.document?.name;
    if (!name) return;
    frappe.prompt(
      [{ fieldname: "complaint", fieldtype: "Small Text", label: "Nội dung khiếu nại/bảo hành", reqd: 1 }],
      async (values) => {
        try {
          await call("add_so_warranty_claim", { sales_order: name, complaint: values.complaint }, "POST");
          frappe.show_alert({ message: "Đã tạo phiếu bảo hành", indicator: "green" });
          loadOrderDetail(name);
        } catch (error) {
          frappe.msgprint(error.message || "Không thể tạo phiếu bảo hành.");
        }
      },
      "Thêm phiếu bảo hành",
      "Lưu"
    );
  }

  // "Thẻ tư vấn" has no dedicated DocType/API in dcnet-crm yet (the only other
  // place using this label — the Opportunity "Sinh thẻ tư vấn" action — just
  // creates a plain CRM Care Card). Keep this an honest stub instead of
  // pretending it's wired up, matching the Customer detail page's Hỗ trợ tab.
  function notifyOrderAction(label) {
    frappe.show_alert({ message: `${label} đang chờ cấu hình luồng xử lý.`, indicator: "blue" }, 4);
  }

  function notifyOrderConsultCardUnavailable() {
    frappe.msgprint({
      title: "Chưa có dữ liệu nguồn",
      message: "Thẻ tư vấn chưa có DocType/API riêng trong dcnet-crm. Mình đã giữ nút phản hồi rõ để không bị bấm im lặng.",
      indicator: "orange",
    });
  }

  // ── Order detail: "Liên hệ" tab — quick-add / link existing Contact ─────
  // Reuses the same customer-scoped endpoints as the Customer detail page's
  // own Liên hệ tab (Contact links to Customer, not to Sales Order).
  function emptySOContactForm() {
    return { first_name: "", last_name: "", email_id: "", mobile_no: "", phone: "", designation: "", is_primary_contact: 0 };
  }
  const soContactDialogOpen = ref(false);
  const soContactForm = ref(emptySOContactForm());
  const soContactSaving = ref(false);
  const soContactPickerOpen = ref(false);
  const soContactPickerSearch = ref("");
  const soContactPickerRows = ref([]);
  const soContactPickerLoading = ref(false);

  function openSOContactDialog() {
    soContactForm.value = emptySOContactForm();
    soContactDialogOpen.value = true;
  }

  function closeSOContactDialog() {
    if (soContactSaving.value) return;
    soContactDialogOpen.value = false;
  }

  async function saveSOContact() {
    const customer = orderDetail.value?.document?.customer;
    if (!customer || !soContactForm.value.first_name?.trim() || soContactSaving.value) return;
    soContactSaving.value = true;
    try {
      await call("save_customer_contact", { customer, contact: soContactForm.value }, "POST");
      soContactDialogOpen.value = false;
      await loadOrderDetail(orderDetail.value.document.name);
      frappe.show_alert({ message: "Đã lưu liên hệ.", indicator: "green" });
    } catch (error) {
      frappe.msgprint(error.message || "Không thể lưu liên hệ.");
    } finally {
      soContactSaving.value = false;
    }
  }

  async function searchSOContacts() {
    const customer = orderDetail.value?.document?.customer;
    if (!customer) return;
    soContactPickerLoading.value = true;
    try {
      soContactPickerRows.value = await call("search_customer_contacts", {
        customer, search: soContactPickerSearch.value, page_length: 30,
      });
    } catch (error) {
      frappe.msgprint(error.message || "Không thể tìm danh sách liên hệ.");
    } finally {
      soContactPickerLoading.value = false;
    }
  }

  async function openSOContactPicker() {
    soContactPickerOpen.value = true;
    soContactPickerSearch.value = "";
    await searchSOContacts();
  }

  async function linkSOContact(contact) {
    const customer = orderDetail.value?.document?.customer;
    if (!contact?.name || !customer || soContactSaving.value) return;
    soContactSaving.value = true;
    try {
      await call("link_customer_contact", { customer, contact: contact.name }, "POST");
      soContactPickerOpen.value = false;
      await loadOrderDetail(orderDetail.value.document.name);
      frappe.show_alert({ message: "Đã liên kết liên hệ với khách hàng.", indicator: "green" });
    } catch (error) {
      frappe.msgprint(error.message || "Không thể liên kết liên hệ.");
    } finally {
      soContactSaving.value = false;
    }
  }

  // ── Order detail: "Hoạt động" tab — task/meeting/call + pagination ─────
  function localDateTimeInput(value) {
    if (value === undefined) value = new Date();
    const date = value instanceof Date ? value : new Date(value);
    if (Number.isNaN(date.getTime())) return "";
    const offset = date.getTimezoneOffset() * 60000;
    return new Date(date.getTime() - offset).toISOString().slice(0, 16);
  }

  const orderActivityDialogOpen = ref(false);
  const orderActivitySaving = ref(false);
  const orderActivityForm = ref({});
  const orderActivityPage = ref(1);
  const orderActivityPageLength = ref(10);

  const orderActivityPageCount = computed(() => Math.max(Math.ceil((orderDetail.value?.activities?.length || 0) / orderActivityPageLength.value), 1));
  const orderActivityPageStart = computed(() => orderDetail.value?.activities?.length ? (orderActivityPage.value - 1) * orderActivityPageLength.value + 1 : 0);
  const orderActivityPageEnd = computed(() => Math.min(orderActivityPage.value * orderActivityPageLength.value, orderDetail.value?.activities?.length || 0));
  const visibleOrderActivities = computed(() => {
    const start = (orderActivityPage.value - 1) * orderActivityPageLength.value;
    return (orderDetail.value?.activities || []).slice(start, start + orderActivityPageLength.value);
  });

  function changeOrderActivityPage(nextPage) {
    orderActivityPage.value = Math.min(Math.max(nextPage, 1), orderActivityPageCount.value);
  }

  function openOrderActivityDialog(activityType, activity) {
    if (activityType === undefined) activityType = "task";
    if (activity === undefined) activity = null;
    const startsOn = activity?.starts_on || localDateTimeInput();
    const defaultEnd = new Date(new Date(startsOn).getTime() + 30 * 60000);
    orderActivityForm.value = {
      name: activity?.name || "",
      activity_type: activity?.activity_type || activityType,
      subject: activity?.subject || "",
      description: activity?.description || "",
      due_date: activity?.due_date ? String(activity.due_date).slice(0, 10) : localDateTimeInput().slice(0, 10),
      starts_on: activity?.starts_on ? localDateTimeInput(activity.starts_on) : startsOn,
      ends_on: activity?.ends_on ? localDateTimeInput(activity.ends_on) : localDateTimeInput(defaultEnd),
      status: activity?.status || "Open",
      priority: activity?.priority || "Medium",
      allocated_to: activity?.performed_by || frappe.session.user,
    };
    orderActivityDialogOpen.value = true;
  }

  async function saveOrderActivity() {
    const name = orderDetail.value?.document?.name;
    if (!name || !orderActivityForm.value.subject?.trim() || orderActivitySaving.value) return;
    orderActivitySaving.value = true;
    try {
      await call("save_so_activity", { sales_order: name, activity: orderActivityForm.value }, "POST");
      orderActivityDialogOpen.value = false;
      await loadOrderDetail(name);
      frappe.show_alert({ message: "Đã lưu hoạt động.", indicator: "green" });
    } catch (error) {
      frappe.msgprint(error.message || "Không thể lưu hoạt động.");
    } finally {
      orderActivitySaving.value = false;
    }
  }

  function orderActivityTypeLabel(type) {
    return type === "task" ? "Nhiệm vụ" : type === "call" ? "Cuộc gọi" : "Lịch hẹn";
  }

  function orderActivityStatusLabel(status) {
    return ({ Open: "Đang thực hiện", Closed: "Đã hoàn thành", Completed: "Đã hoàn thành", Cancelled: "Đã hủy" })[status] || status || "—";
  }

  // Payment Entry.payment_type distinguishes money collected from the customer
  // ("Receive") from money paid back out against this order ("Pay", e.g. refunds).
  const orderActualReceipts = computed(() => (orderDetail.value?.payment_entries || []).filter((row) => row.payment_type === "Receive"));
  const orderActualPayments = computed(() => (orderDetail.value?.payment_entries || []).filter((row) => row.payment_type === "Pay"));

  // ── Dự kiến chi (planned expense) ────────────────────────────────
  const soPlannedExpenses = ref([]);
  const soPlannedExpensesLoading = ref(false);
  const soPlannedExpenseDialogOpen = ref(false);
  const soPlannedExpenseSaving = ref(false);
  const soPlannedExpenseForm = ref({ description: "", percentage: 0, amount: 0, planned_date: "", department: "", department_label: "" });
  const soOrgPickerOpen = ref(false);
  const soOrgTree = ref([]);

  async function loadSOPlannedExpenses(name) {
    if (!name) return;
    soPlannedExpensesLoading.value = true;
    try {
      soPlannedExpenses.value = await call("get_so_planned_expenses", { sales_order: name });
    } catch (error) {
      frappe.msgprint(error.message || "Không thể tải dự kiến chi.");
      soPlannedExpenses.value = [];
    } finally {
      soPlannedExpensesLoading.value = false;
    }
  }

  async function loadOrgUnitRoot() {
    const nodes = await call("get_org_unit_children", { node_type: "root" });
    soOrgTree.value = nodes.map((n) => ({ ...n, expanded: false, loaded: false, loading: false, children: [] }));
  }

  // Shared by any form that needs an "Đơn vị" (Department) picker — defaults
  // to the Dự kiến chi form; pass a different form ref to target it instead
  // (e.g. the "Đề nghị ghi doanh số" action modal).
  let soOrgPickerTargetForm = null;

  function openSOOrgPicker(targetForm) {
    soOrgPickerTargetForm = targetForm || soPlannedExpenseForm;
    soOrgPickerOpen.value = true;
    if (!soOrgTree.value.length) loadOrgUnitRoot();
  }

  function closeSOOrgPicker() {
    soOrgPickerOpen.value = false;
  }

  async function toggleOrgNode(node) {
    if (!node.expandable) return;
    node.expanded = !node.expanded;
    if (node.expanded && !node.loaded) {
      node.loading = true;
      try {
        const children = await call("get_org_unit_children", { node_type: node.node_type, parent: node.value });
        node.children = children.map((c) => ({ ...c, expanded: false, loaded: false, loading: false, children: [] }));
        node.loaded = true;
      } finally {
        node.loading = false;
      }
    }
  }

  function selectSOOrgNode(node) {
    if (!node.selectable) return;
    const target = soOrgPickerTargetForm || soPlannedExpenseForm;
    target.value.department = node.value;
    target.value.department_label = node.title;
    soOrgPickerOpen.value = false;
  }

  function openSOPlannedExpenseDialog() {
    soPlannedExpenseForm.value = { description: "", percentage: 0, amount: 0, planned_date: "", department: "", department_label: "" };
    soOrgPickerOpen.value = false;
    soPlannedExpenseDialogOpen.value = true;
    if (!soOrgTree.value.length) loadOrgUnitRoot();
  }

  function closeSOPlannedExpenseDialog() {
    soPlannedExpenseDialogOpen.value = false;
    soOrgPickerOpen.value = false;
  }

  async function saveSOPlannedExpense() {
    const name = orderDetail.value?.document?.name;
    if (!name || !soPlannedExpenseForm.value.description?.trim()) return;
    soPlannedExpenseSaving.value = true;
    try {
      await call("add_so_planned_expense", {
        sales_order: name,
        description: soPlannedExpenseForm.value.description,
        percentage: soPlannedExpenseForm.value.percentage || 0,
        amount: soPlannedExpenseForm.value.amount || 0,
        planned_date: soPlannedExpenseForm.value.planned_date || "",
        department: soPlannedExpenseForm.value.department || "",
      }, "POST");
      closeSOPlannedExpenseDialog();
      await loadSOPlannedExpenses(name);
    } catch (error) {
      frappe.msgprint(error.message || "Không thể lưu dự kiến chi.");
    } finally {
      soPlannedExpenseSaving.value = false;
    }
  }

  const orderDetailEditing = ref(false);
  const orderDetailSaving = ref(false);
  const soRevenueRequestSaving = ref(false);
  const soDocumentGenerating = ref(false);
  const soPrintDialogOpen = ref(false);
  const soPrintTemplatesLoading = ref(false);
  const soPrintTemplates = ref([]);
  const soPrintActionTemplate = ref("");
  const soPrintPreviewOpen = ref(false);
  const soPrintPreviewHtml = ref("");
  const soPrintPreviewTitle = ref("");
  const orderDetailForm = ref({});
  const orderDetailComment = ref("");
  const soItemDescExpanded = ref([]);

  function toggleSOItemDesc(idx) {
    const i = soItemDescExpanded.value.indexOf(idx);
    if (i >= 0) soItemDescExpanded.value.splice(i, 1);
    else soItemDescExpanded.value.push(idx);
  }

  function formatSOAddress(value) {
    if (!value) return "";
    const element = document.createElement("div");
    element.innerHTML = String(value).replace(/<br\s*\/?>/gi, ", ");
    return (element.textContent || "")
      .replace(/\s+/g, " ")
      .replace(/(?:,\s*){2,}/g, ", ")
      .replace(/^,\s*|,\s*$/g, "")
      .trim();
  }

  // ── Goods editor (Cập nhật hàng hóa popup) ─────────────────
  const soGoodsEditorOpen = ref(false);
  const soGoodsEditorSaving = ref(false);
  const soGoodsEditorItems = ref([]);

  function openSOGoodsEditor() {
    if (!orderDetail.value?.items) return;
    soGoodsEditorItems.value = orderDetail.value.items.map((item) => ({
      name: item.name || "",
      item_code: item.item_code || "",
      item_name: item.item_name || "",
      description: item.description || "",
      uom: item.uom || "Cái",
      qty: parseFloat(item.qty) || 0,
      price_list_rate: parseFloat(item.price_list_rate) || 0,
      discount_percentage: parseFloat(item.discount_percentage) || 0,
      rate: parseFloat(item.rate) || 0,
      amount: parseFloat(item.amount) || 0,
      a_end: item.custom_a_end || "",
      z_end: item.custom_z_end || "",
    }));
    if (!soGoodsEditorItems.value.length) soGoodsEditorItems.value = [_soBlankItem()];
    // Ensure the item list is loaded for the picker / datalist
    if (!soItemList.value.length) {
      call("get_so_form_options", { customer: orderDetail.value?.document?.customer || "" })
        .then((opts) => {
          soFormOptions.value = opts;
          soItemList.value = opts.items || [];
        })
        .catch(() => {});
    }
    soGoodsEditorOpen.value = true;
  }

  function closeSOGoodsEditor() {
    soGoodsEditorOpen.value = false;
    soGoodsEditorItems.value = [];
  }

  function addSOGoodsEditorItem() { soGoodsEditorItems.value.push(_soBlankItem()); }
  function removeSOGoodsEditorItem(idx) { soGoodsEditorItems.value.splice(idx, 1); }
  function clearSOGoodsEditorItems() { soGoodsEditorItems.value = [_soBlankItem()]; }

  function autoFillSOGoodsEditorItem(item) {
    const found = soItemList.value.find((i) => i.name === item.item_code);
    if (found) {
      if (!item.item_name) item.item_name = found.item_name || found.name;
      if (!item.uom || item.uom === "Cái") item.uom = found.stock_uom || "Cái";
    }
  }

  function soGoodsEditorRowAmount(item) {
    const plr = parseFloat(item.price_list_rate) || 0;
    const disc = parseFloat(item.discount_percentage) || 0;
    if (plr) item.rate = Math.round(plr * (1 - disc / 100));
    item.amount = Math.round((parseFloat(item.qty) || 0) * (parseFloat(item.rate) || 0));
  }

  function soGoodsEditorTotalQty() {
    return soGoodsEditorItems.value.reduce((s, i) => s + (parseFloat(i.qty) || 0), 0);
  }
  function soGoodsEditorTotalAmount() {
    return soGoodsEditorItems.value.reduce((s, i) => s + (parseFloat(i.amount) || 0), 0);
  }

  async function saveSOGoodsEditor() {
    if (soGoodsEditorSaving.value) return;
    const validItems = soGoodsEditorItems.value.filter((i) => i.item_code && (parseFloat(i.qty) || 0) > 0);
    if (!validItems.length) { frappe.msgprint("Vui lòng thêm ít nhất một hàng hóa."); return; }
    soGoodsEditorSaving.value = true;
    try {
      await call("update_so_items", {
        name: orderDetailName.value,
        items: validItems,
      }, "POST");
      soGoodsEditorOpen.value = false;
      soGoodsEditorItems.value = [];
      await loadOrderDetail();
    } catch (error) {
      frappe.msgprint(error.message || "Không thể cập nhật hàng hóa.");
    } finally {
      soGoodsEditorSaving.value = false;
    }
  }

  // ── Action menu (···) ──────────────────────────────────────
  const soActionMenuOpen = ref(false);
  const soActionSaving = ref(false);

  function toggleSOActionMenu() {
    soActionMenuOpen.value = !soActionMenuOpen.value;
  }

  function closeSOActionMenu() {
    soActionMenuOpen.value = false;
  }

  // ── SO Action Modal ─────────────────────────────────────────
  const _SO_ACTION_LABEL_MAP = {
    invoice: "Đề nghị xuất hóa đơn",
    delivery: "Giao hàng",
    return: "Đề nghị trả hàng",
    purchase_request: "Yêu cầu mua hàng",
    activity: "Nhật ký hoạt động",
  };

  const _MODAL_TASK_TYPES = [
    "Đề nghị xuất hóa đơn", "Giao hàng", "Đề nghị trả hàng", "Yêu cầu mua hàng",
    "Gửi báo giá", "Nhắc cước đến hạn", "Check TT DVVT", "Khảo sát DVVT",
    "Triển khai DVVT", "Lập PAKD", "Nghiệm thu DVVT", "Hỗ trợ kỹ thuật",
    "Chăm sóc khách hàng", "Họp tư vấn", "Khác",
  ];

  const soActionModalOpen = ref(false);
  const soActionModalAction = ref("");
  const soActionModalForm = ref({});
  const soActionModalSaving = ref(false);
  const soActionModalUserQuery = ref("");
  const soActionModalUserDropdown = ref([]);
  const soActionModalUserDdOpen = ref(false);
  const soActionModalTtOpen = ref(false);
  const soActionModalTtQuery = ref("");
  let _soActionUserTimer = null;

  const soActionModalFilteredTt = computed(() => {
    const q = soActionModalTtQuery.value.toLowerCase();
    return q ? _MODAL_TASK_TYPES.filter((t) => t.toLowerCase().includes(q)) : _MODAL_TASK_TYPES;
  });

  function openSOActionModal(action) {
    soActionMenuOpen.value = false;
    soActionModalAction.value = action;
    const label = _SO_ACTION_LABEL_MAP[action] || action;
    const doc = orderDetail.value?.document || {};
    soActionModalForm.value = {
      title: `${label} - ${doc.name || orderDetailName.value}`,
      date: "",
      priority: "Medium",
      status: "Open",
      task_type: label,
      related_users: [],
    };
    soActionModalUserQuery.value = "";
    soActionModalUserDropdown.value = [];
    soActionModalUserDdOpen.value = false;
    soActionModalTtOpen.value = false;
    soActionModalTtQuery.value = "";
    soActionModalOpen.value = true;
  }

  async function generateSalesOrderWord(template) {
    if (!orderDetailName.value || soDocumentGenerating.value) return;
    soDocumentGenerating.value = true;
    soPrintActionTemplate.value = template.name;
    try {
      const result = await call("generate_sales_order_word", {
        name: orderDetailName.value,
        template_name: template.name,
      }, "POST");
      if (!result?.file_url) throw new Error("Missing generated file URL");
      const link = document.createElement("a");
      link.href = result.file_url;
      link.download = result.file_name || "don-hang.docx";
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error("Sales Order Word generation failed", error);
      frappe.show_alert({
        message: __("Không thể tạo mẫu Word cho đơn hàng."),
        indicator: "red",
      }, 5);
    } finally {
      soDocumentGenerating.value = false;
      soPrintActionTemplate.value = "";
    }
  }

  async function loadSalesOrderPrintTemplates() {
    if (!orderDetailName.value) return;
    soPrintTemplatesLoading.value = true;
    try {
      soPrintTemplates.value = await call("get_sales_order_print_templates", {
        name: orderDetailName.value,
      }) || [];
    } catch (error) {
      console.error("Sales Order print templates failed", error);
      soPrintTemplates.value = [];
      frappe.show_alert({ message: __("Không thể tải danh sách mẫu in."), indicator: "red" }, 5);
    } finally {
      soPrintTemplatesLoading.value = false;
    }
  }

  async function printSalesOrder() {
    if (!orderDetailName.value) return;
    soPrintDialogOpen.value = true;
    await loadSalesOrderPrintTemplates();
  }

  function closeSalesOrderPrintDialog() {
    if (soDocumentGenerating.value) return;
    soPrintDialogOpen.value = false;
  }

  function deleteSalesOrderPrintTemplate(template) {
    if (!template?.name || soPrintActionTemplate.value === template.name) return;
    frappe.confirm(
      __("Xóa mẫu in \"{0}\"? Hành động này không thể hoàn tác.", [template.template_name || template.name]),
      async () => {
        soPrintActionTemplate.value = template.name;
        try {
          await call("delete_sales_order_print_template", { template_name: template.name }, "POST");
          frappe.show_alert({ message: __("Đã xóa mẫu in."), indicator: "green" });
          await loadSalesOrderPrintTemplates();
        } catch (error) {
          frappe.msgprint(error.message || __("Không thể xóa mẫu in."));
        } finally {
          soPrintActionTemplate.value = "";
        }
      },
    );
  }

  function downloadSalesOrderTemplate(template) {
    return generateSalesOrderWord(template);
  }

  async function getSalesOrderPrintHtml(template) {
    soPrintActionTemplate.value = template.name;
    try {
      return await call("preview_sales_order_print_template", {
        name: orderDetailName.value,
        template_name: template.name,
      }, "POST");
    } finally {
      soPrintActionTemplate.value = "";
    }
  }

  function sanitizeSalesOrderPrintHtml(html) {
    const holder = document.createElement("template");
    holder.innerHTML = String(html || "");
    holder.content.querySelectorAll("script, iframe, object, embed, form").forEach((node) => node.remove());
    holder.content.querySelectorAll("*").forEach((node) => {
      Array.from(node.attributes).forEach((attribute) => {
        const name = attribute.name.toLowerCase();
        const value = String(attribute.value || "").trim().toLowerCase();
        if (name.startsWith("on") || ((name === "href" || name === "src") && value.startsWith("javascript:"))) {
          node.removeAttribute(attribute.name);
        }
      });
    });
    return holder.innerHTML;
  }

  async function previewSalesOrderTemplate(template) {
    try {
      const result = await getSalesOrderPrintHtml(template);
      soPrintPreviewHtml.value = sanitizeSalesOrderPrintHtml(
        result?.html || "<p>Mẫu này chưa có nội dung xem trước.</p>",
      );
      soPrintPreviewTitle.value = result?.template_name || template.template_name || template.name;
      soPrintPreviewOpen.value = true;
    } catch (error) {
      console.error("Sales Order template preview failed", error);
      frappe.show_alert({ message: __("Không thể tạo bản xem trước."), indicator: "red" }, 5);
    }
  }

  function closeSalesOrderPrintPreview() {
    soPrintPreviewOpen.value = false;
  }

  function writeSalesOrderPrintWindow(printWindow, html, title) {
    const safeTitle = String(title || orderDetailName.value).replace(/[<>]/g, "");
    printWindow.document.write(`<!doctype html><html><head><meta charset="utf-8"><title>${safeTitle}</title><style>
      @page { size: A4; margin: 20mm; }
      body { color:#111; font-family:'Times New Roman',serif; font-size:13pt; line-height:1.65; margin:0 auto; max-width:800px; padding:20mm; }
      table { border-collapse:collapse; width:100%; } td,th { padding:4px 8px; }
      @media print { body { margin:0; max-width:none; padding:0; } }
    </style></head><body>${html}</body></html>`);
    printWindow.document.close();
    printWindow.focus();
    setTimeout(() => printWindow.print(), 250);
  }

  async function printSalesOrderTemplate(template) {
    const printWindow = window.open("", "_blank");
    if (!printWindow) {
      frappe.show_alert({ message: __("Trình duyệt đang chặn cửa sổ in."), indicator: "orange" }, 5);
      return;
    }
    printWindow.document.write("<p style='font-family:sans-serif;padding:24px'>Đang tạo bản in...</p>");
    try {
      const result = await getSalesOrderPrintHtml(template);
      printWindow.document.open();
      writeSalesOrderPrintWindow(
        printWindow,
        sanitizeSalesOrderPrintHtml(result?.html || "<p>Mẫu này chưa có nội dung.</p>"),
        `${orderDetailName.value} - ${result?.template_name || template.template_name || template.name}`,
      );
    } catch (error) {
      printWindow.close();
      console.error("Sales Order template print failed", error);
      frappe.show_alert({ message: __("Không thể tạo bản in."), indicator: "red" }, 5);
    }
  }

  function printSalesOrderPreview() {
    const printWindow = window.open("", "_blank");
    if (!printWindow) return;
    writeSalesOrderPrintWindow(
      printWindow,
      soPrintPreviewHtml.value,
      `${orderDetailName.value} - ${soPrintPreviewTitle.value}`,
    );
  }

  function openSalesOrderTemplateBuilder() {
    window.open("/app/contract-template-builder?new=1", "_blank");
  }

  function openOrderCustomer() {
    const customer = orderDetail.value?.document?.customer;
    if (customer) ctx.openRelated("Customer", { name: customer });
  }

  function requestSOApproval() {
    openSOActionModal("activity");
    const docName = orderDetail.value?.document?.name || orderDetailName.value;
    soActionModalForm.value.title = `Gửi phê duyệt - ${docName}`;
    soActionModalForm.value.task_type = "Gửi phê duyệt";
  }

  function requestSORevenueRecognition() {
    openSOActionModal("activity");
    const docName = orderDetail.value?.document?.name || orderDetailName.value;
    soActionModalForm.value.title = `Đề nghị ghi doanh số - ${docName}`;
    soActionModalForm.value.task_type = "Đề nghị ghi doanh số";
    soActionModalForm.value.revenue_item = "";
    soActionModalForm.value.department = "";
    soActionModalForm.value.department_label = "";
    soActionModalForm.value.recognized_amount = orderDetail.value?.document?.grand_total || 0;
    soActionModalForm.value.achieved_amount = 0;
    soActionModalForm.value.note = "";
  }

  async function withdrawSORevenueRecognition() {
    if (soRevenueRequestSaving.value || !orderDetailName.value) return;
    const confirmed = await new Promise((resolve) => {
      frappe.confirm(
        "Thu hồi đề nghị ghi sẽ hủy nhiệm vụ và thu hồi thông báo đã gửi cho người liên quan. Bạn có chắc muốn tiếp tục?",
        () => resolve(true),
        () => resolve(false),
      );
    });
    if (!confirmed) return;

    soRevenueRequestSaving.value = true;
    try {
      const result = await call("withdraw_so_revenue_request", {
        so_name: orderDetailName.value,
      }, "POST");
      await loadOrderDetail(orderDetailName.value);
      const notificationCount = Number(result?.retracted_notifications || 0);
      frappe.show_alert({
        message: notificationCount
          ? `Đã thu hồi đề nghị ghi và ${notificationCount} thông báo liên quan.`
          : "Đã thu hồi đề nghị ghi.",
        indicator: "green",
      }, 6);
    } catch (err) {
      frappe.msgprint(err.message || "Không thể thu hồi đề nghị ghi.");
    } finally {
      soRevenueRequestSaving.value = false;
    }
  }

  function closeSOActionModal() {
    soActionModalOpen.value = false;
  }

  async function _soModalFetchUsers(q) {
    try {
      const res = await call("search_crm_users", { query: q, limit: 20 });
      soActionModalUserDropdown.value = res || [];
    } catch {
      soActionModalUserDropdown.value = [];
    }
  }

  function soActionModalOnUserFocus() {
    if (!soActionModalUserDdOpen.value || soActionModalUserDropdown.value.length === 0) {
      soActionModalUserDdOpen.value = true;
      _soModalFetchUsers(soActionModalUserQuery.value || "");
    }
  }

  function soActionModalOnUserInput() {
    soActionModalUserDdOpen.value = true;
    clearTimeout(_soActionUserTimer);
    _soActionUserTimer = setTimeout(() => _soModalFetchUsers(soActionModalUserQuery.value || ""), 200);
  }

  function soActionModalIsUserSel(email) {
    return !!(soActionModalForm.value.related_users || []).find((u) => u.name === email);
  }

  function soActionModalToggleUser(user) {
    const f = soActionModalForm.value;
    if (!f.related_users) f.related_users = [];
    if (soActionModalIsUserSel(user.name)) {
      f.related_users = f.related_users.filter((u) => u.name !== user.name);
    } else {
      f.related_users = [...f.related_users, { name: user.name, full_name: user.full_name }];
    }
  }

  function soActionModalRemoveUser(email) {
    const f = soActionModalForm.value;
    if (f.related_users) f.related_users = f.related_users.filter((u) => u.name !== email);
  }

  function soActionModalCloseUserDd() {
    soActionModalUserDdOpen.value = false;
  }

  function soActionModalToggleTt() {
    soActionModalTtOpen.value = !soActionModalTtOpen.value;
    if (soActionModalTtOpen.value) soActionModalTtQuery.value = "";
  }

  function soActionModalSelectTt(type) {
    soActionModalForm.value.task_type = type;
    soActionModalTtOpen.value = false;
  }

  function soActionModalCloseTt() {
    soActionModalTtOpen.value = false;
  }

  async function confirmSOActionModal() {
    if (soActionModalSaving.value) return;
    soActionModalSaving.value = true;
    try {
      const form = soActionModalForm.value;
      const res = await call("create_so_action", {
        so_name: orderDetailName.value,
        action: soActionModalAction.value,
        extra: form,
      }, "POST");
      soActionModalOpen.value = false;
      if (res) {
        const docLink = res.doc_name
          ? ` → <a href="/app/${(res.doc_type || "").toLowerCase().replace(/ /g, "-")}/${res.doc_name}" target="_blank">${res.doc_name}</a>`
          : "";
        frappe.show_alert({ message: `${res.label} đã tạo${docLink}`, indicator: "green" }, 6);
        await loadOrderDetail(orderDetailName.value);
      }
    } catch (err) {
      frappe.msgprint(err.message || "Không thể tạo hoạt động.");
    } finally {
      soActionModalSaving.value = false;
    }
  }

  // ── Stock lookup (Tra cứu số lượng tồn popup) ───────────────
  const soStockLookupOpen = ref(false);
  const soStockLookupLoading = ref(false);
  const soStockLookupItems = ref([]);
  const soStockLookupExpanded = ref([]);

  function toggleSOStockLookupRow(code) {
    const i = soStockLookupExpanded.value.indexOf(code);
    if (i >= 0) soStockLookupExpanded.value.splice(i, 1);
    else soStockLookupExpanded.value.push(code);
  }

  async function openSOStockLookup() {
    if (!orderDetailName.value) return;
    soStockLookupOpen.value = true;
    soStockLookupLoading.value = true;
    soStockLookupItems.value = [];
    soStockLookupExpanded.value = [];
    try {
      const res = await call("get_so_stock_balance", { name: orderDetailName.value });
      soStockLookupItems.value = (res && res.items) || [];
    } catch (error) {
      soStockLookupItems.value = [];
      frappe.msgprint(error.message || "Không thể tra cứu số lượng tồn.");
    } finally {
      soStockLookupLoading.value = false;
    }
  }

  function closeSOStockLookup() {
    soStockLookupOpen.value = false;
    soStockLookupItems.value = [];
    soStockLookupExpanded.value = [];
  }

  async function loadOrderDetail(name) {
    const target = name !== undefined ? name : orderDetailName.value;
    if (!target) return ctx.navigate("orders");
    ctx.loading.value = true;
    orderDetail.value = null;
    try {
      orderDetail.value = await call("get_so_detail", { name: target });
      orderDetailName.value = target;
      loadSOPlannedExpenses(target);
    } catch (error) {
      frappe.msgprint(error.message || "Không thể tải chi tiết đơn hàng.");
    } finally {
      ctx.loading.value = false;
    }
  }

  function openOrderDetail(row) {
    if (!row?.name) return;
    orderDetailName.value = row.name;
    orderDetailTab.value = "items";
    orderDetailEditing.value = false;
    // Avoid frappe.set_route race condition: set route directly + sync URL
    ctx.route.value = "order-detail";
    frappe.route_options = { view: "order-detail", order: row.name };
    const url = new URL(window.location.href);
    url.hash = "";
    url.searchParams.set("view", "order-detail");
    url.searchParams.set("order", row.name);
    url.searchParams.delete("customer");
    url.searchParams.delete("opportunity");
    window.history.replaceState(window.history.state, "", url);
    window.sessionStorage.setItem("dcnet-crm-view", "order-detail");
    window.setTimeout(() => {
      document.querySelectorAll(".body-sidebar .standard-sidebar-item").forEach((item) => {
        item.classList.remove("active-sidebar");
      });
      const container = [...document.querySelectorAll(".body-sidebar .sidebar-item-container")]
        .find((item) => item.getAttribute("item-name") === "Đơn hàng");
      container?.querySelector(".standard-sidebar-item")?.classList.add("active-sidebar");
    }, 50);
    loadOrderDetail(row.name);
  }

  function backToOrders() {
    ctx.navigate("orders");
  }

  function orderDetailTotalQty() {
    if (!orderDetail.value?.items) return 0;
    return orderDetail.value.items.reduce((s, i) => s + (parseFloat(i.qty) || 0), 0);
  }

  function orderDetailTotalDelivered() {
    if (!orderDetail.value?.items) return 0;
    return orderDetail.value.items.reduce((s, i) => s + (parseFloat(i.delivered_qty) || 0), 0);
  }

  function orderDetailTotalTax() {
    if (!orderDetail.value?.items) return 0;
    return orderDetail.value.items.reduce((s, i) => s + (parseFloat(i.tax_amount) || 0), 0);
  }

  // ── "Ghi chú và đính kèm" tab: attachments (Ghi chú reuses the existing
  // orderDetailComment/saveOrderDetailComment/orderDetail.comments already
  // wired up for the Trao đổi tab — same real Comment records, just also
  // surfaced here per the reference UI). ─────────────────────────────────
  const orderNoteSection = ref("notes");
  const soAttachUploading = ref(false);

  async function uploadSOFile(event) {
    const file = event?.target?.files?.[0];
    if (event?.target) event.target.value = "";
    const target = orderDetail.value?.document?.name;
    if (!file || !target || soAttachUploading.value) return;
    soAttachUploading.value = true;
    try {
      const formData = new FormData();
      formData.append("file", file, file.name);
      formData.append("is_private", 1);
      formData.append("doctype", "Sales Order");
      formData.append("docname", target);
      const response = await window.fetch("/api/method/upload_file", {
        method: "POST",
        headers: { "X-Frappe-CSRF-Token": frappe.csrf_token },
        body: formData,
      });
      if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        throw new Error(data?._server_messages || data?.exception || "Tải tệp thất bại");
      }
      await loadOrderDetail(target);
      frappe.show_alert({ message: "Đã thêm tệp đính kèm.", indicator: "green" });
    } catch (error) {
      frappe.msgprint(error.message || "Không thể tải tệp.");
    } finally {
      soAttachUploading.value = false;
    }
  }

  function addSOAttachmentLink() {
    const target = orderDetail.value?.document?.name;
    if (!target) return;
    frappe.prompt(
      [
        { fieldname: "url", fieldtype: "Data", label: "Liên kết (URL)", default: "https://", reqd: 1 },
        { fieldname: "title", fieldtype: "Data", label: "Tên hiển thị" },
      ],
      async (values) => {
        try {
          await call("add_so_attachment_link", {
            name: target,
            url: /^(https?:\/\/)/i.test(values.url.trim()) ? values.url.trim() : `https://${values.url.trim()}`,
            title: values.title || "",
          }, "POST");
          await loadOrderDetail(target);
          frappe.show_alert({ message: "Đã thêm liên kết.", indicator: "green" });
        } catch (error) {
          frappe.msgprint(error.message || "Không thể thêm liên kết.");
        }
      },
      "Thêm liên kết",
      "Lưu"
    );
  }

  function deleteSOAttachment(fileName) {
    if (!fileName) return;
    frappe.confirm("Xóa tài liệu này?", async () => {
      try {
        await call("delete_so_attachment", { file_name: fileName }, "POST");
        await loadOrderDetail(orderDetail.value?.document?.name);
        frappe.show_alert({ message: "Đã xóa tài liệu.", indicator: "green" });
      } catch (error) {
        frappe.msgprint(error.message || "Không thể xóa tài liệu.");
      }
    });
  }

  async function saveOrderDetailComment() {
    const content = orderDetailComment.value.trim();
    if (!content || !orderDetailName.value) return;
    await call("add_note", { resource: "orders", name: orderDetailName.value, content }, "POST");
    orderDetailComment.value = "";
    await loadOrderDetail();
  }

  function startOrderDetailEdit() {
    if (!orderDetail.value) return;
    orderDetailForm.value = { ...orderDetail.value.document };
    orderDetailEditing.value = true;
  }

  function cancelOrderDetailEdit() {
    orderDetailEditing.value = false;
    orderDetailForm.value = {};
  }

  async function saveOrderDetailEdit() {
    if (orderDetailSaving.value) return;
    orderDetailSaving.value = true;
    try {
      await call("update_sales_order", {
        name: orderDetailName.value,
        data: orderDetailForm.value,
      }, "POST");
      orderDetailEditing.value = false;
      await loadOrderDetail();
    } catch (error) {
      frappe.msgprint(error.message || "Không thể lưu đơn hàng.");
    } finally {
      orderDetailSaving.value = false;
    }
  }

  // ── Edit mode ────────────────────────────────────────────────
  const soEditMode = ref(false);
  const soEditTarget = ref("");

  function openEditSO(detail) {
    if (!detail?.document) return;
    const doc = detail.document;

    soEditMode.value = true;
    soEditTarget.value = doc.name;

    createSOContext.value = {
      customer: doc.customer || "",
      customerName: doc.customer_name || "",
      opportunity: doc.opportunity || "",
    };

    createSOForm.value = {
      customer: doc.customer || "",
      contact_person: doc.contact_person || "",
      opportunity: doc.opportunity || "",
      order_type: doc.order_type || "Sales",
      transaction_date: doc.transaction_date || "",
      delivery_date: doc.delivery_date || "",
      po_no: doc.po_no || "",
      po_date: doc.po_date || "",
      contract_duration: doc.custom_contract_duration || "",
      contract_expiry: doc.custom_contract_expiry || "",
      installation_zone: doc.custom_installation_zone || "",
      campaign: doc.campaign || "",
      selling_price_list: doc.selling_price_list || "",
      currency: doc.currency || "VND",
      payment_terms_template: doc.payment_terms_template || "",
      taxes_and_charges: doc.taxes_and_charges || "",
      territory: doc.territory || "",
      company: doc.company || "",
      title: doc.title || "",
      note: doc.notes || doc.note || "",
      execution_status: doc.custom_execution_status || "Chưa thực hiện",
      revenue_recognition_date: doc.custom_revenue_recognition_date || doc.transaction_date || "",
      revenue_status: doc.custom_revenue_status || "Bản nhập",
      payment_due_date: doc.custom_payment_due_date || "",
      acceptance_date: doc.custom_acceptance_date || "",
      billing_customer: doc.customer || "",
      billing_address: doc.address_display || "",
      billing_district: doc.custom_billing_district || "",
      billing_ward: doc.custom_billing_ward || "",
      billing_street: doc.custom_billing_street || "",
      billing_zipcode: doc.custom_billing_zipcode || "",
      shipping_recipient: detail.shipping?.recipient || "",
      shipping_address: detail.shipping?.address || "",
      shipping_district: doc.custom_shipping_district || "",
      shipping_ward: doc.custom_shipping_ward || "",
      shipping_street: doc.custom_shipping_street || "",
      shipping_zipcode: doc.custom_shipping_zipcode || "",
      warehouse: doc.set_warehouse || "",
      contract_type: doc.custom_contract_type || "",
      order_category: doc.custom_order_category || "",
      order_value: parseFloat(doc.grand_total) || 0,
      credit_days: parseFloat(doc.credit_days) || 0,
      liquidation_value: parseFloat(doc.custom_liquidation_value) || 0,
      payment_cycle: doc.custom_payment_cycle || "",
      production_deadline: doc.custom_production_deadline || "",
      shared_flag: !!doc.custom_shared,
      sync_price: !!doc.custom_sync_price,
      referral_partner: doc.custom_referral_partner || "",
    };

    createSOItems.value = (detail.items || []).map((item) => ({
      name: item.name || "",
      item_code: item.item_code || "",
      item_name: item.item_name || "",
      description: item.description || "",
      uom: item.uom || "Cái",
      qty: parseFloat(item.qty) || 1,
      price_list_rate: parseFloat(item.price_list_rate) || 0,
      discount_percentage: parseFloat(item.discount_percentage) || 0,
      rate: parseFloat(item.net_rate || item.rate) || 0,
      amount: parseFloat(item.net_amount || item.amount) || 0,
      a_end: item.custom_a_end || "",
      z_end: item.custom_z_end || "",
      account_id: item.custom_dcnet_account_id || "",
      tax_rate: parseFloat(item.tax_rate) || 0,
    }));
    if (!createSOItems.value.length) createSOItems.value = [_soBlankItem()];

    // Auto-fetch account for items that have item_code but no account_id yet
    if (doc.order_type !== "Maintenance") {
      createSOItems.value.forEach((item) => {
        if (item.item_code && !item.account_id) autoFetchSOItemAccount(item);
      });
      if (createSOItems.value.some(i => i.item_code)) {
        _loadSOEndpointSuggestions(createSOItems.value.find(i => i.item_code)?.item_code || "");
      }
    }

    call("get_so_form_options", { customer: doc.customer || "" })
      .then((opts) => { soFormOptions.value = opts; soItemList.value = opts.items || []; })
      .catch(() => {});

    ctx.route.value = "create-sales-order";
    const url = new URL(window.location.href);
    url.searchParams.set("view", "create-sales-order");
    url.searchParams.set("order", doc.name);
    url.searchParams.delete("customer");
    url.searchParams.delete("opportunity");
    window.history.replaceState(window.history.state, "", url);
    window.sessionStorage.setItem("dcnet-crm-view", "create-sales-order");
  }

  function cancelEditSO() {
    const name = soEditTarget.value;
    soEditMode.value = false;
    soEditTarget.value = "";
    if (name) {
      openOrderDetail({ name });
    } else {
      ctx.navigate("orders");
    }
  }

  const createSOContext = ref({ customer: "", customerName: "", opportunity: "", quotation: "" });
  const createSOSaving = ref(false);
  const createSOForm = ref({});
  const createSOItems = ref([]);
  const soFormOptions = ref({
    items: [], customers: [], opportunities: [], contacts: [],
    price_lists: [], payment_terms: [], territories: [],
    campaigns: [], taxes_templates: [],
  });

  // Reload contacts/opportunities when the customer is picked from the dropdown
  function onSOCustomerChange(val) {
    createSOForm.value.contact_person = "";
    createSOForm.value.opportunity = "";
    createSOForm.value.billing_customer = val || "";
    if (!val) return;
    call("get_so_form_options", { customer: val })
      .then((opts) => { soFormOptions.value = opts; soItemList.value = opts.items || []; })
      .catch(() => {});
  }

  // ── Item Picker ──────────────────────────────────────────────
  const soItemPickerOpen = ref(false);
  const soItemPickerSearch = ref("");
  const soItemPickerPage = ref(1);
  const soItemPickerPageLength = ref(10);
  const soItemPickerSelected = ref([]);
  const soItemPickerCategoryFilter = ref("");
  const soItemList = ref([]);
  const soItemPickerTarget = ref("create");

  const soItemPickerFiltered = computed(() => {
    const kw = soItemPickerSearch.value.trim().toLocaleLowerCase("vi");
    const cat = soItemPickerCategoryFilter.value;
    return soItemList.value.filter((item) => {
      if (cat && item.item_group !== cat) return false;
      if (!kw) return true;
      return (item.name || "").toLocaleLowerCase("vi").includes(kw)
        || (item.item_name || "").toLocaleLowerCase("vi").includes(kw);
    });
  });
  const soItemPickerPageCount = computed(() => Math.ceil(soItemPickerFiltered.value.length / soItemPickerPageLength.value) || 1);
  const soItemPickerRows = computed(() => {
    const start = (soItemPickerPage.value - 1) * soItemPickerPageLength.value;
    return soItemPickerFiltered.value.slice(start, start + soItemPickerPageLength.value);
  });
  const soItemPickerCategories = computed(() => {
    const cats = new Set(soItemList.value.map((i) => i.item_group).filter(Boolean));
    return [...cats].sort((a, b) => a.localeCompare(b, "vi"));
  });

  function _soBlankItem() {
    return {
      item_code: "", item_name: "", description: "",
      a_end: "", z_end: "",
      account_id: "", account_new: false,
      uom: "Cái", qty: 1,
      price_list_rate: 0, discount_percentage: 0,
      rate: 0, amount: 0,
      tax_rate: 0,
    };
  }

  // ── Service Account suggestions ─────────────────────────────────────
  const soAEndOptions = ref([]);
  const soZEndOptions = ref([]);

  async function _loadSOEndpointSuggestions(item_code) {
    const customer = createSOContext.value.customer;
    if (!customer) return;
    try {
      const rows = await call("get_customer_service_accounts", { customer, item_code: item_code || undefined });
      const aEnds = new Set(rows.map(r => r.a_end).filter(Boolean));
      const zEnds = new Set(rows.map(r => r.z_end).filter(Boolean));
      soAEndOptions.value = [...aEnds].sort();
      soZEndOptions.value = [...zEnds].sort();
    } catch { /* ignore */ }
  }

  async function autoFetchSOItemAccount(item) {
    if (createSOForm.value.order_type === "Maintenance") return;
    const customer = createSOContext.value.customer;
    if (!customer || !item.item_code) { item.account_id = ""; item.account_new = false; return; }
    try {
      // Preview only — the account is created when the order is saved, not now.
      const result = await call("preview_service_account", {
        customer,
        item_code: item.item_code,
        a_end: item.a_end || "",
        z_end: item.z_end || "",
      });
      if (result && result.is_new) { item.account_id = ""; item.account_new = true; }
      else if (result && result.account_code) { item.account_id = result.account_code; item.account_new = false; }
      else { item.account_id = ""; item.account_new = false; }
    } catch { /* ignore */ }
  }

  function _soBlankPaymentRow() {
    return { payment_term: "", invoice_portion: 0, payment_amount: 0, due_date: "" };
  }
  const createSOPaymentSchedule = ref([_soBlankPaymentRow()]);
  function addSOPaymentRow() { createSOPaymentSchedule.value.push(_soBlankPaymentRow()); }
  function removeSOPaymentRow(idx) { createSOPaymentSchedule.value.splice(idx, 1); }
  function soPaymentScheduleTotal() {
    return createSOPaymentSchedule.value.reduce((s, r) => s + (parseFloat(r.invoice_portion) || 0), 0);
  }
  function soPaymentScheduleTotalAmount() {
    return createSOPaymentSchedule.value.reduce((s, r) => s + (parseFloat(r.payment_amount) || 0), 0);
  }
  function soItemTax(item) {
    return Math.round((parseFloat(item.amount) || 0) * ((parseFloat(item.tax_rate) || 0) / 100));
  }

  // ── Paste from Excel ────────────────────────────────────────────
  const soPasteToast = ref({ show: false, message: "", error: false });
  let _soPasteToastTimer = null;

  function _showSoPasteToast(message, error = false) {
    if (_soPasteToastTimer) clearTimeout(_soPasteToastTimer);
    soPasteToast.value = { show: true, message, error };
    _soPasteToastTimer = setTimeout(() => { soPasteToast.value.show = false; }, 3500);
  }

  function _parseExcelNum(s) {
    if (!s) return 0;
    let v = s.trim();
    // "1.234,56" → European decimal
    if (/\d\.\d{3},/.test(v)) v = v.replace(/\./g, "").replace(",", ".");
    else v = v.replace(/,/g, ""); // strip thousands commas
    return parseFloat(v.replace(/[^\d.\-]/g, "")) || 0;
  }

  function _pasteSOItemsFromText(text) {
    const isMaint = createSOForm.value.order_type === "Maintenance";
    const rawLines = text.replace(/\r\n/g, "\n").replace(/\r/g, "\n").trim().split("\n").filter(l => l.trim());
    if (!rawLines.length) return 0;

    // Only keep rows that have at least 2 tab characters (≥3 columns).
    // Single-cell lines are continuation fragments from multi-line Excel cells — skip them.
    const rows = rawLines
      .map(l => l.split("\t").map(s => s.trim()))
      .filter(r => r.length >= 3);

    if (!rows.length) return 0;

    // Detect STT (row-number) prefix column: if the first column of every row is a small integer,
    // shift all column indices by 1.
    const allFirstInts = rows.every(r => /^\d+$/.test(r[0]) && parseInt(r[0]) <= 9999);
    const offset = allFirstInts ? 1 : 0;

    // Column map (editable columns, calculated ones skipped):
    // DVVT:  [o+0]Mã [o+1]Tên [o+2]Mô tả [o+3]A-End [o+4]Z-End [o+5]ĐVT [o+6]SL [o+7]Đơn giá [o+8]CK% [o+9]Thuế suất
    // Maint: [o+0]Mã [o+1]Tên [o+2]Mô tả [o+3]ĐVT [o+4]SL [o+5]Đơn giá [o+6]CK% [o+7]Thuế suất
    const qtyIdx = offset + (isMaint ? 4 : 6);

    // Skip header row if qty column is not numeric
    const firstQty = (rows[0][qtyIdx] || "").replace(/[,\s]/g, "");
    const startIdx = (firstQty === "" || isNaN(parseFloat(firstQty))) ? 1 : 0;

    const newItems = [];
    const o = offset;
    for (let i = startIdx; i < rows.length; i++) {
      const c = rows[i];
      const item = _soBlankItem();
      if (isMaint) {
        item.item_code           = c[o + 0] || "";
        item.item_name           = c[o + 1] || "";
        item.description         = c[o + 2] || "";
        item.uom                 = c[o + 3] || "Cái";
        item.qty                 = _parseExcelNum(c[o + 4]) || 1;
        item.price_list_rate     = _parseExcelNum(c[o + 5]);
        item.discount_percentage = _parseExcelNum(c[o + 6]);
        item.tax_rate            = _parseExcelNum(c[o + 7]);
      } else {
        item.item_code           = c[o + 0] || "";
        item.item_name           = c[o + 1] || "";
        item.description         = c[o + 2] || "";
        item.a_end               = c[o + 3] || "";
        item.z_end               = c[o + 4] || "";
        item.uom                 = c[o + 5] || "Cái";
        item.qty                 = _parseExcelNum(c[o + 6]) || 1;
        item.price_list_rate     = _parseExcelNum(c[o + 7]);
        item.discount_percentage = _parseExcelNum(c[o + 8]);
        item.tax_rate            = _parseExcelNum(c[o + 9]);
      }
      if (!item.item_code && !item.item_name) continue;
      updateSOItemRate(item);
      newItems.push(item);
    }
    if (!newItems.length) return 0;

    // Replace the single blank placeholder row
    if (createSOItems.value.length === 1) {
      const only = createSOItems.value[0];
      if (!only.item_code && !only.item_name && !only.price_list_rate) {
        createSOItems.value = newItems;
        return newItems.length;
      }
    }
    createSOItems.value.push(...newItems);
    return newItems.length;
  }

  async function handleSOExcelPasteBtn() {
    try {
      const text = await navigator.clipboard.readText();
      if (!text.trim()) { _showSoPasteToast("Clipboard đang trống", true); return; }
      const count = _pasteSOItemsFromText(text);
      if (count > 0) _showSoPasteToast(`Đã dán ${count} dòng từ Excel`);
      else _showSoPasteToast("Không đọc được dữ liệu — kiểm tra định dạng cột", true);
    } catch {
      _showSoPasteToast("Không đọc được clipboard — hãy dùng Ctrl+V trên bảng", true);
    }
  }

  function onSOTablePaste(e) {
    const tag = (e.target || {}).tagName;
    if (tag === "INPUT" || tag === "SELECT" || tag === "TEXTAREA") return;
    const text = e.clipboardData?.getData("text") || "";
    if (!text.trim()) return;
    e.preventDefault();
    const count = _pasteSOItemsFromText(text);
    if (count > 0) _showSoPasteToast(`Đã dán ${count} dòng từ Excel`);
    else _showSoPasteToast("Không đọc được dữ liệu — kiểm tra định dạng cột", true);
  }
  // ────────────────────────────────────────────────────────────────

  function openCreateSO(customer, custDisplayName, opportunity, quotation) {
    soEditMode.value = false;
    soEditTarget.value = "";
    if (customer === undefined) customer = "";
    if (custDisplayName === undefined) custDisplayName = "";
    if (opportunity === undefined) opportunity = "";
    if (quotation === undefined) quotation = null;
    const today = new Date().toISOString().split("T")[0];
    createSOContext.value = {
      customer,
      customerName: custDisplayName,
      opportunity,
      quotation: quotation?.document?.name || "",
    };

    // Load form options async (non-blocking)
    call("get_so_form_options", { customer: customer || "" })
      .then((opts) => {
        soFormOptions.value = opts;
        soItemList.value = opts.items || [];
      })
      .catch(() => {});
    createSOForm.value = {
      customer,
      contact_person: "",
      opportunity,
      order_type: "Sales",
      transaction_date: today,
      delivery_date: "",
      po_no: "",
      po_date: "",
      contract_duration: "",
      contract_expiry: "",
      installation_zone: "",
      campaign: "",
      selling_price_list: "",
      currency: "VND",
      payment_terms_template: "",
      taxes_and_charges: "",
      territory: "",
      company: (frappe.defaults && frappe.defaults.get_user_default && frappe.defaults.get_user_default("Company")) || "",
      title: "",
      note: "",
      // Tình trạng
      execution_status: "Chưa thực hiện",
      revenue_recognition_date: today,
      revenue_status: "Bản nhập",
      payment_due_date: "",
      acceptance_date: "",
      // Địa chỉ
      billing_customer: customer,
      billing_address: "",
      billing_district: "",
      billing_ward: "",
      billing_street: "",
      billing_zipcode: "",
      shipping_recipient: "",
      shipping_address: "",
      shipping_district: "",
      shipping_ward: "",
      shipping_street: "",
      shipping_zipcode: "",
      warehouse: "",
      // Hợp đồng mua bán fields
      contract_type: "",
      order_category: "",
      order_value: 0,
      credit_days: 0,
      liquidation_value: 0,
      payment_cycle: "",
      production_deadline: "",
      // Thông tin hệ thống
      shared_flag: false,
      sync_price: false,
      referral_partner: "",
    };
    createSOItems.value = (quotation?.items || []).map((item) => ({
      ..._soBlankItem(),
      item_code: item.item_code || "",
      item_name: item.item_name || item.item_code || "",
      description: item.description || "",
      a_end: item.a_end || "",
      z_end: item.z_end || "",
      uom: item.uom || "Cái",
      qty: item.qty || 1,
      price_list_rate: item.price_list_rate || item.net_rate || 0,
      discount_percentage: item.discount_percentage || 0,
      rate: item.net_rate || item.price_list_rate || 0,
      amount: item.net_amount || 0,
      tax_rate: item.tax_rate || 0,
      prevdoc_docname: quotation?.document?.name || "",
    }));
    createSOPaymentSchedule.value = [_soBlankPaymentRow()];
    ctx.route.value = "create-sales-order";
    const url = new URL(window.location.href);
    url.hash = "";
    url.searchParams.set("view", "create-sales-order");
    if (customer) url.searchParams.set("customer", customer);
    else url.searchParams.delete("customer");
    url.searchParams.delete("opportunity");
    window.history.replaceState(window.history.state, "", url);
    window.sessionStorage.setItem("dcnet-crm-view", "create-sales-order");
    window.setTimeout(() => {
      document.querySelectorAll(".body-sidebar .standard-sidebar-item").forEach((item) => {
        item.classList.remove("active-sidebar");
      });
      const container = [...document.querySelectorAll(".body-sidebar .sidebar-item-container")]
        .find((item) => item.getAttribute("item-name") === "Đơn hàng");
      container?.querySelector(".standard-sidebar-item")?.classList.add("active-sidebar");
    }, 50);
  }

  function addSOItem() { createSOItems.value.push(_soBlankItem()); }
  function removeSOItem(idx) { createSOItems.value.splice(idx, 1); }
  function clearSOItems() { createSOItems.value = [_soBlankItem()]; }

  async function openSOItemPicker(target) {
    soItemPickerTarget.value = target === "goods-editor" ? "goods-editor" : "create";
    if (!soItemList.value.length) {
      if (soFormOptions.value.items?.length) {
        soItemList.value = soFormOptions.value.items;
      } else {
        try {
          const opts = await call("get_so_form_options", { customer: createSOContext.value.customer || "" });
          soFormOptions.value = opts;
          soItemList.value = opts.items || [];
        } catch {}
      }
    }
    soItemPickerSearch.value = "";
    soItemPickerPage.value = 1;
    soItemPickerSelected.value = [];
    soItemPickerCategoryFilter.value = "";
    soItemPickerOpen.value = true;
  }
  function closeSOItemPicker() {
    soItemPickerOpen.value = false;
    soItemPickerSelected.value = [];
  }
  function toggleSOItemPickerRow(name) {
    const idx = soItemPickerSelected.value.indexOf(name);
    if (idx >= 0) soItemPickerSelected.value.splice(idx, 1);
    else soItemPickerSelected.value.push(name);
  }
  function confirmSOItemPicker() {
    const toAdd = soItemPickerSelected.value
      .map((name) => soItemList.value.find((i) => i.name === name))
      .filter(Boolean);
    const targetRef = soItemPickerTarget.value === "goods-editor" ? soGoodsEditorItems : createSOItems;
    targetRef.value = targetRef.value.filter((i) => i.item_code || i.item_name);
    for (const item of toAdd) {
      if (!targetRef.value.find((r) => r.item_code === item.name)) {
        targetRef.value.push({
          ..._soBlankItem(),
          item_code: item.name,
          item_name: item.item_name || item.name,
          uom: item.stock_uom || "Cái",
        });
      }
    }
    if (!targetRef.value.length) targetRef.value = [_soBlankItem()];
    closeSOItemPicker();
  }

  function autoFillSOItemByCode(item) {
    const found = soFormOptions.value.items.find((i) => i.name === item.item_code);
    if (found) {
      if (!item.item_name) item.item_name = found.item_name || found.name;
      if (!item.uom || item.uom === "Cái") item.uom = found.stock_uom || "Cái";
    }
    if (createSOForm.value.order_type !== "Maintenance") {
      _loadSOEndpointSuggestions(item.item_code);
      autoFetchSOItemAccount(item);
    }
  }

  function updateSOItemAmount(item) {
    item.amount = Math.round((parseFloat(item.qty) || 0) * (parseFloat(item.rate) || 0));
  }

  function updateSOItemRate(item) {
    const plr = parseFloat(item.price_list_rate) || 0;
    const disc = parseFloat(item.discount_percentage) || 0;
    if (plr) item.rate = Math.round(plr * (1 - disc / 100));
    updateSOItemAmount(item);
  }

  function soItemPreTotal(item) {
    return Math.round((parseFloat(item.price_list_rate) || 0) * (parseFloat(item.qty) || 0));
  }
  function soItemDiscount(item) {
    return Math.round(soItemPreTotal(item) * ((parseFloat(item.discount_percentage) || 0) / 100));
  }
  function soSubtotal() {
    return createSOItems.value.reduce((s, i) => s + soItemPreTotal(i), 0);
  }
  function soTotalDiscount() {
    return createSOItems.value.reduce((s, i) => s + soItemDiscount(i), 0);
  }
  function soGrandTotal() {
    return createSOItems.value.reduce((s, i) => s + (parseFloat(i.amount) || 0), 0);
  }
  function soTotalQty() {
    return createSOItems.value.reduce((s, i) => s + (parseFloat(i.qty) || 0), 0);
  }

  async function saveCreateSO() {
    if (createSOSaving.value) return;
    if (!createSOForm.value.customer) { frappe.msgprint("Vui lòng chọn khách hàng."); return; }
    if (!createSOForm.value.transaction_date) { frappe.msgprint("Vui lòng nhập ngày đặt hàng."); return; }
    const validItems = createSOItems.value.filter(i => i.item_code && i.qty > 0);
    if (!validItems.length) { frappe.msgprint("Vui lòng thêm ít nhất một sản phẩm."); return; }
    createSOSaving.value = true;
    try {
      if (soEditMode.value) {
        // ── Edit existing SO ─────────────────────────────────────
        await call("update_sales_order", {
          name: soEditTarget.value,
          data: { ...createSOForm.value, items: validItems },
        }, "POST");
        frappe.show_alert({ message: `Đã cập nhật đơn hàng ${soEditTarget.value}`, indicator: "green" }, 5);
        const name = soEditTarget.value;
        soEditMode.value = false;
        soEditTarget.value = "";
        ctx.route.value = "order-detail";
        const url = new URL(window.location.href);
        url.hash = "";
        url.searchParams.set("view", "order-detail");
        url.searchParams.set("order", name);
        url.searchParams.delete("customer");
        url.searchParams.delete("opportunity");
        window.history.replaceState(window.history.state, "", url);
        window.sessionStorage.setItem("dcnet-crm-view", "order-detail");
        await loadOrderDetail(name);
      } else {
        // ── Create new SO ─────────────────────────────────────────
        const result = await call("create_sales_order", {
          data: { ...createSOForm.value, items: validItems },
        }, "POST");
        frappe.show_alert({ message: `Đã tạo đơn hàng ${result.name}`, indicator: "green" }, 5);
        if (createSOContext.value.customer) {
          ctx.customerName.value = createSOContext.value.customer;
          ctx.route.value = "customer-detail";
          const url = new URL(window.location.href);
          url.hash = "";
          url.searchParams.set("view", "customer-detail");
          url.searchParams.set("customer", createSOContext.value.customer);
          url.searchParams.delete("opportunity");
          window.history.replaceState(window.history.state, "", url);
          window.sessionStorage.setItem("dcnet-crm-view", "customer-detail");
          await ctx.loadCustomerDetail(createSOContext.value.customer);
        } else {
          ctx.route.value = "orders";
          const url = new URL(window.location.href);
          url.hash = "";
          url.searchParams.set("view", "orders");
          url.searchParams.delete("customer");
          url.searchParams.delete("opportunity");
          window.history.replaceState(window.history.state, "", url);
          window.sessionStorage.setItem("dcnet-crm-view", "orders");
        }
      }
    } catch (error) {
      frappe.msgprint(error.message || "Không thể lưu đơn hàng.");
    } finally {
      createSOSaving.value = false;
    }
  }

  function soRevenueStatusClass(status) {
    const map = {
      "Bản nhập": "draft",
      "Bản nháp": "draft",
      "Đơn nháp": "draft",
      "Đề nghị ghi": "pending",
      "Đã ghi": "done",
      "Từ chối ghi": "rejected",
      "Hủy": "cancelled",
    };
    return map[status] || "draft";
  }

  function soDeliveryStatusClass(status) {
    const map = {
      "Fully Delivered": "done",
      "Partly Delivered": "partial",
      "Not Delivered": "draft",
      "Closed": "done",
    };
    return map[status] || "draft";
  }

  // ── Detail view toggle ──────────────────────────────────────────
  const soDetailShowEmpty = ref(true);
  const soCurrentUser = ref(
    (typeof frappe !== "undefined" && frappe.session && (frappe.session.user_fullname || frappe.session.user)) || ""
  );

  // ── Layout configurator (Sửa bố cục) ────────────────────────────
  const SO_LAYOUT_KEY = "dcnet-crm-so-layout";
  const SO_LAYOUT_DEFAULTS = { mo_ta: true, tinh_trang: true, hoa_don: true, giao_hang: true };

  function _loadSOLayout() {
    try {
      const saved = JSON.parse(localStorage.getItem(SO_LAYOUT_KEY) || "null");
      if (saved && typeof saved === "object") return { ...SO_LAYOUT_DEFAULTS, ...saved };
    } catch {}
    return { ...SO_LAYOUT_DEFAULTS };
  }

  const soLayoutOpen = ref(false);
  const soVisibleSections = ref(_loadSOLayout());

  function openSOLayout() { soLayoutOpen.value = true; }
  function closeSOLayout() { soLayoutOpen.value = false; }
  function toggleSOSection(key) {
    soVisibleSections.value[key] = !soVisibleSections.value[key];
    try { localStorage.setItem(SO_LAYOUT_KEY, JSON.stringify(soVisibleSections.value)); } catch {}
  }
  function resetSOLayout() {
    soVisibleSections.value = { ...SO_LAYOUT_DEFAULTS };
    try { localStorage.removeItem(SO_LAYOUT_KEY); } catch {}
  }

  // ── Order detail: "Thông tin tóm tắt" field customize (Tùy chỉnh tóm tắt) ─
  const orderSummaryFields = ref(readOrderSummaryFields());
  const orderSummaryDialogOpen = ref(false);
  const orderSummarySearch = ref("");
  const orderSummaryDraft = ref([]);

  const availableOrderSummaryFields = computed(() => {
    const keyword = orderSummarySearch.value.trim().toLocaleLowerCase("vi");
    return ORDER_SUMMARY_FIELDS.filter((item) => (
      !orderSummaryDraft.value.includes(item.field)
      && (!keyword || item.label.toLocaleLowerCase("vi").includes(keyword))
    ));
  });
  const selectedOrderSummaryFields = computed(() => orderSummaryDraft.value
    .map((field) => ORDER_SUMMARY_FIELDS.find((item) => item.field === field))
    .filter(Boolean));
  const visibleOrderSummaryFields = computed(() => orderSummaryFields.value
    .map((field) => ORDER_SUMMARY_FIELDS.find((item) => item.field === field))
    .filter(Boolean));

  function orderSummaryValue(field) {
    const definition = ORDER_SUMMARY_FIELDS.find((item) => item.field === field);
    const document = orderDetail.value?.document || {};
    let value = document[field];

    if (definition?.format === "date" && value) {
      try {
        value = window.frappe?.datetime?.str_to_user?.(value) || value;
      } catch (_) {
        // Keep the server value when Frappe's date formatter cannot parse it.
      }
    }
    if (definition?.format === "datetime" && value) {
      try {
        value = window.frappe?.datetime?.str_to_user?.(value, true) || value;
      } catch (_) {
        // Keep the server value when Frappe's date formatter cannot parse it.
      }
    }
    if (definition?.format === "currency" && value !== null && value !== undefined && value !== "") {
      value = new Intl.NumberFormat("vi-VN", { maximumFractionDigits: 2 }).format(Number(value) || 0);
    }
    if (definition?.format === "percent" && value !== null && value !== undefined && value !== "") {
      value = `${Number(value) || 0}%`;
    }
    if (value === 0) return "0";
    if (value === false) return "Không";
    return value || definition?.empty || "—";
  }

  function openOrderSummaryDialog() {
    orderSummaryDraft.value = [...orderSummaryFields.value];
    orderSummarySearch.value = "";
    orderSummaryDialogOpen.value = true;
  }

  function cancelOrderSummaryDialog() {
    orderSummaryDialogOpen.value = false;
    orderSummarySearch.value = "";
    orderSummaryDraft.value = [];
  }

  function addOrderSummaryField(field) {
    if (!orderSummaryDraft.value.includes(field)) orderSummaryDraft.value.push(field);
  }

  function removeOrderSummaryField(field) {
    orderSummaryDraft.value = orderSummaryDraft.value.filter((item) => item !== field);
  }

  function resetOrderSummaryFields() {
    orderSummaryDraft.value = [...DEFAULT_ORDER_SUMMARY_FIELDS];
  }

  function saveOrderSummaryFields() {
    orderSummaryFields.value = [...orderSummaryDraft.value];
    window.localStorage.setItem(orderSummaryStorageKey(), JSON.stringify(orderSummaryFields.value));
    cancelOrderSummaryDialog();
  }

  // ── Orders list filter state ────────────────────────────────────
  const soFilterOpen = ref(true);
  const soItemsPanelVisible = ref(true);
  const soSavedFilterActive = ref("");
  const ordersEnabledFilters = ref([]);
  const ordersFilterValues = ref({});

  const SO_SAVED_FILTERS = [
    { key: "order_month", label: "Đặt hàng tháng này" },
    { key: "order_week", label: "Đặt hàng tuần này" },
    { key: "revenue_month", label: "Ghi số tháng này" },
    { key: "revenue_week", label: "Ghi số tuần này" },
  ];

  const SO_FILTER_CRITERIA = [
    { field: "custom_revenue_status", label: "Tình trạng ghi doanh số" },
    { field: "name", label: "Số đơn hàng/HĐ" },
    { field: "title", label: "Diễn giải" },
    { field: "transaction_date", label: "Ngày đặt hàng" },
    { field: "custom_revenue_recognition_date", label: "Ngày ghi số" },
    { field: "owner", label: "Người thực hiện" },
    { field: "company", label: "Đơn vị" },
    { field: "delivery_status", label: "Tình trạng giao hàng" },
  ];

  const soSavedFilterDates = computed(() => {
    const key = soSavedFilterActive.value;
    if (!key) return {};
    const now = new Date();
    const y = now.getFullYear();
    const m = String(now.getMonth() + 1).padStart(2, "0");
    const dow = now.getDay();
    const monday = new Date(now);
    monday.setDate(now.getDate() - ((dow + 6) % 7));
    const mondayStr = monday.toISOString().split("T")[0];
    const monthStart = `${y}-${m}-01`;
    if (key === "order_month") return { transaction_date: [">=", monthStart] };
    if (key === "order_week") return { transaction_date: [">=", mondayStr] };
    if (key === "revenue_month") return { custom_revenue_recognition_date: [">=", monthStart] };
    if (key === "revenue_week") return { custom_revenue_recognition_date: [">=", mondayStr] };
    return {};
  });

  function activateSavedFilter(key) {
    soSavedFilterActive.value = soSavedFilterActive.value === key ? "" : key;
    ctx.loadRows();
  }

  function toggleOrdersFilter(field) {
    const idx = ordersEnabledFilters.value.indexOf(field);
    if (idx >= 0) {
      ordersEnabledFilters.value.splice(idx, 1);
      const vals = { ...ordersFilterValues.value };
      delete vals[field];
      ordersFilterValues.value = vals;
    } else {
      ordersEnabledFilters.value.push(field);
    }
    ctx.loadRows();
  }

  return {
    soDetailItems, soDetailLoading, loadSODetail,
    soExpandedItem, toggleSODetailItem,
    orderDetailName, orderDetail, orderDetailTab, orderDetailEditing,
    orderRelatedSection, orderRelatedSectionLabel,
    orderCashflowSection, orderCashflowSectionLabel, orderActualReceipts, orderActualPayments,
    soSideCollapsed, toggleSOSidePanel,
    orderSupportSection, orderSupportSectionLabel, openSOWarrantyClaimDialog, notifyOrderConsultCardUnavailable, notifyOrderAction,
    orderOtherSection, orderOtherSectionLabel, orderRevenueRequestStatusLabel,
    soContactDialogOpen, soContactForm, soContactSaving, openSOContactDialog, closeSOContactDialog, saveSOContact,
    soContactPickerOpen, soContactPickerSearch, soContactPickerRows, soContactPickerLoading, openSOContactPicker, searchSOContacts, linkSOContact,
    orderActivityDialogOpen, orderActivitySaving, orderActivityForm,
    orderActivityPage, orderActivityPageLength, orderActivityPageCount, orderActivityPageStart, orderActivityPageEnd,
    visibleOrderActivities, changeOrderActivityPage, openOrderActivityDialog, saveOrderActivity,
    orderActivityTypeLabel, orderActivityStatusLabel,
    soPlannedExpenses, soPlannedExpensesLoading, loadSOPlannedExpenses,
    soPlannedExpenseDialogOpen, soPlannedExpenseSaving, soPlannedExpenseForm,
    openSOPlannedExpenseDialog, closeSOPlannedExpenseDialog, saveSOPlannedExpense,
    soOrgPickerOpen, soOrgTree, openSOOrgPicker, closeSOOrgPicker, toggleOrgNode, selectSOOrgNode,
    orderDetailSaving, orderDetailForm, orderDetailComment,
    orderNoteSection, soAttachUploading, uploadSOFile, addSOAttachmentLink, deleteSOAttachment,
    soItemDescExpanded, toggleSOItemDesc,
    formatSOAddress,
    soGoodsEditorOpen, soGoodsEditorSaving, soGoodsEditorItems,
    openSOGoodsEditor, closeSOGoodsEditor,
    addSOGoodsEditorItem, removeSOGoodsEditorItem, clearSOGoodsEditorItems,
    autoFillSOGoodsEditorItem, soGoodsEditorRowAmount,
    soGoodsEditorTotalQty, soGoodsEditorTotalAmount, saveSOGoodsEditor,
    soStockLookupOpen, soStockLookupLoading, soStockLookupItems, soStockLookupExpanded,
    openSOStockLookup, closeSOStockLookup, toggleSOStockLookupRow,
    soEditMode, soEditTarget, openEditSO, cancelEditSO,
    loadOrderDetail, openOrderDetail, backToOrders, orderDetailTotalQty,
    orderDetailTotalDelivered, orderDetailTotalTax,
    saveOrderDetailComment, startOrderDetailEdit, cancelOrderDetailEdit, saveOrderDetailEdit,
    soRevenueStatusClass, soDeliveryStatusClass,
    createSOContext, createSOSaving, createSOForm, createSOItems,
    soFormOptions, onSOCustomerChange,
    openCreateSO, addSOItem, removeSOItem, clearSOItems,
    updateSOItemAmount, updateSOItemRate, autoFillSOItemByCode,
    soItemPreTotal, soItemDiscount,
    soSubtotal, soTotalDiscount, soGrandTotal, soTotalQty,
    soItemTax, saveCreateSO,
    createSOPaymentSchedule, addSOPaymentRow, removeSOPaymentRow,
    soPaymentScheduleTotal, soPaymentScheduleTotalAmount,
    soItemPickerOpen, soItemPickerSearch, soItemPickerPage, soItemPickerPageLength,
    soItemPickerSelected, soItemPickerCategoryFilter, soItemList,
    soItemPickerFiltered, soItemPickerPageCount, soItemPickerRows, soItemPickerCategories,
    openSOItemPicker, closeSOItemPicker, toggleSOItemPickerRow, confirmSOItemPicker,
    soActionMenuOpen, soActionSaving, toggleSOActionMenu, closeSOActionMenu,
    soActionModalOpen, soActionModalForm, soActionModalSaving,
    soActionModalUserQuery, soActionModalUserDropdown, soActionModalUserDdOpen,
    soActionModalTtOpen, soActionModalTtQuery, soActionModalFilteredTt,
    openSOActionModal, closeSOActionModal, confirmSOActionModal,
    printSalesOrder, soDocumentGenerating, openOrderCustomer,
    soPrintDialogOpen, soPrintTemplatesLoading, soPrintTemplates, soPrintActionTemplate,
    soPrintPreviewOpen, soPrintPreviewHtml, soPrintPreviewTitle,
    closeSalesOrderPrintDialog, downloadSalesOrderTemplate, previewSalesOrderTemplate, deleteSalesOrderPrintTemplate,
    closeSalesOrderPrintPreview, printSalesOrderTemplate, printSalesOrderPreview,
    openSalesOrderTemplateBuilder,
    requestSOApproval, requestSORevenueRecognition,
    withdrawSORevenueRecognition, soRevenueRequestSaving,
    soActionModalOnUserFocus, soActionModalOnUserInput,
    soActionModalIsUserSel, soActionModalToggleUser, soActionModalRemoveUser, soActionModalCloseUserDd,
    soActionModalToggleTt, soActionModalSelectTt, soActionModalCloseTt,
    soDetailShowEmpty, soCurrentUser,
    soPasteToast, handleSOExcelPasteBtn, onSOTablePaste,
    soAEndOptions, soZEndOptions, autoFetchSOItemAccount,
    soLayoutOpen, soVisibleSections, openSOLayout, closeSOLayout, toggleSOSection, resetSOLayout,
    orderSummaryFields, orderSummaryDialogOpen, orderSummarySearch, orderSummaryDraft,
    availableOrderSummaryFields, selectedOrderSummaryFields, visibleOrderSummaryFields, orderSummaryValue,
    openOrderSummaryDialog, cancelOrderSummaryDialog, addOrderSummaryField, removeOrderSummaryField,
    resetOrderSummaryFields, saveOrderSummaryFields,
    soFilterOpen, soItemsPanelVisible, soSavedFilterActive,
    ordersEnabledFilters, ordersFilterValues, soSavedFilterDates,
    SO_SAVED_FILTERS, SO_FILTER_CRITERIA,
    activateSavedFilter, toggleOrdersFilter, exportResource,
  };
}
