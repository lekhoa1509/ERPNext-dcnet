export default /* html */ `
<div v-else-if="route === 'activities'" class="hd-page">

  <!-- ===== LIST VIEW: dense table + filters (shown when nothing is selected) ===== -->
  <div v-if="!activitySelectedName && !activityDetailLoading" class="act-list-shell">
    <section class="act-list-panel">
      <div class="customer-list-tools">
        <label class="smart-search"><CRMIcon name="search" /><input v-model="activitySearch" @input="onActivitySearchInput" placeholder="Tìm kiếm theo tên hoạt động"></label>
        <div class="tool-buttons">
          <button class="icon-button" type="button" data-tooltip="Làm mới" @click="loadActivityList"><CRMIcon name="refresh" /></button>
          <button class="icon-button" type="button" data-tooltip="Bộ lọc" :class="{ active: activityFilterPanelOpen }" @click="activityFilterPanelOpen = !activityFilterPanelOpen"><CRMIcon name="filter" /></button>
        </div>
      </div>
      <div v-if="activityCustomerFilter" class="act-scope-banner">
        <span>Đang lọc theo khách hàng: <strong>{{ activityCustomerFilterLabel }}</strong></span>
        <button type="button" @click="clearActivityCustomerFilter">Xóa lọc ×</button>
      </div>
      <div class="customer-table-scroll">
        <table class="customer-table act-table">
          <thead>
            <tr><th>Tên hoạt động</th><th>Loại hoạt động</th><th>Đối tượng chính</th><th>Liên quan đến</th><th>Hạn hoàn thành</th><th>Trạng thái</th><th>Ngày kết thúc</th></tr>
          </thead>
          <tbody>
            <tr v-for="item in activityList" :key="(item.doctype || 'ToDo') + '-' + item.name" @click="selectActivity(item.name, item.doctype || 'ToDo')">
              <td class="act-cell-title"><a href="#" @click.prevent.stop="selectActivity(item.name, item.doctype || 'ToDo')">{{ item.description }}</a></td>
              <td>{{ item.task_type || '—' }}</td>
              <td>{{ item.customer_name || item.reference_name || '—' }}</td>
              <td>{{ (item.related_users && item.related_users.length) ? item.related_users.map((u) => u.full_name || u.name).join(', ') : '—' }}</td>
              <td>{{ fmtDate(item.date) }}</td>
              <td><span class="hd-item-badge" :class="actStatusBadgeClass(item.status)">{{ actStatusLabel(item.status) }}</span></td>
              <td>{{ item.status === 'Closed' ? fmtDT(item.modified) : '—' }}</td>
            </tr>
          </tbody>
        </table>
        <p v-if="activityListLoading" class="crm-empty">Đang tải...</p>
        <p v-else-if="!activityList.length" class="crm-empty">Không có hoạt động nào</p>
      </div>
      <footer class="customer-pagination">
        <strong><CRMIcon name="all" /> Tổng số {{ activityTotal.toLocaleString('vi-VN') }}</strong>
        <div>
          <span>Số dòng/trang</span>
          <select v-model.number="activityPageLength" @change="changeActivityPageLength"><option :value="20">20</option><option :value="50">50</option><option :value="100">100</option></select>
          <button type="button" :disabled="activityPage <= 1" @click="changeActivityPage(activityPage - 1)">‹</button>
          <button type="button" :disabled="activityPage * activityPageLength >= activityTotal" @click="changeActivityPage(activityPage + 1)">›</button>
        </div>
      </footer>
    </section>
    <aside v-if="activityFilterPanelOpen" class="customer-filter-panel">
      <header><h2>Bộ lọc</h2><button type="button" @click="activityFilterPanelOpen = false">×</button></header>
      <label class="act-filter-field">
        <span>Trạng thái</span>
        <select v-model="activityStatusFilter" @change="changeActivityStatusFilter(activityStatusFilter)">
          <option value="all">Tất cả</option>
          <option value="Open">Đang thực hiện</option>
          <option value="Closed">Hoàn thành</option>
          <option value="Cancelled">Đã hủy</option>
        </select>
      </label>
    </aside>
  </div>

  <!-- ===== DETAIL VIEW: 3-column list/detail/customer-info (shown once selected) ===== -->
  <div v-else class="hd-body">

    <!-- ===== LEFT: Activity list panel ===== -->
    <div class="hd-list-panel">
      <div class="hd-list-search">
        <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="hd-search-ico"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
        <input class="hd-search-input" placeholder="Tìm kiếm" v-model="activitySearch" @input="onActivitySearchInput">
      </div>
      <div class="hd-list-scroll">
        <div v-if="activityListLoading" class="hd-list-state">Đang tải...</div>
        <div v-else-if="!activityList.length" class="hd-list-state">Không có hoạt động nào</div>
        <div
          v-for="item in activityList"
          :key="(item.doctype || 'ToDo') + '-' + item.name"
          class="hd-item"
          :class="{ 'hd-item-sel': activitySelectedName === item.name && activitySelectedDoctype === (item.doctype || 'ToDo') }"
          @click="selectActivity(item.name, item.doctype || 'ToDo')"
        >
          <div class="hd-item-row1">
            <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="hd-item-doc-ico"><rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><line x1="12" y1="11" x2="16" y2="11"/><line x1="12" y1="16" x2="16" y2="16"/><line x1="8" y1="11" x2="8.01" y2="11"/><line x1="8" y1="16" x2="8.01" y2="16"/></svg>
            <span class="hd-item-title">{{ item.description }}</span>
          </div>
          <div class="hd-item-row2">
            <span class="hd-item-person">{{ item.owner_full_name || item.owner }}</span>
            <span class="hd-item-badge" :class="actStatusBadgeClass(item.status)">{{ actStatusLabel(item.status) }}</span>
          </div>
          <div class="hd-item-date">{{ item.date }}</div>
        </div>
      </div>
    </div>

    <!-- ===== CENTER: Detail / Edit panel ===== -->
    <div class="hd-detail">

      <!-- ── EDIT FORM ── -->
      <template v-if="activityEditMode && activityDetail">
        <div class="hd-ef-page">

          <!-- Form header -->
          <div class="hd-ef-header">
            <span class="hd-ef-title">Sửa Nhiệm vụ</span>
            <div class="hd-ef-header-actions">
              <button class="hd-ef-btn hd-ef-btn-cancel" @click="cancelActivityEdit">Hủy</button>
              <button class="hd-ef-btn hd-ef-btn-save" :disabled="activityEditSaving" @click="saveActivityEdit">
                {{ activityEditSaving ? 'Đang lưu...' : 'Lưu' }}
              </button>
            </div>
          </div>

          <!-- Form body -->
          <div class="hd-ef-body">
            <div class="hd-ef-section">
              <div class="hd-ef-section-title">Thông tin nhiệm vụ</div>

              <!-- Tiêu đề -->
              <div class="hd-ef-row">
                <span class="hd-ef-lbl hd-ef-lbl-req">Tiêu đề</span>
                <div class="hd-ef-input-wrap">
                  <input class="hd-ef-input" v-model="activityEditForm.description" placeholder="Tiêu đề nhiệm vụ">
                  <button class="hd-ef-clear-btn" v-if="activityEditForm.description" @click="activityEditForm.description = ''">
                    <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                  </button>
                </div>
              </div>

              <!-- Mô tả -->
              <div class="hd-ef-row hd-ef-row-top">
                <span class="hd-ef-lbl">Mô tả</span>
                <textarea class="hd-ef-textarea" v-model="activityEditForm.description" rows="3" placeholder="Ghi chú thêm..."></textarea>
              </div>

              <!-- Khách hàng (read-only) -->
              <div class="hd-ef-row">
                <span class="hd-ef-lbl">Khách hàng</span>
                <div class="hd-ef-readonly">
                  <span>{{ activityDetail.customer_name || '—' }}</span>
                  <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:#9ca3af;flex-shrink:0"><path d="m6 9 6 6 6-6"/></svg>
                </div>
              </div>

              <!-- Hóa đơn (read-only) -->
              <div class="hd-ef-row">
                <span class="hd-ef-lbl">Hóa đơn</span>
                <div class="hd-ef-readonly">
                  <span>{{ activityDetail.reference_name || '—' }}</span>
                  <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:#9ca3af;flex-shrink:0"><path d="m6 9 6 6 6-6"/></svg>
                </div>
              </div>

              <!-- Hạn hoàn thành -->
              <div class="hd-ef-row">
                <span class="hd-ef-lbl">Hạn hoàn thành</span>
                <div class="hd-ef-date-wrap">
                  <input class="hd-ef-input hd-ef-date-input" type="date" v-model="activityEditForm.date">
                </div>
              </div>

              <!-- Mức độ ưu tiên -->
              <div class="hd-ef-row">
                <span class="hd-ef-lbl hd-ef-lbl-req">Mức độ ưu tiên</span>
                <div class="hd-ef-select-wrap">
                  <select class="hd-ef-select" v-model="activityEditForm.priority">
                    <option value="Low">Thấp</option>
                    <option value="Medium">Trung bình</option>
                    <option value="High">Cao</option>
                    <option value="Urgent">Khẩn cấp</option>
                  </select>
                  <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="hd-ef-select-ico"><path d="m6 9 6 6 6-6"/></svg>
                </div>
              </div>

              <!-- Trạng thái -->
              <div class="hd-ef-row">
                <span class="hd-ef-lbl hd-ef-lbl-req">Trạng thái</span>
                <div class="hd-ef-select-wrap">
                  <select class="hd-ef-select" v-model="activityEditForm.status">
                    <option value="Open">Đang thực hiện</option>
                    <option value="Closed">Hoàn thành</option>
                    <option value="Cancelled">Đã hủy</option>
                  </select>
                  <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="hd-ef-select-ico"><path d="m6 9 6 6 6-6"/></svg>
                </div>
              </div>

              <!-- Người liên quan -->
              <div class="hd-ef-row hd-ef-row-top">
                <span class="hd-ef-lbl">Người liên quan</span>
                <div class="hd-ef-users-wrap" v-click-outside="closeUserDropdown">
                  <div class="hd-ef-tags-box" @click="onUserFocus">
                    <!-- Selected tags -->
                    <span
                      v-for="u in activityEditForm.related_users"
                      :key="u.name"
                      class="hd-ef-tag"
                    >
                      <span class="hd-ef-tag-avatar">{{ (u.full_name || u.name).charAt(0).toUpperCase() }}</span>
                      {{ u.full_name || u.name }}
                      <button class="hd-ef-tag-remove" @click.stop="removeRelatedUser(u.name)">
                        <svg viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                      </button>
                    </span>
                    <!-- Search input -->
                    <div class="hd-ef-user-search-wrap">
                      <input
                        class="hd-ef-user-input"
                        placeholder="Thêm người liên quan..."
                        v-model="activityUserQuery"
                        @input="onUserQueryInput"
                        @focus.stop="onUserFocus"
                      >
                      <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="hd-ef-user-ico"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                    </div>
                  </div>
                  <!-- Dropdown — all users, checkmark on selected -->
                  <div v-if="activityUserDropdownOpen && activityUserDropdown.length" class="hd-ef-user-dd">
                    <div
                      v-for="u in activityUserDropdown"
                      :key="u.name"
                      class="hd-ef-user-dd-item"
                      :class="{ 'hd-ef-dd-selected': isUserSelected(u.name) }"
                      @mousedown.prevent="toggleRelatedUser(u)"
                    >
                      <span class="hd-ef-dd-avatar" :class="{ 'hd-ef-dd-avatar--sel': isUserSelected(u.name) }">
                        {{ (u.full_name || u.name).charAt(0).toUpperCase() }}
                      </span>
                      <div class="hd-ef-dd-info">
                        <span class="hd-ef-dd-name">{{ u.full_name }}</span>
                      </div>
                      <svg v-if="isUserSelected(u.name)" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="hd-ef-dd-check"><polyline points="20 6 9 17 4 12"/></svg>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Loại nhiệm vụ -->
              <div class="hd-ef-row">
                <span class="hd-ef-lbl">Loại nhiệm vụ</span>
                <div class="hd-ef-tt-wrap" v-click-outside="closeTaskTypeDropdown">
                  <button class="hd-ef-tt-btn" @click.stop="toggleTaskTypeDropdown" type="button">
                    <span :class="{ 'hd-ef-tt-placeholder': !activityEditForm.task_type }">
                      {{ activityEditForm.task_type || 'Chọn loại nhiệm vụ' }}
                    </span>
                    <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
                  </button>
                  <div v-if="activityTaskTypeOpen" class="hd-ef-tt-dd">
                    <div class="hd-ef-tt-search-wrap">
                      <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="hd-ef-tt-search-ico"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
                      <input class="hd-ef-tt-search-input" placeholder="Tìm kiếm" v-model="activityTaskTypeQuery" @click.stop>
                    </div>
                    <div class="hd-ef-tt-list">
                      <div
                        v-for="opt in filteredTaskTypes"
                        :key="opt"
                        class="hd-ef-tt-item"
                        :class="{ 'hd-ef-tt-item--sel': activityEditForm.task_type === opt }"
                        @click.stop="selectTaskType(opt)"
                      >
                        <span>{{ opt }}</span>
                        <svg v-if="activityEditForm.task_type === opt" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="hd-ef-tt-check"><polyline points="20 6 9 17 4 12"/></svg>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </template>

      <!-- ── VIEW MODE ── -->
      <template v-else>

        <!-- Empty / loading state -->
        <div v-if="!activitySelectedName && !activityDetailLoading" class="hd-det-empty">
          <svg viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="#d1d5db" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
          <p>Chọn một hoạt động để xem chi tiết</p>
        </div>
        <div v-else-if="activityDetailLoading" class="hd-det-empty">Đang tải...</div>

        <template v-else-if="activityDetail">

          <!-- Header row: back + title + actions -->
          <div class="hd-det-head">
            <div class="hd-det-head-l">
              <button class="hd-det-back-btn" @click="clearActivitySelection">
                <svg viewBox="0 0 24 24" width="19" height="19" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
              </button>
              <span class="hd-det-title">{{ activityDetail.description }}</span>
            </div>
            <div class="hd-det-head-r">
              <button class="hd-det-edit-btn" @click="startActivityEdit" v-if="activityDetail.can_write">
                <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/></svg>
                Sửa
              </button>
              <details class="crm-detail-more">
                <summary class="hd-det-more-btn" aria-label="Thao tác khác" data-tooltip="Thao tác khác">
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><circle cx="5" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="19" cy="12" r="2"/></svg>
                </summary>
                <div class="crm-detail-more-menu" role="menu">
                  <button type="button" role="menuitem" @click="openActivityDeskRecord(); $event.currentTarget.closest('details').removeAttribute('open')">
                    <CRMIcon name="externalLink" :size="17" />
                    <span>Mở biểu mẫu hệ thống</span>
                  </button>
                  <div class="crm-detail-more-separator" role="separator"></div>
                  <button type="button" role="menuitem" @click="openAuditLog(activitySelectedDoctype, activitySelectedName); $event.currentTarget.closest('details').removeAttribute('open')">
                    <CRMIcon name="history" :size="17" />
                    <span>Nhật ký</span>
                  </button>
                </div>
              </details>
              <button class="hd-det-cust-btn" v-if="activityDetail.customer_name" @click="openActivityCustomer">
                <span>{{ activityDetail.customer_name }}</span>
                <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
              </button>
            </div>
          </div>

          <!-- Sub-row: status + tag -->
          <div class="hd-det-sub">
            <span class="hd-det-status-pill" :class="actStatusPillClass(activityDetail.status)">
              <span class="hd-det-status-dot" :class="actStatusDotClass(activityDetail.status)"></span>
              {{ actStatusLabel(activityDetail.status) }}
            </span>
            <span class="hd-det-sep">•</span>
            <button v-if="showUnreadyFeatures" class="hd-det-tag-btn" @click="notifyActivityAction('Thêm thẻ')">
              <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg>
              Thêm thẻ
            </button>
          </div>

          <!-- Quick fields -->
          <div class="hd-qf">
            <div class="hd-qf-row">
              <span class="hd-qf-lbl">Mô tả</span>
              <span class="hd-qf-val">{{ activityDetail.description || '—' }}</span>
            </div>
            <div class="hd-qf-row">
              <span class="hd-qf-lbl">Khách hàng</span>
              <a class="hd-qf-link">{{ activityDetail.customer_name || '—' }}</a>
            </div>
            <div class="hd-qf-row">
              <span class="hd-qf-lbl">Hóa đơn</span>
              <a class="hd-qf-link">{{ activityDetail.reference_name || '—' }}</a>
            </div>
            <div class="hd-qf-row">
              <span class="hd-qf-lbl">Mức độ ưu tiên</span>
              <span class="hd-qf-priority">{{ actPriorityLabel(activityDetail.priority) }}</span>
            </div>
            <div class="hd-qf-row">
              <span class="hd-qf-lbl">Loại nhiệm vụ</span>
              <span class="hd-qf-val hd-task-type">
                <span class="hd-task-dot"></span>{{ activityDetail.task_type || 'Nhiệm vụ' }}
              </span>
            </div>
          </div>

          <!-- Tabs bar -->
          <div class="hd-tabs-bar">
            <button class="hd-tab" :class="{ 'hd-tab-active': activityDetailTab === 'info' }" @click="activityDetailTab = 'info'">Thông tin chi tiết</button>
            <button class="hd-tab" :class="{ 'hd-tab-active': activityDetailTab === 'files' }" @click="activityDetailTab = 'files'">Tài liệu đính kèm</button>
            <button class="hd-tab" :class="{ 'hd-tab-active': activityDetailTab === 'chat' }" @click="activityDetailTab = 'chat'">Nội dung trao đổi</button>
            <button class="hd-tab" :class="{ 'hd-tab-active': activityDetailTab === 'notes' }" @click="activityDetailTab = 'notes'">Ghi chú</button>
            <div class="hd-tabs-end">
              <button class="hd-tab-act-btn" @click="createRelatedActivity">
                <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
              </button>
              <button v-if="showUnreadyFeatures" class="hd-tab-act-btn" @click="notifyActivityAction('Tùy chọn hiển thị')">
                <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
              </button>
            </div>
          </div>

          <!-- Tab content -->
          <div class="hd-tab-body">
            <div v-if="activityDetailTab === 'info'" class="hd-ct-section">
              <h3 class="hd-ct-heading">Thông tin nhiệm vụ</h3>
              <div class="hd-ct-grid">
                <div class="hd-ct-row hd-ct-row-top">
                  <span class="hd-ct-lbl">Tiêu đề</span>
                  <span class="hd-ct-val">{{ activityDetail.description }}</span>
                </div>
                <div class="hd-ct-row hd-ct-row-top">
                  <span class="hd-ct-lbl">Mô tả</span>
                  <span class="hd-ct-val">{{ activityDetail.description }}</span>
                </div>
                <div class="hd-ct-row">
                  <span class="hd-ct-lbl">Khách hàng</span>
                  <a class="hd-ct-link">{{ activityDetail.customer_name || '—' }}</a>
                </div>
                <div class="hd-ct-row">
                  <span class="hd-ct-lbl">Hóa đơn</span>
                  <a class="hd-ct-link">{{ activityDetail.reference_name || '—' }}</a>
                </div>
                <div class="hd-ct-row">
                  <span class="hd-ct-lbl">Người thực hiện</span>
                  <a class="hd-ct-link">{{ activityDetail.owner_full_name || activityDetail.owner || '—' }}</a>
                </div>
                <div class="hd-ct-row">
                  <span class="hd-ct-lbl">Đơn vị</span>
                  <span class="hd-ct-val">{{ activityDetail.department || '—' }}</span>
                </div>
                <div class="hd-ct-row">
                  <span class="hd-ct-lbl">Hạn hoàn thành</span>
                  <span class="hd-ct-val">{{ fmtDate(activityDetail.date) }}</span>
                </div>
                <div class="hd-ct-row">
                  <span class="hd-ct-lbl">Mức độ ưu tiên</span>
                  <span class="hd-qf-priority">{{ actPriorityLabel(activityDetail.priority) }}</span>
                </div>
                <div class="hd-ct-row">
                  <span class="hd-ct-lbl">Trạng thái</span>
                  <span :class="actDetailStatusClass(activityDetail.status)">{{ actStatusLabel(activityDetail.status) }}</span>
                </div>
                <div class="hd-ct-row hd-ct-row-top">
                  <span class="hd-ct-lbl">Người liên quan</span>
                  <div v-if="activityDetail.related_users && activityDetail.related_users.length" class="hd-ct-related">
                    <span v-for="u in activityDetail.related_users" :key="u.name" class="hd-ct-person">{{ u.full_name || u.name }}</span>
                  </div>
                  <span v-else class="hd-ct-val">—</span>
                </div>
                <div class="hd-ct-row" v-if="activityDetail.status === 'Closed'">
                  <span class="hd-ct-lbl">Ngày kết thúc</span>
                  <span class="hd-ct-val">{{ fmtDT(activityDetail.modified) }}</span>
                </div>
                <div class="hd-ct-row">
                  <span class="hd-ct-lbl">Loại nhiệm vụ</span>
                  <span class="hd-ct-val hd-task-type">
                    <span class="hd-task-dot"></span>{{ activityDetail.task_type || '—' }}
                  </span>
                </div>
                <div class="hd-ct-row">
                  <span class="hd-ct-lbl">Người tạo</span>
                  <span class="hd-ct-val">{{ activityDetail.owner_full_name || activityDetail.owner || '—' }}</span>
                </div>
                <div class="hd-ct-row">
                  <span class="hd-ct-lbl">Ngày tạo</span>
                  <span class="hd-ct-val">{{ fmtDT(activityDetail.creation) }}</span>
                </div>
                <div class="hd-ct-row">
                  <span class="hd-ct-lbl">Người sửa</span>
                  <span class="hd-ct-val">{{ activityDetail.modified_by_full_name || activityDetail.modified_by || '—' }}</span>
                </div>
                <div class="hd-ct-row">
                  <span class="hd-ct-lbl">Ngày sửa</span>
                  <span class="hd-ct-val">{{ fmtDT(activityDetail.modified) }}</span>
                </div>
              </div>
            </div>
            <div v-else-if="activityDetailTab === 'files'" class="hd-ct-section">
              <div class="profile-records-heading">
                <div><h2>Tài liệu đính kèm</h2></div>
                <div><button @click="addActivityAttachmentLink">Thêm liên kết</button><button :disabled="activityAttachUploading" @click="$refs.activityFileInput.click()">{{ activityAttachUploading ? 'Đang tải...' : 'Thêm tệp' }}</button><input ref="activityFileInput" type="file" style="display:none" @change="uploadActivityFile"></div>
              </div>
              <div class="profile-table-wrap">
                <table class="profile-related-table"><thead><tr><th>Tên tài liệu</th><th>Người đính kèm</th><th>Ngày đính kèm</th><th>Dung lượng</th><th></th></tr></thead><tbody><tr v-for="file in activityDetail.files" :key="file.name"><td><a :href="file.file_url" target="_blank" rel="noopener">{{ file.file_name }}</a></td><td>{{ file.owner || '—' }}</td><td>{{ fmtDT(file.creation) }}</td><td>{{ file.file_size ? formatFileSize(file.file_size) : '—' }}</td><td><button class="profile-row-action" @click="deleteActivityAttachment(file.name)">Xóa</button></td></tr></tbody></table>
                <p v-if="!activityDetail.files || !activityDetail.files.length" class="profile-empty">Không có bản ghi nào</p>
              </div>
            </div>
            <div v-else-if="activityDetailTab === 'chat'" class="hd-ct-section hd-ct-conversation">
              <div class="customer-conversation-shell">
                <header class="customer-conversation-heading">
                  <div><h2>Nội dung trao đổi</h2></div>
                  <span>{{ (activityDetail.communications || []).length }} bình luận</span>
                </header>
                <div v-if="activityDetail.communications && activityDetail.communications.length" class="customer-comment-feed">
                  <article v-for="entry in activityDetail.communications" :key="entry.name" class="customer-comment">
                    <span class="customer-comment-avatar" aria-hidden="true">{{ (entry.sender_full_name || entry.sender || 'CRM').slice(0, 1).toUpperCase() }}</span>
                    <div class="customer-comment-content">
                      <div class="customer-comment-meta"><strong>{{ entry.sender_full_name || entry.sender || 'CRM' }}</strong><time>{{ fmtDT(entry.creation) }}</time></div>
                      <div class="customer-comment-bubble"><p>{{ stripHtml(entry.content || '') }}</p></div>
                    </div>
                  </article>
                </div>
                <div v-else class="customer-conversation-empty"><CRMIcon name="message" /><strong>Chưa có nội dung trao đổi</strong><span>Hãy bắt đầu bằng bình luận đầu tiên về hoạt động này.</span></div>
                <div class="customer-comment-composer">
                  <span class="customer-comment-avatar current" aria-hidden="true">{{ (boot?.full_name || boot?.user || 'CRM').slice(0, 1).toUpperCase() }}</span>
                  <div class="customer-comment-editor">
                    <textarea v-model="activityConversationText" rows="3" aria-label="Nội dung trao đổi" placeholder="Viết bình luận..." @keydown.ctrl.enter.prevent="saveActivityNoteFromDetail('conversation')"></textarea>
                    <div class="customer-comment-actions">
                      <button class="crm-button primary" type="button" :disabled="!activityConversationText.trim()" @click="saveActivityNoteFromDetail('conversation')"><CRMIcon name="send" /> Gửi</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else-if="activityDetailTab === 'notes'" class="hd-ct-section">
              <h3 class="hd-ct-heading">Ghi chú</h3>
              <div class="customer-note-box">
                <textarea v-model="activityInlineNote" rows="3" placeholder="Nhập nội dung ghi chú..." @keydown.ctrl.enter.prevent="saveActivityNoteFromDetail('note')"></textarea>
                <div class="customer-note-actions">
                  <span>Nhấn Ctrl + Enter để lưu nhanh</span>
                  <button class="crm-button primary" type="button" :disabled="!activityInlineNote.trim()" @click="saveActivityNoteFromDetail('note')"><CRMIcon name="send" /> Lưu ghi chú</button>
                </div>
              </div>
              <div v-if="activityDetail.comments && activityDetail.comments.length" class="profile-timeline-list">
                <article v-for="entry in activityDetail.comments" :key="entry.name">
                  <strong>{{ entry.comment_email || entry.owner || 'CRM' }}</strong>
                  <span>{{ fmtDT(entry.creation) }}</span>
                  <p>{{ stripHtml(entry.content || '') }}</p>
                </article>
              </div>
              <p v-else class="profile-empty">Không có ghi chú nào.</p>
            </div>
            <div v-else class="hd-tab-empty">Chưa có dữ liệu</div>
          </div>

        </template>
      </template>
    </div>

    <!-- ===== RIGHT: Customer info panel ===== -->
    <div class="hd-right">
      <div class="hd-rp-top">
        <button class="hd-rp-cust-dd" @click="openActivityCustomer">
          <span>{{ activityDetail && activityDetail.customer_name || '—' }}</span>
          <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
        </button>
      </div>
      <div class="hd-rp-tabs">
        <button v-if="showUnreadyFeatures" class="hd-rp-tab hd-rp-tab-active" @click="notifyActivityAction('Thông tin khách hàng')">Thông tin</button>
      </div>
      <div class="hd-rp-scroll">
        <template v-if="activityDetail && activityDetail.customer_info">
          <a class="hd-rp-custname">{{ activityDetail.customer_info.customer_name }}</a>
          <span class="hd-rp-custtype">{{ activityDetail.customer_info.customer_type === 'Company' ? 'Công ty' : 'Khách hàng' }}</span>
          <div class="hd-rp-cust-fields">
            <div class="hd-rp-cf-row">
              <span class="hd-rp-cfl">Mã số thuế</span>
              <span class="hd-rp-cfv">{{ activityDetail.customer_info.tax_id || '—' }}</span>
            </div>
            <div class="hd-rp-cf-row">
              <span class="hd-rp-cfl">Điện thoại</span>
              <span class="hd-rp-cfv hd-rp-phone" v-if="activityDetail.customer_info.mobile_no">
                <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 13a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.61 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 9.91a16 16 0 0 0 6.22 6.22l.95-.95a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                {{ activityDetail.customer_info.mobile_no }}
              </span>
              <span class="hd-rp-cfv" v-else>—</span>
            </div>
            <div class="hd-rp-cf-row">
              <span class="hd-rp-cfl">Ngành nghề</span>
              <span class="hd-rp-cfv">{{ activityDetail.customer_info.industry || '' }}</span>
            </div>
            <div class="hd-rp-cf-row">
              <span class="hd-rp-cfl">Doanh thu</span>
              <span class="hd-rp-cfv"></span>
            </div>
          </div>
          <a class="hd-rp-more">Xem thêm</a>

          <div class="hd-rp-divider"></div>

          <div class="hd-rp-tasks-head">
            <span class="hd-rp-tasks-title">Công việc đang thực hiện</span>
            <button class="hd-rp-add-btn" @click="createRelatedActivity">
              <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
              Thêm
            </button>
          </div>

          <div
            v-for="task in activityDetail.related_tasks"
            :key="task.name"
            class="hd-rp-task"
            @click="selectActivity(task.name, task.doctype || 'ToDo')"
          >
            <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="hd-rp-task-ico"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
            <div class="hd-rp-task-body">
              <a class="hd-rp-task-title">{{ task.description }}</a>
              <span class="hd-rp-task-date">{{ task.date }}</span>
            </div>
          </div>
        </template>
        <template v-else>
          <div class="hd-rp-empty">Không có thông tin khách hàng</div>
        </template>
      </div>
      <button v-if="showUnreadyFeatures" class="hd-rp-edge-btn" @click="notifyActivityAction('Thu gọn panel khách hàng')">›</button>
    </div>

  </div>
</div>
`;
