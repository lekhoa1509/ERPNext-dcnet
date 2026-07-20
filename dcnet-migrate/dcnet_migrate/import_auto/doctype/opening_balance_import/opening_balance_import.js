const OPENING_IMPORT_API = "dcnet_migrate.import_auto.doctype.opening_balance_import.opening_balance_import";

frappe.ui.form.on("Opening Balance Import", {
    onload(frm) {
        // Register realtime listener once — notify user when background AI analysis completes
        frappe.realtime.on("opening_analysis_complete", (data) => {
            if (data.docname !== frm.doc.name) return;
            if (data.ok) {
                frappe.show_alert(
                    { message: __("✓ AI phân tích xong: {0}", [frappe.utils.escape_html(frm.doc.display_name || frm.doc.name)]), indicator: "green" },
                    7
                );
            } else {
                frappe.show_alert(
                    { message: __("✗ AI phân tích thất bại — xem Log để biết chi tiết"), indicator: "red" },
                    7
                );
            }
            frm.reload_doc();
        });
    },

    refresh(frm) {
        frm.clear_custom_buttons();
        setup_opening_page_chrome(frm);
        frm.page.set_title(frm.doc.display_name || __("Migration"));
        frm.page.set_indicator(...opening_status_indicator(frm.doc.status));

        // Minimal toolbar — main actions are in the dashboard command bar
        frm.add_custom_button(__("AI Settings"), () => frappe.set_route("Form", "Import Auto Settings"));

        render_opening_import_dashboard(frm);
    },
});

function run_analyze_background(frm) {
    if (frm.doc.__islocal || frm.is_dirty()) {
        frm.save().then(() => run_analyze_background(frm));
        return;
    }
    if (frm.doc.status === "Analyzing") {
        frappe.show_alert({ message: __("AI đang phân tích, vui lòng chờ..."), indicator: "orange" }, 4);
        return;
    }
    frappe.call({
        method: `${OPENING_IMPORT_API}.analyze_files`,
        args: { docname: frm.doc.name },
    }).then((r) => {
        if (r && r.message && r.message.enqueued) {
            frappe.show_alert(
                { message: __("AI đang phân tích trong nền — bạn có thể làm việc khác, sẽ thông báo khi xong."), indicator: "blue" },
                8
            );
            frm.reload_doc();
        }
    });
}

function setup_opening_page_chrome(frm) {
    const $page = frm.page.wrapper;
    $page.find(".layout-side-section").hide();
    $page.find(".layout-main-section-wrapper").css({
        "max-width": "none",
        "width": "100%",
        "padding-right": "0",
    });

    const field = frm.fields_dict.dashboard_html;
    if (field && field.$wrapper) {
        field.$wrapper.closest(".form-column").css({
            "flex": "0 0 100%",
            "max-width": "100%",
            "width": "100%",
        });
    }
}

function opening_status_indicator(status) {
    const map = {
        Draft: [__("Draft"), "gray"],
        Analyzing: [__("Analyzing"), "orange"],
        Analyzed: [__("Analyzed"), "blue"],
        Importing: [__("Importing"), "orange"],
        Completed: [__("Completed"), "green"],
        Partial: [__("Partial"), "yellow"],
        Failed: [__("Failed"), "red"],
    };
    return map[status || "Draft"] || map.Draft;
}

function opening_status_tone(status) {
    return {
        Draft: "neutral",
        Analyzing: "warn",
        Analyzed: "info",
        Importing: "warn",
        Completed: "ok",
        Partial: "warn",
        Failed: "danger",
    }[status || "Draft"] || "neutral";
}

function run_opening_action(frm, method, freeze_message, args = {}, process_config = null) {
    if (frm.doc.__islocal || frm.is_dirty()) {
        return frm.save().then(() => run_opening_action(frm, method, freeze_message, args, process_config));
    }

    const process_state = process_config ? open_opening_process_dialog(process_config) : null;
    const COMPLETE_EVENT = "opening_invoice_import_complete";

    // Resolves only when the action truly finishes. For enqueued (background)
    // actions that means a realtime completion event — so a sequential caller
    // that `await`s this (Sales → Purchase) waits for the first import to fully
    // finish (lock released, status cleared) before starting the next.
    return new Promise((resolve) => {
        let settled = false;
        let safety_timer = null;

        // Pre-register BEFORE the call: with enqueue_after_commit a small import
        // can publish completion before .then() runs, so registering later would
        // miss the event and hang the dialog + the awaiting promise.
        const completion_handler = (data) => {
            if (!data || data.docname !== frm.doc.name) return;
            if (args.invoice_type && data.invoice_type && data.invoice_type !== args.invoice_type) return;
            settle(data.result || { ok: data.ok !== false });
        };
        frappe.realtime.on(COMPLETE_EVENT, completion_handler);

        function settle(result) {
            if (settled) return;
            settled = true;
            if (safety_timer) clearTimeout(safety_timer);
            frappe.realtime.off(COMPLETE_EVENT, completion_handler);
            if (process_state) {
                finish_opening_process_dialog(process_state, result);
            } else {
                frappe.show_alert({
                    message: result.message || __("Processing complete."),
                    indicator: result.ok === false ? "orange" : "green",
                });
            }
            frm.reload_doc().then(() => resolve(result));
        }

        frappe.call({
            method: `${OPENING_IMPORT_API}.${method}`,
            args: { docname: frm.doc.name, ...args },
            freeze: !process_state,
            freeze_message,
        }).then((response) => {
            const result = response.message || {};
            if (result.enqueued) {
                // Background job: keep dialog running; completion_handler settles.
                // Safety net so the UI never wedges if a worker dies without publishing.
                safety_timer = setTimeout(() => settle({
                    ok: false,
                    message: __("Import đang chạy nền lâu bất thường — kiểm tra trạng thái tài liệu và Error Log."),
                }), 25 * 60 * 1000);
                return;
            }
            // Synchronous actions (opening journal / stock / AI journal) settle now.
            settle(result);
        }).catch((error) => {
            settle({ ok: false, message: opening_call_error_message(error) });
        });
    });
}

function parse_opening_json(value, fallback) {
    if (!value) return fallback;
    try {
        return typeof value === "string" ? JSON.parse(value) : value;
    } catch (e) {
        return fallback;
    }
}

function render_opening_import_dashboard(frm) {
    const field = frm.fields_dict.dashboard_html;
    if (!field) return;

    const analysis = parse_opening_json(frm.doc.analysis_json, {});
    const slots = parse_opening_json(frm.doc.file_slots_json, {});
    const summary = parse_opening_json(frm.doc.summary_json, {});
    const files = Array.isArray(analysis.files) ? analysis.files : [];
    const imported = summary.imported || {};
    const master_plan = analysis.master_plan || analysis.auto_master || {};
    const master_summary = summary.opening_master_data || {};
    const ai_journal_count = files.filter((file) => file.handler === "ai_journal").length;
    const master_missing = Number(master_plan.missing || 0);
    const slot_count = Object.keys(slots).length;

    // Determine overall step state
    const step_uploaded = slot_count > 0;
    const step_analyzed = files.length > 0;
    const step_done = summary.status === "Completed" || Boolean(imported.total_created);

    field.$wrapper.html(`
        ${opening_import_styles()}
        <div class="opening-import-shell">

            <section class="opening-import-hero">
                <div class="opening-import-hero__main">
                    <div class="opening-import-hero__meta">
                        <span>Migration</span>
                        <span>${frappe.utils.escape_html(frm.doc.company || "")}</span>
                    </div>
                    <h2>${frappe.utils.escape_html(frm.doc.display_name || __("Opening Balances"))}</h2>
                </div>
                <div class="opening-import-hero__side">
                    ${opening_status_chip(frm.doc.status)}
                    <div class="opening-import-date">
                        <span>${__("Ngày hạch toán đầu kỳ")}</span>
                        <b>${frappe.utils.escape_html(String(frm.doc.posting_date || "2026-01-01"))}</b>
                    </div>
                </div>
            </section>

            <!-- Step guide -->
            <section class="ob-step-guide">
                <div class="ob-step ${step_uploaded ? "ob-step--done" : "ob-step--active"}">
                    <div class="ob-step__num">1</div>
                    <div class="ob-step__body">
                        <b>${__("Upload file Excel")}</b>
                        <span>${slot_count ? __("{0} file đã upload", [slot_count]) : __("Kéo thả file vào ô bên dưới hoặc bấm Upload")}</span>
                    </div>
                </div>
                <div class="ob-step__arrow">→</div>
                <div class="ob-step ${step_analyzed ? "ob-step--done" : step_uploaded ? "ob-step--active" : "ob-step--todo"}">
                    <div class="ob-step__num">2</div>
                    <div class="ob-step__body">
                        <b>${__("AI Phân tích")}</b>
                        <span>${step_analyzed ? __("{0} file đã phân tích", [files.length]) : __("Nhận diện cột, kiểm tra dữ liệu")}</span>
                    </div>
                </div>
                <div class="ob-step__arrow">→</div>
                <div class="ob-step ${step_done ? "ob-step--done" : step_analyzed ? "ob-step--active" : "ob-step--todo"}">
                    <div class="ob-step__num">3</div>
                    <div class="ob-step__body">
                        <b>${__("Import vào ERPNext")}</b>
                        <span>${step_done ? __("Hoàn thành") : __("Tạo chứng từ kế toán")}</span>
                    </div>
                </div>
            </section>

            <!-- File slots grouped by category -->
            ${render_file_slot_grid(slots, files, imported)}

            <!-- Primary action bar -->
            <section class="opening-import-commandbar">
                <div class="ob-action-primary">
                    ${opening_action_button("bulk-upload", "upload", __("Upload cả thư mục"), "quiet")}
                    ${opening_action_button("analyze", "sparkles",
                        step_analyzed ? __("Phân tích lại ({0})", [slot_count]) : __("Phân tích AI{0}", [slot_count ? ` (${slot_count} file)` : ""]),
                        step_uploaded ? "primary" : "quiet")}
                </div>
                <div class="ob-action-secondary">
                    ${slots["chart_of_accounts"] ? opening_action_button("import-coa", "tree", __("Import Hệ thống tài khoản"), "primary") : ""}
                    ${step_analyzed && !master_missing ? opening_action_button("import-opening", "book", __("Import Số dư đầu kỳ"), "success") : ""}
                    ${step_analyzed && !master_missing ? opening_action_button("import-transactions", "receipt", __("Import Phát sinh"), "success") : ""}
                    ${master_missing ? opening_action_button("master", "users", __("Tạo master data ({0} thiếu)", [master_missing]), "warn") : ""}
                    <button class="btn btn-xs btn-default ob-btn-more" data-action="show-advanced">
                        ${frappe.utils.icon("menu", "xs")} ${__("Nâng cao")}
                    </button>
                </div>
            </section>

            ${render_opening_pipeline(frm.doc.status, files, imported, master_plan)}

            ${render_imported_summary(imported)}
        </div>
    `);

    bind_opening_dashboard_actions(frm, field.$wrapper);
    bind_slot_actions(frm, field.$wrapper);
}

function bind_opening_dashboard_actions(frm, wrapper) {
    wrapper.find('[data-action="analyze"]').on("click", () => run_analyze_background(frm));
    wrapper.find('[data-action="master"]').on("click", () => confirm_create_missing_masters(frm));
    wrapper.find('[data-action="plan"]').on("click", () => open_opening_plan_dialog(frm));
    wrapper.find('[data-action="journal"]').on("click", () => confirm_opening_journal(frm));
    wrapper.find('[data-action="stock"]').on("click", () => confirm_opening_stock(frm));
    wrapper.find('[data-action="sales"]').on("click", () => confirm_invoice_import(frm, "sales_invoice"));
    wrapper.find('[data-action="purchase"]').on("click", () => confirm_invoice_import(frm, "purchase_invoice"));
    wrapper.find('[data-action="ai-journal"]').on("click", () => confirm_ai_journal(frm));

    // New simplified actions
    wrapper.find('[data-action="bulk-upload"]').on("click", () => open_bulk_folder_upload(frm));
    wrapper.find('[data-action="import-coa"]').on("click", () => confirm_import_coa(frm));
    wrapper.find('[data-action="import-opening"]').on("click", () => confirm_import_opening_all(frm));
    wrapper.find('[data-action="import-transactions"]').on("click", () => confirm_import_transactions_all(frm));
    wrapper.find('[data-action="show-advanced"]').on("click", () => open_advanced_actions_dialog(frm));
}

// ---------------------------------------------------------------------------
// Bulk folder upload — auto-assign files to slots by filename
// ---------------------------------------------------------------------------

function open_bulk_folder_upload(frm) {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = ".xlsx,.xls";
    input.multiple = true;
    input.setAttribute("webkitdirectory", "");
    input.setAttribute("directory", "");
    input.style.display = "none";
    document.body.appendChild(input);
    input.addEventListener("change", () => {
        const files = Array.from(input.files || []).filter(
            (f) => f && !f.name.startsWith("~$") && /\.(xlsx|xls)$/i.test(f.name)
        );
        input.remove();
        if (!files.length) {
            frappe.msgprint({ title: __("Không tìm thấy file Excel"), message: __("Thư mục không có file .xlsx/.xls"), indicator: "orange" });
            return;
        }
        // Auto-assign each file to a slot
        const assignments = [];
        const unmatched = [];
        for (const file of files) {
            const type = detect_slot_type(file.name);
            if (type) {
                assignments.push({ file, type });
            } else {
                unmatched.push(file.name);
            }
        }

        // Show preview dialog
        const rows_html = assignments.map(({ file, type }) => {
            const group_label = SLOT_GROUPS.flatMap((g) => g.slots).find((s) => s.type === type);
            return `<tr>
                <td>${frappe.utils.escape_html(file.name)}</td>
                <td><b>${frappe.utils.escape_html(group_label ? group_label.name : type)}</b></td>
            </tr>`;
        }).join("");
        const unmatched_html = unmatched.length
            ? `<p style="color:#b45309;margin-top:8px">${__("Không nhận diện được")} ${unmatched.length} file: ${frappe.utils.escape_html(unmatched.slice(0, 4).join(", "))}${unmatched.length > 4 ? "..." : ""}</p>`
            : "";

        const dialog = new frappe.ui.Dialog({
            title: __("Xác nhận upload hàng loạt"),
            fields: [{
                fieldtype: "HTML",
                options: `<table class="table table-bordered table-sm" style="font-size:13px">
                    <thead><tr><th>${__("File")}</th><th>${__("Gán vào slot")}</th></tr></thead>
                    <tbody>${rows_html}</tbody>
                </table>${unmatched_html}`,
            }],
            primary_action_label: __("Upload {0} file", [assignments.length]),
            primary_action() {
                dialog.hide();
                _bulk_upload_with_slots(frm, assignments);
            },
        });
        dialog.show();
    });
    input.click();
}

