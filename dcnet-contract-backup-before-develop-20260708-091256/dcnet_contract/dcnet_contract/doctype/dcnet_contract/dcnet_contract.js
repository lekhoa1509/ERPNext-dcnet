frappe.ui.form.on("DCNet Contract", {
	refresh(frm) {
		frm.trigger("service_type");

		// "In hợp đồng" — always visible after save, opens template selection dialog
		if (!frm.is_new()) {
			const $btn = frm.add_custom_button(__("In hợp đồng"), function () {
				_show_print_dialog(frm);
			});
			$btn.removeClass("btn-default").addClass("btn-primary");
		}

		if (frm.doc.docstatus === 0 && !frm.is_new()) {
			frm.add_custom_button(__("Tạo từ mẫu"), function () {
				const d = new frappe.ui.Dialog({
					title: __("Chọn mẫu hợp đồng"),
					fields: [
						{
							fieldname: "template",
							fieldtype: "Link",
							label: __("Mẫu hợp đồng"),
							options: "DCNet Contract Template",
							reqd: 1,
						},
					],
					primary_action_label: __("Áp dụng"),
					primary_action(values) {
						frappe.call({
							method: "dcnet_contract.dcnet_contract.doctype.dcnet_contract_template.dcnet_contract_template.get_template",
							args: { template_name: values.template },
							callback(r) {
								if (r.message) {
									const tpl = r.message;
									if (tpl.service_type) frm.set_value("service_type", tpl.service_type);
									if (tpl.contract_type) frm.set_value("contract_type", tpl.contract_type);
									if (tpl.payment_mode) frm.set_value("payment_mode", tpl.payment_mode);
									if (tpl.package_term_months) frm.set_value("package_term_months", tpl.package_term_months);
									// Fill items
									frm.clear_table("items");
									(tpl.items || []).forEach(function (item) {
										let row = frm.add_child("items");
										row.item_label = item.item_label;
										row.description = item.description;
										row.uom = item.uom;
										row.qty = item.qty;
										row.unit_price = item.unit_price;
										row.amount_per_period = (item.qty || 0) * (item.unit_price || 0);
									});
									frm.refresh_fields();
									frm.dirty();
								}
								d.hide();
							},
						});
					},
				});
				d.show();
			});
		}

		// "In Hop dong" standalone button — opens print view with contract + appendix
		if (frm.doc.docstatus >= 1 || (frm.doc.docstatus === 0 && frm.doc.status !== "Draft")) {
			const printLabel = __("In Hop dong");
			frm.add_custom_button(printLabel, function () {
				const url =
					"/printview?doctype=DCNet+Contract" +
					"&name=" + encodeURIComponent(frm.doc.name) +
					"&format=Hop+Dong+Chuan";
				window.open(url, "_blank");
			});
			// Style as primary standalone (not in dropdown)
			if (frm.custom_buttons[printLabel]) {
				frm.custom_buttons[printLabel].removeClass("btn-default").addClass("btn-primary-dark");
			}
		}

		// "Xuat Hop dong" button — export DOCX/PDF
		if (frm.doc.docstatus >= 1 || (frm.doc.docstatus === 0 && frm.doc.status !== "Draft")) {
			frm.add_custom_button(__("Xuat Hop dong"), function () {
				// Auto-find matching templates by service_type
				frappe.call({
					method: "frappe.client.get_list",
					args: {
						doctype: "DCNet Contract Template",
						filters: {
							template_file: ["is", "set"],
							service_type: frm.doc.service_type || "",
						},
						fields: ["name", "template_category", "service_type"],
						limit_page_length: 0,
					},
					callback(r) {
						const matches = (r.message || []);
						if (matches.length === 1) {
							// Exactly one match — export directly
							_export_contract(frm, matches[0].name, "docx");
						} else {
							// Multiple or no matches — show dialog with pre-filtered list
							_show_export_dialog(frm, matches.length ? matches[0].name : null);
						}
					},
				});
			}, __("Actions"));
		}

		if (frm.doc.docstatus === 1 && frm.doc.status === "Active") {
			frm.add_custom_button(__("Tạo PAKD"), function () {
				frappe.new_doc("Phuong An Kinh Doanh", {
					contract_ref: frm.doc.name,
				});
			}, __("Tạo"));

			frm.add_custom_button(__("Tạm ngưng"), function () {
				frappe.prompt(
					{ fieldname: "reason", fieldtype: "Small Text", label: "Lý do tạm ngưng" },
					function (values) {
						frappe.call({
							method: "dcnet_contract.dcnet_contract.doctype.dcnet_contract.dcnet_contract.suspend_contract",
							args: { name: frm.doc.name, reason: values.reason },
							callback: function () { frm.reload_doc(); },
						});
					},
					__("Tạm ngưng hợp đồng"),
					__("Xác nhận")
				);
			}, __("Actions"));
		}

		if (frm.doc.docstatus === 1 && frm.doc.status === "Suspended") {
			frm.add_custom_button(__("Kích hoạt lại"), function () {
				frappe.call({
					method: "dcnet_contract.dcnet_contract.doctype.dcnet_contract.dcnet_contract.resume_contract",
					args: { name: frm.doc.name },
					callback: function () { frm.reload_doc(); },
				});
			}, __("Actions"));
		}
	},

	customer(frm) {
		if (!frm.doc.customer) return;
		frappe.call({
			method: "dcnet_contract.dcnet_contract.doctype.dcnet_contract.dcnet_contract.get_customer_info",
			args: { customer: frm.doc.customer },
			callback(r) {
				if (r.message) {
					for (let [field, value] of Object.entries(r.message)) {
						if (!frm.doc[field] && value) {
							frm.set_value(field, value);
						}
					}
				}
			}
		});
	},

	company(frm) {
		if (!frm.doc.company) return;
		frappe.call({
			method: "frappe.client.get_value",
			args: {
				doctype: "DCNet Contract Settings",
				filters: "DCNet Contract Settings",
				fieldname: ["default_representative", "default_representative_title"]
			},
			callback(r) {
				if (r.message) {
					if (!frm.doc.company_representative && r.message.default_representative) {
						frm.set_value("company_representative", r.message.default_representative);
					}
					if (!frm.doc.company_representative_title && r.message.default_representative_title) {
						frm.set_value("company_representative_title", r.message.default_representative_title);
					}
				}
			}
		});
	},

	service_type(frm) {
		const recurring = ["P2P", "MPLS", "ILL", "FTTH DN", "FTTH HGD", "IT Managed"];
		const oneoff = ["VTTB", "Thi công"];
		if (recurring.includes(frm.doc.service_type)) {
			frm.set_value("contract_type", "Recurring");
		} else if (oneoff.includes(frm.doc.service_type)) {
			frm.set_value("contract_type", "One-off");
			frm.set_value("payment_mode", "OneOff");
		}
	},
});

