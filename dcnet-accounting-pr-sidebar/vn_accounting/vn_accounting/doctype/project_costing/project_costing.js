// Project Costing form.
//
// Tab "Thông tin chính" renders 5 KPI cards (eager). Tab "Giai đoạn & Gắn
// chi phí" embeds the pivot UI (eager). The 5 list tabs (SI/PI/SE/TK154/PnL)
// lazy-load on first activation to avoid 5 RPC round-trips on form open.

frappe.ui.form.on("Project Costing", {
    refresh: function (frm) {
        if (frm.is_new()) {
            _render_placeholder(frm.fields_dict.summary_html,
                __("KPI sẽ hiển thị sau khi lưu công trình lần đầu."));
            ["stages_html", "si_html", "pi_html", "se_html", "tk154_html", "pnl_html"].forEach(f => {
                _render_placeholder(frm.fields_dict[f], __("Lưu công trình trước khi xem tab này."));
            });
            return;
        }

        // Eager: Thông tin chính + Giai đoạn (frequently used)
        _load_summary(frm);
        _render_pivot(frm);

        // Lazy: render each list tab when activated for the first time
        _setup_lazy_tabs(frm);
    },
});

const _TAB_LOADERS = {
    si_tab: { html_field: "si_html", loader: _render_sales_invoices },
    pi_tab: { html_field: "pi_html", loader: _render_purchase_invoices },
    se_tab: { html_field: "se_html", loader: _render_stock_entries },
    tk154_tab: { html_field: "tk154_html", loader: _render_tk154 },
    pnl_tab: { html_field: "pnl_html", loader: _render_pnl },
};

function _setup_lazy_tabs(frm) {
    if (frm.__pc_lazy_setup) return;
    frm.__pc_lazy_setup = true;
    Object.entries(_TAB_LOADERS).forEach(([tab_field, cfg]) => {
        _render_placeholder(frm.fields_dict[cfg.html_field],
            __("Đang chờ — nội dung sẽ tải khi bấm vào tab."));
    });
    // Hook tab click events on the rendered tab nav
    setTimeout(() => {
        const $tabs = $(frm.layout.wrapper).find('.form-tabs-list .nav-link');
        $tabs.off("click.pc_lazy").on("click.pc_lazy", function () {
            const target = $(this).attr("data-fieldname") || "";
            const cfg = _TAB_LOADERS[target];
            if (cfg && !frm[`__pc_loaded_${target}`]) {
                frm[`__pc_loaded_${target}`] = true;
                cfg.loader(frm);
            }
        });
    }, 200);
}

function _refresh_tab(frm, tab_field) {
    const cfg = _TAB_LOADERS[tab_field];
    if (!cfg) return;
    frm[`__pc_loaded_${tab_field}`] = true;
    cfg.loader(frm);
}

function _render_placeholder(field, html) {
    if (!field) return;
    field.$wrapper.html('<div class="text-muted small" style="padding:8px">' + html + "</div>");
}

// ─────────────────────────────────────────────────────────────────────────────
// Tab "Thông tin chính" — KPI dashboard
// ─────────────────────────────────────────────────────────────────────────────

function _load_summary(frm) {
    const field = frm.fields_dict.summary_html;
    if (!field) return;
    field.$wrapper.html(
        '<div class="text-muted small" style="padding:12px">' +
        __("Đang tải KPI...") + "</div>");

    frappe.call({
        method: "vn_accounting.project_costing.api.get_project_summary",
        args: { project_costing: frm.doc.name },
        callback: (r) => {
            if (!r || !r.message) return;
            _render_summary(frm, field, r.message);
        },
        error: () => {
            field.$wrapper.html(
                '<div class="text-danger small" style="padding:12px">' +
                __("Không tải được KPI. Thử reload trang.") + "</div>");
        },
    });
}

function _render_summary(frm, field, m) {
    const fmt = (v) => format_currency(flt(v), erpnext?.get_currency?.(m.company) || "VND", 0);
    const sc = m.stage_counts || {done: 0, in_progress: 0, pending: 0, total: 0};
    const margin_color = m.margin_pct >= 15 ? "text-success" : (m.margin_pct >= 0 ? "text-warning" : "text-danger");
    const last = m.last_activity ? frappe.datetime.str_to_user(m.last_activity) : __("Chưa có hoạt động");
    const wip_label = m.wip_account
        ? __("Số dư TK {0}", [m.wip_account.split(" - ")[0] || "154"])
        : __("Số dư chi phí dở dang (TK 154)");

    const card = (icon, label, value, sub, color) => `
        <div class="pc-kpi-card" style="
            flex:1; min-width:180px; padding:14px 16px;
            background:var(--card-bg); border:1px solid var(--border-color);
            border-radius:6px; box-shadow:0 1px 2px rgba(0,0,0,0.03);">
            <div class="text-muted" style="font-size:11px; text-transform:uppercase; letter-spacing:0.04em;">
                ${icon ? `<span style="margin-right:4px">${icon}</span>` : ""}${frappe.utils.escape_html(label)}
            </div>
            <div class="${color || ""}" style="font-size:20px; font-weight:600; margin-top:4px;">
                ${value}
            </div>
            ${sub ? `<div class="text-muted" style="font-size:11px; margin-top:2px;">${sub}</div>` : ""}
        </div>`;

    const stage_sub = `${sc.done}/${sc.total} ${__("hoàn thành")} · ${sc.in_progress} ${__("đang làm")} · ${sc.pending} ${__("chờ")}`;

    let close_banner = "";
    if (m.status === "Đã hoàn thành" && m.closed_on) {
        close_banner = `
            <div class="alert alert-success" style="padding:10px 12px; margin-bottom:12px; font-size:13px;">
                ✓ ${__("Công trình đã đóng ngày {0}", [frappe.datetime.str_to_user(m.closed_on)])}
                ${frm.doc.writeoff_je ? ` · ${__("Write-off JE")}: <a href="/app/journal-entry/${encodeURIComponent(frm.doc.writeoff_je)}" target="_blank">${frappe.utils.escape_html(frm.doc.writeoff_je)}</a>` : ""}
            </div>`;
    } else if (m.status === "Đã hủy") {
        close_banner = `<div class="alert alert-danger" style="padding:10px 12px; margin-bottom:12px;">⊘ ${__("Công trình đã hủy")}</div>`;
    }

    const html = `
        <div style="padding:8px 0 16px 0;">
            ${close_banner}
            <div style="display:flex; gap:12px; flex-wrap:wrap;">
                ${card("", __("Tổng CP đã tập hợp"), fmt(m.total_collected), __("Từ PI/SE/DN/EC/Salary"))}
                ${card("", __("Tổng HĐ đã xuất"), fmt(m.total_invoiced), __("Hóa đơn đã ghi nhận"))}
                ${card("", wip_label, fmt(m.wip_balance), __("GL Entry Dr − Cr"))}
                ${card("", __("Lãi gộp"), fmt(m.gross_profit), `${__("Tỷ suất LN")} ${m.margin_pct.toFixed(1)}%`, margin_color)}
                ${card("", __("Giai đoạn"), sc.total, stage_sub)}
            </div>
            <div style="margin-top:10px; font-size:11px; color:var(--text-muted);">
                ${__("Hoạt động gần nhất")}: ${last}
            </div>
        </div>`;

    field.$wrapper.html(html);

    _ensure_action_buttons(frm);
}

