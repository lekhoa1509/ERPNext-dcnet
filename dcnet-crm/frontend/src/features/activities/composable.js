import { ref, computed } from "vue/dist/vue.esm-bundler.js";
import { call } from "../../utils.js";

const TASK_TYPES = [
  "Đề nghị xuất hóa đơn",
  "Giao hàng",
  "Đề nghị trả hàng",
  "Yêu cầu mua hàng",
  "Gửi báo giá",
  "Nhắc cước đến hạn",
  "Check TT DVVT",
  "Khảo sát DVVT",
  "Triển khai DVVT",
  "Lập PAKD",
  "Nghiệm thu DVVT",
  "Hỗ trợ kỹ thuật",
  "Chăm sóc khách hàng",
  "Họp tư vấn",
  "Khác",
];

export function useActivities(ctx) {
  const activityList = ref([]);
  const activityTotal = ref(0);
  const activityPage = ref(1);
  const activityPageLength = ref(20);
  const activitySearch = ref("");
  const activityStatusFilter = ref("all");
  const activityListLoading = ref(false);
  const activityFilterPanelOpen = ref(false);
  const activityCustomerFilter = ref("");
  const activityCustomerFilterLabel = ref("");

  const activitySelectedName = ref("");
  const activitySelectedDoctype = ref("ToDo");
  const activityDetail = ref(null);
  const activityDetailLoading = ref(false);
  const activityDetailTab = ref("info");

  const activityEditMode = ref(false);
  const activityEditForm = ref({});
  const activityEditSaving = ref(false);

  const activityInlineNote = ref("");
  const activityConversationText = ref("");
  const activityAttachUploading = ref(false);

  // User search state for "Người liên quan"
  const activityUserQuery = ref("");
  const activityUserDropdown = ref([]);
  const activityUserDropdownOpen = ref(false);
  let userSearchTimer = null;

  // Task type dropdown state
  const activityTaskTypeQuery = ref("");
  const activityTaskTypeOpen = ref(false);

  const filteredTaskTypes = computed(() => {
    const q = activityTaskTypeQuery.value.toLowerCase();
    return q ? TASK_TYPES.filter((t) => t.toLowerCase().includes(q)) : TASK_TYPES;
  });

  async function loadActivityList() {
    activityListLoading.value = true;
    try {
      const res = await call("get_activity_list", {
        search: activitySearch.value || "",
        page: activityPage.value,
        page_length: activityPageLength.value,
        status: activityStatusFilter.value === "all" ? "" : activityStatusFilter.value,
        customer: activityCustomerFilter.value || "",
      });
      activityList.value = res?.data || [];
      activityTotal.value = res?.total || 0;
    } catch {
      activityList.value = [];
      activityTotal.value = 0;
    } finally {
      activityListLoading.value = false;
    }
  }

  function changeActivityPage(page) {
    activityPage.value = page;
    loadActivityList();
  }

  function changeActivityPageLength() {
    activityPage.value = 1;
    loadActivityList();
  }

  function setActivityCustomerFilter(customer, customerLabel) {
    activityCustomerFilter.value = customer || "";
    activityCustomerFilterLabel.value = customerLabel || customer || "";
    activityPage.value = 1;
  }

  function clearActivityCustomerFilter() {
    activityCustomerFilter.value = "";
    activityCustomerFilterLabel.value = "";
    activityPage.value = 1;
    loadActivityList();
  }

  async function selectActivity(name, doctype = "") {
    const requestedDoctype = doctype || "ToDo";
    if (
      activitySelectedName.value === name
      && activitySelectedDoctype.value === requestedDoctype
      && activityDetail.value
    ) return;
    activitySelectedName.value = name;
    activitySelectedDoctype.value = requestedDoctype;
    activityDetail.value = null;
    activityEditMode.value = false;
    activityDetailTab.value = "info";
    activityInlineNote.value = "";
    activityConversationText.value = "";
    activityDetailLoading.value = true;
    try {
      activityDetail.value = await call("get_activity_detail", { name, doctype });
      activitySelectedDoctype.value = activityDetail.value?.doctype || requestedDoctype;
    } catch (err) {
      frappe.msgprint(err.message || "Không thể tải chi tiết hoạt động.");
    } finally {
      activityDetailLoading.value = false;
    }
  }

  function startActivityEdit() {
    if (!activityDetail.value) return;
    const d = activityDetail.value;
    activityEditForm.value = {
      description: d.description || "",
      date: d.date || "",
      status: d.status || "Open",
      priority: d.priority || "Medium",
      task_type: d.task_type || "",
      related_users: (d.related_users || []).map((u) => ({ name: u.name, full_name: u.full_name })),
    };
    activityUserQuery.value = "";
    activityUserDropdown.value = [];
    activityUserDropdownOpen.value = false;
    activityTaskTypeQuery.value = "";
    activityTaskTypeOpen.value = false;
    activityEditMode.value = true;
  }

  function cancelActivityEdit() {
    activityEditMode.value = false;
    activityEditForm.value = {};
    activityUserQuery.value = "";
    activityUserDropdown.value = [];
    activityUserDropdownOpen.value = false;
    activityTaskTypeQuery.value = "";
    activityTaskTypeOpen.value = false;
  }

  async function saveActivityEdit() {
    if (activityEditSaving.value) return;
    activityEditSaving.value = true;
    try {
      await call("update_activity", {
        name: activitySelectedName.value,
        data: activityEditForm.value,
      }, "POST");
      frappe.show_alert({ message: "Đã lưu hoạt động", indicator: "green" }, 3);
      activityEditMode.value = false;
      const current = activitySelectedName.value;
      activityDetail.value = null;
      await selectActivity(current, activitySelectedDoctype.value);
      await loadActivityList();
    } catch (err) {
      frappe.msgprint(err.message || "Không thể lưu.");
    } finally {
      activityEditSaving.value = false;
    }
  }

  async function markActivityDone(name) {
    try {
      await call("update_activity", { name, data: { status: "Closed" } }, "POST");
      if (activitySelectedName.value === name && activityDetail.value) {
        activityDetail.value = { ...activityDetail.value, status: "Closed" };
      }
      await loadActivityList();
      frappe.show_alert({ message: "Đã đánh dấu hoàn thành", indicator: "green" }, 3);
    } catch (err) {
      frappe.msgprint(err.message || "Không thể cập nhật trạng thái.");
    }
  }

  async function reloadActivityDetail() {
    const name = activitySelectedName.value;
    if (!name) return;
    try {
      activityDetail.value = await call("get_activity_detail", { name, doctype: activitySelectedDoctype.value });
    } catch (err) {
      frappe.msgprint(err.message || "Không thể tải chi tiết hoạt động.");
    }
  }

  async function saveActivityNoteFromDetail(source) {
    const target = activitySelectedName.value;
    const content = (source === "conversation" ? activityConversationText.value : activityInlineNote.value).trim();
    if (!target || !content) return;
    try {
      if (source === "conversation") {
        await call("add_activity_conversation", { name: target, content }, "POST");
      } else {
        await call("add_activity_note", { name: target, content }, "POST");
      }
      if (source === "conversation") activityConversationText.value = "";
      else activityInlineNote.value = "";
      await reloadActivityDetail();
      frappe.show_alert({ message: "Đã lưu nội dung.", indicator: "green" }, 3);
    } catch (err) {
      frappe.msgprint(err.message || "Không thể lưu nội dung.");
    }
  }

  async function uploadActivityFile(event) {
    const file = event?.target?.files?.[0];
    if (event?.target) event.target.value = "";
    const target = activitySelectedName.value;
    if (!file || !target || activityAttachUploading.value) return;
    activityAttachUploading.value = true;
    try {
      const formData = new FormData();
      formData.append("file", file, file.name);
      formData.append("is_private", 1);
      formData.append("doctype", "ToDo");
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
      await reloadActivityDetail();
      frappe.show_alert({ message: "Đã thêm tệp đính kèm.", indicator: "green" }, 3);
    } catch (err) {
      frappe.msgprint(err.message || "Không thể tải tệp.");
    } finally {
      activityAttachUploading.value = false;
    }
  }

  function addActivityAttachmentLink() {
    const target = activitySelectedName.value;
    if (!target) return;
    frappe.prompt(
      [
        { fieldname: "url", fieldtype: "Data", label: "Liên kết (URL)", default: "https://", reqd: 1 },
        { fieldname: "title", fieldtype: "Data", label: "Tên hiển thị" },
      ],
      async (values) => {
        try {
          await call("add_activity_attachment_link", {
            name: target,
            url: /^(https?:\/\/)/i.test(values.url.trim()) ? values.url.trim() : `https://${values.url.trim()}`,
            title: values.title || "",
          }, "POST");
          await reloadActivityDetail();
          frappe.show_alert({ message: "Đã thêm liên kết.", indicator: "green" }, 3);
        } catch (err) {
          frappe.msgprint(err.message || "Không thể thêm liên kết.");
        }
      },
      "Thêm liên kết",
      "Thêm"
    );
  }

  function deleteActivityAttachment(fileName) {
    if (!fileName) return;
    const target = activitySelectedName.value;
    frappe.confirm("Xóa tài liệu này?", async () => {
      try {
        await call("delete_activity_attachment", { file_name: fileName }, "POST");
        await reloadActivityDetail();
        frappe.show_alert({ message: "Đã xóa tài liệu.", indicator: "green" }, 3);
      } catch (err) {
        frappe.msgprint(err.message || "Không thể xóa tài liệu.");
      }
    });
  }

  // ── User search / multi-select ─────────────────────────────────────────────

  async function _fetchUsers(query) {
    try {
      const res = await call("search_crm_users", { query, limit: 20 });
      activityUserDropdown.value = res || [];
    } catch {
      activityUserDropdown.value = [];
    }
  }

  function onUserFocus() {
    if (!activityUserDropdownOpen.value || activityUserDropdown.value.length === 0) {
      activityUserDropdownOpen.value = true;
      _fetchUsers(activityUserQuery.value || "");
    }
  }

  function onUserQueryInput() {
    activityUserDropdownOpen.value = true;
    clearTimeout(userSearchTimer);
    userSearchTimer = setTimeout(() => _fetchUsers(activityUserQuery.value || ""), 200);
  }

  function isUserSelected(email) {
    return !!(activityEditForm.value.related_users || []).find((u) => u.name === email);
  }

  function toggleRelatedUser(user) {
    const form = activityEditForm.value;
    if (!form.related_users) form.related_users = [];
    if (isUserSelected(user.name)) {
      form.related_users = form.related_users.filter((u) => u.name !== user.name);
    } else {
      form.related_users = [...form.related_users, { name: user.name, full_name: user.full_name }];
    }
  }

  function removeRelatedUser(email) {
    const form = activityEditForm.value;
    if (!form.related_users) return;
    form.related_users = form.related_users.filter((u) => u.name !== email);
  }

  function closeUserDropdown() {
    activityUserDropdownOpen.value = false;
  }

  // ── Task type dropdown ─────────────────────────────────────────────────────

  function toggleTaskTypeDropdown() {
    activityTaskTypeOpen.value = !activityTaskTypeOpen.value;
    if (activityTaskTypeOpen.value) activityTaskTypeQuery.value = "";
  }

  function selectTaskType(type) {
    activityEditForm.value.task_type = type;
    activityTaskTypeOpen.value = false;
    activityTaskTypeQuery.value = "";
  }

  function closeTaskTypeDropdown() {
    activityTaskTypeOpen.value = false;
  }

  // ── Status / priority helpers ──────────────────────────────────────────────

  function actStatusLabel(status) {
    if (status === "Open") return "Đang thực hiện";
    if (status === "Closed") return "Hoàn thành";
    if (status === "Cancelled") return "Đã hủy";
    return status || "—";
  }

  function actStatusClass(status) {
    if (status === "Closed") return "act-status--done";
    if (status === "Cancelled") return "act-status--cancelled";
    return "act-status--open";
  }

  function actStatusBadgeClass(status) {
    if (status === "Closed") return "hd-badge-done";
    if (status === "Cancelled") return "hd-badge-cancelled";
    return "hd-badge-inprogress";
  }

  function actStatusPillClass(status) {
    if (status === "Open") return "hd-det-sp--open";
    if (status === "Cancelled") return "hd-det-sp--cancelled";
    return "";
  }

  function actStatusDotClass(status) {
    if (status === "Open") return "hd-det-sd--open";
    if (status === "Cancelled") return "hd-det-sd--cancelled";
    return "";
  }

  function actDetailStatusClass(status) {
    if (status === "Closed") return "hd-ct-status-done";
    if (status === "Cancelled") return "hd-ct-status-cancelled";
    return "hd-ct-status-open";
  }

  function fmtDT(dt) {
    if (!dt) return "—";
    const spaceIdx = dt.indexOf(" ");
    const datePart = spaceIdx > 0 ? dt.slice(0, spaceIdx) : dt;
    const timePart = spaceIdx > 0 ? dt.slice(spaceIdx + 1, spaceIdx + 6) : "";
    const [y, m, d] = datePart.split("-");
    if (!y || !m || !d) return dt;
    return timePart ? `${d}/${m}/${y}   ${timePart}` : `${d}/${m}/${y}`;
  }

  function fmtDate(d) {
    if (!d) return "—";
    const [y, m, day] = String(d).split("-");
    return y && m && day ? `${day}/${m}/${y}` : d;
  }

  function actPriorityLabel(p) {
    const m = { Low: "Thấp", Medium: "Trung bình", High: "Cao", Urgent: "Khẩn cấp" };
    return m[p] || p || "—";
  }

  function actPriorityClass(p) {
    if (p === "Urgent" || p === "High") return "act-priority--high";
    if (p === "Low") return "act-priority--low";
    return "act-priority--medium";
  }

  let activitySearchTimer;
  function onActivitySearchInput() {
    clearTimeout(activitySearchTimer);
    activityPage.value = 1;
    activitySearchTimer = setTimeout(loadActivityList, 300);
  }

  function changeActivityStatusFilter(status) {
    activityStatusFilter.value = status;
    activityPage.value = 1;
    loadActivityList();
  }

  function notifyActivityAction(label) {
    frappe.msgprint({
      title: __(label),
      message: __("Chức năng này đang chờ cấu hình luồng xử lý/API theo spec."),
      indicator: "blue",
    });
  }

  function clearActivitySelection() {
    activitySelectedName.value = "";
    activitySelectedDoctype.value = "ToDo";
    activityDetail.value = null;
    activityEditMode.value = false;
  }

  function openActivityDeskRecord(name = activitySelectedName.value) {
    if (!name) return notifyActivityAction("Mở hoạt động");
    frappe.set_route("Form", activityDetail.value?.doctype || activitySelectedDoctype.value || "ToDo", name);
  }

  function openActivityCustomer() {
    const customer = activityDetail.value?.customer;
    if (!customer) return notifyActivityAction("Mở khách hàng");
    ctx.openRelated("Customer", { name: customer });
  }

  function createRelatedActivity() {
    const customer = activityDetail.value?.customer;
    if (!customer) return notifyActivityAction("Thêm công việc");
    frappe.new_doc("ToDo", { reference_type: "Customer", reference_name: customer });
  }

  function callActivityCustomer() {
    const phone = activityDetail.value?.customer_info?.mobile_no;
    if (!phone) return notifyActivityAction("Gọi điện");
    window.location.href = `tel:${phone}`;
  }

  return {
    activityList, activityTotal, activityPage, activityPageLength,
    activitySearch, activityStatusFilter,
    activityFilterPanelOpen, activityCustomerFilter, activityCustomerFilterLabel,
    changeActivityPage, changeActivityPageLength,
    setActivityCustomerFilter, clearActivityCustomerFilter,
    activityListLoading, activitySelectedName, activitySelectedDoctype,
    activityDetail, activityDetailLoading, activityDetailTab,
    activityEditMode, activityEditForm, activityEditSaving,
    activityInlineNote, activityConversationText, activityAttachUploading,
    saveActivityNoteFromDetail, uploadActivityFile, addActivityAttachmentLink, deleteActivityAttachment,
    activityUserQuery, activityUserDropdown, activityUserDropdownOpen,
    activityTaskTypeQuery, activityTaskTypeOpen, filteredTaskTypes,
    loadActivityList, selectActivity,
    startActivityEdit, cancelActivityEdit, saveActivityEdit, markActivityDone,
    onUserFocus, onUserQueryInput, isUserSelected, toggleRelatedUser, removeRelatedUser, closeUserDropdown,
    toggleTaskTypeDropdown, selectTaskType, closeTaskTypeDropdown,
    actStatusLabel, actStatusClass, actStatusBadgeClass,
    actStatusPillClass, actStatusDotClass, actDetailStatusClass,
    actPriorityLabel, actPriorityClass,
    fmtDT, fmtDate,
    onActivitySearchInput, changeActivityStatusFilter,
    notifyActivityAction, clearActivitySelection, openActivityDeskRecord,
    openActivityCustomer, createRelatedActivity, callActivityCustomer,
  };
}
