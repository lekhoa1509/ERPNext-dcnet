
<template>
  <div class="app-container">
    <header class="app-header">
      <div class="header-left">
        <button class="back-btn" @click="goBack">← Quay lại</button>
        <div v-if="docInfo" class="doc-meta">
          <div class="doc-title-row">
            <span class="doc-id">{{ docInfo.name }}</span>
            <span class="status-badge" :class="docInfo.status.toLowerCase()">{{ docInfo.status }}</span>
          </div>
          <div class="doc-subtitle">
            {{ docInfo.declaration_type }} · {{ docInfo.period }} · {{ docInfo.company }}
          </div>
        </div>
      </div>
      <div class="header-right">
        <div class="save-status">
          <span class="dot"></span> Đã lưu
        </div>
      </div>
    </header>

    <ActionToolbar
      :showCompare="showCompare"
      :isValidated="isValidated"
      @toggle-compare="showCompare = !showCompare"
      @fetch="handleAction('fetch')"
      @refresh="handleAction('refresh')"
      @validate="handleAction('validate')"
      @submit="handleAction('submit')"
      @export-xml="handleAction('export-xml')"
      @export-excel="handleAction('export-excel')"
    />
    
    <main class="app-main">
      <aside class="sidebar">
        <div class="sidebar-section">
          <h3>Thông tin chỉ tiêu</h3>
          <div class="legend-box">
            <div class="legend-item">
              <span class="indicator-chip auto">[21]</span>
              Hệ thống tự điền
            </div>
            <div class="legend-item">
              <span class="indicator-chip manual">⚠️ [22]</span>
              Giá trị sửa tay
            </div>
            <div class="legend-item">
              <span class="indicator-chip formula">[43]</span>
              Kết quả tính toán
            </div>
            <div class="legend-item">
              <span class="indicator-chip danger">[40]</span>
              Tiền thuế / Phải nộp
            </div>
          </div>
        </div>
        
        <div class="sidebar-section">
          <h3>Trạng thái tính toán</h3>
          <div v-if="rawData" class="stats">
            <div class="stat-row">
              <span>Tổng chỉ tiêu:</span>
              <strong>{{ Object.keys(rawData.indicators || {}).length }}</strong>
            </div>
          </div>
        </div>
      </aside>
      
      <section class="content-area">
        <div class="spreadsheet-wrapper">
        <div class="spreadsheet-content">
          <template v-if="activeTab === 0">
            <HTKKFormDynamic
              v-if="rawData"
              :data="rawData"
              :isSaving="isSaving"
              :showCompare="showCompare"
              @save="handleSaveData"
              @cancel="handleCancel"
            />
            <div v-else class="loading-state">
              <div class="spinner"></div>
              Đang tải biểu mẫu tờ khai...
            </div>
          </template>
          
          <template v-else-if="activeTab >= 1 && appendixTabs.length > 0">
            <HTKKAppendixGrid
              v-if="rawData"
              :appendixType="appendixTabs[activeTab - 1]?.type"
              :data="rawData.appendices?.[appendixTabs[activeTab - 1]?.key] || []"
            />
          </template>

          <template v-else>
            <div class="loading-state">
              Chọn một tab để xem dữ liệu
            </div>
          </template>
        </div>

          <SheetTabs
            v-if="rawData"
            v-model="activeTab"
            :tabs="computedTabs"
          />
        </div>
      </section>

      <!-- Toast Notifications -->
      <transition-group name="toast" tag="div" class="toast-container">
        <div v-for="toast in toasts" :key="toast.id" class="toast" :class="toast.type">
          <span class="toast-icon">{{ toast.type === 'success' ? '✅' : '❌' }}</span>
          {{ toast.message }}
        </div>
      </transition-group>
    </main>

    <!-- Validation Error Modal -->
    <div v-if="showValidationModal" class="modal-overlay" @click.self="showValidationModal = false">
      <div class="validation-modal">
        <div class="modal-header">
          <div class="header-icon">⚠️</div>
          <div class="header-content">
            <h3>Phát hiện lỗi tờ khai</h3>
            <p>Phát hiện {{ validationErrors.length }} vấn đề cần xử lý</p>
          </div>
          <button class="close-modal" @click="showValidationModal = false">×</button>
        </div>
        
        <div class="modal-body">
          <ul class="error-list">
            <li v-for="(err, idx) in validationErrors" :key="idx" class="error-item">
              <span class="error-bullet">•</span>
              <span class="error-text">{{ err }}</span>
            </li>
          </ul>
        </div>
        
        <div class="modal-footer">
          <button class="copy-btn" @click="handleCopyErrors">
            <span v-if="copied">✅ Đã sao chép</span>
            <span v-else>📋 Sao chép lỗi</span>
          </button>
          <button class="close-btn" @click="showValidationModal = false">Đóng</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, toRaw } from 'vue';
