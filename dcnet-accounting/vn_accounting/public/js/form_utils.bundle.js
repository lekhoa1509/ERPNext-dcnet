// vn_accounting form utilities — shared helpers for DocType controllers.
//
// Currently exposes:
//   vn_accounting.render_linked_journal_entries(frm)
//     Surfaces every Journal Entry that references frm.doc via
//     reference_type+reference_name. Used by Bank Loan, Term Deposit,
//     and Cash Count forms to give users one-click access to related
//     JV/PE entries without digging through Accounting reports.
//
// History: started inline in bank_loan.js (FB-525/527), copied into
// term_deposit.js, and extracted here when cash_count.js became the
// 3rd consumer (FB-513). See ~/.claude/rules/programming.md
// "rule of three" — third consumer triggers extraction.

(function () {
	window.vn_accounting = window.vn_accounting || {};

	const STATUS_MAP = { 0: "Nháp", 1: "Đã duyệt", 2: "Đã hủy" };
	const VOUCHER_TYPE_LABELS = {
		"Journal Entry": "Bút toán",
		"Bank Entry": "Bút toán ngân hàng",
		"Cash Entry": "Bút toán tiền mặt",
		"Contra Entry": "Bút toán đối ứng",
		"Depreciation Entry": "Bút toán khấu hao",
		"Opening Entry": "Bút toán khai mạc",
		"Write Off Entry": "Bút toán xóa nợ",
	};

	// render_linked_journal_entries(frm, options?)
	//   options.je_names: optional explicit list of JE names. When provided, we
	//     skip the JE Account reference_type lookup and use this list directly.
	//     Useful for DocTypes that store JE references as direct Link fields
	//     on themselves (e.g. Cash Count → pending_je / resolution_je) instead
	//     of via Journal Entry Account.reference_type/_name.
	//   options.title: optional panel heading (defaults to "Bút toán liên quan").
	window.vn_accounting.render_linked_journal_entries = async function (frm, options) {
		options = options || {};
		const mount_class = "vn-linked-jes-box";
		$(frm.wrapper).find("." + mount_class).remove();
		if (frm.is_new()) return;

		// Query parent Journal Entry directly with a child-table filter.
		// Querying `Journal Entry Account` (child) hits a 403 because Accounts roles
		// only carry DocPerm on the parent; Frappe parent-child filter syntax JOINs
		// the child table while running the permission check on the parent.
		let je_resp;
		if (options.je_names) {
			const names = [...new Set(options.je_names.filter(Boolean))];
			if (!names.length) return;
			je_resp = await frappe.call({
				method: "frappe.client.get_list",
				args: {
					doctype: "Journal Entry",
					filters: { name: ["in", names] },
					fields: ["name", "posting_date", "voucher_type", "total_debit", "docstatus", "user_remark"],
					limit_page_length: 200,
					order_by: "posting_date desc",
				},
			});
		} else {
			je_resp = await frappe.call({
				method: "frappe.client.get_list",
				args: {
					doctype: "Journal Entry",
					filters: [
						["Journal Entry Account", "reference_type", "=", frm.doc.doctype],
						["Journal Entry Account", "reference_name", "=", frm.doc.name],
					],
					fields: ["name", "posting_date", "voucher_type", "total_debit", "docstatus", "user_remark"],
					limit_page_length: 200,
					order_by: "posting_date desc",
				},
			});
		}
		const jes = je_resp.message || [];
		if (!jes.length) return;

		const rows = jes
			.map(
				(je) => `
				<tr>
					<td>${frappe.format(je.posting_date, { fieldtype: "Date" })}</td>
					<td><a href="/app/journal-entry/${encodeURIComponent(je.name)}">${frappe.utils.escape_html(je.name)}</a></td>
					<td>${frappe.utils.escape_html(__(VOUCHER_TYPE_LABELS[je.voucher_type] || je.voucher_type || ""))}</td>
					<td class="text-right">${format_currency(je.total_debit || 0)}</td>
					<td>${__(STATUS_MAP[je.docstatus] || "")}</td>
					<td>${frappe.utils.escape_html(je.user_remark || "")}</td>
				</tr>`
			)
			.join("");
		const title = options.title || __("Bút toán liên quan");
		const html = `
			<div class="${mount_class}" style="margin: 20px 15px 0;">
				<h6 style="margin-bottom: 8px;">${frappe.utils.escape_html(title)}</h6>
				<div class="table-responsive">
					<table class="table table-bordered table-sm" style="margin-bottom: 0;">
						<thead><tr>
							<th>${__("Ngày")}</th>
							<th>${__("Số chứng từ")}</th>
							<th>${__("Loại")}</th>
							<th class="text-right">${__("Số tiền")}</th>
							<th>${__("Trạng thái")}</th>
							<th>${__("Diễn giải")}</th>
						</tr></thead>
						<tbody>${rows}</tbody>
					</table>
				</div>
			</div>`;
		$(frm.wrapper).find(".layout-main-section").first().append(html);
	};

	const EXCEL_PRINT_DOCTYPES = [
		"Asset", "Asset Movement", "Asset Repair", "BOM", "Delivery Note",
		"Delivery Trip", "Employee Advance", "Expense Claim", "Job Card",
		"Journal Entry", "Material Request", "Payment Entry", "Purchase Invoice",
		"Purchase Order", "Purchase Receipt", "Quotation", "Request for Quotation",
		"Sales Invoice", "Sales Order", "Stock Entry", "Stock Reconciliation",
		"Subcontracting Order", "Subcontracting Receipt", "Supplier Quotation", "Work Order",
	];

	window.vn_accounting.open_excel_print_dialog = async function (frm) {
		if (frm.is_new()) {
			frappe.msgprint(__("Hãy lưu chứng từ trước khi in Excel."));
			return;
		}
		const dialog = new frappe.ui.Dialog({
			title: __("In Excel") + " — " + frm.doc.name,
			size: "large",
		});
		window.vn_accounting.ensure_excel_print_dialog_styles();
		const $body = dialog.$wrapper.find(".modal-body");
		$body.html(`
			<div class="xpd-header">
				<div>
					<div class="xpd-heading">${__("Mẫu in Excel")}</div>
					<div class="xpd-subheading">${__(frm.doctype)} · ${frappe.utils.escape_html(frm.doc.name)}</div>
				</div>
				<button class="btn btn-xs btn-primary xpd-new" type="button">
					${frappe.utils.icon("plus", "xs")} ${__("Tạo mẫu mới")}
				</button>
			</div>
			<div class="xpd-list" aria-live="polite">
				<div class="xpd-empty">${frappe.utils.icon("loader", "sm")} ${__("Đang tải mẫu...")}</div>
			</div>`);
		dialog.show();

		dialog.$wrapper.find(".xpd-new").on("click", () => {
			const url = "/app/excel-print-template-builder?new=1&document_type="
				+ encodeURIComponent(frm.doctype) + "&document_name=" + encodeURIComponent(frm.doc.name);
			window.open(url, "_blank", "noopener");
			frappe.show_alert({ message: __("Đã mở trình soạn mẫu trong tab mới"), indicator: "blue" });
		});

		async function loadTemplates() {
			const response = await frappe.call({
				method: "vn_accounting.excel_printing.api.get_templates_for_document",
				type: "GET",
				args: { document_type: frm.doctype },
			});
			const payload = response.message || {};
			const templates = payload.templates || [];
			const canManage = Boolean(payload.can_manage);
			const $list = dialog.$wrapper.find(".xpd-list").empty();
			dialog.$wrapper.find(".xpd-new").toggle(canManage);

			if (!templates.length) {
				$list.html(`<div class="xpd-empty">
					${frappe.utils.icon("file-spreadsheet", "md")}
					<div class="xpd-empty-title">${__("Chưa có mẫu in Excel")}</div>
					<div>${canManage ? __("Nhấn “Tạo mẫu mới” để load và cấu hình file Excel.") : __("Liên hệ Accounts Manager để tạo mẫu in.")}</div>
				</div>`);
				return;
			}

			templates.forEach((template) => {
				const row = $(`<div class="xpd-row">
					<div class="xpd-info">
						<div class="xpd-name">
							${frappe.utils.escape_html(template.template_name || template.name)}
							${template.is_default ? `<span class="xpd-badge">${__("Mặc định")}</span>` : ""}
						</div>
						<div class="xpd-meta">${__(frm.doctype)} · ${template.source_file ? "XLSX" : __("Mẫu Excel")}</div>
					</div>
					<div class="xpd-actions">
						<button class="btn btn-xs btn-default xpd-edit" type="button" title="${__("Sửa mẫu")}" aria-label="${__("Sửa mẫu")}">${frappe.utils.icon("edit", "xs")}</button>
						<button class="btn btn-xs btn-danger xpd-delete" type="button" title="${__("Xóa mẫu")}" aria-label="${__("Xóa mẫu")}">${frappe.utils.icon("delete", "xs")}</button>
						<button class="btn btn-xs btn-default xpd-preview" type="button">${frappe.utils.icon("view", "xs")} ${__("Xem trước")}</button>
						<button class="btn btn-xs btn-default xpd-download" type="button">${frappe.utils.icon("download", "xs")} ${__("Tải")}</button>
						<button class="btn btn-xs btn-primary xpd-print" type="button">${frappe.utils.icon("printer", "xs")} ${__("In")}</button>
					</div>
				</div>`);
				row.find(".xpd-edit, .xpd-delete").toggle(canManage);
				row.find(".xpd-edit").on("click", () => {
					const url = "/app/excel-print-template-builder?template=" + encodeURIComponent(template.name)
						+ "&document_name=" + encodeURIComponent(frm.doc.name);
					window.open(url, "_blank", "noopener");
				});
				row.find(".xpd-delete").on("click", () => {
					frappe.confirm(
						__("Xóa mẫu [{0}]? Thao tác này không thể hoàn tác.", [template.template_name || template.name]),
						async () => {
							await frappe.call({
								method: "vn_accounting.excel_printing.api.delete_excel_template",
								args: { template_name: template.name },
								freeze: true,
								freeze_message: __("Đang xóa mẫu..."),
							});
							frappe.show_alert({ message: __("Đã xóa mẫu"), indicator: "green" });
							await loadTemplates();
						}
					);
				});
				row.find(".xpd-preview").on("click", () => previewTemplate(template.name, false));
				row.find(".xpd-download").on("click", () => exportTemplate(template.name));
				row.find(".xpd-print").on("click", () => previewTemplate(template.name, true));
				$list.append(row);
			});
		}

		async function previewTemplate(templateName, autoPrint) {
			const result = await frappe.call({
				method: "vn_accounting.excel_printing.api.preview_excel_template_grid",
				args: { template_name: templateName, document_type: frm.doctype, document_name: frm.doc.name },
				freeze: true,
				freeze_message: __("Đang dựng bản xem trước..."),
			});
			window.vn_accounting.show_excel_print_preview(result.message.workbook_state, autoPrint);
		}

		async function exportTemplate(templateName) {
			const result = await frappe.call({
				method: "vn_accounting.excel_printing.api.export_excel_document",
				args: { template_name: templateName, document_type: frm.doctype, document_name: frm.doc.name },
				freeze: true,
				freeze_message: __("Đang tạo file Excel..."),
			});
			if (result.message?.file_url) window.open(result.message.file_url, "_blank", "noopener");
		}

		await loadTemplates();
	};

	window.vn_accounting.ensure_excel_print_dialog_styles = function () {
		if (document.getElementById("xpd-dialog-styles")) return;
		const style = document.createElement("style");
		style.id = "xpd-dialog-styles";
		style.textContent = `
			.xpd-header{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:10px 12px;border-bottom:1px solid var(--border-color)}
			.xpd-heading{font-size:13px;font-weight:600;color:var(--text-color)}
			.xpd-subheading,.xpd-meta{font-size:11px;color:var(--text-muted)}
			.xpd-list{max-height:420px;overflow-y:auto}
			.xpd-row{display:flex;align-items:center;gap:12px;padding:9px 12px;border-bottom:1px solid var(--border-color);transition:background-color .16s ease}
			.xpd-row:hover{background:var(--bg-color)}
			.xpd-info{flex:1;min-width:160px}
			.xpd-name{font-size:13px;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
			.xpd-badge{display:inline-block;margin-left:6px;padding:1px 6px;border-radius:10px;background:#dcfce7;color:#166534;font-size:10px;font-weight:600}
			.xpd-actions{display:flex;align-items:center;gap:6px;flex-wrap:wrap;justify-content:flex-end}
			.xpd-actions .btn{min-height:30px;display:inline-flex;align-items:center;gap:4px}
			.xpd-empty{display:flex;min-height:170px;align-items:center;justify-content:center;flex-direction:column;gap:6px;padding:32px;color:var(--text-muted);text-align:center}
			.xpd-empty-title{font-size:13px;font-weight:600;color:var(--text-color)}
			.xpd-row button:focus-visible,.xpd-new:focus-visible{outline:3px solid rgba(3,105,161,.25);outline-offset:1px}
			@media(max-width:768px){.xpd-row{align-items:flex-start;flex-direction:column}.xpd-actions{justify-content:flex-start}.xpd-header{align-items:flex-start}}
			@media(prefers-reduced-motion:reduce){.xpd-row{transition:none}}
			@media print{
				body.xpd-printing *{visibility:hidden!important}
				body.xpd-printing .xpd-preview-modal,body.xpd-printing .xpd-preview-modal *{visibility:visible!important}
				body.xpd-printing .xpd-preview-modal{position:absolute!important;inset:0!important;display:block!important;background:#fff!important}
				body.xpd-printing .xpd-preview-modal .modal-dialog{width:100%!important;max-width:none!important;margin:0!important}
				body.xpd-printing .xpd-preview-modal .modal-content{border:0!important;box-shadow:none!important}
				body.xpd-printing .xpd-preview-modal .modal-header,body.xpd-printing .xpd-preview-modal .modal-footer{display:none!important}
			}
		`;
		document.head.appendChild(style);
	};

	window.vn_accounting.show_excel_print_preview = function (state, autoPrint = false) {
		const helper = window.vn_accounting.excel_preview_helper;
		helper(state, autoPrint);
	};

	window.vn_accounting.excel_preview_helper = function (state, autoPrint = false) {
		const columnName = (index) => {
			let value = "";
			while (index) {
				index--;
				value = String.fromCharCode(65 + (index % 26)) + value;
				index = Math.floor(index / 26);
			}
			return value;
		};
		const columnIndex = (name) => [...name].reduce((total, character) => total * 26 + character.charCodeAt(0) - 64, 0);
		const color = (value, fallback) => {
			const rgb = value?.rgb || "";
			if (value?.type === "rgb" && /^[0-9A-F]{8}$/i.test(rgb)) return `#${rgb.slice(2)}`;
			if (value?.type === "rgb" && /^[0-9A-F]{6}$/i.test(rgb)) return `#${rgb}`;
			return fallback;
		};
		const cellStyle = (style) => {
			const font = style?.font || {};
			const alignment = style?.alignment || {};
			const fill = style?.fill || {};
			const border = style?.border || {};
			const output = [
				`font-family:'${String(font.name || "Arial").replace(/[^a-zA-Z0-9 _-]/g, "")}'`,
				`font-size:${Number(font.size || 10)}pt`,
				`font-weight:${font.bold ? 700 : 400}`,
				`font-style:${font.italic ? "italic" : "normal"}`,
				`text-decoration:${font.underline ? "underline" : "none"}`,
				`color:${color(font.color, "#0f172a")}`,
				`background-color:${color(fill.fg_color, "#ffffff")}`,
				`text-align:${alignment.horizontal || "left"}`,
				`vertical-align:${alignment.vertical === "top" ? "top" : alignment.vertical === "bottom" ? "bottom" : "middle"}`,
				`white-space:${alignment.wrap_text ? "pre-wrap" : "nowrap"}`,
			];
			["top", "right", "bottom", "left"].forEach((side) => {
				if (!border[side]?.style) return;
				const borderStyle = ["dashed", "dotted", "double"].includes(border[side].style) ? border[side].style : "solid";
				output.push(`border-${side}:1px ${borderStyle} ${color(border[side].color, "#334155")}`);
			});
			return output.join(";");
		};
		const rawValue = (value) => value && typeof value === "object" && value.__type ? value.value || "" : value ?? "";
		const displayValue = (cell) => {
			const value = rawValue(cell.display_value ?? cell.value ?? "");
			const format = String(cell.style?.number_format || "");
			if (typeof value === "number" && /\[\$[đ₫]-vi-VN\]|[đ₫]/i.test(format)) {
				return `${new Intl.NumberFormat("vi-VN", { maximumFractionDigits: 2 }).format(value)}${format.includes("₫") ? " ₫" : "đ"}`;
			}
			if (typeof value === "number" && format.includes("%")) {
				return `${new Intl.NumberFormat("vi-VN", { maximumFractionDigits: 2 }).format(value * 100)}%`;
			}
			return value;
		};
		const mergeMap = (ranges) => {
			const starts = {};
			const covered = new Set();
			(ranges || []).forEach((range) => {
				const match = String(range).replace(/\$/g, "").match(/^([A-Z]+)(\d+):([A-Z]+)(\d+)$/);
				if (!match) return;
				const [, startColumn, startRow, endColumn, endRow] = match;
				starts[`${startColumn}${startRow}`] = {
					rows: Number(endRow) - Number(startRow) + 1,
					columns: columnIndex(endColumn) - columnIndex(startColumn) + 1,
				};
				for (let row = Number(startRow); row <= Number(endRow); row++) {
					for (let column = columnIndex(startColumn); column <= columnIndex(endColumn); column++) {
						const coordinate = `${columnName(column)}${row}`;
						if (coordinate !== `${startColumn}${startRow}`) covered.add(coordinate);
					}
				}
			});
			return { starts, covered };
		};

		const sheets = (state?.sheets || []).map((sheet) => {
			const merges = mergeMap(sheet.merged_cells);
			const bounds = sheet.preview_bounds || { min_column: 1, min_row: 1, max_column: sheet.max_column, max_row: sheet.max_row };
			let html = `<section style="width:max-content;min-width:760px;margin:0 auto 22px;padding:28px;background:#fff;box-shadow:0 2px 14px rgba(15,23,42,.16)"><h5 style="margin:0 0 12px;color:#475569">${frappe.utils.escape_html(sheet.title)}</h5><table style="border-collapse:collapse;table-layout:fixed"><colgroup>`;
			for (let column = bounds.min_column; column <= bounds.max_column; column++) {
				const width = Math.max(55, Math.min(360, Math.round(Number(sheet.column_widths?.[columnName(column)] || 12) * 7)));
				html += `<col style="width:${width}px">`;
			}
			html += "</colgroup>";
			for (let row = bounds.min_row; row <= bounds.max_row; row++) {
				const height = Math.max(20, Math.round(Number(sheet.row_heights?.[String(row)] || 18) * 1.34));
				html += `<tr style="height:${height}px">`;
				for (let column = bounds.min_column; column <= bounds.max_column; column++) {
					const coordinate = `${columnName(column)}${row}`;
					if (merges.covered.has(coordinate)) continue;
					const cell = sheet.cells?.[coordinate] || {};
					const merge = merges.starts[coordinate];
					const value = displayValue(cell);
					html += `<td style="overflow:hidden;padding:3px 5px;${cellStyle(cell.style)}" ${merge ? `rowspan="${merge.rows}" colspan="${merge.columns}"` : ""}>${frappe.utils.escape_html(String(value))}</td>`;
				}
				html += "</tr>";
			}
			return html + "</table></section>";
		}).join("");

		const dialog = new frappe.ui.Dialog({ title: __("Xem trước mẫu in Excel"), size: "extra-large" });
		dialog.$wrapper.addClass("xpd-preview-modal");
		dialog.$body.html(`<div style="max-height:75vh;overflow:auto;padding:24px;background:#e5e7eb">${sheets}</div>`);
		const printPreview = () => {
			document.body.classList.add("xpd-printing");
			const cleanup = () => document.body.classList.remove("xpd-printing");
			window.addEventListener("afterprint", cleanup, { once: true });
			window.print();
			setTimeout(cleanup, 1500);
		};
		dialog.set_primary_action(__("In"), printPreview);
		dialog.show();
		const modal = dialog.$wrapper.find(".modal-dialog").css({ "max-width": "94vw", width: "94vw" });
		dialog.$wrapper.find(".modal-content").css({ resize: "both", overflow: "auto", "min-width": "720px", "min-height": "420px" });
		const expand = $(`<button type="button" class="btn btn-xs btn-default" style="margin-left:auto" aria-label="${__("Phóng to/thu nhỏ")}">${frappe.utils.icon("expand", "sm")}</button>`);
		let expanded = false;
		expand.on("click", () => {
			expanded = !expanded;
			modal.css(expanded ? { width: "98vw", "max-width": "98vw", margin: "1vh auto" } : { width: "94vw", "max-width": "94vw", margin: "1.75rem auto" });
		});
		dialog.$wrapper.find(".modal-title").after(expand);
		if (autoPrint) setTimeout(printPreview, 250);
	};

	EXCEL_PRINT_DOCTYPES.forEach((doctype) => {
		frappe.ui.form.on(doctype, {
			refresh(frm) {
				if (frm.is_new()) return;
				frm.add_custom_button(__("In Excel"), () => window.vn_accounting.open_excel_print_dialog(frm), __("In"));
			},
		});
	});
})();
