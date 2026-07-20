
<script setup>
defineProps({
  showCompare: Boolean,
  isValidated: Boolean
});

defineEmits(['fetch', 'refresh', 'toggle-compare', 'validate', 'submit', 'export-xml', 'export-excel']);
</script>

<template>
  <div class="action-toolbar shadow-sm">
    <div class="toolbar-section">
      <button class="btn btn-primary shadow-sm" @click="$emit('fetch')">
        <span class="icon">📥</span> Lấy dữ liệu
      </button>
      <button class="btn btn-ghost" @click="$emit('refresh')">
        <span class="icon">🔄</span> Lấy lại
      </button>
      <button 
        class="btn btn-ghost" 
        :class="{ active: showCompare }"
        @click="$emit('toggle-compare')"
      >
        <span class="icon">📋</span> {{ showCompare ? 'Tắt so sánh' : 'So sánh với DL gốc' }}
      </button>
    </div>
    
    <div class="toolbar-section gap-3">
      <button 
        class="btn btn-validate" 
        :class="{ 'validated-success': isValidated }"
        @click="$emit('validate')"
      >
        <span class="icon">{{ isValidated ? '✅' : '🔍' }}</span> 
        {{ isValidated ? 'Đã Validate' : 'Validate' }}
      </button>

      <div class="h-8 w-px bg-slate-200 self-center mx-1"></div>

      <button 
        class="btn btn-secondary" 
        :disabled="!isValidated"
        :title="!isValidated ? 'Cần validate thành công trước khi gửi duyệt' : ''"
        @click="$emit('submit')"
      >
        <span class="icon">📤</span> Gửi duyệt
      </button>
      <button
        class="btn btn-success"
        :disabled="!isValidated"
        :title="!isValidated ? 'Cần validate thành công trước khi xuất XML' : ''"
        @click="$emit('export-xml')"
      >
        <span class="icon">📄</span> Xuất XML
      </button>
      <button
        class="btn btn-excel"
        @click="$emit('export-excel')"
      >
        <span class="icon">📊</span> Xuất Excel
      </button>
    </div>
  </div>
</template>

<style scoped>
.action-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 16px;
  background: white;
  border-bottom: 1px solid #dee2e6;
  gap: 12px;
}

.toolbar-section {
  display: flex;
  gap: 8px;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  border: 1px solid transparent;
  transition: all 0.2s;
  font-family: inherit;
}

.btn .icon {
  font-size: 14px;
}

.btn-primary {
  background: #1b4f72;
  color: white;
}

.btn-primary:hover {
  background: #153e5a;
}

.btn-secondary {
  background: white;
  color: #1b4f72;
  border-color: #1b4f72;
}

.btn-secondary:hover {
  background: #f8f9fa;
}

.btn-ghost {
  background: transparent;
  color: #7f8c8d;
  border-color: #dee2e6;
}

.btn-ghost:hover {
  background: #f8f9fa;
  color: #2c3e50;
}

.btn-ghost.active {
  background: #eef2ff;
  border-color: #1b4f72;
  color: #1b4f72;
}

.btn-validate {
  background: white;
  border-color: #e2e8f0;
  color: #64748b;
}

.btn-validate:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.btn-validate.validated-success {
  background: #f0fdf4;
  border-color: #4ade80;
  color: #166534;
}

.btn-success {
  background: #166534;
  color: white;
}

.btn-success:hover:not(:disabled) {
  background: #14532d;
}

.btn-excel {
  background: #217346;
  color: white;
}

.btn-excel:hover {
  background: #1a5c38;
}

.btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  filter: grayscale(1);
}
</style>