import HTKKFormDynamic from './components/HTKKFormDynamic.vue';
import HTKKAppendixGrid from './components/HTKKAppendixGrid.vue';
import ActionToolbar from './components/ActionToolbar.vue';
import SheetTabs from './components/SheetTabs.vue';

const rawData = ref(null);
const templateData = ref(null); // Template với appendices từ API

const showCompare = ref(false);
const activeTab = ref(0);
const docInfo = ref(null);
const isValidated = ref(false);
const isSaving = ref(false);
const toasts = ref([]);
const showValidationModal = ref(false);
const validationErrors = ref([]);
const copied = ref(false);

// Computed: danh sách phụ lục từ API (thay vì hardcode)
const appendixTabs = computed(() => {
  // Lấy appendices từ template data (đã fetch từ API)
  const appendices = templateData.value?.appendices || [];
  return appendices.map(a => ({
    type: a.type || a.label,
    key: a.key,
    label: a.label
  }));
});

// Computed: tabs hiển thị (tờ khai chính + phụ lục)
const computedTabs = computed(() => {
  const declType = docInfo.value?.declaration_type || '01/GTGT';
  const mainTab = `Tờ khai ${declType}`;
  const appendixLabels = appendixTabs.value.map(a => a.label);
  return [mainTab, ...appendixLabels];
});

let toastId = 0;
const showToast = (message, type = 'success') => {
  const id = toastId++;
  toasts.value.push({ id, message, type });
  setTimeout(() => {
    toasts.value = toasts.value.filter(t => t.id !== id);
  }, 3000);
};

const handleCopyErrors = () => {
  const text = validationErrors.value.map(e => `- ${e}`).join('\n');
  navigator.clipboard.writeText(text);
  copied.value = true;
  setTimeout(() => copied.value = false, 2000);
  showToast('Đã sao chép danh sách lỗi');
};

// Lấy ID từ HTKK_CONFIG (native mode) hoặc URL params (dev mode)
const urlParams = new URLSearchParams(window.location.search);
const currentId = ref(
  window.HTKK_CONFIG?.declarationId ||
  urlParams.get('id') ||
  ''
);

const fetchDocInfo = async (declarationId) => {
  try {
    const response = await fetch(`/api/method/dcnet_apps.htkk.api.get_declaration_info?declaration_id=${declarationId}`, { credentials: 'include' });
    const data = await response.json();
    if (data.message) {
      docInfo.value = data.message;
    }
  } catch (error) {
    console.error('Failed to fetch doc info:', error);
  }
};

const fetchRawData = async (declarationId) => {
  try {
    const response = await fetch(`/api/method/dcnet_apps.htkk.api.get_declaration_data?declaration_id=${declarationId}`, { credentials: 'include' });
    const data = await response.json();
    if (data.message) {
      rawData.value = data.message;
    }
  } catch (error) {
    console.error('Failed to fetch raw data:', error);
  }
};

// Cache CSRF token
let cachedCsrfToken = '';

const getCsrfTokenSync = () => {
  // Try multiple sources for CSRF token
  if (window.HTKK_CONFIG && window.HTKK_CONFIG.csrfToken) {
    return window.HTKK_CONFIG.csrfToken;
  }
  if (window.csrf_token) {
    return window.csrf_token;
  }
  if (window.frappe && window.frappe.csrf_token) {
    return window.frappe.csrf_token;
  }
  const cookies = document.cookie.split('; ');
  for (const cookie of cookies) {
    if (cookie.startsWith('csrf_token=') || cookie.startsWith('frappe_csrf_token=')) {
      return cookie.split('=')[1];
    }
  }
  return cachedCsrfToken;
};

const fetchCsrfToken = async () => {
  // First try sync sources
  const syncToken = getCsrfTokenSync();
  if (syncToken) {
    cachedCsrfToken = syncToken;
    return syncToken;
  }
  // Fetch from API
  try {
    const response = await fetch('/api/method/dcnet_apps.htkk.api.get_csrf_token', {
      credentials: 'include'
    });
    const data = await response.json();
    if (data.message && data.message.csrf_token) {
      cachedCsrfToken = data.message.csrf_token;
      return cachedCsrfToken;
    }
  } catch (e) {
    console.error('Failed to fetch CSRF token:', e);
  }
  return '';
};

