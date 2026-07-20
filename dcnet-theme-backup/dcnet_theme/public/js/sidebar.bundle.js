/**
 * dcnet_theme — sidebar resolver + UX patches.
 *
 * 3 IIFE blocks:
 *   1. route_options patch          — Frappe v16 ignores route_options on
 *                                     DocType / Report Link items; this fixes
 *                                     it. Also tracks last-clicked sidebar
 *                                     label for Block 3 active-highlight
 *                                     scoring.
 *   2. set_workspace_sidebar (v0.3 strict-with-explicit-release) —
 *                                     4-branch resolver:
 *                                       a. workspace-nav (URL is workspace) →
 *                                          save lock + setup (RELEASE old lock)
 *                                       b. lock valid → keep (strict sticky)
 *                                          regardless of entity membership
 *                                       c. no lock → pick first viable
 *                                          (NO lock save — preserve explicit pick)
 *                                       d. no candidates → defer Frappe
 *                                          show_sidebar_for_module
 *                                     Plus capture-phase click listeners on
 *                                     desktop icons (reads `data-id`) AND
 *                                     sidebar items (reads enclosing
 *                                     `.body-sidebar[data-title]`) so both
 *                                     entry points pin the lock before
 *                                     Frappe's body click handler navigates.
 *                                     Plus setup("private"|"Personal") rewrite
 *                                     to "My Workspaces" lock.
 *                                     Lock released ONLY by explicit workspace
 *                                     URL nav (Step 1), desktop icon click,
 *                                     or sidebar-item click in another sidebar.
 *                                     Through doctype/list/report navigation
 *                                     the lock holds — entity NOT being in
 *                                     locked sidebar's items is fine; the
 *                                     workspace stays as user's chosen context.
 *   3. is_route_in_sidebar scoring  — correct active highlight when multiple
 *                                     items link to same DocType with
 *                                     different route_options (e.g. Payment
 *                                     Entry Receive vs Pay).
 *
 * The VN Accounting auto-accordion (formerly Block 4) lives in the
 * vn_accounting app at public/js/sidebar_accordion.bundle.js — extracted
 * because it's app-specific, not theme-level.
 */

// ──────────────────────────────────────────────────────────────
// Block 0: Defensive guard for Frappe core sidebar methods.
// Older Frappe builds crashed inside get_workspace_sidebars /
// get_correct_workspace_sidebars with "Cannot read properties of undefined
// (reading 'forEach')" when boot data was missing. Guard catches that.
//
// Guard against `this.all_sidebar_items` being undefined — that's the
// property Frappe core iterates (sidebar.js sets it from
// frappe.boot.workspace_sidebar_item). The previous version of this guard
// checked frappe.boot.workspace_sidebars (plural) which doesn't exist on
// current Frappe builds → guard returned [] on EVERY call, silently masking
// every candidate lookup. That cascaded into resolver branch-3 never firing,
// query_report.js calling show_sidebar_for_module() with preferred_sidebars=[]
// (sticky guard misses), and sidebar flipping to the report's module workspace
// (FB-2026-00448 "sidebar switches to Mua when clicking BC mua hàng").
// ──────────────────────────────────────────────────────────────
(function () {
	if (!frappe.ui?.Sidebar?.prototype) return;
	const proto = frappe.ui.Sidebar.prototype;
	["get_workspace_sidebars", "get_correct_workspace_sidebars"].forEach(function (method) {
		const orig = proto[method];
		const flag = "_dcnet_" + method + "_guarded";
		if (typeof orig !== "function" || proto[flag]) return;
		proto[flag] = true;
		proto[method] = function (entity_name) {
			if (!this.all_sidebar_items) return [];
			try {
				return orig.call(this, entity_name);
			} catch (e) {
				console.warn("[dcnet_theme] " + method + " threw, returning []:", e.message);
				return [];
			}
		};
	});
})();

// ──────────────────────────────────────────────────────────────
// Block 0b: Guard TypeSectionBreak.toggle() crash.
// Frappe core calls toggle() which accesses this.$drop_icon.attr(),
// but $drop_icon is only set when item.collapsible or item.show_arrow.
// Without this guard, ALL page navigation breaks.
// ──────────────────────────────────────────────────────────────
(function () {
	const SB = frappe.ui?.sidebar_item?.TypeSectionBreak;
	if (!SB || !SB.prototype.toggle) return;
	const orig = SB.prototype.toggle;
	SB.prototype.toggle = function () {
		if (!this.$drop_icon) return;
		orig.call(this);
	};
})();

