
<template>
  <div class="sheet-tabs">
    <button 
      v-for="(tab, index) in tabs" 
      :key="index"
      class="tab-btn"
      :class="{ active: modelValue === index }"
      @click="$emit('update:modelValue', index)"
    >
      {{ tab }}
    </button>
  </div>
</template>

<script setup>
defineProps({
  tabs: {
    type: Array,
    required: true
  },
  modelValue: {
    type: Number,
    default: 0
  }
});

defineEmits(['update:modelValue']);
</script>

<style scoped>
.sheet-tabs {
  display: flex;
  background: rgba(248, 250, 252, 0.8);
  border-top: 1px solid rgba(226, 232, 240, 0.8);
  padding: 4px 12px;
  gap: 4px;
  overflow-x: auto;
  scrollbar-width: none;
}

.tab-btn {
  padding: 8px 16px;
  font-size: 12px;
  font-weight: 500;
  color: #64748b;
  background: transparent;
  border: none;
  cursor: pointer;
  border-radius: 8px;
  white-space: nowrap;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid transparent;
  font-family: inherit;
}

.tab-btn:hover {
  background: rgba(255, 255, 255, 0.8);
  color: #1a237e;
}

.tab-btn.active {
  background: white;
  color: #1a237e;
  font-weight: 600;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
  border: 1px solid rgba(226, 232, 240, 1);
}
</style>
