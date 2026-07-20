import { computed, nextTick, ref } from "vue/dist/vue.esm-bundler.js";
import { call } from "../../utils.js";

export function useAuditLog() {
  const auditLogOpen = ref(false);
  const auditLogLoading = ref(false);
  const auditLogError = ref("");
  const auditLogData = ref(null);

  const auditLogEntries = computed(() => auditLogData.value?.entries || []);

  async function loadAuditLog(doctype, name) {
    auditLogLoading.value = true;
    auditLogError.value = "";
    try {
      auditLogData.value = await call("get_document_audit_log", { doctype, name, limit: 50 });
    } catch (error) {
      auditLogError.value = error?.message || "Không thể tải nhật ký dữ liệu.";
    } finally {
      auditLogLoading.value = false;
    }
  }

  async function openAuditLog(doctype, name) {
    if (!doctype || !name) return;
    auditLogOpen.value = true;
    auditLogData.value = { doctype, name, entries: [] };
    await nextTick();
    document.querySelector(".crm-audit-dialog")?.focus();
    await loadAuditLog(doctype, name);
  }

  function closeAuditLog() {
    auditLogOpen.value = false;
  }

  function refreshAuditLog() {
    if (auditLogData.value?.doctype && auditLogData.value?.name) {
      loadAuditLog(auditLogData.value.doctype, auditLogData.value.name);
    }
  }

  function formatAuditDate(value) {
    if (!value) return "—";
    const date = new Date(String(value).replace(" ", "T"));
    if (Number.isNaN(date.getTime())) return String(value);
    return new Intl.DateTimeFormat("vi-VN", {
      day: "2-digit", month: "2-digit", year: "numeric", hour: "2-digit", minute: "2-digit",
    }).format(date);
  }

  function formatAuditValue(value) {
    if (value === null || value === undefined || value === "") return "Trống";
    if (value === "0") return "Không";
    if (value === "1") return "Có";
    return String(value);
  }

  return {
    auditLogOpen, auditLogLoading, auditLogError, auditLogData, auditLogEntries,
    openAuditLog, closeAuditLog, refreshAuditLog, formatAuditDate, formatAuditValue,
  };
}
