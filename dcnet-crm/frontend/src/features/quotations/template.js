export default `
        <main v-else-if="route === 'quotation-detail'" class="qtd-page">
          <div v-if="quotationDetailLoading" class="crm-empty qtd-loading">Đang tải chi tiết báo giá...</div>
          <div v-else-if="!quotationDetail" class="crm-empty qtd-loading">Không tìm thấy báo giá.</div>
          <template v-else>
            <header class="qtd-header">
              <div class="qtd-heading">
                <button type="button" class="qtd-back" aria-label="Quay lại danh sách báo giá" @click="backToQuotationList">←</button>
                <div>
                  <h1>{{ quotationDetail.document.name }}<span v-if="quotationDetail.document.customer_name || quotationDetail.document.party_name"> - {{ quotationDetail.document.customer_name || quotationDetail.document.party_name }}</span></h1>
                  <button type="button" class="qtd-tag-action" @click="openQuotationTagDialog">◇ Thêm thẻ</button>
                </div>
              </div>
              <div class="qtd-actions">
                <span v-if="quotationDetail.document.custom_approval_requested" class="qtd-approval-badge"><CRMIcon name="history" /> Chờ phê duyệt</span>
                <button v-if="quotationDetail.can_write" type="button" class="crm-button" @click="notifyQuotationDetailAction('Sửa báo giá')">Sửa</button>
                <button v-if="quotationDetail.can_create_order && quotationDetail.document.quotation_to === 'Customer'" type="button" class="crm-button primary" @click="createOrderFromQuotation">Sinh đơn hàng</button>
                <details class="crm-detail-more">
                  <summary class="crm-btn-icon" data-tooltip="Thêm thao tác" aria-label="Thêm thao tác"><CRMIcon name="more" /></summary>
                  <div class="crm-detail-more-menu" role="menu">
                    <button type="button" role="menuitem" @click="openRelated('Quotation', quotationDetail.document); $event.currentTarget.closest('details').removeAttribute('open')"><CRMIcon name="document" /><span>Mở biểu mẫu hệ thống</span></button>
                    <div class="crm-detail-more-separator"></div>
                    <button v-if="quotationDetail.can_write && !quotationDetail.document.custom_approval_requested" type="button" role="menuitem" @click="toggleQuotationApprovalRequest(); $event.currentTarget.closest('details').removeAttribute('open')"><CRMIcon name="send" /><span>Yêu cầu duyệt</span></button>
                    <button v-if="quotationDetail.can_write && quotationDetail.document.custom_approval_requested" type="button" role="menuitem" @click="toggleQuotationApprovalRequest(); $event.currentTarget.closest('details').removeAttribute('open')"><CRMIcon name="close" /><span>Thu hồi phê duyệt</span></button>
                    <div class="crm-detail-more-separator"></div>
                    <button type="button" role="menuitem" @click="openAuditLog('Quotation', quotationDetail.document.name); $event.currentTarget.closest('details').removeAttribute('open')"><CRMIcon name="history" /><span>Nhật ký</span></button>
                  </div>
                </details>
              </div>
            </header>

            <nav class="qtd-tabs" aria-label="Nội dung báo giá">
              <button :class="{active: quotationDetailTab === 'info'}" @click="quotationDetailTab = 'info'">Thông tin chi tiết</button>
              <button :class="{active: quotationDetailTab === 'items'}" @click="quotationDetailTab = 'items'">Hàng hóa <b>{{ quotationDetailTabCount('items') }}</b></button>
              <button :class="{active: quotationDetailTab === 'notes'}" @click="quotationDetailTab = 'notes'">Ghi chú <b v-if="quotationDetailTabCount('notes')">{{ quotationDetailTabCount('notes') }}</b></button>
              <button :class="{active: quotationDetailTab === 'attachments'}" @click="quotationDetailTab = 'attachments'">Tài liệu đính kèm <b v-if="quotationDetailTabCount('attachments')">{{ quotationDetailTabCount('attachments') }}</b></button>
              <button :class="{active: quotationDetailTab === 'orders'}" @click="quotationDetailTab = 'orders'">Đơn hàng <b v-if="quotationDetailTabCount('orders')">{{ quotationDetailTabCount('orders') }}</b></button>
              <button :class="{active: quotationDetailTab === 'activities'}" @click="quotationDetailTab = 'activities'">Công việc đang thực hiện <b v-if="quotationDetailTabCount('activities')">{{ quotationDetailTabCount('activities') }}</b></button>
              <button :class="{active: quotationDetailTab === 'completed'}" @click="quotationDetailTab = 'completed'">Công việc đã hoàn thành <b v-if="quotationDetailTabCount('completed')">{{ quotationDetailTabCount('completed') }}</b></button>
              <button :class="{active: quotationDetailTab === 'conversation'}" @click="quotationDetailTab = 'conversation'">Nội dung trao đổi</button>
            </nav>

            <section v-if="['info','items'].includes(quotationDetailTab)" class="qtd-card">
              <div v-if="quotationDetailTab === 'info'" class="qtd-card-toolbar">
                <label class="qtd-search"><CRMIcon name="search" /><input v-model="quotationDetailFieldSearch" placeholder="Tìm kiếm trường"></label>
                <label class="qtd-empty-toggle"><input type="checkbox" v-model="quotationDetailShowEmpty"><span>Hiển thị dữ liệu trống</span></label>
              </div>

              <template v-if="quotationDetailTab === 'info'">
                <section class="qtd-section">
                  <h2>Thông tin tiền tệ</h2>
                  <div class="qtd-fields qtd-fields--single">
                    <div v-show="showQuotationDetailField('Sử dụng ngoại tệ', quotationDetail.document.currency)"><span>Sử dụng ngoại tệ</span><strong>{{ quotationDetail.document.currency || '—' }}</strong></div>
                  </div>
                </section>

                <section class="qtd-section">
                  <h2>Thông tin chi tiết</h2>
                  <div class="qtd-fields">
                    <div v-show="showQuotationDetailField('Số báo giá', quotationDetail.document.name)"><span>Số báo giá</span><strong>{{ quotationDetail.document.name }}</strong></div>
                    <div v-show="showQuotationDetailField('Ngày báo giá', quotationDetail.document.transaction_date)"><span>Ngày báo giá</span><strong>{{ formatValue(quotationDetail.document.transaction_date, 'date') }}</strong></div>
                    <div v-show="showQuotationDetailField('Cơ hội', quotationDetail.document.opportunity)"><span>Cơ hội</span><a v-if="quotationDetail.document.opportunity" href="#" class="crm-record-link" @click.prevent="openRelated('Opportunity', {name: quotationDetail.document.opportunity})">{{ quotationDetail.document.opportunity }}</a><strong v-else>—</strong></div>
                    <div v-show="showQuotationDetailField('Tình trạng', quotationDetail.document.status)"><span>Tình trạng</span><strong class="qtd-status">{{ quotationDetail.document.status || '—' }}</strong></div>
                    <div v-show="showQuotationDetailField('Loại hàng hóa', quotationDetail.document.order_type)"><span>Loại hàng hóa</span><strong>{{ quotationDetail.document.order_type || '—' }}</strong></div>
                    <div v-show="showQuotationDetailField('Khu vực lắp đặt dịch vụ', quotationDetail.document.custom_installation_zone)"><span>Khu vực lắp đặt dịch vụ</span><strong>{{ quotationDetail.document.custom_installation_zone || '—' }}</strong></div>
                    <div v-show="showQuotationDetailField('Chu kỳ thanh toán', quotationDetail.document.payment_terms_template)"><span>Chu kỳ thanh toán</span><strong>{{ quotationDetail.document.payment_terms_template || '—' }}</strong></div>
                    <div v-show="showQuotationDetailField('Hiệu lực đến ngày', quotationDetail.document.valid_till)"><span>Hiệu lực đến ngày</span><strong>{{ quotationDetail.document.valid_till ? formatValue(quotationDetail.document.valid_till, 'date') : '—' }}</strong></div>
                    <div v-show="showQuotationDetailField('Khách hàng', quotationDetail.document.party_name)"><span>Khách hàng</span><a v-if="quotationDetail.document.quotation_to === 'Customer'" href="#" class="crm-record-link" @click.prevent="openRelated('Customer', {name: quotationDetail.document.party_name})">{{ quotationDetail.document.customer_name || quotationDetail.document.party_name }}</a><strong v-else>{{ quotationDetail.document.party_name || '—' }}</strong></div>
                    <div v-show="showQuotationDetailField('Mã số thuế', quotationDetail.customer_tax_id)"><span>Mã số thuế</span><strong>{{ quotationDetail.customer_tax_id || '—' }}</strong></div>
                    <div v-show="showQuotationDetailField('Liên hệ', quotationDetail.document.contact_person)"><span>Liên hệ</span><a v-if="quotationDetail.document.contact_person" href="#" class="crm-record-link" @click.prevent="openRelated('Contact', {name: quotationDetail.document.contact_person})">{{ quotationDetail.document.contact_display || quotationDetail.document.contact_person }}</a><strong v-else>—</strong></div>
                    <div v-show="showQuotationDetailField('Email KH', quotationDetail.document.contact_email)"><span>Email KH</span><strong>{{ quotationDetail.document.contact_email || '—' }}</strong></div>
                  </div>
                </section>

                <section class="qtd-section">
                  <h2>Thông tin mô tả</h2>
                  <div class="qtd-long-fields">
                    <div v-show="showQuotationDetailField('Mô tả', quotationDetail.document.custom_internal_notes)"><span>Mô tả</span><p>{{ stripHtml(quotationDetail.document.custom_internal_notes || quotationDetail.document.terms || '') || '—' }}</p></div>
                    <div v-show="showQuotationDetailField('Thời gian triển khai', quotationDetail.document.custom_implementation_time)"><span>Thời gian triển khai</span><p>{{ quotationDetail.document.custom_implementation_time || '—' }}</p></div>
                    <div v-show="showQuotationDetailField('Cam kết chất lượng (SLA)', quotationDetail.document.custom_sla)"><span>Cam kết chất lượng (SLA)</span><p>{{ quotationDetail.document.custom_sla || '—' }}</p></div>
                  </div>
                </section>
              </template>

              <section class="qtd-section qtd-items-section">
                <div class="qtd-section-head"><h2>Thông tin hàng hóa</h2><button type="button" @click="openQuotationStockLookup">◇ Tra cứu số lượng tồn</button></div>
                <div class="qtd-table-wrap">
                  <table class="qtd-items-table">
                    <thead><tr><th>STT</th><th>Mã hàng hóa</th><th>Tên hàng hóa</th><th>Mô tả</th><th>Điểm lắp đặt A-End</th><th>Điểm lắp đặt Z-End</th><th>Đơn vị tính</th><th>Số lượng</th><th>Đơn giá</th><th>Thành tiền</th><th>Tỷ lệ CK</th><th>Tiền chiết khấu</th><th>Đơn giá sau CK</th><th>Thành tiền sau CK</th><th>Thuế suất</th><th>Tiền thuế</th><th>Tổng tiền</th></tr></thead>
                    <tbody>
                      <tr v-if="!quotationDetail.items.length"><td colspan="17" class="qtd-empty-row">Chưa có hàng hóa.</td></tr>
                      <tr v-for="item in quotationDetail.items" :key="item.name || item.idx">
                        <td class="num center">{{ item.idx }}</td><td><a href="#" class="crm-record-link" @click.prevent>{{ item.item_code }}</a></td><td>{{ item.item_name || item.item_code }}</td><td class="qtd-wrap-text">{{ stripHtml(item.description) || '—' }}</td><td class="qtd-wrap-text">{{ item.a_end || '—' }}</td><td class="qtd-wrap-text">{{ item.z_end || '—' }}</td><td>{{ item.uom }}</td><td class="num">{{ item.qty }}</td><td class="num">{{ formatValue(item.price_list_rate, 'grand_total') }}</td><td class="num">{{ formatValue(item.gross_amount, 'grand_total') }}</td><td class="num">{{ item.discount_percentage || 0 }}%</td><td class="num">{{ formatValue(item.discount_amount, 'grand_total') }}</td><td class="num">{{ formatValue(item.net_rate, 'grand_total') }}</td><td class="num">{{ formatValue(item.net_amount, 'grand_total') }}</td><td class="num">{{ item.tax_rate || 0 }}%</td><td class="num">{{ formatValue(item.tax_amount, 'grand_total') }}</td><td class="num">{{ formatValue(item.total_with_tax, 'grand_total') }}</td>
                      </tr>
                    </tbody>
                    <tfoot v-if="quotationDetail.items.length"><tr><td colspan="7">Tổng cộng</td><td class="num">{{ quotationDetailTotal('qty') }}</td><td></td><td class="num">{{ formatValue(quotationDetailTotal('gross_amount'), 'grand_total') }}</td><td></td><td class="num">{{ formatValue(quotationDetailTotal('discount_amount'), 'grand_total') }}</td><td></td><td class="num">{{ formatValue(quotationDetailTotal('net_amount'), 'grand_total') }}</td><td></td><td class="num">{{ formatValue(quotationDetailTotal('tax_amount'), 'grand_total') }}</td><td class="num">{{ formatValue(quotationDetailTotal('total_with_tax'), 'grand_total') }}</td></tr></tfoot>
                  </table>
                </div>
                <div class="qtd-table-footer"><strong>Tổng số {{ quotationDetail.items.length }}</strong><span>Số dòng/trang <b>20</b> · 1 - {{ quotationDetail.items.length || 1 }}</span></div>
              </section>

              <section v-if="quotationDetailTab === 'info'" class="qtd-section">
                <h2>Thông tin hệ thống</h2>
                <div class="qtd-fields">
                  <div><span>Người thực hiện</span><strong>{{ quotationDetail.document.owner || '—' }}</strong></div><div><span>Đơn vị</span><strong>{{ quotationDetail.document.company || '—' }}</strong></div>
                  <div><span>Người tạo</span><strong>{{ quotationDetail.document.owner || '—' }}</strong></div><div><span>Ngày tạo</span><strong>{{ formatValue(quotationDetail.document.creation, 'creation') }}</strong></div>
                  <div><span>Người sửa</span><strong>{{ quotationDetail.document.modified_by || '—' }}</strong></div><div><span>Ngày sửa</span><strong>{{ formatValue(quotationDetail.document.modified, 'modified') }}</strong></div>
                  <div><span>Dùng chung</span><strong>{{ quotationDetail.document.custom_is_shared ? 'Có' : 'Không' }}</strong></div><div><span>Bố cục</span><strong>Mẫu báo giá DVVT</strong></div>
                </div>
              </section>
            </section>

            <section v-else class="qtd-card qtd-related-card">
              <template v-if="['notes','conversation'].includes(quotationDetailTab)">
                <div class="qtd-related-head"><h2>{{ quotationDetailTab === 'notes' ? 'Ghi chú' : 'Nội dung trao đổi' }}</h2></div>
                <form v-if="quotationDetail.can_write" class="qtd-composer" @submit.prevent="saveQuotationNote">
                  <textarea v-model="quotationNoteText" rows="3" :placeholder="quotationDetailTab === 'notes' ? 'Nhập ghi chú cho báo giá…' : 'Nhập nội dung cần trao đổi…'" @keydown.ctrl.enter.prevent="saveQuotationNote"></textarea>
                  <div><small>Nhấn Ctrl + Enter để lưu</small><button type="submit" class="crm-button primary" :disabled="quotationNoteSaving || !quotationNoteText.trim()">{{ quotationNoteSaving ? 'Đang lưu…' : 'Thêm nội dung' }}</button></div>
                </form>
                <div v-if="!quotationDetail.comments.length" class="qtd-empty-related">Chưa có nội dung.</div>
                <article v-for="row in quotationDetail.comments" :key="row.name" class="qtd-related-row"><strong>{{ row.comment_by_fullname || 'Người dùng' }}</strong><span>{{ formatValue(row.creation, 'creation') }}</span><p>{{ stripHtml(row.content) }}</p></article>
              </template>
              <template v-else-if="quotationDetailTab === 'attachments'">
                <div class="qtd-related-head">
                  <h2>Tài liệu đính kèm</h2>
                  <button v-if="quotationDetail.can_write" type="button" class="crm-button primary" :disabled="quotationAttachmentUploading" @click="$refs.quotationFileInput.click()">{{ quotationAttachmentUploading ? 'Đang tải…' : '+ Thêm tệp' }}</button>
                  <input ref="quotationFileInput" type="file" hidden @change="uploadQuotationAttachment">
                </div>
                <div v-if="!quotationDetail.attachments.length" class="qtd-empty-related">Chưa có tài liệu đính kèm.</div>
                <a v-for="row in quotationDetail.attachments" :key="row.name" class="qtd-related-row qtd-attachment-link" :href="row.file_url" target="_blank" rel="noopener"><strong class="crm-record-link">{{ row.file_name }}</strong><span>{{ row.owner }} · {{ formatValue(row.creation, 'creation') }}</span></a>
              </template>
              <template v-else-if="quotationDetailTab === 'orders'">
                <div class="qtd-related-head"><h2>Đơn hàng</h2><button v-if="quotationDetail.can_create_order && quotationDetail.document.quotation_to === 'Customer'" type="button" class="crm-button primary" @click="createOrderFromQuotation">+ Sinh đơn hàng</button></div>
                <div v-if="!quotationDetail.orders.length" class="qtd-empty-related">Chưa có đơn hàng được sinh từ báo giá này.</div>
                <button v-for="row in quotationDetail.orders" :key="row.name" class="qtd-related-row qtd-related-button" @click="openRelated('Sales Order', row)"><strong class="crm-record-link">{{ row.name }}</strong><span>{{ formatValue(row.transaction_date, 'date') }} · {{ row.status }} · {{ formatValue(row.grand_total, 'grand_total') }}</span></button>
              </template>
              <template v-else-if="['activities','completed'].includes(quotationDetailTab)">
                <div class="qtd-related-head"><h2>{{ quotationDetailTab === 'completed' ? 'Công việc đã hoàn thành' : 'Công việc đang thực hiện' }}</h2><button v-if="quotationDetailTab === 'activities' && quotationDetail.can_create_activity" type="button" class="crm-button primary" @click="createQuotationActivity">+ Thêm công việc</button></div>
                <div v-if="!quotationDetail.activities.filter(row => quotationDetailTab === 'completed' ? row.status === 'Closed' : row.status !== 'Closed').length" class="qtd-empty-related">Không có công việc nào.</div>
                <button v-for="row in quotationDetail.activities.filter(row => quotationDetailTab === 'completed' ? row.status === 'Closed' : row.status !== 'Closed')" :key="row.name" type="button" class="qtd-related-row qtd-related-button" @click="openQuotationActivity(row)"><strong class="crm-record-link">{{ row.description }}</strong><span>{{ row.status }} · {{ row.priority || 'Medium' }} · {{ row.date ? formatValue(row.date, 'date') : '—' }}</span></button>
              </template>
            </section>
          </template>

          <teleport to="body"><div v-if="qtStockDialogOpen" class="column-dialog-backdrop customer-summary-dialog-backdrop" @click.self="qtStockDialogOpen = false">
            <section class="qt-stock-dialog">
              <header class="qt-stock-dialog-header">
                <h2>Tra cứu số lượng tồn</h2>
                <button type="button" data-tooltip="Đóng" @click="qtStockDialogOpen = false">×</button>
              </header>
              <div class="qt-stock-dialog-body">
                <table class="qt-stock-table">
                  <thead>
                    <tr><th>Mã hàng hóa</th><th>Diễn giải</th><th>Đơn vị tính</th><th>Kho</th><th>Số lượng</th><th>SL đã giao</th><th>Số lượng tồn</th></tr>
                  </thead>
                  <tbody>
                    <tr v-if="qtStockLoading"><td colspan="7" class="qt-stock-empty">Đang tải...</td></tr>
                    <tr v-else-if="!qtStockRows.length"><td colspan="7" class="qt-stock-empty">Không có dữ liệu.</td></tr>
                    <tr v-else v-for="row in qtStockRows.slice((qtStockPage-1)*qtStockPageLength, (qtStockPage-1)*qtStockPageLength + qtStockPageLength)" :key="row.item_code">
                      <td>{{ row.item_code }}</td>
                      <td>{{ row.description }}</td>
                      <td>{{ row.uom || '—' }}</td>
                      <td>{{ row.warehouse || '-' }}</td>
                      <td>{{ row.qty }}</td>
                      <td>{{ row.delivered_qty }}</td>
                      <td>{{ row.stock_qty }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <footer class="qt-stock-dialog-footer">
                <span>Tổng số <strong>{{ qtStockRows.length }}</strong></span>
                <div class="qt-stock-pagination">
                  <span>Số dòng/trang</span>
                  <select v-model.number="qtStockPageLength"><option :value="10">10</option><option :value="20">20</option><option :value="50">50</option></select>
                  <span>{{ qtStockRows.length ? ((qtStockPage-1)*qtStockPageLength + 1) : 0 }} - {{ Math.min(qtStockPage*qtStockPageLength, qtStockRows.length) }}</span>
                  <button type="button" :disabled="qtStockPage<=1" @click="qtStockPage = 1">«</button>
                  <button type="button" :disabled="qtStockPage<=1" @click="qtStockPage--">‹</button>
                  <button type="button" :disabled="qtStockPage*qtStockPageLength >= qtStockRows.length" @click="qtStockPage++">›</button>
                  <button type="button" :disabled="qtStockPage*qtStockPageLength >= qtStockRows.length" @click="qtStockPage = Math.ceil(qtStockRows.length/qtStockPageLength)">»</button>
                </div>
                <button type="button" class="crm-button primary" @click="qtStockDialogOpen = false">Đóng</button>
              </footer>
            </section>
          </div></teleport>
        </main>

        <main v-else-if="route === 'create-quotation'" class="opportunity-form-page">
          <header class="opportunity-form-header">
            <div>
              <button class="crm-button" @click="backToQuotations()">← Quay lại</button>
              <h1>Thêm Báo giá</h1>
              <span class="so-type-badge">
                <select v-model="createQTForm.order_type" class="so-type-sel">
                  <option value="Sales">Mẫu báo giá DVVT</option>
                  <option value="Maintenance">Mẫu báo giá khác</option>
                </select>
              </span>
            </div>
            <div>
              <button class="crm-button" :disabled="createQTSaving" @click="backToQuotations()">Hủy</button>
              <button class="crm-button" :disabled="createQTSaving" @click="saveCreateQuotation(true)">{{ createQTSaving ? 'Đang lưu...' : 'Lưu và thêm' }}</button>
              <button class="crm-button primary" :disabled="createQTSaving" @click="saveCreateQuotation(false)">{{ createQTSaving ? 'Đang lưu...' : 'Lưu' }}</button>
            </div>
          </header>

          <form class="opportunity-form-card" @submit.prevent="saveCreateQuotation(false)">

            <section>
              <h2>Thông tin chi tiết</h2>
              <div class="opportunity-form-grid">
                <label><span>Số báo giá</span><input disabled placeholder="Mã tự sinh"></label>
                <label><span>Ngày báo giá <b>*</b></span><input type="date" v-model="createQTForm.transaction_date" required></label>
                <label><span>Cơ hội</span>
                  <search-select v-model="createQTForm.opportunity" :options="qtFormOptions.opportunities" label-key="title" placeholder="- Không chọn -"></search-select>
                </label>
                <label><span>Tình trạng</span>
                  <select v-model="createQTForm.status">
                    <option value="Draft">Bản thảo</option>
                    <option value="Open">Đang mở</option>
                    <option value="Ordered">Đã đặt hàng</option>
                    <option value="Lost">Thất bại</option>
                  </select>
                </label>
                <label><span>Chu kỳ thanh toán <b>*</b></span>
                  <search-select v-model="createQTForm.payment_terms_template" :options="qtFormOptions.payment_terms" placeholder="- Không chọn -"></search-select>
                </label>
                <label><span>Khu vực lắp đặt dịch vụ <b>*</b></span>
                  <select v-model="createQTForm.installation_zone">
                    <option value="Bắc">Miền Bắc</option>
                    <option value="Trung">Miền Trung</option>
                    <option value="Nam">Miền Nam</option>
                    <option value="Toàn Quốc">Toàn Quốc</option>
                  </select>
                </label>
                <label><span>Khách hàng <b>*</b></span>
                  <input v-if="createQTContext.customer" :value="createQTForm.customer" disabled>
                  <search-select v-else v-model="createQTForm.customer" @update:model-value="onQTCustomerChange" @add="createDocument('Customer')" :options="qtFormOptions.customers" value-key="name" label-key="customer_name" :meta-keys="['tax_id','name','mobile_no']" desc-key="primary_address" add-label="Thêm khách hàng" placeholder="- Không chọn -"></search-select>
                </label>
                <label><span>Hiệu lực đến ngày</span><input type="date" v-model="createQTForm.valid_till" placeholder="DD/MM/YYYY"></label>
                <label><span>Liên hệ</span>
                  <search-select v-model="createQTForm.contact_person" :options="qtFormOptions.contacts" label-key="full_name" sub-key="mobile_no" placeholder="- Không chọn -"></search-select>
                </label>
                <label><span>Mã số thuế</span><input v-model="createQTForm.tax_id" placeholder="Mã số thuế..."></label>
                <div></div>
                <label><span>Email KH</span><input v-model="createQTForm.email_id" placeholder="Email khách hàng..."></label>
              </div>
            </section>

            <section>
              <h2>Thông tin mô tả</h2>
              <div class="opportunity-form-grid">
                <label style="grid-column: 1 / -1"><span>Mô tả</span><textarea v-model="createQTForm.note" placeholder="Mô tả báo giá..."></textarea></label>
                <label style="grid-column: 1 / -1"><span>Thời gian triển khai</span><textarea v-model="createQTForm.implementation_time" placeholder="Thời gian triển khai..."></textarea></label>
                <label style="grid-column: 1 / -1"><span>Cam kết chất lượng (SLA)</span><textarea v-model="createQTForm.sla" placeholder="Cam kết chất lượng dịch vụ..."></textarea></label>
              </div>
            </section>

            <section>
              <div class="opportunity-section-heading">
                <div><h2>Thông tin hàng hóa</h2></div>
                <div class="qt-goods-head-actions">
                  <label v-if="createQTItems.length" class="qt-auto-qty"><input type="checkbox" v-model="qtAutoIncreaseQty"><span>Tự động tăng SL khi chọn trùng</span></label>
                  <button v-if="createQTItems.length > 1" type="button" class="danger" @click="clearQTItems">× Xóa tất cả</button>
                </div>
              </div>
              <div v-if="!createQTItems.length" class="opportunity-items-empty">
                <button type="button" class="crm-button primary" @click="openQTItemPicker">＋ Chọn hàng hóa</button>
                <button type="button" class="so-paste-excel-btn" @click="addQTItem" style="margin-left:8px">
                  <svg width="14" height="14" viewBox="0 0 16 16" fill="none"><rect x="2" y="1" width="8" height="11" rx="1" stroke="currentColor" stroke-width="1.4"/><path d="M5 1h4a1 1 0 011 1v1H4V2a1 1 0 011-1z" stroke="currentColor" stroke-width="1.4"/><path d="M10 6h4M10 9h4M10 12h4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>
                  Thêm dòng trống
                </button>
              </div>
              <div v-else class="opportunity-items-scroll">
                <table class="opportunity-items-table so-items-table">
                  <colgroup>
                    <col class="col-stt"><col class="col-item-code"><col class="col-item-name">
                    <col class="col-desc"><col class="col-aend"><col class="col-zend">
                    <col class="col-uom"><col class="col-qty"><col class="col-price">
                    <col class="col-amt"><col class="col-ck-pct"><col class="col-ck-amt">
                    <col class="col-price-ck"><col class="col-amt-ck"><col class="col-tax-rate"><col class="col-tax-amt"><col class="col-amt-total">
                  </colgroup>
                  <thead>
                    <tr>
                      <th>STT</th><th>Mã hàng hóa</th><th>Tên hàng hóa <b>*</b></th><th>Mô tả</th>
                      <th>Điểm lắp đặt A-End</th><th>Điểm lắp đặt Z-End</th>
                      <th>Đơn vị tính</th><th>Số lượng</th><th>Đơn giá</th><th>Thành tiền</th>
                      <th>Tỷ lệ chiết ...</th><th>Tiền chiết khấu</th><th>Đơn giá sau CK</th>
                      <th>Thành tiền sa...</th><th>Thuế suất</th><th>Tiền thuế</th><th>Tổng tiền</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(item, index) in createQTItems" :key="index">
                      <td class="item-stt-cell">
                        <span class="item-stt-num">{{ index + 1 }}</span>
                        <button type="button" class="item-row-del" @click="removeQTItem(index)">×</button>
                      </td>
                      <td><search-select :model-value="item.item_code" @update:model-value="(v) => { item.item_code = v; autoFillQTItemByCode(item); }" :options="qtItemList" value-key="name" label-key="name" desc-key="item_name" placeholder="Mã hàng"></search-select></td>
                      <td><input v-model="item.item_name" placeholder="Tên hàng hóa / dịch vụ"></td>
                      <td><input v-model="item.description" placeholder="Mô tả..."></td>
                      <td><input v-model="item.a_end" placeholder="Địa chỉ A-End..."></td>
                      <td><input v-model="item.z_end" placeholder="Địa chỉ Z-End..."></td>
                      <td><input v-model="item.uom" placeholder="Cái"></td>
                      <td><input type="number" min="0" step="any" v-model.number="item.qty" @input="updateQTItemAmount(item)"></td>
                      <td><input type="number" min="0" step="any" v-model.number="item.price_list_rate" @input="updateQTItemRate(item)" placeholder="0"></td>
                      <td class="item-calc-cell">{{ formatValue(qtItemPreTotal(item), 'grand_total') }}</td>
                      <td><input type="number" min="0" max="100" step="any" v-model.number="item.discount_percentage" @input="updateQTItemRate(item)" placeholder="0"></td>
                      <td class="item-calc-cell">{{ formatValue(qtItemDiscount(item), 'grand_total') }}</td>
                      <td><input type="number" min="0" step="any" v-model.number="item.rate" @input="updateQTItemAmount(item)" placeholder="0"></td>
                      <td class="item-calc-cell">{{ formatValue(item.amount, 'grand_total') }}</td>
                      <td><input type="number" min="0" v-model.number="item.tax_rate" placeholder="0"></td>
                      <td class="item-calc-cell">{{ formatValue(qtItemTax(item), 'grand_total') }}</td>
                      <td class="item-calc-cell">{{ formatValue((item.amount||0) + qtItemTax(item), 'grand_total') }}</td>
                    </tr>
                    <tr class="items-total-row">
                      <td></td>
                      <td colspan="6" class="items-total-label">Tổng cộng</td>
                      <td>{{ qtTotalQty() }}</td>
                      <td></td>
                      <td class="items-total-num">{{ formatValue(qtSubtotal(), 'grand_total') }}</td>
                      <td></td>
                      <td class="items-total-num">{{ formatValue(qtTotalDiscount(), 'grand_total') }}</td>
                      <td></td>
                      <td class="items-total-num">{{ formatValue(qtGrandTotal(), 'grand_total') }}</td>
                      <td></td>
                      <td class="items-total-num">{{ formatValue(qtTotalTax(), 'grand_total') }}</td>
                      <td class="items-total-num">{{ formatValue(qtGrandTotal() + qtTotalTax(), 'grand_total') }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-if="createQTItems.length" class="opportunity-item-actions">
                <strong>Tổng số: {{ createQTItems.length }}</strong>
                <div class="item-action-btns">
                  <button type="button" class="crm-button" @click="addQTItem">＋ Thêm dòng</button>
                  <button type="button" class="crm-button primary" @click="openQTItemPicker">＋ Chọn hàng hóa</button>
                </div>
              </div>
              <datalist id="qt-item-options">
                <option v-for="opt in qtItemList" :key="opt.name" :value="opt.name">{{ opt.item_name }}</option>
              </datalist>

              <teleport to="body"><div v-if="qtItemPickerOpen" class="crm-modal-backdrop" @click.self="closeQTItemPicker">
                <div class="crm-modal item-picker-modal">
                  <header>
                    <h2>Chọn hàng hóa<span v-if="qtItemPickerSelected.length" class="picker-selected-badge">{{ qtItemPickerSelected.length }} đã chọn</span></h2>
                    <button type="button" @click="closeQTItemPicker">×</button>
                  </header>
                  <div class="item-picker-toolbar">
                    <div class="item-picker-search-wrap">
                      <svg width="14" height="14" viewBox="0 0 16 16" fill="none"><circle cx="7" cy="7" r="5" stroke="#9ca3af" stroke-width="1.5"/><path d="M11 11l3 3" stroke="#9ca3af" stroke-width="1.5" stroke-linecap="round"/></svg>
                      <input v-model="qtItemPickerSearch" @input="qtItemPickerPage = 1" placeholder="Tìm theo mã hoặc tên hàng hóa..." class="item-picker-search" autofocus>
                    </div>
                    <select v-model="qtItemPickerCategoryFilter" @change="qtItemPickerPage = 1" class="item-picker-cat">
                      <option value="">Tất cả nhóm</option>
                      <option v-for="cat in qtItemPickerCategories" :key="cat" :value="cat">{{ cat }}</option>
                    </select>
                  </div>
                  <div class="item-picker-table-wrap">
                    <table class="item-picker-table">
                      <thead>
                        <tr>
                          <th class="picker-check-col">
                            <input type="checkbox"
                              :checked="qtItemPickerRows.length > 0 && qtItemPickerRows.every(r => qtItemPickerSelected.includes(r.name))"
                              @change="e => { if(e.target.checked) qtItemPickerRows.forEach(r => { if(!qtItemPickerSelected.includes(r.name)) qtItemPickerSelected.push(r.name) }); else qtItemPickerSelected = qtItemPickerSelected.filter(n => !qtItemPickerRows.find(r => r.name === n)) }">
                          </th>
                          <th>Mã hàng hóa</th><th>Tên hàng hóa</th><th>Nhóm</th><th>ĐVT</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="item in qtItemPickerRows" :key="item.name"
                          @click="toggleQTItemPickerRow(item.name)"
                          :class="{ selected: qtItemPickerSelected.includes(item.name) }">
                          <td class="picker-check-col"><input type="checkbox" :checked="qtItemPickerSelected.includes(item.name)" @click.stop="toggleQTItemPickerRow(item.name)"></td>
                          <td>{{ item.name }}</td>
                          <td>{{ item.item_name }}</td>
                          <td>{{ item.item_group || '—' }}</td>
                          <td>{{ item.stock_uom || 'Cái' }}</td>
                        </tr>
                        <tr v-if="!qtItemPickerRows.length" class="picker-empty-row">
                          <td colspan="5">Không tìm thấy hàng hóa phù hợp.</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <div class="item-picker-footer">
                    <span>Tổng <strong>{{ qtItemPickerFiltered.length }}</strong> hàng hóa</span>
                    <div class="item-picker-pagination">
                      <span>Số dòng/trang</span>
                      <select v-model.number="qtItemPickerPageLength" @change="qtItemPickerPage = 1">
                        <option :value="20">20</option><option :value="50">50</option><option :value="100">100</option>
                      </select>
                      <span>{{ (qtItemPickerPage-1)*qtItemPickerPageLength+1 }}–{{ Math.min(qtItemPickerPage*qtItemPickerPageLength, qtItemPickerFiltered.length) }}</span>
                      <button type="button" :disabled="qtItemPickerPage <= 1" @click="qtItemPickerPage = 1" data-tooltip="Trang đầu">«</button>
                      <button type="button" :disabled="qtItemPickerPage <= 1" @click="qtItemPickerPage--" data-tooltip="Trang trước">‹</button>
                      <button type="button" :disabled="qtItemPickerPage >= qtItemPickerPageCount" @click="qtItemPickerPage++" data-tooltip="Trang sau">›</button>
                      <button type="button" :disabled="qtItemPickerPage >= qtItemPickerPageCount" @click="qtItemPickerPage = qtItemPickerPageCount" data-tooltip="Trang cuối">»</button>
                    </div>
                  </div>
                  <footer>
                    <button type="button" class="crm-button" @click="closeQTItemPicker">Hủy</button>
                    <button type="button" class="crm-button primary" :disabled="!qtItemPickerSelected.length" @click="confirmQTItemPicker">
                      {{ qtItemPickerSelected.length ? 'Thêm ' + qtItemPickerSelected.length + ' hàng hóa' : 'Chọn hàng hóa' }}
                    </button>
                  </footer>
                </div>
              </div></teleport>
            </section>

            <section>
              <h2>Thông tin hệ thống</h2>
              <div class="opportunity-form-grid">
                <label><span>Người thực hiện</span><input disabled :value="qtCurrentUser"></label>
                <label><span>Công ty</span><input v-model="createQTForm.company" placeholder="Tên công ty..."></label>
                <label class="so-check-row"><span>Dùng chung</span><input type="checkbox" v-model="createQTForm.shared_flag"></label>
              </div>
            </section>

          </form>
        </main>

        <main v-else-if="route === 'quotations'" class="orders-list-layout qt-list-page">

          <!-- Row 1: Title + view dropdown + add (full width, above the 3-column split) -->
          <div class="orders-toolbar-r1">
            <div class="otr1-left">
              <h1>Tất cả báo giá</h1>
              <svg class="otr1-title-caret" viewBox="0 0 16 16" fill="none" width="14" height="14"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
              <span v-if="qtSavedFilterActive" class="otr1-filter-active">● {{ QT_SAVED_FILTERS.find(f=>f.key===qtSavedFilterActive)?.label }}</span>
            </div>
            <div class="otr1-right">
              <button class="crm-btn-ghost otr1-import-btn" @click="importQuotations"><CRMIcon name="document" /> Nhập từ Excel</button>
              <button v-if="boot?.resources?.[route]?.can_create" class="crm-btn-ghost otr1-add-btn" @click="createDocument()"><CRMIcon name="plus" /> Thêm</button>
              <details class="crm-detail-more">
                <summary class="crm-btn-icon" data-tooltip="Thêm thao tác" aria-label="Thêm thao tác"><CRMIcon name="more" /></summary>
                <div class="crm-detail-more-menu" role="menu">
                  <button type="button" role="menuitem" @click="toggleQuotationQuickStats(); $event.currentTarget.closest('details').removeAttribute('open')">
                    <CRMIcon name="history" /><span>Thống kê nhanh</span>
                  </button>
                  <div class="crm-detail-more-separator"></div>
                  <button type="button" role="menuitem" @click="exportResource('quotations'); $event.currentTarget.closest('details').removeAttribute('open')">
                    <CRMIcon name="externalLink" /><span>Xuất ra Excel</span>
                  </button>
                </div>
              </details>
            </div>
          </div>

          <div class="qt-list-body">
          <!-- ── Main table panel ─────────────────────────────── -->
          <div class="orders-main">

            <!-- Row 2: Search + action icons -->
            <div class="orders-toolbar-r2">
              <div class="otr2-search">
                <svg width="14" height="14" viewBox="0 0 16 16" fill="none"><circle cx="7" cy="7" r="5" stroke="#9ca3af" stroke-width="1.5"/><path d="M11 11l3 3" stroke="#9ca3af" stroke-width="1.5" stroke-linecap="round"/></svg>
                <input v-model="search" @keyup.enter="loadRows" class="otr2-inp" placeholder="Tìm kiếm thông minh">
              </div>
              <div class="otr2-actions">
                <button class="crm-btn-icon" @click="loadRows" data-tooltip="Làm mới">
                  <svg viewBox="0 0 16 16" fill="none" width="14" height="14"><path d="M2.5 8a5.5 5.5 0 1 1 1.1 3.3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M2.5 11.5V8H6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </button>
                <button class="crm-btn-icon" :class="{active: quotationColumnDialogOpen}" data-tooltip="Tùy chỉnh cột" @click="openQuotationColumnDialog"><CRMIcon name="settings" /></button>
                <button class="crm-btn-icon" :class="{active: qtItemsPanelOpen}" @click="qtItemsPanelOpen = !qtItemsPanelOpen" data-tooltip="Ẩn/hiện Hàng hóa"><CRMIcon name="package" /></button>
                <button class="crm-btn-icon" :class="{active: qtFilterOpen}" @click="qtFilterOpen = !qtFilterOpen; if (qtFilterOpen) qtQuickStatsOpen = false" data-tooltip="Bộ lọc">
                  <svg viewBox="0 0 16 16" fill="none" width="14" height="14"><path d="M2 4h12M4 8h8M6 12h4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
                </button>
              </div>
            </div>

            <!-- Table -->
            <div class="orders-table-scroll">
              <table class="orders-table">
                <thead>
                  <tr>
                    <th class="ot-chk-col"><input type="checkbox"></th>
                    <th class="ot-col-tag">Thẻ</th>
                    <th v-for="column in shownQuotationColumns" :key="column.field" class="ot-th-resizable" :style="{ width: quotationColumnWidths[column.field] || column.width }">
                      <span v-if="column.field !== 'transaction_date'">{{ column.label }}</span>
                      <button v-else type="button" class="ot-sort-th" :class="{ 'ot-sort-th--active': qtSortField === 'transaction_date' }" @click="toggleQuotationSort('transaction_date')">
                        {{ column.label }}
                        <CRMIcon name="chevron" :class="{ 'ot-sort-icon--asc': qtSortField === 'transaction_date' && qtSortDirection === 'asc' }" />
                      </button>
                      <span class="ot-th-resize" @mousedown="startQuotationColumnResize($event, column.field, column.width)"></span>
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="loading"><td :colspan="shownQuotationColumns.length + 2" class="ot-loading">Đang tải...</td></tr>
                  <tr v-else-if="!rows.length"><td :colspan="shownQuotationColumns.length + 2" class="ot-loading">Chưa có dữ liệu phù hợp.</td></tr>
                  <tr v-else v-for="row in rows" :key="row.name"
                    :class="{ 'ot-selected': selected?.name === row.name }"
                    @click="selectRow(row); loadQuotationDetail(row.name)"
                    @dblclick="openDocument(row)">
                    <td class="ot-chk-col" @click.stop><input type="checkbox"></td>
                    <td class="ot-tag-cell">
                      <span v-if="row.status && row.status !== 'Draft'" :class="'ot-qstatus ot-qstatus--' + quotationStatusClass(row.status)">{{ row.status }}</span>
                      <span v-else class="ot-muted">—</span>
                    </td>
                    <td v-for="column in shownQuotationColumns" :key="column.field" :style="{ width: quotationColumnWidths[column.field] || column.width }">
                      <a v-if="column.field === 'name'" class="ot-link" @click.stop="openDocument(row)">{{ row.name }}</a>
                      <span v-else-if="column.field === 'customer_name'" class="ot-customer-cell" :data-tooltip="row.customer_name || row.party_name">{{ row.customer_name || row.party_name || '—' }}</span>
                      <span v-else-if="column.field === 'contact_display'" class="ot-contact-cell" :data-tooltip="row.contact_display">{{ row.contact_display || '—' }}</span>
                      <span v-else :data-tooltip="row[column.field]">{{ formatValue(row[column.field], column.field) }}</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Footer: aggregates + pagination -->
            <div class="orders-footer">
              <div class="of-agg">
                <span class="of-agg-sep">≡</span>
                <span>Tổng số <strong>{{ total }}</strong></span>
                <span class="of-agg-div">|</span>
                <span>Thành tiền: <strong>{{ formatValue(rows.reduce((s,r) => s+(r.net_total||0), 0), 'grand_total') }}</strong></span>
                <span class="of-agg-div">|</span>
                <span>Tiền thuế: <strong>{{ formatValue(rows.reduce((s,r) => s+(r.total_taxes_and_charges||0), 0), 'grand_total') }}</strong></span>
                <span class="of-agg-div">|</span>
                <span>Tiền chiết khấu: <strong>{{ formatValue(rows.reduce((s,r) => s+(r.discount_amount||0), 0), 'grand_total') }}</strong></span>
                <span class="of-agg-div">|</span>
                <span>Tổng tiền: <strong>{{ formatValue(rows.reduce((s,r) => s+(r.grand_total||0), 0), 'grand_total') }}</strong></span>
              </div>
              <div class="of-pagination">
                <span>Số dòng/trang</span>
                <select v-model.number="pageLength" class="of-page-len">
                  <option :value="20">20</option>
                  <option :value="50">50</option>
                  <option :value="100">100</option>
                </select>
                <span>{{ pageStart }} – {{ pageEnd }}</span>
                <button class="of-pg-btn" :disabled="page <= 1" @click="changePage(1)">«</button>
                <button class="of-pg-btn" :disabled="page <= 1" @click="changePage(page - 1)">‹</button>
                <button class="of-pg-btn" :disabled="page >= pageCount" @click="changePage(page + 1)">›</button>
                <button class="of-pg-btn" :disabled="page >= pageCount" @click="changePage(pageCount)">»</button>
              </div>
            </div>
          </div>

          <!-- ── Items detail panel (Hàng hóa) ──────────────────── -->
          <aside v-if="selected && qtItemsPanelOpen" class="orders-detail-panel">
            <div class="odp-header">
              <div class="odp-header-title">
                <span>Hàng hóa</span>
                <span class="odp-count">{{ qtDetailItems.length }}</span>
              </div>
              <div class="odp-header-actions">
                <button class="crm-btn-icon" :class="{ active: qtItemsSearchOpen }" @click="toggleQuotationItemsSearch" data-tooltip="Tìm kiếm hàng hóa"><CRMIcon name="search" /></button>
                <button class="crm-btn-icon" @click="openDocument()" data-tooltip="Sửa báo giá"><CRMIcon name="edit" /></button>
              </div>
            </div>

            <div v-if="qtItemsSearchOpen" class="odp-search">
              <CRMIcon name="search" />
              <input v-model="qtItemsSearch" placeholder="Tìm kiếm hàng hóa" autofocus>
            </div>

            <div class="odp-so-meta">
              <div class="odp-so-name">{{ selected.name }}</div>
              <div class="odp-so-customer">{{ selected.customer_name || selected.party_name }}</div>
            </div>

            <div class="odp-items-list">
              <div v-if="qtDetailLoading" class="odp-empty">Đang tải...</div>
              <template v-else-if="qtDetailItemsFiltered.length">
                <div v-for="(item, idx) in qtDetailItemsFiltered" :key="item.item_code + idx" class="odp-item" :class="{ 'odp-item--open': qtExpandedItem === idx }">
                  <div class="odp-item-main" @click="toggleQuotationDetailItem(idx)">
                    <div class="odp-item-heading">
                      <span class="odp-item-idx">#{{ idx + 1 }}.</span>
                      <span class="odp-item-name">{{ item.item_code }}{{ item.item_name && item.item_name !== item.item_code ? ' - ' + item.item_name : '' }}</span>
                      <svg class="odp-item-chevron" viewBox="0 0 16 16" fill="none" width="12" height="12"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    </div>
                    <div class="odp-item-calc">
                      <span>{{ item.qty }} {{ item.uom }} ×</span>
                      <span class="odp-masked">{{ formatValue(item.rate, 'grand_total') }}</span>
                      <span>=</span>
                      <span class="odp-masked odp-masked--total">{{ formatValue(item.amount, 'grand_total') }}</span>
                    </div>
                  </div>
                  <div v-if="qtExpandedItem === idx" class="odp-item-detail">
                    <div class="odp-item-detail-grid">
                      <div class="odp-item-detail-cell">
                        <div class="odp-item-detail-label">Đơn giá sau CK</div>
                        <div class="odp-masked">{{ formatValue(item.net_rate, 'grand_total') }}</div>
                      </div>
                      <div class="odp-item-detail-cell">
                        <div class="odp-item-detail-label">Thành tiền</div>
                        <div class="odp-masked">{{ formatValue(item.net_amount, 'grand_total') }}</div>
                      </div>
                    </div>
                    <div v-if="item.description" class="odp-item-detail-row">
                      <div class="odp-item-detail-label">Mô tả</div>
                      <div class="odp-item-detail-value">{{ item.description }}</div>
                    </div>
                  </div>
                </div>
              </template>
              <div v-else class="odp-empty">Chưa có hàng hóa</div>
            </div>

            <div class="odp-footer">
              <div class="odp-footer-row">
                <span>Số lượng: <strong>{{ qtDetailItems.reduce((s,i) => s+(i.qty||0), 0) }}</strong></span>
                <span>Tổng tiền: <strong>{{ formatValue(qtDetailItems.reduce((s,i) => s+(i.amount||0), 0), 'grand_total') }}</strong></span>
              </div>
            </div>
          </aside>

          <!-- ── Thống kê nhanh ──────────────────────────────────── -->
          <aside v-if="qtQuickStatsOpen" class="orders-filter-panel qt-stats-panel">
            <div class="ofp-header">
              <span class="ofp-title">Thống kê nhanh</span>
              <button class="crm-btn-icon" @click="qtQuickStatsOpen = false" data-tooltip="Đóng">
                <svg viewBox="0 0 16 16" fill="none" width="11" height="11"><path d="M3 3l10 10M13 3L3 13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
              </button>
            </div>
            <div class="ofp-body">
              <div v-if="qtQuickStatsLoading" class="ofp-empty">Đang tải...</div>
              <template v-else-if="qtQuickStats">
                <div class="qt-stats-summary">
                  <div class="qt-stats-summary-item">
                    <span>Tổng số báo giá</span>
                    <strong>{{ qtQuickStats.total_count }}</strong>
                  </div>
                  <div class="qt-stats-summary-item">
                    <span>Tổng giá trị</span>
                    <strong>{{ formatValue(qtQuickStats.total_value, 'grand_total') }}</strong>
                  </div>
                </div>
                <div class="ofp-section">
                  <div class="ofp-section-title">Theo trạng thái</div>
                  <div v-for="row in qtQuickStats.by_status" :key="row.status" class="qt-stats-row">
                    <span class="qt-stats-row-label">{{ row.status }}</span>
                    <span class="qt-stats-row-count">{{ row.count }}</span>
                    <span class="qt-stats-row-value">{{ formatValue(row.value, 'grand_total') }}</span>
                  </div>
                </div>
              </template>
            </div>
          </aside>

          <!-- ── Filter panel (Bộ lọc) ──────────────────────────── -->
          <aside v-if="qtFilterOpen" class="orders-filter-panel">
            <div class="ofp-header">
              <span class="ofp-title">Bộ lọc</span>
              <button class="crm-btn-icon" @click="qtFilterOpen = false" data-tooltip="Đóng">
                <svg viewBox="0 0 16 16" fill="none" width="11" height="11"><path d="M3 3l10 10M13 3L3 13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
              </button>
            </div>
            <div class="ofp-body">
              <div class="ofp-section">
                <div class="ofp-section-title">TIÊU CHÍ LỌC</div>
                <label class="ofp-crit-search"><CRMIcon name="search" /><input v-model="qtFilterCriteriaSearch" placeholder="Tìm kiếm tiêu chí"></label>
                <label v-for="fc in QT_FILTER_CRITERIA.filter(f => !qtFilterCriteriaSearch.trim() || f.label.toLocaleLowerCase('vi').includes(qtFilterCriteriaSearch.trim().toLocaleLowerCase('vi')))" :key="fc.key" class="ofp-crit-item">
                  <input type="checkbox"
                    :checked="quotationsEnabledFilters.includes(fc.field)"
                    @change="toggleQuotationsFilter(fc.field)"
                    class="ofp-crit-chk">
                  <span>{{ fc.label }}</span>
                </label>
                <template v-if="qtShowMoreFilters">
                  <label v-for="fc in QT_FILTER_CRITERIA_MORE.filter(f => !qtFilterCriteriaSearch.trim() || f.label.toLocaleLowerCase('vi').includes(qtFilterCriteriaSearch.trim().toLocaleLowerCase('vi')))" :key="fc.key" class="ofp-crit-item">
                    <input type="checkbox"
                      :checked="quotationsEnabledFilters.includes(fc.field)"
                      @change="toggleQuotationsFilter(fc.field)"
                      class="ofp-crit-chk">
                    <span>{{ fc.label }}</span>
                  </label>
                </template>
                <button type="button" class="ofp-show-more" @click="qtShowMoreFilters = !qtShowMoreFilters">{{ qtShowMoreFilters ? 'Thu gọn' : 'Xem thêm' }}</button>
              </div>
              <div v-if="quotationsEnabledFilters.length" class="ofp-section">
                <div class="ofp-section-title">GIÁ TRỊ LỌC</div>
                <div v-for="field in quotationsEnabledFilters" :key="field" class="ofp-filter-row">
                  <label class="ofp-filter-label">{{ [...QT_FILTER_CRITERIA, ...QT_FILTER_CRITERIA_MORE].find(f=>f.field===field)?.label }}</label>
                  <template v-if="field === 'status'">
                    <select v-model="quotationsFilterValues[field]" @change="loadRows" class="ofp-filter-sel">
                      <option value="">Tất cả</option>
                      <option>Draft</option><option>Open</option>
                      <option>Ordered</option><option>Expired</option>
                      <option>Lost</option><option>Cancelled</option>
                    </select>
                  </template>
                  <template v-else-if="['transaction_date','valid_till','modified'].includes(field)">
                    <input type="date" v-model="quotationsFilterValues[field]" @change="loadRows" class="ofp-filter-inp">
                  </template>
                  <template v-else>
                    <input v-model="quotationsFilterValues[field]" @keyup.enter="loadRows" class="ofp-filter-inp" placeholder="Lọc...">
                  </template>
                </div>
              </div>
            </div>
          </aside>
          </div>

          <teleport to="body"><div v-if="quotationColumnDialogOpen" class="column-dialog-backdrop" @click.self="cancelQuotationColumnDialog">
            <section class="column-dialog">
              <header><h2>Tùy chỉnh cột</h2><button data-tooltip="Đóng" @click="cancelQuotationColumnDialog">×</button></header>
              <div class="column-dialog-body">
                <section class="column-picker">
                  <label class="column-search"><CRMIcon name="search" /><input v-model="quotationColumnSearch" placeholder="Tìm kiếm cột"></label>
                  <strong>Chọn trường</strong>
                  <div class="column-picker-list">
                    <label v-for="column in filteredQuotationColumns" :key="column.field">
                      <input type="checkbox" :checked="quotationColumnDraft.includes(column.field)" @change="toggleQuotationDraftColumn(column.field)">
                      <span>{{ column.label }}</span>
                    </label>
                    <p v-if="!filteredQuotationColumns.length" class="crm-empty">Không tìm thấy cột phù hợp.</p>
                  </div>
                </section>
                <section class="selected-columns">
                  <header><strong>Đã chọn ({{ selectedQuotationColumns.length }})</strong><button @click="quotationColumnDraft = []">Xóa tất cả</button></header>
                  <div>
                    <article v-for="column in selectedQuotationColumns" :key="column.field">
                      <span>{{ column.label }}</span><button :aria-label="'Bỏ cột ' + column.label" @click="removeQuotationDraftColumn(column.field)">×</button>
                    </article>
                    <p v-if="!selectedQuotationColumns.length" class="crm-empty">Chưa chọn cột nào.</p>
                  </div>
                </section>
              </div>
              <footer>
                <button class="column-default" @click="resetQuotationDraftColumns">Mặc định</button>
                <div><button class="crm-button" @click="cancelQuotationColumnDialog">Hủy</button><button class="crm-button primary" @click="saveQuotationColumns">Lưu</button></div>
              </footer>
            </section>
          </div></teleport>
        </main>
`;
