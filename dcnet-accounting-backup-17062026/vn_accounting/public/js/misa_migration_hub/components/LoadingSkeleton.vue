<template>
	<div :class="['loading-skeleton', `variant-${variant}`]">
		<div
			v-for="i in count"
			:key="i"
			class="sk-row"
			:style="{ animationDelay: `${(i - 1) * 80}ms` }"
		>
			<div v-for="c in cols" :key="c" class="sk-cell"></div>
		</div>
	</div>
</template>

<script setup>
defineProps({
	count: { type: Number, default: 5 },
	cols: { type: Number, default: 4 },
	// "table" — full-width grid; "list" — single column rows; "card" — taller
	variant: { type: String, default: "table" },
});
</script>

<style scoped>
.loading-skeleton {
	width: 100%;
	display: flex;
	flex-direction: column;
	gap: 6px;
}
.sk-row {
	display: grid;
	gap: 8px;
	animation: skeleton-shimmer 1.4s ease-in-out infinite;
}
.variant-table .sk-row {
	grid-template-columns: repeat(var(--cols, 4), 1fr);
}
.variant-list .sk-row { grid-template-columns: 1fr; }
.variant-card .sk-row { grid-template-columns: 1fr; }
.variant-card .sk-cell { height: 56px; }
.sk-cell {
	background: linear-gradient(
		90deg,
		#f3f4f6 0%, #e5e7eb 50%, #f3f4f6 100%
	);
	background-size: 200% 100%;
	border-radius: 4px;
	height: 18px;
	animation: skeleton-shimmer 1.4s ease-in-out infinite;
}
@keyframes skeleton-shimmer {
	0%   { background-position: 200% 0; opacity: 0.6; }
	50%  { background-position: 0 0; opacity: 1; }
	100% { background-position: -200% 0; opacity: 0.6; }
}
</style>