// ──────────────────────────────────────────────────────────────
// Block 1: route_options patch on DocType + Report Link items
// ──────────────────────────────────────────────────────────────
(function () {
	if (!frappe.ui?.sidebar_item?.TypeLink) {
		console.warn("[dcnet_sidebar_routing] sidebar_item.TypeLink not found, route_options patch skipped");
		return;
	}

	const OriginalGetPath = frappe.ui.sidebar_item.TypeLink.prototype.get_path;

	frappe.ui.sidebar_item.TypeLink.prototype.get_path = function () {
		// DocType links with route_options: encode into URL query params
		if (
			this.item.type === "Link" &&
			this.item.link_type === "DocType" &&
			this.item.route_options &&
			!this.item.filters
		) {
			// Why: frappe.utils.generate_route flattens array filter values
			// like ["=", 1] into "=,1" → list view reads it as a literal
			// equality on the string "=,1" and matches no rows. Build the
			// list URL ourselves: scalar → ?k=v, array → ?k=<json> (Frappe
			// list URL parser unmarshals JSON arrays back into [op, val]).
			const route_options = JSON.parse(this.item.route_options);
			const base = frappe.utils.generate_route({
				type: this.item.link_type,
				name: this.item.link_to,
				tab: this.item.tab,
				doc_view: "List",
			});
			const qs = Object.entries(route_options)
				.filter(([, v]) => v !== null && v !== undefined && v !== "")
				.map(([k, v]) => {
					const encoded = Array.isArray(v) ? JSON.stringify(v) : v;
					return `${encodeURIComponent(k)}=${encodeURIComponent(encoded)}`;
				})
				.join("&");
			return qs ? `${base}${base.includes("?") ? "&" : "?"}${qs}` : base;
		}

		// Report links with route_options: append as URL query params
		if (
			this.item.type === "Link" &&
			this.item.link_type === "Report" &&
			this.item.route_options
		) {
			let path = OriginalGetPath.call(this);
			const params = JSON.parse(this.item.route_options);
			const qs = Object.entries(params)
				.map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
				.join("&");
			return path + (path.includes("?") ? "&" : "?") + qs;
		}

		return OriginalGetPath.call(this);
	};

	// Track most-recently-clicked sidebar label (for active highlight scoring)
	$(document).on("click", ".item-anchor", function () {
		const label = $(this).find(".sidebar-item-label").text().trim() || $(this).text().trim();
		if (label) {
			window._vna_last_clicked_sidebar = label;
			setTimeout(() => { window._vna_last_clicked_sidebar = null; }, 3000);
		}
	});
})();