frappe.ui.form.on("DCNet Contract Item", {
	qty(frm, cdt, cdn) {
		_calc_item_amount(frm, cdt, cdn);
	},
	unit_price(frm, cdt, cdn) {
		_calc_item_amount(frm, cdt, cdn);
	},
});

function _calc_item_amount(frm, cdt, cdn) {
	let row = locals[cdt][cdn];
	frappe.model.set_value(cdt, cdn, "amount_per_period", (row.qty || 0) * (row.unit_price || 0));
}

function _export_contract(frm, template_name, output_format) {
	frappe.call({
		method: "dcnet_contract.dcnet_contract.doctype.dcnet_contract.dcnet_contract.generate_contract_document",
		args: {
			contract_name: frm.doc.name,
			template_name: template_name,
			output_format: output_format,
		},
		freeze: true,
		freeze_message: __("Dang tao van ban..."),
		callback(r) {
			if (r.message) {
				window.open(r.message, "_blank");
				frm.reload_doc();
			}
		},
	});
}

function _show_export_dialog(frm, default_template) {
	const d = new frappe.ui.Dialog({
		title: __("Xuat van ban hop dong"),
		fields: [
			{
				fieldname: "template",
				fieldtype: "Link",
				label: __("Mau van ban"),
				options: "DCNet Contract Template",
				reqd: 1,
				default: default_template,
				get_query() {
					return {
						filters: { template_file: ["is", "set"] },
					};
				},
			},
			{
				fieldname: "output_format",
				fieldtype: "Select",
				label: __("Dinh dang"),
				options: "docx\npdf",
				default: "docx",
			},
		],
		primary_action_label: __("Tao"),
		primary_action(values) {
			d.hide();
			_export_contract(frm, values.template, values.output_format);
		},
	});
	d.show();
}

