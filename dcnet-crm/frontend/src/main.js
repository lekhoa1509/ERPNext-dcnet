import { createApp } from "vue/dist/vue.esm-bundler.js";
import styles from "./styles.css";
import { CRMApp } from "./app.js";
import { SearchSelect } from "./components/SearchSelect.js";
import { OrgUnitNode } from "./components/OrgUnitNode.js";

function mountCRM(wrapper) {
  if (wrapper.dataset.dcnetCrmMounted) {
    window.dispatchEvent(new CustomEvent("dcnet-crm-route-change"));
    return;
  }
  wrapper.dataset.dcnetCrmMounted = "1";
  const root = document.createElement("div");
  root.className = "dcnet-crm-root";
  const mountTarget = wrapper.querySelector(".layout-main-section") || wrapper;
  mountTarget.appendChild(root);
  const style = document.createElement("style");
  style.textContent = styles;
  document.head.appendChild(style);
  createApp(CRMApp)
    .component("SearchSelect", SearchSelect)
    .component("OrgUnitNode", OrgUnitNode)
    .directive("click-outside", {
      beforeMount(el, binding) {
        el._coHandler = (e) => { if (!el.contains(e.target)) binding.value(e); };
        document.addEventListener("click", el._coHandler, true);
      },
      unmounted(el) { document.removeEventListener("click", el._coHandler, true); },
    })
    .mount(root);
}

frappe.pages["dcnet-crm"].on_page_load = function (wrapper) {
  frappe.ui.make_app_page({ parent: wrapper, title: __("CRM"), single_column: true });
  mountCRM(wrapper);
};

frappe.pages["dcnet-crm"].on_page_show = function (wrapper) {
  mountCRM(wrapper);
  window.dispatchEvent(new CustomEvent("dcnet-crm-route-change"));
};
