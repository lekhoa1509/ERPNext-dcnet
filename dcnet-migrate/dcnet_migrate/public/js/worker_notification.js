/**
 * Injects a "Tiến trình" (Workers) tab into Frappe's notification panel.
 *
 * Strategy: override frappe.ui.Notifications (before Frappe instantiates it
 * inside setup_notifications()) to add a 4th tab backed by ImportWorkersView.
 *
 * The tab polls get_active_jobs every 3 s while visible, and shows a badge
 * with the count of running jobs on the notification bell icon area.
 */
(function () {
	"use strict";

	// Guard: only extend once even if script is loaded more than once
	if (window._dcnet_worker_panel_ready) return;

	// ---------------------------------------------------------------------------
	// ImportWorkersView — mirrors the BaseNotificationsView API
	// ---------------------------------------------------------------------------
	class ImportWorkersView {
		constructor(wrapper, parent, _settings) {
			this.wrapper = wrapper;
			this.parent = parent;
			this.$container = $("<div></div>").appendTo(this.wrapper);
			this._poll = null;
			this._render_placeholder();
		}

		show() {
			this.$container.show();
			this._start_polling();
		}

		hide() {
			this.$container.hide();
			this._stop_polling();
		}

		// ---- private ----

		_render_placeholder() {
			this.$container.html(
				`<div class="notification-null-state">
					<div class="text-center">
						<div class="title">${__("Đang tải...")}</div>
					</div>
				</div>`
			);
		}

		_start_polling() {
			this._load();
			this._poll = setInterval(() => this._load(), 3000);
		}

		_stop_polling() {
			if (this._poll) {
				clearInterval(this._poll);
				this._poll = null;
			}
		}

		_load() {
			frappe.call({
				method: "dcnet_migrate.import_auto.api.get_active_jobs",
				callback: (r) => {
					const jobs = r.message || [];
					this._render(jobs);
					// Update badge on the tab header
					this._update_badge(jobs.length);
				},
			});
		}

		_update_badge(count) {
			const $badge = this.parent.find(
				".notifications-category#import_workers .worker-count-badge"
			);
			if (count > 0) {
				$badge.text(count).show();
			} else {
				$badge.hide();
			}
		}

		_render(jobs) {
			if (!jobs.length) {
				this.$container.html(
					`<div class="notification-null-state">
						<div class="text-center">
							<div style="font-size:1.8rem;margin-bottom:8px">✓</div>
							<div class="title">${__("Không có tiến trình nào")}</div>
							<div class="subtitle">${__("Tất cả tác vụ đã hoàn thành.")}</div>
						</div>
					</div>`
				);
				return;
			}

			const html = jobs.map((job) => this._job_html(job)).join("");
			this.$container.html(html);

			this.$container.find(".worker-cancel-btn").on("click", (e) => {
				e.stopPropagation();
				const jobId = $(e.currentTarget).data("job-id");
				this._cancel(jobId, $(e.currentTarget).closest(".worker-item"));
			});
		}

		_job_html(job) {
			const pct = Math.max(0, Math.min(100, job.percent || 0));
			const subtitle = [job.message, job.current_file]
				.filter(Boolean)
				.map((s) => frappe.utils.escape_html(s))
				.join(" · ");

			const progress_html =
				pct > 0
					? `<div class="worker-bar-wrap">
						<div class="worker-bar-track">
							<div class="worker-bar" style="width:${pct}%"></div>
						</div>
						<span class="worker-pct">${pct}%</span>
					</div>`
					: `<div class="worker-bar-wrap">
						<div class="worker-bar-track">
							<div class="worker-bar worker-bar--indeterminate"></div>
						</div>
						<span class="worker-pct">...</span>
					</div>`;

			return `
				<div class="worker-item recent-item" data-job-id="${frappe.utils.escape_html(job.job_id)}">
					<div class="worker-body">
						<div class="worker-icon">${job.icon || "⚙️"}</div>
						<div class="worker-info">
							<div class="worker-type">${frappe.utils.escape_html(job.type_label)}</div>
							<div class="worker-doc text-muted">${frappe.utils.escape_html(job.label || job.docname)}</div>
							${subtitle ? `<div class="worker-subtext text-muted">${subtitle}</div>` : ""}
							${progress_html}
						</div>
						<button
							class="worker-cancel-btn btn-reset"
							data-job-id="${frappe.utils.escape_html(job.job_id)}"
							title="${__("Hủy tiến trình")}"
						>${frappe.utils.icon("x", "xs")}</button>
					</div>
				</div>`;
		}

		_cancel(jobId, $item) {
			frappe.confirm(__("Hủy tiến trình này?"), () => {
				frappe.call({
					method: "dcnet_migrate.import_auto.api.cancel_import_job",
					args: { job_id: jobId },
					callback: (r) => {
						if (r.message && r.message.success) {
							$item.fadeOut(250, () => {
								$item.remove();
								this._update_badge(this.$container.find(".worker-item").length);
							});
							frappe.show_alert({ message: __("Đã hủy tiến trình"), indicator: "green" });
						} else {
							const msg = (r.message && r.message.error) || __("Không thể hủy");
							frappe.show_alert({ message: msg, indicator: "red" });
						}
					},
				});
			});
		}
	}

	// ---------------------------------------------------------------------------
	// Extend frappe.ui.Notifications
	// ---------------------------------------------------------------------------
	function extend_notifications() {
		if (!frappe || !frappe.ui || !frappe.ui.Notifications) {
			setTimeout(extend_notifications, 100);
			return;
		}

		const _Original = frappe.ui.Notifications;

		frappe.ui.Notifications = class extends _Original {
			setup_headers() {
				// Inject the workers panel div BEFORE parent sets up categories
				// (this.body is already set by make() at this point)
				this.panel_workers = $('<div class="panel-workers"></div>').appendTo(
					this.body
				);

				super.setup_headers();

				this._add_workers_tab();
			}

			_add_workers_tab() {
				const category = {
					label: __("Tiến trình"),
					id: "import_workers",
					view: ImportWorkersView,
					el: this.panel_workers,
				};

				this.categories.push(category);

				// Create tab header and append to existing nav
				const $nav = this.dropdown_list.find(".notification-item-tabs");
				category.$tab = $(
					`<li class="notifications-category" id="import_workers">
						${category.label}
						<span class="worker-count-badge" style="display:none"></span>
					</li>`
				);
				category.$tab.on("click", (e) => {
					e.stopImmediatePropagation();
					this.switch_tab(category);
				});
				$nav.append(category.$tab);

				// Instantiate view
				const view = new ImportWorkersView(
					category.el,
					this.dropdown,
					this.notification_settings
				);
				this.tabs[category.id] = view;

				// Refresh badge whenever the panel opens
				this.dropdown.on("show.bs.dropdown", () => {
					this._refresh_workers_badge();
				});
			}

			_refresh_workers_badge() {
				frappe.call({
					method: "dcnet_migrate.import_auto.api.get_active_jobs",
					callback: (r) => {
						const count = (r.message || []).length;
						const $badge = this.dropdown_list.find(
							".notifications-category#import_workers .worker-count-badge"
						);
						if (count > 0) {
							$badge.text(count).show();
						} else {
							$badge.hide();
						}
					},
				});
			}
		};

		window._dcnet_worker_panel_ready = true;
	}

	extend_notifications();
})();
