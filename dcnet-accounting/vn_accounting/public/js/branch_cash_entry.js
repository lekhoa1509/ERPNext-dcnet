frappe.ui.form.on("Branch Cash Entry", {
	setup(frm) {
		frm.set_query("branch", () => getBranchQuery(frm));
		patchInvoiceAttachWithoutAutosave(frm);

		frm.set_query("accounting_unit", () => ({
			filters: {
				company: frm.doc.company,
				is_group: 0,
			},
		}));

		frm.set_query("cash_account", () => ({
			filters: {
				company: frm.doc.company,
				is_group: 0,
				account_number: ["like", "111%"],
			},
		}));

		frm.set_query("offset_account", () => ({
			filters: {
				company: frm.doc.company,
				is_group: 0,
			},
		}));
	},

	async onload(frm) {
		await applyUserBranchContext(frm);
	},

	async refresh(frm) {
		patchInvoiceAttachWithoutAutosave(frm);
		await applyUserBranchContext(frm);
		toggleOfficialFields(frm);
		updatePostingScopeIntro(frm);
		toggleInvoiceSections(frm);

		if (frm.doc.official_journal_entry) {
			frm.add_custom_button(__("Mở bút toán"), () => {
				frappe.set_route("Form", "Journal Entry", frm.doc.official_journal_entry);
			});
		}
	},

	posting_scope(frm) {
		toggleOfficialFields(frm);
		updatePostingScopeIntro(frm);
	},

	has_invoice(frm) {
		toggleInvoiceSections(frm);
	},

	invoice_file(frm) {
		toggleInvoiceSections(frm);
		if (frm.doc.has_invoice && frm.doc.invoice_file) {
			loadInvoice(frm);
		}
	},

	load_invoice_btn(frm) {
		loadInvoice(frm);
	},
});

let branchContextPromise;

function patchInvoiceAttachWithoutAutosave(frm) {
	const field = frm.fields_dict.invoice_file;
	if (!field || field.__branchCashNoAutosavePatched) return;

	field.__branchCashNoAutosavePatched = true;
	field.on_upload_complete = async function (attachment) {
		if (!attachment || !attachment.file_url) return;

		await this.parse_validate_and_set_in_model(attachment.file_url);
		if (this.frm && this.frm.attachments) {
			this.frm.attachments.update_attachment(attachment);
		}
		this.set_input(attachment.file_url);
		this.toggle_reload_button();
	};
}

function getBranchQuery(frm) {
	const context = frm.__branchPermissionContext;
	if (!context || context.is_privileged || !context.branch) {
		return {};
	}

	return {
		filters: {
			name: context.branch,
		},
	};
}

async function applyUserBranchContext(frm) {
	const context = await getCurrentUserBranchContext();
	frm.__branchPermissionContext = context;

	if (context.is_privileged) {
		frm.set_df_property("branch", "read_only", 0);
		return;
	}

	if (context.branch) {
		if (!frm.doc.branch || frm.is_new()) {
			await frm.set_value("branch", context.branch);
		}
		frm.set_df_property("branch", "read_only", 1);
		return;
	}

	frm.set_df_property("branch", "read_only", 1);
	if (!frm.__branchPermissionWarned) {
		frappe.msgprint(__("User hiện tại chưa được gán chi nhánh trên hồ sơ User."));
		frm.__branchPermissionWarned = true;
	}
}

async function getCurrentUserBranchContext() {
	if (!branchContextPromise) {
		branchContextPromise = frappe.call({
			method: "vn_accounting.branch_cash.service.get_current_user_branch_context",
		});
	}

	const response = await branchContextPromise;
	return response.message || {};
}

function toggleOfficialFields(frm) {
	const isOfficial = frm.doc.posting_scope === "Official";
	frm.toggle_reqd("cash_account", isOfficial);
	frm.toggle_reqd("offset_account", isOfficial);
	frm.toggle_display("cash_account", isOfficial);
	frm.toggle_display("offset_account", isOfficial);
	frm.toggle_display("official_journal_entry", Boolean(frm.doc.official_journal_entry));
}

function toggleInvoiceSections(frm) {
	const enabled = Boolean(frm.doc.has_invoice);
	[
		"invoice_file",
		"section_break_invoice_meta",
		"section_break_invoice_seller",
		"section_break_invoice_buyer",
		"section_break_invoice_payment",
		"section_break_invoice_items",
		"section_break_invoice_totals",
	].forEach((field) => frm.toggle_display(field, enabled));
	frm.toggle_display("load_invoice_btn", enabled && Boolean(frm.doc.invoice_file));
}

async function loadInvoice(frm) {
	if (!frm.doc.invoice_file) {
		frappe.msgprint(__("Vui lòng tải lên file hóa đơn (XML/HTML) trước."));
		return;
	}

	frappe.dom.freeze(__("Đang đọc dữ liệu hóa đơn..."));
	try {
		const r = await frappe.call({
			method: "vn_accounting.vn_accounting.doctype.branch_cash_entry.branch_cash_entry.load_invoice_from_file",
			args: { file_url: frm.doc.invoice_file },
		});
		const data = r.message || {};
		await applyInvoiceData(frm, data);
		frappe.show_alert({ message: __("Đã tải dữ liệu hóa đơn."), indicator: "green" });
	} catch (err) {
		console.error(err);
	} finally {
		frappe.dom.unfreeze();
	}
}

async function applyInvoiceData(frm, data) {
	const scalarFields = [
		"invoice_form_no",
		"invoice_serial",
		"invoice_number",
		"invoice_id",
		"invoice_date",
		"invoice_currency",
		"exchange_rate",
		"seller_name",
		"seller_tax_code",
		"seller_phone",
		"seller_address",
		"buyer_contact_name",
		"buyer_company_name",
		"buyer_tax_code",
		"buyer_warehouse",
		"buyer_address",
		"payment_method",
		"payment_due_date",
		"buyer_bank_account",
		"buyer_bank_name",
		"reference_number",
		"total_before_tax",
		"tax_rate",
		"tax_amount",
		"total_amount",
		"total_in_words",
	];

	for (const field of scalarFields) {
		if (data[field] !== undefined && data[field] !== null && data[field] !== "") {
			frm.doc[field] = data[field];
		}
	}

	frm.doc.invoice_items = [];
	(data.invoice_items || []).forEach((item) => {
		const row = frm.add_child("invoice_items");
		Object.assign(row, item);
	});

	if (!frm.doc.amount && data.total_amount) {
		frm.doc.amount = data.total_amount;
	}
	if (!frm.doc.remarks && data.invoice_number) {
		const note = `Hóa đơn ${data.invoice_serial || ""} số ${data.invoice_number}`.trim();
		frm.doc.remarks = note;
	}

	frm.refresh_fields();
	frm.dirty();
}

function updatePostingScopeIntro(frm) {
	if (frm.doc.posting_scope === "Official") {
		frm.set_intro(__("Chế độ hạch toán sổ cái sẽ tự tạo bút toán khi nộp phiếu."), "blue");
		return;
	}

	if (frm.doc.posting_scope === "Internal") {
		frm.set_intro(__("Chế độ nội bộ chỉ ghi nhận trong quỹ chi nhánh, không hạch toán vào sổ cái."), "orange");
		return;
	}

	frm.set_intro("");
}