function _ensure_action_buttons(frm) {
    if (frm.__pc_actions_added) return;
    frm.__pc_actions_added = true;

    frm.add_custom_button(__("Báo cáo Lãi/Lỗ chi tiết"), () => {
        frappe.set_route("query-report", "Project PnL Detailed", {
            company: frm.doc.company,
            project: frm.doc.project,
        });
    }, __("Hành động"));

    frm.add_custom_button(__("Bảng tập hợp chi phí"), () => {
        frappe.set_route("query-report", "Project Cost Collection", {
            company: frm.doc.company,
            project: frm.doc.project,
        });
    }, __("Hành động"));

    // Đóng công trình / Mở lại — based on current status
    if (frm.doc.status === "Đang thi công") {
        frm.add_custom_button(__("Đóng công trình"), () => _open_close_dialog(frm), __("Hành động"));
    } else if (frm.doc.status === "Đã hoàn thành") {
        frm.add_custom_button(__("Mở lại công trình"), () => _open_reopen_dialog(frm), __("Hành động"));
    }
}

function _open_close_dialog(frm) {
    // Step 1: probe balance via close() with force=false
    frappe.call({
        doc: frm.doc,
        method: "close",
        args: { force: 0 },
        callback: (r) => {
            const res = r.message || {};
            if (!res.needs_decision) {
                // Clean close (balance == 0) — already done
                frappe.show_alert({ message: __("Đã đóng công trình."), indicator: "green" });
                frm.reload_doc();
                return;
            }
            // Balance non-zero — show write-off decision dialog
            const bal = flt(res.balance);
            const d = new frappe.ui.Dialog({
                title: __("Đóng công trình — quyết định Write-off"),
                fields: [
                    {
                        fieldname: "info",
                        fieldtype: "HTML",
                        options: `<div style="padding:8px 0">
                            <div class="alert alert-warning" style="padding:10px;">
                                <strong>${__("Số dư TK 154 còn")}: ${format_currency(bal, "VND", 0)}</strong><br>
                                ${__("Đóng công trình sẽ tạo bút toán write-off để cân bằng:")} ${bal > 0 ? "Dr Write-off / Cr 154" : "Dr 154 / Cr Write-off"}.
                            </div>
                            <div class="text-muted small">
                                ${__("VAS chuẩn: số dư dương = chi phí dư chưa recognize → write-off vào TK 642 (chi phí QLDN).")}<br>
                                ${__("Nếu là giá vốn không phân bổ được → chọn TK 632 (giá vốn).")}
                            </div>
                        </div>`,
                    },
                    {
                        fieldname: "writeoff_account",
                        fieldtype: "Link",
                        options: "Account",
                        label: __("Tài khoản write-off"),
                        get_query: () => ({
                            filters: {
                                company: frm.doc.company,
                                is_group: 0,
                                root_type: "Expense",
                            },
                        }),
                        description: __("Mặc định lấy từ Cài đặt VN Accounting (TK 642). Có thể chọn 632 nếu là giá vốn."),
                    },
                ],
                primary_action_label: __("Xác nhận đóng + tạo write-off"),
                primary_action: (values) => {
                    frappe.call({
                        doc: frm.doc,
                        method: "close",
                        args: {
                            writeoff_account: values.writeoff_account || null,
                            force: 1,
                        },
                        callback: (r2) => {
                            const res2 = r2.message || {};
                            frappe.show_alert({
                                message: res2.writeoff_je
                                    ? __("Đã đóng + tạo write-off JE {0}", [res2.writeoff_je])
                                    : __("Đã đóng công trình."),
                                indicator: "green",
                            });
                            d.hide();
                            frm.reload_doc();
                        },
                    });
                },
                secondary_action_label: __("Hủy"),
                secondary_action: () => d.hide(),
            });
            d.show();
        },
    });
}

function _open_reopen_dialog(frm) {
    frappe.confirm(
        __("Mở lại công trình? Nếu có write-off JE, JE đó sẽ bị hủy (cần ghi nhận lý do mở lại)."),
        () => {
            frappe.call({
                doc: frm.doc,
                method: "reopen",
                callback: () => {
                    frappe.show_alert({ message: __("Đã mở lại."), indicator: "blue" });
                    frm.reload_doc();
                },
            });
        }
    );
}

// ─────────────────────────────────────────────────────────────────────────────
// Tab "Giai đoạn & Gắn chi phí" — embedded Pivot (was separate Page before phase 2)
// ─────────────────────────────────────────────────────────────────────────────

function _render_pivot(frm) {
    const field = frm.fields_dict.stages_html;
    if (!field) return;
    field.$wrapper.html(
        '<div class="text-muted small" style="padding:12px">' +
        __("Đang tải Pivot...") + "</div>");

    frappe.call({
        method: "vn_accounting.project_costing.services.pivot_service.get_pivot_data",
        args: { costing_name: frm.doc.name },
        callback: (r) => {
            if (!r || !r.message || !r.message.costing) {
                field.$wrapper.html(
                    '<div class="text-danger small" style="padding:12px">' +
                    __("Không tải được dữ liệu Pivot.") + "</div>");
                return;
            }
            _render_pivot_html(frm, field, r.message);
        },
        error: () => {
            field.$wrapper.html(
                '<div class="text-danger small" style="padding:12px">' +
                __("Không tải được dữ liệu Pivot.") + "</div>");
        },
    });
}

function _render_pivot_html(frm, field, data) {
    const stages = data.stages || [];
    const common_pool = data.common_pool || [];

    const header = `
        <div style="display:flex; justify-content:space-between; align-items:center; padding:8px 0 12px; gap:12px; flex-wrap:wrap;">
            <div class="text-muted small">${__("Gắn chi phí từ Tập hợp chi phí chưa gắn vào từng giai đoạn để tính giá thành.")}</div>
            <div style="display:flex; gap:6px;">
                <button class="btn btn-xs btn-primary vn-pc-gen-project-si">${__("+ Tạo HĐ dự án (không theo giai đoạn)")}</button>
                <button class="btn btn-xs btn-default vn-pc-refresh">${__("Tải lại")}</button>
            </div>
        </div>`;

    const cp_html = common_pool.length
        ? _pivot_common_pool_banner(common_pool)
        : `<div class="text-muted small" style="padding:8px 0 12px; border-bottom:1px solid var(--border-color); margin-bottom:12px;">
              ✓ ${__("Mọi chi phí của công trình đã được gắn vào giai đoạn — không còn chi phí cần xử lý.")}
           </div>`;

    const stages_html = stages.length
        ? `<div class="pivot-stages-grid" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:12px;">
              ${stages.map(s => _pivot_stage_card(s)).join("")}
           </div>`
        : `<div class="text-muted text-center" style="padding:30px; border:1px dashed var(--border-color); border-radius:6px;">
              ${__("Công trình chưa có giai đoạn nào. Thêm giai đoạn qua menu Liên kết → Giai đoạn công trình.")}
           </div>`;

    field.$wrapper.html(`${header}${cp_html}${stages_html}`);

    _pivot_bind_actions(frm, field);
}

