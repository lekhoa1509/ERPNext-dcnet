// Landed Cost Voucher — VN UX
// 1. Toggle "Hàng nhập khẩu" → auto-insert import-only rows in taxes table
// 2. Toggle "Có chịu thuế nhập khẩu" → add/remove the import_duty row
// 3. Live expense_account suggestion when KTT types description in a charge row
// 4. Show suggested-account intro panel for non-import expense types
//
// Data source: LCV Allocation Settings (seeded with 12 expense types per TT99/2025).
// Backend endpoint: vn_accounting.landed_cost.lcv_hooks.get_lcv_expense_types

(function () {
    const SETTINGS_CACHE_KEY = "_vn_lcv_expense_types";

    function fetch_expense_types(frm) {
        if (frm[SETTINGS_CACHE_KEY]) return Promise.resolve(frm[SETTINGS_CACHE_KEY]);
        return frappe.call({
            method: "vn_accounting.landed_cost.lcv_hooks.get_lcv_expense_types",
            type: "GET",
        }).then(r => {
            const types = (r && r.message) || [];
            frm[SETTINGS_CACHE_KEY] = types;
            // Build a lookup map: label → account
            frm._vn_lcv_label_to_account = {};
            frm._vn_lcv_key_to_row = {};
            for (const t of types) {
                if (t.default_expense_account) {
                    frm._vn_lcv_label_to_account[t.expense_type] = t.default_expense_account;
                }
                frm._vn_lcv_key_to_row[t.expense_type_key] = t;
            }
            return types;
        });
    }

    function row_matches_key(row, expense_type_key, frm) {
        const t = (frm._vn_lcv_key_to_row || {})[expense_type_key];
        if (!t) return false;
        return (row.description || "").trim() === t.expense_type;
    }

    function add_row_for_key(frm, expense_type_key) {
        const t = (frm._vn_lcv_key_to_row || {})[expense_type_key];
        if (!t) return;
        // Skip if already present
        const exists = (frm.doc.taxes || []).some(r => row_matches_key(r, expense_type_key, frm));
        if (exists) return;
        const row = frm.add_child("taxes");
        row.description = t.expense_type;
        if (t.default_expense_account) {
            row.expense_account = t.default_expense_account;
        }
        frm.refresh_field("taxes");
    }

    function remove_row_for_key(frm, expense_type_key) {
        const before = (frm.doc.taxes || []).length;
        frm.doc.taxes = (frm.doc.taxes || []).filter(r => !row_matches_key(r, expense_type_key, frm));
        if (frm.doc.taxes.length !== before) {
            frm.refresh_field("taxes");
        }
    }

    function apply_import_rows(frm) {
        const types = frm[SETTINGS_CACHE_KEY] || [];
        for (const t of types) {
            if (!t.is_import_only) continue;
            // Skip import_duty here — that's gated by vn_is_subject_to_import_duty
            if (t.expense_type_key === "import_duty") continue;
            add_row_for_key(frm, t.expense_type_key);
        }
    }

    function remove_import_rows(frm) {
        const types = frm[SETTINGS_CACHE_KEY] || [];
        for (const t of types) {
            if (!t.is_import_only) continue;
            remove_row_for_key(frm, t.expense_type_key);
        }
    }

    const GUIDE_STORAGE_KEY = "vn_lcv_guide_collapsed";

    function render_help_panel(frm) {
        // Only show on editable (draft) forms
        if (frm.doc.docstatus && frm.doc.docstatus !== 0) return;

        // Avoid duplicates
        if ($(frm.layout.wrapper).find(".vn-lcv-guide").length) return;

        const types = frm[SETTINGS_CACHE_KEY] || [];
        const non_import = types.filter(t => !t.is_import_only).map(t => t.expense_type);

        const collapsed = localStorage.getItem(GUIDE_STORAGE_KEY) === "1";

        const html = `
        <div class="vn-lcv-guide" style="background:#f0f7fa; border:1px solid #d0e3ed; border-radius:8px; padding:0; margin:8px 0 16px; font-size:13px; line-height:1.7; color:#1a3a4a">
            <div class="vn-lcv-guide-header" style="display:flex; justify-content:space-between; align-items:center; padding:12px 18px; cursor:pointer; user-select:none">
                <span style="font-size:14px; font-weight:600">Hướng dẫn sử dụng Phiếu phân bổ chi phí vào giá vốn</span>
                <span class="vn-lcv-guide-toggle" style="font-size:12px; color:#5a7a8a; white-space:nowrap">${collapsed ? "▸ Mở rộng" : "▾ Thu gọn"}</span>
            </div>
            <div class="vn-lcv-guide-body" style="padding:0 18px 14px; ${collapsed ? "display:none" : ""}">
                <div style="margin-bottom:10px">
                    <strong>Mục đích:</strong> Phân bổ các chi phí phát sinh (vận chuyển, bảo hiểm, thuế NK…) vào giá vốn hàng tồn kho, đảm bảo giá vốn phản ánh đúng tổng chi phí mua/sản xuất theo TT99/2025.
                </div>
                <table style="width:100%; border-collapse:collapse; font-size:12.5px; margin-bottom:10px">
                    <tr style="background:#dae8f0">
                        <th style="padding:8px 10px; border:1px solid #c8d8e4; text-align:left; width:50%">Mua hàng (phổ biến nhất)</th>
                        <th style="padding:8px 10px; border:1px solid #c8d8e4; text-align:left">Sản xuất</th>
                    </tr>
                    <tr>
                        <td style="padding:8px 10px; border:1px solid #c8d8e4; vertical-align:top">
                            <strong>Nguồn:</strong> Phiếu nhập kho mua hàng (Purchase Receipt)<br>
                            <strong>Bút toán:</strong> Nợ TK 1562 / Có TK 331, 3333, 3332…<br>
                            <strong>Khi nào:</strong> Sau khi nhận hàng, có đủ HĐ CP vận chuyển/bảo hiểm/thuế NK
                        </td>
                        <td style="padding:8px 10px; border:1px solid #c8d8e4; vertical-align:top">
                            <strong>Nguồn:</strong> Phiếu nhập kho SX (Stock Entry - Material Receipt)<br>
                            <strong>Bút toán:</strong> Nợ TK 155/152 / Có TK 331…<br>
                            <strong>Khi nào:</strong> CP vận chuyển NVL, CP không đưa được vào BOM
                        </td>
                    </tr>
                </table>
                <div style="margin-bottom:8px">
                    <strong>Các bước:</strong>
                    <ol style="margin:4px 0 0 -20px; padding-left:20px">
                        <li><strong>Chứng từ:</strong> Chọn loại (Purchase Receipt / Stock Entry) → chọn phiếu nhập cần phân bổ CP</li>
                        <li><strong>Lấy hàng hóa:</strong> Nhấn "Lấy hàng hóa từ phiếu trên" → hệ thống liệt kê các mặt hàng + số tiền</li>
                        <li><strong>Chi phí áp dụng:</strong> Thêm từng dòng CP (gõ tên loại CP vào ô Description → hệ thống tự điền TK)</li>
                        <li><strong>Duyệt:</strong> Kiểm tra → Lưu → Gửi duyệt (Submit)</li>
                    </ol>
                </div>
                ${non_import.length ? `<div style="margin-bottom:6px"><strong>Loại CP thường gặp:</strong> ${non_import.map(l => `<span class="badge badge-light border" style="font-weight:normal; margin:2px">${frappe.utils.escape_html(l)}</span>`).join("")}</div>` : ""}
                <div style="font-size:12px; color:#5a7a8a; border-top:1px solid #d0e3ed; padding-top:8px; margin-top:4px">
                    <strong>Lưu ý:</strong> VAT NK được khấu trừ (TK 1331) <strong>không</strong> đưa vào bảng chi phí (không cộng vào giá vốn). Tick "Hàng nhập khẩu" → dùng nút "Tạo phiếu VAT NK khấu trừ" ở Actions để tạo bút toán Nợ 1331 / Có 33312 riêng.<br>
                    <a href="/app/lcv-allocation-settings" target="_blank">Cài đặt phân bổ CP vào giá vốn →</a>
                </div>
            </div>
        </div>`;

        // Insert full-width above the form sections (frm.layout.wrapper IS .form-layout)
        $(frm.layout.wrapper).prepend(html);

        // Toggle handler with localStorage persistence
        $(frm.layout.wrapper).find(".vn-lcv-guide-header").on("click", function () {
            const $body = $(this).siblings(".vn-lcv-guide-body");
            const $toggle = $(this).find(".vn-lcv-guide-toggle");
            const isVisible = $body.is(":visible");
            $body.slideToggle(200);
            $toggle.text(isVisible ? "▸ Mở rộng" : "▾ Thu gọn");
            localStorage.setItem(GUIDE_STORAGE_KEY, isVisible ? "1" : "0");
        });
    }

    function show_deductible_vat_dialog(frm) {
        const dlg = new frappe.ui.Dialog({
            title: __("Tạo phiếu VAT NK khấu trừ"),
            fields: [
                {
                    fieldtype: "HTML",
                    fieldname: "intro",
                    options: `
                        <div class="alert alert-info py-2 mb-2">
                            <strong>Cơ chế:</strong> Sinh Phiếu kế toán nháp với bút toán:<br>
                            &nbsp;&nbsp;Nợ <code>1331 - Thuế GTGT được khấu trừ</code> / Có <code>33312 - Thuế GTGT hàng nhập khẩu</code><br>
                            KTT kiểm tra rồi duyệt phiếu (Submit) sau khi tạo.
                        </div>
                    `,
                },
                {
                    fieldtype: "Currency",
                    fieldname: "deductible_amount",
                    label: __("Số tiền VAT NK khấu trừ"),
                    reqd: 1,
                    description: __("Phần VAT nhập khẩu được khấu trừ đầu vào, không cộng vào giá vốn hàng tồn kho."),
                },
                {
                    fieldtype: "Date",
                    fieldname: "posting_date",
                    label: __("Ngày phiếu kế toán"),
                    default: frm.doc.posting_date || frappe.datetime.now_date(),
                },
            ],
            primary_action_label: __("Tạo phiếu nháp"),
            primary_action(values) {
                frappe.call({
                    method: "vn_accounting.landed_cost.lcv_hooks.create_import_vat_deductible_je",
                    args: {
                        lcv_name: frm.doc.name,
                        deductible_amount: values.deductible_amount,
                        posting_date: values.posting_date,
                    },
                    freeze: true,
                    freeze_message: __("Đang tạo phiếu kế toán..."),
                    callback(r) {
                        if (!r.message) return;
                        dlg.hide();
                        frappe.show_alert({
                            message: __(`Đã tạo phiếu kế toán nháp: <a href="/app/journal-entry/${r.message}" target="_blank">${r.message}</a>. Kiểm tra rồi duyệt.`),
                            indicator: "green",
                        }, 10);
                    },
                });
            },
        });
        dlg.show();
    }

    function toggle_deductible_vat_button(frm) {
        // Show button only when LCV is saved (has name) and is import LCV
        const should_show = !frm.is_new() && frm.doc.vn_is_import_lcv;
        // Remove existing button first (avoid duplicates on refresh)
        frm.remove_custom_button(__("Tạo phiếu VAT NK khấu trừ"), __("Hành động"));
        if (should_show) {
            frm.add_custom_button(
                __("Tạo phiếu VAT NK khấu trừ"),
                () => show_deductible_vat_dialog(frm),
                __("Hành động"),
            );
        }
    }

    async function fetch_inventory_split_default(frm) {
        // On NEW LCV: pre-fill landed_cost_inventory_account from Settings.
        if (!frm.is_new()) return;
        if (frm.doc.landed_cost_inventory_account) return;
        if (!frm.doc.company) return;
        try {
            const r = await frappe.call({
                method: "vn_accounting.landed_cost.lcv_hooks.get_lcv_inventory_split_default",
                args: { company: frm.doc.company },
            });
            const acc = r && r.message && r.message.default_account;
            if (acc) frm.set_value("landed_cost_inventory_account", acc);
        } catch (e) {
            // Settings missing or no 1562 — silently skip; hook will warn on submit.
        }
    }

    frappe.ui.form.on("Landed Cost Voucher", {
        async onload(frm) {
            await fetch_expense_types(frm);
            await fetch_inventory_split_default(frm);
        },

        async company(frm) {
            // When KTT changes Company on a fresh LCV, refresh the suggested
            // inventory account (different companies have different 1562 leaves).
            await fetch_inventory_split_default(frm);
        },

        async refresh(frm) {
            await fetch_expense_types(frm);
            render_help_panel(frm);
            toggle_deductible_vat_button(frm);
        },

        async vn_is_import_lcv(frm) {
            await fetch_expense_types(frm);
            toggle_deductible_vat_button(frm);
            if (frm.doc.vn_is_import_lcv) {
                apply_import_rows(frm);
                frappe.show_alert({
                    message: __("Đã thêm các dòng chi phí nhập khẩu mặc định. Tích thêm 'Có chịu thuế nhập khẩu' nếu lô hàng phải nộp thuế NK. VAT NK khấu trừ tạo riêng qua nút 'Tạo phiếu VAT NK khấu trừ' ở Actions."),
                    indicator: "blue",
                }, 10);
            } else {
                // Confirm before removing — KTT may have entered amounts already
                const import_rows_with_amounts = (frm.doc.taxes || []).filter(r => {
                    const t = (frm[SETTINGS_CACHE_KEY] || []).find(x => x.expense_type === r.description);
                    return t && t.is_import_only && (r.amount || 0) !== 0;
                });
                if (import_rows_with_amounts.length) {
                    frappe.confirm(
                        __(`Xoá ${import_rows_with_amounts.length} dòng chi phí nhập khẩu đã nhập số tiền?`),
                        () => {
                            remove_import_rows(frm);
                            frm.set_value("vn_is_subject_to_import_duty", 0);
                        },
                        () => {
                            // Restore checkbox if user cancels
                            frm.set_value("vn_is_import_lcv", 1);
                        },
                    );
                } else {
                    remove_import_rows(frm);
                    frm.set_value("vn_is_subject_to_import_duty", 0);
                }
            }
        },

        async vn_is_subject_to_import_duty(frm) {
            await fetch_expense_types(frm);
            if (!frm.doc.vn_is_import_lcv) return;
            if (frm.doc.vn_is_subject_to_import_duty) {
                add_row_for_key(frm, "import_duty");
            } else {
                // Confirm if there's an amount on the duty row
                const duty_row = (frm.doc.taxes || []).find(r => row_matches_key(r, "import_duty", frm));
                if (duty_row && (duty_row.amount || 0) !== 0) {
                    frappe.confirm(
                        __("Xoá dòng Thuế nhập khẩu đã nhập số tiền?"),
                        () => remove_row_for_key(frm, "import_duty"),
                        () => frm.set_value("vn_is_subject_to_import_duty", 1),
                    );
                } else {
                    remove_row_for_key(frm, "import_duty");
                }
            }
        },
    });

    frappe.ui.form.on("Landed Cost Taxes and Charges", {
        description(frm, cdt, cdn) {
            // Live auto-fill expense_account when description matches a known type
            const row = locals[cdt][cdn];
            if (!row || !row.description) return;
            if (row.expense_account) return; // respect manual entry
            const account = (frm._vn_lcv_label_to_account || {})[row.description.trim()];
            if (account) {
                frappe.model.set_value(cdt, cdn, "expense_account", account);
                frappe.show_alert({
                    message: __(`Đã gợi ý TK: ${account}`),
                    indicator: "green",
                }, 3);
            }
        },
    });
})();