// ──────────────────────────────────────────────────────────────
// Block 2: set_workspace_sidebar — STICKY context model
// ──────────────────────────────────────────────────────────────
//
// DEBUG: enable verbose console logging via:
//   localStorage.setItem("dcnet_sidebar_debug", "1")  // turn ON
//   localStorage.removeItem("dcnet_sidebar_debug")    // turn OFF
//
// Or call window.dcnetSidebarStatus() to dump current state.
//
// Mental model: explicit sidebar/desktop click = short-lived LOCK.
// The lock protects the route caused by that click, then passive navigation
// (Search/Awesomebar/direct URL) falls back to explicit DocType ownership,
// module/app matching, and finally Frappe's module sidebar fallback.
//
// Storage: sessionStorage (per-tab) + localStorage TTL 30 phút (cross-tab recency).
(function () {
	const CONTEXT_KEY = "workspace_context";
	const SOURCE_KEY = "workspace_context_source";
	const CONTEXT_TTL_MS = 30 * 60 * 1000;
	const SOURCE_TTL_MS = 4000;
	const DEBUG_KEY = "dcnet_sidebar_debug";

	function _dbg(...args) {
		try {
			if (localStorage.getItem(DEBUG_KEY)) console.log("[sidebar]", ...args);
		} catch {}
	}

	function _saveContext(name, source) {
		if (!name) return;
		try {
			sessionStorage.setItem(CONTEXT_KEY, name);
			localStorage.setItem(
				CONTEXT_KEY,
				JSON.stringify({ value: name, savedAt: Date.now() })
			);
			if (source) {
				sessionStorage.setItem(
					SOURCE_KEY,
					JSON.stringify({ source, value: name, savedAt: Date.now() })
				);
			}
			_dbg("lock saved →", name);
		} catch {}
	}

	function _getContext() {
		try {
			const sess = sessionStorage.getItem(CONTEXT_KEY);
			if (sess) return sess;
			const raw = localStorage.getItem(CONTEXT_KEY);
			if (!raw) return null;
			const { value, savedAt } = JSON.parse(raw);
			if (Date.now() - savedAt > CONTEXT_TTL_MS) {
				localStorage.removeItem(CONTEXT_KEY);
				return null;
			}
			return value;
		} catch {
			return null;
		}
	}

	function _clearContext(reason) {
		try {
			sessionStorage.removeItem(CONTEXT_KEY);
			localStorage.removeItem(CONTEXT_KEY);
			sessionStorage.removeItem(SOURCE_KEY);
			_dbg("lock cleared", reason || "");
		} catch {}
	}

	function _getRecentSource() {
		try {
			const raw = sessionStorage.getItem(SOURCE_KEY);
			if (!raw) return null;
			const source = JSON.parse(raw);
			if (Date.now() - source.savedAt > SOURCE_TTL_MS) {
				sessionStorage.removeItem(SOURCE_KEY);
				return null;
			}
			return source;
		} catch {
			return null;
		}
	}

	// Workspace có 2 dạng tên: URL slug (lowercase) và canonical label (PascalCase).
	// Storage và resolver luôn làm việc với canonical label.
	function _canonicalize(slugOrName) {
		if (!slugOrName) return null;
		const item = frappe.boot?.workspace_sidebar_item?.[slugOrName.toLowerCase()];
		return item?.label || slugOrName;
	}

	// Lock có còn hợp lệ không? (workspace tồn tại + user có quyền module)
	function _isLockValid(canonicalName) {
		if (!canonicalName) return false;
		const items = frappe.boot?.workspace_sidebar_item || {};
		const item = Object.values(items).find((i) => i.label === canonicalName);
		if (!item) return false;
		if (!item.module) return true;
		const allowed = new Set(frappe.boot?.user_allowed_modules || []);
		return allowed.has(item.module);
	}

	function _filterByModule(candidates) {
		const allowed = new Set(frappe.boot.user_allowed_modules || []);
		const sb_modules = frappe.boot.workspace_sidebar_modules || {};
		if (!allowed.size && !Object.keys(sb_modules).length) return candidates;
		return candidates.filter((name) => {
			const mod = sb_modules[name];
			return !mod || allowed.has(mod);
		});
	}

	function _getDirectSidebarLabel(entityName) {
		if (!entityName) return null;
		const sidebar = frappe.boot?.workspace_sidebar_item?.[entityName.toLowerCase()];
		return sidebar?.label || null;
	}

	if (!frappe.ui?.Sidebar) {
		console.warn("[dcnet_sidebar_routing] frappe.ui.Sidebar not found, resolver skipped");
		return;
	}

	let _routerEventFired = false;
	let _inResolver = false;

	// setup() patch — minimal:
	//   • setup("private"|"Personal") → save lock for new-private-workspace flow.
	//   • Idempotent guard — skip rerender when already at requested workspace.
	//   • Otherwise pass through. Resolver is authoritative for sidebar choice;
	//     external setup() callers (workspace.js, page-change) are trusted.
	//
	// Strict force-lock removed in favour of conditional sticky in resolver
	// (Block 2 v0.2 — see below). Force-lock conflicted with conditional model:
	// when user typed URL outside locked sidebar, force-lock would redirect
	// back to old lock even though resolver decided to release it.
	const _origSetup = frappe.ui.Sidebar.prototype.setup;
	frappe.ui.Sidebar.prototype.setup = function (name) {
		if (!_routerEventFired || _inResolver) {
			return _origSetup.apply(this, arguments);
		}

		// setup("private") / setup("Personal") = user just created a private
		// workspace (workspace.js:609) and Frappe is switching to the "My
		// Workspaces" sidebar to show it. Save lock so the new-private flow
		// is preserved across F5.
		if (name === "private" || name === "Personal") {
			_saveContext("My Workspaces");
			_dbg("setup(", name, ") → private workspace switch, lock=My Workspaces");
			return _origSetup.apply(this, arguments);
		}

		const want = _canonicalize(name);
		const recent = _getRecentSource();
		const locked = _canonicalize(_getContext());

		// Workspace pages call setup(page.name) after route resolution. When a
		// user just clicked a Desktop Icon / sidebar item whose first link opens
		// a Workspace (e.g. DCNet Contract → Contract Manager), keep the explicit
		// sidebar context instead of letting that Workspace name overwrite it.
		if (
			recent &&
			locked &&
			_isLockValid(locked) &&
			want &&
			want !== locked
		) {
			_dbg("setup(", want, ") → recent explicit lock keeps", locked);
			if (this.sidebar_title !== locked) {
				return _origSetup.call(this, locked);
			}
			return;
		}

		// Idempotent guard — Frappe core has many code paths that call setup()
		// for the same workspace (resolver + workspace.setup_sidebar + page-change
		// toggle + show_sidebar_for_module). Skip rerender when already current
		// to avoid flicker + duplicate Vue mount warnings on the onboarding widget.
		if (want && this.sidebar_title === want) {
			_dbg("setup(", want, ") → already current, skipped");
			return;
		}

		return _origSetup.apply(this, arguments);
	};

	// Inspector — paste `dcnetSidebarStatus()` in console for one-shot dump.
	window.dcnetSidebarStatus = function () {
		const stored = _getContext();
		const canon = _canonicalize(stored);
		return {
			route: frappe.get_route?.(),
			stored_raw: stored,
			stored_canonical: canon,
			lock_valid: canon ? _isLockValid(canon) : false,
			current_sidebar_title: frappe.app?.sidebar?.sidebar_title,
			workspace_sidebar_keys: Object.keys(frappe.boot?.workspace_sidebar_item || {}),
			user_allowed_modules: frappe.boot?.user_allowed_modules || [],
			debug_enabled: !!localStorage.getItem(DEBUG_KEY),
		};
	};

	// Desktop icon click → update lock from data-id.
	// `<a class="desktop-icon" data-id="<icon.label>">` template puts the
	// canonical workspace_sidebar name in data-id.
	//
	// MUST use capture phase: Frappe's `$("body").on("click","a",...)` handler
	// (router.js) intercepts the bubble at <body>, calls frappe.set_route →
	// push_state → router.route() SYNCHRONOUSLY. The resolver reads stored
	// lock during route(). A bubble-phase listener on document fires AFTER
	// body, so it would save AFTER the resolver — too late. Capture phase
	// runs document → body, so we save BEFORE Frappe redirects.
	document.addEventListener("click", function (e) {
		const icon = e.target.closest && e.target.closest(".desktop-icon");
		if (!icon) return;
		const id = icon.getAttribute("data-id");
		_dbg("desktop-icon click data-id=", id);
		if (!id) return;
		const items = frappe.boot?.workspace_sidebar_item || {};
		if (items[id.toLowerCase()]) {
			_saveContext(id, "desktop");
		} else {
			_dbg("  ↳ no match in workspace_sidebar_item, lock unchanged");
		}
	}, true);

	// Sidebar-item click → save lock from the enclosing sidebar's data-title.
	// Must run in capture phase so the lock is in place BEFORE Frappe's body
	// click handler dispatches set_route → router → resolver. Without this,
	// when no lock is set and the clicked item points to an entity that lives
	// in multiple workspaces (e.g. Purchase Analytics ∈ Mua + VN Accounting),
	// the resolver falls through to Branch 3 ("pick-first") and may pick the
	// wrong sidebar (FB-2026-00448).
	document.addEventListener("click", function (e) {
		const anchor = e.target.closest && e.target.closest(".item-anchor");
		if (!anchor) return;
		const sidebarEl = anchor.closest(".body-sidebar[data-title]");
		const title = sidebarEl && sidebarEl.getAttribute("data-title");
		if (!title) return;
		const items = frappe.boot?.workspace_sidebar_item || {};
		if (!items[title.toLowerCase()]) {
			_dbg("item-anchor click: '" + title + "' not in boot, skip");
			return;
		}
		_dbg("item-anchor click → save lock", title);
		_saveContext(title, "sidebar");
	}, true);

	frappe.ui.Sidebar.prototype.set_workspace_sidebar = function (router) {
		_routerEventFired = true;
		_inResolver = true;
		try {
			let route = frappe.get_route();
			let entity_name;
			_dbg("resolver entry route=", route, "stored=", _getContext());
			switch (route.length) {
				case 1:
					entity_name = route[0];
					break;
				case 2:
					entity_name = route[1];
					break;
				case 3:
					entity_name = route[1];
					if (route[0] == "Workspaces" && route[1] == "private") {
						entity_name = route[2];
					}
					break;
				default:
					entity_name = route[1];
			}

			// ── Bước 1: nav workspace tường minh → cập nhật lock ──
			// /app/<slug> hoặc /app/Workspaces/<name> với entity_name là một workspace
			const isWorkspaceNav =
				(route.length === 1 || route.length === 2) &&
				frappe.boot.workspace_sidebar_item?.[entity_name?.toLowerCase()];
			if (isWorkspaceNav) {
				const ws = _canonicalize(entity_name);
				const recent = _getRecentSource();
				const locked = _canonicalize(_getContext());
				const chosen = recent && locked && _isLockValid(locked) ? locked : ws;
				_dbg("  branch=workspace-nav → setup", chosen, "(route workspace=", ws, ")");
				frappe.app.sidebar.setup(chosen);
				_saveContext(chosen);
				this.set_active_workspace_item();
				return;
			}

			// Compute candidates once: which workspace sidebars contain entity_name?
			// Used by Step 3 fallback when no lock; not gating Step 2 sticky.
			const _getSidebars = this.get_workspace_sidebars || this.get_correct_workspace_sidebars;
			const candidates = _getSidebars ? _getSidebars.call(this, entity_name) : [];
			this.preferred_sidebars = candidates;

			// ── Bước 2: explicit sticky — lock còn hợp lệ thì giữ ──
			// Only keep a stored sidebar for the route that immediately follows a
			// sidebar/desktop click. Passive navigation from Search/Awesomebar
			// must not drag a stale sidebar context onto unrelated or shared DocTypes.
			const stored = _canonicalize(_getContext());
			const recent = _getRecentSource();
			const storedIsCandidate = stored && candidates.includes(stored);
			const recentExplicit = recent && recent.value === stored;
			if (stored && _isLockValid(stored) && recentExplicit) {
				_dbg("  branch=sticky → keep", stored, "(current=", this.sidebar_title, ")");
				if (this.sidebar_title !== stored) {
					frappe.app.sidebar.setup(stored);
				}
				this.set_active_workspace_item();
				return;
			}
			if (stored && !recentExplicit) {
				_dbg("  sticky ignored: passive navigation", stored, candidates);
				_clearContext(storedIsCandidate ? "passive navigation" : "stored sidebar not in current candidates");
			}

			// ── Bước 3: chưa có lock → Frappe-style fallback, KHÔNG save lock ──
			// Pick first viable candidate by user's allowed modules. Preserve user's
			// last explicit pick — passive nav (URL typed / awesome bar) shouldn't
			// override what the user clicked last.
			const viable = _filterByModule(candidates);
			let working = viable.length ? viable : candidates;
			if (working.length) {
				const module = router?.meta?.module;
				const directOwner = _getDirectSidebarLabel(entity_name);
				if (directOwner && working.includes(directOwner)) {
					_dbg("  branch=direct-owner → setup", directOwner, "candidates=", candidates);
					frappe.app.sidebar.setup(directOwner);
					this.set_active_workspace_item();
					return;
				}

				const app = module && frappe.boot.module_app?.[module.toLowerCase().replace(/[ -]/g, "_")];
				if (module && app && this.filter_sidebars_from_app) {
					const appSidebars = this.filter_sidebars_from_app(working, app);
					if (appSidebars.length) working = appSidebars;
				}
				const moduleWorkspace = module && this.get_workspace_for_module?.(module);
				const picked =
					moduleWorkspace && working.includes(moduleWorkspace)
						? moduleWorkspace
						: working[0];
				_dbg("  branch=pick-first → setup", picked, "candidates=", candidates, "(no lock save)");
				frappe.app.sidebar.setup(picked);
				this.set_active_workspace_item();
				return;
			}

			// ── Bước 4: không có sidebar nào chứa entity → module fallback ──
			const module = router?.meta?.module;
			_dbg("  branch=defer-module → module=", module);
			if (module) this.show_sidebar_for_module(module);
		} catch (e) {
			console.log(e);
		} finally {
			_inResolver = false;
		}
		this.set_active_workspace_item();
	};
})();

