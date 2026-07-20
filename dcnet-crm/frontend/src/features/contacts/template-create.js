export default `
<!-- ════════ TẠO LIÊN HỆ ════════ -->
<div v-else-if="route === 'create-contact'" class="ccf-page">

  <!-- Header -->
  <div class="ccf-header">
    <div class="ccf-header-left">
      <button class="ccf-btn-back" @click="cancelCreateContact" title="Quay lại">
        <svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 3L5 8l5 5"/></svg>
      </button>
      <h1 class="ccf-title">Thêm Liên hệ</h1>
      <span class="ccf-template-label">Mẫu tiêu chuẩn</span>
    </div>
    <div class="ccf-header-actions">
      <button class="ccf-btn-ghost" @click="cancelCreateContact" :disabled="createContactSaving">Hủy</button>
      <button class="ccf-btn-secondary" @click="saveCreateContact(true)" :disabled="createContactSaving">Lưu và thêm</button>
      <button class="ccf-btn-primary" @click="saveCreateContact(false)" :disabled="createContactSaving">
        <span v-if="createContactSaving">Đang lưu...</span>
        <span v-else>Lưu</span>
      </button>
    </div>
  </div>

  <!-- Form body -->
  <div class="ccf-body">
    <div class="ccf-card">

      <!-- Thông tin chung -->
      <div class="ccf-section">
        <div class="ccf-section-title">Thông tin chung</div>
        <div class="ccf-grid">
          <div class="ccf-field">
            <label class="ccf-label">Mã liên hệ</label>
            <input class="ccf-input ccf-input--readonly" value="Mã tự sinh" disabled placeholder="Mã tự sinh" />
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Xưng hô</label>
            <select class="ccf-select" v-model="createContactForm.salutation">
              <option value="">- Không chọn -</option>
              <option v-for="opt in contactCreateOptions.salutations" :key="opt.name" :value="opt.name">{{ opt.name }}</option>
            </select>
          </div>

          <div class="ccf-field">
            <label class="ccf-label">Họ và đệm</label>
            <input class="ccf-input" v-model="createContactForm.last_name" placeholder="Họ và đệm" />
          </div>
          <div class="ccf-field ccf-required">
            <label class="ccf-label">Tên</label>
            <input class="ccf-input" v-model="createContactForm.first_name" placeholder="Tên" />
          </div>

          <div class="ccf-field">
            <label class="ccf-label">Họ và tên</label>
            <input class="ccf-input ccf-input--readonly" :value="((createContactForm.last_name || '') + ' ' + (createContactForm.first_name || '')).trim()" disabled placeholder="Tự động ghép" />
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Chức danh</label>
            <input class="ccf-input" v-model="createContactForm.designation" placeholder="Nhập chức danh tại khách hàng">
          </div>

          <div class="ccf-field">
            <label class="ccf-label">Phòng ban</label>
            <input class="ccf-input" v-model="createContactForm.department" placeholder="Nhập phòng ban tại khách hàng">
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Tổ chức</label>
            <select class="ccf-select" v-model="createContactForm.customer">
              <option value="">- Không chọn -</option>
              <option v-for="opt in contactCreateOptions.customers" :key="opt.name" :value="opt.name">{{ opt.customer_name || opt.name }}</option>
            </select>
          </div>

          <div class="ccf-field">
            <label class="ccf-label">Phân loại khách hàng</label>
            <select class="ccf-select" v-model="createContactForm.phan_loai_kh">
              <option value="">- Không chọn -</option>
              <option>Khách hàng</option>
              <option>Nhà cung cấp</option>
              <option>Đối tác</option>
              <option>Khác</option>
            </select>
          </div>
          <div class="ccf-field ccf-field--checkbox">
            <label class="ccf-checkbox-label">
              <input type="checkbox" v-model="createContactForm.khong_goi_dien" :true-value="1" :false-value="0" />
              <span>Không gọi điện</span>
            </label>
          </div>

          <div class="ccf-field ccf-field--checkbox">
            <label class="ccf-checkbox-label">
              <input type="checkbox" v-model="createContactForm.khong_gui_email" :true-value="1" :false-value="0" />
              <span>Không gửi Email</span>
            </label>
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Điện thoại khác</label>
            <input class="ccf-input" v-model="createContactForm.dien_thoai_khac" placeholder="Số điện thoại khác" />
          </div>

          <div class="ccf-field">
            <label class="ccf-label">ĐT di động</label>
            <input class="ccf-input" v-model="createContactForm.mobile_no" placeholder="Số di động" />
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Email cá nhân</label>
            <input class="ccf-input" type="email" v-model="createContactForm.email_ca_nhan" placeholder="email@gmail.com" />
          </div>

          <div class="ccf-field">
            <label class="ccf-label">ĐT cơ quan</label>
            <input class="ccf-input" v-model="createContactForm.phone" placeholder="Số cơ quan" />
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Nguồn gốc</label>
            <select class="ccf-select" v-model="createContactForm.nguon_goc">
              <option value="">- Không chọn -</option>
              <option>Gọi điện</option>
              <option>Trực tiếp</option>
              <option>Giới thiệu</option>
              <option>Mạng xã hội</option>
              <option>Email</option>
              <option>Khác</option>
            </select>
          </div>

          <div class="ccf-field">
            <label class="ccf-label">Email cơ quan</label>
            <input class="ccf-input" type="email" v-model="createContactForm.email_id" placeholder="email@company.com" />
          </div>
          <div class="ccf-field"></div>

          <div class="ccf-field">
            <label class="ccf-label">Zalo</label>
            <input class="ccf-input" v-model="createContactForm.zalo" placeholder="Số Zalo" />
          </div>
          <div class="ccf-field"></div>
        </div>
      </div>

      <!-- Thông tin địa chỉ -->
      <div class="ccf-section">
        <div class="ccf-section-title">Thông tin địa chỉ</div>
        <div class="ccf-grid">
          <div class="ccf-field">
            <label class="ccf-label">Quốc gia</label>
            <select class="ccf-select" v-model="ccBillingForm.country">
              <option value="Vietnam">Việt Nam</option>
              <option v-for="opt in contactCreateOptions.countries" :key="opt.name" :value="opt.name">{{ opt.name }}</option>
            </select>
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Tỉnh/Thành phố</label>
            <select class="ccf-select" v-model="ccBillingProvinceCode">
              <option value="">- Không chọn -</option>
              <option v-for="p in ccVnProvinces" :key="p.code" :value="String(p.code)">{{ p.name }}</option>
            </select>
          </div>

          <div class="ccf-field">
            <label class="ccf-label">Phường/Xã</label>
            <select class="ccf-select" v-model="ccBillingForm.county" :disabled="!ccBillingProvinceCode || ccLoadingBillingWards">
              <option value="">{{ ccLoadingBillingWards ? 'Đang tải...' : '- Không chọn -' }}</option>
              <option v-for="w in ccVnBillingWards" :key="w.code" :value="w.name">{{ w.name }}</option>
            </select>
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Mã vùng</label>
            <input class="ccf-input" v-model="ccBillingForm.pincode" placeholder="Mã bưu chính" />
          </div>

          <div class="ccf-field ccf-span2">
            <label class="ccf-label">Số nhà, Đường phố</label>
            <input class="ccf-input" v-model="ccBillingForm.address_line1" placeholder="Số nhà, tên đường" />
          </div>
        </div>
      </div>

      <!-- Thông tin địa chỉ giao hàng -->
      <div class="ccf-section">
        <div class="ccf-section-title">
          <span>Thông tin địa chỉ giao hàng</span>
          <button type="button" class="ccf-copy-addr-btn" @click="copyContactAddress">
            <svg viewBox="0 0 16 16" width="13" height="13" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="5" y="5" width="9" height="9" rx="1.5"/><path d="M11 5V3a1.5 1.5 0 0 0-1.5-1.5H3A1.5 1.5 0 0 0 1.5 3v6.5A1.5 1.5 0 0 0 3 11h2"/></svg>
            Sao chép địa chỉ
          </button>
        </div>
        <div class="ccf-grid">
          <div class="ccf-field">
            <label class="ccf-label">Quốc gia (Giao hàng)</label>
            <select class="ccf-select" v-model="ccShippingForm.country">
              <option value="Vietnam">Việt Nam</option>
              <option v-for="opt in contactCreateOptions.countries" :key="opt.name" :value="opt.name">{{ opt.name }}</option>
            </select>
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Tỉnh/Thành phố (Giao hàng)</label>
            <select class="ccf-select" v-model="ccShippingProvinceCode">
              <option value="">- Không chọn -</option>
              <option v-for="p in ccVnProvinces" :key="p.code" :value="String(p.code)">{{ p.name }}</option>
            </select>
          </div>

          <div class="ccf-field">
            <label class="ccf-label">Phường/Xã (Giao hàng)</label>
            <select class="ccf-select" v-model="ccShippingForm.county" :disabled="!ccShippingProvinceCode || ccLoadingShippingWards">
              <option value="">{{ ccLoadingShippingWards ? 'Đang tải...' : '- Không chọn -' }}</option>
              <option v-for="w in ccVnShippingWards" :key="w.code" :value="w.name">{{ w.name }}</option>
            </select>
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Mã vùng (Giao hàng)</label>
            <input class="ccf-input" v-model="ccShippingForm.pincode" placeholder="Mã bưu chính" />
          </div>

          <div class="ccf-field ccf-span2">
            <label class="ccf-label">Số nhà, Đường phố (Giao hàng)</label>
            <input class="ccf-input" v-model="ccShippingForm.address_line1" placeholder="Số nhà, tên đường" />
          </div>
        </div>
      </div>

      <!-- Thông tin mô tả -->
      <div class="ccf-section">
        <div class="ccf-section-title">Thông tin mô tả</div>
        <div class="ccf-grid">
          <div class="ccf-field ccf-span2">
            <label class="ccf-label">Mô tả</label>
            <textarea class="ccf-textarea" v-model="createContactForm.mo_ta" rows="3" placeholder="Ghi chú về liên hệ..."></textarea>
          </div>
        </div>
      </div>

      <!-- Thông tin hệ thống -->
      <div class="ccf-section">
        <div class="ccf-section-title">Thông tin hệ thống</div>
        <div class="ccf-grid">
          <div class="ccf-field ccf-field--checkbox">
            <label class="ccf-checkbox-label">
              <input type="checkbox" v-model="createContactForm.dung_chung" :true-value="1" :false-value="0" />
              <span>Dùng chung</span>
            </label>
          </div>
        </div>
      </div>

    </div>
  </div>
</div>
`;
