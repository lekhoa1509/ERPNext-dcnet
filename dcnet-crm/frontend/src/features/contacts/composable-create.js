import { nextTick, ref, computed, watch } from "vue/dist/vue.esm-bundler.js";
import { call } from "../../utils.js";
import { fetchVnProvinces, fetchVnWards } from "../../utils-vn-address.js";

const CONTACT_DETAIL_TABS = [
  { key: "info", label: "Thông tin chi tiết" },
  { key: "notes", label: "Ghi chú" },
  { key: "attachments", label: "Tài liệu đính kèm" },
  { key: "purchased_items", label: "Hàng hóa đã mua" },
  { key: "opportunities", label: "Cơ hội" },
  { key: "orders", label: "Đơn hàng" },
  { key: "quotations", label: "Báo giá" },
  { key: "invoices", label: "Hóa đơn" },
  { key: "campaigns", label: "Chiến dịch" },
  { key: "active_tasks", label: "Công việc đang thực hiện" },
  { key: "done_tasks", label: "Công việc đã hoàn thành" },
  { key: "consult_cards", label: "Thẻ tư vấn" },
  { key: "email", label: "Email" },
  { key: "sms", label: "SMS" },
  { key: "routes", label: "Lộ trình di tuyến" },
  { key: "conversations", label: "Nội dung trao đổi" },
  { key: "other", label: "Khác" },
];

