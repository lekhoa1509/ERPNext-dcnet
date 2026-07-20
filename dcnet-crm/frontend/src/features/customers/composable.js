import { ref, computed, watch } from "vue/dist/vue.esm-bundler.js";
import { call, exportResource } from "../../utils.js";
import { CUSTOMER_COLUMNS } from "../../constants.js";
import { fetchVnProvinces, fetchVnWards } from "../../utils-vn-address.js";

const CUSTOMER_SUMMARY_FIELDS = [
  { field: "name", label: "Mã khách hàng", source: "document" },
  { field: "customer_name", label: "Tên khách hàng", source: "customer" },
  { field: "ten_viet_tat", label: "Tên viết tắt", source: "customer" },
  { field: "tax_id", label: "Mã số thuế", source: "customer" },
  { field: "phone", label: "Điện thoại", source: "derived" },
  { field: "email", label: "Email", source: "derived" },
  { field: "customer_type", label: "Loại khách hàng", source: "customer", empty: "- Không chọn -" },
  { field: "customer_group", label: "Nhóm khách hàng", source: "customer", empty: "- Không chọn -" },
  { field: "nguon_goc", label: "Nguồn gốc", source: "customer", empty: "- Không chọn -" },
  { field: "territory", label: "Khu vực", source: "customer", empty: "- Không chọn -" },
  { field: "industry", label: "Lĩnh vực", source: "customer", empty: "- Không chọn -" },
  { field: "nganh_nghe", label: "Ngành nghề", source: "customer", empty: "- Không chọn -" },
  { field: "loai_hinh", label: "Loại hình", source: "customer", empty: "- Không chọn -" },
  { field: "market_segment", label: "Phân khúc", source: "customer", empty: "- Không chọn -" },
  { field: "default_price_list", label: "Bảng giá", source: "customer", empty: "- Không chọn -" },
  { field: "account_manager", label: "Người phụ trách", source: "customer" },
  { field: "website", label: "Website", source: "customer" },
  { field: "address_title", label: "Tên địa chỉ", source: "address" },
  { field: "address_type", label: "Loại địa chỉ", source: "address", empty: "- Không chọn -" },
  { field: "address_line1", label: "Số nhà, đường phố", source: "address" },
  { field: "state", label: "Tỉnh/Thành phố", source: "address", empty: "- Không chọn -" },
  { field: "county", label: "Phường/Xã", source: "address", empty: "- Không chọn -" },
  { field: "city", label: "Quận/Huyện", source: "address", empty: "- Không chọn -" },
  { field: "country", label: "Quốc gia", source: "address", empty: "- Không chọn -" },
  { field: "pincode", label: "Mã vùng", source: "address" },
  { field: "billing_phone", label: "Điện thoại hóa đơn", source: "address", sourceField: "phone" },
  { field: "tai_khoan_ngan_hang", label: "Tài khoản ngân hàng", source: "customer" },
  { field: "mo_tai_ngan_hang", label: "Mở tại ngân hàng", source: "customer" },
  { field: "ngay_thanh_lap", label: "Ngày thành lập/Ngày sinh", source: "customer", format: "date" },
  { field: "la_kh_tu", label: "Là khách hàng từ", source: "customer", format: "date" },
  { field: "quy_mo_doanh_thu", label: "Doanh thu", source: "customer", empty: "- Không chọn -" },
  { field: "quy_mo_nhan_su", label: "Quy mô nhân sự", source: "customer", empty: "- Không chọn -" },
  { field: "loai_han_muc_no", label: "Loại hạn mức nợ", source: "customer", empty: "- Không chọn -" },
  { field: "outstanding", label: "Công nợ", source: "summary", format: "currency" },
  { field: "so_ngay_duoc_no", label: "Loại điều khoản thanh toán", source: "customer" },
  { field: "first_order_date", label: "Ngày mua hàng đầu tiên", source: "derived", format: "date" },
  { field: "last_order_date", label: "Ngày mua hàng gần nhất", source: "derived", format: "date" },
  { field: "order_count", label: "Số lượng đơn hàng", source: "summary" },
  { field: "order_value", label: "Doanh số đơn hàng", source: "summary", format: "currency" },
  { field: "customer_details", label: "Mô tả", source: "customer" },
];
const DEFAULT_CUSTOMER_SUMMARY_FIELDS = ["tax_id", "phone", "industry", "quy_mo_doanh_thu"];

function customerSummaryStorageKey() {
  return `dcnet-crm-customer-summary-fields:${window.frappe?.session?.user || "Guest"}`;
}

function readCustomerSummaryFields() {
  try {
    const stored = JSON.parse(window.localStorage.getItem(customerSummaryStorageKey()));
    if (!Array.isArray(stored)) return [...DEFAULT_CUSTOMER_SUMMARY_FIELDS];
    const allowed = new Set(CUSTOMER_SUMMARY_FIELDS.map((item) => item.field));
    return [...new Set(stored.filter((field) => allowed.has(field)))];
  } catch (_) {
    return [...DEFAULT_CUSTOMER_SUMMARY_FIELDS];
  }
}

