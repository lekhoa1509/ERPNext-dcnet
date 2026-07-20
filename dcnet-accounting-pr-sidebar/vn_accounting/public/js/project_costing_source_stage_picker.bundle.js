// Source-doc stage picker visibility.
//
// Reads frappe.boot.vn_accounting.auto_show_stage_picker_on_source_docs
// (set by boot_session via _inject_vn_accounting_settings). When OFF,
// hides the `project_costing_stage` custom field on PI/SE/DN/EC so
// KTT only pins via Pivot Tool. When ON (default), the field stays
// visible (its own depends_on:eval:doc.project still gates on project).

(function () {
    function _setting_on() {
        return !!(frappe.boot && frappe.boot.vn_accounting &&
                  frappe.boot.vn_accounting.auto_show_stage_picker_on_source_docs);
    }

    // Parent-level field (Stock Entry, Expense Claim)
    ["Stock Entry", "Expense Claim"].forEach(function (dt) {
        frappe.ui.form.on(dt, {
            refresh: function (frm) {
                if (!frm.fields_dict.project_costing_stage) return;
                if (!_setting_on()) {
                    frm.set_df_property("project_costing_stage", "hidden", 1);
                } else {
                    frm.set_df_property("project_costing_stage", "hidden", 0);
                    frm.set_df_property(
                        "project_costing_stage", "description",
                        __("Gắn giai đoạn ngay → giảm việc gắn lại ở 'Tập hợp chi phí chưa gắn' của công trình.")
                    );
                }
                frm.refresh_field("project_costing_stage");
            },
        });
    });

    // Item-level field — visibility on grid column via Form Item Grid customization.
    // Frappe grids honor df.hidden on each column; we toggle via grid_settings hook.
    ["Purchase Invoice", "Delivery Note"].forEach(function (dt) {
        const item_child_dt = dt + " Item";
        frappe.ui.form.on(dt, {
            refresh: function (frm) {
                const grid = frm.fields_dict.items && frm.fields_dict.items.grid;
                if (!grid) return;
                const stage_df = (grid.docfields || []).find(
                    function (f) { return f.fieldname === "project_costing_stage"; }
                );
                if (!stage_df) return;
                stage_df.hidden = _setting_on() ? 0 : 1;
                if (_setting_on()) {
                    stage_df.description = __(
                        "Gắn ngay theo dòng → giảm việc gắn lại sau ở Tập hợp chi phí chưa gắn."
                    );
                }
                grid.refresh();
            },
        });
    });
})();
