import { io } from "socket.io-client"

// Port is injected at runtime via frappe.boot.socketio_port (set server-side, see frappe/public/js/frappe/socketio_client.js).
// Avoid importing common_site_config.json at build time: when this app is symlinked into a
// frappe-bench (apps/hrms -> /workspace/dcnet_hrms), Vite resolves relative paths from the
// real filesystem location and cannot find ../../../../sites/common_site_config.json.
const socketio_port = (typeof window !== "undefined" && window.frappe?.boot?.socketio_port) || 9000

import { getCachedListResource } from "frappe-ui/src/resources/listResource"
import { getCachedResource } from "frappe-ui/src/resources/resources"

export function initSocket() {
	let host = window.location.hostname
	let siteName = window.site_name
	let port = window.location.port ? `:${socketio_port}` : ""
	let protocol = port ? "http" : "https"
	let url = `${protocol}://${host}${port}/${siteName}`
	let socket = io(url, {
		withCredentials: true,
		reconnectionAttempts: 5,
	})

	socket.on("hrms:refetch_resource", (data) => {
		if (data.cache_key) {
			let resource =
				getCachedResource(data.cache_key) ||
				getCachedListResource(data.cache_key)

			if (resource) {
				resource.reload()
			}
		}
	})

	return socket
}
