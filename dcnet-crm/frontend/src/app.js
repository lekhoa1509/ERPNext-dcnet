import { computed, onMounted, ref, watch } from "vue/dist/vue.esm-bundler.js";
import { RESOURCES, CUSTOMER_COLUMNS, CONTACT_COLUMNS, OPPORTUNITY_COLUMNS, QUOTATION_COLUMNS, ICONS } from "./constants.js";
import { call, formatValue, stripHtml, CRMIcon } from "./utils.js";
import { useDashboard } from "./features/dashboard/composable.js";
import { useLeads } from "./features/leads/composable.js";
import { useOpportunities } from "./features/opportunities/composable.js";
import { useCustomers } from "./features/customers/composable.js";
import { useCreateCustomer } from "./features/customers/composable-create.js";
import { useContacts } from "./features/contacts/composable.js";
import { useCreateContact } from "./features/contacts/composable-create.js";
import { useOrders } from "./features/orders/composable.js";
import { useAccounts } from "./features/accounts/composable.js";
import { useQuotations } from "./features/quotations/composable.js";
import { useActivities } from "./features/activities/composable.js";
import { useCareCards } from "./features/care-cards/composable.js";
import { useAuditLog } from "./features/audit/composable.js";
import dashboardTemplate from "./features/dashboard/template.js";
import leadsTemplate from "./features/leads/template.js";
import opportunitiesTemplate from "./features/opportunities/template.js";
import customersTemplate from "./features/customers/template.js";
import createCustomerTemplate from "./features/customers/template-create.js";
import ordersTemplate from "./features/orders/template.js";
import accountsTemplate from "./features/accounts/template.js";
import quotationsTemplate from "./features/quotations/template.js";
import createContactTemplate from "./features/contacts/template-create.js";
import contactDetailTemplate from "./features/contacts/template-detail.js";
import activitiesTemplate from "./features/activities/template.js";
import careCardsTemplate from "./features/care-cards/template.js";
import auditTemplate from "./features/audit/template.js";