export function useCustomers(ctx) {
  const customerTab = ref("activity");
  const customerDetailTab = ref("overview");
  const customerSalesSection = ref("orders");
  const customerSupportSection = ref("consult_cards");
  const customerMarketingSection = ref("campaigns");
  const customerNoteSection = ref("notes");
  const customerInlineNote = ref("");
  const customerConversationText = ref("");
  const customerAttachUploading = ref(false);
  const customerName = ref("");
  const customerEditing = ref(false);
  const customerSaving = ref(false);
  const detailFieldSearch = ref("");
  const showEmptyDetailFields = ref(true);
  const customerForm = ref({ customer: {}, contact: {}, address: {} });
  const contactDialogOpen = ref(false);
  const contactDialogMode = ref("quick");
  const contactSaving = ref(false);
  const contactPickerOpen = ref(false);
  const contactPickerLoading = ref(false);
  const contactPickerSearch = ref("");

  // ── VN Address cascade (edit mode) ──────────────────────────────
  const editVnProvinces = ref([]);
  const editVnWards = ref([]);
  const editVnLoadingWards = ref(false);
  const editProvinceCode = ref("");

  watch(editProvinceCode, async (code) => {
    customerForm.value.address.state = "";
    customerForm.value.address.county = "";
    editVnWards.value = [];
    if (!code) return;
    const p = editVnProvinces.value.find(x => String(x.code) === String(code));
    if (p) customerForm.value.address.state = p.name;
    editVnLoadingWards.value = true;
    editVnWards.value = await fetchVnWards(code);
    editVnLoadingWards.value = false;
  });
  const contactPickerRows = ref([]);
  const contactPage = ref(1);
  const contactPageLength = ref(20);
  const contactForm = ref({});
  const activityDialogOpen = ref(false);
  const activitySaving = ref(false);
  const activityPage = ref(1);
  const activityPageLength = ref(10);
  const activityForm = ref({});
  const customerActivityOpen = ref(true);
  const customerFilterOpen = ref(true);
  const customerViewMenuOpen = ref(false);
  const customerListMoreMenuOpen = ref(false);
  const customerListView = ref("all");
  const customerVisibleFields = ref(CUSTOMER_COLUMNS.map((item) => item.field));
  const customerColumnDialogOpen = ref(false);
  const customerColumnSearch = ref("");
  const customerColumnDraft = ref([]);
  const customerSummaryFields = ref(readCustomerSummaryFields());
  const customerSummaryDialogOpen = ref(false);
  const customerSummarySearch = ref("");
  const customerSummaryDraft = ref([]);
  const customerEnabledFilters = ref([]);
  const customerFilterValues = ref({});

  const customerListViewLabel = computed(() => ({
    all: "Tất cả khách hàng",
    mine: "Khách hàng của tôi",
    partners: "Tất cả Đối tác/CTV",
    team: "Khách hàng của nhóm tôi",
  })[customerListView.value] || "Tất cả khách hàng");

  const customerListMoreActions = [
    { key: "update-address", label: "Cập nhật địa chỉ", icon: "search", ai: true },
    { key: "import-with-contact", label: "Nhập khẩu kèm Liên hệ", icon: "contact" },
    { key: "auto-merge-duplicate", label: "Tự động gộp trùng", icon: "refresh" },
    { key: "manage-tags", label: "Quản lý thẻ", icon: "tag", separator: true },
    { key: "trash", label: "Thùng rác", icon: "trash" },
  ];

  const contactPageCount = computed(() => Math.max(Math.ceil((ctx.detail.value?.contacts?.length || 0) / contactPageLength.value), 1));
  const contactPageStart = computed(() => ctx.detail.value?.contacts?.length ? (contactPage.value - 1) * contactPageLength.value + 1 : 0);
  const contactPageEnd = computed(() => Math.min(contactPage.value * contactPageLength.value, ctx.detail.value?.contacts?.length || 0));
  const visibleCustomerContacts = computed(() => {
    const start = (contactPage.value - 1) * contactPageLength.value;
    return (ctx.detail.value?.contacts || []).slice(start, start + contactPageLength.value);
  });
  const activityPageCount = computed(() => Math.max(Math.ceil((ctx.detail.value?.activities?.length || 0) / activityPageLength.value), 1));
  const activityPageStart = computed(() => ctx.detail.value?.activities?.length ? (activityPage.value - 1) * activityPageLength.value + 1 : 0);
  const activityPageEnd = computed(() => Math.min(activityPage.value * activityPageLength.value, ctx.detail.value?.activities?.length || 0));
  const visibleCustomerActivities = computed(() => {
    const start = (activityPage.value - 1) * activityPageLength.value;
    return (ctx.detail.value?.activities || []).slice(start, start + activityPageLength.value);
  });
  const customerPurchaseRecords = computed(() => {
    const records = [
      ...(ctx.detail.value?.quotations || []).map((row) => ({
        ...row,
        record_type: "quotation",
        record_label: "Báo giá",
        record_doctype: "Quotation",
        record_date: row.transaction_date,
      })),
      ...(ctx.detail.value?.orders || []).map((row) => ({
        ...row,
        record_type: "order",
        record_label: "Đơn hàng",
        record_doctype: "Sales Order",
        record_date: row.transaction_date,
      })),
      ...(ctx.detail.value?.invoices || []).map((row) => ({
        ...row,
        record_type: "invoice",
        record_label: "Hóa đơn",
        record_doctype: "Sales Invoice",
        record_date: row.posting_date,
      })),
    ];
    return records.sort((left, right) => String(right.record_date || "").localeCompare(String(left.record_date || "")));
  });
  const customerPrimaryContact = computed(() => ctx.detail.value?.contacts?.[0] || {});
  const customerDisplayPhone = computed(() => (
    ctx.detail.value?.document?.misa_mobile
    || ctx.detail.value?.document?.mobile_no
    || customerPrimaryContact.value.mobile_no
    || customerPrimaryContact.value.phone
    || ""
  ));
  const customerDisplayEmail = computed(() => (
    ctx.detail.value?.document?.misa_email
    || ctx.detail.value?.document?.email_id
    || customerPrimaryContact.value.email_id
    || ""
  ));
  const availableCustomerSummaryFields = computed(() => {
    const keyword = customerSummarySearch.value.trim().toLocaleLowerCase("vi");
    return CUSTOMER_SUMMARY_FIELDS.filter((item) => (
      !customerSummaryDraft.value.includes(item.field)
      && (!keyword || item.label.toLocaleLowerCase("vi").includes(keyword))
    ));
  });
  const selectedCustomerSummaryFields = computed(() => customerSummaryDraft.value
    .map((field) => CUSTOMER_SUMMARY_FIELDS.find((item) => item.field === field))
    .filter(Boolean));
  const visibleCustomerSummaryFields = computed(() => customerSummaryFields.value
    .map((field) => CUSTOMER_SUMMARY_FIELDS.find((item) => item.field === field))
    .filter(Boolean));
  const customerTimelineEntries = computed(() => ctx.detail.value?.timeline || []);
  const customerCommentEntries = computed(() => customerTimelineEntries.value.filter((row) => row.activity_type === "comment"));
  const customerConversationEntries = computed(() => customerTimelineEntries.value.filter((row) => row.activity_type === "communication"));
  const customerOrderDates = computed(() => (ctx.detail.value?.orders || [])
    .map((order) => order.transaction_date)
    .filter(Boolean)
    .sort());
  const customerPurchaseCycleDays = computed(() => {
    const dates = customerOrderDates.value.map((date) => new Date(date).getTime());
    if (dates.length < 2) return null;
    let totalGap = 0;
    for (let i = 1; i < dates.length; i++) totalGap += dates[i] - dates[i - 1];
    return Math.round(totalGap / (dates.length - 1) / (1000 * 60 * 60 * 24));
  });
  const customerDaysSinceLastOrder = computed(() => {
    const dates = customerOrderDates.value;
    if (!dates.length) return null;
    const last = new Date(dates[dates.length - 1]).getTime();
    return Math.max(0, Math.round((Date.now() - last) / (1000 * 60 * 60 * 24)));
  });

  async function loadCustomerDetail(name) {
    const targetName = name !== undefined ? name : customerName.value;
    if (!targetName) return ctx.navigate("customers");
    ctx.loading.value = true;
    ctx.selected.value = { name: targetName };
    ctx.detail.value = null;
    try {
      ctx.detail.value = await call("get_customer_workspace", { name: targetName });
      ctx.selected.value = ctx.detail.value.document;
      contactPage.value = 1;
      activityPage.value = 1;
      initialiseCustomerForm();
    } catch (error) {
      frappe.msgprint(error.message || __("Không thể tải hồ sơ khách hàng."));
    } finally {
      ctx.loading.value = false;
    }
  }

  function openCustomerDetail(row) {
    if (!row?.name) return;
    const selected = row || ctx.selected.value;
    if (!selected?.name) return;
    customerName.value = selected.name;
    ctx.route.value = "customer-detail";
    customerDetailTab.value = "details";
    customerSalesSection.value = "orders";
    customerSupportSection.value = "consult_cards";
    customerMarketingSection.value = "campaigns";
    customerNoteSection.value = "notes";
    customerEditing.value = false;
    frappe.route_options = { view: "customer-detail", customer: selected.name };
    frappe.set_route("dcnet-crm").then(() => {
      const url = new URL(window.location.href);
      url.hash = "";
      url.searchParams.set("view", "customer-detail");
      url.searchParams.set("customer", selected.name);
      url.searchParams.delete("opportunity");
      window.history.replaceState(window.history.state, "", url);
    });
  }

  function backToCustomers() {
    ctx.navigate("customers");
  }

  function initialiseCustomerForm() {
    if (!ctx.detail.value?.document) return;
    const document = ctx.detail.value.document;
    const contact = ctx.detail.value.contacts.find((item) => item.name === document.customer_primary_contact)
      || ctx.detail.value.contacts[0]
      || {};
    const address = ctx.detail.value.addresses.find((item) => item.name === document.customer_primary_address)
      || ctx.detail.value.addresses.find((item) => item.is_primary_address)
      || ctx.detail.value.addresses[0]
      || {};

    customerForm.value = {
      customer: {
        customer_name: document.customer_name || "",
        ten_viet_tat: document.ten_viet_tat || "",
        customer_type: document.customer_type || "Company",
        customer_group: document.customer_group || "",
        territory: document.territory || "",
        tax_id: document.tax_id || "",
        misa_mobile: document.misa_mobile || document.mobile_no || "",
        misa_email: document.misa_email || document.email_id || "",
        nguon_goc: document.nguon_goc || "",
        gender: document.gender || "",
        industry: document.industry || "",
        loai_hinh: document.loai_hinh || "",
        nganh_nghe: document.nganh_nghe || "",
        market_segment: document.market_segment || "",
        default_price_list: document.default_price_list || "",
        account_manager: document.account_manager || "",
        tai_khoan_ngan_hang: document.tai_khoan_ngan_hang || "",
        mo_tai_ngan_hang: document.mo_tai_ngan_hang || "",
        ngay_thanh_lap: document.ngay_thanh_lap || "",
        la_kh_tu: document.la_kh_tu || "",
        quy_mo_doanh_thu: document.quy_mo_doanh_thu || "",
        quy_mo_nhan_su: document.quy_mo_nhan_su || "",
        loai_han_muc_no: document.loai_han_muc_no || "",
        so_ngay_duoc_no: document.so_ngay_duoc_no || 0,
        website: document.website || "",
        customer_details: document.customer_details || "",
        dung_chung: Number(document.dung_chung || 0),
        la_kh_ca_nhan: Number(document.la_kh_ca_nhan || 0),
        la_doi_tac_ctv: Number(document.la_doi_tac_ctv || 0),
        doi_tac_gioi_thieu: document.doi_tac_gioi_thieu || "",
      },
      contact: {
        name: contact.name || "",
        first_name: contact.first_name || contact.full_name || "",
        last_name: contact.last_name || "",
        designation: contact.designation || "",
        mobile_no: contact.mobile_no || "",
        phone: contact.phone || "",
        email_id: contact.email_id || "",
      },
      address: {
        name: address.name || "",
        address_title: address.address_title || document.customer_name || "",
        address_type: address.address_type || "Billing",
        address_line1: address.address_line1 || "",
        address_line2: address.address_line2 || "",
        city: address.city || "",
        county: address.county || "",
        state: address.state || "",
        country: address.country || "Vietnam",
        pincode: address.pincode || "",
        email_id: address.email_id || "",
        phone: address.phone || "",
        is_primary_address: address.is_primary_address === undefined ? 1 : Number(address.is_primary_address),
        is_shipping_address: Number(address.is_shipping_address || 0),
      },
    };
  }

  async function beginCustomerEdit() {
    if (!ctx.detail.value?.can_write) return;
    customerDetailTab.value = "details";
    initialiseCustomerForm();
    customerEditing.value = true;
    // Load provinces if not yet loaded
    if (!editVnProvinces.value.length) {
      editVnProvinces.value = await fetchVnProvinces();
    }
    // Pre-select province from existing state value
    const stateName = customerForm.value.address.state;
    if (stateName && editVnProvinces.value.length) {
      const norm = s => s.toLowerCase().replace(/^tp\.?\s+/i, "").replace(/^thành phố\s+/i, "").replace(/^tỉnh\s+/i, "").replace(/\s+/g, " ").trim();
      const target = norm(stateName);
      const matched = editVnProvinces.value.find(p => { const pn = norm(p.name); return pn === target || pn.includes(target) || target.includes(pn); });
      if (matched) {
        const existingCounty = customerForm.value.address.county;
        editProvinceCode.value = String(matched.code);
        // Restore county after watcher resets it
        if (existingCounty) {
          const restoreCounty = async () => {
            if (!editVnLoadingWards.value && editVnWards.value.length) {
              customerForm.value.address.county = existingCounty;
            } else {
              setTimeout(restoreCounty, 100);
            }
          };
          setTimeout(restoreCounty, 50);
        }
      }
    }
  }

  function cancelCustomerEdit() {
    initialiseCustomerForm();
    customerEditing.value = false;
    editProvinceCode.value = "";
    editVnWards.value = [];
  }

  async function saveCustomerDetails() {
    if (!ctx.detail.value?.document?.name || customerSaving.value) return;
    customerSaving.value = true;
    try {
      await call("update_customer_details", {
        name: ctx.detail.value.document.name,
        customer: customerForm.value.customer,
        contact: customerForm.value.contact,
        address: customerForm.value.address,
      }, "POST");
      await loadCustomerDetail(ctx.detail.value.document.name);
      customerEditing.value = false;
      frappe.show_alert({ message: __("Đã cập nhật thông tin khách hàng."), indicator: "green" });
    } catch (error) {
      frappe.msgprint(error.message || __("Không thể cập nhật thông tin khách hàng."));
    } finally {
      customerSaving.value = false;
    }
  }

  function showDetailField(label, value) {
    const keyword = detailFieldSearch.value.trim().toLocaleLowerCase("vi");
    const matchesSearch = !keyword || label.toLocaleLowerCase("vi").includes(keyword);
    const hasValue = value !== null && value !== undefined && String(value).trim() !== "" && String(value).trim() !== "-";
    return matchesSearch && (showEmptyDetailFields.value || hasValue || customerEditing.value);
  }

  function hasCustomerOption(options, value) {
    if (!value) return true;
    return (options || []).some((option) => (option?.name || option) === value);
  }

  function emptyContactForm() {
    return {
      name: "",
      first_name: "",
      middle_name: "",
      last_name: "",
      salutation: "",
      gender: "",
      status: "Open",
      department: "",
      designation: "",
      email_id: "",
      mobile_no: "",
      phone: "",
      company_name: ctx.detail.value?.document?.customer_name || "",
      is_primary_contact: ctx.detail.value?.contacts?.length ? 0 : 1,
    };
  }

  function openContactDialog(mode, contact) {
    if (mode === undefined) mode = "quick";
    contactDialogMode.value = mode;
    contactForm.value = contact ? {
      name: contact.name || "",
      first_name: contact.first_name || "",
      middle_name: contact.middle_name || "",
      last_name: contact.last_name || "",
      salutation: contact.salutation || "",
      gender: contact.gender || "",
      status: contact.status || "Open",
      department: contact.department || "",
      designation: contact.designation || "",
      email_id: contact.email_id || "",
      mobile_no: contact.mobile_no || "",
      phone: contact.phone || "",
      company_name: contact.company_name || ctx.detail.value?.document?.customer_name || "",
      is_primary_contact: Number(contact.is_primary_contact || contact.name === ctx.detail.value?.document?.customer_primary_contact),
    } : emptyContactForm();
    contactDialogOpen.value = true;
  }

  function closeContactDialog() {
    if (contactSaving.value) return;
    contactDialogOpen.value = false;
  }

  async function saveCustomerContact() {
    if (!contactForm.value.first_name?.trim() || contactSaving.value) return;
    contactSaving.value = true;
    try {
      await call("save_customer_contact", {
        customer: ctx.detail.value.document.name,
        contact: contactForm.value,
      }, "POST");
      contactDialogOpen.value = false;
      await loadCustomerDetail(ctx.detail.value.document.name);
      customerDetailTab.value = "contacts";
      frappe.show_alert({ message: __("Đã lưu liên hệ."), indicator: "green" });
    } catch (error) {
      frappe.msgprint(error.message || __("Không thể lưu liên hệ."));
    } finally {
      contactSaving.value = false;
    }
  }

  async function openContactPicker() {
    contactPickerOpen.value = true;
    contactPickerSearch.value = "";
    await searchCustomerContacts();
  }

  async function searchCustomerContacts() {
    if (!ctx.detail.value?.document?.name) return;
    contactPickerLoading.value = true;
    try {
      contactPickerRows.value = await call("search_customer_contacts", {
        customer: ctx.detail.value.document.name,
        search: contactPickerSearch.value,
        page_length: 30,
      });
    } catch (error) {
      frappe.msgprint(error.message || __("Không thể tìm danh sách liên hệ."));
    } finally {
      contactPickerLoading.value = false;
    }
  }

  async function linkCustomerContact(contact) {
    if (!contact?.name || contactSaving.value) return;
    contactSaving.value = true;
    try {
      await call("link_customer_contact", {
        customer: ctx.detail.value.document.name,
        contact: contact.name,
      }, "POST");
      contactPickerOpen.value = false;
      await loadCustomerDetail(ctx.detail.value.document.name);
      customerDetailTab.value = "contacts";
      frappe.show_alert({ message: __("Đã liên kết liên hệ với khách hàng."), indicator: "green" });
    } catch (error) {
      frappe.msgprint(error.message || __("Không thể liên kết liên hệ."));
    } finally {
      contactSaving.value = false;
    }
  }

  function changeContactPage(nextPage) {
    contactPage.value = Math.min(Math.max(nextPage, 1), contactPageCount.value);
  }

  function localDateTimeInput(value) {
    if (value === undefined) value = new Date();
    const date = value instanceof Date ? value : new Date(value);
    if (Number.isNaN(date.getTime())) return "";
    const offset = date.getTimezoneOffset() * 60000;
    return new Date(date.getTime() - offset).toISOString().slice(0, 16);
  }

  function openActivityDialog(activityType, activity) {
    if (activityType === undefined) activityType = "task";
    if (activity === undefined) activity = null;
    const startsOn = activity?.starts_on || localDateTimeInput();
    const defaultEnd = new Date(new Date(startsOn).getTime() + 30 * 60000);
    activityForm.value = {
      name: activity?.name || "",
      activity_type: activity?.activity_type || activityType,
      subject: activity?.subject || "",
      description: activity?.description || "",
      due_date: activity?.due_date ? String(activity.due_date).slice(0, 10) : localDateTimeInput().slice(0, 10),
      starts_on: activity?.starts_on ? localDateTimeInput(activity.starts_on) : startsOn,
      ends_on: activity?.ends_on ? localDateTimeInput(activity.ends_on) : localDateTimeInput(defaultEnd),
      status: activity?.status || "Open",
      priority: activity?.priority || "Medium",
      allocated_to: activity?.performed_by || ctx.boot.value?.user || "",
    };
    activityDialogOpen.value = true;
  }

  async function saveCustomerActivity() {
    if (!activityForm.value.subject?.trim() || activitySaving.value) return;
    activitySaving.value = true;
    try {
      await call("save_customer_activity", {
        customer: ctx.detail.value.document.name,
        activity: activityForm.value,
      }, "POST");
      activityDialogOpen.value = false;
      await loadCustomerDetail(ctx.detail.value.document.name);
      customerDetailTab.value = "activity";
      frappe.show_alert({ message: __("Đã lưu hoạt động."), indicator: "green" });
    } catch (error) {
      frappe.msgprint(error.message || __("Không thể lưu hoạt động."));
    } finally {
      activitySaving.value = false;
    }
  }

  function changeActivityPage(nextPage) {
    activityPage.value = Math.min(Math.max(nextPage, 1), activityPageCount.value);
  }

  function activityTypeLabel(type) {
    return type === "task" ? "Nhiệm vụ" : type === "call" ? "Cuộc gọi" : "Lịch hẹn";
  }

  function activityStatusLabel(status) {
    return ({ Open: "Đang thực hiện", Closed: "Đã hoàn thành", Completed: "Đã hoàn thành", Cancelled: "Đã hủy" })[status] || status || "—";
  }

  function formatFileSize(bytes) {
    const value = Number(bytes || 0);
    if (!value) return "—";
    if (value < 1024) return `${value} B`;
    if (value < 1024 * 1024) return `${(value / 1024).toFixed(1)} KB`;
    return `${(value / 1024 / 1024).toFixed(1)} MB`;
  }

  function customerDetailTabBadge(tab) {
    const current = ctx.detail.value || {};
    const map = {
      contacts: current.contacts?.length,
      activity: current.activities?.length,
      sales: (current.orders?.length || 0) + (current.sales_returns?.length || 0) + (current.opportunities?.length || 0)
        + (current.quotations?.length || 0) + (current.invoices?.length || 0) + (current.purchased_items?.length || 0)
        + (current.subsidiaries?.length || 0),
      support: 0,
      marketing: 0,
      notes: (current.files?.length || 0) + (current.timeline || []).filter((row) => row.activity_type === "comment").length,
    };
    return map[tab] || 0;
  }

  function customerSalesSectionLabel(section) {
    return ({
      orders: "Đơn hàng",
      returns: "Trả lại hàng bán",
      opportunities: "Cơ hội",
      quotations: "Báo giá",
      invoices: "Hóa đơn",
      items: "Hàng hóa đã mua",
      subsidiaries: "Đại lý/Công ty con",
    })[section] || "Bán hàng";
  }

  function customerSupportSectionLabel(section) {
    return ({ consult_cards: "Thẻ tư vấn", care_cards: "Thẻ chăm sóc", warranty: "Phiếu bảo hành" })[section] || "Hỗ trợ";
  }

  function customerMarketingSectionLabel(section) {
    return ({
      campaigns: "Chiến dịch",
      promotions: "Khuyến mại",
      loyalty: "Tích lũy",
      rewards: "Trả thưởng",
      email: "Email",
      sms: "SMS",
      routes: "Lộ trình đi tuyến",
      aimarketing: "aiMarketing",
    })[section] || "Marketing";
  }

  function customerNoteSectionLabel(section) {
    return ({ notes: "Ghi chú", attachments: "Tài liệu đính kèm" })[section] || "Ghi chú và đính kèm";
  }

  function notifyCustomerUnavailable(label) {
    frappe.msgprint({
      title: __("Chưa có dữ liệu nguồn"),
      message: __("{0} chưa có DocType/API riêng trong dcnet-crm. Mình đã giữ nút phản hồi rõ để không bị bấm im lặng.", [label]),
      indicator: "orange",
    });
  }

  function promptCustomerTag() {
    const target = ctx.detail.value?.document?.name;
    if (!target) return;
    frappe.prompt(
      [{ fieldname: "tag", fieldtype: "Data", label: "Tên thẻ", reqd: 1 }],
      async (values) => {
        try {
          await call("add_customer_tag", { name: target, tag: values.tag }, "POST");
          await loadCustomerDetail(target);
          frappe.show_alert({ message: __("Đã thêm thẻ."), indicator: "green" });
        } catch (error) {
          frappe.msgprint(error.message || __("Không thể thêm thẻ."));
        }
      },
      "Thêm thẻ",
      "Thêm"
    );
  }

  async function saveCustomerNoteFromDetail(source) {
    const target = ctx.detail.value?.document?.name;
    const content = (source === "conversation" ? customerConversationText.value : customerInlineNote.value).trim();
    if (!target || !content) return;
    try {
      if (source === "conversation") {
        await call("add_customer_conversation", { name: target, content }, "POST");
      } else {
        await call("add_note", { resource: "customers", name: target, content }, "POST");
      }
      if (source === "conversation") customerConversationText.value = "";
      else customerInlineNote.value = "";
      await loadCustomerDetail(target);
      customerNoteSection.value = source === "conversation" ? customerNoteSection.value : "notes";
      frappe.show_alert({ message: __("Đã lưu nội dung."), indicator: "green" });
    } catch (error) {
      frappe.msgprint(error.message || __("Không thể lưu nội dung."));
    }
  }

  async function uploadCustomerFile(event) {
    const file = event?.target?.files?.[0];
    if (event?.target) event.target.value = "";
    const target = ctx.detail.value?.document?.name;
    if (!file || !target || customerAttachUploading.value) return;
    customerAttachUploading.value = true;
    try {
      const formData = new FormData();
      formData.append("file", file, file.name);
      formData.append("is_private", 1);
      formData.append("doctype", "Customer");
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
      await loadCustomerDetail(target);
      customerNoteSection.value = "attachments";
      frappe.show_alert({ message: __("Đã thêm tệp đính kèm."), indicator: "green" });
    } catch (error) {
      frappe.msgprint(error.message || __("Không thể tải tệp."));
    } finally {
      customerAttachUploading.value = false;
    }
  }

  function addCustomerAttachmentLink() {
    const target = ctx.detail.value?.document?.name;
    if (!target) return;
    frappe.prompt(
      [
        { fieldname: "url", fieldtype: "Data", label: "Liên kết (URL)", default: "https://", reqd: 1 },
        { fieldname: "title", fieldtype: "Data", label: "Tên hiển thị" },
      ],
      async (values) => {
        try {
          await call("add_customer_attachment_link", {
            name: target,
            url: /^(https?:\/\/)/i.test(values.url.trim()) ? values.url.trim() : `https://${values.url.trim()}`,
            title: values.title || "",
          }, "POST");
          await loadCustomerDetail(target);
          customerNoteSection.value = "attachments";
          frappe.show_alert({ message: __("Đã thêm liên kết."), indicator: "green" });
        } catch (error) {
          frappe.msgprint(error.message || __("Không thể thêm liên kết."));
        }
      },
      "Thêm liên kết",
      "Thêm"
    );
  }

  function deleteCustomerAttachment(fileName) {
    if (!fileName) return;
    frappe.confirm("Xóa tài liệu này?", async () => {
      try {
        await call("delete_customer_attachment", { file_name: fileName }, "POST");
        await loadCustomerDetail(ctx.detail.value?.document?.name);
        frappe.show_alert({ message: __("Đã xóa tài liệu."), indicator: "green" });
      } catch (error) {
        frappe.msgprint(error.message || __("Không thể xóa tài liệu."));
      }
    });
  }

  function createCustomerInvoice(isReturn = false) {
    const target = ctx.detail.value?.document?.name;
    if (!target) return;
    frappe.new_doc("Sales Invoice", {
      customer: target,
      is_return: isReturn ? 1 : 0,
    });
  }

  function callCustomerPhone() {
    if (!customerDisplayPhone.value) {
      notifyCustomerUnavailable("Số điện thoại khách hàng");
      return;
    }
    window.location.href = `tel:${customerDisplayPhone.value}`;
  }

  function emailCustomer() {
    if (!customerDisplayEmail.value) {
      notifyCustomerUnavailable("Email khách hàng");
      return;
    }
    window.location.href = `mailto:${customerDisplayEmail.value}`;
  }

  function toggleCustomerColumn(field) {
    const fields = customerVisibleFields.value;
    customerVisibleFields.value = fields.includes(field)
      ? fields.filter((item) => item !== field)
      : [...fields, field];
  }

  function toggleCustomerFilter(field) {
    const fields = customerEnabledFilters.value;
    customerEnabledFilters.value = fields.includes(field)
      ? fields.filter((item) => item !== field)
      : [...fields, field];
    if (!customerEnabledFilters.value.includes(field)) {
      delete customerFilterValues.value[field];
      ctx.loadRows();
    }
  }

  function openCustomerColumnDialog() {
    customerColumnDraft.value = [...customerVisibleFields.value];
    customerColumnSearch.value = "";
    customerColumnDialogOpen.value = true;
  }

  function cancelCustomerColumnDialog() {
    customerColumnDialogOpen.value = false;
    customerColumnSearch.value = "";
    customerColumnDraft.value = [];
  }

  function toggleCustomerDraftColumn(field) {
    customerColumnDraft.value = customerColumnDraft.value.includes(field)
      ? customerColumnDraft.value.filter((item) => item !== field)
      : [...customerColumnDraft.value, field];
  }

  function removeCustomerDraftColumn(field) {
    customerColumnDraft.value = customerColumnDraft.value.filter((item) => item !== field);
  }

  function resetCustomerDraftColumns() {
    customerColumnDraft.value = CUSTOMER_COLUMNS.map((item) => item.field);
  }

  function saveCustomerColumns() {
    customerVisibleFields.value = [...customerColumnDraft.value];
    window.localStorage.setItem("dcnet-crm-customer-columns", JSON.stringify(customerVisibleFields.value));
    cancelCustomerColumnDialog();
  }

  function customerSummaryValue(field) {
    const definition = CUSTOMER_SUMMARY_FIELDS.find((item) => item.field === field);
    const document = ctx.detail.value?.document || {};
    const customer = customerForm.value.customer || {};
    const address = customerForm.value.address || {};
    const summary = ctx.detail.value?.summary || {};
    const orders = ctx.detail.value?.orders || [];
    const sourceField = definition?.sourceField || field;
    let value;

    if (definition?.source === "customer") value = customer[sourceField] ?? document[sourceField];
    else if (definition?.source === "address") value = address[sourceField];
    else if (definition?.source === "summary") value = summary[sourceField];
    else value = document[sourceField];

    if (field === "phone") value = customerDisplayPhone.value;
    if (field === "email") value = customerDisplayEmail.value;
    if (field === "first_order_date") value = orders.length ? orders[orders.length - 1].transaction_date : "";
    if (field === "last_order_date") value = orders.length ? orders[0].transaction_date : "";
    if (field === "customer_type") {
      value = ({ Company: "Công ty", Individual: "Cá nhân", Partnership: "Đối tác" })[value] || value;
    }
    if (field === "address_type") {
      value = ({ Billing: "Hóa đơn", Shipping: "Giao hàng", Office: "Văn phòng", Personal: "Cá nhân" })[value] || value;
    }
    if (definition?.format === "date" && value) {
      try {
        value = window.frappe?.datetime?.str_to_user?.(value) || value;
      } catch (_) {
        // Keep the server value when Frappe's date formatter cannot parse it.
      }
    }
    if (definition?.format === "currency" && value !== null && value !== undefined && value !== "") {
      value = new Intl.NumberFormat("vi-VN", { maximumFractionDigits: 2 }).format(Number(value) || 0);
    }
    if (value === 0) return "0";
    if (value === false) return "Không";
    return value || definition?.empty || "—";
  }

  function openCustomerSummaryDialog() {
    customerSummaryDraft.value = [...customerSummaryFields.value];
    customerSummarySearch.value = "";
    customerSummaryDialogOpen.value = true;
  }

  function cancelCustomerSummaryDialog() {
    customerSummaryDialogOpen.value = false;
    customerSummarySearch.value = "";
    customerSummaryDraft.value = [];
  }

  function addCustomerSummaryField(field) {
    if (!customerSummaryDraft.value.includes(field)) customerSummaryDraft.value.push(field);
  }

  function removeCustomerSummaryField(field) {
    customerSummaryDraft.value = customerSummaryDraft.value.filter((item) => item !== field);
  }

  function resetCustomerSummaryFields() {
    customerSummaryDraft.value = [...DEFAULT_CUSTOMER_SUMMARY_FIELDS];
  }

  function saveCustomerSummaryFields() {
    customerSummaryFields.value = [...customerSummaryDraft.value];
    window.localStorage.setItem(customerSummaryStorageKey(), JSON.stringify(customerSummaryFields.value));
    cancelCustomerSummaryDialog();
  }

  function selectCustomerListView(view) {
    if (!["all", "mine"].includes(view)) return;
    customerListView.value = view;
    customerViewMenuOpen.value = false;
    ctx.page.value = 1;
    ctx.loadRows();
  }

  function importCustomers() {
    frappe.new_doc("Data Import", { reference_doctype: "Customer", import_type: "Insert New Records" });
  }

  function getCustomerActionTargets() {
    const names = new Set([...(ctx.selectedNames?.value || [])]);
    if (!names.size && ctx.selected.value?.name) names.add(ctx.selected.value.name);
    return [...names];
  }

  function requireCustomerActionTargets(actionLabel) {
    const targets = getCustomerActionTargets();
    if (!targets.length) {
      frappe.msgprint({
        title: __("Chưa chọn khách hàng"),
        message: __("Hãy tick hoặc chọn ít nhất một khách hàng để thực hiện {0}.", [actionLabel]),
        indicator: "orange",
      });
      return [];
    }
    return targets;
  }

  function escapeCustomerHtml(value) {
    const node = document.createElement("div");
    node.textContent = value == null ? "" : String(value);
    return node.innerHTML;
  }

  function showCustomerActionResult(title, result) {
    const errors = result?.errors || [];
    const message = [
      result?.updated ? `Đã cập nhật ${result.updated} khách hàng.` : "",
      result?.tagged ? `Đã xử lý thẻ cho ${result.tagged} khách hàng.` : "",
      result?.merged ? `Đã gộp ${result.merged} khách hàng trùng.` : "",
      result?.groups ? `Số nhóm kiểm tra: ${result.groups}.` : "",
      errors.length ? `<br><b>Lỗi:</b><br>${errors.map((row) => escapeCustomerHtml(row.error || row.name || row.source || "")).join("<br>")}` : "",
    ].filter(Boolean).join("<br>");
    frappe.msgprint({
      title,
      message: message || __("Đã hoàn tất."),
      indicator: errors.length ? "orange" : "green",
    });
  }

  function openBulkAddressDialog() {
    const targets = requireCustomerActionTargets("cập nhật địa chỉ");
    if (!targets.length) return;
    const dialog = new frappe.ui.Dialog({
      title: __("Cập nhật địa chỉ"),
      fields: [
        { fieldname: "address_line1", fieldtype: "Data", label: "Số nhà, Đường phố", reqd: 1 },
        { fieldname: "county", fieldtype: "Data", label: "Quận/Huyện" },
        { fieldname: "state", fieldtype: "Data", label: "Tỉnh/Thành phố" },
        { fieldname: "city", fieldtype: "Data", label: "Thành phố hiển thị" },
        { fieldname: "pincode", fieldtype: "Data", label: "Mã vùng" },
        { fieldname: "country", fieldtype: "Link", options: "Country", label: "Quốc gia", default: "Vietnam" },
        { fieldname: "address_type", fieldtype: "Select", options: "Billing\nShipping", label: "Loại địa chỉ", default: "Billing" },
        { fieldname: "is_shipping_address", fieldtype: "Check", label: "Đồng thời là địa chỉ giao hàng" },
      ],
      primary_action_label: __("Cập nhật"),
      async primary_action(values) {
        try {
          dialog.disable_primary_action();
          const result = await call("bulk_update_customer_address", {
            customers: JSON.stringify(targets),
            address: JSON.stringify({
              ...values,
              is_primary_address: values.address_type !== "Shipping" ? 1 : 0,
              is_shipping_address: values.address_type === "Shipping" || values.is_shipping_address ? 1 : 0,
            }),
          }, "POST");
          dialog.hide();
          showCustomerActionResult(__("Cập nhật địa chỉ"), result);
          ctx.loadRows();
        } catch (error) {
          frappe.msgprint(error.message || __("Không thể cập nhật địa chỉ."));
        } finally {
          dialog.enable_primary_action();
        }
      },
    });
    dialog.show();
  }

  function openContactImportWithCustomer() {
    frappe.new_doc("Data Import", { reference_doctype: "Contact", import_type: "Insert New Records" });
    frappe.show_alert({
      message: __("Đã mở nhập Liên hệ. Trong mẫu Contact, dùng bảng Links để nối link_doctype = Customer và link_name = mã khách hàng."),
      indicator: "blue",
    }, 8);
  }

  function autoMergeDuplicateCustomers() {
    const targets = getCustomerActionTargets();
    const selectedScope = targets.length >= 2;
    const scopeLabel = selectedScope
      ? `${targets.length} khách hàng đã chọn`
      : "toàn bộ khách hàng bạn có quyền đọc";
    frappe.confirm(
      __(
        "Tự động gộp trùng sẽ ưu tiên nhóm cùng Mã số thuế, sau đó nhóm cùng Tên khách hàng. Tiếp tục kiểm tra {0}?",
        [scopeLabel]
      ),
      async () => {
        try {
          const result = await call("auto_merge_duplicate_customers", {
            customers: JSON.stringify(selectedScope ? targets : []),
          }, "POST");
          showCustomerActionResult(__("Tự động gộp trùng"), result);
          ctx.loadRows();
        } catch (error) {
          frappe.msgprint(error.message || __("Không thể gộp trùng khách hàng."));
        }
      }
    );
  }

  function openBulkTagDialog() {
    const targets = requireCustomerActionTargets("quản lý thẻ");
    if (!targets.length) return;
    frappe.prompt(
      [
        { fieldname: "action", fieldtype: "Select", options: "Thêm thẻ\nGỡ thẻ", label: "Thao tác", default: "Thêm thẻ", reqd: 1 },
        { fieldname: "tag", fieldtype: "Data", label: "Tên thẻ", reqd: 1 },
      ],
      async (values) => {
        try {
          const result = await call("bulk_manage_customer_tags", {
            customers: JSON.stringify(targets),
            tag: values.tag,
            action: values.action === "Gỡ thẻ" ? "remove" : "add",
          }, "POST");
          showCustomerActionResult(__("Quản lý thẻ"), result);
          ctx.loadRows();
        } catch (error) {
          frappe.msgprint(error.message || __("Không thể xử lý thẻ."));
        }
      },
      "Quản lý thẻ",
      "Thực hiện"
    );
  }

  function openCustomerTrash() {
    frappe.route_options = { deleted_doctype: "Customer" };
    frappe.set_route("List", "Deleted Document");
  }

  function toggleCustomerListMoreMenu() {
    customerListMoreMenuOpen.value = !customerListMoreMenuOpen.value;
  }

  function closeCustomerListMoreMenu() {
    customerListMoreMenuOpen.value = false;
  }

  function handleCustomerListMoreAction(action) {
    customerListMoreMenuOpen.value = false;
    if (action === "update-address") return openBulkAddressDialog();
    if (action === "import-with-contact") return openContactImportWithCustomer();
    if (action === "auto-merge-duplicate") return autoMergeDuplicateCustomers();
    if (action === "manage-tags") return openBulkTagDialog();
    if (action === "trash") return openCustomerTrash();
  }

  function createCustomerTask() {
    if (!ctx.selected.value) return;
    frappe.new_doc("ToDo", { reference_type: "Customer", reference_name: ctx.selected.value.name });
  }

  function openContact(contact) {
    ctx.openRelated("Contact", contact);
  }

  return {
    customerTab, customerDetailTab, customerSalesSection, customerSupportSection,
    customerMarketingSection, customerNoteSection, customerName,
    customerEditing, customerSaving, detailFieldSearch, showEmptyDetailFields,
    customerForm, contactDialogOpen, contactDialogMode, contactSaving,
    contactPickerOpen, contactPickerLoading, contactPickerSearch, contactPickerRows,
    contactPage, contactPageLength, contactForm,
    activityDialogOpen, activitySaving, activityPage, activityPageLength, activityForm,
    customerActivityOpen, customerFilterOpen, customerViewMenuOpen, customerListMoreMenuOpen,
    customerListView, customerVisibleFields, customerColumnDialogOpen,
    customerColumnSearch, customerColumnDraft, customerEnabledFilters, customerFilterValues,
    customerSummaryFields, customerSummaryDialogOpen, customerSummarySearch, customerSummaryDraft,
    customerListMoreActions,
    customerListViewLabel, contactPageCount, contactPageStart, contactPageEnd,
    visibleCustomerContacts, activityPageCount, activityPageStart, activityPageEnd,
    visibleCustomerActivities, customerPurchaseRecords, customerPrimaryContact,
    customerDisplayPhone, customerDisplayEmail, availableCustomerSummaryFields,
    selectedCustomerSummaryFields, visibleCustomerSummaryFields, customerTimelineEntries,
    customerCommentEntries, customerConversationEntries,
    customerPurchaseCycleDays, customerDaysSinceLastOrder,
    customerInlineNote, customerConversationText, customerAttachUploading,
    editVnProvinces, editVnWards, editVnLoadingWards, editProvinceCode,
    loadCustomerDetail, openCustomerDetail, backToCustomers,
    initialiseCustomerForm, beginCustomerEdit, cancelCustomerEdit, saveCustomerDetails,
    showDetailField, hasCustomerOption, openContactDialog, closeContactDialog,
    saveCustomerContact, openContactPicker, searchCustomerContacts, linkCustomerContact,
    changeContactPage, openActivityDialog, saveCustomerActivity, changeActivityPage,
    activityTypeLabel, activityStatusLabel, formatFileSize, customerDetailTabBadge,
    customerSalesSectionLabel, customerSupportSectionLabel, customerMarketingSectionLabel,
    customerNoteSectionLabel, notifyCustomerUnavailable, promptCustomerTag,
    saveCustomerNoteFromDetail, uploadCustomerFile, addCustomerAttachmentLink,
    deleteCustomerAttachment, createCustomerInvoice, callCustomerPhone, emailCustomer,
    toggleCustomerColumn, toggleCustomerFilter,
    openCustomerColumnDialog, cancelCustomerColumnDialog,
    toggleCustomerDraftColumn, removeCustomerDraftColumn,
    resetCustomerDraftColumns, saveCustomerColumns,
    customerSummaryValue, openCustomerSummaryDialog, cancelCustomerSummaryDialog,
    addCustomerSummaryField, removeCustomerSummaryField,
    resetCustomerSummaryFields, saveCustomerSummaryFields,
    selectCustomerListView,
    importCustomers, toggleCustomerListMoreMenu, closeCustomerListMoreMenu,
    handleCustomerListMoreAction, createCustomerTask, openContact, exportResource,
  };
}
