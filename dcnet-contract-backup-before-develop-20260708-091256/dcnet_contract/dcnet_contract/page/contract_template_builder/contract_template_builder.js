frappe.pages["contract-template-builder"].on_page_load = function (wrapper) {
	const params = frappe.utils.get_query_params();
	const templateKey = params.template || "";
	const isNew = params.new === "1";
	const contractName = params.contract || ""; // Contract name passed from "In hợp đồng" dialog

	const pageTitle = contractName
		? `Trình soạn mẫu hợp đồng — ${contractName}`
		: "Trình soạn mẫu hợp đồng";

	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: pageTitle,
		single_column: true,
	});

	// -----------------------------------------------------------------------
	// Styles
	// -----------------------------------------------------------------------
	frappe.dom.set_style(`
		.ctb-wrap { display:flex; flex-direction:column; height:calc(100vh - 95px); background:#f0f0f0; }

		/* Meta bar */
		.ctb-meta { display:flex; align-items:center; gap:8px; padding:8px 12px;
		            background:#fff; border-bottom:1px solid var(--border-color); flex-wrap:wrap; }
		.ctb-meta input.ctb-name {
			border:none; border-bottom:2px solid var(--border-color);
			font-size:15px; font-weight:600; padding:4px 6px; min-width:240px; outline:none; }
		.ctb-meta input.ctb-name:focus { border-bottom-color:var(--primary); }
		.ctb-meta select.form-control { height:30px; padding:2px 6px; font-size:12px; }

		/* Body */
		.ctb-body { display:flex; flex:1; overflow:hidden; }

		/* Sidebar */
		.ctb-sidebar {
			width:240px; min-width:200px; background:#fff;
			border-right:1px solid var(--border-color); overflow-y:auto; }
		.ctb-sidebar-search { padding:8px; border-bottom:1px solid var(--border-color); }
		.ctb-sidebar-search input {
			width:100%; padding:4px 8px; border:1px solid var(--border-color);
			border-radius:4px; font-size:12px; outline:none; }
		.ctb-group-header {
			padding:6px 10px 3px; font-size:10px; font-weight:700;
			color:var(--text-muted); text-transform:uppercase; letter-spacing:.5px;
			background:#fafafa; border-bottom:1px solid var(--border-color); margin-top:4px; }
		.ctb-chip {
			margin:3px 8px; padding:5px 9px; background:#EEF5FF;
			border:1px solid #BFDBFE; border-radius:4px; cursor:grab;
			display:flex; align-items:center; gap:6px; user-select:none; }
		.ctb-chip:hover { background:#DBEAFE; border-color:#93C5FD; }
		.ctb-chip:active { cursor:grabbing; }
		.ctb-chip-label { flex:1; font-size:12px; color:#1e40af; font-weight:500; }
		.ctb-chip-key { font-size:10px; color:#6b7280; font-family:monospace; }

		/* Editor section */
		.ctb-editor-col { flex:1; display:flex; flex-direction:column; overflow:hidden; }
		.ctb-toolbar {
			background:#fff; border-bottom:1px solid var(--border-color);
			padding:5px 10px; display:flex; align-items:center; gap:2px; flex-wrap:wrap; }
		.ctb-tb-btn {
			padding:3px 9px; border:1px solid transparent; background:transparent;
			border-radius:3px; cursor:pointer; font-size:13px; line-height:1.4;
			color:var(--text-color); }
		.ctb-tb-btn:hover { background:#f3f4f6; border-color:#d1d5db; }
		.ctb-tb-sep { width:1px; height:20px; background:#e5e7eb; margin:0 4px; }
		.ctb-tb-select {
			padding:2px 6px; border:1px solid #d1d5db; border-radius:3px;
			font-size:12px; cursor:pointer; }

		/* Page area */
		.ctb-page-area {
			flex:1; overflow-y:auto; padding:24px 32px; background:#f0f0f0; }
		.ctb-editor {
			background:#fff; min-height:1000px; width:100%; max-width:800px;
			margin:0 auto; padding:48px 64px; box-shadow:0 2px 12px rgba(0,0,0,.12);
			border-radius:2px; outline:none; font-family:'Times New Roman',serif;
			font-size:13pt; line-height:1.8; color:#111; }
		.ctb-editor:empty:before {
			content:attr(data-placeholder); color:#9ca3af; pointer-events:none; }
		.ctb-editor:focus { box-shadow:0 2px 12px rgba(0,0,0,.15); }

		/* Placeholder chip inside editor */
		.ph { display:inline-block; background:#FEF9C3; border:1px solid #FCD34D;
		       border-radius:3px; padding:0 6px; font-size:11px; font-family:monospace;
		       color:#92400E; line-height:1.6; vertical-align:middle;
		       cursor:grab; user-select:none; white-space:nowrap; }
		.ph:hover { background:#FEF08A; }
		.ph:active { cursor:grabbing; }
		.ph.ph-dragging { opacity:0.4; }

		/* Drag-over highlight */
		.ctb-editor.drag-over { outline:2px dashed var(--primary); outline-offset:2px; }

		/* Preview dialog */
		.ctb-preview-wrap { padding: 16px; background: #f0f0f0; }
		.ctb-preview-page {
			background: #fff; padding: 48px 64px; min-height: 800px;
			font-family: 'Times New Roman', serif; font-size: 13pt;
			line-height: 1.8; color: #111; max-width: 800px;
			margin: 0 auto; box-shadow: 0 2px 12px rgba(0,0,0,0.12);
			border-radius: 2px;
		}
		.ctb-preview-ph {
			background: #fef08a; color: #92400e; padding: 0 4px;
			border-radius: 2px; font-size: 11px; font-family: monospace;
		}
	`);

	// -----------------------------------------------------------------------
	// Markup
	// -----------------------------------------------------------------------
	const $body = $(wrapper).find(".page-content");
	$body.html(`
		<div class="ctb-wrap">
			<div class="ctb-meta">
				<input class="ctb-name" type="text" placeholder="Tên mẫu hợp đồng..." />
				<select class="form-control" id="ctb-category" style="width:140px">
					<option value="">Loại mẫu</option>
					<option value="Hợp đồng">Hợp đồng</option>
					<option value="Phụ lục">Phụ lục</option>
				</select>
				<select class="form-control" id="ctb-svc" style="width:140px">
					<option value="">Loại dịch vụ</option>
					<option value="P2P">P2P</option>
					<option value="MPLS">MPLS</option>
					<option value="ILL">ILL</option>
					<option value="FTTH DN">FTTH DN</option>
					<option value="IT Managed">IT Managed</option>
					<option value="VTTB">VTTB</option>
					<option value="Thi công">Thi công</option>
				</select>
				<div style="flex:1"></div>
				<button class="btn btn-default btn-sm" id="ctb-import">
					<i class="fa fa-upload"></i>&nbsp;Nhập từ Word
				</button>
				<button class="btn btn-default btn-sm" id="ctb-preview">
					<i class="fa fa-eye"></i>&nbsp;Xem trước
				</button>
				<button class="btn btn-primary btn-sm" id="ctb-save">
					<i class="fa fa-save"></i>&nbsp;Lưu mẫu
				</button>
			</div>

			<div class="ctb-body">
				<!-- Left sidebar -->
				<div class="ctb-sidebar">
					<div class="ctb-sidebar-search">
						<input type="text" id="ctb-search" placeholder="Tìm trường..."/>
					</div>
					<div id="ctb-field-list">
						<div style="padding:20px;text-align:center;color:var(--text-muted)">
							<i class="fa fa-spinner fa-spin"></i>
						</div>
					</div>
				</div>

				<!-- Editor -->
				<div class="ctb-editor-col">
					<div class="ctb-toolbar" id="ctb-toolbar">
						<button class="ctb-tb-btn" data-cmd="bold" title="Đậm (Ctrl+B)"><b>B</b></button>
						<button class="ctb-tb-btn" data-cmd="italic" title="Nghiêng (Ctrl+I)"><i>I</i></button>
						<button class="ctb-tb-btn" data-cmd="underline" title="Gạch chân (Ctrl+U)"><u>U</u></button>
						<div class="ctb-tb-sep"></div>
						<button class="ctb-tb-btn" data-cmd="justifyLeft" title="Căn trái">
							<i class="fa fa-align-left"></i></button>
						<button class="ctb-tb-btn" data-cmd="justifyCenter" title="Căn giữa">
							<i class="fa fa-align-center"></i></button>
						<button class="ctb-tb-btn" data-cmd="justifyRight" title="Căn phải">
							<i class="fa fa-align-right"></i></button>
						<button class="ctb-tb-btn" data-cmd="justifyFull" title="Căn đều">
							<i class="fa fa-align-justify"></i></button>
						<div class="ctb-tb-sep"></div>
						<select class="ctb-tb-select" id="ctb-heading">
							<option value="p">Đoạn văn</option>
							<option value="h1">Tiêu đề 1</option>
							<option value="h2">Tiêu đề 2</option>
							<option value="h3">Tiêu đề 3</option>
						</select>
						<div class="ctb-tb-sep"></div>
						<button class="ctb-tb-btn" data-cmd="insertOrderedList" title="Danh sách số">
							<i class="fa fa-list-ol"></i></button>
						<button class="ctb-tb-btn" data-cmd="insertUnorderedList" title="Danh sách đầu mục">
							<i class="fa fa-list-ul"></i></button>
						<div class="ctb-tb-sep"></div>
						<button class="ctb-tb-btn" data-cmd="insertHorizontalRule" title="Đường kẻ">
							<i class="fa fa-minus"></i></button>
						<button class="ctb-tb-btn" id="ctb-insert-table" title="Thêm bảng">
							<i class="fa fa-table"></i></button>
					</div>

					<div class="ctb-page-area">
						<div class="ctb-editor" id="ctb-editor" contenteditable="true"
							 data-placeholder="Kéo trường từ thanh bên, hoặc nhấp vào trường để chèn tại vị trí con trỏ…">
						</div>
					</div>
				</div>
			</div>
		</div>
	`);

	// -----------------------------------------------------------------------
	// State
	// -----------------------------------------------------------------------
	let currentKey = templateKey;
	let savedDocxUrl = "";
	let _draggingEditorChip = null; // chip being moved within the editor

	// -----------------------------------------------------------------------
	// Toolbar commands
	// -----------------------------------------------------------------------
	$("#ctb-toolbar .ctb-tb-btn[data-cmd]").on("click", function (e) {
		e.preventDefault();
		document.execCommand($(this).data("cmd"), false, null);
		$("#ctb-editor").focus();
	});

	$("#ctb-heading").on("change", function () {
		document.execCommand("formatBlock", false, this.value);
		$("#ctb-editor").focus();
	});

	$("#ctb-insert-table").on("click", function (e) {
		e.preventDefault();
		const tableHtml = `
			<table border="1" style="width:100%;border-collapse:collapse;margin:8px 0">
				<tr>
					<td style="padding:4px 8px;border:1px solid #999">&nbsp;</td>
					<td style="padding:4px 8px;border:1px solid #999">&nbsp;</td>
					<td style="padding:4px 8px;border:1px solid #999">&nbsp;</td>
				</tr>
				<tr>
					<td style="padding:4px 8px;border:1px solid #999">&nbsp;</td>
					<td style="padding:4px 8px;border:1px solid #999">&nbsp;</td>
					<td style="padding:4px 8px;border:1px solid #999">&nbsp;</td>
				</tr>
			</table><p><br></p>`;
		document.execCommand("insertHTML", false, tableHtml);
		$("#ctb-editor").focus();
	});

	// -----------------------------------------------------------------------
	// Placeholder chip helpers
	// -----------------------------------------------------------------------
	function _chipHtml(key) {
		return `<span class="ph" data-ph="${key}" contenteditable="false" draggable="true">{{${key}}}</span>`;
	}

	function insertAtCursor(key) {
		const editor = document.getElementById("ctb-editor");
		editor.focus();
		document.execCommand("insertHTML", false, _chipHtml(key) + "&nbsp;");
	}

	function loadIntoEditor(html) {
		// Decorate {{key}} as visual chips
		const decorated = html.replace(/\{\{(\w+)\}\}/g, function (_m, key) {
			return _chipHtml(key);
		});

		const editor = document.getElementById("ctb-editor");

		// Nếu HTML có sẵn style inline, giữ nguyên
		// Nếu không có block element, wrap trong <p>
		if (decorated && !decorated.match(/<(p|h[1-6]|div|table|ul|ol)/i)) {
			editor.innerHTML = `<p>${decorated}</p>`;
		} else {
			editor.innerHTML = decorated || "";
		}

		// Focus và đặt cursor ở cuối
		editor.focus();
	}

	function extractHtml() {
		const clone = document.getElementById("ctb-editor").cloneNode(true);
		clone.querySelectorAll(".ph").forEach(function (span) {
			const key = span.getAttribute("data-ph");
			span.replaceWith(document.createTextNode("{{" + key + "}}"));
		});
		return clone.innerHTML;
	}

	// -----------------------------------------------------------------------
	// Load field list
	// -----------------------------------------------------------------------
	frappe.call({
		method: "dcnet_contract.dcnet_contract.api.get_contract_fields",
		callback(r) {
			if (!r.message) return;
			const $list = $("#ctb-field-list").empty();
			let allChips = [];

			r.message.forEach(function (group) {
				const $header = $(`<div class="ctb-group-header">${group.group}</div>`);
				$list.append($header);

				group.fields.forEach(function (field) {
					const $chip = $(`
						<div class="ctb-chip" draggable="true"
						     data-key="${field.key}" data-label="${field.label}">
							<span class="ctb-chip-label">${field.label}</span>
							<span class="ctb-chip-key">${field.key}</span>
						</div>
					`);

					$chip[0].addEventListener("dragstart", function (e) {
						e.dataTransfer.setData("text/plain", "{{" + field.key + "}}");
						e.dataTransfer.setData("x-ph-key", field.key);
						e.dataTransfer.effectAllowed = "copy";
					});

					$chip.on("click", function () {
						insertAtCursor(field.key);
					});

					$list.append($chip);
					allChips.push({ key: field.key, label: field.label, el: $chip });
				});
			});

			// Search filter
			$("#ctb-search").on("input", function () {
				const q = this.value.toLowerCase().trim();
				allChips.forEach(function (c) {
					const match = !q || c.key.includes(q) || c.label.toLowerCase().includes(q);
					c.el.toggle(match);
				});
				// Hide headers with no visible chips
				$list.find(".ctb-group-header").each(function () {
					const $h = $(this);
					let hasVisible = false;
					let $next = $h.next();
					while ($next.length && !$next.hasClass("ctb-group-header")) {
						if ($next.is(":visible")) { hasVisible = true; break; }
						$next = $next.next();
					}
					$h.toggle(hasVisible);
				});
			});
		},
	});

	// -----------------------------------------------------------------------
	// Editor drag-over / drop  (handles both sidebar→editor and chip move)
	// -----------------------------------------------------------------------
	const editorEl = document.getElementById("ctb-editor");

	// Intercept dragstart from chips already inside the editor
	editorEl.addEventListener("dragstart", function (e) {
		const chip = e.target;
		if (chip && chip.classList && chip.classList.contains("ph")) {
			_draggingEditorChip = chip;
			chip.classList.add("ph-dragging");
			e.dataTransfer.setData("x-ph-key", chip.getAttribute("data-ph"));
			e.dataTransfer.setData("x-ph-from-editor", "1");
			e.dataTransfer.effectAllowed = "move";
		}
	});

	editorEl.addEventListener("dragend", function () {
		if (_draggingEditorChip) {
			_draggingEditorChip.classList.remove("ph-dragging");
			_draggingEditorChip = null;
		}
	});

	editorEl.addEventListener("dragover", function (e) {
		e.preventDefault();
		e.dataTransfer.dropEffect = _draggingEditorChip ? "move" : "copy";
		editorEl.classList.add("drag-over");
	});

	editorEl.addEventListener("dragleave", function (e) {
		// Only remove highlight when leaving the editor entirely
		if (!editorEl.contains(e.relatedTarget)) {
			editorEl.classList.remove("drag-over");
		}
	});

	editorEl.addEventListener("drop", function (e) {
		e.preventDefault();
		editorEl.classList.remove("drag-over");
		const key = e.dataTransfer.getData("x-ph-key");
		if (!key) return;

		const fromEditor = e.dataTransfer.getData("x-ph-from-editor") === "1";

		// Determine caret position at drop point
		let range;
		if (document.caretRangeFromPoint) {
			range = document.caretRangeFromPoint(e.clientX, e.clientY);
		} else if (document.caretPositionFromPoint) {
			const pos = document.caretPositionFromPoint(e.clientX, e.clientY);
			if (pos) {
				range = document.createRange();
				range.setStart(pos.offsetNode, pos.offset);
			}
		}

		if (fromEditor && _draggingEditorChip) {
			// Move: remove chip from original position, re-insert at drop target
			const chip = _draggingEditorChip;
			_draggingEditorChip = null;
			chip.classList.remove("ph-dragging");
			chip.remove();
		} else {
			_draggingEditorChip = null;
		}

		if (range) {
			const sel = window.getSelection();
			sel.removeAllRanges();
			sel.addRange(range);
		}
		insertAtCursor(key);
	});

	// -----------------------------------------------------------------------
	// Click on chip → move cursor to right after it (prevents cursor landing inside)
	// -----------------------------------------------------------------------
	editorEl.addEventListener("click", function (e) {
		const chip = e.target && e.target.closest && e.target.closest(".ph");
		if (!chip) return;
		const range = document.createRange();
		range.setStartAfter(chip);
		range.collapse(true);
		const sel = window.getSelection();
		sel.removeAllRanges();
		sel.addRange(range);
	});

	// -----------------------------------------------------------------------
	// Keyboard: delete entire chip on Backspace / Delete
	// -----------------------------------------------------------------------
	editorEl.addEventListener("keydown", function (e) {
		if (e.key !== "Backspace" && e.key !== "Delete") return;

		const sel = window.getSelection();
		if (!sel || !sel.rangeCount) return;
		const range = sel.getRangeAt(0);

		// Case 0: cursor is somehow INSIDE a chip — delete the whole chip
		let node = range.startContainer;
		while (node && node !== editorEl) {
			if (node.nodeType === Node.ELEMENT_NODE && node.classList && node.classList.contains("ph")) {
				e.preventDefault();
				node.remove();
				return;
			}
			node = node.parentNode;
		}

		// If selection spans content, let browser handle it normally
		if (!range.collapsed) return;

		const { startContainer, startOffset } = range;
		let target = null;

		if (e.key === "Backspace") {
			if (startContainer.nodeType === Node.ELEMENT_NODE) {
				const prev = startContainer.childNodes[startOffset - 1];
				if (prev && prev.nodeType === Node.ELEMENT_NODE && prev.classList.contains("ph")) {
					target = prev;
				}
			} else if (startContainer.nodeType === Node.TEXT_NODE && startOffset === 0) {
				const prev = startContainer.previousSibling;
				if (prev && prev.nodeType === Node.ELEMENT_NODE && prev.classList.contains("ph")) {
					target = prev;
				}
			}
		} else { // Delete
			if (startContainer.nodeType === Node.ELEMENT_NODE) {
				const next = startContainer.childNodes[startOffset];
				if (next && next.nodeType === Node.ELEMENT_NODE && next.classList.contains("ph")) {
					target = next;
				}
			} else if (startContainer.nodeType === Node.TEXT_NODE &&
			           startOffset === startContainer.textContent.length) {
				const next = startContainer.nextSibling;
				if (next && next.nodeType === Node.ELEMENT_NODE && next.classList.contains("ph")) {
					target = next;
				}
			}
		}

		if (target) {
			e.preventDefault();
			target.remove();
		}
	});

	// -----------------------------------------------------------------------
	// Import DOCX
	// -----------------------------------------------------------------------
	$("#ctb-import").on("click", function () {
		const d = new frappe.ui.Dialog({
			title: "Nhập từ Word (.docx)",
			fields: [{
				fieldname: "docx_file",
				fieldtype: "Attach",
				label: "Chọn file Word (.docx)",
				reqd: 1,
				options: "Private",
				description: "File sẽ được chuyển đổi sang HTML, giữ nguyên định dạng Word.",
			}],
			primary_action_label: "Nhập",
			primary_action(values) {
				if (!values.docx_file) {
					frappe.msgprint({ message: "Vui lòng chọn file Word!", indicator: "red" });
					return;
				}

				d.hide();

				// Show loading với timeout
				frappe.show_alert({
					message: "Đang chuyển đổi file Word... Vui lòng chờ.",
					indicator: "blue"
				});

				// Disable button để tránh click nhiều lần
				$("#ctb-import").prop("disabled", true);

				frappe.call({
					method: "dcnet_contract.dcnet_contract.api.docx_to_html",
					args: { file_url: values.docx_file },
					callback(r) {
						$("#ctb-import").prop("disabled", false);

						if (r.exc) {
							// Error từ server
							frappe.throw({
								title: "Lỗi chuyển đổi",
								message: "Không thể chuyển đổi file Word. Vui lòng kiểm tra file và thử lại.",
							});
							return;
						}

						if (r.message && r.message.html) {
							savedDocxUrl = values.docx_file;
							loadIntoEditor(r.message.html);
							frappe.show_alert({
								message: "Đã nhập nội dung từ Word thành công!",
								indicator: "green"
							});
						} else {
							frappe.msgprint({
								message: "File Word không có nội dung hoặc không thể đọc được.",
								indicator: "orange"
							});
						}
					},
					error(err) {
						$("#ctb-import").prop("disabled", false);
						frappe.throw({
							title: "Lỗi kết nối",
							message: "Không thể kết nối đến server. Vui lòng thử lại.",
						});
					},
				});
			},
		});
		d.show();
	});

	// -----------------------------------------------------------------------
	// Preview
	// -----------------------------------------------------------------------
	$("#ctb-preview").on("click", function () {
		const html = extractHtml();
		const templateDisplayName = $(".ctb-name").val().trim() || "Mẫu hợp đồng";

		// Check if there are any placeholders
		const placeholders = html.match(/\{\{(\w+)\}\}/g);
		if (!placeholders) {
			frappe.msgprint({ message: "Mẫu chưa có placeholder nào để xem trước.", indicator: "orange" });
			return;
		}

		function _doPreviewWithContract(cname) {
			frappe.call({
				method: "dcnet_contract.dcnet_contract.api.preview_template_html",
				args: {
					contract_name: cname,
					template_html: html,
				},
				freeze: true,
				freeze_message: "Đang tạo xem trước với dữ liệu thật...",
				callback(r) {
					if (r.message && r.message.html) {
						_show_preview_dialog(r.message.html, templateDisplayName, cname);
					} else {
						frappe.show_alert({ message: "Không lấy được dữ liệu hợp đồng, hiển thị dữ liệu mẫu.", indicator: "orange" });
						_show_preview_with_sample(html, templateDisplayName);
					}
				},
			});
		}

		// If we have a contract context, use real data from API
		if (contractName) {
			_doPreviewWithContract(contractName);
		} else {
			// No contract context — ask user to pick one for real-data preview
			const d = new frappe.ui.Dialog({
				title: "Xem trước với hợp đồng",
				fields: [
					{
						fieldname: "info",
						fieldtype: "HTML",
						options: `<div style="padding:6px 0 10px;color:var(--text-muted);font-size:12px;">
							Chọn một hợp đồng để xem trước với dữ liệu thật.
							Bỏ qua để xem với dữ liệu mẫu.
						</div>`,
					},
					{
						fieldname: "contract_name",
						fieldtype: "Link",
						label: "Hợp đồng",
						options: "DCNet Contract",
					},
				],
				primary_action_label: "Xem trước",
				primary_action(values) {
					d.hide();
					if (values.contract_name) {
						_doPreviewWithContract(values.contract_name);
					} else {
						_show_preview_with_sample(html, templateDisplayName);
					}
				},
				secondary_action_label: "Dùng dữ liệu mẫu",
				secondary_action() {
					d.hide();
					_show_preview_with_sample(html, templateDisplayName);
				},
			});
			d.show();
		}
	});

	// -----------------------------------------------------------------------
	// Save
	// -----------------------------------------------------------------------
	$("#ctb-save").on("click", function () {
		const name = $(".ctb-name").val().trim();
		if (!name) {
			frappe.msgprint({ message: "Vui lòng nhập tên mẫu.", indicator: "orange" });
			return;
		}

		const html = extractHtml();
		frappe.call({
			method: "dcnet_contract.dcnet_contract.api.save_template_from_builder",
			args: {
				template_name_key: currentKey || "",
				display_name: name,
				html_content: html,
				template_category: $("#ctb-category").val() || "",
				service_type: $("#ctb-svc").val() || "",
				docx_file_url: savedDocxUrl || "",
			},
			freeze: true,
			freeze_message: "Đang lưu mẫu...",
			callback(r) {
				if (r.message) {
					currentKey = r.message.name;
					// Update URL without page reload
					if (history.replaceState) {
						history.replaceState(
							{},
							"",
							"/app/contract-template-builder?template=" + encodeURIComponent(currentKey)
						);
					}
					frappe.show_alert({ message: "Đã lưu mẫu: " + r.message.template_name, indicator: "green" });
				}
			},
		});
	});

	// -----------------------------------------------------------------------
	// Load existing template on page load
	// -----------------------------------------------------------------------
	if (templateKey && !isNew) {
		frappe.call({
			method: "dcnet_contract.dcnet_contract.api.get_template_html",
			args: { template_name: templateKey },
			callback(r) {
				if (!r.message) return;
				const tpl = r.message;
				$(".ctb-name").val(tpl.template_name || "");
				$("#ctb-category").val(tpl.template_category || "");
				$("#ctb-svc").val(tpl.service_type || "");
				savedDocxUrl = tpl.template_file || "";
				if (tpl.template_html) {
					loadIntoEditor(tpl.template_html);
				}
			},
		});
	}
};