async function _bulk_upload_with_slots(frm, assignments) {
    if (!assignments.length) return;
    try {
        if (frm.doc.__islocal || frm.is_dirty()) await frm.save();
        frappe.dom.freeze(__("Đang upload file..."));
        for (let i = 0; i < assignments.length; i++) {
            const { file, type } = assignments[i];
            frappe.show_progress(__("Upload"), i + 1, assignments.length, file.name);
            await _upload_single_slot_file(frm.doc.name, file, type);
        }
        frappe.dom.unfreeze();
        frappe.show_alert({ message: __(`Đã upload ${assignments.length} file thành công`), indicator: "green" }, 5);
        await frm.reload_doc();
        run_analyze_background(frm);
    } catch (err) {
        frappe.dom.unfreeze();
        frappe.msgprint({ title: __("Upload thất bại"), message: frappe.utils.escape_html(String(err.message || err)), indicator: "red" });
    }
}

async function _upload_single_slot_file(docname, file, migration_type) {
    const form_data = new FormData();
    form_data.append("docname", docname);
    form_data.append("migration_type", migration_type);
    form_data.append("relative_path", file.name);
    form_data.append("file", file, file.name);
    const response = await fetch(
        `/api/method/dcnet_migrate.import_auto.doctype.opening_balance_import.opening_balance_import.upload_excel_file`,
        { method: "POST", headers: { "X-Frappe-CSRF-Token": frappe.csrf_token }, credentials: "same-origin", body: form_data }
    );
    const data = await response.json().catch(() => ({}));
    if (!response.ok || data.exc) {
        throw new Error(opening_upload_server_error(data) || response.statusText || __("Upload thất bại"));
    }
    return data.message || {};
}

// ---------------------------------------------------------------------------
// Simplified import-all actions
// ---------------------------------------------------------------------------

function confirm_import_coa(frm) {
    const d = new frappe.ui.Dialog({
        title: __("Import Hệ thống tài khoản"),
        fields: [
            {
                fieldtype: "HTML",
                options: `<div style="padding:8px 0">
                    <p>Sẽ tạo:</p>
                    <ul style="margin-left:16px;line-height:1.8">
                        <li>5 nhóm gốc TT200: Tài sản · Nợ phải trả · Vốn CSH · Doanh thu · Chi phí</li>
                        <li>Toàn bộ cây tài khoản từ file <b>Danh_sach_he_thong_tai_khoan.xlsx</b></li>
                        <li>Quan hệ cha-con tự động từ số tài khoản (111 → 1111, 1112...)</li>
                    </ul>
                </div>`,
            },
            { fieldtype: "Check", fieldname: "force", label: __("Ghi đè tài khoản đã tồn tại (force)"), default: 0 },
            {
                fieldtype: "Check",
                fieldname: "clear",
                label: __("⚠️ Xóa toàn bộ tài khoản cũ trước khi import (bỏ qua TK đã có giao dịch)"),
                default: 0,
            },
        ],
        primary_action_label: __("Import"),
        primary_action(values) {
            d.hide();
            frappe.show_progress(__("Import cây tài khoản..."), 0, 100, __("Đang xử lý..."));
            frappe.call({
                method: "dcnet_migrate.import_auto.doctype.opening_balance_import.opening_balance_import.import_chart_of_accounts",
                args: { docname: frm.doc.name, force: values.force ? 1 : 0, clear: values.clear ? 1 : 0 },
                callback(r) {
                    frappe.hide_progress();
                    if (r.exc) return;
                    const res = r.message || {};
                    let msg = __("Tạo {0} tài khoản, bỏ qua {1}, lỗi {2}.", [res.created || 0, res.skipped || 0, res.error_count || 0]);
                    if (res.cleared) {
                        const c = res.cleared;
                        msg = __("Đã xóa {0} TK cũ (bỏ qua {1} TK có GL entry).", [c.deleted || 0, c.skipped_gl || 0]) + "<br>" + msg;
                    }
                    if (res.error_count > 0) {
                        frappe.msgprint({
                            title: __("Import hoàn tất (có lỗi)"),
                            message: msg + "<br><br>" + (res.errors || []).slice(0, 10).map((e) => __("TK {0}: {1}", [e.num, e.error])).join("<br>"),
                            indicator: "orange",
                        });
                    } else {
                        frappe.show_alert({ message: msg, indicator: "green" }, 6);
                    }
                    frm.refresh();
                },
            });
        },
    });
    d.show();
}

function confirm_import_opening_all(frm) {
    const d = new frappe.ui.Dialog({
        title: __("Import Số dư đầu kỳ"),
        fields: [
            {
                fieldtype: "HTML",
                options: `<div style="padding:8px 0">
                    <p>Sẽ chạy tuần tự:</p>
                    <ol style="margin-left:16px;line-height:1.8">
                        <li>Tạo Journal Entry đầu kỳ (TK 131, 331, 131K, 112...)</li>
                        <li>Tạo Stock Reconciliation (tồn kho VTHH)</li>
                        <li>Import AI Journal cho TSCĐ, CCDC, Chi phí trả trước</li>
                    </ol>
                </div>`,
            },
            { fieldtype: "Check", fieldname: "submit", label: __("Submit ngay sau khi tạo"), default: 1 },
            { fieldtype: "Check", fieldname: "force",  label: __("Ghi đè nếu đã tồn tại (force)"), default: 0 },
            {
                fieldtype: "Date",
                fieldname: "posting_date",
                label: __("Ngày hạch toán"),
                default: frm.doc.posting_date || "2026-01-01",
            },
        ],
        primary_action_label: __("Bắt đầu Import"),
        async primary_action(values) {
            d.hide();
            // Run opening JE → stock → ai journal sequentially
            await run_opening_action(frm, "execute_opening_journal", __("Tạo Opening Journal Entry..."),
                { posting_date: values.posting_date, submit: values.submit ? 1 : 0, force: values.force ? 1 : 0 },
                opening_process_config("journal", frm));
            await run_opening_action(frm, "execute_opening_stock", __("Tạo Stock Reconciliation..."),
                { posting_date: values.posting_date, submit: values.submit ? 1 : 0, force: values.force ? 1 : 0 },
                opening_process_config("stock", frm));
            if (frm.doc.analysis_json) {
                const analysis = parse_opening_json(frm.doc.analysis_json, {});
                const ai_count = (analysis.files || []).filter((f) => f.handler === "ai_journal").length;
                if (ai_count) {
                    await run_opening_action(frm, "execute_ai_journal", __("Tạo AI Journal..."),
                        { posting_date: values.posting_date, submit: values.submit ? 1 : 0, force: values.force ? 1 : 0 },
                        opening_process_config("ai-journal", frm));
                }
            }
        },
    });
    d.show();
}

function confirm_import_transactions_all(frm) {
    const d = new frappe.ui.Dialog({
        title: __("Import Phát sinh trong năm"),
        fields: [
            {
                fieldtype: "HTML",
                options: `<div style="padding:8px 0">
                    <p>Sẽ import:</p>
                    <ol style="margin-left:16px;line-height:1.8">
                        <li>Hóa đơn bán ra (Sales Invoice)</li>
                        <li>Hóa đơn mua vào (Purchase Invoice)</li>
                    </ol>
                    <p style="color:#64748b;font-size:12px;margin-top:8px">
                        Sổ Nhật Ký Chung và Sổ chi tiết VTHH dùng để đối chiếu — chưa import tự động.
                    </p>
                </div>`,
            },
            { fieldtype: "Check", fieldname: "submit", label: __("Submit ngay sau khi tạo"), default: 1 },
            { fieldtype: "Check", fieldname: "force",  label: __("Ghi đè nếu đã tồn tại (force)"), default: 0 },
            { fieldtype: "Int",   fieldname: "limit",  label: __("Giới hạn số dòng (để trống = không giới hạn)") },
        ],
        primary_action_label: __("Bắt đầu Import"),
        async primary_action(values) {
            d.hide();
            await run_opening_action(frm, "execute_invoices", __("Import Sales Invoice..."),
                { invoice_type: "sales_invoice", submit: values.submit ? 1 : 0, force: values.force ? 1 : 0, limit: values.limit || null },
                opening_process_config("sales", frm));
            await run_opening_action(frm, "execute_invoices", __("Import Purchase Invoice..."),
                { invoice_type: "purchase_invoice", submit: values.submit ? 1 : 0, force: values.force ? 1 : 0, limit: values.limit || null },
                opening_process_config("purchase", frm));
        },
    });
    d.show();
}

function open_advanced_actions_dialog(frm) {
    const d = new frappe.ui.Dialog({
        title: __("Nâng cao"),
        fields: [{ fieldtype: "HTML", options: `
            <div style="display:flex;flex-direction:column;gap:8px;padding:4px 0">
                <button class="btn btn-sm btn-default" data-adv="plan">📋 ${__("Xem kế hoạch import (View Plan)")}</button>
                <button class="btn btn-sm btn-default" data-adv="journal">📖 ${__("Chỉ tạo Opening JE")}</button>
                <button class="btn btn-sm btn-default" data-adv="stock">📦 ${__("Chỉ tạo Opening Stock")}</button>
                <button class="btn btn-sm btn-default" data-adv="sales">🧾 ${__("Chỉ import Sales Invoice")}</button>
                <button class="btn btn-sm btn-default" data-adv="purchase">🧾 ${__("Chỉ import Purchase Invoice")}</button>
                <button class="btn btn-sm btn-default" data-adv="ai-journal">🤖 ${__("Chỉ chạy AI Journal")}</button>
                <button class="btn btn-sm btn-default" data-adv="master">👤 ${__("Tạo master data thiếu")}</button>
            </div>
        `}],
    });
    d.$wrapper.find("[data-adv]").on("click", function () {
        const action = $(this).data("adv");
        d.hide();
        if (action === "plan")       open_opening_plan_dialog(frm);
        if (action === "journal")    confirm_opening_journal(frm);
        if (action === "stock")      confirm_opening_stock(frm);
        if (action === "sales")      confirm_invoice_import(frm, "sales_invoice");
        if (action === "purchase")   confirm_invoice_import(frm, "purchase_invoice");
        if (action === "ai-journal") confirm_ai_journal(frm);
        if (action === "master")     confirm_create_missing_masters(frm);
    });
    d.show();
}

function open_opening_upload_picker(frm, mode) {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = ".xlsx,.xls";
    input.multiple = true;
    if (mode === "folder") {
        input.setAttribute("webkitdirectory", "");
        input.setAttribute("directory", "");
    }
    input.style.display = "none";
    document.body.appendChild(input);
    input.addEventListener("change", () => {
        const files = Array.from(input.files || []);
        input.remove();
        confirm_opening_upload_files(frm, files, mode);
    });
    input.click();
}

function confirm_opening_upload_files(frm, files, mode) {
    const excel_files = files.filter((file) => (
        file && !file.name.startsWith("~$") && /\.(xlsx|xls)$/i.test(file.name || "")
    ));
    if (!excel_files.length) {
        frappe.msgprint({
            title: __("No Excel Files"),
            message: __("Please choose one or more .xlsx/.xls files."),
            indicator: "orange",
        });
        return;
    }

    const max_file_size = Number(frappe.boot.max_file_size || 25 * 1024 * 1024);
    const oversized_files = excel_files.filter((file) => file.size > max_file_size);
    if (oversized_files.length) {
        const file_list = oversized_files.slice(0, 6)
            .map((file) => `<li>${frappe.utils.escape_html(file.name)} (${opening_format_file_size(file.size)})</li>`)
            .join("");
        frappe.msgprint({
            title: __("File Too Large"),
            message: `
                <div>${__("Each uploaded file must not exceed {0}.", [opening_format_file_size(max_file_size)])}</div>
                <ul>${file_list}</ul>
            `,
            indicator: "orange",
        });
        return;
    }

    const sample_names = excel_files.slice(0, 6)
        .map((file) => `<li>${frappe.utils.escape_html(opening_upload_relative_path(file))}</li>`)
        .join("");
    const hidden_count = Math.max(excel_files.length - 6, 0);
    const dialog = new frappe.ui.Dialog({
        title: mode === "folder" ? __("Upload Folder") : __("Upload Excel Files"),
        fields: [
            {
                fieldtype: "HTML",
                fieldname: "upload_summary",
                options: `
                    <div class="opening-upload-summary">
                        <div><strong>${excel_files.length}</strong> ${__("Excel file(s) selected")}</div>
                        <ul>${sample_names}${hidden_count ? `<li>${__("+ {0} more files", [hidden_count])}</li>` : ""}</ul>
                    </div>
                `,
            },
            {
                fieldtype: "Check",
                fieldname: "clear_existing",
                label: __("Replace files in this opening import server folder"),
                default: 1,
            },
        ],
        primary_action_label: __("Upload and Analyze"),
        primary_action(values) {
            dialog.hide();
            upload_opening_files_to_server(frm, excel_files, Boolean(values.clear_existing));
        },
    });
    dialog.show();
}

function opening_upload_relative_path(file) {
    return file.webkitRelativePath || file.name;
}

function opening_format_file_size(bytes) {
    const size = Number(bytes || 0);
    if (size >= 1024 * 1024) {
        return `${(size / (1024 * 1024)).toFixed(1)} MB`;
    }
    return `${Math.max(1, Math.ceil(size / 1024))} KB`;
}

async function upload_opening_files_to_server(frm, files, clear_existing) {
    try {
        if (frm.doc.__islocal || frm.is_dirty()) {
            await frm.save();
        }

        frappe.dom.freeze(__("Uploading opening Excel files to server..."));
        for (let index = 0; index < files.length; index++) {
            const file = files[index];
            frappe.show_progress(
                __("Uploading opening Excel files"),
                index + 1,
                files.length,
                opening_upload_relative_path(file)
            );
            await upload_single_opening_excel_file(
                frm.doc.name,
                file,
                index === 0 && clear_existing
            );
        }
        frappe.dom.unfreeze();
        if (frappe.hide_progress) {
            frappe.hide_progress();
        }
        frappe.show_alert({
            message: __("Uploaded {0} Excel file(s) to server.", [files.length]),
            indicator: "green",
        }, 5);

        await frm.reload_doc();
        return run_opening_action(
            frm,
            "analyze_files",
            __("Analyzing uploaded files..."),
            {},
            opening_process_config("analyze", frm)
        );
    } catch (error) {
        frappe.dom.unfreeze();
        if (frappe.hide_progress) {
            frappe.hide_progress();
        }
        frappe.msgprint({
            title: __("Upload Failed"),
            message: frappe.utils.escape_html(error.message || String(error)),
            indicator: "red",
        });
        return null;
    }
}

