<template>
	<div class="empty-state">
		<div class="es-icon">{{ icon }}</div>
		<div class="es-title">{{ title }}</div>
		<div v-if="hint" class="es-hint">{{ hint }}</div>
		<button
			v-if="actionLabel"
			class="btn btn-primary"
			@click="$emit('action')"
		>
			{{ actionLabel }}
		</button>
	</div>
</template>

<script setup>
defineProps({
	icon: { type: String, default: "📋" },
	title: { type: String, required: true },
	hint: { type: String, default: "" },
	actionLabel: { type: String, default: "" },
});
defineEmits(["action"]);
</script>

<style scoped>
.empty-state {
	padding: 36px 16px;
	text-align: center;
	color: var(--text-muted, #6b7280);
	display: flex;
	flex-direction: column;
	gap: 6px;
	align-items: center;
}
.es-icon {
	font-size: 36px;
	line-height: 1;
	opacity: 0.55;
	margin-bottom: 4px;
}
.es-title {
	font-size: 14px;
	color: var(--text-color, #374151);
	font-weight: 500;
}
.es-hint {
	font-size: 12px;
	color: #9ca3af;
	max-width: 380px;
}
.btn-primary {
	margin-top: 12px;
	background: #2563eb; color: white; border: none;
	padding: 6px 14px; border-radius: 4px; cursor: pointer; font-size: 13px;
}
.btn-primary:hover { background: #1d4ed8; }
</style>