export function useCreateContact(ctx) {
  const createContactSaving = ref(false);
  const contactCreateOptions = ref({
    salutations: [], genders: [],
    customers: [], territories: [], countries: [],
  });
  const contactCreateOptionsLoaded = ref(false);

  const createContactForm = ref({});
  const ccBillingForm = ref({});
  const ccShippingForm = ref({});
  const ccSameAddress = ref(false);

  // ── VN Address cascade (2025 reform: tỉnh → phường/xã) ──────────
  const ccVnProvinces = ref([]);
  const ccVnBillingWards = ref([]);
  const ccVnShippingWards = ref([]);
  const ccLoadingBillingWards = ref(false);
  const ccLoadingShippingWards = ref(false);
  const ccBillingProvinceCode = ref("");
  const ccShippingProvinceCode = ref("");

  function _blankForm() {
    return {
      first_name: "",
      middle_name: "",
      last_name: "",
      salutation: "",
      designation: "",
      company_name: "",
      department: "",
      customer: "",
      gender: "",
      khong_goi_dien: 0,
      khong_gui_email: 0,
      mobile_no: "",
      phone: "",
      dien_thoai_khac: "",
      email_id: "",
      email_ca_nhan: "",
      zalo: "",
      phan_loai_kh: "",
      nguon_goc: "",
      mo_ta: "",
      dung_chung: 0,
    };
  }
  function _blankAddr() {
    return { address_line1: "", county: "", state: "", country: "Vietnam", pincode: "" };
  }

  function _resetForms() {
    createContactForm.value = _blankForm();
    ccBillingForm.value = _blankAddr();
    ccShippingForm.value = _blankAddr();
    ccSameAddress.value = false;
    ccBillingProvinceCode.value = "";
    ccShippingProvinceCode.value = "";
    ccVnBillingWards.value = [];
    ccVnShippingWards.value = [];
  }

  // Cascade billing province → wards
  watch(ccBillingProvinceCode, async (code) => {
    ccBillingForm.value.state = "";
    ccBillingForm.value.county = "";
    ccVnBillingWards.value = [];
    if (!code) return;
    const p = ccVnProvinces.value.find((x) => String(x.code) === String(code));
    if (p) ccBillingForm.value.state = p.name;
    ccLoadingBillingWards.value = true;
    ccVnBillingWards.value = await fetchVnWards(code);
    ccLoadingBillingWards.value = false;
  });

  // Cascade shipping province → wards
  watch(ccShippingProvinceCode, async (code) => {
    ccShippingForm.value.state = "";
    ccShippingForm.value.county = "";
    ccVnShippingWards.value = [];
    if (!code) return;
    const p = ccVnProvinces.value.find((x) => String(x.code) === String(code));
    if (p) ccShippingForm.value.state = p.name;
    ccLoadingShippingWards.value = true;
    ccVnShippingWards.value = await fetchVnWards(code);
    ccLoadingShippingWards.value = false;
  });

  async function _loadOptions() {
    if (contactCreateOptionsLoaded.value && contactCreateOptions.value.countries.length) return;
    try {
      const opts = await call("get_contact_create_options");
      if (opts) {
        contactCreateOptions.value = opts;
        if (opts.countries && opts.countries.length) contactCreateOptionsLoaded.value = true;
      }
    } catch {}
    if (!ccVnProvinces.value.length) {
      ccVnProvinces.value = await fetchVnProvinces();
    }
  }
  _loadOptions();

  function openCreateContact() {
    _resetForms();
    ctx.navigate("create-contact");
    _loadOptions();
  }

  function cancelCreateContact() {
    ctx.navigate("contacts");
  }

  function copyContactAddress() {
    ccSameAddress.value = !ccSameAddress.value;
    if (ccSameAddress.value) {
      ccShippingForm.value = { ...ccBillingForm.value };
      ccShippingProvinceCode.value = ccBillingProvinceCode.value;
      ccVnShippingWards.value = [...ccVnBillingWards.value];
    }
  }

  async function saveCreateContact(andNew = false) {
    if (createContactSaving.value) return;
    const f = createContactForm.value;
    if (!(f.first_name || "").trim()) {
      frappe.msgprint({ title: "Lỗi", message: "Tên là bắt buộc.", indicator: "red" });
      return;
    }
    createContactSaving.value = true;
    try {
      const payload = {
        first_name: f.first_name,
        last_name: f.last_name || "",
        salutation: f.salutation || "",
        designation: f.designation || "",
        company_name: f.company_name || "",
        department: f.department || "",
        mobile_no: f.mobile_no || "",
        phone: f.phone || "",
        email_id: f.email_id || "",
        customer: f.customer || "",
        billing_address: { ...ccBillingForm.value },
      };
      const result = await call("create_contact_standalone", { data: payload }, "POST");
      frappe.show_alert({ message: `Đã tạo liên hệ ${result.full_name || result.name}`, indicator: "green" });
      if (andNew) {
        _resetForms();
      } else {
        ctx.navigate("contacts");
      }
    } catch (err) {
      frappe.msgprint({ title: "Lỗi", message: err.message || "Không thể tạo liên hệ.", indicator: "red" });
    } finally {
      createContactSaving.value = false;
    }
  }

  // ════════ CONTACT DETAIL / EDIT (MISA-style) ════════
  const contactDetailTab = ref("info");
  const contactDetailShowEmpty = ref(true);
  const contactDetailFieldSearch = ref("");
  const contactRightTab = ref("activity");
  const contactDetailName = ref("");
  const contactDetail = ref(null);
  const contactDetailLoading = ref(false);
  const contactDetailEditing = ref(false);
  const contactDetailSaving = ref(false);
  const contactNoteText = ref("");
  const contactNoteSaving = ref(false);
  const contactAttachUploading = ref(false);
  const contactActivityDialogOpen = ref(false);
  const contactActivitySaving = ref(false);
  const contactActivityMoreOpen = ref(false);
  const contactActivityForm = ref({});
  const contactActivities = computed(() => contactDetail.value?.activities || []);
  const contactActiveActivities = computed(() => contactActivities.value.filter((item) => item.status === "Open"));
  const contactDoneActivities = computed(() => contactActivities.value.filter((item) => item.status !== "Open"));
  // Opportunity picker (Chọn cơ hội) state
  const oppPickerOpen = ref(false);
  const oppPickerRows = ref([]);
  const oppPickerTotal = ref(0);
  const oppPickerSearch = ref("");
  const oppPickerPage = ref(1);
  const oppPickerPageLength = ref(20);
  const oppPickerSelected = ref([]);
  const oppPickerLoading = ref(false);
  const oppPickerSaving = ref(false);
  const oppPickerPageCount = computed(() =>
    Math.max(1, Math.ceil(oppPickerTotal.value / oppPickerPageLength.value)));
  const oppPickerAllChecked = computed(() =>
    oppPickerRows.value.length > 0 &&
    oppPickerRows.value.every((r) => oppPickerSelected.value.includes(r.name)));
  const cdForm = ref(_blankForm());
  const cdBillingForm = ref(_blankAddr());
  const cdShippingForm = ref(_blankAddr());
  const cdSameAddress = ref(false);
  const cdAddressName = ref("");
  const cdVnBillingWards = ref([]);
  const cdVnShippingWards = ref([]);
  const cdLoadingBillingWards = ref(false);
  const cdLoadingShippingWards = ref(false);

  function normalizeContactFieldText(value) {
    return String(value || "")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLocaleLowerCase("vi")
      .trim();
  }

  async function filterContactDetailFields() {
    await nextTick();
    const root = document.querySelector(".ccd-info-view");
    if (!root) return;
    const keyword = normalizeContactFieldText(contactDetailFieldSearch.value);
    root.querySelectorAll(".sod-section").forEach((section) => {
      let visibleRows = 0;
      section.querySelectorAll(".sod-drow").forEach((row) => {
        if (!row.querySelector(".sod-dlabel")) return;
        const label = normalizeContactFieldText(row.querySelector(".sod-dlabel")?.textContent);
        const valueElement = row.querySelector(".sod-dval");
        const value = normalizeContactFieldText(valueElement?.textContent);
        const isEmpty = !value || value === "—" || value.includes("khong chon");
        const matchesSearch = !keyword || label.includes(keyword);
        const matchesEmptyState = contactDetailEditing.value || contactDetailShowEmpty.value || !isEmpty;
        const visible = matchesSearch && matchesEmptyState;
        row.hidden = !visible;
        if (visible) visibleRows += 1;
      });
      section.hidden = visibleRows === 0;
    });
  }

  watch(
    [contactDetailFieldSearch, contactDetailShowEmpty, contactDetailEditing, contactDetailTab],
    filterContactDetailFields
  );
  const cdBillingProvinceCode = ref("");
  const cdShippingProvinceCode = ref("");
  const _cdPendingBillingWard = ref("");
  const _cdPendingShippingWard = ref("");

  function _matchProvince(rawName) {
    if (!rawName || !ccVnProvinces.value.length) return null;
    const norm = (str) => str.toLowerCase().replace(/^tp\.?\s+/i, "").replace(/^thành phố\s+/i, "").replace(/^tỉnh\s+/i, "").replace(/\s+/g, " ").trim();
    const target = norm(rawName);
    return ccVnProvinces.value.find((prov) => {
      const pn = norm(prov.name);
      return pn === target || pn.includes(target) || target.includes(pn);
    }) || null;
  }
  function _matchWard(wards, rawName) {
    if (!rawName || !wards.length) return null;
    const norm = (str) => str.toLowerCase().replace(/\s+/g, " ").trim();
    const target = norm(rawName);
    return wards.find((ward) => norm(ward.name) === target)
      || wards.find((ward) => norm(ward.name).includes(target) || target.includes(norm(ward.name)))
      || null;
  }

  watch(cdBillingProvinceCode, async (code) => {
    cdBillingForm.value.state = "";
    cdBillingForm.value.county = "";
    cdVnBillingWards.value = [];
    if (!code) return;
    const prov = ccVnProvinces.value.find((x) => String(x.code) === String(code));
    if (prov) cdBillingForm.value.state = prov.name;
    cdLoadingBillingWards.value = true;
    cdVnBillingWards.value = await fetchVnWards(code);
    cdLoadingBillingWards.value = false;
    if (_cdPendingBillingWard.value) {
      const matched = _matchWard(cdVnBillingWards.value, _cdPendingBillingWard.value);
      if (matched) cdBillingForm.value.county = matched.name;
      _cdPendingBillingWard.value = "";
    }
  });
  watch(cdShippingProvinceCode, async (code) => {
    cdShippingForm.value.state = "";
    cdShippingForm.value.county = "";
    cdVnShippingWards.value = [];
    if (!code) return;
    const prov = ccVnProvinces.value.find((x) => String(x.code) === String(code));
    if (prov) cdShippingForm.value.state = prov.name;
    cdLoadingShippingWards.value = true;
    cdVnShippingWards.value = await fetchVnWards(code);
    cdLoadingShippingWards.value = false;
    if (_cdPendingShippingWard.value) {
      const matched = _matchWard(cdVnShippingWards.value, _cdPendingShippingWard.value);
      if (matched) cdShippingForm.value.county = matched.name;
      _cdPendingShippingWard.value = "";
    }
  });

  function _applyContactDetailToForm(detail) {
    cdForm.value = {
      ..._blankForm(),
      first_name: detail.first_name || "",
      last_name: detail.last_name || "",
      middle_name: detail.middle_name || "",
      salutation: detail.salutation || "",
      designation: detail.designation || "",
      company_name: detail.company_name || "",
      department: detail.department || "",
      customer: detail.customer || "",
      gender: detail.gender || "",
      mobile_no: detail.mobile_no || "",
      phone: detail.phone || "",
      email_id: detail.email_id || "",
    };
    const billing = detail.billing_address || {};
    cdBillingForm.value = {
      address_line1: billing.address_line1 || "",
      county: billing.county || "",
      state: billing.state || "",
      country: billing.country || "Vietnam",
      pincode: billing.pincode || "",
    };
    cdShippingForm.value = _blankAddr();
    cdShippingProvinceCode.value = "";
    cdVnShippingWards.value = [];
    cdSameAddress.value = false;
    cdAddressName.value = detail.address_name || "";
    // Try to cascade billing province from text
    cdBillingProvinceCode.value = "";
    if (billing.state) {
      const matched = _matchProvince(billing.state);
      if (matched) {
        _cdPendingBillingWard.value = billing.county || "";
        cdBillingProvinceCode.value = String(matched.code);
      }
    }
  }

  async function loadContactDetail(name) {
    const target = name || contactDetailName.value;
    if (!target) return;
    contactDetailName.value = target;
    contactDetailLoading.value = true;
    contactDetailEditing.value = false;
    contactDetail.value = null;
    await _loadOptions();
    try {
      const detail = await call("get_contact_detail", { name: target });
      contactDetail.value = detail;
      _applyContactDetailToForm(detail);
    } catch (err) {
      frappe.msgprint({ title: "Lỗi", message: err.message || "Không thể tải liên hệ.", indicator: "red" });
    } finally {
      contactDetailLoading.value = false;
    }
  }

  async function addContactNote() {
    const content = contactNoteText.value.trim();
    if (!content || contactNoteSaving.value) return;
    const target = contactDetailName.value;
    if (!target) return;
    contactNoteSaving.value = true;
    try {
      await call("add_note", { resource: "contacts", name: target, content }, "POST");
      contactNoteText.value = "";
      await loadContactDetail(target);
    } catch (err) {
      frappe.msgprint({ title: "Lỗi", message: err.message || "Không thể thêm ghi chú.", indicator: "red" });
    } finally {
      contactNoteSaving.value = false;
    }
  }

  function formatFileSize(bytes) {
    const n = Number(bytes) || 0;
    if (n < 1024) return n + " B";
    if (n < 1024 * 1024) return (n / 1024).toFixed(1) + " KB";
    return (n / (1024 * 1024)).toFixed(1) + " MB";
  }

  function contactDetailTabLabel(tab) {
    return CONTACT_DETAIL_TABS.find((item) => item.key === tab)?.label || "";
  }

  function contactDetailTabBadge(tab) {
    const detail = contactDetail.value || {};
    if (tab === "notes") return detail.notes?.length || 0;
    if (tab === "attachments") return detail.attachments?.length || 0;
    if (tab === "purchased_items") return detail.purchased_items?.length || 0;
    if (tab === "opportunities") return detail.opportunities?.length || 0;
    if (tab === "orders") return detail.orders?.length || 0;
    if (tab === "quotations") return detail.quotations?.length || 0;
    if (tab === "invoices") return detail.invoices?.length || 0;
    if (tab === "active_tasks") return contactActiveActivities.value.length;
    if (tab === "done_tasks") return contactDoneActivities.value.length;
    return 0;
  }

  function notifyContactTabAction(label) {
    frappe.msgprint({
      title: __(label),
      message: __("Chức năng này đang chờ cấu hình luồng xử lý/API theo spec."),
      indicator: "blue",
    });
  }

  function openContactRelated(doctype, name) {
    if (!doctype || !name) return;
    ctx.openRelated(doctype, { name });
  }

  function createOpportunityFromContact() {
    const detail = contactDetail.value || {};
    if (!detail.name) return;
    ctx.openOpportunityForm(detail.customer || "", detail.full_name || detail.name, detail.name);
  }

  function callContactPhone() {
    const detail = contactDetail.value || {};
    const phone = detail.mobile_no || detail.phone;
    if (!phone) return notifyContactTabAction("Gọi điện");
    window.location.href = `tel:${phone}`;
  }

  function emailContact() {
    const email = contactDetail.value?.email_id;
    if (!email) return notifyContactTabAction("Gửi email");
    window.location.href = `mailto:${email}`;
  }

  function addContactTag() {
    const name = contactDetailName.value;
    if (!name) return;
    frappe.prompt(
      [{ fieldname: "tag", fieldtype: "Data", label: __("Tên thẻ"), reqd: 1 }],
      async (values) => {
        try {
          await frappe.call({
            method: "frappe.desk.doctype.tag.tag.add_tag",
            args: { tag: values.tag, dt: "Contact", dn: name },
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

  function contactAttachmentIcon(file) {
    const fileUrl = String(file?.file_url || "");
    const fileName = String(file?.file_name || fileUrl).split(/[?#]/)[0].toLowerCase();
    const isExternalLink = /^https?:\/\//i.test(fileUrl) && !Number(file?.file_size || 0);
    if (isExternalLink) return "link";
    if (/\.(avif|bmp|gif|heic|jpeg|jpg|png|svg|webp)$/.test(fileName)) return "image";
    return "document";
  }

  function localContactDateTimeInput(value = new Date()) {
    const date = value instanceof Date ? value : new Date(String(value).replace(" ", "T"));
    if (Number.isNaN(date.getTime())) return "";
    const offset = date.getTimezoneOffset() * 60000;
    return new Date(date.getTime() - offset).toISOString().slice(0, 16);
  }

  function contactActivityTypeLabel(type) {
    return type === "task" ? "Nhiệm vụ" : type === "call" ? "Cuộc gọi" : "Lịch hẹn";
  }

  function contactActivityStatusLabel(status) {
    return ({
      Open: "Chưa bắt đầu",
      Closed: "Hoàn thành",
      Completed: "Hoàn thành",
      Cancelled: "Đã hủy",
    })[status] || status || "—";
  }

  function formatContactActivityDate(value) {
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

  function openContactActivityDialog(activityType = "task") {
    if (!contactDetail.value?.can_create_activity) {
      frappe.msgprint(__("Bạn không có quyền tạo hoạt động."));
      return;
    }
    const startsOn = localContactDateTimeInput();
    const endMinutes = activityType === "meeting" ? 60 : 30;
    const endsOn = localContactDateTimeInput(new Date(new Date(startsOn).getTime() + endMinutes * 60000));
    const label = contactActivityTypeLabel(activityType);
    const contactName = contactDetail.value?.full_name || contactDetail.value?.name || "";
    contactActivityForm.value = {
      activity_type: activityType,
      subject: `${label} - ${contactName}`.trim(),
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
      phone: contactDetail.value?.mobile_no || contactDetail.value?.phone || "",
    };
    contactDetailTab.value = "active_tasks";
    contactActivityMoreOpen.value = false;
    contactActivityDialogOpen.value = true;
  }

  function closeContactActivityDialog() {
    if (contactActivitySaving.value) return;
    contactActivityDialogOpen.value = false;
  }

  function updateContactCallEnd() {
    const form = contactActivityForm.value;
    if (form.activity_type !== "call" || !form.starts_on) return;
    const durationMs = Math.max(Number(form.call_minutes || 0), 0) * 60000
      + Math.max(Number(form.call_seconds || 0), 0) * 1000;
    form.ends_on = localContactDateTimeInput(new Date(new Date(form.starts_on).getTime() + durationMs));
  }

  async function saveContactActivity() {
    const form = contactActivityForm.value;
    if (!form.subject?.trim() || contactActivitySaving.value) return;
    contactActivitySaving.value = true;
    try {
      if (form.activity_type === "call" && form.starts_on) updateContactCallEnd();
      await call("save_contact_activity", {
        contact: contactDetailName.value,
        activity: { ...form, due_date: form.due_date || null },
      }, "POST");
      contactActivityDialogOpen.value = false;
      const target = contactDetailName.value;
      await loadContactDetail(target);
      contactDetailTab.value = form.status === "Open" ? "active_tasks" : "done_tasks";
      frappe.show_alert({ message: __(`Đã thêm ${contactActivityTypeLabel(form.activity_type).toLowerCase()}.`), indicator: "green" });
    } catch (error) {
      frappe.msgprint(error.message || __("Không thể lưu hoạt động."));
    } finally {
      contactActivitySaving.value = false;
    }
  }

  async function uploadContactFile(event) {
    const file = event?.target?.files?.[0];
    if (event?.target) event.target.value = "";
    const target = contactDetailName.value;
    if (!file || !target || !contactDetail.value?.can_write || contactAttachUploading.value) return;
    contactAttachUploading.value = true;
    try {
      const formData = new FormData();
      formData.append("file", file, file.name);
      formData.append("is_private", 1);
      formData.append("doctype", "Contact");
      formData.append("docname", target);
      const res = await window.fetch("/api/method/upload_file", {
        method: "POST",
        headers: { "X-Frappe-CSRF-Token": frappe.csrf_token },
        body: formData,
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data?._server_messages || data?.exception || "Tải tệp thất bại");
      }
      await loadContactDetail(target);
      contactDetailTab.value = "attachments";
      frappe.show_alert({ message: __("Đã thêm tệp đính kèm."), indicator: "green" });
    } catch (err) {
      frappe.msgprint({ title: "Lỗi", message: err.message || "Tải tệp thất bại.", indicator: "red" });
    } finally {
      contactAttachUploading.value = false;
    }
  }

  function addContactAttachmentLink() {
    const target = contactDetailName.value;
    if (!target || !contactDetail.value?.can_write) return;
    frappe.prompt(
      [
        { fieldname: "url", fieldtype: "Data", label: "Liên kết (URL)", default: "https://", reqd: 1 },
        { fieldname: "title", fieldtype: "Data", label: "Tên hiển thị" },
      ],
      async (values) => {
        try {
          await call("add_contact_attachment_link", {
            name: target,
            url: /^(https?:\/\/)/i.test(values.url.trim()) ? values.url.trim() : `https://${values.url.trim()}`,
            title: values.title || "",
          }, "POST");
          await loadContactDetail(target);
          contactDetailTab.value = "attachments";
          frappe.show_alert({ message: __("Đã thêm liên kết."), indicator: "green" });
        } catch (err) {
          frappe.msgprint({ title: "Lỗi", message: err.message || "Không thể thêm liên kết.", indicator: "red" });
        }
      },
      "Thêm liên kết",
      "Thêm"
    );
  }

  function deleteContactAttachment(fileName) {
    if (!fileName) return;
    frappe.confirm("Xóa tài liệu này?", async () => {
      try {
        await call("delete_contact_attachment", { file_name: fileName }, "POST");
        await loadContactDetail(contactDetailName.value);
      } catch (err) {
        frappe.msgprint({ title: "Lỗi", message: err.message || "Không thể xóa tài liệu.", indicator: "red" });
      }
    });
  }

  let oppPickerSearchTimer = null;

  async function loadOppPicker() {
    oppPickerLoading.value = true;
    try {
      const res = await call("get_linkable_opportunities", {
        contact: contactDetailName.value,
        search: oppPickerSearch.value || "",
        page: oppPickerPage.value,
        page_length: oppPickerPageLength.value,
      });
      oppPickerRows.value = res?.rows || [];
      oppPickerTotal.value = res?.total || 0;
    } catch (err) {
      frappe.msgprint({ title: "Lỗi", message: err.message || "Không thể tải danh sách cơ hội.", indicator: "red" });
    } finally {
      oppPickerLoading.value = false;
    }
  }

  function openOppPicker() {
    if (!contactDetailName.value) return;
    oppPickerSearch.value = "";
    oppPickerPage.value = 1;
    oppPickerSelected.value = [];
    oppPickerOpen.value = true;
    loadOppPicker();
  }

  function closeOppPicker() {
    oppPickerOpen.value = false;
  }

  function isOppPicked(name) {
    return oppPickerSelected.value.includes(name);
  }

  function toggleOppPickerRow(name) {
    const i = oppPickerSelected.value.indexOf(name);
    if (i >= 0) oppPickerSelected.value.splice(i, 1);
    else oppPickerSelected.value.push(name);
  }

  function toggleOppPickerAll() {
    if (oppPickerAllChecked.value) {
      const pageNames = new Set(oppPickerRows.value.map((r) => r.name));
      oppPickerSelected.value = oppPickerSelected.value.filter((n) => !pageNames.has(n));
    } else {
      oppPickerRows.value.forEach((r) => {
        if (!oppPickerSelected.value.includes(r.name)) oppPickerSelected.value.push(r.name);
      });
    }
  }

  function onOppPickerSearch() {
    clearTimeout(oppPickerSearchTimer);
    oppPickerPage.value = 1;
    oppPickerSearchTimer = setTimeout(loadOppPicker, 300);
  }

  function oppPickerChangePage(delta) {
    const next = Math.min(oppPickerPageCount.value, Math.max(1, oppPickerPage.value + delta));
    if (next !== oppPickerPage.value) {
      oppPickerPage.value = next;
      loadOppPicker();
    }
  }

  async function confirmOppPicker() {
    if (!oppPickerSelected.value.length) { closeOppPicker(); return; }
    oppPickerSaving.value = true;
    try {
      await call("link_opportunities_to_contact", {
        contact: contactDetailName.value,
        opportunities: JSON.stringify(oppPickerSelected.value),
      }, "POST");
      oppPickerOpen.value = false;
      await loadContactDetail(contactDetailName.value);
    } catch (err) {
      frappe.msgprint({ title: "Lỗi", message: err.message || "Không thể liên kết cơ hội.", indicator: "red" });
    } finally {
      oppPickerSaving.value = false;
    }
  }

  function unlinkContactOpportunity(opportunity) {
    if (!opportunity) return;
    frappe.confirm("Bỏ liên kết cơ hội này khỏi liên hệ?", async () => {
      try {
        await call("unlink_opportunity_from_contact", { opportunity }, "POST");
        await loadContactDetail(contactDetailName.value);
      } catch (err) {
        frappe.msgprint({ title: "Lỗi", message: err.message || "Không thể bỏ liên kết.", indicator: "red" });
      }
    });
  }

  function openContactDetail(row) {
    const name = row?.name || row;
    if (!name) return;
    contactDetailName.value = name;
    ctx.route.value = "contact-detail";
    const url = new URL(window.location.href);
    url.hash = "";
    url.searchParams.set("view", "contact-detail");
    url.searchParams.set("contact", name);
    window.history.replaceState(window.history.state, "", url);
    window.sessionStorage.setItem("dcnet-crm-view", "contact-detail");
    loadContactDetail(name);
  }

  function backToContacts() {
    contactDetailEditing.value = false;
    ctx.navigate("contacts");
  }

  function startContactEdit() {
    if (!contactDetail.value?.can_write) {
      frappe.msgprint({ title: "Không đủ quyền", message: "Bạn không có quyền sửa liên hệ này.", indicator: "orange" });
      return;
    }
    contactDetailEditing.value = true;
  }

  function cancelContactEdit() {
    if (contactDetail.value) _applyContactDetailToForm(contactDetail.value);
    contactDetailEditing.value = false;
  }

  function copyContactDetailAddress() {
    cdSameAddress.value = !cdSameAddress.value;
    if (cdSameAddress.value) {
      cdShippingForm.value = { ...cdBillingForm.value };
      cdShippingProvinceCode.value = cdBillingProvinceCode.value;
      cdVnShippingWards.value = [...cdVnBillingWards.value];
    }
  }

  async function saveContactDetail() {
    if (contactDetailSaving.value) return;
    const f = cdForm.value;
    if (!(f.first_name || "").trim()) {
      frappe.msgprint({ title: "Lỗi", message: "Tên là bắt buộc.", indicator: "red" });
      return;
    }
    contactDetailSaving.value = true;
    try {
      const payload = {
        first_name: f.first_name,
        last_name: f.last_name || "",
        salutation: f.salutation || "",
        designation: f.designation || "",
        company_name: f.company_name || "",
        department: f.department || "",
        gender: f.gender || "",
        mobile_no: f.mobile_no || "",
        phone: f.phone || "",
        email_id: f.email_id || "",
        customer: f.customer || "",
        address_name: cdAddressName.value || "",
        billing_address: { ...cdBillingForm.value },
      };
      const result = await call("update_contact_standalone", { name: contactDetailName.value, data: payload }, "POST");
      frappe.show_alert({ message: `Đã lưu liên hệ ${result.full_name || result.name}`, indicator: "green" });
      contactDetailEditing.value = false;
      await loadContactDetail(contactDetailName.value);
    } catch (err) {
      frappe.msgprint({ title: "Lỗi", message: err.message || "Không thể lưu liên hệ.", indicator: "red" });
    } finally {
      contactDetailSaving.value = false;
    }
  }

  return {
    createContactSaving, contactCreateOptions,
    createContactForm, ccBillingForm, ccShippingForm, ccSameAddress,
    ccVnProvinces, ccVnBillingWards, ccVnShippingWards,
    ccLoadingBillingWards, ccLoadingShippingWards,
    ccBillingProvinceCode, ccShippingProvinceCode,
    openCreateContact, cancelCreateContact, copyContactAddress, saveCreateContact,
    // Contact detail / edit
    CONTACT_DETAIL_TABS,
    contactDetailTab, contactDetailShowEmpty, contactDetailFieldSearch, contactRightTab,
    filterContactDetailFields,
    contactDetailName, contactDetail, contactDetailLoading, contactDetailEditing, contactDetailSaving,
    contactNoteText, contactNoteSaving, addContactNote,
    contactAttachUploading, formatFileSize, contactDetailTabLabel, contactDetailTabBadge,
    notifyContactTabAction, openContactRelated, createOpportunityFromContact,
    callContactPhone, emailContact, addContactTag,
    contactAttachmentIcon, uploadContactFile, addContactAttachmentLink, deleteContactAttachment,
    contactActivities, contactActiveActivities, contactDoneActivities,
    contactActivityDialogOpen, contactActivitySaving, contactActivityMoreOpen, contactActivityForm,
    contactActivityTypeLabel, contactActivityStatusLabel, formatContactActivityDate,
    openContactActivityDialog, closeContactActivityDialog, updateContactCallEnd, saveContactActivity,
    unlinkContactOpportunity,
    oppPickerOpen, oppPickerRows, oppPickerTotal, oppPickerSearch, oppPickerPage, oppPickerPageLength,
    oppPickerSelected, oppPickerLoading, oppPickerSaving, oppPickerPageCount, oppPickerAllChecked,
    openOppPicker, closeOppPicker, isOppPicked, toggleOppPickerRow, toggleOppPickerAll,
    onOppPickerSearch, oppPickerChangePage, confirmOppPicker,
    cdForm, cdBillingForm, cdShippingForm, cdSameAddress, cdAddressName,
    cdVnBillingWards, cdVnShippingWards, cdLoadingBillingWards, cdLoadingShippingWards,
    cdBillingProvinceCode, cdShippingProvinceCode,
    loadContactDetail, openContactDetail, backToContacts,
    startContactEdit, cancelContactEdit, copyContactDetailAddress, saveContactDetail,
  };
}
