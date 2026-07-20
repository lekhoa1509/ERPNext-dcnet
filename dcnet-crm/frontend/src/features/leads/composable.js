import { computed, ref } from "vue/dist/vue.esm-bundler.js";
import { call, exportResource } from "../../utils.js";

const LEAD_DETAIL_TABS = [
  { key: "detail", label: "Thông tin chi tiết" },
  { key: "notes", label: "Ghi chú" },
  { key: "attachments", label: "Tài liệu đính kèm" },
  { key: "interested_items", label: "Hàng hóa quan tâm" },
  { key: "campaigns", label: "Chiến dịch" },
  { key: "email", label: "Email" },
  { key: "active_tasks", label: "Công việc đang thực hiện" },
  { key: "sms", label: "SMS" },
  { key: "done_tasks", label: "Công việc đã hoàn thành" },
  { key: "routes", label: "Lộ trình di chuyển" },
  { key: "conversations", label: "Nội dung trao đổi" },
  { key: "aimarketing", label: "aiMarketing" },
];

const LEAD_FILTER_DEFINITIONS = [
  { field: "lead_name", label: "Họ và tên" },
  { field: "job_title", label: "Chức danh" },
  { field: "mobile_no", label: "ĐT di động" },
  { field: "phone", label: "ĐT cơ quan" },
  { field: "custom_work_email", label: "Email cơ quan" },
  { field: "email_id", label: "Email cá nhân" },
  { field: "company_name", label: "Tổ chức" },
  { field: "custom_full_address", label: "Địa chỉ" },
  { field: "state", label: "Tỉnh/Thành phố" },
  { field: "custom_district", label: "Quận/Huyện" },
  { field: "custom_ward", label: "Phường/Xã" },
  { field: "utm_source", label: "Nguồn gốc" },
  { field: "custom_business_type", label: "Loại hình" },
  { field: "custom_sector", label: "Lĩnh vực" },
  { field: "custom_lead_type", label: "Loại tiềm năng" },
  { field: "status", label: "Trạng thái" },
  { field: "lead_owner", label: "Phụ trách" },
  { field: "creation", label: "Ngày tạo" },
];

const LEAD_LIST_COLUMNS = [
  { field: "lead_name", label: "Tên", width: "250px" },
  { field: "phone", label: "Điện thoại", width: "150px" },
  { field: "email_id", label: "Email", width: "220px" },
  { field: "status", label: "Trạng thái", width: "140px" },
  { field: "utm_source", label: "Nguồn", width: "160px" },
  { field: "lead_owner", label: "Phụ trách", width: "190px" },
];