function _pivot_status_indicator(status) {
    const colors = {
        "Đang thi công": "blue",
        "Đã hoàn thành": "green",
        "Đã hủy": "red",
        "Chờ xuất HĐ": "orange",
        "Đã xuất HĐ": "green",
        "Đã thu tiền": "green",
        "Đã có SI draft": "blue",
        "Dự kiến": "gray",
    };
    const color = colors[status] || "gray";
    return `<span class="indicator ${color}">${frappe.utils.escape_html(status || "")}</span>`;
}

function _pivot_stage_card(stage) {
    const is_locked = !!stage.cogs_je;
    const items_html = (stage.items || []).map(it => _pivot_cost_card(it, false, is_locked)).join("") ||
        `<div class="text-muted text-center" style="padding:16px 8px; font-size:12px">${__("Chưa có chi phí gắn")}</div>`;

    const target_price = flt(stage.price_override) || flt(stage.price_suggested);
    const invoiced = flt(stage.invoiced_total);
    const remaining = target_price - invoiced;
    const price_display = stage.price_override
        ? `<strong>${format_currency(stage.price_override, "VND", 0)}</strong>
           <span class="text-muted" style="font-size:10px"> (${__("đề xuất")} ${format_currency(stage.price_suggested || 0, "VND", 0)})</span>`
        : `<strong>${format_currency(stage.price_suggested || 0, "VND", 0)}</strong>`;

    const invoices = stage.invoices || [];
    const invoices_html = invoices.length ? `
        <div style="margin-top:4px; padding-top:4px; border-top:1px dotted var(--border-color); font-size:11px;">
            <div class="text-muted" style="font-size:10px;">${__("Hóa đơn đã tạo")} (${invoices.length})</div>
            ${invoices.map(si => {
                const st_color = si.docstatus === 0 ? "orange" : (si.status === "Paid" ? "green" : "blue");
                const st_text = si.docstatus === 0 ? __("Nháp") : (si.status || __("Đã ghi nhận"));
                return `<div style="display:flex; justify-content:space-between; gap:4px; align-items:center;">
                    <a href="/app/sales-invoice/${encodeURIComponent(si.name)}" target="_blank" style="font-size:11px; flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${frappe.utils.escape_html(si.name)}</a>
                    <span style="font-size:11px;"><strong>${format_currency(si.amount, "VND", 0)}</strong></span>
                    <span class="indicator-pill ${st_color}" style="font-size:9px;">${frappe.utils.escape_html(st_text)}</span>
                </div>`;
            }).join("")}
            <div style="display:flex; justify-content:space-between; margin-top:2px; font-size:11px; color:var(--text-muted);">
                <span>${__("Đã xuất")} / ${__("còn")}</span>
                <span><strong>${format_currency(invoiced, "VND", 0)}</strong> / ${format_currency(Math.max(remaining, 0), "VND", 0)}</span>
            </div>
        </div>` : "";

    const lock_border = is_locked ? "border-color:#e8a84c;" : "";
    const lock_badge = is_locked
        ? ` <span style="font-size:10px; color:#c77c11; font-weight:normal;" title="${__("Đã xuất HĐ — giá vốn đã khóa, không thể thêm/bỏ chi phí")}">🔒</span>`
        : "";
    const drop_class = is_locked ? "" : "vn-pc-drop-target";

    return `
        <div class="pivot-stage" style="border:1px solid var(--border-color); border-radius:6px; background:var(--card-bg); padding:10px; display:flex; flex-direction:column; min-width:0; ${lock_border}">
            <div style="border-bottom:1px solid var(--border-color); padding-bottom:6px; margin-bottom:8px;">
                <div style="font-weight:600; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${__("Giai đoạn")} ${stage.stage_order} — ${frappe.utils.escape_html(stage.stage_name)}${lock_badge}</div>
                <div style="font-size:11px; margin-top:2px;">${_pivot_status_indicator(stage.status)}</div>
            </div>
            <div style="background:var(--bg-light-gray); padding:6px 8px; border-radius:4px; margin-bottom:8px; font-size:12px; line-height:1.5;">
                <div><span class="text-muted">${__("Hệ số markup")}:</span> ${frappe.utils.escape_html(stage.markup_method || "—")} <strong>${stage.markup_value || 0}</strong></div>
                <div><span class="text-muted">${__("CP đã gắn")}:</span> <strong>${format_currency(stage.pinned_total || 0, "VND", 0)}</strong></div>
                <div><span class="text-muted">${__("Giá xuất HĐ")}:</span> ${price_display}</div>
                ${invoices_html}
            </div>
            ${is_locked ? `<div style="background:#fef3e2; border:1px solid #e8a84c; border-radius:4px; padding:4px 8px; margin-bottom:8px; font-size:11px; color:#8a5a00;">🔒 ${__("Đã xuất HĐ — giá vốn đã khóa. Không thể thêm/bỏ chi phí.")}</div>` : ""}
            <div style="display:flex; gap:4px; margin-bottom:8px;">
                <button class="btn btn-xs btn-default vn-pc-recalc" data-stage="${frappe.utils.escape_html(stage.name)}">${__("Tính lại")}</button>
                <button class="btn btn-xs btn-primary vn-pc-gen-si" data-stage="${frappe.utils.escape_html(stage.name)}" data-remaining="${remaining}" data-target="${target_price}">${invoices.length ? __("+ Hóa đơn") : __("Tạo HĐ")}</button>
            </div>
            <div class="pivot-stage-items ${drop_class}" data-stage="${frappe.utils.escape_html(stage.name)}" style="flex:1; overflow-y:auto; max-height:320px;">
                ${items_html}
            </div>
        </div>`;
}

function _pivot_common_pool_banner(items) {
    const items_html = items.map(it => _pivot_cost_card(it, /*compact*/ true)).join("");
    const big = items.length > 20;
    return `
        <div class="pivot-common-pool" style="border:2px dashed var(--border-color); border-radius:6px; background:var(--bg-light-gray); padding:10px 12px; margin-bottom:16px;">
            <div style="display:flex; justify-content:space-between; align-items:baseline; flex-wrap:wrap; gap:8px; margin-bottom:8px;">
                <div style="font-weight:600;">
                    📥 ${__("Tập hợp chi phí chưa gắn")}
                    <span class="text-muted" style="font-weight:normal; font-size:12px">
                        (<span class="vn-pc-cp-count">${items.length}</span> ${__("chi phí")},
                        ${__("tổng")} <strong>${format_currency(items.reduce((s, it) => s + flt(it.amount), 0), "VND", 0)}</strong>)
                    </span>
                </div>
                <div style="display:flex; gap:6px; align-items:center;">
                    <input type="search" class="form-control input-xs vn-pc-cp-search" placeholder="${__("Tìm theo mô tả / chứng từ...")}" style="width:220px; height:24px; font-size:12px;">
                    <span class="text-muted small">${__("Kéo thả vào ô giai đoạn ở dưới")}</span>
                </div>
            </div>
            <div class="vn-pc-cp-body vn-pc-drop-target" data-stage="" style="${big ? "max-height:240px; overflow-y:auto;" : ""}">
                <div class="vn-pc-cp-grid" style="display:grid; grid-template-columns:repeat(auto-fill, minmax(240px, 1fr)); gap:8px;">
                    ${items_html}
                </div>
            </div>
        </div>`;
}

