export default `
<!-- ════════ TẠO KHÁCH HÀNG ════════ -->
<div v-if="route === 'create-customer'" class="ccf-page">

  <!-- Header -->
  <div class="ccf-header">
    <div class="ccf-header-left">
      <button class="ccf-btn-back" @click="cancelCreateCustomer" title="Quay lại">
        <svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M10 3L5 8l5 5"/>
        </svg>
      </button>
      <h1 class="ccf-title">Thêm Khách hàng</h1>
      <div class="ccf-type-selector">
        <select class="ccf-type-select" v-model="createCustomerForm.customer_type" @change="createCustomerForm.la_kh_ca_nhan = createCustomerForm.customer_type === 'Individual' ? 1 : 0">
          <option value="Company">Khách hàng DN</option>
          <option value="Individual">Khách hàng cá nhân</option>
        </select>
        <svg class="ccf-type-chevron" viewBox="0 0 16 16" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6l4 4 4-4"/></svg>
      </div>
    </div>
    <div class="ccf-header-actions">
      <button class="ccf-btn-ghost" @click="cancelCreateCustomer" :disabled="createSaving">Hủy</button>
      <button class="ccf-btn-secondary" @click="saveCreateCustomer(true)" :disabled="createSaving">Lưu và thêm</button>
      <button class="ccf-btn-primary" @click="saveCreateCustomer(false)" :disabled="createSaving">
        <span v-if="createSaving">Đang lưu...</span>
        <span v-else>Lưu</span>
      </button>
    </div>
  </div>

  <!-- Form body -->
  <div class="ccf-body">

    <!-- AVA / MST Banner -->
    <div v-if="avaVisible" class="ccf-ava">
      <div class="ccf-ava-header">
        <div class="ccf-ava-icon">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/>
            <path d="M18 3l1.5 1.5M20.5 6H22M18 9l1.5-1.5" stroke-linecap="round"/>
          </svg>
        </div>
        <div class="ccf-ava-titles">
          <span class="ccf-ava-name">Tra cứu MST</span>
          <span class="ccf-ava-sub">Nhập mã số thuế để tự động điền thông tin doanh nghiệp</span>
        </div>
        <button class="ccf-ava-close" @click="dismissAva" title="Đóng">
          <svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <path d="M4 4l8 8M12 4l-8 8"/>
          </svg>
        </button>
      </div>
      <div class="ccf-ava-row">
        <input
          class="ccf-ava-input"
          v-model="avaInput"
          placeholder="Nhập MST doanh nghiệp (10 hoặc 13 số), ví dụ: 0319488060"
          @keyup.enter="sendAvaInput"
        />
        <button class="ccf-ava-send" @click="sendAvaInput" :disabled="!avaInput.trim() || taxLookupStatus === 'loading'" title="Tra cứu">
          <svg v-if="taxLookupStatus !== 'loading'" viewBox="0 0 16 16" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M2 8h12M10 4l4 4-4 4"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" class="ccf-spin">
            <circle cx="12" cy="12" r="10" stroke-dasharray="31 63"/>
          </svg>
        </button>
      </div>
      <div v-if="taxLookupStatus === 'duplicate' && taxLookupResult" class="ccf-ava-result ccf-ava-result--err">
        <svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M8 2l6 12H2z"/><path d="M8 7v3M8 12v.5"/></svg>
        <span>MST này đã có trong hệ thống: <strong>{{ taxLookupResult.existing_customer?.customer_name }}</strong> — vui lòng tìm và cập nhật khách hàng đó thay vì tạo mới.</span>
      </div>
      <div v-if="taxLookupStatus === 'found' && taxLookupResult" class="ccf-ava-result ccf-ava-result--ok">
        <svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8l3.5 3.5L13 5"/></svg>
        <span><strong>{{ taxLookupResult.name }}</strong> · {{ taxLookupResult.address }}</span>
        <span v-if="taxLookupResult.status" class="ccf-ava-status-badge">{{ taxLookupResult.status }}</span>
      </div>
      <div v-if="taxLookupStatus === 'found-inactive' && taxLookupResult" class="ccf-ava-result ccf-ava-result--err">
        <svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M8 2l6 12H2z"/><path d="M8 7v3M8 12v.5"/></svg>
        <span><strong>{{ taxLookupResult.name }}</strong> · {{ taxLookupResult.address }}</span>
        <span class="ccf-ava-status-badge ccf-ava-status-badge--err">{{ taxLookupResult.status }}</span>
      </div>
      <div v-if="taxLookupStatus === 'not-found'" class="ccf-ava-result ccf-ava-result--warn">
        <svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="8" cy="8" r="6"/><path d="M8 5v3M8 11v.5"/></svg>
        Không tìm thấy doanh nghiệp với MST này trên dữ liệu GDT
      </div>
      <div v-if="taxLookupStatus === 'error'" class="ccf-ava-result ccf-ava-result--err">
        <svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M8 2l6 12H2z"/><path d="M8 7v3M8 12v.5"/></svg>
        Lỗi kết nối dịch vụ tra cứu MST, vui lòng thử lại
      </div>
    </div>

    <div class="ccf-card">

      <!-- Thông tin chung -->
      <div class="ccf-section">
        <div class="ccf-section-title">Thông tin chung</div>
        <div class="ccf-grid">
          <!-- Left col -->
          <div class="ccf-field">
            <label class="ccf-label">Mã khách hàng</label>
            <input class="ccf-input ccf-input--readonly" value="Mã tự sinh" disabled placeholder="Mã tự sinh" />
          </div>
          <!-- Right col -->
          <div class="ccf-field ccf-required">
            <label class="ccf-label">Tên khách hàng</label>
            <input class="ccf-input" v-model="createCustomerForm.customer_name" placeholder="Nhập tên khách hàng" />
          </div>
          <!-- Left col -->
          <div class="ccf-field">
            <label class="ccf-label">Tên viết tắt</label>
            <input class="ccf-input" v-model="createCustomerForm.ten_viet_tat" placeholder="Tên viết tắt" />
          </div>
          <!-- Right col -->
          <div class="ccf-field">
            <label class="ccf-label">Mã số thuế</label>
            <div class="ccf-input-wrap">
              <input class="ccf-input" v-model="createCustomerForm.tax_id" placeholder="Nhập MST (tự động tra cứu)" />
              <span v-if="taxLookupStatus === 'loading'" class="ccf-tax-badge ccf-tax-badge--loading">
                <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5" class="ccf-spin"><circle cx="12" cy="12" r="9" stroke-dasharray="28 57"/></svg>
              </span>
              <span v-if="taxLookupStatus === 'found'" class="ccf-tax-badge ccf-tax-badge--ok">
                <svg viewBox="0 0 16 16" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8l3.5 3.5L13 5"/></svg>
              </span>
              <span v-if="taxLookupStatus === 'found-inactive'" class="ccf-tax-badge ccf-tax-badge--err">
                <svg viewBox="0 0 16 16" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M8 2l6 12H2z"/><path d="M8 7v3M8 12v.5"/></svg>
              </span>
              <span v-if="taxLookupStatus === 'duplicate'" class="ccf-tax-badge ccf-tax-badge--err">
                <svg viewBox="0 0 16 16" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M8 2l6 12H2z"/><path d="M8 7v3M8 12v.5"/></svg>
              </span>
              <span v-if="taxLookupStatus === 'not-found' || taxLookupStatus === 'error'" class="ccf-tax-badge ccf-tax-badge--warn">
                <svg viewBox="0 0 16 16" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="8" cy="8" r="6"/><path d="M8 5v3M8 11v.5"/></svg>
              </span>
            </div>
          </div>
          <!-- Left col -->
          <div class="ccf-field">
            <label class="ccf-label">Điện thoại</label>
            <input class="ccf-input" v-model="createCustomerForm.misa_mobile" placeholder="Số điện thoại" />
          </div>
          <!-- Right col -->
          <div class="ccf-field">
            <label class="ccf-label">Email</label>
            <input class="ccf-input" type="email" v-model="createCustomerForm.misa_email" placeholder="email@company.com" />
          </div>
          <!-- Left col -->
          <div class="ccf-field">
            <label class="ccf-label">Nguồn gốc</label>
            <select class="ccf-select" v-model="createCustomerForm.nguon_goc">
              <option value="">- Không chọn -</option>
              <option>Gọi điện</option>
              <option>Trực tiếp</option>
              <option>Giới thiệu</option>
              <option>Mạng xã hội</option>
              <option>Email</option>
              <option>Khác</option>
            </select>
          </div>
          <!-- Right col -->
          <div class="ccf-field ccf-required">
            <label class="ccf-label">Loại khách hàng</label>
            <select class="ccf-select" v-model="createCustomerForm.customer_group">
              <option value="">- Không chọn -</option>
              <option v-for="opt in createOptions.customer_groups" :key="opt.name" :value="opt.name">{{ opt.name }}</option>
            </select>
          </div>
          <!-- Left col -->
          <div class="ccf-field">
            <label class="ccf-label">Lĩnh vực</label>
            <select class="ccf-select" v-model="createCustomerForm.industry">
              <option value="">- Không chọn -</option>
              <option v-for="opt in createOptions.industries" :key="opt.name" :value="opt.name">{{ opt.name }}</option>
            </select>
          </div>
          <!-- Right col -->
          <div class="ccf-field">
            <label class="ccf-label">Loại hình</label>
            <select class="ccf-select" v-model="createCustomerForm.loai_hinh">
              <option value="">- Không chọn -</option>
              <option>TNHH</option>
              <option>Cổ phần</option>
              <option>Hộ kinh doanh</option>
              <option>Doanh nghiệp tư nhân</option>
              <option>Công ty hợp danh</option>
              <option>Cá nhân</option>
            </select>
          </div>
          <!-- Left col: empty -->
          <div class="ccf-field"></div>
          <!-- Right col -->
          <div class="ccf-field">
            <label class="ccf-label">Ngành nghề</label>
            <select class="ccf-select" v-model="createCustomerForm.nganh_nghe">
              <option value="">- Không chọn -</option>
              <option>Bán lẻ</option>
              <option>Bán buôn</option>
              <option>Sản xuất</option>
              <option>Dịch vụ</option>
              <option>Xây dựng</option>
              <option>Nông nghiệp</option>
              <option>Công nghệ thông tin</option>
              <option>Giáo dục</option>
              <option>Y tế</option>
              <option>Tài chính ngân hàng</option>
              <option>Khác</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Thông tin hóa đơn -->
      <div class="ccf-section">
        <div class="ccf-section-title">Thông tin hóa đơn</div>
        <div class="ccf-grid">
          <div class="ccf-field">
            <label class="ccf-label">Quốc gia (Hóa đơn)</label>
            <select class="ccf-select" v-model="createBillingForm.country">
              <option value="">- Không chọn -</option>
              <option v-for="opt in createOptions.countries" :key="opt.name" :value="opt.name">{{ opt.name }}</option>
            </select>
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Tỉnh/Thành phố (Hóa đơn)</label>
            <select class="ccf-select" v-model="billingProvinceCode">
              <option value="">{{ createBillingForm.state && !billingProvinceCode ? createBillingForm.state + ' (chọn lại tỉnh 2025)' : '- Chọn tỉnh/thành phố -' }}</option>
              <option v-for="p in vnProvinces" :key="p.code" :value="p.code">{{ p.name }}</option>
            </select>
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Phường/Xã (Hóa đơn)</label>
            <select class="ccf-select" v-model="createBillingForm.county" :disabled="billingProvinceCode ? false : vnBillingWards.length === 0">
              <option value="">{{ vnLoadingBillingWards ? 'Đang tải...' : (billingProvinceCode ? '- Chọn phường/xã -' : (createBillingForm.county ? createBillingForm.county : '- Chọn tỉnh/TP trước -')) }}</option>
              <option v-for="w in vnBillingWards" :key="w.code" :value="w.name">{{ w.name }}</option>
            </select>
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Số nhà, Đường phố (Hóa đơn)</label>
            <input class="ccf-input" v-model="createBillingForm.address_line1" placeholder="Số nhà, tên đường..." />
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Mã vùng (Hóa đơn)</label>
            <input class="ccf-input" v-model="createBillingForm.pincode" placeholder="Mã bưu chính" />
          </div>
        </div>
      </div>

      <!-- Thông tin giao hàng -->
      <div class="ccf-section">
        <div class="ccf-section-title">
          <span>Thông tin giao hàng</span>
          <button class="ccf-copy-addr-btn" @click="copySameAddress" type="button">
            <svg viewBox="0 0 16 16" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="4" y="4" width="9" height="10" rx="1.5"/>
              <path d="M3 12H2a1 1 0 01-1-1V2a1 1 0 011-1h9a1 1 0 011 1v1"/>
            </svg>
            {{ createSameAddress ? 'Đang sao chép · Bỏ sao chép' : 'Sao chép địa chỉ hóa đơn' }}
          </button>
        </div>
        <div :class="['ccf-grid', createSameAddress ? 'ccf-grid--muted' : '']">
          <div class="ccf-field">
            <label class="ccf-label">Quốc gia (Giao hàng)</label>
            <select class="ccf-select" v-model="createShippingForm.country" :disabled="createSameAddress">
              <option value="">- Không chọn -</option>
              <option v-for="opt in createOptions.countries" :key="opt.name" :value="opt.name">{{ opt.name }}</option>
            </select>
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Tỉnh/Thành phố (Giao hàng)</label>
            <select class="ccf-select" v-model="shippingProvinceCode" :disabled="createSameAddress">
              <option value="">{{ createShippingForm.state && !shippingProvinceCode ? createShippingForm.state + ' (chọn lại tỉnh 2025)' : '- Chọn tỉnh/thành phố -' }}</option>
              <option v-for="p in vnProvinces" :key="p.code" :value="p.code">{{ p.name }}</option>
            </select>
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Phường/Xã (Giao hàng)</label>
            <select class="ccf-select" v-model="createShippingForm.county" :disabled="createSameAddress || (shippingProvinceCode ? false : vnShippingWards.length === 0)">
              <option value="">{{ vnLoadingShippingWards ? 'Đang tải...' : (shippingProvinceCode ? '- Chọn phường/xã -' : (createShippingForm.county ? createShippingForm.county : '- Chọn tỉnh/TP trước -')) }}</option>
              <option v-for="w in vnShippingWards" :key="w.code" :value="w.name">{{ w.name }}</option>
            </select>
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Số nhà, Đường phố (Giao hàng)</label>
            <input class="ccf-input" v-model="createShippingForm.address_line1" :disabled="createSameAddress" placeholder="Số nhà, tên đường..." />
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Mã vùng (Giao hàng)</label>
            <input class="ccf-input" v-model="createShippingForm.pincode" :disabled="createSameAddress" placeholder="Mã bưu chính" />
          </div>
        </div>
      </div>

      <!-- Thông tin bổ sung -->
      <div class="ccf-section">
        <div class="ccf-section-title">Thông tin bổ sung</div>
        <div class="ccf-grid">
          <div class="ccf-field">
            <label class="ccf-label">Tài khoản ngân hàng</label>
            <input class="ccf-input" v-model="createCustomerForm.tai_khoan_ngan_hang" placeholder="Số tài khoản" />
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Mở tại ngân hàng</label>
            <input class="ccf-input" v-model="createCustomerForm.mo_tai_ngan_hang" placeholder="Tên ngân hàng" />
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Ngày thành lập/Ngày sinh</label>
            <input class="ccf-input" type="date" v-model="createCustomerForm.ngay_thanh_lap" />
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Là khách hàng từ</label>
            <input class="ccf-input" type="date" v-model="createCustomerForm.la_kh_tu" />
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Doanh thu</label>
            <select class="ccf-select" v-model="createCustomerForm.quy_mo_doanh_thu">
              <option value="">- Không chọn -</option>
              <option>Dưới 1 tỷ</option>
              <option>1-5 tỷ</option>
              <option>5-10 tỷ</option>
              <option>10-50 tỷ</option>
              <option>50-200 tỷ</option>
              <option>Trên 200 tỷ</option>
            </select>
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Quy mô nhân sự</label>
            <select class="ccf-select" v-model="createCustomerForm.quy_mo_nhan_su">
              <option value="">- Không chọn -</option>
              <option>1-10</option>
              <option>11-50</option>
              <option>51-200</option>
              <option>201-500</option>
              <option>501-1000</option>
              <option>Trên 1000</option>
            </select>
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Loại hạn mức nợ</label>
            <select class="ccf-select" v-model="createCustomerForm.loai_han_muc_no">
              <option>Không giới hạn</option>
              <option>Có giới hạn</option>
            </select>
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Website</label>
            <input class="ccf-input" v-model="createCustomerForm.website" placeholder="https://..." />
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Số ngày được nợ</label>
            <input class="ccf-input" type="number" min="0" v-model.number="createCustomerForm.so_ngay_duoc_no" placeholder="0" />
          </div>
        </div>
      </div>

      <!-- Thông tin Liên hệ đại diện -->
      <div class="ccf-section">
        <div class="ccf-section-title">Thông tin Liên hệ đại diện</div>
        <div class="ccf-grid">
          <div class="ccf-field">
            <label class="ccf-label">Tên liên hệ</label>
            <input class="ccf-input" v-model="createContactForm.first_name" placeholder="Họ và tên" />
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Email liên hệ</label>
            <input class="ccf-input" type="email" v-model="createContactForm.email_id" placeholder="email@company.com" />
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Điện thoại liên hệ</label>
            <input class="ccf-input" v-model="createContactForm.mobile_no" placeholder="0901 234 567" />
          </div>
        </div>
      </div>

      <!-- Thông tin mô tả -->
      <div class="ccf-section">
        <div class="ccf-section-title">Thông tin mô tả</div>
        <div class="ccf-grid">
          <div class="ccf-field ccf-span2">
            <label class="ccf-label">Mô tả</label>
            <textarea class="ccf-textarea" v-model="createCustomerForm.customer_details" rows="3" placeholder="Ghi chú về khách hàng..."></textarea>
          </div>
        </div>
      </div>

      <!-- Thông tin hệ thống -->
      <div class="ccf-section">
        <div class="ccf-section-title">Thông tin hệ thống</div>
        <div class="ccf-grid">
          <div class="ccf-field ccf-field--checkbox">
            <label class="ccf-checkbox-label">
              <input type="checkbox" v-model="createCustomerForm.dung_chung" :true-value="1" :false-value="0" />
              <span>Dùng chung</span>
            </label>
          </div>
          <div class="ccf-field">
            <label class="ccf-label">Đối tác/CTV giới thiệu</label>
            <input class="ccf-input" v-model="createCustomerForm.doi_tac_gioi_thieu" placeholder="Mã đối tác giới thiệu" />
          </div>
          <div class="ccf-field ccf-field--checkbox">
            <label class="ccf-checkbox-label">
              <input type="checkbox" v-model="createCustomerForm.la_kh_ca_nhan" :true-value="1" :false-value="0" />
              <span>Là KH cá nhân</span>
            </label>
          </div>
          <div></div>
          <div class="ccf-field ccf-field--checkbox">
            <label class="ccf-checkbox-label">
              <input type="checkbox" v-model="createCustomerForm.la_doi_tac_ctv" :true-value="1" :false-value="0" />
              <span>Là đối tác/cộng tác viên</span>
            </label>
          </div>
        </div>
      </div>

    </div>
  </div>
</div>
`;
