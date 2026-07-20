import { computed, ref } from "vue/dist/vue.esm-bundler.js";
import { CONTACT_COLUMNS } from "../../constants.js";

const CONTACT_VIEWS_STORAGE_KEY = "dcnet-crm-contact-views-v1";
const CONTACT_ACTIVE_VIEW_STORAGE_KEY = "dcnet-crm-contact-active-view-v1";
const DEFAULT_CONTACT_FIELDS = CONTACT_COLUMNS.map((item) => item.field);
const DEFAULT_CONTACT_VIEWS = [
  {
    id: "all",
    name: "Tất cả liên hệ",
    scope: "all",
    fields: DEFAULT_CONTACT_FIELDS,
    summary_fields: ["total"],
    sort_field: "modified",
    sort_direction: "desc",
    built_in: true,
  },
  {
    id: "mine",
    name: "Liên hệ của tôi",
    scope: "mine",
    fields: DEFAULT_CONTACT_FIELDS,
    summary_fields: ["total"],
    sort_field: "modified",
    sort_direction: "desc",
    built_in: true,
  },
];

function cloneView(view) {
  return {
    ...view,
    fields: [...(view.fields || [])],
    summary_fields: [...(view.summary_fields || [])],
  };
}

export function useContacts(ctx) {
  const contactMoreOpen = ref(false);
  const contactExporting = ref(false);
  const contactActivityOpen = ref(true);
  const contactFilterOpen = ref(true);
  const contactListTab = ref("activity");
  const contactVisibleFields = ref(CONTACT_COLUMNS.map((item) => item.field));
  const contactEnabledFilters = ref([]);
  const contactFilterValues = ref({});
  const contactViewMenuOpen = ref(false);
  const contactViewEditorOpen = ref(false);
  const contactViewSearch = ref("");
  const contactViews = ref(loadContactViews());
  const savedActiveView = window.localStorage.getItem(CONTACT_ACTIVE_VIEW_STORAGE_KEY);
  const contactListView = ref(contactViews.value.some((view) => view.id === savedActiveView) ? savedActiveView : "all");
  const contactViewDraft = ref(cloneView(contactViews.value[0]));

  const currentContactView = computed(() =>
    contactViews.value.find((view) => view.id === contactListView.value) || contactViews.value[0]
  );
  const contactListViewLabel = computed(() => currentContactView.value?.name || "Tất cả liên hệ");
  const contactViewSummaryFields = computed(() => currentContactView.value?.summary_fields || ["total"]);
  const contactActivityItems = computed(() => {
    const detail = ctx.detail.value || {};
    const notes = (detail.notes || []).map((row) => ({
      ...row,
      activity_key: `note-${row.name}`,
      activity_type: "comment",
      content: row.content || "",
      actor: row.comment_by_fullname || row.comment_by || "",
      activity_date: row.creation || "",
    }));
    const activities = (detail.activities || []).map((row) => ({
      ...row,
      activity_key: `activity-${row.activity_type || "item"}-${row.name}`,
      content: row.description || row.subject || "",
      actor: row.performed_by_name || row.performed_by || row.allocated_to || row.owner || "",
      activity_date: row.due_date || row.starts_on || row.creation || row.modified || "",
    }));
    return [...notes, ...activities].sort((left, right) =>
      String(right.activity_date || "").localeCompare(String(left.activity_date || ""))
    );
  });
  const contactPurchaseRecords = computed(() => {
    const detail = ctx.detail.value || {};
    const records = [
      ...(detail.quotations || []).map((row) => ({
        ...row,
        record_doctype: "Quotation",
        record_type: "Báo giá",
        record_icon: "quotation",
        record_date: row.transaction_date || row.modified || "",
        record_amount: row.grand_total,
        record_status: row.status,
        record_description: row.title || "",
      })),
      ...(detail.opportunities || []).map((row) => ({
        ...row,
        record_doctype: "Opportunity",
        record_type: "Cơ hội",
        record_icon: "opportunity",
        record_date: row.expected_closing || row.modified || "",
        record_amount: row.opportunity_amount,
        record_status: row.sales_stage || row.status,
        record_description: row.title || "",
      })),
      ...(detail.orders || []).map((row) => ({
        ...row,
        record_doctype: "Sales Order",
        record_type: "Đơn hàng",
        record_icon: "order",
        record_date: row.transaction_date || row.modified || "",
        record_amount: row.grand_total,
        record_status: row.status,
        record_description: row.customer_name || "",
      })),
      ...(detail.invoices || []).map((row) => ({
        ...row,
        record_doctype: "Sales Invoice",
        record_type: "Hóa đơn",
        record_icon: "document",
        record_date: row.posting_date || row.modified || "",
        record_amount: row.grand_total,
        record_status: row.status,
        record_description: row.customer_name || "",
      })),
    ];
    return records.sort((left, right) =>
      String(right.record_date || "").localeCompare(String(left.record_date || ""))
    );
  });

  function loadContactViews() {
    try {
      const stored = JSON.parse(window.localStorage.getItem(CONTACT_VIEWS_STORAGE_KEY) || "[]");
      if (!Array.isArray(stored)) return DEFAULT_CONTACT_VIEWS.map(cloneView);
      const storedById = new Map(stored.filter((view) => view?.id).map((view) => [view.id, view]));
      const builtIns = DEFAULT_CONTACT_VIEWS.map((view) => cloneView(storedById.get(view.id) || view));
      const custom = stored.filter((view) => view?.id && !DEFAULT_CONTACT_VIEWS.some((item) => item.id === view.id));
      return [...builtIns, ...custom.map(cloneView)];
    } catch {
      return DEFAULT_CONTACT_VIEWS.map(cloneView);
    }
  }

  function persistContactViews() {
    window.localStorage.setItem(CONTACT_VIEWS_STORAGE_KEY, JSON.stringify(contactViews.value));
  }

  function applyContactView(view) {
    if (!view) return;
    const validFields = new Set(CONTACT_COLUMNS.map((column) => column.field));
    const fields = (view.fields || []).filter((field) => validFields.has(field));
    contactVisibleFields.value = fields.length ? fields : [...DEFAULT_CONTACT_FIELDS];
  }

  function selectContactListView(id) {
    if (id === "team") {
      frappe.msgprint({
        title: "Cần cấu hình",
        message: "Cần clarify với khách hàng về mô hình nhóm nhân viên phụ trách trước khi bật giao diện này.",
        indicator: "orange",
      });
      return;
    }
    const view = contactViews.value.find((item) => item.id === id);
    if (!view) return;
    contactListView.value = id;
    window.localStorage.setItem(CONTACT_ACTIVE_VIEW_STORAGE_KEY, id);
    contactViewMenuOpen.value = false;
    applyContactView(view);
    ctx.loadRows();
  }

  function openContactViewEditor(createNew = false) {
    const source = createNew
      ? {
          id: `custom-${Date.now()}`,
          name: "Giao diện mới",
          scope: "all",
          fields: [...DEFAULT_CONTACT_FIELDS],
          summary_fields: ["total"],
          sort_field: "modified",
          sort_direction: "desc",
          built_in: false,
        }
      : currentContactView.value;
    contactViewDraft.value = cloneView(source);
    contactViewSearch.value = "";
    contactViewMenuOpen.value = false;
    contactViewEditorOpen.value = true;
  }

  function cancelContactViewEditor() {
    contactViewEditorOpen.value = false;
    contactViewSearch.value = "";
  }

  function addContactViewField(field) {
    if (!contactViewDraft.value.fields.includes(field)) {
      contactViewDraft.value.fields.push(field);
    }
  }

  function removeContactViewField(field) {
    if (field === "full_name") {
      frappe.show_alert({ message: "Họ và tên là cột bắt buộc.", indicator: "orange" });
      return;
    }
    contactViewDraft.value.fields = contactViewDraft.value.fields.filter((item) => item !== field);
  }

  function moveContactViewField(field, direction) {
    const fields = [...contactViewDraft.value.fields];
    const index = fields.indexOf(field);
    const nextIndex = index + direction;
    if (index < 0 || nextIndex < 0 || nextIndex >= fields.length) return;
    [fields[index], fields[nextIndex]] = [fields[nextIndex], fields[index]];
    contactViewDraft.value.fields = fields;
  }

  function toggleContactViewSummary(field) {
    const fields = contactViewDraft.value.summary_fields || [];
    contactViewDraft.value.summary_fields = fields.includes(field)
      ? fields.filter((item) => item !== field)
      : [...fields, field];
  }

  function saveContactView() {
    const name = String(contactViewDraft.value.name || "").trim();
    if (!name) {
      frappe.msgprint({ title: "Thiếu thông tin", message: "Tên giao diện là bắt buộc.", indicator: "orange" });
      return;
    }
    if (!contactViewDraft.value.fields.includes("full_name")) {
      frappe.msgprint({ title: "Thiếu cột bắt buộc", message: "Giao diện phải có cột Họ và tên.", indicator: "orange" });
      return;
    }
    const saved = cloneView({ ...contactViewDraft.value, name });
    const index = contactViews.value.findIndex((view) => view.id === saved.id);
    if (index >= 0) contactViews.value.splice(index, 1, saved);
    else contactViews.value.push(saved);
    persistContactViews();
    contactListView.value = saved.id;
    window.localStorage.setItem(CONTACT_ACTIVE_VIEW_STORAGE_KEY, saved.id);
    applyContactView(saved);
    contactViewEditorOpen.value = false;
    ctx.loadRows();
    frappe.show_alert({ message: "Đã lưu giao diện liên hệ.", indicator: "green" });
  }

  function duplicateContactView() {
    contactViewDraft.value = cloneView({
      ...contactViewDraft.value,
      id: `custom-${Date.now()}`,
      name: `${String(contactViewDraft.value.name || "Giao diện").trim()} - Bản sao`,
      built_in: false,
    });
    saveContactView();
  }

  function toggleContactFilter(field) {
    const fields = contactEnabledFilters.value;
    contactEnabledFilters.value = fields.includes(field)
      ? fields.filter((item) => item !== field)
      : [...fields, field];
    if (!contactEnabledFilters.value.includes(field)) {
      delete contactFilterValues.value[field];
      ctx.loadRows();
    }
  }

  function importContacts() {
    frappe.new_doc("Data Import", { reference_doctype: "Contact", import_type: "Insert New Records" });
  }

  function buildContactFilters() {
    const filters = {};
    // Liên hệ chỉ là người đại diện của khách hàng — loại bỏ Contact mà Frappe
    // tự sinh ra khi tạo User (tài khoản đăng nhập hệ thống, không phải liên hệ KH)
    filters.user = ["is", "not set"];
    if (currentContactView.value?.scope === "mine") {
      filters.owner = ctx.boot.value?.user;
    }
    contactEnabledFilters.value.forEach((field) => {
      const value = contactFilterValues.value[field];
      if (value === undefined || value === null || value === "") return;
      filters[field] = ["salutation", "company_name", "department", "status"].includes(field)
        ? value
        : ["like", `%${value}%`];
    });
    return filters;
  }

  async function exportContacts() {
    if (contactExporting.value) return;
    contactExporting.value = true;
    try {
      const params = new URLSearchParams({
        search: ctx.search.value || "",
        filters: JSON.stringify(buildContactFilters()),
        fields: JSON.stringify(contactVisibleFields.value),
        sort_field: currentContactView.value?.sort_field || "",
        sort_direction: currentContactView.value?.sort_direction || "",
      });
      const response = await window.fetch(
        `/api/method/dcnet_crm.api.export_contacts?${params.toString()}`,
        { credentials: "same-origin" }
      );
      if (!response.ok) {
        let message = "Không thể xuất danh sách liên hệ.";
        try {
          const payload = await response.json();
          const serverMessages = JSON.parse(payload._server_messages || "[]");
          message = serverMessages[0]?.message || payload.message || message;
        } catch {
          // Keep the user-facing fallback when the server does not return JSON.
        }
        throw new Error(message);
      }

      const blob = await response.blob();
      const disposition = response.headers.get("content-disposition") || "";
      const filenameMatch = disposition.match(/filename="?([^";]+)"?/i);
      const filename = filenameMatch?.[1] || "danh_sach_lien_he.xlsx";
      const objectUrl = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = objectUrl;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(objectUrl);
      frappe.show_alert({ message: "Đã xuất danh sách liên hệ.", indicator: "green" });
    } catch (error) {
      frappe.msgprint({
        title: "Xuất Excel không thành công",
        message: error.message || "Không thể xuất danh sách liên hệ.",
        indicator: "red",
      });
    } finally {
      contactExporting.value = false;
    }
  }

  applyContactView(currentContactView.value);

  return {
    contactMoreOpen, contactExporting, contactActivityOpen, contactFilterOpen, contactListTab,
    contactVisibleFields, contactEnabledFilters, contactFilterValues,
    contactViewMenuOpen, contactViewEditorOpen, contactListView, contactViewSearch,
    contactViews, contactViewDraft, currentContactView, contactListViewLabel, contactViewSummaryFields,
    contactActivityItems, contactPurchaseRecords,
    toggleContactFilter, importContacts,
    buildContactFilters, exportContacts,
    selectContactListView, openContactViewEditor, cancelContactViewEditor,
    addContactViewField, removeContactViewField, moveContactViewField,
    toggleContactViewSummary, saveContactView, duplicateContactView,
  };
}
