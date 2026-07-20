<template>
  <div class="list-app">
    <!-- Header -->
    <header class="app-header">
      <div class="header-left">
        <a href="/app" class="back-btn">← Desk</a>
        <div class="app-title">
          <h1>HTKK - Quản lý tờ khai thuế</h1>
          <p>Hỗ trợ kê khai thuế điện tử theo TT80/2021/TT-BTC</p>
        </div>
      </div>
      <div class="header-right">
        <div class="user-info" v-if="userInfo">
          <span class="user-name">{{ userInfo.full_name }}</span>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="app-main">
      <DeclarationList
        ref="listRef"
        @view="handleView"
        @create="showCreateModal = true"
      />
    </main>

    <!-- Create Modal -->
    <CreateDeclarationModal
      v-if="showCreateModal"
      @close="showCreateModal = false"
      @created="handleCreated"
    />

    <!-- Toast Notifications -->
    <transition-group name="toast" tag="div" class="toast-container">
      <div v-for="toast in toasts" :key="toast.id" class="toast" :class="toast.type">
        <span class="toast-icon">{{ toast.type === 'success' ? '✅' : '❌' }}</span>
        {{ toast.message }}
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import DeclarationList from './components/DeclarationList.vue';
import CreateDeclarationModal from './components/CreateDeclarationModal.vue';

// State
const listRef = ref(null);
const showCreateModal = ref(false);
const userInfo = ref(null);
const toasts = ref([]);
let toastId = 0;

// Methods
const showToast = (message, type = 'success') => {
  const id = toastId++;
  toasts.value.push({ id, message, type });
  setTimeout(() => {
    toasts.value = toasts.value.filter(t => t.id !== id);
  }, 3000);
};

const handleView = (declarationId) => {
  // Navigate to detail view
  window.location.href = `/htkk?id=${encodeURIComponent(declarationId)}`;
};

const handleCreated = (declarationId) => {
  showCreateModal.value = false;
  showToast(`Đã tạo tờ khai ${declarationId}`);

  // Navigate to detail view to start working
  window.location.href = `/htkk?id=${encodeURIComponent(declarationId)}`;
};

const fetchUserInfo = async () => {
  try {
    const response = await fetch(
      '/api/method/frappe.auth.get_logged_user',
      { credentials: 'include' }
    );
    const data = await response.json();
    if (data.message) {
      // Get full name
      const userResponse = await fetch(
        `/api/method/frappe.client.get_value?doctype=User&fieldname=full_name&filters={"name":"${data.message}"}`,
        { credentials: 'include' }
      );
      const userData = await userResponse.json();
      userInfo.value = {
        user: data.message,
        full_name: userData.message?.full_name || data.message
      };
    }
  } catch (e) {
    console.error('Failed to fetch user info:', e);
  }
};

onMounted(() => {
  fetchUserInfo();
});
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap');

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

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: 'Outfit', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background-color: var(--bg);
  background-image:
    radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.1) 0px, transparent 50%),
    radial-gradient(at 100% 0%, rgba(2, 136, 209, 0.08) 0px, transparent 50%);
  color: var(--text);
  -webkit-font-smoothing: antialiased;
  min-height: 100vh;
}

.list-app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Header */
.app-header {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  padding: 0 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 72px;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 24px;
}

.back-btn {
  color: var(--text-muted);
  text-decoration: none;
  font-size: 13px;
  font-weight: 500;
  padding: 8px 12px;
  border-radius: 8px;
  transition: all 0.2s;
}

.back-btn:hover {
  background: #f1f5f9;
  color: var(--text);
}

.app-title h1 {
  margin: 0;
  font-size: 20px;
  font-weight: 800;
  color: var(--text);
  background: linear-gradient(135deg, #1a237e, #6366f1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.app-title p {
  margin: 4px 0 0;
  font-size: 12px;
  color: var(--text-muted);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: #f8fafc;
  border-radius: 20px;
}

.user-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--text);
}

/* Main */
.app-main {
  flex: 1;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  padding: 32px;
}

/* Toast */
.toast-container {
  position: fixed;
  top: 24px;
  right: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  z-index: 1001;
}

.toast {
  padding: 14px 24px;
  border-radius: 12px;
  background: white;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 600;
  font-size: 14px;
  min-width: 280px;
  border-left: 4px solid var(--accent);
}

.toast.success { border-left-color: var(--success); color: var(--success); }
.toast.error { border-left-color: var(--danger); color: var(--danger); }

.toast-enter-active, .toast-leave-active {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.toast-enter-from { opacity: 0; transform: translateX(100px); }
.toast-leave-to { opacity: 0; transform: scale(0.9); }

/* Responsive */
@media (max-width: 768px) {
  .app-header {
    padding: 0 16px;
    height: 64px;
  }

  .app-title h1 {
    font-size: 16px;
  }

  .app-title p {
    display: none;
  }

  .app-main {
    padding: 16px;
  }

  .stats-row {
    grid-template-columns: repeat(2, 1fr) !important;
  }

  .declaration-grid {
    grid-template-columns: 1fr !important;
  }
}
</style>
