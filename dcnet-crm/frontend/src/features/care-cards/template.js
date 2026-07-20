export default /* html */ `
<div v-else-if="route === 'care'" class="cc-page">

 <!-- ========================== LIST VIEW ========================== -->
 <template v-if="careView === 'list'">

  <!-- ===== Toolbar ===== -->
  <div class="cc-toolbar">
    <div class="cc-toolbar-title">
      <span>Tất cả thẻ chăm sóc</span>
      <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
    </div>
    <div class="cc-toolbar-actions">
      <button class="cc-tb-btn cc-tb-btn-ghost" @click="importCareCards">
        <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
        Nhập từ Excel
      </button>
      <button class="cc-tb-btn cc-tb-btn-primary" @click="createCareCard">
        <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        Thêm
      </button>
      <button v-if="showUnreadyFeatures" class="cc-tb-ico" @click="notifyCareAction('Lịch sử thẻ chăm sóc')">
        <svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>
      </button>
      <button v-if="showUnreadyFeatures" class="cc-tb-ico" @click="notifyCareAction('Thêm thao tác')">
        <svg viewBox="0 0 24 24" width="17" height="17" fill="currentColor"><circle cx="5" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="19" cy="12" r="2"/></svg>
      </button>
    </div>
  </div>

  <!-- ===== Body ===== -->
  <div class="cc-body">

    <!-- ===== LEFT: grid ===== -->
    <div class="cc-grid-wrap">
      <div class="cc-grid-toolbar">
        <div class="cc-search">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
          <input class="cc-search-input" placeholder="Tìm kiếm theo Khách hàng, Mã thẻ..." v-model="careSearch" @input="onCareSearchInput">
        </div>
        <div class="cc-grid-tools">
          <button class="cc-tool-btn" data-tooltip="Làm mới" @click="loadCareCards">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 2v6h-6"/><path d="M3 12a9 9 0 0 1 15-6.7L21 8"/><path d="M3 22v-6h6"/><path d="M21 12a9 9 0 0 1-15 6.7L3 16"/></svg>
          </button>
          <button v-if="showUnreadyFeatures" class="cc-tool-btn" data-tooltip="Cấu hình cột" @click="notifyCareAction('Cấu hình cột')">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
          </button>
          <button v-if="showUnreadyFeatures" class="cc-tool-btn cc-tool-btn-active" data-tooltip="Thống kê" @click="notifyCareAction('Thống kê')">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h4l2-5 4 10 2-5h6"/></svg>
          </button>
          <button class="cc-tool-btn" :class="{ 'cc-tool-btn-active': careFilterOpen }" data-tooltip="Bộ lọc" @click="careFilterOpen = !careFilterOpen">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
          </button>
        </div>
      </div>

      <div class="cc-table-scroll">
        <table class="cc-table">
          <thead>
            <tr>
              <th class="cc-th-check"><input type="checkbox" disabled></th>
              <th>Mã thẻ chăm sóc</th>
              <th>Khách hàng</th>
              <th>Mã số thuế</th>
              <th>Điện thoại</th>
              <th>Email</th>
              <th>Địa chỉ</th>
              <th>Bố cục</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="careListLoading">
              <td class="cc-td-state" colspan="8">Đang tải...</td>
            </tr>
            <tr v-else-if="!careList.length">
              <td class="cc-td-state" colspan="8">Không có thẻ chăm sóc nào</td>
            </tr>
            <tr
              v-for="row in careList"
              :key="row.name"
              class="cc-row"
              :class="{ 'cc-row-sel': careSelectedName === row.name }"
              @click="selectCareCard(row.name)"
            >
              <td class="cc-th-check" @click.stop><input type="checkbox"></td>
              <td class="cc-td-code"><a class="cc-cust-link" @click.stop="openCareDetail(row.name)">{{ row.name }}</a></td>
              <td class="cc-td-cust"><a class="cc-cust-link" @click.stop="openCareDetail(row.name)">{{ row.customer_name || row.customer }}</a></td>
              <td>{{ row.tax_id || '' }}</td>
              <td class="cc-td-phone">
                <span v-if="row.mobile_no" class="cc-phone">
                  <svg viewBox="0 0 24 24" width="12" height="12" fill="#22c55e" stroke="none"><path d="M6.62 10.79a15.53 15.53 0 0 0 6.59 6.59l2.2-2.2a1 1 0 0 1 1.05-.24 11.36 11.36 0 0 0 3.56.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1 11.36 11.36 0 0 0 .57 3.56 1 1 0 0 1-.24 1.05z"/></svg>
                  {{ row.mobile_no }}
                </span>
              </td>
              <td>{{ row.email_id || '-' }}</td>
              <td>{{ row.address || row.country || 'Việt Nam' }}</td>
              <td>{{ row.layout || 'Mặc định' }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="cc-grid-footer">
        <span class="cc-footer-total">Tổng số <b>{{ careTotal }}</b></span>
        <div class="cc-pager">
          <span class="cc-pager-lbl">Số dòng/trang</span>
          <select class="cc-pager-select" :value="carePageLength" @change="setCarePageLength($event.target.value)">
            <option :value="20">20</option>
            <option :value="50">50</option>
            <option :value="100">100</option>
          </select>
          <span class="cc-pager-range">{{ carePageStart }} - {{ carePageEnd }}</span>
          <button class="cc-pager-btn" :disabled="carePage <= 1" @click="changeCarePage(-(carePage - 1))">«</button>
          <button class="cc-pager-btn" :disabled="carePage <= 1" @click="changeCarePage(-1)">‹</button>
          <button class="cc-pager-btn" :disabled="carePage >= carePageCount" @click="changeCarePage(1)">›</button>
          <button class="cc-pager-btn" :disabled="carePage >= carePageCount" @click="changeCarePage(carePageCount - carePage)">»</button>
        </div>
      </div>
    </div>

    <!-- ===== CENTER: activity timeline panel ===== -->
    <div class="cc-activity">
      <div class="cc-act-iconbar">
        <button class="cc-act-ico" data-tooltip="Gọi điện" @click="callCareCustomer"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 13a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.61 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 9.91a16 16 0 0 0 6.22 6.22l.95-.95a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg></button>
        <button class="cc-act-ico" data-tooltip="Ghi chú" @click="showCareNoteComposer"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg></button>
        <button v-if="showUnreadyFeatures" class="cc-act-ico" data-tooltip="Lịch" @click="notifyCareAction('Thêm lịch')"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg></button>
        <button class="cc-act-ico" data-tooltip="Email" @click="emailCareCustomer"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 5L2 7"/></svg></button>
        <button class="cc-act-ico" data-tooltip="Trao đổi" @click="careTab = 'care'"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></button>
        <button class="cc-act-ico" data-tooltip="Gọi ra" @click="callCareCustomer"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.05 2a9 9 0 0 1 8 7.94M14.05 6A5 5 0 0 1 18 10M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 13a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.61 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L7.91 9.91a16 16 0 0 0 6.22 6.22l.95-.95a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg></button>
      </div>

      <div class="cc-act-tabs">
        <button class="cc-act-tab" :class="{ 'cc-act-tab-active': careTab === 'activities' }" @click="careTab = 'activities'">Hoạt động</button>
        <button class="cc-act-tab" :class="{ 'cc-act-tab-active': careTab === 'purchases' }" @click="careTab = 'purchases'">Mua hàng</button>
        <button class="cc-act-tab" :class="{ 'cc-act-tab-active': careTab === 'care' }" @click="careTab = 'care'">Chăm sóc</button>
      </div>

      <!-- Compose note (Chăm sóc tab) -->
      <div v-if="careTab === 'care' && careSelectedName" class="cc-note-box">
        <textarea class="cc-note-input" rows="2" placeholder="Thêm ghi chú chăm sóc..." v-model="careNoteText"></textarea>
        <button class="cc-note-send" :disabled="careNoteSaving || !careNoteText.trim()" @click="addCareNote">
          {{ careNoteSaving ? 'Đang lưu...' : 'Gửi' }}
        </button>
      </div>

      <div class="cc-act-scroll">
        <div v-if="careDetailLoading" class="cc-act-state">Đang tải...</div>
        <div v-else-if="!careSelectedName" class="cc-act-state">Chọn một thẻ chăm sóc</div>
        <div v-else-if="!careTimeline.length" class="cc-act-state">Chưa có dữ liệu</div>

        <!-- Purchases -->
        <template v-else-if="careTab === 'purchases'">
          <div v-for="p in careTimeline" :key="p.name" class="cc-purchase">
            <div class="cc-purchase-l">
              <span class="cc-purchase-kind">{{ p.kind }}</span>
              <a class="cc-purchase-name">{{ p.name }}</a>
              <span class="cc-purchase-date">{{ fmtDate(p.date) }}</span>
            </div>
            <div class="cc-purchase-r">
              <b class="cc-purchase-amount">{{ fmtMoney(p.amount, p.currency) }}</b>
              <span class="cc-purchase-status">{{ p.status }}</span>
            </div>
          </div>
        </template>

        <!-- Activities / Care timeline -->
        <template v-else>
          <div v-for="t in careTimeline" :key="t.name" class="cc-tl-item" :class="{ 'cc-tl-item--link': t.kind === 'Task' }" @click="t.kind === 'Task' && openActivityRecord(t.name)" :data-tooltip="t.kind === 'Task' ? 'Mở hoạt động' : ''">
            <span class="cc-tl-ico" :class="'cc-tl-ico--' + careKindIcon(t.kind)">
              <CRMIcon :name="careKindIcon(t.kind)" />
            </span>
            <div class="cc-tl-body">
              <div class="cc-tl-title">{{ t.title }}</div>
              <div v-if="t.content" class="cc-tl-content">{{ t.content }}</div>
              <div class="cc-tl-meta">
                <span class="cc-tl-person">{{ t.owner_full_name || '—' }}</span>
                <span class="cc-tl-dot">·</span>
                <span class="cc-tl-date">{{ fmtDate(t.date) }}</span>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>

    <!-- ===== FAR RIGHT: Bộ lọc ===== -->
    <div class="cc-filter" v-if="careFilterOpen">
      <div class="cc-filter-head">
        <span>Bộ lọc</span>
        <button class="cc-filter-x" @click="careFilterOpen = false">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>

      <div class="cc-filter-sec">
        <div class="cc-filter-sec-title">
          ĐÃ LƯU
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m18 15-6-6-6 6"/></svg>
        </div>
      </div>

      <div class="cc-filter-sec cc-filter-criteria">
        <div class="cc-filter-sec-title">
          TIÊU CHÍ LỌC
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
        </div>
        <div class="cc-filter-search">
          <input placeholder="Tìm kiếm" v-model="careFilterSearch">
        </div>
        <div class="cc-filter-list">
          <label v-for="d in careFilterDefinitions" :key="d.field" class="cc-filter-row">
            <input type="checkbox" :checked="isCareFilterOn(d.field)" @change="toggleCareFilter(d.field)">
            <span>{{ d.label }}</span>
          </label>
        </div>
      </div>

      <div v-if="careEnabledFilters.length" class="cc-filter-values">
        <div v-for="f in careEnabledFilters" :key="f" class="cc-fv-row">
          <span class="cc-fv-lbl">{{ (careAllFilterDefs.find(x => x.field === f) || {}).label || f }}</span>
          <select
            v-if="['satisfaction_level','status'].includes(f)"
            class="cc-fv-input"
            v-model="careFilterValues[f]"
          >
            <option value="">Tất cả</option>
            <option v-for="o in ((careAllFilterDefs.find(x => x.field === f) || {}).options || [])" :key="o" :value="o">{{ o }}</option>
          </select>
          <input
            v-else-if="['care_date','modified','creation'].includes(f)"
            class="cc-fv-input" type="date" v-model="careFilterValues[f]"
          >
          <input v-else class="cc-fv-input" placeholder="Nhập giá trị" v-model="careFilterValues[f]">
        </div>
      </div>

      <div class="cc-filter-actions">
        <button class="cc-filter-clear" @click="clearCareFilters">Xóa lọc</button>
        <button class="cc-filter-apply" @click="applyCareFilters">Áp dụng</button>
      </div>
    </div>

  </div>
 </template>

 <!-- ========================== DETAIL VIEW ========================== -->
 <template v-else>
  <div class="cc-detail">

    <!-- Header -->
    <div class="cc-det-header">
      <div class="cc-det-head-l">
        <button class="cc-det-back" @click="backToCareList">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
        </button>
        <div class="cc-det-head-title">
          <h1>{{ (careForm.customer_name) || (careDetail && careDetail.card && careDetail.card.customer_name) || 'Thẻ chăm sóc mới' }}</h1>
          <button v-if="showUnreadyFeatures" class="cc-det-addtag" @click="notifyCareAction('Thêm thẻ')"><svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg> Thêm thẻ</button>
        </div>
      </div>
      <div class="cc-det-head-r">
        <template v-if="careFormMode === 'view'">
          <button class="cc-tb-btn cc-tb-btn-ghost" @click="startCareEdit" v-if="!careDetail || !careDetail.card || careDetail.card.can_write !== false">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/></svg>
            Sửa
          </button>
          <button class="cc-tb-btn cc-tb-btn-primary" @click="createCareOrder">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
            Sinh đơn hàng
          </button>
          <button v-if="showUnreadyFeatures" class="cc-tb-ico" @click="notifyCareAction('Thêm thao tác')"><svg viewBox="0 0 24 24" width="17" height="17" fill="currentColor"><circle cx="5" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="19" cy="12" r="2"/></svg></button>
        </template>
        <template v-else>
          <button class="cc-tb-btn cc-tb-btn-ghost" @click="cancelCareEdit">Hủy</button>
          <button class="cc-tb-btn cc-tb-btn-primary" :disabled="careFormSaving" @click="saveCareForm">
            {{ careFormSaving ? 'Đang lưu...' : 'Lưu' }}
          </button>
        </template>
      </div>
    </div>

    <!-- Top summary row -->
    <div class="cc-det-summary">
      <div class="cc-det-sum-col">
        <div class="cc-det-sum-row"><span class="cc-det-sum-lbl">Khách hàng</span><a class="cc-det-sum-link">{{ (careForm.customer_name) || (careDetail && careDetail.card && careDetail.card.customer_name) || '—' }}</a></div>
        <div class="cc-det-sum-row"><span class="cc-det-sum-lbl">Mã số thuế</span><span>{{ (careForm.tax_id) || (careDetail && careDetail.card && careDetail.card.tax_id) || '—' }}</span></div>
      </div>
      <div class="cc-det-sum-col">
        <div class="cc-det-sum-row"><span class="cc-det-sum-lbl">Điện thoại</span><span>{{ (careForm.mobile_no) || (careDetail && careDetail.card && careDetail.card.mobile_no) || '—' }}</span></div>
        <div class="cc-det-sum-row"><span class="cc-det-sum-lbl">Email</span><span>{{ (careForm.email_id) || (careDetail && careDetail.card && careDetail.card.email_id) || '—' }}</span></div>
      </div>
    </div>

    <!-- Tabs -->
    <div class="cc-det-tabs">
      <button class="cc-det-tab" :class="{ 'cc-det-tab-active': careDetailTab === 'info' }" @click="careDetailTab = 'info'">Thông tin chi tiết</button>
      <template v-if="showUnreadyFeatures">
        <button class="cc-det-tab" :class="{ 'cc-det-tab-active': careDetailTab === 'notes' }" @click="careDetailTab = 'notes'">Ghi chú</button>
        <button class="cc-det-tab" :class="{ 'cc-det-tab-active': careDetailTab === 'files' }" @click="careDetailTab = 'files'">Tài liệu đính kèm</button>
        <button class="cc-det-tab" :class="{ 'cc-det-tab-active': careDetailTab === 'open' }" @click="careDetailTab = 'open'">Công việc đang thực hiện</button>
        <button class="cc-det-tab" :class="{ 'cc-det-tab-active': careDetailTab === 'done' }" @click="careDetailTab = 'done'">Công việc đã hoàn thành</button>
        <button class="cc-det-tab" :class="{ 'cc-det-tab-active': careDetailTab === 'chat' }" @click="careDetailTab = 'chat'">Nội dung trao đổi</button>
        <button class="cc-det-tab" :class="{ 'cc-det-tab-active': careDetailTab === 'advisory' }" @click="careDetailTab = 'advisory'">Thẻ tư vấn</button>
      </template>
    </div>

    <!-- Body -->
    <div class="cc-det-body">
      <template v-if="careDetailTab === 'info'">

        <!-- Field toolbar -->
        <div class="cc-det-fieldbar">
          <div class="cc-det-fieldsearch">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
            <input placeholder="Tìm kiếm trường" v-model="careFieldSearch">
          </div>
          <label class="cc-det-empty-toggle">
            <input type="checkbox" v-model="careShowEmpty">
            <span>Hiển thị dữ liệu trống</span>
          </label>
        </div>

        <!-- ── Thông tin chung ── -->
        <div class="cc-det-section">
          <h2 class="cc-det-sec-title">Thông tin chung</h2>
          <div class="cc-det-grid">
            <div class="cc-fld" v-if="showCareField('Mã thẻ chăm sóc', careSelectedName)">
              <span class="cc-fld-lbl">Mã thẻ chăm sóc</span>
              <span class="cc-fld-val cc-fld-ro">{{ careSelectedName || '(Tự sinh)' }}</span>
            </div>
            <div class="cc-fld" v-if="showCareField('Khách hàng', careForm.customer_name)">
              <span class="cc-fld-lbl">Khách hàng</span>
              <a class="cc-fld-val cc-fld-link">{{ careForm.customer_name || '—' }}</a>
            </div>
            <div class="cc-fld" v-if="showCareField('Mã số thuế', careForm.tax_id)">
              <span class="cc-fld-lbl">Mã số thuế</span>
              <template v-if="careFormMode !== 'view'"><input class="cc-fld-input" v-model="careForm.tax_id"></template>
              <span class="cc-fld-val" v-else>{{ careForm.tax_id || '—' }}</span>
            </div>
            <div class="cc-fld" v-if="showCareField('Điện thoại', careForm.mobile_no)">
              <span class="cc-fld-lbl">Điện thoại</span>
              <template v-if="careFormMode !== 'view'"><input class="cc-fld-input" v-model="careForm.mobile_no"></template>
              <span class="cc-fld-val" v-else>{{ careForm.mobile_no || '—' }}</span>
            </div>
            <div class="cc-fld" v-if="showCareField('Email', careForm.email_id)">
              <span class="cc-fld-lbl">Email</span>
              <template v-if="careFormMode !== 'view'"><input class="cc-fld-input" v-model="careForm.email_id"></template>
              <span class="cc-fld-val" v-else>{{ careForm.email_id || '—' }}</span>
            </div>
            <div class="cc-fld" v-if="showCareField('Quốc gia', careForm.country)">
              <span class="cc-fld-lbl">Quốc gia</span>
              <template v-if="careFormMode !== 'view'"><input class="cc-fld-input" v-model="careForm.country"></template>
              <span class="cc-fld-val" v-else>{{ careForm.country || '—' }}</span>
            </div>
            <div class="cc-fld" v-if="showCareField('Tỉnh/Thành phố', careForm.province)">
              <span class="cc-fld-lbl">Tỉnh/Thành phố</span>
              <template v-if="careFormMode !== 'view'"><input class="cc-fld-input" v-model="careForm.province"></template>
              <span class="cc-fld-val" v-else>{{ careForm.province || '—' }}</span>
            </div>
            <div class="cc-fld" v-if="showCareField('Quận/Huyện', careForm.district)">
              <span class="cc-fld-lbl">Quận/Huyện</span>
              <template v-if="careFormMode !== 'view'"><input class="cc-fld-input" v-model="careForm.district"></template>
              <span class="cc-fld-val" v-else>{{ careForm.district || '—' }}</span>
            </div>
            <div class="cc-fld" v-if="showCareField('Phường/Xã', careForm.ward)">
              <span class="cc-fld-lbl">Phường/Xã</span>
              <template v-if="careFormMode !== 'view'"><input class="cc-fld-input" v-model="careForm.ward"></template>
              <span class="cc-fld-val" v-else>{{ careForm.ward || '—' }}</span>
            </div>
            <div class="cc-fld" v-if="showCareField('Ngày thành lập/Ngày sinh', careForm.established_date)">
              <span class="cc-fld-lbl">Ngày thành lập/Ngày sinh</span>
              <template v-if="careFormMode !== 'view'"><input type="date" class="cc-fld-input" v-model="careForm.established_date"></template>
              <span class="cc-fld-val" v-else>{{ fmtDate(careForm.established_date) }}</span>
            </div>
            <div class="cc-fld" v-if="showCareField('Số đơn hàng', careForm.sales_order)">
              <span class="cc-fld-lbl">Số đơn hàng</span>
              <template v-if="careFormMode !== 'view'"><input class="cc-fld-input" v-model="careForm.sales_order"></template>
              <a class="cc-fld-val cc-fld-link" v-else>{{ careForm.sales_order || '—' }}</a>
            </div>
            <div class="cc-fld" v-if="showCareField('Hàng hóa', careForm.item)">
              <span class="cc-fld-lbl">Hàng hóa</span>
              <template v-if="careFormMode !== 'view'"><input class="cc-fld-input" v-model="careForm.item"></template>
              <span class="cc-fld-val" v-else>{{ careForm.item || '—' }}</span>
            </div>
            <div class="cc-fld" v-if="showCareField('Loại hàng hóa', careForm.item_type)">
              <span class="cc-fld-lbl">Loại hàng hóa</span>
              <template v-if="careFormMode !== 'view'"><input class="cc-fld-input" v-model="careForm.item_type"></template>
              <span class="cc-fld-val cc-fld-chip" v-else-if="careForm.item_type">{{ careForm.item_type }}</span>
              <span class="cc-fld-val" v-else>—</span>
            </div>
          </div>
        </div>

        <!-- ── Thông tin chăm sóc ── -->
        <div class="cc-det-section">
          <h2 class="cc-det-sec-title">Thông tin chăm sóc</h2>
          <div class="cc-det-grid">
            <div class="cc-fld" v-if="showCareField('Tình trạng chăm sóc', careForm.status)">
              <span class="cc-fld-lbl">Tình trạng chăm sóc</span>
              <select v-if="careFormMode !== 'view'" class="cc-fld-input" v-model="careForm.status">
                <option>Chưa chăm sóc</option><option>Đang chăm sóc</option><option>Đã chăm sóc</option>
              </select>
              <span class="cc-fld-val" v-else>{{ careForm.status || '—' }}</span>
            </div>
            <div class="cc-fld" v-if="showCareField('Ngày chăm sóc', careForm.care_date)">
              <span class="cc-fld-lbl">Ngày chăm sóc</span>
              <template v-if="careFormMode !== 'view'"><input type="date" class="cc-fld-input" v-model="careForm.care_date"></template>
              <span class="cc-fld-val" v-else>{{ fmtDate(careForm.care_date) }}</span>
            </div>
            <div class="cc-fld" v-if="showCareField('Mức độ hài lòng', careForm.satisfaction_level)">
              <span class="cc-fld-lbl">Mức độ hài lòng</span>
              <select v-if="careFormMode !== 'view'" class="cc-fld-input" v-model="careForm.satisfaction_level">
                <option value="">- Không chọn -</option>
                <option>Rất hài lòng</option><option>Hài lòng</option><option>Bình thường</option><option>Không hài lòng</option>
              </select>
              <span class="cc-fld-val" v-else>{{ careForm.satisfaction_level || '—' }}</span>
            </div>
            <div class="cc-fld" v-if="showCareField('Lý do không hài lòng', careForm.dissatisfaction_reason)">
              <span class="cc-fld-lbl">Lý do không hài lòng</span>
              <template v-if="careFormMode !== 'view'"><input class="cc-fld-input" v-model="careForm.dissatisfaction_reason"></template>
              <span class="cc-fld-val" v-else>{{ careForm.dissatisfaction_reason || '—' }}</span>
            </div>
            <div class="cc-fld cc-fld-wide" v-if="showCareField('Mô tả', careForm.description)">
              <span class="cc-fld-lbl">Mô tả</span>
              <template v-if="careFormMode !== 'view'"><textarea class="cc-fld-input cc-fld-textarea" rows="2" v-model="careForm.description"></textarea></template>
              <span class="cc-fld-val" v-else>{{ careForm.description || '—' }}</span>
            </div>
          </div>
        </div>

        <!-- ── Thông tin hệ thống ── -->
        <div class="cc-det-section">
          <h2 class="cc-det-sec-title">Thông tin hệ thống</h2>
          <div class="cc-det-grid">
            <div class="cc-fld" v-if="showCareField('Chủ sở hữu', careDetail && careDetail.card && careDetail.card.owner_full_name)">
              <span class="cc-fld-lbl">Chủ sở hữu</span>
              <a class="cc-fld-val cc-fld-link">{{ (careDetail && careDetail.card && careDetail.card.owner_full_name) || '—' }}</a>
            </div>
            <div class="cc-fld" v-if="showCareField('Đơn vị', careForm.department)">
              <span class="cc-fld-lbl">Đơn vị</span>
              <template v-if="careFormMode !== 'view'"><input class="cc-fld-input" v-model="careForm.department"></template>
              <span class="cc-fld-val" v-else>{{ careForm.department || '—' }}</span>
            </div>
            <div class="cc-fld" v-if="showCareField('Người tạo', careDetail && careDetail.card && careDetail.card.owner_full_name)">
              <span class="cc-fld-lbl">Người tạo</span>
              <span class="cc-fld-val">{{ (careDetail && careDetail.card && careDetail.card.owner_full_name) || '—' }}</span>
            </div>
            <div class="cc-fld" v-if="showCareField('Ngày tạo', careDetail && careDetail.card && careDetail.card.creation)">
              <span class="cc-fld-lbl">Ngày tạo</span>
              <span class="cc-fld-val">{{ fmtDate(careDetail && careDetail.card && careDetail.card.creation) }}</span>
            </div>
            <div class="cc-fld" v-if="showCareField('Người sửa', careDetail && careDetail.card && careDetail.card.modified_by_full_name)">
              <span class="cc-fld-lbl">Người sửa</span>
              <span class="cc-fld-val">{{ (careDetail && careDetail.card && careDetail.card.modified_by_full_name) || '—' }}</span>
            </div>
            <div class="cc-fld" v-if="showCareField('Ngày sửa', careDetail && careDetail.card && careDetail.card.modified)">
              <span class="cc-fld-lbl">Ngày sửa</span>
              <span class="cc-fld-val">{{ fmtDate(careDetail && careDetail.card && careDetail.card.modified) }}</span>
            </div>
            <div class="cc-fld" v-if="showCareField('Bố cục', careForm.layout)">
              <span class="cc-fld-lbl">Bố cục</span>
              <template v-if="careFormMode !== 'view'"><input class="cc-fld-input" v-model="careForm.layout"></template>
              <span class="cc-fld-val" v-else>{{ careForm.layout || '—' }}</span>
            </div>
            <div class="cc-fld" v-if="showCareField('Người liên quan', careForm.related_users)">
              <span class="cc-fld-lbl">Người liên quan</span>
              <template v-if="careFormMode !== 'view'"><input class="cc-fld-input" v-model="careForm.related_users"></template>
              <span class="cc-fld-val" v-else>{{ careForm.related_users || '—' }}</span>
            </div>
            <div class="cc-fld" v-if="showCareField('Người thực hiện đơn hàng', careForm.order_executor)">
              <span class="cc-fld-lbl">Người thực hiện đơn hàng</span>
              <template v-if="careFormMode !== 'view'"><input class="cc-fld-input" v-model="careForm.order_executor"></template>
              <span class="cc-fld-val" v-else>{{ (careDetail && careDetail.card && careDetail.card.order_executor_name) || careForm.order_executor || '—' }}</span>
            </div>
          </div>
        </div>

      </template>

      <div v-else class="cc-det-tab-empty">Chưa có dữ liệu</div>
    </div>
  </div>
 </template>

</div>
`;
