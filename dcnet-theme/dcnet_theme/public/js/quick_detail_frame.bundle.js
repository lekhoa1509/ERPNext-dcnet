/**
 * dcnet_theme — Quick Detail Frame
 *
 * Adds a toggleable bottom panel (1/4 viewport on desktop, full overlay on
 * tablet) to List View, Report View, and Query Report that loads the focal
 * child table of the selected row's parent document. Cells render with
 * Frappe controls; inline edit respects full Frappe permission + docstatus
 * rules via the dcnet_theme.api.quick_detail.set_cell endpoint.
 *
 * Spec: docs/specs/2026-05-13-quick-detail-frame-design.md
 * Feedback origin: FB-2026-00601 (dcnet bench, 2026-05-13)
 */

(function () {
    "use strict";

    if (!window.frappe || frappe.__dcnet_qdf_patched) return;

    // ─────────────────────────────────────────────────────────────────────
    //  Constants
    // ─────────────────────────────────────────────────────────────────────

    const BREAKPOINT_TABLET_MIN = 768;
    const BREAKPOINT_DESKTOP_MIN = 1024;
    const HINT_MAX_AUTO_SHOW = 3;
    const ROW_CHANGE_DEBOUNCE_MS = 200;
    const SAVED_INDICATOR_MS = 2000;

    // Prefetch pipeline tuning. Conservative defaults so large lists (100/500
    // rows) and Query Reports with many rows don't blow up the page.
    const MAX_CACHE_SIZE = 30;            // LRU eviction
    const MAX_QUEUE_SIZE = 20;            // pending prefetch enqueues
    const MAX_CONCURRENT_BATCHES = 3;     // in-flight HTTP batches
    const BATCH_SIZE = 20;                // max pairs per HTTP call
    const BATCH_COALESCE_MS = 100;        // gather requests within this window
    const SCROLL_DEBOUNCE_MS = 300;       // pause prefetch while user scrolls

    const FALLBACK_REGISTRY = {
        "Sales Invoice": "items", "Sales Order": "items", "Delivery Note": "items",
        "Quotation": "items", "Purchase Invoice": "items", "Purchase Order": "items",
        "Purchase Receipt": "items", "Supplier Quotation": "items",
        "Material Request": "items", "Stock Entry": "items", "Pick List": "locations",
        "Stock Reconciliation": "items", "Journal Entry": "accounts",
        "Payment Entry": "references", "Bank Transaction": "payment_entries",
        "Expense Claim": "expenses", "Asset Movement": "assets",
        "Salary Slip": "earnings", "Opportunity": "items",
    };

    // ─────────────────────────────────────────────────────────────────────
    //  LocalStorage helpers
    // ─────────────────────────────────────────────────────────────────────

    const LS = {
        // Global toggle — single switch shared across all list/report views.
        isGlobalEnabled() {
            try { return localStorage.getItem("qdf:global_enabled") === "1"; }
            catch (e) { return false; }
        },
        setGlobalEnabled(on) {
            try {
                if (on) localStorage.setItem("qdf:global_enabled", "1");
                else localStorage.removeItem("qdf:global_enabled");
            } catch (e) {}
        },
        getHintSeenCount() {
            try { return parseInt(localStorage.getItem("qdf:hint_seen_count") || "0", 10); }
            catch (e) { return 0; }
        },
        incHintSeenCount() {
            try {
                const n = LS.getHintSeenCount() + 1;
                localStorage.setItem("qdf:hint_seen_count", String(n));
                return n;
            } catch (e) { return 0; }
        },
        isHintDismissed() {
            try { return localStorage.getItem("qdf:hint_dismissed") === "1"; }
            catch (e) { return false; }
        },
        setHintDismissed() {
            try { localStorage.setItem("qdf:hint_dismissed", "1"); } catch (e) {}
        },
        getHintForceShow() {
            try { return localStorage.getItem("qdf:hint_force_show") === "1"; }
            catch (e) { return false; }
        },
        setHintForceShow(on) {
            try {
                if (on) localStorage.setItem("qdf:hint_force_show", "1");
                else localStorage.removeItem("qdf:hint_force_show");
            } catch (e) {}
        },
    };

    // ─────────────────────────────────────────────────────────────────────
    //  Viewport
    // ─────────────────────────────────────────────────────────────────────

    function getViewportMode() {
        const w = window.innerWidth;
        if (w < BREAKPOINT_TABLET_MIN) return "mobile";
        if (w < BREAKPOINT_DESKTOP_MIN) return "tablet";
        return "desktop";
    }

    // ─────────────────────────────────────────────────────────────────────
    //  Resolve doctype's child field (client-side, mirrors server registry)
    // ─────────────────────────────────────────────────────────────────────

    function getRegistry() {
        const boot = frappe.boot && frappe.boot.dcnet_qdf;
        return (boot && boot.registry) || FALLBACK_REGISTRY;
    }

    function getOverrides() {
        const boot = frappe.boot && frappe.boot.dcnet_qdf;
        return (boot && boot.overrides) || {};
    }

    function isGloballyEnabled() {
        const boot = frappe.boot && frappe.boot.dcnet_qdf;
        if (!boot) return true;  // boot data not loaded yet — default on
        return boot.enabled !== false;
    }

    function quickResolveChildField(doctype) {
        const overrides = getOverrides();
        if (overrides[doctype]) return overrides[doctype];
        const registry = getRegistry();
        if (registry[doctype]) return registry[doctype];
        // Heuristic — we don't have meta client-side, so let server resolve.
        return null;
    }

    // ─────────────────────────────────────────────────────────────────────
    //  LRU cache + Prefetch batcher (singleton — shared across mounts)
    // ─────────────────────────────────────────────────────────────────────

    class LRUCache {
        constructor(max) {
            this.max = max;
            this.map = new Map();  // insertion order = LRU order
        }
        key(doctype, name) { return `${doctype}::${name}`; }
        get(doctype, name) {
            const k = this.key(doctype, name);
            if (!this.map.has(k)) return null;
            const v = this.map.get(k);
            // Re-insert to mark as recently used
            this.map.delete(k);
            this.map.set(k, v);
            return v;
        }
        set(doctype, name, value) {
            const k = this.key(doctype, name);
            if (this.map.has(k)) this.map.delete(k);
            this.map.set(k, value);
            while (this.map.size > this.max) {
                const first = this.map.keys().next().value;
                this.map.delete(first);
            }
        }
        has(doctype, name) { return this.map.has(this.key(doctype, name)); }
        invalidate(doctype, name) { this.map.delete(this.key(doctype, name)); }
        clear() { this.map.clear(); }
    }

    class PrefetchBatcher {
        constructor(cache) {
            this.cache = cache;
            this.pending = new Map();  // key → { doctype, name, resolve, reject, promise }
            this.flushTimer = null;
            this.inFlight = 0;
            // Track jqXHR / fetch handles for in-flight batches so we can
            // abort them on route change. Map<batchId, abortHandle>.
            this.inFlightHandles = new Map();
            this._batchCounter = 0;
            // Generation token: bumped on clearPending so already-sent batches
            // can detect their responses are stale and skip cache update.
            this.gen = 0;
        }

        request(doctype, name) {
            if (this.cache.has(doctype, name)) {
                return Promise.resolve(this.cache.get(doctype, name));
            }
            const key = `${doctype}::${name}`;
            const existing = this.pending.get(key);
            if (existing) return existing.promise;

            if (this.pending.size >= MAX_QUEUE_SIZE) {
                // Queue full — drop oldest queued request to make room.
                const firstKey = this.pending.keys().next().value;
                const dropped = this.pending.get(firstKey);
                this.pending.delete(firstKey);
                dropped.reject(new Error("Queue full — request dropped"));
            }

            let resolve, reject;
            const promise = new Promise((res, rej) => { resolve = res; reject = rej; });
            this.pending.set(key, { doctype, name, resolve, reject, promise });

            this._scheduleFlush();
            return promise;
        }

        _scheduleFlush() {
            if (this.flushTimer) return;
            this.flushTimer = setTimeout(() => this._flush(), BATCH_COALESCE_MS);
        }

        _flush() {
            this.flushTimer = null;
            if (this.inFlight >= MAX_CONCURRENT_BATCHES) {
                // Slot full — try again later (defer to next idle).
                this._scheduleFlush();
                return;
            }
            const items = Array.from(this.pending.values()).slice(0, BATCH_SIZE);
            if (!items.length) return;
            items.forEach((i) => this.pending.delete(`${i.doctype}::${i.name}`));

            this.inFlight++;
            const batchId = ++this._batchCounter;
            const myGen = this.gen;

            // Use frappe.call's underlying $.ajax so we get a real jqXHR with
            // .abort(). The Promise returned by frappe.call itself doesn't
            // expose abort, but the jqXHR returned by frappe.request.call does.
            const xhr = frappe.call({
                method: "dcnet_theme.dcnet_theme.api.quick_detail.get_frame_batch",
                args: { pairs: items.map((i) => ({ doctype: i.doctype, name: i.name })) },
                callback: (r) => this._onBatchSuccess(batchId, myGen, items, r),
                error: (xhrObj) => this._onBatchError(batchId, myGen, items, xhrObj),
                always: () => this._onBatchAlways(batchId),
            });
            // frappe.call returns the jqXHR in v16; track it for abort.
            if (xhr && typeof xhr.abort === "function") {
                this.inFlightHandles.set(batchId, xhr);
            }
        }

        _onBatchSuccess(batchId, myGen, items, r) {
            if (myGen !== this.gen) {
                // Stale response from before clearPending — silently drop.
                items.forEach((i) => i.reject(new Error("Stale")));
                return;
            }
            const data = (r && r.message) || {};
            items.forEach((i) => {
                const key = `${i.doctype}::${i.name}`;
                const entry = data[key] || { parent: null, reason: "Empty response" };
                if (entry && entry.parent && entry.child) {
                    this.cache.set(i.doctype, i.name, entry);
                }
                i.resolve(entry);
            });
        }

        _onBatchError(batchId, myGen, items, xhrObj) {
            const aborted = xhrObj && (xhrObj.statusText === "abort" || xhrObj.status === 0);
            const reason = aborted ? "Aborted" : (xhrObj && xhrObj.statusText) || "Network error";
            items.forEach((i) => i.reject(new Error(reason)));
        }

        _onBatchAlways(batchId) {
            this.inFlight--;
            this.inFlightHandles.delete(batchId);
            if (this.pending.size > 0) this._scheduleFlush();
        }

        clearPending() {
            // Step 1: bump generation so any successful response that races
            // through gets discarded by _onBatchSuccess.
            this.gen++;

            // Step 2: reject pending (not-yet-sent) requests.
            this.pending.forEach((entry) => entry.reject(new Error("Cancelled")));
            this.pending.clear();
            if (this.flushTimer) {
                clearTimeout(this.flushTimer);
                this.flushTimer = null;
            }

            // Step 3: abort in-flight HTTP requests. Releases browser
            // connection slots immediately so the next page's requests
            // aren't queued behind our prefetches.
            this.inFlightHandles.forEach((xhr) => {
                try { xhr.abort(); } catch (e) {}
            });
            this.inFlightHandles.clear();
        }
    }

    const _qdfCache = new LRUCache(MAX_CACHE_SIZE);
    const _qdfBatcher = new PrefetchBatcher(_qdfCache);

    // ─────────────────────────────────────────────────────────────────────
    //  CSS escape helper
    // ─────────────────────────────────────────────────────────────────────

    const cssEsc = (s) => (globalThis.CSS && globalThis.CSS.escape)
        ? globalThis.CSS.escape(s)
        : String(s).replace(/[^a-zA-Z0-9_-]/g, (ch) => "\\" + ch);

    // ─────────────────────────────────────────────────────────────────────
    //  Main class
    // ─────────────────────────────────────────────────────────────────────

    class QuickDetailFrame {
        constructor({ host, mode }) {
            this.host = host;
            this.mode = mode;  // "list" | "query_report"
            this.doctype = this._resolveHostDocType();

            this.frameEl = null;
            this.toggleBtn = null;
            this.hintBar = null;
            this.currentRow = null;
            this.currentParent = null;
            this.editControls = [];
            this.rowChangeTimer = null;
            this.bodyKeyListener = null;
            this.resizeListener = null;

            if (!isGloballyEnabled() || !this.doctype) return;

            try {
                this._mount();
            } catch (e) {
                console.warn("[dcnet_qdf] mount failed:", e);
            }
        }

        _resolveHostDocType() {
            if (this.mode === "list") {
                return (this.host && this.host.doctype) || null;
            }
            if (this.mode === "query_report") {
                // For Query Report, doctype is determined per row; toggle button
                // shows but each row resolves its own doctype via voucher_type.
                return "__query_report__";
            }
            return null;
        }

        // ─── mount / unmount ────────────────────────────────────────────

        _mount() {
            if (getViewportMode() === "mobile") return;

            // Remove any leftover frame elements from previous list views
            // (each route change can spawn a new QuickDetailFrame instance).
            document.querySelectorAll(".qdf-frame").forEach((el) => el.remove());

            this._renderToggleButton();
            this._renderFrameContainer();
            this._bindRowClickDelegation();
            this._bindResizeListener();
            this._updateLayoutOffset();
            this._bindRowPrefetchObserver();

            // Apply GLOBAL toggle state — user's master switch across views.
            if (LS.isGlobalEnabled()) {
                this._setFrameOpen(true, /*persist=*/false);
            }
        }

        // ─── prefetch via IntersectionObserver ──────────────────────────

        _bindRowPrefetchObserver() {
            if (this.rowObserver) {
                this.rowObserver.disconnect();
                this.rowObserver = null;
            }

            // Throttle observer callbacks to skip prefetch during fast scroll.
            this._lastScrollAt = 0;
            const onScroll = () => { this._lastScrollAt = Date.now(); };
            this._scrollListener = onScroll;
            window.addEventListener("scroll", onScroll, { passive: true, capture: true });

            // Pump function: read pending visible rows from a Set + queue them
            // through the batcher when the user is idle and not actively scrolling.
            this._pendingVisible = new Set();
            const pump = () => {
                if (!this._pendingVisible.size) return;
                const sinceScroll = Date.now() - this._lastScrollAt;
                if (sinceScroll < SCROLL_DEBOUNCE_MS) {
                    // User still scrolling — defer.
                    setTimeout(pump, SCROLL_DEBOUNCE_MS - sinceScroll + 50);
                    return;
                }
                const items = Array.from(this._pendingVisible).slice(0, MAX_QUEUE_SIZE);
                this._pendingVisible.clear();
                const fire = () => {
                    items.forEach(({ doctype, name }) => {
                        // No await — fire and forget; cache populates in background.
                        _qdfBatcher.request(doctype, name).catch(() => {});
                    });
                };
                if (typeof requestIdleCallback === "function") {
                    requestIdleCallback(fire, { timeout: 500 });
                } else {
                    setTimeout(fire, 0);
                }
            };
            this._prefetchPump = pump;

            this.rowObserver = new IntersectionObserver((entries) => {
                let added = false;
                entries.forEach((entry) => {
                    if (!entry.isIntersecting) return;
                    const resolved = this._resolveRowTarget(entry.target);
                    if (!resolved) return;
                    if (_qdfCache.has(resolved.doctype, resolved.name)) return;
                    this._pendingVisible.add(resolved);
                    added = true;
                });
                if (added) pump();
            }, { root: null, threshold: 0.1 });

            // Observe rows now AND after route-internal refreshes. List view
            // rebuilds rows on filter/sort, so we re-observe after a short
            // delay + a MutationObserver on the result container.
            const observeAll = () => {
                if (!this.rowObserver) return;
                const sel = this.mode === "list"
                    ? ".list-row-container, .list-row"
                    : ".dt-row[data-row-index]";
                document.querySelectorAll(sel).forEach((row) => {
                    try { this.rowObserver.observe(row); } catch (e) {}
                });
            };
            // Initial observe + repeat to catch late-rendered rows.
            setTimeout(observeAll, 100);
            setTimeout(observeAll, 600);

            // Re-observe when list result area mutates.
            const $area = this.host.$result || this.host.$container ||
                          $(this.host.page && this.host.page.body);
            const areaEl = ($area && $area.length) ? $area.get(0) : null;
            if (areaEl) {
                this._areaMutationObserver = new MutationObserver(() => {
                    observeAll();
                });
                this._areaMutationObserver.observe(areaEl, {
                    childList: true, subtree: true,
                });
            }
        }

        _resolveRowTarget(rowEl) {
            if (this.mode === "list") {
                const matchingCarrier = rowEl.querySelector(
                    `[data-name][data-doctype="${cssEsc(this.doctype)}"]`
                );
                const anyCarrier = rowEl.querySelector("[data-name][data-doctype]");
                const carrier = matchingCarrier || anyCarrier;
                const name = carrier?.getAttribute("data-name");
                const doctype = carrier?.getAttribute("data-doctype") || this.doctype;
                if (!name || !doctype || doctype === "__query_report__") return null;
                return { doctype, name };
            }
            if (this.mode === "query_report") {
                const idx = parseInt(rowEl.getAttribute("data-row-index") || "-1", 10);
                if (idx < 0 || !this.host.data || !this.host.data[idx]) return null;
                const row = this.host.data[idx];
                const doctype = row.voucher_type || row.doctype || row.ref_doctype;
                const name = row.voucher_no || row.doc_name || row.ref_docname || row.name;
                if (!doctype || !name) return null;
                return { doctype, name };
            }
            return null;
        }

        destroy() {
            if (this.toggleBtn) this.toggleBtn.remove();
            if (this.frameEl) this.frameEl.remove();
            if (this.bodyKeyListener) {
                document.removeEventListener("keydown", this.bodyKeyListener, true);
            }
            if (this.bodyClickListener) {
                document.removeEventListener("click", this.bodyClickListener, true);
            }
            if (this.resizeListener) {
                window.removeEventListener("resize", this.resizeListener);
            }
            if (this.rowObserver) {
                try { this.rowObserver.disconnect(); } catch (e) {}
                this.rowObserver = null;
            }
            if (this._areaMutationObserver) {
                try { this._areaMutationObserver.disconnect(); } catch (e) {}
                this._areaMutationObserver = null;
            }
            if (this._scrollListener) {
                window.removeEventListener("scroll", this._scrollListener, { capture: true });
                this._scrollListener = null;
            }
            this.host.__dcnet_qdf = null;
        }

        // ─── toggle button ──────────────────────────────────────────────

        _renderToggleButton(retry) {
            // Idempotent only while the button is still attached. After a
            // list→list navigation the old button can be detached with its
            // page wrapper — drop the stale ref and re-render.
            if (this.toggleBtn && this.toggleBtn.isConnected) return;
            this.toggleBtn = null;
            retry = retry || 0;

            // Find a stable anchor in the page header
            const $page = this.host.$page || $(this.host.page && this.host.page.wrapper);
            const $actions = ($page && $page.length)
                ? $page.find(".page-actions").first()
                : $(".page-actions").first();

            if (!$actions.length) {
                // .page-actions not in DOM yet — retry up to 20 times (4s)
                if (retry < 20) {
                    setTimeout(() => this._renderToggleButton(retry + 1), 200);
                }
                return;
            }

            const isOn = LS.isGlobalEnabled();
            this.toggleBtn = $(`
                <button class="btn btn-default btn-sm qdf-toggle-btn ${isOn ? "qdf-toggle-btn--on" : ""}"
                        title="${__("Bật/tắt khung xem nhanh")}">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
                         stroke="currentColor" stroke-width="2" stroke-linecap="round"
                         stroke-linejoin="round" style="vertical-align: -2px;">
                        <rect x="3" y="3" width="18" height="18" rx="2"/>
                        <path d="M3 14h18"/>
                    </svg>
                    <span class="qdf-toggle-label">${__("Xem nhanh")}</span>
                    <span class="qdf-toggle-check" aria-hidden="true">✓</span>
                </button>
            `).get(0);

            // Clear any stale toggle button left in this page header by a
            // previous list's QDF instance before adding our own.
            $actions.find(".qdf-toggle-btn").remove();
            $actions.prepend(this.toggleBtn);

            this.toggleBtn.addEventListener("click", () => {
                const willOpen = !this.frameEl.classList.contains("qdf-frame--open");
                this._setFrameOpen(willOpen, /*persist=*/true);
            });
        }

        // ─── frame container ────────────────────────────────────────────

        _renderFrameContainer() {
            this.frameEl = document.createElement("section");
            this.frameEl.className = "qdf-frame";
            this.frameEl.setAttribute("role", "region");
            this.frameEl.setAttribute("aria-label", __("Khung xem nhanh chi tiết"));
            this.frameEl.innerHTML = `
                <header class="qdf-header">
                    <div class="qdf-header-title">${__("Click 1 dòng để xem chi tiết")}</div>
                    <div class="qdf-header-actions">
                        <button type="button" class="qdf-btn-hint" title="${__("Hướng dẫn phím")}">?</button>
                        <a class="qdf-btn-open-form" href="#" target="_blank"
                           style="display:none;">↗ ${__("Mở chi tiết")}</a>
                        <button type="button" class="qdf-btn-close" title="${__("Đóng")}">×</button>
                    </div>
                </header>
                <div class="qdf-hint-bar" style="display:none;">
                    <span><kbd>↓↑</kbd> ${__("chuyển dòng")}</span>
                    <span> · <kbd>Tab</kbd> ${__("vào sửa")}</span>
                    <span> · <kbd>Enter</kbd> ${__("mở form")}</span>
                    <span> · <kbd>Esc</kbd> ${__("đóng")}</span>
                    <button type="button" class="qdf-hint-dismiss" aria-label="${__("Tắt hướng dẫn")}">×</button>
                </div>
                <div class="qdf-body">
                    <div class="qdf-empty">
                        📋 ${__("Click 1 dòng trong danh sách để xem chi tiết")}
                    </div>
                </div>
            `;
            document.body.appendChild(this.frameEl);

            this.frameEl.querySelector(".qdf-btn-close").addEventListener("click", () => {
                this._setFrameOpen(false, /*persist=*/true);
            });
            this.frameEl.querySelector(".qdf-btn-hint").addEventListener("click", () => {
                LS.setHintForceShow(!LS.getHintForceShow());
                this._refreshHintVisibility();
            });
            this.frameEl.querySelector(".qdf-hint-dismiss").addEventListener("click", () => {
                LS.setHintDismissed();
                LS.setHintForceShow(false);
                this._refreshHintVisibility();
            });
        }

        _setFrameOpen(open, persist) {
            if (!this.frameEl) return;
            const mode = getViewportMode();
            if (open) {
                this.frameEl.classList.add("qdf-frame--open");
                this.frameEl.classList.add(`qdf-frame--${mode}`);
                if (mode === "desktop") {
                    document.body.classList.add("qdf-frame-open-desktop");
                }
                this._updateLayoutOffset();
                this._refreshHintVisibility();
                this._bindKeyboardNav();
            } else {
                this.frameEl.classList.remove("qdf-frame--open");
                document.body.classList.remove("qdf-frame-open-desktop");
                this._unbindKeyboardNav();
                this._clearRowSelection();
            }
            if (this.toggleBtn) {
                this.toggleBtn.classList.toggle("qdf-toggle-btn--on", open);
            }
            if (persist) {
                LS.setGlobalEnabled(open);
            }
        }

        _updateLayoutOffset() {
            // Make the frame start to the right of the desk sidebar so the
            // sidebar stays visible/clickable. Sidebar width is dynamic
            // (collapsed vs expanded) so we read it on each update.
            try {
                const sidebar = document.querySelector(".body-sidebar-container, .body-sidebar-placeholder");
                const width = (sidebar && sidebar.offsetParent !== null) ? sidebar.offsetWidth : 0;
                document.documentElement.style.setProperty("--qdf-sidebar-offset", width + "px");
            } catch (e) {}
        }

        _refreshHintVisibility() {
            const hint = this.frameEl.querySelector(".qdf-hint-bar");
            if (!hint) return;
            if (getViewportMode() !== "desktop") {
                hint.style.display = "none";
                return;
            }
            const dismissed = LS.isHintDismissed();
            const forceShow = LS.getHintForceShow();
            const seenCount = LS.getHintSeenCount();

            let visible;
            if (forceShow) visible = true;
            else if (dismissed) visible = false;
            else visible = seenCount < HINT_MAX_AUTO_SHOW;

            hint.style.display = visible ? "" : "none";
            if (visible && !forceShow && !dismissed) {
                LS.incHintSeenCount();
            }
        }

        // ─── row click delegation ───────────────────────────────────────

        _bindRowClickDelegation() {
            // Bind at document level with CAPTURE phase so we intercept the
            // row click BEFORE Frappe's bubble-phase handler runs set_route().
            if (this.bodyClickListener) return;

            this.bodyClickListener = (e) => {
                if (!this.frameEl) return;
                if (!this.frameEl.classList.contains("qdf-frame--open")) return;

                const target = e.target;
                if (!target || !target.closest) return;

                // Skip if click on link, checkbox, action button — preserve
                // Frappe defaults for these affordances.
                if (target.closest("a") ||
                    target.closest("input[type='checkbox']") ||
                    target.closest(".list-row-checkbox") ||
                    target.closest(".list-actions") ||
                    target.closest(".btn") ||
                    target.closest("button")) {
                    return;
                }

                if (this.mode === "list") {
                    const rowEl = target.closest(".list-row-container, .list-row");
                    if (!rowEl) return;
                    // Skip the header row (no data, has list-row-head class).
                    if (rowEl.querySelector(".list-row-head") &&
                        !rowEl.querySelector("[data-name]")) return;
                    e.preventDefault();
                    e.stopPropagation();
                    this._handleListRowSelect(rowEl);
                } else if (this.mode === "query_report") {
                    if (target.closest(".dt-cell--header")) return;
                    const rowEl = target.closest(".dt-row");
                    if (!rowEl) return;
                    e.preventDefault();
                    e.stopPropagation();
                    this._handleQueryReportRowSelect(rowEl);
                }
            };

            document.addEventListener("click", this.bodyClickListener, /*capture=*/true);
        }

        _handleListRowSelect(rowEl) {
            // Prefer the element that carries BOTH data-name and data-doctype
            // (Frappe list-row checkbox + ID link both have these). This
            // disambiguates rows that contain inline party/customer links with
            // their own data-name. Use that element's data-doctype as the
            // authoritative target, falling back to the list view's doctype.
            const matchingCarrier = rowEl.querySelector(
                `[data-name][data-doctype="${CSS && CSS.escape ? CSS.escape(this.doctype) : this.doctype}"]`
            );
            const anyCarrier = rowEl.querySelector("[data-name][data-doctype]");
            const carrier = matchingCarrier || anyCarrier;

            const name = carrier?.getAttribute("data-name") ||
                         rowEl.getAttribute("data-name") ||
                         rowEl.querySelector("[data-name]")?.getAttribute("data-name");
            const doctype = carrier?.getAttribute("data-doctype") || this.doctype;
            if (!name) return;
            this._selectRowVisual(rowEl);
            this._debounceRowChange(doctype, name);
        }

        _handleQueryReportRowSelect(rowEl) {
            // Query Report: rows have data-row-index; we need voucher_type + voucher_no
            const idx = parseInt(rowEl.getAttribute("data-row-index") || "-1", 10);
            if (idx < 0 || !this.host.data || !this.host.data[idx]) return;
            const row = this.host.data[idx];
            const vtype = row.voucher_type || row.doctype || row.ref_doctype;
            const vno = row.voucher_no || row.doc_name || row.ref_docname || row.name;
            if (!vtype || !vno) {
                this._renderMessage(
                    __("Báo cáo này chưa hỗ trợ xem nhanh (thiếu cột voucher_type/voucher_no)")
                );
                return;
            }
            this._selectRowVisual(rowEl);
            this._debounceRowChange(vtype, vno);
        }

        _selectRowVisual(rowEl) {
            // Clear previous selection
            const allRows = (rowEl.parentElement || document).querySelectorAll(".qdf-row-selected");
            allRows.forEach((r) => r.classList.remove("qdf-row-selected"));
            rowEl.classList.add("qdf-row-selected");
        }

        _clearRowSelection() {
            document.querySelectorAll(".qdf-row-selected")
                .forEach((r) => r.classList.remove("qdf-row-selected"));
        }

        _debounceRowChange(doctype, name) {
            if (this.rowChangeTimer) clearTimeout(this.rowChangeTimer);
            // Adaptive: cache hit → fire immediately (no perceptible delay).
            // Cache miss → debounce 200ms so rapid keyboard ↓↓↓↓ scanning
            // doesn't flood the server with intermediate fetches.
            if (_qdfCache.has(doctype, name)) {
                this.loadRow(doctype, name);
            } else {
                this.rowChangeTimer = setTimeout(() => {
                    this.loadRow(doctype, name);
                }, ROW_CHANGE_DEBOUNCE_MS);
            }
        }

        // ─── data load ──────────────────────────────────────────────────

        async loadRow(doctype, name) {
            // Pre-flight 1: if a save is currently in flight, wait for it to
            // finish (up to 2.5s). Prevents state corruption where the save
            // response would overwrite the next row's label_fields.
            const saving = this.frameEl.querySelector(".qdf-cell--saving");
            if (saving) {
                for (let i = 0; i < 50; i++) {
                    await new Promise((r) => setTimeout(r, 50));
                    if (!this.frameEl.querySelector(".qdf-cell--saving")) break;
                }
            }

            // Pre-flight 2: if the user has an unsaved edit, confirm before
            // discarding it. Skip the prompt for the row that owns the edit
            // (same parent name → re-rendering would lose the input anyway,
            // so prompt is meaningful).
            const sess = this._currentEditSession;
            if (sess && sess.dirty && !sess.committed) {
                const ok = await new Promise((resolve) => {
                    frappe.confirm(
                        __("Bỏ thay đổi chưa lưu ở dòng đang chọn?"),
                        () => resolve(true),
                        () => resolve(false),
                    );
                });
                if (!ok) return;
                // User confirmed — mark session committed so the pending edit
                // won't try to save on blur after re-render.
                sess.committed = true;
            }

            // 1. Cache hit → render synchronously, no flicker.
            const cached = _qdfCache.get(doctype, name);
            if (cached) {
                this._applyResponse(cached);
                return;
            }

            // 2. Skeleton mode: if a previous row was rendered, keep it visible
            //    while loading. Only show "Đang tải..." if frame body is empty.
            const hasPrevContent = !!this.frameEl.querySelector(".qdf-table");
            if (!hasPrevContent) {
                this._renderLoading();
            } else {
                this.frameEl.classList.add("qdf-frame--loading");
            }

            try {
                // Go through the batcher so concurrent prefetches dedupe.
                const data = await _qdfBatcher.request(doctype, name);
                this.frameEl.classList.remove("qdf-frame--loading");
                this._applyResponse(data);
            } catch (e) {
                this.frameEl.classList.remove("qdf-frame--loading");
                // Silent on navigation-induced cancellations.
                const msg = e && e.message;
                if (msg === "Cancelled" || msg === "Aborted" || msg === "Stale") return;
                this._renderMessage("⚠️ " + (msg || __("Lỗi khi tải dữ liệu")));
            }
        }

        _applyResponse(data) {
            if (!data) {
                this._renderMessage(__("Không có dữ liệu"));
                return;
            }
            this.currentParent = data.parent;
            if (!data.parent) {
                this._renderMessage(data.reason || __("Không tìm thấy chứng từ"));
                return;
            }
            if (!data.child) {
                this._renderMessage(data.reason || __("Không có bảng con phù hợp"));
                return;
            }
            this._renderHeader(data.parent);
            this._renderTable(data.child);
        }

        _renderLoading() {
            this.frameEl.querySelector(".qdf-body").innerHTML = `
                <div class="qdf-empty">⏳ ${__("Đang tải...")}</div>
            `;
        }

        _renderMessage(msg) {
            this.frameEl.querySelector(".qdf-body").innerHTML =
                `<div class="qdf-empty">${frappe.utils.escape_html(msg)}</div>`;
            this.frameEl.querySelector(".qdf-btn-open-form").style.display = "none";
            const title = this.frameEl.querySelector(".qdf-header-title");
            title.textContent = __("Khung xem nhanh");
        }

        _renderHeader(parent) {
            const title = this.frameEl.querySelector(".qdf-header-title");
            const parts = [parent.name];
            for (const fname in parent.label_fields) {
                const val = parent.label_fields[fname];
                if (val != null && val !== "") parts.push(__(this._formatHeaderValue(val)));
            }
            // textContent is safe — values are pre-stripped of HTML.
            title.textContent = parts.join(" · ");

            const openBtn = this.frameEl.querySelector(".qdf-btn-open-form");
            openBtn.href = parent.form_url;
            openBtn.style.display = "";
        }

        _formatHeaderValue(val) {
            if (typeof val === "number") {
                // Plain number formatting; avoid frappe.format which returns
                // HTML-wrapped Currency strings.
                return new Intl.NumberFormat("vi-VN").format(val);
            }
            // Strip any inline HTML from string values (defense in depth).
            return String(val).replace(/<[^>]*>/g, "").trim();
        }

        // ─── table render ───────────────────────────────────────────────

        _renderTable(child) {
            this.editControls = [];
            this.currentChild = child;
            // Re-rendering wipes any in-progress edit UI.
            this._currentEditSession = null;

            const $body = $(this.frameEl).find(".qdf-body").empty();
            const $table = $(`
                <table class="qdf-table">
                    <thead><tr></tr></thead>
                    <tbody></tbody>
                </table>
            `);
            const $tr = $table.find("thead tr");
            $tr.append(`<th class="qdf-col-idx">#</th>`);
            child.fields.forEach((f) => {
                const $th = $(`<th class="qdf-col-${cssEsc(f.fieldname)}"></th>`)
                    .text(__(f.label));
                $tr.append($th);
            });

            const $tbody = $table.find("tbody");
            child.rows.forEach((row, idx) => {
                const $row = $(`<tr class="qdf-row" data-row-name="${cssEsc(row.name)}"></tr>`);
                $row.append(`<td class="qdf-col-idx">${row.idx ?? idx + 1}</td>`);
                child.fields.forEach((f) => {
                    const editable = (row.__editable && row.__editable[f.fieldname]) === true;
                    const $td = $(`<td></td>`)
                        .addClass(editable ? "qdf-cell qdf-cell--editable" : "qdf-cell qdf-cell--locked")
                        .attr("data-fieldname", f.fieldname)
                        .attr("data-row-name", row.name)
                        .attr("tabindex", editable ? "0" : "-1");
                    const value = row[f.fieldname];
                    $td.html(this._formatCell(value, f, row));
                    if (editable) {
                        $td.on("click.qdf", (e) => {
                            // Prevent any embedded <a> (e.g. Link format) from
                            // navigating before edit mode kicks in.
                            e.preventDefault();
                            this._enterEditMode($td.get(0), f, row);
                        });
                    }
                    $row.append($td);
                });
                $tbody.append($row);
            });

            $body.append($table);
        }

        _formatCell(value, fieldMeta, row) {
            if (value == null || value === "") return "";
            try {
                // Link/Dynamic Link rendered as plain text so cell click enters
                // edit mode instead of navigating to the linked form.
                if (fieldMeta.fieldtype === "Link" || fieldMeta.fieldtype === "Dynamic Link") {
                    return frappe.utils.escape_html(String(value));
                }
                return frappe.format(value, fieldMeta, { inline: 1 }, row);
            } catch (e) {
                return frappe.utils.escape_html(String(value));
            }
        }

        // ─── edit mode ──────────────────────────────────────────────────

        _enterEditMode(cellEl, fieldMeta, row) {
            if (cellEl.classList.contains("qdf-cell--editing")) return;
            cellEl.classList.add("qdf-cell--editing");

            const oldValue = row[fieldMeta.fieldname];
            const wrapper = document.createElement("div");
            wrapper.className = "qdf-cell-control";
            cellEl.innerHTML = "";
            cellEl.appendChild(wrapper);

            // Flags + session state:
            //   initDone: blocks the initial set_value() from firing a save.
            //   dirty:    user actually typed/selected something different.
            //   committed: lock against duplicate saves (Enter+blur race).
            //   focusedOnce: the input received focus at least once (filters
            //                synthetic blur events that fire before user can interact).
            const session = {
                initDone: false, dirty: false, committed: false, focusedOnce: false,
            };
            // Track currently active edit session at instance level so
            // loadRow can detect unsaved changes before re-rendering.
            this._currentEditSession = session;

            const ctrl = frappe.ui.form.make_control({
                df: {
                    fieldname: fieldMeta.fieldname,
                    label: fieldMeta.label,
                    fieldtype: fieldMeta.fieldtype,
                    options: fieldMeta.options,
                    precision: fieldMeta.precision,
                    placeholder: fieldMeta.label,
                    change: () => {
                        // Commit on change ONLY after user has focused the
                        // input AND the new value is different from oldValue.
                        // Filters out Frappe's internal change-after-set_value
                        // and initial wrapper-render side effects.
                        if (!session.initDone || session.committed) return;
                        if (!session.focusedOnce) return;
                        const newVal = ctrl.get_value();
                        if (newVal === oldValue || (newVal == null && oldValue == null)
                            || (newVal === "" && oldValue == null)) {
                            return;
                        }
                        session.dirty = true;
                        session.committed = true;
                        this._saveCell(cellEl, fieldMeta, row, oldValue, ctrl);
                    },
                },
                parent: wrapper,
                render_input: true,
                // Render the full Frappe control wrapper (label hidden via CSS).
                // This gives Link fields their proper Awesomplete dropdown.
            });
            // Hide the auto-rendered label — the column header already labels.
            if (ctrl.$wrapper) {
                ctrl.$wrapper.find(".control-label").hide();
                ctrl.$wrapper.find(".help-box").hide();
            }
            ctrl.set_value(oldValue == null ? "" : oldValue);
            session.initDone = true;
            this.editControls.push(ctrl);

            // Focus
            setTimeout(() => {
                if (ctrl.$input && ctrl.$input.length) ctrl.$input.focus().select();
            }, 0);

            const tryCommit = (force) => {
                if (session.committed) return;
                if (!session.dirty && !force) {
                    // No change → exit without server round-trip.
                    this._exitEditMode(cellEl, fieldMeta, row, oldValue);
                    return;
                }
                session.committed = true;
                this._saveCell(cellEl, fieldMeta, row, oldValue, ctrl);
            };

            const onBlur = () => {
                if (cellEl.classList.contains("qdf-cell--saving")) return;
                // Ignore blur that fires before the user ever focused the input
                // (synthetic clicks, screen reader, etc.). Real user interaction
                // sets focusedOnce via the focus event.
                if (!session.focusedOnce) return;
                tryCommit(false);
            };
            const onFocus = () => { session.focusedOnce = true; };
            const onInput = () => { session.dirty = true; };
            const onKeydown = (e) => {
                if (e.key === "Escape") {
                    e.preventDefault();
                    e.stopPropagation();
                    session.committed = true;  // prevent blur from saving
                    this._exitEditMode(cellEl, fieldMeta, row, oldValue);
                } else if (e.key === "Enter") {
                    e.preventDefault();
                    tryCommit(true);
                } else if (e.key === "Tab") {
                    tryCommit(true);
                }
            };
            if (ctrl.$input && ctrl.$input.length) {
                ctrl.$input.on("focus.qdfedit", onFocus);
                ctrl.$input.on("blur.qdfedit", onBlur);
                ctrl.$input.on("input.qdfedit", onInput);
                ctrl.$input.on("keydown.qdfedit", onKeydown);
                ctrl.$input.on("awesomplete-selectcomplete.qdfedit", () => {
                    session.dirty = true;
                    if (!session.committed) {
                        session.committed = true;
                        this._saveCell(cellEl, fieldMeta, row, oldValue, ctrl);
                    }
                });
            }
        }

        _exitEditMode(cellEl, fieldMeta, row, valueToRender) {
            cellEl.classList.remove("qdf-cell--editing", "qdf-cell--saving");
            cellEl.innerHTML = this._formatCell(valueToRender, fieldMeta, row);
            this._currentEditSession = null;
        }

        async _saveCell(cellEl, fieldMeta, row, oldValue, ctrl, noBlur) {
            if (cellEl.classList.contains("qdf-cell--saving")) return;
            const newValue = ctrl.get_value();
            if (newValue === oldValue || (newValue === "" && oldValue == null)) {
                this._exitEditMode(cellEl, fieldMeta, row, oldValue);
                return;
            }
            cellEl.classList.add("qdf-cell--saving");

            try {
                const r = await frappe.call({
                    method: "dcnet_theme.dcnet_theme.api.quick_detail.set_cell",
                    args: {
                        parent_doctype: this.currentParent.doctype,
                        parent_name: this.currentParent.name,
                        child_doctype: this.currentChild.doctype,
                        row_name: row.name,
                        fieldname: fieldMeta.fieldname,
                        value: newValue,
                        version: this.currentParent.modified,
                    },
                });
                if (!r || !r.message || !r.message.ok) {
                    throw new Error(__("Lưu thất bại"));
                }
                // Success: update row + parent state from response
                Object.assign(row, r.message.row || {});
                this.currentParent.modified = r.message.new_version;
                this.currentParent.label_fields = r.message.parent_label_fields;
                this.currentParent.docstatus = r.message.parent_docstatus;
                // Invalidate cache so the next visit re-fetches with new data.
                _qdfCache.invalidate(this.currentParent.doctype, this.currentParent.name);

                this._renderHeader(this.currentParent);
                this._exitEditMode(cellEl, fieldMeta, row, row[fieldMeta.fieldname]);
                cellEl.classList.add("qdf-cell--saved");
                setTimeout(() => cellEl.classList.remove("qdf-cell--saved"), SAVED_INDICATOR_MS);

                // Refresh corresponding row in list view (mode=list only)
                if (this.mode === "list") {
                    this._refreshListRow(this.currentParent.doctype, this.currentParent.name);
                }
            } catch (e) {
                cellEl.classList.remove("qdf-cell--saving");
                const msg = (e && e.message) || __("Lỗi khi lưu");
                // 409 stale-version → reload whole frame
                if (/đã được cập nhật|StaleVersion|409/i.test(msg)) {
                    frappe.show_alert({
                        message: __("Chứng từ đã được cập nhật. Đang tải lại..."),
                        indicator: "orange",
                    });
                    this.loadRow(this.currentParent.doctype, this.currentParent.name);
                    return;
                }
                frappe.show_alert({ message: msg, indicator: "red" });
                this._exitEditMode(cellEl, fieldMeta, row, oldValue);
            }
        }

        async _refreshListRow(doctype, name) {
            try {
                if (!this.host || typeof this.host.refresh !== "function") return;
                // Cheapest reliable path: call host.refresh() (re-fetches current page).
                // For per-row optimization, use this.host.data lookup + redraw.
                this.host.refresh();
            } catch (e) {
                // Silent — list-view inconsistency is recoverable by user F5.
            }
        }

        // ─── keyboard navigation ────────────────────────────────────────

        _bindKeyboardNav() {
            if (this.bodyKeyListener) return;
            this.bodyKeyListener = (e) => {
                // Skip if user is editing (focus in input/textarea/etc.)
                const t = e.target;
                if (t && t.matches && t.matches(
                    "input, textarea, select, [contenteditable=true], .awesomplete input"
                )) return;
                // Only react when frame is open
                if (!this.frameEl.classList.contains("qdf-frame--open")) return;

                switch (e.key) {
                    case "ArrowDown":
                        e.preventDefault();
                        this._navigateRow(1);
                        break;
                    case "ArrowUp":
                        e.preventDefault();
                        this._navigateRow(-1);
                        break;
                    case "Home":
                        e.preventDefault();
                        this._navigateToEdge("first");
                        break;
                    case "End":
                        e.preventDefault();
                        this._navigateToEdge("last");
                        break;
                    case "Enter":
                        if (this.currentParent && this.currentParent.form_url) {
                            e.preventDefault();
                            window.open(this.currentParent.form_url, "_blank");
                        }
                        break;
                    case "Escape":
                        e.preventDefault();
                        this._clearRowSelection();
                        this._renderMessage(__("Click 1 dòng để xem chi tiết"));
                        break;
                    case "Tab":
                        // If frame has data, move focus to first editable cell.
                        if (this.currentChild) {
                            const firstEditable = this.frameEl.querySelector(
                                ".qdf-cell--editable"
                            );
                            if (firstEditable) {
                                e.preventDefault();
                                firstEditable.click();
                            }
                        }
                        break;
                }
            };
            document.addEventListener("keydown", this.bodyKeyListener, true);
        }

        _unbindKeyboardNav() {
            if (this.bodyKeyListener) {
                document.removeEventListener("keydown", this.bodyKeyListener, true);
                this.bodyKeyListener = null;
            }
        }

        _navigateRow(direction) {
            const rows = this._getNavigableRows();
            if (!rows.length) return;
            // Find current selected — match by row OR by selected descendant
            // (qdf-row-selected may land on either .list-row-container or
            // .list-row depending on prior code path).
            let cur = rows.findIndex((r) =>
                r.classList.contains("qdf-row-selected") ||
                r.querySelector(".qdf-row-selected")
            );
            const next = Math.max(0, Math.min(rows.length - 1, (cur < 0 ? 0 : cur + direction)));
            if (next === cur && cur >= 0) return;
            rows[next].click();
            rows[next].scrollIntoView({ block: "nearest", behavior: "smooth" });
        }

        _navigateToEdge(which) {
            const rows = this._getNavigableRows();
            if (!rows.length) return;
            const target = which === "first" ? rows[0] : rows[rows.length - 1];
            target.click();
            target.scrollIntoView({ block: "nearest", behavior: "smooth" });
        }

        _getNavigableRows() {
            // List view: each data row is a single .list-row-container (outer
            // wrapper). Inner .list-row would produce duplicates → only query
            // the outer. Skip the header container (no [data-name] inside).
            // Report view shares the same .list-row-container shape.
            // Query Report uses .dt-row[data-row-index].
            if (this.mode === "list") {
                return Array.from(document.querySelectorAll(".list-row-container"))
                    .filter((r) =>
                        r.offsetParent !== null &&
                        r.querySelector("[data-name][data-doctype]")
                    );
            }
            return Array.from(document.querySelectorAll(".dt-row[data-row-index]"))
                .filter((r) => r.offsetParent !== null);
        }

        // ─── responsive resize ──────────────────────────────────────────

        _bindResizeListener() {
            let t = null;
            this.resizeListener = () => {
                if (t) clearTimeout(t);
                t = setTimeout(() => this._handleResize(), 200);
            };
            window.addEventListener("resize", this.resizeListener);
        }

        _handleResize() {
            const mode = getViewportMode();
            if (mode === "mobile") {
                if (this.toggleBtn) this.toggleBtn.style.display = "none";
                this._setFrameOpen(false, /*persist=*/false);
            } else {
                if (this.toggleBtn) this.toggleBtn.style.display = "";
                this.frameEl.classList.remove("qdf-frame--desktop", "qdf-frame--tablet");
                if (this.frameEl.classList.contains("qdf-frame--open")) {
                    this.frameEl.classList.add(`qdf-frame--${mode}`);
                    document.body.classList.toggle(
                        "qdf-frame-open-desktop", mode === "desktop",
                    );
                }
            }
            this._updateLayoutOffset();
        }
    }

    // ─────────────────────────────────────────────────────────────────────
    //  Patch points
    // ─────────────────────────────────────────────────────────────────────

    function _waitFor(check, callback, maxRetries = 50, retry = 0) {
        if (check()) { callback(); return; }
        if (retry >= maxRetries) return;
        setTimeout(() => _waitFor(check, callback, maxRetries, retry + 1), 100);
    }

    const SKIP_VIEWS = ["Image", "Gantt", "Kanban", "Calendar", "Map", "Inbox"];

    function _mountList(inst) {
        if (!inst || inst.__dcnet_qdf) return;
        if (SKIP_VIEWS.includes(inst.view_name)) return;
        try {
            inst.__dcnet_qdf = new QuickDetailFrame({
                host: inst, mode: "list",
            });
        } catch (e) {
            console.warn("[dcnet_qdf] list mount failed:", e);
        }
    }

    function _mountQR(inst) {
        if (!inst || inst.__dcnet_qdf) return;
        try {
            inst.__dcnet_qdf = new QuickDetailFrame({
                host: inst, mode: "query_report",
            });
        } catch (e) {
            console.warn("[dcnet_qdf] query-report mount failed:", e);
        }
    }

    _waitFor(
        () => window.frappe && frappe.views && frappe.views.BaseList,
        () => {
            const BaseListProto = frappe.views.BaseList.prototype;
            const origSetupView = BaseListProto.setup_view;
            if (origSetupView && !origSetupView.__dcnet_qdf_patched) {
                BaseListProto.setup_view = function () {
                    const ret = origSetupView.apply(this, arguments);
                    _mountList(this);
                    return ret;
                };
                BaseListProto.setup_view.__dcnet_qdf_patched = true;
            }
        }
    );

    // Initial-page-load fallback: poll for cur_list / cur_page to mount on
    // the view that loaded BEFORE our patch (the prototype patch only catches
    // subsequent navigations). Stop polling after first mount or 10s.
    let pollStart = Date.now();
    const initialPoll = setInterval(() => {
        if (Date.now() - pollStart > 10000) { clearInterval(initialPoll); return; }
        if (!window.frappe) return;
        const inst = window.cur_list;
        if (!inst) return;

        if (inst instanceof (frappe.views.QueryReport || function(){})) {
            _mountQR(inst);
        } else if (inst instanceof (frappe.views.BaseList || function(){})) {
            _mountList(inst);
        }
        if (inst.__dcnet_qdf) clearInterval(initialPoll);
    }, 200);

    // Hook route changes:
    //   - Mount on new list/report view (in case prototype patch was bypassed)
    //   - Auto-close + remove frame when entering a Form/detail view
    //     (frame is for list browsing, not form editing)
    function _isListLikeRoute(route) {
        if (!route || !route.length) return false;
        const first = String(route[0]).toLowerCase();
        return first === "list" || first === "report" || first === "query-report" ||
               first === "tree" || first === "image" || first === "kanban" ||
               first === "calendar" || first === "gantt" || first === "dashboard-view";
    }

    function _isFormRoute(route) {
        if (!route || !route.length) return false;
        const first = String(route[0]).toLowerCase();
        return first === "form";
    }

    if (window.frappe && frappe.router) {
        frappe.router.on("change", () => {
            const route = frappe.get_route ? frappe.get_route() : null;
            // Always cancel pending prefetches on navigation — old list's
            // queue is no longer relevant.
            _qdfBatcher.clearPending();

            // Form view → tear down any visible frame + toggle button.
            if (_isFormRoute(route)) {
                document.querySelectorAll(".qdf-frame").forEach((el) => el.remove());
                document.querySelectorAll(".qdf-toggle-btn").forEach((el) => el.remove());
                document.body.classList.remove("qdf-frame-open-desktop");
                document.documentElement.style.removeProperty("--qdf-sidebar-offset");
                return;
            }
            // List-like view → defer mount.
            setTimeout(() => {
                if (window.cur_list && !window.cur_list.__dcnet_qdf) {
                    if (window.cur_list instanceof (frappe.views.QueryReport || function(){})) {
                        _mountQR(window.cur_list);
                    } else {
                        _mountList(window.cur_list);
                    }
                }
            }, 300);
        });
    }

    _waitFor(
        () => window.frappe && frappe.views && frappe.views.QueryReport,
        () => {
            const QRProto = frappe.views.QueryReport.prototype;
            const origRefresh = QRProto.refresh_report;
            if (origRefresh && !origRefresh.__dcnet_qdf_patched) {
                QRProto.refresh_report = function () {
                    const ret = origRefresh.apply(this, arguments);
                    const attach = () => _mountQR(this);
                    if (ret && typeof ret.then === "function") ret.then(attach);
                    else attach();
                    return ret;
                };
                QRProto.refresh_report.__dcnet_qdf_patched = true;
            }
        }
    );

    frappe.QuickDetailFrame = QuickDetailFrame;
    // Exposed for diagnostics / introspection. Production code MUST NOT
    // mutate _qdfCache or _qdfBatcher; treat as read-only.
    frappe.__qdf_internal = { cache: _qdfCache, batcher: _qdfBatcher };
    frappe.__dcnet_qdf_patched = true;
})();