// ---------------------------------------------------------------------------
// Print dialog — template selection with CRUD
// ---------------------------------------------------------------------------
function _show_print_dialog(frm) {
	const d = new frappe.ui.Dialog({
		title: __("In hợp đồng") + " — " + frm.doc.name,
		size: "large",
	});

	// Inject custom styles once
	if (!document.getElementById("ctb-dialog-styles")) {
		const style = document.createElement("style");
		style.id = "ctb-dialog-styles";
		style.textContent = `
			.ctb-tpl-row {
				display:flex; align-items:center; padding:8px 12px; gap:8px;
				border-bottom:1px solid var(--border-color); }
			.ctb-tpl-row:hover { background:var(--bg-color); }
			.ctb-tpl-info { flex:1; min-width:0; }
			.ctb-tpl-name { font-weight:600; font-size:13px; white-space:nowrap;
			                overflow:hidden; text-overflow:ellipsis; }
			.ctb-tpl-meta { font-size:11px; color:var(--text-muted); }
			.ctb-tpl-status { font-size:10px; padding:1px 6px; border-radius:10px;
			                  font-weight:600; }
			.ctb-tpl-status.Draft   { background:#FEF9C3; color:#92400E; }
			.ctb-tpl-status.Approved { background:#DCFCE7; color:#166534; }
			.ctb-tpl-status.Pending { background:#DBEAFE; color:#1e40af; }
			.ctb-tpl-status.Archived { background:#f3f4f6; color:#6b7280; }
			.ctb-no-tpl { padding:32px; text-align:center; color:var(--text-muted); }
		`;
		document.head.appendChild(style);
	}

	const $body = d.$wrapper.find(".modal-body");
	$body.html(`
		<div style="padding:8px 12px 10px; display:flex; justify-content:space-between; align-items:center;
		            border-bottom:1px solid var(--border-color);">
			<span style="font-weight:600; font-size:13px;">${__("Mẫu hợp đồng")}</span>
			<button class="btn btn-xs btn-primary" id="ctb-new-tpl">
				<i class="fa fa-plus"></i>&nbsp;${__("Tạo mẫu mới")}
			</button>
		</div>
		<div id="ctb-tpl-list" style="max-height:360px; overflow-y:auto;">
			<div class="ctb-no-tpl"><i class="fa fa-spinner fa-spin"></i></div>
		</div>
	`);
	d.show();

	// Open builder in new tab (pass contract_name for preview)
	d.$wrapper.find("#ctb-new-tpl").on("click", function () {
		const url = "/app/contract-template-builder?new=1&contract=" + encodeURIComponent(frm.doc.name);
		window.open(url, "_blank");
		frappe.show_alert({ message: __("Đã mở trình soạn mẫu trong tab mới"), indicator: "blue" });
	});

	function _reload_list() {
		frappe.call({
			method: "dcnet_contract.dcnet_contract.api.get_print_templates",
			callback(r) {
				const list = r.message || [];
				const $list = d.$wrapper.find("#ctb-tpl-list").empty();

				if (!list.length) {
					$list.html(`<div class="ctb-no-tpl">Chưa có mẫu nào. Nhấn "+ Tạo mẫu mới" để bắt đầu.</div>`);
					return;
				}

				list.forEach(function (tpl) {
					const hasFile = !!(tpl.template_file || tpl.template_html);
					const statusClass = (tpl.status || "Draft").replace(" ", "");
					const row = $(`
						<div class="ctb-tpl-row">
							<div class="ctb-tpl-info">
								<div class="ctb-tpl-name">
									${frappe.utils.escape_html(tpl.template_name || tpl.name)}
									<span class="ctb-tpl-status ${statusClass}">${__(tpl.status || "Draft")}</span>
								</div>
								<div class="ctb-tpl-meta">
									${tpl.template_category ? frappe.utils.escape_html(tpl.template_category) : ""}
									${tpl.service_type ? "· " + frappe.utils.escape_html(tpl.service_type) : ""}
									${tpl.template_file ? '· <i class="fa fa-file-word-o"></i> DOCX' : ""}
								</div>
							</div>
							<button class="btn btn-xs btn-default ctb-btn-edit" title="${__("Sửa mẫu")}">
								<i class="fa fa-pencil"></i>
							</button>
							<button class="btn btn-xs btn-danger ctb-btn-del" title="${__("Xóa mẫu")}">
								<i class="fa fa-trash"></i>
							</button>
							<button class="btn btn-xs btn-default ctb-btn-preview" title="${__("Xem trước")}"
							        ${hasFile ? "" : "disabled"}>
								<i class="fa fa-eye"></i>&nbsp;${__("Xem trước")}
							</button>
							<button class="btn btn-xs btn-default ctb-btn-download"
							    ${hasFile ? "" : "disabled"} title="${__("Tải xuống Word")}">
								<i class="fa fa-download"></i>&nbsp;${__("Tải")}
							</button>
							<button class="btn btn-xs btn-primary ctb-btn-print"
							    ${hasFile ? "" : "disabled"} title="${__("Xuất & In")}">
								<i class="fa fa-print"></i>&nbsp;${__("In")}
							</button>
						</div>
					`);

					row.find(".ctb-btn-edit").on("click", function () {
						const editUrl = "/app/contract-template-builder?template=" + encodeURIComponent(tpl.name)
							+ "&contract=" + encodeURIComponent(frm.doc.name);
						window.open(editUrl, "_blank");
						frappe.show_alert({ message: __("Đã mở mẫu trong tab mới"), indicator: "blue" });
					});

					row.find(".ctb-btn-del").on("click", function () {
						frappe.confirm(
							__("Xóa mẫu [{0}]? Thao tác này không thể hoàn tác.", [tpl.template_name || tpl.name]),
							function () {
								frappe.call({
									method: "dcnet_contract.dcnet_contract.api.delete_print_template",
									args: { template_name: tpl.name },
									callback() {
										frappe.show_alert({ message: __("Đã xóa mẫu"), indicator: "green" });
										_reload_list();
									},
								});
							}
						);
					});

					row.find(".ctb-btn-preview").on("click", function () {
						_show_contract_preview(frm, tpl.name);
					});

					row.find(".ctb-btn-download").on("click", function () {
						frappe.call({
							method: "dcnet_contract.dcnet_contract.doctype.dcnet_contract.dcnet_contract.generate_contract_document",
							args: {
								contract_name: frm.doc.name,
								template_name: tpl.name,
								output_format: "docx",
							},
							freeze: true,
							freeze_message: __("Đang tạo file Word..."),
							callback(r) {
								if (r.message) {
									const a = document.createElement("a");
									a.href = r.message;
									a.download = frm.doc.name + ".docx";
									document.body.appendChild(a);
									a.click();
									document.body.removeChild(a);
									frm.reload_doc();
								}
							},
						});
					});

					row.find(".ctb-btn-print").on("click", function () {
						d.hide();
						_export_contract(frm, tpl.name, "docx");
					});

					$list.append(row);
				});
			},
		});
	}

	_reload_list();
}

