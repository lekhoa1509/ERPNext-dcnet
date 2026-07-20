frappe.ui.form.on("Asset Handover", {
    refresh(frm) {
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__("Xem biên bản"), () => {
                const url = `/printview?doctype=${encodeURIComponent(frm.doctype)}`
                    + `&name=${encodeURIComponent(frm.docname)}`
                    + `&format=${encodeURIComponent("Asset Handover S22-DN")}`
                    + `&no_letterhead=0`;
                window.open(url, "_blank");
            });
            frm.add_custom_button(__("In biên bản"), () => {
                frappe.utils.print(frm.doctype, frm.docname, "Asset Handover S22-DN");
            }, __("Hành động"));
        }
        frm.trigger("_set_item_doctype");
        frm.trigger("_apply_threshold_highlight");
    },
    scope(frm) {
        frm.trigger("_set_item_doctype");
    },
    total_asset_value(frm) {
        frm.trigger("_apply_threshold_highlight");
    },
    _set_item_doctype(frm) {
        const dt_map = {"TSCĐ": "Asset", "CCDC": "CCDC Item"};
        const allowed_dt = dt_map[frm.doc.scope] || null;
        if (!allowed_dt) return;
        (frm.doc.handover_items || []).forEach((row) => {
            if (!row.target_doctype) {
                frappe.model.set_value(row.doctype, row.name, "target_doctype", allowed_dt);
            }
        });
        frm.fields_dict.handover_items.grid.update_docfield_property(
            "target_name", "options", allowed_dt
        );
    },
    _apply_threshold_highlight(frm) {
        const co_signer_field = frm.fields_dict.co_signer_employee;
        if (!co_signer_field || !co_signer_field.$wrapper) return;
        const $input = co_signer_field.$wrapper.find(".control-input");
        $input.css("background-color", "");
        co_signer_field.set_description("");
        if (!frm.doc.total_asset_value) return;
        frappe.db.get_single_value("VN Accounting Settings", "handover_threshold")
            .then((threshold) => {
                threshold = parseFloat(threshold) || 0;
                if (!threshold) return;
                const total = parseFloat(frm.doc.total_asset_value) || 0;
                const ratio = total / threshold;
                if (ratio >= 0.8 && ratio < 1.0) {
                    $input.css("background-color", "#fff8dc");
                    co_signer_field.set_description(
                        __("Sắp đạt ngưỡng yêu cầu KTT đồng ký")
                    );
                } else if (ratio >= 1.0) {
                    $input.css("background-color", "#fff8dc");
                    co_signer_field.set_description(
                        __("Vượt ngưỡng — bắt buộc có KTT đồng ký")
                    );
                }
            });
    }
});

frappe.ui.form.on("Asset Handover Item", {
    handover_items_add(frm, cdt, cdn) {
        const dt_map = {"TSCĐ": "Asset", "CCDC": "CCDC Item"};
        const allowed_dt = dt_map[frm.doc.scope];
        if (allowed_dt) {
            frappe.model.set_value(cdt, cdn, "target_doctype", allowed_dt);
        }
    }
});