function _pivot_cost_card(item, compact, stage_locked) {
    const subtitle = item.posting_date ? frappe.datetime.str_to_user(item.posting_date).split(" ")[0] : "";
    const src_dt_slug = (item.source_doctype || "").toLowerCase().replace(/\s+/g, "-");
    const src_url = `/app/${src_dt_slug}/${encodeURIComponent(item.source_name || "")}`;
    const search_key = `${item.description || ""} ${item.source_doctype || ""} ${item.source_name || ""} ${item.amount || ""}`.toLowerCase();
    const draggable = stage_locked ? "false" : "true";
    const cursor = stage_locked ? "default" : "grab";
    const lock_style = stage_locked ? "opacity:0.7; background:#fef9ee;" : "background:var(--card-bg);";
    return `
        <div class="pivot-cost-card vn-pc-cost-card" draggable="${draggable}" style="border:1px solid var(--border-color); border-radius:4px; padding:6px 8px; margin-bottom:${compact ? "0" : "6px"}; ${lock_style} font-size:12px; min-width:0; cursor:${cursor};"
             data-src-dt="${frappe.utils.escape_html(item.source_doctype)}"
             data-src-name="${frappe.utils.escape_html(item.source_name)}"
             data-src-row="${frappe.utils.escape_html(item.source_row || "")}"
             data-stage="${frappe.utils.escape_html(item.stage || "")}"
             data-search="${frappe.utils.escape_html(search_key)}">
            <div style="display:flex; justify-content:space-between; gap:6px; min-width:0;">
                <div style="flex:1; min-width:0;">
                    <div style="font-weight:500; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;" title="${frappe.utils.escape_html(item.description || "")}">
                        ${frappe.utils.escape_html(item.description || "")}
                    </div>
                    <div class="text-muted" style="font-size:10px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                        ${frappe.utils.escape_html(item.source_doctype)} ·
                        <a href="${src_url}" target="_blank" style="color:inherit; text-decoration:underline;" title="${__("Mở chứng từ")}">${frappe.utils.escape_html(item.source_name)}</a>
                        · ${subtitle}
                    </div>
                </div>
                <div style="font-weight:600; white-space:nowrap;">${format_currency(item.amount, "VND", 0)}</div>
            </div>
            <div style="margin-top:4px; text-align:right;">
                <button class="btn btn-xs btn-link vn-pc-pin-btn" data-action="pin" style="padding:0 4px;">${__("Gắn")}</button>
            </div>
        </div>`;
}

function _pivot_bind_actions(frm, field) {
    const $body = field.$wrapper;

    $body.off("click", ".vn-pc-refresh").on("click", ".vn-pc-refresh", () => _render_pivot(frm));

    $body.off("click", ".vn-pc-pin-btn").on("click", ".vn-pc-pin-btn", function (e) {
        e.stopPropagation();
        const $card = $(this).closest(".vn-pc-cost-card");
        _pivot_open_pin_dialog(frm, $card);
    });

    $body.off("click", ".vn-pc-recalc").on("click", ".vn-pc-recalc", function () {
        const stage = $(this).data("stage");
        frappe.call({
            method: "vn_accounting.project_costing.services.pivot_service.recalculate_stage_price",
            args: { stage_name: stage },
            callback: (r) => {
                if (r.message) {
                    frappe.show_alert({
                        message: __("Đã tính lại: cost {0}, giá đề xuất {1}",
                            [format_currency(r.message.cost_pinned, "VND", 0),
                             format_currency(r.message.price_suggested, "VND", 0)]),
                        indicator: "blue",
                    });
                    _render_pivot(frm);
                }
            },
        });
    });

    $body.off("click", ".vn-pc-gen-si").on("click", ".vn-pc-gen-si", function () {
        const $btn = $(this);
        const stage = $btn.data("stage");
        const remaining = flt($btn.data("remaining"));
        const target = flt($btn.data("target"));
        _open_stage_si_dialog(frm, stage, remaining, target);
    });

    $body.off("click", ".vn-pc-gen-project-si").on("click", ".vn-pc-gen-project-si", function () {
        _open_project_si_dialog(frm);
    });

    // Common Pool search filter (client-side)
    $body.off("input", ".vn-pc-cp-search").on("input", ".vn-pc-cp-search", function () {
        const q = ($(this).val() || "").toLowerCase().trim();
        const $cards = $body.find(".vn-pc-cp-grid .vn-pc-cost-card");
        let shown = 0;
        $cards.each(function () {
            const hay = $(this).data("search") || "";
            const match = !q || String(hay).indexOf(q) !== -1;
            $(this).toggle(match);
            if (match) shown++;
        });
        $body.find(".vn-pc-cp-count").text(shown === $cards.length ? $cards.length : `${shown}/${$cards.length}`);
    });

    // HTML5 drag & drop — drag cost card into stage drop target
    $body.off("dragstart", ".vn-pc-cost-card").on("dragstart", ".vn-pc-cost-card", function (e) {
        const $card = $(this);
        const payload = {
            src_dt: $card.data("src-dt"),
            src_name: $card.data("src-name"),
            src_row: $card.data("src-row") || "",
            current_stage: $card.data("stage") || "",
        };
        e.originalEvent.dataTransfer.effectAllowed = "move";
        e.originalEvent.dataTransfer.setData("text/plain", JSON.stringify(payload));
        $card.css("opacity", "0.4");
    });

    $body.off("dragend", ".vn-pc-cost-card").on("dragend", ".vn-pc-cost-card", function () {
        $(this).css("opacity", "");
    });

    $body.off("dragover", ".vn-pc-drop-target").on("dragover", ".vn-pc-drop-target", function (e) {
        e.preventDefault();
        e.originalEvent.dataTransfer.dropEffect = "move";
        $(this).css("background", "var(--bg-light-blue, #e8f0fe)");
    });

    $body.off("dragleave", ".vn-pc-drop-target").on("dragleave", ".vn-pc-drop-target", function () {
        $(this).css("background", "");
    });

    $body.off("drop", ".vn-pc-drop-target").on("drop", ".vn-pc-drop-target", function (e) {
        e.preventDefault();
        $(this).css("background", "");
        let payload;
        try { payload = JSON.parse(e.originalEvent.dataTransfer.getData("text/plain")); }
        catch (err) { return; }
        const target_stage = $(this).data("stage") || "";
        if (target_stage === payload.current_stage) return;  // same target — noop
        frappe.call({
            method: "vn_accounting.project_costing.services.pivot_service.pin_cost_to_stage",
            args: {
                source_doctype: payload.src_dt,
                source_name: payload.src_name,
                source_row: payload.src_row || null,
                stage_name: target_stage || null,
            },
            callback: (r) => {
                if (r.message) {
                    frappe.show_alert({
                        message: target_stage ? __("Đã gắn vào giai đoạn") : __("Đã bỏ gắn"),
                        indicator: "green",
                    });
                    _render_pivot(frm);
                    _load_summary(frm);
                }
            },
        });
    });
}

function _pivot_open_pin_dialog(frm, $card) {
    const src_dt = $card.data("src-dt");
    const src_name = $card.data("src-name");
    const src_row = $card.data("src-row");
    const current_stage = $card.data("stage") || "";

    const stages = (frm.__pivot_stages_cache || []);

    frappe.call({
        method: "vn_accounting.project_costing.services.pivot_service.get_pivot_data",
        args: { costing_name: frm.doc.name },
        callback: (r) => {
            const fresh_stages = (r.message && r.message.stages) || stages;
            frm.__pivot_stages_cache = fresh_stages;
            _pivot_show_pin_dialog(frm, src_dt, src_name, src_row, current_stage, fresh_stages);
        },
    });
}