// ---------------------------------------------------------------------------
// Preview dialog — render template with real contract data
// ---------------------------------------------------------------------------
function _show_contract_preview(frm, template_name) {
	frappe.call({
		method: "dcnet_contract.dcnet_contract.api.preview_template_with_contract",
		args: {
			contract_name: frm.doc.name,
			template_name: template_name,
		},
		freeze: true,
		freeze_message: __("Đang tạo xem trước..."),
		callback(r) {
			if (!r.message) {
				frappe.msgprint({ message: __("Không thể tạo xem trước. Vui lòng thử lại."), indicator: "red" });
				return;
			}

			const previewHtml = r.message.html || "";
			const tplName = r.message.template_name || template_name;
			const noPlaceholders = r.message.no_placeholders;

			const warningBanner = noPlaceholders
				? `<div style="padding:10px 12px;background:#FEF9C3;border:1px solid #FCD34D;border-radius:6px;margin-bottom:10px;font-size:12px;color:#92400E;">
					<i class="fa fa-exclamation-triangle"></i>
					<b>Mẫu chưa có placeholder.</b>
					Các trường dữ liệu hợp đồng sẽ không được điền vào. Hãy mở trình soạn mẫu, thêm placeholder (ví dụ: <code>{{customer_tax_id}}</code>, <code>{{customer_bank_account}}</code>), rồi bấm <b>Lưu mẫu</b> trước khi xem trước.
					<a href="/app/contract-template-builder?template=${encodeURIComponent(template_name)}&contract=${encodeURIComponent(frm.doc.name)}" target="_blank"
					   style="margin-left:8px;font-weight:600;">Mở trình soạn mẫu →</a>
				</div>`
				: "";

			const d = new frappe.ui.Dialog({
				title: __("Xem trước: ") + tplName,
				size: "extra-large",
				fields: [
					{
						fieldname: "info",
						fieldtype: "HTML",
						options: `${warningBanner}<div style="padding:8px 0;color:var(--text-muted);font-size:12px;">
							<i class="fa fa-file-text-o"></i> Hợp đồng: <b>${frm.doc.name}</b>
							&middot; Khách hàng: <b>${frappe.utils.escape_html(frm.doc.customer_name || frm.doc.customer || "")}</b>
							&middot; Mẫu: <b>${frappe.utils.escape_html(tplName)}</b>
						</div>`,
					},
					{
						fieldname: "preview_container",
						fieldtype: "HTML",
						options: `<div style="background:#f0f0f0;padding:16px;overflow-y:auto;max-height:70vh;">
							<div style="background:#fff;padding:48px 64px;min-height:600px;font-family:'Times New Roman',serif;font-size:13pt;line-height:1.8;color:#111;max-width:800px;margin:0 auto;box-shadow:0 2px 12px rgba(0,0,0,0.12);border-radius:2px;">
								${previewHtml}
							</div>
						</div>`,
					},
				],
				primary_action_label: __("In / Xuất PDF"),
				primary_action() {
					const printWindow = window.open("", "_blank");
					printWindow.document.write(`<!DOCTYPE html>
<html>
<head>
	<title>${frm.doc.name} - ${tplName}</title>
	<style>
		@page { size: A4; margin: 20mm; }
		body { font-family: 'Times New Roman', serif; font-size: 13pt; line-height: 1.8; color: #111; max-width: 800px; margin: 0 auto; padding: 20mm; }
		table { width: 100%; border-collapse: collapse; margin: 8px 0; }
		td, th { padding: 4px 8px; border: 1px solid #999; }
		@media print { body { max-width: none; margin: 0; padding: 0; } }
	</style>
</head>
<body>
	${previewHtml}
	<script>window.onload = function() { window.print(); };<\/script>
</body>
</html>`);
					printWindow.document.close();
				},
			});
			d.show();
		},
	});
}

