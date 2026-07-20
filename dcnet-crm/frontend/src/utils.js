import { ICONS } from "./constants.js";

const API = "dcnet_crm.api";

export function call(method, args = {}, type = "GET") {
  return frappe.call({ method: `${API}.${method}`, args, type }).then((response) => response.message);
}

export function exportResource(resource, options = {}) {
  const params = new URLSearchParams({ resource });
  for (const [key, value] of Object.entries(options)) {
    if (value !== undefined && value !== null && value !== "") {
      params.set(key, typeof value === "string" ? value : JSON.stringify(value));
    }
  }
  window.location.assign(`/api/method/${API}.export_resource?${params.toString()}`);
}

export function formatValue(value, field = "") {
  if (value === null || value === undefined || value === "") return "—";
  if (["grand_total", "opportunity_amount", "order_value", "net_total", "total_taxes_and_charges", "discount_amount"].includes(field)) {
    return new Intl.NumberFormat("vi-VN").format(Number(value || 0));
  }
  if (field === "probability") return `${value}%`;
  if (/date|creation|modified/.test(field)) {
    const date = new Date(value);
    if (!Number.isNaN(date.getTime())) {
      const hasTime = typeof value === "string" && /[T ]\d{2}:\d{2}/.test(value);
      return new Intl.DateTimeFormat("vi-VN", hasTime ? {
        day: "2-digit", month: "2-digit", year: "numeric", hour: "2-digit", minute: "2-digit",
      } : undefined).format(date);
    }
  }
  return String(value);
}

export function stripHtml(value) {
  const element = document.createElement("div");
  element.innerHTML = String(value || "");
  return element.textContent || "";
}

export const CRMIcon = {
  props: ["name"],
  computed: { svg() { return ICONS[this.name] || ICONS.all; } },
  template: '<span class="crm-menu-icon" aria-hidden="true" v-html="svg"></span>',
};