function _pivot_show_pin_dialog(frm, src_dt, src_name, src_row, current_stage, stages) {
    const options = [
        { label: __("(Bỏ gắn — trả về Tập hợp chi phí chưa gắn)"), value: "" },
        ...stages.map(s => ({
            label: `${s.stage_order} — ${s.stage_name} (${s.status})`,
            value: s.name,
        })),
    ];

    const d = new frappe.ui.Dialog({
        title: __("Gắn chi phí vào giai đoạn"),
        fields: [
            {
                fieldname: "current",
                fieldtype: "HTML",
                options: `<div class="text-muted">${frappe.utils.escape_html(src_dt)} · ${frappe.utils.escape_html(src_name)}${src_row ? " · row " + src_row : ""}</div>`,
            },
            {
                fieldname: "stage",
                fieldtype: "Select",
                label: __("Giai đoạn"),
                options: options.map(o => `${o.value}|${o.label}`).join("\n"),
                default: current_stage,
                reqd: 0,
            },
        ],
        primary_action_label: __("Gắn"),
        primary_action: (values) => {
            const v = values.stage || "";
            const stage_value = v.split("|")[0];
            frappe.call({
                method: "vn_accounting.project_costing.services.pivot_service.pin_cost_to_stage",
                args: {
                    source_doctype: src_dt,
                    source_name: src_name,
                    source_row: src_row || null,
                    stage_name: stage_value || null,
                },
                callback: (r) => {
                    if (r.message) {
                        frappe.show_alert({
                            message: __("Đã gắn"),
                            indicator: "green",
                        });
                        d.hide();
                        _render_pivot(frm);
                        _load_summary(frm);
                    }
                },
            });
        },
    });
    d.show();
}

// ─────────────────────────────────────────────────────────────────────────────
// Lazy-loaded list tabs (SI / PI / SE / TK 154 / PnL)
// ─────────────────────────────────────────────────────────────────────────────

function _doc_link(doctype, name) {
    const slug = (doctype || "").toLowerCase().replace(/\s+/g, "-");
    return `<a href="/app/${slug}/${encodeURIComponent(name)}" target="_blank">${frappe.utils.escape_html(name)}</a>`;
}

function _money(v) { return format_currency(flt(v), "VND", 0); }
function _date(v) { return v ? frappe.datetime.str_to_user(v).split(" ")[0] : ""; }

function _list_table_shell(field, title, refresh_id, body_html) {
    field.$wrapper.html(`
        <div style="padding:8px 0 12px; display:flex; justify-content:space-between; align-items:center; gap:12px;">
            <div style="font-weight:600;">${title}</div>
            <button class="btn btn-xs btn-default" data-refresh="${refresh_id}">${__("Tải lại")}</button>
        </div>
        ${body_html}`);
}

function _empty_state(msg) {
    return `<div class="text-muted text-center" style="padding:24px; border:1px dashed var(--border-color); border-radius:6px;">${msg}</div>`;
}

function _render_sales_invoices(frm) {
    const field = frm.fields_dict.si_html;
    _render_placeholder(field, __("Đang tải hóa đơn đầu ra..."));
    frappe.call({
        method: "vn_accounting.project_costing.api.get_sales_invoices_for_project",
        args: { project_costing: frm.doc.name },
        callback: (r) => {
            const d = r.message || {};
            const rows = d.rows || [];
            const title = __("Hóa đơn đầu ra") + ` <span class="text-muted" style="font-weight:normal; font-size:12px">(${d.count || 0} ${__("hóa đơn")}, ${__("tổng")} <strong>${_money(d.total)}</strong>, ${__("còn nợ")} <strong>${_money(d.outstanding_total)}</strong>)</span>`;
            if (!rows.length) {
                _list_table_shell(field, title, "si", _empty_state(__("Chưa có hóa đơn bán nào tag dự án này.")));
                return;
            }
            const body = `
                <table class="table table-sm table-bordered" style="font-size:12px;">
                  <thead><tr>
                    <th>${__("Ngày")}</th><th>${__("Số HĐ")}</th><th>${__("Khách hàng")}</th>
                    <th style="text-align:right;">${__("Tổng tiền")}</th>
                    <th style="text-align:right;">${__("Còn nợ")}</th>
                    <th>${__("Hạn TT")}</th><th>${__("Trạng thái")}</th>
                  </tr></thead>
                  <tbody>
                    ${rows.map(r => `
                      <tr>
                        <td>${_date(r.posting_date)}</td>
                        <td>${_doc_link("Sales Invoice", r.name)}</td>
                        <td>${frappe.utils.escape_html(r.customer_name || r.customer || "")}</td>
                        <td style="text-align:right;"><strong>${_money(r.grand_total)}</strong></td>
                        <td style="text-align:right;">${_money(r.outstanding_amount)}</td>
                        <td>${_date(r.due_date)}</td>
                        <td><span class="indicator ${r.status === 'Paid' ? 'green' : r.status === 'Overdue' ? 'red' : 'orange'}">${frappe.utils.escape_html(r.status || "")}</span></td>
                      </tr>`).join("")}
                  </tbody>
                </table>`;
            _list_table_shell(field, title, "si", body);
            field.$wrapper.off("click", "[data-refresh='si']").on("click", "[data-refresh='si']", () => _render_sales_invoices(frm));
        },
    });
}

function _render_purchase_invoices(frm) {
    const field = frm.fields_dict.pi_html;
    _render_placeholder(field, __("Đang tải hóa đơn đầu vào..."));
    frappe.call({
        method: "vn_accounting.project_costing.api.get_purchase_invoices_for_project",
        args: { project_costing: frm.doc.name },
        callback: (r) => {
            const d = r.message || {};
            const rows = d.rows || [];
            const title = __("Hóa đơn đầu vào") + ` <span class="text-muted" style="font-weight:normal; font-size:12px">(${d.count || 0} ${__("hóa đơn")}, ${__("CP gắn dự án")} <strong>${_money(d.project_amount_total)}</strong>, ${__("còn nợ NCC")} <strong>${_money(d.outstanding_total)}</strong>)</span>`;
            if (!rows.length) {
                _list_table_shell(field, title, "pi", _empty_state(__("Chưa có hóa đơn mua nào tag dự án này.")));
                return;
            }
            const body = `
                <table class="table table-sm table-bordered" style="font-size:12px;">
                  <thead><tr>
                    <th>${__("Ngày")}</th><th>${__("Số HĐ")}</th><th>${__("Nhà cung cấp")}</th>
                    <th style="text-align:right;">${__("CP gắn dự án")}</th>
                    <th style="text-align:right;">${__("Tổng HĐ")}</th>
                    <th style="text-align:right;">${__("Còn phải trả")}</th>
                    <th>${__("Hạn TT")}</th><th>${__("Trạng thái")}</th>
                  </tr></thead>
                  <tbody>
                    ${rows.map(r => `
                      <tr>
                        <td>${_date(r.posting_date)}</td>
                        <td>${_doc_link("Purchase Invoice", r.name)}</td>
                        <td>${frappe.utils.escape_html(r.supplier_name || r.supplier || "")}</td>
                        <td style="text-align:right;"><strong>${_money(r.project_amount)}</strong></td>
                        <td style="text-align:right;">${_money(r.grand_total)}</td>
                        <td style="text-align:right;">${_money(r.outstanding_amount)}</td>
                        <td>${_date(r.due_date)}</td>
                        <td><span class="indicator ${r.status === 'Paid' ? 'green' : r.status === 'Overdue' ? 'red' : 'orange'}">${frappe.utils.escape_html(r.status || "")}</span></td>
                      </tr>`).join("")}
                  </tbody>
                </table>`;
            _list_table_shell(field, title, "pi", body);
            field.$wrapper.off("click", "[data-refresh='pi']").on("click", "[data-refresh='pi']", () => _render_purchase_invoices(frm));
        },
    });
}

