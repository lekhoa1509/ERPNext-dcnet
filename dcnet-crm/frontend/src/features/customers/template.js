export default `
        <main v-else-if="route === 'customer-detail'" class="customer-profile customer-profile--misa">
          <header class="profile-header">
            <div class="profile-heading">
              <button class="profile-back" data-tooltip="Quay lại danh sách" @click="backToCustomers">←</button>
              <h1>{{ detail?.document?.name || customerName }}</h1>
            </div>
            <div class="profile-header-actions">
              <template v-if="customerEditing">
                <button class="crm-button" :disabled="customerSaving" @click="cancelCustomerEdit">Hủy</button>
                <button class="crm-button primary" :disabled="customerSaving" @click="saveCustomerDetails">
                  {{ customerSaving ? 'Đang lưu...' : 'Lưu' }}
                </button>
              </template>
              <button v-else-if="detail?.can_write" class="crm-button profile-edit-btn" @click="beginCustomerEdit"><CRMIcon name="edit" /> Sửa</button>
              <span class="profile-generate-group">
                <button class="profile-generate" @click="createCustomerOrder"><CRMIcon name="cart" /> Sinh đơn hàng</button>
                <button class="profile-generate-caret" @click="createCustomerOrder"><CRMIcon name="chevron" /></button>
              </span>
              <details class="crm-detail-more">
                <summary class="icon-button profile-more-btn" data-tooltip="Thêm thao tác" aria-label="Thêm thao tác"><CRMIcon name="more" /></summary>
                <div class="crm-detail-more-menu" role="menu">
                  <button type="button" role="menuitem" @click="openRelated('Customer', detail.document); $event.currentTarget.closest('details').removeAttribute('open')"><CRMIcon name="document" /><span>Mở biểu mẫu hệ thống</span></button>
                  <div class="crm-detail-more-separator"></div>
                  <button type="button" role="menuitem" @click="openAuditLog('Customer', detail.document.name); $event.currentTarget.closest('details').removeAttribute('open')"><CRMIcon name="history" /><span>Nhật ký</span></button>
                </div>
              </details>
            </div>
          </header>

          <section v-if="detail" class="profile-shell">
            <aside class="profile-summary-panel">
              <div class="profile-identity">
                <div class="profile-avatar">
                  <img v-if="detail.document.image" :src="detail.document.image" alt="">
                  <CRMIcon v-else name="customer" />
                </div>
                <div><h2>{{ detail.document.customer_name }}</h2><span>{{ detail.document.customer_type === 'Company' ? 'Công ty' : 'Cá nhân' }}</span></div>
              </div>
              <button class="profile-tag" @click="promptCustomerTag"><CRMIcon name="tag" /> Thêm thẻ</button>
              <div class="profile-quick-actions">
                <a :href="customerDisplayPhone ? 'tel:' + customerDisplayPhone : undefined" data-tooltip="Gọi điện"><CRMIcon name="phone" /></a>
                <button data-tooltip="Tạo công việc" @click="openActivityDialog('task')"><CRMIcon name="task" /></button>
                <button data-tooltip="Tạo lịch" @click="openActivityDialog('meeting')"><CRMIcon name="calendar" /></button>
                <a :href="customerDisplayEmail ? 'mailto:' + customerDisplayEmail : undefined" data-tooltip="Gửi email"><CRMIcon name="email" /></a>
                <button data-tooltip="Thêm ghi chú" @click="customerDetailTab = 'notes'; customerNoteSection = 'notes'"><CRMIcon name="contact" /></button>
              </div>

              <section class="profile-facts">
                <header><h3>Thông tin tóm tắt</h3><button data-tooltip="Tùy chỉnh thông tin tóm tắt" aria-label="Tùy chỉnh thông tin tóm tắt" @click="openCustomerSummaryDialog"><CRMIcon name="sliders" /></button></header>
                <dl>
                  <div v-for="field in visibleCustomerSummaryFields" :key="field.field">
                    <dt>{{ field.label }}</dt><dd>{{ customerSummaryValue(field.field) }}</dd>
                  </div>
                  <div v-if="!visibleCustomerSummaryFields.length" class="profile-facts-empty">Chưa chọn trường hiển thị.</div>
                </dl>
              </section>
            </aside>

            <section class="profile-main">
              <nav class="profile-tabs">
                <button :class="{ active: customerDetailTab === 'overview' }" @click="customerDetailTab = 'overview'">Tổng quan</button>
                <button :class="{ active: customerDetailTab === 'details' }" @click="customerDetailTab = 'details'">Thông tin chi tiết</button>
                <button :class="{ active: customerDetailTab === 'contacts' }" @click="customerDetailTab = 'contacts'">Liên hệ <b v-if="customerDetailTabBadge('contacts')">{{ customerDetailTabBadge('contacts') }}</b></button>
                <button :class="{ active: customerDetailTab === 'activity' }" @click="customerDetailTab = 'activity'">Hoạt động <b v-if="customerDetailTabBadge('activity')">{{ customerDetailTabBadge('activity') }}</b></button>
                <button :class="{ active: customerDetailTab === 'sales' }" @click="customerDetailTab = 'sales'">Bán hàng <b v-if="customerDetailTabBadge('sales')">{{ customerDetailTabBadge('sales') }}</b></button>
                <button :class="{ active: customerDetailTab === 'support' }" @click="customerDetailTab = 'support'">Hỗ trợ</button>
                <button v-if="showUnreadyFeatures" :class="{ active: customerDetailTab === 'marketing' }" @click="customerDetailTab = 'marketing'">Marketing <b v-if="customerDetailTabBadge('marketing')">{{ customerDetailTabBadge('marketing') }}</b></button>
                <button :class="{ active: customerDetailTab === 'notes' }" @click="customerDetailTab = 'notes'">Ghi chú và đính kèm <b v-if="customerDetailTabBadge('notes')">{{ customerDetailTabBadge('notes') }}</b></button>
                <button :class="{ active: customerDetailTab === 'conversation' }" @click="customerDetailTab = 'conversation'">Trao đổi</button>
              </nav>

              <section v-if="customerDetailTab === 'overview'" class="profile-single-panel profile-overview-panel">
                <div class="profile-overview-main">
                  <header class="profile-overview-heading"><h2>Tổng quan Khách hàng</h2></header>
                  <section class="profile-overview-kpis">
                    <div class="ov-stat-card">
                      <span class="ov-stat-icon cyan"><CRMIcon name="order" /></span>
                      <div class="ov-stat-text">
                        <span class="ov-stat-label">Số lượng đơn hàng</span>
                        <strong class="ov-stat-value">{{ detail.summary?.order_count || 0 }}</strong>
                      </div>
                    </div>
                    <div class="ov-stat-card">
                      <span class="ov-stat-icon amber"><CRMIcon name="trend" /></span>
                      <div class="ov-stat-text">
                        <span class="ov-stat-label">Giá trị đơn hàng</span>
                        <strong class="ov-stat-value">{{ formatValue(detail.summary?.order_value, 'order_value') }}</strong>
                      </div>
                    </div>
                    <div class="ov-stat-card ov-stat-card--sync">
                      <span class="ov-stat-icon violet"><CRMIcon name="dollar" /></span>
                      <div class="ov-stat-text">
                        <span class="ov-stat-label">Công nợ</span>
                        <strong class="ov-stat-value">{{ formatValue(detail.summary?.outstanding, 'grand_total') }}</strong>
                        <span class="ov-stat-note">Hạn mức: {{ formatValue(detail.summary?.credit_limit, 'grand_total') }}</span>
                      </div>
                      <button type="button" class="ov-stat-sync" data-tooltip="Đồng bộ công nợ" aria-label="Đồng bộ công nợ" :disabled="loading" @click="loadCustomerDetail(detail.document.name)">
                        <CRMIcon name="refresh" /> Đồng bộ
                      </button>
                    </div>
                    <div class="ov-stat-card">
                      <span class="ov-stat-icon blue"><CRMIcon name="activity" /></span>
                      <div class="ov-stat-text">
                        <span class="ov-stat-label">Chu kỳ mua hàng</span>
                        <strong v-if="customerPurchaseCycleDays !== null" class="ov-stat-value">{{ customerPurchaseCycleDays }} ngày</strong>
                        <strong v-else class="ov-stat-value ov-stat-value--muted">Chưa đủ dữ liệu</strong>
                        <span v-if="customerDaysSinceLastOrder !== null" class="ov-stat-note">Đã {{ customerDaysSinceLastOrder }} ngày chưa mua</span>
                      </div>
                    </div>
                  </section>
                  <section class="profile-records profile-overview-purchased">
                    <div class="profile-records-heading"><div><h2>Hàng hóa đã mua</h2></div><button data-tooltip="Xem tất cả" @click="customerDetailTab = 'sales'; customerSalesSection = 'items'"><CRMIcon name="arrow-right" /></button></div>
                    <div v-if="detail.purchased_items.length" class="profile-table-wrap">
                      <table class="profile-related-table"><thead><tr><th>Mã hàng hóa</th><th>Tên hàng hóa</th><th>Loại hàng hóa</th><th>Số lượng</th><th>Doanh số</th></tr></thead><tbody><tr v-for="row in detail.purchased_items.slice(0, 5)" :key="row.item_code"><td><a href="#" @click.prevent>{{ row.item_code }}</a></td><td><a href="#" @click.prevent>{{ row.item_name || row.item_code }}</a></td><td>{{ row.item_group || '—' }}</td><td>{{ formatValue(row.qty) }}</td><td>{{ formatValue(row.amount, 'grand_total') }}</td></tr></tbody></table>
                    </div>
                    <p v-else class="profile-empty">Không có bản ghi nào</p>
                  </section>
                  <section class="profile-records profile-overview-conversation">
                    <div class="profile-records-heading"><div><h2>Nội dung trao đổi</h2></div><span class="profile-overview-conv-count">{{ customerConversationEntries.length }} bình luận</span></div>
                    <div v-if="customerConversationEntries.length" class="customer-comment-feed">
                      <article v-for="entry in customerConversationEntries" :key="entry.activity_type + '-' + entry.name" class="customer-comment">
                        <span class="customer-comment-avatar" aria-hidden="true">{{ (entry.sender || entry.comment_email || entry.owner || 'CRM').slice(0, 1).toUpperCase() }}</span>
                        <div class="customer-comment-content">
                          <div class="customer-comment-meta"><strong>{{ entry.sender || entry.comment_email || entry.owner || 'CRM' }}</strong><time>{{ formatValue(entry.creation, 'creation') }}</time></div>
                          <div class="customer-comment-bubble"><p>{{ stripHtml(entry.content || entry.subject || '') }}</p></div>
                        </div>
                      </article>
                    </div>
                    <p v-else class="profile-empty">Không có dữ liệu.</p>
                    <div class="customer-comment-composer">
                      <span class="customer-comment-avatar current" aria-hidden="true">{{ (boot?.full_name || boot?.user || 'CRM').slice(0, 1).toUpperCase() }}</span>
                      <div class="customer-comment-editor">
                        <textarea v-model="customerConversationText" rows="2" aria-label="Nội dung trao đổi" placeholder="Nhập nội dung..." @keydown.ctrl.enter.prevent="saveCustomerNoteFromDetail('conversation')"></textarea>
                        <div class="customer-comment-actions">
                          <button class="crm-button primary" type="button" :disabled="!customerConversationText.trim()" @click="saveCustomerNoteFromDetail('conversation')"><CRMIcon name="send" /> Gửi</button>
                        </div>
                      </div>
                    </div>
                  </section>
                </div>
                <aside class="profile-overview-side">
                  <section class="profile-overview-activity">
                    <header><h3>Hoạt động</h3></header>
                    <div v-if="detail.activities.length" class="cust-act-list">
                      <button v-for="item in detail.activities" :key="item.activity_type + '-' + item.name" class="cust-act-card" @click="openActivityRecord(item.name, item.activity_type === 'task' ? 'ToDo' : 'Event', detail.document.name, detail.document.customer_name)" data-tooltip="Mở hoạt động">
                        <span class="cust-act-ico"><CRMIcon :name="item.activity_type === 'task' ? 'task' : item.activity_type === 'call' ? 'phone' : 'calendar'" /></span>
                        <span class="cust-act-body">
                          <strong class="cust-act-title">{{ item.subject || item.name }}</strong>
                          <span class="cust-act-foot">
                            <em>{{ item.performed_by_name || item.performed_by || '—' }}</em>
                            <i>·</i>
                            <em>{{ formatValue(item.due_date, 'date') }}</em>
                          </span>
                        </span>
                      </button>
                    </div>
                    <p v-else class="crm-empty">Chưa có hoạt động liên quan.</p>
                  </section>
                </aside>
              </section>

              <div v-else-if="customerDetailTab === 'sales'" class="profile-tab-layout profile-sales-layout">
                <nav class="profile-subnav">
                  <button :class="{ active: customerSalesSection === 'orders' }" @click="customerSalesSection = 'orders'"><CRMIcon name="order" />Đơn hàng <b>{{ detail.orders.length }}</b></button>
                  <button :class="{ active: customerSalesSection === 'returns' }" @click="customerSalesSection = 'returns'"><CRMIcon name="customer" />Trả lại hàng bán <b v-if="detail.sales_returns.length">{{ detail.sales_returns.length }}</b></button>
                  <button :class="{ active: customerSalesSection === 'opportunities' }" @click="customerSalesSection = 'opportunities'"><CRMIcon name="opportunity" />Cơ hội <b>{{ detail.opportunities.length }}</b></button>
                  <button :class="{ active: customerSalesSection === 'quotations' }" @click="customerSalesSection = 'quotations'"><CRMIcon name="quotation" />Báo giá <b>{{ detail.quotations.length }}</b></button>
                  <button :class="{ active: customerSalesSection === 'invoices' }" @click="customerSalesSection = 'invoices'"><CRMIcon name="all" />Hóa đơn <b>{{ detail.invoices.length }}</b></button>
                  <button :class="{ active: customerSalesSection === 'items' }" @click="customerSalesSection = 'items'"><CRMIcon name="customer" />Hàng hóa đã mua <b v-if="detail.purchased_items.length">{{ detail.purchased_items.length }}</b></button>
                  <button :class="{ active: customerSalesSection === 'subsidiaries' }" @click="customerSalesSection = 'subsidiaries'"><CRMIcon name="contact" />Đại lý/Công ty con <b v-if="detail.subsidiaries.length">{{ detail.subsidiaries.length }}</b></button>
                </nav>
                <section class="profile-records">
                  <div class="profile-records-heading">
                    <div><h2>{{ customerSalesSectionLabel(customerSalesSection) }}</h2><button data-tooltip="Làm mới" @click="loadCustomerDetail(detail.document.name)"><CRMIcon name="refresh" /></button></div>
                    <button v-if="customerSalesSection === 'orders' && detail.can_create_order" @click="createCustomerOrder">+ Thêm Đơn hàng</button>
                  </div>
                  <template v-if="customerSalesSection === 'orders'">
                    <div v-if="detail.orders.length" class="profile-table-wrap">
                      <table class="profile-related-table">
                        <thead><tr><th>Số đơn hàng/hợp đồng</th><th>Account</th><th>Giá trị đơn hàng</th><th>Tình trạng</th><th>Tình trạng ghi doanh số</th><th>Người thực hiện</th><th>Đơn vị</th><th>Ngày đặt hàng</th><th>Ngày ghi sổ</th></tr></thead>
                        <tbody><tr v-for="row in detail.orders" :key="row.name" @click="openRelated('Sales Order', row)">
                          <td><a href="#" @click.prevent.stop="openRelated('Sales Order', row)">{{ row.name }}</a></td>
                          <td>
                            <span v-if="row.accounts && row.accounts.length" class="ccd-account-cell">
                              <button type="button" class="ccd-account-code" @click.stop="navigate('accounts'); openAccountDetail({ account_code: row.accounts[0].code })">{{ row.accounts[0].code }}</button>
                              <span v-if="row.accounts[0].a_end || row.accounts[0].z_end" class="ccd-account-endpoints">{{ row.accounts[0].a_end || '—' }} → {{ row.accounts[0].z_end || '—' }}</span>
                              <b v-if="row.accounts.length > 1" :data-tooltip="row.accounts.slice(1).map((acc) => acc.code).join(', ')">+{{ row.accounts.length - 1 }}</b>
                            </span>
                            <span v-else>—</span>
                          </td>
                          <td>{{ formatValue(row.grand_total, 'grand_total') }}</td><td><span class="ccd-status-ok">{{ row.status || '—' }}</span></td><td>Đã ghi</td><td>—</td><td>—</td><td>{{ formatValue(row.transaction_date, 'date') }}</td><td>{{ formatValue(row.modified, 'date') }}</td>
                        </tr></tbody>
                      </table>
                    </div>
                    <div v-else class="sales-empty"><span>Không có bản ghi nào</span><button v-if="detail.can_create_order" @click="createCustomerOrder">+ Thêm Đơn hàng</button></div>
                    <footer class="ccd-related-footer"><strong>Tổng số {{ detail.orders.length }}</strong><span class="ccd-related-page"><span>Số dòng/trang</span><b>10</b><span>1 - {{ detail.orders.length || 1 }}</span><button disabled>‹</button><button disabled>›</button></span></footer>
                  </template>
                  <template v-else-if="customerSalesSection === 'returns'">
                    <div v-if="detail.sales_returns.length" class="profile-table-wrap">
                      <table class="profile-related-table"><thead><tr><th>Số chứng từ</th><th>Trả cho hóa đơn</th><th>Giá trị trả lại</th><th>Tình trạng</th><th>Ngày ghi sổ</th></tr></thead><tbody><tr v-for="row in detail.sales_returns" :key="row.name" @click="openRelated('Sales Invoice', row)"><td><a href="#" @click.prevent.stop="openRelated('Sales Invoice', row)">{{ row.name }}</a></td><td>{{ row.return_against || '—' }}</td><td>{{ formatValue(Math.abs(row.grand_total || 0), 'grand_total') }}</td><td>{{ row.status || '—' }}</td><td>{{ formatValue(row.posting_date, 'date') }}</td></tr></tbody></table>
                    </div>
                    <div v-else class="sales-empty"><span>Không có bản ghi nào</span><button @click="createCustomerInvoice(true)">+ Thêm Trả lại hàng bán</button></div>
                  </template>
                  <template v-else-if="customerSalesSection === 'opportunities'">
                    <div v-if="detail.opportunities.length" class="profile-table-wrap">
                      <table class="profile-related-table"><thead><tr><th>Tên cơ hội</th><th>Số tiền</th><th>Giai đoạn</th><th>Tỷ lệ thành công</th><th>Doanh số kỳ vọng</th><th>Người thực hiện</th></tr></thead><tbody><tr v-for="row in detail.opportunities" :key="row.name" @click="openRelated('Opportunity', row)"><td><a href="#" @click.prevent.stop="openRelated('Opportunity', row)">{{ row.title || row.name }}</a></td><td>{{ formatValue(row.opportunity_amount, 'grand_total') }}</td><td>{{ row.sales_stage || row.status || '—' }}</td><td>—</td><td>{{ formatValue(row.opportunity_amount, 'grand_total') }}</td><td>—</td></tr></tbody></table>
                    </div>
                    <div v-else class="sales-empty"><span>Không có bản ghi nào</span><button @click="openOpportunityForm(detail.document.name, detail.document.customer_name)">+ Thêm Cơ hội</button></div>
                  </template>
                  <template v-else-if="customerSalesSection === 'quotations'">
                    <div v-if="detail.quotations.length" class="profile-table-wrap">
                      <table class="profile-related-table"><thead><tr><th>Số báo giá</th><th>Ngày báo giá</th><th>Hiệu lực đến ngày</th><th>Tổng tiền</th><th>Tình trạng</th><th>Mô tả</th></tr></thead><tbody><tr v-for="row in detail.quotations" :key="row.name" @click="openRelated('Quotation', row)"><td><a href="#" @click.prevent.stop="openRelated('Quotation', row)">{{ row.name }}</a></td><td>{{ formatValue(row.transaction_date, 'date') }}</td><td>—</td><td>{{ formatValue(row.grand_total, 'grand_total') }}</td><td>{{ row.status || '—' }}</td><td>—</td></tr></tbody></table>
                    </div>
                    <div v-else class="sales-empty"><span>Không có bản ghi nào</span><button @click="openCreateQuotation(detail.document.name, detail.document.customer_name)">+ Thêm Báo giá</button></div>
                  </template>
                  <template v-else-if="customerSalesSection === 'invoices'">
                    <div v-if="detail.invoices.length" class="profile-table-wrap">
                      <table class="profile-related-table"><thead><tr><th>Số hóa đơn</th><th>Diễn giải</th><th>Tổng tiền</th><th>Còn phải thu</th><th>Tình trạng</th><th>Người thực hiện</th><th>Ngày hóa đơn</th></tr></thead><tbody><tr v-for="row in detail.invoices" :key="row.name" @click="openRelated('Sales Invoice', row)"><td><a href="#" @click.prevent.stop="openRelated('Sales Invoice', row)">{{ row.name }}</a></td><td>{{ detail.document.customer_name }}</td><td>{{ formatValue(row.grand_total, 'grand_total') }}</td><td>{{ formatValue(row.outstanding_amount, 'grand_total') }}</td><td>{{ row.status || '—' }}</td><td>—</td><td>{{ formatValue(row.posting_date, 'date') }}</td></tr></tbody></table>
                    </div>
                    <div v-else class="sales-empty"><span>Không có bản ghi nào</span><button @click="createCustomerInvoice(false)">+ Thêm Hóa đơn</button></div>
                  </template>
                  <template v-else-if="customerSalesSection === 'items'">
                    <div v-if="detail.purchased_items.length" class="profile-table-wrap">
                      <table class="profile-related-table"><thead><tr><th>Mã hàng hóa</th><th>Tên hàng hóa</th><th>Loại hàng hóa</th><th>Số lượng</th><th>Doanh số</th></tr></thead><tbody><tr v-for="row in detail.purchased_items" :key="row.item_code"><td><a href="#" @click.prevent>{{ row.item_code }}</a></td><td><a href="#" @click.prevent>{{ row.item_name || row.item_code }}</a></td><td>{{ row.item_group || '—' }}</td><td>{{ formatValue(row.qty) }}</td><td>{{ formatValue(row.amount, 'grand_total') }}</td></tr></tbody></table>
                    </div>
                    <p v-else class="profile-empty">Không có bản ghi nào</p>
                  </template>
                  <template v-else>
                    <div class="sales-empty"><span>Không có bản ghi nào</span><button @click="createDocument('Customer')">+ Thêm Khách hàng</button></div>
                  </template>
                </section>
              </div>

              <section v-else-if="customerDetailTab === 'details'" class="profile-single-panel profile-details-panel">
                <div class="detail-form-toolbar">
                  <label><CRMIcon name="search" /><input v-model="detailFieldSearch" placeholder="Tìm kiếm trường"></label>
                  <span class="detail-edit-status" v-if="customerEditing">Đang chỉnh sửa</span>
                  <label class="detail-empty-toggle">
                    <input v-model="showEmptyDetailFields" type="checkbox">
                    <i></i><span>Hiển thị dữ liệu trống</span>
                  </label>
                </div>

                <form class="customer-detail-form" @submit.prevent="saveCustomerDetails">
                  <section class="detail-section">
                    <h2>Thông tin chung</h2>
                    <div class="detail-form-grid">
                      <label v-show="showDetailField('Mã khách hàng', detail.document.name)" class="detail-field">
                        <span>Mã khách hàng</span><input :value="detail.document.name" disabled>
                      </label>
                      <label v-show="showDetailField('Tên viết tắt', customerForm.customer.ten_viet_tat)" class="detail-field">
                        <span>Tên viết tắt</span><input v-model="customerForm.customer.ten_viet_tat" :disabled="!customerEditing">
                      </label>
                      <label v-show="showDetailField('Tên khách hàng', customerForm.customer.customer_name)" class="detail-field">
                        <span>Tên khách hàng</span><input v-model="customerForm.customer.customer_name" :disabled="!customerEditing" required>
                      </label>
                      <label v-show="showDetailField('Loại khách hàng', customerForm.customer.customer_type)" class="detail-field">
                        <span>Loại khách hàng</span>
                        <select v-model="customerForm.customer.customer_type" :disabled="!customerEditing">
                          <option value="Company">Công ty</option><option value="Individual">Cá nhân</option><option value="Partnership">Đối tác</option>
                        </select>
                      </label>
                      <label v-show="showDetailField('Mã số thuế', customerForm.customer.tax_id)" class="detail-field">
                        <span>Mã số thuế</span><input v-model="customerForm.customer.tax_id" :disabled="!customerEditing">
                      </label>
                      <label v-show="showDetailField('Điện thoại', customerForm.customer.misa_mobile)" class="detail-field">
                        <span>Điện thoại</span><input v-model="customerForm.customer.misa_mobile" :disabled="!customerEditing" :placeholder="customerDisplayPhone || ''">
                      </label>
                      <label v-show="showDetailField('Email', customerForm.customer.misa_email)" class="detail-field">
                        <span>Email</span><input v-model="customerForm.customer.misa_email" :disabled="!customerEditing" type="email" :placeholder="customerDisplayEmail || ''">
                      </label>
                      <label v-show="showDetailField('Nguồn gốc', customerForm.customer.nguon_goc)" class="detail-field">
                        <span>Nguồn gốc</span>
                        <select v-model="customerForm.customer.nguon_goc" :disabled="!customerEditing">
                          <option value="">- Không chọn -</option>
                          <option v-if="!hasCustomerOption(createOptions.sources, customerForm.customer.nguon_goc)" :value="customerForm.customer.nguon_goc">{{ customerForm.customer.nguon_goc }}</option>
                          <option v-for="opt in createOptions.sources" :key="opt.name" :value="opt.name">{{ opt.name }}</option>
                        </select>
                      </label>
                      <label v-show="showDetailField('Nhóm khách hàng', customerForm.customer.customer_group)" class="detail-field">
                        <span>Nhóm khách hàng</span>
                        <select v-model="customerForm.customer.customer_group" :disabled="!customerEditing">
                          <option value="">- Không chọn -</option>
                          <option v-if="!hasCustomerOption(createOptions.customer_groups, customerForm.customer.customer_group)" :value="customerForm.customer.customer_group">{{ customerForm.customer.customer_group }}</option>
                          <option v-for="opt in createOptions.customer_groups" :key="opt.name" :value="opt.name">{{ opt.name }}</option>
                        </select>
                      </label>
                      <label v-show="showDetailField('Khu vực', customerForm.customer.territory)" class="detail-field">
                        <span>Khu vực</span>
                        <select v-model="customerForm.customer.territory" :disabled="!customerEditing">
                          <option value="">- Không chọn -</option>
                          <option v-if="!hasCustomerOption(createOptions.territories, customerForm.customer.territory)" :value="customerForm.customer.territory">{{ customerForm.customer.territory }}</option>
                          <option v-for="opt in createOptions.territories" :key="opt.name" :value="opt.name">{{ opt.name }}</option>
                        </select>
                      </label>
                      <label v-show="showDetailField('Lĩnh vực', customerForm.customer.industry)" class="detail-field">
                        <span>Lĩnh vực</span>
                        <select v-model="customerForm.customer.industry" :disabled="!customerEditing">
                          <option value="">- Không chọn -</option>
                          <option v-if="!hasCustomerOption(createOptions.industries, customerForm.customer.industry)" :value="customerForm.customer.industry">{{ customerForm.customer.industry }}</option>
                          <option v-for="opt in createOptions.industries" :key="opt.name" :value="opt.name">{{ opt.name }}</option>
                        </select>
                      </label>
                      <label v-show="showDetailField('Loại hình', customerForm.customer.loai_hinh)" class="detail-field">
                        <span>Loại hình</span>
                        <select v-model="customerForm.customer.loai_hinh" :disabled="!customerEditing">
                          <option value="">- Không chọn -</option>
                          <option v-if="!hasCustomerOption(createOptions.legal_types, customerForm.customer.loai_hinh)" :value="customerForm.customer.loai_hinh">{{ customerForm.customer.loai_hinh }}</option>
                          <option v-for="opt in createOptions.legal_types" :key="opt.name" :value="opt.name">{{ opt.name }}</option>
                        </select>
                      </label>
                      <label v-show="showDetailField('Ngành nghề', customerForm.customer.nganh_nghe)" class="detail-field">
                        <span>Ngành nghề</span>
                        <select v-model="customerForm.customer.nganh_nghe" :disabled="!customerEditing">
                          <option value="">- Không chọn -</option>
                          <option v-if="!hasCustomerOption(createOptions.business_lines, customerForm.customer.nganh_nghe)" :value="customerForm.customer.nganh_nghe">{{ customerForm.customer.nganh_nghe }}</option>
                          <option v-for="opt in createOptions.business_lines" :key="opt.name" :value="opt.name">{{ opt.name }}</option>
                        </select>
                      </label>
                      <label v-show="showDetailField('Phân khúc', customerForm.customer.market_segment)" class="detail-field">
                        <span>Phân khúc</span>
                        <select v-model="customerForm.customer.market_segment" :disabled="!customerEditing">
                          <option value="">- Không chọn -</option>
                          <option v-if="!hasCustomerOption(createOptions.market_segments, customerForm.customer.market_segment)" :value="customerForm.customer.market_segment">{{ customerForm.customer.market_segment }}</option>
                          <option v-for="opt in createOptions.market_segments" :key="opt.name" :value="opt.name">{{ opt.name }}</option>
                        </select>
                      </label>
                      <label v-show="showDetailField('Website', customerForm.customer.website)" class="detail-field">
                        <span>Website</span><input v-model="customerForm.customer.website" :disabled="!customerEditing">
                      </label>
                      <label v-show="showDetailField('Bảng giá', customerForm.customer.default_price_list)" class="detail-field">
                        <span>Bảng giá</span>
                        <select v-model="customerForm.customer.default_price_list" :disabled="!customerEditing">
                          <option value="">- Không chọn -</option>
                          <option v-if="!hasCustomerOption(createOptions.price_lists, customerForm.customer.default_price_list)" :value="customerForm.customer.default_price_list">{{ customerForm.customer.default_price_list }}</option>
                          <option v-for="opt in createOptions.price_lists" :key="opt.name" :value="opt.name">{{ opt.name }}</option>
                        </select>
                      </label>
                      <label v-show="showDetailField('Người phụ trách', customerForm.customer.account_manager)" class="detail-field">
                        <span>Người phụ trách</span>
                        <select v-model="customerForm.customer.account_manager" :disabled="!customerEditing">
                          <option value="">- Không chọn -</option>
                          <option v-if="!hasCustomerOption(detail.activity_users, customerForm.customer.account_manager)" :value="customerForm.customer.account_manager">{{ customerForm.customer.account_manager }}</option>
                          <option v-for="user in detail.activity_users" :key="user.name" :value="user.name">{{ user.full_name || user.name }}</option>
                        </select>
                      </label>
                    </div>
                  </section>

                  <section class="detail-section">
                    <h2>Thông tin hóa đơn</h2>
                    <div class="detail-form-grid">
                      <label v-show="showDetailField('Tên địa chỉ', customerForm.address.address_title)" class="detail-field">
                        <span>Tên địa chỉ</span><input v-model="customerForm.address.address_title" :disabled="!customerEditing">
                      </label>
                      <label v-show="showDetailField('Loại địa chỉ', customerForm.address.address_type)" class="detail-field">
                        <span>Loại địa chỉ</span>
                        <select v-model="customerForm.address.address_type" :disabled="!customerEditing">
                          <option value="Billing">Hóa đơn</option><option value="Shipping">Giao hàng</option><option value="Office">Văn phòng</option><option value="Personal">Cá nhân</option>
                        </select>
                      </label>
                      <label v-show="showDetailField('Số nhà, đường phố', customerForm.address.address_line1)" class="detail-field detail-field--addr-line">
                        <span>Số nhà, đường phố</span><input v-model="customerForm.address.address_line1" :disabled="!customerEditing" placeholder="Số nhà, tên đường...">
                      </label>
                      <label v-show="customerEditing || showDetailField('Tỉnh/Thành phố', customerForm.address.state)" class="detail-field">
                        <span>Tỉnh/Thành phố</span>
                        <template v-if="customerEditing">
                          <select v-model="editProvinceCode">
                            <option value="">- Chọn tỉnh/thành phố -</option>
                            <option v-for="p in editVnProvinces" :key="p.code" :value="p.code">{{ p.name }}</option>
                          </select>
                        </template>
                        <template v-else><span class="detail-value">{{ customerForm.address.state || '—' }}</span></template>
                      </label>
                      <label v-show="customerEditing || showDetailField('Phường/Xã', customerForm.address.county)" class="detail-field">
                        <span>Phường/Xã</span>
                        <template v-if="customerEditing">
                          <select v-model="customerForm.address.county" :disabled="!editProvinceCode">
                            <option value="">{{ editVnLoadingWards ? 'Đang tải...' : (editProvinceCode ? '- Chọn phường/xã -' : '- Chọn tỉnh/TP trước -') }}</option>
                            <option v-for="w in editVnWards" :key="w.code" :value="w.name">{{ w.name }}</option>
                          </select>
                        </template>
                        <template v-else><span class="detail-value">{{ customerForm.address.county || '—' }}</span></template>
                      </label>
                      <label v-show="showDetailField('Quốc gia', customerForm.address.country)" class="detail-field">
                        <span>Quốc gia</span><input v-model="customerForm.address.country" :disabled="!customerEditing">
                      </label>
                      <label v-show="showDetailField('Mã vùng', customerForm.address.pincode)" class="detail-field">
                        <span>Mã vùng</span><input v-model="customerForm.address.pincode" :disabled="!customerEditing">
                      </label>
                      <label v-show="showDetailField('Điện thoại hóa đơn', customerForm.address.phone)" class="detail-field">
                        <span>Điện thoại hóa đơn</span><input v-model="customerForm.address.phone" :disabled="!customerEditing">
                      </label>
                    </div>
                    <div v-if="customerEditing" class="detail-address-flags">
                      <label><input v-model.number="customerForm.address.is_primary_address" :true-value="1" :false-value="0" type="checkbox"> Địa chỉ chính</label>
                      <label><input v-model.number="customerForm.address.is_shipping_address" :true-value="1" :false-value="0" type="checkbox"> Đồng thời là địa chỉ giao hàng</label>
                    </div>
                  </section>

                  <section class="detail-section">
                    <h2>Thông tin giao hàng</h2>
                    <div class="detail-form-grid">
                      <label v-show="showDetailField('Quốc gia giao hàng', customerForm.address.country)" class="detail-field">
                        <span>Quốc gia (Giao hàng)</span><span class="detail-value">{{ customerForm.address.country || '— Không chọn —' }}</span>
                      </label>
                      <label v-show="showDetailField('Tỉnh/Thành phố giao hàng', customerForm.address.state)" class="detail-field">
                        <span>Tỉnh/Thành phố (Giao hàng)</span><span class="detail-value">{{ customerForm.address.state || '— Không chọn —' }}</span>
                      </label>
                      <label v-show="showDetailField('Quận/Huyện giao hàng', customerForm.address.city)" class="detail-field">
                        <span>Quận/Huyện (Giao hàng)</span><span class="detail-value">{{ customerForm.address.city || '— Không chọn —' }}</span>
                      </label>
                      <label v-show="showDetailField('Phường/Xã giao hàng', customerForm.address.county)" class="detail-field">
                        <span>Phường/Xã (Giao hàng)</span><span class="detail-value">{{ customerForm.address.county || '— Không chọn —' }}</span>
                      </label>
                      <label v-show="showDetailField('Số nhà giao hàng', customerForm.address.address_line1)" class="detail-field">
                        <span>Số nhà, Đường phố (Giao hàng)</span><span class="detail-value">{{ customerForm.address.address_line1 || '—' }}</span>
                      </label>
                      <label v-show="showDetailField('Mã vùng giao hàng', customerForm.address.pincode)" class="detail-field">
                        <span>Mã vùng (Giao hàng)</span><span class="detail-value">{{ customerForm.address.pincode || '—' }}</span>
                      </label>
                    </div>
                  </section>

                  <section class="detail-section">
                    <h2>Thông tin bổ sung</h2>
                    <div class="detail-form-grid">
                      <label v-show="showDetailField('Tài khoản ngân hàng', customerForm.customer.tai_khoan_ngan_hang)" class="detail-field">
                        <span>Tài khoản ngân hàng</span><input v-model="customerForm.customer.tai_khoan_ngan_hang" :disabled="!customerEditing">
                      </label>
                      <label v-show="showDetailField('Mở tại ngân hàng', customerForm.customer.mo_tai_ngan_hang)" class="detail-field">
                        <span>Mở tại ngân hàng</span><input v-model="customerForm.customer.mo_tai_ngan_hang" :disabled="!customerEditing">
                      </label>
                      <label v-show="showDetailField('Ngày thành lập/Ngày sinh', customerForm.customer.ngay_thanh_lap)" class="detail-field">
                        <span>Ngày thành lập/Ngày sinh</span><input v-model="customerForm.customer.ngay_thanh_lap" :disabled="!customerEditing" type="date">
                      </label>
                      <label v-show="showDetailField('Là khách hàng từ', customerForm.customer.la_kh_tu)" class="detail-field">
                        <span>Là khách hàng từ</span><input v-model="customerForm.customer.la_kh_tu" :disabled="!customerEditing" type="date">
                      </label>
                      <label v-show="showDetailField('Doanh thu', customerForm.customer.quy_mo_doanh_thu)" class="detail-field">
                        <span>Doanh thu</span><input v-model="customerForm.customer.quy_mo_doanh_thu" :disabled="!customerEditing">
                      </label>
                      <label v-show="showDetailField('Quy mô nhân sự', customerForm.customer.quy_mo_nhan_su)" class="detail-field">
                        <span>Quy mô nhân sự</span><input v-model="customerForm.customer.quy_mo_nhan_su" :disabled="!customerEditing">
                      </label>
                      <label v-show="showDetailField('Loại hạn mức nợ', customerForm.customer.loai_han_muc_no)" class="detail-field">
                        <span>Loại hạn mức nợ</span><input v-model="customerForm.customer.loai_han_muc_no" :disabled="!customerEditing">
                      </label>
                      <label v-show="showDetailField('Công nợ', detail.summary.outstanding)" class="detail-field">
                        <span>Công nợ</span><span class="detail-value">{{ formatValue(detail.summary.outstanding, 'grand_total') }}</span>
                      </label>
                      <label v-show="showDetailField('Loại điều khoản TT', customerForm.customer.so_ngay_duoc_no)" class="detail-field">
                        <span>Loại điều khoản TT</span><input v-model.number="customerForm.customer.so_ngay_duoc_no" :disabled="!customerEditing" type="number" min="0">
                      </label>
                    </div>
                  </section>

                  <section class="detail-section">
                    <h2>Thống kê mua hàng</h2>
                    <div class="detail-form-grid">
                      <label class="detail-field">
                        <span>Ngày mua hàng đầu tiên</span><span class="detail-value">{{ detail.orders.length ? formatValue(detail.orders[detail.orders.length - 1].transaction_date, 'date') : '—' }}</span>
                      </label>
                      <label class="detail-field">
                        <span>Số ngày chưa mua hàng</span><span class="detail-value">—</span>
                      </label>
                      <label class="detail-field">
                        <span>Ngày mua hàng gần nhất</span><span class="detail-value">{{ detail.orders.length ? formatValue(detail.orders[0].transaction_date, 'date') : '—' }}</span>
                      </label>
                      <label class="detail-field">
                        <span>Doanh số đơn hàng</span><span class="detail-value">{{ formatValue(detail.summary.order_value, 'grand_total') }}</span>
                      </label>
                      <label class="detail-field">
                        <span>Số lượng đơn hàng</span><span class="detail-value">{{ detail.summary.order_count || 0 }}</span>
                      </label>
                      <label class="detail-field">
                        <span>Số ngày TB giữa các lần mua</span><span class="detail-value">—</span>
                      </label>
                    </div>
                  </section>

                  <section class="detail-section">
                    <h2>Thông tin mô tả</h2>
                    <div class="detail-form-grid">
                      <label v-show="showDetailField('Mô tả', customerForm.customer.customer_details)" class="detail-field wide">
                        <span>Mô tả</span><textarea v-model="customerForm.customer.customer_details" :disabled="!customerEditing"></textarea>
                      </label>
                    </div>
                  </section>

                  <section class="detail-section">
                    <h2>Thông tin hệ thống</h2>
                    <div class="detail-form-grid">
                      <label class="detail-field"><span>Chủ sở hữu</span><span class="detail-value">{{ detail.document.owner || '—' }}</span></label>
                      <label class="detail-field"><span>Đơn vị</span><span class="detail-value">—</span></label>
                      <label class="detail-field"><span>Người tạo</span><span class="detail-value">{{ detail.document.owner || '—' }}</span></label>
                      <label class="detail-field"><span>Ngày tạo</span><span class="detail-value">{{ formatValue(detail.document.creation, 'creation') }}</span></label>
                      <label class="detail-field"><span>Người sửa</span><span class="detail-value">{{ detail.document.modified_by || '—' }}</span></label>
                      <label class="detail-field"><span>Ngày sửa</span><span class="detail-value">{{ formatValue(detail.document.modified, 'creation') }}</span></label>
                      <label class="detail-field"><span>Dùng chung</span><span class="detail-value">{{ customerForm.customer.dung_chung ? 'Có' : '—' }}</span></label>
                      <label class="detail-field"><span>Điểm khách hàng</span><span class="detail-value">0</span></label>
                      <label class="detail-field"><span>Là KH cá nhân</span><span class="detail-value">{{ customerForm.customer.la_kh_ca_nhan ? 'Có' : '—' }}</span></label>
                      <label class="detail-field"><span>Ngừng theo dõi</span><span class="detail-value">—</span></label>
                      <label class="detail-field"><span>Là đối tác/cộng tác viên</span><span class="detail-value">{{ customerForm.customer.la_doi_tac_ctv ? 'Có' : '—' }}</span></label>
                      <label class="detail-field"><span>Đối tác/CTV giới thiệu</span><span class="detail-value">{{ customerForm.customer.doi_tac_gioi_thieu || '— Không chọn —' }}</span></label>
                    </div>
                  </section>

                  <section class="detail-section">
                    <h2>Thông tin Cổng thông tin</h2>
                    <div class="detail-form-grid">
                      <label class="detail-field"><span>Có quyền truy cập CTT</span><span class="detail-value">—</span></label>
                      <label class="detail-field"><span>Tài khoản truy cập CTT</span><span class="detail-value">—</span></label>
                    </div>
                  </section>

                  <footer v-if="customerEditing" class="detail-form-actions">
                    <button class="crm-button" type="button" :disabled="customerSaving" @click="cancelCustomerEdit">Hủy</button>
                    <button class="crm-button primary" type="submit" :disabled="customerSaving">{{ customerSaving ? 'Đang lưu...' : 'Lưu thay đổi' }}</button>
                  </footer>
                </form>
              </section>

              <section v-else-if="customerDetailTab === 'contacts'" class="profile-contacts-panel">
                <div class="profile-contacts-card">
                  <header class="contacts-table-heading">
                    <div><h2>Liên hệ</h2><button data-tooltip="Làm mới" @click="loadCustomerDetail(detail.document.name)"><CRMIcon name="refresh" /></button></div>
                    <div>
                      <button v-if="detail.can_create_contact" @click="openContactDialog('full')">＋ Thêm</button>
                      <button v-if="detail.can_create_contact" @click="openContactDialog('quick')">＋ Thêm nhanh</button>
                      <button v-if="detail.can_write_contact" @click="openContactPicker">☑ Chọn</button>
                    </div>
                  </header>
                  <div class="contacts-table-scroll">
                    <table class="contacts-table">
                      <thead><tr>
                        <th>Loại liên hệ</th><th>Email cá nhân</th><th>Họ và tên</th><th>Xưng hô</th>
                        <th>Email cơ quan</th><th>Chức danh</th><th>ĐT di động</th><th>ĐT cơ quan</th><th>Tổ chức</th>
                      </tr></thead>
                      <tbody>
                        <tr v-for="contact in visibleCustomerContacts" :key="contact.name">
                          <td><span class="contact-type-icons"><i data-tooltip="Cá nhân">P</i><i v-if="contact.email_id" data-tooltip="Email">E</i><i v-if="contact.mobile_no || contact.phone" data-tooltip="Điện thoại">T</i></span></td>
                          <td>{{ contact.email_id || '—' }}</td>
                          <td><button v-if="detail.can_write_contact" class="contact-name-link" @click="openContactDialog('full', contact)">{{ contact.full_name || contact.name }}</button><span v-else>{{ contact.full_name || contact.name }}</span></td>
                          <td>{{ contact.salutation || '—' }}</td>
                          <td>—</td>
                          <td>{{ contact.designation || '—' }}</td>
                          <td><a v-if="contact.mobile_no" :href="'tel:' + contact.mobile_no">{{ contact.mobile_no }}</a><span v-else>—</span></td>
                          <td><a v-if="contact.phone" :href="'tel:' + contact.phone">{{ contact.phone }}</a><span v-else>—</span></td>
                          <td>{{ contact.company_name || detail.document.customer_name }}</td>
                        </tr>
                      </tbody>
                    </table>
                    <p v-if="!detail.contacts.length" class="profile-empty contacts-empty">Không có bản ghi nào</p>
                  </div>
                  <footer class="contacts-pagination">
                    <strong>Tổng số {{ detail.contacts.length.toLocaleString('vi-VN') }}</strong>
                    <div><label>Số dòng/trang</label>
                      <select v-model.number="contactPageLength"><option :value="20">20</option><option :value="50">50</option><option :value="100">100</option></select>
                      <span>{{ contactPageStart }} - {{ contactPageEnd }}</span>
                      <button :disabled="contactPage <= 1" @click="changeContactPage(1)">|‹</button>
                      <button :disabled="contactPage <= 1" @click="changeContactPage(contactPage - 1)">‹</button>
                      <button :disabled="contactPage >= contactPageCount" @click="changeContactPage(contactPage + 1)">›</button>
                      <button :disabled="contactPage >= contactPageCount" @click="changeContactPage(contactPageCount)">›|</button>
                    </div>
                  </footer>
                </div>
              </section>

              <section v-else-if="customerDetailTab === 'activity'" class="profile-activity-panel">
                <div class="profile-activity-card">
                  <header class="activity-table-heading">
                    <div><h2>Hoạt động</h2><button data-tooltip="Làm mới" @click="loadCustomerDetail(detail.document.name)"><CRMIcon name="refresh" /></button></div>
                    <div v-if="detail.can_create_activity">
                      <button @click="openActivityDialog('task')"><CRMIcon name="task" /> Thêm Nhiệm vụ</button>
                      <button @click="openActivityDialog('meeting')"><CRMIcon name="calendar" /> Thêm Lịch hẹn</button>
                      <button @click="openActivityDialog('call')"><CRMIcon name="phone" /> Thêm Cuộc gọi</button>
                    </div>
                  </header>
                  <div class="activity-table-scroll">
                    <table class="activity-table">
                      <thead><tr><th>Tên hoạt động</th><th>Loại hoạt động</th><th>Hạn hoàn thành</th><th>Trạng thái</th><th>Ngày kết thúc</th><th>Người thực hiện</th></tr></thead>
                      <tbody><tr v-for="activity in visibleCustomerActivities" :key="activity.activity_type + '-' + activity.name">
                        <td><button @click="openActivityRecord(activity.name, activity.activity_type === 'task' ? 'ToDo' : 'Event', detail.document.name, detail.document.customer_name)">{{ activity.subject || activity.name }}</button></td>
                        <td>{{ activityTypeLabel(activity.activity_type) }}</td>
                        <td>{{ formatValue(activity.due_date, 'date') }}</td>
                        <td><span class="activity-status" :class="'status-' + String(activity.status || '').toLowerCase()">{{ activityStatusLabel(activity.status) }}</span></td>
                        <td>{{ formatValue(activity.ends_on, 'date') }}</td>
                        <td>{{ activity.performed_by_name || activity.performed_by || '—' }}</td>
                      </tr></tbody>
                    </table>
                    <p v-if="!detail.activities.length" class="profile-empty activity-empty-row">Không có bản ghi nào</p>
                  </div>
                  <footer class="activity-pagination">
                    <strong>Tổng số {{ detail.activities.length.toLocaleString('vi-VN') }}</strong>
                    <div><label>Số dòng/trang</label>
                      <select v-model.number="activityPageLength"><option :value="10">10</option><option :value="20">20</option><option :value="50">50</option></select>
                      <span>{{ activityPageStart }} - {{ activityPageEnd }}</span>
                      <button :disabled="activityPage <= 1" @click="changeActivityPage(1)">|‹</button>
                      <button :disabled="activityPage <= 1" @click="changeActivityPage(activityPage - 1)">‹</button>
                      <button :disabled="activityPage >= activityPageCount" @click="changeActivityPage(activityPage + 1)">›</button>
                      <button :disabled="activityPage >= activityPageCount" @click="changeActivityPage(activityPageCount)">›|</button>
                    </div>
                  </footer>
                </div>
              </section>

              <div v-else-if="customerDetailTab === 'support'" class="profile-tab-layout profile-group-layout">
                <nav class="profile-subnav">
                  <button :class="{ active: customerSupportSection === 'consult_cards' }" @click="customerSupportSection = 'consult_cards'"><CRMIcon name="quotation" />Thẻ tư vấn</button>
                  <button :class="{ active: customerSupportSection === 'care_cards' }" @click="customerSupportSection = 'care_cards'"><CRMIcon name="care" />Thẻ chăm sóc</button>
                  <button :class="{ active: customerSupportSection === 'warranty' }" @click="customerSupportSection = 'warranty'"><CRMIcon name="settings" />Phiếu bảo hành</button>
                </nav>
                <section class="profile-records">
                  <div class="profile-records-heading"><div><h2>{{ customerSupportSectionLabel(customerSupportSection) }}</h2><button data-tooltip="Làm mới" @click="loadCustomerDetail(detail.document.name)"><CRMIcon name="refresh" /></button></div><button @click="customerSupportSection === 'care_cards' ? navigate('care') : notifyCustomerUnavailable(customerSupportSectionLabel(customerSupportSection))">+ Thêm</button></div>
                  <div class="sales-empty"><span>Không có bản ghi nào</span><button @click="customerSupportSection === 'care_cards' ? navigate('care') : notifyCustomerUnavailable(customerSupportSectionLabel(customerSupportSection))">+ Thêm</button></div>
                </section>
              </div>

              <div v-else-if="customerDetailTab === 'marketing'" class="profile-tab-layout profile-group-layout">
                <nav class="profile-subnav">
                  <button :class="{ active: customerMarketingSection === 'campaigns' }" @click="customerMarketingSection = 'campaigns'"><CRMIcon name="activity" />Chiến dịch</button>
                  <button :class="{ active: customerMarketingSection === 'promotions' }" @click="customerMarketingSection = 'promotions'"><CRMIcon name="tag" />Khuyến mại</button>
                  <button :class="{ active: customerMarketingSection === 'loyalty' }" @click="customerMarketingSection = 'loyalty'"><CRMIcon name="dollar" />Tích lũy</button>
                  <button :class="{ active: customerMarketingSection === 'rewards' }" @click="customerMarketingSection = 'rewards'"><CRMIcon name="thumbsup" />Trả thưởng</button>
                  <button :class="{ active: customerMarketingSection === 'email' }" @click="customerMarketingSection = 'email'"><CRMIcon name="email" />Email</button>
                  <button :class="{ active: customerMarketingSection === 'sms' }" @click="customerMarketingSection = 'sms'"><CRMIcon name="message" />SMS</button>
                  <button :class="{ active: customerMarketingSection === 'routes' }" @click="customerMarketingSection = 'routes'"><CRMIcon name="send" />Lộ trình đi tuyến</button>
                  <button :class="{ active: customerMarketingSection === 'aimarketing' }" @click="customerMarketingSection = 'aimarketing'"><CRMIcon name="sparkles" />aiMarketing</button>
                </nav>
                <section class="profile-records">
                  <div class="profile-records-heading"><div><h2>{{ customerMarketingSectionLabel(customerMarketingSection) }}</h2><button data-tooltip="Làm mới" @click="loadCustomerDetail(detail.document.name)"><CRMIcon name="refresh" /></button></div><button v-if="customerMarketingSection === 'campaigns'" @click="frappe.new_doc('Campaign')">+ Thêm Chiến dịch</button></div>
                  <div class="sales-empty"><span>Không có bản ghi nào</span><button v-if="customerMarketingSection === 'campaigns'" @click="frappe.new_doc('Campaign')">+ Thêm</button><button v-else @click="notifyCustomerUnavailable(customerMarketingSectionLabel(customerMarketingSection))">+ Thêm</button></div>
                </section>
              </div>

              <div v-else-if="customerDetailTab === 'notes'" class="profile-tab-layout profile-group-layout">
                <nav class="profile-subnav">
                  <button :class="{ active: customerNoteSection === 'notes' }" @click="customerNoteSection = 'notes'"><CRMIcon name="contact" />Ghi chú</button>
                  <button :class="{ active: customerNoteSection === 'attachments' }" @click="customerNoteSection = 'attachments'"><CRMIcon name="package" />Tài liệu đính kèm <b v-if="detail.files.length">{{ detail.files.length }}</b></button>
                </nav>
                <section v-if="customerNoteSection === 'notes'" class="profile-records">
                  <div class="profile-records-heading"><div><h2>Ghi chú</h2></div><button data-tooltip="Làm mới" @click="loadCustomerDetail(detail.document.name)"><CRMIcon name="refresh" /></button></div>
                  <div class="customer-note-box">
                    <textarea v-model="customerInlineNote" rows="3" placeholder="Nhập nội dung ghi chú..." @keydown.ctrl.enter.prevent="saveCustomerNoteFromDetail('note')"></textarea>
                    <div class="customer-note-actions">
                      <span>Nhấn Ctrl + Enter để lưu nhanh</span>
                      <button class="crm-button primary" type="button" :disabled="!customerInlineNote.trim()" @click="saveCustomerNoteFromDetail('note')"><CRMIcon name="send" /> Lưu ghi chú</button>
                    </div>
                  </div>
                  <div v-if="customerCommentEntries.length" class="profile-timeline-list">
                    <article v-for="entry in customerCommentEntries" :key="entry.name">
                      <strong>{{ entry.comment_email || entry.owner || 'CRM' }}</strong>
                      <span>{{ formatValue(entry.creation, 'creation') }}</span>
                      <p>{{ stripHtml(entry.content || entry.subject || '') }}</p>
                    </article>
                  </div>
                  <p v-else class="profile-empty">Không có ghi chú nào.</p>
                </section>
                <section v-else class="profile-records">
                  <div class="profile-records-heading"><div><h2>Tài liệu đính kèm</h2><button data-tooltip="Làm mới" @click="loadCustomerDetail(detail.document.name)"><CRMIcon name="refresh" /></button></div><div><button @click="addCustomerAttachmentLink">Thêm liên kết</button><button :disabled="customerAttachUploading" @click="$refs.customerFileInput.click()">{{ customerAttachUploading ? 'Đang tải...' : 'Thêm tệp' }}</button><input ref="customerFileInput" type="file" style="display:none" @change="uploadCustomerFile"></div></div>
                  <div class="profile-table-wrap">
                    <table class="profile-related-table"><thead><tr><th>Tên tài liệu</th><th>Người đính kèm</th><th>Ngày đính kèm</th><th>Dung lượng</th><th></th></tr></thead><tbody><tr v-for="file in detail.files" :key="file.name"><td><a :href="file.file_url" target="_blank" rel="noopener">{{ file.file_name }}</a></td><td>{{ file.owner || '—' }}</td><td>{{ formatValue(file.creation, 'creation') }}</td><td>{{ file.file_size ? formatFileSize(file.file_size) : '—' }}</td><td><button class="profile-row-action" @click="deleteCustomerAttachment(file.name)">Xóa</button></td></tr></tbody></table>
                    <p v-if="!detail.files.length" class="profile-empty contacts-empty">Không có bản ghi nào</p>
                  </div>
                </section>
              </div>

              <section v-else-if="customerDetailTab === 'conversation'" class="profile-single-panel profile-conversation-panel">
                <div class="customer-conversation-shell">
                  <header class="customer-conversation-heading">
                    <div><h2>Trao đổi</h2><p>Theo dõi và cập nhật nội dung làm việc với khách hàng.</p></div>
                    <span>{{ customerConversationEntries.length }} bình luận</span>
                  </header>
                  <div v-if="customerConversationEntries.length" class="customer-comment-feed">
                    <article v-for="entry in customerConversationEntries" :key="entry.activity_type + '-' + entry.name" class="customer-comment">
                      <span class="customer-comment-avatar" aria-hidden="true">{{ (entry.sender || entry.comment_email || entry.owner || 'CRM').slice(0, 1).toUpperCase() }}</span>
                      <div class="customer-comment-content">
                        <div class="customer-comment-meta"><strong>{{ entry.sender || entry.comment_email || entry.owner || 'CRM' }}</strong><time>{{ formatValue(entry.creation, 'creation') }}</time></div>
                        <div class="customer-comment-bubble"><p>{{ stripHtml(entry.content || entry.subject || '') }}</p></div>
                      </div>
                    </article>
                  </div>
                  <div v-else class="customer-conversation-empty"><CRMIcon name="message" /><strong>Chưa có nội dung trao đổi</strong><span>Hãy bắt đầu bằng bình luận đầu tiên về khách hàng này.</span></div>
                  <div class="customer-comment-composer">
                    <span class="customer-comment-avatar current" aria-hidden="true">{{ (boot?.full_name || boot?.user || 'CRM').slice(0, 1).toUpperCase() }}</span>
                    <div class="customer-comment-editor">
                      <textarea v-model="customerConversationText" rows="3" aria-label="Nội dung trao đổi" placeholder="Viết bình luận..." @keydown.ctrl.enter.prevent="saveCustomerNoteFromDetail('conversation')"></textarea>
                      <div class="customer-comment-actions">
                        <button type="button" data-tooltip="Mở tài liệu đính kèm" @click="customerDetailTab = 'notes'; customerNoteSection = 'attachments'"><CRMIcon name="package" /> Đính kèm</button>
                        <span>Ctrl + Enter để gửi</span>
                        <button type="button" class="crm-button primary" :disabled="!customerConversationText.trim()" @click="saveCustomerNoteFromDetail('conversation')"><CRMIcon name="send" /> Gửi</button>
                      </div>
                    </div>
                  </div>
                </div>
              </section>

              <section v-else class="profile-single-panel">
                <h2>Không có dữ liệu</h2>
                <p class="profile-empty">Không có bản ghi nào.</p>
              </section>
            </section>
          </section>
          <p v-else class="crm-empty">Đang tải hồ sơ khách hàng...</p>

          <div v-if="contactDialogOpen" class="crm-modal-backdrop" @click.self="closeContactDialog">
            <form class="crm-modal contact-modal" @submit.prevent="saveCustomerContact">
              <header><div><h2>{{ contactForm.name ? 'Sửa liên hệ' : contactDialogMode === 'quick' ? 'Thêm nhanh liên hệ' : 'Thêm liên hệ' }}</h2><p>Liên kết trực tiếp với {{ detail.document.customer_name }}</p></div><button type="button" @click="closeContactDialog">×</button></header>
              <div class="contact-modal-grid">
                <label><span>Tên <b>*</b></span><input v-model="contactForm.first_name" required autofocus></label>
                <label><span>Họ</span><input v-model="contactForm.last_name"></label>
                <label><span>Email cá nhân</span><input v-model="contactForm.email_id" type="email"></label>
                <label><span>ĐT di động</span><input v-model="contactForm.mobile_no"></label>
                <label><span>ĐT cơ quan</span><input v-model="contactForm.phone"></label>
                <label><span>Chức danh</span><input v-model="contactForm.designation"></label>
                <template v-if="contactDialogMode === 'full'">
                  <label><span>Tên đệm</span><input v-model="contactForm.middle_name"></label>
                  <label><span>Xưng hô</span><input v-model="contactForm.salutation"></label>
                  <label><span>Phòng ban</span><input v-model="contactForm.department"></label>
                  <label><span>Tổ chức</span><input v-model="contactForm.company_name"></label>
                  <label><span>Trạng thái</span><select v-model="contactForm.status"><option value="Open">Đang hoạt động</option><option value="Replied">Đã phản hồi</option><option value="Passive">Không hoạt động</option></select></label>
                  <label><span>Giới tính</span><input v-model="contactForm.gender"></label>
                </template>
                <label class="contact-primary-check">
                  <input v-model.number="contactForm.is_primary_contact" :true-value="1" :false-value="0" type="checkbox">
                  <span class="contact-primary-box" aria-hidden="true"></span>
                  <span class="contact-primary-copy"><strong>Đặt làm liên hệ chính</strong><small>Liên hệ này sẽ được ưu tiên khi giao dịch với khách hàng.</small></span>
                </label>
              </div>
              <footer><button class="crm-button" type="button" :disabled="contactSaving" @click="closeContactDialog">Hủy</button><button class="crm-button primary" type="submit" :disabled="contactSaving || !contactForm.first_name?.trim()">{{ contactSaving ? 'Đang lưu...' : 'Lưu liên hệ' }}</button></footer>
            </form>
          </div>

          <div v-if="contactPickerOpen" class="crm-modal-backdrop" @click.self="contactPickerOpen = false">
            <section class="crm-modal contact-picker-modal">
              <header><div><h2>Chọn liên hệ</h2><p>Chọn Contact đã tồn tại để liên kết với {{ detail.document.customer_name }}</p></div><button type="button" @click="contactPickerOpen = false">×</button></header>
              <div class="contact-picker-search"><CRMIcon name="search" /><input v-model="contactPickerSearch" placeholder="Tìm theo tên, email hoặc điện thoại" @keyup.enter="searchCustomerContacts"><button @click="searchCustomerContacts">Tìm kiếm</button></div>
              <div class="contact-picker-list">
                <button v-for="contact in contactPickerRows" :key="contact.name" :disabled="contactSaving" @click="linkCustomerContact(contact)">
                  <span class="contact-avatar">{{ (contact.full_name || contact.name).slice(0, 1) }}</span>
                  <span><strong>{{ contact.full_name || contact.name }}</strong><small>{{ contact.email_id || contact.mobile_no || contact.phone || 'Chưa có thông tin liên lạc' }}</small></span>
                  <b>Chọn</b>
                </button>
                <p v-if="contactPickerLoading" class="crm-empty">Đang tìm...</p>
                <p v-else-if="!contactPickerRows.length" class="crm-empty">Không có liên hệ chưa liên kết phù hợp.</p>
              </div>
            </section>
          </div>

          <div v-if="activityDialogOpen" class="crm-modal-backdrop" @click.self="activityDialogOpen = false">
            <form class="crm-modal activity-modal" @submit.prevent="saveCustomerActivity">
              <header><div><h2>{{ activityForm.name ? 'Sửa ' : 'Thêm ' }}{{ activityTypeLabel(activityForm.activity_type).toLowerCase() }}</h2><p>Hoạt động của {{ detail.document.customer_name }}</p></div><button type="button" @click="activityDialogOpen = false">×</button></header>
              <div class="activity-modal-grid">
                <label class="wide"><span>Tên hoạt động <b>*</b></span><input v-model="activityForm.subject" required autofocus></label>
                <template v-if="activityForm.activity_type === 'task'">
                  <label><span>Hạn hoàn thành</span><input v-model="activityForm.due_date" type="date"></label>
                  <label><span>Người thực hiện</span><select v-model="activityForm.allocated_to"><option v-for="user in detail.activity_users" :key="user.name" :value="user.name">{{ user.full_name || user.name }}</option></select></label>
                  <label><span>Trạng thái</span><select v-model="activityForm.status"><option value="Open">Đang thực hiện</option><option value="Closed">Đã hoàn thành</option><option value="Cancelled">Đã hủy</option></select></label>
                  <label><span>Ưu tiên</span><select v-model="activityForm.priority"><option value="High">Cao</option><option value="Medium">Trung bình</option><option value="Low">Thấp</option></select></label>
                </template>
                <template v-else>
                  <label><span>Bắt đầu</span><input v-model="activityForm.starts_on" type="datetime-local" required></label>
                  <label><span>Kết thúc</span><input v-model="activityForm.ends_on" type="datetime-local"></label>
                  <label><span>Trạng thái</span><select v-model="activityForm.status"><option value="Open">Đang thực hiện</option><option value="Completed">Đã hoàn thành</option><option value="Closed">Đã đóng</option><option value="Cancelled">Đã hủy</option></select></label>
                  <label><span>Người thực hiện</span><select v-model="activityForm.allocated_to"><option v-for="user in detail.activity_users" :key="user.name" :value="user.name">{{ user.full_name || user.name }}</option></select></label>
                </template>
                <label class="wide"><span>Mô tả</span><textarea v-model="activityForm.description"></textarea></label>
              </div>
              <footer><button class="crm-button" type="button" :disabled="activitySaving" @click="activityDialogOpen = false">Hủy</button><button class="crm-button primary" type="submit" :disabled="activitySaving || !activityForm.subject?.trim()">{{ activitySaving ? 'Đang lưu...' : 'Lưu hoạt động' }}</button></footer>
            </form>
          </div>

          <teleport to="body"><div v-if="customerSummaryDialogOpen" class="column-dialog-backdrop customer-summary-dialog-backdrop" @click.self="cancelCustomerSummaryDialog">
            <section class="customer-summary-dialog" role="dialog" aria-modal="true" aria-labelledby="customer-summary-dialog-title">
              <header>
                <div>
                  <h2 id="customer-summary-dialog-title">Tùy chỉnh tóm tắt</h2>
                  <p>Chọn trường thông tin để hiển thị trong phần thông tin tóm tắt.</p>
                </div>
                <button class="customer-summary-close" data-tooltip="Đóng" aria-label="Đóng" @click="cancelCustomerSummaryDialog">×</button>
              </header>
              <div class="customer-summary-picker">
                <section>
                  <h3>Chưa chọn <span>{{ availableCustomerSummaryFields.length }}</span></h3>
                  <label class="customer-summary-search">
                    <CRMIcon name="search" />
                    <input v-model="customerSummarySearch" placeholder="Tìm kiếm trường" autofocus>
                  </label>
                  <div class="customer-summary-field-list">
                    <button v-for="field in availableCustomerSummaryFields" :key="field.field" type="button" @click="addCustomerSummaryField(field.field)">
                      <span>{{ field.label }}</span><b aria-hidden="true">+</b>
                    </button>
                    <p v-if="!availableCustomerSummaryFields.length" class="crm-empty">Không còn trường phù hợp.</p>
                  </div>
                </section>
                <section>
                  <h3>Được chọn <span>{{ selectedCustomerSummaryFields.length }}</span></h3>
                  <div class="customer-summary-field-list customer-summary-field-list--selected">
                    <button v-for="field in selectedCustomerSummaryFields" :key="field.field" type="button" @click="removeCustomerSummaryField(field.field)">
                      <span>{{ field.label }}</span><b aria-hidden="true">×</b>
                    </button>
                    <p v-if="!selectedCustomerSummaryFields.length" class="crm-empty">Chưa chọn trường nào.</p>
                  </div>
                </section>
              </div>
              <footer>
                <button class="column-default" type="button" @click="resetCustomerSummaryFields">Mặc định</button>
                <div>
                  <button class="crm-button" type="button" @click="cancelCustomerSummaryDialog">Hủy</button>
                  <button class="crm-button primary" type="button" @click="saveCustomerSummaryFields">Lưu</button>
                </div>
              </footer>
            </section>
          </div></teleport>
        </main>

        <main v-else-if="route === 'customers'" class="customer-workspace">
          <header class="customer-heading">
            <div class="customer-title">
              <div class="customer-view-selector">
                <button class="customer-view-trigger" :aria-expanded="customerViewMenuOpen" aria-haspopup="menu" @click="customerViewMenuOpen = !customerViewMenuOpen">
                  <h1>{{ customerListViewLabel }}</h1><CRMIcon name="chevron" />
                </button>
                <div v-if="customerViewMenuOpen" class="customer-view-menu">
                  <strong>CHIA SẺ VỚI TÔI</strong>
                  <button :class="{ active: customerListView === 'all' }" @click="selectCustomerListView('all')">Tất cả khách hàng</button>
                  <button :class="{ active: customerListView === 'mine' }" @click="selectCustomerListView('mine')">Khách hàng của tôi</button>
                  <button disabled data-tooltip="Cần xác định Customer Group dành cho Đối tác/CTV">Tất cả Đối tác/CTV<small>Chưa cấu hình</small></button>
                  <button disabled data-tooltip="Cần xác định mô hình nhóm nhân viên phụ trách">Khách hàng của nhóm tôi<small>Chưa cấu hình</small></button>
                  <button class="add-view" disabled>＋ Thêm giao diện</button>
                </div>
              </div>
              <button class="customer-view-edit" @click="openCustomerColumnDialog">Sửa giao diện</button>
            </div>
            <div class="customer-actions">
              <button class="icon-button" data-tooltip="Kiểu hiển thị" @click="notifyCustomerUnavailable('Kiểu hiển thị khác')"><CRMIcon name="all" /></button>
              <button class="crm-button import" @click="importCustomers"><CRMIcon name="package" /> Nhập từ Excel</button>
              <button class="crm-button" @click="exportResource('customers', { search })">⇤ Xuất Excel</button>
              <button v-if="boot?.resources?.customers?.can_create" class="crm-button primary" @click="createDocument('Customer')"><CRMIcon name="customer" /> Thêm khách hàng</button>
              <div class="customer-more-menu" @keydown.esc.stop="closeCustomerListMoreMenu">
                <button class="icon-button customer-more-trigger" data-tooltip="Thêm thao tác" aria-label="Thêm thao tác" aria-haspopup="menu" :aria-expanded="customerListMoreMenuOpen" @click.stop="toggleCustomerListMoreMenu"><CRMIcon name="more" /></button>
                <div v-if="customerListMoreMenuOpen" class="customer-more-popover" role="menu">
                  <template v-for="item in customerListMoreActions" :key="item.key">
                    <div v-if="item.separator" class="customer-more-separator" aria-hidden="true"></div>
                    <button type="button" role="menuitem" @click="handleCustomerListMoreAction(item.key)">
                      <CRMIcon :name="item.icon" />
                      <span>{{ item.label }}</span>
                      <b v-if="item.ai">AI</b>
                    </button>
                  </template>
                </div>
              </div>
            </div>
          </header>

          <section class="customer-grid" :class="{ 'detail-closed': !customerActivityOpen, 'filter-closed': !customerFilterOpen }">
            <section class="customer-list-panel">
              <div class="customer-list-tools">
                <label class="smart-search"><CRMIcon name="search" /><input v-model="search" placeholder="Tìm kiếm thông minh"><b>AI</b></label>
                <div class="tool-buttons">
                  <button class="icon-button" data-tooltip="Làm mới" @click="loadRows"><CRMIcon name="refresh" /></button>
                  <button class="icon-button" :class="{ active: customerColumnDialogOpen }" data-tooltip="Tùy chỉnh cột" @click="openCustomerColumnDialog"><CRMIcon name="settings" /></button>
                  <button class="icon-button" :class="{ active: customerActivityOpen }" data-tooltip="Ẩn/hiện hoạt động" @click="customerActivityOpen = !customerActivityOpen"><CRMIcon name="activity" /></button>
                  <button class="icon-button" :class="{ active: customerFilterOpen }" data-tooltip="Ẩn/hiện bộ lọc" @click="customerFilterOpen = !customerFilterOpen"><CRMIcon name="filter" /></button>
                </div>
              </div>
              <div class="customer-table-scroll">
                <table class="customer-table">
                  <colgroup><col class="check-column"><col v-for="column in shownCustomerColumns" :key="column.field" :style="{ width: column.width }"></colgroup>
                  <thead><tr><th><input type="checkbox" :checked="allSelected" :indeterminate.prop="someSelected" aria-label="Chọn tất cả" @change="toggleSelectAll"></th><th v-for="column in shownCustomerColumns" :key="column.field">{{ column.label }}</th></tr></thead>
                  <tbody>
                    <tr v-for="row in rows" :key="row.name" :class="{ selected: selected?.name === row.name }" tabindex="0" @click="selectRow(row)" @dblclick="openCustomerDetail(row)" @keydown.enter="openCustomerDetail(row)">
                      <td @click.stop><input type="checkbox" :checked="selectedNames.has(row.name)" :aria-label="'Chọn ' + row.name" @change="toggleSelectRow(row.name)"></td>
                      <td v-for="column in shownCustomerColumns" :key="column.field">
                        <a v-if="column.field === 'name' || column.field === 'customer_name'" href="#" @click.prevent.stop="openCustomerDetail(row)">{{ formatValue(row[column.field], column.field) }}</a>
                        <span v-else>{{ formatValue(row[column.field], column.field) }}</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
                <p v-if="loading" class="crm-empty">Đang tải...</p>
                <p v-else-if="!rows.length" class="crm-empty">Không có khách hàng phù hợp.</p>
              </div>
              <footer class="customer-pagination">
                <strong><CRMIcon name="all" /> Tổng số {{ total.toLocaleString('vi-VN') }}</strong>
                <div><span>Số dòng/trang</span><select v-model.number="pageLength"><option :value="20">20</option><option :value="50">50</option><option :value="100">100</option></select>
                  <span>{{ pageStart }} - {{ pageEnd }}</span>
                  <button :disabled="page <= 1" @click="changePage(1)">|‹</button><button :disabled="page <= 1" @click="changePage(page - 1)">‹</button>
                  <button :disabled="page >= pageCount" @click="changePage(page + 1)">›</button><button :disabled="page >= pageCount" @click="changePage(pageCount)">›|</button>
                </div>
              </footer>
            </section>

            <aside v-if="customerActivityOpen" class="customer-detail-panel">
              <nav class="customer-tabs">
                <button :class="{ active: customerTab === 'activity' }" @click="customerTab = 'activity'">Hoạt động</button>
                <button :class="{ active: customerTab === 'orders' }" @click="customerTab = 'orders'">Mua hàng</button>
                <button :class="{ active: customerTab === 'contacts' }" @click="customerTab = 'contacts'">Liên hệ</button>
              </nav>
              <div v-if="selected" class="customer-detail-body">
                <template v-if="customerTab === 'activity'">
                  <div class="cust-act-list">
                    <button v-for="item in detail?.activities || []" :key="item.activity_type + '-' + item.name" class="cust-act-card" @click="openActivityRecord(item.name, item.activity_type === 'task' ? 'ToDo' : 'Event', detail.document.name, detail.document.customer_name)" data-tooltip="Mở hoạt động">
                      <span class="cust-act-ico"><CRMIcon :name="item.activity_type === 'task' ? 'task' : item.activity_type === 'call' ? 'phone' : 'calendar'" /></span>
                      <span class="cust-act-body">
                        <strong class="cust-act-title">{{ item.subject || item.name }}</strong>
                        <span v-if="item.description && item.description !== item.subject" class="cust-act-desc">{{ stripHtml(item.description) }}</span>
                        <span class="cust-act-foot">
                          <em>{{ item.performed_by_name || item.performed_by || '—' }}</em>
                          <i>·</i>
                          <em>{{ formatValue(item.due_date, 'date') }}</em>
                        </span>
                      </span>
                    </button>
                    <p v-if="detail && !detail.activities.length" class="crm-empty">Chưa có hoạt động liên quan.</p>
                  </div>
                </template>
                <template v-else-if="customerTab === 'orders'">
                  <button v-for="record in customerPurchaseRecords" :key="record.record_doctype + '-' + record.name" class="detail-list-row purchase-row" @click="openRelated(record.record_doctype, record)">
                    <span><em :class="'purchase-type ' + record.record_type">{{ record.record_label }}</em><strong>{{ record.name }}</strong><small>{{ formatValue(record.record_date, 'date') }}</small></span>
                    <span><b>{{ formatValue(record.grand_total, 'grand_total') }}</b><small>{{ record.status || '—' }}</small></span>
                  </button>
                  <p v-if="detail && !customerPurchaseRecords.length" class="crm-empty">Chưa có báo giá, đơn hàng hoặc hóa đơn.</p>
                </template>
                <template v-else>
                  <article v-for="contact in detail?.contacts || []" :key="contact.name" class="detail-list-row contact-row">
                    <span class="contact-list-identity"><i>{{ (contact.full_name || contact.name).slice(0, 2).toUpperCase() }}</i><span><strong>{{ contact.full_name || contact.name }}</strong><small>{{ contact.designation || 'Liên hệ khách hàng' }}</small></span></span>
                    <span><b>{{ contact.mobile_no || contact.phone || '—' }}</b><small>{{ contact.email_id || '—' }}</small></span>
                  </article>
                  <p v-if="detail && !detail.contacts.length" class="crm-empty">Chưa có người liên hệ.</p>
                </template>
              </div>
              <div v-else class="crm-empty customer-no-selection">Chọn một khách hàng để xem hoạt động, mua hàng và liên hệ.</div>
            </aside>

            <aside v-if="customerFilterOpen" class="customer-filter-panel">
              <header><h2>Bộ lọc</h2><button @click="customerFilterOpen = false">×</button></header>
              <section><strong>ĐÃ LƯU</strong><span>⌃</span></section>
              <section><strong>TIÊU CHÍ LỌC</strong><CRMIcon name="search" /></section>
              <div class="column-options filter-options">
                <div v-for="column in customerFilterDefinitions" :key="column.field">
                  <label>
                    <input type="checkbox" :checked="customerEnabledFilters.includes(column.field)" @change="toggleCustomerFilter(column.field)">
                    <span>{{ column.label }}</span>
                  </label>
                  <select v-if="column.field === 'customer_type' && customerEnabledFilters.includes(column.field)" v-model="customerFilterValues[column.field]">
                    <option value="">Tất cả</option><option value="Company">Công ty</option><option value="Individual">Cá nhân</option><option value="Partnership">Đối tác</option>
                  </select>
                  <input v-else-if="customerEnabledFilters.includes(column.field)" v-model="customerFilterValues[column.field]" :type="column.field === 'creation' ? 'date' : 'text'" :placeholder="'Nhập ' + column.label.toLowerCase()">
                </div>
              </div>
            </aside>
          </section>

          <teleport to="body"><div v-if="customerColumnDialogOpen" class="column-dialog-backdrop" @click.self="cancelCustomerColumnDialog">
            <section class="column-dialog">
              <header><h2>Tùy chỉnh cột</h2><button data-tooltip="Đóng" @click="cancelCustomerColumnDialog">×</button></header>
              <div class="column-dialog-body">
                <section class="column-picker">
                  <label class="column-search"><CRMIcon name="search" /><input v-model="customerColumnSearch" placeholder="Tìm kiếm cột"></label>
                  <strong>Chọn trường</strong>
                  <div class="column-picker-list">
                    <label v-for="column in filteredCustomerColumns" :key="column.field">
                      <input type="checkbox" :checked="customerColumnDraft.includes(column.field)" @change="toggleCustomerDraftColumn(column.field)">
                      <span>{{ column.label }}</span>
                    </label>
                    <p v-if="!filteredCustomerColumns.length" class="crm-empty">Không tìm thấy cột phù hợp.</p>
                  </div>
                </section>
                <section class="selected-columns">
                  <header><strong>Đã chọn ({{ selectedCustomerColumns.length }})</strong><button @click="customerColumnDraft = []">Xóa tất cả</button></header>
                  <div>
                    <article v-for="column in selectedCustomerColumns" :key="column.field">
                      <span>{{ column.label }}</span><button :aria-label="'Bỏ cột ' + column.label" @click="removeCustomerDraftColumn(column.field)">×</button>
                    </article>
                    <p v-if="!selectedCustomerColumns.length" class="crm-empty">Chưa chọn cột nào.</p>
                  </div>
                </section>
              </div>
              <footer>
                <button class="column-default" @click="resetCustomerDraftColumns">Mặc định</button>
                <div><button class="crm-button" @click="cancelCustomerColumnDialog">Hủy</button><button class="crm-button primary" @click="saveCustomerColumns">Lưu</button></div>
              </footer>
            </section>
          </div></teleport>
        </main>
`;