const handleSaveData = async (indicators) => {
  isSaving.value = true;
  try {
    // Unwrap Vue reactive proxy to plain object
    const plainIndicators = toRaw(indicators);
    const declarationId = currentId.value;

    // Debug logging
    console.log('Save request:', {
      declaration_id: declarationId,
      indicators: plainIndicators
    });

    // Use frappe.call if available (Desk mode), otherwise use fetch
    if (window.frappe && window.frappe.call) {
      // Frappe Desk mode - use frappe.call (handles CSRF automatically)
      window.frappe.call({
        method: 'dcnet_apps.htkk.api.save_declaration_data',
        args: {
          declaration_id: declarationId,
          indicators: plainIndicators
        },
        callback: (r) => {
          if (r.message && r.message.status === 'success') {
            showToast('Đã lưu dữ liệu tờ khai!');
            fetchRawData(declarationId);
          } else {
            showToast('Có lỗi khi lưu dữ liệu', 'error');
          }
          isSaving.value = false;
        },
        error: (err) => {
          console.error('Save error:', err);
          showToast('Lỗi kết nối server', 'error');
          isSaving.value = false;
        }
      });
    } else {
      // Standalone mode - use fetch with JSON body
      // Fetch CSRF token first
      const csrfToken = await fetchCsrfToken();
      console.log('Using CSRF token:', csrfToken ? csrfToken.substring(0, 10) + '...' : '(none)');

      const response = await fetch(`/api/method/dcnet_apps.htkk.api.save_declaration_data`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'X-Frappe-CSRF-Token': csrfToken
        },
        credentials: 'include',
        body: JSON.stringify({
          declaration_id: declarationId,
          indicators: plainIndicators
        })
      });

      // Debug response
      console.log('Save response status:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Save error response:', errorText);
        showToast('Có lỗi khi lưu dữ liệu', 'error');
        return;
      }

      const data = await response.json();
      if (data.message && data.message.status === 'success') {
        showToast('Đã lưu dữ liệu tờ khai!');
        fetchRawData(declarationId);
      } else {
        console.error('Save error:', data);
        showToast('Có lỗi khi lưu dữ liệu', 'error');
      }
    }
  } catch (error) {
    console.error('Save exception:', error);
    showToast('Lỗi kết nối server', 'error');
  } finally {
    if (!window.frappe || !window.frappe.call) {
      isSaving.value = false;
    }
  }
};

const handleCancel = () => {
  fetchRawData(currentId.value);
  isValidated.value = false;
  showToast('Đã hủy các thay đổi');
};

const goBack = () => {
  // Navigate back to list page
  window.location.href = '/htkk_list';
};

const handleAction = async (action) => {
  console.log('Action triggered:', action);
  
  if (action === 'export-xml') {
    try {
      const response = await fetch(`/api/method/dcnet_apps.htkk.api.export_declaration?declaration_id=${currentId.value}`, { credentials: 'include' });
      const data = await response.json();
      
      if (data.message && data.message.file_url) {
        window.open(data.message.file_url, '_blank');
        fetchDocInfo(currentId.value);
        showToast('Xuất XML thành công!');
      } else {
        showToast('Có lỗi xảy ra khi xuất XML', 'error');
      }
    } catch (error) {
      showToast('Lỗi kết nối server', 'error');
    }
  } else if (action === 'submit') {
    try {
      const response = await fetch(`/api/method/dcnet_apps.htkk.api.submit_declaration?declaration_id=${currentId.value}`, { credentials: 'include' });
      const data = await response.json();
      
      if (data.message && data.message.status === 'success') {
        fetchDocInfo(currentId.value);
        showToast('Đã gửi duyệt tờ khai thành công!');
      } else {
        showToast('Có lỗi xảy ra khi gửi duyệt', 'error');
      }
    } catch (error) {
      showToast('Lỗi kết nối server', 'error');
    }
  } else if (action === 'fetch') {
    try {
      showToast('Đang tính toán dữ liệu...', 'success');
      const response = await fetch(`/api/method/dcnet_apps.htkk.api.calculate_declaration?declaration_id=${currentId.value}`, { credentials: 'include' });
      const data = await response.json();
      
      if (data.message && data.message.status === 'success') {
        isValidated.value = false; // Reset sau khi tính toán mới
        showToast('Đã tính toán xong các chỉ tiêu!');
        fetchRawData(currentId.value);
      } else {
        showToast('Có lỗi xảy ra khi tính toán', 'error');
      }
    } catch (error) {
      showToast('Lỗi kết nối server', 'error');
    }
  } else if (action === 'validate') {
    try {
      const response = await fetch(`/api/method/dcnet_apps.htkk.api.validate_declaration?declaration_id=${currentId.value}`, { credentials: 'include' });
      const data = await response.json();

      if (data.message && data.message.status === 'success') {
        isValidated.value = true;
        showToast('Tờ khai hợp lệ!');
      } else if (data.message && data.message.errors) {
        isValidated.value = false;
        validationErrors.value = data.message.errors;
        showValidationModal.value = true;
      } else {
        isValidated.value = false;
        showToast('Có lỗi xảy ra khi kiểm tra', 'error');
      }
    } catch (error) {
      showToast('Lỗi kết nối server', 'error');
    }
  } else if (action === 'export-excel') {
    try {
      showToast('Đang xuất Excel...');
      // Use window.open for binary download
      window.open(`/api/method/dcnet_apps.htkk.api.export_declaration_excel?declaration_id=${currentId.value}`, '_blank');
      showToast('Đã tải xuống file Excel!');
    } catch (error) {
      showToast('Lỗi kết nối server', 'error');
    }
  }
};