// ──────────────────────────────────────────────────────────────
// Block 3: is_route_in_sidebar scoring (active highlight)
// ──────────────────────────────────────────────────────────────
//
// Frappe's is_route_in_sidebar() strips query params before comparing,
// so when 2 items link to same DocType with different route_options
// (e.g. Payment Entry "Thu tiền NH" with payment_type=Receive and
// "Chi tiền NH" with payment_type=Pay), the LAST match wins
// regardless of which item the user actually clicked.
//
// This patch scores matches:
//   +100 if label matches user's last click
//   +3 per route_options key matching cur_frm.doc field
//   -3 per route_options key NOT matching cur_frm.doc field
//   +2 per route_options key matching URL query param
(function () {
	if (!frappe.ui?.Sidebar?.prototype) return;

	frappe.ui.Sidebar.prototype.is_route_in_sidebar = function () {
		let match = false;
		let bestScore = -1;
		const that = this;

		const currentPath = decodeURIComponent(window.location.pathname).replace(/\/$/, "");
		const currentParams = new URLSearchParams(window.location.search);
		const clickedLabel = window._vna_last_clicked_sidebar;

		$(".item-anchor").each(function () {
			const rawHref = $(this).attr("href");
			if (!rawHref) return;

			const [hrefPath, hrefQuery] = rawHref.split("?");
			const cleanHref = decodeURIComponent(hrefPath).replace(/\/$/, "");

			let baseHref = cleanHref;
			const viewListIdx = baseHref.indexOf("/view/");
			if (viewListIdx > 0) baseHref = baseHref.substring(0, viewListIdx);

			const isPathMatch =
				currentPath === cleanHref ||
				currentPath.startsWith(cleanHref + "/") ||
				currentPath === baseHref ||
				currentPath.startsWith(baseHref + "/");
			if (!isPathMatch) return;

			const label = $(this).find(".sidebar-item-label").text().trim() || $(this).text().trim();
			let score = 0;
			if (clickedLabel && label === clickedLabel) score += 100;

			if (hrefQuery) {
				const hrefParams = new URLSearchParams(hrefQuery);
				for (const [key, val] of hrefParams) {
					if (currentParams.get(key) === val) score += 2;
				}
				if (typeof cur_frm !== "undefined" && cur_frm?.doc) {
					for (const [key, val] of hrefParams) {
						const formVal = cur_frm.doc[key];
						if (formVal !== undefined && formVal !== null && String(formVal) === decodeURIComponent(val)) {
							score += 3;
						} else if (formVal !== undefined && formVal !== null) {
							score -= 3;
						}
					}
				}
			}

			if (score > bestScore || !match) {
				match = true;
				bestScore = score;
				if (that.active_item) that.active_item.removeClass("active-sidebar");
				that.active_item = $(this).parent();
			}
		});
		return match;
	};
})();

