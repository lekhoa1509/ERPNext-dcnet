const IMPORT_AUTO_API = "dcnet_migrate.import_auto.doctype.import_auto.import_auto";
const SMART_FIX_MAX_RETRY = 3;

/* --------------------------------------------------------------------------
 * Category taxonomy — groups file/sheet rows by target_doctype so the page
 * can be reviewed and controlled "từng danh mục một" instead of one long
 * flat table. Order mirrors DOCTYPE_ORDER in services/doctype_metadata.py.
 * -------------------------------------------------------------------------- */

const CATEGORY_META = {
    "UOM": { order: 1, label: "Đơn vị tính (UOM)", icon: "📏" },
    "Item Group": { order: 2, label: "Nhóm vật tư (Item Group)", icon: "🏷️" },
    "Bank": { order: 3, label: "Ngân hàng (Bank)", icon: "🏦" },
    "Account": { order: 4, label: "Hệ thống tài khoản (Account)", icon: "🌳" },
    "Branch": { order: 5, label: "Chi nhánh (Branch)", icon: "🏢" },
    "Department": { order: 6, label: "Phòng ban (Department)", icon: "🗂️" },
    "Warehouse": { order: 7, label: "Kho (Warehouse)", icon: "📦" },
    "Bank Account": { order: 8, label: "Tài khoản ngân hàng (Bank Account)", icon: "💳" },
    "Customer Group": { order: 9, label: "Nhóm khách hàng (Customer Group)", icon: "👥" },
    "Supplier Group": { order: 10, label: "Nhóm nhà cung cấp (Supplier Group)", icon: "👥" },
    "Customer": { order: 11, label: "Khách hàng (Customer)", icon: "👤" },
    "Supplier": { order: 12, label: "Nhà cung cấp (Supplier)", icon: "🏭" },
    "Item": { order: 13, label: "Hàng hóa dịch vụ (Item)", icon: "📋" },
    "Employee": { order: 14, label: "Nhân viên (Employee)", icon: "👔" },
    "Project": { order: 15, label: "Công trình (Project)", icon: "🏗️" },
};
const UNSUPPORTED_CATEGORY_KEY = "__unsupported__";
const UNSUPPORTED_CATEGORY_META = { order: 999, label: __("Không hỗ trợ / Khác (Unsupported)"), icon: "⚠️" };

function category_key(target_doctype) {
    return target_doctype || UNSUPPORTED_CATEGORY_KEY;
}

function category_meta(target_doctype) {
    if (!target_doctype) return UNSUPPORTED_CATEGORY_META;
    return CATEGORY_META[target_doctype] || { order: 500, label: target_doctype, icon: "📄" };
}

frappe.ui.form.on("Import Auto", {
    onload(frm) {
        frm.layout.show_message_help = false;
    },

    refresh(frm) {
        const page_title = frm.doc.display_name
            ? `${__("Import Danh Mục (Master Data Import)")}: ${frm.doc.display_name}`
            : __("Import Danh Mục (Master Data Import)");
        frm.page.set_title(page_title);
        setup_import_auto_progress_listener(frm);
        hide_sidebar_and_widen(frm);
        frm.set_df_property("folder_path", "hidden", 1);
        frm.page.set_indicator(...status_indicator(frm.doc.status));

        frm.add_custom_button(__("AI Settings"), () => {
            frappe.set_route("Form", "Import Auto Settings");
        });

        render_import_auto_file_list(frm);
    },

    scan_files_btn(frm) {
        run_doc_action(frm, "scan_files", __("Scanning Excel files..."));
    },

    analyze_files_btn(frm) {
        run_doc_action(frm, "analyze_files", __("Analyzing files..."));
    },

    test_connection_btn(frm) {
        run_doc_action(frm, "test_ai_connection", __("Checking AI connection..."));
    },
});

/* --------------------------------------------------------------------------
 * Page chrome: hide sidebar & widen container
 * -------------------------------------------------------------------------- */

function hide_sidebar_and_widen(frm) {
    if (frm.sidebar && frm.sidebar.sidebar) {
        frm.sidebar.sidebar.hide();
    }
    const $page = frm.page.wrapper;
    $page.find(".layout-side-section").hide();
    $page.find(".layout-main-section-wrapper").css({
        "max-width": "none",
        "width": "100%",
        "padding-right": "0",
    });

    // Walk up DOM and force any ancestor .container to be full-width.
    const wrapperEl = $page.get(0);
    if (wrapperEl) {
        let node = wrapperEl;
        while (node && node !== document.body) {
            if (node.classList && node.classList.contains("container")) {
                node.style.setProperty("max-width", "100%", "important");
                node.style.setProperty("width", "100%", "important");
                node.style.setProperty("padding-left", "24px", "important");
                node.style.setProperty("padding-right", "24px", "important");
            }
            node = node.parentElement;
        }
        // Also catch any .container inside the page wrapper itself
        wrapperEl.querySelectorAll(".container").forEach((el) => {
            el.style.setProperty("max-width", "100%", "important");
            el.style.setProperty("width", "100%", "important");
        });
    }

    const files_field = frm.fields_dict.files_html;
    if (files_field && files_field.$wrapper) {
        files_field.$wrapper.closest(".form-column").css({
            "flex": "0 0 100%",
            "max-width": "100%",
            "width": "100%",
        });
        files_field.$wrapper.closest(".section-body").css({
            "display": "block",
            "width": "100%",
        });
        files_field.$wrapper.closest(".form-section").css({
            "width": "100%",
            "max-width": "100%",
        });
    }

    const existing_page_style = document.getElementById("import-auto-page-css");
    if (existing_page_style) {
        existing_page_style.remove();
    }

    const style = document.createElement("style");
    style.id = "import-auto-page-css";
    style.textContent = `
            .form-page[data-doctype-name="Import Auto"] .layout-main,
            .form-page[data-doctype-name="Import Auto"] .layout-main-section,
            .form-page[data-doctype-name="Import Auto"] .layout-main-section-wrapper,
            .form-page[data-doctype-name="Import Auto"] .form-layout {
                width: 100% !important;
                max-width: 100% !important;
                flex: 1 1 100% !important;
            }
            .form-page[data-doctype-name="Import Auto"] .layout-side-section { display: none !important; }
            [data-fieldname="files_html"] { padding: 0 !important; width: 100% !important; }
            [data-fieldname="files_html"] .form-group { margin-bottom: 0 !important; }
            [data-fieldname="files_html"] .control-input-wrapper { width: 100% !important; }
        `;
    document.head.appendChild(style);
}

function status_indicator(status) {
    const map = {
        "Draft":      [__("Draft"), "gray"],
        "Scanning":   [__("Scanning"), "blue"],
        "Scanned":    [__("Scanned"), "blue"],
        "Analyzing":  [__("Analyzing"), "orange"],
        "Analyzed":   [__("Analyzed"), "purple"],
        "Importing":  [__("Importing"), "orange"],
        "Completed":  [__("Completed"), "green"],
        "Partial":    [__("Partial"), "yellow"],
        "Failed":     [__("Failed"), "red"],
    };
    return map[status] || [__("Draft"), "gray"];
}

/* --------------------------------------------------------------------------
 * Action runner
 * -------------------------------------------------------------------------- */

function run_doc_action(frm, method, freeze_message) {
    if (frm.doc.__islocal || frm.is_dirty()) {
        frm.save().then(() => call_doc_action(frm, method, freeze_message));
        return;
    }
    call_doc_action(frm, method, freeze_message);
}

function call_doc_action(frm, method, freeze_message) {
    const progress_action = ["scan_files", "analyze_files"].includes(method);
    if (progress_action) {
        update_progress_panel(frm, {
            percent: 0,
            processed: 0,
            total: frm.doc.files?.length || frm.doc.excel_file_count || 0,
            message: method === "scan_files" ? __("Scanning folder...") : __("Starting analysis..."),
            status: "running",
        });
    }

    frappe.call({
        method: `${IMPORT_AUTO_API}.${method}`,
        args: { docname: frm.doc.name },
        freeze: !progress_action,
        freeze_message,
    }).then((response) => {
        if (progress_action) {
            const result = response.message || {};
            frappe.show_alert({
                message: result.already_queued ? __("A job is already running.") : __("Queued. Progress will update here."),
                indicator: "blue",
            });
        }
        frm.reload_doc();
    });
}

function setup_import_auto_progress_listener(frm) {
    if (frm.__import_auto_progress_listener_bound) return;

    frappe.realtime.on("import_auto_progress", (data) => {
        if (!data || data.docname !== frm.doc.name) return;

        frm.doc.progress_percent = data.percent || 0;
        frm.doc.progress_message = data.message || "";
        frm.doc.processed_files = data.processed || 0;
        frm.doc.total_files = data.total || 0;
        frm.doc.current_file = data.current_file || "";
        update_progress_panel(frm, data);

        if (data.stage === "reanalyze") {
            handle_reanalyze_progress(frm, data);
            return;
        }

        if (["complete", "failed"].includes(data.status)) {
            setTimeout(() => frm.reload_doc(), 700);
        }
    });

    frm.__import_auto_progress_listener_bound = true;
}

function handle_reanalyze_progress(frm, data) {
    if (!data || !data.row_name) return;
    if (["complete", "failed"].includes(data.status)) {
        setTimeout(() => frm.reload_doc(), 500);
        return;
    }
    // Mark row as Reanalyzing optimistically
    const row = (frm.doc.files || []).find((r) => r.name === data.row_name);
    if (row && row.status !== "Reanalyzing") {
        row.status = "Reanalyzing";
        render_import_auto_file_list(frm);
    }
}

/* --------------------------------------------------------------------------
 * Main render
 * -------------------------------------------------------------------------- */

function render_import_auto_file_list(frm) {
    const field = frm.fields_dict.files_html;
    if (!field) return;

    ensure_slot_defs_loaded(frm, () => render_import_auto_file_list(frm));

    const rows = (frm.doc.files || []).slice().sort((a, b) => {
        return (a.import_order || 9999) - (b.import_order || 9999) || (a.idx || 0) - (b.idx || 0);
    });

    const total = frm.doc.excel_file_count || rows.length || 0;
    const safe_count = rows.filter((row) => row.safety_status === "Safe").length;
    const warning_count = rows.filter((row) => row.safety_status === "Warning").length;
    const error_count = rows.filter((row) => row.safety_status === "Error").length;
    const imported_count = rows.filter((row) => ["Imported", "Partial"].includes(row.status)).length;

    const active_filter = frm.__stat_filter || null;
    let display_rows = rows;
    if (active_filter === "safe")     display_rows = rows.filter((r) => r.safety_status === "Safe");
    else if (active_filter === "warning")  display_rows = rows.filter((r) => r.safety_status === "Warning");
    else if (active_filter === "error")    display_rows = rows.filter((r) => r.safety_status === "Error");
    else if (active_filter === "imported") display_rows = rows.filter((r) => ["Imported", "Partial"].includes(r.status));

    const filter_bar = active_filter ? `
        <div class="import-auto-filter-bar">
            <span class="import-auto-filter-bar__label">
                <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
                ${__("Filtered")}: <b>${frappe.utils.escape_html(active_filter_label(active_filter))}</b>
                &mdash; ${display_rows.length} / ${rows.length} ${__("files")}
            </span>
            <button type="button" class="import-auto-filter-bar__clear" data-stat-filter-clear>
                ${__("Clear filter")} &times;
            </button>
        </div>
    ` : "";

    const html = `
        ${import_auto_styles()}
        <div class="import-auto-import-shell">
            ${render_toolbar(frm)}
            ${render_step_guide(frm)}
            ${render_master_slot_grid(frm)}
            ${render_progress_panel(frm)}
            <div class="import-auto-import-summary">
                ${stat_card("file",    "indigo", __("Excel Files"), total, __("Found in folder"), "all", active_filter)}
                ${stat_card("check",   "green",  __("Safe"), safe_count, __("Ready to import"), "safe", active_filter)}
                ${stat_card("warning", "amber",  __("Warning"), warning_count, __("Exact duplicates found"), "warning", active_filter)}
                ${stat_card("alert",   "red",    __("Error"), error_count, __("Needs review"), "error", active_filter)}
                ${stat_card("upload",  "blue",   __("Imported"), imported_count, __("Sent to DCNET"), "imported", active_filter)}
            </div>
            ${filter_bar}
            ${display_rows.length ? render_category_groups(frm, display_rows) : (rows.length ? render_filter_empty(active_filter) : render_empty())}
        </div>
    `;

    field.$wrapper.html(html);
    bind_toolbar(frm, field.$wrapper);
    bind_slot_upload_actions(frm, field.$wrapper);
    bind_stat_filters(frm, field.$wrapper);
    bind_category_actions(frm, field.$wrapper);
    bind_file_preview_links(frm, field.$wrapper);
    bind_reanalyze_buttons(frm, field.$wrapper);
    bind_check_duplicate_buttons(frm, field.$wrapper);
    bind_smart_buttons(frm, field.$wrapper);
    bind_ai_resolution_buttons(frm, field.$wrapper);
    bind_manual_file_action_buttons(frm, field.$wrapper);
    bind_reason_toggles(field.$wrapper);
    bind_import_report_buttons(frm, field.$wrapper);
}

function bind_stat_filters(frm, wrapper) {
    wrapper.find("[data-stat-filter]").on("click", function () {
        const key = $(this).data("stat-filter");
        // "all" clears filter; clicking active filter also clears
        frm.__stat_filter = (key === "all" || frm.__stat_filter === key) ? null : key;
        render_import_auto_file_list(frm);
    });
    wrapper.find("[data-stat-filter-clear]").on("click", function () {
        frm.__stat_filter = null;
        render_import_auto_file_list(frm);
    });
}

function active_filter_label(filter) {
    const map = {
        safe: __("Safe"),
        warning: __("Warning"),
        error: __("Error"),
        imported: __("Imported"),
    };
    return map[filter] || filter;
}

function render_filter_empty(active_filter) {
    return `
        <div class="import-auto-empty">
            <div class="import-auto-empty__icon">
                <svg viewBox="0 0 24 24" width="44" height="44" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>
                </svg>
            </div>
            <div class="import-auto-empty__title">${__("No files match filter")}: <b>${frappe.utils.escape_html(active_filter_label(active_filter))}</b></div>
            <div class="import-auto-empty__hint">${__("Click the card again or Clear filter to show all files.")}</div>
        </div>
    `;
}

/* --------------------------------------------------------------------------
 * Step guide — 1) Scan → 2) AI Analyze → 3) Import, mirrors Opening Balance
 * Import's ob-step-guide so both import tools read the same way.
 * -------------------------------------------------------------------------- */

function render_step_guide(frm) {
    const status = frm.doc.status || "Draft";
    const files = frm.doc.files || [];

    const step_scanned = status !== "Draft" || files.length > 0;
    const step_analyzed = ["Analyzed", "Importing", "Completed", "Partial"].includes(status);
    const step_imported = status === "Completed";

    const step_class = (done, active) => (done ? "iac-step--done" : (active ? "iac-step--active" : "iac-step--todo"));

    return `
        <section class="import-auto-step-guide">
            <div class="iac-step ${step_class(step_scanned, true)}">
                <div class="iac-step__num">${step_scanned ? "✓" : "1"}</div>
                <div class="iac-step__body">
                    <b>${__("Upload từng danh mục (Upload each category)")}</b>
                    <span>${files.length ? __("{0} file đã upload", [files.length]) : __("Upload file vào ô danh mục cần thiết bên dưới")}</span>
                </div>
            </div>
            <div class="iac-step__arrow">→</div>
            <div class="iac-step ${step_class(step_analyzed, step_scanned)}">
                <div class="iac-step__num">${step_analyzed ? "✓" : "2"}</div>
                <div class="iac-step__body">
                    <b>${__("Kiểm tra kết quả (Review results)")}</b>
                    <span>${step_analyzed ? __("Đã phân loại theo từng danh mục") : __("Mapping cột được xử lý tự động, không qua AI")}</span>
                </div>
            </div>
            <div class="iac-step__arrow">→</div>
            <div class="iac-step ${step_class(step_imported, step_analyzed)}">
                <div class="iac-step__num">${step_imported ? "✓" : "3"}</div>
                <div class="iac-step__body">
                    <b>${__("Import vào DCNET (Import to DCNET)")}</b>
                    <span>${step_imported ? __("Hoàn thành") : __("Duyệt và import từng danh mục")}</span>
                </div>
            </div>
        </section>
    `;
}

/* --------------------------------------------------------------------------
 * Master-data slot grid — fixed upload slots (one per category the ERP
 * needs), mirroring Opening Balance Import's SLOT_GROUPS. Replaces
 * "scan a whole folder and let AI guess" as the primary way to get files
 * in: the slot already fixes target_doctype, so upload_slot_file() on the
 * server skips AI entirely (see services/slot_import.py).
 * -------------------------------------------------------------------------- */

function ensure_slot_defs_loaded(frm, on_loaded) {
    if (frm.__slot_defs || frm.__slot_defs_loading) return;
    frm.__slot_defs_loading = true;
    frappe.call({
        method: `${IMPORT_AUTO_API}.get_slot_defs`,
    }).then((r) => {
        frm.__slot_defs = r.message || [];
        frm.__slot_defs_loading = false;
        on_loaded();
    }).catch(() => {
        frm.__slot_defs_loading = false;
    });
}

function slot_rows(frm, slot_key) {
    return (frm.doc.files || []).filter((row) => row.slot_key === slot_key);
}

function render_master_slot_grid(frm) {
    if (!frm.__slot_defs) {
        return `<div class="import-auto-slot-hint">${__("Đang tải danh sách danh mục...")}</div>`;
    }

    // Group slots by theme (Cơ cấu tổ chức / Vật tư hàng hóa / Đối tác & Ngân
    // hàng / Khác — see slot_import.SLOT_DEFS), preserving the backend's
    // declared order, so the grid reads as labeled sections like Opening
    // Balance Import's SLOT_GROUPS instead of one flat wall of cards.
    const groups = [];
    const group_by_label = new Map();
    frm.__slot_defs.forEach((slot) => {
        const label = slot.group || __("Danh mục");
        if (!group_by_label.has(label)) {
            const group = { label, slots: [] };
            group_by_label.set(label, group);
            groups.push(group);
        }
        group_by_label.get(label).slots.push(slot);
    });

    const groups_html = groups.map((group) => {
        const uploaded_in_group = group.slots.filter((s) => slot_rows(frm, s.key).length).length;
        const cards = group.slots.map((slot) => render_slot_card(frm, slot)).join("");
        return `
            <div class="import-auto-slot-group">
                <div class="import-auto-slot-group__label">
                    <span>${frappe.utils.escape_html(group.label)}</span>
                    <span class="import-auto-slot-group__count">${uploaded_in_group}/${group.slots.length} ${__("file")}</span>
                </div>
                <div class="import-auto-slot-cards">${cards}</div>
            </div>
        `;
    }).join("");

    return `<section class="import-auto-slot-grid">${groups_html}${render_extra_upload_card(frm)}</section>`;
}

/* --------------------------------------------------------------------------
 * Extra card — upload multiple files that have no fixed slot above. Reuses
 * the same "Upload Files" picker + scan_files/analyze_files pipeline the
 * "Nâng cao (Advanced)" dialog uses, just surfaced directly in the grid so
 * users don't have to find the gear-menu dialog for this common case.
 * -------------------------------------------------------------------------- */

function render_extra_upload_card(frm) {
    const rows = (frm.doc.files || []).filter((row) => !row.slot_key);
    const total = rows.length;
    const error = rows.filter((r) => r.safety_status === "Error").length;
    const imported = rows.filter((r) => ["Imported", "Partial"].includes(r.status)).length;

    let state, state_label;
    if (!total) { state = "empty"; state_label = __("Chưa có file"); }
    else if (imported === total) { state = "imported"; state_label = __("Đã import"); }
    else if (error > 0) { state = "error"; state_label = __("Có lỗi"); }
    else { state = "ready"; state_label = __("Sẵn sàng"); }

    const meta_line = total
        ? __("{0} file — xem chi tiết ở bảng danh mục bên dưới", [total])
        : __("Cho file KHÔNG có trong danh sách ô cố định ở trên. Chọn nhiều file cùng lúc, AI sẽ tự đoán DocType.");

    return `
        <div class="import-auto-slot-group">
            <div class="import-auto-slot-group__label">
                <span>${__("File khác (chưa có ô cố định)")}</span>
                <span class="import-auto-slot-group__count">${total} ${__("file")}</span>
            </div>
            <div class="import-auto-slot-cards">
                <div class="import-auto-slot-card import-auto-slot-card--${state}">
                    <div class="import-auto-slot-card__head">
                        <span class="import-auto-slot-icon">📥</span>
                        <div class="import-auto-slot-card__title-wrap">
                            <div class="import-auto-slot-title">${__("Upload nhiều file khác")}</div>
                            <div class="import-auto-slot-hint">${meta_line}</div>
                        </div>
                        <span class="import-auto-slot-badge import-auto-slot-badge--${state}">${state_label}</span>
                    </div>
                    <div class="import-auto-slot-actions">
                        <button type="button" class="btn btn-xs btn-primary" data-action="upload-others">
                            ${__("Upload nhiều file")}
                        </button>
                        ${total ? `
                            <button type="button" class="btn btn-xs btn-default" data-action="show-advanced">
                                ${__("Phân tích bằng AI")}
                            </button>
                        ` : ""}
                    </div>
                </div>
            </div>
        </div>
    `;
}

function render_slot_card(frm, slot) {
    const rows = slot_rows(frm, slot.key);
    const total = rows.length;
    const error = rows.filter((r) => r.safety_status === "Error").length;
    const imported = rows.filter((r) => ["Imported", "Partial"].includes(r.status)).length;

    let state, state_label;
    if (!total) { state = "empty"; state_label = __("Chưa upload"); }
    else if (imported === total) { state = "imported"; state_label = __("Đã import"); }
    else if (error > 0) { state = "error"; state_label = __("Có lỗi"); }
    else { state = "ready"; state_label = __("Sẵn sàng"); }

    const file_name = rows[0] ? rows[0].file_name : "";
    const meta_line = total
        ? `${frappe.utils.escape_html(file_name)}${slot.is_combo ? ` · ${total} sheet` : ""}`
        : frappe.utils.escape_html(slot.hint || "");

    return `
        <div class="import-auto-slot-card import-auto-slot-card--${state}" data-slot-key="${frappe.utils.escape_html(slot.key)}">
            <div class="import-auto-slot-card__head">
                <span class="import-auto-slot-icon">${slot.icon}</span>
                <div class="import-auto-slot-card__title-wrap">
                    <div class="import-auto-slot-title">${frappe.utils.escape_html(slot.label)}</div>
                    <div class="import-auto-slot-hint">${meta_line}</div>
                </div>
                <span class="import-auto-slot-badge import-auto-slot-badge--${state}">${state_label}</span>
            </div>
            <div class="import-auto-slot-actions">
                <button type="button" class="btn btn-xs ${total ? "btn-default" : "btn-primary"} import-auto-slot-upload-btn" data-slot-key="${frappe.utils.escape_html(slot.key)}">
                    ${total ? __("Thay file") : __("Upload")}
                </button>
                ${total ? `
                    <button type="button" class="btn btn-xs btn-default import-auto-slot-clear-btn" data-slot-key="${frappe.utils.escape_html(slot.key)}" title="${__("Xóa file")}">
                        ${__("Xóa")}
                    </button>
                ` : ""}
            </div>
        </div>
    `;
}

function bind_slot_upload_actions(frm, wrapper) {
    wrapper.find(".import-auto-slot-upload-btn").on("click", function () {
        open_slot_upload_picker(frm, $(this).data("slot-key"));
    });
    wrapper.find('[data-action="upload-others"]').on("click", () => open_upload_picker(frm, "files"));
    wrapper.find(".import-auto-slot-clear-btn").on("click", function () {
        const slot_key = $(this).data("slot-key");
        const slot = (frm.__slot_defs || []).find((s) => s.key === slot_key);
        frappe.confirm(
            __("Xóa file đã upload cho danh mục '{0}'?", [slot ? slot.label : slot_key]),
            () => clear_slot(frm, slot_key)
        );
    });
}

function open_slot_upload_picker(frm, slot_key) {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = ".xlsx,.xls,.csv";
    input.style.display = "none";
    document.body.appendChild(input);
    input.addEventListener("change", () => {
        const file = input.files && input.files[0];
        input.remove();
        if (file) upload_slot_file_to_server(frm, slot_key, file);
    });
    input.click();
}

async function upload_slot_file_to_server(frm, slot_key, file) {
    try {
        if (frm.doc.__islocal || frm.is_dirty()) await frm.save();
        frappe.dom.freeze(__("Đang upload và xử lý file..."));

        const form_data = new FormData();
        form_data.append("docname", frm.doc.name);
        form_data.append("slot_key", slot_key);
        form_data.append("relative_path", file.name);
        form_data.append("file", file, file.name);

        const response = await fetch(`/api/method/${IMPORT_AUTO_API}.upload_slot_file`, {
            method: "POST",
            headers: { "X-Frappe-CSRF-Token": frappe.csrf_token },
            credentials: "same-origin",
            body: form_data,
        });
        const data = await response.json().catch(() => ({}));
        frappe.dom.unfreeze();
        if (!response.ok || data.exc) {
            throw new Error(read_server_error(data) || response.statusText || __("Upload failed."));
        }
        const result = data.message || {};
        frappe.show_alert({
            message: result.error_count
                ? __("Đã xử lý '{0}': {1} an toàn, {2} lỗi.", [result.file_name, result.safe_count || 0, result.error_count])
                : __("Đã xử lý '{0}': {1} dòng an toàn.", [result.file_name, result.safe_count || 0]),
            indicator: result.error_count ? "orange" : "green",
        }, 6);
        await frm.reload_doc();
    } catch (error) {
        frappe.dom.unfreeze();
        frappe.msgprint({
            title: __("Upload thất bại"),
            message: frappe.utils.escape_html(error.message || String(error)),
            indicator: "red",
        });
    }
}

function clear_slot(frm, slot_key) {
    frappe.call({
        method: `${IMPORT_AUTO_API}.clear_slot_file`,
        args: { docname: frm.doc.name, slot_key },
        freeze: true,
        freeze_message: __("Đang xóa..."),
    }).then(() => {
        frappe.show_alert({ message: __("Đã xóa file."), indicator: "green" }, 4);
        frm.reload_doc();
    });
}

/* --------------------------------------------------------------------------
 * Toolbar
 * -------------------------------------------------------------------------- */

function render_toolbar(frm) {
    const is_running = is_import_auto_running(frm);
    const has_folder = Boolean(frm.doc.folder_path);
    const folder_hint = has_folder ? __("Server folder configured ✓") : __("Upload Excel files to create a server folder.");

    return `
        <div class="import-auto-toolbar">
            <div class="import-auto-toolbar__left">
                <div class="import-auto-brand">
                    <div class="import-auto-brand__icon">
                        <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
                        </svg>
                    </div>
                    <div class="import-auto-brand__body">
                        <div class="import-auto-brand__title">${__("Trợ Lý Import Danh Mục (Master Data Import Assistant)")}</div>
                        <div class="import-auto-brand__sub">${__("Upload từng danh mục vào ô tương ứng bên dưới")}</div>
                        <div class="import-auto-brand__path">${frappe.utils.escape_html(folder_hint)}</div>
                    </div>
                </div>
            </div>
            <div class="import-auto-toolbar__right">
                <button class="import-auto-btn import-auto-btn--ghost" data-action="show-advanced" ${is_running ? "disabled" : ""}>
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="3"/>
                        <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
                    </svg>
                    <span>${__("Nâng cao (Advanced)")}</span>
                </button>
            </div>
        </div>
    `;
}

function bind_toolbar(frm, wrapper) {
    wrapper.find('[data-action="show-advanced"]').on("click", () => open_advanced_actions_dialog(frm));
}

