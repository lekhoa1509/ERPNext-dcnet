import { ref, watch } from "vue/dist/vue.esm-bundler.js";
import { call } from "../../utils.js";
import { fetchVnProvinces, fetchVnWards } from "../../utils-vn-address.js";

export function useCreateCustomer(ctx) {
  const createOpen = ref(false);
  const createSaving = ref(false);
  const createOptions = ref({
    customer_groups: [],
    territories: [],
    industries: [],
    countries: [],
    market_segments: [],
    price_lists: [],
    sources: [],
    legal_types: [],
    business_lines: [],
  });
  const createOptionsLoaded = ref(false);

  const createCustomerForm = ref({
    // Thông tin chung
    customer_name: "",
    ten_viet_tat: "",
    misa_mobile: "",
    misa_email: "",
    tax_id: "",
    nguon_goc: "",
    customer_group: "",
    industry: "",
    loai_hinh: "",
    nganh_nghe: "",
    customer_type: "Company",
    // Thông tin bổ sung
    tai_khoan_ngan_hang: "",
    mo_tai_ngan_hang: "",
    ngay_thanh_lap: "",
    la_kh_tu: "",
    quy_mo_doanh_thu: "",
    quy_mo_nhan_su: "",
    loai_han_muc_no: "Không giới hạn",
    so_ngay_duoc_no: 0,
    website: "",
    // Mô tả
    customer_details: "",
    // Hệ thống
    dung_chung: 0,
    la_kh_ca_nhan: 0,
    la_doi_tac_ctv: 0,
    doi_tac_gioi_thieu: "",
    // ERPNext required
    territory: "",
  });

  const createContactForm = ref({
    first_name: "",
    mobile_no: "",
    email_id: "",
  });

  const createBillingForm = ref({
    address_line1: "",
    county: "",       // Phường/Xã
    city: "",         // Quận/Huyện
    state: "",        // Tỉnh/TP
    country: "Vietnam",
    pincode: "",
  });

  const createShippingForm = ref({
    address_line1: "",
    county: "",
    city: "",
    state: "",
    country: "Vietnam",
    pincode: "",
  });

  const createSameAddress = ref(false);

  // ── VN Address (2025 reform: tỉnh → phường/xã, bỏ quận/huyện) ───
  const vnProvinces = ref([]);
  const vnBillingWards = ref([]);
  const vnShippingWards = ref([]);
  const vnLoadingBillingWards = ref(false);
  const vnLoadingShippingWards = ref(false);
  const billingProvinceCode = ref("");
  const shippingProvinceCode = ref("");
  const _pendingBillingWard = ref("");   // ward name to auto-select after wards load
  const _pendingShippingWard = ref(""); // same for shipping

  // Parse a Vietnamese address string → { province, ward, street }
  function _parseVnAddress(addressStr) {
    if (!addressStr) return {};
    const parts = addressStr.split(",").map(s => s.trim()).filter(Boolean);
    const provincePart = parts[parts.length - 1] || "";
    let wardPart = "";
    let wardIdx = -1;
    for (let i = parts.length - 2; i >= 0; i--) {
      if (/^(phường|xã|thị trấn|đặc khu)/i.test(parts[i])) {
        wardPart = parts[i];
        wardIdx = i;
        break;
      }
    }
    const street = wardIdx > 0 ? parts.slice(0, wardIdx).join(", ") : parts.slice(0, parts.length - 1).join(", ");
    return { province: provincePart, ward: wardPart, street };
  }

  function _matchProvince(rawName) {
    if (!rawName || !vnProvinces.value.length) return null;
    const norm = s => s.toLowerCase().replace(/^tp\.?\s+/i, "").replace(/^thành phố\s+/i, "").replace(/^tỉnh\s+/i, "").replace(/\s+/g, " ").trim();
    const target = norm(rawName);
    return vnProvinces.value.find(p => {
      const pn = norm(p.name);
      return pn === target || pn.includes(target) || target.includes(pn);
    }) || null;
  }

  function _matchWard(wards, rawName) {
    if (!rawName || !wards.length) return null;
    const norm = s => s.toLowerCase().replace(/\s+/g, " ").trim();
    const target = norm(rawName);
    return wards.find(w => norm(w.name) === target) || wards.find(w => norm(w.name).includes(target) || target.includes(norm(w.name))) || null;
  }

  // ── MST lookup ──────────────────────────────────────────────────
  const taxLookupStatus = ref(null);
  const taxLookupResult = ref(null);

  // ── AVA banner ──────────────────────────────────────────────────
  const avaVisible = ref(true);
  const avaInput = ref("");

  async function lookupTaxpayer(taxCode) {
    const code = (taxCode || "").trim();
    if (!/^\d{10}(-\d{3})?$/.test(code)) return;
    taxLookupStatus.value = "loading";
    taxLookupResult.value = null;
    try {
      // Ensure provinces are loaded before matching (provinces API may still be in-flight)
      if (!vnProvinces.value.length) {
        vnProvinces.value = await fetchVnProvinces();
      }
      const result = await call("lookup_taxpayer", { tax_code: code });
      if (result) {
        taxLookupResult.value = result;
        if (result.existing_customer) {
          taxLookupStatus.value = "duplicate";
          return;
        }
        const isActive = (result.status || "").includes("đang hoạt động");
        taxLookupStatus.value = isActive ? "found" : "found-inactive";
        if (!createCustomerForm.value.customer_name) {
          createCustomerForm.value.customer_name = result.name || "";
        }
        if (result.address) {
          const parsed = _parseVnAddress(result.address);
          const street = parsed.street || result.address;
          // Fill billing address
          createBillingForm.value.address_line1 = street;
          createBillingForm.value.country = "Vietnam";
          // Fill shipping address with same data
          createShippingForm.value.address_line1 = street;
          createShippingForm.value.country = "Vietnam";
          if (parsed.province) {
            const matchedProvince = _matchProvince(parsed.province);
            if (matchedProvince) {
              // Matched 2025 province → cascade dropdown for both billing and shipping
              _pendingBillingWard.value = parsed.ward || "";
              _pendingShippingWard.value = parsed.ward || "";
              billingProvinceCode.value = String(matchedProvince.code);
              shippingProvinceCode.value = String(matchedProvince.code);
            } else {
              // Province not in 2025 list → save as text in both forms
              createBillingForm.value.state = parsed.province;
              createShippingForm.value.state = parsed.province;
              if (parsed.ward) {
                createBillingForm.value.county = parsed.ward;
                createShippingForm.value.county = parsed.ward;
              }
            }
          }
        }
      } else {
        taxLookupStatus.value = "not-found";
      }
    } catch {
      taxLookupStatus.value = "error";
    }
  }

  function dismissAva() { avaVisible.value = false; }

  async function sendAvaInput() {
    const code = (avaInput.value || "").trim();
    if (!code) return;
    createCustomerForm.value.tax_id = code;
    avaInput.value = "";
    await lookupTaxpayer(code);
  }

  let _taxTimer = null;
  watch(() => createCustomerForm.value.tax_id, (val) => {
    clearTimeout(_taxTimer);
    const code = (val || "").trim();
    if (/^\d{10}(-\d{3})?$/.test(code)) {
      _taxTimer = setTimeout(() => lookupTaxpayer(code), 600);
    } else {
      taxLookupStatus.value = null;
      taxLookupResult.value = null;
    }
  });

  // Sync la_kh_ca_nhan → customer_type
  watch(() => createCustomerForm.value.la_kh_ca_nhan, (val) => {
    createCustomerForm.value.customer_type = val ? "Individual" : "Company";
  });

  // Cascade: billing province → wards (+ auto-match pending ward from MST lookup)
  watch(billingProvinceCode, async (code) => {
    createBillingForm.value.state = "";
    createBillingForm.value.county = "";
    vnBillingWards.value = [];
    if (!code) return;
    const p = vnProvinces.value.find(x => String(x.code) === String(code));
    if (p) createBillingForm.value.state = p.name;
    vnLoadingBillingWards.value = true;
    vnBillingWards.value = await fetchVnWards(code);
    vnLoadingBillingWards.value = false;
    if (_pendingBillingWard.value) {
      const matched = _matchWard(vnBillingWards.value, _pendingBillingWard.value);
      if (matched) createBillingForm.value.county = matched.name;
      _pendingBillingWard.value = "";
    }
  });

  // Cascade: shipping province → wards (+ auto-match pending ward from MST lookup)
  watch(shippingProvinceCode, async (code) => {
    createShippingForm.value.state = "";
    createShippingForm.value.county = "";
    vnShippingWards.value = [];
    if (!code) return;
    const p = vnProvinces.value.find(x => String(x.code) === String(code));
    if (p) createShippingForm.value.state = p.name;
    vnLoadingShippingWards.value = true;
    vnShippingWards.value = await fetchVnWards(code);
    vnLoadingShippingWards.value = false;
    if (_pendingShippingWard.value) {
      const matched = _matchWard(vnShippingWards.value, _pendingShippingWard.value);
      if (matched) createShippingForm.value.county = matched.name;
      _pendingShippingWard.value = "";
    }
  });

  function _resetForms() {
    createCustomerForm.value = {
      customer_name: "", ten_viet_tat: "", misa_mobile: "", misa_email: "",
      tax_id: "", nguon_goc: "", customer_group: "", industry: "",
      loai_hinh: "", nganh_nghe: "", customer_type: "Company",
      tai_khoan_ngan_hang: "", mo_tai_ngan_hang: "", ngay_thanh_lap: "",
      la_kh_tu: "", quy_mo_doanh_thu: "", quy_mo_nhan_su: "",
      loai_han_muc_no: "Không giới hạn", so_ngay_duoc_no: 0, website: "",
      customer_details: "", dung_chung: 0, la_kh_ca_nhan: 0,
      la_doi_tac_ctv: 0, doi_tac_gioi_thieu: "", territory: "",
    };
    createContactForm.value = { first_name: "", mobile_no: "", email_id: "" };
    createBillingForm.value = { address_line1: "", county: "", city: "", state: "", country: "Vietnam", pincode: "" };
    createShippingForm.value = { address_line1: "", county: "", city: "", state: "", country: "Vietnam", pincode: "" };
    createSameAddress.value = false;
    billingProvinceCode.value = "";
    shippingProvinceCode.value = "";
    vnBillingWards.value = [];
    vnShippingWards.value = [];
    _pendingBillingWard.value = "";
    _pendingShippingWard.value = "";
    taxLookupStatus.value = null;
    taxLookupResult.value = null;
    avaVisible.value = true;
    avaInput.value = "";
  }

  async function _loadCreateOptions() {
    if (createOptionsLoaded.value && createOptions.value.countries.length) return;
    try {
      const opts = await call("get_customer_create_options");
      if (opts) {
        createOptions.value = opts;
        if (opts.countries && opts.countries.length) createOptionsLoaded.value = true;
      }
    } catch {}
    if (!vnProvinces.value.length) {
      vnProvinces.value = await fetchVnProvinces();
    }
  }

  // Load eagerly so options are ready on direct URL navigation
  _loadCreateOptions();

  async function openCreateCustomer() {
    _resetForms();
    createOpen.value = true;
    ctx.navigate("create-customer");
    await _loadCreateOptions();
  }

  function cancelCreateCustomer() {
    createOpen.value = false;
    ctx.navigate("customers");
  }

  async function saveCreateCustomer(andNew = false) {
    if (taxLookupStatus.value === "duplicate" && taxLookupResult.value?.existing_customer) {
      const ec = taxLookupResult.value.existing_customer;
      frappe.msgprint({
        title: "Khách hàng đã tồn tại",
        message: `MST này đã có trong hệ thống: <b>${ec.customer_name}</b> (${ec.name}). Vui lòng tìm và cập nhật khách hàng đó thay vì tạo mới.`,
        indicator: "red",
      });
      return;
    }
    if (taxLookupStatus.value === "found-inactive" && taxLookupResult.value) {
      const status = taxLookupResult.value.status || "Ngừng hoạt động";
      const confirmed = await new Promise((resolve) => {
        frappe.confirm(
          `<b>Cảnh báo:</b> MST này có trạng thái:<br>"${status}".<br><br>Bạn có chắc muốn tạo khách hàng với MST đã ngừng hoạt động?`,
          () => resolve(true),
          () => resolve(false),
        );
      });
      if (!confirmed) return;
    }
    if (!(createCustomerForm.value.customer_name || "").trim()) {
      frappe.msgprint({ title: "Lỗi", message: "Tên khách hàng là bắt buộc.", indicator: "red" });
      return;
    }
    createSaving.value = true;
    try {
      // Sync misa_mobile → contact if no contact mobile set
      if (createCustomerForm.value.misa_mobile && !createContactForm.value.mobile_no) {
        createContactForm.value.mobile_no = createCustomerForm.value.misa_mobile;
      }
      if (createCustomerForm.value.misa_email && !createContactForm.value.email_id) {
        createContactForm.value.email_id = createCustomerForm.value.misa_email;
      }

      const shippingPayload = createSameAddress.value
        ? { ...createBillingForm.value }
        : { ...createShippingForm.value };

      const result = await call(
        "create_customer",
        {
          customer: { ...createCustomerForm.value },
          contact: { ...createContactForm.value },
          billing_address: { ...createBillingForm.value },
          shipping_address: shippingPayload,
        },
        "POST",
      );

      frappe.show_alert({ message: "Đã tạo khách hàng thành công", indicator: "green" });

      if (andNew) {
        _resetForms();
      } else {
        createOpen.value = false;
        frappe.route_options = { view: "customer-detail", customer: result.name };
        frappe.set_route("dcnet-crm");
      }
    } catch (err) {
      frappe.msgprint({ title: "Lỗi", message: err.message || "Không thể tạo khách hàng.", indicator: "red" });
    } finally {
      createSaving.value = false;
    }
  }

  function copySameAddress() {
    createSameAddress.value = !createSameAddress.value;
    if (createSameAddress.value) {
      createShippingForm.value = { ...createBillingForm.value };
      shippingProvinceCode.value = billingProvinceCode.value;
      vnShippingWards.value = [...vnBillingWards.value];
    }
  }

  return {
    createOpen,
    createSaving,
    createOptions,
    createCustomerForm,
    createContactForm,
    createBillingForm,
    createShippingForm,
    createSameAddress,
    taxLookupStatus,
    taxLookupResult,
    avaVisible,
    avaInput,
    // VN address
    vnProvinces,
    vnBillingWards,
    vnShippingWards,
    vnLoadingBillingWards,
    vnLoadingShippingWards,
    billingProvinceCode,
    shippingProvinceCode,
    openCreateCustomer,
    cancelCreateCustomer,
    saveCreateCustomer,
    copySameAddress,
    lookupTaxpayer,
    sendAvaInput,
    dismissAva,
  };
}
