(function () {
	"use strict";

	const API_METHOD = "dcnet_apps.notifications.get_unread_summary";
	const BADGE_CLASS = "dcnet-notification-badge";
	const NOTIFICATION_STORAGE_PREFIX = "dcnet_notification_shown_";
	const TITLE_PREFIX_RE = /^\(\d+\)\s+/;

	let lastUnreadCount = 0;
	let originalTitle = document.title;
	let refreshTimer = null;
	let realtimeBound = false;
	let hasFocus = !document.hidden;

	function callAfterReady(fn, retry = 0) {
		if (window.frappe?.session?.user && frappe.session.user !== "Guest" && frappe.call) {
			fn();
			return;
		}
		if (retry < 40) {
			setTimeout(() => callAfterReady(fn, retry + 1), 250);
		}
	}

	function findNotificationTriggers() {
		return $(
			[
				".desktop-notifications .dropdown-notifications > button",
				".desktop-notifications .dropdown-notifications > .dropdown-toggle",
				".desktop-notifications .btn-reset.nav-link",
				".sidebar-notification .standard-sidebar-item",
				".sidebar-notification .item-anchor",
				".sidebar-notification",
			].join(",")
		);
	}

	function ensureBadge($target) {
		if (!$target.length) return $();
		$target.addClass("dcnet-notification-anchor");
		let $badge = $target.children(`.${BADGE_CLASS}`).first();
		if (!$badge.length) {
			$badge = $(`<span class="${BADGE_CLASS}" aria-label="${__("Unread notifications")}"></span>`);
			$target.append($badge);
		}
		return $badge;
	}

	function updateBadge(count) {
		const displayValue = count > 99 ? "99+" : String(count);
		findNotificationTriggers().each(function () {
			const $badge = ensureBadge($(this));
			$badge.text(displayValue).css("display", count > 0 ? "inline-flex" : "none");
		});

		document.title = count > 0 ? `(${displayValue}) ${originalTitle.replace(TITLE_PREFIX_RE, "")}` : originalTitle.replace(TITLE_PREFIX_RE, "");
		lastUnreadCount = count;
	}

	function shouldShowBrowserNotification(item) {
		if (!item?.name) return false;
		if (!document.hidden && hasFocus) return false;

		const key = `${NOTIFICATION_STORAGE_PREFIX}${item.name}`;
		if (localStorage.getItem(key)) return false;
		localStorage.setItem(key, String(Date.now()));
		return true;
	}

	function stripHtml(value) {
		return $("<div>").html(value || "").text().replace(/\s+/g, " ").trim();
	}

	function getNotificationLink(item) {
		if (item?.link) return item.link;
		if (item?.document_type && item?.document_name) {
			return frappe.utils.get_form_link(item.document_type, item.document_name);
		}
		return "/app/List/Notification Log";
	}

	function showInAppToast(item) {
		const subject = stripHtml(item?.subject) || __("Bạn có thông báo mới");
		if (frappe.show_alert) {
			frappe.show_alert({
				message: item?.is_order_notification ? __("Bạn có thông báo đơn hàng mới") : subject,
				indicator: item?.is_order_notification ? "orange" : "blue",
			}, 7);
		}
	}

	function showBrowserNotification(item) {
		if (!("Notification" in window) || !shouldShowBrowserNotification(item)) return;

		const title = item.is_order_notification
			? __("Bạn có thông báo đơn hàng mới")
			: __("Bạn có thông báo mới");
		const body = stripHtml(item.subject) || [item.document_type, item.document_name].filter(Boolean).join(" ");

		const openNotification = () => {
			const notification = new Notification(title, {
				body,
				icon: "/assets/dcnet_apps/images/favicon.png",
				tag: item.name,
				renotify: true,
			});
			notification.onclick = function () {
				window.focus();
				window.location.href = getNotificationLink(item);
				notification.close();
			};
		};

		if (Notification.permission === "granted") {
			openNotification();
		} else if (Notification.permission === "default") {
			Notification.requestPermission().then((permission) => {
				if (permission === "granted" && (document.hidden || !hasFocus)) {
					openNotification();
				}
			});
		}
	}

	function refreshBadge({ notify = false } = {}) {
		clearTimeout(refreshTimer);
		refreshTimer = setTimeout(() => {
			frappe.call({
				method: API_METHOD,
				args: { limit: 1 },
				type: "GET",
				callback(r) {
					const summary = r.message || {};
					const count = cint(summary.unread_count || 0);
					const latest = summary.latest;
					const grew = count > lastUnreadCount;
					updateBadge(count);

					if (notify && latest && grew) {
						if (document.hidden || !hasFocus) {
							showBrowserNotification(latest);
						} else {
							showInAppToast(latest);
						}
					}
				},
			});
		}, 150);
	}

	function bindRealtime() {
		if (realtimeBound || !frappe.realtime?.on) return;
		realtimeBound = true;
		frappe.realtime.on("notification", () => refreshBadge({ notify: true }));
		frappe.realtime.on("indicator_hide", () => refreshBadge());
	}

	function bindClicks() {
		$(document).on(
			"click",
			[
				".mark-as-read",
				".mark-all-read",
				".notification-item",
				".desktop-notifications .dropdown-notifications > button",
				".sidebar-notification",
			].join(","),
			() => {
				if ("Notification" in window && Notification.permission === "default") {
					Notification.requestPermission();
				}
				setTimeout(() => refreshBadge(), 600);
			}
		);
	}

	function init() {
		originalTitle = document.title;
		bindRealtime();
		bindClicks();
		refreshBadge();
		setInterval(() => refreshBadge(), 60000);
	}

	window.addEventListener("focus", () => {
		hasFocus = true;
		refreshBadge();
	});
	window.addEventListener("blur", () => {
		hasFocus = false;
	});
	document.addEventListener("visibilitychange", () => {
		hasFocus = !document.hidden;
		refreshBadge();
	});

	$(document).on("toolbar_setup page-change", () => callAfterReady(refreshBadge));
	$(document).ready(() => callAfterReady(init));
})();