function open_advanced_actions_dialog(frm) {
    const status = frm.doc.status || "Draft";
    const is_running = is_import_auto_running(frm);
    const can_analyze = ["Scanned", "Analyzed", "Completed", "Partial"].includes(status);
    const has_folder = Boolean(frm.doc.folder_path);

    const dialog = new frappe.ui.Dialog({
        title: __("Nâng cao (Advanced) — quét cả thư mục bằng AI"),
        fields: [
            {
                fieldtype: "HTML",
                options: `<p class="text-muted" style="margin-bottom: 14px;">
                    ${__("Chỉ dùng khi có file không nằm trong danh sách danh mục cố định ở trên — hệ thống sẽ dùng AI để tự đoán DocType.")}
                </p>`,
            },
        ],
        primary_action_label: __("Đóng"),
        primary_action() { dialog.hide(); },
    });

    const $body = dialog.$body;
    const btn = (action, label, extra_class, disabled) => `
        <button type="button" class="btn btn-sm ${extra_class || "btn-default"}" data-adv-action="${action}" style="width: 100%; margin-bottom: 8px; text-align: left;" ${disabled ? "disabled" : ""}>
            ${label}
        </button>
    `;
    $body.append(`
        <div class="import-auto-advanced-actions">
            ${btn("upload-files", __("Upload Files"), "btn-default", is_running)}
            ${btn("upload-folder", __("Upload Folder"), "btn-default", is_running)}
            ${btn("server-folder", __("Server Folder"), "btn-default", is_running)}
            ${btn("scan", __("Scan Excel Files"), "btn-default", is_running || !has_folder)}
            ${btn("analyze", __("Analyze & Generate AI Script"), "btn-primary", !can_analyze || is_running)}
        </div>
    `);

    $body.find('[data-adv-action="upload-files"]').on("click", () => { dialog.hide(); open_upload_picker(frm, "files"); });
    $body.find('[data-adv-action="upload-folder"]').on("click", () => { dialog.hide(); open_upload_picker(frm, "folder"); });
    $body.find('[data-adv-action="server-folder"]').on("click", () => { dialog.hide(); open_server_folder_dialog(frm); });
    $body.find('[data-adv-action="scan"]').on("click", () => {
        dialog.hide();
        if (frm.doc.__islocal || frm.is_dirty()) {
            frm.save().then(() => call_doc_action(frm, "scan_files", __("Scanning Excel files...")));
            return;
        }
        call_doc_action(frm, "scan_files", __("Scanning Excel files..."));
    });
    $body.find('[data-adv-action="analyze"]').on("click", () => {
        dialog.hide();
        if (frm.doc.__islocal || frm.is_dirty()) {
            frm.save().then(() => call_doc_action(frm, "analyze_files", __("Analyzing files...")));
            return;
        }
        call_doc_action(frm, "analyze_files", __("Analyzing files..."));
    });

    dialog.show();
}

function open_upload_picker(frm, mode) {
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
        confirm_upload_files(frm, files, mode);
    });
    input.click();
}

function confirm_upload_files(frm, files, mode) {
    const excel_files = files.filter(is_excel_upload_file);
    if (!excel_files.length) {
        frappe.msgprint({
            title: __("No Excel Files"),
            message: __("Please choose one or more .xlsx/.xls files."),
            indicator: "orange",
        });
        return;
    }

    const sample_names = excel_files.slice(0, 6)
        .map((file) => `<li>${frappe.utils.escape_html(upload_relative_path(file))}</li>`)
        .join("");
    const hidden_count = Math.max(excel_files.length - 6, 0);
    const dialog = new frappe.ui.Dialog({
        title: mode === "folder" ? __("Upload Folder") : __("Upload Excel Files"),
        fields: [
            {
                fieldtype: "HTML",
                fieldname: "upload_summary",
                options: `
                    <div class="import-auto-upload-summary">
                        <div><strong>${excel_files.length}</strong> ${__("Excel file(s) selected")}</div>
                        <ul>${sample_names}${hidden_count ? `<li>${__("+ {0} more files", [hidden_count])}</li>` : ""}</ul>
                    </div>
                `,
            },
            {
                fieldtype: "Check",
                fieldname: "clear_existing",
                label: __("Replace files in this Import Auto server folder"),
                default: 1,
            },
        ],
        primary_action_label: __("Upload and Scan"),
        primary_action(values) {
            dialog.hide();
            upload_files_to_server(frm, excel_files, Boolean(values.clear_existing));
        },
    });
    dialog.show();
}

function is_excel_upload_file(file) {
    return file && !file.name.startsWith("~$") && /\.(xlsx|xls)$/i.test(file.name || "");
}

function upload_relative_path(file) {
    return file.webkitRelativePath || file.name;
}

async function upload_files_to_server(frm, files, clear_existing) {
    try {
        if (frm.doc.__islocal || frm.is_dirty()) {
            await frm.save();
        }

        frappe.dom.freeze(__("Uploading Excel files to server..."));
        let folder_path = "";
        for (let index = 0; index < files.length; index++) {
            const file = files[index];
            frappe.show_progress(__("Uploading Excel files"), index + 1, files.length, upload_relative_path(file));
            const result = await upload_single_excel_file(frm.doc.name, file, index === 0 && clear_existing);
            folder_path = result.folder_path || folder_path;
        }

        frappe.dom.unfreeze();
        if (frappe.hide_progress) {
            frappe.hide_progress();
        }
        frappe.show_alert({
            message: __("Uploaded {0} Excel file(s) to server folder.", [files.length]),
            indicator: "green",
        }, 5);

        await frm.reload_doc();
        if (folder_path) {
            frm.doc.folder_path = folder_path;
        }
        call_doc_action(frm, "scan_files", __("Scanning uploaded Excel files..."));
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
    }
}