// ---------------------------------------------------------------------------
// Preview helper functions
// ---------------------------------------------------------------------------
function _show_preview_dialog(previewHtml, templateName, contractName) {
	const infoHtml = contractName
		? `<div style="padding:8px 0;color:var(--text-muted);font-size:12px;">
			<i class="fa fa-file-text-o"></i> Hợp đồng: <b>${contractName}</b>
			&middot; Mẫu: <b>${templateName}</b>
			&middot; <span style="color:green;">Dữ liệu thật</span>
		   </div>`
		: `<div style="padding:8px 0;color:var(--text-muted);font-size:12px;">
			<i class="fa fa-file-text-o"></i> Mẫu: <b>${templateName}</b>
			&middot; <span style="color:orange;">Dữ liệu mẫu</span>
		   </div>`;

	const d = new frappe.ui.Dialog({
		title: "Xem trước mẫu hợp đồng",
		size: "extra-large",
		fields: [
			{ fieldname: "info", fieldtype: "HTML", options: infoHtml },
			{
				fieldname: "preview_html",
				fieldtype: "HTML",
				options: `
					<div class="ctb-preview-wrap">
						<div class="ctb-preview-page">
							${previewHtml}
						</div>
					</div>
				`,
			},
		],
		primary_action_label: "In / Xuất PDF",
		primary_action() {
			const printWindow = window.open("", "_blank");
			printWindow.document.write(`
				<!DOCTYPE html>
				<html>
				<head>
					<title>${templateName}</title>
					<style>
						@page { size: A4; margin: 20mm; }
						body { font-family: 'Times New Roman', serif; font-size: 13pt; line-height: 1.8; color: #111; max-width: 800px; margin: 0 auto; }
						table { width: 100%; border-collapse: collapse; margin: 8px 0; }
						td, th { padding: 4px 8px; border: 1px solid #999; }
						@media print { body { max-width: none; margin: 0; } }
					</style>
				</head>
				<body>
					${previewHtml}
					<script>window.onload = function() { window.print(); };</script>
				</body>
				</html>
			`);
			printWindow.document.close();
		},
	});
	d.show();
}

