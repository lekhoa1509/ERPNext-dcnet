import { defineStore } from "pinia";

const API = "vn_accounting.misa_migration.api.upload";
const PARSE_API = "vn_accounting.misa_migration.api.parse";
const REVIEW_API = "vn_accounting.misa_migration.api.review";
const POST_API = "vn_accounting.misa_migration.api.post";
const UNDO_API = "vn_accounting.misa_migration.api.undo";
const DEMO_API = "vn_accounting.misa_migration.api.demo_data";
const RESUME_API = "vn_accounting.misa_migration.api.resume";

// UX Gap 1: localStorage key for persisting the active batch_name across
// page reloads. Scoped per-site by the browser origin already, so no
// need to namespace further.
const _LS_KEY = "misa_migration_hub:active_batch";

// Map batch.status (server) → step index (UI stepper).
// Spec §8.6 state machine has 8 states; UI collapses to 4 steps.
const STATUS_TO_STEP = {
	DRAFT: 0,
	UPLOADED: 1,
	PARSED: 2,
	REVIEWED: 3, // advance to PostStep so user can press Đăng
	POSTING: 3,
	POSTED: 3,
	REVERSING: 3,
	REVERSED: 3,
	STUCK: 3, // show PostStep — has resume button + health check card + recovery tools
};

export const STEP_KEYS = ["upload", "parse", "review", "post"];

// Update document.title to show migration progress so the operator can
// see status from another tab. Format: "(75% — PHASE_4_SUBMIT) Misa Migration".
// Restores the original title on terminal state.
let _ORIG_TITLE = null;
function _update_tab_title(state, live) {
	try {
		if (_ORIG_TITLE === null) _ORIG_TITLE = document.title;
		const st = state.status;
		if (!st || st === "DRAFT" || st === "POSTED" || st === "REVERSED") {
			document.title = _ORIG_TITLE;
			return;
		}
		// Prefer live row-status based pct (from get_post_progress_live)
		// over the stale batch.posted_docs_count which only updates at
		// end of phase.
		let pct = 0;
		let phase = st;
		if (live && live.pct !== undefined) {
			pct = live.pct;
			if (live.phase_hint) phase = live.phase_hint;
		} else {
			const tot = state.total_rows || 0;
			const posted = state.posted_docs_count || 0;
			pct = tot ? Math.round(posted * 100 / tot) : 0;
		}
		document.title = `(${pct}% — ${phase}) ${_ORIG_TITLE}`;
	} catch (e) { /* document not available */ }
}

function _call(method, args = {}) {
	return new Promise((resolve, reject) => {
		frappe.call({
			method: method,
			args: args,
			callback: (r) => {
				if (r && r.message !== undefined) resolve(r.message);
				else resolve(null);
			},
			error: (xhr) => {
				const msg = xhr?.responseJSON?._server_messages || xhr?.statusText || "Network error";
				reject(new Error(typeof msg === "string" ? msg : JSON.stringify(msg)));
			},
		});
	});
}

function _uploadToFrappe(file, doctype, docname, fieldname) {
	// Use Frappe's standard upload endpoint. Returns the saved File doc.
	return new Promise((resolve, reject) => {
		const form = new FormData();
		form.append("file", file, file.name);
		form.append("is_private", 0);
		form.append("folder", "Home");
		if (doctype) form.append("doctype", doctype);
		if (docname) form.append("docname", docname);
		if (fieldname) form.append("fieldname", fieldname);
		fetch("/api/method/upload_file", {
			method: "POST",
			body: form,
			headers: { "X-Frappe-CSRF-Token": frappe.csrf_token || "" },
		})
			.then((r) => r.json())
			.then((j) => {
				if (j && j.message) resolve(j.message);
				else reject(new Error(j._server_messages || "upload_file failed"));
			})
			.catch(reject);
	});
}