async function upload_single_excel_file(docname, file, clear_existing) {
    const form_data = new FormData();
    form_data.append("docname", docname);
    form_data.append("relative_path", upload_relative_path(file));
    form_data.append("clear_existing", clear_existing ? "1" : "0");
    form_data.append("file", file, file.name);

    const response = await fetch(`/api/method/${IMPORT_AUTO_API}.upload_excel_file`, {
        method: "POST",
        headers: {
            "X-Frappe-CSRF-Token": frappe.csrf_token,
        },
        credentials: "same-origin",
        body: form_data,
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok || data.exc) {
        throw new Error(read_server_error(data) || response.statusText || __("Upload failed."));
    }
    return data.message || {};
}

function read_server_error(data) {
    if (!data) return "";
    if (data._server_messages) {
        try {
            const messages = JSON.parse(data._server_messages).map((message) => {
                const parsed = JSON.parse(message);
                return parsed.message || message;
            });
            return messages.join("<br>");
        } catch (error) {
            return data._server_messages;
        }
    }
    return data.exception || data.exc || "";
}

function open_server_folder_dialog(frm) {
    const open_dialog = () => {
        frappe.call({
            method: `${IMPORT_AUTO_API}.list_server_upload_folders`,
            args: { docname: frm.doc.name },
            freeze: true,
        }).then((response) => {
            const data = response.message || {};
            const folders = data.folders || [];
            if (!folders.length) {
                frappe.msgprint({
                    title: __("No Server Folders"),
                    message: __("Upload Excel files first, then the server folder will appear here."),
                    indicator: "orange",
                });
                return;
            }

            const summary = folders.slice(0, 8)
                .map((folder) => `
                    <li>
                        <strong>${frappe.utils.escape_html(folder.folder_name)}</strong>
                        <span>${folder.file_count || 0} ${__("file(s)")}</span>
                    </li>
                `)
                .join("");
            const dialog = new frappe.ui.Dialog({
                title: __("Select Server Folder"),
                fields: [
                    {
                        fieldtype: "HTML",
                        fieldname: "folder_summary",
                        options: `<div class="import-auto-upload-summary"><ul>${summary}</ul></div>`,
                    },
                    {
                        fieldtype: "Select",
                        fieldname: "folder_name",
                        label: __("Server Folder"),
                        options: folders.map((folder) => folder.folder_name).join("\n"),
                        reqd: 1,
                    },
                    {
                        fieldtype: "Check",
                        fieldname: "scan_after_select",
                        label: __("Scan this folder after selecting"),
                        default: 1,
                    },
                ],
                primary_action_label: __("Use Folder"),
                primary_action(values) {
                    dialog.hide();
                    frappe.call({
                        method: `${IMPORT_AUTO_API}.set_server_upload_folder`,
                        args: {
                            docname: frm.doc.name,
                            folder_name: values.folder_name,
                        },
                        freeze: true,
                    }).then(async () => {
                        await frm.reload_doc();
                        if (values.scan_after_select) {
                            call_doc_action(frm, "scan_files", __("Scanning selected server folder..."));
                        }
                    });
                },
            });
            dialog.show();
        });
    };

    if (frm.doc.__islocal || frm.is_dirty()) {
        frm.save().then(open_dialog);
        return;
    }
    open_dialog();
}

function is_import_auto_running(frm) {
    const status = (frm && frm.doc && frm.doc.status) || "";
    return ["Scanning", "Analyzing", "Importing"].includes(status);
}

/* --------------------------------------------------------------------------
 * Stat cards
 * -------------------------------------------------------------------------- */

function stat_card(icon, tone, label, value, hint, filter_key, active_filter) {
    const is_active = filter_key && active_filter === filter_key;
    const extra_cls = [
        filter_key ? "is-clickable" : "",
        is_active ? "is-active" : "",
    ].filter(Boolean).join(" ");
    const attrs = filter_key ? ` type="button" data-stat-filter="${filter_key}"` : "";
    const tag = filter_key ? "button" : "div";
    return `
        <${tag}${attrs} class="import-auto-stat import-auto-stat--${tone} ${extra_cls}">
            <div class="import-auto-stat__icon">${stat_icon(icon)}</div>
            <div class="import-auto-stat__body">
                <div class="import-auto-stat__value">${frappe.utils.escape_html(String(value))}</div>
                <div class="import-auto-stat__label">${label}</div>
                <div class="import-auto-stat__hint">${hint}</div>
            </div>
        </${tag}>
    `;
}

function stat_icon(name) {
    const icons = {
        file:   '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>',
        check:  '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
        alert:  '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
        upload: '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>',
        warning: '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="7" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    };
    return icons[name] || "";
}

function render_empty() {
    return `
        <div class="import-auto-empty">
            <div class="import-auto-empty__icon">
                <svg viewBox="0 0 24 24" width="44" height="44" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
                </svg>
            </div>
            <div class="import-auto-empty__title">${__("No Files Yet")}</div>
            <div class="import-auto-empty__hint">${__("Click <b>Scan Excel Files</b> to list files in the folder.")}</div>
        </div>
    `;
}

/* --------------------------------------------------------------------------
 * Progress card
 * -------------------------------------------------------------------------- */

function render_progress_panel(frm) {
    const percent = Math.max(0, Math.min(100, Math.round(frm.doc.progress_percent || 0)));
    const processed = frm.doc.processed_files || 0;
    const total = frm.doc.total_files || frm.doc.excel_file_count || 0;
    const message = frm.doc.progress_message || __("Ready to scan or analyze files");
    const current_file = frm.doc.current_file || "";
    const status = frm.doc.status || "Draft";
    const is_running = ["Scanning", "Analyzing", "Importing"].includes(status);
    const status_label = status_indicator(status)[0];

    return `
        <div class="import-auto-progress-card ${is_running ? "is-running" : ""}" data-progress-panel>
            <div class="import-auto-progress-glow"></div>
            <div class="import-auto-progress-head">
                <div class="import-auto-progress-brand">
                    <div class="import-auto-ai-badge">
                        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
                        </svg>
                        <span>${__("IMPORT DANH MỤC AI")}</span>
                    </div>
                    <div class="import-auto-progress-title">${frappe.utils.escape_html(message)}</div>
                    <div class="import-auto-progress-subtitle" data-current-file>${frappe.utils.escape_html(current_file || __("Idle"))}</div>
                </div>
                <div class="import-auto-progress-figures">
                    <div class="import-auto-progress-percent" data-progress-percent>${percent}<small>%</small></div>
                    <div class="import-auto-progress-status-pill" data-progress-status>${is_running ? __("Running") : __("Idle")}</div>
                </div>
            </div>
            <div class="import-auto-progress-track">
                <div class="import-auto-progress-fill" data-progress-fill style="width: ${percent}%"></div>
            </div>
            <div class="import-auto-progress-meta">
                <span class="import-auto-progress-meta__item">
                    <span class="import-auto-progress-meta__dot"></span>
                    <span data-progress-count>${frappe.utils.escape_html(String(processed))}/${frappe.utils.escape_html(String(total))} ${__("files")}</span>
                </span>
                <span class="import-auto-progress-meta__item">${__("Status")}: <b data-progress-label>${frappe.utils.escape_html(status_label)}</b></span>
            </div>
        </div>
    `;
}

function update_progress_panel(frm, data) {
    const wrapper = frm.fields_dict.files_html?.$wrapper;
    if (!wrapper) return;

    const percent = Math.max(0, Math.min(100, Math.round(data.percent || 0)));
    const processed = data.processed || 0;
    const total = data.total || frm.doc.excel_file_count || 0;
    const running = !["complete", "failed"].includes(data.status);

    wrapper.find("[data-progress-percent]").html(`${percent}<small>%</small>`);
    wrapper.find("[data-progress-fill]").css("width", `${percent}%`);
    wrapper.find(".import-auto-progress-title").text(data.message || __("Processing..."));
    wrapper.find("[data-current-file]").text(data.current_file || __("Idle"));
    const status_text = data.status === "queued"
        ? __("Queued")
        : (data.status === "complete" ? __("Complete") : __("Running"));
    wrapper.find("[data-progress-count]").text(`${processed}/${total} ${__("files")}`);
    wrapper.find("[data-progress-status]").text(running ? status_text : __("Idle"));
    wrapper.find(".import-auto-progress-card").toggleClass("is-running", running);
}

/* --------------------------------------------------------------------------
 * Category groups — buckets rows by target_doctype so the page can be
 * reviewed/imported "từng danh mục một" instead of one flat table. Each
 * bucket still renders through the existing render_table()/render_table_row()
 * (unchanged), so every row-level action (Import, AI Resolve, Duplicate
 * check, Reanalyze, Preview, Report, Mark Imported, Delete) keeps working
 * exactly as before — those bind_* functions query the whole wrapper, not
 * a specific <table>.
 * -------------------------------------------------------------------------- */

function group_rows_by_category(rows) {
    const buckets = new Map();
    rows.forEach((row) => {
        const key = category_key(row.target_doctype);
        if (!buckets.has(key)) buckets.set(key, []);
        buckets.get(key).push(row);
    });
    return Array.from(buckets.entries())
        .map(([key, bucket_rows]) => ({
            key,
            target_doctype: key === UNSUPPORTED_CATEGORY_KEY ? null : key,
            meta: category_meta(key === UNSUPPORTED_CATEGORY_KEY ? null : key),
            rows: bucket_rows,
        }))
        .sort((a, b) => a.meta.order - b.meta.order || a.meta.label.localeCompare(b.meta.label));
}

function render_category_groups(frm, rows) {
    const groups = group_rows_by_category(rows);
    frm.__collapsed_categories = frm.__collapsed_categories || new Set();

    const body = groups.map((group) => {
        const total = group.rows.length;
        const safe = group.rows.filter((r) => r.safety_status === "Safe").length;
        const warning = group.rows.filter((r) => r.safety_status === "Warning").length;
        const error = group.rows.filter((r) => r.safety_status === "Error").length;
        const imported = group.rows.filter((r) => ["Imported", "Partial"].includes(r.status)).length;
        const bulk_eligible = group.rows.filter((r) => can_smart_import(r));

        // Auto-collapse fully-imported categories on first render; respect
        // any manual toggle the user has already made this session.
        if (imported === total && total > 0 && !frm.__collapsed_categories_seeded?.has(group.key)) {
            frm.__collapsed_categories.add(group.key);
        }
        frm.__collapsed_categories_seeded = frm.__collapsed_categories_seeded || new Set();
        frm.__collapsed_categories_seeded.add(group.key);
        const is_collapsed = frm.__collapsed_categories.has(group.key);

        const mini_badge = (count, cls, label) => (count
            ? `<span class="import-auto-category-mini import-auto-category-mini--${cls}">${count} ${label}</span>`
            : "");

        return `
            <section class="import-auto-category-card ${is_collapsed ? "is-collapsed" : ""}" data-category="${frappe.utils.escape_html(group.key)}">
                <header class="import-auto-category-header" data-category-toggle>
                    <span class="import-auto-category-icon">${group.meta.icon}</span>
                    <span class="import-auto-category-title">${frappe.utils.escape_html(group.meta.label)}</span>
                    <span class="import-auto-category-count">${total} ${__("file")}</span>
                    <span class="import-auto-category-minis">
                        ${mini_badge(safe, "safe", __("Safe"))}
                        ${mini_badge(warning, "warning", __("Warning"))}
                        ${mini_badge(error, "error", __("Error"))}
                        ${mini_badge(imported, "imported", __("Imported"))}
                    </span>
                    <span class="import-auto-category-actions">
                        ${bulk_eligible.length ? `
                            <button type="button" class="btn btn-xs btn-primary import-auto-category-bulk-btn" data-category-bulk-import="${frappe.utils.escape_html(group.key)}">
                                ${__("Import tất cả ({0}) — Import all", [bulk_eligible.length])}
                            </button>
                        ` : ""}
                        <span class="import-auto-category-chevron">${is_collapsed ? "▸" : "▾"}</span>
                    </span>
                </header>
                <div class="import-auto-category-body" data-category-body ${is_collapsed ? "hidden" : ""}>
                    ${render_table(frm, group.rows)}
                </div>
            </section>
        `;
    }).join("");

    return `<div class="import-auto-category-groups">${body}</div>`;
}

function bind_category_actions(frm, wrapper) {
    wrapper.find("[data-category-toggle]").on("click", function () {
        const card = $(this).closest(".import-auto-category-card");
        const key = card.data("category");
        const was_collapsed = frm.__collapsed_categories.has(key);
        if (was_collapsed) {
            frm.__collapsed_categories.delete(key);
        } else {
            frm.__collapsed_categories.add(key);
        }
        const is_collapsed = !was_collapsed;
        // The body starts hidden via the HTML `hidden` attribute (set by
        // render_category_groups for auto-collapsed categories), not a CSS
        // class. jQuery's .toggle() only flips inline style.display, so on a
        // category that started collapsed via `hidden` it can never actually
        // show again — the attribute keeps forcing display:none regardless
        // of inline style. Set the same `hidden` property here instead.
        card.toggleClass("is-collapsed", is_collapsed);
        card.find("[data-category-body]").prop("hidden", is_collapsed);
        card.find(".import-auto-category-chevron").text(is_collapsed ? "▸" : "▾");
    });

    wrapper.find("[data-category-bulk-import]").on("click", function (e) {
        e.stopPropagation();
        const key = $(this).data("category-bulk-import");
        const target_doctype = key === UNSUPPORTED_CATEGORY_KEY ? null : key;
        run_bulk_import_for_category(frm, target_doctype);
    });
}

/* --------------------------------------------------------------------------
 * Per-category bulk import — replays the exact same single-row "Import"
 * call (run_smart_plan with execute_after_plan) sequentially for every
 * eligible row in one category. No new backend logic: reuses smart_plan_file
 * + smart_execute_file exactly as the per-row Import button does.
 * -------------------------------------------------------------------------- */

function run_bulk_import_for_category(frm, target_doctype) {
    const rows = (frm.doc.files || []).filter(
        (r) => category_key(r.target_doctype) === category_key(target_doctype) && can_smart_import(r)
    );
    if (!rows.length) return;

    frappe.confirm(
        __("Import {0} file Safe/Warning trong danh mục này? — Import {0} eligible file(s) in this category?", [rows.length]),
        () => run_bulk_import_queue(frm, rows)
    );
}

const BULK_IMPORT_ROW_TIMEOUT_MS = 5 * 60 * 1000;

async function run_bulk_import_queue(frm, rows) {
    let done = 0;
    let failed = 0;
    frm.__bulk_import_active = true;
    frappe.show_progress(__("Import Danh Mục"), 0, rows.length, rows[0].file_name);

    try {
        for (const row of rows) {
            const current = (frm.doc.files || []).find((r) => r.name === row.name);
            if (!current || !can_smart_import(current)) { done += 1; continue; }

            frappe.show_progress(__("Import Danh Mục"), done, rows.length, current.file_name);
            try {
                await new Promise((resolve) => {
                    let settled = false;
                    const timer = setTimeout(() => {
                        if (settled) return;
                        settled = true;
                        frm.__bulk_import_row_done = null;
                        failed += 1;
                        resolve();
                    }, BULK_IMPORT_ROW_TIMEOUT_MS);
                    frm.__bulk_import_row_done = (row_name, result) => {
                        if (row_name !== row.name || settled) return;
                        settled = true;
                        clearTimeout(timer);
                        frm.__bulk_import_row_done = null;
                        if (result && result.error) failed += 1;
                        resolve();
                    };
                    run_smart_plan(frm, row.name, null, { execute_after_plan: true });
                });
            } catch (e) {
                failed += 1;
            }
            done += 1;
        }
    } finally {
        frm.__bulk_import_active = false;
        frm.__bulk_import_row_done = null;
    }

    frappe.hide_progress();
    await frm.reload_doc();
    frappe.show_alert({
        message: failed
            ? __("Đã import {0}/{1} file, {2} file lỗi — Imported {0}/{1}, {2} failed.", [done - failed, rows.length, failed])
            : __("Đã import {0} file trong danh mục — Imported {0} file(s) in this category.", [done]),
        indicator: failed ? "orange" : "green",
    }, 6);
}

/* --------------------------------------------------------------------------
 * File table
 * -------------------------------------------------------------------------- */

function render_table(frm, rows) {
    const body = rows.map((row, idx) => render_table_row(row, idx)).join("");

    return `
        <div class="import-auto-table-wrap">
            <table class="import-auto-import-table">
                <colgroup>
                    <col class="col-order" />
                    <col class="col-file" />
                    <col class="col-target" />
                    <col class="col-conf" />
                    <col class="col-status" />
                    <col class="col-action" />
                </colgroup>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>${__("File")}</th>
                        <th>${__("Target DocType")}</th>
                        <th>${__("AI Confidence")}</th>
                        <th>${__("Status")}</th>
                        <th style="text-align: right;">${__("Actions")}</th>
                    </tr>
                </thead>
                <tbody>${body}</tbody>
            </table>
        </div>
    `;
}

function render_table_row(row, idx) {
    const state = row.status === "Reanalyzing"
        ? "reanalyzing"
        : (["Imported", "Partial"].includes(row.status)
            ? (row.status === "Partial" ? "warning" : "imported")
            : (row.safety_status === "Safe"
                ? "safe"
                : (row.safety_status === "Warning"
                    ? "warning"
                    : (row.safety_status === "Error" ? "error" : "pending"))));
    const target = row.target_doctype || "—";
    const import_report = parse_import_report(row.error_detail);
    const reason = import_report ? import_report.summary : (post_import_fallback_reason(row) || row.error_detail || row.analysis_note || "");
    const order = row.import_order || (idx + 1);
    const conf_val = Math.round(row.confidence || 0);
    const conf_tone = conf_val >= 80 ? "high" : (conf_val >= 50 ? "mid" : (conf_val ? "low" : "none"));
    const feedback_history = parse_feedback_history(row.feedback_history_json);
    const feedback_html = (feedback_history.length || row.user_feedback)
        ? `<div class="import-auto-feedback" title="${frappe.utils.escape_html(latest_feedback_text(row, feedback_history))}">
                <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
                <span>${feedback_history.length ? __("{0} feedback", [feedback_history.length]) : __("User feedback added")}</span>
           </div>`
        : "";
    const status_label = vi_status(row.status, row.safety_status);

    return `
        <tr class="import-auto-row import-auto-row--${state}" data-row-name="${frappe.utils.escape_html(row.name)}">
            <td class="import-auto-col-order">
                <span class="import-auto-order-chip">${frappe.utils.escape_html(String(order))}</span>
            </td>
            <td class="import-auto-col-file">
                <div class="import-auto-file">
                    <div class="import-auto-file__icon import-auto-file__icon--${state}">
                        ${state === "reanalyzing" ? `<div class="import-auto-spinner"></div>` : `
                            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                                <polyline points="14 2 14 8 20 8"/>
                            </svg>`}
                    </div>
                    <div class="import-auto-file__body">
                        <button type="button" class="import-auto-file-name import-auto-file-name--link ${state}" data-preview-row-name="${frappe.utils.escape_html(row.name)}" title="${__("Preview Excel File")}" aria-label="${__("Preview Excel File")} ${frappe.utils.escape_html(row.file_name || "")}">
                            ${frappe.utils.escape_html(row.file_name || "")}
                        </button>
                        <div class="import-auto-muted">${frappe.utils.escape_html(row.sheet_name || row.file_path || "")}</div>
                        ${feedback_html}
                    </div>
                </div>
            </td>
            <td class="import-auto-col-target">
                <span class="import-auto-chip import-auto-chip--ghost">${frappe.utils.escape_html(target)}</span>
                ${row.row_count ? `<div class="import-auto-muted">${frappe.utils.escape_html(String(row.row_count))} ${__("rows")}</div>` : ""}
            </td>
            <td class="import-auto-col-conf">
                ${render_confidence(conf_val, conf_tone)}
            </td>
            <td class="import-auto-col-status">
                <span class="import-auto-status-pill ${state}">
                    <span class="import-auto-status-dot"></span>
                    ${frappe.utils.escape_html(status_label)}
                </span>
                ${reason ? `
                    <div class="import-auto-muted import-auto-muted--reason" data-reason-text>${frappe.utils.escape_html(reason)}</div>
                    <span class="import-auto-reason-toggle" data-reason-toggle hidden>${__("Show More")}</span>
                ` : ""}
            </td>
            <td class="import-auto-action-cell">
                ${render_action_cell(row, state)}
            </td>
        </tr>
    `;
}

function render_action_cell(row, state) {
    if (state === "reanalyzing") {
        return `
            <div class="import-auto-action-running">
                <div class="import-auto-spinner import-auto-spinner--sm"></div>
                <span>${__("Reanalyzing...")}</span>
            </div>
        `;
    }

    const can_check = ["Safe", "Warning"].includes(row.safety_status);
    const has_script = has_cached_smart_plan(row);
    const import_report = parse_import_report(row.error_detail);
    const import_issue_count = import_report_issue_count(import_report);
    const is_post_import = ["Imported", "Partial"].includes(row.status);
    const plan_error = (row.smart_plan_status || "") === "Error";
    const can_script_import = can_smart_import(row);
    const script_label = row.status === "Imported"
        ? `✓ ${__("Imported")}`
        : (plan_error
            ? __("Script Error")
            : (row.safety_status === "Warning" ? __("Import (Warning)") : __("Import")));
    const script_btn_class = row.safety_status === "Warning" ? "btn-warning" : "btn-primary";
    const script_title = plan_error
        ? (row.smart_plan_error || __("Cannot generate an import script for this file."))
        : (row.status === "Imported"
            ? __("This file is already imported. Use the report button to review errors/skips.")
            : (has_script
                ? __("Run the generated script; Python will read the full Excel file")
                : __("Use the analysis mapping to build and run the import script.")));
    const report_btn = import_report && import_issue_count
        ? `<button class="import-auto-icon-btn import-auto-report-btn import-auto-report-btn--warning" data-import-report-row="${frappe.utils.escape_html(row.name)}" title="${__("View error/skipped rows")}">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="11" cy="11" r="7"/>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                </svg>
                <span class="import-auto-issue-badge" title="${__("Error/skipped row count")}">${frappe.utils.escape_html(String(import_issue_count))}</span>
            </button>`
        : "";
    const ai_resolution_btn = can_ai_resolution(row)
        ? `<button class="btn btn-sm import-auto-ai-resolve-btn" data-row-name="${frappe.utils.escape_html(row.name)}" title="${__("AI reanalyzes this file and waits for your approval before import")}">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 2v4"/><path d="M12 18v4"/><path d="m4.93 4.93 2.83 2.83"/><path d="m16.24 16.24 2.83 2.83"/><path d="M2 12h4"/><path d="M18 12h4"/><path d="m4.93 19.07 2.83-2.83"/><path d="m16.24 7.76 2.83-2.83"/><circle cx="12" cy="12" r="3"/>
                </svg>
                <span>${__("AI Resolve")}</span>
            </button>`
        : "";
    const dup_count = row.duplicate_match_count || 0;
    const dup_status = row.duplicate_check_status || "Pending";
    const dup_badge = dup_count > 0 ? `<span class="import-auto-dup-badge" title="${__("Exact duplicate row count")}">${dup_count}</span>` : "";
    const dup_title = dup_status === "Warning"
        ? __("Duplicates found - click for details")
        : (dup_status === "Clean" ? __("Checked - no duplicates. Click to rerun.") : __("Check whether data already exists"));
    const dup_btn = can_check && !is_post_import
        ? `<button class="import-auto-icon-btn import-auto-check-dup-btn import-auto-check-dup-btn--${dup_status.toLowerCase()}" data-row-name="${frappe.utils.escape_html(row.name)}" title="${dup_title}">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="11" cy="11" r="7"/>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                </svg>
                ${dup_badge}
            </button>`
        : "";
    const mark_imported_btn = `<button class="import-auto-icon-btn import-auto-mark-imported-btn" data-row-name="${frappe.utils.escape_html(row.name)}" ${row.status === "Imported" ? "disabled" : ""} title="${row.status === "Imported" ? __("Đã import") : __("Đánh dấu đã import thành công")}" aria-label="${__("Đánh dấu đã import thành công")}">
            <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20 6 9 17 4 12"/>
            </svg>
        </button>`;
    const delete_file_btn = `<button class="import-auto-icon-btn import-auto-delete-file-btn" data-row-name="${frappe.utils.escape_html(row.name)}" title="${__("Xóa file này")}" aria-label="${__("Xóa file này")}">
            <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
        </button>`;

    return `
        <div class="import-auto-action-group">
            <button class="btn btn-sm import-auto-import-btn import-auto-smart-btn ${can_script_import ? script_btn_class : "btn-default"}" data-row-name="${frappe.utils.escape_html(row.name)}" ${can_script_import ? "" : "disabled"} title="${frappe.utils.escape_html(script_title)}">
                ${script_label}
            </button>
            ${ai_resolution_btn}
            ${mark_imported_btn}
            ${delete_file_btn}
            ${report_btn}
            ${dup_btn}
            <button class="import-auto-icon-btn import-auto-reanalyze-btn" data-row-name="${frappe.utils.escape_html(row.name)}" title="${__("Reanalyze this file")}">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="23 4 23 10 17 10"/>
                    <polyline points="1 20 1 14 7 14"/>
                    <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
                </svg>
            </button>
        </div>
    `;
}

function can_smart_import(row) {
    if (!row) return false;
    return ["Safe", "Warning"].includes(row.safety_status)
        && row.status !== "Reanalyzing"
        && row.status !== "Imported"
        && row.smart_plan_status !== "Error"
        && Boolean(row.target_doctype);
}

function can_ai_resolution(row) {
    if (!row || row.status === "Reanalyzing" || row.status === "Imported") return false;
    return row.status === "Error"
        || row.safety_status === "Error"
        || row.smart_plan_status === "Error"
        || !row.target_doctype;
}

function has_cached_smart_plan(row) {
    return Boolean(row && row.smart_plan_json && row.smart_plan_status === "Ready");
}

function get_cached_smart_plan(row) {
    if (!has_cached_smart_plan(row)) return null;
    try {
        const plan = typeof row.smart_plan_json === "string"
            ? JSON.parse(row.smart_plan_json)
            : row.smart_plan_json;
        return plan && Array.isArray(plan.steps) && plan.steps.length ? plan : null;
    } catch (error) {
        return null;
    }
}

function vi_status(status, safety) {
    const s = status || safety || "";
    const map = {
        "Imported": "Imported",
        "Safe": "Safe",
        "Warning": "Warning",
        "Error": "Error",
        "Scanned": "Scanned",
        "Analyzed": "Analyzed",
        "Ready": "Ready",
        "Partial": "Partial",
        "Reanalyzing": "Reanalyzing",
        "Data Import Created": "Data Import Draft",
        "Pending": "Pending",
    };
    return __(map[s] || s || "Unknown");
}

function post_import_fallback_reason(row) {
    if (!row || !["Imported", "Partial"].includes(row.status)) return "";
    const detail = String(row.error_detail || "");
    if (detail && !is_duplicate_warning_note(detail)) {
        return detail;
    }
    if (row.status === "Partial") {
        return __("Partial import. Error/skipped rows are in the import report.");
    }
    return "";
}

function is_duplicate_warning_note(text) {
    const value = String(text || "").toLowerCase();
    return value.includes("trùng trong cơ sở dữ liệu")
        || value.includes("dữ liệu trùng")
        || value.includes("khả năng trùng");
}

function parse_feedback_history(history_json) {
    if (!history_json) return [];
    try {
        const history = JSON.parse(history_json);
        return Array.isArray(history) ? history : [];
    } catch (error) {
        return [];
    }
}

function latest_feedback_text(row, history) {
    const latest = history && history.length ? history[history.length - 1] : null;
    return (latest && latest.feedback) || row.user_feedback || "";
}

function render_confidence(value, tone) {
    if (!value) {
        return `<span class="import-auto-muted">—</span>`;
    }
    return `
        <div class="import-auto-conf import-auto-conf--${tone}">
            <div class="import-auto-conf__bar"><span style="width:${value}%"></span></div>
            <div class="import-auto-conf__value">${value}<small>%</small></div>
        </div>
    `;
}

function bind_file_preview_links(frm, wrapper) {
    wrapper.find("[data-preview-row-name]").on("click", function () {
        const row_name = $(this).data("preview-row-name");
        if (!row_name) return;

        frappe.call({
            method: `${IMPORT_AUTO_API}.preview_import_file`,
            args: { docname: frm.doc.name, file_row_name: row_name },
            freeze: true,
            freeze_message: __("Opening preview..."),
        }).then((response) => {
            show_file_preview_dialog(response.message || {}, frm, row_name);
        });
    });
}

/* --------------------------------------------------------------------------
 * Confirm dialog
 * -------------------------------------------------------------------------- */

function bind_reason_toggles(wrapper) {
    wrapper.find("[data-reason-text]").each(function () {
        const $el = $(this);
        const $toggle = $el.next("[data-reason-toggle]");
        const node = $el.get(0);
        if (!node || !$toggle.length) return;
        const is_clamped = node.scrollHeight > node.clientHeight + 2;
        if (is_clamped) {
            $toggle.removeAttr("hidden");
            $toggle.off("click").on("click", function () {
                const expanded = $el.toggleClass("is-expanded").hasClass("is-expanded");
                $toggle.text(expanded ? __("Show Less") : __("Show More"));
            });
        }
    });
}

function parse_import_report(value) {
    if (!value) return null;
    try {
        const parsed = typeof value === "string" ? JSON.parse(value) : value;
        return parsed && parsed.type === "smart_import_execution_report"
            ? normalise_import_report(parsed)
            : null;
    } catch (error) {
        return null;
    }
}

function normalise_import_report(report) {
    if (!report || typeof report !== "object") return null;

    const clean_object = (value) => {
        return value && typeof value === "object" && !Array.isArray(value) ? value : {};
    };

    const steps = Array.isArray(report.steps)
        ? report.steps.map((step) => {
            const clean_step = clean_object(step);
            return {
                ...clean_step,
                errors: Array.isArray(clean_step.errors) ? clean_step.errors : [],
                skipped_rows: Array.isArray(clean_step.skipped_rows) ? clean_step.skipped_rows : [],
                skipped_by_type: clean_object(clean_step.skipped_by_type),
            };
        })
        : [];

    return {
        ...report,
        steps,
        total_skipped_by_type: clean_object(report.total_skipped_by_type),
    };
}

function import_report_issue_count(report) {
    report = normalise_import_report(report);
    if (!report) return 0;

    const explicit = Number(report.total_failed || 0) + Number(report.total_skipped || 0);
    if (Number.isFinite(explicit) && explicit > 0) {
        return explicit;
    }

    return collect_import_report_rows(report, "errors").length
        + collect_import_report_rows(report, "skipped_rows").length;
}

function bind_import_report_buttons(frm, wrapper) {
    wrapper.find("[data-import-report-row]").on("click", function () {
        const row_name = $(this).data("import-report-row");
        const row = (frm.doc.files || []).find((item) => item.name === row_name);
        const report = parse_import_report(row && row.error_detail);
        if (report) {
            show_import_report_dialog(report, {
                frm,
                row_name,
                plan: get_cached_smart_plan(row),
            });
        }
    });
}

function show_import_report_dialog(report, context = {}) {
    report = normalise_import_report(report);
    if (!report) return;

    const first_error = first_import_error(report);
    const first_issue = first_error || first_import_skipped_issue(report);
    const can_ai_fix = Boolean(first_issue && context.frm && context.row_name && context.plan);
    const dialog_config = {
        title: __("Import Row List"),
        size: "extra-large",
        fields: [
            {
                fieldtype: "HTML",
                fieldname: "body",
                options: `${import_auto_styles()}${render_import_report(report)}`,
            },
        ],
        primary_action_label: can_ai_fix ? __("AI Fix & Re-import") : __("Close"),
        primary_action() {
            if (can_ai_fix) {
                dialog.hide();
                run_smart_fix(
                    context.frm,
                    context.row_name,
                    context.plan,
                    error_payload_from_report_row(first_issue),
                    context.parent_dialog || null,
                    { auto_execute: true }
                );
                return;
            }
            dialog.hide();
        },
    };
    if (first_issue) {
        dialog_config.secondary_action_label = __("Manual Fix");
        dialog_config.secondary_action = function () {
            dialog.hide();
            frappe.msgprint({
                title: __("Manual Fix"),
                indicator: "blue",
                message: __("Fix the source Excel row, then reanalyze or re-import this file."),
            });
        };
    }
    const dialog = new frappe.ui.Dialog(dialog_config);
    dialog.show();
}

function first_import_error(report) {
    report = normalise_import_report(report);
    for (const step of ((report && report.steps) || [])) {
        const errors = Array.isArray(step.errors) ? step.errors : [];
        if (errors.length) {
            return {
                ...errors[0],
                step: step.step,
                step_title: step.title,
                target_doctype: step.target_doctype,
            };
        }
    }
    return null;
}

function first_import_skipped_issue(report) {
    const skipped_rows = collect_import_report_rows(report, "skipped_rows");
    if (!skipped_rows.length) return null;
    return skipped_rows.find((row) => row.reason_type !== "duplicate") || skipped_rows[0];
}

function error_payload_from_report_row(row) {
    row = row || {};
    return {
        error: row.error || row.reason || __("Import row failed."),
        failed_step_index: row.step,
        failed_row_index: row.row,
        failed_record: row.record || null,
        error_type: row.error_type || row.reason_type || "",
    };
}

function render_import_report(report) {
    report = normalise_import_report(report);
    if (!report) {
        return `<div class="import-auto-report-empty">${__("Cannot read import row list.")}</div>`;
    }

    const skipped_rows = collect_import_report_rows(report, "skipped_rows");
    const error_rows = collect_import_report_rows(report, "errors");
    const skipped_by_type = report.total_skipped_by_type || {};
    const type_parts = Object.keys(skipped_by_type).map((key) => {
        return `${import_skip_type_label(key)}: ${skipped_by_type[key] || 0}`;
    });

    return `
        <div class="import-auto-report">
            <div class="import-auto-report__summary">
                <div>
                    <div class="import-auto-report__eyebrow">${frappe.utils.escape_html(report.file_name || "")}</div>
                    <div class="import-auto-report__title">${frappe.utils.escape_html(report.summary || "")}</div>
                    ${type_parts.length ? `<div class="import-auto-report__sub">${frappe.utils.escape_html(type_parts.join(" • "))}</div>` : ""}
                </div>
                <div class="import-auto-report__stats">
                    ${report_stat(__("Source Rows"), report.source_rows || 0)}
                    ${report_stat(__("Created"), report.total_inserted || 0)}
                    ${report_stat(__("Skipped"), report.total_skipped || 0)}
                    ${report_stat(__("Errors"), report.total_failed || 0)}
                </div>
            </div>
            ${render_import_report_table(__("Error Rows"), error_rows, "error")}
            ${render_import_report_table(__("Skipped Rows"), skipped_rows, "skipped")}
            ${report_has_truncated_steps(report) ? `<div class="import-auto-report__note">${__("List is limited to {0} rows per step to keep the screen responsive.", [report.detail_limit || 500])}</div>` : ""}
        </div>
    `;
}

function collect_import_report_rows(report, key) {
    const rows = [];
    ((report && report.steps) || []).forEach((step) => {
        const step_rows = Array.isArray(step[key]) ? step[key] : [];
        step_rows.forEach((row) => {
            rows.push({
                step: step.step,
                step_title: step.title || "",
                target_doctype: step.target_doctype || "",
                ...row,
            });
        });
    });
    return rows;
}

function report_has_truncated_steps(report) {
    return ((report && report.steps) || []).some((step) => step.skipped_rows_truncated);
}

function report_stat(label, value) {
    return `
        <div class="import-auto-report-stat">
            <span>${frappe.utils.escape_html(String(label))}</span>
            <b>${frappe.utils.escape_html(String(value))}</b>
        </div>
    `;
}

function render_import_report_table(title, rows, tone) {
    if (!rows.length) {
        return `<div class="import-auto-report-empty">${frappe.utils.escape_html(title)}: ${__("none")}</div>`;
    }

    return `
        <div class="import-auto-report-section import-auto-report-section--${tone}">
            <h5>${frappe.utils.escape_html(title)} (${rows.length})</h5>
            <div class="import-auto-report-table-wrap">
                <table class="table import-auto-report-table">
                    <thead>
                        <tr>
                            <th>${__("Step")}</th>
                            <th>${__("Row")}</th>
                            <th>${__("DocType")}</th>
                            <th>${__("Reason")}</th>
                            <th>${__("Data")}</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${rows.map((row) => `
                            <tr>
                                <td>${frappe.utils.escape_html(String(row.step || ""))}</td>
                                <td>
                                    ${frappe.utils.escape_html(String(row.source_row || row.row || ""))}
                                    ${row.source_row && row.row && row.source_row !== row.row
                                        ? `<div class="import-auto-report-muted">${__("plan")}: ${frappe.utils.escape_html(String(row.row))}</div>`
                                        : ""}
                                </td>
                                <td>${frappe.utils.escape_html(row.target_doctype || "")}</td>
                                <td>
                                    ${frappe.utils.escape_html(row.error || row.reason || "")}
                                    ${row.reason_type ? `<div class="import-auto-report-muted">${frappe.utils.escape_html(import_skip_type_label(row.reason_type))}</div>` : ""}
                                </td>
                                <td><code>${frappe.utils.escape_html(format_report_record(row.record))}</code></td>
                            </tr>
                        `).join("")}
                    </tbody>
                </table>
            </div>
        </div>
    `;
}

function import_skip_type_label(type) {
    const map = {
        duplicate: __("Existing"),
        source_duplicate: __("Duplicate in Source"),
        missing_required: __("Missing Required Data"),
        not_importable: __("Not Importable"),
        total_row: __("Total Row"),
    };
    return map[type] || type || "";
}

function format_report_record(record) {
    if (!record || typeof record !== "object") return "";
    try {
        return JSON.stringify(record);
    } catch (error) {
        return String(record);
    }
}

/* --------------------------------------------------------------------------
 * Duplicate check
 * -------------------------------------------------------------------------- */

function bind_check_duplicate_buttons(frm, wrapper) {
    wrapper.find(".import-auto-check-dup-btn").on("click", function () {
        const row_name = $(this).data("row-name");
        if (!row_name) return;

        frappe.call({
            method: `${IMPORT_AUTO_API}.check_duplicates_file`,
            args: { docname: frm.doc.name, file_row_name: row_name },
            freeze: true,
            freeze_message: __("Checking against database..."),
        }).then((response) => {
            const result = response.message || {};
            if (Object.prototype.hasOwnProperty.call(result, "post_import_report")) {
                if (result.post_import_report) {
                    show_import_report_dialog(result.post_import_report, {
                        frm,
                        row_name,
                        plan: get_cached_smart_plan((frm.doc.files || []).find((r) => r.name === row_name)),
                    });
                } else {
                    frappe.msgprint({
                        title: __("File Imported"),
                        indicator: "blue",
                        message: frappe.utils.escape_html(result.message || __("This file is already imported, so duplicate check is skipped.")),
                    });
                }
                return;
            }
            // Update local row state so UI reflects new safety/dup status without full reload.
            const local = (frm.doc.files || []).find((r) => r.name === row_name);
            if (local) {
                if (result.safety_status) local.safety_status = result.safety_status;
                local.duplicate_check_status = result.duplicate_check_status || "Pending";
                local.duplicate_match_count = (result.report && result.report.total_matches) || 0;
                local.duplicate_report_json = JSON.stringify(result.report || {});
                if (local.safety_status === "Warning") {
                    local.error_detail = (result.report && result.report.note) || local.error_detail;
                }
                render_import_auto_file_list(frm);
            }
            show_duplicate_dialog(result);
        });
    });
}

function show_duplicate_dialog(result) {
    const report = (result && result.report) || {};
    const dialog = new frappe.ui.Dialog({
        title: __("Duplicate Check"),
        size: "large",
        fields: [
            {
                fieldtype: "HTML",
                fieldname: "body",
                options: `${import_auto_styles()}${render_duplicate_report(result, report)}`,
            },
        ],
        primary_action_label: __("Close"),
        primary_action() {
            dialog.hide();
        },
    });
    dialog.show();
}

function render_duplicate_report(result, report) {
    const target = report.target_doctype || result.target_doctype || "—";
    const total = report.total_matches || 0;
    const exact = report.exact_match_count || 0;
    const total_records = report.total_records || 0;
    const samples = Array.isArray(report.samples) ? report.samples : [];
    const note = report.note || (total
        ? __("Exact duplicates found. These rows will be skipped and reported during import.")
        : __("No duplicate records found in the database."));
    const tone = total ? "warning" : "ok";

    const stats = `
        <div class="import-auto-dup-stats">
            <div class="import-auto-dup-stat import-auto-dup-stat--total">
                <span>${__("Total Rows in File")}</span>
                <b>${frappe.utils.escape_html(String(total_records))}</b>
            </div>
            <div class="import-auto-dup-stat import-auto-dup-stat--exact">
                <span>${__("Exact Duplicates")}</span>
                <b>${frappe.utils.escape_html(String(exact))}</b>
            </div>
        </div>
    `;

    const sample_table = samples.length
        ? `
            <div class="import-auto-dup-table-wrap">
                <table class="import-auto-dup-table">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>${__("Type")}</th>
                            <th>${__("Matched Field")}</th>
                            <th>${__("File Value")}</th>
                            <th>${__("Existing Record")}</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${samples.map((sample) => render_duplicate_sample_row(sample, target)).join("")}
                    </tbody>
                </table>
            </div>
        `
        : `<div class="import-auto-dup-empty">${__("No duplicate rows to display.")}</div>`;

    const truncated_note = total > samples.length
        ? `<div class="import-auto-dup-truncated">${__("Showing first {0}/{1} duplicate rows.", [samples.length, total])}</div>`
        : "";

    return `
        <div class="import-auto-dup">
            <div class="import-auto-dup-summary import-auto-dup-summary--${tone}">
                <div class="import-auto-dup-summary__icon">
                    ${tone === "warning"
                        ? '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'
                        : '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>'}
                </div>
                <div class="import-auto-dup-summary__body">
                    <div class="import-auto-dup-summary__title">${__("Checked DocType")}: <b>${frappe.utils.escape_html(target)}</b></div>
                    <div class="import-auto-dup-summary__note">${frappe.utils.escape_html(note)}</div>
                </div>
            </div>
            ${stats}
            ${sample_table}
            ${truncated_note}
        </div>
    `;
}

function render_duplicate_sample_row(sample, target) {
    const match_class = "exact";
    const match_label = __("Exact Duplicate");
    const existing_link = sample.existing_name
        ? `<a class="import-auto-link" href="/app/${encodeURIComponent(slugify_doctype(target))}/${encodeURIComponent(sample.existing_name)}" target="_blank">${frappe.utils.escape_html(sample.existing_label || sample.existing_name)}</a><div class="import-auto-muted">${frappe.utils.escape_html(sample.existing_name)}</div>`
        : "—";
    const matched_value = sample.matched_value != null ? String(sample.matched_value) : "";

    return `
        <tr>
            <td>${frappe.utils.escape_html(String(sample.row_number || ""))}</td>
            <td><span class="import-auto-dup-pill import-auto-dup-pill--${match_class}">${match_label}</span></td>
            <td>${frappe.utils.escape_html(sample.matched_field || "")}</td>
            <td>${frappe.utils.escape_html(matched_value)}</td>
            <td>${existing_link}</td>
        </tr>
    `;
}

function slugify_doctype(doctype) {
    return String(doctype || "").toLowerCase().replace(/\s+/g, "-");
}

/* --------------------------------------------------------------------------
 * Smart import (AI-driven multi-step plan)
 * -------------------------------------------------------------------------- */

function bind_smart_buttons(frm, wrapper) {
    wrapper.find(".import-auto-smart-btn").on("click", function () {
        const row_name = $(this).data("row-name");
        if (!row_name) return;
        const row = (frm.doc.files || []).find((r) => r.name === row_name);
        if (!can_smart_import(row)) {
            frappe.msgprint({
                title: __("Cannot Import Yet"),
                indicator: "orange",
                message: row && row.smart_plan_error
                    ? frappe.utils.escape_html(row.smart_plan_error)
                    : __("This file has no safe mapping or target DocType yet. Reanalyze it and give AI instructions first."),
            });
            return;
        }
        const cached_plan = get_cached_smart_plan(row);
        if (cached_plan) {
            execute_smart_plan(frm, row_name, cached_plan, null);
            return;
        }
        run_smart_plan(frm, row_name, null, { execute_after_plan: true });
    });
}

function bind_ai_resolution_buttons(frm, wrapper) {
    wrapper.find(".import-auto-ai-resolve-btn").on("click", function () {
        const row_name = $(this).data("row-name");
        if (!row_name) return;
        const row = (frm.doc.files || []).find((r) => r.name === row_name);
        if (!can_ai_resolution(row)) return;

        frappe.confirm(
            __("AI will reanalyze this file, suggest DocTypes/steps, and import only after your approval. Continue?"),
            () => {
                run_smart_plan(frm, row_name, ai_resolution_feedback(row), {
                    force_ai_import: true,
                    review_mode: "ai_resolution",
                });
            }
        );
    });
}

function bind_manual_file_action_buttons(frm, wrapper) {
    wrapper.find(".import-auto-mark-imported-btn").on("click", function () {
        const row_name = $(this).data("row-name");
        if (!row_name || $(this).prop("disabled")) return;
        const row = (frm.doc.files || []).find((r) => r.name === row_name);
        const file_name = frappe.utils.escape_html((row && row.file_name) || row_name);

        frappe.confirm(
            __("Đánh dấu file <b>{0}</b> là đã import thành công? Hệ thống sẽ không chạy import cho file này.", [file_name]),
            () => {
                frappe.call({
                    method: `${IMPORT_AUTO_API}.mark_file_imported`,
                    args: { docname: frm.doc.name, file_row_name: row_name },
                    freeze: true,
                    freeze_message: __("Đang đánh dấu đã import..."),
                }).then((response) => {
                    const result = response.message || {};
                    frappe.show_alert({
                        message: result.message || __("Đã đánh dấu đã import."),
                        indicator: "green",
                    }, 5);
                    frm.reload_doc();
                });
            }
        );
    });

    wrapper.find(".import-auto-delete-file-btn").on("click", function () {
        const row_name = $(this).data("row-name");
        if (!row_name) return;
        const row = (frm.doc.files || []).find((r) => r.name === row_name);
        const file_name = frappe.utils.escape_html((row && row.file_name) || row_name);

        frappe.confirm(
            __("Xóa file <b>{0}</b> khỏi server và khỏi danh sách import?", [file_name]),
            () => {
                frappe.call({
                    method: `${IMPORT_AUTO_API}.delete_import_file`,
                    args: { docname: frm.doc.name, file_row_name: row_name },
                    freeze: true,
                    freeze_message: __("Đang xóa file..."),
                }).then((response) => {
                    const result = response.message || {};
                    frappe.show_alert({
                        message: result.message || __("Đã xóa file."),
                        indicator: "green",
                    }, 5);
                    frm.reload_doc();
                });
            }
        );
    });
}

function ai_resolution_feedback(row) {
    const reason = row && (row.error_detail || row.analysis_note || row.smart_plan_error);
    return [
        "File này đang bị phân tích lỗi hoặc chưa xác định được danh mục/DocType.",
        "Hãy phân tích lại headers và sample rows, xác định đúng DocType hoặc chuỗi DocType cần import.",
        "Trả về plan_summary bằng tiếng Việt, nêu rõ hướng xử lý và các bước sẽ tạo.",
        "Nếu đây là bảng kê hóa đơn/chứng từ bán ra, hãy nhận diện là dữ liệu nghiệp vụ bán ra thay vì ép vào master data.",
        "Chỉ tạo kế hoạch an toàn, bỏ qua dòng không đủ dữ liệu và không sửa dữ liệu nguồn quan trọng.",
        reason ? `Lý do lỗi hiện tại: ${reason}` : "",
    ].filter(Boolean).join(" ");
}

function run_smart_plan(frm, row_name, user_feedback, options) {
    options = options || {};
    setup_smart_plan_listener(frm);
    open_smart_progress_dialog(frm, row_name);
    frm.__pending_smart_plan_options = frm.__pending_smart_plan_options || {};
    frm.__pending_smart_plan_options[row_name] = options;
    frappe.call({
        method: `${IMPORT_AUTO_API}.smart_plan_file`,
        args: {
            docname: frm.doc.name,
            file_row_name: row_name,
            user_feedback: user_feedback || null,
            force: options.force_ai_import ? 1 : 0,
        },
    }).then((response) => {
        const result = response.message || {};
        if (result.queued) {
            if (!frm.__smart_progress_dialog) {
                open_smart_progress_dialog(frm, row_name);
            }
            frm.__pending_smart_plan_row = row_name;
            return;
        }
        close_smart_progress_dialog(frm);
        if (result.plan && result.plan.error) {
            if (frm.__bulk_import_active) {
                frm.__bulk_import_row_done && frm.__bulk_import_row_done(row_name, { error: true });
                return;
            }
            frappe.msgprint({
                title: __("Cannot Create Plan"),
                message: frappe.utils.escape_html(result.plan.error),
                indicator: "red",
            });
            return;
        }
        handle_smart_plan_ready(frm, row_name, result);
    }).catch(() => {
        close_smart_progress_dialog(frm);
        if (frm.__pending_smart_plan_options) {
            delete frm.__pending_smart_plan_options[row_name];
        }
        frm.__bulk_import_row_done && frm.__bulk_import_row_done(row_name, { error: true });
    });
}

function setup_smart_plan_listener(frm) {
    if (frm.__smart_plan_listener_bound) return;
    frappe.realtime.on("import_auto_smart_plan", (data) => {
        if (!data || data.docname !== frm.doc.name) return;
        const status = data.status;
        update_smart_progress_dialog(frm, data);
        if (status === "running") return;
        if (status === "failed" || (data.plan && data.plan.error)) {
            close_smart_progress_dialog(frm);
            const failed_row_name = data.row_name || frm.__pending_smart_plan_row;
            if (failed_row_name && frm.__pending_smart_plan_options) {
                delete frm.__pending_smart_plan_options[failed_row_name];
            }
            if (frm.__bulk_import_active) {
                frm.__bulk_import_row_done && frm.__bulk_import_row_done(failed_row_name, { error: true });
                return;
            }
            frappe.msgprint({
                title: __("Cannot Create Plan"),
                message: frappe.utils.escape_html(data.message || (data.plan && data.plan.error) || __("AI failed.")),
                indicator: "red",
            });
            return;
        }
        const row_name = data.row_name || frm.__pending_smart_plan_row;
        if (!row_name) return;
        close_smart_progress_dialog(frm);
        handle_smart_plan_ready(frm, row_name, {
            file_name: data.file_name,
            target_doctype: data.target_doctype,
            plan: data.plan,
        });
    });
    frm.__smart_plan_listener_bound = true;
}

function handle_smart_plan_ready(frm, row_name, payload) {
    const plan = payload && payload.plan;
    const options = (frm.__pending_smart_plan_options || {})[row_name] || {};
    if (frm.__pending_smart_plan_options) {
        delete frm.__pending_smart_plan_options[row_name];
    }
    if (!plan || !Array.isArray(plan.steps) || !plan.steps.length) {
        if (frm.__bulk_import_active) {
            frm.__bulk_import_row_done && frm.__bulk_import_row_done(row_name, { error: true });
            return;
        }
        frappe.msgprint({
            title: __("Cannot Create Plan"),
            message: __("AI did not return a valid import script."),
            indicator: "red",
        });
        return;
    }
    cache_smart_plan_on_row(frm, row_name, plan);
    if (options.execute_after_plan) {
        execute_smart_plan(frm, row_name, plan, null);
        return;
    }
    show_smart_plan_dialog(frm, row_name, {
        ...payload,
        review_mode: options.review_mode || "",
    });
}

function cache_smart_plan_on_row(frm, row_name, plan) {
    const row = (frm.doc.files || []).find((item) => item.name === row_name);
    if (!row) return;
    row.smart_plan_status = "Ready";
    row.smart_plan_json = JSON.stringify(plan);
    row.smart_plan_error = null;
    const target = guess_plan_target_doctype(plan);
    if (target && !row.target_doctype) {
        row.target_doctype = target;
    }
    if (row.safety_status === "Error") {
        row.safety_status = "Warning";
    }
}

function guess_plan_target_doctype(plan) {
    const steps = plan && Array.isArray(plan.steps) ? plan.steps : [];
    const auxiliary_doctypes = new Set([
        "Address", "Contact", "Customer Group", "Supplier Group", "Item Group",
        "UOM", "Brand", "Territory",
    ]);
    const usable_steps = steps.filter((step) => step && step.target_doctype);
    const primary_steps = usable_steps.filter((step) => !auxiliary_doctypes.has(step.target_doctype));
    const picked = primary_steps.length ? primary_steps[primary_steps.length - 1] : usable_steps[0];
    return picked ? picked.target_doctype : "";
}

function smart_progress_stage_label(stage) {
    const map = {
        queued:        __("Queued"),
        reading:       __("Reading Excel File"),
        thinking:      __("Building Mapping"),
        materialising: __("Normalizing Script"),
        complete:      __("Complete"),
        failed:        __("Failed"),
    };
    return map[stage] || __("Processing...");
}

function open_smart_progress_dialog(frm, row_name) {
    if (frm.__smart_progress_dialog) {
        frm.__smart_progress_dialog.show();
        return;
    }

    const dialog = new frappe.ui.Dialog({
        title: __("Preparing Mapping/Script"),
        size: "small",
        fields: [
            {
                fieldtype: "HTML",
                fieldname: "body",
                options: `${import_auto_styles()}${render_smart_progress_panel(0, "queued", __("Preparing..."))}`,
            },
        ],
        primary_action_label: __("Close"),
        primary_action() {
            dialog.hide();
        },
    });
    dialog.$wrapper.find(".btn-primary").addClass("btn-default").removeClass("btn-primary");
    dialog.$wrapper.find(".modal-header .indicator").remove();
    dialog.show();
    // Bootstrap appends this dialog's own backdrop synchronously during
    // show(), before its fade-in transition even starts — grab it now so
    // close_smart_progress_dialog() can remove exactly this backdrop later,
    // deterministically, without waiting on any animation/event.
    dialog.__own_backdrop = $(".modal-backdrop").last();

    frm.__smart_progress_dialog = dialog;
    frm.__pending_smart_plan_row = row_name;
}

function update_smart_progress_dialog(frm, data) {
    const dialog = frm.__smart_progress_dialog;
    if (!dialog) return;
    const percent = Math.max(0, Math.min(100, Math.round(data.percent || 0)));
    const stage = data.stage || (data.status === "running" ? "thinking" : data.status);
    const message = data.message || smart_progress_stage_label(stage);
    dialog.fields_dict.body.$wrapper.html(
        `${import_auto_styles()}${render_smart_progress_panel(percent, stage, message, data.file_name)}`
    );
}

function close_smart_progress_dialog(frm) {
    const dialog = frm.__smart_progress_dialog;
    frm.__smart_progress_dialog = null;
    if (!dialog) return;
    // Close synchronously — do not wait on Bootstrap's async hide
    // transition/'hidden.bs.modal' event. A dialog opened right after this
    // one (e.g. the confirm() in execute_smart_plan) shows up before that
    // transition finishes, and Bootstrap doesn't reliably fire the event
    // once modals stack like that — leaving this dialog (and its backdrop)
    // stuck on screen forever. Instead: hide for Frappe's internal state,
    // then rip out exactly this dialog's own wrapper + backdrop right away.
    try { dialog.hide(); } catch (e) {}
    try { dialog.$wrapper.remove(); } catch (e) {}
    if (dialog.__own_backdrop) {
        try { dialog.__own_backdrop.remove(); } catch (e) {}
    }
    if (!$(".modal:visible").length) {
        $("body").removeClass("modal-open").css({ overflow: "", "padding-right": "" });
    }
}

function render_smart_progress_panel(percent, stage, message, file_name) {
    const stage_label = smart_progress_stage_label(stage);
    const stages = ["queued", "reading", "thinking", "materialising", "complete"];
    const stage_idx = stages.indexOf(stage);
    const is_failed = stage === "failed";
    const is_done = stage === "complete";

    const dots = stages.map((s, idx) => {
        const active = !is_failed && (idx <= stage_idx || is_done);
        const current = !is_failed && idx === stage_idx && !is_done;
        return `<div class="import-auto-smart-progress__dot ${active ? "is-active" : ""} ${current ? "is-current" : ""}" title="${frappe.utils.escape_html(smart_progress_stage_label(s))}"></div>`;
    }).join("");

    return `
        <div class="import-auto-smart-progress ${is_failed ? "is-failed" : ""}">
            <div class="import-auto-smart-progress__head">
                <div class="import-auto-smart-progress__icon ${is_failed ? "is-failed" : ""}">
                    ${is_failed
                        ? `<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="6" y1="6" x2="18" y2="18"/><line x1="6" y1="18" x2="18" y2="6"/></svg>`
                        : (is_done
                            ? `<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>`
                            : `<div class="import-auto-spinner"></div>`)}
                </div>
                <div class="import-auto-smart-progress__body">
                    <div class="import-auto-smart-progress__eyebrow">${__("Mapping")}</div>
                    <div class="import-auto-smart-progress__stage">${frappe.utils.escape_html(stage_label)}</div>
                    ${file_name ? `<div class="import-auto-smart-progress__file">${frappe.utils.escape_html(file_name)}</div>` : ""}
                </div>
                <div class="import-auto-smart-progress__percent">${percent}<small>%</small></div>
            </div>
            <div class="import-auto-smart-progress__track">
                <div class="import-auto-smart-progress__fill" style="width: ${percent}%"></div>
            </div>
            <div class="import-auto-smart-progress__dots">${dots}</div>
            <div class="import-auto-smart-progress__message">${frappe.utils.escape_html(message)}</div>
            <div class="import-auto-smart-progress__hint">${__("If mapping already exists, the system uses cached mapping; AI only reruns when needed.")}</div>
        </div>
    `;
}

function show_smart_plan_dialog(frm, row_name, payload) {
    const plan = (payload && payload.plan) || {};
    const file_name = (payload && payload.file_name) || "";
    const review_mode = payload && payload.review_mode;
    const is_ai_resolution = review_mode === "ai_resolution";
    const dialog = new frappe.ui.Dialog({
        title: is_ai_resolution
            ? __("AI Resolution Proposal - {0}", [file_name])
            : __("Import Mapping/Script - {0}", [file_name]),
        size: "extra-large",
        fields: [
            {
                fieldtype: "HTML",
                fieldname: "body",
                options: `${import_auto_styles()}${render_smart_plan(plan, file_name, review_mode)}`,
            },
            {
                fieldtype: "Small Text",
                fieldname: "user_feedback",
                label: is_ai_resolution
                    ? __("Extra AI instructions before replanning")
                    : __("Extra AI instructions if the plan needs changes"),
                description: is_ai_resolution
                    ? __("If the plan is not correct, add instructions and reanalyze. Accept only when you approve this import plan.")
                    : __("Click Reanalyze after entering instructions so AI can rebuild the plan."),
            },
        ],
        primary_action_label: is_ai_resolution
            ? __("Accept & Import This Plan")
            : __("Run Import Script"),
        primary_action() {
            execute_smart_plan(frm, row_name, plan, dialog);
        },
        secondary_action_label: __("Reanalyze"),
        secondary_action() {
            const feedback = dialog.get_value("user_feedback") || "";
            dialog.hide();
            run_smart_plan(frm, row_name, feedback);
        },
    });
    dialog.$wrapper.find(".btn-primary").prop("disabled", !plan || !plan.steps || !plan.steps.length);
    dialog.show();
}

function render_smart_plan(plan, file_name, review_mode) {
    if (!plan || plan.error) {
        const message = (plan && plan.error) || __("AI did not return a valid plan.");
        return `
            <div class="import-auto-plan import-auto-plan--error">
                <div class="import-auto-plan__title">${__("Cannot Create Plan")}</div>
                <div class="import-auto-plan__message">${frappe.utils.escape_html(message)}</div>
            </div>
        `;
    }

    const steps = Array.isArray(plan.steps) ? plan.steps : [];
    const summary = plan.plan_summary || "";
    const total_records = plan.total_records || 0;
    const total_steps = plan.total_steps || steps.length;
    const is_ai_resolution = review_mode === "ai_resolution";

    return `
        <div class="import-auto-plan">
            <div class="import-auto-plan__header">
                <div>
                    <div class="import-auto-plan__eyebrow">${is_ai_resolution ? __("AI Proposed Resolution") : __("Import Mapping/Script")}</div>
                    <div class="import-auto-plan__title">${frappe.utils.escape_html(file_name || "")}</div>
                </div>
                <div class="import-auto-plan__meta">
                    <span><b>${frappe.utils.escape_html(String(total_steps))}</b> ${__("steps")}</span>
                    <span><b>${frappe.utils.escape_html(String(total_records))}</b> ${__("records processed by Python")}</span>
                </div>
            </div>
            ${summary ? `<div class="import-auto-plan__summary">${frappe.utils.escape_html(summary)}</div>` : ""}
            <div class="import-auto-plan__steps">
                ${steps.map((step) => render_smart_step(step)).join("")}
            </div>
        </div>
    `;
}

function render_smart_step(step) {
    const records = Array.isArray(step.records) ? step.records : [];
    const preview_format = step.preview_format || (step.parent_field ? "tree" : "table");
    const body = preview_format === "tree"
        ? render_smart_tree(records, step)
        : render_smart_table(records, step);

    return `
        <div class="import-auto-plan-step">
            <div class="import-auto-plan-step__head">
                <div class="import-auto-plan-step__index">${frappe.utils.escape_html(String(step.step || ""))}</div>
                <div class="import-auto-plan-step__body">
                    <div class="import-auto-plan-step__title">${frappe.utils.escape_html(step.title || step.target_doctype || "")}</div>
                    <div class="import-auto-plan-step__meta">
                        <span class="import-auto-chip import-auto-chip--ghost">${frappe.utils.escape_html(step.target_doctype || "")}</span>
                        <span class="import-auto-muted">${frappe.utils.escape_html(String(step.record_count || records.length))} ${__("records")}</span>
                        <span class="import-auto-muted">${preview_format === "tree" ? __("Tree") : __("Table")}</span>
                    </div>
                    ${step.description ? `<div class="import-auto-plan-step__desc">${frappe.utils.escape_html(step.description)}</div>` : ""}
                </div>
            </div>
            <div class="import-auto-plan-step__preview">
                ${body}
            </div>
        </div>
    `;
}

function render_smart_table(records, step) {
    if (!records.length) {
        return `<div class="import-auto-plan-empty">${__("No records to preview.")}</div>`;
    }

    const fieldset = new Set();
    records.slice(0, 20).forEach((rec) => {
        Object.keys(rec || {}).forEach((key) => {
            if (key === "doctype") return;
            const value = rec[key];
            if (value === null || value === undefined || value === "") return;
            if (Array.isArray(value)) return;
            fieldset.add(key);
        });
    });
    const fields = Array.from(fieldset).slice(0, 8);
    const display_records = records.slice(0, 20);

    return `
        <div class="import-auto-plan-table-wrap">
            <table class="import-auto-plan-table">
                <thead>
                    <tr>${fields.map((f) => `<th>${frappe.utils.escape_html(f)}</th>`).join("")}</tr>
                </thead>
                <tbody>
                    ${display_records.map((rec) => `
                        <tr>${fields.map((f) => `<td>${frappe.utils.escape_html(format_smart_value(rec[f]))}</td>`).join("")}</tr>
                    `).join("")}
                </tbody>
            </table>
            ${records.length > display_records.length ? `<div class="import-auto-plan-truncated">${__("Showing first {0}/{1} records.", [display_records.length, records.length])}</div>` : ""}
        </div>
    `;
}

function render_smart_tree(records, step) {
    if (!records.length) {
        return `<div class="import-auto-plan-empty">${__("No records to preview.")}</div>`;
    }
    const parent_field = step.parent_field || "parent_account";
    const label_field = step.label_field || guess_label_field(records[0]);
    const key_field = step.unique_key || label_field;

    // Build maps using both potential keys (the "name" and the label).
    const by_key = new Map();
    records.forEach((rec, idx) => {
        const key = rec[key_field] || rec.name || rec[label_field] || `node-${idx}`;
        by_key.set(String(key), { record: rec, children: [], idx });
    });

    const roots = [];
    records.forEach((rec, idx) => {
        const key = String(rec[key_field] || rec.name || rec[label_field] || `node-${idx}`);
        const parent_value = rec[parent_field];
        if (parent_value && by_key.has(String(parent_value))) {
            by_key.get(String(parent_value)).children.push(by_key.get(key));
        } else {
            roots.push(by_key.get(key));
        }
    });

    const render_node = (node, depth) => {
        const rec = node.record;
        const label = rec[label_field] || rec[key_field] || rec.name || "—";
        const detail_pieces = [];
        Object.keys(rec).forEach((field) => {
            if ([label_field, key_field, parent_field, "doctype", "company"].includes(field)) return;
            const value = rec[field];
            if (value === null || value === undefined || value === "") return;
            if (typeof value === "object") return;
            detail_pieces.push(`${field}: ${value}`);
        });
        const detail = detail_pieces.slice(0, 3).join(" · ");
        return `
            <div class="import-auto-plan-tree-node" style="--depth:${depth}">
                <div class="import-auto-plan-tree-row">
                    <span class="import-auto-plan-tree-bullet"></span>
                    <span class="import-auto-plan-tree-label">${frappe.utils.escape_html(String(label))}</span>
                    ${detail ? `<span class="import-auto-plan-tree-detail">${frappe.utils.escape_html(detail)}</span>` : ""}
                </div>
                ${node.children.length ? `<div class="import-auto-plan-tree-children">${node.children.map((child) => render_node(child, depth + 1)).join("")}</div>` : ""}
            </div>
        `;
    };

    return `<div class="import-auto-plan-tree">${roots.map((node) => render_node(node, 0)).join("")}</div>`;
}

function guess_label_field(record) {
    if (!record) return "name";
    const candidates = ["account_name", "item_name", "item_group_name", "customer_name", "supplier_name", "bank_name", "department_name", "warehouse_name", "title", "name"];
    for (const candidate of candidates) {
        if (Object.prototype.hasOwnProperty.call(record, candidate)) return candidate;
    }
    return Object.keys(record)[0] || "name";
}

function format_smart_value(value) {
    if (value === null || value === undefined) return "—";
    if (typeof value === "object") return JSON.stringify(value);
    return String(value);
}

function execute_smart_plan(frm, row_name, plan, dialog, options = {}) {
    const total_records = plan.total_records || 0;
    const run_import = () => {
        setup_smart_execute_listener(frm);
        const progress = open_smart_execute_progress_dialog(frm, row_name, plan);
        set_smart_plan_dialog_busy(dialog, true);
        frm.__pending_smart_execute = frm.__pending_smart_execute || {};
        frm.__pending_smart_execute[row_name] = { plan, dialog, options, progress };
        frappe.call({
            method: `${IMPORT_AUTO_API}.smart_execute_file`,
            args: {
                docname: frm.doc.name,
                file_row_name: row_name,
                plan_json: JSON.stringify(plan),
            },
        }).then((response) => {
            const result = response.message || {};
            if (result.queued) {
        update_smart_execute_progress_dialog(progress, {
                    stage: "queued",
                    status: "running",
                    percent: 2,
                    message: result.message || __("Import script is running in the background..."),
                });
                return;
            }
            handle_smart_execute_result(frm, row_name, plan, dialog, result, options, progress);
        }, (error) => {
            close_smart_execute_progress_dialog(progress);
            set_smart_plan_dialog_busy(dialog, false);
            if (frm.__pending_smart_execute) {
                delete frm.__pending_smart_execute[row_name];
            }
            frappe.msgprint({
                title: __("Import Not Complete"),
                indicator: "red",
                message: frappe.utils.escape_html(smart_import_call_error_message(error)),
            });
        });
    };

    if (options.skip_confirm) {
        run_import();
        return;
    }

    frappe.confirm(
        __("Python will reread Excel and process <b>{0}</b> records across <b>{1}</b> steps. Continue?", [total_records, plan.total_steps]),
        run_import,
        () => cleanup_import_auto_modal_state()
    );
}

function setup_smart_execute_listener(frm) {
    if (frm.__smart_execute_listener_bound) return;
    frappe.realtime.on("import_auto_smart_execute", (data) => {
        if (!data || data.docname !== frm.doc.name) return;
        const row_name = data.row_name;
        const pending = row_name && frm.__pending_smart_execute
            ? frm.__pending_smart_execute[row_name]
            : null;
        if (!pending) return;

        update_smart_execute_progress_dialog(pending.progress, data);
        if (data.status === "running") return;

        handle_smart_execute_result(
            frm,
            row_name,
            pending.plan,
            pending.dialog,
            data.result || { ok: false, error: data.message },
            pending.options || {},
            pending.progress
        );
    });
    frm.__smart_execute_listener_bound = true;
}

function handle_smart_execute_result(frm, row_name, plan, dialog, result, options, progress) {
    if (frm.__pending_smart_execute) {
        delete frm.__pending_smart_execute[row_name];
    }
    close_smart_execute_progress_dialog(progress);
    set_smart_plan_dialog_busy(dialog, false);
    try {
        result = result || {};
        if (result.ok) {
            if (frm.__smart_fix_retry_count) {
                delete frm.__smart_fix_retry_count[row_name];
            }
            if (dialog) dialog.hide();
            const report = result.import_report || null;
            const skipped = report ? (report.total_skipped || 0) : (result.total_skipped || 0);
            const failed = report ? (report.total_failed || 0) : (result.total_failed || 0);
            update_local_row_after_smart_import(frm, row_name, result, report);
            frappe.show_alert({
                message: skipped || failed
                        ? __("Created {0}, skipped {1}, failed {2} rows across {3} steps.", [
                        result.total_inserted || 0,
                        skipped,
                        failed,
                        (result.results || []).length,
                    ])
                    : __("Created {0} records across {1} steps.", [
                        result.total_inserted || 0,
                        (result.results || []).length,
                    ]),
                indicator: "green",
            });
            // Bulk-import mode (see run_bulk_import_queue) suppresses the
            // per-row report dialog and per-row reload so N sequential rows
            // don't stack N modals — the caller shows one aggregate summary
            // and reloads once at the end of the batch.
            if (report && (skipped || failed) && !frm.__bulk_import_active) {
                try {
                    show_import_report_dialog(report, {
                        frm,
                        row_name,
                        plan,
                        parent_dialog: dialog,
                    });
                } catch (report_error) {
                    console.error("Import Auto report render failed", report_error);
                    frappe.show_alert({
                        message: __("Import finished but report could not be opened. Reload and use the row list button."),
                        indicator: "orange",
                    }, 8);
                }
                frm.__bulk_import_row_done && frm.__bulk_import_row_done(row_name, result);
                return;
            }
            frm.__bulk_import_row_done && frm.__bulk_import_row_done(row_name, result);
            if (!frm.__bulk_import_active) frm.reload_doc();
            return;
        }

        if (frm.__bulk_import_active) {
            frm.__bulk_import_row_done && frm.__bulk_import_row_done(row_name, { ...result, error: true });
            return;
        }

        if (should_auto_fix_smart_error(frm, row_name, result, options)) {
            frappe.show_alert({
                message: __("Import paused at an error row. AI is fixing it and will continue."),
                indicator: "orange",
            }, 6);
            run_smart_fix(
                frm,
                row_name,
                plan,
                smart_error_payload_from_result(result),
                dialog,
                { auto_execute: true }
            );
        } else {
            show_smart_error_dialog(frm, row_name, plan, result, dialog);
        }
    } catch (ui_error) {
        console.error("Import Auto success handler failed", ui_error);
        frm.__bulk_import_row_done && frm.__bulk_import_row_done(row_name, { error: true });
        if (frm.__bulk_import_active) return;
        frappe.show_alert({
            message: __("Import finished, but UI did not update immediately. Reloading form."),
            indicator: "orange",
        }, 8);
        frm.reload_doc();
    }
}

function update_local_row_after_smart_import(frm, row_name, result, report) {
    const row = (frm.doc.files || []).find((item) => item.name === row_name);
    if (!row) return;

    const skipped = report ? (report.total_skipped || 0) : (result.total_skipped || 0);
    const failed = report ? (report.total_failed || 0) : (result.total_failed || 0);
    row.status = skipped || failed ? "Partial" : "Imported";
    row.imported_records = result.total_inserted || 0;
    row.failed_records = failed;
    if (report && (skipped || failed)) {
        row.error_detail = JSON.stringify(report);
    } else {
        row.error_detail = null;
    }
    render_import_auto_file_list(frm);
}

function smart_import_call_error_message(error) {
    if (!error) {
        return __("Connection interrupted or server returned an error. Check Import Log before retrying.");
    }
    if (error._server_messages) {
        try {
            const messages = JSON.parse(error._server_messages)
                .map((item) => JSON.parse(item).message)
                .filter(Boolean);
            if (messages.length) return messages.join("\n");
        } catch (parse_error) {}
    }
    return error.message || error.statusText || __("Connection interrupted or server returned an error. Check Import Log before retrying.");
}

function smart_error_payload_from_result(result) {
    result = result || {};
    return {
        error: result.error || __("An error occurred during import."),
        failed_step_index: result.failed_step_index,
        failed_row_index: result.failed_row_index,
        failed_record: result.failed_record || null,
        error_type: result.error_type || "",
    };
}

function should_auto_fix_smart_error(frm, row_name, result, options = {}) {
    if (options.auto_fix_on_partial === false) return false;
    if (
        !result
        || !result.can_resume
        || !["failed_row_only", "failed_rows_only"].includes(result.rollback_scope)
    ) return false;

    const retry_count = (frm.__smart_fix_retry_count && frm.__smart_fix_retry_count[row_name]) || 0;
    return retry_count < SMART_FIX_MAX_RETRY;
}

function set_smart_plan_dialog_busy(dialog, busy) {
    if (!dialog || !dialog.$wrapper) return;
    dialog.$wrapper.find(".modal-footer .btn-primary")
        .prop("disabled", !!busy)
        .toggleClass("disabled", !!busy)
        .text(busy ? __("Importing...") : __("Run Import Script"));
    dialog.$wrapper.find(".modal-footer .btn-secondary")
        .prop("disabled", !!busy)
        .toggleClass("disabled", !!busy);
}

function open_smart_execute_progress_dialog(frm, row_name, plan) {
    const row = (frm.doc.files || []).find((item) => item.name === row_name) || {};
    const state = {
        started_at: Date.now(),
        row_name,
        file_name: row.file_name || "",
        plan: plan || {},
        percent: 0,
        stage: "queued",
        status: "running",
        message: "",
        timer: null,
        dialog: null,
    };

    const dialog = new frappe.ui.Dialog({
        title: __("Importing into DCNET"),
        size: "large",
        fields: [
            {
                fieldtype: "HTML",
                fieldname: "body",
                options: `${import_auto_styles()}${render_smart_execute_progress_panel(state)}`,
            },
        ],
        primary_action_label: __("Running..."),
        primary_action() {},
    });
    dialog.show();
    dialog.$wrapper.find(".modal-footer .btn-primary").prop("disabled", true).addClass("disabled");
    // See open_smart_progress_dialog — captured so close_smart_execute_progress_dialog
    // can remove exactly this dialog's own backdrop deterministically.
    dialog.__own_backdrop = $(".modal-backdrop").last();
    state.dialog = dialog;
    state.timer = setInterval(() => update_smart_execute_progress_dialog(state), 1000);
    return state;
}

function update_smart_execute_progress_dialog(state, data) {
    if (state && data) {
        state.percent = Math.max(0, Math.min(100, Math.round(data.percent || state.percent || 0)));
        state.stage = data.stage || state.stage || "executing";
        state.status = data.status || state.status || "running";
        state.message = data.message || state.message || "";
        if (data.file_name) state.file_name = data.file_name;
        [
            "current_step",
            "current_step_title",
            "target_doctype",
            "step_processed",
            "step_total",
            "total_processed",
            "total_records",
            "inserted",
            "skipped",
            "failed",
            "batch_size",
        ].forEach((key) => {
            if (Object.prototype.hasOwnProperty.call(data, key)) {
                state[key] = data[key];
            }
        });
    }
    if (!state || !state.dialog || !state.dialog.fields_dict || !state.dialog.fields_dict.body) return;
    state.dialog.fields_dict.body.$wrapper.html(
        `${import_auto_styles()}${render_smart_execute_progress_panel(state)}`
    );
}

function close_smart_execute_progress_dialog(state) {
    if (!state) return;
    if (state.timer) clearInterval(state.timer);
    const dialog = state.dialog;
    if (!dialog) return;
    // See close_smart_progress_dialog — close synchronously, don't wait on
    // Bootstrap's async hide transition/event, which can stall indefinitely
    // once a second dialog is shown on top before it finishes.
    try { dialog.hide(); } catch (e) {}
    try { dialog.$wrapper.remove(); } catch (e) {}
    if (dialog.__own_backdrop) {
        try { dialog.__own_backdrop.remove(); } catch (e) {}
    }
    if (!$(".modal:visible").length) {
        $("body").removeClass("modal-open").css({ overflow: "", "padding-right": "" });
    }
}

function cleanup_import_auto_modal_state(attempt = 0) {
    setTimeout(() => {
        const visible_modals = $(".modal.show:visible, .modal.in:visible").length;
        if (visible_modals) {
            if (attempt < 5) {
                cleanup_import_auto_modal_state(attempt + 1);
            }
            return;
        }

        $(".modal-backdrop").remove();
        $("body")
            .removeClass("modal-open")
            .css({
                overflow: "",
                "padding-right": "",
            });

        if (frappe.dom && frappe.dom.unfreeze) {
            frappe.dom.unfreeze();
        }
    }, attempt ? 150 : 350);
}

function render_smart_execute_progress_panel(state) {
    const plan = state.plan || {};
    const steps = Array.isArray(plan.steps) ? plan.steps : [];
    const total_steps = plan.total_steps || steps.length || 0;
    const total_records = plan.total_records || steps.reduce((sum, step) => sum + (step.record_count || (step.records || []).length || 0), 0);
    const total_processed = Math.max(0, Number(state.total_processed || 0));
    const live_total_records = Math.max(total_records, Number(state.total_records || 0));
    const inserted = Math.max(0, Number(state.inserted || 0));
    const skipped = Math.max(0, Number(state.skipped || 0));
    const failed = Math.max(0, Number(state.failed || 0));
    const step_processed = Math.max(0, Number(state.step_processed || 0));
    const step_total = Math.max(0, Number(state.step_total || 0));
    const elapsed_seconds = Math.max(0, Math.floor((Date.now() - state.started_at) / 1000));
    const messages = [
        __("Checking data and links before writing."),
        __("Creating records in DCNET in plan order."),
        __("Processing dependencies such as groups, UOMs, and addresses."),
        __("Background job is still running. Large files may take a few minutes."),
    ];
    const message = state.message || messages[Math.floor(elapsed_seconds / 5) % messages.length];
    const percent = Math.max(0, Math.min(100, Math.round(state.percent || 0)));
    const visible_steps = steps.slice(0, 6);
    const hidden_steps = Math.max(0, steps.length - visible_steps.length);

    return `
        <div class="import-auto-execute-progress">
            <div class="import-auto-execute-progress__head">
                <div class="import-auto-execute-progress__icon">
                    <div class="import-auto-spinner"></div>
                </div>
                <div class="import-auto-execute-progress__title-wrap">
                    <div class="import-auto-execute-progress__eyebrow">${__("Python Import Script")}</div>
                    <div class="import-auto-execute-progress__title">${__("Reading Excel and importing into DCNET")}</div>
                    ${state.file_name ? `<div class="import-auto-execute-progress__file">${frappe.utils.escape_html(state.file_name)}</div>` : ""}
                </div>
                <div class="import-auto-execute-progress__live">
                    <span class="import-auto-execute-progress__live-dot"></span>
                    ${__("Running")}
                </div>
            </div>

            <div class="import-auto-execute-progress__bar">
                <div class="import-auto-execute-progress__bar-fill" style="width: ${percent || 18}%"></div>
            </div>

            <div class="import-auto-execute-progress__stats">
                <div class="import-auto-execute-stat">
                    <span>${__("Time")}</span>
                    <b>${frappe.utils.escape_html(format_elapsed_time(elapsed_seconds))}</b>
                </div>
                <div class="import-auto-execute-stat">
                    <span>${__("Plan")}</span>
                    <b>${frappe.utils.escape_html(String(total_steps))} ${__("steps")}</b>
                </div>
                <div class="import-auto-execute-stat">
                    <span>${__("Data")}</span>
                    <b>${frappe.utils.escape_html(String(total_processed))}/${frappe.utils.escape_html(String(live_total_records || total_records))} ${__("records")}</b>
                </div>
            </div>

            <div class="import-auto-execute-live-grid">
                <div class="import-auto-execute-live import-auto-execute-live--inserted">
                    <span>${__("Created")}</span>
                    <b>${frappe.utils.escape_html(String(inserted))}</b>
                </div>
                <div class="import-auto-execute-live import-auto-execute-live--skipped">
                    <span>${__("Skipped")}</span>
                    <b>${frappe.utils.escape_html(String(skipped))}</b>
                </div>
                <div class="import-auto-execute-live import-auto-execute-live--failed">
                    <span>${__("Errors")}</span>
                    <b>${frappe.utils.escape_html(String(failed))}</b>
                </div>
                <div class="import-auto-execute-live">
                    <span>${__("Batch realtime")}</span>
                    <b>${frappe.utils.escape_html(String(state.batch_size || 200))} ${__("rows")}</b>
                </div>
            </div>

            ${(state.current_step || step_total) ? `
                <div class="import-auto-execute-current">
                    <div class="import-auto-execute-current__head">
                        <b>${__("Current Step")}: ${frappe.utils.escape_html(String(state.current_step || ""))}</b>
                        <span>${frappe.utils.escape_html(String(state.target_doctype || ""))}</span>
                    </div>
                    <div class="import-auto-execute-current__title">${frappe.utils.escape_html(state.current_step_title || "")}</div>
                    <div class="import-auto-execute-current__track">
                        <div style="width:${step_total ? Math.max(3, Math.min(100, Math.round((step_processed / step_total) * 100))) : 0}%"></div>
                    </div>
                    <small>${frappe.utils.escape_html(String(step_processed))}/${frappe.utils.escape_html(String(step_total))} ${__("records in step")}</small>
                </div>
            ` : ""}

            <div class="import-auto-execute-progress__message">
                <span class="import-auto-execute-progress__message-dot"></span>
                <span>${frappe.utils.escape_html(message)}</span>
            </div>

            ${visible_steps.length ? `
                <div class="import-auto-execute-steps">
                    <div class="import-auto-execute-steps__title">${__("Steps are running sequentially")}</div>
                    ${visible_steps.map((step, index) => render_smart_execute_step(step, index)).join("")}
                    ${hidden_steps ? `<div class="import-auto-execute-steps__more">${__("+ {0} more steps", [hidden_steps])}</div>` : ""}
                </div>
            ` : ""}

            <div class="import-auto-execute-progress__hint">
                ${__("Import is running as a background job. Keep this screen open for realtime results.")}
            </div>
        </div>
    `;
}

function render_smart_execute_step(step, index) {
    const title = step.title || __("Step {0}", [index + 1]);
    const target = step.target_doctype || "—";
    const count = step.record_count || (step.records || []).length || 0;
    return `
        <div class="import-auto-execute-step">
            <span class="import-auto-execute-step__index">${frappe.utils.escape_html(String(index + 1))}</span>
            <span class="import-auto-execute-step__body">
                <b>${frappe.utils.escape_html(title)}</b>
                <small>${frappe.utils.escape_html(target)} · ${frappe.utils.escape_html(String(count))} ${__("records")}</small>
            </span>
        </div>
    `;
}

function format_elapsed_time(total_seconds) {
    const minutes = Math.floor(total_seconds / 60);
    const seconds = total_seconds % 60;
    return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}


function bind_reanalyze_buttons(frm, wrapper) {
    wrapper.find(".import-auto-reanalyze-btn").on("click", function () {
        const row_name = $(this).data("row-name");
        if (!row_name) return;
        const row = (frm.doc.files || []).find((r) => r.name === row_name);
        if (!row) return;
        show_reanalyze_dialog(frm, row);
    });
}

function show_reanalyze_dialog(frm, row) {
    const target = row.target_doctype || "—";
    const dialog = new frappe.ui.Dialog({
        title: __("Reanalyze File"),
        fields: [
            {
                fieldtype: "HTML",
                fieldname: "intro",
                options: `
                    ${import_auto_styles()}
                    <div class="import-auto-confirm">
                        <div class="import-auto-confirm__row">
                            <span class="import-auto-confirm__label">${__("File")}</span>
                            <span class="import-auto-confirm__value">${frappe.utils.escape_html(row.file_name || "")}</span>
                        </div>
                        <div class="import-auto-confirm__row">
                            <span class="import-auto-confirm__label">${__("Current DocType")}</span>
                            <span class="import-auto-confirm__value"><span class="import-auto-chip import-auto-chip--ghost">${frappe.utils.escape_html(target)}</span></span>
                        </div>
                    </div>
                    ${render_feedback_history(row)}
                `,
            },
            {
                fieldtype: "Small Text",
                fieldname: "user_feedback",
                label: __("Your Feedback for AI"),
                description: __("Describe what AI analyzed incorrectly so it can adjust."),
                reqd: 1,
                default: row.user_feedback || "",
            },
        ],
        primary_action_label: __("Send to AI for Reanalysis"),
        primary_action(values) {
            const feedback = (values.user_feedback || "").trim();
            if (!feedback) {
                frappe.msgprint(__("Please enter feedback so AI knows what to adjust."));
                return;
            }
            dialog.hide();
            frappe.call({
                method: `${IMPORT_AUTO_API}.reanalyze_file`,
                args: {
                    docname: frm.doc.name,
                    file_row_name: row.name,
                    user_feedback: feedback,
                },
            }).then((response) => {
                const message = response.message || {};
                frappe.show_alert({
                    message: __("Reanalysis request sent."),
                    indicator: "blue",
                });
                // Optimistically mark row as Reanalyzing
                const target_row = (frm.doc.files || []).find((r) => r.name === row.name);
                if (target_row) {
                    target_row.status = "Reanalyzing";
                    target_row.user_feedback = feedback;
                    if (message.feedback_log_entry) {
                        const history = parse_feedback_history(target_row.feedback_history_json);
                        history.push(message.feedback_log_entry);
                        target_row.feedback_history_json = JSON.stringify(history);
                    }
                }
                render_import_auto_file_list(frm);
            });
        },
    });
    dialog.show();
}

function render_feedback_history(row) {
    const history = parse_feedback_history(row.feedback_history_json);
    if (!history.length) {
        return `
            <div class="import-auto-chat import-auto-chat--empty">
                <div class="import-auto-chat__title">${__("Feedback History")}</div>
                <div class="import-auto-chat__empty">${__("No feedback for this file yet.")}</div>
            </div>
        `;
    }

    return `
        <div class="import-auto-chat">
            <div class="import-auto-chat__title">
                <span>${__("Feedback History")}</span>
                <span class="import-auto-chat__count">${history.length}</span>
            </div>
            <div class="import-auto-chat__log">
                ${history.map((entry, index) => render_feedback_entry(entry, index)).join("")}
            </div>
        </div>
    `;
}

function render_feedback_entry(entry, index) {
    const user_name = entry.user_name || entry.user || __("User");
    const feedback_time = format_feedback_time(entry.created_on);
    const response_time = format_feedback_time(entry.responded_on);
    const response = entry.ai_response || __("AI is reanalyzing with this feedback...");
    const status_class = feedback_entry_status_class(entry.status);
    const target_after = entry.target_doctype_after || entry.target_doctype_before || "";
    const confidence = Math.round(entry.confidence_after || 0);

    return `
        <div class="import-auto-chat-entry import-auto-chat-entry--${status_class}">
            <div class="import-auto-chat-entry__meta">
                <span>${frappe.utils.escape_html(__("Attempt {0}", [index + 1]))}</span>
                <span>${frappe.utils.escape_html(feedback_time)}</span>
            </div>
            <div class="import-auto-chat-bubble import-auto-chat-bubble--user">
                <div class="import-auto-chat-bubble__head">
                    <span>${frappe.utils.escape_html(user_name)}</span>
                    <span>${frappe.utils.escape_html(history_status_label(entry.status))}</span>
                </div>
                <div class="import-auto-chat-bubble__body">${frappe.utils.escape_html(entry.feedback || "")}</div>
            </div>
            <div class="import-auto-chat-bubble import-auto-chat-bubble--ai">
                <div class="import-auto-chat-bubble__head">
                    <span>AI</span>
                    <span>${response_time ? frappe.utils.escape_html(response_time) : frappe.utils.escape_html(__("Pending"))}</span>
                </div>
                <div class="import-auto-chat-bubble__body">${frappe.utils.escape_html(response)}</div>
                ${(target_after || confidence) ? `
                    <div class="import-auto-chat-result">
                        ${target_after ? `<span>${frappe.utils.escape_html(target_after)}</span>` : ""}
                        ${confidence ? `<span>${confidence}%</span>` : ""}
                    </div>
                ` : ""}
            </div>
        </div>
    `;
}

function feedback_entry_status_class(status) {
    if (status === "Failed" || status === "Error") return "error";
    if (status === "Running") return "running";
    return "done";
}

function history_status_label(status) {
    const map = {
        Running: __("Analyzing"),
        Ready: __("Ready"),
        Error: __("Error"),
        Failed: __("Failed"),
    };
    return map[status] || status || __("Complete");
}

function format_feedback_time(value) {
    if (!value) return "";
    try {
        if (frappe.datetime && frappe.datetime.str_to_user) {
            return frappe.datetime.str_to_user(value);
        }
    } catch (error) {
        return String(value);
    }
    return String(value);
}

function show_file_preview_dialog(preview, frm, row_name) {
    const dialog = new frappe.ui.Dialog({
        title: __("Review Excel File"),
        size: "extra-large",
        fields: [
            {
                fieldtype: "HTML",
                fieldname: "preview",
                options: `
                    ${import_auto_styles()}
                    ${render_file_preview(preview)}
                `,
            },
        ],
        primary_action_label: __("Close"),
        primary_action() {
            dialog.hide();
        },
    });

    if (
        frm
        && row_name
        && ["Safe", "Warning"].includes(preview.safety_status)
        && preview.target_doctype
        && preview.status !== "Imported"
    ) {
        dialog.set_secondary_action_label(__("Import"));
        dialog.set_secondary_action(() => {
            dialog.hide();
            const row = (frm.doc.files || []).find((item) => item.name === row_name);
            const cached_plan = get_cached_smart_plan(row);
            if (cached_plan) {
                execute_smart_plan(frm, row_name, cached_plan, null);
                return;
            }
            run_smart_plan(frm, row_name, null, { execute_after_plan: true });
        });
    }

    dialog.show();
}

function render_file_preview(preview) {
    const sheets = preview.sheets || [];
    const confidence = Math.round(preview.confidence || 0);
    const status_label = vi_status(preview.status, preview.safety_status);
    const status_class = preview_status_class(preview.status, preview.safety_status);
    const import_report = parse_import_report(preview.error_detail);
    const note = import_report ? import_report.summary : (preview.error_detail || preview.analysis_note || "");

    return `
        <div class="import-auto-preview">
            <div class="import-auto-preview__header">
                <div>
                    <div class="import-auto-preview__eyebrow">${__("Excel Preview")}</div>
                    <div class="import-auto-preview__title">${frappe.utils.escape_html(preview.file_name || "")}</div>
                    <div class="import-auto-preview__path">${frappe.utils.escape_html(preview.file_path || "")}</div>
                </div>
                <div class="import-auto-preview__meta">
                    <span class="import-auto-chip import-auto-chip--ghost">${frappe.utils.escape_html(preview.target_doctype || __("Unknown"))}</span>
                    <span class="import-auto-status-pill ${status_class}">
                        <span class="import-auto-status-dot"></span>
                        ${frappe.utils.escape_html(status_label)}
                    </span>
                </div>
            </div>
            <div class="import-auto-preview__stats">
                ${preview_stat(__("Sheet"), sheets.length || "—")}
                ${preview_stat(__("Rows"), preview.row_count || "—")}
                ${preview_stat(__("Confidence"), confidence ? `${confidence}%` : "—")}
                ${preview_stat(__("Preview"), `${preview.preview_row_limit || 0} ${__("rows/sheet")}`)}
            </div>
            ${note ? `<div class="import-auto-preview__note">${frappe.utils.escape_html(note)}</div>` : ""}
            ${import_report ? render_import_report(import_report) : ""}
            ${sheets.length ? sheets.map((sheet) => render_sheet_preview(sheet)).join("") : render_no_preview()}
        </div>
    `;
}

function preview_status_class(status, safety) {
    if (status === "Imported") return "imported";
    if (status === "Partial") return "warning";
    if (safety === "Safe") return "safe";
    if (safety === "Error" || status === "Error" || status === "Failed") return "error";
    return "pending";
}

function preview_stat(label, value) {
    return `
        <div class="import-auto-preview-stat">
            <span>${frappe.utils.escape_html(String(label))}</span>
            <b>${frappe.utils.escape_html(String(value))}</b>
        </div>
    `;
}

function render_sheet_preview(sheet) {
    const rows = sheet.sample_rows || [];
    const headers = preview_headers(sheet, rows);

    return `
        <section class="import-auto-preview-sheet">
            <div class="import-auto-preview-sheet__head">
                <div>
                    <h4>${frappe.utils.escape_html(sheet.sheet_name || __("Sheet"))}</h4>
                    <p>
                        ${__("Header Row")} ${frappe.utils.escape_html(String(sheet.detected_header_row || "—"))}
                        · ${frappe.utils.escape_html(String(sheet.max_row || 0))} ${__("rows")}
                        · ${frappe.utils.escape_html(String(sheet.max_column || 0))} ${__("columns")}
                    </p>
                </div>
            </div>
            ${rows.length && headers.length ? render_preview_table(headers, rows) : render_no_preview()}
        </section>
    `;
}

function preview_headers(sheet, rows) {
    const detected = (sheet.detected_headers || [])
        .map((header, index) => String(header || `column_${index + 1}`))
        .filter(Boolean);

    if (detected.length) return detected;
    if (!rows.length) return [];

    return Object.keys(rows[0] || {});
}

function render_preview_table(headers, rows) {
    const head = headers.map((header) => `<th>${frappe.utils.escape_html(header)}</th>`).join("");
    const body = rows.map((row) => {
        const cells = headers.map((header) => {
            const value = row[header];
            return `<td>${frappe.utils.escape_html(format_preview_cell(value))}</td>`;
        }).join("");
        return `<tr>${cells}</tr>`;
    }).join("");

    return `
        <div class="import-auto-preview-table-wrap">
            <table class="import-auto-preview-table">
                <thead><tr>${head}</tr></thead>
                <tbody>${body}</tbody>
            </table>
        </div>
    `;
}

function format_preview_cell(value) {
    if (value === null || value === undefined) return "";
    if (typeof value === "object") return JSON.stringify(value);
    return String(value);
}

function render_no_preview() {
    return `
        <div class="import-auto-preview-empty">
            ${__("No preview data for this sheet.")}
        </div>
    `;
}

/* --------------------------------------------------------------------------
 * Styles
 * -------------------------------------------------------------------------- */

function import_auto_styles() {
    const existing_style = document.getElementById("import-auto-import-css");
    if (existing_style) {
        existing_style.remove();
    }
    const style = document.createElement("style");
    style.id = "import-auto-import-css";
    style.textContent = `
            .import-auto-import-shell {
                width: 100%;
                min-width: 0;
                border: 1px solid var(--border-color);
                border-radius: 14px;
                overflow: hidden;
                background: var(--card-bg);
                box-shadow: 0 18px 40px rgba(15, 23, 42, 0.06);
            }

            /* === Toolbar === */
            .import-auto-toolbar {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 16px;
                padding: 16px 20px;
                background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
                border-bottom: 1px solid var(--border-color);
                flex-wrap: wrap;
            }
            .import-auto-brand { display: flex; align-items: center; gap: 12px; }
            .import-auto-brand__icon {
                width: 42px; height: 42px;
                border-radius: 12px;
                display: flex; align-items: center; justify-content: center;
                color: #fff;
                background: linear-gradient(135deg, #6366f1, #8b5cf6 60%, #ec4899);
                box-shadow: 0 8px 18px rgba(99, 102, 241, .35);
            }
            .import-auto-brand__title {
                font-size: 16px; font-weight: 700;
                color: var(--text-color);
                line-height: 1.2;
            }
            .import-auto-brand__sub {
                font-size: 12px;
                color: var(--text-muted);
                margin-top: 2px;
            }
            .import-auto-brand__path {
                max-width: min(720px, 70vw);
                margin-top: 6px;
                padding: 5px 8px;
                border-radius: 6px;
                background: #eef2f7;
                color: #475569;
                font-size: 11px;
                line-height: 1.35;
                overflow-wrap: anywhere;
            }
            .import-auto-toolbar__right {
                display: inline-flex; gap: 8px;
                flex-wrap: wrap;
                justify-content: flex-end;
            }
            .import-auto-btn {
                display: inline-flex; align-items: center; gap: 8px;
                padding: 9px 16px;
                border-radius: 10px;
                font-size: 13px; font-weight: 600;
                border: 1px solid transparent;
                cursor: pointer;
                transition: transform .12s ease, box-shadow .15s ease, background .15s ease;
                line-height: 1;
            }
            .import-auto-btn:active { transform: translateY(1px); }
            .import-auto-btn[disabled] { opacity: .55; cursor: not-allowed; pointer-events: none; }
            .import-auto-btn--ghost {
                background: #fff;
                color: var(--text-color);
                border-color: var(--border-color);
            }
            .import-auto-btn--ghost:hover {
                background: #f8fafc;
                box-shadow: 0 6px 14px rgba(15, 23, 42, .06);
            }
            .import-auto-btn--primary {
                color: #fff;
                background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 60%, #ec4899 100%);
                box-shadow: 0 10px 22px rgba(99, 102, 241, .35);
            }
            .import-auto-btn--primary:hover {
                box-shadow: 0 14px 26px rgba(99, 102, 241, .45);
                filter: brightness(1.04);
            }
            .import-auto-upload-summary {
                color: var(--text-color);
                font-size: 13px;
                line-height: 1.45;
            }
            .import-auto-upload-summary ul {
                margin: 10px 0 0;
                padding-left: 18px;
                color: var(--text-muted);
                overflow-wrap: anywhere;
            }
            .import-auto-upload-summary li + li {
                margin-top: 4px;
            }
            .import-auto-upload-summary li span {
                margin-left: 6px;
                color: var(--text-muted);
                font-size: 12px;
            }

            /* === Progress card === */
            .import-auto-progress-card {
                position: relative;
                padding: 22px 24px 18px;
                color: #f8fafc;
                background:
                    radial-gradient(120% 180% at 0% 0%, rgba(99,102,241,.45) 0%, transparent 55%),
                    radial-gradient(120% 180% at 100% 0%, rgba(16,185,129,.35) 0%, transparent 55%),
                    linear-gradient(135deg, #0f172a 0%, #1e293b 60%, #0b1220 100%);
                overflow: hidden;
                border-bottom: 1px solid rgba(255,255,255,.04);
            }
            .import-auto-progress-glow {
                position: absolute; inset: -40% -10% auto -10%;
                height: 140%;
                background: radial-gradient(60% 60% at 50% 0%, rgba(99,102,241,.35), transparent 60%);
                pointer-events: none;
            }
            .import-auto-progress-head {
                position: relative; z-index: 1;
                display: flex; gap: 16px;
                align-items: flex-start;
                justify-content: space-between;
                margin-bottom: 14px;
                flex-wrap: wrap;
            }
            .import-auto-ai-badge {
                display: inline-flex; align-items: center; gap: 6px;
                padding: 4px 10px;
                border-radius: 999px;
                background: rgba(255,255,255,.10);
                color: #e2e8f0;
                font-size: 11px; font-weight: 700;
                letter-spacing: .08em;
                backdrop-filter: blur(6px);
                margin-bottom: 8px;
            }
            .import-auto-progress-title {
                font-weight: 700; font-size: 16px;
                color: #f8fafc;
                line-height: 1.35;
            }
            .import-auto-progress-subtitle {
                color: rgba(226, 232, 240, .72);
                font-size: 12px;
                margin-top: 4px;
                overflow-wrap: anywhere;
            }
            .import-auto-progress-figures {
                text-align: right;
                display: flex; flex-direction: column; align-items: flex-end; gap: 6px;
            }
            .import-auto-progress-percent {
                font-size: 32px; line-height: 1;
                font-weight: 800;
                color: #fff;
                letter-spacing: -0.02em;
            }
            .import-auto-progress-percent small {
                font-size: 14px; opacity: .7; margin-left: 1px;
            }
            .import-auto-progress-status-pill {
                font-size: 11px; font-weight: 600;
                color: #a7f3d0;
                background: rgba(16,185,129,.16);
                border: 1px solid rgba(16,185,129,.35);
                padding: 2px 10px; border-radius: 999px;
            }
            .import-auto-progress-card.is-running .import-auto-progress-status-pill {
                color: #fde68a;
                background: rgba(245, 158, 11, .14);
                border-color: rgba(245, 158, 11, .4);
            }
            .import-auto-progress-track {
                position: relative; z-index: 1;
                height: 8px;
                border-radius: 999px;
                background: rgba(255,255,255,.08);
                overflow: hidden;
            }
            .import-auto-progress-fill {
                height: 100%;
                width: 0%;
                border-radius: inherit;
                background: linear-gradient(90deg, #6366f1 0%, #22d3ee 50%, #10b981 100%);
                box-shadow: 0 0 12px rgba(99, 102, 241, .55);
                transition: width .3s ease;
                position: relative;
            }
            .import-auto-progress-card.is-running .import-auto-progress-fill::after {
                content: "";
                position: absolute; inset: 0;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,.45), transparent);
                animation: import-auto-shimmer 1.6s linear infinite;
            }
            @keyframes import-auto-shimmer {
                0% { transform: translateX(-100%); }
                100% { transform: translateX(100%); }
            }
            .import-auto-progress-meta {
                position: relative; z-index: 1;
                display: flex; justify-content: space-between; gap: 12px;
                margin-top: 10px;
                color: rgba(226, 232, 240, .7);
                font-size: 12px;
                flex-wrap: wrap;
            }
            .import-auto-progress-meta b { color: #f1f5f9; font-weight: 600; }
            .import-auto-progress-meta__item { display: inline-flex; align-items: center; gap: 6px; }
            .import-auto-progress-meta__dot {
                width: 8px; height: 8px; border-radius: 50%;
                background: #22d3ee;
                box-shadow: 0 0 0 3px rgba(34, 211, 238, .25);
            }
            .import-auto-progress-card.is-running .import-auto-progress-meta__dot {
                animation: import-auto-pulse 1.2s ease-in-out infinite;
            }
            @keyframes import-auto-pulse {
                0%, 100% { opacity: 1; transform: scale(1); }
                50%      { opacity: .55; transform: scale(.85); }
            }

            /* === Stat cards === */
            .import-auto-import-summary {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 12px;
                padding: 16px 20px;
                border-bottom: 1px solid var(--border-color);
                background: var(--bg-light-gray, #f8fafc);
            }
            .import-auto-stat {
                display: flex; align-items: center; gap: 12px;
                padding: 14px 16px;
                background: var(--card-bg);
                border: 1px solid var(--border-color);
                border-radius: 12px;
                transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;
                text-align: left;
            }
            .import-auto-stat.is-clickable { cursor: pointer; }
            .import-auto-stat.is-clickable:hover {
                transform: translateY(-1px);
                box-shadow: 0 8px 18px rgba(15, 23, 42, .08);
            }
            .import-auto-stat.is-active {
                border-color: currentColor;
                box-shadow: 0 0 0 2px currentColor;
                transform: translateY(-1px);
            }
            .import-auto-stat--amber.is-active  { color: #b45309; }
            .import-auto-stat--green.is-active  { color: #059669; }
            .import-auto-stat--red.is-active    { color: #dc2626; }
            .import-auto-stat--blue.is-active   { color: #2563eb; }
            .import-auto-stat--indigo.is-active { color: #4f46e5; }

            /* === Filter bar === */
            .import-auto-filter-bar {
                display: flex; align-items: center; justify-content: space-between;
                padding: 7px 14px;
                background: rgba(59,130,246,.07);
                border: 1px solid rgba(59,130,246,.22);
                border-radius: 8px;
                font-size: 12.5px;
                color: var(--text-color);
            }
            .import-auto-filter-bar__label {
                display: flex; align-items: center; gap: 6px;
            }
            .import-auto-filter-bar__clear {
                background: none; border: none; cursor: pointer;
                font-size: 12px; color: var(--text-muted);
                padding: 2px 6px; border-radius: 4px;
                transition: background .12s, color .12s;
            }
            .import-auto-filter-bar__clear:hover {
                background: rgba(0,0,0,.06); color: var(--text-color);
            }
            .import-auto-stat__icon {
                width: 42px; height: 42px;
                border-radius: 11px;
                display: flex; align-items: center; justify-content: center;
                flex-shrink: 0;
            }
            .import-auto-stat--indigo .import-auto-stat__icon { background: rgba(99,102,241,.12); color: #4f46e5; }
            .import-auto-stat--green  .import-auto-stat__icon { background: rgba(16,185,129,.12); color: #059669; }
            .import-auto-stat--red    .import-auto-stat__icon { background: rgba(239,68,68,.12);  color: #dc2626; }
            .import-auto-stat--blue   .import-auto-stat__icon { background: rgba(59,130,246,.12); color: #2563eb; }
            .import-auto-stat__body { min-width: 0; }
            .import-auto-stat__value {
                font-size: 24px; font-weight: 700; line-height: 1.1;
                color: var(--text-color);
                letter-spacing: -0.01em;
            }
            .import-auto-stat__label {
                font-size: 13px; font-weight: 600;
                color: var(--text-color);
                margin-top: 2px;
            }
            .import-auto-stat__hint {
                font-size: 11px;
                color: var(--text-muted);
                margin-top: 1px;
            }

            /* === Table === */
            .import-auto-table-wrap {
                width: 100%;
                overflow-x: hidden;
            }
            .import-auto-import-table {
                width: 100%;
                border-collapse: separate;
                border-spacing: 0;
                table-layout: fixed;
            }
            .import-auto-import-table col.col-order  { width: 44px; }
            .import-auto-import-table col.col-file   { width: auto; }
            .import-auto-import-table col.col-target { width: 118px; }
            .import-auto-import-table col.col-conf   { width: 90px; }
            .import-auto-import-table col.col-status { width: 188px; }
            .import-auto-import-table col.col-action { width: 264px; }
            .import-auto-import-table td.import-auto-col-file,
            .import-auto-import-table td.import-auto-col-target,
            .import-auto-import-table td.import-auto-col-status { overflow: hidden; }
            .import-auto-import-table td.import-auto-col-target .import-auto-chip { white-space: normal; word-break: break-word; }
            .import-auto-import-table th,
            .import-auto-import-table td {
                padding: 14px 12px;
                border-bottom: 1px solid var(--border-color);
                vertical-align: middle;
            }
            .import-auto-import-table th {
                font-size: 11px;
                color: var(--text-muted);
                background: var(--bg-light-gray, #f8fafc);
                text-transform: uppercase;
                letter-spacing: .04em;
                font-weight: 600;
                border-bottom: 1px solid var(--border-color);
            }
            .import-auto-row { transition: background-color .15s ease; }
            .import-auto-row:hover { background: rgba(99, 102, 241, .03); }
            .import-auto-row:last-child td { border-bottom: 0; }

            .import-auto-order-chip {
                display: inline-flex; align-items: center; justify-content: center;
                min-width: 26px; height: 26px;
                padding: 0 7px;
                border-radius: 8px;
                background: var(--bg-light-gray, #f1f5f9);
                color: var(--text-muted);
                font-size: 12px; font-weight: 600;
            }
            .import-auto-file { display: flex; gap: 12px; align-items: flex-start; }
            .import-auto-file__icon {
                width: 38px; height: 38px;
                border-radius: 10px;
                display: flex; align-items: center; justify-content: center;
                flex-shrink: 0;
            }
            .import-auto-file__icon--safe     { background: rgba(16,185,129,.12); color: #059669; }
            .import-auto-file__icon--error    { background: rgba(239,68,68,.12);  color: #dc2626; }
            .import-auto-file__icon--imported { background: rgba(59,130,246,.12); color: #2563eb; }
            .import-auto-file__icon--pending  { background: var(--bg-light-gray, #f1f5f9); color: var(--text-muted); }
            .import-auto-file__body { min-width: 0; flex: 1; }
            .import-auto-file-name {
                font-weight: 600;
                color: var(--text-color);
                overflow-wrap: anywhere;
                word-break: break-word;
                white-space: normal;
                display: block;
                width: 100%;
            }
            .import-auto-file-name--link {
                display: inline;
                padding: 0;
                border: 0;
                background: transparent;
                text-align: left;
                cursor: pointer;
                color: #1d4ed8;
                line-height: 1.35;
                transition: color .15s ease, text-decoration-color .15s ease;
                text-decoration: underline;
                text-decoration-color: transparent;
                text-underline-offset: 3px;
                overflow-wrap: anywhere;
            }
            .import-auto-file-name--link:hover,
            .import-auto-file-name--link:focus-visible {
                color: #4338ca;
                text-decoration-color: currentColor;
            }
            .import-auto-file-name--link:focus-visible {
                outline: 2px solid rgba(67, 56, 202, .35);
                outline-offset: 3px;
                border-radius: 4px;
            }
            .import-auto-muted {
                color: var(--text-muted);
                font-size: 12px;
                margin-top: 3px;
                overflow-wrap: break-word;
                word-break: normal;
            }
            .import-auto-muted--reason {
                display: -webkit-box;
                -webkit-line-clamp: 3;
                -webkit-box-orient: vertical;
                overflow: hidden;
                overflow-wrap: anywhere;
                line-height: 1.45;
                margin-top: 6px;
                cursor: help;
            }
            .import-auto-muted--reason.is-expanded {
                display: block;
                -webkit-line-clamp: unset;
            }
            .import-auto-reason-toggle {
                display: inline-block;
                margin-top: 4px;
                font-size: 11px;
                font-weight: 600;
                color: #4f46e5;
                cursor: pointer;
                user-select: none;
            }
            .import-auto-reason-toggle:hover { text-decoration: underline; }
            .import-auto-link {
                font-size: 12px;
                color: #2563eb;
                margin-top: 3px;
                display: inline-block;
                text-decoration: none;
            }
            .import-auto-link:hover { text-decoration: underline; }
            .import-auto-report-link {
                border: 0;
                background: transparent;
                padding: 0;
                cursor: pointer;
                font-weight: 600;
            }
            .import-auto-report {
                margin-top: 12px;
            }
            .import-auto-report__summary {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                gap: 16px;
                padding: 14px 16px;
                border: 1px solid var(--border-color);
                border-radius: 8px;
                background: #f8fafc;
                flex-wrap: wrap;
            }
            .import-auto-report__eyebrow {
                color: var(--text-muted);
                font-size: 11px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: .04em;
                margin-bottom: 4px;
                overflow-wrap: anywhere;
            }
            .import-auto-report__title {
                font-size: 14px;
                font-weight: 700;
                color: var(--text-color);
            }
            .import-auto-report__sub,
            .import-auto-report__note {
                margin-top: 6px;
                color: var(--text-muted);
                font-size: 12px;
            }
            .import-auto-report__stats {
                display: grid;
                grid-template-columns: repeat(4, minmax(82px, 1fr));
                gap: 8px;
                min-width: 360px;
            }
            .import-auto-report-stat {
                padding: 8px 10px;
                border: 1px solid var(--border-color);
                border-radius: 7px;
                background: #fff;
            }
            .import-auto-report-stat span {
                display: block;
                color: var(--text-muted);
                font-size: 11px;
            }
            .import-auto-report-stat b {
                color: var(--text-color);
                font-size: 16px;
            }
            .import-auto-report-section {
                margin-top: 14px;
            }
            .import-auto-report-section h5 {
                margin: 0 0 8px;
                font-size: 13px;
                font-weight: 700;
            }
            .import-auto-report-table-wrap {
                max-height: 420px;
                overflow: auto;
                border: 1px solid var(--border-color);
                border-radius: 8px;
            }
            .import-auto-report-table {
                margin: 0;
                font-size: 12px;
            }
            .import-auto-report-table th {
                position: sticky;
                top: 0;
                background: #f8fafc;
                z-index: 1;
            }
            .import-auto-report-table code {
                white-space: normal;
                overflow-wrap: anywhere;
                color: #334155;
                background: #f1f5f9;
            }
            .import-auto-report-muted,
            .import-auto-report-empty {
                color: var(--text-muted);
                font-size: 11px;
            }
            .import-auto-report-empty {
                margin-top: 10px;
            }

            .import-auto-chip {
                display: inline-flex; align-items: center;
                padding: 4px 10px;
                border-radius: 7px;
                font-size: 12px;
                font-weight: 500;
            }
            .import-auto-chip--ghost {
                background: var(--bg-light-gray, #f1f5f9);
                color: var(--text-color);
                border: 1px solid var(--border-color);
            }

            /* Confidence */
            .import-auto-conf { display: flex; flex-direction: column; gap: 4px; }
            .import-auto-conf__bar {
                height: 6px;
                border-radius: 999px;
                background: var(--bg-light-gray, #f1f5f9);
                overflow: hidden;
            }
            .import-auto-conf__bar > span {
                display: block;
                height: 100%;
                border-radius: inherit;
                transition: width .3s ease;
            }
            .import-auto-conf--high .import-auto-conf__bar > span { background: linear-gradient(90deg, #10b981, #34d399); }
            .import-auto-conf--mid  .import-auto-conf__bar > span { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
            .import-auto-conf--low  .import-auto-conf__bar > span { background: linear-gradient(90deg, #ef4444, #f87171); }
            .import-auto-conf__value { font-size: 12px; font-weight: 600; color: var(--text-color); }
            .import-auto-conf__value small { font-size: 10px; opacity: .65; margin-left: 1px; }

            /* Status pill */
            .import-auto-status-pill {
                display: inline-flex; align-items: center; gap: 6px;
                padding: 4px 10px;
                border-radius: 999px;
                font-size: 12px; font-weight: 600;
                white-space: nowrap;
            }
            .import-auto-status-dot {
                width: 6px; height: 6px; border-radius: 50%;
                background: currentColor;
            }
            .import-auto-status-pill.safe     { background: rgba(16,185,129,.12); color: #047857; }
            .import-auto-status-pill.warning  { background: rgba(245,158,11,.16); color: #b45309; }
            .import-auto-status-pill.error    { background: rgba(239,68,68,.12);  color: #b91c1c; }
            .import-auto-status-pill.imported { background: rgba(59,130,246,.12); color: #1d4ed8; }
            .import-auto-status-pill.pending  { background: var(--bg-light-gray, #f1f5f9); color: var(--text-muted); }
            .import-auto-row--warning { background: rgba(245,158,11,.04); }
            .import-auto-stat--amber { color: #b45309; }
            .import-auto-stat--amber .import-auto-stat__icon { background: rgba(245,158,11,.12); }

            .import-auto-dup-badge {
                position: absolute; top: -4px; right: -4px;
                min-width: 16px; height: 16px;
                padding: 0 4px;
                border-radius: 999px;
                background: #b45309; color: #fff;
                font-size: 10px; font-weight: 700;
                display: inline-flex; align-items: center; justify-content: center;
                line-height: 1;
            }
            .import-auto-icon-btn { position: relative; }
            .import-auto-check-dup-btn--warning { color: #b45309; border-color: rgba(245,158,11,.4); background: rgba(245,158,11,.08); }
            .import-auto-check-dup-btn--clean   { color: #047857; }
            .import-auto-report-btn--warning {
                color: #b45309;
                border-color: rgba(245,158,11,.4);
                background: rgba(245,158,11,.08);
            }
            .import-auto-issue-badge {
                position: absolute; top: -4px; right: -4px;
                min-width: 16px; height: 16px;
                padding: 0 4px;
                border-radius: 999px;
                background: #b45309; color: #fff;
                font-size: 10px; font-weight: 700;
                display: inline-flex; align-items: center; justify-content: center;
                line-height: 1;
            }

            .import-auto-dup { display: flex; flex-direction: column; gap: 14px; }
            .import-auto-dup-summary {
                display: flex; gap: 12px; align-items: flex-start;
                padding: 12px 14px;
                border-radius: 10px;
                border: 1px solid var(--border-color);
            }
            .import-auto-dup-summary--warning {
                background: rgba(245,158,11,.08);
                border-color: rgba(245,158,11,.35);
                color: #92400e;
            }
            .import-auto-dup-summary--ok {
                background: rgba(16,185,129,.08);
                border-color: rgba(16,185,129,.35);
                color: #065f46;
            }
            .import-auto-dup-summary__title { font-weight: 600; font-size: 14px; }
            .import-auto-dup-summary__note  { margin-top: 4px; font-size: 13px; line-height: 1.45; }
            .import-auto-dup-stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
                gap: 8px;
            }
            .import-auto-dup-stat {
                padding: 10px 12px;
                background: #fff;
                border: 1px solid var(--border-color);
                border-radius: 8px;
            }
            .import-auto-dup-stat span { display: block; font-size: 11px; color: var(--text-muted); font-weight: 600; }
            .import-auto-dup-stat b    { display: block; margin-top: 3px; font-size: 16px; font-weight: 700; color: var(--text-color); }
            .import-auto-dup-stat--exact b { color: #b45309; }

            .import-auto-dup-table-wrap { border: 1px solid var(--border-color); border-radius: 8px; overflow: auto; max-height: 360px; }
            .import-auto-dup-table { width: 100%; border-collapse: separate; border-spacing: 0; font-size: 12px; }
            .import-auto-dup-table th, .import-auto-dup-table td { padding: 8px 10px; border-bottom: 1px solid var(--border-color); border-right: 1px solid var(--border-color); text-align: left; vertical-align: top; }
            .import-auto-dup-table th:last-child, .import-auto-dup-table td:last-child { border-right: 0; }
            .import-auto-dup-table tr:last-child td { border-bottom: 0; }
            .import-auto-dup-table th { position: sticky; top: 0; background: #f8fafc; color: var(--text-muted); font-weight: 700; }
            .import-auto-dup-pill { display: inline-flex; align-items: center; padding: 2px 8px; border-radius: 999px; font-size: 11px; font-weight: 700; }
            .import-auto-dup-pill--exact { background: rgba(180,83,9,.14); color: #92400e; }
            .import-auto-dup-empty { padding: 20px; text-align: center; color: var(--text-muted); font-size: 13px; }
            .import-auto-dup-truncated { font-size: 12px; color: var(--text-muted); text-align: right; }
            .import-auto-icon-btn.import-auto-smart-btn { color: #4f46e5; }
            .import-auto-icon-btn.import-auto-smart-btn:hover { background: rgba(79,70,229,.08); border-color: rgba(79,70,229,.4); }

            .import-auto-plan { display: flex; flex-direction: column; gap: 14px; }
            .import-auto-plan__header { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; flex-wrap: wrap; }
            .import-auto-plan__eyebrow { font-size: 11px; font-weight: 700; color: var(--text-muted); letter-spacing: .04em; text-transform: uppercase; }
            .import-auto-plan__title { font-size: 16px; font-weight: 700; color: var(--text-color); margin-top: 4px; overflow-wrap: anywhere; }
            .import-auto-plan__meta { display: inline-flex; gap: 14px; flex-wrap: wrap; align-items: center; color: var(--text-muted); font-size: 12px; }
            .import-auto-plan__meta b { color: var(--text-color); font-weight: 700; margin-right: 4px; }
            .import-auto-plan__summary { padding: 12px 14px; border-radius: 10px; background: rgba(79,70,229,.06); border: 1px solid rgba(79,70,229,.2); color: #312e81; font-size: 13px; line-height: 1.5; white-space: pre-wrap; }

            .import-auto-plan__steps { display: flex; flex-direction: column; gap: 12px; }
            .import-auto-plan-step { border: 1px solid var(--border-color); border-radius: 12px; background: #fff; overflow: hidden; }
            .import-auto-plan-step__head { display: flex; gap: 12px; padding: 12px 14px; background: var(--bg-light-gray, #f8fafc); border-bottom: 1px solid var(--border-color); align-items: flex-start; }
            .import-auto-plan-step__index { width: 28px; height: 28px; border-radius: 999px; background: linear-gradient(135deg, #6366f1, #8b5cf6); color: #fff; font-weight: 700; display: inline-flex; align-items: center; justify-content: center; flex-shrink: 0; }
            .import-auto-plan-step__title { font-weight: 700; color: var(--text-color); font-size: 14px; }
            .import-auto-plan-step__meta { display: inline-flex; gap: 10px; align-items: center; flex-wrap: wrap; margin-top: 4px; }
            .import-auto-plan-step__desc { margin-top: 6px; color: var(--text-muted); font-size: 12px; line-height: 1.45; }
            .import-auto-plan-step__preview { padding: 12px 14px; background: #fff; }

            .import-auto-plan-table-wrap { overflow: auto; max-height: 320px; border: 1px solid var(--border-color); border-radius: 8px; }
            .import-auto-plan-table { width: 100%; border-collapse: separate; border-spacing: 0; font-size: 12px; }
            .import-auto-plan-table th, .import-auto-plan-table td { padding: 8px 10px; border-right: 1px solid var(--border-color); border-bottom: 1px solid var(--border-color); text-align: left; vertical-align: top; }
            .import-auto-plan-table th:last-child, .import-auto-plan-table td:last-child { border-right: 0; }
            .import-auto-plan-table tr:last-child td { border-bottom: 0; }
            .import-auto-plan-table th { position: sticky; top: 0; background: #f8fafc; color: var(--text-muted); font-weight: 700; }
            .import-auto-plan-truncated { padding: 6px 10px; text-align: right; font-size: 12px; color: var(--text-muted); }
            .import-auto-plan-empty { padding: 20px; text-align: center; color: var(--text-muted); font-size: 13px; border: 1px dashed var(--border-color); border-radius: 8px; }

            .import-auto-plan-tree { display: flex; flex-direction: column; gap: 4px; max-height: 340px; overflow: auto; padding: 4px; border: 1px solid var(--border-color); border-radius: 8px; background: #fff; }
            .import-auto-plan-tree-node { padding-left: calc(var(--depth, 0) * 18px); }
            .import-auto-plan-tree-row { display: flex; gap: 8px; align-items: center; padding: 6px 8px; border-radius: 6px; }
            .import-auto-plan-tree-row:hover { background: rgba(99,102,241,.06); }
            .import-auto-plan-tree-bullet { width: 8px; height: 8px; border-radius: 999px; background: linear-gradient(135deg, #6366f1, #8b5cf6); flex-shrink: 0; }
            .import-auto-plan-tree-label { font-weight: 600; color: var(--text-color); }
            .import-auto-plan-tree-detail { color: var(--text-muted); font-size: 12px; }
            .import-auto-plan-tree-children { margin-top: 2px; }
            .import-auto-plan--error { padding: 14px; border-radius: 10px; background: rgba(239,68,68,.08); border: 1px solid rgba(239,68,68,.3); color: #b91c1c; }
            .import-auto-plan--error .import-auto-plan__title { color: #b91c1c; font-size: 14px; margin-bottom: 4px; }
            .import-auto-plan--error .import-auto-plan__message { font-size: 13px; line-height: 1.5; }

            .import-auto-smart-progress { display: flex; flex-direction: column; gap: 14px; padding: 4px 2px; }
            .import-auto-smart-progress__head { display: flex; gap: 14px; align-items: center; }
            .import-auto-smart-progress__icon {
                width: 48px; height: 48px;
                border-radius: 14px;
                display: flex; align-items: center; justify-content: center;
                background: linear-gradient(135deg, rgba(99,102,241,.16), rgba(236,72,153,.18));
                color: #4f46e5;
                flex-shrink: 0;
                box-shadow: 0 12px 24px rgba(99,102,241,.18);
            }
            .import-auto-smart-progress__icon.is-failed {
                background: rgba(239,68,68,.12);
                color: #b91c1c;
                box-shadow: none;
            }
            .import-auto-smart-progress__body { flex: 1; min-width: 0; }
            .import-auto-smart-progress__eyebrow {
                font-size: 11px; font-weight: 700; color: var(--text-muted);
                letter-spacing: .04em; text-transform: uppercase;
            }
            .import-auto-smart-progress__stage {
                font-size: 15px; font-weight: 700; color: var(--text-color);
                margin-top: 3px; line-height: 1.3;
            }
            .import-auto-smart-progress__file {
                font-size: 12px; color: var(--text-muted); margin-top: 4px;
                overflow-wrap: anywhere;
            }
            .import-auto-smart-progress__percent {
                font-size: 22px; font-weight: 800; color: #4f46e5;
                line-height: 1; flex-shrink: 0;
            }
            .import-auto-smart-progress__percent small { font-size: 12px; font-weight: 700; opacity: .7; margin-left: 1px; }
            .import-auto-smart-progress.is-failed .import-auto-smart-progress__percent { color: #b91c1c; }

            .import-auto-smart-progress__track {
                width: 100%; height: 6px;
                background: rgba(99,102,241,.12);
                border-radius: 999px;
                overflow: hidden;
                position: relative;
            }
            .import-auto-smart-progress__fill {
                height: 100%;
                background: linear-gradient(90deg, #6366f1, #a855f7 60%, #ec4899);
                border-radius: 999px;
                box-shadow: 0 0 12px rgba(99,102,241,.45);
                transition: width .35s ease;
                position: relative;
            }
            .import-auto-smart-progress__fill::after {
                content: "";
                position: absolute;
                top: 0; right: 0; bottom: 0; width: 30%;
                background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.5));
                animation: import-auto-smart-shimmer 1.4s linear infinite;
            }
            .import-auto-smart-progress.is-failed .import-auto-smart-progress__fill {
                background: linear-gradient(90deg, #ef4444, #f97316);
                box-shadow: none;
                animation: none;
            }
            .import-auto-smart-progress.is-failed .import-auto-smart-progress__fill::after { display: none; }
            @keyframes import-auto-smart-shimmer {
                0% { transform: translateX(-100%); }
                100% { transform: translateX(100%); }
            }

            .import-auto-smart-progress__dots {
                display: flex; gap: 8px; align-items: center; justify-content: center;
            }
            .import-auto-smart-progress__dot {
                width: 10px; height: 10px; border-radius: 999px;
                background: rgba(99,102,241,.18);
                transition: all .25s ease;
            }
            .import-auto-smart-progress__dot.is-active { background: #6366f1; }
            .import-auto-smart-progress__dot.is-current {
                background: #ec4899;
                box-shadow: 0 0 0 4px rgba(236,72,153,.18);
                transform: scale(1.18);
            }

            .import-auto-smart-progress__message {
                font-size: 13px; color: var(--text-color); line-height: 1.5;
                padding: 10px 12px; border-radius: 10px;
                background: rgba(99,102,241,.06);
                border: 1px solid rgba(99,102,241,.18);
                overflow-wrap: anywhere;
            }
            .import-auto-smart-progress.is-failed .import-auto-smart-progress__message {
                background: rgba(239,68,68,.08);
                border-color: rgba(239,68,68,.3);
                color: #b91c1c;
            }
            .import-auto-smart-progress__hint {
                font-size: 12px; color: var(--text-muted); line-height: 1.5;
                text-align: center;
            }

            .import-auto-execute-progress {
                display: flex;
                flex-direction: column;
                gap: 14px;
                padding: 2px;
            }
            .import-auto-execute-progress__head {
                display: flex;
                align-items: center;
                gap: 14px;
            }
            .import-auto-execute-progress__icon {
                width: 48px;
                height: 48px;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                background: rgba(79, 70, 229, .10);
                color: #4f46e5;
                flex-shrink: 0;
            }
            .import-auto-execute-progress__title-wrap {
                flex: 1;
                min-width: 0;
            }
            .import-auto-execute-progress__eyebrow {
                font-size: 11px;
                font-weight: 700;
                color: var(--text-muted);
                letter-spacing: .04em;
                text-transform: uppercase;
            }
            .import-auto-execute-progress__title {
                margin-top: 3px;
                font-size: 16px;
                line-height: 1.3;
                font-weight: 700;
                color: var(--text-color);
            }
            .import-auto-execute-progress__file {
                margin-top: 4px;
                color: var(--text-muted);
                font-size: 12px;
                overflow-wrap: anywhere;
            }
            .import-auto-execute-progress__live {
                display: inline-flex;
                align-items: center;
                gap: 7px;
                padding: 6px 10px;
                border-radius: 999px;
                background: rgba(16, 185, 129, .10);
                color: #047857;
                font-size: 12px;
                font-weight: 700;
                flex-shrink: 0;
            }
            .import-auto-execute-progress__live-dot,
            .import-auto-execute-progress__message-dot {
                width: 8px;
                height: 8px;
                border-radius: 999px;
                background: #10b981;
                box-shadow: 0 0 0 4px rgba(16, 185, 129, .14);
                animation: import-auto-execute-pulse 1.2s ease-in-out infinite;
                flex-shrink: 0;
            }
            .import-auto-execute-progress__bar {
                height: 8px;
                border-radius: 999px;
                overflow: hidden;
                background: rgba(79, 70, 229, .10);
                position: relative;
            }
            .import-auto-execute-progress__bar-fill {
                position: absolute;
                top: 0;
                bottom: 0;
                left: 0;
                border-radius: inherit;
                background: #4f46e5;
                transition: width .35s ease;
            }
            .import-auto-execute-progress__stats {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 10px;
            }
            .import-auto-execute-stat {
                padding: 10px 12px;
                border: 1px solid var(--border-color);
                border-radius: 8px;
                background: #fff;
            }
            .import-auto-execute-stat span {
                display: block;
                color: var(--text-muted);
                font-size: 11px;
                font-weight: 700;
            }
            .import-auto-execute-stat b {
                display: block;
                margin-top: 4px;
                color: var(--text-color);
                font-size: 15px;
                font-weight: 700;
            }
            .import-auto-execute-live-grid {
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 8px;
            }
            .import-auto-execute-live {
                padding: 9px 10px;
                border: 1px solid var(--border-color);
                border-radius: 8px;
                background: var(--bg-light-gray, #f8fafc);
            }
            .import-auto-execute-live span {
                display: block;
                color: var(--text-muted);
                font-size: 11px;
                font-weight: 700;
            }
            .import-auto-execute-live b {
                display: block;
                margin-top: 3px;
                color: var(--text-color);
                font-size: 16px;
                font-weight: 800;
            }
            .import-auto-execute-live--inserted b { color: #047857; }
            .import-auto-execute-live--skipped b { color: #b45309; }
            .import-auto-execute-live--failed b { color: #b91c1c; }
            .import-auto-execute-current {
                display: flex;
                flex-direction: column;
                gap: 6px;
                padding: 10px 12px;
                border: 1px solid rgba(79, 70, 229, .18);
                border-radius: 8px;
                background: rgba(79, 70, 229, .04);
            }
            .import-auto-execute-current__head {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 10px;
                color: var(--text-color);
                font-size: 12px;
            }
            .import-auto-execute-current__head span,
            .import-auto-execute-current small {
                color: var(--text-muted);
                font-size: 12px;
            }
            .import-auto-execute-current__title {
                color: var(--text-color);
                font-size: 12px;
                font-weight: 700;
                overflow-wrap: anywhere;
            }
            .import-auto-execute-current__track {
                height: 6px;
                border-radius: 999px;
                background: rgba(79, 70, 229, .12);
                overflow: hidden;
            }
            .import-auto-execute-current__track div {
                height: 100%;
                border-radius: inherit;
                background: #4f46e5;
                transition: width .25s ease;
            }
            .import-auto-execute-progress__message {
                display: flex;
                align-items: flex-start;
                gap: 10px;
                padding: 11px 12px;
                border: 1px solid rgba(79, 70, 229, .20);
                border-radius: 8px;
                background: rgba(79, 70, 229, .06);
                color: #312e81;
                font-size: 13px;
                line-height: 1.5;
            }
            .import-auto-execute-steps {
                display: flex;
                flex-direction: column;
                gap: 8px;
                padding: 10px;
                border: 1px solid var(--border-color);
                border-radius: 8px;
                background: var(--bg-light-gray, #f8fafc);
                max-height: 230px;
                overflow: auto;
            }
            .import-auto-execute-steps__title {
                font-size: 12px;
                font-weight: 700;
                color: var(--text-muted);
            }
            .import-auto-execute-step {
                display: flex;
                align-items: flex-start;
                gap: 9px;
                padding: 8px;
                border-radius: 7px;
                background: #fff;
                border: 1px solid rgba(148, 163, 184, .28);
            }
            .import-auto-execute-step__index {
                width: 22px;
                height: 22px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                border-radius: 999px;
                background: rgba(79, 70, 229, .10);
                color: #4f46e5;
                font-size: 11px;
                font-weight: 800;
                flex-shrink: 0;
            }
            .import-auto-execute-step__body {
                display: flex;
                flex-direction: column;
                gap: 2px;
                min-width: 0;
            }
            .import-auto-execute-step__body b {
                color: var(--text-color);
                font-size: 12px;
                line-height: 1.35;
                overflow-wrap: anywhere;
            }
            .import-auto-execute-step__body small,
            .import-auto-execute-steps__more,
            .import-auto-execute-progress__hint {
                color: var(--text-muted);
                font-size: 12px;
                line-height: 1.45;
            }
            .import-auto-execute-steps__more {
                padding: 2px 8px;
                text-align: center;
                font-weight: 600;
            }
            .import-auto-execute-progress__hint {
                text-align: center;
            }
            @keyframes import-auto-execute-bar {
                0% { transform: translateX(0); }
                100% { transform: translateX(385%); }
            }
            @keyframes import-auto-execute-pulse {
                0%, 100% { opacity: 1; transform: scale(1); }
                50% { opacity: .45; transform: scale(.82); }
            }
            @media (max-width: 640px) {
                .import-auto-execute-progress__head {
                    align-items: flex-start;
                    flex-wrap: wrap;
                }
                .import-auto-execute-progress__live {
                    margin-left: 62px;
                }
                .import-auto-execute-progress__stats {
                    grid-template-columns: 1fr;
                }
                .import-auto-execute-live-grid {
                    grid-template-columns: repeat(2, minmax(0, 1fr));
                }
                .import-auto-execute-current__head {
                    align-items: flex-start;
                    flex-direction: column;
                    gap: 3px;
                }
            }
            @media (prefers-reduced-motion: reduce) {
                .import-auto-execute-progress__bar-fill,
                .import-auto-execute-progress__live-dot,
                .import-auto-execute-progress__message-dot {
                    animation: none;
                }
            }

            .import-auto-action-cell { text-align: right; padding-right: 10px !important; padding-left: 8px !important; }
            .import-auto-action-group {
                display: inline-flex;
                gap: 6px;
                align-items: center;
                justify-content: flex-end;
                flex-wrap: nowrap;
                max-width: 100%;
            }
            .import-auto-import-btn {
                min-width: 86px;
                max-width: 134px;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
                font-weight: 600;
                border-radius: 8px;
            }
            .import-auto-ai-resolve-btn {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                min-width: 82px;
                height: 32px;
                padding: 0 10px;
                border-radius: 8px;
                font-size: 12px;
                font-weight: 700;
                color: #4338ca;
                background: rgba(99, 102, 241, .08);
                border: 1px solid rgba(99, 102, 241, .28);
                white-space: nowrap;
            }
            .import-auto-ai-resolve-btn:hover {
                color: #312e81;
                background: rgba(99, 102, 241, .14);
                border-color: rgba(99, 102, 241, .48);
            }
            .import-auto-import-btn[disabled] {
                opacity: .55;
                pointer-events: none;
            }
            .import-auto-icon-btn {
                width: 32px; height: 32px;
                display: inline-flex; align-items: center; justify-content: center;
                background: var(--card-bg);
                border: 1px solid var(--border-color);
                border-radius: 8px;
                color: var(--text-muted);
                cursor: pointer;
                transition: all .15s ease;
            }
            .import-auto-icon-btn:hover {
                color: #4f46e5;
                border-color: #4f46e5;
                background: rgba(99,102,241,.06);
            }
            .import-auto-icon-btn[disabled] {
                opacity: .55;
                cursor: not-allowed;
                pointer-events: none;
            }
            .import-auto-mark-imported-btn {
                color: #047857;
                border-color: rgba(16,185,129,.30);
                background: rgba(16,185,129,.08);
            }
            .import-auto-mark-imported-btn:hover {
                color: #065f46;
                border-color: rgba(16,185,129,.55);
                background: rgba(16,185,129,.14);
            }
            .import-auto-delete-file-btn {
                color: #b91c1c;
                border-color: rgba(239,68,68,.30);
                background: rgba(239,68,68,.06);
            }
            .import-auto-delete-file-btn:hover {
                color: #991b1b;
                border-color: rgba(239,68,68,.55);
                background: rgba(239,68,68,.12);
            }

            .import-auto-action-running {
                display: inline-flex; align-items: center; gap: 8px;
                color: #4f46e5;
                font-size: 12px;
                font-weight: 600;
            }

            .import-auto-spinner {
                width: 18px; height: 18px;
                border-radius: 50%;
                border: 2px solid rgba(99,102,241,.2);
                border-top-color: #4f46e5;
                animation: import-auto-spin .7s linear infinite;
            }
            .import-auto-spinner--sm { width: 14px; height: 14px; border-width: 2px; }
            @keyframes import-auto-spin { to { transform: rotate(360deg); } }

            .import-auto-status-pill.reanalyzing {
                background: rgba(99,102,241,.12);
                color: #4338ca;
            }
            .import-auto-status-pill.reanalyzing .import-auto-status-dot {
                animation: import-auto-pulse 1.2s ease-in-out infinite;
            }
            .import-auto-file__icon--reanalyzing { background: rgba(99,102,241,.10); color: #4f46e5; }
            .import-auto-row--reanalyzing { background: rgba(99,102,241,.04); }
            .import-auto-row--reanalyzing td { position: relative; }

            .import-auto-feedback {
                display: inline-flex; align-items: center; gap: 5px;
                margin-top: 4px;
                padding: 2px 8px;
                background: rgba(99,102,241,.10);
                color: #4338ca;
                border-radius: 6px;
                font-size: 11px;
                font-weight: 600;
                cursor: help;
            }

            .import-auto-chat {
                margin-top: 12px;
                border: 1px solid var(--border-color);
                border-radius: 8px;
                background: #fff;
                overflow: hidden;
            }
            .import-auto-chat__title {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 10px 12px;
                background: var(--bg-light-gray, #f8fafc);
                border-bottom: 1px solid var(--border-color);
                color: var(--text-color);
                font-size: 13px;
                font-weight: 700;
            }
            .import-auto-chat__count {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                min-width: 22px;
                height: 22px;
                padding: 0 7px;
                border-radius: 999px;
                background: rgba(99,102,241,.12);
                color: #4338ca;
                font-size: 12px;
            }
            .import-auto-chat__log {
                display: flex;
                flex-direction: column;
                gap: 12px;
                max-height: 310px;
                overflow: auto;
                padding: 12px;
            }
            .import-auto-chat__empty {
                padding: 14px 12px;
                color: var(--text-muted);
                font-size: 13px;
            }
            .import-auto-chat-entry {
                display: flex;
                flex-direction: column;
                gap: 8px;
            }
            .import-auto-chat-entry__meta {
                display: flex;
                justify-content: space-between;
                gap: 10px;
                color: var(--text-muted);
                font-size: 11px;
                font-weight: 600;
            }
            .import-auto-chat-bubble {
                padding: 10px 12px;
                border-radius: 8px;
                font-size: 13px;
                line-height: 1.45;
            }
            .import-auto-chat-bubble--user {
                margin-left: 36px;
                background: rgba(59,130,246,.09);
                border: 1px solid rgba(59,130,246,.18);
                color: #1e3a8a;
            }
            .import-auto-chat-bubble--ai {
                margin-right: 36px;
                background: rgba(15,23,42,.04);
                border: 1px solid var(--border-color);
                color: var(--text-color);
            }
            .import-auto-chat-entry--running .import-auto-chat-bubble--ai {
                border-color: rgba(99,102,241,.24);
                background: rgba(99,102,241,.06);
            }
            .import-auto-chat-entry--error .import-auto-chat-bubble--ai {
                border-color: rgba(239,68,68,.24);
                background: rgba(239,68,68,.06);
                color: #991b1b;
            }
            .import-auto-chat-bubble__head {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 10px;
                margin-bottom: 5px;
                font-size: 11px;
                font-weight: 700;
                color: var(--text-muted);
            }
            .import-auto-chat-bubble__body {
                white-space: pre-wrap;
                overflow-wrap: anywhere;
            }
            .import-auto-chat-result {
                display: flex;
                flex-wrap: wrap;
                gap: 6px;
                margin-top: 8px;
            }
            .import-auto-chat-result span {
                display: inline-flex;
                align-items: center;
                padding: 3px 8px;
                border-radius: 999px;
                background: #fff;
                border: 1px solid var(--border-color);
                color: var(--text-color);
                font-size: 11px;
                font-weight: 700;
            }

            /* Empty state */
            .import-auto-empty {
                padding: 64px 16px;
                text-align: center;
                color: var(--text-muted);
            }
            .import-auto-empty__icon {
                width: 76px; height: 76px;
                margin: 0 auto 12px;
                border-radius: 50%;
                background: var(--bg-light-gray, #f1f5f9);
                display: flex; align-items: center; justify-content: center;
                color: var(--text-muted);
            }
            .import-auto-empty__title { font-size: 15px; font-weight: 600; color: var(--text-color); }
            .import-auto-empty__hint  { font-size: 13px; margin-top: 4px; }

            /* Confirm dialog */
            .import-auto-alert {
                display: flex; align-items: center; gap: 8px;
                padding: 10px 12px;
                border-radius: 8px;
                font-size: 13px;
                margin-bottom: 14px;
            }
            .import-auto-alert--ok   { background: rgba(16,185,129,.10); color: #047857; border: 1px solid rgba(16,185,129,.25); }
            .import-auto-alert--warn { background: rgba(245,158,11,.10); color: #92400e; border: 1px solid rgba(245,158,11,.30); }
            .import-auto-alert__dot {
                width: 8px; height: 8px; border-radius: 50%;
                background: currentColor;
            }
            .import-auto-confirm { display: flex; flex-direction: column; gap: 8px; }
            .import-auto-confirm__row {
                display: flex; justify-content: space-between; gap: 12px;
                padding: 10px 12px;
                background: var(--bg-light-gray, #f8fafc);
                border-radius: 8px;
                font-size: 13px;
            }
            .import-auto-confirm__label {
                color: var(--text-muted);
                font-weight: 500;
            }
            .import-auto-confirm__value {
                color: var(--text-color);
                font-weight: 600;
                text-align: right;
                overflow-wrap: anywhere;
            }

            /* File preview dialog */
            .import-auto-preview {
                display: flex;
                flex-direction: column;
                gap: 14px;
                max-height: 72vh;
                overflow: auto;
                padding-right: 2px;
            }
            .import-auto-preview__header {
                display: flex;
                justify-content: space-between;
                gap: 16px;
                align-items: flex-start;
                padding: 14px;
                background: var(--bg-light-gray, #f8fafc);
                border: 1px solid var(--border-color);
                border-radius: 8px;
            }
            .import-auto-preview__eyebrow {
                font-size: 11px;
                font-weight: 700;
                color: var(--text-muted);
                text-transform: uppercase;
                letter-spacing: .04em;
            }
            .import-auto-preview__title {
                margin-top: 3px;
                color: var(--text-color);
                font-size: 17px;
                font-weight: 700;
                line-height: 1.3;
                overflow-wrap: anywhere;
            }
            .import-auto-preview__path {
                margin-top: 4px;
                color: var(--text-muted);
                font-size: 12px;
                overflow-wrap: anywhere;
            }
            .import-auto-preview__meta {
                display: inline-flex;
                gap: 8px;
                align-items: center;
                justify-content: flex-end;
                flex-wrap: wrap;
            }
            .import-auto-preview__stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
                gap: 10px;
            }
            .import-auto-preview-stat {
                padding: 10px 12px;
                background: #fff;
                border: 1px solid var(--border-color);
                border-radius: 8px;
            }
            .import-auto-preview-stat span {
                display: block;
                color: var(--text-muted);
                font-size: 11px;
                font-weight: 600;
            }
            .import-auto-preview-stat b {
                display: block;
                margin-top: 3px;
                color: var(--text-color);
                font-size: 15px;
                font-weight: 700;
            }
            .import-auto-preview__note {
                padding: 10px 12px;
                border-radius: 8px;
                background: rgba(245,158,11,.10);
                border: 1px solid rgba(245,158,11,.28);
                color: #92400e;
                font-size: 13px;
                line-height: 1.45;
            }
            .import-auto-preview-sheet {
                border: 1px solid var(--border-color);
                border-radius: 8px;
                overflow: hidden;
                background: #fff;
            }
            .import-auto-preview-sheet__head {
                display: flex;
                justify-content: space-between;
                gap: 12px;
                padding: 12px 14px;
                background: var(--bg-light-gray, #f8fafc);
                border-bottom: 1px solid var(--border-color);
            }
            .import-auto-preview-sheet__head h4 {
                margin: 0;
                color: var(--text-color);
                font-size: 14px;
                font-weight: 700;
            }
            .import-auto-preview-sheet__head p {
                margin: 4px 0 0;
                color: var(--text-muted);
                font-size: 12px;
            }
            .import-auto-preview-table-wrap {
                overflow: auto;
                max-height: 360px;
            }
            .import-auto-preview-table {
                width: 100%;
                min-width: 720px;
                border-collapse: separate;
                border-spacing: 0;
                font-size: 12px;
            }
            .import-auto-preview-table th,
            .import-auto-preview-table td {
                padding: 8px 10px;
                border-right: 1px solid var(--border-color);
                border-bottom: 1px solid var(--border-color);
                text-align: left;
                vertical-align: top;
                max-width: 260px;
                overflow-wrap: anywhere;
            }
            .import-auto-preview-table th {
                position: sticky;
                top: 0;
                z-index: 1;
                background: #f8fafc;
                color: var(--text-muted);
                font-weight: 700;
            }
            .import-auto-preview-table tr:last-child td { border-bottom: 0; }
            .import-auto-preview-table th:last-child,
            .import-auto-preview-table td:last-child { border-right: 0; }
            .import-auto-preview-empty {
                padding: 22px;
                color: var(--text-muted);
                font-size: 13px;
                text-align: center;
            }
            @media (max-width: 768px) {
                .import-auto-preview__header {
                    flex-direction: column;
                }
                .import-auto-preview__meta {
                    justify-content: flex-start;
                }
            }

            /* === Smart error + fix dialog === */
            .import-auto-error {
                display: flex; flex-direction: column; gap: 12px;
                color: var(--text-color);
            }
            .import-auto-error__message {
                display: flex; gap: 12px; align-items: flex-start;
                padding: 12px 14px;
                background: #fef2f2;
                border: 1px solid #fecaca;
                border-radius: 10px;
                color: #991b1b;
            }
            .import-auto-error__icon {
                font-size: 20px; line-height: 1;
            }
            .import-auto-error__text {
                font-weight: 600;
                white-space: pre-wrap;
                word-break: break-word;
            }
            .import-auto-error-meta {
                display: grid; gap: 4px;
                font-size: 13px;
                padding: 10px 12px;
                background: var(--bg-color);
                border-radius: 8px;
                border: 1px solid var(--border-color);
            }
            .import-auto-error-record {
                background: #0f172a;
                color: #e2e8f0;
                padding: 12px;
                border-radius: 8px;
                font-size: 12px;
                max-height: 220px;
                overflow: auto;
                margin: 0;
            }
            .import-auto-error__hint {
                font-size: 12.5px;
                color: var(--text-muted);
                line-height: 1.5;
                padding: 8px 0;
            }
            .import-auto-error__retry {
                font-size: 12px;
                color: var(--text-muted);
            }

            .import-auto-fix {
                display: flex; flex-direction: column; gap: 16px;
            }
            .import-auto-fix-summary {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
                gap: 10px;
            }
            .import-auto-fix-summary__item.is-proposal {
                background: #eef2ff; border-color: #c7d2fe; color: #3730a3;
            }
            .import-auto-fix-summary__item {
                padding: 12px 14px;
                border-radius: 10px;
                border: 1px solid var(--border-color);
                background: var(--card-bg);
                text-align: center;
            }
            .import-auto-fix-summary__item.is-applied {
                background: #ecfdf5; border-color: #a7f3d0; color: #065f46;
            }
            .import-auto-fix-summary__item.is-rejected {
                background: #f1f5f9; border-color: #cbd5e1; color: #475569;
            }
            .import-auto-fix-summary__item.is-unresolved {
                background: #fffbeb; border-color: #fde68a; color: #92400e;
            }
            .import-auto-fix-summary__value {
                font-size: 22px; font-weight: 700;
            }
            .import-auto-fix-summary__label {
                font-size: 12px; margin-top: 2px;
            }
            .import-auto-fix-table {
                font-size: 13px;
            }
            .import-auto-fix-table th {
                background: #f8fafc;
                font-weight: 600;
            }
            .import-auto-fix-old {
                color: #991b1b;
                text-decoration: line-through;
                background: #fef2f2;
            }
            .import-auto-fix-new {
                color: #065f46;
                background: #ecfdf5;
                font-weight: 600;
            }
            .import-auto-fix-table--rejected td {
                color: var(--text-muted);
                font-size: 12.5px;
            }

            /* AI dependency proposals */
            .import-auto-dep-proposals {
                display: flex; flex-direction: column; gap: 12px;
                padding: 14px; border-radius: 12px;
                background: linear-gradient(140deg, rgba(99,102,241,.07), rgba(168,85,247,.05));
                border: 1px solid rgba(99,102,241,.25);
            }
            .import-auto-dep-proposals__title {
                display: inline-flex; align-items: center; gap: 8px;
                font-weight: 700; color: #3730a3; font-size: 14px;
            }
            .import-auto-dep-proposals__title svg { color: #6366f1; }
            .import-auto-dep-proposals__hint {
                font-size: 12.5px; color: #4338ca; line-height: 1.45;
                background: rgba(255,255,255,.6); padding: 8px 10px; border-radius: 8px;
                border: 1px dashed rgba(99,102,241,.3);
            }
            .import-auto-dep-proposal {
                background: #fff; border: 1px solid rgba(99,102,241,.25);
                border-radius: 12px; overflow: hidden;
            }
            .import-auto-dep-proposal__head {
                display: flex; gap: 12px; align-items: flex-start;
                padding: 12px 14px; background: #f5f3ff; border-bottom: 1px solid rgba(99,102,241,.2);
            }
            .import-auto-dep-proposal__icon {
                width: 36px; height: 36px; border-radius: 10px;
                background: linear-gradient(135deg, #6366f1, #a855f7);
                color: #fff; display: inline-flex; align-items: center; justify-content: center;
                flex-shrink: 0; box-shadow: 0 4px 12px rgba(99,102,241,.35);
            }
            .import-auto-dep-proposal__body { flex: 1; min-width: 0; }
            .import-auto-dep-proposal__title {
                font-weight: 700; color: #1e1b4b; font-size: 14px;
                display: inline-flex; gap: 8px; flex-wrap: wrap; align-items: center;
            }
            .import-auto-dep-proposal__count {
                font-size: 11px; font-weight: 700; padding: 2px 8px;
                background: rgba(99,102,241,.15); color: #4338ca; border-radius: 999px;
            }
            .import-auto-dep-proposal__exists {
                font-size: 11px; color: #6b7280; font-weight: 500;
            }
            .import-auto-dep-proposal__reason {
                margin-top: 4px; font-size: 12.5px; color: #4338ca; line-height: 1.45;
            }
            .import-auto-dep-proposal__meta {
                margin-top: 6px; display: inline-flex; gap: 14px; flex-wrap: wrap;
                font-size: 11.5px; color: #6b7280;
            }
            .import-auto-dep-proposal__meta b { color: #312e81; }
            .import-auto-dep-proposal__meta code {
                background: rgba(99,102,241,.1); padding: 1px 5px; border-radius: 4px; color: #4338ca;
            }
            .import-auto-dep-proposal__select-all {
                align-self: center; font-size: 11.5px; padding: 4px 10px;
                background: #fff; border: 1px solid rgba(99,102,241,.35); color: #4338ca;
                border-radius: 6px; cursor: pointer; transition: all .15s;
            }
            .import-auto-dep-proposal__select-all:hover {
                background: rgba(99,102,241,.1); border-color: #6366f1;
            }
            .import-auto-dep-proposal__table-wrap {
                max-height: 260px; overflow: auto;
            }
            .import-auto-dep-proposal__table {
                width: 100%; border-collapse: separate; border-spacing: 0;
                font-size: 12.5px; margin-bottom: 0;
            }
            .import-auto-dep-proposal__table th,
            .import-auto-dep-proposal__table td {
                padding: 6px 10px; border-bottom: 1px solid var(--border-color);
                text-align: left; vertical-align: top;
            }
            .import-auto-dep-proposal__table th {
                position: sticky; top: 0; background: #f8fafc;
                color: var(--text-muted); font-weight: 700; font-size: 11.5px;
                text-transform: uppercase; letter-spacing: .03em;
            }
            .import-auto-dep-proposal__table tr:last-child td { border-bottom: 0; }
            .import-auto-dep-proposal__check-cell { width: 32px; text-align: center; }
            .import-auto-dep-proposal__check { cursor: pointer; transform: scale(1.15); }
            .import-auto-dep-proposal__check:checked { accent-color: #6366f1; }
            .import-auto-dep-proposal__table tbody tr:hover { background: rgba(99,102,241,.04); }

            .import-auto-fix-empty {
                padding: 16px;
                text-align: center;
                color: var(--text-muted);
                background: var(--bg-color);
                border-radius: 8px;
            }
            .import-auto-fix-details {
                background: var(--bg-color);
                border-radius: 8px;
                padding: 8px 12px;
            }
            .import-auto-fix-details summary {
                cursor: pointer;
                font-weight: 600;
                font-size: 13px;
            }
            .import-auto-fix-unresolved {
                background: #fffbeb;
                border: 1px solid #fde68a;
                border-radius: 10px;
                padding: 12px 14px;
            }
            .import-auto-fix-unresolved h5 {
                margin: 0 0 8px; color: #92400e;
            }
            .import-auto-fix-unresolved__hint {
                font-size: 12px;
                color: #92400e;
                margin-top: 8px;
            }

            /* === Smart fix progress dialog === */
            .import-auto-fix-progress {
                display: flex; flex-direction: column; gap: 14px;
                padding: 4px 2px;
            }
            .import-auto-fix-progress__head {
                display: flex; align-items: center; gap: 12px;
            }
            .import-auto-fix-progress__icon {
                width: 44px; height: 44px; flex-shrink: 0;
                border-radius: 12px;
                display: flex; align-items: center; justify-content: center;
                color: #fff;
                background: linear-gradient(135deg, #6366f1, #8b5cf6 60%, #ec4899);
                box-shadow: 0 8px 18px rgba(99, 102, 241, .35);
            }
            .import-auto-fix-progress__icon.is-failed {
                background: linear-gradient(135deg, #ef4444, #b91c1c);
                box-shadow: 0 8px 18px rgba(239, 68, 68, .35);
            }
            .import-auto-fix-progress__body { flex: 1; min-width: 0; }
            .import-auto-fix-progress__eyebrow {
                font-size: 11px; font-weight: 600;
                text-transform: uppercase; letter-spacing: .04em;
                color: var(--text-muted);
            }
            .import-auto-fix-progress__message {
                font-size: 14px; font-weight: 600;
                color: var(--text-color);
                margin-top: 2px;
                line-height: 1.35;
            }
            .import-auto-fix-progress__file {
                font-size: 12px; color: var(--text-muted); margin-top: 2px;
                white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
            }
            .import-auto-fix-progress__percent {
                font-size: 26px; font-weight: 700;
                color: var(--text-color);
                margin-left: auto;
            }
            .import-auto-fix-progress__percent small {
                font-size: 13px; color: var(--text-muted); font-weight: 600;
                margin-left: 1px;
            }
            .import-auto-fix-progress__track {
                height: 6px;
                background: var(--bg-color);
                border-radius: 999px;
                overflow: hidden;
            }
            .import-auto-fix-progress__fill {
                height: 100%;
                background: linear-gradient(90deg, #6366f1, #8b5cf6 60%, #ec4899);
                transition: width .35s ease;
                border-radius: 999px;
            }
            .import-auto-fix-progress.is-failed .import-auto-fix-progress__fill {
                background: linear-gradient(90deg, #ef4444, #b91c1c);
            }
            .import-auto-fix-progress__stages {
                display: flex; justify-content: space-between;
                gap: 8px;
                padding: 4px 2px 0;
            }
            .import-auto-fix-stage {
                flex: 1; display: flex; flex-direction: column;
                align-items: center; gap: 4px;
                font-size: 10.5px;
                color: var(--text-muted);
                text-align: center;
                min-width: 0;
            }
            .import-auto-fix-stage__dot {
                width: 10px; height: 10px;
                border-radius: 999px;
                background: var(--border-color);
                transition: all .25s ease;
            }
            .import-auto-fix-stage.is-active .import-auto-fix-stage__dot {
                background: linear-gradient(135deg, #6366f1, #8b5cf6);
                box-shadow: 0 0 0 3px rgba(99, 102, 241, .15);
            }
            .import-auto-fix-stage.is-current .import-auto-fix-stage__dot {
                animation: import-auto-fix-pulse 1.4s ease-in-out infinite;
            }
            .import-auto-fix-stage.is-active .import-auto-fix-stage__label {
                color: var(--text-color); font-weight: 600;
            }
            .import-auto-fix-progress__hint {
                font-size: 11.5px;
                color: var(--text-muted);
                text-align: center;
                padding-top: 4px;
            }
            @keyframes import-auto-fix-pulse {
                0%, 100% { transform: scale(1); box-shadow: 0 0 0 3px rgba(99, 102, 241, .15); }
                50% { transform: scale(1.25); box-shadow: 0 0 0 5px rgba(99, 102, 241, .25); }
            }

            /* === Step guide === */
            .import-auto-step-guide {
                display: flex;
                align-items: center;
                gap: 10px;
                padding: 14px 20px;
                background: #f8fafc;
                border-bottom: 1px solid var(--border-color);
                flex-wrap: wrap;
            }
            .iac-step {
                display: flex; align-items: center; gap: 10px;
                padding: 8px 12px;
                border-radius: 10px;
                border: 1px solid var(--border-color);
                background: #fff;
                flex: 1 1 220px;
                min-width: 200px;
            }
            .iac-step__num {
                width: 24px; height: 24px; flex: 0 0 24px;
                border-radius: 999px;
                display: flex; align-items: center; justify-content: center;
                font-size: 12px; font-weight: 700;
                background: var(--border-color);
                color: var(--text-muted);
            }
            .iac-step__body { display: flex; flex-direction: column; line-height: 1.3; min-width: 0; }
            .iac-step__body b { font-size: 12.5px; color: var(--text-color); }
            .iac-step__body span { font-size: 11px; color: var(--text-muted); overflow-wrap: anywhere; }
            .iac-step--active {
                border-color: #6366f1;
                box-shadow: 0 0 0 3px rgba(99, 102, 241, .12);
            }
            .iac-step--active .iac-step__num {
                background: linear-gradient(135deg, #6366f1, #8b5cf6);
                color: #fff;
            }
            .iac-step--done .iac-step__num {
                background: #16a34a;
                color: #fff;
            }
            .iac-step--done { border-color: #86efac; background: #f0fdf4; }
            .iac-step__arrow { color: var(--text-muted); font-size: 14px; flex: 0 0 auto; }

            /* === Category groups === */
            .import-auto-category-groups {
                display: flex;
                flex-direction: column;
                gap: 14px;
                padding: 16px 20px;
            }
            .import-auto-category-card {
                border: 1px solid var(--border-color);
                border-radius: 12px;
                overflow: hidden;
                background: #fff;
            }
            .import-auto-category-header {
                display: flex;
                align-items: center;
                gap: 10px;
                padding: 12px 16px;
                background: #f8fafc;
                cursor: pointer;
                user-select: none;
                flex-wrap: wrap;
            }
            .import-auto-category-card.is-collapsed .import-auto-category-header {
                border-bottom: none;
            }
            .import-auto-category-icon { font-size: 18px; line-height: 1; }
            .import-auto-category-title { font-size: 13.5px; font-weight: 700; color: var(--text-color); }
            .import-auto-category-count {
                font-size: 11px; color: var(--text-muted);
                background: var(--border-color);
                padding: 2px 8px; border-radius: 999px;
            }
            .import-auto-category-minis {
                display: inline-flex; gap: 6px; flex-wrap: wrap;
                margin-left: 4px;
            }
            .import-auto-category-mini {
                font-size: 10.5px; font-weight: 600;
                padding: 2px 7px; border-radius: 999px;
                white-space: nowrap;
            }
            .import-auto-category-mini--safe { background: #dcfce7; color: #15803d; }
            .import-auto-category-mini--warning { background: #fef3c7; color: #b45309; }
            .import-auto-category-mini--error { background: #fee2e2; color: #b91c1c; }
            .import-auto-category-mini--imported { background: #dbeafe; color: #1d4ed8; }
            .import-auto-category-actions {
                display: inline-flex; align-items: center; gap: 10px;
                margin-left: auto;
            }
            .import-auto-category-bulk-btn { white-space: nowrap; }
            .import-auto-category-chevron {
                font-size: 12px; color: var(--text-muted);
                width: 14px; text-align: center;
            }
            .import-auto-category-body { border-top: 1px solid var(--border-color); }

            /* === Master-data slot grid === */
            .import-auto-slot-hint {
                padding: 14px 20px;
                font-size: 12px;
                color: var(--text-muted);
            }
            .import-auto-slot-grid {
                display: flex;
                flex-direction: column;
                gap: 16px;
                padding: 16px 20px;
                border-bottom: 1px solid var(--border-color);
            }
            .import-auto-slot-group__label {
                display: flex;
                align-items: center;
                gap: 10px;
                font-size: 12px; font-weight: 700;
                color: var(--text-color);
                text-transform: uppercase;
                letter-spacing: .02em;
                margin-bottom: 8px;
            }
            .import-auto-slot-group__count {
                font-size: 10.5px; font-weight: 600;
                color: var(--text-muted);
                text-transform: none;
                letter-spacing: normal;
                background: var(--border-color);
                padding: 1px 8px; border-radius: 999px;
            }
            .import-auto-slot-cards {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
                gap: 12px;
            }
            .import-auto-slot-card {
                border: 1px solid var(--border-color);
                border-radius: 10px;
                background: #fff;
                padding: 12px;
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
            .import-auto-slot-card--ready { border-color: #86efac; background: #f7fdf9; }
            .import-auto-slot-card--error { border-color: #fca5a5; background: #fef7f7; }
            .import-auto-slot-card--imported { border-color: #93c5fd; background: #f5f9ff; }
            .import-auto-slot-card__head {
                display: flex;
                align-items: flex-start;
                gap: 8px;
            }
            .import-auto-slot-icon { font-size: 18px; line-height: 1.3; }
            .import-auto-slot-card__title-wrap { flex: 1; min-width: 0; }
            .import-auto-slot-title {
                font-size: 12.5px; font-weight: 700;
                color: var(--text-color);
                line-height: 1.3;
            }
            .import-auto-slot-hint {
                font-size: 10.5px;
                color: var(--text-muted);
                margin-top: 2px;
                overflow-wrap: anywhere;
                padding: 0;
            }
            .import-auto-slot-badge {
                font-size: 9.5px; font-weight: 700;
                text-transform: uppercase;
                padding: 2px 6px; border-radius: 999px;
                white-space: nowrap;
                flex: 0 0 auto;
            }
            .import-auto-slot-badge--empty { background: var(--border-color); color: var(--text-muted); }
            .import-auto-slot-badge--ready { background: #dcfce7; color: #15803d; }
            .import-auto-slot-badge--error { background: #fee2e2; color: #b91c1c; }
            .import-auto-slot-badge--imported { background: #dbeafe; color: #1d4ed8; }
            .import-auto-slot-actions { display: flex; gap: 6px; }
            .import-auto-slot-actions .btn { flex: 1; }
    `;
    document.head.appendChild(style);
    return "";
}


/* --------------------------------------------------------------------------
 * Smart error → AI fix → diff preview → re-execute
 * -------------------------------------------------------------------------- */

function show_smart_error_dialog(frm, row_name, plan, result, parent_dialog) {
    const error_msg = (result && result.error) || __("An error occurred during import.");
    const failed_step = result && result.failed_step_index;
    const failed_step_title = result && result.failed_step_title;
    const failed_doctype = result && result.failed_target_doctype;
    const failed_row = result && result.failed_row_index;
    const failed_record = (result && result.failed_record) || null;
    const error_type = (result && result.error_type) || "";

    const retry_count = (frm.__smart_fix_retry_count && frm.__smart_fix_retry_count[row_name]) || 0;
    const max_retry = SMART_FIX_MAX_RETRY;
    const can_fix = retry_count < max_retry;

    const record_html = failed_record
        ? `<pre class="import-auto-error-record">${frappe.utils.escape_html(JSON.stringify(failed_record, null, 2))}</pre>`
        : "";

    const meta_html = `
        <div class="import-auto-error-meta">
            ${failed_step ? `<div><b>${__("Step")}:</b> ${frappe.utils.escape_html(String(failed_step))} - ${frappe.utils.escape_html(failed_step_title || "")}</div>` : ""}
            ${failed_doctype ? `<div><b>${__("DocType")}:</b> ${frappe.utils.escape_html(failed_doctype)}</div>` : ""}
            ${failed_row ? `<div><b>${__("Error Row")}:</b> ${frappe.utils.escape_html(String(failed_row))}</div>` : ""}
            ${error_type ? `<div><b>${__("Error Type")}:</b> ${frappe.utils.escape_html(error_type)}</div>` : ""}
        </div>
    `;

    const hint = can_fix
        ? __("Records before the error row are kept. AI will only patch safe fields and continue.")
        : __("Tried {0} fixes without success. Please edit the Excel file or reanalyze.", [max_retry]);

    const dialog = new frappe.ui.Dialog({
        title: __("Import Paused at Error Row"),
        size: "large",
        fields: [
            {
                fieldtype: "HTML",
                fieldname: "body",
                options: `
                    ${import_auto_styles()}
                    <div class="import-auto-error">
                        <div class="import-auto-error__message">
                            <div class="import-auto-error__icon">⚠</div>
                            <div class="import-auto-error__text">${frappe.utils.escape_html(error_msg)}</div>
                        </div>
                        ${meta_html}
                        ${record_html}
                        <div class="import-auto-error__hint">${hint}</div>
                        <div class="import-auto-error__retry">${__("Fix Attempts")}: <b>${retry_count}/${max_retry}</b></div>
                    </div>
                `,
            },
        ],
        primary_action_label: can_fix ? __("Fix with AI") : __("Close"),
        primary_action() {
            if (!can_fix) {
                dialog.hide();
                return;
            }
            const error_payload = {
                error: error_msg,
                failed_step_index: failed_step,
                failed_row_index: failed_row,
                failed_record: failed_record,
                error_type: error_type,
            };
            dialog.hide();
            run_smart_fix(frm, row_name, plan, error_payload, parent_dialog);
        },
        secondary_action_label: __("Close"),
        secondary_action() {
            dialog.hide();
        },
    });
    dialog.show();
}

function run_smart_fix(frm, row_name, plan, error_payload, parent_dialog, options = {}) {
    frm.__smart_fix_retry_count = frm.__smart_fix_retry_count || {};
    frm.__smart_fix_retry_count[row_name] = (frm.__smart_fix_retry_count[row_name] || 0) + 1;

    // Cache plan + parent dialog so the realtime handler can use them when
    // the background job completes.
    frm.__smart_fix_pending = frm.__smart_fix_pending || {};
    frm.__smart_fix_pending[row_name] = {
        plan,
        parent_dialog,
        auto_execute: !!options.auto_execute,
    };

    setup_smart_fix_listener(frm);
    open_smart_fix_progress_dialog(frm, row_name);

    frappe.call({
        method: `${IMPORT_AUTO_API}.smart_fix_file`,
        args: {
            docname: frm.doc.name,
            file_row_name: row_name,
            plan_json: JSON.stringify(plan),
            error_json: JSON.stringify(error_payload),
        },
    }).catch(() => {
        close_smart_fix_progress_dialog(frm);
        delete frm.__smart_fix_pending[row_name];
    });
}

function setup_smart_fix_listener(frm) {
    if (frm.__smart_fix_listener_bound) return;
    frappe.realtime.on("import_auto_smart_fix", (data) => {
        if (!data || data.docname !== frm.doc.name) return;
        const row_name = data.row_name;
        const status = data.status;

        update_smart_fix_progress_dialog(frm, data);

        if (status === "running") return;

        const pending = (frm.__smart_fix_pending || {})[row_name] || {};
        const parent_dialog = pending.parent_dialog;
        delete (frm.__smart_fix_pending || {})[row_name];

        if (status === "failed") {
            close_smart_fix_progress_dialog(frm);
            const msg = (data.result && data.result.error) || data.message || __("An error occurred while AI was fixing.");
            frappe.msgprint({
                title: __("AI Could Not Fix"),
                message: frappe.utils.escape_html(msg),
                indicator: "red",
            });
            return;
        }

        // status === "complete"
        close_smart_fix_progress_dialog(frm);
        const result = data.result || {};
        if (result.error) {
            frappe.msgprint({
                title: __("AI Could Not Fix"),
                message: frappe.utils.escape_html(result.error),
                indicator: "red",
            });
            return;
        }
        if (!result.plan || !result.plan.steps || !result.plan.steps.length) {
            frappe.msgprint({
                title: __("No Changes"),
                message: __("AI did not return a fixed plan."),
                indicator: "orange",
            });
            return;
        }
        const fixes = Array.isArray(result.fixes) ? result.fixes : [];
        const rejected = Array.isArray(result.rejected) ? result.rejected : [];
        const unresolved = Array.isArray(result.unresolved) ? result.unresolved : [];
        const proposals = Array.isArray(result.new_dependency_steps) ? result.new_dependency_steps : [];
        if (
            pending.auto_execute
            && fixes.length
            && !rejected.length
            && !unresolved.length
            && !proposals.length
        ) {
            frappe.show_alert({
                message: __("AI fixed the error row and is continuing with the patched plan."),
                indicator: "green",
            }, 5);
            execute_smart_plan(frm, row_name, result.plan, parent_dialog, { skip_confirm: true });
            return;
        }
        show_smart_fix_diff_dialog(frm, row_name, result, parent_dialog);
    });
    frm.__smart_fix_listener_bound = true;
}

function open_smart_fix_progress_dialog(frm, row_name) {
    if (frm.__smart_fix_progress_dialog) {
        try { frm.__smart_fix_progress_dialog.hide(); } catch (e) {}
    }
    const dialog = new frappe.ui.Dialog({
        title: __("AI Fixing Error..."),
        size: "small",
        fields: [
            {
                fieldtype: "HTML",
                fieldname: "body",
                options: `${import_auto_styles()}${render_smart_fix_progress(0, "queued", __("Queuing..."))}`,
            },
        ],
    });
    dialog.no_cancel = false;
    dialog.show();
    frm.__smart_fix_progress_dialog = dialog;
    frm.__smart_fix_progress_row = row_name;
}

function update_smart_fix_progress_dialog(frm, data) {
    const dialog = frm.__smart_fix_progress_dialog;
    if (!dialog) return;
    const percent = Math.max(0, Math.min(100, Number(data.percent) || 0));
    const stage = data.stage || "running";
    const message = data.message || "";
    const wrapper = dialog.$wrapper.find('[data-fieldname="body"]');
    if (wrapper.length) {
        wrapper.html(`${import_auto_styles()}${render_smart_fix_progress(percent, stage, message, data.file_name)}`);
    }
}

function close_smart_fix_progress_dialog(frm) {
    if (frm.__smart_fix_progress_dialog) {
        try { frm.__smart_fix_progress_dialog.hide(); } catch (e) {}
        frm.__smart_fix_progress_dialog = null;
        frm.__smart_fix_progress_row = null;
    }
}

function render_smart_fix_progress(percent, stage, message, file_name) {
    const stages = [
        { key: "queued",       label: __("Queued") },
        { key: "reading",      label: __("Reading File") },
        { key: "preparing",    label: __("Preparing") },
        { key: "scanning",     label: __("Scanning Dependencies") },
        { key: "thinking",     label: __("AI Analyzing") },
        { key: "applying",     label: __("Applying") },
        { key: "merging",      label: __("Merging Plan") },
        { key: "complete",     label: __("Complete") },
    ];
    const stage_idx = Math.max(0, stages.findIndex((s) => s.key === stage));
    const is_failed = stage === "failed";
    const is_done = stage === "complete";

    const steps_html = stages.map((s, idx) => {
        const active = !is_failed && (idx <= stage_idx || is_done);
        const current = !is_failed && idx === stage_idx && !is_done;
        return `
            <div class="import-auto-fix-stage ${active ? "is-active" : ""} ${current ? "is-current" : ""}">
                <div class="import-auto-fix-stage__dot"></div>
                <div class="import-auto-fix-stage__label">${frappe.utils.escape_html(s.label)}</div>
            </div>
        `;
    }).join("");

    return `
        <div class="import-auto-fix-progress ${is_failed ? "is-failed" : ""}">
            <div class="import-auto-fix-progress__head">
                <div class="import-auto-fix-progress__icon ${is_failed ? "is-failed" : ""}">
                    ${is_failed
                        ? `<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="6" y1="6" x2="18" y2="18"/><line x1="6" y1="18" x2="18" y2="6"/></svg>`
                        : (is_done
                            ? `<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>`
                            : `<div class="import-auto-spinner"></div>`)}
                </div>
                <div class="import-auto-fix-progress__body">
                    <div class="import-auto-fix-progress__eyebrow">${__("AI Error Fix")}</div>
                    <div class="import-auto-fix-progress__message">${frappe.utils.escape_html(message || __("Processing..."))}</div>
                    ${file_name ? `<div class="import-auto-fix-progress__file">${frappe.utils.escape_html(file_name)}</div>` : ""}
                </div>
                <div class="import-auto-fix-progress__percent">${percent}<small>%</small></div>
            </div>
            <div class="import-auto-fix-progress__track">
                <div class="import-auto-fix-progress__fill" style="width: ${percent}%"></div>
            </div>
            <div class="import-auto-fix-progress__stages">${steps_html}</div>
            <div class="import-auto-fix-progress__hint">${__("You can close this window; results will still arrive via realtime notification.")}</div>
        </div>
    `;
}

function show_smart_fix_diff_dialog(frm, row_name, fix_result, parent_dialog) {
    const new_plan = fix_result.plan || {};
    const fixes = Array.isArray(fix_result.fixes) ? fix_result.fixes : [];
    const rejected = Array.isArray(fix_result.rejected) ? fix_result.rejected : [];
    const unresolved = Array.isArray(fix_result.unresolved) ? fix_result.unresolved : [];
    const proposals = Array.isArray(fix_result.new_dependency_steps) ? fix_result.new_dependency_steps : [];

    const has_changes = fixes.length > 0;
    const has_proposals = proposals.length > 0;

    let primary_label;
    if (has_proposals && has_changes) {
        primary_label = __("Create Missing Data & Re-run Script");
    } else if (has_proposals) {
        primary_label = __("Create Missing Data & Re-run Script ({0} items)", [proposals.length]);
    } else if (has_changes) {
        primary_label = __("Re-run Script ({0} changes)", [fixes.length]);
    } else {
        primary_label = __("Re-run Script (no changes)");
    }

    const dialog = new frappe.ui.Dialog({
        title: __("AI Fixed the Error - Review Before Re-running"),
        size: "extra-large",
        fields: [
            {
                fieldtype: "HTML",
                fieldname: "body",
                options: `${import_auto_styles()}${render_smart_fix_diff(fixes, rejected, unresolved, new_plan, proposals)}`,
            },
        ],
        primary_action_label: primary_label,
        primary_action() {
            // Collect checked proposals
            const $checks = dialog.$wrapper.find(".import-auto-dep-proposal__check:checked");
            const accepted_ids = $checks.map(function () { return $(this).data("proposal-id"); }).get();

            if (!has_proposals || accepted_ids.length === 0) {
                // No proposals to merge — straight to execute
                dialog.hide();
                execute_smart_plan(frm, row_name, new_plan, parent_dialog);
                return;
            }

            // Merge then execute
            dialog.hide();
            open_smart_fix_progress_dialog(frm, row_name);
            update_smart_fix_progress_dialog(frm, {
                row_name, stage: "merging", percent: 30,
                message: __("Merging {0} dependency steps into the plan...", [accepted_ids.length]),
            });
            frappe.call({
                method: `${IMPORT_AUTO_API}.confirm_smart_fix_dependencies`,
                args: {
                    docname: frm.doc.name,
                    file_row_name: row_name,
                    plan_json: JSON.stringify(new_plan),
                    proposals_json: JSON.stringify(proposals),
                    accepted_ids_json: JSON.stringify(accepted_ids),
                },
            }).then((response) => {
                const merged = (response.message || {}).plan || new_plan;
                close_smart_fix_progress_dialog(frm);
                frappe.show_alert({
                    message: __("Added {0} dependency steps - re-importing", [accepted_ids.length]),
                    indicator: "green",
                }, 5);
                execute_smart_plan(frm, row_name, merged, parent_dialog);
            }).catch((err) => {
                close_smart_fix_progress_dialog(frm);
                frappe.msgprint({
                    title: __("Cannot Merge Dependency Steps"),
                    indicator: "red",
                    message: (err && err.message) || __("Unknown error."),
                });
            });
        },
        secondary_action_label: __("Close"),
        secondary_action() {
            dialog.hide();
        },
    });
    if (unresolved.length || (has_proposals && !has_changes)) {
        dialog.$wrapper.find(".btn-primary").addClass("btn-warning");
    }
    dialog.show();
    // Wire up "select all / none" buttons for proposals
    dialog.$wrapper.find(".import-auto-dep-proposal__select-all").on("click", function () {
        const target = $(this).data("target");
        const checked = $(this).data("checked") !== "1";
        dialog.$wrapper.find(`.import-auto-dep-proposal__check[data-target="${target}"]`)
            .prop("checked", checked);
        $(this).data("checked", checked ? "1" : "0");
        $(this).text(checked ? __("Unselect All") : __("Select All"));
    });
}

function render_smart_fix_diff(fixes, rejected, unresolved, new_plan, proposals) {
    const summary = `
        <div class="import-auto-fix-summary">
            <div class="import-auto-fix-summary__item is-applied">
                <div class="import-auto-fix-summary__value">${fixes.length}</div>
                <div class="import-auto-fix-summary__label">${__("Fixed")}</div>
            </div>
            <div class="import-auto-fix-summary__item is-proposal">
                <div class="import-auto-fix-summary__value">${(proposals || []).reduce((s,p)=>s+(p.record_count||0),0)}</div>
                <div class="import-auto-fix-summary__label">${__("Proposed Dependencies")}</div>
            </div>
            <div class="import-auto-fix-summary__item is-rejected">
                <div class="import-auto-fix-summary__value">${rejected.length}</div>
                <div class="import-auto-fix-summary__label">${__("Rejected (protected data)")}</div>
            </div>
            <div class="import-auto-fix-summary__item is-unresolved">
                <div class="import-auto-fix-summary__value">${unresolved.length}</div>
                <div class="import-auto-fix-summary__label">${__("Unresolved")}</div>
            </div>
        </div>
    `;

    const fixes_table = fixes.length
        ? `
            <h5>${__("AI-applied Fixes")}</h5>
            <table class="table import-auto-fix-table">
                <thead>
                    <tr>
                        <th>${__("Step")}</th>
                        <th>${__("Row")}</th>
                        <th>${__("Field")}</th>
                        <th>${__("Old")}</th>
                        <th>${__("New")}</th>
                        <th>${__("Reason")}</th>
                    </tr>
                </thead>
                <tbody>
                    ${fixes.map((f) => `
                        <tr>
                            <td>${frappe.utils.escape_html(String(f.step || ""))}</td>
                            <td>${frappe.utils.escape_html(String(f.row || ""))}</td>
                            <td><code>${frappe.utils.escape_html(String(f.field || ""))}</code></td>
                            <td class="import-auto-fix-old">${frappe.utils.escape_html(format_fix_value(f.before))}</td>
                            <td class="import-auto-fix-new">${frappe.utils.escape_html(format_fix_value(f.after))}</td>
                            <td>${frappe.utils.escape_html(f.reason || "")}</td>
                        </tr>
                    `).join("")}
                </tbody>
            </table>
        `
        : `<div class="import-auto-fix-empty">${__("AI did not patch any fields; the plan may already be valid or the error is outside auto-fix scope.")}</div>`;

    const rejected_block = rejected.length
        ? `
            <details class="import-auto-fix-details">
                <summary>${__("{0} rejected changes (protected data)", [rejected.length])}</summary>
                <table class="table import-auto-fix-table import-auto-fix-table--rejected">
                    <thead><tr><th>${__("Step")}</th><th>${__("Row")}</th><th>${__("Field")}</th><th>${__("Reason")}</th></tr></thead>
                    <tbody>
                        ${rejected.map((r) => `
                            <tr>
                                <td>${frappe.utils.escape_html(String(r.step || ""))}</td>
                                <td>${frappe.utils.escape_html(String(r.row || ""))}</td>
                                <td><code>${frappe.utils.escape_html(String(r.field || ""))}</code></td>
                                <td>${frappe.utils.escape_html(r.reason || "")}</td>
                            </tr>
                        `).join("")}
                    </tbody>
                </table>
            </details>
        `
        : "";

    const unresolved_block = unresolved.length
        ? `
            <div class="import-auto-fix-unresolved">
                <h5>${__("AI Could Not Fix - Manual Action Needed")}</h5>
                <table class="table">
                    <thead><tr><th>${__("Step")}</th><th>${__("Row")}</th><th>${__("Reason")}</th></tr></thead>
                    <tbody>
                        ${unresolved.map((u) => `
                            <tr>
                                <td>${frappe.utils.escape_html(String(u.step || ""))}</td>
                                <td>${frappe.utils.escape_html(String(u.row || ""))}</td>
                                <td>${frappe.utils.escape_html(u.reason || "")}</td>
                            </tr>
                        `).join("")}
                    </tbody>
                </table>
                <div class="import-auto-fix-unresolved__hint">
                    ${__("You can still re-import, but missing required data may fail again.")}
                </div>
            </div>
        `
        : "";

    const proposals_block = render_smart_fix_proposals(proposals || []);

    return `
        <div class="import-auto-fix">
            ${summary}
            ${proposals_block}
            ${fixes_table}
            ${rejected_block}
            ${unresolved_block}
        </div>
    `;
}

function render_smart_fix_proposals(proposals) {
    if (!Array.isArray(proposals) || !proposals.length) return "";

    const blocks = proposals.map((p, idx) => {
        const target = p.target_doctype;
        const records = Array.isArray(p.records) ? p.records : [];
        const label_field = p.label_field || guess_label_field(target, records);
        const head_fields = pick_proposal_columns(records, label_field);
        const rows = records.map((rec, ridx) => {
            const checked = "checked";
            const cells = head_fields.map((f) => `<td>${frappe.utils.escape_html(format_proposal_value(rec[f]))}</td>`).join("");
            return `
                <tr>
                    <td class="import-auto-dep-proposal__check-cell">
                        <input type="checkbox" class="import-auto-dep-proposal__check"
                               data-proposal-id="${frappe.utils.escape_html(p.proposal_id || "")}"
                               data-record-index="${ridx}"
                               data-target="${frappe.utils.escape_html(target)}"
                               ${checked}>
                    </td>
                    ${cells}
                </tr>
            `;
        }).join("");

        const headers = head_fields.map((f) => `<th>${frappe.utils.escape_html(f)}</th>`).join("");
        const total_in_db = p.already_exists_count || 0;

        return `
            <div class="import-auto-dep-proposal" data-proposal-id="${frappe.utils.escape_html(p.proposal_id || "")}">
                <div class="import-auto-dep-proposal__head">
                    <div class="import-auto-dep-proposal__icon">
                        <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="12" y1="5" x2="12" y2="19"/>
                            <line x1="5" y1="12" x2="19" y2="12"/>
                        </svg>
                    </div>
                    <div class="import-auto-dep-proposal__body">
                        <div class="import-auto-dep-proposal__title">
                            ${frappe.utils.escape_html(target)}
                            <span class="import-auto-dep-proposal__count">${records.length} ${__("new records")}</span>
                            ${total_in_db ? `<span class="import-auto-dep-proposal__exists">${__("({0} already in DB, skipped)", [total_in_db])}</span>` : ""}
                        </div>
                        <div class="import-auto-dep-proposal__reason">${frappe.utils.escape_html(p.reason || "")}</div>
                        <div class="import-auto-dep-proposal__meta">
                            <span>${__("Insert before step")} <b>${p.insert_before_step || "?"}</b></span>
                            <span>${__("Deduplicate by")} <code>${frappe.utils.escape_html(p.unique_key || "name")}</code></span>
                        </div>
                    </div>
                    <button class="btn btn-xs import-auto-dep-proposal__select-all"
                            data-target="${frappe.utils.escape_html(target)}" data-checked="1">
                        ${__("Unselect All")}
                    </button>
                </div>
                <div class="import-auto-dep-proposal__table-wrap">
                    <table class="table import-auto-dep-proposal__table">
                        <thead>
                            <tr>
                                <th style="width:32px;">✓</th>
                                ${headers}
                            </tr>
                        </thead>
                        <tbody>
                            ${rows}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    }).join("");

    return `
        <div class="import-auto-dep-proposals">
            <div class="import-auto-dep-proposals__title">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M9 12l2 2 4-4"/>
                    <circle cx="12" cy="12" r="10"/>
                </svg>
                ${__("AI-proposed Dependency Data")}
            </div>
            <div class="import-auto-dep-proposals__hint">
                ${__("Uncheck records you do not want to create. Checked records are inserted first, then the original plan continues.")}
            </div>
            ${blocks}
        </div>
    `;
}

function pick_proposal_columns(records, label_field) {
    if (!records.length) return [];
    const all_keys = new Set();
    records.forEach((r) => Object.keys(r || {}).forEach((k) => all_keys.add(k)));
    const ordered = [];
    if (label_field && all_keys.has(label_field)) {
        ordered.push(label_field);
        all_keys.delete(label_field);
    }
    // Prefer common ID/label-ish fields first
    ["name", "department_name", "designation_name", "uom_name", "item_group_name",
     "warehouse_name", "cost_center_name", "territory_name",
     "customer_group_name", "supplier_group_name", "brand", "company",
     "parent_department", "parent_item_group", "parent_cost_center",
     "parent_warehouse", "parent_territory", "is_group"
    ].forEach((k) => {
        if (all_keys.has(k)) { ordered.push(k); all_keys.delete(k); }
    });
    Array.from(all_keys).forEach((k) => ordered.push(k));
    return ordered.slice(0, 6);
}

function format_proposal_value(v) {
    if (v === null || v === undefined || v === "") return "—";
    if (typeof v === "object") return JSON.stringify(v);
    return String(v);
}

function guess_label_field(doctype, records) {
    const key_by_doctype = {
        "Department": "department_name",
        "Designation": "designation_name",
        "Employee Grade": "name",
        "Branch": "branch",
        "Customer Group": "customer_group_name",
        "Supplier Group": "supplier_group_name",
        "Territory": "territory_name",
        "Item Group": "item_group_name",
        "UOM": "uom_name",
        "Brand": "brand",
        "Warehouse": "warehouse_name",
        "Cost Center": "cost_center_name",
        "Account": "account_name",
        "Project": "project_name",
    };
    if (key_by_doctype[doctype]) return key_by_doctype[doctype];
    if (records && records[0]) {
        const keys = Object.keys(records[0]);
        return keys[0] || "name";
    }
    return "name";
}

function format_fix_value(v) {
    if (v === null || v === undefined || v === "") return "—";
    if (typeof v === "object") return JSON.stringify(v);
    return String(v);
}