function _render_stock_entries(frm) {
    const field = frm.fields_dict.se_html;
    _render_placeholder(field, __("Đang tải phiếu xuất nhập kho..."));
    frappe.call({
        method: "vn_accounting.project_costing.api.get_stock_entries_for_project",
        args: { project_costing: frm.doc.name },
        callback: (r) => {
            const d = r.message || {};
            const rows = d.rows || [];
            const title = __("Điều chuyển kho dự án") + ` <span class="text-muted" style="font-weight:normal; font-size:12px">(${d.count || 0} ${__("phiếu")}, ${__("tổng giá trị")} <strong>${_money(d.total)}</strong>)</span>`;
            if (!rows.length) {
                _list_table_shell(field, title, "se", _empty_state(__("Chưa có phiếu xuất/nhập kho nào tag dự án này.")));
                return;
            }
            const body = `
                <table class="table table-sm table-bordered" style="font-size:12px;">
                  <thead><tr>
                    <th>${__("Ngày")}</th><th>${__("Số phiếu")}</th><th>${__("Loại")}</th>
                    <th>${__("Kho xuất")}</th><th>${__("Kho nhập")}</th>
                    <th style="text-align:right;">${__("Giá trị")}</th>
                    <th>${__("Ghi chú")}</th>
                  </tr></thead>
                  <tbody>
                    ${rows.map(r => `
                      <tr>
                        <td>${_date(r.posting_date)}</td>
                        <td>${_doc_link("Stock Entry", r.name)}</td>
                        <td>${frappe.utils.escape_html(r.stock_entry_type || "")}</td>
                        <td>${frappe.utils.escape_html(r.from_warehouse || "—")}</td>
                        <td>${frappe.utils.escape_html(r.to_warehouse || "—")}</td>
                        <td style="text-align:right;"><strong>${_money(r.amount)}</strong></td>
                        <td style="font-size:11px; color:var(--text-muted);">${frappe.utils.escape_html((r.remarks || "").slice(0, 80))}</td>
                      </tr>`).join("")}
                  </tbody>
                </table>`;
            _list_table_shell(field, title, "se", body);
            field.$wrapper.off("click", "[data-refresh='se']").on("click", "[data-refresh='se']", () => _render_stock_entries(frm));
        },
    });
}

function _render_tk154(frm) {
    const field = frm.fields_dict.tk154_html;
    _render_placeholder(field, __("Đang tải bút toán TK 154..."));
    frappe.call({
        method: "vn_accounting.project_costing.api.get_tk154_entries_for_project",
        args: { project_costing: frm.doc.name },
        callback: (r) => {
            const d = r.message || {};
            const rows = d.rows || [];
            const wip_code = (d.wip_account || "").split(" - ")[0] || "154";
            const title = __("Bút toán TK {0}", [wip_code]) + ` <span class="text-muted" style="font-weight:normal; font-size:12px">(${d.count || 0} ${__("dòng")}, ${__("Nợ")} <strong>${_money(d.total_debit)}</strong> · ${__("Có")} <strong>${_money(d.total_credit)}</strong> · ${__("Số dư")} <strong>${_money(d.balance)}</strong>)</span>`;
            if (!rows.length) {
                _list_table_shell(field, title, "tk154", _empty_state(__("Chưa có bút toán nào trên TK 154 cho dự án này.")));
                return;
            }
            const body = `
                <table class="table table-sm table-bordered" style="font-size:12px;">
                  <thead><tr>
                    <th>${__("Ngày")}</th><th>${__("Số BT")}</th>
                    <th>${__("Chứng từ nguồn")}</th><th>${__("Giai đoạn")}</th>
                    <th style="text-align:right;">${__("Nợ")}</th>
                    <th style="text-align:right;">${__("Có")}</th>
                    <th>${__("Diễn giải")}</th>
                  </tr></thead>
                  <tbody>
                    ${rows.map(r => {
                        const locked = r.stage_locked;
                        const rowStyle = locked ? ' style="background:#fef3e2; opacity:0.85;"' : '';
                        const stageHtml = r.stage
                            ? (locked
                                ? `<span class="indicator orange" title="${__("Đã xuất HĐ — giá vốn đã khóa")}">🔒 ${frappe.utils.escape_html(r.stage)}</span>`
                                : `<span class="indicator blue">${frappe.utils.escape_html(r.stage)}</span>`)
                            : `<span class="text-muted">${__("(chưa gắn)")}</span>`;
                        return `
                      <tr${rowStyle}>
                        <td>${_date(r.posting_date)}</td>
                        <td>${_doc_link("Journal Entry", r.voucher_no)}</td>
                        <td>${r.reference_type ? `${frappe.utils.escape_html(r.reference_type)}<br><span style="font-size:11px;">${r.reference_name ? _doc_link(r.reference_type, r.reference_name) : ""}</span>` : "—"}</td>
                        <td>${stageHtml}</td>
                        <td style="text-align:right;"><strong>${flt(r.debit) > 0 ? _money(r.debit) : ""}</strong></td>
                        <td style="text-align:right;"><strong>${flt(r.credit) > 0 ? _money(r.credit) : ""}</strong></td>
                        <td style="font-size:11px; color:var(--text-muted);">${frappe.utils.escape_html((r.remarks || "").slice(0, 100))}</td>
                      </tr>`;
                    }).join("")}
                    <tr style="background:var(--bg-light-gray); font-weight:600;">
                      <td colspan="4" style="text-align:right;">${__("TỔNG")}</td>
                      <td style="text-align:right;">${_money(d.total_debit)}</td>
                      <td style="text-align:right;">${_money(d.total_credit)}</td>
                      <td>${__("Số dư Nợ")}: ${_money(d.balance)}</td>
                    </tr>
                  </tbody>
                </table>`;
            _list_table_shell(field, title, "tk154", body);
            field.$wrapper.off("click", "[data-refresh='tk154']").on("click", "[data-refresh='tk154']", () => _render_tk154(frm));
        },
    });
}

function _render_pnl(frm, from_date, to_date) {
    const field = frm.fields_dict.pnl_html;
    _render_placeholder(field, __("Đang tải Lãi/Lỗ dự án..."));
    frappe.call({
        method: "vn_accounting.project_costing.api.get_project_pnl",
        args: {
            project_costing: frm.doc.name,
            from_date: from_date || "",
            to_date: to_date || "",
        },
        callback: (r) => {
            if (!r || !r.message) return;
            _render_pnl_html(frm, field, r.message);
        },
    });
}