export const CRMApp = {
  components: { CRMIcon },
  setup() {
    // === Shared state ===
    const boot = ref(null);
    const route = ref("dashboard");
    const rows = ref([]);
    const total = ref(0);
    const search = ref("");
    const loading = ref(false);
    const selected = ref(null);
    const detail = ref(null);
    const note = ref("");
    const page = ref(1);
    const pageLength = ref(20);
    const showUnreadyFeatures = computed(() => Boolean(boot.value?.show_unready_features));

    // === Row selection ===
    const selectedNames = ref(new Set());
    const allSelected = computed(() => rows.value.length > 0 && rows.value.every(r => selectedNames.value.has(r.name)));
    const someSelected = computed(() => !allSelected.value && rows.value.some(r => selectedNames.value.has(r.name)));
    function toggleSelectAll() {
      selectedNames.value = allSelected.value ? new Set() : new Set(rows.value.map(r => r.name));
    }
    function toggleSelectRow(name) {
      const s = new Set(selectedNames.value);
      if (s.has(name)) s.delete(name); else s.add(name);
      selectedNames.value = s;
    }
    async function deleteSelectedRows(doctype) {
      const names = [...selectedNames.value];
      if (!names.length) return;
      const label = doctype === "Contact" ? "liên hệ" : doctype === "Customer" ? "khách hàng" : "cơ hội";
      frappe.confirm(
        `Bạn có chắc muốn xóa ${names.length} ${label} đã chọn?`,
        async () => {
          try {
            for (const name of names) {
              await frappe.call({ method: "frappe.client.delete", args: { doctype, name } });
            }
            frappe.show_alert({ message: `Đã xóa ${names.length} ${label}`, indicator: "green" });
            selectedNames.value = new Set();
            loadRowsRef.fn?.();
          } catch (err) {
            frappe.msgprint({ title: "Lỗi", message: err.message || "Không thể xóa.", indicator: "red" });
          }
        }
      );
    }

    // === Shared computed ===
    const config = computed(() => RESOURCES[route.value]);
    const visibleColumns = computed(() => {
      if (!config.value) return [];
      const available = new Set(boot.value?.resources?.[route.value]?.fields || []);
      return config.value.columns.filter(([field]) => available.has(field));
    });
    const pageCount = computed(() => Math.max(Math.ceil(total.value / pageLength.value), 1));
    const pageStart = computed(() => total.value ? (page.value - 1) * pageLength.value + 1 : 0);
    const pageEnd = computed(() => Math.min(page.value * pageLength.value, total.value));

    // === Deferred loadRows to avoid circular deps ===
    const loadRowsRef = { fn: null };
    const auditState = useAuditLog();

    // === ctx object passed to composables ===
    // Note: customerName is set below after custState is created
    // We use a proxy-style object for the refs that come from composables
    const ctx = {
      get route() { return route; },
      get loading() { return loading; },
      get boot() { return boot; },
      get detail() { return detail; },
      get selected() { return selected; },
      get selectedNames() { return selectedNames; },
      get rows() { return rows; },
      get note() { return note; },
      get page() { return page; },
      get search() { return search; },
      get config() { return config; },
      navigate: (key) => navigate(key),
      openRelated: (doctype, record) => openRelated(doctype, record),
      openActivityRecord: (name, doctype, customer, customerLabel) => openActivityRecord(name, doctype, customer, customerLabel),
      openAuditLog: (doctype, name) => auditState.openAuditLog(doctype, name),
      createSalesOrder: (customer, customerName, opportunity, quotation) =>
        ordersState.openCreateSO(customer, customerName, opportunity, quotation),
      createCareCardForOrder: (salesOrder) => careState.createCareCardForOrder(salesOrder),
      openCareCardFromOrder: (name) => careState.openCareCardFromOrder(name),
      openOpportunityForm: (customer, customerName, contactPerson) =>
        oppsState.openOpportunityForm(customer, customerName, contactPerson),
      loadRows: () => loadRowsRef.fn?.(),
      loadCustomerDetail: (name) => custState.loadCustomerDetail(name),
      get customerName() { return custState ? custState.customerName : { value: "" }; },
    };

    // === Feature composables ===
    const dashState = useDashboard(ctx);
    const leadsState = useLeads(ctx);
    const oppsState = useOpportunities(ctx);
    const custState = useCustomers(ctx);
    const createCustState = useCreateCustomer(ctx);
    const contState = useContacts(ctx);
    const createContState = useCreateContact(ctx);
    const ordersState = useOrders(ctx);
    const accountsState = useAccounts(ctx);
    const quotationsState = useQuotations(ctx);
    const activitiesState = useActivities(ctx);
    const careState = useCareCards(ctx);

    // === Computed that depend on composable state ===
    const availableCustomerColumns = computed(() => {
      const available = new Set(boot.value?.resources?.customers?.fields || []);
      return CUSTOMER_COLUMNS.filter((item) => available.has(item.field));
    });
    const shownCustomerColumns = computed(() => availableCustomerColumns.value.filter((item) => custState.customerVisibleFields.value.includes(item.field)));
    const filteredCustomerColumns = computed(() => {
      const keyword = custState.customerColumnSearch.value.trim().toLocaleLowerCase("vi");
      if (!keyword) return availableCustomerColumns.value;
      return availableCustomerColumns.value.filter((item) => item.label.toLocaleLowerCase("vi").includes(keyword));
    });
    const selectedCustomerColumns = computed(() => custState.customerColumnDraft.value
      .map((field) => availableCustomerColumns.value.find((item) => item.field === field))
      .filter(Boolean));
    const availableContactColumns = computed(() => {
      const available = new Set(boot.value?.resources?.contacts?.fields || []);
      return CONTACT_COLUMNS.filter((item) => available.has(item.field));
    });
    const shownContactColumns = computed(() => contState.contactVisibleFields.value
      .map((field) => availableContactColumns.value.find((item) => item.field === field))
      .filter(Boolean));
    const contactViewAvailableColumns = computed(() => {
      const keyword = contState.contactViewSearch.value.trim().toLocaleLowerCase("vi");
      return availableContactColumns.value.filter((column) =>
        !contState.contactViewDraft.value.fields.includes(column.field)
        && (!keyword || column.label.toLocaleLowerCase("vi").includes(keyword))
      );
    });
    const contactViewSelectedColumns = computed(() => contState.contactViewDraft.value.fields
      .map((field) => availableContactColumns.value.find((column) => column.field === field))
      .filter(Boolean));
    const displayContactRows = computed(() => {
      const source = [...rows.value];
      const field = contState.currentContactView.value?.sort_field;
      const direction = contState.currentContactView.value?.sort_direction === "asc" ? 1 : -1;
      if (!field) return source;
      return source.sort((a, b) => {
        const left = a?.[field];
        const right = b?.[field];
        if (left === right) return 0;
        if (left === null || left === undefined || left === "") return 1;
        if (right === null || right === undefined || right === "") return -1;
        return String(left).localeCompare(String(right), "vi", { numeric: true }) * direction;
      });
    });
    const availableOpportunityColumns = computed(() => {
      const available = new Set(boot.value?.resources?.opportunities?.fields || []);
      return OPPORTUNITY_COLUMNS.filter((item) => available.has(item.field));
    });
    const shownOpportunityColumns = computed(() => availableOpportunityColumns.value.filter((item) => oppsState.opportunityVisibleFields.value.includes(item.field)));
    const availableQuotationColumns = computed(() => {
      const available = new Set(boot.value?.resources?.quotations?.fields || []);
      return QUOTATION_COLUMNS.filter((item) => available.has(item.field));
    });
    const shownQuotationColumns = computed(() => availableQuotationColumns.value.filter((item) => quotationsState.quotationVisibleFields.value.includes(item.field)));
    const filteredQuotationColumns = computed(() => {
      const keyword = quotationsState.quotationColumnSearch.value.trim().toLocaleLowerCase("vi");
      if (!keyword) return availableQuotationColumns.value;
      return availableQuotationColumns.value.filter((item) => item.label.toLocaleLowerCase("vi").includes(keyword));
    });
    const selectedQuotationColumns = computed(() => quotationsState.quotationColumnDraft.value
      .map((field) => availableQuotationColumns.value.find((item) => item.field === field))
      .filter(Boolean));
    const opportunityFilterDefinitions = computed(() => availableOpportunityColumns.value.filter((item) => [
      "title", "contact_display", "opportunity_amount", "sales_stage", "expected_closing",
      "opportunity_type", "opportunity_owner", "creation", "customer_name", "status",
    ].includes(item.field)));
    const customerFilterDefinitions = computed(() => availableCustomerColumns.value.filter((item) => [
      "name", "customer_type", "customer_name", "tax_id", "mobile_no", "email_id",
      "customer_group", "territory", "account_manager", "creation",
    ].includes(item.field)));
    const contactFilterDefinitions = computed(() => availableContactColumns.value.filter((item) => [
      "name", "salutation", "full_name", "designation", "mobile_no", "phone",
      "email_id", "company_name", "department", "status",
    ].includes(item.field)));
    const filteredOpportunityColumns = computed(() => {
      const keyword = oppsState.opportunityColumnSearch.value.trim().toLocaleLowerCase("vi");
      if (!keyword) return availableOpportunityColumns.value;
      return availableOpportunityColumns.value.filter((item) => item.label.toLocaleLowerCase("vi").includes(keyword));
    });
    const selectedOpportunityColumns = computed(() => oppsState.opportunityColumnDraft.value
      .map((field) => availableOpportunityColumns.value.find((item) => item.field === field))
      .filter(Boolean));

    // === Shared functions ===
    function parseRouteView(value) {
      if (!value) return "";
      try {
        const parsed = JSON.parse(value);
        return typeof parsed === "string" ? parsed : value;
      } catch {
        return value;
      }
    }

    function syncRouteUrl(view, name) {
      if (name === undefined) name = "";
      if (!view || !window.location.pathname.endsWith("/dcnet-crm")) return;
      window.sessionStorage.setItem("dcnet-crm-view", view);
      const url = new URL(window.location.href);
      url.hash = "";
      url.searchParams.set("view", view);
      if (view === "opportunity-detail") {
        if (name) url.searchParams.set("opportunity", name);
        else url.searchParams.delete("opportunity");
        url.searchParams.delete("customer");
      } else if (view === "lead-detail") {
        if (name) url.searchParams.set("lead", name);
        else url.searchParams.delete("lead");
        url.searchParams.delete("customer");
        url.searchParams.delete("opportunity");
      } else if (view === "customer-detail") {
        if (name) url.searchParams.set("customer", name);
        else url.searchParams.delete("customer");
        url.searchParams.delete("opportunity");
      } else if (view === "create-sales-order") {
        if (name) url.searchParams.set("customer", name);
        else url.searchParams.delete("customer");
        url.searchParams.delete("opportunity");
      } else if (view === "create-quotation") {
        if (name) url.searchParams.set("customer", name);
        else url.searchParams.delete("customer");
        url.searchParams.delete("opportunity");
      } else if (view === "contact-detail") {
        if (name) url.searchParams.set("contact", name);
        else url.searchParams.delete("contact");
        url.searchParams.delete("customer");
        url.searchParams.delete("opportunity");
      } else if (view === "order-detail") {
        if (name) url.searchParams.set("order", name);
        else url.searchParams.delete("order");
        url.searchParams.delete("customer");
        url.searchParams.delete("opportunity");
      } else if (view === "quotation-detail") {
        if (name) url.searchParams.set("quotation", name);
        else url.searchParams.delete("quotation");
        url.searchParams.delete("customer");
        url.searchParams.delete("opportunity");
        url.searchParams.delete("order");
      } else {
        url.searchParams.delete("customer");
        url.searchParams.delete("opportunity");
        url.searchParams.delete("order");
        url.searchParams.delete("quotation");
      }
      window.history.replaceState(window.history.state, "", url);
    }

    function syncNativeSidebarActive(view) {
      const labels = {
        dashboard: "Bàn làm việc",
        leads: "Tiềm năng",
        "lead-detail": "Tiềm năng",
        contacts: "Liên hệ",
        customers: "Khách hàng",
        "customer-detail": "Khách hàng",
        "opportunity-detail": "Cơ hội",
        opportunities: "Cơ hội",
        "create-customer": "Khách hàng",
        "create-contact": "Liên hệ",
        "contact-detail": "Liên hệ",
        "create-sales-order": "Đơn hàng",
        "create-quotation": "Báo giá",
        "quotation-detail": "Báo giá",
        "order-detail": "Đơn hàng",
        quotations: "Báo giá",
        orders: "Đơn hàng",
        accounts: "Tài khoản",
        activities: "Hoạt động",
        care: "Thẻ chăm sóc",
      };
      // Runs on the next paint frame instead of a fixed setTimeout delay —
      // still lets Frappe's own native sidebar DOM/click handling settle
      // first, but without the visible "wrong item flashes active" glitch a
      // longer artificial delay (e.g. 50ms) causes.
      requestAnimationFrame(() => {
        document.querySelectorAll(".body-sidebar .sidebar-item-container").forEach((item) => {
          const name = String(item.getAttribute("item-name") || "").trim().toLowerCase();
          if (["notification", "notifications", "thông báo"].includes(name)) item.hidden = true;
        });
        document.querySelectorAll(".body-sidebar .standard-sidebar-item").forEach((item) => {
          item.classList.remove("active-sidebar");
        });
        const container = [...document.querySelectorAll(".body-sidebar .sidebar-item-container")]
          .find((item) => item.getAttribute("item-name") === labels[view]);
        container?.querySelector(".standard-sidebar-item")?.classList.add("active-sidebar");
      });
    }

    function readRoute() {
      const params = new URLSearchParams(window.location.search);
      const optionView = parseRouteView(params.get("view") || frappe.route_options?.view);
      const legacyView = window.location.hash.replace(/^#\/?/, "").split("/")[0];
      const savedView = window.sessionStorage.getItem("dcnet-crm-view");
      const key = optionView || legacyView || savedView || "dashboard";

      if (oppsState.opportunityFormOpen.value && key !== "opportunities") {
        if (oppsState.opportunityFormDirty.value) {
          syncRouteUrl("opportunities");
          oppsState.pendingNavigationView.value = key;
          oppsState.leaveFormConfirmOpen.value = true;
          return;
        }
        oppsState.closeOpportunityForm();
      }

      route.value = RESOURCES[key] || ["dashboard", "customer-detail", "opportunity-detail", "create-sales-order", "create-quotation", "create-customer", "create-contact", "contact-detail", "lead-detail", "order-detail", "quotation-detail", "accounts", "activities", "care"].includes(key) ? key : "dashboard";
      custState.customerName.value = params.get("customer") || frappe.route_options?.customer || "";
      oppsState.opportunityDetailName.value = params.get("opportunity") || frappe.route_options?.opportunity || "";
      leadsState.leadDetailName.value = params.get("lead") || frappe.route_options?.lead || "";
      ordersState.orderDetailName.value = params.get("order") || frappe.route_options?.order || "";
      quotationsState.quotationDetailName.value = params.get("quotation") || frappe.route_options?.quotation || "";
      if (route.value === "contact-detail") { const cn = params.get("contact") || frappe.route_options?.contact || ""; if (cn) createContState.contactDetailName.value = cn; else route.value = "contacts"; }
      if (route.value === "customer-detail" && !custState.customerName.value) route.value = "customers";
      if (route.value === "opportunity-detail" && !oppsState.opportunityDetailName.value) route.value = "opportunities";
      if (route.value === "lead-detail" && !leadsState.leadDetailName.value) route.value = "leads";
      if (route.value === "order-detail" && !ordersState.orderDetailName.value) route.value = "orders";
      if (route.value === "quotation-detail" && !quotationsState.quotationDetailName.value) route.value = "quotations";
      // Sidebar navigation to Activities always lands back on the list (openActivityRecord
      // sets the selection afterwards via syncRouteUrl, which does not re-trigger readRoute).
      if (route.value === "activities") activitiesState.clearActivitySelection();
      // Re-initialise create forms on direct navigation / reload so their dropdowns load
      if (route.value === "create-sales-order" && !Object.keys(ordersState.createSOForm.value || {}).length) {
        const c = params.get("customer") || "";
        ordersState.openCreateSO(c, c);
      }
      if (route.value === "create-quotation" && !Object.keys(quotationsState.createQTForm.value || {}).length) {
        const c = params.get("customer") || "";
        quotationsState.openCreateQuotation(c, c);
      }
      const detailName =
        route.value === "contact-detail" ? createContState.contactDetailName.value :
        route.value === "opportunity-detail" ? oppsState.opportunityDetailName.value :
        route.value === "lead-detail" ? leadsState.leadDetailName.value :
        route.value === "order-detail" ? ordersState.orderDetailName.value :
        route.value === "quotation-detail" ? quotationsState.quotationDetailName.value :
        custState.customerName.value;
      window.setTimeout(() => syncRouteUrl(route.value, detailName), 0);
      syncNativeSidebarActive(route.value);
    }

    function navigate(key) {
      route.value = key;
      custState.customerName.value = "";
      frappe.route_options = { view: key };
      frappe.set_route("dcnet-crm").then(() => syncRouteUrl(key));
    }

    async function loadRows() {
      if (!config.value) return;
      loading.value = true;
      selected.value = null;
      detail.value = null;
      try {
        const filters = {};
        if (route.value === "leads") {
          Object.assign(filters, leadsState.buildLeadFilters());
        } else if (route.value === "customers") {
          if (custState.customerListView.value === "mine") {
            filters.account_manager = boot.value?.user;
          }
          custState.customerEnabledFilters.value.forEach((field) => {
            const value = custState.customerFilterValues.value[field];
            if (value === undefined || value === null || value === "") return;
            filters[field] = ["customer_type", "customer_group", "territory", "account_manager"].includes(field)
              ? value
              : ["like", `%${value}%`];
          });
        } else if (route.value === "contacts") {
          Object.assign(filters, contState.buildContactFilters());
        } else if (route.value === "opportunities") {
          oppsState.opportunityEnabledFilters.value.forEach((field) => {
            const value = oppsState.opportunityFilterValues.value[field];
            if (value === undefined || value === null || value === "") return;
            if (field === "creation") {
              filters[field] = ["between", [`${value} 00:00:00`, `${value} 23:59:59`]];
            } else {
              filters[field] = ["title", "contact_display", "customer_name"].includes(field)
                ? ["like", `%${value}%`]
                : value;
            }
          });
        } else if (route.value === "orders") {
          const savedDates = ordersState.soSavedFilterDates.value;
          Object.assign(filters, savedDates);
          ordersState.ordersEnabledFilters.value.forEach((field) => {
            const value = ordersState.ordersFilterValues.value[field];
            if (value === undefined || value === null || value === "") return;
            if (["custom_revenue_status", "delivery_status"].includes(field)) {
              filters[field] = value;
            } else if (["transaction_date", "custom_revenue_recognition_date"].includes(field)) {
              filters[field] = ["between", [`${value} 00:00:00`, `${value} 23:59:59`]];
            } else {
              filters[field] = ["like", `%${value}%`];
            }
          });
        } else if (route.value === "quotations") {
          Object.assign(filters, quotationsState.qtSavedFilterDates.value);
          quotationsState.quotationsEnabledFilters.value.forEach((field) => {
            const value = quotationsState.quotationsFilterValues.value[field];
            if (value === undefined || value === null || value === "") return;
            if (field === "status") {
              filters[field] = value;
            } else if (["transaction_date", "valid_till"].includes(field)) {
              filters[field] = value;
            } else {
              filters[field] = ["like", `%${value}%`];
            }
          });
        }
        const result = await call("get_list", {
          resource: route.value,
          search: search.value,
          filters,
          page: page.value,
          page_length: pageLength.value,
          sort_field: route.value === "contacts"
            ? contState.currentContactView.value?.sort_field
            : route.value === "quotations" ? quotationsState.qtSortField.value : "",
          sort_direction: route.value === "contacts"
            ? contState.currentContactView.value?.sort_direction
            : route.value === "quotations" ? quotationsState.qtSortDirection.value : "",
        });
        rows.value = result.data;
        total.value = result.total;
        selectedNames.value = new Set();
      } catch (error) {
        frappe.msgprint(error.message || __("Không thể tải dữ liệu CRM."));
      } finally {
        loading.value = false;
      }
    }

    async function selectRow(row) {
      selected.value = row;
      detail.value = null;
      try {
        detail.value = route.value === "customers"
          ? await call("get_customer_workspace", { name: row.name })
          : route.value === "contacts"
            ? await call("get_contact_detail", { name: row.name })
            : route.value === "opportunities"
              ? await call("get_opportunity_detail", { name: row.name })
            : await call("get_document", { resource: route.value, name: row.name });
      } catch (error) {
        frappe.msgprint(error.message || __("Không thể tải chi tiết."));
      }
    }

    async function addNote() {
      if (!note.value.trim()) return;
      if (route.value === "lead-detail" && leadsState.leadDetailName.value) {
        await call("add_note", { resource: "leads", name: leadsState.leadDetailName.value, content: note.value }, "POST");
        note.value = "";
        await leadsState.loadLeadDetail();
        return;
      }
      if (!selected.value) return;
      const resource = route.value === "customer-detail" ? "customers" : route.value;
      await call("add_note", { resource, name: selected.value.name, content: note.value }, "POST");
      note.value = "";
      if (route.value === "customer-detail") await custState.loadCustomerDetail(selected.value.name);
      else await selectRow(selected.value);
    }

    function openDocument(row) {
      if (row === undefined) row = selected.value;
      if (!row?.name) return;
      if (route.value === "opportunities") { oppsState.openOpportunityDetail(row); return; }
      if (route.value === "leads") { leadsState.openLeadDetail(row); return; }
      if (route.value === "customers") { custState.openCustomerDetail(row); return; }
      if (route.value === "contacts") { createContState.openContactDetail(row); return; }
      if (route.value === "orders") { ordersState.openOrderDetail(row); return; }
      if (route.value === "quotations") { openRelated("Quotation", row); return; }
      frappe.set_route("Form", config.value?.doctype, row.name);
    }

    function createDocument(doctype) {
      if (doctype === undefined) doctype = config.value?.doctype;
      if (doctype === "Lead" || route.value === "leads") { leadsState.openLeadForm(); return; }
      if (doctype === "Opportunity") {
        oppsState.openOpportunityForm();
        return;
      }
      if (doctype === "Sales Order" || route.value === "orders") { ordersState.openCreateSO(); return; }
      if (doctype === "Quotation" || route.value === "quotations") { quotationsState.openCreateQuotation(); return; }
      if (doctype === "Customer" || route.value === "customers") { createCustState.openCreateCustomer(); return; }
      if (doctype === "Contact" || route.value === "contacts") { createContState.openCreateContact(); return; }
      if (doctype) frappe.new_doc(doctype);
    }

    function createCustomerOrder() {
      const custId = custState.customerName.value || selected.value?.name || "";
      const custDisplayName = detail.value?.customer_name || detail.value?.name || selected.value?.customer_name || custId;
      ordersState.openCreateSO(custId, custDisplayName);
    }

    function showRelatedPermissionDenied() {
      frappe.show_alert({
        message: __("Bạn không có quyền thực hiện chức năng này."),
        indicator: "orange",
      }, 5);
    }

    async function openRelated(doctype, row) {
      const record = typeof row === "string" ? { name: row } : row;
      if (!doctype || !record?.name) return;

      if (doctype === "Lead") {
        leadsState.openLeadDetail(record);
        return;
      }
      if (doctype === "Customer") {
        custState.openCustomerDetail(record);
        return;
      }
      if (doctype === "Contact") {
        createContState.openContactDetail(record);
        return;
      }
      if (doctype === "Opportunity") {
        oppsState.openOpportunityDetail(record);
        return;
      }
      if (doctype === "Sales Order") {
        ordersState.openOrderDetail(record);
        return;
      }
      if (doctype === "Quotation") {
        quotationsState.openQuotationDetail(record);
        return;
      }
      if (doctype === "Sales Invoice") {
        try {
          const permission = await call("can_open_accounting_document", {
            doctype,
            name: record.name,
          });
          if (!permission?.allowed) {
            showRelatedPermissionDenied();
            return;
          }
          frappe.set_route("Form", doctype, record.name);
        } catch {
          showRelatedPermissionDenied();
        }
        return;
      }

      frappe.set_route("Form", doctype, record.name);
    }

    // Jump to the CRM Activities page and open a specific ToDo/Event.
    // customer/customerLabel scope the surrounding list to that customer's activities only.
    async function openActivityRecord(name, doctype = "", customer = "", customerLabel = "") {
      if (!name) return;
      route.value = "activities";
      custState.customerName.value = "";
      syncRouteUrl("activities");
      syncNativeSidebarActive("activities");
      if (customer) {
        activitiesState.setActivityCustomerFilter(customer, customerLabel);
      }
      await activitiesState.loadActivityList();
      await activitiesState.selectActivity(name, doctype);
    }

    function changePage(nextPage) {
      const target = Math.min(Math.max(nextPage, 1), pageCount.value);
      if (target === page.value) return;
      page.value = target;
      loadRows();
    }

    // Wire up deferred loadRows
    loadRowsRef.fn = loadRows;

    // === Watchers ===
    let searchTimer;
    watch(search, () => {
      clearTimeout(searchTimer);
      page.value = 1;
      searchTimer = setTimeout(loadRows, 300);
    });
    watch(pageLength, () => {
      page.value = 1;
      loadRows();
    });
    watch(custState.contactPageLength, () => {
      custState.contactPage.value = 1;
    });
    watch(custState.activityPageLength, () => {
      custState.activityPage.value = 1;
    });
    watch(custState.customerFilterValues, () => {
      if (route.value !== "customers") return;
      clearTimeout(searchTimer);
      page.value = 1;
      searchTimer = setTimeout(loadRows, 300);
    }, { deep: true });
    watch(leadsState.leadFilterValues, () => {
      if (route.value !== "leads") return;
      clearTimeout(searchTimer);
      page.value = 1;
      searchTimer = setTimeout(loadRows, 300);
    }, { deep: true });
    watch(contState.contactFilterValues, () => {
      if (route.value !== "contacts") return;
      clearTimeout(searchTimer);
      page.value = 1;
      searchTimer = setTimeout(loadRows, 300);
    }, { deep: true });
    watch(oppsState.opportunityFilterValues, () => {
      if (route.value !== "opportunities") return;
      clearTimeout(searchTimer);
      page.value = 1;
      searchTimer = setTimeout(loadRows, 300);
    }, { deep: true });
    watch(quotationsState.quotationsFilterValues, () => {
      if (route.value !== "quotations") return;
      clearTimeout(searchTimer);
      page.value = 1;
      searchTimer = setTimeout(loadRows, 300);
    }, { deep: true });
    watch(route, async (value) => {
      search.value = "";
      page.value = 1;
      if (!boot.value) return;
      if (value === "dashboard") await dashState.loadDashboard();
      else if (value === "customer-detail") await custState.loadCustomerDetail();
      else if (value === "lead-detail") await leadsState.loadLeadDetail();
      else if (value === "opportunity-detail") await oppsState.loadOpportunityDetail();
      else if (value === "order-detail") await ordersState.loadOrderDetail();
      else if (value === "quotation-detail") await quotationsState.loadQuotationDetailPage();
      else if (value === "contact-detail") await createContState.loadContactDetail();
      else if (value === "accounts") await accountsState.loadAccounts();
      else if (value === "activities") await activitiesState.loadActivityList();
      else if (value === "care") await careState.loadCareCards();
      else await loadRows();
    });

    onMounted(async () => {
      window.addEventListener("popstate", readRoute);
      window.addEventListener("dcnet-crm-route-change", readRoute);
      readRoute();
      boot.value = await call("get_boot");
      try {
        const savedValue = window.localStorage.getItem("dcnet-crm-customer-columns");
        if (savedValue !== null) {
          const savedCustomerColumns = JSON.parse(savedValue);
          const available = new Set(availableCustomerColumns.value.map((item) => item.field));
          custState.customerVisibleFields.value = Array.isArray(savedCustomerColumns)
            ? savedCustomerColumns.filter((field) => available.has(field))
            : custState.customerVisibleFields.value;
        }
      } catch {
        window.localStorage.removeItem("dcnet-crm-customer-columns");
      }
      if (route.value === "dashboard") await dashState.loadDashboard();
      else if (route.value === "customer-detail") await custState.loadCustomerDetail();
      else if (route.value === "lead-detail") await leadsState.loadLeadDetail();
      else if (route.value === "opportunity-detail") await oppsState.loadOpportunityDetail();
      else if (route.value === "order-detail") await ordersState.loadOrderDetail();
      else if (route.value === "quotation-detail") await quotationsState.loadQuotationDetailPage();
      else if (route.value === "contact-detail") await createContState.loadContactDetail();
      else if (route.value === "accounts") await accountsState.loadAccounts();
      else if (route.value === "activities") await activitiesState.loadActivityList();
      else if (route.value === "care") await careState.loadCareCards();
      else await loadRows();
    });

    return {
      // Shared
      boot, route, rows, total, search, loading, selected, detail, note, page, pageLength,
      showUnreadyFeatures,
      config, visibleColumns, pageCount, pageStart, pageEnd,
      RESOURCES, CONTACT_COLUMNS, CUSTOMER_COLUMNS, OPPORTUNITY_COLUMNS,
      formatValue, stripHtml,
      navigate, loadRows, changePage, addNote, selectRow, openDocument, createDocument,
      createCustomerOrder, openRelated, openActivityRecord,
      selectedNames, allSelected, someSelected, toggleSelectAll, toggleSelectRow, deleteSelectedRows,
      // Computed that were moved here
      availableCustomerColumns, shownCustomerColumns, filteredCustomerColumns, selectedCustomerColumns,
      availableContactColumns, shownContactColumns,
      contactViewAvailableColumns, contactViewSelectedColumns, displayContactRows,
      availableOpportunityColumns, shownOpportunityColumns,
      opportunityFilterDefinitions, customerFilterDefinitions, contactFilterDefinitions,
      filteredOpportunityColumns, selectedOpportunityColumns,
      availableQuotationColumns, shownQuotationColumns, filteredQuotationColumns, selectedQuotationColumns,
      // Dashboard
      ...dashState,
      // Leads
      ...leadsState,
      // Opportunities
      ...oppsState,
      // Customers
      ...custState,
      ...createCustState,
      // Contacts
      ...contState,
      ...createContState,
      // Orders
      ...ordersState,
      // Accounts
      ...accountsState,
      // Quotations
      ...quotationsState,
      // Activities
      ...activitiesState,
      ...careState,
      ...auditState,
    };
  },
  template: `<div class="dcnet-crm"><section class="crm-content">`
    + dashboardTemplate
    + customersTemplate
    + createCustomerTemplate
    + opportunitiesTemplate
    + leadsTemplate
    + ordersTemplate
    + accountsTemplate
    + quotationsTemplate
    + createContactTemplate
    + contactDetailTemplate
    + activitiesTemplate
    + careCardsTemplate
    + auditTemplate
    + `</section></div>`,
};