// Fetch template data (bao gồm appendices) từ API
const fetchTemplateData = async (declarationType) => {
  try {
    const response = await fetch(`/api/method/dcnet_apps.htkk.api.get_declaration_template?declaration_type=${encodeURIComponent(declarationType)}`, { credentials: 'include' });
    const data = await response.json();
    if (data.message) {
      templateData.value = data.message;
    }
  } catch (error) {
    console.error('Failed to fetch template data:', error);
  }
};

onMounted(async () => {
  await fetchDocInfo(currentId.value);
  // Sau khi có docInfo, fetch template data để lấy appendices
  if (docInfo.value?.declaration_type) {
    await fetchTemplateData(docInfo.value.declaration_type);
  }
  await fetchRawData(currentId.value);
});
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap');

:root {
  --primary: #1a237e;
  --secondary: #0288d1;
  --bg: #f0f2f5;
  --surface: rgba(255, 255, 255, 0.9);
  --border: rgba(226, 232, 240, 0.8);
  --text: #1e293b;
  --text-muted: #64748b;
  --success: #10b981;
  --warning: #f59e0b;
  --danger: #ef4444;
  --accent: #6366f1;
}

body {
  margin: 0;
  font-family: 'Outfit', 'Inter', sans-serif;
  background-color: var(--bg);
  background-image: 
    radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
    radial-gradient(at 100% 0%, rgba(2, 136, 209, 0.1) 0px, transparent 50%);
  color: var(--text);
  -webkit-font-smoothing: antialiased;
}

.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  overflow-x: hidden; /* Prevent horizontal scroll/jitter */
}