function _render_pnl_html(frm, field, data) {
    const kpi = data.kpi || {};
    const period = data.period || {};
    const stages = data.stages || [];
    const accounts = data.accounts || {};
    const wip_code = (accounts.wip || "").split(" - ")[0] || "154";
    const cogs_code = (accounts.cogs || "").split(" - ")[0] || "632";

    const sign = (v) => v < 0 ? "−" : "";
    const money_signed = (v) => `${sign(v)}${_money(Math.abs(v))}`;
    const margin_class = (pct) => pct >= 15 ? "text-success" : (pct >= 0 ? "text-warning" : "text-danger");

    const kpi_card = (label, value, sub, color) => `
        <div class="pc-kpi-card" style="
            flex:1; min-width:160px; padding:14px 16px;
            background:var(--card-bg); border:1px solid var(--border-color);
            border-radius:6px; box-shadow:0 1px 2px rgba(0,0,0,0.03);">
            <div class="text-muted" style="font-size:11px; text-transform:uppercase; letter-spacing:0.04em;">
                ${frappe.utils.escape_html(label)}
            </div>
            <div class="${color || ""}" style="font-size:18px; font-weight:600; margin-top:4px;">${value}</div>
            ${sub ? `<div class="text-muted" style="font-size:11px; margin-top:2px;">${sub}</div>` : ""}
        </div>`;

    const kpi_row = `
        <div style="display:flex; gap:12px; flex-wrap:wrap; margin-bottom:16px;">
            ${kpi_card(__("Doanh thu"), _money(kpi.revenue), __("Tổng các TK Doanh thu (Cr − Dr)"))}
            ${kpi_card(__("Tổng chi phí"), _money(kpi.total_cost), __("Giá vốn + Chi phí khác"))}
            ${kpi_card(__("Lãi gộp"), money_signed(kpi.gross_profit), `${__("Tỷ suất LN gộp")} ${kpi.gross_margin_pct.toFixed(1)}% · ${__("DT − Giá vốn")}`, margin_class(kpi.gross_margin_pct))}
            ${kpi_card(__("Lãi ròng"), money_signed(kpi.net_profit), `${__("Tỷ suất LN ròng")} ${kpi.net_margin_pct.toFixed(1)}% · ${__("DT − Tổng CP")}`, margin_class(kpi.net_margin_pct))}
        </div>`;

    // Component breakdown table
    const breakdown_row = (label, amount, klass, indent) => `
        <tr ${klass ? `class="${klass}"` : ""}>
            <td style="padding-left:${(indent || 0) * 20 + 8}px;">${frappe.utils.escape_html(label)}</td>
            <td style="text-align:right;">${money_signed(amount)}</td>
        </tr>`;

    const breakdown_table = `
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:16px;">
          <div>
            <div style="font-weight:600; margin-bottom:8px;">${__("Chi tiết P&L")}</div>
            <table class="table table-sm table-bordered" style="font-size:13px;">
              <tbody>
                ${breakdown_row(__("Doanh thu (tổng các TK Doanh thu)"), kpi.revenue)}
                ${breakdown_row(__("Giá vốn (TK {0})", [cogs_code]), -kpi.cogs, "", 1)}
                ${breakdown_row(__("Lãi gộp"), kpi.gross_profit, "table-info")}
                ${breakdown_row(__("CP khác (6XX trừ TK {0})", [cogs_code]), -kpi.other_expenses, "", 1)}
                ${breakdown_row(__("Tổng chi phí"), -kpi.total_cost, "table-warning")}
                ${breakdown_row(__("Lãi ròng"), kpi.net_profit, "table-success")}
              </tbody>
            </table>
          </div>
          <div>
            <div style="font-weight:600; margin-bottom:8px;">${__("Chi phí dở dang & Cảnh báo")}</div>
            <table class="table table-sm table-bordered" style="font-size:13px; margin-bottom:8px;">
              <tbody>
                <tr><td>${__("Số dư TK {0} (chi phí đang treo, chưa kết chuyển giá vốn)", [wip_code])}</td>
                    <td style="text-align:right;"><strong>${_money(kpi.wip_balance)}</strong></td></tr>
                <tr><td style="padding-left:24px;">${__("Trong đó CP gián tiếp đã phân bổ (CAR)")}</td>
                    <td style="text-align:right;">${_money(kpi.allocated_cost)}</td></tr>
                <tr><td>${__("Tập hợp chi phí chưa gắn giai đoạn")}</td>
                    <td style="text-align:right;"><strong>${_money(kpi.common_pool)}</strong></td></tr>
              </tbody>
            </table>
            ${kpi.common_pool > 0 ? `
              <div class="alert alert-warning" style="font-size:12px; padding:8px 10px; margin-bottom:6px;">
                ⚠ ${__("{0} chưa gắn giai đoạn — chi phí này sẽ thiếu trong giá vốn khi xuất hóa đơn.", [_money(kpi.common_pool)])}
              </div>` : `
              <div class="alert alert-success" style="font-size:12px; padding:8px 10px; margin-bottom:6px;">
                ✓ ${__("Mọi chi phí đã gắn giai đoạn.")}
              </div>`}
            ${kpi.wip_balance > 0 && kpi.cogs === 0 ? `
              <div class="alert alert-info" style="font-size:12px; padding:8px 10px; margin-bottom:6px;">
                ℹ ${__("Có {0} treo trên TK 154 nhưng chưa ghi nhận giá vốn (TK 632). Xuất HĐ cho giai đoạn sẽ tự sinh bút toán Dr 632 / Cr 154.", [_money(kpi.wip_balance)])}
              </div>` : ""}
            ${kpi.net_profit < 0 ? `
              <div class="alert alert-danger" style="font-size:12px; padding:8px 10px;">
                ⚠ ${__("Lãi ròng âm — dự án đang lỗ.")}
              </div>` : ""}
          </div>
        </div>`;

    // Stage breakdown table
    const stage_total_rev = stages.reduce((s, x) => s + x.revenue, 0);
    const stage_total_cost = stages.reduce((s, x) => s + x.cost_pinned, 0);
    const stage_total_gross = stage_total_rev - stage_total_cost;
    const stage_table = stages.length ? `
        <div style="font-weight:600; margin-bottom:8px;">${__("Lãi/lỗ theo giai đoạn")}</div>
        <table class="table table-sm table-bordered" style="font-size:12px; margin-bottom:0;">
          <thead><tr>
            <th>${__("Giai đoạn")}</th>
            <th>${__("Trạng thái")}</th>
            <th>${__("Hóa đơn")}</th>
            <th style="text-align:right;">${__("Doanh thu")}</th>
            <th style="text-align:right;">${__("CP đã gắn")}</th>
            <th style="text-align:right;">${__("Lãi gộp")}</th>
            <th style="text-align:right;">${__("Tỷ suất LN")}</th>
          </tr></thead>
          <tbody>
            ${stages.map(s => `
              <tr>
                <td>${s.stage_order} — ${frappe.utils.escape_html(s.stage_name)}</td>
                <td>${_pivot_status_indicator(s.status)}</td>
                <td>${s.sales_invoice ? _doc_link("Sales Invoice", s.sales_invoice) : `<span class="text-muted">—</span>`}</td>
                <td style="text-align:right;">${_money(s.revenue)}</td>
                <td style="text-align:right;">${_money(s.cost_pinned)}</td>
                <td style="text-align:right;" class="${margin_class(s.gross_margin_pct)}"><strong>${money_signed(s.gross)}</strong></td>
                <td style="text-align:right;" class="${margin_class(s.gross_margin_pct)}">${s.gross_margin_pct.toFixed(1)}%</td>
              </tr>`).join("")}
            <tr style="background:var(--bg-light-gray); font-weight:600;">
              <td colspan="3" style="text-align:right;">${__("TỔNG")}</td>
              <td style="text-align:right;">${_money(stage_total_rev)}</td>
              <td style="text-align:right;">${_money(stage_total_cost)}</td>
              <td style="text-align:right;" class="${margin_class(stage_total_rev > 0 ? stage_total_gross / stage_total_rev * 100 : 0)}">${money_signed(stage_total_gross)}</td>
              <td style="text-align:right;">${stage_total_rev > 0 ? (stage_total_gross / stage_total_rev * 100).toFixed(1) : "0.0"}%</td>
            </tr>
          </tbody>
        </table>
        <div class="text-muted small" style="margin-top:6px;">
            ${__("Doanh thu/giai đoạn = tổng hóa đơn bán liên kết với giai đoạn. Chi phí/giai đoạn = tổng các khoản đã gắn vào giai đoạn (mua hàng / xuất kho / phiếu chi / phân bổ).")}
        </div>` : "";

    const header = `
        <div style="display:flex; justify-content:space-between; align-items:center; gap:12px; flex-wrap:wrap; padding:8px 0 12px; border-bottom:1px solid var(--border-color); margin-bottom:16px;">
            <div>
                <div style="font-weight:600;">${__("Lãi/Lỗ dự án")}</div>
                <div class="text-muted small">${__("Kỳ")}: <input type="date" class="vn-pc-pnl-from" value="${period.from_date}" style="font-size:12px; padding:2px 6px; border:1px solid var(--border-color); border-radius:3px;"/> → <input type="date" class="vn-pc-pnl-to" value="${period.to_date}" style="font-size:12px; padding:2px 6px; border:1px solid var(--border-color); border-radius:3px;"/></div>
            </div>
            <div style="display:flex; gap:6px;">
                <button class="btn btn-xs btn-default vn-pc-pnl-apply">${__("Áp dụng")}</button>
                <a href="/app/query-report/Project PnL Detailed?company=${encodeURIComponent(frm.doc.company)}&project=${encodeURIComponent(frm.doc.project)}" target="_blank" class="btn btn-xs btn-default">${__("Xem báo cáo full")}</a>
            </div>
        </div>`;

    field.$wrapper.html(`${header}${kpi_row}${breakdown_table}${stage_table}`);

    // Wire period filter
    field.$wrapper.off("click", ".vn-pc-pnl-apply").on("click", ".vn-pc-pnl-apply", () => {
        const fd = field.$wrapper.find(".vn-pc-pnl-from").val();
        const td = field.$wrapper.find(".vn-pc-pnl-to").val();
        _render_pnl(frm, fd, td);
    });
}