export const useMisaStore = defineStore("misaMigration", {
	state: () => ({
		batch_name: null,
		batch_title: "",
		company: null,
		status: "DRAFT",
		files: [],
		total_rows: 0,
		posted_docs_count: 0,
		failed_rows_count: 0,
		job_id: null,
		stuck_at: null,
		notes: "",
		loading: false,
		last_error: null,
	}),

	getters: {
		activeStepIdx(state) {
			return STATUS_TO_STEP[state.status] ?? 0;
		},
		isLocked(state) {
			return ["POSTING", "REVERSING"].includes(state.status);
		},
		canPost(state) {
			return state.status === "REVIEWED";
		},
		canUndo(state) {
			return state.status === "POSTED";
		},
	},

	actions: {
		setBatch(payload) {
			if (!payload) {
				this.$reset();
				// UX Gap 1: clear persisted batch on reset
				try { localStorage.removeItem(_LS_KEY); } catch (e) { /* noop */ }
				return;
			}
			this.batch_name = payload.name ?? null;
			this.batch_title = payload.batch_title ?? "";
			this.company = payload.company ?? null;
			this.status = payload.status ?? "DRAFT";
			this.files = payload.files ?? [];
			this.total_rows = payload.total_rows ?? 0;
			this.posted_docs_count = payload.posted_docs_count ?? 0;
			this.failed_rows_count = payload.failed_rows_count ?? 0;
			this.job_id = payload.job_id ?? null;
			this.stuck_at = payload.stuck_at ?? null;
			this.notes = payload.notes ?? "";
			// UX Gap 1: persist batch_name in localStorage so the hub
			// can resume on page reload. POSTED/REVERSED batches are
			// considered "done" — don't auto-resume those (operator
			// usually wants a fresh batch). STUCK is the one terminal
			// state we DO persist so operator can recover.
			try {
				if (this.batch_name && this.status !== "POSTED" && this.status !== "REVERSED") {
					localStorage.setItem(_LS_KEY, this.batch_name);
				} else {
					localStorage.removeItem(_LS_KEY);
				}
			} catch (e) { /* private mode, ignore */ }
		},

		// UX Gap 1: resume the last in-flight batch from localStorage.
		// Falls back to server-side discovery (find_active_batch) when
		// localStorage is empty (cleared, different browser, incognito)
		// so the operator never loses track of an in-flight migration.
		// Returns true if a batch was loaded, false otherwise.
		async resumeFromStorage() {
			let stored = null;
			try { stored = localStorage.getItem(_LS_KEY); } catch (e) { /* noop */ }
			if (stored) {
				try {
					const data = await _call(`${API}.get_batch`, { batch_name: stored });
					if (data && data.name) {
						this.setBatch(data);
						return true;
					}
				} catch (e) {
					// Stale entry — clear + fall through to server discovery
					try { localStorage.removeItem(_LS_KEY); } catch (e2) { /* noop */ }
				}
			}
			// Server-side discovery: find any in-flight batch on the site
			try {
				const data = await _call(`${API}.find_active_batch`);
				if (data && data.name) {
					this.setBatch(data);
					return true;
				}
			} catch (e) { /* noop */ }
			return false;
		},

		// UX Gap N: while batch is POSTING/REVERSING, the per-doctype
		// row counts only update at the END of the phase. Poll the
		// batch every 5s so the operator sees progress incrementally
		// without manual refresh. Stops automatically on terminal
		// state. Idempotent — safe to call multiple times.
		startProgressPoll() {
			if (this._poll_handle) return;
			// Exponential backoff on consecutive failures. Caps at 30s so
			// poll noise drops dramatically when server is unreachable
			// (transient bench restart, network blip) — operator still
			// gets a recovery probe within 30s. Resets to 5s on success.
			let interval_ms = 5000;
			const MAX_INTERVAL = 30000;
			const tick = async () => {
				if (!this.batch_name) return;
				let ok = false;
				try {
					const [batch_data, live] = await Promise.all([
						_call(`${API}.get_batch`, { batch_name: this.batch_name }),
						_call(`${API}.get_post_progress_live`, { batch_name: this.batch_name }),
					]);
					if (batch_data && batch_data.name) {
						this.setBatch(batch_data);
					}
					if (live) {
						this.live_progress = live;
					}
					_update_tab_title(this, live);
					ok = true;
				} catch (e) { /* swallow — keep polling */ }
				// Re-schedule with exponential backoff on failure
				if (this._poll_handle) {
					clearInterval(this._poll_handle);
					interval_ms = ok ? 5000 : Math.min(MAX_INTERVAL, interval_ms * 2);
					this._poll_handle = setInterval(tick, interval_ms);
				}
				// Auto-stop on terminal state
				if (["POSTED", "REVERSED"].includes(this.status)) {
					this.stopProgressPoll();
				}
			};
			this._poll_handle = setInterval(tick, interval_ms);
			// Also fire once immediately so user sees a fresh state
			tick();
		},
		stopProgressPoll() {
			if (this._poll_handle) {
				clearInterval(this._poll_handle);
				this._poll_handle = null;
			}
		},

		async createBatch(company, batch_title, ob_posting_date, shard_token) {
			this.loading = true;
			try {
				const data = await _call(`${API}.create_batch`, {
					company, batch_title, ob_posting_date,
					shard_token: shard_token || "",
				});
				this.setBatch(data);
			} finally {
				this.loading = false;
			}
		},

		async refreshBatch() {
			if (!this.batch_name) return;
			const data = await _call(`${API}.get_batch`, { batch_name: this.batch_name });
			this.setBatch(data);
		},

		async uploadFile(file, file_type = "Unknown") {
			if (!this.batch_name) {
				throw new Error("Chưa tạo batch.");
			}
			this.loading = true;
			try {
				const fileDoc = await _uploadToFrappe(file, "Misa Migration Batch", this.batch_name, "files");
				const data = await _call(`${API}.attach_file`, {
					batch_name: this.batch_name,
					file_url: fileDoc.file_url,
					file_type: file_type,
					original_filename: file.name,
					size_bytes: file.size,
				});
				this.setBatch(data);
			} finally {
				this.loading = false;
			}
		},

		async updateFileType(file_row_name, file_type) {
			const data = await _call(`${API}.update_file_type`, {
				batch_name: this.batch_name,
				file_row_name,
				file_type,
			});
			this.setBatch(data);
		},

		async removeFile(file_row_name) {
			const data = await _call(`${API}.remove_file`, {
				batch_name: this.batch_name,
				file_row_name,
			});
			this.setBatch(data);
		},

		// --- Phase B: parse / review / post / undo flows ------------------

		async startParse(sync = false) {
			if (!this.batch_name) throw new Error("Chưa có batch");
			await _call(`${PARSE_API}.start_parse`, { batch_name: this.batch_name, sync });
			await this.refreshBatch();
		},

		async getParseProgress() {
			if (!this.batch_name) return null;
			return _call(`${PARSE_API}.get_parse_progress`, { batch_name: this.batch_name });
		},

		async aggregateCounts() {
			if (!this.batch_name) return { counts: {} };
			return _call(`${REVIEW_API}.aggregate_counts`, { batch_name: this.batch_name });
		},

		async listRows({ file_type, status, search, page = 1, limit = 50 } = {}) {
			if (!this.batch_name) return { rows: [], total: 0 };
			return _call(`${REVIEW_API}.list_rows`, {
				batch_name: this.batch_name, file_type, status, search, page, limit,
			});
		},

		async resolveRow(row_name, action, rename_suffix) {
			return _call(`${REVIEW_API}.resolve_row`, {
				batch_name: this.batch_name, row_name, action, rename_suffix,
			});
		},

		async markReviewed() {
			await _call(`${REVIEW_API}.mark_reviewed`, { batch_name: this.batch_name });
			await this.refreshBatch();
		},

		async preflight() {
			return _call(`${POST_API}.preflight`, { batch_name: this.batch_name });
		},

		async startPost(sync = false) {
			await _call(`${POST_API}.start_post`, { batch_name: this.batch_name, sync });
			await this.refreshBatch();
		},

		async startPostBulkFull() {
			// SQL-INSERT pump path — ~140x faster than ORM submit. Bypasses
			// ERPNext validate/hooks. Best for archival historical batches
			// where source data is trusted clean.
			const r = await _call(`${POST_API}.start_post_bulk_full`, {
				batch_name: this.batch_name,
			});
			await this.refreshBatch();
			return r;
		},

		async installMisaCoa() {
			return _call(`${POST_API}.install_misa_coa`, { batch_name: this.batch_name });
		},

		async bootstrapCoaForce() {
			// Wipe non-VN CoA + install VN VAS template. Safe only when 0 GL Entry.
			return _call(
				"vn_accounting.misa_migration.bulk_pump.coa_bootstrap.bootstrap_coa",
				{ company: this.company, template: "vn_large_enterprise", force: 1 },
			);
		},

		async deriveMastersFromBatch() {
			return _call(
				"vn_accounting.misa_migration.scripts.derive_masters_from_batch.derive_masters_for_batch",
				{ batch_name: this.batch_name },
			);
		},

		async refreshCompanyDefaultAccounts() {
			return _call(
				"vn_accounting.misa_migration.bulk_pump.coa_bootstrap.refresh_company_default_accounts",
				{ company: this.company },
			);
		},

		async getPostProgress() {
			return _call(`${POST_API}.get_post_progress`, { batch_name: this.batch_name });
		},

		async startUndo(sync = false, force = false) {
			const r = await _call(`${UNDO_API}.start_undo`, {
				batch_name: this.batch_name, sync, force,
			});
			await this.refreshBatch();
			return r;
		},

		async undoConstraintCheck() {
			return _call(`${UNDO_API}.constraint_check`, { batch_name: this.batch_name });
		},

		async detectDemoData() {
			return _call(`${DEMO_API}.detect_demo_data`, {});
		},

		async wipeDemoData() {
			return _call(`${DEMO_API}.wipe_demo_data`, { confirm: "WIPE-DEMO-DATA" });
		},

		async resumePost(sync = false) {
			const r = await _call(`${RESUME_API}.resume_post`, {
				batch_name: this.batch_name, sync,
			});
			await this.refreshBatch();
			return r;
		},

		async retryFailed(sync = false) {
			const r = await _call(`${RESUME_API}.retry_failed_rows`, {
				batch_name: this.batch_name, sync,
			});
			await this.refreshBatch();
			return r;
		},

		async getFailedRows(limit = 100) {
			return _call(`${RESUME_API}.get_failed_rows`, {
				batch_name: this.batch_name, limit,
			});
		},

		// Pipeline recovery (Item 2) — operator-typed batch name confirms
		async cancelPhase4(confirm_token) {
			return _call(`${POST_API}.cancel_phase_4`, {
				batch_name: this.batch_name,
				confirm_token,
			});
		},

		async deletePhase4(confirm_token) {
			return _call(`${POST_API}.delete_phase_4`, {
				batch_name: this.batch_name,
				confirm_token,
			});
		},
	},
});
