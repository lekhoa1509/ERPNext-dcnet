(function () {
	if (window.__DCNET_PERMISSION_MANAGER__) {
		return;
	}
	window.__DCNET_PERMISSION_MANAGER__ = true;

	const API = {
		dashboard: "dcnet_permission.api.dashboard",
		saveUser: "dcnet_permission.api.save_user",
		disableUser: "dcnet_permission.api.disable_user",
		revokeDeptAccess: "dcnet_permission.api.revoke_dept_access",
		getUserPermissions: "dcnet_permission.api.get_user_permission_matrix",
		saveUserPermissions: "dcnet_permission.api.save_user_permission_matrix",
		getModulePermissions: "dcnet_permission.api.get_module_permissions",
		saveModulePermissions: "dcnet_permission.api.save_module_permissions",
	};

	frappe.pages["dcnet-permission-manager"].on_page_load = function (wrapper) {
		const page = frappe.ui.make_app_page({
			parent: wrapper,
			title: __("Department Permissions"),
			single_column: true,
		});

		const manager = new DCNETPermissionManager(page);
		manager.init();
	};

	class DCNETPermissionManager {
		constructor(page) {
			this.page = page;
			this.state = {
				dashboard: null,
				department: "",
				query: "",
				status: "enabled",
				activeTab: "users",
				modulePermissions: null,
				moduleDraft: {},
				moduleQuery: "",
			};
		}

		init() {
			this.page.main.addClass("dcnet-permission-page");
			this.page.set_primary_action(__("Create User"), () => this.openForm(), "add");
			this.page.set_secondary_action(__("Refresh"), () => this.load(), "refresh");
			this.renderShell();
			this.load();
		}

		renderShell() {
			this.page.main.html(`
				<div class="dpm-root">
					<section class="dpm-stats" aria-live="polite"></section>

					<div class="dpm-layout">
						<aside class="dpm-sidebar">
							<div class="dpm-sidebar-head">
								<span class="dpm-sidebar-title">${__("Departments")}</span>
								<span class="dpm-sidebar-count">0</span>
							</div>
							<div class="dpm-sidebar-search">
								<input class="dpm-sidebar-search-input" type="search" placeholder="${__("Search...")}" />
							</div>
							<div class="dpm-scopes"></div>
						</aside>

						<main class="dpm-main">
							<div class="dpm-main-body"></div>
						</main>
					</div>
				</div>
			`);
		}

		load() {
			this.page.main.addClass("dpm-loading");
			frappe.call({
				method: API.dashboard,
				freeze: true,
				callback: (response) => {
					this.state.dashboard = response.message || {};
					const initialDepartment =
						this.departmentList().find((department) => department.is_configured)?.name ||
						this.departmentList()[0]?.name;
					if (!this.state.department && initialDepartment) {
						this.state.department = initialDepartment;
					}
					this.render();
				},
				always: () => {
					this.page.main.removeClass("dpm-loading");
				},
			});
		}

		render() {
			this.renderStats();
			this.renderScopes();
			this.renderUsers();
		}

		renderStats() {
			const stats = this.state.dashboard?.stats || {};
			const cards = [
				{
					label: __("Departments"),
					value: stats.departments || 0,
					iconBg: "#f0fdfa",
					iconColor: "#0f766e",
					icon: '<path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/>',
				},
				{
					label: __("Managed Users"),
					value: stats.users || 0,
					iconBg: "#eff6ff",
					iconColor: "#2563eb",
					icon: '<path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/>',
				},
				{
					label: __("Active"),
					value: stats.enabled_users || 0,
					iconBg: "#f0fdf4",
					iconColor: "#16a34a",
					icon: '<path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>',
				},
				{
					label: __("Permission Items"),
					value: stats.permission_items || 0,
					iconBg: "#fff7ed",
					iconColor: "#ea580c",
					icon: '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/>',
				},
			];

			this.page.main.find(".dpm-stats").html(
				cards
					.map(
						(card) => `
							<div class="dpm-stat-card">
								<div class="dpm-stat-icon" style="background:${card.iconBg}">
									<svg viewBox="0 0 24 24" fill="none" stroke="${card.iconColor}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${card.icon}</svg>
								</div>
								<div class="dpm-stat-body">
									<div class="dpm-stat-value">${frappe.utils.escape_html(String(card.value))}</div>
									<div class="dpm-stat-label">${card.label}</div>
								</div>
							</div>
						`
					)
					.join("")
			);
		}

		renderScopes() {
			const departments = this.departmentList();

			if (!departments.length) {
				this.page.main.find(".dpm-scopes").html(`
					<div class="dpm-empty">
						<strong>${__("No Departments")}</strong>
						<span>${__("No Department records found.")}</span>
					</div>
				`);
				return;
			}

			this.page.main.find(".dpm-scopes").html(
				departments
					.map((department) => {
						const active = department.name === this.state.department ? "is-active" : "";
						const roles = this.rolesForDepartment(department.name);
						const extraProfiles = this.extraProfilesForDepartment(department.name);
						const metaParts = [roles.length ? `${roles.length} ${__("roles")}` : __("Not Configured")];
						if (extraProfiles.length) {
							metaParts.push(`+${extraProfiles.length} ${__("profiles")}`);
						}
						const meta = metaParts.join(" · ");
						const userCount = (this.state.dashboard?.users || []).filter(
							(u) => (u.departments || [u.department]).includes(department.name) && u.enabled
						).length;
						const badge = userCount
							? `<span class="dpm-scope-badge">${userCount}</span>`
							: "";
						return `
							<button class="dpm-scope ${active}" data-department="${frappe.utils.escape_html(department.name)}">
								<div class="dpm-scope-header">
									<span class="dpm-scope-name">${frappe.utils.escape_html(department.name)}</span>
									${badge}
								</div>
								<span class="dpm-scope-meta">${frappe.utils.escape_html(meta)}</span>
							</button>
						`;
					})
					.join("")
			);

			this.page.main.find(".dpm-scope").on("click", (event) => {
				const newDept = event.currentTarget.dataset.department;
				if (newDept !== this.state.department) {
					this.state.modulePermissions = null;
					this.state.moduleDraft = {};
					this.state.moduleQuery = "";
				}
				this.state.department = newDept;
				this.renderScopes();
				this.renderUsers();
			});

			this.page.main.find(".dpm-sidebar-count").text(departments.length);

			this.page.main.find(".dpm-sidebar-search-input").on("input", (event) => {
				const query = (event.target.value || "").trim().toLowerCase();
				this.page.main.find(".dpm-scope").each((_i, el) => {
					const name = (el.dataset.department || "").toLowerCase();
					el.style.display = !query || name.includes(query) ? "" : "none";
				});
			});
		}

		renderUsers() {
			const body = this.page.main.find(".dpm-main-body");
			const dept = this.state.department;
			const userCount = (this.state.dashboard?.users || []).filter((u) => (u.departments || [u.department]).includes(dept)).length;
			const countBadge = dept ? `<span class="dpm-dept-count">${userCount} ${__("users")}</span>` : "";
			const isModulesTab = this.state.activeTab === "modules";

			const tabBar = `
				<div class="dpm-tab-bar">
					<button class="dpm-tab ${!isModulesTab ? "is-active" : ""}" data-tab="users">${__("Người dùng")}</button>
					<button class="dpm-tab ${isModulesTab ? "is-active" : ""}" data-tab="modules">${__("Phân quyền Module")}</button>
				</div>
			`;

			const userControls = `
				<div class="dpm-search-wrap">
					<input class="dpm-search form-control" type="search" placeholder="${__("Search user, email, role")}" value="${frappe.utils.escape_html(this.state.query)}" />
				</div>
				<select class="dpm-status form-control">
					<option value="enabled">${__("Active")}</option>
					<option value="disabled">${__("Disabled")}</option>
					<option value="all">${__("All")}</option>
				</select>
			`;

			const moduleControls = `
				<div class="dpm-search-wrap">
					<input class="dpm-module-search form-control" type="search" placeholder="${__("Search module...")}" value="${frappe.utils.escape_html(this.state.moduleQuery)}" />
				</div>
			`;

			body.html(`
				<div class="dpm-toolbar">
					<span class="dpm-dept-label">${frappe.utils.escape_html(dept || __("Select a department"))}</span>
					${countBadge}
					${tabBar}
					<div class="dpm-toolbar-gap"></div>
					${isModulesTab ? moduleControls : userControls}
				</div>
				<div class="dpm-users${isModulesTab ? " dpm-hidden" : ""}"></div>
				<div class="dpm-module-panel${!isModulesTab ? " dpm-hidden" : ""}"></div>
			`);

			body.find(".dpm-tab").on("click", (event) => {
				const tab = event.currentTarget.dataset.tab;
				if (tab !== this.state.activeTab) {
					this.state.activeTab = tab;
					this.renderUsers();
				}
			});

			if (isModulesTab) {
				body.find(".dpm-module-search").on("input", (event) => {
					this.state.moduleQuery = (event.target.value || "").trim().toLowerCase();
					this.renderModuleCards();
				});
				this.loadAndRenderModulePermissions();
			} else {
				body.find(".dpm-status").val(this.state.status);
				body.find(".dpm-search").on("input", (event) => {
					this.state.query = event.target.value || "";
					this.renderUserRows();
				});
				body.find(".dpm-status").on("change", (event) => {
					this.state.status = event.target.value || "enabled";
					this.renderUserRows();
				});
				this.renderUserRows();
			}
		}

		loadAndRenderModulePermissions() {
			const panel = this.page.main.find(".dpm-module-panel");

			if (!this.state.department) {
				panel.html(`
					<div class="dpm-empty dpm-empty-large">
						<div class="dpm-empty-icon">${frappe.utils.icon("grid", "xl")}</div>
						<strong>${__("No Department Selected")}</strong>
						<span>${__("Select a department from the sidebar to configure module access.")}</span>
					</div>
				`);
				return;
			}

			if (this.state.modulePermissions) {
				this.renderModulePanel();
				return;
			}

			panel.html(`<div class="dpm-module-loading"><span class="dpm-spinner"></span>&ensp;${__("Loading modules...")}</div>`);

			frappe.call({
				method: API.getModulePermissions,
				args: { department: this.state.department },
				callback: (r) => {
					this.state.modulePermissions = r.message || { modules: [], user_count: 0 };
					this.state.moduleDraft = {};
					this.renderModulePanel();
				},
				error: () => {
					panel.html(`
						<div class="dpm-empty dpm-empty-large">
							<strong>${__("Error")}</strong>
							<span>${__("Failed to load module permissions.")}</span>
						</div>
					`);
				},
			});
		}

		renderModulePanel() {
			const panel = this.page.main.find(".dpm-module-panel");
			const data = this.state.modulePermissions;
			const userCount = data?.user_count || 0;
			const blockedCount = (data?.modules || []).filter((m) => {
				const draft = this.state.moduleDraft;
				return draft.hasOwnProperty(m.name) ? draft[m.name] : m.blocked;
			}).length;

			panel.html(`
				<div class="dpm-module-summary">
					<div class="dpm-module-summary-info">
						<span class="dpm-module-summary-text">${__("Applied to {0} users · {1} modules blocked", [userCount, blockedCount])}</span>
					</div>
					<div class="dpm-toolbar-gap"></div>
					<button class="dpm-save-modules-btn dpm-action-primary-btn">
						${frappe.utils.icon("check", "xs")}&ensp;${__("Lưu thay đổi")}
					</button>
				</div>
				<div class="dpm-module-groups-wrap">
					<div class="dpm-module-groups"></div>
				</div>
			`);

			panel.find(".dpm-save-modules-btn").on("click", () => this.saveModulePermissions());
			this.renderModuleCards();
		}

		renderModuleCards() {
			const data = this.state.modulePermissions;
			const container = this.page.main.find(".dpm-module-groups");
			if (!data || !container.length) return;

			const query = (this.state.moduleQuery || "").trim().toLowerCase();
			const modules = (data.modules || []).filter(
				(m) => !query || m.name.toLowerCase().includes(query) || (m.label || "").toLowerCase().includes(query)
			);

			if (!modules.length) {
				container.html(`
					<div class="dpm-empty dpm-empty-large">
						<strong>${__("No Modules Found")}</strong>
						<span>${__("No modules match your search.")}</span>
					</div>
				`);
				return;
			}

			const grouped = {};
			modules.forEach((m) => {
				const key = m.app_label || m.app || __("Other");
				grouped[key] = grouped[key] || [];
				grouped[key].push(m);
			});

			container.html(
				Object.entries(grouped)
					.map(
						([appLabel, items]) => `
					<div class="dpm-module-group">
						<div class="dpm-module-group-header">${frappe.utils.escape_html(appLabel)}</div>
						<div class="dpm-module-list">
							${items.map((m) => this.renderModuleItem(m)).join("")}
						</div>
					</div>
				`
					)
					.join("")
			);

			container.find(".dpm-module-toggle-input").on("change", (event) => {
				const moduleName = event.currentTarget.dataset.module;
				const isAllowed = event.currentTarget.checked;
				this.state.moduleDraft[moduleName] = !isAllowed;
				const row = $(event.currentTarget).closest(".dpm-module-item");
				row.toggleClass("is-blocked", !isAllowed);
				this.updateModuleSummaryCount();
			});
		}

		renderModuleItem(m) {
			const draft = this.state.moduleDraft;
			const isBlocked = draft.hasOwnProperty(m.name) ? draft[m.name] : m.blocked;
			const isPartial = !draft.hasOwnProperty(m.name) && m.partial;
			const cls = ["dpm-module-item", isBlocked ? "is-blocked" : "", isPartial ? "is-partial" : ""].filter(Boolean).join(" ");

			return `
				<div class="${cls}">
					<div class="dpm-module-item-info">
						<span class="dpm-module-item-label">${frappe.utils.escape_html(m.label || m.name)}</span>
						<span class="dpm-module-item-sub">${frappe.utils.escape_html(m.name)}</span>
					</div>
					${isPartial && !draft.hasOwnProperty(m.name) ? `<span class="dpm-module-partial-tag" title="${__("Some users have this module blocked")}">${__("Mixed")}</span>` : ""}
					<label class="dpm-toggle" title="${frappe.utils.escape_html(isBlocked ? __("Blocked — click to allow") : __("Allowed — click to block"))}">
						<input type="checkbox" class="dpm-module-toggle-input" data-module="${frappe.utils.escape_html(m.name)}" ${!isBlocked ? "checked" : ""} />
						<span class="dpm-toggle-track"></span>
					</label>
				</div>
			`;
		}

		updateModuleSummaryCount() {
			const data = this.state.modulePermissions;
			if (!data) return;
			const blockedCount = (data.modules || []).filter((m) => {
				const draft = this.state.moduleDraft;
				return draft.hasOwnProperty(m.name) ? draft[m.name] : m.blocked;
			}).length;
			this.page.main.find(".dpm-module-summary-text").text(
				__("Applied to {0} users · {1} modules blocked", [data.user_count || 0, blockedCount])
			);
		}

		saveModulePermissions() {
			const data = this.state.modulePermissions;
			if (!data) return;

			const blockedModules = (data.modules || [])
				.filter((m) => {
					const draft = this.state.moduleDraft;
					return draft.hasOwnProperty(m.name) ? draft[m.name] : m.blocked;
				})
				.map((m) => m.name);

			const saveBtn = this.page.main.find(".dpm-save-modules-btn");
			const originalHtml = saveBtn.html();
			saveBtn.prop("disabled", true).html(`<span class="dpm-btn-spinner" aria-hidden="true"></span>${frappe.utils.escape_html(__("Saving..."))}`);

			frappe.call({
				method: API.saveModulePermissions,
				args: {
					data: JSON.stringify({
						department: this.state.department,
						blocked_modules: blockedModules,
					}),
				},
				callback: (r) => {
					const result = r.message || {};
					this.state.modulePermissions = result;
					this.state.moduleDraft = {};
					const reloadedCount = (result.reloaded_users || []).length;
					const msg = reloadedCount > 0
						? __("Module permissions saved. {0} user(s) will reload automatically.", [reloadedCount])
						: __("Module permissions saved. Users must refresh their browser to see changes.");
					frappe.show_alert({ message: msg, indicator: "green" }, 6);
					this.renderModulePanel();
				},
				always: () => {
					saveBtn.prop("disabled", false).html(originalHtml);
				},
			});
		}

		renderUserRows() {
			const users = this.filteredUsers();
			const currentDepartment = this.state.department;
			const usersWrapper = this.page.main.find(".dpm-users");

			if (!currentDepartment) {
				usersWrapper.html(`
					<div class="dpm-empty dpm-empty-large">
						<div class="dpm-empty-icon">${frappe.utils.icon("shield", "xl")}</div>
						<strong>${__("No Data")}</strong>
						<span>${__("No department scope is assigned to you.")}</span>
					</div>
				`);
				return;
			}

			if (!users.length) {
				usersWrapper.html(`
					<div class="dpm-empty dpm-empty-large">
						<div class="dpm-empty-icon">${frappe.utils.icon("users", "xl")}</div>
						<strong>${__("No Matching Users")}</strong>
						<span>${__("Create a new user or change filters.")}</span>
					</div>
				`);
				return;
			}

			const rows = users
				.map((user) => {
					const statusClass = user.enabled ? "is-enabled" : "is-disabled";
					const statusLabel = user.enabled ? __("Active") : __("Disabled");
					const colorIdx = this.avatarColorIndex(user);
					const rolesHtml = this.renderUserRoleChips(user);

					return `
						<tr>
							<td>
								<div class="dpm-user">
									<div class="dpm-avatar dpm-avatar--${colorIdx}">${this.initials(user)}</div>
									<div>
										<div class="dpm-user-name">${frappe.utils.escape_html(user.full_name || user.email)}</div>
										<div class="dpm-user-email">${frappe.utils.escape_html(user.email || user.name)}</div>
									</div>
								</div>
							</td>
							<td>
								<span class="dpm-status-pill ${statusClass}">
									<span class="dpm-status-dot"></span>${statusLabel}
								</span>
							</td>
							<td><div class="dpm-role-list">${rolesHtml}</div></td>
							<td class="dpm-actions">
								<button class="dpm-action-primary-btn dpm-edit-permissions" data-user="${frappe.utils.escape_html(user.name)}">
									${frappe.utils.icon("lock", "xs")} ${__("Permissions")}
								</button>
								<button class="dpm-action-icon-btn dpm-edit" data-user="${frappe.utils.escape_html(user.name)}" title="${__("Edit User")}">
									${frappe.utils.icon("edit", "xs")}
								</button>
								<div class="dropdown dpm-row-menu">
									<button class="dpm-action-icon-btn dropdown-toggle" data-toggle="dropdown" title="${__("More")}">
										${frappe.utils.icon("dot-horizontal", "xs")}
									</button>
									<ul class="dropdown-menu dropdown-menu-right">
										<li><a class="dpm-revoke-dept text-danger" data-user="${frappe.utils.escape_html(user.name)}">${__("Khóa quyền phòng")}</a></li>
									</ul>
								</div>
							</td>
						</tr>
					`;
				})
				.join("");

			const allInDept = (this.state.dashboard?.users || []).filter((u) => (u.departments || [u.department]).includes(currentDepartment));

			usersWrapper.html(`
				<div class="dpm-table-wrap">
					<table class="table dpm-table">
						<thead>
							<tr>
								<th>${__("User")}</th>
								<th>${__("Status")}</th>
								<th>${__("Roles")}</th>
								<th></th>
							</tr>
						</thead>
						<tbody>${rows}</tbody>
					</table>
				</div>
				<div class="dpm-table-footer">
					<span class="dpm-footer-count">${__("{0} / {1} users", [users.length, allInDept.length])}</span>
					<span class="dpm-footer-note">${frappe.utils.escape_html(currentDepartment)}</span>
				</div>
			`);

			usersWrapper.find(".dpm-edit-permissions").on("click", (event) => {
				this.openUserPermissions(event.currentTarget.dataset.user, this.state.department);
			});
			usersWrapper.find(".dpm-edit").on("click", (event) => {
				event.preventDefault();
				const user = this.findUser(event.currentTarget.dataset.user);
				this.openForm(user);
			});
			usersWrapper.find(".dpm-revoke-dept").on("click", (event) => {
				event.preventDefault();
				this.revokeDeptAccess(event.currentTarget.dataset.user, this.state.department);
			});
		}

		renderUserRoleChips(user) {
			if (user.permission_mode === "user") {
				return `<span class="dpm-role-tag dpm-role-tag--primary">${__("Custom Permissions")}</span>`;
			}

			const roles = user.roles || [];
			if (!roles.length) {
				return `<span class="dpm-muted">${__("No scoped roles")}</span>`;
			}

			const maxVisible = 2;
			const visible = roles.slice(0, maxVisible);
			const overflow = roles.length - maxVisible;

			const chips = visible
				.map((role, i) => `<span class="dpm-role-tag ${i === 0 ? "dpm-role-tag--primary" : ""}">${frappe.utils.escape_html(role)}</span>`)
				.join("");
			const overflowChip = overflow > 0 ? `<span class="dpm-role-tag dpm-role-tag--more">+${overflow}</span>` : "";

			return chips + overflowChip;
		}

		renderEmployeeCell(user) {
			if (!user.employee) {
				return `<div class="dpm-muted">${__("Not linked")}</div>`;
			}

			const status = user.employee_status ? ` · ${frappe.utils.escape_html(__(user.employee_status))}` : "";
			return `
				<div class="dpm-employee">
					<strong>${frappe.utils.escape_html(user.employee_name || user.employee)}</strong>
					<span>${frappe.utils.escape_html(user.employee)}${status}</span>
				</div>
			`;
		}

		openUserPermissions(userName, department) {
			frappe.call({
				method: API.getUserPermissions,
				args: { user: userName, department: department || "" },
				freeze: true,
				callback: (response) => {
					const data = response.message || {};
					const user = data.user || {};
					const dialog = new frappe.ui.Dialog({
						title: __("Edit Permissions: {0}", [user.full_name || user.email || userName]),
						size: "extra-large",
						fields: [{ fieldtype: "HTML", fieldname: "permissions_html" }],
						primary_action_label: __("Save Permissions"),
						primary_action: () => this.saveUserPermissions(dialog, data),
					});
					dialog.show();
					dialog.$wrapper.addClass("dpm-permission-dialog");
					this.renderUserPermissionMatrix(dialog, data);
				},
			});
		}

		renderUserPermissionMatrix(dialog, data) {
			const wrapper = dialog.fields_dict.permissions_html.$wrapper;
			const grouped = this.groupPermissionItems(data.items || []);
			const groupNames = Object.keys(grouped);
			const columns = data.columns || [];
			const source = data.source_roles?.length ? data.source_roles.join(", ") : __("No Base Permissions");
			dialog.get_primary_btn().prop("disabled", !groupNames.length);

			wrapper.html(`
				<div class="dpm-user-permission-summary">
					<div>
						<div class="dpm-panel-title">${frappe.utils.escape_html(data.user?.full_name || data.user?.email || "")}</div>
						<div class="dpm-muted">${frappe.utils.escape_html(data.department || "")} · ${__("Current Permission Source")}: ${frappe.utils.escape_html(source)}</div>
					</div>
					<span class="dpm-status-pill ${data.mode === "user" ? "is-enabled" : "is-neutral"}">${data.mode === "user" ? __("Custom") : __("By Role")}</span>
				</div>
				${
					groupNames.length
						? `<div class="dpm-permission-grid">
							${groupNames.map((group) => this.renderPermissionGroup(group, grouped[group], columns, data.permissions || {})).join("")}
						</div>`
						: `<div class="dpm-empty dpm-empty-large">
							<strong>${__("No Permission Catalog")}</strong>
							<span>${__("This department has no business permission catalog configured.")}</span>
						</div>`
				}
				<div class="dpm-dialog-saving" hidden>
					<div class="dpm-saving-card" role="status" aria-live="assertive">
						<span class="dpm-spinner" aria-hidden="true"></span>
						<span class="dpm-dialog-saving-text">${__("Saving user permissions...")}</span>
					</div>
				</div>
			`);

			wrapper.find(".dpm-perm-check").on("change", (event) => this.onUserPermissionChange(event, data, wrapper));
		}

		renderPermissionGroup(group, items, columns, permissionsByKey) {
			return `
				<section class="dpm-permission-group">
					<div class="dpm-permission-group-title">${frappe.utils.escape_html(__(group))}</div>
					<div class="dpm-table-wrap">
						<table class="table dpm-table dpm-permission-table">
							<thead>
								<tr>
									<th>${__("Module")}</th>
									${columns.map((column) => `<th>${frappe.utils.escape_html(__(column.label))}</th>`).join("")}
								</tr>
							</thead>
							<tbody>
								${items.map((item) => this.renderPermissionRow(item, columns, permissionsByKey)).join("")}
							</tbody>
						</table>
					</div>
				</section>
			`;
		}

		renderPermissionRow(item, columns, permissionsByKey) {
			const permissions = permissionsByKey[item.key] || {};
			const allowed = new Set(item.permission_fields || []);
			return `
				<tr>
					<td>
						<div class="dpm-permission-item">
							<strong>${frappe.utils.escape_html(__(item.label))}</strong>
							<span>${frappe.utils.escape_html(item.name)}${item.ref_doctype ? ` · ${frappe.utils.escape_html(item.ref_doctype)}` : ""}</span>
						</div>
					</td>
					${columns
						.map((column) => {
							const isAllowed = allowed.has(column.key);
							const checked = permissions[column.key] ? "checked" : "";
							const disabled = isAllowed ? "" : "disabled";
							const ariaLabel = __("{0}: {1}", [__(column.label), __(item.label)]);
							return `
								<td>
									<label class="dpm-perm-cell ${isAllowed ? "" : "is-disabled"}" title="${frappe.utils.escape_html(ariaLabel)}">
										<input class="dpm-perm-check" type="checkbox" aria-label="${frappe.utils.escape_html(ariaLabel)}" data-key="${frappe.utils.escape_html(item.key)}" data-permission="${frappe.utils.escape_html(column.key)}" ${checked} ${disabled} />
										<span class="dpm-perm-box" aria-hidden="true"></span>
									</label>
								</td>
							`;
						})
						.join("")}
				</tr>
			`;
		}

		onUserPermissionChange(event, data, wrapper) {
			const input = event.currentTarget;
			const key = input.dataset.key;
			const permission = input.dataset.permission;
			data.permissions[key] = { ...(data.permissions[key] || {}) };
			data.permissions[key][permission] = input.checked ? 1 : 0;

			if (input.checked && permission !== "read") {
				data.permissions[key].read = 1;
				wrapper.find(`.dpm-perm-check[data-key="${this.escapeSelectorValue(key)}"][data-permission="read"]`).prop("checked", true);
			}
			if (permission === "read" && !input.checked) {
				Object.keys(data.permissions[key]).forEach((field) => {
					data.permissions[key][field] = 0;
				});
				wrapper.find(`.dpm-perm-check[data-key="${this.escapeSelectorValue(key)}"]`).prop("checked", false);
			}
		}

		saveUserPermissions(dialog, data) {
			const entries = (data.items || []).map((item) => ({
				key: item.key,
				permissions: data.permissions?.[item.key] || {},
			}));

			this.setPermissionDialogSaving(dialog, true, __("Saving user permissions..."));
			frappe.call({
				method: API.saveUserPermissions,
				args: {
					data: JSON.stringify({
						user: data.user?.name,
						department: data.department || "",
						entries,
					}),
				},
				callback: (response) => {
					dialog.hide();
					this.state.dashboard = response.message || this.state.dashboard;
					frappe.show_alert({ message: __("Custom user permissions saved"), indicator: "green" }, 4);
					this.render();
				},
				always: () => {
					this.setPermissionDialogSaving(dialog, false);
				},
			});
		}

		setPermissionDialogSaving(dialog, isSaving, message) {
			if (!dialog?.$wrapper) {
				return;
			}

			const primaryButton = dialog.get_primary_btn();
			const label = message || __("Processing...");
			dialog.$wrapper.toggleClass("dpm-is-saving", !!isSaving);
			dialog.$wrapper.find(".dpm-dialog-saving").prop("hidden", !isSaving);
			dialog.$wrapper.find(".dpm-dialog-saving-text").text(label);
			dialog.$wrapper.find(".modal-header .close, .modal-header .btn-modal-close").prop("disabled", !!isSaving);

			if (!primaryButton?.length) {
				return;
			}

			if (isSaving) {
				if (!primaryButton.data("dpm-original-html")) {
					primaryButton.data("dpm-original-html", primaryButton.html());
				}
				primaryButton
					.prop("disabled", true)
					.addClass("dpm-btn-loading")
					.html(`<span class="dpm-btn-spinner" aria-hidden="true"></span>${frappe.utils.escape_html(label)}`);
				return;
			}

			const originalHtml = primaryButton.data("dpm-original-html");
			primaryButton
				.prop("disabled", false)
				.removeClass("dpm-btn-loading")
				.html(originalHtml || __("Save Permissions"))
				.removeData("dpm-original-html");
		}

		openForm(user) {
			const isEdit = !!user;
			const department = user?.department || this.state.department || this.state.dashboard?.departments?.[0] || "";
			const roles = this.rolesForDepartment(department);
			const selectedRoles = new Set(user?.roles || roles.filter((role) => this.isDefaultRole(department, role)));
			const departmentOptions = this.departmentList().map((item) => item.name);
			const employeeOptions = this.employeeOptionsForDepartment(department, user?.employee, user?.email || user?.name);
			const hasEmployeeDoctype = !!this.state.dashboard?.has_employee_doctype;

			if (!isEdit && !roles.length) {
				frappe.msgprint({
					title: __("Scope Not Configured"),
					message: __("This department exists but has no DCNET Permission Scope for role assignment."),
					indicator: "orange",
				});
				return;
			}

			let dialog;
			dialog = new frappe.ui.Dialog({
				title: isEdit ? __("Edit User") : __("Create User"),
				fields: [
					{
						fieldtype: "Data",
						fieldname: "email",
						label: __("Email"),
						reqd: 1,
						default: user?.email || "",
						read_only: isEdit ? 1 : 0,
						change: () => this.refreshEmployeeOptions(dialog),
					},
					{ fieldtype: "Data", fieldname: "first_name", label: __("First Name"), reqd: 1, default: user?.first_name || "" },
					{ fieldtype: "Data", fieldname: "last_name", label: __("Last Name"), default: user?.last_name || "" },
					{ fieldtype: "Column Break" },
					{
						fieldtype: "Select",
						fieldname: "department",
						label: __("Department"),
						reqd: 1,
						options: departmentOptions.join("\n"),
						default: department,
						change: () => {
							this.refreshRoleChecklist(dialog);
							this.refreshEmployeeOptions(dialog);
						},
					},
					{ fieldtype: "Check", fieldname: "enabled", label: __("Active"), default: user ? user.enabled : 1 },
					...(isEdit
						? []
						: [
								{
									fieldtype: "HTML",
									fieldname: "initial_password_html",
									options: `<div class="dpm-password-note">${__("Default Password")}: <strong>123456</strong>. ${__("User must change password on first login.")}</div>`,
								},
							]),
					...(hasEmployeeDoctype
						? [
								{ fieldtype: "Section Break", label: __("Employee") },
								{
									fieldtype: "Select",
									fieldname: "employee",
									label: __("Employee"),
									options: employeeOptions.join("\n"),
									default: user?.employee || "",
									change: () => this.renderEmployeeHint(dialog),
								},
								{ fieldtype: "HTML", fieldname: "employee_hint_html" },
							]
						: []),
					{ fieldtype: "Section Break", label: __("Role") },
					{ fieldtype: "HTML", fieldname: "roles_html" },
				],
				primary_action_label: isEdit ? __("Save Changes") : __("Create User"),
				primary_action: () => this.saveUser(dialog),
			});

			dialog.show();
			this.renderRoleChecklist(dialog, roles, selectedRoles);
			this.renderEmployeeHint(dialog);
		}

		refreshRoleChecklist(dialog) {
			const values = dialog.get_values(true) || {};
			const department = values.department;
			const roles = this.rolesForDepartment(department);
			const selectedRoles = new Set(roles.filter((role) => this.isDefaultRole(department, role)));
			this.renderRoleChecklist(dialog, roles, selectedRoles);
		}

		refreshEmployeeOptions(dialog) {
			if (!dialog.fields_dict.employee) {
				return;
			}

			const values = dialog.get_values(true) || {};
			const options = this.employeeOptionsForDepartment(values.department, values.employee, values.email);
			dialog.set_df_property("employee", "options", options.join("\n"));
			if (values.employee && !options.includes(values.employee)) {
				dialog.set_value("employee", "");
			}
			this.renderEmployeeHint(dialog);
		}

		renderEmployeeHint(dialog) {
			if (!dialog.fields_dict.employee_hint_html) {
				return;
			}

			const values = dialog.get_values(true) || {};
			const employee = this.findEmployee(values.employee);
			if (employee) {
				dialog.fields_dict.employee_hint_html.$wrapper.html(`
					<div class="dpm-employee-note">
						<strong>${frappe.utils.escape_html(employee.employee_name || employee.name)}</strong>
						<span>${frappe.utils.escape_html(employee.name)} · ${frappe.utils.escape_html(employee.department || "")}${employee.user_id ? ` · ${__("Linked")}: ${frappe.utils.escape_html(employee.user_id)}` : ""}</span>
					</div>
				`);
				return;
			}

			const department = values.department;
			const count = this.employeesForDepartment(department, values.employee, values.email).length;
			dialog.fields_dict.employee_hint_html.$wrapper.html(`
				<div class="dpm-employee-note is-muted">
					<span>${count ? __("Select an existing Employee in this department, or leave blank for service/non-employee users.") : __("No available Employee records in this department.")}</span>
				</div>
			`);
		}

		renderRoleChecklist(dialog, roles, selectedRoles) {
			const wrapper = dialog.fields_dict.roles_html.$wrapper;
			if (!roles.length) {
				wrapper.html(`<div class="dpm-dialog-empty">${__("This department has no assignable roles.")}</div>`);
				return;
			}

			wrapper.html(`
				<div class="dpm-role-checks">
					${roles
						.map(
							(role) => `
								<label class="dpm-role-check">
									<input type="checkbox" value="${frappe.utils.escape_html(role)}" ${selectedRoles.has(role) ? "checked" : ""} />
									<span>${frappe.utils.escape_html(role)}</span>
								</label>
							`
						)
						.join("")}
				</div>
			`);
		}

		saveUser(dialog) {
			const values = dialog.get_values();
			if (!values) {
				return;
			}

			const roles = dialog.fields_dict.roles_html.$wrapper
				.find("input:checked")
				.map((index, input) => input.value)
				.get();

			frappe.call({
				method: API.saveUser,
				args: {
					data: JSON.stringify({ ...values, roles }),
				},
				freeze: true,
				freeze_message: __("Saving user..."),
				callback: () => {
					dialog.hide();
					frappe.show_alert({ message: __("User saved"), indicator: "green" }, 4);
					this.load();
				},
			});
		}

		disableUser(user) {
			frappe.confirm(__("Disable user {0}?", [user]), () => {
				frappe.call({
					method: API.disableUser,
					args: { user },
					freeze: true,
					callback: () => {
						frappe.show_alert({ message: __("User disabled"), indicator: "orange" }, 4);
						this.load();
					},
				});
			});
		}

		revokeDeptAccess(user, department) {
			frappe.confirm(__("Khóa quyền phòng {0} của user {1}?", [department, user]), () => {
				frappe.call({
					method: API.revokeDeptAccess,
					args: { user, department },
					freeze: true,
					callback: (r) => {
						this.state.dashboard = r.message;
						frappe.show_alert({ message: __("Đã khóa quyền phòng"), indicator: "orange" }, 4);
						this.render();
					},
				});
			});
		}

		filteredUsers() {
			const query = (this.state.query || "").trim().toLowerCase();
			return (this.state.dashboard?.users || []).filter((user) => {
				if (!(user.departments || [user.department]).includes(this.state.department)) {
					return false;
				}
				if (this.state.status === "enabled" && !user.enabled) {
					return false;
				}
				if (this.state.status === "disabled" && user.enabled) {
					return false;
				}
				if (!query) {
					return true;
				}
				const haystack = [user.full_name, user.email, user.department, user.employee, user.employee_name, ...(user.roles || [])]
					.join(" ")
					.toLowerCase();
				return haystack.includes(query);
			});
		}

		rolesForDepartment(department) {
			const roles = [];
			(this.state.dashboard?.scopes || []).forEach((scope) => {
				if (scope.department === department) {
					(scope.allowed_roles || []).forEach((role) => roles.push(role.role));
				}
			});
			return [...new Set(roles)].sort();
		}

		extraProfilesForDepartment(department) {
			const profiles = [];
			(this.state.dashboard?.scopes || []).forEach((scope) => {
				if (scope.department === department) {
					(scope.extra_permission_profiles || []).forEach((profile) => profiles.push(profile.label || profile.profile));
				}
			});
			return [...new Set(profiles)].sort();
		}

		departmentList() {
			return this.state.dashboard?.department_catalog || (this.state.dashboard?.departments || []).map((name) => ({ name, label: name, is_configured: 1 }));
		}

		employeeCatalog() {
			return this.state.dashboard?.employees || [];
		}

		employeesForDepartment(department, includeEmployee, userEmail) {
			const normalizedUser = (userEmail || "").toLowerCase();
			return this.employeeCatalog().filter((employee) => {
				if (employee.department !== department) {
					return false;
				}
				if (employee.name === includeEmployee) {
					return true;
				}
				if (!employee.user_id) {
					return true;
				}
				return normalizedUser && String(employee.user_id).toLowerCase() === normalizedUser;
			});
		}

		employeeOptionsForDepartment(department, includeEmployee, userEmail) {
			const options = this.employeesForDepartment(department, includeEmployee, userEmail).map((employee) => employee.name);
			if (includeEmployee && !options.includes(includeEmployee)) {
				options.unshift(includeEmployee);
			}
			return ["", ...new Set(options)];
		}

		findEmployee(employeeName) {
			return this.employeeCatalog().find((employee) => employee.name === employeeName);
		}

		isDefaultRole(department, roleName) {
			return (this.state.dashboard?.scopes || []).some((scope) => {
				return scope.department === department && (scope.allowed_roles || []).some((role) => role.role === roleName && role.is_default);
			});
		}

		groupScopes(scopes) {
			return (scopes || []).reduce((out, scope) => {
				if (!scope.department) {
					return out;
				}
				out[scope.department] = out[scope.department] || [];
				out[scope.department].push(scope);
				return out;
			}, {});
		}

		groupPermissionItems(items) {
			return (items || []).reduce((out, item) => {
				out[item.group] = out[item.group] || [];
				out[item.group].push(item);
				return out;
			}, {});
		}

		escapeSelectorValue(value) {
			return String(value).replace(/\\/g, "\\\\").replace(/"/g, '\\"');
		}

		findUser(userName) {
			return (this.state.dashboard?.users || []).find((user) => user.name === userName);
		}

		initials(user) {
			const source = user.full_name || user.email || "?";
			return source
				.split(/\s+/)
				.filter(Boolean)
				.slice(0, 2)
				.map((part) => part[0])
				.join("")
				.toUpperCase();
		}

		avatarColorIndex(user) {
			const source = user.full_name || user.email || "";
			const initial = source.trim()[0] || "A";
			return initial.toUpperCase().charCodeAt(0) % 5;
		}
	}
})();