function _show_preview_with_sample(html, templateName) {
	const sampleData = {
		customer_name: "CÔNG TY TNHH ABC", customer_address: "123 Nguyễn Huệ, Q.1, TP.HCM",
		customer_phone: "028 1234 5678", customer_fax: "028 1234 5679",
		customer_email: "contact@abc.com.vn", customer_tax_id: "0123456789",
		customer_representative: "Nguyễn Văn A", customer_representative_title: "Giám đốc",
		customer_bank_account: "1234567890", customer_id_number: "012345678901",
		customer_id_date: "01/01/2020", customer_id_place: "TP. Hồ Chí Minh",
		customer_dob: "01/01/1980",
		company_name_b: "CÔNG TY TNHH DCNET", company_address_b: "456 Lê Lợi, Q.3, TP.HCM",
		company_phone_b: "028 9876 5432", company_fax_b: "028 9876 5433",
		company_tax_id_b: "0987654321", company_representative_b: "Trần Văn B",
		company_representative_title_b: "Tổng Giám đốc", company_bank_account_b: "0987654321",
		company_bank_b: "Vietcombank",
		contract_number: "DCNET/2026/001", contract_date: "04 tháng 05 năm 2026",
		acceptance_date: "10 tháng 05 năm 2026", end_date: "04 tháng 05 năm 2027",
		package_term: "12 tháng", service_type: "P2P", package_name: "Gói Enterprise 100Mbps",
		installation_address: "789 Hai Bà Trưng, Q.1, TP.HCM",
		bandwidth: "100 Mbps", point_a: "Trụ sở chính - 123 Nguyễn Huệ, Q.1",
		point_b: "Chi nhánh - 789 Hai Bà Trưng, Q.1", sla_restore_hours: "4 giờ",
		monthly_fee: "5,000,000", monthly_fee_vat: "500,000", monthly_fee_total: "5,500,000",
		monthly_fee_words: "Năm triệu năm trăm nghìn đồng",
		setup_fee: "2,000,000", setup_fee_vat: "200,000", setup_fee_total: "2,200,000",
		setup_fee_words: "Hai triệu hai trăm nghìn đồng",
		item_stt: "01", item_label: "Dịch vụ Internet Leased Line",
		item_qty: "01", item_uom: "Gói", item_price: "5,000,000", item_amount: "5,000,000",
	};

	let previewHtml = html;
	Object.keys(sampleData).forEach(function (key) {
		const regex = new RegExp("\\{\\{" + key + "\\}\\}", "g");
		previewHtml = previewHtml.replace(regex, sampleData[key]);
	});

	const remaining = previewHtml.match(/\{\{(\w+)\}\}/g);
	if (remaining) {
		remaining.forEach(function (ph) {
			const escaped = ph.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
			previewHtml = previewHtml.replace(new RegExp(escaped, "g"), `<span class="ctb-preview-ph">${ph}</span>`);
		});
	}

	_show_preview_dialog(previewHtml, templateName, "");
}
