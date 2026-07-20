export default `
<!-- ════════ TÀI KHOẢN DỊCH VỤ ════════ -->
<div v-if="route === 'accounts'" class="acl-page">

  <!-- Toolbar -->
  <div class="acl-toolbar">
    <div class="acl-toolbar-left">
      <svg class="acl-toolbar-icon" viewBox="0 0 20 20" fill="none">
        <rect x="2" y="2" width="7" height="7" rx="1.5" stroke="currentColor" stroke-width="1.5"/>
        <rect x="11" y="2" width="7" height="7" rx="1.5" stroke="currentColor" stroke-width="1.5"/>
        <rect x="2" y="11" width="7" height="7" rx="1.5" stroke="currentColor" stroke-width="1.5"/>
        <rect x="11" y="11" width="7" height="7" rx="1.5" stroke="currentColor" stroke-width="1.5"/>
      </svg>
      <h1 class="acl-title">Tài khoản dịch vụ</h1>
      <span v-if="accountsTotal" class="acl-count-badge">{{ accountsTotal }}</span>
    </div>
    <button class="crm-button" type="button" @click="exportResource('accounts', { search: accountsSearch })">⇤ Xuất Excel</button>
    <div class="acl-search-wrap">
      <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
        <circle cx="7" cy="7" r="5" stroke="currentColor" stroke-width="1.5"/>
        <path d="M11 11l3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
      </svg>
      <input
        v-model="accountsSearch"
        @input="onAccountsSearchInput"
        placeholder="Tìm mã tài khoản, khách hàng, dịch vụ..."
        aria-label="Tìm kiếm tài khoản dịch vụ"
        class="acl-search-input"
      >
    </div>
  </div>

  <!-- Split layout: list | detail -->
  <div :class="['acl-body', accountDetail ? 'acl-body--split' : '']">

    <!-- List column -->
    <div class="acl-list-col" :aria-busy="accountsLoading">
      <div class="acl-list-wrap">
        <table class="acl-list-table">
          <thead>
            <tr>
              <th class="acl-th-code">Mã Account</th>
              <th v-if="!accountDetail" class="acl-th-customer">Khách hàng</th>
              <th class="acl-th-item">Mã dịch vụ</th>
              <th v-if="!accountDetail" class="acl-th-name">Tên dịch vụ</th>
              <th class="acl-th-aend">A-End</th>
              <th v-if="!accountDetail" class="acl-th-zend">Z-End</th>
              <th class="acl-th-status">Trạng thái</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="accountsLoading && !accountsList.length">
              <td :colspan="accountDetail ? 4 : 7" class="acl-empty-row">
                <span class="acl-spinner"></span> Đang tải...
              </td>
            </tr>
            <tr v-else-if="!accountsList.length">
              <td :colspan="accountDetail ? 4 : 7" class="acl-empty-row">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" style="opacity:.3;margin-bottom:6px">
                  <rect x="3" y="3" width="8" height="8" rx="1" stroke="currentColor" stroke-width="1.5"/>
                  <rect x="13" y="3" width="8" height="8" rx="1" stroke="currentColor" stroke-width="1.5"/>
                  <rect x="3" y="13" width="8" height="8" rx="1" stroke="currentColor" stroke-width="1.5"/>
                  <rect x="13" y="13" width="8" height="8" rx="1" stroke="currentColor" stroke-width="1.5"/>
                </svg>
                <div>Chưa có dữ liệu.</div>
              </td>
            </tr>
            <tr
              v-for="row in accountsList"
              :key="row.account_code"
              :class="['acl-list-row', accountDetail && accountDetail.account_code === row.account_code ? 'acl-list-row--active' : '']"
              @click="openAccountDetail(row)"
            >
              <td><span class="acl-code-chip">{{ row.account_code }}</span></td>
              <td v-if="!accountDetail" class="acl-cell-customer">{{ row.customer }}</td>
              <td class="acl-cell-mono">{{ row.item_code || '—' }}</td>
              <td v-if="!accountDetail" class="acl-cell-name">{{ row.item_name || '—' }}</td>
              <td class="acl-cell-addr">{{ row.a_end || '—' }}</td>
              <td v-if="!accountDetail" class="acl-cell-addr">{{ row.z_end || '—' }}</td>
              <td>
                <span :class="['acl-status-chip', row.is_active ? 'active' : 'inactive']">
                  {{ row.is_active ? 'Hoạt động' : 'Dừng' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pager -->
      <div class="acl-pager" v-if="accountsTotal > 0">
        <span class="acl-pager-info">{{ accountsPageStart }}–{{ accountsPageEnd }} / {{ accountsTotal }}</span>
        <div class="acl-pager-btns">
          <button class="acl-pager-btn" :disabled="accountsPage <= 1" @click="changeAccountsPage(1)" data-tooltip="Trang đầu">«</button>
          <button class="acl-pager-btn" :disabled="accountsPage <= 1" @click="changeAccountsPage(accountsPage - 1)" data-tooltip="Trang trước">‹</button>
          <span class="acl-pager-cur">{{ accountsPage }} / {{ accountsPageCount }}</span>
          <button class="acl-pager-btn" :disabled="accountsPage >= accountsPageCount" @click="changeAccountsPage(accountsPage + 1)" data-tooltip="Trang sau">›</button>
          <button class="acl-pager-btn" :disabled="accountsPage >= accountsPageCount" @click="changeAccountsPage(accountsPageCount)" data-tooltip="Trang cuối">»</button>
        </div>
      </div>
    </div>

    <!-- Detail panel -->
    <transition name="acl-panel-slide">
      <div v-if="accountDetail" class="acl-detail-col">

        <div v-if="accountDetailLoading" class="acl-detail-loading">
          <span class="acl-spinner"></span> Đang tải...
        </div>
        <template v-else>

          <!-- Detail header -->
          <div class="acl-detail-header">
            <div class="acl-detail-header-left">
              <span class="acl-code-chip acl-code-chip--lg">{{ accountDetail.account_code }}</span>
              <span :class="['acl-status-chip', accountDetail.is_active ? 'active' : 'inactive']">
                {{ accountDetail.is_active ? 'Hoạt động' : 'Dừng' }}
              </span>
            </div>
            <div class="acl-detail-actions">
              <template v-if="accountEditMode"><button class="crm-button" :disabled="accountEditSaving" @click="cancelAccountEdit">Hủy</button><button class="crm-button primary" :disabled="accountEditSaving" @click="saveAccountEdit">{{ accountEditSaving ? 'Đang lưu...' : 'Lưu' }}</button></template>
              <button v-else-if="accountDetail.can_write" class="crm-button" @click="startAccountEdit"><CRMIcon name="edit" /> Sửa</button>
            <button class="acl-detail-close" @click="closeAccountDetail" data-tooltip="Đóng">
              <svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                <path d="M3 3l10 10M13 3L3 13"/>
              </svg>
            </button>
            </div>
          </div>

          <!-- Info section -->
          <div class="acl-detail-section">
            <div class="acl-section-label">Thông tin</div>
            <div class="acl-info-grid">
              <div class="acl-info-row">
                <span class="acl-info-label">Khách hàng</span>
                <input v-if="accountEditMode" v-model="accountEditForm.customer" class="acl-edit-input"><span v-else class="acl-info-val">{{ accountDetail.customer || '—' }}</span>
              </div>
              <div class="acl-info-row">
                <span class="acl-info-label">Mã dịch vụ</span>
                <input v-if="accountEditMode" v-model="accountEditForm.item_code" class="acl-edit-input acl-cell-mono"><span v-else class="acl-info-val acl-cell-mono">{{ accountDetail.item_code || '—' }}</span>
              </div>
              <div class="acl-info-row">
                <span class="acl-info-label">Tên dịch vụ</span>
                <span class="acl-info-val">{{ accountDetail.item_name || '—' }}</span>
              </div>
              <div class="acl-info-row">
                <span class="acl-info-label">A-End</span>
                <input v-if="accountEditMode" v-model="accountEditForm.a_end" class="acl-edit-input"><span v-else class="acl-info-val">{{ accountDetail.a_end || '—' }}</span>
              </div>
              <div class="acl-info-row">
                <span class="acl-info-label">Z-End</span>
                <input v-if="accountEditMode" v-model="accountEditForm.z_end" class="acl-edit-input"><span v-else class="acl-info-val">{{ accountDetail.z_end || '—' }}</span>
              </div>
            </div>
            <label v-if="accountEditMode" class="acl-active-toggle"><input v-model.number="accountEditForm.is_active" type="checkbox" :true-value="1" :false-value="0"> Tài khoản đang hoạt động</label>
          </div>

          <!-- Related orders section -->
          <div class="acl-detail-section">
            <div class="acl-section-label">
              Đơn hàng liên quan
              <span class="acl-count-badge" style="margin-left:6px">{{ (accountDetail.sales_orders || []).length }}</span>
            </div>
            <div v-if="!(accountDetail.sales_orders || []).length" class="acl-empty-row" style="padding:20px 0">
              Chưa có đơn hàng nào.
            </div>
            <table v-else class="acl-so-table">
              <thead>
                <tr>
                  <th>Mã đơn hàng</th>
                  <th>Ngày</th>
                  <th style="text-align:center">Trạng thái</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="so in accountDetail.sales_orders"
                  :key="so.name"
                  class="acl-so-row"
                  @click="openOrderDetail({ name: so.name })"
                >
                  <td class="acl-so-name">{{ so.name }}</td>
                  <td class="acl-so-date">{{ so.transaction_date }}</td>
                  <td style="text-align:center">
                    <span :class="['acl-so-status-chip', so.status ? so.status.toLowerCase().replace(/ /g,'-') : '']">{{ so.status }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

        </template>
      </div>
    </transition>

  </div>
</div>
`;