export function useLeads(ctx) {
  const visibleLeadDetailTabs = computed(() => LEAD_DETAIL_TABS);
  const leadDetailName = ref("");
  const leadDetail = ref(null);
  const leadDetailTab = ref("detail");
  const leadDetailEditing = ref(false);
  const leadDetailSaving = ref(false);
  const leadDetailForm = ref({});
  const leadShowEmpty = ref(true);
  const leadDetailFieldSearch = ref("");
  const leadDetailMoreOpen = ref(false);
  const leadFormReturnName = ref("");
  const leadFilterOpen = ref(true);
  const leadActivityOpen = ref(true);
  const leadColumnDialogOpen = ref(false);
  const leadVisibleFields = ref(LEAD_LIST_COLUMNS.map((column) => column.field));
  const leadShownColumns = computed(() => LEAD_LIST_COLUMNS.filter((column) => leadVisibleFields.value.includes(column.field)));
  const leadEnabledFilters = ref([]);
  const leadFilterValues = ref({});
  const leadVisibleFilterDefinitions = computed(() => LEAD_FILTER_DEFINITIONS);
  const leadAppliedFilterCount = computed(() => (
    leadEnabledFilters.value.filter((field) => String(leadFilterValues.value[field] || "").trim()).length
  ));
  const leadFormOpen = ref(false);
  const leadFormMode = ref("create");
  const leadFormSaving = ref(false);
  const leadFormOptions = ref({ salutations: [], sources: [], industries: [], countries: [], companies: [], items: [] });
  const leadForm = ref({});
  const leadInterestedItems = ref([]);
  const leadItemPickerOpen = ref(false);
  const leadItemPickerSearch = ref("");
  const leadItemPickerSelected = ref([]);
  const leadItemPickerPage = ref(1);
  const leadItemPickerPageLength = ref(20);
  const leadActivityDialogOpen = ref(false);
  const leadActivitySaving = ref(false);
  const leadActivityMoreOpen = ref(false);
  const leadActivityForm = ref({});
  const leadAttachmentUploading = ref(false);

  const leadActivities = computed(() => leadDetail.value?.activities || []);
  const leadActiveActivities = computed(() => leadActivities.value.filter((item) => item.status === "Open"));
  const leadDoneActivities = computed(() => leadActivities.value.filter((item) => item.status !== "Open"));

  const leadItemPickerFiltered = computed(() => {
    const keyword = leadItemPickerSearch.value.trim().toLocaleLowerCase("vi");
    return (leadFormOptions.value.items || []).filter((item) => {
      if (!keyword) return true;
      return (item.name || "").toLocaleLowerCase("vi").includes(keyword)
        || (item.item_name || "").toLocaleLowerCase("vi").includes(keyword)
        || (item.item_group || "").toLocaleLowerCase("vi").includes(keyword);
    });
  });
  const leadItemPickerPageCount = computed(() => Math.max(Math.ceil(leadItemPickerFiltered.value.length / leadItemPickerPageLength.value), 1));
  const leadItemPickerRows = computed(() => {
    const start = (leadItemPickerPage.value - 1) * leadItemPickerPageLength.value;
    return leadItemPickerFiltered.value.slice(start, start + leadItemPickerPageLength.value);
  });

  function buildLeadFilters() {
    const filters = {};
    for (const field of leadEnabledFilters.value) {
      const rawValue = leadFilterValues.value[field];
      const value = String(rawValue || "").trim();
      if (!value) continue;
      if (["status", "custom_lead_type", "custom_business_type"].includes(field)) {
        filters[field] = value;
      } else if (field === "creation") {
        filters[field] = ["between", [`${value} 00:00:00`, `${value} 23:59:59`]];
      } else {
        filters[field] = ["like", `%${value}%`];
      }
    }
    return filters;
  }

  function toggleLeadFilter(field) {
    leadEnabledFilters.value = leadEnabledFilters.value.includes(field)
      ? leadEnabledFilters.value.filter((item) => item !== field)
      : [...leadEnabledFilters.value, field];
    if (!leadEnabledFilters.value.includes(field)) {
      delete leadFilterValues.value[field];
      ctx.loadRows();
    }
  }

  function clearLeadFilters() {
    leadEnabledFilters.value = [];
    leadFilterValues.value = {};
  }

  function toggleLeadColumn(field) {
    if (field === "lead_name") return;
    leadVisibleFields.value = leadVisibleFields.value.includes(field)
      ? leadVisibleFields.value.filter((item) => item !== field)
      : [...leadVisibleFields.value, field];
  }

  function resetLeadColumns() {
    leadVisibleFields.value = LEAD_LIST_COLUMNS.map((column) => column.field);
  }

  function _emptyLeadForm() {
    return {
      salutation: "", last_name: "", first_name: "", department: "",
      job_title: "", mobile_no: "", phone: "", source: "",
      custom_lead_type: "", custom_zalo: "", email_id: "",
      custom_work_email: "", company_name: "", custom_tax_id: "",
      custom_bank_account: "", custom_bank_name: "", custom_founding_date: "",
      custom_business_type: "", custom_sector: "", industry: "",
      country: "Vietnam", state: "", custom_district: "", custom_ward: "",
      address_line1: "", pincode: "", custom_full_address: "",
      notes: "", custom_is_shared: 0, status: "Lead",
    };
  }

  async function loadLeadDetail(name) {
    const targetName = name !== undefined ? name : leadDetailName.value;
    if (!targetName) return ctx.navigate("leads");
    ctx.loading.value = true;
    leadDetail.value = null;
    try {
      leadDetail.value = await call("get_lead_detail", { name: targetName });
      leadDetailName.value = targetName;
      if (!LEAD_DETAIL_TABS.some((tab) => tab.key === leadDetailTab.value)) {
        leadDetailTab.value = "detail";
      }
    } catch (error) {
      frappe.msgprint(error.message || __("Không thể tải tiềm năng."));
    } finally {
      ctx.loading.value = false;
    }
  }

  async function ensureLeadFormOptions() {
    if (leadFormOptions.value.sources?.length && leadFormOptions.value.items?.length) return;
    try {
      const opts = await call("get_lead_form_options");
      leadFormOptions.value = { ...leadFormOptions.value, ...opts };
    } catch {}
  }

  function openLeadDetail(row) {
    if (!row?.name) return;
    leadDetailName.value = row.name;
    leadDetailTab.value = "detail";
    leadDetailEditing.value = false;
    leadInterestedItems.value = [];
    ctx.route.value = "lead-detail";
    frappe.route_options = { view: "lead-detail", lead: row.name };
    frappe.set_route("dcnet-crm").then(() => {
      const url = new URL(window.location.href);
      url.hash = "";
      url.searchParams.set("view", "lead-detail");
      url.searchParams.set("lead", row.name);
      url.searchParams.delete("customer");
      url.searchParams.delete("opportunity");
      window.history.replaceState(window.history.state, "", url);
    });
  }

  function backToLeads() {
    ctx.navigate("leads");
  }

  async function openLeadForm(existingLead) {
    leadFormReturnName.value = ctx.route.value === "lead-detail" ? leadDetailName.value : "";
    ctx.route.value = "leads";
    await ensureLeadFormOptions();
    if (existingLead) {
      leadForm.value = { ...existingLead };
      leadFormMode.value = "edit";
    } else {
      leadForm.value = _emptyLeadForm();
      leadFormMode.value = "create";
    }
    leadFormOpen.value = true;
  }

  function closeLeadForm() {
    leadFormOpen.value = false;
    leadForm.value = {};
    if (leadFormReturnName.value) {
      const name = leadFormReturnName.value;
      leadFormReturnName.value = "";
      openLeadDetail({ name });
      loadLeadDetail(name);
    }
  }

  async function saveLead(addAnother) {
    if (addAnother === undefined) addAnother = false;
    if (leadFormSaving.value) return;
    if (!leadForm.value.first_name?.trim()) {
      frappe.msgprint(__("Tên là bắt buộc")); return;
    }
    if (!leadForm.value.mobile_no?.trim()) {
      frappe.msgprint(__("ĐT di động là bắt buộc")); return;
    }
    leadFormSaving.value = true;
    try {
      if (leadFormMode.value === "edit") {
        const editedName = leadForm.value.name;
        const returnToDetailName = leadFormReturnName.value || editedName;
        await call("update_lead", { name: editedName, data: leadForm.value }, "POST");
        leadFormOpen.value = false;
        leadForm.value = {};
        leadFormReturnName.value = "";
        openLeadDetail({ name: returnToDetailName });
        await loadLeadDetail(returnToDetailName);
      } else {
        await call("save_lead", { lead: leadForm.value }, "POST");
        if (addAnother) {
          leadForm.value = { ..._emptyLeadForm() };
        } else {
          closeLeadForm();
          await ctx.loadRows();
        }
      }
      frappe.show_alert({ message: __("Đã lưu thành công"), indicator: "green" });
    } catch (error) {
      frappe.msgprint(error.message || __("Không thể lưu tiềm năng."));
    } finally {
      leadFormSaving.value = false;
    }
  }

  async function saveLeadDetailEdit() {
    if (leadDetailSaving.value) return;
    leadDetailSaving.value = true;
    try {
      await call("update_lead", { name: leadDetailName.value, data: leadDetailForm.value }, "POST");
      leadDetailEditing.value = false;
      await loadLeadDetail();
      frappe.show_alert({ message: __("Đã cập nhật"), indicator: "green" });
    } catch (error) {
      frappe.msgprint(error.message || __("Không thể cập nhật tiềm năng."));
    } finally {
      leadDetailSaving.value = false;
    }
  }

  function beginLeadEdit() {
    leadDetailForm.value = { ...leadDetail.value?.document };
    leadDetailEditing.value = true;
  }

  function cancelLeadEdit() {
    leadDetailEditing.value = false;
    leadDetailForm.value = {};
  }

  function setLeadDetailTab(tab) {
    if (LEAD_DETAIL_TABS.some((item) => item.key === tab)) {
      leadDetailTab.value = tab;
    }
  }

  function showLeadDetailField(label, value) {
    const keyword = leadDetailFieldSearch.value.trim().toLocaleLowerCase("vi");
    const matchesSearch = !keyword || String(label || "").toLocaleLowerCase("vi").includes(keyword);
    const hasValue = value !== undefined && value !== null && value !== "" && value !== false;
    return matchesSearch && (leadShowEmpty.value || hasValue || leadDetailEditing.value);
  }

  function leadDetailTabLabel(tab) {
    return LEAD_DETAIL_TABS.find((item) => item.key === tab)?.label || "";
  }

  function leadDetailTabBadge(tab) {
    if (tab === "notes") return leadDetail.value?.document?.notes ? 1 : 0;
    if (tab === "attachments") return leadDetail.value?.attachments?.length || 0;
    if (tab === "interested_items") return leadInterestedItems.value.length;
    if (tab === "conversations") return leadDetail.value?.timeline?.length || 0;
    if (tab === "active_tasks") return leadActiveActivities.value.length;
    if (tab === "done_tasks") return leadDoneActivities.value.length;
    return 0;
  }

  function formatFileSize(bytes) {
    const size = Number(bytes || 0);
    if (!size) return "—";
    if (size < 1024) return `${size} B`;
    if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`;
    return `${(size / 1024 / 1024).toFixed(1)} MB`;
  }

  function notifyLeadTabAction(label) {
    frappe.msgprint({
      title: __(label),
      message: __("Chức năng này đang chờ cấu hình luồng xử lý/API theo spec."),
      indicator: "blue",
    });
  }

  function callLeadPhone() {
    const doc = leadDetail.value?.document || ctx.detail.value?.document || ctx.selected.value || {};
    const phone = doc.mobile_no || doc.phone;
    if (!phone) return notifyLeadTabAction("Gọi điện");
    window.location.href = `tel:${phone}`;
  }

  function emailLead() {
    const doc = leadDetail.value?.document || ctx.detail.value?.document || ctx.selected.value || {};
    const email = doc.custom_work_email || doc.email_id;
    if (!email) return notifyLeadTabAction("Gửi email");
    window.location.href = `mailto:${email}`;
  }

  function addLeadTag() {
    const name = leadDetail.value?.document?.name;
    if (!name) return;
    frappe.prompt(
      [{ fieldname: "tag", fieldtype: "Data", label: __("Tên thẻ"), reqd: 1 }],
      async (values) => {
        try {
          await frappe.call({
            method: "frappe.desk.doctype.tag.tag.add_tag",
            args: { tag: values.tag, dt: "Lead", dn: name },
            type: "POST",
          });
          frappe.show_alert({ message: __("Đã thêm thẻ"), indicator: "green" });
        } catch (error) {
          frappe.msgprint(error.message || __("Không thể thêm thẻ."));
        }
      },
      __("Thêm thẻ"),
      __("Thêm"),
    );
  }

  function addLeadAttachmentLink() {
    const target = leadDetailName.value;
    if (!target || !leadDetail.value?.can_write) return;
    frappe.prompt(
      [
        {
          fieldname: "url",
          fieldtype: "Data",
          label: __("Liên kết (URL)"),
          default: "https://",
          reqd: 1,
        },
        { fieldname: "title", fieldtype: "Data", label: __("Tên hiển thị") },
      ],
      async (values) => {
        try {
          await call("add_lead_attachment_link", {
            name: target,
            url: /^(https?:\/\/)/i.test(values.url.trim())
              ? values.url.trim()
              : `https://${values.url.trim()}`,
            title: values.title || "",
          }, "POST");
          await loadLeadDetail(target);
          leadDetailTab.value = "attachments";
          frappe.show_alert({ message: __("Đã thêm liên kết."), indicator: "green" });
        } catch (error) {
          frappe.msgprint(error.message || __("Không thể thêm liên kết."));
        }
      },
      __("Thêm liên kết"),
      __("Thêm"),
    );
  }

  function leadAttachmentIcon(file) {
    const fileUrl = String(file?.file_url || "");
    const fileName = String(file?.file_name || fileUrl).split(/[?#]/)[0].toLowerCase();
    const isExternalLink = /^https?:\/\//i.test(fileUrl) && !Number(file?.file_size || 0);
    if (isExternalLink) return "link";
    if (/\.(avif|bmp|gif|heic|jpeg|jpg|png|svg|webp)$/.test(fileName)) return "image";
    return "document";
  }

  async function uploadLeadAttachment(event) {
    const file = event?.target?.files?.[0];
    if (event?.target) event.target.value = "";
    const target = leadDetailName.value;
    if (!file || !target || !leadDetail.value?.can_write || leadAttachmentUploading.value) return;
    leadAttachmentUploading.value = true;
    try {
      const formData = new FormData();
      formData.append("file", file, file.name);
      formData.append("is_private", 1);
      formData.append("doctype", "Lead");
      formData.append("docname", target);
      const response = await window.fetch("/api/method/upload_file", {
        method: "POST",
        headers: { "X-Frappe-CSRF-Token": frappe.csrf_token },
        body: formData,
      });
      if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        throw new Error(data?._server_messages || data?.exception || __("Tải tệp thất bại"));
      }
      await loadLeadDetail(target);
      leadDetailTab.value = "attachments";
      frappe.show_alert({ message: __("Đã thêm tệp đính kèm."), indicator: "green" });
    } catch (error) {
      frappe.msgprint(error.message || __("Không thể tải tệp."));
    } finally {
      leadAttachmentUploading.value = false;
    }
  }

  function localLeadDateTimeInput(value = new Date()) {
    const date = value instanceof Date ? value : new Date(String(value).replace(" ", "T"));
    if (Number.isNaN(date.getTime())) return "";
    const offset = date.getTimezoneOffset() * 60000;
    return new Date(date.getTime() - offset).toISOString().slice(0, 16);
  }

  function leadActivityTypeLabel(type) {
    return type === "task" ? "Nhiệm vụ" : type === "call" ? "Cuộc gọi" : "Lịch hẹn";
  }

  function leadActivityStatusLabel(status) {
    return ({
      Open: "Chưa bắt đầu",
      Closed: "Hoàn thành",
      Completed: "Hoàn thành",
      Cancelled: "Đã hủy",
    })[status] || status || "—";
  }

  function formatLeadActivityDate(value) {
    if (!value) return "—";
    const text = String(value);
    const date = new Date(text.includes("T") ? text : text.replace(" ", "T"));
    if (Number.isNaN(date.getTime())) return text;
    const hasTime = /[ T]\d{2}:\d{2}/.test(text);
    return new Intl.DateTimeFormat("vi-VN", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      ...(hasTime ? { hour: "2-digit", minute: "2-digit", hour12: false } : {}),
    }).format(date);
  }

  function openLeadActivityDialog(activityType = "task") {
    if (!leadDetail.value?.can_create_activity) {
      frappe.msgprint(__("Bạn không có quyền tạo hoạt động."));
      return;
    }
    const startsOn = localLeadDateTimeInput();
    const endMinutes = activityType === "meeting" ? 60 : 30;
    const endsOn = localLeadDateTimeInput(new Date(new Date(startsOn).getTime() + endMinutes * 60000));
    const label = leadActivityTypeLabel(activityType);
    const leadName = leadDetail.value?.document?.lead_name || "";
    leadActivityForm.value = {
      activity_type: activityType,
      subject: `${label} - ${leadName}`.trim(),
      description: "",
      location: "",
      all_day: 0,
      due_date: startsOn.slice(0, 10),
      due_time: startsOn.slice(11, 16),
      starts_on: startsOn,
      ends_on: endsOn,
      status: "Open",
      priority: "Medium",
      allocated_to: ctx.boot.value?.user || "",
      campaign: "",
      related_to: "",
      task_type: "",
      call_minutes: 0,
      call_seconds: 30,
      call_type: "Gọi đi",
      call_result: "",
      phone: leadDetail.value?.document?.mobile_no || leadDetail.value?.document?.phone || "",
    };
    leadDetailTab.value = "active_tasks";
    leadActivityMoreOpen.value = false;
    leadActivityDialogOpen.value = true;
  }

  function closeLeadActivityDialog() {
    if (leadActivitySaving.value) return;
    leadActivityDialogOpen.value = false;
  }

  function updateLeadCallEnd() {
    const form = leadActivityForm.value;
    if (form.activity_type !== "call" || !form.starts_on) return;
    const durationMs = Math.max(Number(form.call_minutes || 0), 0) * 60000
      + Math.max(Number(form.call_seconds || 0), 0) * 1000;
    form.ends_on = localLeadDateTimeInput(new Date(new Date(form.starts_on).getTime() + durationMs));
  }

  async function saveLeadActivity() {
    const form = leadActivityForm.value;
    if (!form.subject?.trim() || leadActivitySaving.value) return;
    leadActivitySaving.value = true;
    try {
      if (form.activity_type === "call" && form.starts_on) {
        updateLeadCallEnd();
      }
      await call("save_lead_activity", {
        lead: leadDetailName.value,
        activity: {
          ...form,
          due_date: form.due_date || null,
        },
      }, "POST");
      leadActivityDialogOpen.value = false;
      await loadLeadDetail();
      leadDetailTab.value = form.status === "Open" ? "active_tasks" : "done_tasks";
      frappe.show_alert({ message: __(`Đã thêm ${leadActivityTypeLabel(form.activity_type).toLowerCase()}.`), indicator: "green" });
    } catch (error) {
      frappe.msgprint(error.message || __("Không thể lưu hoạt động."));
    } finally {
      leadActivitySaving.value = false;
    }
  }

  async function openLeadItemPicker() {
    await ensureLeadFormOptions();
    leadItemPickerSearch.value = "";
    leadItemPickerSelected.value = [];
    leadItemPickerPage.value = 1;
    leadItemPickerOpen.value = true;
  }

  function closeLeadItemPicker() {
    leadItemPickerOpen.value = false;
  }

  function toggleLeadItemPicker(name) {
    const index = leadItemPickerSelected.value.indexOf(name);
    if (index >= 0) leadItemPickerSelected.value.splice(index, 1);
    else leadItemPickerSelected.value.push(name);
  }

  function toggleLeadItemPickerPage(checked) {
    const pageNames = leadItemPickerRows.value.map((item) => item.name);
    if (checked) {
      const merged = new Set([...leadItemPickerSelected.value, ...pageNames]);
      leadItemPickerSelected.value = Array.from(merged);
      return;
    }
    leadItemPickerSelected.value = leadItemPickerSelected.value.filter((name) => !pageNames.includes(name));
  }

  function changeLeadItemPickerPage(delta) {
    const next = leadItemPickerPage.value + delta;
    leadItemPickerPage.value = Math.min(Math.max(next, 1), leadItemPickerPageCount.value);
  }

  function confirmLeadItemPicker() {
    const selected = leadItemPickerSelected.value
      .map((name) => leadFormOptions.value.items.find((item) => item.name === name))
      .filter(Boolean);
    for (const item of selected) {
      if (leadInterestedItems.value.some((row) => row.item_code === item.name)) continue;
      leadInterestedItems.value.push({
        item_code: item.name,
        item_name: item.item_name || item.name,
        item_group: item.item_group || "—",
        uom: item.stock_uom || "—",
      });
    }
    leadItemPickerOpen.value = false;
  }

  function convertLead() {
    const lead = leadDetail.value?.document;
    if (!lead?.name || lead.status === "Converted") return;
    frappe.confirm(
      __("Chuyển Lead {0} thành Customer và Opportunity?", [lead.lead_name || lead.name]),
      async () => {
        try {
          const result = await call("convert_lead", {
            name: lead.name,
            create_customer: 1,
            create_opportunity: 1,
          }, "POST");
          await loadLeadDetail(lead.name);
          frappe.msgprint({
            title: __("Chuyển đổi thành công"),
            message: __(
              "Customer: {0}<br>Opportunity: {1}",
              [result.customer || "—", result.opportunity || "—"],
            ),
            indicator: "green",
          });
        } catch (error) {
          frappe.msgprint(error.message || __("Không thể chuyển đổi Lead."));
        }
      },
    );
  }

  function importLeads() {
    frappe.new_doc("Data Import", { reference_doctype: "Lead", import_type: "Insert New Records" });
  }

  return {
    LEAD_DETAIL_TABS: visibleLeadDetailTabs, leadDetailName, leadDetail, leadDetailTab, leadDetailEditing, leadDetailSaving, leadDetailForm,
    leadShowEmpty, leadDetailFieldSearch, leadDetailMoreOpen, showLeadDetailField,
    LEAD_LIST_COLUMNS, leadActivityOpen, leadColumnDialogOpen,
    leadVisibleFields, leadShownColumns,
    leadFilterOpen, leadEnabledFilters, leadFilterValues,
    leadVisibleFilterDefinitions, leadAppliedFilterCount,
    leadFormOpen, leadFormMode, leadFormSaving, leadFormOptions, leadForm,
    leadInterestedItems, leadItemPickerOpen, leadItemPickerSearch, leadItemPickerSelected,
    leadItemPickerPage, leadItemPickerPageLength, leadItemPickerFiltered,
    leadItemPickerPageCount, leadItemPickerRows,
    leadActivityDialogOpen, leadActivitySaving, leadActivityMoreOpen, leadActivityForm,
    leadAttachmentUploading,
    leadActivities, leadActiveActivities, leadDoneActivities,
    loadLeadDetail, openLeadDetail, backToLeads, openLeadForm, closeLeadForm,
    saveLead, saveLeadDetailEdit, beginLeadEdit, cancelLeadEdit, setLeadDetailTab,
    leadDetailTabLabel, leadDetailTabBadge, formatFileSize, notifyLeadTabAction,
    callLeadPhone, emailLead, addLeadTag, addLeadAttachmentLink, uploadLeadAttachment,
    leadAttachmentIcon,
    openLeadActivityDialog, closeLeadActivityDialog, saveLeadActivity,
    updateLeadCallEnd,
    leadActivityTypeLabel, leadActivityStatusLabel, formatLeadActivityDate,
    openLeadItemPicker, closeLeadItemPicker, toggleLeadItemPicker, toggleLeadItemPickerPage,
    changeLeadItemPickerPage, confirmLeadItemPicker,
    buildLeadFilters, toggleLeadFilter, clearLeadFilters,
    toggleLeadColumn, resetLeadColumns,
    convertLead, importLeads, exportResource,
  };
}
