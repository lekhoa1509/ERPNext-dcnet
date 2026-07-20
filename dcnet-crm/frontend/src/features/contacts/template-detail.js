export default `
<!-- ════════ CHI TIẾT LIÊN HỆ (MISA-style full-page) ════════ -->
<div v-else-if="route === 'contact-detail'" class="ccd-page">

  <!-- Loading -->
  <div v-if="contactDetailLoading" class="ccd-loading">Đang tải...</div>

  <template v-else-if="contactDetail">

    <!-- ── HEADER ── -->
    <div class="ccd-header">
      <div class="ccd-header-left">
        <button class="ccd-back" @click="backToContacts" title="Quay lại">
          <svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10 3L5 8l5 5"/></svg>
        </button>
        <div class="ccd-avatar">{{ (contactDetail.full_name || contactDetailName || 'C').slice(0,1).toUpperCase() }}</div>
        <div class="ccd-identity">
          <h1 class="ccd-name">{{ contactDetail.full_name || contactDetailName }}</h1>
          <div class="ccd-identity-meta">
            <a
              v-if="contactDetail.customer"
              href="#"
              class="ccd-company-link"
              @click.prevent="openCustomerDetail({ name: contactDetail.customer })"
            >{{ contactDetail.company_name || contactDetail.customer }}</a>
            <span v-else-if="contactDetail.company_name" class="ccd-company-name">{{ contactDetail.company_name }}</span>
            <span v-if="contactDetail.customer || contactDetail.company_name" class="ccd-identity-dot">•</span>
            <button class="ccd-add-tag" @click="addContactTag">
              <svg viewBox="0 0 16 16" width="13" height="13" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"><path d="M2.5 3.5v4.2L8.3 13.5l5.2-5.2-5.8-5.8H3.5a1 1 0 0 0-1 1Z"/><circle cx="6" cy="6" r="1"/></svg>
              Thêm thẻ
            </button>
          </div>
        </div>
      </div>
      <div class="ccd-header-actions">
        <template v-if="contactDetailEditing">
          <button class="ccd-btn" @click="cancelContactEdit" :disabled="contactDetailSaving">Hủy</button>
          <button class="ccd-btn ccd-btn--primary" @click="saveContactDetail" :disabled="contactDetailSaving">
            {{ contactDetailSaving ? 'Đang lưu...' : 'Lưu' }}
          </button>
        </template>
        <template v-else>
          <button v-if="contactDetail.can_write" class="ccd-btn ccd-btn--with-icon" @click="startContactEdit">
            <svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10.8 2.2a1.4 1.4 0 0 1 2 2L5.2 11.8 2.5 13l1.2-2.7 7.1-8.1Z"/><path d="m9.6 3.6 2.8 2.8"/></svg>
            Sửa
          </button>
          <div class="ccd-split-btn">
            <button class="ccd-btn ccd-btn--primary" @click="createOpportunityFromContact">Sinh cơ hội</button>
            <button class="ccd-btn ccd-btn--primary ccd-btn--arrow" @click="notifyContactTabAction('Tùy chọn sinh cơ hội')">
              <svg viewBox="0 0 10 6" width="10" height="6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M1 1l4 4 4-4"/></svg>
            </button>
          </div>
          <details class="crm-detail-more">
            <summary class="ccd-btn ccd-btn--icon" title="Thêm thao tác" aria-label="Thêm thao tác"><CRMIcon name="more" /></summary>
            <div class="crm-detail-more-menu" role="menu">
              <button type="button" role="menuitem" @click="openContactRelated('Contact', contactDetail.name); $event.currentTarget.closest('details').removeAttribute('open')"><CRMIcon name="document" /><span>Mở biểu mẫu hệ thống</span></button>
              <div class="crm-detail-more-separator"></div>
              <button type="button" role="menuitem" @click="openAuditLog('Contact', contactDetail.name); $event.currentTarget.closest('details').removeAttribute('open')"><CRMIcon name="history" /><span>Nhật ký</span></button>
            </div>
          </details>
        </template>
      </div>
    </div>

    <!-- ── SUMMARY BAR ── -->
    <div class="ccd-summary-bar">
      <div class="ccd-summ-item">
        <span class="ccd-summ-label">Chức danh</span>
        <span class="ccd-summ-val" :class="!contactDetail.designation && 'ccd-summ-empty'">{{ contactDetail.designation || '— Không chọn —' }}</span>
      </div>
      <div class="ccd-summ-item">
        <span class="ccd-summ-label">Phòng ban</span>
        <span class="ccd-summ-val" :class="!contactDetail.department && 'ccd-summ-empty'">{{ contactDetail.department || '— Không chọn —' }}</span>
      </div>
      <div class="ccd-summ-item">
        <span class="ccd-summ-label">ĐT di động</span>
        <span class="ccd-summ-val">{{ contactDetail.mobile_no || '—' }}</span>
      </div>
      <div class="ccd-summ-item">
        <span class="ccd-summ-label">ĐT cơ quan</span>
        <span class="ccd-summ-val">{{ contactDetail.phone || '—' }}</span>
      </div>
      <div class="ccd-summ-item ccd-summ-item--wide">
        <span class="ccd-summ-label">Email cơ quan</span>
        <span class="ccd-summ-val">{{ contactDetail.email_id || '—' }}</span>
      </div>
    </div>

    <!-- ── BODY ── -->
    <div class="ccd-body">

      <!-- LEFT: tabs + content -->
      <div class="ccd-main">

        <!-- Tab bar -->
        <div class="ccd-tabs-bar">
          <nav class="ccd-tabs" role="tablist" aria-label="Liên hệ">
            <button
              v-for="tab in CONTACT_DETAIL_TABS"
              :key="tab.key"
              :class="{active: contactDetailTab === tab.key}"
              :aria-selected="contactDetailTab === tab.key"
              type="button"
              role="tab"
              @click="contactDetailTab = tab.key"
            >{{ tab.label }}<b v-if="contactDetailTabBadge(tab.key)" class="ccd-tab-badge">{{ contactDetailTabBadge(tab.key) }}</b></button>
          </nav>
        </div>

        <!-- Tab content -->
        <div class="ccd-tabcontent">

          <!-- ── Tab: Thông tin chi tiết ── -->
          <div v-if="contactDetailTab === 'info'" class="ccd-info-view">
            <div class="ccd-info-toolbar">
              <label class="ccd-field-search">
                <CRMIcon name="search" />
                <input
                  v-model="contactDetailFieldSearch"
                  type="search"
                  placeholder="Tìm kiếm trường"
                  aria-label="Tìm kiếm trường thông tin liên hệ"
                >
              </label>
              <label class="sod-dtoggle-label">
                <input type="checkbox" class="sod-dtoggle-inp" v-model="contactDetailShowEmpty">
                <span class="sod-dtoggle-track"></span>
                <span class="ccd-toggle-text">Hiển thị dữ liệu trống</span>
              </label>
            </div>

            <!-- Section: Thông tin chung -->
            <div class="sod-section">
              <div class="sod-section-title">Thông tin chung</div>
              <div class="sod-detail-grid">

                <div class="sod-drow">
                  <span class="sod-dlabel">Mã liên hệ</span>
                  <div class="sod-dval">{{ contactDetail.name }}</div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Xưng hô</span>
                  <div class="sod-dval">
                    <select v-if="contactDetailEditing" class="ccd-inp" v-model="cdForm.salutation">
                      <option value="">- Không chọn -</option>
                      <option v-for="opt in contactCreateOptions.salutations" :key="opt.name" :value="opt.name">{{ opt.name }}</option>
                    </select>
                    <template v-else>
                      <span v-if="contactDetail.salutation">{{ contactDetail.salutation }}</span>
                      <span v-else class="sod-dval-empty">— Không chọn —</span>
                    </template>
                  </div>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Họ và đệm</span>
                  <div class="sod-dval">
                    <input v-if="contactDetailEditing" class="ccd-inp" v-model="cdForm.last_name" placeholder="Họ và đệm" />
                    <span v-else>{{ contactDetail.last_name || '' }}</span>
                  </div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Tên <span class="ccd-req">*</span></span>
                  <div class="sod-dval">
                    <input v-if="contactDetailEditing" class="ccd-inp" v-model="cdForm.first_name" placeholder="Tên" />
                    <span v-else>{{ contactDetail.first_name || '' }}</span>
                  </div>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Họ và tên</span>
                  <div class="sod-dval">{{ contactDetailEditing ? ((cdForm.last_name||'')+' '+(cdForm.first_name||'')).trim()||'—' : (contactDetail.full_name||'—') }}</div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Chức danh</span>
                  <div class="sod-dval">
                    <input v-if="contactDetailEditing" class="ccd-inp" v-model="cdForm.designation" placeholder="Nhập chức danh tại khách hàng">
                    <template v-else>
                      <span v-if="contactDetail.designation">{{ contactDetail.designation }}</span>
                      <span v-else class="sod-dval-empty">— Không chọn —</span>
                    </template>
                  </div>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Phòng ban</span>
                  <div class="sod-dval">
                    <input v-if="contactDetailEditing" class="ccd-inp" v-model="cdForm.department" placeholder="Nhập phòng ban tại khách hàng">
                    <template v-else>
                      <span v-if="contactDetail.department">{{ contactDetail.department }}</span>
                      <span v-else class="sod-dval-empty">— Không chọn —</span>
                    </template>
                  </div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Tổ chức</span>
                  <div class="sod-dval">
                    <select v-if="contactDetailEditing" class="ccd-inp" v-model="cdForm.customer">
                      <option value="">- Không chọn -</option>
                      <option v-for="opt in contactCreateOptions.customers" :key="opt.name" :value="opt.name">{{ opt.customer_name || opt.name }}</option>
                    </select>
                    <template v-else>
                      <a v-if="contactDetail.customer" href="#" class="sod-dlink" @click.prevent="openCustomerDetail({ name: contactDetail.customer })">{{ contactDetail.company_name || contactDetail.customer }}</a>
                      <span v-else-if="contactDetail.company_name">{{ contactDetail.company_name }}</span>
                      <span v-else class="sod-dval-empty">— Không chọn —</span>
                    </template>
                  </div>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Phân loại khách hàng</span>
                  <div class="sod-dval"><span class="sod-dval-empty">— Không chọn —</span></div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Không gọi điện</span>
                  <div class="sod-dval">
                    <input v-if="contactDetailEditing" type="checkbox" class="ccd-check" v-model="cdForm.khong_goi_dien" :true-value="1" :false-value="0">
                    <span v-else>{{ contactDetail.khong_goi_dien ? 'Có' : '' }}</span>
                  </div>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Không gửi Email</span>
                  <div class="sod-dval">
                    <input v-if="contactDetailEditing" type="checkbox" class="ccd-check" v-model="cdForm.khong_gui_email" :true-value="1" :false-value="0">
                    <span v-else>{{ contactDetail.khong_gui_email ? 'Có' : '' }}</span>
                  </div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Điện thoại khác</span>
                  <div class="sod-dval">
                    <input v-if="contactDetailEditing" class="ccd-inp" v-model="cdForm.dien_thoai_khac" placeholder="—" />
                    <span v-else>{{ '' }}</span>
                  </div>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">ĐT di động</span>
                  <div class="sod-dval">
                    <input v-if="contactDetailEditing" class="ccd-inp" v-model="cdForm.mobile_no" placeholder="Số di động" />
                    <span v-else>{{ contactDetail.mobile_no || '' }}</span>
                  </div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Email cá nhân</span>
                  <div class="sod-dval">
                    <input v-if="contactDetailEditing" class="ccd-inp" type="email" v-model="cdForm.email_ca_nhan" placeholder="—" />
                    <span v-else>{{ '' }}</span>
                  </div>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">ĐT cơ quan</span>
                  <div class="sod-dval">
                    <input v-if="contactDetailEditing" class="ccd-inp" v-model="cdForm.phone" placeholder="Số cơ quan" />
                    <span v-else>{{ contactDetail.phone || '' }}</span>
                  </div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Nguồn gốc</span>
                  <div class="sod-dval">
                    <select v-if="contactDetailEditing" class="ccd-inp" v-model="cdForm.nguon_goc">
                      <option value="">- Không chọn -</option>
                      <option>Gọi điện</option><option>Trực tiếp</option><option>Giới thiệu</option>
                      <option>Mạng xã hội</option><option>Email</option><option>Khác</option>
                    </select>
                    <template v-else>
                      <span v-if="contactDetail.nguon_goc">{{ contactDetail.nguon_goc }}</span>
                      <span v-else class="sod-dval-empty">— Không chọn —</span>
                    </template>
                  </div>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Email cơ quan</span>
                  <div class="sod-dval">
                    <input v-if="contactDetailEditing" class="ccd-inp" type="email" v-model="cdForm.email_id" placeholder="email@company.com" />
                    <span v-else>{{ contactDetail.email_id || '' }}</span>
                  </div>
                </div>
                <div class="sod-drow"></div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Zalo</span>
                  <div class="sod-dval">
                    <input v-if="contactDetailEditing" class="ccd-inp" v-model="cdForm.zalo" placeholder="—" />
                    <span v-else-if="contactDetail.mobile_no" class="sod-dlink">{{ contactDetail.mobile_no }}</span>
                    <span v-else></span>
                  </div>
                </div>
                <div class="sod-drow"></div>

              </div>
            </div>

            <!-- Section: Thông tin địa chỉ -->
            <div class="sod-section">
              <div class="sod-section-title">Thông tin địa chỉ</div>
              <div class="sod-detail-grid">

                <div class="sod-drow">
                  <span class="sod-dlabel">Quốc gia</span>
                  <div class="sod-dval">
                    <select v-if="contactDetailEditing" class="ccd-inp" v-model="cdBillingForm.country">
                      <option value="Vietnam">Việt Nam</option>
                      <option v-for="opt in contactCreateOptions.countries" :key="opt.name" :value="opt.name">{{ opt.name }}</option>
                    </select>
                    <template v-else>
                      <span v-if="contactDetail.billing_address?.country">{{ contactDetail.billing_address.country }}</span>
                      <span v-else class="sod-dval-empty">— Không chọn —</span>
                    </template>
                  </div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Tỉnh/Thành phố</span>
                  <div class="sod-dval">
                    <select v-if="contactDetailEditing" class="ccd-inp" v-model="cdBillingProvinceCode">
                      <option value="">- Không chọn -</option>
                      <option v-for="p in ccVnProvinces" :key="p.code" :value="String(p.code)">{{ p.name }}</option>
                    </select>
                    <template v-else>
                      <span v-if="contactDetail.billing_address?.state">{{ contactDetail.billing_address.state }}</span>
                      <span v-else class="sod-dval-empty">— Không chọn —</span>
                    </template>
                  </div>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Quận/Huyện</span>
                  <div class="sod-dval"><span class="sod-dval-empty">— Không chọn —</span></div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Phường/Xã</span>
                  <div class="sod-dval">
                    <select v-if="contactDetailEditing" class="ccd-inp" v-model="cdBillingForm.county" :disabled="!cdBillingProvinceCode || cdLoadingBillingWards">
                      <option value="">{{ cdLoadingBillingWards ? 'Đang tải...' : '- Không chọn -' }}</option>
                      <option v-for="w in cdVnBillingWards" :key="w.code" :value="w.name">{{ w.name }}</option>
                    </select>
                    <template v-else>
                      <span v-if="contactDetail.billing_address?.county">{{ contactDetail.billing_address.county }}</span>
                      <span v-else class="sod-dval-empty">— Không chọn —</span>
                    </template>
                  </div>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Số nhà, Đường phố</span>
                  <div class="sod-dval">
                    <input v-if="contactDetailEditing" class="ccd-inp" v-model="cdBillingForm.address_line1" placeholder="—" />
                    <span v-else>{{ contactDetail.billing_address?.address_line1 || '' }}</span>
                  </div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Mã vùng</span>
                  <div class="sod-dval">
                    <input v-if="contactDetailEditing" class="ccd-inp" v-model="cdBillingForm.pincode" placeholder="—" />
                    <span v-else>{{ contactDetail.billing_address?.pincode || '' }}</span>
                  </div>
                </div>

                <div class="sod-drow sod-drow--full">
                  <span class="sod-dlabel">Địa chỉ</span>
                  <div class="sod-dval">{{ contactDetail.billing_address?.address_line1 || '' }}</div>
                </div>
                <div class="sod-drow sod-drow--full">
                  <span class="sod-dlabel"></span>
                  <div class="sod-dval"><a href="#" class="sod-dlink" @click.prevent>Vị trí cắm mốc</a></div>
                </div>

              </div>
            </div>

            <!-- Section: Thông tin địa chỉ giao hàng -->
            <div class="sod-section">
              <div class="sod-section-title">Thông tin địa chỉ giao hàng</div>
              <div class="sod-detail-grid">
                <div class="sod-drow">
                  <span class="sod-dlabel">Quốc gia (Giao hàng)</span>
                  <div class="sod-dval"><span class="sod-dval-empty">— Không chọn —</span></div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Tỉnh/Thành phố (Giao hàng)</span>
                  <div class="sod-dval"><span class="sod-dval-empty">— Không chọn —</span></div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Quận/Huyện (Giao hàng)</span>
                  <div class="sod-dval"><span class="sod-dval-empty">— Không chọn —</span></div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Phường/Xã (Giao hàng)</span>
                  <div class="sod-dval"><span class="sod-dval-empty">— Không chọn —</span></div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Số nhà, Đường phố (Giao hàng)</span>
                  <div class="sod-dval"></div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Mã vùng (Giao hàng)</span>
                  <div class="sod-dval"></div>
                </div>
                <div class="sod-drow sod-drow--full">
                  <span class="sod-dlabel">Địa chỉ (Giao hàng)</span>
                  <div class="sod-dval"></div>
                </div>
                <div class="sod-drow sod-drow--full">
                  <span class="sod-dlabel"></span>
                  <div class="sod-dval"><a href="#" class="sod-dlink" @click.prevent>Vị trí cắm mốc</a></div>
                </div>
              </div>
            </div>

            <!-- Section: Thông tin khác -->
            <div class="sod-section">
              <div class="sod-section-title">Thông tin khác</div>
              <div class="sod-detail-grid">
                <div class="sod-drow">
                  <span class="sod-dlabel">Ngày sinh</span>
                  <div class="sod-dval">{{ contactDetail.date_of_birth || '' }}</div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Giới tính</span>
                  <div class="sod-dval">
                    <select v-if="contactDetailEditing" class="ccd-inp" v-model="cdForm.gender">
                      <option value="">- Không chọn -</option>
                      <option v-for="opt in contactCreateOptions.genders" :key="opt.name" :value="opt.name">{{ opt.name }}</option>
                    </select>
                    <template v-else>
                      <span v-if="contactDetail.gender">{{ contactDetail.gender }}</span>
                      <span v-else class="sod-dval-empty">— Không chọn —</span>
                    </template>
                  </div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Tình trạng hôn nhân</span>
                  <div class="sod-dval"><span class="sod-dval-empty">— Không chọn —</span></div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Facebook</span>
                  <div class="sod-dval"></div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Tài khoản ngân hàng</span>
                  <div class="sod-dval"></div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Mở tại ngân hàng</span>
                  <div class="sod-dval"></div>
                </div>
              </div>
            </div>

            <!-- Section: Thông tin mô tả -->
            <div class="sod-section">
              <div class="sod-section-title">Thông tin mô tả</div>
              <div class="sod-detail-grid">
                <div class="sod-drow sod-drow--full sod-dval--top">
                  <span class="sod-dlabel">Mô tả</span>
                  <div class="sod-dval">
                    <textarea v-if="contactDetailEditing" class="ccd-textarea" v-model="cdForm.mo_ta" rows="3" placeholder="—"></textarea>
                    <span v-else>{{ contactDetail.description || '' }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Section: Thông tin hệ thống -->
            <div class="sod-section">
              <div class="sod-section-title">Thông tin hệ thống</div>
              <div class="sod-detail-grid">
                <div class="sod-drow">
                  <span class="sod-dlabel">Chủ sở hữu</span>
                  <div class="sod-dval"><span class="sod-dlink">{{ contactDetail.owner || '' }}</span></div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Đơn vị</span>
                  <div class="sod-dval"></div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Người tạo</span>
                  <div class="sod-dval">
                    <span class="sod-dlink">{{ contactDetail.owner || '' }}</span>
                    <span v-if="contactDetail.owner" style="color:var(--crm-text-muted);margin-left:4px">- CRM</span>
                  </div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Ngày tạo</span>
                  <div class="sod-dval">{{ contactDetail.creation ? contactDetail.creation.slice(0,16).replace('T',' ') : '' }}</div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Người sửa</span>
                  <div class="sod-dval">
                    <span class="sod-dlink">{{ contactDetail.modified_by || '' }}</span>
                    <span v-if="contactDetail.modified_by" style="color:var(--crm-text-muted);margin-left:4px">- CRM</span>
                  </div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Ngày sửa</span>
                  <div class="sod-dval">{{ contactDetail.modified ? contactDetail.modified.slice(0,16).replace('T',' ') : '' }}</div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Dùng chung</span>
                  <div class="sod-dval">
                    <input v-if="contactDetailEditing" type="checkbox" class="ccd-check" v-model="cdForm.dung_chung" :true-value="1" :false-value="0">
                    <span v-else>{{ contactDetail.dung_chung ? 'Có' : '' }}</span>
                  </div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Bố cục</span>
                  <div class="sod-dval">Mẫu tiêu chuẩn</div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Điểm liên hệ</span>
                  <div class="sod-dval">0</div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Ngừng theo dõi</span>
                  <div class="sod-dval"></div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Ngày tương tác gần nhất</span>
                  <div class="sod-dval"></div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Số ngày chưa tương tác</span>
                  <div class="sod-dval">0</div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Ngày ghé thăm gần nhất</span>
                  <div class="sod-dval"></div>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Ngày cuộc gọi gần nhất</span>
                  <div class="sod-dval"></div>
                </div>
                <div class="sod-drow sod-drow--full">
                  <span class="sod-dlabel">Người liên quan</span>
                  <div class="sod-dval"></div>
                </div>
              </div>
            </div>

          </div>

          <!-- Notes tab -->
          <div v-else-if="contactDetailTab === 'notes'" class="ccd-notes-view">
            <div class="ccd-notes-card">
              <div class="ccd-notes-title">Ghi chú</div>
              <div class="ccd-notes-add">
                <textarea v-model="contactNoteText" class="ccd-notes-input" rows="2" placeholder="Thêm ghi chú"></textarea>
                <button class="crm-button primary ccd-notes-send" :disabled="!contactNoteText.trim() || contactNoteSaving" @click="addContactNote">{{ contactNoteSaving ? 'Đang lưu…' : 'Thêm' }}</button>
              </div>
            </div>
            <div v-if="contactDetail.notes && contactDetail.notes.length" class="opp-comment-list ccd-notes-list">
              <div v-for="n in contactDetail.notes" :key="n.name" class="opp-comment-item">
                <div class="opp-comment-avatar">{{ (n.comment_by_fullname || n.comment_by || '?')[0].toUpperCase() }}</div>
                <div class="opp-comment-body">
                  <strong>{{ n.comment_by_fullname || n.comment_by }}</strong>
                  <p>{{ stripHtml(n.content || '') }}</p>
                  <small>{{ formatValue(n.creation, 'creation') }}</small>
                </div>
              </div>
            </div>
            <div v-else class="ccd-empty-tab">
              <svg viewBox="0 0 64 64" width="48" height="48" fill="none">
                <rect x="8" y="12" width="48" height="40" rx="4" stroke="#e5e7eb" stroke-width="2"/>
                <path d="M20 28h24M20 36h16" stroke="#d1d5db" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <span>Chưa có ghi chú</span>
            </div>
          </div>

          <!-- Attachments tab -->
          <div v-else-if="contactDetailTab === 'attachments'" class="ccd-attach-view">
            <div class="ccd-attach-card">
              <div class="ccd-attach-head">
                <div class="ccd-attach-title">Tài liệu đính kèm</div>
                <div v-if="contactDetail.can_write" class="ccd-attach-actions">
                  <button class="ccd-attach-btn" @click="addContactAttachmentLink">
                    <svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"><path d="M6.5 9.5l3-3"/><path d="M7 4.5l1-1a2.5 2.5 0 0 1 3.5 3.5l-1 1"/><path d="M9 11.5l-1 1A2.5 2.5 0 0 1 4.5 9l1-1"/></svg>
                    Thêm liên kết
                  </button>
                  <button class="ccd-attach-btn primary" :disabled="contactAttachUploading" @click="$refs.contactFileInput.click()">
                    <svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="M13 7l-5.5 5.5a3 3 0 0 1-4.2-4.2L9 2.5a2 2 0 0 1 2.8 2.8L6 11.2a1 1 0 0 1-1.4-1.4L9.5 5"/></svg>
                    {{ contactAttachUploading ? 'Đang tải…' : 'Thêm tệp' }}
                  </button>
                  <input ref="contactFileInput" type="file" style="display:none" @change="uploadContactFile" />
                </div>
              </div>
              <div class="ccd-attach-tablewrap">
                <table class="ccd-attach-table">
                  <thead>
                    <tr>
                      <th>Tên tài liệu</th>
                      <th>Người đính kèm</th>
                      <th>Ngày đính kèm</th>
                      <th>Dung lượng</th>
                      <th class="ccd-attach-col-act"></th>
                    </tr>
                  </thead>
                  <tbody v-if="contactDetail.attachments && contactDetail.attachments.length">
                    <tr v-for="f in contactDetail.attachments" :key="f.name">
                      <td><a :href="f.file_url" target="_blank" rel="noopener" class="sod-dlink ccd-attachment-link"><CRMIcon :name="contactAttachmentIcon(f)" /><span>{{ f.file_name || f.file_url }}</span></a></td>
                      <td>{{ f.owner }}</td>
                      <td>{{ formatValue(f.creation, 'creation') }}</td>
                      <td>{{ f.file_size ? formatFileSize(f.file_size) : '—' }}</td>
                      <td class="ccd-attach-col-act"><button v-if="contactDetail.can_write" class="ccd-attach-del" title="Xóa" @click="deleteContactAttachment(f.name)">×</button></td>
                    </tr>
                  </tbody>
                </table>
                <div v-if="!contactDetail.attachments || !contactDetail.attachments.length" class="ccd-empty-tab">
                  <svg viewBox="0 0 64 64" width="48" height="48" fill="none">
                    <rect x="8" y="12" width="48" height="40" rx="4" stroke="#e5e7eb" stroke-width="2"/>
                    <path d="M20 28h24M20 36h16" stroke="#d1d5db" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                  <span>Không có bản ghi nào</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Purchased items tab -->
          <div v-else-if="contactDetailTab === 'purchased_items'" class="ccd-attach-view">
            <div class="ccd-attach-card">
              <div class="ccd-attach-head">
                <div class="ccd-attach-title">Hàng hóa đã mua <button class="ccd-title-refresh" type="button" @click="loadContactDetail(contactDetailName)"><CRMIcon name="refresh" /></button></div>
              </div>
              <div class="ccd-attach-tablewrap">
                <table class="ccd-attach-table">
                  <thead><tr><th>Mã hàng hóa</th><th>Tên hàng hóa</th><th>Loại hàng hóa</th><th>Số lượng</th><th>Doanh số</th></tr></thead>
                  <tbody v-if="contactDetail.purchased_items && contactDetail.purchased_items.length">
                    <tr v-for="item in contactDetail.purchased_items" :key="item.item_code">
                      <td><a href="#" class="sod-dlink" @click.prevent="openContactRelated('Item', item.item_code)">{{ item.item_code || '—' }}</a></td>
                      <td><a href="#" class="sod-dlink" @click.prevent="openContactRelated('Item', item.item_code)">{{ item.item_name || item.item_code }}</a></td>
                      <td><a href="#" class="sod-dlink" @click.prevent>{{ item.item_group || '—' }}</a></td>
                      <td>{{ item.qty || 0 }}</td>
                      <td>{{ formatValue(item.amount, 'grand_total') }}</td>
                    </tr>
                  </tbody>
                </table>
                <div v-if="!contactDetail.purchased_items || !contactDetail.purchased_items.length" class="ccd-empty-tab">
                  <CRMIcon name="package" />
                  <span>Không có bản ghi nào</span>
                </div>
              </div>
              <footer class="ccd-related-footer">
                <strong>Tổng số {{ (contactDetail.purchased_items || []).length }}</strong>
                <span class="ccd-related-page"><span>Số dòng/trang</span><b>20</b><span>1 - {{ (contactDetail.purchased_items || []).length || 1 }}</span><button disabled>‹</button><button disabled>›</button></span>
              </footer>
            </div>
          </div>

          <!-- Opportunities tab -->
          <div v-else-if="contactDetailTab === 'opportunities'" class="ccd-attach-view">
            <div class="ccd-attach-card">
              <div class="ccd-attach-head">
                <div class="ccd-attach-title">Cơ hội</div>
                <div class="ccd-attach-actions">
                  <button class="ccd-attach-btn primary" @click="openOppPicker">
                    <svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8.5l3.5 3.5L13 5"/></svg>
                    Chọn
                  </button>
                </div>
              </div>
              <div class="ccd-attach-tablewrap">
                <table class="ccd-attach-table" v-if="contactDetail.opportunities && contactDetail.opportunities.length">
                  <thead>
                    <tr>
                      <th>Tên cơ hội</th>
                      <th>Số tiền</th>
                      <th>Giai đoạn</th>
                      <th>Tỷ lệ thành công</th>
                      <th>Doanh số kỳ vọng</th>
                      <th>Ngày kỳ vọng/kết thúc</th>
                      <th>Người thực hiện</th>
                      <th class="ccd-attach-col-act"></th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="o in contactDetail.opportunities" :key="o.name">
                      <td><a href="#" class="sod-dlink crm-record-link" @click.prevent="openOpportunityDetail({ name: o.name })">{{ o.title || o.name }}</a></td>
                      <td>{{ formatValue(o.opportunity_amount, 'opportunity_amount') }}</td>
                      <td>{{ o.sales_stage || '—' }}</td>
                      <td>{{ o.probability != null ? o.probability + '%' : '—' }}</td>
                      <td>{{ formatValue(o.expected_revenue, 'opportunity_amount') }}</td>
                      <td>{{ formatValue(o.expected_closing, 'date') }}</td>
                      <td>{{ o.opportunity_owner || '—' }}</td>
                      <td class="ccd-attach-col-act"><button class="ccd-attach-del" title="Bỏ liên kết" @click="unlinkContactOpportunity(o.name)">×</button></td>
                    </tr>
                  </tbody>
                </table>
                <div v-else class="ccd-empty-tab">
                  <svg viewBox="0 0 64 64" width="48" height="48" fill="none">
                    <rect x="8" y="12" width="48" height="40" rx="4" stroke="#e5e7eb" stroke-width="2"/>
                    <path d="M20 28h24M20 36h16" stroke="#d1d5db" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                  <span>Không có bản ghi nào</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Sales orders tab -->
          <div v-else-if="contactDetailTab === 'orders'" class="ccd-attach-view">
            <div class="ccd-attach-card">
              <div class="ccd-attach-head">
                <div class="ccd-attach-title">Đơn hàng <button class="ccd-title-refresh" type="button" @click="loadContactDetail(contactDetailName)"><CRMIcon name="refresh" /></button></div>
                <div class="ccd-attach-actions"><button class="ccd-attach-btn primary" type="button" @click="notifyContactTabAction('Chọn đơn hàng')">Chọn</button></div>
              </div>
              <div class="ccd-attach-tablewrap">
                <table class="ccd-attach-table">
                  <thead><tr><th>Số đơn hàng/hợp đồng</th><th>Diễn giải</th><th>Giá trị đơn hàng</th><th>Tình trạng</th><th>Tình trạng ghi doanh số</th><th>Người thực hiện</th><th>Đơn vị</th><th>Ngày đặt hàng</th><th>Ngày ghi sổ</th></tr></thead>
                  <tbody v-if="contactDetail.orders && contactDetail.orders.length">
                    <tr v-for="row in contactDetail.orders" :key="row.name">
                      <td><a href="#" class="sod-dlink crm-record-link" @click.prevent="openContactRelated('Sales Order', row.name)">{{ row.name }}</a></td>
                      <td><a href="#" class="sod-dlink crm-record-link" @click.prevent="openContactRelated('Sales Order', row.name)">{{ row.customer_name || contactDetail.company_name || '—' }}</a></td>
                      <td>{{ formatValue(row.grand_total, 'grand_total') }}</td>
                      <td><span class="ccd-status-text">{{ row.status || '—' }}</span></td>
                      <td><span class="ccd-status-ok">{{ row.custom_revenue_recognition_date ? 'Đã ghi' : 'Chưa ghi' }}</span></td>
                      <td><a href="#" class="sod-dlink" @click.prevent>{{ row.owner || '—' }}</a></td>
                      <td>{{ row.company || '—' }}</td>
                      <td>{{ formatValue(row.transaction_date, 'date') }}</td>
                      <td>{{ formatValue(row.custom_revenue_recognition_date || row.transaction_date, 'date') }}</td>
                    </tr>
                  </tbody>
                </table>
                <div v-if="!contactDetail.orders || !contactDetail.orders.length" class="ccd-empty-tab"><CRMIcon name="order" /><span>Không có bản ghi nào</span></div>
              </div>
              <footer class="ccd-related-footer">
                <strong>Tổng số {{ (contactDetail.orders || []).length }}</strong>
                <span class="ccd-related-page"><span>Số dòng/trang</span><b>20</b><span>1 - {{ (contactDetail.orders || []).length || 1 }}</span><button disabled>‹</button><button disabled>›</button></span>
              </footer>
            </div>
          </div>

          <!-- Quotations tab -->
          <div v-else-if="contactDetailTab === 'quotations'" class="ccd-attach-view">
            <div class="ccd-attach-card">
              <div class="ccd-attach-head">
                <div class="ccd-attach-title">Báo giá <button class="ccd-title-refresh" type="button" @click="loadContactDetail(contactDetailName)"><CRMIcon name="refresh" /></button></div>
                <div class="ccd-attach-actions"><button class="ccd-attach-btn primary" type="button" @click="notifyContactTabAction('Chọn báo giá')">Chọn</button></div>
              </div>
              <div class="ccd-attach-tablewrap">
                <table class="ccd-attach-table">
                  <thead><tr><th>Số báo giá</th><th>Ngày báo giá</th><th>Hiệu lực đến ngày</th><th>Tổng tiền</th><th>Tình trạng</th><th>Mô tả</th></tr></thead>
                  <tbody v-if="contactDetail.quotations && contactDetail.quotations.length">
                    <tr v-for="row in contactDetail.quotations" :key="row.name">
                      <td><a href="#" class="sod-dlink crm-record-link" @click.prevent="openContactRelated('Quotation', row.name)">{{ row.name }}</a></td>
                      <td>{{ formatValue(row.transaction_date, 'date') }}</td>
                      <td>{{ formatValue(row.valid_till, 'date') }}</td>
                      <td>{{ formatValue(row.grand_total, 'grand_total') }}</td>
                      <td><span class="ccd-status-text">{{ row.status || '—' }}</span></td>
                      <td>{{ row.title || row.party_name || '—' }}</td>
                    </tr>
                  </tbody>
                </table>
                <div v-if="!contactDetail.quotations || !contactDetail.quotations.length" class="ccd-empty-tab"><CRMIcon name="quotation" /><span>Không có bản ghi nào</span></div>
              </div>
              <footer class="ccd-related-footer">
                <strong>Tổng số {{ (contactDetail.quotations || []).length }}</strong>
                <span class="ccd-related-page"><span>Số dòng/trang</span><b>20</b><span>1 - {{ (contactDetail.quotations || []).length || 1 }}</span><button disabled>‹</button><button disabled>›</button></span>
              </footer>
            </div>
          </div>

          <!-- Invoices tab -->
          <div v-else-if="contactDetailTab === 'invoices'" class="ccd-attach-view">
            <div class="ccd-attach-card">
              <div class="ccd-attach-head">
                <div class="ccd-attach-title">Hóa đơn <button class="ccd-title-refresh" type="button" @click="loadContactDetail(contactDetailName)"><CRMIcon name="refresh" /></button></div>
                <div class="ccd-attach-actions"><button class="ccd-attach-btn" type="button" @click="notifyContactTabAction('Thêm Hóa đơn')">+ Thêm Hóa đơn</button></div>
              </div>
              <div class="ccd-attach-tablewrap">
                <table class="ccd-attach-table">
                  <thead><tr><th>Số hóa đơn</th><th>Diễn giải</th><th>Tổng tiền</th><th>Còn phải thu</th><th>Tình trạng</th><th>Người thực hiện</th><th>Đơn vị</th><th>Ngày hóa đơn</th><th>Hạn thanh toán</th></tr></thead>
                  <tbody v-if="contactDetail.invoices && contactDetail.invoices.length">
                    <tr v-for="row in contactDetail.invoices" :key="row.name">
                      <td><a href="#" class="sod-dlink crm-record-link" @click.prevent="openContactRelated('Sales Invoice', row.name)">{{ row.name }}</a></td>
                      <td><a href="#" class="sod-dlink crm-record-link" @click.prevent="openContactRelated('Sales Invoice', row.name)">{{ row.customer_name || contactDetail.company_name || '—' }}</a></td>
                      <td>{{ formatValue(row.grand_total, 'grand_total') }}</td>
                      <td>{{ formatValue(row.outstanding_amount, 'grand_total') }}</td>
                      <td><span class="ccd-status-text">{{ row.status || '—' }}</span></td>
                      <td><a href="#" class="sod-dlink" @click.prevent>{{ row.owner || '—' }}</a></td>
                      <td>{{ row.company || '—' }}</td>
                      <td>{{ formatValue(row.posting_date, 'date') }}</td>
                      <td>{{ formatValue(row.due_date, 'date') }}</td>
                    </tr>
                  </tbody>
                </table>
                <div v-if="!contactDetail.invoices || !contactDetail.invoices.length" class="ccd-inline-empty">Không có bản ghi nào <button type="button" @click="notifyContactTabAction('Thêm Hóa đơn')">+ Thêm Hóa đơn</button></div>
              </div>
              <footer class="ccd-related-footer">
                <strong>Tổng số {{ (contactDetail.invoices || []).length }}</strong>
                <span class="ccd-related-page"><span>Số dòng/trang</span><b>20</b><span>1 - {{ (contactDetail.invoices || []).length || 1 }}</span><button disabled>‹</button><button disabled>›</button></span>
              </footer>
            </div>
          </div>

          <!-- Campaigns / activity style empty tabs -->
          <div v-else-if="contactDetailTab === 'campaigns'" class="ccd-attach-view">
            <div class="ccd-attach-card ccd-short-card">
              <div class="ccd-attach-title">Chiến dịch <button class="ccd-title-refresh" type="button" @click="loadContactDetail(contactDetailName)"><CRMIcon name="refresh" /></button></div>
              <div class="ccd-inline-empty">Không có bản ghi nào <button type="button" @click="notifyContactTabAction('Chọn chiến dịch')">Chọn</button></div>
            </div>
          </div>

          <div v-else-if="contactDetailTab === 'active_tasks'" class="ccd-attach-view">
            <div class="ccd-attach-card ccd-short-card">
              <div class="ccd-attach-head">
                <div class="ccd-attach-title">Công việc đang thực hiện <button class="ccd-title-refresh" type="button" @click="loadContactDetail(contactDetailName)"><CRMIcon name="refresh" /></button></div>
                <div v-if="contactDetail.can_create_activity" class="ccd-activity-actions">
                  <button type="button" @click="openContactActivityDialog('task')"><CRMIcon name="task" /> Thêm Nhiệm vụ</button>
                  <button type="button" @click="openContactActivityDialog('meeting')"><CRMIcon name="calendar" /> Thêm Lịch hẹn</button>
                  <button type="button" @click="openContactActivityDialog('call')"><CRMIcon name="phone" /> Thêm Cuộc gọi</button>
                </div>
              </div>
              <div v-if="contactActiveActivities.length" class="ccd-activity-table-wrap">
                <table class="ccd-attach-table misa-activity-table">
                  <thead><tr><th>Tên hoạt động</th><th>Loại hoạt động</th><th>Hạn hoàn thành</th><th>Trạng thái</th><th>Ngày kết thúc</th><th>Người thực hiện</th></tr></thead>
                  <tbody><tr v-for="activity in contactActiveActivities" :key="activity.activity_type + '-' + activity.name">
                    <td><a href="#" class="sod-dlink" @click.prevent="openActivityRecord(activity.name, activity.activity_type === 'task' ? 'ToDo' : 'Event')">{{ activity.subject || activity.name }}</a></td>
                    <td>{{ contactActivityTypeLabel(activity.activity_type) }}</td>
                    <td>{{ formatContactActivityDate(activity.activity_type === 'task' ? activity.due_date : activity.starts_on) }}</td>
                    <td><span class="misa-activity-status" :class="'status-' + String(activity.status || '').toLowerCase()">{{ contactActivityStatusLabel(activity.status) }}</span></td>
                    <td>{{ formatContactActivityDate(activity.ends_on) }}</td>
                    <td>{{ activity.performed_by_name || activity.performed_by || '—' }}</td>
                  </tr></tbody>
                </table>
              </div>
              <div v-else class="ccd-empty-tab"><CRMIcon name="task" /><span>Không có bản ghi nào</span></div>
              <footer class="ccd-related-footer"><strong>Tổng số {{ contactActiveActivities.length }}</strong></footer>
            </div>
          </div>

          <div v-else-if="contactDetailTab === 'done_tasks'" class="ccd-attach-view">
            <div class="ccd-attach-card ccd-short-card">
              <div class="ccd-attach-title">Công việc đã hoàn thành <button class="ccd-title-refresh" type="button" @click="loadContactDetail(contactDetailName)"><CRMIcon name="refresh" /></button></div>
              <div v-if="contactDoneActivities.length" class="ccd-activity-table-wrap">
                <table class="ccd-attach-table misa-activity-table">
                  <thead><tr><th>Tên hoạt động</th><th>Loại hoạt động</th><th>Hạn hoàn thành</th><th>Trạng thái</th><th>Ngày kết thúc</th><th>Người thực hiện</th></tr></thead>
                  <tbody><tr v-for="activity in contactDoneActivities" :key="activity.activity_type + '-' + activity.name">
                    <td><a href="#" class="sod-dlink" @click.prevent="openActivityRecord(activity.name, activity.activity_type === 'task' ? 'ToDo' : 'Event')">{{ activity.subject || activity.name }}</a></td>
                    <td>{{ contactActivityTypeLabel(activity.activity_type) }}</td>
                    <td>{{ formatContactActivityDate(activity.activity_type === 'task' ? activity.due_date : activity.starts_on) }}</td>
                    <td><span class="misa-activity-status" :class="'status-' + String(activity.status || '').toLowerCase()">{{ contactActivityStatusLabel(activity.status) }}</span></td>
                    <td>{{ formatContactActivityDate(activity.ends_on) }}</td>
                    <td>{{ activity.performed_by_name || activity.performed_by || '—' }}</td>
                  </tr></tbody>
                </table>
              </div>
              <div v-else class="ccd-empty-tab"><CRMIcon name="task" /><span>Không có bản ghi nào</span></div>
              <footer class="ccd-related-footer"><strong>Tổng số {{ contactDoneActivities.length }}</strong></footer>
            </div>
          </div>

          <div v-else-if="['consult_cards','email','sms','routes','other'].includes(contactDetailTab)" class="ccd-attach-view">
            <div class="ccd-attach-card ccd-short-card">
              <div class="ccd-attach-title">{{ contactDetailTabLabel(contactDetailTab) }} <button class="ccd-title-refresh" type="button" @click="loadContactDetail(contactDetailName)"><CRMIcon name="refresh" /></button></div>
              <div class="ccd-inline-empty">Không có bản ghi nào <button v-if="contactDetailTab === 'consult_cards' || contactDetailTab === 'routes'" type="button" @click="notifyContactTabAction('Thêm ' + contactDetailTabLabel(contactDetailTab))">+ Thêm</button></div>
            </div>
          </div>

          <div v-else-if="contactDetailTab === 'conversations'" class="ccd-attach-view">
            <div class="ccd-attach-card ccd-conversation-card">
              <div class="ccd-attach-title">Nội dung trao đổi</div>
              <div v-if="contactDetail.notes && contactDetail.notes.length" class="ccd-conversation-list">
                <article v-for="n in contactDetail.notes" :key="n.name" class="ccd-conversation-item">
                  <div class="ccd-conversation-avatar">{{ (n.comment_by_fullname || n.comment_by || '?')[0].toUpperCase() }}</div>
                  <div><strong>{{ n.comment_by_fullname || n.comment_by }}</strong><p>{{ stripHtml(n.content || '') }}</p><small>{{ formatValue(n.creation, 'creation') }}</small></div>
                </article>
              </div>
              <div class="ccd-conversation-input"><input placeholder="Nhập nội dung"><button type="button" @click="notifyContactTabAction('Gửi nội dung trao đổi')"><CRMIcon name="send" /></button></div>
            </div>
          </div>

        </div>
      </div>

      <!-- RIGHT panel -->
      <div class="ccd-right">
        <div class="ccd-right-toolbar" aria-label="Thao tác nhanh của liên hệ">
          <button class="ccd-right-icon-btn" type="button" title="Gọi điện" aria-label="Gọi điện" @click="callContactPhone">
            <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5.2 2.8 7 6.3 5.6 7.5c.9 2 2.5 3.6 4.5 4.5l1.3-1.5 3.5 1.8-.6 2.4c-.2.7-.9 1.1-1.6 1-5.4-.8-9.6-5-10.4-10.4-.1-.7.3-1.4 1-1.6l1.9-.9Z"/></svg>
          </button>
          <button class="ccd-right-icon-btn" type="button" title="Thêm nhiệm vụ" aria-label="Thêm nhiệm vụ" @click="openContactActivityDialog('task')">
            <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="3" width="10" height="13" rx="1.5"/><path d="M7 3V2h4v1M6.5 8l1.3 1.3L11.5 6M7 13h4"/></svg>
          </button>
          <button class="ccd-right-icon-btn" type="button" title="Thêm lịch hẹn" aria-label="Thêm lịch hẹn" @click="openContactActivityDialog('meeting')">
            <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2.5" y="4" width="13" height="11.5" rx="1.5"/><path d="M5.5 2v4M12.5 2v4M2.5 7.5h13"/></svg>
          </button>
          <button class="ccd-right-icon-btn" type="button" title="Gửi email" aria-label="Gửi email" @click="emailContact">
            <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="14" height="10" rx="1.5"/><path d="m3 5 6 5 6-5"/></svg>
          </button>
          <button class="ccd-right-icon-btn" type="button" title="Trao đổi" aria-label="Trao đổi" @click="contactDetailTab='conversations'">
            <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3.5h12v9H8l-3.5 2.5v-2.5H3v-9Z"/><path d="M6 7.5h6M6 10h4"/></svg>
          </button>
          <button class="ccd-right-icon-btn" type="button" title="Làm mới" aria-label="Làm mới" @click="loadContactDetail(contactDetailName)">
            <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 5A6.2 6.2 0 1 0 15 9"/><path d="M14.5 2v3.5H11"/></svg>
          </button>
        </div>
        <div class="ccd-right-tabs">
          <button :class="{active: contactRightTab==='activity'}" @click="contactRightTab='activity'">Hoạt động</button>
          <button :class="{active: contactRightTab==='sales'}"    @click="contactRightTab='sales'">Mua hàng</button>
        </div>
        <div class="ccd-right-content">
          <div v-if="contactRightTab === 'activity' && ((contactDetail.notes || []).length || contactActivities.length)" class="ccd-right-feed">
            <article v-for="n in contactDetail.notes || []" :key="'note-' + n.name">
              <strong>{{ n.comment_by_fullname || n.comment_by || 'Ghi chú' }}</strong>
              <p>{{ stripHtml(n.content || '') }}</p>
              <small>{{ formatValue(n.creation, 'creation') }}</small>
            </article>
            <article v-for="activity in contactActivities" :key="activity.activity_type + '-' + activity.name" class="ccd-feed-link" role="button" tabindex="0" @click="openActivityRecord(activity.name, activity.activity_type === 'task' ? 'ToDo' : 'Event')" @keydown.enter.prevent="openActivityRecord(activity.name, activity.activity_type === 'task' ? 'ToDo' : 'Event')">
              <strong>{{ activity.subject || activity.name }}</strong>
              <p>{{ contactActivityTypeLabel(activity.activity_type) }} · {{ contactActivityStatusLabel(activity.status) }}</p>
              <small>{{ activity.performed_by_name || activity.performed_by || '—' }} · {{ formatContactActivityDate(activity.creation || activity.starts_on || activity.due_date) }}</small>
            </article>
          </div>
          <div v-else-if="contactRightTab === 'sales' && ((contactDetail.orders || []).length || (contactDetail.quotations || []).length || (contactDetail.invoices || []).length)" class="ccd-right-feed">
            <article v-for="row in contactDetail.orders || []" :key="'so-' + row.name">
              <strong>{{ row.name }}</strong>
              <p>Đơn hàng · {{ formatValue(row.grand_total, 'grand_total') }}</p>
              <small>{{ formatValue(row.transaction_date, 'date') }}</small>
            </article>
            <article v-for="row in contactDetail.quotations || []" :key="'qt-' + row.name">
              <strong>{{ row.name }}</strong>
              <p>Báo giá · {{ formatValue(row.grand_total, 'grand_total') }}</p>
              <small>{{ formatValue(row.transaction_date, 'date') }}</small>
            </article>
            <article v-for="row in contactDetail.invoices || []" :key="'si-' + row.name">
              <strong>{{ row.name }}</strong>
              <p>Hóa đơn · {{ formatValue(row.grand_total, 'grand_total') }}</p>
              <small>{{ formatValue(row.posting_date, 'date') }}</small>
            </article>
          </div>
          <div v-else class="ccd-right-empty">
            <svg viewBox="0 0 64 64" width="44" height="44" fill="none"><circle cx="32" cy="32" r="26" stroke="#e5e7eb" stroke-width="2"/><path d="M22 30h20M22 37h12" stroke="#d1d5db" stroke-width="2" stroke-linecap="round"/></svg>
            <span>Không có dữ liệu</span>
          </div>
        </div>
      </div>

    </div>

    <!-- Activity modal: nhiệm vụ / lịch hẹn / cuộc gọi -->
    <div v-if="contactActivityDialogOpen" class="crm-modal-backdrop misa-activity-backdrop" @click.self="closeContactActivityDialog">
      <form class="crm-modal misa-activity-modal" @submit.prevent="saveContactActivity">
        <header>
          <h2>Thêm {{ contactActivityTypeLabel(contactActivityForm.activity_type).toLowerCase() }}</h2>
          <div><button type="button" title="Đóng" aria-label="Đóng" @click="closeContactActivityDialog">×</button></div>
        </header>
        <div class="misa-activity-form">
          <label><span>Tiêu đề <b>*</b></span><input v-model="contactActivityForm.subject" required autofocus></label>
          <label><span>Mô tả</span><textarea v-model="contactActivityForm.description"></textarea></label>

          <label v-if="contactActivityMoreOpen && contactActivityForm.activity_type === 'call'"><span>Điện thoại</span><input v-model="contactActivityForm.phone" type="tel"></label>
          <template v-if="contactActivityMoreOpen">
            <label><span>Liên hệ</span><input :value="contactDetail.full_name || contactDetail.name" readonly></label>
            <label><span>Chiến dịch</span><select v-model="contactActivityForm.campaign"><option value="">- Không chọn -</option><option v-for="campaign in contactDetail.activity_campaigns || []" :key="campaign.name" :value="campaign.name">{{ campaign.name }}</option></select></label>
            <label><span>Người thực hiện</span><select v-model="contactActivityForm.allocated_to"><option v-for="user in contactDetail.activity_users || []" :key="user.name" :value="user.name">{{ user.full_name || user.name }}</option></select></label>
            <label><span>Người liên quan</span><select v-model="contactActivityForm.related_to"><option value="">- Không chọn -</option><option v-for="user in contactDetail.activity_users || []" :key="'contact-related-' + user.name" :value="user.name">{{ user.full_name || user.name }}</option></select></label>
          </template>

          <template v-if="contactActivityForm.activity_type === 'meeting'">
            <label><span>Địa điểm</span><input v-model="contactActivityForm.location"></label>
            <label class="misa-activity-check"><span>Cả ngày</span><input v-model.number="contactActivityForm.all_day" type="checkbox" :true-value="1" :false-value="0"></label>
            <label><span>Ngày bắt đầu <b>*</b></span><input v-model="contactActivityForm.starts_on" type="datetime-local" required></label>
            <label><span>Ngày kết thúc <b>*</b></span><input v-model="contactActivityForm.ends_on" type="datetime-local" required></label>
            <label><span>Trạng thái <b>*</b></span><select v-model="contactActivityForm.status"><option value="Open">Chưa bắt đầu</option><option value="Closed">Hoàn thành</option><option value="Cancelled">Đã hủy</option></select></label>
          </template>

          <template v-else-if="contactActivityForm.activity_type === 'task'">
            <label><span>Hạn hoàn thành</span><span class="misa-activity-date-pair"><input v-model="contactActivityForm.due_date" type="date"><input v-model="contactActivityForm.due_time" type="time"></span></label>
            <label v-if="contactActivityMoreOpen"><span>Mức độ ưu tiên <b>*</b></span><select v-model="contactActivityForm.priority"><option value="Medium">Không xác định</option><option value="High">Cao</option><option value="Low">Thấp</option></select></label>
            <label><span>Trạng thái <b>*</b></span><select v-model="contactActivityForm.status"><option value="Open">Chưa bắt đầu</option><option value="Closed">Hoàn thành</option><option value="Cancelled">Đã hủy</option></select></label>
            <label v-if="contactActivityMoreOpen"><span>Loại nhiệm vụ</span><select v-model="contactActivityForm.task_type"><option value="">- Không chọn -</option><option value="Chăm sóc khách hàng">Chăm sóc khách hàng</option><option value="Theo dõi liên hệ">Theo dõi liên hệ</option><option value="Gọi xác nhận">Gọi xác nhận</option><option value="Khác">Khác</option></select></label>
          </template>

          <template v-else>
            <label><span>Ngày bắt đầu <b>*</b></span><input v-model="contactActivityForm.starts_on" type="datetime-local" required @input="updateContactCallEnd"></label>
            <label><span>Thời gian gọi <b>*</b></span><span class="misa-call-duration"><input v-model.number="contactActivityForm.call_minutes" min="0" type="number" @input="updateContactCallEnd"><small>Phút</small><input v-model.number="contactActivityForm.call_seconds" min="0" max="59" type="number" @input="updateContactCallEnd"><small>Giây</small></span></label>
            <label><span>Ngày kết thúc <b>*</b></span><input :value="contactActivityForm.ends_on" type="datetime-local" readonly></label>
            <label v-if="contactActivityMoreOpen"><span>Loại cuộc gọi <b>*</b></span><select v-model="contactActivityForm.call_type"><option value="Gọi đi">Gọi đi</option><option value="Gọi đến">Gọi đến</option></select></label>
            <label><span>Trạng thái <b>*</b></span><select v-model="contactActivityForm.status"><option value="Open">Chưa bắt đầu</option><option value="Closed">Hoàn thành</option><option value="Cancelled">Đã hủy</option></select></label>
            <label><span>Kết quả gọi điện</span><select v-model="contactActivityForm.call_result"><option value="">- Không chọn -</option><option value="Liên hệ thành công">Liên hệ thành công</option><option value="Không nghe máy">Không nghe máy</option><option value="Hẹn gọi lại">Hẹn gọi lại</option><option value="Sai số">Sai số</option></select></label>
          </template>
        </div>
        <footer>
          <button v-if="!contactActivityMoreOpen" class="misa-activity-more" type="button" @click="contactActivityMoreOpen = true">Thông tin khác</button>
          <button v-else class="misa-activity-more" type="button" @click="contactActivityMoreOpen = false">Thu gọn</button>
          <button class="crm-button" type="button" :disabled="contactActivitySaving" @click="closeContactActivityDialog">Hủy</button>
          <button v-if="contactActivityMoreOpen && contactActivityForm.activity_type === 'task'" class="crm-button misa-save-close" type="submit" :disabled="contactActivitySaving || !contactActivityForm.subject?.trim()">Lưu và đóng</button>
          <button class="crm-button primary" type="submit" :disabled="contactActivitySaving || !contactActivityForm.subject?.trim()">{{ contactActivitySaving ? 'Đang lưu...' : 'Lưu' }}</button>
        </footer>
      </form>
    </div>

    <!-- Opportunity picker modal (Chọn cơ hội) -->
    <div v-if="oppPickerOpen" class="ccd-oppk-backdrop" @click.self="closeOppPicker">
      <div class="ccd-oppk-modal">
        <header class="ccd-oppk-head">
          <h2>Chọn cơ hội</h2>
          <button class="ccd-oppk-close" @click="closeOppPicker">×</button>
        </header>
        <div class="ccd-oppk-search">
          <svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="7" cy="7" r="4.5"/><path d="M11 11l3 3" stroke-linecap="round"/></svg>
          <input v-model="oppPickerSearch" @input="onOppPickerSearch" placeholder="Tìm kiếm" />
        </div>
        <div class="ccd-oppk-body">
          <table class="ccd-attach-table ccd-oppk-table">
            <thead>
              <tr>
                <th class="ccd-oppk-chk"><input type="checkbox" :checked="oppPickerAllChecked" @change="toggleOppPickerAll" /></th>
                <th>Tên cơ hội</th>
                <th>Liên hệ</th>
                <th>Số tiền</th>
                <th>Giai đoạn</th>
                <th>Ngày kỳ vọng/kết thúc</th>
                <th>Loại hàng hóa</th>
                <th>Người thực hiện</th>
                <th>Ngày tạo</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="o in oppPickerRows" :key="o.name" :class="{ selected: isOppPicked(o.name) }" @click="toggleOppPickerRow(o.name)">
                <td class="ccd-oppk-chk"><input type="checkbox" :checked="isOppPicked(o.name)" @click.stop="toggleOppPickerRow(o.name)" /></td>
                <td>{{ o.title || o.name }}</td>
                <td>{{ o.contact_display || '—' }}</td>
                <td>{{ formatValue(o.opportunity_amount, 'opportunity_amount') }}</td>
                <td>{{ o.sales_stage || '—' }}</td>
                <td>{{ formatValue(o.expected_closing, 'date') }}</td>
                <td>{{ o.opportunity_type || '—' }}</td>
                <td>{{ o.opportunity_owner || '—' }}</td>
                <td>{{ formatValue(o.creation, 'creation') }}</td>
              </tr>
              <tr v-if="!oppPickerRows.length && !oppPickerLoading"><td colspan="9" class="ccd-oppk-empty">Không có cơ hội</td></tr>
              <tr v-if="oppPickerLoading"><td colspan="9" class="ccd-oppk-empty">Đang tải…</td></tr>
            </tbody>
          </table>
        </div>
        <div class="ccd-oppk-foot">
          <div class="ccd-oppk-total">Tổng số <b>{{ oppPickerTotal }}</b><span v-if="oppPickerSelected.length"> · Đã chọn {{ oppPickerSelected.length }}</span></div>
          <div class="ccd-oppk-pager">
            <span>{{ oppPickerTotal ? ((oppPickerPage-1)*oppPickerPageLength)+1 : 0 }} - {{ Math.min(oppPickerPage*oppPickerPageLength, oppPickerTotal) }}</span>
            <button @click="oppPickerChangePage(-1)" :disabled="oppPickerPage<=1">‹</button>
            <button @click="oppPickerChangePage(1)" :disabled="oppPickerPage>=oppPickerPageCount">›</button>
          </div>
        </div>
        <footer class="ccd-oppk-actions">
          <button class="ccd-attach-btn" @click="closeOppPicker">Hủy</button>
          <button class="ccd-attach-btn primary" :disabled="!oppPickerSelected.length || oppPickerSaving" @click="confirmOppPicker">{{ oppPickerSaving ? 'Đang lưu…' : 'Tiếp theo' }}</button>
        </footer>
      </div>
    </div>

  </template>
</div>
`;