// Template integration handlers (from dcnet_contract_template_integration.js)
frappe.ui.form.on("DCNet Contract", {
	onload(frm) {
		// Cache original HTML for edit detection
		if (frm.doc.contract_html) {
			frm.doc.__original_contract_html = frm.doc.contract_html;
		}
		// Filter template_ref to only Approved templates
		frm.set_query("template_ref", () => ({
			filters: { status: "Approved" },
		}));
	},

	refresh(frm) {
		// Template version warning for Draft contracts
		if (frm.doc.template_ref && frm.doc.docstatus === 0 && frm.doc.template_outdated) {
			frm.dashboard.set_headline(
				__("Template has been updated. Click 'Re-apply Template' to use the latest version."),
				"orange"
			);
		}
		// Apply Template button (Draft only, template selected)
		if (frm.doc.template_ref && frm.doc.docstatus === 0) {
			frm.add_custom_button(__("Apply Template"), () => {
				let warning = "";
				if (frm.doc.contract_html_edited) {
					warning = __("You have edited the contract content. Applying template will overwrite your changes. Continue?");
				} else {
					warning = __("Apply template content to this contract?");
				}
				frappe.confirm(warning, () => {
					frappe.call({
						method: "dcnet_contract.dcnet_contract.utils.template_engine.apply_template",
						args: {
							contract_name: frm.doc.name,
							template_name: frm.doc.template_ref,
						},
						callback: () => frm.reload_doc(),
					});
				});
			}, __("Template"));
		}
	},

	template_ref(frm) {
		if (!frm.doc.template_ref) return;
		// Auto-fill from template
		frappe.call({
			method: "dcnet_contract.dcnet_contract.doctype.dcnet_contract_template.dcnet_contract_template.get_template",
			args: { template_name: frm.doc.template_ref },
			callback(r) {
				if (!r.message) return;
				const tmpl = r.message;
				if (tmpl.service_type) frm.set_value("service_type", tmpl.service_type);
				if (tmpl.contract_type) frm.set_value("contract_type", tmpl.contract_type);
				if (tmpl.payment_mode) frm.set_value("payment_mode", tmpl.payment_mode);
				if (tmpl.package_term_months) frm.set_value("package_term_months", tmpl.package_term_months);
				if (!frm.doc.items || frm.doc.items.length === 0) {
					frm.clear_table("items");
					(tmpl.items || []).forEach((item) => {
						frm.add_child("items", item);
					});
					frm.refresh_field("items");
				}
				frm.set_value("template_version", tmpl.version || 1);
			},
		});
	},

	contract_html(frm) {
		// Track if HTML was edited by user
		if (frm.doc.template_ref && frm.doc.__original_contract_html !== undefined) {
			if (frm.doc.contract_html !== frm.doc.__original_contract_html) {
				frm.set_value("contract_html_edited", 1);
			}
		}
	},
});