.app-header {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  padding: 0 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 64px;
  flex-shrink: 0;
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.back-btn {
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  font-size: 13px;
  padding: 8px 12px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.back-btn:hover {
  background: rgba(99, 102, 241, 0.1);
  color: var(--accent);
}

.doc-meta {
  display: flex;
  flex-direction: column;
}

.doc-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.doc-id {
  font-weight: 700;
  font-size: 16px;
  color: #2c3e50;
}

.status-badge {
  font-size: 11px;
  font-weight: 600;
  padding: 2px 10px;
  border-radius: 12px;
  text-transform: capitalize;
}

.status-badge.draft { background: #EBF5FB; color: var(--secondary); }
.status-badge.pending { background: #FEF9E7; color: var(--warning); }
.status-badge.submitted { background: #EAFAF1; color: var(--success); }

.doc-subtitle {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 2px;
}

.save-status {
  font-size: 11px;
  color: var(--success);
  display: flex;
  align-items: center;
  gap: 6px;
}

.save-status .dot {
  width: 6px;
  height: 6px;
  background: var(--success);
  border-radius: 50%;
}

.app-main {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.sidebar {
  width: 280px;
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(8px);
  border-right: 1px solid var(--border);
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 32px;
  transition: all 0.3s ease;
}

.sidebar-section {
  animation: slideInLeft 0.5s ease-out;
}

@keyframes slideInLeft {
  from { opacity: 0; transform: translateX(-20px); }
  to { opacity: 1; transform: translateX(0); }
}

.sidebar-section h3 {
  margin: 0 0 12px 0;
  font-size: 12px;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.legend-box {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--text);
}

.indicator-chip {
  padding: 2px 8px;
  border-radius: 6px;
  font-family: 'Outfit', sans-serif;
  font-weight: 700;
  font-size: 11px;
  min-width: 44px;
  text-align: center;
  border: 1px solid transparent;
  transition: all 0.2s ease;
}

.indicator-chip.auto { 
  background: #eef2ff; 
  border-color: #e0e7ff; 
  color: #4f46e5; 
}

.indicator-chip.manual { 
  background: #fffbeb; 
  border-color: #fef3c7; 
  color: #d97706; 
}

.indicator-chip.formula { 
  background: #ecfdf5; 
  border-color: #d1fae5; 
  color: #059669; 
}

.indicator-chip.danger { 
  background: #fff1f2; 
  border-color: #ffe4e6; 
  color: #e11d48; 
}

.legend-item:hover .indicator-chip {
  transform: scale(1.1);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.content-area {
  flex: 1;
  padding: 16px;
  overflow: hidden;
  overflow-x: hidden; /* Block horizontal overflow */
  display: flex;
  flex-direction: column;
  min-width: 0; /* Prevent flex children from stretching beyond parent */
}

.spreadsheet-wrapper {
  background: white;
  border: 1px solid var(--border);
  border-radius: 12px;
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
  min-width: 0;
  min-height: 0;
}

.spreadsheet-content {
  flex: 1;
  overflow-y: auto;
  position: relative;
  display: flex;
  flex-direction: column;
}

/* Removed :hover box-shadow transition - it was triggering layout recalcs */

.loading-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  color: var(--text-muted);
  font-size: 14px;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid var(--secondary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Toast System */
.toast-container {
  position: fixed;
  top: 24px;
  right: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  z-index: 1000;
}

.toast {
  padding: 12px 24px;
  border-radius: 12px;
  background: white;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 600;
  font-size: 14px;
  min-width: 250px;
  border-left: 4px solid var(--accent);
}

.toast.success { border-left-color: var(--success); color: var(--success); }
.toast.error { border-left-color: var(--danger); color: var(--danger); }

.toast-enter-active, .toast-leave-active {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.toast-enter-from { opacity: 0; transform: translateX(100px); }
.toast-enter-from { opacity: 0; transform: translateX(100px); }
.toast-leave-to { opacity: 0; transform: scale(0.9); }

/* Modal Styles */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.4);
  backdrop-filter: blur(4px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.validation-modal {
  background: white;
  width: 100%;
  max-width: 600px;
  border-radius: 20px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  overflow: hidden;
  animation: modalPop 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes modalPop {
  from { transform: scale(0.95); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.modal-header {
  padding: 24px;
  background: #fff5f5;
  border-bottom: 1px solid #fee2e2;
  display: flex;
  align-items: center;
  gap: 16px;
  position: relative;
}

.header-icon {
  font-size: 32px;
}

.modal-header h3 {
  margin: 0;
  color: #991b1b;
  font-size: 18px;
  font-weight: 700;
}

.modal-header p {
  margin: 4px 0 0 0;
  color: #b91c1c;
  font-size: 13px;
  opacity: 0.8;
}

.close-modal {
  position: absolute;
  top: 16px;
  right: 16px;
  background: transparent;
  border: none;
  font-size: 24px;
  color: #991b1b;
  cursor: pointer;
  opacity: 0.5;
  transition: opacity 0.2s;
}

.close-modal:hover { opacity: 1; }

.modal-body {
  padding: 24px;
  max-height: 400px;
  overflow-y: auto;
}

.error-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.error-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  background: #fffafb;
  border-radius: 10px;
  border: 1px solid #fff1f2;
}

.error-bullet {
  color: #ef4444;
  font-weight: bold;
}

.error-text {
  font-size: 14px;
  line-height: 1.5;
  color: #374151;
  font-family: 'JetBrains Mono', 'Monaco', monospace;
}

.modal-footer {
  padding: 16px 24px;
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.copy-btn {
  padding: 10px 20px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.copy-btn:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
  color: #475569;
}

.close-btn {
  padding: 10px 24px;
  background: #1e293b;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #0f172a;
}
</style>