// ──────────────────────────────────────────────────────────────
// Block 4: Suppress sidebar item Bootstrap tooltips (FB-490).
// Frappe's sidebar_item.html sets title= + data-toggle="tooltip" on every
// .sidebar-item-container. When the cursor enters a nested item, both the
// item AND its parent section fire tooltips simultaneously → user sees
// 2 stacked lines (item label + section name). Labels render in full
// inside the sidebar, so the tooltip is pure noise. Dispose them on each
// sidebar render.
// ──────────────────────────────────────────────────────────────
(function () {
	function disposeSidebarTooltips() {
		try {
			$(".body-sidebar [data-toggle='tooltip']").each(function () {
				const $el = $(this);
				if ($el.data("bs.tooltip")) {
					try { $el.tooltip("dispose"); } catch (_e) { /* ignore */ }
				}
				$el.removeAttr("data-toggle title data-original-title");
			});
		} catch (_e) { /* ignore */ }
	}

	$(document).ready(() => {
		setTimeout(disposeSidebarTooltips, 300);
		setTimeout(disposeSidebarTooltips, 1500);
	});
	if (frappe.router && frappe.router.on) {
		frappe.router.on("change", () => setTimeout(disposeSidebarTooltips, 200));
	}
	// Watch sidebar DOM for re-renders (Frappe rebuilds it on workspace change)
	const sidebar = document.querySelector(".body-sidebar-container");
	if (sidebar && typeof MutationObserver !== "undefined") {
		let t = null;
		new MutationObserver(() => {
			clearTimeout(t);
			t = setTimeout(disposeSidebarTooltips, 150);
		}).observe(sidebar, { childList: true, subtree: true });
	}
})();
