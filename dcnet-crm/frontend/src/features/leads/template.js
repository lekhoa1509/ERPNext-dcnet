export default `

        <main v-else-if="route === 'lead-detail'" class="lead-detail-page misa-lead-page">
          <div v-if="loading" class="crm-empty misa-lead-loading">Đang tải...</div>
          <template v-else-if="leadDetail">
            <header class="misa-lead-header">
              <div class="misa-lead-titlebar">
                <button class="misa-back-button" @click="backToLeads" aria-label="Quay lại Tiềm năng">‹</button>
                <div class="misa-lead-avatar">{{ (leadDetail.document.lead_name || leadDetailName || 'T').charAt(0).toUpperCase() }}</div>
                <div class="misa-lead-title">
                  <div>
                    <h1>{{ leadDetail.document.lead_name || leadDetailName }}</h1>
                  </div>
                  <button class="misa-add-tag" type="button" @click="addLeadTag"><CRMIcon name="tag" /> Thêm thẻ</button>
                </div>
              </div>
              <div class="lead-detail-actions" v-if="leadDetail">
                <template v-if="leadDetailEditing">
                  <button class="crm-button" @click="cancelLeadEdit" :disabled="leadDetailSaving">Hủy</button>
                  <button class="crm-button primary" @click="saveLeadDetailEdit" :disabled="leadDetailSaving">{{ leadDetailSaving ? 'Đang lưu...' : 'Lưu' }}</button>
                </template>
                <template v-else>
                  <button class="crm-button" @click="openLeadForm(leadDetail.document)">Sửa</button>
                  <details class="crm-detail-more">
                    <summary class="icon-button" data-tooltip="Thêm thao tác" aria-label="Thêm thao tác"><CRMIcon name="more" /></summary>
                    <div class="crm-detail-more-menu" role="menu">
                      <button v-if="leadDetail.document.status !== 'Converted'" type="button" role="menuitem" @click="convertLead(); $event.currentTarget.closest('details').removeAttribute('open')"><CRMIcon name="handoff" /><span>Chuyển đổi tiềm năng</span></button>
                      <div class="crm-detail-more-separator"></div>
                      <button type="button" role="menuitem" @click="openAuditLog('Lead', leadDetail.document.name); $event.currentTarget.closest('details').removeAttribute('open')"><CRMIcon name="history" /><span>Nhật ký</span></button>
                    </div>
                  </details>
                </template>
              </div>
            </header>

            <section class="misa-lead-summary">
              <div><span>Chức danh</span><strong>{{ leadDetail.document.job_title || '- Không chọn -' }}</strong></div>
              <div><span>ĐT di động</span><strong>{{ leadDetail.document.mobile_no || '—' }}</strong></div>
              <div><span>Email cơ quan</span><strong>{{ leadDetail.document.custom_work_email || '—' }}</strong></div>
              <div><span>ĐT cơ quan</span><strong>{{ leadDetail.document.phone || '—' }}</strong></div>
            </section>

            <nav class="misa-lead-tabs" aria-label="Tiềm năng" role="tablist">
              <button
                v-for="tab in LEAD_DETAIL_TABS"
                :key="tab.key"
                :class="{ active: leadDetailTab === tab.key }"
                :aria-selected="leadDetailTab === tab.key"
                role="tab"
                type="button"
                @click="setLeadDetailTab(tab.key)"
              >{{ tab.label }}<b v-if="leadDetailTabBadge(tab.key)" class="misa-tab-badge">{{ leadDetailTabBadge(tab.key) }}</b></button>
            </nav>

            <div class="misa-lead-shell">
              <section class="misa-lead-card">
                <template v-if="leadDetailTab === 'detail'">
                  <div class="misa-lead-tools">
                    <label class="misa-field-search"><CRMIcon name="search" /><input v-model="leadDetailFieldSearch" type="search" placeholder="Tìm kiếm trường"></label>
                    <label class="misa-toggle"><input v-model="leadShowEmpty" type="checkbox"><span></span>Hiển thị dữ liệu trống</label>
                  </div>

                  <section class="misa-detail-section">
                  <h2>Thông tin chung</h2>
                  <div class="lead-form-grid misa-field-grid">
                    <div v-show="showLeadDetailField('Xưng hô', leadDetail.document.salutation)" class="lead-form-field"><span>Xưng hô</span><span>{{ leadDetail.document.salutation || '- Không chọn -' }}</span></div>
                    <div v-show="showLeadDetailField('Họ và đệm', leadDetail.document.last_name)" class="lead-form-field"><span>Họ và đệm</span><span>{{ leadDetail.document.last_name || '—' }}</span></div>
                    <div v-show="showLeadDetailField('Tên', leadDetail.document.first_name)" class="lead-form-field"><span>Tên</span><strong>{{ leadDetail.document.first_name || '—' }}</strong></div>
                    <div v-show="showLeadDetailField('Họ và tên', leadDetail.document.lead_name)" class="lead-form-field"><span>Họ và tên</span><strong>{{ leadDetail.document.lead_name || '—' }}</strong></div>
                    <div v-show="showLeadDetailField('Phòng ban', leadDetail.document.department)" class="lead-form-field"><span>Phòng ban</span><span>{{ leadDetail.document.department || '- Không chọn -' }}</span></div>
                    <div v-show="showLeadDetailField('Chức danh', leadDetail.document.job_title)" class="lead-form-field"><span>Chức danh</span><span>{{ leadDetail.document.job_title || '- Không chọn -' }}</span></div>
                    <div v-show="showLeadDetailField('ĐT di động', leadDetail.document.mobile_no)" class="lead-form-field"><span>ĐT di động</span><strong>{{ leadDetail.document.mobile_no || '—' }}</strong></div>
                    <div v-show="showLeadDetailField('ĐT cơ quan', leadDetail.document.phone)" class="lead-form-field"><span>ĐT cơ quan</span><span>{{ leadDetail.document.phone || '—' }}</span></div>
                    <div v-show="showLeadDetailField('Điện thoại khác', leadDetail.document.custom_other_phone)" class="lead-form-field"><span>Điện thoại khác</span><span>{{ leadDetail.document.custom_other_phone || '—' }}</span></div>
                    <div v-show="showLeadDetailField('Loại tiềm năng', leadDetail.document.custom_lead_type)" class="lead-form-field"><span>Loại tiềm năng</span><strong class="misa-lead-type-value">{{ leadDetail.document.custom_lead_type || '- Không chọn -' }}</strong></div>
                    <div v-show="showLeadDetailField('Nguồn gốc', leadDetail.document.source || leadDetail.document.utm_source)" class="lead-form-field"><span>Nguồn gốc</span><span>{{ leadDetail.document.source || leadDetail.document.utm_source || '- Không chọn -' }}</span></div>
                    <div v-show="showLeadDetailField('Không gọi điện', leadDetail.document.custom_do_not_call)" class="lead-form-field"><span>Không gọi điện</span><span>{{ leadDetail.document.custom_do_not_call ? 'Có' : '—' }}</span></div>
                    <div v-show="showLeadDetailField('Không gửi Email', leadDetail.document.custom_do_not_email)" class="lead-form-field"><span>Không gửi Email</span><span>{{ leadDetail.document.custom_do_not_email ? 'Có' : '—' }}</span></div>
                    <div v-show="showLeadDetailField('Email cá nhân', leadDetail.document.email_id)" class="lead-form-field"><span>Email cá nhân</span><span>{{ leadDetail.document.email_id || '—' }}</span></div>
                    <div v-show="showLeadDetailField('Zalo', leadDetail.document.custom_zalo)" class="lead-form-field"><span>Zalo</span><a v-if="leadDetail.document.custom_zalo" :href="'tel:' + leadDetail.document.custom_zalo">{{ leadDetail.document.custom_zalo }}</a><span v-else>—</span></div>
                    <div v-show="showLeadDetailField('Tổ chức', leadDetail.document.company_name)" class="lead-form-field"><span>Tổ chức</span><span>{{ leadDetail.document.company_name || '—' }}</span></div>
                    <div v-show="showLeadDetailField('Email cơ quan', leadDetail.document.custom_work_email)" class="lead-form-field"><span>Email cơ quan</span><span>{{ leadDetail.document.custom_work_email || '—' }}</span></div>
                    <div v-show="showLeadDetailField('Mã số thuế', leadDetail.document.custom_tax_id)" class="lead-form-field"><span>Mã số thuế</span><span>{{ leadDetail.document.custom_tax_id || '—' }}</span></div>
                  </div>
                  </section>

                  <section class="misa-detail-section">
                  <h2>Thông tin cá nhân</h2>
                  <div class="lead-form-grid misa-field-grid">
                    <div v-show="showLeadDetailField('Giới tính', leadDetail.document.gender)" class="lead-form-field"><span>Giới tính</span><span>{{ leadDetail.document.gender || '- Không chọn -' }}</span></div>
                    <div v-show="showLeadDetailField('Ngày sinh', leadDetail.document.custom_date_of_birth)" class="lead-form-field"><span>Ngày sinh</span><span>{{ formatValue(leadDetail.document.custom_date_of_birth, 'date') }}</span></div>
                    <div v-show="showLeadDetailField('Facebook', leadDetail.document.custom_facebook)" class="lead-form-field"><span>Facebook</span><span>{{ leadDetail.document.custom_facebook || '—' }}</span></div>
                  </div>
                  </section>

                  <section class="misa-detail-section">
                  <h2>Thông tin tổ chức</h2>
                  <div class="lead-form-grid misa-field-grid">
                    <div v-show="showLeadDetailField('Tài khoản ngân hàng', leadDetail.document.custom_bank_account)" class="lead-form-field"><span>Tài khoản ngân hàng</span><span>{{ leadDetail.document.custom_bank_account || '—' }}</span></div>
                    <div v-show="showLeadDetailField('Mở tại ngân hàng', leadDetail.document.custom_bank_name)" class="lead-form-field"><span>Mở tại ngân hàng</span><span>{{ leadDetail.document.custom_bank_name || '—' }}</span></div>
                    <div v-show="showLeadDetailField('Ngày thành lập', leadDetail.document.custom_founding_date)" class="lead-form-field"><span>Ngày thành lập</span><span>{{ formatValue(leadDetail.document.custom_founding_date, 'date') }}</span></div>
                    <div v-show="showLeadDetailField('Loại hình', leadDetail.document.custom_business_type)" class="lead-form-field"><span>Loại hình</span><span>{{ leadDetail.document.custom_business_type || '- Không chọn -' }}</span></div>
                    <div v-show="showLeadDetailField('Lĩnh vực', leadDetail.document.custom_sector)" class="lead-form-field"><span>Lĩnh vực</span><span>{{ leadDetail.document.custom_sector || '- Không chọn -' }}</span></div>
                    <div v-show="showLeadDetailField('Ngành nghề', leadDetail.document.industry)" class="lead-form-field"><span>Ngành nghề</span><span>{{ leadDetail.document.industry || '- Không chọn -' }}</span></div>
                    <div v-show="showLeadDetailField('Website', leadDetail.document.website)" class="lead-form-field"><span>Website</span><span>{{ leadDetail.document.website || '—' }}</span></div>
                  </div>
                  </section>

                  <section class="misa-detail-section">
                  <h2>Thông tin địa chỉ</h2>
                  <div class="lead-form-grid misa-field-grid">
                    <div v-show="showLeadDetailField('Quốc gia', leadDetail.document.country)" class="lead-form-field"><span>Quốc gia</span><strong>{{ leadDetail.document.country || 'Việt Nam' }}</strong></div>
                    <div v-show="showLeadDetailField('Tỉnh/Thành phố', leadDetail.document.state)" class="lead-form-field"><span>Tỉnh/Thành phố</span><span>{{ leadDetail.document.state || '- Không chọn -' }}</span></div>
                    <div v-show="showLeadDetailField('Quận/Huyện', leadDetail.document.custom_district)" class="lead-form-field"><span>Quận/Huyện</span><span>{{ leadDetail.document.custom_district || '- Không chọn -' }}</span></div>
                    <div v-show="showLeadDetailField('Phường/Xã', leadDetail.document.custom_ward)" class="lead-form-field"><span>Phường/Xã</span><span>{{ leadDetail.document.custom_ward || '- Không chọn -' }}</span></div>
                    <div v-show="showLeadDetailField('Số nhà, Đường phố', leadDetail.document.address_line1)" class="lead-form-field"><span>Số nhà, Đường phố</span><span>{{ leadDetail.document.address_line1 || '—' }}</span></div>
                    <div v-show="showLeadDetailField('Mã vùng', leadDetail.document.pincode)" class="lead-form-field"><span>Mã vùng</span><span>{{ leadDetail.document.pincode || '—' }}</span></div>
                    <div v-show="showLeadDetailField('Địa chỉ', leadDetail.document.custom_full_address)" class="lead-form-field"><span>Địa chỉ</span><span>{{ leadDetail.document.custom_full_address || '—' }}</span></div>
                    <div v-show="showLeadDetailField('Vị trí cắm mốc', leadDetail.document.custom_marker_location)" class="lead-form-field"><span></span><a v-if="leadDetail.document.custom_marker_location" :href="leadDetail.document.custom_marker_location" target="_blank" rel="noopener">Vị trí cắm mốc</a><span v-else class="misa-placeholder-link">Vị trí cắm mốc</span></div>
                  </div>
                  </section>

                  <section class="misa-detail-section">
                  <h2>Thông tin mô tả</h2>
                  <div v-show="showLeadDetailField('Mô tả', leadDetail.document.notes)" class="lead-form-field lead-form-field-full misa-description"><span>Mô tả</span><span class="lead-notes">{{ stripHtml(leadDetail.document.notes || '') || '—' }}</span></div>
                  </section>

                  <section class="misa-detail-section">
                  <h2>Thông tin hệ thống</h2>
                  <div class="lead-form-grid misa-field-grid">
                    <div v-show="showLeadDetailField('Chủ sở hữu', leadDetail.document.lead_owner || leadDetail.document.owner)" class="lead-form-field"><span>Chủ sở hữu</span><a href="#" @click.prevent>{{ leadDetail.document.lead_owner || leadDetail.document.owner || '—' }}</a></div>
                    <div v-show="showLeadDetailField('Đơn vị', leadDetail.document.custom_branch)" class="lead-form-field"><span>Đơn vị</span><strong>{{ leadDetail.document.custom_branch || '—' }}</strong></div>
                    <div v-show="showLeadDetailField('Người tạo', leadDetail.document.owner)" class="lead-form-field"><span>Người tạo</span><span>{{ leadDetail.document.owner || '—' }}</span></div>
                    <div v-show="showLeadDetailField('Ngày tạo', leadDetail.document.creation)" class="lead-form-field"><span>Ngày tạo</span><span>{{ formatValue(leadDetail.document.creation, 'creation') }}</span></div>
                    <div v-show="showLeadDetailField('Người sửa', leadDetail.document.modified_by)" class="lead-form-field"><span>Người sửa</span><span>{{ leadDetail.document.modified_by || '—' }}</span></div>
                    <div v-show="showLeadDetailField('Ngày sửa', leadDetail.document.modified)" class="lead-form-field"><span>Ngày sửa</span><span>{{ formatValue(leadDetail.document.modified, 'modified') }}</span></div>
                    <div v-show="showLeadDetailField('Dùng chung', leadDetail.document.custom_is_shared)" class="lead-form-field"><span>Dùng chung</span><span>{{ leadDetail.document.custom_is_shared ? 'Có' : 'Không' }}</span></div>
                    <div v-show="showLeadDetailField('Bố cục', leadDetail.document.custom_layout)" class="lead-form-field"><span>Bố cục</span><span>{{ leadDetail.document.custom_layout || 'Mẫu tiêu chuẩn' }}</span></div>
                    <div v-show="showLeadDetailField('Mã tiềm năng', leadDetail.document.name)" class="lead-form-field"><span>Mã tiềm năng</span><strong>{{ leadDetail.document.name }}</strong></div>
                    <div v-show="showLeadDetailField('Ngừng theo dõi', leadDetail.document.disabled)" class="lead-form-field"><span>Ngừng theo dõi</span><span>{{ leadDetail.document.disabled ? 'Có' : '—' }}</span></div>
                    <div v-show="showLeadDetailField('Ngày tương tác gần nhất', leadDetail.document.custom_last_interaction_date)" class="lead-form-field"><span>Ngày tương tác gần nhất</span><span>{{ formatValue(leadDetail.document.custom_last_interaction_date, 'date') }}</span></div>
                    <div v-show="showLeadDetailField('Số ngày chưa tương tác', leadDetail.document.custom_inactive_days)" class="lead-form-field"><span>Số ngày chưa tương tác</span><span>{{ leadDetail.document.custom_inactive_days || 0 }}</span></div>
                    <div v-show="showLeadDetailField('Ngày ghé thăm gần nhất', leadDetail.document.custom_last_visit_date)" class="lead-form-field"><span>Ngày ghé thăm gần nhất</span><span>{{ formatValue(leadDetail.document.custom_last_visit_date, 'date') }}</span></div>
                    <div v-show="showLeadDetailField('Ngày cuộc gọi gần nhất', leadDetail.document.custom_last_call_date)" class="lead-form-field"><span>Ngày cuộc gọi gần nhất</span><span>{{ formatValue(leadDetail.document.custom_last_call_date, 'date') }}</span></div>
                    <div v-show="showLeadDetailField('Người liên quan', leadDetail.document.custom_related_person)" class="lead-form-field"><span>Người liên quan</span><span>{{ leadDetail.document.custom_related_person || '—' }}</span></div>
                  </div>
                  </section>
                </template>

                <section v-else-if="leadDetailTab === 'notes'" class="misa-tab-panel misa-notes-panel">
                  <div class="misa-related-card misa-notes-card">
                    <div class="misa-related-head">
                      <h2>Ghi chú</h2>
                      <button v-if="showUnreadyFeatures" class="misa-icon-link" type="button" @click="notifyLeadTabAction('Thu gọn ghi chú')"><CRMIcon name="chevron" /></button>
                    </div>
                    <div class="misa-note-feed-box">
                      <textarea v-model="note" placeholder="Thêm ghi chú"></textarea>
                      <button class="misa-send-note" :disabled="!note.trim()" @click="addNote">Lưu ghi chú</button>
                    </div>
                    <article v-if="leadDetail.document.notes" class="misa-note-item">
                      <div class="misa-note-avatar">{{ (boot?.full_name || boot?.user || 'A').charAt(0).toUpperCase() }}</div>
                      <div class="misa-note-body">
                        <strong>{{ boot?.full_name || boot?.user || 'Administrator' }}</strong>
                        <p>{{ leadDetail.document.notes }}</p>
                        <small>Tiềm năng · vừa xong</small>
                      </div>
                      <div class="misa-note-actions">
                        <button v-if="showUnreadyFeatures" type="button" @click="notifyLeadTabAction('Sửa ghi chú')"><CRMIcon name="edit" /></button>
                        <button v-if="showUnreadyFeatures" type="button" @click="notifyLeadTabAction('Xóa ghi chú')">×</button>
                      </div>
                    </article>
                    <div v-else class="misa-inline-empty">Không có bản ghi nào</div>
                  </div>
                </section>

                <section v-else-if="leadDetailTab === 'attachments'" class="misa-tab-panel">
                  <div class="misa-related-card">
                    <div class="misa-related-head">
                      <h2>Tài liệu đính kèm <button type="button" @click="loadLeadDetail()"><CRMIcon name="refresh" /></button></h2>
                      <div v-if="leadDetail.can_write" class="misa-related-actions">
                        <button type="button" @click="addLeadAttachmentLink"><CRMIcon name="link" /> Thêm liên kết</button>
                        <button type="button" :disabled="leadAttachmentUploading" @click="$refs.leadAttachmentInput.click()"><CRMIcon name="paperclip" /> {{ leadAttachmentUploading ? 'Đang tải...' : 'Thêm tệp' }}</button>
                        <input ref="leadAttachmentInput" type="file" hidden @change="uploadLeadAttachment">
                      </div>
                    </div>
                    <table class="misa-related-table">
                      <thead><tr><th>Tên tài liệu</th><th>Người đính kèm</th><th>Ngày đính kèm</th><th>Dung lượng</th></tr></thead>
                      <tbody v-if="leadDetail.attachments && leadDetail.attachments.length">
                        <tr v-for="file in leadDetail.attachments" :key="file.name">
                          <td><a class="misa-attachment-link" :href="file.file_url" target="_blank" rel="noopener"><CRMIcon :name="leadAttachmentIcon(file)" /> <span>{{ file.file_name || file.file_url }}</span></a></td>
                          <td>{{ file.owner || '—' }}</td>
                          <td>{{ formatValue(file.creation, 'creation') }}</td>
                          <td>{{ formatFileSize(file.file_size) }}</td>
                        </tr>
                      </tbody>
                    </table>
                    <div v-if="!leadDetail.attachments || !leadDetail.attachments.length" class="misa-table-empty">
                      <CRMIcon name="quotation" />
                      <span>Không có bản ghi nào</span>
                    </div>
                  </div>
                </section>

                <section v-else-if="leadDetailTab === 'interested_items'" class="misa-tab-panel">
                  <div class="misa-related-card">
                    <div class="misa-related-head">
                      <h2>Hàng hóa quan tâm <button type="button" @click="loadLeadDetail()"><CRMIcon name="refresh" /></button></h2>
                      <div class="misa-related-actions"><button type="button" @click="openLeadItemPicker">☑ Chọn</button></div>
                    </div>
                    <table class="misa-related-table">
                      <thead><tr><th>Mã hàng hóa</th><th>Tên hàng hóa</th><th>Loại hàng hóa</th><th>Đơn vị tính</th></tr></thead>
                      <tbody v-if="leadInterestedItems.length">
                        <tr v-for="item in leadInterestedItems" :key="item.item_code">
                          <td><a href="#" @click.prevent>{{ item.item_code }}</a></td>
                          <td><a href="#" @click.prevent>{{ item.item_name }}</a></td>
                          <td><a href="#" @click.prevent>{{ item.item_group }}</a></td>
                          <td>{{ item.uom }}</td>
                        </tr>
                      </tbody>
                    </table>
                    <footer class="misa-table-footer"><strong>Tổng số {{ leadInterestedItems.length }}</strong><span>Số dòng/trang <b>20</b> · 1 - {{ leadInterestedItems.length || 1 }}</span></footer>
                    <div v-if="!leadInterestedItems.length" class="misa-table-empty">
                      <CRMIcon name="package" />
                      <span>Không có bản ghi nào</span>
                    </div>
                  </div>
                </section>

                <section v-else-if="leadDetailTab === 'campaigns'" class="misa-tab-panel">
                  <div class="misa-related-card">
                    <div class="misa-related-head"><h2>Chiến dịch <button type="button" @click="loadLeadDetail()"><CRMIcon name="refresh" /></button></h2></div>
                    <div class="misa-inline-empty">Không có bản ghi nào <template v-if="showUnreadyFeatures"><button v-if="showUnreadyFeatures" type="button" @click="notifyLeadTabAction('Thêm chiến dịch')">＋ Thêm</button><button v-if="showUnreadyFeatures" type="button" @click="notifyLeadTabAction('Chọn chiến dịch')">☑ Chọn</button></template></div>
                  </div>
                </section>

                <section v-else-if="leadDetailTab === 'email' || leadDetailTab === 'sms' || leadDetailTab === 'aimarketing'" class="misa-tab-panel">
                  <div class="misa-related-card">
                    <div class="misa-related-head">
                      <h2>{{ leadDetailTabLabel(leadDetailTab) }} <button type="button" @click="loadLeadDetail()"><CRMIcon name="refresh" /></button></h2>
                      <div v-if="showUnreadyFeatures" class="misa-related-actions"><button v-if="showUnreadyFeatures" type="button" @click="notifyLeadTabAction('Tạo ' + leadDetailTabLabel(leadDetailTab))">＋ Thêm</button></div>
                    </div>
                    <div class="misa-inline-empty">Không có bản ghi nào</div>
                  </div>
                </section>

                <section v-else-if="leadDetailTab === 'active_tasks'" class="misa-tab-panel">
                  <div class="misa-related-card">
                    <div class="misa-related-head">
                      <h2>Công việc đang thực hiện <button type="button" @click="loadLeadDetail()"><CRMIcon name="refresh" /></button></h2>
                      <div v-if="leadDetail.can_create_activity" class="misa-related-actions">
                        <button type="button" @click="openLeadActivityDialog('task')"><CRMIcon name="task" /> Thêm Nhiệm vụ</button>
                        <button type="button" @click="openLeadActivityDialog('meeting')"><CRMIcon name="calendar" /> Thêm Lịch hẹn</button>
                        <button type="button" @click="openLeadActivityDialog('call')"><CRMIcon name="phone" /> Thêm Cuộc gọi</button>
                      </div>
                    </div>
                    <div class="misa-activity-table-wrap" v-if="leadActiveActivities.length">
                      <table class="misa-related-table misa-activity-table">
                        <thead><tr><th>Tên hoạt động</th><th>Loại hoạt động</th><th>Hạn hoàn thành</th><th>Trạng thái</th><th>Ngày kết thúc</th><th>Người thực hiện</th></tr></thead>
                        <tbody><tr v-for="activity in leadActiveActivities" :key="activity.activity_type + '-' + activity.name">
                          <td><a href="#" @click.prevent="openActivityRecord(activity.name, activity.activity_type === 'task' ? 'ToDo' : 'Event')">{{ activity.subject || activity.name }}</a></td>
                          <td>{{ leadActivityTypeLabel(activity.activity_type) }}</td>
                          <td>{{ formatLeadActivityDate(activity.activity_type === 'task' ? activity.due_date : activity.starts_on) }}</td>
                          <td><span class="misa-activity-status" :class="'status-' + String(activity.status || '').toLowerCase()">{{ leadActivityStatusLabel(activity.status) }}</span></td>
                          <td>{{ formatLeadActivityDate(activity.ends_on) }}</td>
                          <td><a href="#" @click.prevent>{{ activity.performed_by_name || activity.performed_by || '—' }}</a></td>
                        </tr></tbody>
                      </table>
                    </div>
                    <div v-else class="misa-table-empty misa-activity-empty"><CRMIcon name="task" /><span>Không có bản ghi nào</span></div>
                    <footer class="misa-activity-footer"><strong>Tổng số {{ leadActiveActivities.length }}</strong></footer>
                  </div>
                </section>

                <section v-else-if="leadDetailTab === 'done_tasks'" class="misa-tab-panel">
                  <div class="misa-related-card">
                    <div class="misa-related-head"><h2>Công việc đã hoàn thành <button type="button" @click="loadLeadDetail()"><CRMIcon name="refresh" /></button></h2></div>
                    <div class="misa-activity-table-wrap" v-if="leadDoneActivities.length">
                      <table class="misa-related-table misa-activity-table">
                        <thead><tr><th>Tên hoạt động</th><th>Loại hoạt động</th><th>Hạn hoàn thành</th><th>Trạng thái</th><th>Ngày kết thúc</th><th>Người thực hiện</th></tr></thead>
                        <tbody><tr v-for="activity in leadDoneActivities" :key="activity.activity_type + '-' + activity.name">
                          <td><a href="#" @click.prevent="openActivityRecord(activity.name, activity.activity_type === 'task' ? 'ToDo' : 'Event')">{{ activity.subject || activity.name }}</a></td>
                          <td>{{ leadActivityTypeLabel(activity.activity_type) }}</td>
                          <td>{{ formatLeadActivityDate(activity.activity_type === 'task' ? activity.due_date : activity.starts_on) }}</td>
                          <td><span class="misa-activity-status" :class="'status-' + String(activity.status || '').toLowerCase()">{{ leadActivityStatusLabel(activity.status) }}</span></td>
                          <td>{{ formatLeadActivityDate(activity.ends_on) }}</td>
                          <td><a href="#" @click.prevent>{{ activity.performed_by_name || activity.performed_by || '—' }}</a></td>
                        </tr></tbody>
                      </table>
                    </div>
                    <div v-else class="misa-table-empty misa-activity-empty"><CRMIcon name="task" /><span>Không có bản ghi nào</span></div>
                    <footer class="misa-activity-footer"><strong>Tổng số {{ leadDoneActivities.length }}</strong></footer>
                  </div>
                </section>

                <section v-else-if="leadDetailTab === 'routes'" class="misa-tab-panel">
                  <div class="misa-related-card">
                    <div class="misa-related-head"><h2>Lộ trình di chuyển <button type="button" @click="loadLeadDetail()"><CRMIcon name="refresh" /></button></h2></div>
                    <div class="misa-inline-empty">Không có bản ghi nào <button v-if="showUnreadyFeatures" type="button" @click="notifyLeadTabAction('Chọn lộ trình')">☑ Chọn</button></div>
                  </div>
                </section>

                <section v-else-if="leadDetailTab === 'conversations'" class="misa-tab-panel">
                  <div class="customer-conversation-shell">
                    <header class="customer-conversation-heading">
                      <div><h2>Trao đổi</h2><p>Theo dõi và cập nhật nội dung trao đổi về tiềm năng này.</p></div>
                      <span>{{ (leadDetail.comments || []).length }} bình luận</span>
                    </header>
                    <div v-if="(leadDetail.comments || []).length" class="customer-comment-feed">
                      <article v-for="c in leadDetail.comments" :key="c.name" class="customer-comment">
                        <span class="customer-comment-avatar" aria-hidden="true">{{ (c.comment_by_fullname || c.comment_by || 'CRM').slice(0, 1).toUpperCase() }}</span>
                        <div class="customer-comment-content">
                          <div class="customer-comment-meta"><strong>{{ c.comment_by_fullname || c.comment_by }}</strong><time>{{ formatValue(c.creation, 'creation') }}</time></div>
                          <div class="customer-comment-bubble"><p>{{ stripHtml(c.content || '') }}</p></div>
                        </div>
                      </article>
                    </div>
                    <div v-else class="customer-conversation-empty"><CRMIcon name="message" /><strong>Chưa có nội dung trao đổi</strong><span>Hãy bắt đầu bằng bình luận đầu tiên về tiềm năng này.</span></div>
                    <div class="customer-comment-composer">
                      <span class="customer-comment-avatar current" aria-hidden="true">{{ (boot?.full_name || boot?.user || 'CRM').slice(0, 1).toUpperCase() }}</span>
                      <div class="customer-comment-editor">
                        <textarea v-model="note" rows="3" aria-label="Nội dung trao đổi" placeholder="Viết bình luận..." @keydown.ctrl.enter.prevent="addNote"></textarea>
                        <div class="customer-comment-actions">
                          <button type="button" data-tooltip="Mở tài liệu đính kèm" @click="leadDetailTab = 'attachments'"><CRMIcon name="package" /> Đính kèm</button>
                          <span>Ctrl + Enter để gửi</span>
                          <button type="button" class="crm-button primary" :disabled="!note.trim()" @click="addNote"><CRMIcon name="send" /> Gửi</button>
                        </div>
                      </div>
                    </div>
                  </div>
                </section>
              </section>

              <aside class="misa-lead-rail">
                <div class="misa-rail-actions">
                  <button data-tooltip="Gọi điện" type="button" @click="openLeadActivityDialog('call')"><CRMIcon name="phone" /></button>
                  <button data-tooltip="Công việc" type="button" @click="openLeadActivityDialog('task')"><CRMIcon name="task" /></button>
                  <button data-tooltip="Lịch" type="button" @click="openLeadActivityDialog('meeting')"><CRMIcon name="calendar" /></button>
                  <button data-tooltip="Email" type="button" @click="emailLead"><CRMIcon name="email" /></button>
                  <button data-tooltip="Nội dung trao đổi" type="button" @click="leadDetailTab = 'conversations'"><CRMIcon name="message" /></button>
                  <button data-tooltip="Cuộc gọi" type="button" @click="openLeadActivityDialog('call')"><CRMIcon name="phone" /></button>
                </div>
                <section class="misa-rail-section">
                  <h2>Lịch sử giao dịch</h2>
                  <div class="misa-rail-empty" v-if="!(leadDetail.timeline || []).length">
                    <CRMIcon name="task" />
                    <p>Không có dữ liệu</p>
                  </div>
                  <div class="crm-timeline misa-rail-timeline" v-else>
                    <article v-for="item in leadDetail.timeline || []" :key="item.activity_type + '-' + item.name">
                      <i :class="'activity-' + item.activity_type"><CRMIcon :name="item.activity_type === 'call' ? 'phone' : item.activity_type === 'meeting' ? 'calendar' : item.activity_type === 'task' ? 'task' : item.activity_type === 'communication' ? 'email' : 'message'" /></i>
                      <div>
                        <strong>{{ ['task', 'meeting', 'call'].includes(item.activity_type) ? (item.subject || item.name) : stripHtml(item.subject || item.content || 'Hoạt động') }}</strong>
                        <p v-if="item.description && item.description !== item.subject">{{ stripHtml(item.description) }}</p>
                        <small>{{ item.performed_by_name || item.performed_by || item.allocated_to || item.sender || leadDetail.document.lead_owner || '—' }} · {{ formatLeadActivityDate(item.creation) }}</small>
                      </div>
                    </article>
                  </div>
                </section>
              </aside>
            </div>

            <div v-if="leadItemPickerOpen" class="misa-picker-overlay">
              <div class="misa-picker-modal">
                <header class="misa-picker-head">
                  <h2>Chọn hàng hóa</h2>
                  <button type="button" @click="closeLeadItemPicker">×</button>
                </header>
                <div class="misa-picker-tools">
                  <label class="misa-field-search"><CRMIcon name="search" /><input v-model="leadItemPickerSearch" placeholder="Tìm kiếm" @input="leadItemPickerPage = 1"></label>
                  <button v-if="showUnreadyFeatures" class="crm-button primary" type="button" @click="notifyLeadTabAction('Thêm hàng hóa')">＋ Thêm hàng hóa</button>
                </div>
                <div class="misa-picker-tablewrap">
                  <table class="misa-related-table misa-picker-table">
                    <thead><tr><th><input type="checkbox" aria-label="Chọn tất cả trang này" @change="toggleLeadItemPickerPage($event.target.checked)"></th><th>Mã hàng hóa</th><th>Tên hàng hóa</th><th>Loại hàng hóa</th><th>Đơn vị tính</th><th>Thuế GTGT</th></tr></thead>
                    <tbody>
                      <tr v-for="item in leadItemPickerRows" :key="item.name" @click="toggleLeadItemPicker(item.name)">
                        <td><input type="checkbox" :checked="leadItemPickerSelected.includes(item.name)" @click.stop="toggleLeadItemPicker(item.name)"></td>
                        <td>{{ item.name }}</td>
                        <td>{{ item.item_name || item.name }}</td>
                        <td><a href="#" @click.prevent>{{ item.item_group || '—' }}</a></td>
                        <td>{{ item.stock_uom || '—' }}</td>
                        <td>—</td>
                      </tr>
                    </tbody>
                  </table>
                  <div v-if="!leadItemPickerRows.length" class="misa-table-empty"><CRMIcon name="package" /><span>Không có bản ghi nào</span></div>
                </div>
                <footer class="misa-picker-footer">
                  <strong>Tổng số {{ leadItemPickerFiltered.length.toLocaleString('vi-VN') }}</strong>
                  <div>
                    <span>Số dòng/trang</span>
                    <select v-model.number="leadItemPickerPageLength" @change="leadItemPickerPage = 1"><option :value="20">20</option><option :value="50">50</option></select>
                    <span>{{ leadItemPickerPage }} - {{ leadItemPickerPageCount }}</span>
                    <button class="misa-page-button" type="button" :disabled="leadItemPickerPage <= 1" @click="changeLeadItemPickerPage(-1)">‹</button>
                    <button class="misa-page-button" type="button" :disabled="leadItemPickerPage >= leadItemPickerPageCount" @click="changeLeadItemPickerPage(1)">›</button>
                  </div>
                  <button class="crm-button" type="button" @click="closeLeadItemPicker">Hủy</button>
                  <button class="crm-button primary" type="button" :disabled="!leadItemPickerSelected.length" @click="confirmLeadItemPicker">Tiếp theo</button>
                </footer>
              </div>
            </div>

            <div v-if="leadActivityDialogOpen" class="crm-modal-backdrop misa-activity-backdrop" @click.self="closeLeadActivityDialog">
              <form class="crm-modal misa-activity-modal" @submit.prevent="saveLeadActivity">
                <header>
                  <h2>Thêm {{ leadActivityTypeLabel(leadActivityForm.activity_type).toLowerCase() }}</h2>
                  <div><button type="button" data-tooltip="Đóng" aria-label="Đóng" @click="closeLeadActivityDialog">×</button></div>
                </header>
                <div class="misa-activity-form">
                  <label><span>Tiêu đề <b>*</b></span><input v-model="leadActivityForm.subject" required autofocus></label>
                  <label><span>Mô tả</span><textarea v-model="leadActivityForm.description"></textarea></label>

                  <label v-if="leadActivityMoreOpen && leadActivityForm.activity_type === 'call'"><span>Điện thoại</span><input v-model="leadActivityForm.phone" type="tel"></label>
                  <template v-if="leadActivityMoreOpen">
                    <label><span>Tiềm năng</span><input :value="leadDetail.document.lead_name || leadDetail.document.name" readonly></label>
                    <label><span>Chiến dịch</span><select v-model="leadActivityForm.campaign"><option value="">- Không chọn -</option><option v-for="campaign in leadDetail.activity_campaigns || []" :key="campaign.name" :value="campaign.name">{{ campaign.name }}</option></select></label>
                    <label><span>Người thực hiện</span><select v-model="leadActivityForm.allocated_to"><option v-for="user in leadDetail.activity_users || []" :key="user.name" :value="user.name">{{ user.full_name || user.name }}</option></select></label>
                    <label><span>Người liên quan</span><select v-model="leadActivityForm.related_to"><option value="">- Không chọn -</option><option v-for="user in leadDetail.activity_users || []" :key="'related-' + user.name" :value="user.name">{{ user.full_name || user.name }}</option></select></label>
                  </template>

                  <template v-if="leadActivityForm.activity_type === 'meeting'">
                    <label><span>Địa điểm</span><input v-model="leadActivityForm.location"></label>
                    <label class="misa-activity-check"><span>Cả ngày</span><input v-model.number="leadActivityForm.all_day" type="checkbox" :true-value="1" :false-value="0"></label>
                    <label><span>Ngày bắt đầu <b>*</b></span><input v-model="leadActivityForm.starts_on" type="datetime-local" required></label>
                    <label><span>Ngày kết thúc <b>*</b></span><input v-model="leadActivityForm.ends_on" type="datetime-local" required></label>
                    <label><span>Trạng thái <b>*</b></span><select v-model="leadActivityForm.status"><option value="Open">Chưa bắt đầu</option><option value="Closed">Hoàn thành</option><option value="Cancelled">Đã hủy</option></select></label>
                  </template>

                  <template v-else-if="leadActivityForm.activity_type === 'task'">
                    <label><span>Hạn hoàn thành</span><span class="misa-activity-date-pair"><input v-model="leadActivityForm.due_date" type="date"><input v-model="leadActivityForm.due_time" type="time"></span></label>
                    <label v-if="leadActivityMoreOpen"><span>Mức độ ưu tiên <b>*</b></span><select v-model="leadActivityForm.priority"><option value="Medium">Không xác định</option><option value="High">Cao</option><option value="Low">Thấp</option></select></label>
                    <label><span>Trạng thái <b>*</b></span><select v-model="leadActivityForm.status"><option value="Open">Chưa bắt đầu</option><option value="Closed">Hoàn thành</option><option value="Cancelled">Đã hủy</option></select></label>
                    <label v-if="leadActivityMoreOpen"><span>Loại nhiệm vụ</span><select v-model="leadActivityForm.task_type"><option value="">- Không chọn -</option><option value="Chăm sóc khách hàng">Chăm sóc khách hàng</option><option value="Theo dõi tiềm năng">Theo dõi tiềm năng</option><option value="Gọi xác nhận">Gọi xác nhận</option><option value="Khác">Khác</option></select></label>
                  </template>

                  <template v-else>
                    <label><span>Ngày bắt đầu <b>*</b></span><input v-model="leadActivityForm.starts_on" type="datetime-local" required @input="updateLeadCallEnd"></label>
                    <label><span>Thời gian gọi <b>*</b></span><span class="misa-call-duration"><input v-model.number="leadActivityForm.call_minutes" min="0" type="number" @input="updateLeadCallEnd"><small>Phút</small><input v-model.number="leadActivityForm.call_seconds" min="0" max="59" type="number" @input="updateLeadCallEnd"><small>Giây</small></span></label>
                    <label><span>Ngày kết thúc <b>*</b></span><input :value="leadActivityForm.ends_on" type="datetime-local" readonly></label>
                    <label v-if="leadActivityMoreOpen"><span>Loại cuộc gọi <b>*</b></span><select v-model="leadActivityForm.call_type"><option value="Gọi đi">Gọi đi</option><option value="Gọi đến">Gọi đến</option></select></label>
                    <label><span>Trạng thái <b>*</b></span><select v-model="leadActivityForm.status"><option value="Open">Chưa bắt đầu</option><option value="Closed">Hoàn thành</option><option value="Cancelled">Đã hủy</option></select></label>
                    <label><span>Kết quả gọi điện</span><select v-model="leadActivityForm.call_result"><option value="">- Không chọn -</option><option value="Liên hệ thành công">Liên hệ thành công</option><option value="Không nghe máy">Không nghe máy</option><option value="Hẹn gọi lại">Hẹn gọi lại</option><option value="Sai số">Sai số</option></select></label>
                  </template>
                </div>
                <footer>
                  <button v-if="!leadActivityMoreOpen" class="misa-activity-more" type="button" @click="leadActivityMoreOpen = true">Thông tin khác</button>
                  <button v-else class="misa-activity-more" type="button" @click="leadActivityMoreOpen = false">Thu gọn</button>
                  <button class="crm-button" type="button" :disabled="leadActivitySaving" @click="closeLeadActivityDialog">Hủy</button>
                  <button v-if="leadActivityMoreOpen && leadActivityForm.activity_type === 'task'" class="crm-button misa-save-close" type="submit" :disabled="leadActivitySaving || !leadActivityForm.subject?.trim()">Lưu và đóng</button>
                  <button class="crm-button primary" type="submit" :disabled="leadActivitySaving || !leadActivityForm.subject?.trim()">{{ leadActivitySaving ? 'Đang lưu...' : 'Lưu' }}</button>
                </footer>
              </form>
            </div>
          </template>
        </main>

        <main v-else-if="route === 'leads'" class="customer-workspace lead-workspace">
          <header class="customer-heading">
            <div class="customer-title"><h1>Tất cả tiềm năng</h1></div>
            <div class="customer-actions">
              <button class="crm-button import" @click="importLeads">⇥ Nhập từ Excel</button>
              <button class="crm-button" @click="exportResource('leads', { search, filters: buildLeadFilters() })">⇤ Xuất Excel</button>
              <button v-if="boot?.resources?.leads?.can_create" class="crm-button primary" @click="openLeadForm()">＋ Thêm</button>
            </div>
          </header>
          <section class="customer-grid" :class="{ 'detail-closed': !leadActivityOpen, 'filter-closed': !leadFilterOpen }">
            <section class="customer-list-panel">
              <div class="customer-list-tools">
                <label class="smart-search"><CRMIcon name="search" /><input v-model="search" placeholder="Tìm theo tên, điện thoại, email..."></label>
                <div class="tool-buttons">
                  <button class="icon-button" data-tooltip="Làm mới" @click="loadRows"><CRMIcon name="refresh" /></button>
                  <button class="icon-button" :class="{ active: leadColumnDialogOpen }" data-tooltip="Tùy chỉnh cột" @click="leadColumnDialogOpen = true"><CRMIcon name="settings" /></button>
                  <button class="icon-button" :class="{ active: leadActivityOpen }" data-tooltip="Ẩn/hiện lịch sử giao dịch" @click="leadActivityOpen = !leadActivityOpen"><CRMIcon name="activity" /></button>
                  <button
                    class="icon-button"
                    :class="{ active: leadFilterOpen || leadAppliedFilterCount }"
                    type="button"
                    data-tooltip="Ẩn/hiện bộ lọc"
                    aria-label="Ẩn hoặc hiện bộ lọc tiềm năng"
                    :aria-expanded="leadFilterOpen"
                    @click="leadFilterOpen = !leadFilterOpen"
                  >
                    <CRMIcon name="filter" />
                  </button>
                </div>
              </div>
              <div class="customer-table-scroll">
                <table class="customer-table lead-table">
                  <colgroup><col class="check-column"><col v-for="column in leadShownColumns" :key="column.field" :style="{ width: column.width }"></colgroup>
                  <thead><tr><th><input type="checkbox" aria-label="Chọn tất cả"></th><th v-for="column in leadShownColumns" :key="column.field">{{ column.label }}</th></tr></thead>
                  <tbody>
                    <tr v-for="row in rows" :key="row.name" :class="{ selected: selected?.name === row.name }" @click="selectRow(row)" @dblclick="openLeadDetail(row)">
                      <td @click.stop><input type="checkbox" :aria-label="'Chọn ' + row.name"></td>
                      <td v-for="column in leadShownColumns" :key="column.field">
                        <a v-if="column.field === 'lead_name'" href="#" @click.prevent.stop="openLeadDetail(row)">{{ row[column.field] || '—' }}</a>
                        <span v-else>{{ formatValue(row[column.field], column.field) }}</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
                <p v-if="loading" class="crm-empty">Đang tải...</p>
                <p v-else-if="!rows.length" class="crm-empty">Không có tiềm năng phù hợp.</p>
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
            <aside v-if="leadActivityOpen" class="customer-detail-panel lead-activity-panel">
              <div class="lead-activity-title">Lịch sử giao dịch</div>
              <div v-if="selected" class="customer-detail-body">
                <div class="customer-timeline activity-history">
                  <article v-for="item in detail?.timeline || []" :key="item.activity_type + '-' + item.name">
                    <i><CRMIcon :name="item.activity_type === 'task' ? 'task' : item.activity_type === 'communication' ? 'email' : 'contact'" /></i>
                    <div>
                      <strong>{{ item.subject || item.description || stripHtml(item.content) || 'Hoạt động tiềm năng' }}</strong>
                      <p v-if="item.content || item.description">{{ stripHtml(item.content || item.description) }}</p>
                      <small>{{ item.comment_email || item.sender || item.allocated_to || selected.lead_owner || '—' }} · {{ formatValue(item.creation, 'creation') }}</small>
                    </div>
                  </article>
                  <p v-if="detail && !detail.timeline.length" class="crm-empty">Chưa có lịch sử giao dịch.</p>
                  <p v-if="!detail" class="crm-empty">Đang tải lịch sử...</p>
                </div>
              </div>
              <div v-else class="crm-empty customer-no-selection">Chọn một tiềm năng để xem lịch sử giao dịch.</div>
            </aside>
            <aside v-if="leadFilterOpen" class="customer-filter-panel">
              <header><h2>Bộ lọc</h2><button type="button" data-tooltip="Đóng bộ lọc" aria-label="Đóng bộ lọc" @click="leadFilterOpen = false">×</button></header>
              <section><strong>ĐÃ LƯU</strong><span>⌃</span></section>
              <section><strong>TIÊU CHÍ LỌC</strong><CRMIcon name="search" /></section>
              <div class="column-options filter-options">
                <div v-for="column in leadVisibleFilterDefinitions" :key="column.field">
                  <label>
                    <input type="checkbox" :checked="leadEnabledFilters.includes(column.field)" @change="toggleLeadFilter(column.field)">
                    <span>{{ column.label }}</span>
                  </label>
                  <select v-if="column.field === 'status' && leadEnabledFilters.includes(column.field)" v-model="leadFilterValues[column.field]">
                    <option value="">Tất cả</option>
                    <option value="Lead">Lead</option><option value="Open">Open</option><option value="Replied">Replied</option>
                    <option value="Opportunity">Opportunity</option><option value="Quotation">Quotation</option>
                    <option value="Interested">Interested</option><option value="Converted">Converted</option>
                    <option value="Do Not Contact">Do Not Contact</option>
                  </select>
                  <select v-else-if="column.field === 'custom_lead_type' && leadEnabledFilters.includes(column.field)" v-model="leadFilterValues[column.field]">
                    <option value="">Tất cả</option><option value="KH viễn thông">KH viễn thông</option>
                    <option value="KH CNTT">KH CNTT</option><option value="KH hộ gia đình">KH hộ gia đình</option>
                    <option value="KH mua bán thi công">KH mua bán thi công</option><option value="KH mua bán">KH mua bán</option>
                  </select>
                  <select v-else-if="column.field === 'custom_business_type' && leadEnabledFilters.includes(column.field)" v-model="leadFilterValues[column.field]">
                    <option value="">Tất cả</option><option value="Doanh nghiệp tư nhân">Doanh nghiệp tư nhân</option>
                    <option value="Công ty TNHH">Công ty TNHH</option><option value="Công ty cổ phần">Công ty cổ phần</option>
                    <option value="Hộ kinh doanh">Hộ kinh doanh</option><option value="Cá nhân">Cá nhân</option>
                  </select>
                  <input
                    v-else-if="leadEnabledFilters.includes(column.field)"
                    v-model="leadFilterValues[column.field]"
                    :type="column.field === 'creation' ? 'date' : 'text'"
                    :placeholder="'Nhập ' + column.label.toLowerCase()"
                  >
                </div>
              </div>
              <button v-if="leadAppliedFilterCount" class="show-more" type="button" @click="clearLeadFilters">Xóa bộ lọc ({{ leadAppliedFilterCount }})</button>
            </aside>
          </section>

          <teleport to="body"><div v-if="leadColumnDialogOpen" class="column-dialog-backdrop" @click.self="leadColumnDialogOpen = false">
            <section class="column-dialog lead-column-dialog">
              <header><h2>Tùy chỉnh cột Tiềm năng</h2><button type="button" data-tooltip="Đóng" @click="leadColumnDialogOpen = false">×</button></header>
              <div class="column-dialog-body">
                <section class="column-picker">
                  <strong>Chọn cột hiển thị</strong>
                  <div class="column-picker-list">
                    <label v-for="column in LEAD_LIST_COLUMNS" :key="column.field">
                      <input type="checkbox" :checked="leadVisibleFields.includes(column.field)" :disabled="column.field === 'lead_name'" @change="toggleLeadColumn(column.field)">
                      <span>{{ column.label }}</span>
                    </label>
                  </div>
                </section>
              </div>
              <footer><button class="crm-button" type="button" @click="resetLeadColumns">Mặc định</button><button class="crm-button primary" type="button" @click="leadColumnDialogOpen = false">Xong</button></footer>
            </section>
          </div></teleport>

          <div v-if="leadFormOpen" class="lead-form-page">
            <header class="lead-form-header">
              <div>
                <h1>{{ leadFormMode === 'edit' ? 'Sửa tiềm năng' : 'Thêm Tiềm năng' }}</h1>
                <span>Mẫu tiêu chuẩn</span>
              </div>
              <div>
                <button class="crm-button" @click="closeLeadForm" :disabled="leadFormSaving">Hủy</button>
                <button class="crm-button import" @click="saveLead(true)" :disabled="leadFormSaving || leadFormMode === 'edit'">Lưu và thêm</button>
                <button class="crm-button primary" @click="saveLead(false)" :disabled="leadFormSaving">{{ leadFormSaving ? 'Đang lưu...' : 'Lưu' }}</button>
              </div>
            </header>
            <form class="lead-form-card" @submit.prevent="saveLead(false)">
              <section>
                <h2>Thông tin chung</h2>
                <div class="lead-form-grid">
                  <label><span>Xưng hô</span><select v-model="leadForm.salutation"><option value="">- Không chọn -</option><option v-for="s in leadFormOptions.salutations" :key="s.name" :value="s.name">{{ s.name }}</option></select></label>
                  <label><span>Họ và đệm</span><input v-model="leadForm.last_name" placeholder=""></label>
                  <label class="lead-required"><span>Tên <em>*</em></span><input v-model="leadForm.first_name" required placeholder=""></label>
                  <label><span>Họ và tên</span><input :value="[leadForm.last_name, leadForm.first_name].filter(Boolean).join(' ')" disabled class="lead-input-auto" placeholder="Tự sinh"></label>
                  <label><span>Phòng ban</span><input v-model="leadForm.department" placeholder="- Không chọn -"></label>
                  <label><span>Chức danh</span><input v-model="leadForm.job_title" placeholder="- Không chọn -"></label>
                  <label class="lead-required"><span>ĐT di động <em>*</em></span><input v-model="leadForm.mobile_no" type="tel" required placeholder=""></label>
                  <label><span>ĐT cơ quan</span><input v-model="leadForm.phone" type="tel" placeholder=""></label>
                  <label><span>Nguồn gốc</span><select v-model="leadForm.utm_source"><option value="">- Không chọn -</option><option v-for="s in leadFormOptions.sources" :key="s.name" :value="s.name">{{ s.name }}</option></select></label>
                  <label><span>Loại tiềm năng</span><select v-model="leadForm.custom_lead_type"><option value="">- Không chọn -</option><option value="KH viễn thông">KH viễn thông</option><option value="KH CNTT">KH CNTT</option><option value="KH hộ gia đình">KH hộ gia đình</option><option value="KH mua bán thi công">KH mua bán thi công</option><option value="KH mua bán">KH mua bán</option></select></label>
                  <label><span>Zalo</span><input v-model="leadForm.custom_zalo" placeholder=""></label>
                  <label><span>Email cá nhân</span><input v-model="leadForm.email_id" type="email" placeholder=""></label>
                  <label><span>Email cơ quan</span><input v-model="leadForm.custom_work_email" type="email" placeholder=""></label>
                  <label><span>Tổ chức</span><input v-model="leadForm.company_name" placeholder=""></label>
                  <label><span>Mã số thuế</span><input v-model="leadForm.custom_tax_id" placeholder=""></label>
                </div>
              </section>
              <section>
                <h2>Thông tin tổ chức</h2>
                <div class="lead-form-grid">
                  <label><span>Tài khoản ngân hàng</span><input v-model="leadForm.custom_bank_account" placeholder=""></label>
                  <label><span>Mở tại ngân hàng</span><input v-model="leadForm.custom_bank_name" placeholder=""></label>
                  <label><span>Ngày thành lập</span><input v-model="leadForm.custom_founding_date" type="date"></label>
                  <label><span>Loại hình</span><select v-model="leadForm.custom_business_type"><option value="">- Không chọn -</option><option value="Doanh nghiệp tư nhân">Doanh nghiệp tư nhân</option><option value="Công ty TNHH">Công ty TNHH</option><option value="Công ty cổ phần">Công ty cổ phần</option><option value="Hộ kinh doanh">Hộ kinh doanh</option><option value="Cá nhân">Cá nhân</option></select></label>
                  <label><span>Lĩnh vực</span><input v-model="leadForm.custom_sector" placeholder="- Không chọn -"></label>
                  <label><span>Ngành nghề</span><select v-model="leadForm.industry"><option value="">- Không chọn -</option><option v-for="ind in leadFormOptions.industries" :key="ind.name" :value="ind.name">{{ ind.name }}</option></select></label>
                </div>
              </section>
              <section>
                <h2>Thông tin địa chỉ</h2>
                <div class="lead-form-grid">
                  <label><span>Quốc gia</span><select v-model="leadForm.country"><option value="">- Không chọn -</option><option v-for="c in leadFormOptions.countries" :key="c.name" :value="c.name">{{ c.name === 'Vietnam' ? 'Việt Nam' : c.name }}</option></select></label>
                  <label><span>Tỉnh/Thành phố</span><input v-model="leadForm.state" placeholder="- Không chọn -"></label>
                  <label><span>Quận/Huyện</span><input v-model="leadForm.custom_district" placeholder="- Không chọn -"></label>
                  <label><span>Phường/Xã</span><input v-model="leadForm.custom_ward" placeholder="- Không chọn -"></label>
                  <label><span>Số nhà, Đường phố</span><input v-model="leadForm.address_line1" placeholder=""></label>
                  <label><span>Mã vùng</span><input v-model="leadForm.pincode" placeholder=""></label>
                  <label class="lead-col-full"><span>Địa chỉ</span><textarea v-model="leadForm.custom_full_address" rows="3" placeholder="Vị trí cắm mốc"></textarea></label>
                </div>
              </section>
              <section>
                <h2>Thông tin mô tả</h2>
                <div class="lead-form-grid">
                  <label class="lead-col-full"><span>Mô tả</span><textarea v-model="leadForm.notes" rows="4" placeholder=""></textarea></label>
                </div>
              </section>
              <section>
                <h2>Thông tin hệ thống</h2>
                <div class="lead-form-grid">
                  <label class="lead-check-label"><span>Dùng chung</span><input v-model.number="leadForm.custom_is_shared" type="checkbox" :true-value="1" :false-value="0"></label>
                  <label><span>Mã tiềm năng</span><input :value="leadForm.name || ''" disabled placeholder="Mã tự sinh"></label>
                </div>
              </section>
            </form>
          </div>
        </main>

`;
