// Copyright (c) 2026, vn_accounting and contributors
// For license information, please see license.txt

frappe.ui.form.on("Inventory Cost Reallocation", {
    refresh(frm) {
        if (frm.doc.docstatus === 0) {
            frm.add_custom_button(__("Tính lại số tiền phân bổ"), () => recompute(frm), null);
        }
        if (frm.doc.docstatus === 1 && frm.doc.journal_entry) {
            frm.add_custom_button(
                __("Xem Bút toán"),
                () => frappe.set_route("Form", "Journal Entry", frm.doc.journal_entry),
            );
        }
    },

    async onload(frm) {
        if (!frm.is_new()) return;
        if (!frm.doc.company) {
            frm.set_value("company", frappe.defaults.get_user_default("Company"));
        }
        if (frm.doc.company && !frm.doc.source_account) {
            await prefill_default_accounts(frm);
        }
        if (!frm.doc.from_date) {
            const today = frappe.datetime.get_today();
            const ym = today.slice(0, 7);
            frm.set_value("from_date", `${ym}-01`);
            frm.set_value("to_date", frappe.datetime.month_end(today));
            frm.set_value("posting_date", frappe.datetime.month_end(today));
        }
    },

    async company(frm) {
        if (frm.doc.company && (!frm.doc.source_account || !frm.doc.target_account)) {
            await prefill_default_accounts(frm);
        }
    },
});

async function prefill_default_accounts(frm) {
    // Source = 1562 (or Settings default), Target = 1561
    try {
        const r = await frappe.call({
            method: "vn_accounting.landed_cost.lcv_hooks.get_lcv_inventory_split_default",
            args: { company: frm.doc.company },
        });
        const src = r && r.message && r.message.default_account;
        if (src) frm.set_value("source_account", src);
    } catch (e) {
        // ignore
    }
    // Target = company default_inventory_account (= 1561)
    const co = await frappe.db.get_value("Company", frm.doc.company, "default_inventory_account");
    if (co && co.message && co.message.default_inventory_account) {
        frm.set_value("target_account", co.message.default_inventory_account);
    }
}

async function recompute(frm) {
    if (!(frm.doc.company && frm.doc.from_date && frm.doc.to_date && frm.doc.source_account)) {
        frappe.msgprint(__("Vui lòng nhập Công ty, Từ/Đến ngày và TK nguồn trước khi tính."));
        return;
    }
    frappe.dom.freeze(__("Đang tính số tiền phân bổ..."));
    try {
        const r = await frappe.call({
            method:
                "vn_accounting.vn_accounting.doctype.inventory_cost_reallocation.inventory_cost_reallocation.compute_reallocation",
            args: {
                company: frm.doc.company,
                from_date: frm.doc.from_date,
                to_date: frm.doc.to_date,
                source_account: frm.doc.source_account,
                target_account: frm.doc.target_account,
            },
        });
        if (!r || !r.message) return;
        const m = r.message;
        frm.set_value("computed_period_cogs", m.period_cogs);
        frm.set_value("computed_landed_cost_balance", m.source_balance);
        frm.set_value("computed_amount", m.computed_amount);
        frappe.msgprint({
            title: __("Đã tính xong"),
            message: `<pre style="white-space:pre-wrap;font-family:monospace">${
                frappe.utils.escape_html(m.formula_text)
            }</pre>`,
            indicator: "green",
        });
    } finally {
        frappe.dom.unfreeze();
    }
}
