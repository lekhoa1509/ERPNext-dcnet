frappe.ui.form.on("Asset Disposal", {
    refresh(frm) {
        frm.set_query("asset", () => ({
            filters: {
                docstatus: 1,
                status: ["not in", ["Sold", "Scrapped", "Capitalized"]],
            },
        }));

        const account_filters = () => ({
            filters: {
                company: frm.doc.company,
                is_group: 0,
            },
        });
        frm.set_query("fixed_asset_account", account_filters);
        frm.set_query("accumulated_depreciation_account", account_filters);
        frm.set_query("disposal_loss_account", account_filters);
        frm.set_query("disposal_income_account", account_filters);

        if (frm.doc.status === "Draft" && !frm.is_new()) {
            frm.add_custom_button(__("Execute"), () => {
                frappe.confirm(
                    __("Are you sure you want to execute this asset disposal?"),
                    () => {
                        frm.call("execute").then(() => frm.reload_doc());
                    }
                );
            }, null).addClass("btn-primary");
        }

        if (frm.doc.status === "Executed") {
            frm.add_custom_button(__("Cancel Disposal"), () => {
                frappe.confirm(
                    __("Are you sure you want to cancel this disposal and restore the asset?"),
                    () => {
                        frm.call("cancel_disposal").then(() => frm.reload_doc());
                    }
                );
            }, null).addClass("btn-danger");
        }

        // Make fields read-only after execution
        if (frm.doc.status !== "Draft") {
            frm.set_read_only();
        }
    },

    asset(frm) {
        if (!frm.doc.asset) {
            frm.set_value("gross_purchase_amount", 0);
            frm.set_value("accumulated_depreciation", 0);
            frm.set_value("book_value", 0);
            return;
        }

        frappe.db.get_doc("Asset", frm.doc.asset).then((asset) => {
            frm.set_value("gross_purchase_amount", asset.total_asset_cost);
            const book_value = asset.value_after_depreciation || 0;
            frm.set_value("book_value", book_value);
            frm.set_value(
                "accumulated_depreciation",
                (asset.total_asset_cost || 0) - book_value
            );

            // Fetch accounts from Asset Category (not child table — avoid permission issues)
            if (asset.asset_category) {
                frappe.db.get_doc("Asset Category", asset.asset_category).then((cat) => {
                    const row = (cat.accounts || []).find(
                        (r) => r.company_name === asset.company
                    );
                    if (row) {
                        if (row.fixed_asset_account) {
                            frm.set_value("fixed_asset_account", row.fixed_asset_account);
                        }
                        if (row.accumulated_depreciation_account) {
                            frm.set_value(
                                "accumulated_depreciation_account",
                                row.accumulated_depreciation_account
                            );
                        }
                    }
                });
            }

            // Fetch disposal accounts resolved per-company
            if (frm.doc.company) {
                frappe.call({
                    method: "vn_accounting.utils.account_resolver.resolve_accounts_api",
                    args: {
                        fields: JSON.stringify(["disposal_loss_account", "disposal_income_account"]),
                        company: frm.doc.company,
                    },
                    callback(r) {
                        if (!r || !r.message) return;
                        if (r.message.disposal_loss_account) frm.set_value("disposal_loss_account", r.message.disposal_loss_account);
                        if (r.message.disposal_income_account) frm.set_value("disposal_income_account", r.message.disposal_income_account);
                    },
                });
            }
        });
    },
});
