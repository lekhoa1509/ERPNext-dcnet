<template>
	<div v-if="open" class="preflight-dialog-overlay" @click.self="$emit('close')">
		<div class="preflight-dialog">
			<header>
				<h3>{{ __("Pre-flight kiểm tra trước khi tạo") }}</h3>
				<button class="close" @click="$emit('close')">×</button>
			</header>

			<div class="status-banner" :class="statusClass">
				<strong>{{ statusLabel }}</strong>
				<span v-if="data?.issue_count > 0">
					— {{ data.issue_count }} {{ __("vấn đề") }}
					({{ data.block_count || 0 }} {{ __("chặn") }},
					{{ data.warn_count || 0 }} {{ __("cảnh báo") }})
				</span>
			</div>

			<div class="checks">
				<div
					v-for="c in data?.checks || []"
					:key="c.name"
					:class="['check', c.passed ? 'ok' : c.level]"
				>
					<div class="check-head">
						<span class="icon">{{ iconFor(c) }}</span>
						<span class="label">{{ c.label }}</span>
						<span class="level-badge" :class="c.level">{{ c.level }}</span>
					</div>
					<ul v-if="c.issues && c.issues.length" class="issues">
						<li v-for="(iss, i) in c.issues" :key="i">{{ iss }}</li>
					</ul>
				</div>
			</div>

			<footer>
				<button class="btn btn-link" @click="$emit('close')">
					{{ __("Đóng") }}
				</button>
				<button
					v-if="canProceed"
					class="btn btn-primary"
					@click="$emit('confirm')"
				>
					{{ data?.warn_count > 0
						? __("Vẫn tiếp tục tạo")
						: __("Tiếp tục tạo") }}
				</button>
				<span v-else class="blocked-hint">
					{{ __("Sửa các mục chặn ở trên trước khi tạo.") }}
				</span>
			</footer>
		</div>
	</div>
</template>

<script setup>
import { computed } from "vue";

function __(t) { return typeof window.__ === "function" ? window.__(t) : t; }

const props = defineProps({
	open: { type: Boolean, default: false },
	data: { type: Object, default: null },
});

defineEmits(["close", "confirm"]);

const statusClass = computed(() => {
	const s = props.data?.status || (props.data?.phase_d_status);
	return s === "block" ? "block" : s === "warn" ? "warn" : "ok";
});

const statusLabel = computed(() => {
	const s = props.data?.status || (props.data?.phase_d_status);
	if (s === "block") return __("Có vấn đề chặn — không thể tiếp tục");
	if (s === "warn") return __("Có cảnh báo — kiểm tra trước khi tiếp tục");
	return __("Sẵn sàng tạo");
});

const canProceed = computed(() => {
	const s = props.data?.status || props.data?.phase_d_status;
	return s !== "block";
});

function iconFor(c) {
	if (c.passed) return "✓";
	if (c.level === "block") return "⛔";
	if (c.level === "warn") return "⚠";
	return "ℹ";
}
</script>

<style scoped>
.preflight-dialog-overlay {
	position: fixed; inset: 0;
	background: rgba(0,0,0,0.4);
	display: flex; align-items: center; justify-content: center;
	z-index: 999;
}
.preflight-dialog {
	background: white;
	border-radius: 10px;
	width: min(720px, 92vw);
	max-height: 86vh;
	display: flex; flex-direction: column;
	box-shadow: 0 24px 60px rgba(0,0,0,0.2);
	overflow: hidden;
}
header {
	padding: 14px 18px;
	border-bottom: 1px solid #e5e7eb;
	display: flex; justify-content: space-between; align-items: center;
}
header h3 { margin: 0; font-size: 16px; }
.close {
	background: none; border: none; font-size: 26px; line-height: 1;
	cursor: pointer; color: #6b7280;
}
.status-banner {
	padding: 10px 18px; font-size: 13px;
	border-bottom: 1px solid #e5e7eb;
}
.status-banner.ok    { background: #ecfdf5; color: #065f46; }
.status-banner.warn  { background: #fffbeb; color: #92400e; }
.status-banner.block { background: #fef2f2; color: #991b1b; }

.checks { overflow-y: auto; padding: 12px 18px; flex: 1; }
.check {
	padding: 10px 12px;
	border-radius: 6px;
	margin-bottom: 8px;
	border: 1px solid #e5e7eb;
}
.check.ok    { background: #f9fafb; }
.check.warn  { background: #fffbeb; border-color: #fef3c7; }
.check.block { background: #fef2f2; border-color: #fecaca; }
.check.info  { background: #eff6ff; border-color: #dbeafe; }
.check-head {
	display: flex; align-items: center; gap: 8px;
	font-size: 13px; font-weight: 500;
}
.check-head .icon { font-size: 16px; }
.check-head .label { flex: 1; }
.level-badge {
	font-size: 10px; padding: 2px 6px; border-radius: 8px;
	text-transform: uppercase; font-weight: 600;
}
.level-badge.block { background: #991b1b; color: white; }
.level-badge.warn  { background: #c2410c; color: white; }
.level-badge.info  { background: #2563eb; color: white; }
.issues {
	margin: 6px 0 0 22px; padding: 0;
	font-size: 12px; color: #4b5563;
	max-height: 140px; overflow-y: auto;
}
.issues li { padding: 1px 0; }

footer {
	padding: 12px 18px;
	border-top: 1px solid #e5e7eb;
	display: flex; justify-content: flex-end; align-items: center; gap: 10px;
}
.btn { padding: 6px 14px; border-radius: 4px; cursor: pointer; border: none; font-size: 13px; }
.btn-primary { background: #2563eb; color: white; }
.btn-primary:hover { background: #1d4ed8; }
.btn-link { background: transparent; color: #6b7280; }
.blocked-hint { font-size: 12px; color: #991b1b; }
</style>
