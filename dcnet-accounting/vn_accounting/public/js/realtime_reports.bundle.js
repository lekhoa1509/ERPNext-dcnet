/**
 * Realtime cho Query Reports (FB-2026-00625)
 *
 * Cơ chế: report đăng ký nghe `list_update` của các doctype NGUỒN (PE/JE/SI/...).
 * Khi user nào đó submit chứng từ -> Frappe tự broadcast list_update -> report
 * tự chạy lại query (report.refresh) mà KHÔNG cần F5.
 *
 * Các lớp chống quá tải:
 *  - Debounce gộp burst (vd JE nhiều dòng / import).
 *  - Bỏ qua khi tab đang ẩn (refresh lại khi quay lại tab).
 *  - Dirty-check rẻ (max modified + count chứng từ nguồn) trước khi re-query nặng.
 *  - Fallback poll 60s khi socket.io mất kết nối.
 *  - Toggle Bật/Tắt cho user; T1 mặc định Bật, T2 mặc định Tắt; T3 không có ở đây.
 *
 * Registry chính thức (đã duyệt 2026-05-29) — xem
 * docs/specs/2026-05-29-realtime-query-reports-analysis.md mục 3.
 */
(function () {
	const DEBOUNCE_MS = 2500;
	const POLL_MS = 60000;
	const LS_PREFIX = "vn_rt_enabled:"; // localStorage key cho toggle theo report

	// Báo cáo nguồn từ chứng từ tiền/quỹ
	const CASH_SRC = ["Payment Entry", "Journal Entry"];
	const BRANCH_SRC = ["Branch Cash Entry"];
	const LEDGER_SRC = [
		"Payment Entry",
		"Journal Entry",
		"Sales Invoice",
		"Purchase Invoice",
		"Stock Entry",
	];

	// report doc-name -> { tier, doctypes }
	const REGISTRY = {
		// ── TIER 1 — auto BẬT ──
		"Cash Receipts": { tier: 1, doctypes: CASH_SRC },
		"Cash Payments": { tier: 1, doctypes: CASH_SRC },
		"Bank Receipts": { tier: 1, doctypes: CASH_SRC },
		"Bank Payments": { tier: 1, doctypes: CASH_SRC },
		"Cash Book": { tier: 1, doctypes: CASH_SRC },
		"Bank Account Book": { tier: 1, doctypes: CASH_SRC },
		"So Quy Chi Nhanh": { tier: 1, doctypes: BRANCH_SRC },
		"So Noi Bo": { tier: 1, doctypes: BRANCH_SRC },
		// ── TIER 2 — toggle, mặc định TẮT ──
		"Account Detail Ledger": { tier: 2, doctypes: LEDGER_SRC },
		"S03b-DN So Cai": { tier: 2, doctypes: LEDGER_SRC },
		"S03a-DN So Nhat Ky Chung": { tier: 2, doctypes: LEDGER_SRC },
		"Auto Generated Docs Pending": { tier: 2, doctypes: ["Journal Entry"] },
		"Landed Cost Pending Allocation": { tier: 2, doctypes: ["Purchase Invoice"] },
		"Purchase No VAT": { tier: 2, doctypes: ["Purchase Invoice"] },
		"Internal Transfer": { tier: 2, doctypes: CASH_SRC },
	};

	// Trạng thái realtime của report đang mở (null khi không ở report nào trong registry)
	let STATE = null;
	let listenerBound = false;

	function isConnected() {
		return Boolean(frappe.realtime && frappe.realtime.socket && frappe.realtime.socket.connected);
	}

	function defaultEnabled(cfg) {
		const saved = localStorage.getItem(LS_PREFIX + STATE.name);
		if (saved === "1") return true;
		if (saved === "0") return false;
		return cfg.tier === 1; // T1 mặc định bật, T2 mặc định tắt
	}

	// ── Một handler list_update DUY NHẤT, đăng ký 1 lần, đọc STATE hiện hành ──
	function onListUpdate(data) {
		if (!STATE || !STATE.enabled || !data) return;
		if (!STATE.cfg.doctypes.includes(data.doctype)) return;
		scheduleRefresh();
	}

	function bindGlobalListenerOnce() {
		if (listenerBound || !frappe.realtime || !frappe.realtime.on) return;
		frappe.realtime.on("list_update", onListUpdate);
		listenerBound = true;
	}

	function scheduleRefresh() {
		if (!STATE) return;
		clearTimeout(STATE.debTimer);
		STATE.debTimer = setTimeout(function () {
			if (document.visibilityState !== "visible") {
				STATE.pendingWhileHidden = true; // refresh khi quay lại tab
				return;
			}
			maybeRefresh();
		}, DEBOUNCE_MS);
	}

	// Dirty-check rồi refresh nếu có dữ liệu mới
	async function maybeRefresh() {
		if (!STATE || !STATE.report) return;
		const route = frappe.get_route ? frappe.get_route() : [];
		if (route[0] !== "query-report" || route[1] !== STATE.name) return; // đã rời report

		const myGen = STATE.gen;
		let fp = null;
		try {
			fp = await fingerprint();
		} catch (e) {
			fp = null; // lỗi dirty-check -> cứ refresh cho an toàn
		}
		if (!STATE || STATE.gen !== myGen) return; // đã teardown trong lúc chờ

		if (fp !== null && fp === STATE.lastFingerprint) {
			return; // không có gì mới -> bỏ qua, tránh re-query nặng
		}
		STATE.lastFingerprint = fp;
		try {
			STATE.report.refresh();
			// Cue nhẹ để user biết bảng vừa tự đổi (không phải họ bấm)
			frappe.show_alert(
				{ message: __("Số liệu vừa tự cập nhật"), indicator: "green" },
				3
			);
		} catch (e) {
			// nuốt lỗi refresh để không vỡ vòng realtime
		}
	}

	// Gọi endpoint dirty-check; trả null nếu không đủ filter (=> luôn refresh)
	async function fingerprint() {
		const report = STATE.report;
		const company = report.get_filter_value ? report.get_filter_value("company") : null;
		if (!company) return null; // không có company -> bỏ dirty-check
		const r = await frappe.call({
			method: "vn_accounting.api.realtime.report_data_fingerprint",
			args: { doctypes: JSON.stringify(STATE.cfg.doctypes), company: company },
			// im lặng, không hiện loading indicator cho dirty-check
			freeze: false,
		});
		return r && r.message ? r.message : null;
	}

	function subscribe() {
		STATE.cfg.doctypes.forEach(function (dt) {
			frappe.realtime.doctype_subscribe(dt);
		});
	}

	function unsubscribe() {
		if (!STATE) return;
		STATE.cfg.doctypes.forEach(function (dt) {
			try {
				frappe.realtime.doctype_unsubscribe(dt);
			} catch (e) {}
		});
	}

	function startPoll() {
		stopPoll();
		STATE.pollTimer = setInterval(function () {
			if (!STATE || !STATE.enabled) return;
			if (isConnected()) {
				updateToggleButton();
				return; // socket sống -> push lo, poll nghỉ
			}
			// socket chết -> poll làm nhiệm vụ cập nhật
			updateToggleButton();
			if (document.visibilityState !== "visible") return;
			maybeRefresh();
		}, POLL_MS);
	}

	function stopPoll() {
		if (STATE && STATE.pollTimer) {
			clearInterval(STATE.pollTimer);
			STATE.pollTimer = null;
		}
	}

	async function enable() {
		if (!STATE) return;
		STATE.enabled = true;
		localStorage.setItem(LS_PREFIX + STATE.name, "1");
		bindGlobalListenerOnce();
		subscribe();
		startPoll();
		// baseline fingerprint để event đầu tiên không refresh oan
		try {
			STATE.lastFingerprint = await fingerprint();
		} catch (e) {
			STATE.lastFingerprint = null;
		}
		updateToggleButton();
	}

	function disable() {
		if (!STATE) return;
		STATE.enabled = false;
		localStorage.setItem(LS_PREFIX + STATE.name, "0");
		clearTimeout(STATE.debTimer);
		stopPoll();
		unsubscribe();
		updateToggleButton();
	}

	function toggle() {
		if (!STATE) return;
		if (STATE.enabled) disable();
		else enable();
	}

	// ── Nút toggle + trạng thái kết nối trên thanh report ──
	// Tự dựng nút (không dùng add_inner_button vì nó dồn nút vào dropdown "Hành động"
	// và trả về wrapper khiến cập nhật nhãn/màu không trúng).
	function ensureToggleButton() {
		if (!STATE || !STATE.report || !STATE.report.page) return;
		const $actions = STATE.report.page.wrapper.find(".page-actions");
		if (!$actions.length) return;
		// Dọn mọi nút cũ trước (chống nhân bản khi re-setup / F5 / race)
		$actions.find(".vn-rt-toggle").remove();
		// Nút trung tính (btn-default) như các nút khác trên thanh — không dùng màu solid.
		const $btn = $(
			'<button type="button" class="btn btn-default btn-sm vn-rt-toggle" style="margin-right:8px;"></button>'
		);
		$btn.on("click", toggle);
		$actions.prepend($btn);
		STATE.$btn = $btn;
		updateToggleButton();
	}

	// Trạng thái thể hiện bằng chấm indicator của Frappe (đồng bộ UI), không emoji.
	function statusColor() {
		if (!STATE || !STATE.enabled) return "gray";
		return isConnected() ? "green" : "orange";
	}

	function labelText() {
		if (!STATE || !STATE.enabled) return __("Tự cập nhật: Tắt");
		return isConnected() ? __("Tự cập nhật: Bật") : __("Tự cập nhật: đang dò lại");
	}

	function updateToggleButton() {
		if (!STATE || !STATE.$btn) return;
		try {
			STATE.$btn.html(
				'<span class="indicator ' +
					statusColor() +
					'"></span> ' +
					frappe.utils.escape_html(labelText())
			);
			STATE.$btn.attr(
				"title",
				STATE.enabled
					? __("Báo cáo tự cập nhật khi có chứng từ mới. Bấm để tắt.")
					: __("Bấm để bật báo cáo tự cập nhật khi có chứng từ mới.")
			);
		} catch (e) {}
	}

	// ── Vòng đời theo route ──
	function teardown() {
		if (!STATE) return;
		clearTimeout(STATE.debTimer);
		stopPoll();
		if (STATE.enabled) unsubscribe();
		if (STATE.$btn) {
			try {
				STATE.$btn.remove(); // gỡ nút khỏi DOM, tránh nhân bản khi quay lại report
			} catch (e) {}
		}
		STATE.gen += 1; // huỷ mọi maybeRefresh đang chờ
		STATE = null;
	}

	function setupForRoute(retries) {
		const route = frappe.get_route ? frappe.get_route() : [];
		// Route chưa resolve (đang boot / hard reload) -> chờ rồi thử lại
		if (!route.length) {
			if (retries > 0) setTimeout(() => setupForRoute(retries - 1), 300);
			return;
		}
		const isReport = route[0] === "query-report";
		const name = isReport ? route[1] : null;
		const cfg = name ? REGISTRY[name] : null;

		// Rời report cũ
		if (STATE && (!cfg || STATE.name !== name)) teardown();

		if (!cfg) return; // route không phải report trong registry
		if (STATE && STATE.name === name) return; // đã setup

		// chờ instance report sẵn sàng
		if (!frappe.query_report || frappe.query_report.report_name !== name || !frappe.query_report.page) {
			if (retries > 0) setTimeout(() => setupForRoute(retries - 1), 300);
			return;
		}

		STATE = {
			name: name,
			cfg: cfg,
			report: frappe.query_report,
			enabled: false,
			debTimer: null,
			pollTimer: null,
			lastFingerprint: null,
			pendingWhileHidden: false,
			$btn: null,
			gen: 0,
		};
		ensureToggleButton();
		if (defaultEnabled(cfg)) {
			enable();
		} else {
			updateToggleButton();
		}
	}

	// Khi quay lại tab: nếu có refresh bị hoãn lúc ẩn -> chạy
	document.addEventListener("visibilitychange", function () {
		if (document.visibilityState === "visible" && STATE && STATE.enabled && STATE.pendingWhileHidden) {
			STATE.pendingWhileHidden = false;
			maybeRefresh();
		}
	});

	// Cập nhật nhãn nút khi socket connect/disconnect
	function bindSocketStatus() {
		if (!frappe.realtime || !frappe.realtime.socket) return false;
		frappe.realtime.socket.on("connect", updateToggleButton);
		frappe.realtime.socket.on("disconnect", updateToggleButton);
		return true;
	}

	$(document).on("page-change", function () {
		setTimeout(() => setupForRoute(20), 300);
	});

	$(document).ready(function () {
		let tries = 20;
		const t = setInterval(function () {
			if (bindSocketStatus() || --tries <= 0) clearInterval(t);
		}, 400);
		setTimeout(() => setupForRoute(20), 800);
	});
})();
