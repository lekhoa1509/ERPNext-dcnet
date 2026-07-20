// Cost Allocation Run form.
// Phase 2b: "Auto từ Timesheet" button to compute shares % from labor hours.

frappe.ui.form.on("Cost Allocation Run", {
    refresh: function (frm) {
        // Filter Stage dropdown in Shares grid by row.project (per-row dynamic)
        if (frm.fields_dict.shares) {
            frm.fields_dict.shares.grid.get_field("project_costing_stage").get_query = function (doc, cdt, cdn) {
                const row = locals[cdt][cdn] || {};
                if (!row.project) {
                    return { filters: { name: "__no_project_selected__" } };
                }
                return {
                    query: "vn_accounting.project_costing.api.stage_link_query",
                    filters: { project: row.project },
                };
            };
        }
        if (frm.doc.docstatus !== 0) return;
        frm.add_custom_button(__("Auto-fill từ Timesheet"), function () {
            open_timesheet_autofill_dialog(frm);
        });
    },
    method: function (frm) {
        frm.trigger("update_share_amounts");
    },
    update_share_amounts: function (frm) {
        // Server-side recompute via validate on save
    },
});

function open_timesheet_autofill_dialog(frm) {
    const d = new frappe.ui.Dialog({
        title: __("Auto-fill shares từ Timesheet"),
        fields: [
            {
                fieldname: "info",
                fieldtype: "HTML",
                options: `<div class="text-muted small">
                    ${__("Chọn 1 nhân viên + kỳ → hệ thống tổng hợp số giờ làm cho mỗi công trình từ Timesheet và tính % phân bổ tự động.")}
                </div>`,
            },
            {
                fieldname: "employee",
                fieldtype: "Link",
                label: __("Nhân viên"),
                options: "Employee",
                reqd: 1,
            },
            {
                fieldname: "period_start",
                fieldtype: "Date",
                label: __("Kỳ bắt đầu"),
                default: frm.doc.run_period_start,
                reqd: 1,
            },
            {
                fieldname: "period_end",
                fieldtype: "Date",
                label: __("Kỳ kết thúc"),
                default: frm.doc.run_period_end,
                reqd: 1,
            },
        ],
        primary_action_label: __("Tính + Áp dụng"),
        primary_action: function (values) {
            frappe.call({
                method: "vn_accounting.project_costing.services.reclassify_engine.autofill_shares_from_timesheet",
                args: {
                    employee: values.employee,
                    period_start: values.period_start,
                    period_end: values.period_end,
                },
                callback: function (r) {
                    const shares = r.message || [];
                    if (!shares.length) {
                        frappe.msgprint(__("Không tìm thấy Timesheet trong kỳ này."));
                        return;
                    }
                    // Replace existing shares
                    frm.clear_table("shares");
                    shares.forEach(s => {
                        const row = frm.add_child("shares");
                        row.project = s.project;
                        row.percent = s.percent;
                    });
                    // Switch to manual method
                    frm.set_value("method", "Thủ công");
                    frm.refresh_field("shares");
                    frm.refresh_field("method");
                    frappe.show_alert({
                        message: __("Đã import {0} dòng. Σ giờ = {1}h",
                            [shares.length, shares.reduce((s, x) => s + x.hours, 0)]),
                        indicator: "green",
                    });
                    d.hide();
                },
            });
        },
    });
    d.show();
}

frappe.ui.form.on("Cost Allocation Source", {
    amount: function (frm) {
        // Recompute total + shares on amount change
        frm.dirty();
    },
});

frappe.ui.form.on("Cost Allocation Share", {
    percent: function (frm) {
        frm.dirty();
    },
});