async function upload_single_opening_excel_file(docname, file, clear_existing) {
    const form_data = new FormData();
    form_data.append("docname", docname);
    form_data.append("relative_path", opening_upload_relative_path(file));
    form_data.append("clear_existing", clear_existing ? "1" : "0");
    form_data.append("file", file, file.name);

    const response = await fetch(`/api/method/${OPENING_IMPORT_API}.upload_excel_file`, {
        method: "POST",
        headers: {
            "X-Frappe-CSRF-Token": frappe.csrf_token,
        },
        credentials: "same-origin",
        body: form_data,
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok || data.exc) {
        throw new Error(opening_upload_server_error(data) || response.statusText || __("Upload failed."));
    }
    return data.message || {};
}

function opening_upload_server_error(data) {
    if (!data) return "";
    if (data._server_messages) {
        try {
            return JSON.parse(data._server_messages)
                .map((message) => {
                    const parsed = JSON.parse(message);
                    return parsed.message || message;
                })
                .join("<br>");
        } catch (error) {
            return data._server_messages;
        }
    }
    return data.exception || data.exc || "";
}

function opening_status_chip(status) {
    const label = opening_status_indicator(status)[0];
    return `<span class="opening-chip opening-chip--${opening_status_tone(status)}">${frappe.utils.escape_html(label)}</span>`;
}

function opening_action_button(action, icon, label, tone) {
    return `
        <button type="button" class="opening-action opening-action--${tone || "quiet"}" data-action="${frappe.utils.escape_html(action)}">
            ${icon_svg(icon)}
            <span>${frappe.utils.escape_html(label)}</span>
        </button>
    `;
}

function render_opening_pipeline(status, files, imported, master_plan = {}) {
    const has_files = files.length > 0;
    const master_missing = Number(master_plan && master_plan.missing || 0);
    const master_done = has_files && !master_missing;
    const has_journal = Boolean(imported && imported.opening_balance_import);
    const has_stock = Boolean(imported && imported.opening_stock && imported.opening_stock.created);
    const has_invoice = Boolean(
        imported &&
        ((imported.sales_invoice && imported.sales_invoice.created) ||
         (imported.purchase_invoice && imported.purchase_invoice.created))
    );
    const completed = status === "Completed";
    const phases = [
        { key: "analyze", label: __("Analyze Files"), value: has_files ? __("Ready") : __("Not Run"), done: has_files },
        { key: "master", label: __("Master Data"), value: master_done ? __("Ready") : `${master_missing} ${__("missing")}`, done: master_done },
        { key: "journal", label: __("Accounting Balances"), value: has_journal ? __("Created") : __("Pending"), done: has_journal },
        { key: "stock", label: __("Stock"), value: has_stock ? __("Created") : __("Pending"), done: has_stock },
        { key: "invoice", label: __("Invoices"), value: has_invoice ? __("Created") : __("Pending"), done: has_invoice },
        { key: "review", label: __("Review"), value: completed ? __("Complete") : __("Monitoring"), done: completed },
    ];

    return `
        <section class="opening-pipeline">
            ${phases.map((phase, index) => `
                <div class="opening-pipeline-step opening-pipeline-step--${phase.done ? "done" : "todo"}">
                    <div class="opening-pipeline-step__index">${index + 1}</div>
                    <div>
                        <b>${frappe.utils.escape_html(phase.label)}</b>
                        <span>${frappe.utils.escape_html(phase.value)}</span>
                    </div>
                </div>
            `).join("")}
        </section>
    `;
}

function opening_stat_card(label, value, hint, icon) {
    return `
        <div class="opening-import-stat">
            <div class="opening-import-stat__head">
                ${icon_svg(icon)}
                <span>${frappe.utils.escape_html(label)}</span>
            </div>
            <b>${frappe.utils.escape_html(String(value))}</b>
            <small>${frappe.utils.escape_html(hint || "")}</small>
        </div>
    `;
}

// ---------------------------------------------------------------------------
// File Slot Grid
// ---------------------------------------------------------------------------

// Maps filename keywords → migration_type for bulk-folder auto-assign
const SLOT_FILENAME_MAP = [
    { type: "chart_of_accounts", keywords: ["he_thong_tai_khoan", "danh_sach_tai_khoan_ke_toan"] },
    { type: "account_balance",   keywords: ["so_du_tai_khoan"] },
    { type: "customer_balance",  keywords: ["cong_no_khach_hang"] },
    { type: "supplier_balance",  keywords: ["cong_no_nha_cung_cap"] },
    { type: "employee_balance",  keywords: ["cong_no_nhan_vien"] },
    { type: "bank_balance",      keywords: ["nhap_so_du_tai_khoan_ngan_hang", "so_du_ngan_hang"] },
    { type: "stock_balance",     keywords: ["ton_kho_vthh", "ton_kho"] },
    { type: "fixed_asset",       keywords: ["tai_san_co_dinh"] },
    { type: "tools",             keywords: ["cong_cu_dung_cu"] },
    { type: "prepaid",           keywords: ["chi_phi_tra_truoc"] },
    { type: "deferred_revenue",  keywords: ["doanh_thu_nhan_truoc"] },
    { type: "sales_invoice",     keywords: ["ban_ra", "hoa_don_ban"] },
    { type: "purchase_invoice",  keywords: ["mua_vao", "hoa_don_mua"] },
    { type: "stock_detail",      keywords: ["chi_tiet_vat_tu", "so_chi_tiet_vat"] },
    { type: "general_journal",   keywords: ["nhat_ky_chung", "so_nhat_ky"] },
];

function detect_slot_type(filename) {
    const normalized = filename.toLowerCase().replace(/[^a-z0-9]/g, "_");
    for (const { type, keywords } of SLOT_FILENAME_MAP) {
        if (keywords.some((kw) => normalized.includes(kw))) {
            return type;
        }
    }
    return null;
}

const SLOT_GROUPS = [
    {
        label: __("Danh mục kế toán"),
        folder: "01_Danh_Muc",
        slots: [
            { type: "chart_of_accounts", name: __("Hệ thống tài khoản"), icon: "🌳", hint: __("Số TK · Tên TK · Tính chất (Dư Nợ/Có)") },
        ],
    },
    {
        label: __("Số dư đầu kỳ"),
        folder: "02_So_Du_Dau_Ky",
        slots: [
            { type: "account_balance",   name: __("Số dư tài khoản"),          icon: "📊", hint: __("Mã TK · Số dư Nợ · Số dư Có") },
            { type: "customer_balance",  name: __("Công nợ khách hàng"),        icon: "👤", hint: __("Mã KH · Tên KH · Dư Nợ · Dư Có") },
            { type: "supplier_balance",  name: __("Công nợ nhà cung cấp"),      icon: "🏢", hint: __("Mã NCC · Tên NCC · Dư Nợ · Dư Có") },
            { type: "employee_balance",  name: __("Công nợ nhân viên"),         icon: "👔", hint: __("Mã NV · Tên NV · Tạm ứng") },
            { type: "bank_balance",      name: __("Số dư ngân hàng"),           icon: "🏦", hint: __("Ngân hàng · STK · Số dư") },
            { type: "stock_balance",     name: __("Tồn kho VTHH"),              icon: "📦", hint: __("Mã hàng · Tên kho · Số lượng · Giá trị") },
            { type: "fixed_asset",       name: __("Tài sản cố định"),           icon: "🏗️", hint: __("Mã TSCĐ · Nguyên giá · Hao mòn") },
            { type: "tools",             name: __("Công cụ dụng cụ"),           icon: "🔧", hint: __("Mã CCDC · Số lượng · Giá trị") },
            { type: "prepaid",           name: __("Chi phí trả trước"),         icon: "📋", hint: __("Nội dung · Giá trị · Kỳ phân bổ") },
            { type: "deferred_revenue",  name: __("Doanh thu nhận trước"),      icon: "💰", hint: __("Nội dung · Giá trị · Kỳ phân bổ") },
        ],
    },
    {
        label: __("Phát sinh trong năm"),
        folder: "03_Phat_Sinh_Trong_Nam",
        slots: [
            { type: "sales_invoice",    name: __("Hóa đơn bán ra"),            icon: "🧾", hint: __("Số HĐ · Mã KH · Ngày · Tiền") },
            { type: "purchase_invoice", name: __("Hóa đơn mua vào"),           icon: "🧾", hint: __("Số HĐ · Mã NCC · Ngày · Tiền") },
            { type: "stock_detail",     name: __("Sổ chi tiết vật tư hàng hóa"), icon: "📑", hint: __("Mã hàng · Nhập · Xuất · Tồn") },
            { type: "general_journal",  name: __("Sổ nhật ký chung"),          icon: "📒", hint: __("Ngày · Số CT · Mã ĐT · Nợ · Có") },
        ],
    },
];

function render_file_slot_grid(slots, analyzed_files, imported) {
    const analyzed_by_type = {};
    for (const f of (analyzed_files || [])) {
        analyzed_by_type[f.migration_type] = f;
    }
    const imported_types = new Set(
        Object.entries(imported || {}).filter(([, v]) => v && v.created > 0).map(([k]) => k)
    );
    // map imported key → migration_type (invoice types reuse same key)
    const IMPORT_KEY_MAP = {
        opening_balance_import: "account_balance",
        opening_stock: "stock_detail",
        sales_invoice: "sales_invoice",
        purchase_invoice: "purchase_invoice",
        ai_journal: null,
    };

    const groups_html = SLOT_GROUPS.map((group) => {
        const cards = group.slots.map((def) => {
            const file_path = slots[def.type] || "";
            const file_name = file_path ? file_path.split("/").pop() : "";
            const analyzed = analyzed_by_type[def.type];
            const handler = analyzed ? analyzed.handler : null;
            const is_imported = imported_types.has(def.type) || (
                Object.entries(IMPORT_KEY_MAP).some(([k, v]) => v === def.type && imported_types.has(k))
            );

            let status_label, status_class;
            if (is_imported) {
                status_label = __("Imported"); status_class = "done";
            } else if (handler && handler !== "ignored") {
                status_label = __("Analyzed"); status_class = "analyzed";
            } else if (file_path) {
                status_label = __("Uploaded"); status_class = "uploaded";
            } else {
                status_label = __("Empty"); status_class = "empty";
            }

            const handler_chip = handler ? opening_handler_chip(handler) : "";
            const row_count = analyzed ? (analyzed.row_count || "") : "";

            return `
                <div class="ob-slot-card ob-slot-card--${status_class}" data-type="${frappe.utils.escape_html(def.type)}">
                    <div class="ob-slot-card__head">
                        <span class="ob-slot-icon">${def.icon}</span>
                        <div class="ob-slot-card__title-wrap">
                            <div class="ob-slot-title">${frappe.utils.escape_html(def.name)}</div>
                            <div class="ob-slot-hint">${frappe.utils.escape_html(def.hint)}</div>
                        </div>
                        <span class="ob-slot-badge ob-slot-badge--${status_class}">${status_label}</span>
                    </div>
                    ${file_path ? `
                    <div class="ob-slot-file">
                        <span class="ob-slot-filename" title="${frappe.utils.escape_html(file_path)}">
                            ${frappe.utils.escape_html(file_name)}
                        </span>
                        <div class="ob-slot-file-meta">
                            ${handler_chip}
                            ${row_count ? `<span class="ob-slot-rows">${row_count} rows</span>` : ""}
                        </div>
                    </div>` : ""}
                    <div class="ob-slot-actions">
                        <button class="btn btn-xs ob-slot-upload-btn ${file_path ? "btn-default" : "btn-primary"}"
                            data-action="slot-upload" data-type="${frappe.utils.escape_html(def.type)}">
                            ${frappe.utils.icon("upload", "xs")}
                            ${file_path ? __("Replace") : __("Upload")}
                        </button>
                        ${file_path ? `
                        <button class="btn btn-xs btn-default ob-slot-clear-btn"
                            data-action="slot-clear" data-type="${frappe.utils.escape_html(def.type)}"
                            title="${__("Remove file")}">
                            ${frappe.utils.icon("close", "xs")}
                        </button>` : ""}
                    </div>
                </div>`;
        }).join("");

        const uploaded_in_group = group.slots.filter((s) => slots[s.type]).length;
        return `
            <div class="ob-slot-group">
                <div class="ob-slot-group__label">
                    <span>${frappe.utils.escape_html(group.label)}</span>
                    ${group.folder ? `<span class="ob-slot-group__folder">📁 ${frappe.utils.escape_html(group.folder)}</span>` : ""}
                    <span class="ob-slot-group__count">${uploaded_in_group}/${group.slots.length} file</span>
                </div>
                <div class="ob-slot-cards">${cards}</div>
            </div>`;
    }).join("");

    return `
        <section class="ob-slot-section">
            ${groups_html}
        </section>`;
}

function bind_slot_actions(frm, wrapper) {
    wrapper.find('[data-action="slot-upload"]').on("click", function () {
        const migration_type = $(this).data("type");
        _open_slot_upload_picker(frm, migration_type);
    });
    wrapper.find('[data-action="slot-clear"]').on("click", function () {
        const migration_type = $(this).data("type");
        frappe.confirm(
            __("Xóa file đã upload cho slot này?"),
            () => _clear_slot(frm, migration_type)
        );
    });
}

function _open_slot_upload_picker(frm, migration_type) {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = ".xlsx,.xls";
    input.style.display = "none";
    document.body.appendChild(input);
    input.addEventListener("change", () => {
        const file = input.files && input.files[0];
        input.remove();
        if (!file) return;
        if (!/\.(xlsx|xls)$/i.test(file.name)) {
            frappe.msgprint({ title: __("Wrong file type"), message: __("Please select an .xlsx or .xls file."), indicator: "orange" });
            return;
        }
        _upload_slot_file(frm, migration_type, file);
    });
    input.click();
}

function _upload_slot_file(frm, migration_type, file) {
    // Show loading state on the card
    const $wrapper = frm.fields_dict.dashboard_html.$wrapper;
    const $card = $wrapper.find(`.ob-slot-card[data-type="${migration_type}"]`);
    const $btn = $card.find('[data-action="slot-upload"]');
    $btn.prop("disabled", true).html(
        `<span class="ob-spinner"></span> ${__("Đang upload...")}`
    );
    $card.addClass("ob-slot-card--loading");

    const form_data = new FormData();
    form_data.append("file", file, file.name);
    form_data.append("docname", frm.doc.name);
    form_data.append("migration_type", migration_type);

    // Use fetch with FormData — frappe.call serializes as JSON and drops the file
    fetch(`/api/method/${OPENING_IMPORT_API}.upload_excel_file`, {
        method: "POST",
        headers: { "X-Frappe-CSRF-Token": frappe.csrf_token },
        body: form_data,
    })
    .then((resp) => {
        if (!resp.ok) return resp.json().then((d) => { throw new Error(d.exc_type || `HTTP ${resp.status}`); });
        return resp.json();
    })
    .then((data) => {
        if (data.exc) {
            frappe.msgprint({ title: __("Upload thất bại"), message: frappe.utils.escape_html(data.exc), indicator: "red" });
            $card.removeClass("ob-slot-card--loading");
            frm.reload_doc();
            return;
        }
        if (data.message && data.message.file_path) {
            frm.reload_doc().then(() => {
                frappe.show_alert(
                    { message: __("✓ Đã upload: {0}", [frappe.utils.escape_html(file.name)]), indicator: "green" },
                    5
                );
            });
        }
    })
    .catch((err) => {
        $card.removeClass("ob-slot-card--loading");
        $btn.prop("disabled", false).html(
            `${frappe.utils.icon("upload", "xs")} ${__("Upload")}`
        );
        frappe.show_alert(
            { message: __("Upload thất bại: {0}", [err.message || __("Lỗi không xác định")]), indicator: "red" },
            6
        );
    });
}

function _clear_slot(frm, migration_type) {
    frappe.call({
        method: `${OPENING_IMPORT_API}.clear_file_slot`,
        args: { docname: frm.doc.name, migration_type },
        callback() {
            frappe.show_alert({ message: __("Đã xóa file slot"), indicator: "green" });
            frm.reload_doc();
        },
    });
}

// ---------------------------------------------------------------------------

function render_analysis_files(files) {
    if (!files.length) {
        return `
            <section class="opening-import-empty">
                <div class="opening-import-empty__icon">${icon_svg("sparkles")}</div>
                <div>
                    <b>${__("No File Analysis Yet")}</b>
                    <span>${__("Click AI Analyze Files to create the processing list.")}</span>
                </div>
            </section>
        `;
    }

    return `
        <section class="opening-import-panel">
            <div class="opening-import-panel__head">
                <div>
                    <b>${__("File List")}</b>
                    <span>${__("AI classifies, backend runs fixed handlers")}</span>
                </div>
                <span class="opening-panel-count">${files.length}</span>
            </div>
            <div class="opening-import-table-wrap">
                <table class="table opening-import-table">
                    <thead>
                        <tr>
                            <th>${__("File")}</th>
                            <th>${__("Type")}</th>
                            <th>${__("Handler")}</th>
                            <th>${__("Rows")}</th>
                            <th>${__("Confidence")}</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${files.map((file) => `
                            <tr>
                                <td>
                                    <div class="opening-file-name">${frappe.utils.escape_html(file.file_name || "")}</div>
                                    <div class="opening-file-path">${frappe.utils.escape_html(file.reason || "")}</div>
                                </td>
                                <td>${opening_type_chip(file.migration_type || "unknown")}</td>
                                <td>${opening_handler_chip(file.handler || "ignored")}</td>
                                <td>${frappe.utils.escape_html(String(file.row_count || ""))}</td>
                                <td>${opening_confidence(file.confidence || 0)}</td>
                            </tr>
                        `).join("")}
                    </tbody>
                </table>
            </div>
        </section>
    `;
}

function opening_type_chip(type) {
    const map = {
        account_balance: [__("Account Balance"), "blue"],
        customer_balance: [__("Customer Balance"), "green"],
        supplier_balance: [__("Supplier Balance"), "amber"],
        employee_balance: [__("Employee Balance"), "slate"],
        bank_balance: [__("Bank"), "blue"],
        sales_invoice: [__("Sales"), "green"],
        purchase_invoice: [__("Purchase"), "amber"],
        stock_detail: [__("Stock"), "violet"],
        fixed_asset: [__("Fixed Assets"), "slate"],
        tools: [__("CCDC"), "slate"],
        prepaid: [__("CPTT"), "slate"],
        gl_detail: [__("Detail Ledger"), "slate"],
        unknown: [__("Unknown"), "red"],
    };
    const [label, tone] = map[type] || [type, "slate"];
    return `<span class="opening-mini-chip opening-mini-chip--${tone}">${frappe.utils.escape_html(label)}</span>`;
}

function opening_handler_chip(handler) {
    const map = {
        opening_journal: [__("Opening JE"), "blue"],
        sales_invoice: [__("Sales Invoice"), "green"],
        purchase_invoice: [__("Purchase Invoice"), "amber"],
        stock_reconciliation: [__("Stock Reco"), "violet"],
        ai_journal: [__("AI Plan"), "teal"],
        preview_only: [__("Preview"), "slate"],
        ignored: [__("Ignored"), "red"],
    };
    const [label, tone] = map[handler] || [handler, "slate"];
    return `<span class="opening-mini-chip opening-mini-chip--${tone}">${frappe.utils.escape_html(label)}</span>`;
}

function opening_confidence(value) {
    const confidence = Math.max(0, Math.min(100, Number(value || 0)));
    const tone = confidence >= 85 ? "ok" : confidence >= 60 ? "warn" : "danger";
    return `
        <div class="opening-confidence">
            <div class="opening-confidence__bar">
                <span class="opening-confidence__fill opening-confidence__fill--${tone}" style="width: ${confidence}%"></span>
            </div>
            <b>${confidence}%</b>
        </div>
    `;
}

function render_imported_summary(imported) {
    const entries = Object.entries(imported || {}).filter(([key]) => key !== "total_created");
    if (!entries.length) return "";
    return `
        <section class="opening-import-summary">
            <div class="opening-import-panel__head">
                <div>
                    <b>${__("Import Results")}</b>
                    <span>${__("Documents created from this screen")}</span>
                </div>
            </div>
            <div class="opening-result-grid">
                ${entries.map(([key, value]) => `
                    <div class="opening-result-item">
                        <span>${frappe.utils.escape_html(opening_result_label(key))}</span>
                        <b>${frappe.utils.escape_html(String(value && value.created || value || 0))}</b>
                        ${value && value.failed ? `<small>${__("Errors")}: ${frappe.utils.escape_html(String(value.failed))}</small>` : ""}
                    </div>
                `).join("")}
            </div>
        </section>
    `;
}

function opening_result_label(key) {
    return {
        opening_balance_import: __("Opening JE"),
        ai_journal: __("AI Journal"),
        opening_stock: __("Opening Stock"),
        sales_invoice: __("Sales Invoices"),
        purchase_invoice: __("Purchase Invoices"),
    }[key] || key;
}

function open_opening_plan_dialog(frm) {
    if (frm.doc.__islocal || frm.is_dirty()) {
        frm.save().then(() => open_opening_plan_dialog(frm));
        return;
    }

    frappe.call({
        method: `${OPENING_IMPORT_API}.preview_migration`,
        args: { docname: frm.doc.name },
        freeze: true,
        freeze_message: __("Building plan..."),
    }).then((response) => {
        const preview = response.message || {};
        const dialog = new frappe.ui.Dialog({
            title: __("Opening Balance Import Plan"),
            size: "extra-large",
            fields: [{
                fieldtype: "HTML",
                fieldname: "preview_html",
                options: `${opening_import_styles()}${render_opening_preview(preview)}`,
            }],
            primary_action_label: __("Close"),
            primary_action() {
                dialog.hide();
            },
        });
        dialog.show();
    });
}

function render_opening_preview(preview) {
    const journal = preview.opening_journal || {};
    const invoices = preview.invoices || {};
    const stock = preview.stock_opening || {};
    const kpi = preview.file_kpis || {};
    const missing = Array.isArray(journal.missing_links) ? journal.missing_links : [];
    const files = Array.isArray(preview.files) ? preview.files : [];
    const errors = Array.isArray(preview.errors) ? preview.errors : [];
    const stock_errors = Array.isArray(stock.errors) ? stock.errors : [];
    const stock_hard_errors = stock_errors.filter((e) => (e.severity || "error") !== "warning");
    const stock_warnings = stock_errors.filter((e) => e.severity === "warning");
    const diff = Number(journal.difference || 0);
    const has_kpi = kpi.revenue || kpi.expenses || kpi.ar || kpi.ap;

    return `
        <div class="opening-import-shell opening-import-shell--dialog">
            <section class="opening-import-stats opening-import-stats--dialog">
                ${opening_stat_card(__("JE Rows"), journal.row_count || 0, __("Expected accounting rows"), "journal")}
                ${opening_stat_card(__("Total Debit"), format_opening_money(journal.total_debit), __("Opening Journal Entry"), "debit")}
                ${opening_stat_card(__("Total Credit"), format_opening_money(journal.total_credit), __("Opening Journal Entry"), "credit")}
                ${opening_stat_card(__("Difference"), format_opening_money(diff), Math.abs(diff) < 0.5 ? __("Balanced") : __("Needs Review"), "balance")}
                ${opening_stat_card(__("Stock"), stock.row_count || 0, __("Stock Reconciliation rows"), "stock")}
                ${opening_stat_card(__("Stock Value"), format_opening_money(stock.total_value), __("GL into stock account"), "debit")}
                ${opening_stat_card(__("Sales Invoice"), (invoices.sales_invoice && invoices.sales_invoice.invoice_count) || 0, __("Sales Invoices"), "receipt")}
                ${opening_stat_card(__("Purchase Invoice"), (invoices.purchase_invoice && invoices.purchase_invoice.invoice_count) || 0, __("Purchase Invoices"), "receipt")}
            </section>
            ${has_kpi ? `
            <div class="opening-import-section-label">${__("Tổng hợp từ file đang import")}</div>
            <section class="opening-import-stats opening-import-stats--dialog opening-import-stats--kpi">
                ${opening_stat_card(__("Tổng Doanh Thu"), format_opening_money(kpi.revenue || 0), __("Tổng tiền HĐ bán ra (file)"), "receipt")}
                ${opening_stat_card(__("Tổng Doanh Số Mua"), format_opening_money(kpi.expenses || 0), __("Tổng tiền HĐ mua vào (file)"), "debit")}
                ${opening_stat_card(__("Công Nợ Phải Thu"), format_opening_money(kpi.ar || 0), __("Dư Nợ file công nợ KH"), "credit")}
                ${opening_stat_card(__("Công Nợ Phải Trả"), format_opening_money(kpi.ap || 0), __("Dư Có file công nợ NCC"), "balance")}
            </section>` : ""}
            ${errors.length ? render_opening_list(__("Preview Errors"), errors.map((e) => e.message || e), "danger") : ""}
            ${missing.length ? render_opening_list(__("Missing Mapping"), missing.map((m) => `${m.type}: ${m.value} (${m.source || ""} ${__("row")} ${m.source_row || ""})`), "warn") : ""}
            ${render_stock_opening_preview(stock)}
            ${stock_hard_errors.length ? render_opening_list(__("Opening Stock Errors"), stock_hard_errors.map((e) => `${e.item_code || ""} ${e.warehouse || ""}: ${e.error || ""} (${__("row")} ${e.source_row || ""})`), "danger") : ""}
            ${stock_warnings.length ? render_opening_list(__("Opening Stock Warnings"), stock_warnings.map((e) => `${e.item_code || ""} ${e.warehouse || ""}: ${e.error || ""} (${__("row")} ${e.source_row || ""})`), "warn") : ""}
            ${render_analysis_files(files)}
        </div>
    `;
}

function render_stock_opening_preview(stock) {
    if (!stock || !stock.found) return "";
    return `
        <section class="opening-import-panel opening-import-panel--plain">
            <div class="opening-import-panel__head">
                <div>
                    <b>${__("Opening Stock")}</b>
                    <span>${frappe.utils.escape_html(stock.note || __("Use Stock Reconciliation to update Stock Ledger and stock GL."))}</span>
                </div>
                <span class="opening-panel-count">${frappe.utils.escape_html(String(stock.row_count || 0))}</span>
            </div>
            <div class="opening-result-grid">
                <div class="opening-result-item">
                    <span>${__("Stock Value")}</span>
                    <b>${frappe.utils.escape_html(format_opening_money(stock.total_value))}</b>
                    <small>${__("Stock Account")}: ${frappe.utils.escape_html((stock.stock_accounts || []).join(", ") || "1561")}</small>
                </div>
                <div class="opening-result-item">
                    <span>${__("Stock Account Balance")}</span>
                    <b>${frappe.utils.escape_html(format_opening_money(stock.account_balance_stock_value))}</b>
                    <small>${__("Difference")}: ${frappe.utils.escape_html(format_opening_money(stock.balance_difference))}</small>
                </div>
                <div class="opening-result-item">
                    <span>${__("Missing Items")}</span>
                    <b>${frappe.utils.escape_html(String(stock.missing_items || 0))}</b>
                    <small>${__("Minimal records will be created after user confirmation")}</small>
                </div>
                <div class="opening-result-item">
                    <span>${__("Missing Warehouses")}</span>
                    <b>${frappe.utils.escape_html(String(stock.missing_warehouses || 0))}</b>
                    <small>${__("Assign stock account for correct GL posting")}</small>
                </div>
                <div class="opening-result-item">
                    <span>${__("Offset")}</span>
                    <b>${frappe.utils.escape_html(stock.stock_adjustment_account || "—")}</b>
                    <small>${__("Temporary Opening")}</small>
                </div>
            </div>
        </section>
    `;
}

function render_opening_list(title, rows, tone) {
    return `
        <section class="opening-import-panel opening-import-panel--${tone || "plain"}">
            <div class="opening-import-panel__head">
                <div>
                    <b>${frappe.utils.escape_html(title)}</b>
                    <span>${frappe.utils.escape_html(String((rows || []).length))}</span>
                </div>
            </div>
            ${(rows || []).slice(0, 80).map((row) => `<div class="opening-import-line">${frappe.utils.escape_html(String(row))}</div>`).join("")}
        </section>
    `;
}

function render_opening_confirm_card(config) {
    const stats = Array.isArray(config.stats) ? config.stats : [];
    return `
        <div class="opening-process-confirm opening-process-confirm--${frappe.utils.escape_html(config.tone || "plain")}">
            <div class="opening-process-confirm__icon">${icon_svg(config.icon || "journal")}</div>
            <div class="opening-process-confirm__body">
                <div class="opening-process-confirm__eyebrow">${frappe.utils.escape_html(config.eyebrow || "")}</div>
                <div class="opening-process-confirm__title">${frappe.utils.escape_html(config.title || "")}</div>
                <div class="opening-process-confirm__message">${frappe.utils.escape_html(config.message || "")}</div>
                ${stats.length ? `
                    <div class="opening-process-confirm__stats">
                        ${stats.map((item) => `
                            <div>
                                <span>${frappe.utils.escape_html(item.label || "")}</span>
                                <b>${frappe.utils.escape_html(opening_display_value(item.value))}</b>
                            </div>
                        `).join("")}
                    </div>
                ` : ""}
            </div>
        </div>
    `;
}

function render_opening_master_plan(master_plan) {
    const buckets = [
        { key: "customers", label: __("Customer"), data: master_plan.customers || {} },
        { key: "suppliers", label: __("Supplier"), data: master_plan.suppliers || {} },
        { key: "employees", label: __("Employee"), data: master_plan.employees || {} },
    ].filter((item) => Number(item.data.missing || 0));

    if (!buckets.length) {
        return `
            <section class="opening-import-empty">
                <div class="opening-import-empty__icon">${icon_svg("created")}</div>
                <div>
                    <b>${__("No Missing Masters")}</b>
                    <span>${__("Customer, Supplier, and Employee are ready for opening import.")}</span>
                </div>
            </section>
        `;
    }

    return `
        <section class="opening-import-panel opening-import-panel--warn">
            <div class="opening-import-panel__head">
                <div>
                    <b>${__("Masters Created After Confirmation")}</b>
                    <span>${__("Only minimal data is created; users complete details later.")}</span>
                </div>
                <span class="opening-panel-count">${frappe.utils.escape_html(String(master_plan.missing || 0))}</span>
            </div>
            <div class="opening-result-grid">
                ${buckets.map((item) => `
                    <div class="opening-result-item">
                        <span>${frappe.utils.escape_html(item.label)}</span>
                        <b>${frappe.utils.escape_html(String(item.data.missing || 0))}</b>
                        <small>${__("Existing")}: ${frappe.utils.escape_html(String(item.data.existing || 0))}</small>
                    </div>
                `).join("")}
            </div>
            ${buckets.map((item) => `
                <div class="opening-master-preview">
                    <b>${frappe.utils.escape_html(item.label)}</b>
                    ${(item.data.records || []).slice(0, 8).map((row) => `
                        <div class="opening-import-line">
                            ${frappe.utils.escape_html(row.code || "—")} ·
                            ${frappe.utils.escape_html(row.label || "")}
                            ${row.source_row ? ` · ${__("row")} ${frappe.utils.escape_html(String(row.source_row))}` : ""}
                        </div>
                    `).join("")}
                    ${(item.data.records || []).length > 8 ? `<small>${__("+ {0} more rows", [(item.data.records || []).length - 8])}</small>` : ""}
                </div>
            `).join("")}
        </section>
    `;
}

function opening_process_config(kind, frm, values = {}) {
    const company = frm.doc.company || __("Default Company");
    const folder = frm.doc.folder_path || "";
    const analysis = parse_opening_json(frm.doc.analysis_json, {});
    const file_count = Array.isArray(analysis.files) ? analysis.files.length : 0;
    const draft_or_submit = values.submit ? __("Submit") : __("Draft");
    const force_label = values.force ? __("Allow Duplicate Creation") : __("Prevent Duplicates");

    const common = {
        kind,
        company,
        file_name: folder,
        stats: [
            { label: __("Company"), value: company },
            { label: __("Status"), value: frm.doc.status || __("Draft") },
            { label: __("Source"), value: file_count ? `${file_count} ${__("files")}` : __("Data Folder") },
        ],
        stages: [
            __("Read Files"),
            __("Normalize"),
            __("Reconcile"),
            __("Write Data"),
            __("Summarize"),
        ],
        messages: [
            __("Rereading Excel for latest data."),
            __("Normalizing amounts, dates, and master links."),
            __("Running fixed Python handlers; AI does not write data."),
            __("Large files may take a few minutes; the server job continues."),
        ],
    };

    if (kind === "analyze") {
        return {
            ...common,
            title: __("AI Analyzing Opening Files"),
            eyebrow: __("AI classification"),
            message: __("AI only identifies file type, headers, and handlers; import data is handled by Python."),
            icon: "sparkles",
            stats: [
                { label: __("Company"), value: company },
                { label: __("Scope"), value: frm.doc.recursive ? __("Include Subfolders") : __("Current Folder") },
                { label: __("Source"), value: folder || __("Not Set") },
            ],
            stages: [__("Scan Files"), __("Read Samples"), __("AI Classify"), __("Match Local Rules"), __("Save Review List")],
        };
    }

    if (kind === "master") {
        const master_plan = analysis.master_plan || analysis.auto_master || {};
        return {
            ...common,
            title: __("Creating Missing Masters"),
            eyebrow: __("User confirmed"),
            message: __("Creating minimal Customer, Supplier, and Employee records from analysis."),
            icon: "users",
            stats: [
                { label: __("Missing"), value: master_plan.missing || 0 },
                { label: __("Customer"), value: master_plan.customers && master_plan.customers.missing || 0 },
                { label: __("Supplier/Employee"), value: `${master_plan.suppliers && master_plan.suppliers.missing || 0}/${master_plan.employees && master_plan.employees.missing || 0}` },
            ],
            stages: [__("Read Missing List"), __("Create Customer"), __("Create Supplier"), __("Create Employee"), __("Update Result")],
        };
    }

    if (kind === "journal") {
        return {
            ...common,
            title: __("Creating Opening Journal Entry"),
            eyebrow: __("Python Import Script"),
            message: __("Combining account, party, and bank balances into an opening journal entry."),
            icon: "journal",
            stats: [
                { label: __("Posting Date"), value: values.posting_date || frm.doc.posting_date || "2026-01-01" },
                { label: __("Mode"), value: draft_or_submit },
                { label: __("Difference"), value: values.allow_difference ? __("Allow") : __("Block") },
            ],
        };
    }

    if (kind === "ai_journal") {
        const ai_count = Array.isArray(analysis.files)
            ? analysis.files.filter((f) => f.handler === "ai_journal").length
            : 0;
        return {
            ...common,
            title: __("Creating AI-Planned Journal Entries"),
            eyebrow: __("AI Column Plan"),
            message: __("Creates one Opening Journal Entry per file where AI has identified debit/credit accounts and the amount column."),
            icon: "journal",
            stats: [
                { label: __("Files"), value: ai_count },
                { label: __("Posting Date"), value: values.posting_date || frm.doc.posting_date || "2026-01-01" },
                { label: __("Mode"), value: draft_or_submit },
            ],
            stages: [__("Read AI Plans"), __("Resolve Accounts"), __("Read Rows"), __("Write JE"), __("Summarize")],
        };
    }

    if (kind === "stock") {
        return {
            ...common,
            title: __("Importing Opening Stock"),
            eyebrow: __("Stock Reconciliation"),
            message: __("Creating Stock Reconciliation to post stock and GL into stock accounts such as 1561."),
            icon: "stock",
            stats: [
                { label: __("Posting Date"), value: values.posting_date || frm.doc.posting_date || "2026-01-01" },
                { label: __("Mode"), value: draft_or_submit },
                { label: __("Duplicates"), value: force_label },
            ],
            stages: [__("Read Stock Files"), __("Create Missing Items/Warehouses"), __("Assign Stock Accounts"), __("Write Stock Reco"), __("Summarize")],
            messages: [
                __("Reading rows marked as opening balances."),
                __("Ensuring Item, UOM, and Warehouse are available."),
                __("Stock Reconciliation creates GL to stock accounts; Temporary Opening is the offset."),
                __("If submitted immediately, ERPNext updates Stock Ledger and GL now."),
            ],
        };
    }

    const is_sales = kind === "sales_invoice";
    return {
        ...common,
        title: is_sales ? __("Importing Sales Invoices") : __("Importing Purchase Invoices"),
        eyebrow: __("Python Import Script"),
        message: is_sales
            ? __("Grouping sales listing rows into Sales Invoices.")
            : __("Grouping purchase listing rows into Purchase Invoices."),
        icon: "receipt",
        stats: [
            { label: __("Document"), value: is_sales ? __("Sales Invoice") : __("Purchase Invoice") },
            { label: __("Mode"), value: draft_or_submit },
            { label: __("Limit"), value: values.limit ? `${values.limit} ${__("invoices")}` : __("All") },
        ],
        stages: [__("Read Listing"), __("Group Invoices"), __("Create Party"), __("Write Invoice"), __("Summarize")],
    };
}

function open_opening_process_dialog(config) {
    const state = {
        config,
        started_at: Date.now(),
        percent: 8,
        status: "running",
        result: null,
        timer: null,
        dialog: null,
    };
    const dialog = new frappe.ui.Dialog({
        title: config.title || __("Processing"),
        size: "large",
        fields: [
            {
                fieldtype: "HTML",
                fieldname: "body",
                options: `${opening_import_styles()}${render_opening_process_progress(state)}`,
            },
        ],
        primary_action_label: __("Running..."),
        primary_action() {
            if (state.status === "running") return;
            dialog.hide();
            cleanup_opening_modal_state();
        },
    });
    dialog.show();
    dialog.$wrapper.find(".modal-footer .btn-primary").prop("disabled", true).addClass("disabled");
    state.dialog = dialog;
    state.timer = setInterval(() => {
        if (state.status !== "running") return;
        update_opening_process_dialog(state, {
            percent: Math.min(92, state.percent + 7),
        });
    }, 1000);
    return state;
}

function update_opening_process_dialog(state, patch = {}) {
    if (!state || !state.dialog) return;
    Object.assign(state, patch);
    const wrapper = state.dialog.fields_dict && state.dialog.fields_dict.body && state.dialog.fields_dict.body.$wrapper;
    if (wrapper && wrapper.length) {
        wrapper.html(`${opening_import_styles()}${render_opening_process_progress(state)}`);
    }
}

function finish_opening_process_dialog(state, result) {
    if (!state) return;
    if (state.timer) clearInterval(state.timer);
    const has_created = Boolean(
        (result && result.journal_entry)
        || (result && result.stock_reconciliation)
        || (result && Array.isArray(result.files))
        || Number(result && result.created)
    );
    const failed = result && result.ok === false;
    const warning = Boolean(result && result.ai_warning);
    update_opening_process_dialog(state, {
        percent: 100,
        status: failed ? (has_created ? "warning" : "failed") : (warning ? "warning" : "complete"),
        result: result || {},
    });
    if (state.dialog && state.dialog.$wrapper) {
        state.dialog.$wrapper.find(".modal-footer .btn-primary")
            .prop("disabled", false)
            .removeClass("disabled")
            .text(__("Close"));
    }
    frappe.show_alert({
        message: (result && result.message) || (failed ? __("Processing not complete.") : __("Processing complete.")),
        indicator: failed || warning ? "orange" : "green",
    });
}

function render_opening_process_progress(state) {
    const config = state.config || {};
    const percent = Math.max(0, Math.min(100, Math.round(state.percent || 0)));
    const elapsed_seconds = Math.max(0, Math.floor((Date.now() - state.started_at) / 1000));
    const stages = Array.isArray(config.stages) && config.stages.length ? config.stages : [__("Processing")];
    const running_idx = Math.min(stages.length - 1, Math.floor((percent / 100) * stages.length));
    const active_idx = state.status === "complete" || state.status === "warning"
        ? stages.length - 1
        : (state.status === "failed" ? Math.max(0, running_idx - 1) : running_idx);
    const messages = Array.isArray(config.messages) && config.messages.length ? config.messages : [config.message || __("Processing...")];
    const rotating_message = state.status === "running"
        ? messages[Math.floor(elapsed_seconds / 5) % messages.length]
        : opening_process_result_message(state.result, state.status);
    const status_label = {
        running: __("Running"),
        complete: __("Complete"),
        warning: __("Partial"),
        failed: __("Error"),
    }[state.status] || __("Running");

    return `
        <div class="opening-process-progress opening-process-progress--${frappe.utils.escape_html(state.status)}">
            <div class="opening-process-progress__head">
                <div class="opening-process-progress__icon">
                    ${opening_process_status_icon(state.status, config.icon)}
                </div>
                <div class="opening-process-progress__body">
                    <div class="opening-process-progress__eyebrow">${frappe.utils.escape_html(config.eyebrow || "")}</div>
                    <div class="opening-process-progress__title">${frappe.utils.escape_html(config.message || config.title || "")}</div>
                    ${config.file_name ? `<div class="opening-process-progress__file">${frappe.utils.escape_html(config.file_name)}</div>` : ""}
                </div>
                <div class="opening-process-progress__live">
                    <span class="opening-process-progress__live-dot"></span>
                    ${frappe.utils.escape_html(status_label)}
                </div>
            </div>

            <div class="opening-process-progress__bar">
                <div class="opening-process-progress__bar-fill" style="width:${state.status === "running" ? Math.max(percent, 18) : percent}%"></div>
            </div>

            <div class="opening-process-progress__stats">
                <div class="opening-process-stat">
                    <span>${__("Time")}</span>
                    <b>${frappe.utils.escape_html(format_opening_elapsed_time(elapsed_seconds))}</b>
                </div>
                ${(config.stats || []).slice(0, 3).map((item) => `
                    <div class="opening-process-stat">
                        <span>${frappe.utils.escape_html(item.label || "")}</span>
                        <b>${frappe.utils.escape_html(opening_display_value(item.value))}</b>
                    </div>
                `).join("")}
            </div>

            <div class="opening-process-progress__message">
                <span class="opening-process-progress__message-dot"></span>
                <span>${frappe.utils.escape_html(rotating_message || "")}</span>
            </div>

            <div class="opening-process-stages">
                ${stages.map((label, index) => `
                    <div class="opening-process-stage ${index <= active_idx ? "is-active" : ""} ${state.status === "running" && index === active_idx ? "is-current" : ""}">
                        <span class="opening-process-stage__dot"></span>
                        <span class="opening-process-stage__label">${frappe.utils.escape_html(label)}</span>
                    </div>
                `).join("")}
            </div>

            ${state.result ? render_opening_process_result(state.result, state.status) : ""}
        </div>
    `;
}

function opening_process_status_icon(status, icon) {
    if (status === "complete") return icon_svg("created");
    if (status === "warning") return icon_svg("handler");
    if (status === "failed") return '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18 6L6 18"/><path d="M6 6l12 12"/></svg>';
    return `<div class="opening-spinner"></div>`;
}

function opening_process_result_message(result, status) {
    if (!result) return "";
    if (result.message) return result.message;
    if (result.ai_warning) return result.ai_warning;
    if (status === "failed") return __("An error occurred during processing.");
    if (result.journal_entry) return __("Opening Journal Entry created.");
    if (result.stock_reconciliation) return __("Opening Stock Reconciliation created.");
    if (Array.isArray(result.files)) return __("File analysis result saved.");
    if (result.mode === "create_masters") return __("Missing masters processed.");
    if (Object.prototype.hasOwnProperty.call(result, "created")) {
        return __("Invoice import completed.");
    }
    return __("Processing complete.");
}

function render_opening_process_result(result, status) {
    const stats = opening_process_result_stats(result);
    const errors = Array.isArray(result && result.errors) ? result.errors : [];
    return `
        <div class="opening-process-result opening-process-result--${frappe.utils.escape_html(status || "complete")}">
            <div class="opening-process-result__head">
                <b>${status === "failed" ? __("Needs Review") : (status === "warning" ? __("Completed with Fallback") : __("Processing Result"))}</b>
                <span>${frappe.utils.escape_html(opening_process_result_message(result, status))}</span>
            </div>
            ${stats.length ? `
                <div class="opening-process-result__stats">
                    ${stats.map((item) => `
                        <div>
                            <span>${frappe.utils.escape_html(item.label)}</span>
                            <b>${frappe.utils.escape_html(String(item.value))}</b>
                        </div>
                    `).join("")}
                </div>
            ` : ""}
            ${errors.length ? `
                <div class="opening-process-result__errors">
                    ${errors.slice(0, 6).map((item) => `
                        <div>${frappe.utils.escape_html(String(item.error || item.message || item))}</div>
                    `).join("")}
                    ${errors.length > 6 ? `<small>${__("+ {0} more errors", [errors.length - 6])}</small>` : ""}
                </div>
            ` : ""}
        </div>
    `;
}

function opening_process_result_stats(result) {
    if (!result || typeof result !== "object") return [];
    if (Array.isArray(result.files)) {
        const master_plan = result.master_plan || result.auto_master || {};
        return [
            { label: __("File"), value: result.files.length },
            { label: __("AI"), value: result.ai_used ? __("Used") : __("Local Rule") },
            { label: __("Missing Masters"), value: master_plan.missing || 0 },
            { label: __("Company"), value: result.company || "—" },
        ];
    }
    if (result.journal_entry) {
        return [
            { label: __("Journal Entry"), value: result.journal_entry },
            { label: __("Rows"), value: result.rows || 0 },
            { label: __("Docstatus"), value: result.submitted ? __("Submitted") : __("Draft") },
        ];
    }
    if (result.stock_reconciliation) {
        return [
            { label: __("Stock Reco"), value: result.stock_reconciliation },
            { label: __("Rows"), value: result.rows || 0 },
            { label: __("Value"), value: format_opening_money(result.total_value) },
            { label: __("Stock Account Difference"), value: format_opening_money(result.balance_difference) },
            { label: __("Docstatus"), value: result.submitted ? __("Submitted") : __("Draft") },
        ];
    }
    if (result.mode === "create_masters") {
        const banks = result.banks || {};
        return [
            { label: __("Created"), value: result.created || 0 },
            { label: __("Existing"), value: result.existing || 0 },
            { label: __("Errors"), value: result.failed || 0 },
            { label: __("Bank Created"), value: banks.created || 0 },
            { label: __("Bank Existing"), value: banks.existing || 0 },
            { label: __("Bank Errors"), value: banks.failed || 0 },
        ];
    }
    if (Object.prototype.hasOwnProperty.call(result, "created")) {
        return [
            { label: __("Created"), value: result.created || 0 },
            { label: __("Skipped"), value: result.skipped || 0 },
            { label: __("Errors"), value: result.failed || 0 },
        ];
    }
    return [];
}

function confirm_create_missing_masters(frm) {
    const analysis = parse_opening_json(frm.doc.analysis_json, {});
    const master_plan = analysis.master_plan || analysis.auto_master || {};
    const missing = Number(master_plan.missing || 0);

    if (!missing) {
        frappe.msgprint({
            title: __("No Missing Masters"),
            message: __("Customer, Supplier, and Employee are no longer missing in the current analysis."),
            indicator: "green",
        });
        return;
    }

    const dialog = new frappe.ui.Dialog({
        title: __("Create Missing Masters"),
        size: "large",
        fields: [
            {
                fieldtype: "HTML",
                fieldname: "confirm_html",
                options: `${opening_import_styles()}${render_opening_confirm_card({
                    eyebrow: __("Confirmation Required"),
                    title: __("Create Minimal Customer/Supplier/Employee/Bank Account"),
                    message: __("These records are only enough for opening balance and invoice import; users complete details later."),
                    tone: "master",
                    icon: "users",
                    stats: [
                        { label: __("Missing"), value: missing },
                        { label: __("Customer"), value: master_plan.customers && master_plan.customers.missing || 0 },
                        { label: __("Supplier"), value: master_plan.suppliers && master_plan.suppliers.missing || 0 },
                        { label: __("Employee"), value: master_plan.employees && master_plan.employees.missing || 0 },
                        { label: __("Bank Account"), value: master_plan.banks && master_plan.banks.missing || 0 },
                    ],
                })}${render_opening_master_plan(master_plan)}`,
            },
        ],
        primary_action_label: __("Confirm Create"),
        primary_action() {
            dialog.hide();
            setTimeout(() => {
                run_opening_action(
                    frm,
                    "create_missing_masters",
                    __("Creating missing masters..."),
                    {},
                    opening_process_config("master", frm)
                );
            }, 120);
        },
    });
    dialog.show();
}

function confirm_ai_journal(frm) {
    const analysis = parse_opening_json(frm.doc.analysis_json, {});
    const ai_files = Array.isArray(analysis.files)
        ? analysis.files.filter((f) => f.handler === "ai_journal")
        : [];

    if (!ai_files.length) {
        frappe.msgprint({
            title: __("No AI Plans Found"),
            message: __("Re-run AI Analyze Files — no files have an AI-generated column plan yet."),
            indicator: "orange",
        });
        return;
    }

    const file_list = ai_files
        .slice(0, 8)
        .map((f) => {
            const plan = f.column_plan || {};
            const note = plan.note
                ? ` <span class="text-muted">(${frappe.utils.escape_html(plan.note)})</span>`
                : "";
            const mapping = plan.debit_account && plan.amount_col
                ? ` — Nợ ${frappe.utils.escape_html(plan.debit_account)} / Có ${frappe.utils.escape_html(plan.credit_account || "?")} · ${frappe.utils.escape_html(plan.amount_col)}`
                : "";
            return `<li><b>${frappe.utils.escape_html(f.file_name || "")}</b>${mapping}${note}</li>`;
        })
        .join("");

    const dialog = new frappe.ui.Dialog({
        title: __("Create AI-Planned Journal Entries"),
        size: "large",
        fields: [
            {
                fieldtype: "HTML",
                fieldname: "info_html",
                options: `${opening_import_styles()}
                    <div class="opening-import-confirm-card" style="margin-bottom:12px">
                        <div style="font-size:11px;font-weight:600;color:var(--text-muted);margin-bottom:4px">${__("AI Column Plan")}</div>
                        <div style="font-size:14px;font-weight:600;margin-bottom:8px">${__("{0} file(s) will generate Opening Journal Entries", [ai_files.length])}</div>
                        <div style="font-size:12px;color:var(--text-muted);margin-bottom:10px">
                            ${__("The AI identified debit/credit account numbers and amount columns from each file. Python reads the rows and creates one Opening Entry per file.")}
                        </div>
                        <ul style="margin:0;padding-left:16px;font-size:12px">${file_list}</ul>
                    </div>`,
            },
            { fieldtype: "Date", fieldname: "posting_date", label: __("Posting Date"), default: frm.doc.posting_date || "2026-01-01", reqd: 1 },
            { fieldtype: "Check", fieldname: "submit", label: __("Submit Immediately"), default: 0 },
        ],
        primary_action_label: __("Create JE"),
        primary_action(values) {
            dialog.hide();
            setTimeout(() => {
                run_opening_action(frm, "execute_ai_journal", __("Creating AI Journal Entries..."), {
                    posting_date: values.posting_date,
                    submit: values.submit ? 1 : 0,
                    force: 0,
                }, opening_process_config("ai_journal", frm, values));
            }, 120);
        },
    });
    dialog.show();
}

function confirm_opening_journal(frm) {
    const dialog = new frappe.ui.Dialog({
        title: __("Create Opening Journal Entry"),
        size: "large",
        fields: [
            {
                fieldtype: "HTML",
                fieldname: "confirm_html",
                options: `${opening_import_styles()}${render_opening_confirm_card({
                    eyebrow: __("Python hardcode"),
                    title: __("Create Opening Balance Document"),
                    message: __("The system rereads balance files, matches accounts/parties/banks, then creates an Opening Journal Entry."),
                    tone: "journal",
                    icon: "journal",
                    stats: [
                        { label: __("Company"), value: frm.doc.company || __("Default") },
                        { label: __("Posting Date"), value: frm.doc.posting_date || "2026-01-01" },
                        { label: __("Result"), value: __("Journal Entry draft") },
                    ],
                })}`,
            },
            { fieldtype: "Date", fieldname: "posting_date", label: __("Posting Date"), default: frm.doc.posting_date || "2026-01-01", reqd: 1 },
            { fieldtype: "Check", fieldname: "submit", label: __("Submit Immediately"), default: 0 },
            { fieldtype: "Check", fieldname: "force", label: __("Allow creating if Opening Entry exists"), default: 0 },
            { fieldtype: "Section Break", fieldname: "balance_section", label: __("Chênh lệch / Balance") },
            {
                fieldtype: "Link",
                fieldname: "balance_account",
                label: __("TK bù chênh lệch (nếu file số dư không cân)"),
                options: "Account",
                description: __("Nếu Tổng Nợ ≠ Tổng Có, hệ thống sẽ tự động thêm 1 dòng bù vào tài khoản này. Thường dùng TK 421 (Lợi nhuận chưa phân phối) hoặc TK 411 (Vốn chủ sở hữu). Để trống nếu muốn hệ thống báo lỗi khi không cân."),
                get_query() {
                    return { filters: { company: frm.doc.company, is_group: 0 } };
                },
            },
        ],
        primary_action_label: __("Create"),
        primary_action(values) {
            dialog.hide();
            setTimeout(() => {
                run_opening_action(frm, "execute_opening_journal", __("Creating Opening Journal Entry..."), {
                    posting_date: values.posting_date,
                    submit: values.submit ? 1 : 0,
                    force: values.force ? 1 : 0,
                    balance_account: values.balance_account || "",
                }, opening_process_config("journal", frm, values));
            }, 120);
        },
    });
    dialog.show();
}

function confirm_opening_stock(frm) {
    const dialog = new frappe.ui.Dialog({
        title: __("Import Opening Stock"),
        size: "large",
        fields: [
            {
                fieldtype: "HTML",
                fieldname: "confirm_html",
                options: `${opening_import_styles()}${render_opening_confirm_card({
                    eyebrow: __("Stock Reconciliation"),
                    title: __("Post Stock and GL to Stock Account"),
                    message: __("ERPNext does not allow Journal Entry directly to Stock accounts; this step uses Stock Reconciliation."),
                    tone: "stock",
                    icon: "stock",
                    stats: [
                        { label: __("Company"), value: frm.doc.company || __("Default") },
                        { label: __("Posting Date"), value: frm.doc.posting_date || "2026-01-01" },
                        { label: __("Result"), value: __("Stock Reconciliation draft") },
                    ],
                })}`,
            },
            { fieldtype: "Date", fieldname: "posting_date", label: __("Posting Date"), default: frm.doc.posting_date || "2026-01-01", reqd: 1 },
            { fieldtype: "Check", fieldname: "submit", label: __("Submit Immediately"), default: 0 },
            { fieldtype: "Check", fieldname: "force", label: __("Allow creating if same-source Stock Reconciliation exists"), default: 0 },
            { fieldtype: "Check", fieldname: "allow_difference", label: __("Allow stock account balance difference"), default: 0 },
            { fieldtype: "Int", fieldname: "limit", label: __("Test Row Limit"), default: 0 },
        ],
        primary_action_label: __("Create Stock Reco"),
        primary_action(values) {
            const limit = cint(values.limit || 0);
            dialog.hide();
            setTimeout(() => {
                run_opening_action(frm, "execute_opening_stock", __("Importing opening stock..."), {
                    posting_date: values.posting_date,
                    submit: values.submit ? 1 : 0,
                    force: values.force ? 1 : 0,
                    allow_difference: values.allow_difference ? 1 : 0,
                    limit: limit > 0 ? limit : null,
                }, opening_process_config("stock", frm, values));
            }, 120);
        },
    });
    dialog.show();
}

function confirm_invoice_import(frm, invoice_type) {
    const label = invoice_type === "sales_invoice" ? __("sales invoices") : __("purchase invoices");
    const dialog = new frappe.ui.Dialog({
        title: __("Import {0}", [label]),
        size: "large",
        fields: [
            {
                fieldtype: "HTML",
                fieldname: "confirm_html",
                options: `${opening_import_styles()}${render_opening_confirm_card({
                    eyebrow: __("Python hardcode"),
                    title: invoice_type === "sales_invoice"
                        ? __("Import Opening Sales Invoices")
                        : __("Import Opening Purchase Invoices"),
                    message: __("The system groups rows by invoice/document number and creates invoice drafts using confirmed masters."),
                    tone: invoice_type === "sales_invoice" ? "sales" : "purchase",
                    icon: "receipt",
                    stats: [
                        { label: __("Company"), value: frm.doc.company || __("Default") },
                        { label: __("Mode"), value: __("Draft") },
                        { label: __("Source"), value: invoice_type === "sales_invoice" ? __("Sales Listing") : __("Purchase Listing") },
                    ],
                })}`,
            },
            { fieldtype: "Check", fieldname: "submit", label: __("Submit Immediately"), default: 0 },
            { fieldtype: "Check", fieldname: "force", label: __("Allow creating if same-source documents exist"), default: 0 },
            { fieldtype: "Int", fieldname: "limit", label: __("Test Invoice Limit"), default: 0 },
        ],
        primary_action_label: __("Import Draft"),
        primary_action(values) {
            const limit = cint(values.limit || 0);
            dialog.hide();
            setTimeout(() => {
                run_opening_action(frm, "execute_invoices", __("Importing invoices..."), {
                    invoice_type,
                    submit: values.submit ? 1 : 0,
                    force: values.force ? 1 : 0,
                    limit: limit > 0 ? limit : null,
                }, opening_process_config(invoice_type, frm, values));
            }, 120);
        },
    });
    dialog.show();
}

function format_opening_money(value) {
    const number = Number(value || 0);
    return number.toLocaleString("vi-VN", { maximumFractionDigits: 0 });
}

function opening_display_value(value) {
    return value === undefined || value === null || value === "" ? "—" : String(value);
}

function format_opening_elapsed_time(total_seconds) {
    const minutes = Math.floor(total_seconds / 60);
    const seconds = total_seconds % 60;
    return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}

function opening_call_error_message(error) {
    if (!error) {
        return __("Connection interrupted or server returned an error.");
    }

    const messages = [];
    const push_message = (value) => {
        if (!value) return;
        const text = strip_opening_html(String(value)).trim();
        if (text && !messages.includes(text) && text !== "EXPECTATION FAILED") {
            messages.push(text);
        }
    };
    const parse_server_messages = (value) => {
        if (!value) return;
        try {
            const parsed = typeof value === "string" ? JSON.parse(value) : value;
            (Array.isArray(parsed) ? parsed : [parsed]).forEach((item) => {
                try {
                    const message = typeof item === "string" ? JSON.parse(item) : item;
                    push_message(message && (message.message || message.title || message));
                } catch (inner_error) {
                    push_message(item);
                }
            });
        } catch (parse_error) {
            push_message(value);
        }
    };

    parse_server_messages(error._server_messages);
    parse_server_messages(error.server_messages);

    const response_json = error.responseJSON || error.response_json || {};
    parse_server_messages(response_json._server_messages);
    parse_server_messages(response_json.server_messages);
    push_message(response_json.message);
    push_message(response_json.exception);

    if (error.responseText) {
        try {
            const parsed = JSON.parse(error.responseText);
            parse_server_messages(parsed._server_messages);
            push_message(parsed.message);
            push_message(parsed.exception);
        } catch (parse_error) {
            push_message(error.responseText);
        }
    }

    push_message(error.message);
    push_message(error.exc);
    push_message(error.statusText);

    return messages[0] || __("Connection interrupted or server returned an error.");
}

function strip_opening_html(value) {
    return String(value || "")
        .replace(/<br\s*\/?\s*>/gi, "\n")
        .replace(/<[^>]*>/g, "")
        .replace(/&nbsp;/g, " ")
        .replace(/&amp;/g, "&")
        .replace(/&lt;/g, "<")
        .replace(/&gt;/g, ">")
        .replace(/&quot;/g, '"')
        .replace(/&#39;/g, "'");
}

function cleanup_opening_modal_state(attempt = 0) {
    setTimeout(() => {
        const visible_modals = $(".modal.show:visible, .modal.in:visible").length;
        if (visible_modals) {
            if (attempt < 5) cleanup_opening_modal_state(attempt + 1);
            return;
        }
        $(".modal-backdrop").remove();
        $("body").removeClass("modal-open").css({ overflow: "", "padding-right": "" });
        if (frappe.dom && frappe.dom.unfreeze) {
            frappe.dom.unfreeze();
        }
    }, attempt ? 150 : 350);
}

function icon_svg(name) {
    const icons = {
        sparkles: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l1.6 4.4L18 9l-4.4 1.6L12 15l-1.6-4.4L6 9l4.4-1.6L12 3z"/><path d="M19 14l.8 2.2L22 17l-2.2.8L19 20l-.8-2.2L16 17l2.2-.8L19 14z"/><path d="M5 14l.8 2.2L8 17l-2.2.8L5 20l-.8-2.2L2 17l2.2-.8L5 14z"/></svg>',
        list: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 6h13"/><path d="M8 12h13"/><path d="M8 18h13"/><path d="M3 6h.01"/><path d="M3 12h.01"/><path d="M3 18h.01"/></svg>',
        book: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15z"/></svg>',
        receipt: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 2v20l3-2 3 2 3-2 3 2 4-2V2l-4 2-3-2-3 2-3-2-3 2z"/><path d="M8 8h8"/><path d="M8 12h8"/><path d="M8 16h5"/></svg>',
        folder: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6.5A2.5 2.5 0 0 1 5.5 4H10l2 2h6.5A2.5 2.5 0 0 1 21 8.5v8A2.5 2.5 0 0 1 18.5 19h-13A2.5 2.5 0 0 1 3 16.5v-10z"/></svg>',
        upload: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M17 8l-5-5-5 5"/><path d="M12 3v12"/></svg>',
        "folder-upload": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6.5A2.5 2.5 0 0 1 5.5 4H10l2 2h6.5A2.5 2.5 0 0 1 21 8.5v8A2.5 2.5 0 0 1 18.5 19h-13A2.5 2.5 0 0 1 3 16.5v-10z"/><path d="M12 17v-6"/><path d="M9 14l3-3 3 3"/></svg>',
        file: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/></svg>',
        users: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
        handler: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2v6"/><path d="M12 16v6"/><path d="M4.9 4.9l4.2 4.2"/><path d="M14.9 14.9l4.2 4.2"/><path d="M2 12h6"/><path d="M16 12h6"/><path d="M4.9 19.1l4.2-4.2"/><path d="M14.9 9.1l4.2-4.2"/></svg>',
        journal: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3h12v18H6z"/><path d="M9 7h6"/><path d="M9 11h6"/><path d="M9 15h4"/></svg>',
        invoice: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 3h10a2 2 0 0 1 2 2v16l-3-2-3 2-3-2-3 2V5a2 2 0 0 1 2-2z"/><path d="M9 8h6"/><path d="M9 12h6"/></svg>',
        stock: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 8l-9-5-9 5 9 5 9-5z"/><path d="M3 8v8l9 5 9-5V8"/><path d="M12 13v8"/></svg>',
        created: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>',
        debit: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5"/><path d="M5 12l7 7 7-7"/></svg>',
        credit: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14"/><path d="M5 12l7-7 7 7"/></svg>',
        balance: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v18"/><path d="M5 7h14"/><path d="M6 7l-3 6h6L6 7z"/><path d="M18 7l-3 6h6l-3-6z"/></svg>',
    };
    return icons[name] || icons.file;
}

function opening_import_styles() {
    return `
        <style>
            [data-fieldname="dashboard_html"] { padding: 0 !important; }
            [data-fieldname="dashboard_html"] .form-group { margin-bottom: 0 !important; }
            .opening-import-shell {
                --opening-border: #d8dee8;
                --opening-muted: #64748b;
                --opening-text: #0f172a;
                --opening-soft: #f8fafc;
                --opening-blue: #2563eb;
                --opening-green: #16a34a;
                --opening-amber: #b45309;
                --opening-red: #b91c1c;
                display: flex;
                flex-direction: column;
                gap: 14px;
                padding: 4px 0 18px;
                color: var(--opening-text);
            }
            .opening-import-shell svg {
                width: 16px;
                height: 16px;
                fill: none;
                stroke: currentColor;
                stroke-width: 2;
                stroke-linecap: round;
                stroke-linejoin: round;
                flex-shrink: 0;
            }
            .opening-import-shell--dialog { padding: 0; }
            .opening-import-hero {
                display: flex;
                align-items: stretch;
                justify-content: space-between;
                gap: 16px;
                padding: 18px;
                border: 1px solid var(--opening-border);
                border-radius: 8px;
                background: #fff;
                box-shadow: 0 1px 2px rgba(15, 23, 42, .04);
            }
            .opening-import-hero__main {
                min-width: 0;
                display: flex;
                flex-direction: column;
                gap: 8px;
            }
            .opening-import-hero__meta {
                display: flex;
                flex-wrap: wrap;
                gap: 6px;
            }
            .opening-import-hero__meta span {
                border: 1px solid #e2e8f0;
                border-radius: 999px;
                padding: 3px 8px;
                color: #475569;
                background: #f8fafc;
                font-size: 11px;
                font-weight: 700;
                text-transform: uppercase;
            }
            .opening-import-hero h2 {
                margin: 0;
                color: var(--opening-text);
                font-size: 22px;
                font-weight: 750;
                line-height: 1.25;
                letter-spacing: 0;
            }
            .opening-import-path {
                display: flex;
                align-items: center;
                gap: 7px;
                min-width: 0;
                color: var(--opening-muted);
                font-size: 12px;
            }
            .opening-import-path span {
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }
            .opening-import-hero__side {
                display: flex;
                flex-direction: column;
                align-items: flex-end;
                justify-content: space-between;
                gap: 12px;
                flex-shrink: 0;
            }
            .opening-chip,
            .opening-mini-chip {
                display: inline-flex;
                align-items: center;
                min-height: 24px;
                border-radius: 999px;
                padding: 3px 9px;
                font-size: 12px;
                font-weight: 700;
                white-space: nowrap;
            }
            .opening-chip--neutral, .opening-mini-chip--slate { background: #f1f5f9; color: #334155; }
            .opening-chip--info, .opening-mini-chip--blue { background: #dbeafe; color: #1d4ed8; }
            .opening-chip--ok, .opening-mini-chip--green { background: #dcfce7; color: #166534; }
            .opening-chip--warn, .opening-mini-chip--amber { background: #fef3c7; color: #92400e; }
            .opening-chip--danger, .opening-mini-chip--red { background: #fee2e2; color: #991b1b; }
            .opening-mini-chip--violet { background: #ede9fe; color: #6d28d9; }
            .opening-mini-chip--teal { background: #ccfbf1; color: #0f766e; }

            /* ---- File Slot Grid ---- */
            .ob-slot-section {
                display: flex;
                flex-direction: column;
                gap: 16px;
            }
            .ob-slot-group__label {
                font-size: 11px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: .04em;
                color: var(--opening-muted);
                margin-bottom: 8px;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .ob-slot-group__folder {
                font-size: 11px;
                color: #64748b;
                background: #f1f5f9;
                border-radius: 4px;
                padding: 1px 6px;
                font-weight: 500;
                text-transform: none;
                letter-spacing: 0;
            }
            .ob-slot-group__count {
                margin-left: auto;
                font-size: 11px;
                color: #64748b;
                font-weight: 500;
                text-transform: none;
                letter-spacing: 0;
            }
            .ob-slot-cards {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                gap: 10px;
            }
            .ob-slot-card {
                border: 1.5px solid var(--opening-border);
                border-radius: 8px;
                padding: 10px 12px;
                background: #fff;
                display: flex;
                flex-direction: column;
                gap: 7px;
                transition: border-color .15s, box-shadow .15s;
            }
            .ob-slot-card--uploaded { border-color: #93c5fd; }
            .ob-slot-card--analyzed { border-color: #6ee7b7; }
            .ob-slot-card--done     { border-color: #86efac; background: #f0fdf4; }
            .ob-slot-card--loading  { opacity: 0.65; pointer-events: none; }
            .ob-spinner {
                display: inline-block; width: 10px; height: 10px;
                border: 2px solid currentColor; border-top-color: transparent;
                border-radius: 50%; animation: ob-spin 0.7s linear infinite;
                vertical-align: middle;
            }
            @keyframes ob-spin { to { transform: rotate(360deg); } }
            .ob-slot-card__head {
                display: flex;
                align-items: flex-start;
                gap: 7px;
            }
            .ob-slot-icon { font-size: 18px; flex-shrink: 0; line-height: 1.2; }
            .ob-slot-card__title-wrap { flex: 1; min-width: 0; }
            .ob-slot-title { font-size: 12px; font-weight: 600; color: var(--opening-text); line-height: 1.3; }
            .ob-slot-hint  { font-size: 10px; color: var(--opening-muted); margin-top: 2px; line-height: 1.3; }
            .ob-slot-badge {
                flex-shrink: 0;
                font-size: 10px;
                font-weight: 600;
                padding: 2px 6px;
                border-radius: 10px;
                white-space: nowrap;
            }
            .ob-slot-badge--empty    { background: #f1f5f9; color: #64748b; }
            .ob-slot-badge--uploaded { background: #dbeafe; color: #1d4ed8; }
            .ob-slot-badge--analyzed { background: #d1fae5; color: #065f46; }
            .ob-slot-badge--done     { background: #bbf7d0; color: #14532d; }
            .ob-slot-file {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 4px;
                padding: 4px 6px;
                background: var(--opening-soft);
                border-radius: 4px;
            }
            .ob-slot-filename { font-size: 11px; color: var(--opening-text); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1; }
            .ob-slot-file-meta { display: flex; align-items: center; gap: 4px; flex-shrink: 0; }
            .ob-slot-rows { font-size: 10px; color: var(--opening-muted); }
            .ob-slot-actions { display: flex; gap: 6px; margin-top: 2px; }
            .ob-slot-upload-btn { display: flex; align-items: center; gap: 4px; font-size: 11px !important; padding: 3px 8px !important; flex: 1; justify-content: center; }
            .ob-slot-clear-btn  { display: flex; align-items: center; padding: 3px 6px !important; }
            .opening-import-date {
                text-align: right;
            }
            .opening-import-date span {
                display: block;
                color: var(--opening-muted);
                font-size: 11px;
                font-weight: 700;
                text-transform: uppercase;
            }
            .opening-import-date b {
                display: block;
                color: var(--opening-text);
                font-size: 13px;
                margin-top: 2px;
            }
            /* Step guide */
            .ob-step-guide {
                display: flex;
                align-items: center;
                gap: 8px;
                padding: 12px 14px;
                border: 1px solid var(--opening-border);
                border-radius: 8px;
                background: #fff;
            }
            .ob-step {
                display: flex;
                align-items: center;
                gap: 10px;
                flex: 1;
                padding: 8px 10px;
                border-radius: 6px;
                border: 1px solid transparent;
            }
            .ob-step--active {
                border-color: #93c5fd;
                background: #eff6ff;
            }
            .ob-step--done {
                border-color: #86efac;
                background: #f0fdf4;
            }
            .ob-step--todo {
                opacity: 0.5;
            }
            .ob-step__num {
                width: 26px;
                height: 26px;
                border-radius: 999px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 800;
                font-size: 12px;
                background: #e2e8f0;
                flex-shrink: 0;
            }
            .ob-step--active .ob-step__num { background: #2563eb; color: #fff; }
            .ob-step--done .ob-step__num   { background: #16a34a; color: #fff; }
            .ob-step__body { display: flex; flex-direction: column; }
            .ob-step__body b { font-size: 12px; font-weight: 700; }
            .ob-step__body span { font-size: 11px; color: var(--opening-muted); }
            .ob-step__arrow { color: #94a3b8; font-size: 16px; flex-shrink: 0; }

            /* Commandbar layout */
            .opening-import-commandbar {
                display: flex;
                flex-wrap: wrap;
                align-items: center;
                justify-content: space-between;
                gap: 8px;
                padding: 10px 12px;
                border: 1px solid var(--opening-border);
                border-radius: 8px;
                background: #fff;
            }
            .ob-action-primary {
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
            }
            .ob-action-secondary {
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
                align-items: center;
            }
            .ob-btn-more {
                border-radius: 6px !important;
                display: inline-flex !important;
                align-items: center !important;
                gap: 4px !important;
            }
            .opening-action--warn {
                background: #fffbeb;
                color: #92400e;
                border-color: #fde68a;
            }
            .opening-action--warn:hover {
                background: #fef3c7;
                border-color: #fbbf24;
            }
            .opening-action {
                min-height: 38px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 7px;
                border-radius: 8px;
                border: 1px solid var(--opening-border);
                padding: 7px 11px;
                background: #fff;
                color: #334155;
                font-weight: 700;
                font-size: 12px;
                cursor: pointer;
                transition: background .16s ease, border-color .16s ease, color .16s ease, box-shadow .16s ease;
            }
            .opening-action:hover {
                background: #f8fafc;
                border-color: #94a3b8;
                color: #0f172a;
            }
            .opening-action:focus-visible {
                outline: 2px solid rgba(37, 99, 235, .45);
                outline-offset: 2px;
            }
            .opening-action--primary {
                background: #1d4ed8;
                color: #fff;
                border-color: #1d4ed8;
            }
            .opening-action--primary:hover {
                background: #1e40af;
                color: #fff;
                border-color: #1e40af;
            }
            .opening-action--success {
                background: #15803d;
                color: #fff;
                border-color: #15803d;
            }
            .opening-action--success:hover {
                background: #166534;
                color: #fff;
                border-color: #166534;
            }
            .opening-upload-summary {
                border: 1px solid var(--opening-border);
                border-radius: 8px;
                padding: 12px;
                background: var(--opening-soft);
            }
            .opening-upload-summary ul {
                margin: 8px 0 0;
                padding-left: 20px;
                color: var(--opening-muted);
                max-height: 180px;
                overflow: auto;
            }
            .opening-pipeline {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 10px;
            }
            .opening-pipeline-step {
                display: flex;
                align-items: center;
                gap: 10px;
                min-height: 64px;
                border: 1px solid var(--opening-border);
                border-radius: 8px;
                background: #fff;
                padding: 10px;
            }
            .opening-pipeline-step__index {
                width: 28px;
                height: 28px;
                border-radius: 999px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 12px;
                font-weight: 800;
                background: #f1f5f9;
                color: #334155;
                flex-shrink: 0;
            }
            .opening-pipeline-step--done .opening-pipeline-step__index {
                background: #dcfce7;
                color: #166534;
            }
            .opening-pipeline-step b {
                display: block;
                color: var(--opening-text);
                font-size: 12px;
                line-height: 1.25;
            }
            .opening-pipeline-step span {
                display: block;
                color: var(--opening-muted);
                font-size: 12px;
                margin-top: 2px;
            }
            .opening-import-stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
                gap: 10px;
            }
            .opening-import-stats--dialog {
                grid-template-columns: repeat(auto-fit, minmax(145px, 1fr));
            }
            .opening-import-stats--kpi {
                grid-template-columns: repeat(4, minmax(0, 1fr));
            }
            .opening-import-section-label {
                font-size: 11px;
                font-weight: 700;
                color: var(--opening-muted);
                text-transform: uppercase;
                letter-spacing: 0.04em;
                margin-top: 16px;
                margin-bottom: 6px;
                padding-left: 2px;
            }
            .opening-import-stat {
                min-height: 96px;
                border: 1px solid var(--opening-border);
                border-radius: 8px;
                background: #fff;
                padding: 12px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                gap: 8px;
            }
            .opening-import-stat__head {
                display: flex;
                align-items: center;
                gap: 7px;
                color: var(--opening-muted);
                font-size: 12px;
                font-weight: 700;
            }
            .opening-import-stat b {
                color: var(--opening-text);
                font-size: 22px;
                font-weight: 760;
                line-height: 1.1;
                word-break: break-word;
            }
            .opening-import-stat small {
                color: var(--opening-muted);
                font-size: 11px;
                line-height: 1.35;
            }
            .opening-import-panel,
            .opening-import-empty,
            .opening-import-summary {
                border: 1px solid var(--opening-border);
                border-radius: 8px;
                background: #fff;
                box-shadow: 0 1px 2px rgba(15, 23, 42, .03);
            }
            .opening-import-panel--warn { border-color: #f59e0b; }
            .opening-import-panel--danger { border-color: #ef4444; }
            .opening-import-panel__head {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 10px;
                padding: 12px 14px;
                border-bottom: 1px solid #edf2f7;
            }
            .opening-import-panel__head b {
                display: block;
                color: var(--opening-text);
                font-size: 13px;
                font-weight: 760;
            }
            .opening-import-panel__head span {
                display: block;
                color: var(--opening-muted);
                font-size: 12px;
                margin-top: 2px;
            }
            .opening-panel-count {
                min-width: 28px;
                height: 28px;
                border-radius: 999px;
                background: #f1f5f9;
                color: #334155 !important;
                display: inline-flex !important;
                align-items: center;
                justify-content: center;
                font-weight: 800;
                margin-top: 0 !important;
            }
            .opening-import-table-wrap {
                width: 100%;
                overflow-x: auto;
            }
            .opening-import-table {
                margin-bottom: 0;
                min-width: 840px;
                border-collapse: separate;
                border-spacing: 0;
            }
            .opening-import-table th {
                background: #f8fafc;
                color: #475569;
                font-size: 11px;
                font-weight: 800;
                text-transform: uppercase;
                white-space: nowrap;
                border-top: 0 !important;
                border-bottom: 1px solid #e2e8f0 !important;
            }
            .opening-import-table td {
                font-size: 12px;
                vertical-align: top;
                border-top: 0 !important;
                border-bottom: 1px solid #eef2f7 !important;
            }
            .opening-import-table tbody tr:hover td {
                background: #f8fafc;
            }
            .opening-file-name {
                color: var(--opening-text);
                font-weight: 700;
                line-height: 1.35;
                overflow-wrap: anywhere;
            }
            .opening-file-path {
                color: var(--opening-muted);
                font-size: 11px;
                margin-top: 3px;
                line-height: 1.35;
            }
            .opening-confidence {
                display: flex;
                align-items: center;
                gap: 8px;
                min-width: 120px;
            }
            .opening-confidence__bar {
                height: 6px;
                width: 82px;
                border-radius: 999px;
                background: #e2e8f0;
                overflow: hidden;
            }
            .opening-confidence__fill {
                display: block;
                height: 100%;
                border-radius: inherit;
            }
            .opening-confidence__fill--ok { background: #16a34a; }
            .opening-confidence__fill--warn { background: #d97706; }
            .opening-confidence__fill--danger { background: #dc2626; }
            .opening-confidence b {
                color: var(--opening-text);
                font-size: 12px;
                min-width: 34px;
            }
            .opening-import-empty {
                min-height: 112px;
                display: flex;
                align-items: center;
                gap: 14px;
                padding: 18px;
            }
            .opening-import-empty__icon {
                width: 42px;
                height: 42px;
                border-radius: 8px;
                background: #eff6ff;
                color: #1d4ed8;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
            }
            .opening-import-empty__icon svg {
                width: 22px;
                height: 22px;
            }
            .opening-import-empty b {
                display: block;
                color: var(--opening-text);
                font-size: 14px;
            }
            .opening-import-empty span {
                display: block;
                margin-top: 3px;
                color: var(--opening-muted);
                font-size: 12px;
            }
            .opening-import-summary {
                padding: 0 0 12px;
            }
            .opening-result-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
                gap: 10px;
                padding: 12px 14px 0;
            }
            .opening-result-item {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 10px 12px;
                background: #f8fafc;
            }
            .opening-result-item span,
            .opening-result-item small {
                display: block;
                color: var(--opening-muted);
                font-size: 12px;
            }
            .opening-result-item b {
                display: block;
                margin-top: 4px;
                color: var(--opening-text);
                font-size: 18px;
            }
            .opening-import-line {
                padding: 8px 14px;
                border-top: 1px solid #eef2f7;
                font-size: 12px;
                color: #334155;
            }
            .opening-master-preview {
                padding: 10px 14px 2px;
                border-top: 1px solid #eef2f7;
            }
            .opening-master-preview > b {
                display: block;
                margin-bottom: 6px;
                color: var(--opening-text);
                font-size: 12px;
            }
            .opening-master-preview .opening-import-line {
                margin: 0 -14px;
            }
            .opening-process-confirm {
                display: flex;
                align-items: flex-start;
                gap: 14px;
                margin-bottom: 14px;
                padding: 14px;
                border: 1px solid rgba(79, 70, 229, .20);
                border-radius: 8px;
                background: #f8fafc;
            }
            .opening-process-confirm--sales {
                border-color: rgba(22, 163, 74, .25);
                background: #f0fdf4;
            }
            .opening-process-confirm--purchase {
                border-color: rgba(180, 83, 9, .28);
                background: #fffbeb;
            }
            .opening-process-confirm--master {
                border-color: rgba(37, 99, 235, .24);
                background: #eff6ff;
            }
            .opening-process-confirm__icon {
                width: 42px;
                height: 42px;
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
                color: #4f46e5;
                background: #eef2ff;
            }
            .opening-process-confirm--sales .opening-process-confirm__icon {
                color: #15803d;
                background: #dcfce7;
            }
            .opening-process-confirm--purchase .opening-process-confirm__icon {
                color: #b45309;
                background: #fef3c7;
            }
            .opening-process-confirm--master .opening-process-confirm__icon {
                color: #1d4ed8;
                background: #dbeafe;
            }
            .opening-process-confirm__icon svg {
                width: 21px;
                height: 21px;
            }
            .opening-process-confirm__body {
                flex: 1;
                min-width: 0;
            }
            .opening-process-confirm__eyebrow {
                color: var(--opening-muted);
                font-size: 11px;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: .04em;
            }
            .opening-process-confirm__title {
                margin-top: 3px;
                color: var(--opening-text);
                font-size: 16px;
                font-weight: 760;
                line-height: 1.3;
            }
            .opening-process-confirm__message {
                margin-top: 5px;
                color: #475569;
                font-size: 12.5px;
                line-height: 1.45;
            }
            .opening-process-confirm__stats {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 8px;
                margin-top: 12px;
            }
            .opening-process-confirm__stats div,
            .opening-process-stat,
            .opening-process-result__stats div {
                border: 1px solid rgba(148, 163, 184, .28);
                border-radius: 8px;
                background: rgba(255, 255, 255, .82);
                padding: 9px 10px;
                min-width: 0;
            }
            .opening-process-confirm__stats span,
            .opening-process-stat span,
            .opening-process-result__stats span {
                display: block;
                color: var(--opening-muted);
                font-size: 11px;
                font-weight: 750;
                line-height: 1.25;
            }
            .opening-process-confirm__stats b,
            .opening-process-stat b,
            .opening-process-result__stats b {
                display: block;
                margin-top: 4px;
                color: var(--opening-text);
                font-size: 13px;
                font-weight: 760;
                line-height: 1.3;
                overflow-wrap: anywhere;
            }
            .opening-process-progress {
                display: flex;
                flex-direction: column;
                gap: 14px;
                padding: 2px;
                color: var(--opening-text);
            }
            .opening-process-progress__head {
                display: flex;
                align-items: center;
                gap: 14px;
            }
            .opening-process-progress__icon {
                width: 50px;
                height: 50px;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
                color: #4f46e5;
                background: linear-gradient(135deg, rgba(79, 70, 229, .12), rgba(168, 85, 247, .14));
                box-shadow: 0 10px 22px rgba(79, 70, 229, .12);
            }
            .opening-process-progress--complete .opening-process-progress__icon {
                color: #047857;
                background: #ecfdf5;
                box-shadow: none;
            }
            .opening-process-progress--warning .opening-process-progress__icon {
                color: #92400e;
                background: #fffbeb;
                box-shadow: none;
            }
            .opening-process-progress--failed .opening-process-progress__icon {
                color: #b91c1c;
                background: #fef2f2;
                box-shadow: none;
            }
            .opening-process-progress__icon svg {
                width: 22px;
                height: 22px;
            }
            .opening-spinner {
                width: 20px;
                height: 20px;
                border-radius: 50%;
                border: 2px solid rgba(79, 70, 229, .18);
                border-top-color: #4f46e5;
                animation: opening-spin .75s linear infinite;
            }
            .opening-process-progress__body {
                flex: 1;
                min-width: 0;
            }
            .opening-process-progress__eyebrow {
                color: var(--opening-muted);
                font-size: 11px;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: .04em;
            }
            .opening-process-progress__title {
                margin-top: 3px;
                color: var(--opening-text);
                font-size: 16px;
                line-height: 1.3;
                font-weight: 760;
            }
            .opening-process-progress__file {
                margin-top: 4px;
                color: var(--opening-muted);
                font-size: 12px;
                overflow-wrap: anywhere;
            }
            .opening-process-progress__live {
                display: inline-flex;
                align-items: center;
                gap: 7px;
                padding: 6px 10px;
                border-radius: 999px;
                color: #047857;
                background: #ecfdf5;
                font-size: 12px;
                font-weight: 800;
                white-space: nowrap;
                flex-shrink: 0;
            }
            .opening-process-progress--failed .opening-process-progress__live {
                color: #b91c1c;
                background: #fef2f2;
            }
            .opening-process-progress--warning .opening-process-progress__live {
                color: #92400e;
                background: #fffbeb;
            }
            .opening-process-progress__live-dot,
            .opening-process-progress__message-dot {
                width: 8px;
                height: 8px;
                border-radius: 999px;
                background: currentColor;
                box-shadow: 0 0 0 4px rgba(16, 185, 129, .14);
                flex-shrink: 0;
            }
            .opening-process-progress--running .opening-process-progress__live-dot,
            .opening-process-progress--running .opening-process-progress__message-dot {
                animation: opening-process-pulse 1.2s ease-in-out infinite;
            }
            .opening-process-progress__bar {
                height: 8px;
                border-radius: 999px;
                background: rgba(79, 70, 229, .10);
                overflow: hidden;
            }
            .opening-process-progress__bar-fill {
                height: 100%;
                border-radius: inherit;
                background: linear-gradient(90deg, #4f46e5, #8b5cf6 65%, #0ea5e9);
                transition: width .35s ease;
                position: relative;
            }
            .opening-process-progress--failed .opening-process-progress__bar-fill {
                background: linear-gradient(90deg, #ef4444, #b91c1c);
            }
            .opening-process-progress--warning .opening-process-progress__bar-fill {
                background: linear-gradient(90deg, #d97706, #f59e0b);
            }
            .opening-process-progress__stats,
            .opening-process-result__stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(135px, 1fr));
                gap: 9px;
            }
            .opening-process-progress__message {
                display: flex;
                align-items: flex-start;
                gap: 10px;
                padding: 11px 12px;
                border-radius: 8px;
                border: 1px solid rgba(79, 70, 229, .18);
                background: rgba(79, 70, 229, .06);
                color: #312e81;
                font-size: 12.5px;
                line-height: 1.5;
            }
            .opening-process-progress--failed .opening-process-progress__message {
                border-color: rgba(239, 68, 68, .24);
                background: #fef2f2;
                color: #991b1b;
            }
            .opening-process-progress--warning .opening-process-progress__message {
                border-color: rgba(245, 158, 11, .28);
                background: #fffbeb;
                color: #92400e;
            }
            .opening-process-stages {
                display: grid;
                grid-template-columns: repeat(5, minmax(0, 1fr));
                gap: 8px;
                padding: 10px;
                border: 1px solid var(--opening-border);
                border-radius: 8px;
                background: #f8fafc;
            }
            .opening-process-stage {
                display: flex;
                align-items: center;
                gap: 7px;
                min-width: 0;
                color: var(--opening-muted);
                font-size: 11.5px;
                font-weight: 700;
            }
            .opening-process-stage__dot {
                width: 9px;
                height: 9px;
                border-radius: 999px;
                background: #cbd5e1;
                flex-shrink: 0;
            }
            .opening-process-stage.is-active .opening-process-stage__dot {
                background: #4f46e5;
                box-shadow: 0 0 0 3px rgba(79, 70, 229, .13);
            }
            .opening-process-stage.is-active {
                color: var(--opening-text);
            }
            .opening-process-stage.is-current .opening-process-stage__dot {
                animation: opening-process-pulse 1.2s ease-in-out infinite;
            }
            .opening-process-stage__label {
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }
            .opening-process-result {
                border: 1px solid var(--opening-border);
                border-radius: 8px;
                background: #fff;
                overflow: hidden;
            }
            .opening-process-result--complete {
                border-color: rgba(16, 185, 129, .24);
            }
            .opening-process-result--warning {
                border-color: rgba(245, 158, 11, .30);
            }
            .opening-process-result--failed {
                border-color: rgba(239, 68, 68, .28);
            }
            .opening-process-result__head {
                padding: 11px 12px;
                border-bottom: 1px solid #eef2f7;
                background: #f8fafc;
            }
            .opening-process-result__head b {
                display: block;
                color: var(--opening-text);
                font-size: 13px;
                font-weight: 800;
            }
            .opening-process-result__head span {
                display: block;
                color: var(--opening-muted);
                font-size: 12px;
                margin-top: 2px;
                line-height: 1.4;
            }
            .opening-process-result__stats {
                padding: 12px;
            }
            .opening-process-result__errors {
                margin: 0 12px 12px;
                border-radius: 8px;
                border: 1px solid #fecaca;
                background: #fef2f2;
                color: #991b1b;
                overflow: hidden;
            }
            .opening-process-result__errors div {
                padding: 8px 10px;
                border-bottom: 1px solid #fecaca;
                font-size: 12px;
                line-height: 1.4;
            }
            .opening-process-result__errors div:last-child {
                border-bottom: 0;
            }
            .opening-process-result__errors small {
                display: block;
                padding: 8px 10px;
                color: #991b1b;
                font-weight: 700;
            }
            @keyframes opening-spin {
                to { transform: rotate(360deg); }
            }
            @keyframes opening-process-pulse {
                0%, 100% { opacity: 1; transform: scale(1); }
                50% { opacity: .45; transform: scale(.82); }
            }
            @media (max-width: 1100px) {
                .opening-import-stats { grid-template-columns: repeat(2, minmax(0, 1fr)); }
                .opening-pipeline { grid-template-columns: repeat(2, minmax(0, 1fr)); }
                .opening-process-stages { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            }
            @media (max-width: 700px) {
                .opening-import-hero { flex-direction: column; }
                .opening-import-hero__side { align-items: flex-start; }
                .opening-import-commandbar { display: grid; grid-template-columns: 1fr; }
                .opening-action { width: 100%; }
                .opening-import-stats,
                .opening-pipeline { grid-template-columns: 1fr; }
                .opening-import-path span { white-space: normal; overflow-wrap: anywhere; }
                .opening-process-confirm,
                .opening-process-progress__head { flex-direction: column; }
                .opening-process-confirm__stats,
                .opening-process-progress__stats,
                .opening-process-result__stats,
                .opening-process-stages { grid-template-columns: 1fr; }
                .opening-process-progress__live { align-self: flex-start; }
            }
            @media (prefers-reduced-motion: reduce) {
                .opening-action { transition: none; }
                .opening-spinner,
                .opening-process-progress--running .opening-process-progress__live-dot,
                .opening-process-progress--running .opening-process-progress__message-dot,
                .opening-process-stage.is-current .opening-process-stage__dot {
                    animation: none;
                }
            }
        </style>
    `;
}
