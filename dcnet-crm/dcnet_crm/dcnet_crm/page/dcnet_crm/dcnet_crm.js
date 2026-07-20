frappe.pages["dcnet-crm"].on_page_load = function (wrapper) {
  frappe.ui.make_app_page({
    parent: wrapper,
    title: __("CRM"),
    single_column: true,
  });
};

frappe.pages["dcnet-crm"].on_page_show = function () {
  window.dispatchEvent(new Event("dcnet-crm-route-change"));
};
