frappe.listview_settings["EInvoice Provider"] = {
    add_fields: ["enable_inward", "enable_outward", "enabled"],
    formatters: {
        enable_inward(value) {
            return value
                ? `<span class="indicator-pill green">${__("In")}</span>`
                : `<span class="indicator-pill gray">${__("In")}</span>`;
        },
        enable_outward(value) {
            return value
                ? `<span class="indicator-pill blue">${__("Out")}</span>`
                : `<span class="indicator-pill gray">${__("Out")}</span>`;
        },
    },
    get_indicator(doc) {
        if (!doc.enabled) return [__("Tắt"), "gray", "enabled,=,0"];
        if (doc.enable_inward && doc.enable_outward) {
            return [__("In + Out"), "green", "enable_inward,=,1|enable_outward,=,1"];
        }
        if (doc.enable_inward) return [__("In only"), "blue", "enable_inward,=,1|enable_outward,=,0"];
        if (doc.enable_outward) return [__("Out only"), "orange", "enable_outward,=,1|enable_inward,=,0"];
        return [__("Chưa cấu hình"), "red", "enable_inward,=,0|enable_outward,=,0"];
    },
};