// ─────────────────────────────────────────────────────────────────────────────
// Sales Invoice creation dialogs (multi-SI per stage + project-level SI)
// ─────────────────────────────────────────────────────────────────────────────

function _open_stage_si_dialog(frm, stage_name, remaining, target_price) {
    const default_amount = remaining > 0 ? remaining : 0;
    const help = remaining > 0
        ? __("Còn lại chưa xuất: {0} (giá mục tiêu {1}).", [
            format_currency(remaining, "VND", 0),
            format_currency(target_price, "VND", 0),
          ])
        : __("Đã xuất đủ hoặc vượt giá mục tiêu. Bạn vẫn có thể tạo HĐ thêm với số tiền tùy ý.");

    const d = new frappe.ui.Dialog({
        title: __("Tạo hóa đơn cho giai đoạn"),
        fields: [
            {
                fieldname: "info",
                fieldtype: "HTML",
                options: `<div class="text-muted small" style="padding:4px 0">${help}</div>`,
            },
            {
                fieldname: "amount",
                fieldtype: "Currency",
                label: __("Số tiền hóa đơn"),
                default: default_amount,
                reqd: 1,
                description: __("Sẽ tạo SI dạng nháp, KTT review + submit thủ công."),
            },
            {
                fieldname: "description",
                fieldtype: "Small Text",
                label: __("Diễn giải (tùy chọn)"),
                description: __("Để trống → tự gán '[Tên dự án] — [Tên giai đoạn]'"),
            },
        ],
        primary_action_label: __("Tạo hóa đơn nháp"),
        primary_action: (values) => {
            frappe.call({
                method: "vn_accounting.project_costing.services.pivot_service.generate_stage_si",
                args: {
                    stage_name: stage_name,
                    amount: values.amount,
                    description: values.description || null,
                },
                callback: (r) => {
                    if (r.message && r.message.sales_invoice) {
                        frappe.show_alert({
                            message: __("Đã tạo {0}", [r.message.sales_invoice]),
                            indicator: "green",
                        });
                        d.hide();
                        window.open(r.message.url, "_blank");
                        _render_pivot(frm);
                        _load_summary(frm);
                    }
                },
            });
        },
    });
    d.show();
}

function _open_project_si_dialog(frm) {
    const d = new frappe.ui.Dialog({
        title: __("Tạo hóa đơn dự án (không theo giai đoạn)"),
        fields: [
            {
                fieldname: "info",
                fieldtype: "HTML",
                options: `<div class="text-muted small" style="padding:4px 0">
                    ${__("Dùng cho: tạm ứng/đặt cọc chung dự án, thanh toán tổng kết, HĐ bổ sung không thuộc giai đoạn nào.")}
                    <br><strong>⚠ ${__("Lưu ý")}:</strong> ${__("Hóa đơn này KHÔNG tự sinh bút toán giá vốn (Dr 632 / Cr 154) — KTT phải tự kết chuyển hoặc dùng chức năng đóng công trình.")}
                </div>`,
            },
            {
                fieldname: "amount",
                fieldtype: "Currency",
                label: __("Số tiền hóa đơn"),
                reqd: 1,
            },
            {
                fieldname: "description",
                fieldtype: "Small Text",
                label: __("Diễn giải (tùy chọn)"),
                description: __("Để trống → tự gán '[Tên dự án] — Hóa đơn dự án'"),
            },
        ],
        primary_action_label: __("Tạo hóa đơn nháp"),
        primary_action: (values) => {
            frappe.call({
                method: "vn_accounting.project_costing.services.pivot_service.generate_project_si",
                args: {
                    project_costing: frm.doc.name,
                    amount: values.amount,
                    description: values.description || null,
                },
                callback: (r) => {
                    if (r.message && r.message.sales_invoice) {
                        frappe.show_alert({
                            message: __("Đã tạo {0}", [r.message.sales_invoice]),
                            indicator: "green",
                        });
                        d.hide();
                        window.open(r.message.url, "_blank");
                        _render_pivot(frm);
                        _load_summary(frm);
                        // Reload SI tab if already loaded
                        if (frm.__pc_loaded_si_tab) _render_sales_invoices(frm);
                    }
                },
            });
        },
    });
    d.show();
}

