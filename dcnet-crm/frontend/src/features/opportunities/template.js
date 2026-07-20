export default `
        <main v-else-if="route === 'contacts' && !contactViewEditorOpen" class="customer-workspace contact-workspace">
          <header class="customer-heading">
            <div class="customer-title">
              <div class="contact-view-selector">
                <button class="contact-view-trigger" :aria-expanded="contactViewMenuOpen" @click="contactViewMenuOpen = !contactViewMenuOpen">
                  <h1>{{ contactListViewLabel }}</h1><CRMIcon name="chevron" />
                </button>
                <div v-if="contactViewMenuOpen" class="contact-view-menu">
                  <strong>CHIA SẺ VỚI TÔI</strong>
                  <button v-for="view in contactViews" :key="view.id" :class="{ active: contactListView === view.id }" @click="selectContactListView(view.id)">
                    <span>{{ view.name }}</span><CRMIcon v-if="contactListView === view.id" name="checkcircle" />
                  </button>
                  <button disabled data-tooltip="Cần clarify mô hình nhóm nhân viên phụ trách">Liên hệ của nhóm tôi <small>Chưa cấu hình</small></button>
                  <button class="contact-view-add" @click="openContactViewEditor(true)"><span>＋</span> Thêm giao diện</button>
                </div>
              </div>
              <button class="contact-view-edit" @click="openContactViewEditor(false)">Sửa</button>
            </div>
            <div class="customer-actions">
              <button class="icon-button" data-tooltip="Sửa giao diện bảng" @click="openContactViewEditor(false)"><CRMIcon name="all" /></button>
              <button v-if="boot?.resources?.contacts?.can_create" class="crm-button primary" @click="createDocument('Contact')">＋ Thêm</button>
              <div class="crm-more-wrap">
                <button class="icon-button" data-tooltip="Thêm thao tác" @click="contactMoreOpen = !contactMoreOpen">•••</button>
                <div v-if="contactMoreOpen" class="crm-more-dropdown">
                  <button @click="importContacts(); contactMoreOpen = false">⇥ Nhập từ Excel</button>
                  <button :disabled="contactExporting" @click="exportContacts(); contactMoreOpen = false">
                    ⇤ {{ contactExporting ? 'Đang xuất...' : 'Xuất ra Excel' }}
                  </button>
                  <button v-if="selectedNames.size" class="danger" @click="deleteSelectedRows('Contact'); contactMoreOpen = false">🗑 Xóa đã chọn ({{ selectedNames.size }})</button>
                </div>
              </div>
            </div>
          </header>

          <section class="customer-grid" :class="{ 'detail-closed': !contactActivityOpen, 'filter-closed': !contactFilterOpen }">
            <section class="customer-list-panel">
              <div class="customer-list-tools">
                <label class="smart-search contact-search"><CRMIcon name="search" /><input v-model="search" placeholder="Tìm kiếm theo Mã liên hệ, Họ và tên"><b>AI</b></label>
                <div class="tool-buttons">
                  <button class="icon-button" data-tooltip="Làm mới" @click="loadRows"><CRMIcon name="refresh" /></button>
                  <button class="icon-button" data-tooltip="Tùy chỉnh cột" @click="openContactViewEditor(false)"><CRMIcon name="settings" /></button>
                  <button class="icon-button" :class="{ active: contactActivityOpen }" data-tooltip="Ẩn/hiện hoạt động" @click="contactActivityOpen = !contactActivityOpen"><CRMIcon name="activity" /></button>
                  <button class="icon-button" :class="{ active: contactFilterOpen }" data-tooltip="Ẩn/hiện bộ lọc" @click="contactFilterOpen = !contactFilterOpen"><CRMIcon name="filter" /></button>
                </div>
              </div>
              <div class="customer-table-scroll">
                <table class="customer-table contact-table">
                  <colgroup><col class="check-column"><col class="tag-column"><col v-for="column in shownContactColumns" :key="column.field" :style="{ width: column.width }"></colgroup>
                  <thead><tr><th><input type="checkbox" aria-label="Chọn tất cả" :checked="allSelected" :indeterminate.prop="someSelected" @change="toggleSelectAll()"></th><th>Thẻ</th><th v-for="column in shownContactColumns" :key="column.field">{{ column.label }}</th></tr></thead>
                  <tbody>
                    <tr v-for="row in displayContactRows" :key="row.name" :class="{ selected: selected?.name === row.name }" @click="selectRow(row)" @dblclick="openDocument(row)">
                      <td @click.stop><input type="checkbox" :aria-label="'Chọn ' + row.name" :checked="selectedNames.has(row.name)" @change="toggleSelectRow(row.name)"></td>
                      <td>—</td>
                      <td v-for="column in shownContactColumns" :key="column.field">
                        <a v-if="column.field === 'name' || column.field === 'full_name'" href="#" @click.prevent.stop="openDocument(row)">{{ formatValue(row[column.field], column.field) }}</a>
                        <span v-else-if="column.field === 'mobile_no' && row[column.field]" class="contact-phone">{{ row[column.field] }}</span>
                        <span v-else>{{ formatValue(row[column.field], column.field) }}</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
                <p v-if="loading" class="crm-empty">Đang tải...</p>
                <p v-else-if="!rows.length" class="crm-empty">Không có liên hệ phù hợp.</p>
              </div>
              <footer class="customer-pagination">
                <strong v-if="contactViewSummaryFields.includes('total')">☷ Tổng số {{ total.toLocaleString('vi-VN') }}</strong>
                <span v-else></span>
                <div><span>Số dòng/trang</span><select v-model.number="pageLength"><option :value="20">20</option><option :value="50">50</option><option :value="100">100</option></select>
                  <span>{{ pageStart }} - {{ pageEnd }}</span>
                  <button :disabled="page <= 1" @click="changePage(1)">|‹</button><button :disabled="page <= 1" @click="changePage(page - 1)">‹</button>
                  <button :disabled="page >= pageCount" @click="changePage(page + 1)">›</button><button :disabled="page >= pageCount" @click="changePage(pageCount)">›|</button>
                </div>
              </footer>
            </section>

            <aside v-if="contactActivityOpen" class="customer-detail-panel contact-detail-panel">
              <nav class="customer-tabs contact-tabs">
                <button :class="{ active: contactListTab === 'activity' }" @click="contactListTab = 'activity'">Hoạt động</button>
                <button :class="{ active: contactListTab === 'purchases' }" @click="contactListTab = 'purchases'">Mua hàng</button>
              </nav>
              <div v-if="selected && contactListTab === 'activity'" class="customer-detail-body">
                <div class="customer-timeline contact-activity-list">
                  <article v-for="item in contactActivityItems" :key="item.activity_key">
                    <i :class="'is-' + (item.activity_type || 'comment')"><CRMIcon :name="item.activity_type === 'task' ? 'task' : item.activity_type === 'meeting' ? 'calendar' : item.activity_type === 'call' ? 'phone' : 'contact'" /></i>
                    <div><p>{{ stripHtml(item.content) }}</p><small><b v-if="item.actor">{{ item.actor }}</b><span v-if="item.actor && item.activity_date"> · </span>{{ formatValue(item.activity_date, 'creation') }}</small></div>
                  </article>
                  <p v-if="detail && !contactActivityItems.length" class="crm-empty contact-panel-empty">Không có hoạt động.</p>
                </div>
              </div>
              <div v-else-if="selected && contactListTab === 'purchases'" class="customer-detail-body contact-purchase-list">
                <button v-for="record in contactPurchaseRecords" :key="record.record_doctype + '-' + record.name" class="contact-purchase-card" @click="openRelated(record.record_doctype, record)">
                  <i :class="'is-' + record.record_icon"><CRMIcon :name="record.record_icon" /></i>
                  <span><strong>{{ record.name }}</strong><small>{{ record.record_type }} · {{ formatValue(record.record_date, 'date') }}</small><em v-if="record.record_description">{{ record.record_description }}</em><span v-if="record.record_amount !== undefined && record.record_amount !== null">Tổng tiền <b>{{ formatValue(record.record_amount, 'grand_total') }}</b></span><span v-if="record.record_status">Tình trạng <b>{{ record.record_status }}</b></span></span>
                </button>
                <p v-if="detail && !contactPurchaseRecords.length" class="crm-empty contact-panel-empty">Chưa có dữ liệu mua hàng.</p>
              </div>
              <div v-else class="crm-empty customer-no-selection">Không có dữ liệu</div>
            </aside>

            <aside v-if="contactFilterOpen" class="customer-filter-panel">
              <header><h2>Bộ lọc</h2><button @click="contactFilterOpen = false">×</button></header>
              <section><strong>ĐÃ LƯU</strong><span>⌃</span></section>
              <section><strong>TIÊU CHÍ LỌC</strong><CRMIcon name="search" /></section>
              <div class="column-options filter-options">
                <div v-for="column in contactFilterDefinitions" :key="column.field">
                  <label>
                    <input type="checkbox" :checked="contactEnabledFilters.includes(column.field)" @change="toggleContactFilter(column.field)">
                    <span>{{ column.label }}</span>
                  </label>
                  <input v-if="contactEnabledFilters.includes(column.field)" v-model="contactFilterValues[column.field]" :placeholder="'Nhập ' + column.label.toLowerCase()">
                </div>
              </div>
            </aside>
          </section>
        </main>

        <main v-else-if="route === 'contacts' && contactViewEditorOpen" class="contact-view-editor">
          <header class="contact-view-editor-header">
            <div>
              <button class="contact-view-back" aria-label="Quay lại" @click="cancelContactViewEditor"><CRMIcon name="arrow-left" /></button>
              <h1>Sửa giao diện</h1>
            </div>
            <div class="contact-view-editor-actions">
              <button class="crm-button" @click="cancelContactViewEditor">Hủy</button>
              <button class="crm-button" @click="duplicateContactView">Nhân bản</button>
              <button class="crm-button primary" @click="saveContactView">Lưu</button>
            </div>
          </header>

          <div class="contact-view-editor-body">
            <label class="contact-view-name">
              <span>Tên giao diện <b>*</b></span>
              <input v-model="contactViewDraft.name" maxlength="80">
            </label>

            <div class="contact-view-config-grid">
              <section class="contact-view-config">
                <div class="contact-view-config-heading">
                  <h2>Chọn cột - Giao diện dạng bảng</h2>
                  <p>Những cột được chọn sẽ hiển thị trên danh sách liên hệ.</p>
                </div>
                <div class="contact-view-dual-list">
                  <div class="contact-view-list">
                    <strong>Có sẵn</strong>
                    <label class="contact-view-search"><CRMIcon name="search" /><input v-model="contactViewSearch" placeholder="Tìm kiếm"></label>
                    <div class="contact-view-list-body">
                      <button v-for="column in contactViewAvailableColumns" :key="column.field" @click="addContactViewField(column.field)">
                        <span>{{ column.label }}</span><b>＋</b>
                      </button>
                      <p v-if="!contactViewAvailableColumns.length">Không còn cột phù hợp.</p>
                    </div>
                  </div>
                  <div class="contact-view-list selected">
                    <strong>Được chọn <small>{{ contactViewSelectedColumns.length }}</small></strong>
                    <div class="contact-view-list-body">
                      <article v-for="(column, index) in contactViewSelectedColumns" :key="column.field">
                        <span>{{ column.label }} <b v-if="column.field === 'full_name'">*</b></span>
                        <div>
                          <button :disabled="index === 0" :aria-label="'Đưa ' + column.label + ' lên'" @click="moveContactViewField(column.field, -1)">↑</button>
                          <button :disabled="index === contactViewSelectedColumns.length - 1" :aria-label="'Đưa ' + column.label + ' xuống'" @click="moveContactViewField(column.field, 1)">↓</button>
                          <button :disabled="column.field === 'full_name'" :aria-label="'Bỏ ' + column.label" @click="removeContactViewField(column.field)">×</button>
                        </div>
                      </article>
                    </div>
                  </div>
                </div>
              </section>

              <section class="contact-view-config">
                <div class="contact-view-config-heading">
                  <h2>Chọn trường tổng - Giao diện dạng bảng</h2>
                  <p>Chọn số liệu tổng hợp hiển thị ở chân danh sách.</p>
                </div>
                <div class="contact-view-dual-list summary-list">
                  <div class="contact-view-list">
                    <strong>Có sẵn</strong>
                    <div class="contact-view-list-body">
                      <button v-if="!contactViewDraft.summary_fields.includes('total')" @click="toggleContactViewSummary('total')"><span>Tổng số</span><b>＋</b></button>
                      <p v-else>Đã chọn toàn bộ trường tổng.</p>
                    </div>
                  </div>
                  <div class="contact-view-list selected">
                    <strong>Được chọn</strong>
                    <div class="contact-view-list-body">
                      <article v-if="contactViewDraft.summary_fields.includes('total')">
                        <span>Tổng số</span>
                        <div><button aria-label="Bỏ Tổng số" @click="toggleContactViewSummary('total')">×</button></div>
                      </article>
                      <p v-else>Chưa chọn trường tổng.</p>
                    </div>
                  </div>
                </div>
              </section>
            </div>

            <section class="contact-view-sort">
              <h2>Sắp xếp dữ liệu theo</h2>
              <div>
                <select v-model="contactViewDraft.sort_field">
                  <option value="">Không sắp xếp</option>
                  <option v-for="column in availableContactColumns" :key="column.field" :value="column.field">{{ column.label }}</option>
                </select>
                <label><input v-model="contactViewDraft.sort_direction" type="radio" value="asc"> Tăng dần</label>
                <label><input v-model="contactViewDraft.sort_direction" type="radio" value="desc"> Giảm dần</label>
              </div>
            </section>
          </div>

          <footer class="contact-view-editor-footer">
            <button class="crm-button" @click="cancelContactViewEditor">Hủy</button>
            <button class="crm-button" @click="duplicateContactView">Nhân bản</button>
            <button class="crm-button primary" @click="saveContactView">Lưu</button>
          </footer>
        </main>

        <main v-else-if="opportunityFormOpen" class="opportunity-form-page">
            <header class="opportunity-form-header">
              <div><h1>Thêm Cơ hội</h1></div>
              <div><button class="crm-button" :disabled="opportunitySaving" @click="closeOpportunityForm">Hủy</button><button class="crm-button import" :disabled="opportunitySaving" @click="saveOpportunity(true)">Lưu và thêm</button><button class="crm-button primary" :disabled="opportunitySaving" @click="saveOpportunity(false)">{{ opportunitySaving ? 'Đang lưu...' : 'Lưu' }}</button></div>
            </header>
            <form class="opportunity-form-card" @submit.prevent="saveOpportunity(false)">
              <section>
                <h2>Thông tin chung</h2>
                <div class="opportunity-form-grid">
                  <label><span>Khách hàng <b>*</b></span><select v-model="opportunityForm.party_name" required><option value="">- Không chọn -</option><option v-for="customer in opportunityFormOptions.customers" :key="customer.name" :value="customer.name">{{ customer.customer_name || customer.name }}</option></select></label>
                  <label><span>Liên hệ</span><select v-model="opportunityForm.contact_person"><option value="">- Không chọn -</option><option v-for="contact in opportunityFormOptions.contacts" :key="contact.name" :value="contact.name">{{ contact.full_name || contact.name }}</option></select></label>
                  <label><span>Loại khách hàng</span><input :value="opportunityFormOptions.customers.find(item => item.name === opportunityForm.party_name)?.customer_group || ''" disabled placeholder="- Không chọn -"></label>
                  <label><span>Nguồn gốc</span><select v-model="opportunityForm.utm_source"><option value="">- Không chọn -</option><option v-for="source in opportunityFormOptions.sources" :key="source.name" :value="source.name">{{ source.name }}</option></select></label>
                  <label><span>Tên cơ hội <b>*</b></span><input v-model="opportunityForm.title" required></label>
                  <label><span>Loại cơ hội <b>*</b></span><select v-model="opportunityForm.opportunity_type" required><option value="">- Không chọn -</option><option v-for="type in opportunityFormOptions.opportunity_types" :key="type.name" :value="type.name">{{ type.name }}</option></select></label>
                  <label><span>Tỷ lệ thành công</span><input v-model.number="opportunityForm.probability" type="number" min="0" max="100"></label>
                  <label><span>Ngày kỳ vọng/kết thúc <b>*</b></span><input v-model="opportunityForm.expected_closing" type="date" required></label>
                  <label><span>Giai đoạn <b>*</b></span><select v-model="opportunityForm.sales_stage" required><option value="">- Không chọn -</option><option v-for="stage in opportunityFormOptions.sales_stages" :key="stage.name" :value="stage.name">{{ stage.name }}</option></select></label>
                  <label><span>Khu vực lắp đặt dịch vụ <b>*</b></span><select v-model="opportunityForm.territory" required><option value="">- Không chọn -</option><option v-for="territory in opportunityFormOptions.territories" :key="territory.name" :value="territory.name">{{ territory.name }}</option></select></label>
                </div>
              </section>

              <section>
                <div class="opportunity-section-heading">
                  <div><h2>Thông tin hàng hóa</h2><label class="opportunity-toggle"><input v-model.number="opportunityForm.custom_auto_increase_duplicate_qty" type="checkbox" :true-value="1" :false-value="0"><span>Tự động tăng SL khi chọn trùng</span></label></div>
                  <div><button v-if="showUnreadyFeatures" type="button" @click="notifyOpportunityAction('Nhập khẩu hàng hóa')">⇥ Nhập khẩu hàng hóa</button><button v-if="opportunityForm.items.length" type="button" class="danger" @click="clearOpportunityItems">× Xóa tất cả</button></div>
                </div>
                <div v-if="!opportunityForm.items.length" class="opportunity-items-empty">
                  <button type="button" class="crm-button" @click="openItemPicker">＋ Chọn hàng hóa</button>
                </div>
                <template v-else>
                  <div class="opportunity-items-scroll">
                    <table class="opportunity-items-table">
                      <thead><tr><th>STT</th><th>Mã hàng hóa</th><th>Tên hàng hóa</th><th>Mô tả</th><th>Điểm lắp đặt A-End</th><th>Điểm lắp đặt Z-End</th><th>Đơn vị tính</th><th>Số lượng</th><th>Đơn giá</th><th>Thành tiền</th><th>Tỷ lệ CK (%)</th><th>Tiền chiết khấu</th><th>Đơn giá sau CK</th><th>Thành tiền sau CK</th></tr></thead>
                      <tbody>
                        <tr v-for="(item, index) in opportunityForm.items" :key="index">
                          <td class="item-stt-cell"><span class="item-stt-num">{{ index + 1 }}</span><button type="button" class="item-row-del" @click="removeOpportunityItem(index)">×</button></td>
                          <td><select v-model="item.item_code" @change="selectOpportunityItem(item)"><option value="">- Chọn -</option><option v-for="option in opportunityFormOptions.items" :key="option.name" :value="option.name">{{ option.name }}</option></select></td>
                          <td><input v-model="item.item_name"></td><td><input v-model="item.description"></td>
                          <td><input v-model="item.custom_installation_point_a_end"></td><td><input v-model="item.custom_installation_point_z_end"></td>
                          <td><input v-model="item.uom"></td>
                          <td><input v-model.number="item.qty" type="number" min="0" step="any" @input="calcItemDiscount(item)"></td>
                          <td><input v-model.number="item.rate" type="number" min="0" step="any" @input="calcItemDiscount(item)"></td>
                          <td class="item-calc-cell">{{ formatValue((item.qty || 0) * (item.rate || 0), 'grand_total') }}</td>
                          <td><input v-model.number="item.custom_discount_percentage" type="number" min="0" max="100" step="any" @input="calcItemDiscount(item)"></td>
                          <td class="item-calc-cell">{{ formatValue(item.custom_discount_amount || 0, 'grand_total') }}</td>
                          <td class="item-calc-cell">{{ formatValue(item.custom_net_rate || 0, 'grand_total') }}</td>
                          <td class="item-calc-cell">{{ formatValue(item.custom_net_amount || 0, 'grand_total') }}</td>
                        </tr>
                        <tr class="items-total-row">
                          <td></td><td colspan="6" style="text-align:left;padding-left:8px">Tổng cộng</td>
                          <td>{{ opportunityForm.items.reduce((s, i) => s + (Number(i.qty) || 0), 0) }}</td>
                          <td></td>
                          <td>{{ formatValue(opportunityForm.items.reduce((s, i) => s + (i.qty||0)*(i.rate||0), 0), 'grand_total') }}</td>
                          <td></td>
                          <td>{{ formatValue(opportunityForm.items.reduce((s, i) => s + (i.custom_discount_amount||0), 0), 'grand_total') }}</td>
                          <td></td>
                          <td>{{ formatValue(opportunityForm.items.reduce((s, i) => s + (i.custom_net_amount||0), 0), 'grand_total') }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <div class="opportunity-item-actions">
                    <strong>Tổng số: {{ opportunityForm.items.length }}</strong>
                    <div class="item-action-btns">
                      <button type="button" class="crm-button" @click="openItemPicker">＋ Chọn hàng hóa</button>
                      <button type="button" class="crm-button" @click="addOpportunityItem">＋ Thêm dòng</button>
                    </div>
                  </div>
                </template>
              </section>
              <teleport to="body"><div v-if="itemPickerOpen" class="crm-modal-backdrop" @click.self="closeItemPicker">
                <div class="crm-modal item-picker-modal">
                  <header>
                    <h2>Chọn hàng hóa<span v-if="itemPickerSelected.length" class="picker-selected-badge">{{ itemPickerSelected.length }} đã chọn</span></h2>
                    <button type="button" @click="closeItemPicker">×</button>
                  </header>
                  <div class="item-picker-toolbar">
                    <div class="item-picker-search-wrap">
                      <svg class="picker-search-icon" viewBox="0 0 16 16" fill="none"><circle cx="7" cy="7" r="5" stroke="#98a2b3" stroke-width="1.5"/><path d="M11 11l3 3" stroke="#98a2b3" stroke-width="1.5" stroke-linecap="round"/></svg>
                      <input v-model="itemPickerSearch" @input="itemPickerPage = 1" placeholder="Tìm theo mã hoặc tên hàng hóa..." class="item-picker-search" autofocus>
                    </div>
                    <select v-model="itemPickerCategoryFilter" @change="itemPickerPage = 1" class="item-picker-cat">
                      <option value="">Tất cả loại hàng hóa</option>
                      <option v-for="cat in itemPickerCategories" :key="cat" :value="cat">{{ cat }}</option>
                    </select>
                  </div>
                  <div class="item-picker-table-wrap">
                    <table class="item-picker-table">
                      <colgroup><col><col><col><col><col></colgroup>
                      <thead>
                        <tr>
                          <th class="picker-check-col">
                            <input type="checkbox"
                              :checked="itemPickerRows.length > 0 && itemPickerRows.every(r => itemPickerSelected.includes(r.name))"
                              :indeterminate="itemPickerRows.some(r => itemPickerSelected.includes(r.name)) && !itemPickerRows.every(r => itemPickerSelected.includes(r.name))"
                              @change="e => { if(e.target.checked) itemPickerRows.forEach(r => { if(!itemPickerSelected.includes(r.name)) itemPickerSelected.push(r.name) }); else itemPickerSelected = itemPickerSelected.filter(n => !itemPickerRows.find(r => r.name === n)) }">
                          </th>
                          <th>Mã hàng hóa</th>
                          <th>Tên hàng hóa</th>
                          <th>Loại hàng hóa</th>
                          <th>Đơn vị tính</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="item in itemPickerRows" :key="item.name"
                          @click="toggleItemPickerRow(item.name)"
                          :class="{ selected: itemPickerSelected.includes(item.name) }">
                          <td class="picker-check-col"><input type="checkbox" :checked="itemPickerSelected.includes(item.name)" @click.stop="toggleItemPickerRow(item.name)"></td>
                          <td><span class="picker-code">{{ item.name }}</span></td>
                          <td>{{ item.item_name }}</td>
                          <td><span class="picker-tag" v-if="item.item_group && item.item_group !== 'All Item Groups'">{{ item.item_group }}</span><span v-else class="picker-tag-muted">—</span></td>
                          <td>{{ item.stock_uom || '—' }}</td>
                        </tr>
                        <tr v-if="!itemPickerRows.length" class="picker-empty-row">
                          <td colspan="5">Không tìm thấy hàng hóa nào phù hợp</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <div class="item-picker-footer">
                    <span>Tổng <strong>{{ itemPickerFiltered.length }}</strong> hàng hóa</span>
                    <div class="item-picker-pagination">
                      <span>Dòng/trang</span>
                      <select v-model.number="itemPickerPageLength" @change="itemPickerPage = 1">
                        <option :value="10">10</option><option :value="20">20</option><option :value="50">50</option>
                      </select>
                      <span>{{ (itemPickerPage-1)*itemPickerPageLength+1 }}–{{ Math.min(itemPickerPage*itemPickerPageLength, itemPickerFiltered.length) }}</span>
                      <button type="button" :disabled="itemPickerPage <= 1" @click="itemPickerPage = 1" data-tooltip="Trang đầu">«</button>
                      <button type="button" :disabled="itemPickerPage <= 1" @click="itemPickerPage--" data-tooltip="Trang trước">‹</button>
                      <button type="button" :disabled="itemPickerPage >= itemPickerPageCount" @click="itemPickerPage++" data-tooltip="Trang sau">›</button>
                      <button type="button" :disabled="itemPickerPage >= itemPickerPageCount" @click="itemPickerPage = itemPickerPageCount" data-tooltip="Trang cuối">»</button>
                    </div>
                  </div>
                  <footer>
                    <button type="button" class="crm-button" @click="closeItemPicker">Hủy</button>
                    <button type="button" class="crm-button primary" :disabled="!itemPickerSelected.length" @click="confirmItemPicker">
                      {{ itemPickerSelected.length ? 'Thêm ' + itemPickerSelected.length + ' hàng hóa' : 'Chọn hàng hóa' }}
                    </button>
                  </footer>
                </div>
              </div></teleport>

              <section><h2>Thông tin mô tả</h2><label class="opportunity-notes"><span>Mô tả</span><textarea v-model="opportunityForm.notes"></textarea></label></section>
              <section>
                <h2>Thông tin địa chỉ giao hàng</h2>
                <div class="opportunity-form-grid">
                  <label><span>Quốc gia</span><select v-model="opportunityForm.custom_shipping_country"><option value="">- Không chọn -</option><option v-for="country in opportunityFormOptions.countries" :key="country.name" :value="country.name">{{ country.name === 'Vietnam' ? 'Việt Nam' : country.name }}</option></select></label>
                  <label><span>Tỉnh/Thành phố</span><input v-model="opportunityForm.custom_shipping_state" placeholder="- Không chọn -"></label>
                  <label><span>Quận/Huyện</span><input v-model="opportunityForm.custom_shipping_county" placeholder="- Không chọn -"></label>
                  <label><span>Phường/Xã</span><input v-model="opportunityForm.custom_shipping_ward" placeholder="- Không chọn -"></label>
                  <label><span>Số nhà, Đường phố</span><input v-model="opportunityForm.custom_shipping_address_line1"></label>
                  <label><span>Mã vùng</span><input v-model="opportunityForm.custom_shipping_pincode"></label>
                  <label><span>Địa chỉ</span><textarea v-model="opportunityForm.custom_shipping_address"></textarea></label>
                </div>
              </section>
              <section>
                <h2>Thông tin hệ thống</h2>
                <div class="opportunity-form-grid">
                  <label><span>Dùng chung</span><input v-model.number="opportunityForm.custom_is_shared" type="checkbox" :true-value="1" :false-value="0"></label>
                  <label><span>Công ty</span><select v-model="opportunityForm.company" required><option v-for="company in opportunityFormOptions.companies" :key="company.name" :value="company.name">{{ company.name }}</option></select></label>
                  <label><span>Mã cơ hội</span><input disabled placeholder="Tự sinh khi lưu"></label>
                  <label><span>Đối tác/CTV giới thiệu</span><select v-model="opportunityForm.custom_referral_partner"><option value="">- Không chọn -</option><option v-for="customer in opportunityFormOptions.customers" :key="customer.name" :value="customer.name">{{ customer.customer_name || customer.name }}</option></select></label>
                </div>
              </section>
            </form>
          <teleport to="body"><div v-if="leaveFormConfirmOpen" class="crm-modal-backdrop" @click.self="cancelLeaveForm">
            <div class="crm-modal leave-form-confirm">
              <header><h2>Thoát và không lưu?</h2><button type="button" @click="cancelLeaveForm">×</button></header>
              <p>Nếu bạn thoát, các dữ liệu đang nhập liệu sẽ không được lưu lại</p>
              <footer><button class="crm-button" @click="cancelLeaveForm">Ở lại</button><button class="crm-button primary" @click="confirmLeaveForm">Thoát không lưu</button></footer>
            </div>
          </div></teleport>
        </main>

        <main v-else-if="route === 'opportunities'" class="customer-workspace opportunity-workspace">
          <header class="customer-heading">
            <div class="customer-title"><h1>Tất cả cơ hội</h1><span>⌄</span></div>
            <div class="customer-actions">
              <button v-if="showUnreadyFeatures" class="icon-button" data-tooltip="Kiểu hiển thị" @click="notifyOpportunityAction('Kiểu hiển thị khác')"><CRMIcon name="all" /></button>
              <button class="crm-button import" @click="importOpportunities">⇥ Nhập từ Excel</button>
              <button v-if="boot?.resources?.opportunities?.can_create" class="crm-button primary" @click="createDocument('Opportunity')">＋ Thêm</button>
              <div class="crm-more-wrap">
                <button class="icon-button" data-tooltip="Thêm thao tác" @click="opportunityMoreOpen = !opportunityMoreOpen">•••</button>
                <div v-if="opportunityMoreOpen" class="crm-more-dropdown">
                  <button @click="importOpportunities(); opportunityMoreOpen = false">⇥ Nhập từ Excel</button>
                  <button @click="exportResource('opportunities', { search }); opportunityMoreOpen = false">⇤ Xuất ra Excel</button>
                  <button v-if="selectedNames.size" class="danger" @click="deleteSelectedRows('Opportunity'); opportunityMoreOpen = false">🗑 Xóa đã chọn ({{ selectedNames.size }})</button>
                </div>
              </div>
            </div>
          </header>

          <section class="customer-grid" :class="{ 'detail-closed': !opportunityActivityOpen, 'filter-closed': !opportunityFilterOpen }">
            <section class="customer-list-panel">
              <div class="customer-list-tools">
                <label class="smart-search"><CRMIcon name="search" /><input v-model="search" placeholder="Tìm kiếm thông minh"><b>AI</b></label>
                <div class="tool-buttons">
                  <button class="icon-button" data-tooltip="Làm mới" @click="loadRows"><CRMIcon name="refresh" /></button>
                  <button class="icon-button" :class="{ active: opportunityColumnDialogOpen }" data-tooltip="Tùy chỉnh cột" @click="openOpportunityColumnDialog"><CRMIcon name="settings" /></button>
                  <button class="icon-button" :class="{ active: opportunityActivityOpen }" data-tooltip="Ẩn/hiện lịch sử" @click="opportunityActivityOpen = !opportunityActivityOpen"><CRMIcon name="activity" /></button>
                  <button class="icon-button" :class="{ active: opportunityFilterOpen }" data-tooltip="Ẩn/hiện bộ lọc" @click="opportunityFilterOpen = !opportunityFilterOpen"><CRMIcon name="filter" /></button>
                </div>
              </div>
              <div class="customer-table-scroll">
                <table class="customer-table opportunity-table">
                  <colgroup><col class="check-column"><col class="tag-column"><col v-for="column in shownOpportunityColumns" :key="column.field" :style="{ width: column.width }"></colgroup>
                  <thead><tr><th><input type="checkbox" aria-label="Chọn tất cả" :checked="allSelected" :indeterminate.prop="someSelected" @change="toggleSelectAll()"></th><th>Thẻ</th><th v-for="column in shownOpportunityColumns" :key="column.field">{{ column.label }}</th></tr></thead>
                  <tbody>
                    <tr v-for="row in rows" :key="row.name" :class="{ selected: selected?.name === row.name }" @click="selectRow(row)" @dblclick="openDocument(row)">
                      <td @click.stop><input type="checkbox" :aria-label="'Chọn ' + row.name" :checked="selectedNames.has(row.name)" @change="toggleSelectRow(row.name)"></td><td>—</td>
                      <td v-for="column in shownOpportunityColumns" :key="column.field">
                        <a v-if="column.field === 'title'" href="#" class="opp-link" @click.prevent.stop="openOpportunityDetail(row)">{{ formatValue(row[column.field], column.field) }}</a>
                        <span v-else-if="column.field === 'contact_display'">{{ formatValue(row[column.field], column.field) }}</span>
                        <span v-else-if="column.field === 'sales_stage'" class="opportunity-stage">{{ formatValue(row[column.field], column.field) }}</span>
                        <span v-else>{{ formatValue(row[column.field], column.field) }}</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
                <p v-if="loading" class="crm-empty">Đang tải...</p>
                <p v-else-if="!rows.length" class="crm-empty">Không có cơ hội phù hợp.</p>
              </div>
              <footer class="customer-pagination">
                <strong>☷ Tổng số {{ total.toLocaleString('vi-VN') }}</strong>
                <div><span>Số dòng/trang</span><select v-model.number="pageLength"><option :value="20">20</option><option :value="50">50</option><option :value="100">100</option></select>
                  <span>{{ pageStart }} - {{ pageEnd }}</span>
                  <button :disabled="page <= 1" @click="changePage(1)">|‹</button><button :disabled="page <= 1" @click="changePage(page - 1)">‹</button>
                  <button :disabled="page >= pageCount" @click="changePage(page + 1)">›</button><button :disabled="page >= pageCount" @click="changePage(pageCount)">›|</button>
                </div>
              </footer>
            </section>

            <aside v-if="opportunityActivityOpen" class="customer-detail-panel opportunity-detail-panel">
              <div class="customer-detail-actions">
                <button data-tooltip="Gọi điện" @click="callOpportunityPhone"><CRMIcon name="phone" /></button><button data-tooltip="Tạo công việc" @click="createOpportunityTask"><CRMIcon name="task" /></button>
                <button v-if="showUnreadyFeatures" data-tooltip="Tạo lịch" @click="notifyOpportunityAction('Tạo lịch')"><CRMIcon name="calendar" /></button><button data-tooltip="Gửi email" @click="emailOpportunity"><CRMIcon name="email" /></button>
                <button data-tooltip="Xem hoạt động" @click="opportunityTab = 'activity'"><CRMIcon name="contact" /></button><button data-tooltip="Tạo báo giá" :disabled="!selected" @click="selected && openCreateQuotation(selected.party_name, selected.customer_name || selected.party_name, selected.name)"><CRMIcon name="quotation" /></button>
              </div>
              <nav class="opportunity-scope-tabs" aria-label="Phạm vi dữ liệu panel">
                <button :class="{ active: opportunityPanelScope === 'opportunity' }" @click="setOpportunityPanelScope('opportunity')">Cơ hội</button>
                <button :class="{ active: opportunityPanelScope === 'customer' }" :disabled="!opportunityLinkedCustomerName" @click="setOpportunityPanelScope('customer')">Khách hàng</button>
              </nav>
              <nav class="customer-tabs opportunity-tabs" :class="{ 'is-customer-scope': opportunityPanelScope === 'customer' }">
                <button :class="{ active: opportunityTab === 'activity' }" @click="opportunityTab = 'activity'">Hoạt động</button>
                <button :class="{ active: opportunityTab === 'purchases' }" @click="opportunityTab = 'purchases'">Mua hàng</button>
                <button :class="{ active: opportunityTab === 'contact' }" @click="opportunityTab = 'contact'">Liên hệ</button>
                <button v-if="opportunityPanelScope === 'opportunity'" :class="{ active: opportunityTab === 'items' }" @click="opportunityTab = 'items'">Hàng hóa</button>
              </nav>
              <div v-if="selected" class="customer-detail-body">
                <p v-if="opportunityPanelScope === 'customer' && opportunityCustomerLoading" class="crm-empty">Đang tải dữ liệu khách hàng...</p>
                <template v-if="opportunityTab === 'activity'">
                  <div class="customer-timeline">
                    <article v-for="item in opportunityPanelActivities" :key="item.panel_key">
                      <i><CRMIcon :name="item.panel_icon" /></i>
                      <div><strong>{{ stripHtml(item.panel_title) }}</strong><p>{{ stripHtml(item.panel_content) }}</p><small>{{ formatValue(item.panel_date, 'creation') }}</small></div>
                    </article>
                    <p v-if="opportunityPanelDetail && !opportunityPanelActivities.length && !opportunityCustomerLoading" class="crm-empty">Chưa có hoạt động.</p>
                  </div>
                </template>
                <template v-else-if="opportunityTab === 'purchases'">
                  <button v-for="record in opportunityPanelPurchases" :key="record.record_doctype + '-' + record.name" class="detail-list-row purchase-row" @click="openRelated(record.record_doctype, record)">
                    <span><strong>{{ record.name }}</strong><small>{{ record.record_label }} · {{ formatValue(record.record_date, 'transaction_date') }}</small></span>
                    <span><b>{{ formatValue(record.grand_total, 'grand_total') }}</b><small>{{ record.status || '—' }}</small></span>
                  </button>
                  <p v-if="opportunityPanelDetail && !opportunityPanelPurchases.length && !opportunityCustomerLoading" class="crm-empty">Chưa có báo giá, đơn hàng hoặc hóa đơn.</p>
                </template>
                <template v-else-if="opportunityTab === 'contact'">
                  <article v-for="contact in opportunityPanelContacts" :key="contact.name" class="opportunity-contact-row">
                    <span class="opportunity-contact-avatar">{{ (contact.full_name || contact.first_name || contact.name || '?').charAt(0) }}</span>
                    <div><strong>{{ contact.full_name || contact.name }}</strong><p v-if="contact.designation">{{ contact.designation }}</p><p v-if="contact.mobile_no">{{ contact.mobile_no }}</p><p v-if="contact.email_id">{{ contact.email_id }}</p></div>
                  </article>
                  <p v-if="opportunityPanelDetail && !opportunityPanelContacts.length && !opportunityCustomerLoading" class="crm-empty">Chưa có liên hệ.</p>
                </template>
                <template v-else-if="opportunityPanelScope === 'opportunity'">
                  <article v-for="item in opportunityPanelItems" :key="item.idx || item.item_code" class="detail-list-row">
                    <span><strong>{{ item.item_name || item.item_code }}</strong><small>{{ item.item_code }} · {{ item.qty }} {{ item.uom || '' }}</small></span>
                    <span><b>{{ formatValue(item.amount, 'grand_total') }}</b><small>{{ formatValue(item.rate, 'grand_total') }}</small></span>
                  </article>
                  <p v-if="detail && !opportunityPanelItems.length" class="crm-empty">Chưa có hàng hóa.</p>
                </template>
              </div>
              <div v-else class="crm-empty customer-no-selection">Chọn một cơ hội để xem thông tin liên quan.</div>
            </aside>

            <aside v-if="opportunityFilterOpen" class="customer-filter-panel">
              <header><h2>Bộ lọc</h2><button @click="opportunityFilterOpen = false">×</button></header>
              <section><strong>ĐÃ LƯU</strong><span>⌃</span></section>
              <section><strong>TIÊU CHÍ LỌC</strong><CRMIcon name="search" /></section>
              <div class="column-options filter-options">
                <div v-for="column in opportunityFilterDefinitions" :key="column.field">
                  <label><input type="checkbox" :checked="opportunityEnabledFilters.includes(column.field)" @change="toggleOpportunityFilter(column.field)"><span>{{ column.label }}</span></label>
                  <input v-if="opportunityEnabledFilters.includes(column.field)" v-model="opportunityFilterValues[column.field]" :type="['expected_closing', 'creation'].includes(column.field) ? 'date' : 'text'" :placeholder="'Nhập ' + column.label.toLowerCase()">
                </div>
              </div>
            </aside>
          </section>

          <teleport to="body"><div v-if="opportunityColumnDialogOpen" class="column-dialog-backdrop" @click.self="cancelOpportunityColumnDialog">
            <section class="column-dialog">
              <header><h2>Tùy chỉnh cột</h2><button data-tooltip="Đóng" @click="cancelOpportunityColumnDialog">×</button></header>
              <div class="column-dialog-body">
                <section class="column-picker">
                  <label class="column-search"><CRMIcon name="search" /><input v-model="opportunityColumnSearch" placeholder="Tìm kiếm cột"></label>
                  <strong>Chọn trường</strong>
                  <div class="column-picker-list">
                    <label v-for="column in filteredOpportunityColumns" :key="column.field">
                      <input type="checkbox" :checked="opportunityColumnDraft.includes(column.field)" @change="toggleOpportunityDraftColumn(column.field)">
                      <span>{{ column.label }}</span>
                    </label>
                    <p v-if="!filteredOpportunityColumns.length" class="crm-empty">Không tìm thấy cột phù hợp.</p>
                  </div>
                </section>
                <section class="selected-columns">
                  <header><strong>Đã chọn ({{ selectedOpportunityColumns.length }})</strong><button @click="opportunityColumnDraft = []">Xóa tất cả</button></header>
                  <div>
                    <article v-for="column in selectedOpportunityColumns" :key="column.field">
                      <span>{{ column.label }}</span><button :aria-label="'Bỏ cột ' + column.label" @click="removeOpportunityDraftColumn(column.field)">×</button>
                    </article>
                    <p v-if="!selectedOpportunityColumns.length" class="crm-empty">Chưa chọn cột nào.</p>
                  </div>
                </section>
              </div>
              <footer>
                <button class="column-default" @click="resetOpportunityDraftColumns">Mặc định</button>
                <div><button class="crm-button" @click="cancelOpportunityColumnDialog">Hủy</button><button class="crm-button primary" @click="saveOpportunityColumns">Lưu</button></div>
              </footer>
            </section>
          </div></teleport>
        </main>

        <main v-else-if="route === 'opportunity-detail'" class="opp-detail-page">
  <header class="opp-detail-header op-head">
    <div class="op-head-left">
      <button class="opp-back-btn" aria-label="Quay lại danh sách cơ hội" @click="backToOpportunities"><CRMIcon name="arrow-left" /></button>
      <div class="op-record-title">
        <small>Cơ hội</small>
        <b class="op-num">{{ opportunityDetail?.document?.custom_opportunity_code || opportunityDetail?.document?.name || opportunityDetailName }}</b>
      </div>
      <span class="op-stage-pill" v-if="opportunityDetail?.document?.sales_stage">
        <span class="stage-dot"></span>
        {{ opportunityDetail.document.sales_stage }} <CRMIcon name="chevron" />
      </span>
      <button class="icon-button op-refresh" @click="loadOpportunityDetail()"><CRMIcon name="refresh" /></button>
    </div>
    <div class="actions">
      <template v-if="!opportunityDetailEditing">
        <button class="crm-button" :disabled="!opportunityDetail" @click="opportunityDetailEditing = true; opportunityDetailForm = { ...opportunityDetail.document }"><CRMIcon name="edit" /> Sửa</button>
        <div v-if="opportunityDetail" class="op-split-btn">
          <button class="crm-button op-split" @click="openCreateSO(opportunityDetail.document.party_name, opportunityDetail.document.customer_name || opportunityDetail.document.party_name, opportunityDetailName)"><CRMIcon name="cart" /> Sinh đơn hàng</button>
          <button v-if="showUnreadyFeatures" class="crm-button op-split op-split-arrow" aria-label="Tùy chọn sinh đơn hàng" @click="notifyOpportunityAction('Tùy chọn sinh đơn hàng')"><CRMIcon name="chevron" /></button>
        </div>
        <div class="opp-detail-more-wrap">
          <button class="icon-button op-more" aria-haspopup="menu" :aria-expanded="opportunityDetailMoreOpen ? 'true' : 'false'" @click.stop="toggleOpportunityDetailMoreMenu"><CRMIcon name="more" /></button>
          <div v-if="opportunityDetailMoreOpen" class="opp-detail-more-menu" role="menu">
            <template v-for="item in opportunityDetailMoreActions" :key="item.key">
              <div v-if="item.separator" class="opp-detail-more-separator"></div>
              <button v-else type="button" role="menuitem" :class="{ danger: item.danger }" @click.stop="handleOpportunityDetailMoreAction(item.key)">
                <CRMIcon :name="item.icon" />
                <span>{{ item.label }}</span>
              </button>
            </template>
          </div>
        </div>
      </template>
      <template v-else>
        <button class="crm-button" :disabled="opportunityDetailSaving" @click="opportunityDetailEditing = false">Hủy</button>
        <button class="crm-button primary" :disabled="opportunityDetailSaving" @click="saveOpportunityDetailEdit">{{ opportunityDetailSaving ? 'Đang lưu...' : 'Lưu' }}</button>
      </template>
    </div>
  </header>

  <div v-if="loading" class="crm-empty" style="margin-top:40px">Đang tải...</div>
  <div v-else-if="!opportunityDetail" class="crm-empty" style="margin-top:40px">Không tìm thấy cơ hội.</div>
  <div v-else class="opp-detail-body">

    <aside class="opp-detail-sidebar">
      <div class="opp-detail-sidebar-title">
        <h3>{{ opportunityDetail.document.title || opportunityDetail.document.name || '—' }}</h3>
        <button class="opp-sidebar-tag" @click="openOpportunityTagDialog"><CRMIcon name="tag" /> Thêm thẻ</button>
      </div>
      <div class="opp-detail-sidebar-actions">
        <button class="act-btn" data-tooltip="Gọi điện" @click="callOpportunityPhone"><CRMIcon name="phone" /></button>
        <button class="act-btn" data-tooltip="Tạo công việc" @click="createOpportunityActivity('Nhiệm vụ')"><CRMIcon name="task" /></button>
        <button class="act-btn" data-tooltip="Tạo lịch" @click="createOpportunityActivity('Lịch hẹn')"><CRMIcon name="calendar" /></button>
        <button class="act-btn" data-tooltip="Gửi email" @click="emailOpportunity"><CRMIcon name="email" /></button>
        <button class="act-btn" data-tooltip="Trao đổi" @click="opportunityDetailTab = 'chat'"><CRMIcon name="contact" /></button>
        <button class="act-btn" data-tooltip="Gọi" @click="callOpportunityPhone"><CRMIcon name="phone" /></button>
      </div>
      <button class="opp-customer-card" @click="opportunityDetail.document.party_name && openCustomerDetail({ name: opportunityDetail.document.party_name })">
        <span class="occ-icon"><CRMIcon name="customer" /></span>
        <span class="occ-text">
          <strong>{{ opportunityDetail.document.customer_name || opportunityDetail.document.party_name || '—' }}</strong>
          <small>{{ opportunityDetail.document.party_name }}</small>
        </span>
        <span class="occ-chevron">›</span>
      </button>
      <section class="profile-facts">
        <header><h3>Thông tin tóm tắt</h3><button data-tooltip="Tùy chỉnh thông tin tóm tắt" aria-label="Tùy chỉnh thông tin tóm tắt" @click="openOpportunitySummaryDialog"><CRMIcon name="sliders" /></button></header>
        <dl>
          <div v-for="row in opportunitySummaryRows" :key="row.field">
            <dt>{{ row.label }}</dt><dd :class="row.cls">{{ row.display }}</dd>
          </div>
          <div v-if="!opportunitySummaryRows.length" class="profile-facts-empty">Chưa chọn trường hiển thị.</div>
        </dl>
      </section>
    </aside>

    <div class="opp-detail-main">
      <nav class="opp-detail-tabs" role="tablist" aria-label="Nội dung cơ hội">
        <button v-for="tab in opportunityDetailTabs" :key="tab.key" type="button" role="tab"
          :aria-selected="opportunityDetailTab === tab.key ? 'true' : 'false'"
          :tabindex="opportunityDetailTab === tab.key ? 0 : -1"
          :class="{ active: opportunityDetailTab === tab.key }" @click="opportunityDetailTab = tab.key">
          <span>{{ tab.label }}</span><span v-if="tab.count" class="opp-tab-badge">{{ tab.count }}</span>
        </button>
      </nav>

      <div class="opp-detail-tab-content">

        <template v-if="opportunityDetailTab === 'overview'">
          <div class="opp-overview-main">
            <div class="opp-overview-headrow">
              <h3 class="opp-overview-title">Tổng quan Cơ hội</h3>
              <button class="opp-ai-btn" type="button" @click="analyzeOpportunityWithAi"><CRMIcon name="sparkles" /> Phân tích với AI</button>
            </div>
            <div class="op-pipeline">
              <button v-for="(label, i) in ['Kinh doanh lập yêu cầu','P.TH check thông tin','Thực hiện khảo sát','Kinh doanh báo giá cho KH']"
                   :key="label"
                   :class="['op-stage', 'st-c'+i, oppStageState(label, i)]"
                   :style="{ zIndex: 10 - i }"
                   @click="setOpportunityStage(label)">
                {{ label }}
              </button>
              <button class="op-end-btn win" :class="{ on: opportunityDetail.document.sales_stage === 'Kết thúc thắng' }" @click="openOpportunityClosingDialog('Kết thúc thắng')"><CRMIcon name="thumbsup" /> Kết thúc thắng</button>
              <button class="op-end-btn lose" :class="{ on: opportunityDetail.document.sales_stage === 'Kết thúc thất bại' }" @click="openOpportunityClosingDialog('Kết thúc thất bại')"><CRMIcon name="thumbsdown" /> Kết thúc thất bại</button>
            </div>

            <div class="opp-stat-cards">
              <div class="opp-stat-card">
                <span class="opp-sc-icon opp-sc-icon--amount"><CRMIcon name="dollar" /></span>
                <div class="opp-sc-text">
                  <div class="opp-sc-label">Số tiền</div>
                  <div class="opp-sc-value">{{ formatValue(opportunityDetail.document.opportunity_amount, 'opportunity_amount') }}</div>
                </div>
              </div>
              <div class="opp-stat-card">
                <span class="opp-sc-icon opp-sc-icon--rate"><CRMIcon name="checkcircle" /></span>
                <div class="opp-sc-text">
                  <div class="opp-sc-label">Tỷ lệ thành công</div>
                  <div class="opp-sc-value">{{ opportunityDetail.document.probability || 0 }}%</div>
                </div>
              </div>
              <div class="opp-stat-card">
                <span class="opp-sc-icon opp-sc-icon--expected"><CRMIcon name="trend" /></span>
                <div class="opp-sc-text">
                  <div class="opp-sc-label">Doanh số kỳ vọng</div>
                  <div class="opp-sc-value">{{ formatValue((opportunityDetail.document.opportunity_amount || 0) * (opportunityDetail.document.probability || 0) / 100, 'opportunity_amount') }}</div>
                </div>
              </div>
              <div class="opp-stat-card">
                <span class="opp-sc-icon opp-sc-icon--date"><CRMIcon name="calendardays" /></span>
                <div class="opp-sc-text">
                  <div class="opp-sc-label">Ngày kỳ vọng / kết thúc</div>
                  <div class="opp-sc-value">{{ formatValue(opportunityDetail.document.expected_closing, 'expected_closing') }}</div>
                </div>
              </div>
            </div>

            <div class="op-two-cols">
            <div class="opp-section-card">
              <div class="opp-section-header">
                <h4>Hàng hóa</h4>
                <button class="crm-button op-panel-arrow" aria-label="Xem hàng hóa" @click="opportunityDetailTab = 'items'"><CRMIcon name="arrow-right" /></button>
              </div>
              <div v-if="!opportunityDetail.items.length" class="opp-section-empty"><CRMIcon name="package" /> Không có dữ liệu</div>
              <table v-else class="opp-mini-table">
                <thead><tr><th>Tên hàng hóa</th><th>SL</th><th>Thành tiền</th></tr></thead>
                <tbody>
                  <tr v-for="item in opportunityDetail.items.slice(0, 5)" :key="item.idx">
                    <td>{{ item.item_name || item.item_code }}</td>
                    <td>{{ item.qty }}</td>
                    <td>{{ formatValue(item.custom_net_amount || item.amount, 'opportunity_amount') }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="opp-section-card profile-overview-conversation">
              <div class="opp-section-header">
                <h4>Nội dung trao đổi</h4>
                <button class="crm-button op-panel-arrow" aria-label="Xem nội dung trao đổi" @click="opportunityDetailTab = 'chat'"><CRMIcon name="arrow-right" /></button>
              </div>
              <div v-if="opportunityDetail.comments.length" class="customer-comment-feed">
                <article v-for="c in opportunityDetail.comments.slice(-3)" :key="c.name" class="customer-comment">
                  <span class="customer-comment-avatar" aria-hidden="true">{{ (c.comment_by_fullname || c.comment_by || 'CRM').slice(0, 1).toUpperCase() }}</span>
                  <div class="customer-comment-content">
                    <div class="customer-comment-meta"><strong>{{ c.comment_by_fullname || c.comment_by }}</strong><time>{{ formatValue(c.creation, 'creation') }}</time></div>
                    <div class="customer-comment-bubble"><p>{{ stripHtml(c.content || '') }}</p></div>
                  </div>
                </article>
              </div>
              <div v-else class="opp-section-empty"><CRMIcon name="message" /> Chưa có trao đổi nào</div>
              <div class="customer-comment-composer">
                <span class="customer-comment-avatar current" aria-hidden="true">{{ (boot?.full_name || boot?.user || 'CRM').slice(0, 1).toUpperCase() }}</span>
                <div class="customer-comment-editor">
                  <textarea v-model="opportunityDetailComment" rows="2" aria-label="Nội dung trao đổi" placeholder="Nhập nội dung..." @keydown.ctrl.enter.prevent="saveOpportunityDetailComment"></textarea>
                  <div class="customer-comment-actions">
                    <button type="button" class="crm-button primary" :disabled="!opportunityDetailComment.trim()" @click="saveOpportunityDetailComment"><CRMIcon name="send" /> Gửi</button>
                  </div>
                </div>
              </div>
            </div>
            </div>
          </div>

        </template>

        <template v-else-if="opportunityDetailTab === 'info'">
          <div class="detail-form-toolbar">
            <label><CRMIcon name="search" /><input v-model="opportunityDetailFieldSearch" placeholder="Tìm kiếm trường"></label>
            <span class="detail-edit-status" v-if="opportunityDetailEditing">Đang chỉnh sửa</span>
            <label class="detail-empty-toggle">
              <input v-model="opportunityDetailShowEmpty" type="checkbox">
              <i></i><span>Hiển thị dữ liệu trống</span>
            </label>
          </div>

          <div class="opp-info-grid">
            <div class="opp-info-section" style="grid-column: 1 / -1">
              <h4>Thông tin chung</h4>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Khách hàng', opportunityDetail.document.customer_name || opportunityDetail.document.party_name)">
                <label>Khách hàng</label>
                <span>{{ opportunityDetail.document.customer_name || opportunityDetail.document.party_name || '—' }}</span>
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Liên hệ', opportunityDetail.document.contact_display || opportunityDetail.document.contact_person)">
                <label>Liên hệ</label>
                <span v-if="!opportunityDetailEditing">{{ opportunityDetail.document.contact_display || opportunityDetail.document.contact_person || '—' }}</span>
                <input v-else v-model="opportunityDetailForm.contact_person">
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Email liên hệ', opportunityDetail.document.contact_email)">
                <label>Email liên hệ</label>
                <span>{{ opportunityDetail.document.contact_email || '—' }}</span>
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('SĐT liên hệ', opportunityDetail.document.contact_mobile)">
                <label>SĐT liên hệ</label>
                <span>{{ opportunityDetail.document.contact_mobile || '—' }}</span>
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Loại cơ hội', opportunityDetail.document.opportunity_type)">
                <label>Loại cơ hội</label>
                <span v-if="!opportunityDetailEditing">{{ opportunityDetail.document.opportunity_type || '—' }}</span>
                <select v-else v-model="opportunityDetailForm.opportunity_type">
                  <option v-for="t in (opportunityFormOptions.opportunity_types || [])" :key="t.name" :value="t.name">{{ t.name }}</option>
                </select>
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Tên cơ hội', opportunityDetail.document.title)">
                <label>Tên cơ hội</label>
                <span v-if="!opportunityDetailEditing">{{ opportunityDetail.document.title || '—' }}</span>
                <input v-else v-model="opportunityDetailForm.title">
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Loại hàng hóa', opportunityDetail.document.custom_item_category)">
                <label>Loại hàng hóa</label>
                <span v-if="!opportunityDetailEditing">{{ opportunityDetail.document.custom_item_category || '—' }}</span>
                <select v-else v-model="opportunityDetailForm.custom_item_category">
                  <option value="">- Không chọn -</option>
                  <option v-for="g in (opportunityFormOptions.item_groups || [])" :key="g.name" :value="g.name">{{ g.name }}</option>
                </select>
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Tỷ lệ thành công', opportunityDetail.document.probability)">
                <label>Tỷ lệ thành công (%)</label>
                <span v-if="!opportunityDetailEditing">{{ opportunityDetail.document.probability || 0 }}%</span>
                <input v-else type="number" min="0" max="100" v-model.number="opportunityDetailForm.probability">
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Giai đoạn', opportunityDetail.document.sales_stage)">
                <label>Giai đoạn</label>
                <span v-if="!opportunityDetailEditing">{{ opportunityDetail.document.sales_stage || '—' }}</span>
                <select v-else v-model="opportunityDetailForm.sales_stage">
                  <option v-for="s in (opportunityFormOptions.sales_stages || [])" :key="s.name" :value="s.name">{{ s.name }}</option>
                </select>
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Ngày kỳ vọng/kết thúc', opportunityDetail.document.expected_closing)">
                <label>Ngày kỳ vọng/kết thúc</label>
                <span v-if="!opportunityDetailEditing">{{ formatValue(opportunityDetail.document.expected_closing, 'expected_closing') }}</span>
                <input v-else type="date" v-model="opportunityDetailForm.expected_closing">
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Lý do thắng/thua', (opportunityDetail.document.lost_reasons || []).join(', '))">
                <label>Lý do thắng/thua</label>
                <span>{{ (opportunityDetail.document.lost_reasons || []).join(', ') || '- Không chọn -' }}</span>
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Lý do khác', opportunityDetail.document.custom_result_other_reason)">
                <label>Lý do khác</label>
                <span>{{ opportunityDetail.document.custom_result_other_reason || '—' }}</span>
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Nguồn gốc', opportunityDetail.document.source)">
                <label>Nguồn gốc</label>
                <span v-if="!opportunityDetailEditing">{{ opportunityDetail.document.source || '—' }}</span>
                <select v-else v-model="opportunityDetailForm.source">
                  <option v-for="s in (opportunityFormOptions.sources || [])" :key="s.name" :value="s.name">{{ s.name }}</option>
                </select>
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Khu vực', opportunityDetail.document.territory)">
                <label>Khu vực</label>
                <span v-if="!opportunityDetailEditing">{{ opportunityDetail.document.territory || '—' }}</span>
                <select v-else v-model="opportunityDetailForm.territory">
                  <option v-for="t in (opportunityFormOptions.territories || [])" :key="t.name" :value="t.name">{{ t.name }}</option>
                </select>
              </div>
            </div>

            <div class="opp-info-section" style="grid-column: 1 / -1" v-show="showOpportunityDetailField('Mô tả', opportunityDetail.document.notes)">
              <h4>Thông tin mô tả</h4>
              <div class="opp-field-row">
                <label>Mô tả</label>
                <span style="white-space:pre-wrap">{{ stripHtml(opportunityDetail.document.notes || '') || '—' }}</span>
              </div>
            </div>

            <div class="opp-info-section" style="grid-column: 1 / -1">
              <div class="opp-section-header">
                <h4 style="margin:0;border:0;padding:0">Thông tin hàng hóa</h4>
                <button class="crm-button op-panel-arrow" aria-label="Xem hàng hóa" @click="opportunityDetailTab = 'items'"><CRMIcon name="arrow-right" /></button>
              </div>
              <div v-if="!opportunityDetail.items.length" class="opp-section-empty"><CRMIcon name="package" /> Không có dữ liệu</div>
              <div v-else class="opp-items-wrap">
                <table class="opp-items-table">
                  <thead>
                    <tr><th>STT</th><th>Mã HH</th><th>Tên HH</th><th>Mô tả</th><th>ĐVT</th><th>SL</th><th>Đơn giá</th><th>Thành tiền</th></tr>
                  </thead>
                  <tbody>
                    <tr v-for="(item, idx) in opportunityDetail.items" :key="item.idx">
                      <td>{{ idx + 1 }}</td>
                      <td>{{ item.item_code }}</td>
                      <td>{{ item.item_name }}</td>
                      <td>{{ item.description || '—' }}</td>
                      <td>{{ item.uom }}</td>
                      <td>{{ item.qty }}</td>
                      <td>{{ formatValue(item.rate, 'opportunity_amount') }}</td>
                      <td>{{ formatValue(item.amount, 'opportunity_amount') }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <div class="opp-info-section">
              <h4>Thông tin địa chỉ</h4>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Quốc gia', opportunityDetail.document.custom_shipping_country)">
                <label>Quốc gia</label>
                <span v-if="!opportunityDetailEditing">{{ opportunityDetail.document.custom_shipping_country || '—' }}</span>
                <select v-else v-model="opportunityDetailForm.custom_shipping_country">
                  <option value="">- Không chọn -</option>
                  <option v-for="country in (opportunityFormOptions.countries || [])" :key="country.name" :value="country.name">{{ country.name === 'Vietnam' ? 'Việt Nam' : country.name }}</option>
                </select>
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Tỉnh/Thành phố', opportunityDetail.document.custom_shipping_state)">
                <label>Tỉnh/Thành phố</label>
                <span v-if="!opportunityDetailEditing">{{ opportunityDetail.document.custom_shipping_state || '—' }}</span>
                <input v-else v-model="opportunityDetailForm.custom_shipping_state">
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Quận/Huyện', opportunityDetail.document.custom_shipping_county)">
                <label>Quận/Huyện</label>
                <span v-if="!opportunityDetailEditing">{{ opportunityDetail.document.custom_shipping_county || '—' }}</span>
                <input v-else v-model="opportunityDetailForm.custom_shipping_county">
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Phường/Xã', opportunityDetail.document.custom_shipping_ward)">
                <label>Phường/Xã</label>
                <span v-if="!opportunityDetailEditing">{{ opportunityDetail.document.custom_shipping_ward || '—' }}</span>
                <input v-else v-model="opportunityDetailForm.custom_shipping_ward">
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Số nhà, Đường phố', opportunityDetail.document.custom_shipping_address_line1)">
                <label>Số nhà, Đường phố</label>
                <span v-if="!opportunityDetailEditing">{{ opportunityDetail.document.custom_shipping_address_line1 || '—' }}</span>
                <input v-else v-model="opportunityDetailForm.custom_shipping_address_line1">
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Mã vùng', opportunityDetail.document.custom_shipping_pincode)">
                <label>Mã vùng</label>
                <span v-if="!opportunityDetailEditing">{{ opportunityDetail.document.custom_shipping_pincode || '—' }}</span>
                <input v-else v-model="opportunityDetailForm.custom_shipping_pincode">
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Địa chỉ', opportunityDetail.document.custom_shipping_address)">
                <label>Địa chỉ</label>
                <span v-if="!opportunityDetailEditing" style="white-space:pre-wrap">{{ opportunityDetail.document.custom_shipping_address || '—' }}</span>
                <textarea v-else v-model="opportunityDetailForm.custom_shipping_address" rows="2" style="width:100%"></textarea>
              </div>
            </div>

            <div class="opp-info-section">
              <h4>Thông tin hệ thống</h4>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Người thực hiện', opportunityDetail.document.opportunity_owner)">
                <label>Người thực hiện</label>
                <span v-if="!opportunityDetailEditing">{{ opportunityDetail.document.opportunity_owner || '—' }}</span>
                <input v-else v-model="opportunityDetailForm.opportunity_owner">
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Đơn vị', opportunityDetail.document.custom_branch)">
                <label>Đơn vị</label>
                <span v-if="!opportunityDetailEditing">{{ opportunityDetail.document.custom_branch || '—' }}</span>
                <select v-else v-model="opportunityDetailForm.custom_branch">
                  <option value="">- Không chọn -</option>
                  <option v-for="b in (opportunityFormOptions.branches || [])" :key="b.name" :value="b.name">{{ b.name }}</option>
                </select>
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Quy trình bán hàng', opportunityDetail.document.custom_sales_process)">
                <label>Quy trình bán hàng</label>
                <span v-if="!opportunityDetailEditing">{{ opportunityDetail.document.custom_sales_process || '—' }}</span>
                <input v-else v-model="opportunityDetailForm.custom_sales_process">
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Người liên quan', opportunityDetail.document.custom_related_person)">
                <label>Người liên quan</label>
                <span v-if="!opportunityDetailEditing" style="white-space:pre-wrap">{{ opportunityDetail.document.custom_related_person || '—' }}</span>
                <textarea v-else v-model="opportunityDetailForm.custom_related_person" rows="2" style="width:100%"></textarea>
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Đối tác/CTV giới thiệu', opportunityDetail.document.custom_referral_partner)">
                <label>Đối tác/CTV giới thiệu</label>
                <span v-if="!opportunityDetailEditing">{{ opportunityDetail.document.custom_referral_partner || '—' }}</span>
                <select v-else v-model="opportunityDetailForm.custom_referral_partner">
                  <option value="">- Không chọn -</option>
                  <option v-for="c in (opportunityFormOptions.customers || [])" :key="c.name" :value="c.name">{{ c.customer_name || c.name }}</option>
                </select>
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Dùng chung', opportunityDetail.document.custom_is_shared)">
                <label>Dùng chung</label>
                <span v-if="!opportunityDetailEditing">{{ opportunityDetail.document.custom_is_shared ? 'Có' : 'Không' }}</span>
                <input v-else v-model.number="opportunityDetailForm.custom_is_shared" type="checkbox" :true-value="1" :false-value="0">
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Mã cơ hội', opportunityDetail.document.custom_opportunity_code)">
                <label>Mã cơ hội</label>
                <span>{{ opportunityDetail.document.custom_opportunity_code || '—' }}</span>
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Mã tiềm năng', opportunityDetail.document.opportunity_from === 'Lead' ? opportunityDetail.document.party_name : '')">
                <label>Mã tiềm năng</label>
                <span>{{ (opportunityDetail.document.opportunity_from === 'Lead' && opportunityDetail.document.party_name) || '—' }}</span>
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Người tạo', opportunityDetail.document.owner_full_name)">
                <label>Người tạo</label>
                <span>{{ opportunityDetail.document.owner_full_name || '—' }}</span>
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Ngày tạo', opportunityDetail.document.creation)">
                <label>Ngày tạo</label>
                <span>{{ formatValue(opportunityDetail.document.creation, 'creation') }}</span>
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Người sửa', opportunityDetail.document.modified_by_full_name)">
                <label>Người sửa</label>
                <span>{{ opportunityDetail.document.modified_by_full_name || '—' }}</span>
              </div>
              <div class="opp-field-row" v-show="showOpportunityDetailField('Ngày sửa', opportunityDetail.document.modified)">
                <label>Ngày sửa</label>
                <span>{{ formatValue(opportunityDetail.document.modified, 'creation') }}</span>
              </div>
            </div>
          </div>
        </template>

        <template v-else-if="opportunityDetailTab === 'items'">
          <div class="opp-items-panel">
            <div class="opp-items-heading">
              <h4>Thông tin hàng hóa</h4>
              <button v-if="showUnreadyFeatures" class="opp-items-update-link" type="button" @click="notifyOpportunityAction('Cập nhật hàng hóa')"><CRMIcon name="edit" /> Cập nhật hàng hóa</button>
            </div>
            <div v-if="!opportunityDetail.items.length" class="crm-empty opp-tab-empty"><CRMIcon name="package" /><strong>Chưa có hàng hóa</strong><span>Hàng hóa của cơ hội sẽ hiển thị tại đây.</span></div>
            <template v-else>
              <div class="opp-items-wrap">
                <table class="opp-items-table">
                  <thead>
                    <tr>
                      <th class="opp-col-idx">STT</th><th>Mã HH</th><th>Tên HH</th><th class="opp-col-muted">Mô tả</th>
                      <th class="opp-col-muted">A-End</th><th class="opp-col-muted">Z-End</th><th>ĐVT</th>
                      <th class="opp-col-num">SL</th><th class="opp-col-num">Đơn giá</th><th class="opp-col-num">Thành tiền</th>
                      <th class="opp-col-num">Tỷ lệ CK</th><th class="opp-col-num">Tiền CK</th>
                      <th class="opp-col-num opp-col-net">Đơn giá sau CK</th><th class="opp-col-num opp-col-net opp-col-emphasis">Thành tiền sau CK</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(item, idx) in opportunityDetail.items" :key="item.idx">
                      <td class="opp-col-idx">{{ idx + 1 }}</td>
                      <td><strong>{{ item.item_code }}</strong></td>
                      <td>{{ item.item_name }}</td>
                      <td class="opp-col-muted">{{ item.description || '—' }}</td>
                      <td class="opp-col-muted">{{ item.custom_installation_point_a_end || '—' }}</td>
                      <td class="opp-col-muted">{{ item.custom_installation_point_z_end || '—' }}</td>
                      <td>{{ item.uom }}</td>
                      <td class="opp-col-num">{{ item.qty }}</td>
                      <td class="opp-col-num">{{ formatValue(item.rate, 'opportunity_amount') }}</td>
                      <td class="opp-col-num">{{ formatValue(item.amount, 'opportunity_amount') }}</td>
                      <td class="opp-col-num">{{ item.custom_discount_percentage }}%</td>
                      <td class="opp-col-num">{{ formatValue(item.custom_discount_amount, 'opportunity_amount') }}</td>
                      <td class="opp-col-num opp-col-net">{{ formatValue(item.custom_net_rate, 'opportunity_amount') }}</td>
                      <td class="opp-col-num opp-col-net opp-col-emphasis">{{ formatValue(item.custom_net_amount, 'opportunity_amount') }}</td>
                    </tr>
                  </tbody>
                  <tfoot>
                    <tr class="opp-items-total">
                      <td colspan="9" class="opp-col-num">Tổng cộng</td>
                      <td class="opp-col-num">{{ formatValue(opportunityDetail.items.reduce((s,i) => s + (i.amount||0), 0), 'opportunity_amount') }}</td>
                      <td></td>
                      <td class="opp-col-num">{{ formatValue(opportunityDetail.items.reduce((s,i) => s + (i.custom_discount_amount||0), 0), 'opportunity_amount') }}</td>
                      <td></td>
                      <td class="opp-col-num opp-col-emphasis">{{ formatValue(opportunityDetail.items.reduce((s,i) => s + (i.custom_net_amount||0), 0), 'opportunity_amount') }}</td>
                    </tr>
                  </tfoot>
                </table>
              </div>
              <footer class="opp-items-footer"><strong>Tổng số {{ opportunityDetail.items.length }}</strong></footer>
            </template>
          </div>
        </template>

        <template v-else-if="opportunityDetailTab === 'notes'">
          <div class="opp-sales-misa">
            <aside class="opp-sales-subnav">
              <button type="button" :class="{ active: opportunityNotesSection === 'notes' }" @click="opportunityNotesSection = 'notes'">
                <CRMIcon name="document" /><span>Ghi chú</span>
              </button>
              <button type="button" :class="{ active: opportunityNotesSection === 'attachments' }" @click="opportunityNotesSection = 'attachments'">
                <CRMIcon name="package" /><span>Tài liệu đính kèm</span><em v-if="opportunityDetail.attachments.length">{{ opportunityDetail.attachments.length }}</em>
              </button>
            </aside>

            <section class="opp-sales-panel">
              <div v-if="opportunityNotesSection === 'notes'" class="opp-sales-card opp-notes-card">
                <div class="opp-sales-panel-head">
                  <h4>Ghi chú</h4>
                  <button type="button" class="opp-notes-toggle" :aria-expanded="!opportunityNotesCollapsed" :data-tooltip="opportunityNotesCollapsed ? 'Mở rộng' : 'Thu gọn'" @click="opportunityNotesCollapsed = !opportunityNotesCollapsed">
                    <CRMIcon name="chevron" />
                  </button>
                </div>
                <div v-show="!opportunityNotesCollapsed" class="opp-notes-body">
                  <input v-model="opportunityDetailComment" class="opp-notes-quick-input" placeholder="Thêm ghi chú" @keyup.enter="saveOpportunityDetailComment">
                  <div v-if="opportunityDetail.comments.length" class="profile-timeline-list">
                    <article v-for="c in opportunityDetail.comments" :key="c.name">
                      <strong>{{ c.comment_by_fullname || c.comment_by || 'CRM' }}</strong>
                      <span>{{ formatValue(c.creation, 'creation') }}</span>
                      <p>{{ stripHtml(c.content || '') }}</p>
                    </article>
                  </div>
                </div>
              </div>

              <div v-else class="opp-sales-card">
                <div class="opp-sales-panel-head">
                  <h4>Tài liệu đính kèm <button type="button" class="opp-notes-refresh" data-tooltip="Làm mới" @click="loadOpportunityDetail(opportunityDetailName)"><CRMIcon name="refresh" /></button></h4>
                  <div>
                    <button class="opp-sales-link" type="button" @click="addOpportunityAttachmentLink"><CRMIcon name="link" /> Thêm liên kết</button>
                    <button class="opp-sales-link" type="button" :disabled="opportunityAttachmentUploading" @click="uploadOpportunityAttachment"><CRMIcon name="paperclip" /> {{ opportunityAttachmentUploading ? 'Đang tải...' : 'Thêm tệp' }}</button>
                  </div>
                </div>
                <div class="opp-sales-table-wrap">
                  <table class="opp-sales-table">
                    <thead><tr><th>Tên tài liệu</th><th>Người đính kèm</th><th>Ngày đính kèm</th><th>Dung lượng</th></tr></thead>
                    <tbody v-if="opportunityDetail.attachments.length">
                      <tr v-for="f in opportunityDetail.attachments" :key="f.name">
                        <td><a :href="f.file_url" target="_blank" class="opp-attachment-link"><CRMIcon name="document" /> {{ f.file_name }}</a></td>
                        <td>{{ f.owner || '—' }}</td>
                        <td>{{ formatValue(f.creation, 'creation') }}</td>
                        <td>{{ formatFileSize(f.file_size) }}</td>
                      </tr>
                    </tbody>
                  </table>
                  <div v-if="!opportunityDetail.attachments.length" class="misa-table-empty"><CRMIcon name="document" /><span>Không có bản ghi nào</span></div>
                </div>
              </div>
            </section>
          </div>
        </template>

        <template v-else-if="opportunityDetailTab === 'contacts'">
          <div class="opp-section-card opp-list-card">
            <div class="opp-section-header">
              <h4>Liên hệ <button type="button" class="opp-notes-refresh" data-tooltip="Làm mới" @click="loadOpportunityDetail(opportunityDetailName)"><CRMIcon name="refresh" /></button></h4>
              <div>
                <button v-if="showUnreadyFeatures" class="opp-sales-link" type="button" @click="notifyOpportunityAction('Thêm liên hệ')"><CRMIcon name="plus" /> Thêm</button>
                <button v-if="showUnreadyFeatures" class="opp-sales-link" type="button" @click="notifyOpportunityAction('Thêm nhanh liên hệ')"><CRMIcon name="plus" /> Thêm nhanh</button>
                <button v-if="showUnreadyFeatures" class="opp-sales-link" type="button" @click="notifyOpportunityAction('Chọn liên hệ')"><CRMIcon name="checkcircle" /> Chọn</button>
              </div>
            </div>
            <div class="opp-sales-table-wrap">
              <table class="opp-sales-table">
                <thead>
                  <tr>
                    <th>Xưng hô</th><th>Họ và tên</th><th>Chức danh</th>
                    <th>ĐT di động</th><th>ĐT cơ quan</th>
                    <th>Email cơ quan</th><th>Email cá nhân</th><th>Địa chỉ</th>
                  </tr>
                </thead>
                <tbody v-if="opportunityDetail.contacts.length">
                  <tr v-for="c in opportunityDetail.contacts" :key="c.name" @click="openContactDetail(c)">
                    <td>{{ c.salutation || '—' }}</td>
                    <td><a href="#" @click.prevent.stop="openContactDetail(c)">{{ c.full_name }}</a></td>
                    <td>{{ c.designation || '—' }}</td>
                    <td><a v-if="c.mobile_no" :href="'tel:' + c.mobile_no" @click.stop>{{ c.mobile_no }}</a><span v-else>—</span></td>
                    <td><a v-if="c.phone" :href="'tel:' + c.phone" @click.stop>{{ c.phone }}</a><span v-else>—</span></td>
                    <td>—</td>
                    <td>{{ c.email_id || '—' }}</td>
                    <td>{{ c.address || '—' }}</td>
                  </tr>
                </tbody>
              </table>
              <div v-if="!opportunityDetail.contacts.length" class="misa-table-empty"><CRMIcon name="contact" /><span>Không có bản ghi nào</span></div>
            </div>
            <div class="opp-sales-footer"><span>Tổng số {{ opportunityDetail.contacts.length }}</span><span>Số dòng/trang <b>20</b> · 1 - {{ opportunityDetail.contacts.length }}</span></div>
          </div>
        </template>

        <template v-else-if="opportunityDetailTab === 'sales'">
          <div class="opp-sales-misa">
            <aside class="opp-sales-subnav">
              <button
                v-for="item in opportunitySalesMenu"
                :key="item.key"
                type="button"
                :class="{ active: opportunitySalesSection === item.key }"
                @click="opportunitySalesSection = item.key">
                <CRMIcon :name="item.icon" />
                <span>{{ item.label }}</span>
                <em v-if="item.count">{{ item.count }}</em>
              </button>
            </aside>

            <section class="opp-sales-panel">
              <div v-if="opportunitySalesSection === 'orders'" class="opp-sales-card">
                <div class="opp-sales-panel-head">
                  <h4>Đơn hàng</h4>
                  <div>
                    <button class="opp-sales-link" type="button" @click="loadOpportunityDetail(opportunityDetailName)"><CRMIcon name="refresh" /> Làm mới</button>
                    <button class="opp-sales-link" type="button" @click="openCreateSO(opportunityDetail.document.party_name, opportunityDetail.document.customer_name || opportunityDetail.document.party_name, opportunityDetailName)"><CRMIcon name="plus" /> Thêm Đơn hàng</button>
                  </div>
                </div>
                <div v-if="!opportunityDetail.orders.length" class="opp-sales-empty">Không có bản ghi nào</div>
                <template v-else>
                  <div class="opp-sales-table-wrap">
                    <table class="opp-sales-table">
                      <thead><tr><th>Số đơn hàng/hợp đồng</th><th>Giá trị đơn hàng</th><th>Tình trạng</th><th>Tình trạng ghi doanh số</th><th>Người thực hiện</th><th>Đơn vị</th><th>Ngày đặt hàng</th></tr></thead>
                      <tbody>
                        <tr v-for="o in opportunityDetail.orders" :key="o.name" @click="openRelated('Sales Order', o)">
                          <td><a href="#" @click.prevent.stop="openRelated('Sales Order', o)">{{ o.name }}</a></td>
                          <td>{{ formatValue(o.grand_total, 'grand_total') }}</td>
                          <td><span class="opp-sales-status ok">{{ o.status || '—' }}</span></td>
                          <td>Đã ghi</td>
                          <td>{{ o.owner || '—' }}</td>
                          <td>{{ o.company || opportunityDetail.document.company || '—' }}</td>
                          <td>{{ formatValue(o.transaction_date, 'date') }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <div class="opp-sales-footer"><span>Tổng số {{ opportunityDetail.orders.length }}</span><span>Số dòng/trang <b>20</b> · 1 - {{ opportunityDetail.orders.length }}</span></div>
                </template>
              </div>

              <div v-else-if="opportunitySalesSection === 'quotations'" class="opp-sales-card">
                <div class="opp-sales-panel-head">
                  <h4>Báo giá</h4>
                  <div>
                    <button class="opp-sales-link" type="button" @click="loadOpportunityDetail(opportunityDetailName)"><CRMIcon name="refresh" /> Làm mới</button>
                    <button class="opp-sales-link" type="button" @click="openCreateQuotation(opportunityDetail.document.party_name, opportunityDetail.document.customer_name || opportunityDetail.document.party_name, opportunityDetailName)"><CRMIcon name="plus" /> Thêm Báo giá</button>
                  </div>
                </div>
                <div v-if="!opportunityDetail.quotations.length" class="opp-sales-empty">Không có bản ghi nào</div>
                <template v-else>
                  <div class="opp-sales-table-wrap">
                    <table class="opp-sales-table">
                      <thead><tr><th>Số báo giá</th><th>Ngày báo giá</th><th>Tổng tiền</th><th>Tình trạng</th><th>Mô tả</th></tr></thead>
                      <tbody>
                        <tr v-for="q in opportunityDetail.quotations" :key="q.name" @click="openRelated('Quotation', q)">
                          <td><a href="#" @click.prevent.stop="openRelated('Quotation', q)">{{ q.name }}</a></td>
                          <td>{{ formatValue(q.transaction_date, 'date') }}</td>
                          <td>{{ formatValue(q.grand_total, 'grand_total') }}</td>
                          <td>{{ q.status || '—' }}</td>
                          <td>{{ opportunityDetail.document.title || '—' }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <div class="opp-sales-footer"><span>Tổng số {{ opportunityDetail.quotations.length }}</span><span>Số dòng/trang <b>20</b> · 1 - {{ opportunityDetail.quotations.length }}</span></div>
                </template>
              </div>

              <div v-else-if="opportunitySalesSection === 'stage_history'" class="opp-sales-card">
                <div class="opp-sales-panel-head">
                  <h4>Lịch sử giai đoạn</h4>
                  <button class="opp-sales-link" type="button" @click="loadOpportunityDetail(opportunityDetailName)"><CRMIcon name="refresh" /> Làm mới</button>
                </div>
                <div v-if="!(opportunityDetail.stage_history || []).length" class="opp-sales-empty">Không có bản ghi nào</div>
                <div v-else class="opp-sales-table-wrap">
                  <table class="opp-sales-table">
                    <thead><tr><th>Giai đoạn</th><th>Số tiền</th><th>Tỷ lệ thành công</th><th>Doanh số kỳ vọng</th><th>Ngày kết thúc</th><th>Thời gian sửa</th><th>Người sửa</th></tr></thead>
                    <tbody>
                      <tr v-for="row in opportunityDetail.stage_history" :key="row.name || row.modified">
                        <td>{{ row.stage || '—' }}</td>
                        <td>{{ formatValue(row.amount, 'grand_total') }}</td>
                        <td>{{ row.probability || 0 }}</td>
                        <td>{{ formatValue(row.expected_revenue, 'grand_total') }}</td>
                        <td>{{ formatValue(row.expected_closing, 'date') }}</td>
                        <td>{{ formatValue(row.modified, 'modified') }}</td>
                        <td>{{ row.modified_by || '—' }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <div v-else-if="opportunitySalesSection === 'purchase_requests'" class="opp-sales-card">
                <div class="opp-sales-panel-head">
                  <h4>Yêu cầu mua hàng</h4>
                  <div>
                    <button class="opp-sales-link" type="button" @click="loadOpportunityDetail(opportunityDetailName)"><CRMIcon name="refresh" /> Làm mới</button>
                    <button class="opp-sales-link" type="button" @click="createOpportunityPurchaseRequest"><CRMIcon name="plus" /> Thêm Yêu cầu mua hàng</button>
                  </div>
                </div>
                <div v-if="!(opportunityDetail.purchase_requests || []).length" class="opp-sales-empty">Không có bản ghi nào</div>
                <template v-else>
                  <div class="opp-sales-table-wrap">
                    <table class="opp-sales-table">
                      <thead><tr><th>Số yêu cầu</th><th>Ngày yêu cầu</th><th>Ngày cần hàng</th><th>Tình trạng</th><th>Đơn vị</th><th>Người tạo</th></tr></thead>
                      <tbody>
                        <tr v-for="pr in opportunityDetail.purchase_requests" :key="pr.name" @click="openRelated('Purchase Request', pr)">
                          <td><a href="#" @click.prevent.stop="openRelated('Purchase Request', pr)">{{ pr.name }}</a></td>
                          <td>{{ formatValue(pr.transaction_date, 'date') }}</td>
                          <td>{{ formatValue(pr.schedule_date, 'date') }}</td>
                          <td>{{ pr.status || '—' }}</td>
                          <td>{{ pr.company || opportunityDetail.document.company || '—' }}</td>
                          <td>{{ pr.owner || '—' }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <div class="opp-sales-footer"><span>Tổng số {{ opportunityDetail.purchase_requests.length }}</span><span>Số dòng/trang <b>20</b> · 1 - {{ opportunityDetail.purchase_requests.length }}</span></div>
                </template>
              </div>
            </section>
          </div>
        </template>

        <template v-else-if="opportunityDetailTab === 'activities'">
          <div class="opp-section-card opp-list-card">
            <div class="opp-section-header">
              <h4>Hoạt động <button type="button" class="opp-notes-refresh" data-tooltip="Làm mới" @click="loadOpportunityDetail(opportunityDetailName)"><CRMIcon name="refresh" /></button></h4>
              <div>
                <button class="opp-sales-link" type="button" @click="createOpportunityActivity('Nhiệm vụ')"><CRMIcon name="task" /> Thêm Nhiệm vụ</button>
                <button class="opp-sales-link" type="button" @click="createOpportunityActivity('Lịch hẹn')"><CRMIcon name="calendar" /> Thêm Lịch hẹn</button>
                <button class="opp-sales-link" type="button" @click="createOpportunityActivity('Cuộc gọi')"><CRMIcon name="phone" /> Thêm Cuộc gọi</button>
              </div>
            </div>
            <div class="opp-sales-table-wrap">
              <table class="opp-sales-table">
                <thead>
                  <tr>
                    <th>Tên hoạt động</th><th>Loại hoạt động</th><th>Hạn hoàn thành</th>
                    <th>Trạng thái</th><th>Ngày kết thúc</th><th>Người thực hiện</th>
                  </tr>
                </thead>
                <tbody v-if="opportunityDetail.activities.length">
                  <tr v-for="a in opportunityDetail.activities" :key="a.activity_doctype + '-' + a.name" @click="openActivityRecord(a.name, a.activity_doctype)">
                    <td><a href="#" @click.prevent.stop="openActivityRecord(a.name, a.activity_doctype)">{{ a.subject || a.description || a.name }}</a></td>
                    <td>{{ a.activity_doctype === 'Event' ? (a.event_category || 'Sự kiện') : 'Nhiệm vụ' }}</td>
                    <td>{{ formatValue(a.date || a.starts_on, 'modified') }}</td>
                    <td><span class="misa-activity-status" :class="'status-' + String(a.status || '').toLowerCase()">{{ a.status || '—' }}</span></td>
                    <td>{{ formatValue(a.ends_on || (['Closed', 'Cancelled', 'Completed'].includes(a.status) ? a.modified : null), 'modified') }}</td>
                    <td>{{ a.assigned_by_full_name || a.owner || '—' }}</td>
                  </tr>
                </tbody>
              </table>
              <div v-if="!opportunityDetail.activities.length" class="misa-table-empty"><CRMIcon name="activity" /><span>Không có bản ghi nào</span></div>
            </div>
            <div class="opp-sales-footer"><span>Tổng số {{ opportunityDetail.activities.length }}</span><span>Số dòng/trang <b>20</b> · 1 - {{ opportunityDetail.activities.length }}</span></div>
          </div>
        </template>

        <template v-else-if="opportunityDetailTab === 'chat'">
          <div class="customer-conversation-shell">
            <header class="customer-conversation-heading">
              <div><h2>Trao đổi</h2><p>Theo dõi và cập nhật nội dung trao đổi về cơ hội này.</p></div>
              <span>{{ opportunityDetail.comments.length }} bình luận</span>
            </header>
            <div v-if="opportunityDetail.comments.length" class="customer-comment-feed">
              <article v-for="c in opportunityDetail.comments" :key="c.name" class="customer-comment">
                <span class="customer-comment-avatar" aria-hidden="true">{{ (c.comment_by_fullname || c.comment_by || 'CRM').slice(0, 1).toUpperCase() }}</span>
                <div class="customer-comment-content">
                  <div class="customer-comment-meta"><strong>{{ c.comment_by_fullname || c.comment_by }}</strong><time>{{ formatValue(c.creation, 'creation') }}</time></div>
                  <div class="customer-comment-bubble"><p>{{ stripHtml(c.content || '') }}</p></div>
                </div>
              </article>
            </div>
            <div v-else class="customer-conversation-empty"><CRMIcon name="message" /><strong>Chưa có nội dung trao đổi</strong><span>Hãy bắt đầu bằng bình luận đầu tiên về cơ hội này.</span></div>
            <div class="customer-comment-composer">
              <span class="customer-comment-avatar current" aria-hidden="true">{{ (boot?.full_name || boot?.user || 'CRM').slice(0, 1).toUpperCase() }}</span>
              <div class="customer-comment-editor">
                <textarea v-model="opportunityDetailComment" rows="3" aria-label="Nội dung trao đổi" placeholder="Viết bình luận..." @keydown.ctrl.enter.prevent="saveOpportunityDetailComment"></textarea>
                <div class="customer-comment-actions">
                  <button type="button" data-tooltip="Mở tài liệu đính kèm" @click="opportunityDetailTab = 'notes'; opportunityNotesSection = 'attachments'"><CRMIcon name="package" /> Đính kèm</button>
                  <span>Ctrl + Enter để gửi</span>
                  <button type="button" class="crm-button primary" :disabled="!opportunityDetailComment.trim()" @click="saveOpportunityDetailComment"><CRMIcon name="send" /> Gửi</button>
                </div>
              </div>
            </div>
          </div>
        </template>

        <template v-else-if="opportunityDetailTab === 'support'">
          <div class="crm-empty opp-tab-empty"><CRMIcon name="settings" /><strong>Chưa có dữ liệu hỗ trợ được liên kết</strong><span>Spec hiện chưa xác định quan hệ giữa Cơ hội và yêu cầu hỗ trợ. Hệ thống không tự tạo dữ liệu để tránh sai nghiệp vụ.</span></div>
        </template>

      </div>
    </div>
    <aside class="opp-detail-rail">
      <div class="opp-rail-head">
        <div class="opp-activity-tabs">
          <button :class="['atab', { active: oppActivityPanelTab === 'activity' }]" @click="oppActivityPanelTab = 'activity'">Hoạt động</button>
          <button :class="['atab', { active: oppActivityPanelTab === 'purchase' }]" @click="oppActivityPanelTab = 'purchase'">Mua hàng</button>
        </div>
        <button class="op-rail-select" type="button" @click="oppActivityPanelTab = oppActivityPanelTab === 'activity' ? 'purchase' : 'activity'">{{ oppActivityPanelTab === 'activity' ? 'Cơ hội' : 'Mua hàng' }} <CRMIcon name="chevron" /></button>
      </div>
      <div v-if="oppActivityPanelTab === 'activity'" class="opp-activity-list">
        <div v-for="item in opportunityDetail.timeline.slice(0, 12)" :key="item.name"
             class="opp-timeline-item" :class="{ 'opp-timeline-item--link': item.activity_type === 'task' }"
             :data-tooltip="item.activity_type === 'task' ? 'Mở hoạt động' : ''"
             @click="item.activity_type === 'task' && openActivityRecord(item.name, 'ToDo')">
          <div class="opp-tl-avatar">{{ (item.owner || 'A')[0].toUpperCase() }}</div>
          <div class="opp-tl-body">
            <strong>{{ item.subject || item.description || 'Hoạt động' }}</strong>
            <p>{{ stripHtml(item.content || item.description || '') }}</p>
            <small>{{ formatValue(item.creation, 'creation') }}</small>
          </div>
        </div>
        <div v-if="!opportunityDetail.timeline.length" class="opp-rail-empty"><CRMIcon name="activity" /><strong>Chưa có hoạt động</strong><span>Các cuộc gọi, lịch hẹn và công việc sẽ xuất hiện tại đây.</span></div>
      </div>
      <div v-else class="opp-activity-list">
        <div v-for="o in opportunityDetail.orders" :key="'o'+o.name" class="opp-timeline-item">
          <div class="opp-tl-avatar" style="background:#eef2ff;color:#4f46e5"><CRMIcon name="order" /></div>
          <div class="opp-tl-body"><strong>{{ o.name }}</strong><p>Đơn hàng · {{ formatValue(o.grand_total, 'grand_total') }}</p><small>{{ formatValue(o.transaction_date, 'transaction_date') }}</small></div>
        </div>
        <div v-for="q in opportunityDetail.quotations" :key="'q'+q.name" class="opp-timeline-item">
          <div class="opp-tl-avatar" style="background:#fef3c7;color:#92400e"><CRMIcon name="quotation" /></div>
          <div class="opp-tl-body"><strong>{{ q.name }}</strong><p>Báo giá · {{ formatValue(q.grand_total, 'grand_total') }}</p><small>{{ formatValue(q.transaction_date, 'transaction_date') }}</small></div>
        </div>
        <div v-for="i in opportunityDetail.invoices" :key="'i'+i.name" class="opp-timeline-item">
          <div class="opp-tl-avatar" style="background:#dcfce7;color:#166534"><CRMIcon name="customer" /></div>
          <div class="opp-tl-body"><strong>{{ i.name }}</strong><p>Hóa đơn · {{ formatValue(i.grand_total, 'grand_total') }}</p><small>{{ formatValue(i.posting_date, 'posting_date') }}</small></div>
        </div>
        <div v-if="!opportunityDetail.orders.length && !opportunityDetail.quotations.length && !opportunityDetail.invoices.length" class="opp-rail-empty"><CRMIcon name="order" /><strong>Chưa có dữ liệu bán hàng</strong><span>Báo giá, đơn hàng và hóa đơn sẽ xuất hiện tại đây.</span></div>
      </div>
    </aside>
  </div>

  <teleport to="body"><div v-if="opportunitySummaryDialogOpen" class="column-dialog-backdrop customer-summary-dialog-backdrop" @click.self="cancelOpportunitySummaryDialog">
    <section class="customer-summary-dialog" role="dialog" aria-modal="true" aria-labelledby="opportunity-summary-dialog-title">
      <header>
        <div>
          <h2 id="opportunity-summary-dialog-title">Tùy chỉnh tóm tắt</h2>
          <p>Chọn trường thông tin để hiển thị trong phần thông tin tóm tắt.</p>
        </div>
        <button class="customer-summary-close" data-tooltip="Đóng" aria-label="Đóng" @click="cancelOpportunitySummaryDialog">×</button>
      </header>
      <div class="customer-summary-picker">
        <section>
          <h3>Chưa chọn <span>{{ availableOpportunitySummaryFields.length }}</span></h3>
          <label class="customer-summary-search">
            <CRMIcon name="search" />
            <input v-model="opportunitySummarySearch" placeholder="Tìm kiếm trường" autofocus>
          </label>
          <div class="customer-summary-field-list">
            <button v-for="field in availableOpportunitySummaryFields" :key="field.field" type="button" @click="addOpportunitySummaryField(field.field)">
              <span>{{ field.label }}</span><b aria-hidden="true">+</b>
            </button>
            <p v-if="!availableOpportunitySummaryFields.length" class="crm-empty">Không còn trường phù hợp.</p>
          </div>
        </section>
        <section>
          <h3>Được chọn <span>{{ selectedOpportunitySummaryFields.length }}</span></h3>
          <div class="customer-summary-field-list customer-summary-field-list--selected">
            <button v-for="field in selectedOpportunitySummaryFields" :key="field.field" type="button" @click="removeOpportunitySummaryField(field.field)">
              <span>{{ field.label }}</span><b aria-hidden="true">×</b>
            </button>
            <p v-if="!selectedOpportunitySummaryFields.length" class="crm-empty">Chưa chọn trường nào.</p>
          </div>
        </section>
      </div>
      <footer>
        <button class="column-default" type="button" @click="resetOpportunitySummaryFields">Mặc định</button>
        <div>
          <button class="crm-button" type="button" @click="cancelOpportunitySummaryDialog">Hủy</button>
          <button class="crm-button primary" type="button" @click="saveOpportunitySummaryFields">Lưu</button>
        </div>
      </footer>
    </section>
  </div></teleport>
</main>
`;
