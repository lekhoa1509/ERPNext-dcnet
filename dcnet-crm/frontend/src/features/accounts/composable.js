import { ref, computed } from "vue/dist/vue.esm-bundler.js";
import { call, exportResource } from "../../utils.js";

export function useAccounts(ctx) {
  const accountsLoading = ref(false);
  const accountsList = ref([]);
  const accountsTotal = ref(0);
  const accountsSearch = ref("");
  const accountsPage = ref(1);
  const accountsPageLength = ref(20);

  const accountsPageCount = computed(() =>
    Math.max(Math.ceil(accountsTotal.value / accountsPageLength.value), 1)
  );
  const accountsPageStart = computed(() =>
    accountsTotal.value ? (accountsPage.value - 1) * accountsPageLength.value + 1 : 0
  );
  const accountsPageEnd = computed(() =>
    Math.min(accountsPage.value * accountsPageLength.value, accountsTotal.value)
  );

  async function loadAccounts() {
    accountsLoading.value = true;
    try {
      const result = await call("get_service_accounts_list", {
        search: accountsSearch.value || undefined,
        page: accountsPage.value,
        page_length: accountsPageLength.value,
      });
      accountsList.value = result.data || [];
      accountsTotal.value = result.total || 0;
    } catch (e) {
      frappe.msgprint(e.message || "Không thể tải danh sách tài khoản.");
    } finally {
      accountsLoading.value = false;
    }
  }

  function changeAccountsPage(next) {
    const target = Math.min(Math.max(next, 1), accountsPageCount.value);
    if (target === accountsPage.value) return;
    accountsPage.value = target;
    loadAccounts();
  }

  // ── Detail panel ─────────────────────────────────────────────────────────
  const accountDetailLoading = ref(false);
  const accountDetail = ref(null);
  const accountEditMode = ref(false);
  const accountEditSaving = ref(false);
  const accountEditForm = ref({});

  async function openAccountDetail(row) {
    if (!row || !row.account_code) return;
    // If same account clicked, close
    if (accountDetail.value && accountDetail.value.account_code === row.account_code) {
      closeAccountDetail();
      return;
    }
    accountDetailLoading.value = true;
    accountDetail.value = null;
    try {
      accountDetail.value = await call("get_service_account_detail", {
        account_code: row.account_code,
      });
      accountEditMode.value = false;
    } catch (e) {
      frappe.msgprint(e.message || "Không thể tải thông tin tài khoản.");
    } finally {
      accountDetailLoading.value = false;
    }
  }

  function closeAccountDetail() {
    accountDetail.value = null;
    accountEditMode.value = false;
  }

  function startAccountEdit() {
    if (!accountDetail.value?.can_write) return;
    accountEditForm.value = {
      customer: accountDetail.value.customer || "",
      item_code: accountDetail.value.item_code || "",
      a_end: accountDetail.value.a_end || "",
      z_end: accountDetail.value.z_end || "",
      is_active: accountDetail.value.is_active ? 1 : 0,
    };
    accountEditMode.value = true;
  }

  function cancelAccountEdit() {
    accountEditMode.value = false;
    accountEditForm.value = {};
  }

  async function saveAccountEdit() {
    if (accountEditSaving.value || !accountDetail.value?.account_code) return;
    accountEditSaving.value = true;
    try {
      accountDetail.value = await call("update_service_account", {
        account_code: accountDetail.value.account_code,
        data: accountEditForm.value,
      }, "POST");
      accountEditMode.value = false;
      await loadAccounts();
      frappe.show_alert({ message: "Đã cập nhật tài khoản", indicator: "green" });
    } catch (e) {
      frappe.msgprint(e.message || "Không thể cập nhật tài khoản.");
    } finally {
      accountEditSaving.value = false;
    }
  }

  let _searchTimer = null;
  function onAccountsSearchInput() {
    clearTimeout(_searchTimer);
    accountsPage.value = 1;
    _searchTimer = setTimeout(loadAccounts, 300);
  }

  return {
    accountsLoading, accountsList, accountsTotal,
    accountsSearch, accountsPage, accountsPageLength,
    accountsPageCount, accountsPageStart, accountsPageEnd,
    loadAccounts, changeAccountsPage, onAccountsSearchInput,
    accountDetailLoading, accountDetail, accountEditMode, accountEditSaving, accountEditForm,
    openAccountDetail, closeAccountDetail, startAccountEdit, cancelAccountEdit, saveAccountEdit, exportResource,
  };
}
