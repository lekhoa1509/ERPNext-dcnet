// Re-classify JE row vào công trình (Phase 2b Item 1)
//
// Adds button on submitted Journal Entry form: "Re-classify vào công trình"
// → dialog picks 1+ JE Account rows + project + stage → server creates bù JE.

frappe.ui.form.on("Journal Entry", {
    refresh: function (frm) {
        if (frm.doc.docstatus !== 1) return;
        if (frm.doc.user_remark && /\[PROJECT_COSTING:/.test(frm.doc.user_remark)) {
            // Skip on engine-generated JEs (avoid recursive reclassify)
            return;
        }
        frm.add_custom_button(__("Re-classify vào công trình"), function () {
            open_reclassify_dialog(frm);
        }, __("Actions"));
    },
});

function open_reclassify_dialog(frm) {
    // Filter rows with Dr > 0 (only expense Dr rows can be reclassified into 154)
    const candidates = (frm.doc.accounts || []).filter(r =>
        flt(r.debit_in_account_currency) > 0
    );
    if (!candidates.length) {
        frappe.msgprint(__("JE này không có dòng Dr > 0 để re-classify."));
        return;
    }

    const options = candidates.map(r => ({
        label: `${r.account.split(" - ")[0]} | ${format_currency(r.debit_in_account_currency, "VND", 0)}`,
        value: r.name,
    }));

    const d = new frappe.ui.Dialog({
        title: __("Re-classify chi phí vào công trình"),
        fields: [
            {
                fieldname: "source_row",
                fieldtype: "Select",
                label: __("Dòng JE (Dr)"),
                options: options.map(o => `${o.value}|${o.label}`).join("\n"),
                reqd: 1,
            },
            {
                fieldname: "project",
                fieldtype: "Link",
                label: __("Công trình"),
                options: "Project",
                reqd: 1,
            },
            {
                fieldname: "stage",
                fieldtype: "Link",
                label: __("Giai đoạn (optional)"),
                options: "Project Costing Stage",
                get_query: function () {
                    const p = d.get_value("project");
                    // Filter out invoiced stages — cogs_je must be empty
                    return p ? { filters: { parent_costing: p, cogs_je: ["is", "not set"] } } : {};
                },
                description: __("Giai đoạn đã xuất hóa đơn (đã khóa) sẽ không hiện trong danh sách."),
            },
            {
                fieldname: "amount",
                fieldtype: "Currency",
                label: __("Số tiền (optional, default = Dr của dòng)"),
            },
        ],
        primary_action_label: __("Tạo JE bù"),
        primary_action: function (values) {
            const row_value = values.source_row.split("|")[0];
            frappe.call({
                method: "vn_accounting.project_costing.services.reclassify_engine.reclassify_je_row",
                args: {
                    source_je: frm.doc.name,
                    source_row: row_value,
                    project: values.project,
                    stage: values.stage || null,
                    amount: values.amount || null,
                },
                callback: function (r) {
                    if (!r.message) return;
                    if (r.message.status === "already_reclassified") {
                        frappe.msgprint(__("Dòng này đã được phân bổ vào công trình: {0}", [r.message.je]));
                    } else {
                        frappe.show_alert({
                            message: __("Đã tạo JE bù {0}", [r.message.je]),
                            indicator: "green",
                        });
                        window.open("/app/journal-entry/" + r.message.je, "_blank");
                    }
                    d.hide();
                },
                error: function () {
                    // Server-side guards (stage invoiced, row already assigned)
                    // will throw with user-friendly Vietnamese messages via frappe.throw
                    // → Frappe auto-shows the error dialog. No extra handling needed.
                },
            });
        },
    });
    d.show();
}
