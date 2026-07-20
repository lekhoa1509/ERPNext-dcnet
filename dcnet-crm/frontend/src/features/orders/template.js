export default `
        <main v-else-if="route === 'create-sales-order'" class="opportunity-form-page">
          <header class="opportunity-form-header">
            <div>
              <button class="crm-button" @click="soEditMode ? cancelEditSO() : (createSOContext.customer ? (route = 'customer-detail') : (route = 'orders'))">← Quay lại</button>
              <h1>{{ soEditMode ? 'Sửa đơn hàng' : 'Sinh đơn hàng' }}</h1>
              <span v-if="soEditMode && soEditTarget" class="so-edit-name">{{ soEditTarget }}</span>
              <span v-else class="so-type-badge">
                <select v-model="createSOForm.order_type" class="so-type-sel">
                  <option value="Sales">Đơn đặt hàng DVVT</option>
                  <option value="Maintenance">Hợp đồng mua bán - DV khác</option>
                </select>
              </span>
              <button v-if="!soEditMode" type="button" class="so-layout-btn" @click="openSOLayout">
                <svg viewBox="0 0 16 16" width="13" height="13" fill="none"><rect x="1" y="1" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.4"/><rect x="9" y="1" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.4"/><rect x="1" y="9" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.4"/><rect x="9" y="9" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.4"/></svg>
                Sửa bố cục
              </button>
            </div>
            <div>
              <button class="crm-button" :disabled="createSOSaving" @click="soEditMode ? cancelEditSO() : (createSOContext.customer ? (route = 'customer-detail') : (route = 'orders'))">Hủy</button>
              <button class="crm-button primary" :disabled="createSOSaving" @click="saveCreateSO">{{ createSOSaving ? 'Đang lưu...' : (soEditMode ? 'Cập nhật' : 'Lưu') }}</button>
            </div>
          </header>

          <teleport to="body"><div v-if="soLayoutOpen" class="so-layout-overlay" @click.self="closeSOLayout">
            <div class="so-layout-drawer">
              <header class="so-layout-drawer-header">
                <h3>Sửa bố cục</h3>
                <button type="button" class="so-layout-close" @click="closeSOLayout">×</button>
              </header>
              <div class="so-layout-body">
                <p class="so-layout-hint">Chọn các phần hiển thị trong form đơn hàng</p>
                <div class="so-layout-row so-layout-fixed">
                  <svg viewBox="0 0 16 16" width="14" height="14" fill="none"><path d="M8 1a2 2 0 0 1 2 2v2H6V3a2 2 0 0 1 2-2zm3 4V3a3 3 0 1 0-6 0v2H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V5h-2z" fill="#b0b7c3"/></svg>
                  <span>Thông tin chung</span>
                  <span class="so-layout-required">Bắt buộc</span>
                </div>
                <div class="so-layout-row so-layout-fixed">
                  <svg viewBox="0 0 16 16" width="14" height="14" fill="none"><path d="M8 1a2 2 0 0 1 2 2v2H6V3a2 2 0 0 1 2-2zm3 4V3a3 3 0 1 0-6 0v2H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V5h-2z" fill="#b0b7c3"/></svg>
                  <span>Thông tin hàng hóa</span>
                  <span class="so-layout-required">Bắt buộc</span>
                </div>
                <label class="so-layout-row">
                  <input type="checkbox" :checked="soVisibleSections.mo_ta" @change="toggleSOSection('mo_ta')">
                  <span>Thông tin mô tả</span>
                </label>
                <label class="so-layout-row">
                  <input type="checkbox" :checked="soVisibleSections.tinh_trang" @change="toggleSOSection('tinh_trang')">
                  <span>Tình trạng thực hiện đơn hàng</span>
                </label>
                <label class="so-layout-row">
                  <input type="checkbox" :checked="soVisibleSections.hoa_don" @change="toggleSOSection('hoa_don')">
                  <span>Thông tin hóa đơn</span>
                </label>
                <label class="so-layout-row">
                  <input type="checkbox" :checked="soVisibleSections.giao_hang" @change="toggleSOSection('giao_hang')">
                  <span>Thông tin giao hàng</span>
                </label>
              </div>
              <footer class="so-layout-drawer-footer">
                <button type="button" class="crm-button" @click="resetSOLayout">Đặt lại mặc định</button>
                <button type="button" class="crm-button primary" @click="closeSOLayout">Xong</button>
              </footer>
            </div>
          </div></teleport>

          <form class="opportunity-form-card" @submit.prevent="saveCreateSO">

            <section>
              <h2>Thông tin chung</h2>
              <!-- DVVT layout (Sales) — giữ nguyên -->
              <div v-if="createSOForm.order_type !== 'Maintenance'" class="opportunity-form-grid">
                <label><span>Khách hàng <b>*</b></span>
                  <input v-if="createSOContext.customer" :value="createSOForm.customer" disabled>
                  <search-select v-else v-model="createSOForm.customer" @update:model-value="onSOCustomerChange" @add="createDocument('Customer')" :options="soFormOptions.customers" value-key="name" label-key="customer_name" :meta-keys="['tax_id','name','mobile_no']" desc-key="primary_address" add-label="Thêm khách hàng" placeholder="- Không chọn -"></search-select>
                </label>
                <label><span>Liên hệ</span>
                  <search-select v-model="createSOForm.contact_person" :options="soFormOptions.contacts" label-key="full_name" sub-key="mobile_no" placeholder="- Không chọn -"></search-select>
                </label>
                <label><span>Cơ hội</span>
                  <search-select v-model="createSOForm.opportunity" :options="soFormOptions.opportunities" label-key="title" placeholder="- Không chọn -"></search-select>
                </label>
                <label><span>Ngày đặt hàng <b>*</b></span><input type="date" v-model="createSOForm.transaction_date" required></label>
                <label><span>Hạn giao hàng</span><input type="date" v-model="createSOForm.delivery_date"></label>
                <label><span>Số HĐ / PO khách hàng</span><input v-model="createSOForm.po_no" placeholder="VD: HĐ/2026/001"></label>
                <label><span>Ngày ký Hợp đồng</span><input type="date" v-model="createSOForm.po_date"></label>
                <label><span>Thời hạn HĐ (tháng)</span><input type="number" min="0" v-model.number="createSOForm.contract_duration" placeholder="0"></label>
                <label><span>Ngày hết hạn Hợp đồng</span><input type="date" v-model="createSOForm.contract_expiry" disabled></label>
                <label><span>Khu vực lắp đặt dịch vụ</span><select v-model="createSOForm.installation_zone"><option value="">- Không chọn -</option><option value="Bắc">Bắc</option><option value="Trung">Trung</option><option value="Nam">Nam</option><option value="Toàn Quốc">Toàn Quốc</option></select></label>
                <label><span>Chiến dịch</span>
                  <search-select v-model="createSOForm.campaign" :options="soFormOptions.campaigns" placeholder="- Không chọn -"></search-select>
                </label>
                <label><span>Bảng giá</span>
                  <search-select v-model="createSOForm.selling_price_list" :options="soFormOptions.price_lists" placeholder="- Không chọn -"></search-select>
                </label>
                <label><span>Tiền tệ</span><input v-model="createSOForm.currency" placeholder="VND"></label>
                <label><span>Điều khoản thanh toán</span>
                  <search-select v-model="createSOForm.payment_terms_template" :options="soFormOptions.payment_terms" placeholder="- Không chọn -"></search-select>
                </label>
                <label><span>Phí &amp; Thuế</span>
                  <search-select v-model="createSOForm.taxes_and_charges" :options="soFormOptions.taxes_templates" placeholder="- Không chọn -"></search-select>
                </label>
                <label><span>Khu vực</span>
                  <search-select v-model="createSOForm.territory" :options="soFormOptions.territories" placeholder="- Không chọn -"></search-select>
                </label>
                <label><span>Công ty</span><input v-model="createSOForm.company" placeholder="Tên công ty..."></label>
              </div>
              <!-- Hợp đồng mua bán layout (Maintenance) -->
              <div v-else class="opportunity-form-grid">
                <label><span>Khách hàng <b>*</b></span>
                  <input v-if="createSOContext.customer" :value="createSOForm.customer" disabled>
                  <search-select v-else v-model="createSOForm.customer" @update:model-value="onSOCustomerChange" @add="createDocument('Customer')" :options="soFormOptions.customers" value-key="name" label-key="customer_name" :meta-keys="['tax_id','name','mobile_no']" desc-key="primary_address" add-label="Thêm khách hàng" placeholder="- Không chọn -"></search-select>
                </label>
                <label><span>Liên hệ</span>
                  <search-select v-model="createSOForm.contact_person" :options="soFormOptions.contacts" label-key="full_name" sub-key="mobile_no" placeholder="- Không chọn -"></search-select>
                </label>
                <label><span>Số đơn hàng/hợp đồng</span><input v-model="createSOForm.po_no" placeholder="VD: HĐ/2026/001"></label>
                <label><span>Ngày đặt hàng <b>*</b></span><input type="date" v-model="createSOForm.transaction_date" required></label>
                <label><span>Cơ hội</span>
                  <search-select v-model="createSOForm.opportunity" :options="soFormOptions.opportunities" label-key="title" placeholder="- Không chọn -"></search-select>
                </label>
                <label><span>Diễn giải</span><input v-model="createSOForm.title" placeholder="Tóm tắt hợp đồng..."></label>
                <label><span>Hạn giao hàng</span><input type="date" v-model="createSOForm.delivery_date"></label>
                <label><span>Loại đơn hàng</span><select v-model="createSOForm.order_category"><option value="">- Không chọn -</option><option value="Sản phẩm">Sản phẩm</option><option value="Dịch vụ DVVT">Dịch vụ DVVT</option><option value="Dịch vụ khác">Dịch vụ khác</option></select></label>
                <label><span>Loại hợp đồng</span><select v-model="createSOForm.contract_type"><option value="">- Không chọn -</option><option value="Mới">Hợp đồng mới</option><option value="Gia hạn">Gia hạn</option><option value="Bổ sung">Bổ sung</option><option value="Thanh lý">Thanh lý</option></select></label>
                <label><span>Bảo giá</span>
                  <search-select v-model="createSOForm.selling_price_list" :options="soFormOptions.price_lists" placeholder="- Không chọn -"></search-select>
                </label>
                <label><span>Ngày ký Hợp đồng</span><input type="date" v-model="createSOForm.po_date"></label>
                <label><span>Thời hạn HĐ (tháng)</span><input type="number" min="0" v-model.number="createSOForm.contract_duration" placeholder="0"></label>
                <label><span>Giá trị đơn hàng</span><input type="number" min="0" v-model.number="createSOForm.order_value" placeholder="0"></label>
                <label><span>Ngày hết hạn Hợp đồng</span><input type="date" v-model="createSOForm.contract_expiry" disabled></label>
                <label><span>Số ngày được nợ</span><input type="number" min="0" v-model.number="createSOForm.credit_days" placeholder="0"></label>
                <label><span>Giá trị thanh lý</span><input type="number" min="0" v-model.number="createSOForm.liquidation_value" placeholder="0"></label>
                <div></div>
                <label><span>Chiến dịch</span>
                  <search-select v-model="createSOForm.campaign" :options="soFormOptions.campaigns" placeholder="- Không chọn -"></search-select>
                </label>
              </div>
            </section>

            <section>
              <div class="opportunity-section-heading">
                <div><h2>Thông tin hàng hóa</h2></div>
                <div><button v-if="createSOItems.length > 1" type="button" class="danger" @click="clearSOItems">× Xóa tất cả</button></div>
              </div>
              <div v-if="!createSOItems.length" class="opportunity-items-empty">
                <button type="button" class="crm-button primary" @click="openSOItemPicker">＋ Chọn hàng hóa</button>
                <button type="button" class="so-paste-excel-btn" @click="handleSOExcelPasteBtn" style="margin-left:8px">
                  <svg width="14" height="14" viewBox="0 0 16 16" fill="none"><rect x="2" y="1" width="8" height="11" rx="1" stroke="currentColor" stroke-width="1.4"/><path d="M5 1h4a1 1 0 011 1v1H4V2a1 1 0 011-1z" stroke="currentColor" stroke-width="1.4"/><path d="M10 6h4M10 9h4M10 12h4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>
                  Dán từ Excel
                </button>
              </div>
              <template v-else>
                <div class="opportunity-items-scroll" tabindex="-1" @paste="onSOTablePaste">
                  <table class="opportunity-items-table so-items-table">
                    <colgroup>
                      <col class="col-stt">
                      <col class="col-item-code">
                      <col class="col-item-name">
                      <col class="col-desc">
                      <col v-if="createSOForm.order_type !== 'Maintenance'" class="col-aend">
                      <col v-if="createSOForm.order_type !== 'Maintenance'" class="col-zend">
                      <col v-if="createSOForm.order_type !== 'Maintenance'" class="col-account">
                      <col class="col-uom">
                      <col class="col-qty">
                      <col class="col-price">
                      <col class="col-amt">
                      <col class="col-ck-pct">
                      <col class="col-ck-amt">
                      <col class="col-price-ck">
                      <col class="col-amt-ck">
                      <col class="col-tax-rate">
                      <col v-if="createSOForm.order_type === 'Maintenance'" class="col-tax-amt">
                    </colgroup>
                    <thead>
                      <tr>
                        <th>STT</th>
                        <th>Mã hàng hóa</th>
                        <th>Tên hàng hóa</th>
                        <th>Mô tả</th>
                        <th v-if="createSOForm.order_type !== 'Maintenance'">Điểm lắp đặt A-End</th>
                        <th v-if="createSOForm.order_type !== 'Maintenance'">Điểm lắp đặt Z-End</th>
                        <th v-if="createSOForm.order_type !== 'Maintenance'">Account</th>
                        <th>Đơn vị tính</th>
                        <th>Số lượng</th>
                        <th>Đơn giá</th>
                        <th>Thành tiền</th>
                        <th>Tỷ lệ CK (%)</th>
                        <th>Tiền CK</th>
                        <th>Đơn giá sau CK</th>
                        <th>Thành tiền sau CK</th>
                        <th>Thuế suất</th>
                        <th v-if="createSOForm.order_type === 'Maintenance'">Tiền thuế</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(item, index) in createSOItems" :key="index">
                        <td class="item-stt-cell">
                          <span class="item-stt-num">{{ index + 1 }}</span>
                          <button type="button" class="item-row-del" @click="removeSOItem(index)">×</button>
                        </td>
                        <td>
                          <search-select :model-value="item.item_code" @update:model-value="(v) => { item.item_code = v; autoFillSOItemByCode(item); }" :options="soFormOptions.items" value-key="name" label-key="name" desc-key="item_name" placeholder="Mã hàng"></search-select>
                        </td>
                        <td><input v-model="item.item_name" placeholder="Tên hàng hóa / dịch vụ"></td>
                        <td><input v-model="item.description" placeholder="Mô tả..."></td>
                        <td v-if="createSOForm.order_type !== 'Maintenance'"><input list="so-aend-options" v-model="item.a_end" @change="autoFetchSOItemAccount(item)" placeholder="Địa chỉ A-End..."></td>
                        <td v-if="createSOForm.order_type !== 'Maintenance'"><input list="so-zend-options" v-model="item.z_end" @change="autoFetchSOItemAccount(item)" placeholder="Địa chỉ Z-End..."></td>
                        <td v-if="createSOForm.order_type !== 'Maintenance'" class="item-account-cell">
                          <span v-if="item.account_id" class="item-account-badge">{{ item.account_id }}</span>
                          <span v-else-if="item.account_new" class="item-account-pending" data-tooltip="Tài khoản dịch vụ sẽ được tạo khi bạn lưu đơn hàng">Tự sinh khi lưu</span>
                          <span v-else class="item-account-empty">—</span>
                        </td>
                        <td><input v-model="item.uom" placeholder="Cái"></td>
                        <td><input type="number" min="0" step="any" v-model.number="item.qty" @input="updateSOItemAmount(item)"></td>
                        <td><input type="number" min="0" step="any" v-model.number="item.price_list_rate" @input="updateSOItemRate(item)" placeholder="0"></td>
                        <td class="item-calc-cell">{{ formatValue(soItemPreTotal(item), 'grand_total') }}</td>
                        <td><input type="number" min="0" max="100" step="any" v-model.number="item.discount_percentage" @input="updateSOItemRate(item)" placeholder="0"></td>
                        <td class="item-calc-cell">{{ formatValue(soItemDiscount(item), 'grand_total') }}</td>
                        <td><input type="number" min="0" step="any" v-model.number="item.rate" @input="updateSOItemAmount(item)" placeholder="0"></td>
                        <td class="item-calc-cell">{{ formatValue(item.amount, 'grand_total') }}</td>
                        <td><input type="number" min="0" v-model.number="item.tax_rate" placeholder="0"></td>
                        <td v-if="createSOForm.order_type === 'Maintenance'" class="item-calc-cell">{{ formatValue(soItemTax(item), 'grand_total') }}</td>
                      </tr>
                      <tr class="items-total-row">
                        <td></td>
                        <td :colspan="createSOForm.order_type !== 'Maintenance' ? 7 : 4" class="items-total-label">Tổng cộng</td>
                        <td>{{ soTotalQty() }}</td>
                        <td></td>
                        <td class="items-total-num">{{ formatValue(soSubtotal(), 'grand_total') }}</td>
                        <td></td>
                        <td class="items-total-num">{{ formatValue(soTotalDiscount(), 'grand_total') }}</td>
                        <td></td>
                        <td class="items-total-num">{{ formatValue(soGrandTotal(), 'grand_total') }}</td>
                        <td></td>
                        <td v-if="createSOForm.order_type === 'Maintenance'" class="items-total-num">{{ formatValue(createSOItems.reduce((s,i) => s + soItemTax(i), 0), 'grand_total') }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <div class="opportunity-item-actions">
                  <strong>Tổng số: {{ createSOItems.length }}</strong>
                  <div class="item-action-btns">
                    <button type="button" class="so-paste-excel-btn" @click="handleSOExcelPasteBtn" data-tooltip="Dan tu Excel (tab-separated): Ma hang | Ten hang | Mo ta | [A-End | Z-End] | DVT | SL | Don gia | CK% | Thue suat">
                      <svg width="14" height="14" viewBox="0 0 16 16" fill="none"><rect x="2" y="1" width="8" height="11" rx="1" stroke="currentColor" stroke-width="1.4"/><path d="M5 1h4a1 1 0 011 1v1H4V2a1 1 0 011-1z" stroke="currentColor" stroke-width="1.4"/><path d="M10 6h4M10 9h4M10 12h4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>
                      Dán từ Excel
                    </button>
                    <button type="button" class="crm-button primary" @click="openSOItemPicker">＋ Chọn hàng hóa</button>
                  </div>
                </div>
                <!-- Paste toast -->
                <transition name="so-toast-fade">
                  <div v-if="soPasteToast.show" :class="['so-paste-toast', soPasteToast.error ? 'so-paste-toast--err' : '']">
                    <svg v-if="!soPasteToast.error" width="15" height="15" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1.5"/><path d="M5 8l2.5 2.5L11 5.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    <svg v-else width="15" height="15" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1.5"/><path d="M8 5v4M8 11v.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
                    {{ soPasteToast.message }}
                  </div>
                </transition>
              </template>

              <datalist id="so-item-options">
                <option v-for="opt in soFormOptions.items" :key="opt.name" :value="opt.name">{{ opt.item_name }}</option>
              </datalist>
              <datalist id="so-aend-options">
                <option v-for="addr in soAEndOptions" :key="addr" :value="addr"></option>
              </datalist>
              <datalist id="so-zend-options">
                <option v-for="addr in soZEndOptions" :key="addr" :value="addr"></option>
              </datalist>

              <teleport to="body"><div v-if="soItemPickerOpen" class="crm-modal-backdrop" @click.self="closeSOItemPicker">
                <div class="crm-modal item-picker-modal">
                  <header>
                    <h2>Chọn hàng hóa<span v-if="soItemPickerSelected.length" class="picker-selected-badge">{{ soItemPickerSelected.length }} đã chọn</span></h2>
                    <button type="button" @click="closeSOItemPicker">×</button>
                  </header>
                  <div class="item-picker-toolbar">
                    <div class="item-picker-search-wrap">
                      <svg class="picker-search-icon" viewBox="0 0 16 16" fill="none"><circle cx="7" cy="7" r="5" stroke="#98a2b3" stroke-width="1.5"/><path d="M11 11l3 3" stroke="#98a2b3" stroke-width="1.5" stroke-linecap="round"/></svg>
                      <input v-model="soItemPickerSearch" @input="soItemPickerPage = 1" placeholder="Tìm theo mã hoặc tên hàng hóa..." class="item-picker-search" autofocus>
                    </div>
                    <select v-model="soItemPickerCategoryFilter" @change="soItemPickerPage = 1" class="item-picker-cat">
                      <option value="">Tất cả loại hàng hóa</option>
                      <option v-for="cat in soItemPickerCategories" :key="cat" :value="cat">{{ cat }}</option>
                    </select>
                  </div>
                  <div class="item-picker-table-wrap">
                    <table class="item-picker-table">
                      <colgroup><col><col><col><col><col></colgroup>
                      <thead>
                        <tr>
                          <th class="picker-check-col">
                            <input type="checkbox"
                              :checked="soItemPickerRows.length > 0 && soItemPickerRows.every(r => soItemPickerSelected.includes(r.name))"
                              :indeterminate="soItemPickerRows.some(r => soItemPickerSelected.includes(r.name)) && !soItemPickerRows.every(r => soItemPickerSelected.includes(r.name))"
                              @change="e => { if(e.target.checked) soItemPickerRows.forEach(r => { if(!soItemPickerSelected.includes(r.name)) soItemPickerSelected.push(r.name) }); else soItemPickerSelected = soItemPickerSelected.filter(n => !soItemPickerRows.find(r => r.name === n)) }">
                          </th>
                          <th>Mã hàng hóa</th>
                          <th>Tên hàng hóa</th>
                          <th>Loại hàng hóa</th>
                          <th>Đơn vị tính</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="item in soItemPickerRows" :key="item.name"
                          @click="toggleSOItemPickerRow(item.name)"
                          :class="{ selected: soItemPickerSelected.includes(item.name) }">
                          <td class="picker-check-col"><input type="checkbox" :checked="soItemPickerSelected.includes(item.name)" @click.stop="toggleSOItemPickerRow(item.name)"></td>
                          <td><span class="picker-code">{{ item.name }}</span></td>
                          <td>{{ item.item_name }}</td>
                          <td><span class="picker-tag" v-if="item.item_group && item.item_group !== 'All Item Groups'">{{ item.item_group }}</span><span v-else class="picker-tag-muted">—</span></td>
                          <td>{{ item.stock_uom || '—' }}</td>
                        </tr>
                        <tr v-if="!soItemPickerRows.length" class="picker-empty-row">
                          <td colspan="5">Không tìm thấy hàng hóa nào phù hợp</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <div class="item-picker-footer">
                    <span>Tổng <strong>{{ soItemPickerFiltered.length }}</strong> hàng hóa</span>
                    <div class="item-picker-pagination">
                      <span>Dòng/trang</span>
                      <select v-model.number="soItemPickerPageLength" @change="soItemPickerPage = 1">
                        <option :value="10">10</option><option :value="20">20</option><option :value="50">50</option>
                      </select>
                      <span>{{ (soItemPickerPage-1)*soItemPickerPageLength+1 }}–{{ Math.min(soItemPickerPage*soItemPickerPageLength, soItemPickerFiltered.length) }}</span>
                      <button type="button" :disabled="soItemPickerPage <= 1" @click="soItemPickerPage = 1" data-tooltip="Trang đầu">«</button>
                      <button type="button" :disabled="soItemPickerPage <= 1" @click="soItemPickerPage--" data-tooltip="Trang trước">‹</button>
                      <button type="button" :disabled="soItemPickerPage >= soItemPickerPageCount" @click="soItemPickerPage++" data-tooltip="Trang sau">›</button>
                      <button type="button" :disabled="soItemPickerPage >= soItemPickerPageCount" @click="soItemPickerPage = soItemPickerPageCount" data-tooltip="Trang cuối">»</button>
                    </div>
                  </div>
                  <footer>
                    <button type="button" class="crm-button" @click="closeSOItemPicker">Hủy</button>
                    <button type="button" class="crm-button primary" :disabled="!soItemPickerSelected.length" @click="confirmSOItemPicker">
                      {{ soItemPickerSelected.length ? 'Thêm ' + soItemPickerSelected.length + ' hàng hóa' : 'Chọn hàng hóa' }}
                    </button>
                  </footer>
                </div>
              </div></teleport>
            </section>

            <section v-show="soVisibleSections.mo_ta">
              <h2>Thông tin mô tả</h2>
              <label class="opportunity-notes"><span>Tiêu đề / Diễn giải</span><input v-model="createSOForm.title" placeholder="Mô tả ngắn gọn về đơn hàng..."></label>
              <label class="opportunity-notes" style="margin-top:10px"><span>Ghi chú</span><textarea v-model="createSOForm.note" placeholder="Ghi chú nội bộ..."></textarea></label>
            </section>

            <section v-show="soVisibleSections.tinh_trang">
              <h2>Tình trạng thực hiện đơn hàng</h2>
              <!-- DVVT layout — giữ nguyên -->
              <div v-if="createSOForm.order_type !== 'Maintenance'" class="opportunity-form-grid">
                <label><span>Tình trạng <b>*</b></span><select v-model="createSOForm.execution_status"><option value="Chưa thực hiện">Chưa thực hiện</option><option value="Đang thực hiện">Đang thực hiện</option><option value="Hoàn thành">Hoàn thành</option></select></label>
                <label><span>Tình trạng ghi doanh số</span><input disabled value="Đơn nháp"></label>
                <label><span>Ngày ghi doanh số</span><input type="date" v-model="createSOForm.revenue_recognition_date"></label>
                <label><span>Hạn thanh toán</span><input type="date" v-model="createSOForm.payment_due_date"></label>
                <label><span>Ngày nghiệm thu tính cước</span><input type="date" v-model="createSOForm.acceptance_date" disabled></label>
              </div>
              <!-- Maintenance layout -->
              <div v-else class="opportunity-form-grid">
                <label><span>Tình trạng <b>*</b></span><select v-model="createSOForm.execution_status"><option value="Chưa thực hiện">Chưa thực hiện</option><option value="Đang thực hiện">Đang thực hiện</option><option value="Hoàn thành">Hoàn thành</option></select></label>
                <label><span>Tình trạng ghi doanh số</span><input disabled value="Đơn nháp"></label>
                <label><span>Ngày ghi số</span><input type="date" v-model="createSOForm.revenue_recognition_date"></label>
                <label><span>Chu kỳ thanh toán</span><select v-model="createSOForm.payment_cycle"><option value="">- Không chọn -</option><option value="Hàng tháng">Hàng tháng</option><option value="Hàng quý">Hàng quý</option><option value="6 tháng">6 tháng</option><option value="Hàng năm">Hàng năm</option><option value="Một lần">Một lần</option></select></label>
                <label><span>Hạn thanh toán <b>*</b></span><input type="date" v-model="createSOForm.payment_due_date"></label>
                <label><span>Hạn sản xuất</span><input type="date" v-model="createSOForm.production_deadline"></label>
                <label><span>Ngày nghiệm thu tính cước</span><input type="date" v-model="createSOForm.acceptance_date" disabled></label>
              </div>
            </section>

            <!-- Đợt thanh toán — chỉ dành cho Hợp đồng mua bán -->
            <section v-if="createSOForm.order_type === 'Maintenance'">
              <div class="opportunity-section-heading">
                <div><h2>Đợt thanh toán</h2></div>
                <div></div>
              </div>
              <table class="so-payment-table">
                <thead>
                  <tr>
                    <th>Tên đợt</th>
                    <th>Tỷ lệ thanh toán (%)</th>
                    <th>Giá trị thanh toán</th>
                    <th>Hạn thanh toán</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(row, idx) in createSOPaymentSchedule" :key="idx">
                    <td><input v-model="row.payment_term" placeholder="VD: Đợt 1..."></td>
                    <td><input type="number" min="0" max="100" step="any" v-model.number="row.invoice_portion" placeholder="0"></td>
                    <td><input type="number" min="0" step="any" v-model.number="row.payment_amount" placeholder="0"></td>
                    <td><input type="date" v-model="row.due_date"></td>
                    <td class="so-payment-td-del"><button type="button" class="so-payment-del" @click="removeSOPaymentRow(idx)">×</button></td>
                  </tr>
                  <tr class="items-total-row">
                    <td colspan="1" style="text-align:left;padding-left:8px">Tổng cộng</td>
                    <td>{{ soPaymentScheduleTotal().toFixed(1) }}%</td>
                    <td>{{ formatValue(soPaymentScheduleTotalAmount(), 'grand_total') }}</td>
                    <td colspan="2"></td>
                  </tr>
                </tbody>
              </table>
              <div class="item-action-btns" style="margin-top:8px">
                <button type="button" class="crm-button primary" @click="addSOPaymentRow">＋ Thêm dòng</button>
              </div>
            </section>

            <section v-show="soVisibleSections.hoa_don">
              <h2>Thông tin hóa đơn</h2>
              <!-- DVVT: form compact -->
              <div v-if="createSOForm.order_type !== 'Maintenance'" class="opportunity-form-grid">
                <label><span>Khách hàng (Hóa đơn)</span><input v-model="createSOForm.billing_customer" placeholder="Mã khách hàng..."></label>
                <label><span>Người mua hàng</span><input disabled placeholder="- Không chọn -"></label>
                <label><span>Quốc gia</span><select><option>Việt Nam</option></select></label>
                <label><span>Tỉnh/Thành phố</span><select><option value="">- Không chọn -</option></select></label>
                <label style="grid-column: 1 / -1"><span>Địa chỉ</span><textarea v-model="createSOForm.billing_address" placeholder="Địa chỉ hóa đơn..."></textarea></label>
              </div>
              <!-- Maintenance: form đầy đủ địa chỉ -->
              <div v-else class="opportunity-form-grid">
                <label><span>Khách hàng (Hóa đơn)</span><input v-model="createSOForm.billing_customer" placeholder="Mã khách hàng..."></label>
                <label><span>Người mua hàng</span><input disabled placeholder="- Không chọn -"></label>
                <label><span>Quốc gia (Hóa đơn)</span><select><option>Việt Nam</option></select></label>
                <label><span>Tỉnh/Thành phố (Hóa đơn)</span><select><option value="">- Không chọn -</option></select></label>
                <label><span>Quận/Huyện (Hóa đơn)</span><select><option value="">- Không chọn -</option></select></label>
                <label><span>Phường/Xã (Hóa đơn)</span><select><option value="">- Không chọn -</option></select></label>
                <label><span>Số nhà, Đường phố (Hóa đơn)</span><input v-model="createSOForm.billing_street" placeholder="Số nhà, tên đường..."></label>
                <label><span>Mã vùng (Hóa đơn)</span><input v-model="createSOForm.billing_zipcode" placeholder="Mã bưu chính..."></label>
                <label style="grid-column: 1 / -1"><span>Địa chỉ (Hóa đơn)</span><textarea v-model="createSOForm.billing_address" placeholder="Địa chỉ đầy đủ..."></textarea></label>
              </div>
            </section>

            <section v-show="soVisibleSections.giao_hang">
              <h2>Thông tin giao hàng</h2>
              <!-- DVVT: form compact -->
              <div v-if="createSOForm.order_type !== 'Maintenance'" class="opportunity-form-grid">
                <label><span>Người nhận hàng</span><input v-model="createSOForm.shipping_recipient" placeholder="Tên người nhận..."></label>
                <label><span>Điện thoại</span><input disabled placeholder="- Không chọn -"></label>
                <label><span>Quốc gia</span><select><option>Việt Nam</option></select></label>
                <label><span>Tỉnh/Thành phố</span><select><option value="">- Không chọn -</option></select></label>
                <label style="grid-column: 1 / -1"><span>Địa chỉ</span><textarea v-model="createSOForm.shipping_address" placeholder="Địa chỉ giao hàng..."></textarea></label>
              </div>
              <!-- Maintenance: form đầy đủ địa chỉ + kho -->
              <div v-else class="opportunity-form-grid">
                <label><span>Người nhận hàng</span><input v-model="createSOForm.shipping_recipient" placeholder="Tên người nhận..."></label>
                <label><span>Điện thoại</span><input disabled placeholder="- Không chọn -"></label>
                <label><span>Quốc gia (Giao hàng)</span><select><option>Việt Nam</option></select></label>
                <label><span>Tỉnh/Thành phố (Giao hàng)</span><select><option value="">- Không chọn -</option></select></label>
                <label><span>Quận/Huyện (Giao hàng)</span><select><option value="">- Không chọn -</option></select></label>
                <label><span>Phường/Xã (Giao hàng)</span><select><option value="">- Không chọn -</option></select></label>
                <label><span>Số nhà, Đường phố (Giao hàng)</span><input v-model="createSOForm.shipping_street" placeholder="Số nhà, tên đường..."></label>
                <label><span>Mã vùng (Giao hàng)</span><input v-model="createSOForm.shipping_zipcode" placeholder="Mã bưu chính..."></label>
                <label style="grid-column: 1 / -1"><span>Địa chỉ (Giao hàng)</span><textarea v-model="createSOForm.shipping_address" placeholder="Địa chỉ đầy đủ..."></textarea></label>
                <label><span>Xuất hàng từ kho</span><select v-model="createSOForm.warehouse"><option value="">- Không chọn -</option></select></label>
              </div>
            </section>

            <!-- Thông tin hệ thống — chỉ dành cho Hợp đồng mua bán -->
            <section v-if="createSOForm.order_type === 'Maintenance'">
              <h2>Thông tin hệ thống</h2>
              <div class="opportunity-form-grid">
                <label><span>Người thực hiện</span><input disabled :value="soCurrentUser"></label>
                <label><span>Đơn vị</span><input disabled placeholder="- Không chọn -"></label>
                <label class="so-check-row"><span>Dùng chung</span><input type="checkbox" v-model="createSOForm.shared_flag"></label>
                <label class="so-check-row"><span>Đồng bộ đơn giá sau CK</span><input type="checkbox" v-model="createSOForm.sync_price"></label>
                <label><span>Đối tác/CTV giới thiệu</span><input v-model="createSOForm.referral_partner" placeholder="- Không chọn -"></label>
              </div>
            </section>

          </form>
        </main>

        <main v-else-if="route === 'order-detail'" class="sod-page">
  <header class="sod-header">
    <div class="sod-header-left">
      <button class="sod-back" @click="backToOrders" aria-label="Quay lại">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5"/><path d="m12 19-7-7 7-7"/></svg>
      </button>
      <span class="sod-code">{{ orderDetail?.document?.name || orderDetailName }}</span>
      <span class="sod-sep">·</span>
      <span class="sod-ref">{{ orderDetail?.document?.po_no || orderDetail?.document?.title || '' }}</span>
      <button class="sod-refresh" @click="loadOrderDetail()" aria-label="Tải lại"><CRMIcon name="refresh" /></button>
    </div>
    <div class="sod-header-actions">
      <button class="sod-btn" @click="printSalesOrder">In</button>
      <button class="sod-btn" v-if="orderDetail && orderDetail.can_write" @click="openEditSO(orderDetail)">Sửa</button>
      <button class="sod-btn" @click="requestSOApproval">Gửi phê duyệt</button>
      <button
        v-if="orderDetail?.document?.docstatus === 0 && orderDetail?.document?.revenue_request_pending"
        class="sod-btn sod-btn-red"
        :disabled="soRevenueRequestSaving"
        @click="withdrawSORevenueRecognition"
      >{{ soRevenueRequestSaving ? 'Đang thu hồi...' : 'Thu hồi đề nghị ghi' }}</button>
      <div v-else-if="orderDetail?.document?.docstatus === 0" class="sod-split-btn">
        <button
          class="sod-btn sod-btn-green"
          :disabled="soRevenueRequestSaving"
          @click="requestSORevenueRecognition"
        >Đề nghị ghi DS</button>
        <button
          v-if="showUnreadyFeatures"
          class="sod-btn sod-btn-green sod-split-arrow"
          :disabled="soRevenueRequestSaving"
          aria-label="Tùy chọn ghi doanh số"
          @click="notifyOrderAction('Tùy chọn ghi doanh số')"
        ><svg viewBox="0 0 10 6" width="10" height="6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M1 1l4 4 4-4"/></svg></button>
      </div>
      <div class="sod-action-wrap" v-click-outside="closeSOActionMenu">
        <button class="sod-btn sod-btn-icon" :disabled="soActionSaving" @click="toggleSOActionMenu" aria-label="Thêm hành động">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><circle cx="5" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="19" cy="12" r="2"/></svg>
        </button>
        <div v-if="soActionMenuOpen" class="sod-action-menu">
          <button class="sod-action-item" @click="openSOActionModal('invoice')">
            <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
            Đề nghị xuất hóa đơn
          </button>
          <button class="sod-action-item" @click="openSOActionModal('delivery')">
            <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.62l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/></svg>
            Giao hàng
          </button>
          <button class="sod-action-item" @click="openSOActionModal('return')">
            <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 .49-4.51"/></svg>
            Đề nghị trả hàng
          </button>
          <button class="sod-action-item" @click="openSOActionModal('purchase_request')">
            <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
            Yêu cầu mua hàng
          </button>
          <div class="sod-action-sep"></div>
          <button class="sod-action-item" @click="openAuditLog('Sales Order', orderDetail.document.name); closeSOActionMenu()">
            <CRMIcon name="history" />
            Nhật ký
          </button>
        </div>
      </div>
    </div>
  </header>

  <div v-if="loading" class="crm-empty" style="margin-top:40px">Đang tải...</div>
  <div v-else-if="!orderDetail" class="crm-empty" style="margin-top:40px">Không tìm thấy đơn hàng.</div>
  <div v-else class="sod-body">

    <aside class="sod-side" v-show="!soSideCollapsed">
      <div class="sod-side-title">{{ orderDetail.document.title || orderDetail.document.name }}</div>
      <div class="sod-side-tag">
        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12.586 2.586A2 2 0 0 0 11.172 2H4a2 2 0 0 0-2 2v7.172a2 2 0 0 0 .586 1.414l8.704 8.704a2.426 2.426 0 0 0 3.42 0l6.58-6.58a2.426 2.426 0 0 0 0-3.42z"/><circle cx="7.5" cy="7.5" r="1.5"/></svg>
        Thêm thẻ
      </div>

      <div class="sod-side-daterow">
        <span>Ngày ghi số: <b>{{ formatValue(orderDetail.document.custom_revenue_recognition_date || orderDetail.document.transaction_date, 'transaction_date') }}</b></span>
        <span class="sod-status-pill">
          {{ orderDetail.document.display_revenue_status || 'Đơn nháp' }}
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
        </span>
      </div>

      <button type="button" class="sod-card sod-card-customer" @click="openOrderCustomer">
        <span class="sod-card-icon purple">
          <svg viewBox="0 0 24 24" width="19" height="19" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4M10 10h4M10 14h4M10 18h4"/></svg>
        </span>
        <div class="sod-card-cust-body">
          <h3>{{ orderDetail.document.customer_name || orderDetail.document.customer || '—' }}</h3>
          <small>{{ [orderDetail.document.customer, orderDetail.customer_tax_id].filter(Boolean).join(' · ') || '—' }}</small>
        </div>
        <svg class="sod-card-chevron" viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
      </button>

      <div class="sod-card">
        <div class="sod-card-head">
          <span class="sod-card-icon orange">
            <svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/></svg>
          </span>
          <span class="sod-card-title">Thanh toán</span>
          <span class="sod-card-status">{{ orderDetail.payment.status }}</span>
          <svg class="sod-card-circle" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/></svg>
        </div>
        <div class="sod-field-group">
          <div class="sod-field"><span>Hạn thanh toán</span><b>{{ orderDetail.payment.due_date ? formatValue(orderDetail.payment.due_date, 'delivery_date') : '—' }}</b></div>
          <div class="sod-field"><span>Thực thu</span><b>{{ formatValue(orderDetail.payment.paid, 'grand_total') }}</b></div>
          <div class="sod-field"><span>Còn phải thu</span><b>{{ formatValue(orderDetail.payment.outstanding, 'grand_total') }}</b></div>
        </div>
      </div>

      <div class="sod-card">
        <div class="sod-card-head">
          <span class="sod-card-icon blue">
            <svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.62l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/></svg>
          </span>
          <span class="sod-card-title">Giao hàng</span>
        </div>
        <div class="sod-field-group">
          <div class="sod-field"><span>Hạn giao hàng</span><b>{{ orderDetail.shipping.delivery_date ? formatValue(orderDetail.shipping.delivery_date, 'delivery_date') : '—' }}</b></div>
          <div class="sod-field"><span>Người nhận hàng</span><b>{{ orderDetail.shipping.recipient || '—' }}</b></div>
          <div class="sod-field"><span>Điện thoại</span><b>{{ orderDetail.shipping.phone || '—' }}</b></div>
          <div class="sod-field"><span>Địa chỉ</span><b class="sod-address">{{ formatSOAddress(orderDetail.shipping.address) || '—' }}</b></div>
        </div>
      </div>

      <div class="sod-summary">
        <div class="sod-summary-head">
          <span class="sod-summary-title">Thông tin tóm tắt</span>
          <button class="sod-summary-btn" data-tooltip="Tùy chỉnh thông tin tóm tắt" aria-label="Tùy chỉnh thông tin tóm tắt" @click="openOrderSummaryDialog">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/></svg>
          </button>
        </div>
        <div class="sod-field-group">
          <div v-for="field in visibleOrderSummaryFields" :key="field.field" class="sod-summary-item">
            <small>{{ field.label }}</small><span>{{ orderSummaryValue(field.field) }}</span>
          </div>
          <div v-if="!visibleOrderSummaryFields.length" class="profile-facts-empty">Chưa chọn trường hiển thị.</div>
        </div>
      </div>
    </aside>

    <button
      class="sod-side-toggle"
      :class="{ collapsed: soSideCollapsed }"
      :aria-label="soSideCollapsed ? 'Hiện thông tin đơn hàng' : 'Ẩn thông tin đơn hàng'"
      :data-tooltip="soSideCollapsed ? 'Hiện thông tin' : 'Ẩn thông tin'"
      @click="toggleSOSidePanel"
    ><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg></button>

    <teleport to="body"><div v-if="orderSummaryDialogOpen" class="column-dialog-backdrop customer-summary-dialog-backdrop" @click.self="cancelOrderSummaryDialog">
      <section class="customer-summary-dialog" role="dialog" aria-modal="true" aria-labelledby="order-summary-dialog-title">
        <header>
          <div>
            <h2 id="order-summary-dialog-title">Tùy chỉnh tóm tắt</h2>
            <p>Chọn trường thông tin để hiển thị trong phần thông tin tóm tắt.</p>
          </div>
          <button class="customer-summary-close" data-tooltip="Đóng" aria-label="Đóng" @click="cancelOrderSummaryDialog">×</button>
        </header>
        <div class="customer-summary-picker">
          <section>
            <h3>Chưa chọn <span>{{ availableOrderSummaryFields.length }}</span></h3>
            <label class="customer-summary-search">
              <CRMIcon name="search" />
              <input v-model="orderSummarySearch" placeholder="Tìm kiếm trường" autofocus>
            </label>
            <div class="customer-summary-field-list">
              <button v-for="field in availableOrderSummaryFields" :key="field.field" type="button" @click="addOrderSummaryField(field.field)">
                <span>{{ field.label }}</span><b aria-hidden="true">+</b>
              </button>
              <p v-if="!availableOrderSummaryFields.length" class="crm-empty">Không còn trường phù hợp.</p>
            </div>
          </section>
          <section>
            <h3>Được chọn <span>{{ selectedOrderSummaryFields.length }}</span></h3>
            <div class="customer-summary-field-list customer-summary-field-list--selected">
              <button v-for="field in selectedOrderSummaryFields" :key="field.field" type="button" @click="removeOrderSummaryField(field.field)">
                <span>{{ field.label }}</span><b aria-hidden="true">×</b>
              </button>
              <p v-if="!selectedOrderSummaryFields.length" class="crm-empty">Chưa chọn trường nào.</p>
            </div>
          </section>
        </div>
        <footer>
          <button class="column-default" type="button" @click="resetOrderSummaryFields">Mặc định</button>
          <div>
            <button class="crm-button" type="button" @click="cancelOrderSummaryDialog">Hủy</button>
            <button class="crm-button primary" type="button" @click="saveOrderSummaryFields">Lưu</button>
          </div>
        </footer>
      </section>
    </div></teleport>

    <div class="sod-main">
      <nav class="sod-tabs">
        <button :class="{ active: orderDetailTab === 'items' }" @click="orderDetailTab = 'items'">Hàng hóa <span v-if="orderDetail.items.length" class="sod-tab-badge" :class="{ active: orderDetailTab === 'items' }">{{ orderDetail.items.length }}</span></button>
        <button :class="{ active: orderDetailTab === 'info' }" @click="orderDetailTab = 'info'">Thông tin chi tiết</button>
        <button :class="{ active: orderDetailTab === 'sales' }" @click="orderDetailTab = 'sales'">Chứng từ liên quan</button>
        <button :class="{ active: orderDetailTab === 'cashflow' }" @click="orderDetailTab = 'cashflow'">Thu chi</button>
        <button :class="{ active: orderDetailTab === 'actual_delivery' }" @click="orderDetailTab = 'actual_delivery'">Thực xuất</button>
        <button :class="{ active: orderDetailTab === 'support' }" @click="orderDetailTab = 'support'">Hỗ trợ</button>
        <button :class="{ active: orderDetailTab === 'contacts' }" @click="orderDetailTab = 'contacts'">Liên hệ</button>
        <button :class="{ active: orderDetailTab === 'notes' }" @click="orderDetailTab = 'notes'">Ghi chú và đính kèm</button>
        <button :class="{ active: orderDetailTab === 'activities' }" @click="orderDetailTab = 'activities'">Hoạt động <span v-if="orderDetail.activities.length" class="sod-tab-badge" :class="{ active: orderDetailTab === 'activities' }">{{ orderDetail.activities.length }}</span></button>
        <button :class="{ active: orderDetailTab === 'chat' }" @click="orderDetailTab = 'chat'">Trao đổi <span v-if="orderDetail.comments.length" class="sod-tab-badge" :class="{ active: orderDetailTab === 'chat' }">{{ orderDetail.comments.length }}</span></button>
        <button :class="{ active: orderDetailTab === 'other' }" @click="orderDetailTab = 'other'">Khác</button>
      </nav>

      <div class="sod-tabcontent">

        <template v-if="orderDetailTab === 'items'">
          <div class="goods-card">
            <div class="goods-top">
              <h3>Thông tin hàng hóa</h3>
              <div class="goods-top-links">
                <span class="goods-link" @click="openSOStockLookup()">
                  <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></svg>
                  Tra cứu số lượng tồn
                </span>
                <span class="goods-link" v-if="orderDetail.can_write" @click="openSOGoodsEditor()">
                  <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.12 2.12 0 0 1 3 3L12 15l-4 1 1-4Z"/></svg>
                  Cập nhật hàng hóa
                </span>
              </div>
            </div>

            <div class="goods-tablewrap">
              <table class="goods-table goods-table-wide">
                <colgroup>
                  <col style="width:48px"><col style="width:140px"><col style="width:180px"><col style="width:185px">
                  <col style="width:100px">
                  <col style="width:90px"><col style="width:80px"><col style="width:120px"><col style="width:130px">
                  <col style="width:110px"><col style="width:130px"><col style="width:140px"><col style="width:130px">
                  <col style="width:90px"><col style="width:130px"><col style="width:140px">
                  <col style="width:100px"><col style="width:100px"><col style="width:150px">
                </colgroup>
                <thead>
                  <tr>
                    <th class="gt-center">STT</th>
                    <th>Mã hàng hóa</th>
                    <th>Tên hàng hóa</th>
                    <th>Mô tả</th>
                    <th class="gt-center">Account</th>
                    <th>Đơn vị tính</th>
                    <th class="gt-center">Số lượng</th>
                    <th class="gt-right">Đơn giá</th>
                    <th class="gt-right">Thành tiền</th>
                    <th class="gt-center">Tỷ lệ CK</th>
                    <th class="gt-right">Tiền chiết khấu</th>
                    <th class="gt-right">Thành tiền sau CK</th>
                    <th class="gt-right">Đơn giá sau CK</th>
                    <th class="gt-center">Thuế suất</th>
                    <th class="gt-right">Tiền thuế</th>
                    <th class="gt-right">Tổng tiền</th>
                    <th class="gt-center">Số lượng đặt</th>
                    <th class="gt-center">Số lượng giao</th>
                    <th>Kho</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="!orderDetail.items.length">
                    <td colspan="19" class="gt-empty">Chưa có hàng hóa.</td>
                  </tr>
                  <tr v-for="item in orderDetail.items" :key="item.idx">
                    <td class="gt-center">{{ item.idx }}</td>
                    <td class="gt-code">{{ item.item_code }}</td>
                    <td>{{ item.item_name || item.item_code }}</td>
                    <td class="gt-desc">
                      <div class="gt-desc-html" :class="{ collapsed: !soItemDescExpanded.includes(item.idx) }">{{ stripHtml(item.description || '') }}</div>
                      <a v-if="item.description && item.description.length > 60" class="gt-more" @click="toggleSOItemDesc(item.idx)">{{ soItemDescExpanded.includes(item.idx) ? 'thu gọn' : 'xem thêm' }}</a>
                    </td>
                    <td class="gt-center">
                      <span v-if="item.custom_dcnet_account_id" class="item-account-badge">{{ item.custom_dcnet_account_id }}</span>
                      <span v-else class="gt-muted">—</span>
                    </td>
                    <td>{{ item.uom }}</td>
                    <td class="gt-center">{{ item.qty }}</td>
                    <td class="gt-right">{{ formatValue(item.price_list_rate, 'grand_total') }}</td>
                    <td class="gt-right">{{ formatValue(item.gross_amount, 'grand_total') }}</td>
                    <td class="gt-center">{{ item.discount_percentage ? item.discount_percentage + '%' : '' }}</td>
                    <td class="gt-right">{{ formatValue(item.discount_amount, 'grand_total') }}</td>
                    <td class="gt-right">{{ formatValue(item.net_amount, 'grand_total') }}</td>
                    <td class="gt-right">{{ formatValue(item.net_rate, 'grand_total') }}</td>
                    <td class="gt-center">{{ item.tax_rate ? item.tax_rate + '%' : '' }}</td>
                    <td class="gt-right">{{ formatValue(item.tax_amount, 'grand_total') }}</td>
                    <td class="gt-right">{{ formatValue(item.total_with_tax, 'grand_total') }}</td>
                    <td class="gt-center">{{ item.qty }}</td>
                    <td class="gt-center">{{ item.delivered_qty || 0 }}</td>
                    <td>{{ item.warehouse || '' }}</td>
                  </tr>
                </tbody>
                <tfoot v-if="orderDetail.items.length">
                  <tr class="gt-total-row">
                    <td colspan="6" class="gt-total-label">Tổng cộng</td>
                    <td class="gt-center">{{ orderDetailTotalQty() }}</td>
                    <td class="gt-right"></td>
                    <td class="gt-right">{{ formatValue(orderDetail.document.base_total, 'grand_total') }}</td>
                    <td class="gt-center"></td>
                    <td class="gt-right">{{ formatValue(orderDetail.document.discount_amount, 'grand_total') }}</td>
                    <td class="gt-right">{{ formatValue(orderDetail.document.net_total, 'grand_total') }}</td>
                    <td class="gt-right"></td>
                    <td class="gt-center"></td>
                    <td class="gt-right">{{ formatValue(orderDetailTotalTax(), 'grand_total') }}</td>
                    <td class="gt-right">{{ formatValue(orderDetail.document.grand_total, 'grand_total') }}</td>
                    <td class="gt-center">{{ orderDetailTotalQty() }}</td>
                    <td class="gt-center">{{ orderDetailTotalDelivered() }}</td>
                    <td></td>
                  </tr>
                </tfoot>
              </table>
            </div>

            <div class="goods-pager">
              <span class="goods-pager-total">Tổng số <b>{{ orderDetail.items.length }}</b></span>
              <div class="goods-pager-right">
                <span class="goods-pager-label">Số dòng/trang</span>
                <span class="goods-pager-select">20
                  <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
                </span>
                <span class="goods-pager-range">1 - {{ orderDetail.items.length }}</span>
                <button class="goods-pager-nav" disabled>«</button>
                <button class="goods-pager-nav" disabled>‹</button>
                <button class="goods-pager-nav" disabled>›</button>
                <button class="goods-pager-nav" disabled>»</button>
              </div>
            </div>
          </div>
        </template>


        <template v-else-if="orderDetailTab === 'info'">
          <div class="sod-detail-view">

            <!-- Toggle -->
            <div class="sod-detail-topbar">
              <label class="sod-dtoggle-label">
                <input type="checkbox" v-model="soDetailShowEmpty" class="sod-dtoggle-inp">
                <span class="sod-dtoggle-track"></span>
                Hiển thị dữ liệu trống
              </label>
            </div>

            <!-- ── Thông tin chung ─────────────────────────────── -->
            <div class="sod-section">
              <h3 class="sod-section-title">Thông tin chung</h3>
              <div class="sod-detail-grid">
                <div class="sod-drow">
                  <span class="sod-dlabel">Khách hàng</span>
                  <span class="sod-dval"><a class="sod-dlink">{{ orderDetail.document.customer_name || orderDetail.document.customer || '—' }}</a></span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Liên hệ</span>
                  <span class="sod-dval">
                    <a v-if="orderDetail.document.contact_person" class="sod-dlink">{{ orderDetail.document.contact_display || orderDetail.document.contact_person }}</a>
                    <span v-else class="sod-dval-empty">— Không chọn —</span>
                  </span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Cơ hội</span>
                  <span class="sod-dval">
                    <a v-if="orderDetail.document.opportunity" class="sod-dlink sod-dlink--green">{{ orderDetail.document.opportunity }}</a>
                    <span v-else class="sod-dval-empty">— Không chọn —</span>
                  </span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Diễn giải</span>
                  <span class="sod-dval">{{ orderDetail.document.title || '—' }}</span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Số đơn hàng/hợp đồng <i class="sod-info-hint" data-tooltip="Số đơn hàng hoặc số hợp đồng">i</i></span>
                  <span class="sod-dval">{{ orderDetail.document.name }}</span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Ngày đặt hàng</span>
                  <span class="sod-dval">{{ formatValue(orderDetail.document.transaction_date, 'transaction_date') || '—' }}</span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Loại hàng hóa</span>
                  <span class="sod-dval">
                    <template v-if="orderDetail.items.length">
                      <span v-for="(code, idx) in [...new Set(orderDetail.items.map(i => i.item_code))].slice(0, 5)" :key="idx" class="sod-dtag">{{ code }}</span>
                    </template>
                    <span v-else class="sod-dval-empty">—</span>
                  </span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Loại đơn hàng</span>
                  <span class="sod-dval">
                    <a v-if="orderDetail.document.order_type" class="sod-dlink">{{ orderDetail.document.order_type }}</a>
                    <span v-else class="sod-dval-empty">—</span>
                  </span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Đơn hàng cha</span>
                  <span class="sod-dval">
                    <span v-if="orderDetail.document.custom_parent_order" class="sod-dlink">{{ orderDetail.document.custom_parent_order }}</span>
                    <span v-else class="sod-dval-empty">— Không chọn —</span>
                  </span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Bảo giá</span>
                  <span class="sod-dval">
                    <a v-if="orderDetail.quotations && orderDetail.quotations.length" class="sod-dlink">{{ orderDetail.quotations[0].name }}</a>
                    <span v-else class="sod-dval-empty">—</span>
                  </span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Giá trị đơn hàng</span>
                  <span class="sod-dval">{{ formatValue(orderDetail.document.grand_total, 'grand_total') }}</span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Khu vực lắp đặt dịch vụ</span>
                  <span class="sod-dval">
                    <span v-if="orderDetail.document.custom_installation_zone">{{ orderDetail.document.custom_installation_zone }}</span>
                    <span v-else class="sod-dval-empty">— Không chọn —</span>
                  </span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Số ngày được nợ</span>
                  <span class="sod-dval">{{ orderDetail.document.custom_days_receivable ?? 0 }}</span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Hạn giao hàng</span>
                  <span class="sod-dval">{{ orderDetail.document.delivery_date ? formatValue(orderDetail.document.delivery_date, 'delivery_date') : '—' }}</span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Loại hợp đồng</span>
                  <span class="sod-dval">
                    <span v-if="orderDetail.document.custom_contract_type">{{ orderDetail.document.custom_contract_type }}</span>
                    <span v-else class="sod-dval-empty">— Không chọn —</span>
                  </span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Thời hạn HĐg (tháng)</span>
                  <span class="sod-dval">{{ orderDetail.document.custom_contract_duration ?? 0 }}</span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Ngày ký Hợp đồng</span>
                  <span class="sod-dval">{{ orderDetail.document.po_date ? formatValue(orderDetail.document.po_date, 'transaction_date') : '—' }}</span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Ngày hết hạn hợp đồng</span>
                  <span class="sod-dval">{{ orderDetail.document.custom_contract_expiry ? formatValue(orderDetail.document.custom_contract_expiry, 'transaction_date') : '—' }}</span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Ngày thanh lý</span>
                  <span class="sod-dval">{{ orderDetail.document.custom_liquidation_date ? formatValue(orderDetail.document.custom_liquidation_date, 'transaction_date') : '—' }}</span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Giá trị thanh lý</span>
                  <span class="sod-dval">{{ (orderDetail.document.custom_liquidation_value ? formatValue(orderDetail.document.custom_liquidation_value, 'grand_total') : '—') }}</span>
                </div>

                <div class="sod-drow"></div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Chiến dịch</span>
                  <span class="sod-dval">
                    <span v-if="orderDetail.document.campaign">{{ orderDetail.document.campaign }}</span>
                    <span v-else class="sod-dval-empty">— Không chọn —</span>
                  </span>
                </div>

                <div class="sod-drow"></div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Số ĐĐH từ hệ thống khác</span>
                  <span class="sod-dval">{{ orderDetail.document.po_no || '—' }}</span>
                </div>
              </div>
            </div>

            <!-- ── Thông tin mô tả ─────────────────────────────── -->
            <div class="sod-section">
              <h3 class="sod-section-title">Thông tin mô tả</h3>
              <div class="sod-detail-grid">
                <div class="sod-drow sod-drow--full" style="min-height:80px">
                  <span class="sod-dlabel" style="padding-top:10px">Mô tả</span>
                  <span class="sod-dval sod-dval--top" style="white-space:pre-wrap">{{ orderDetail.document.notes || orderDetail.document.note || orderDetail.document.custom_note || '—' }}</span>
                </div>
              </div>
            </div>

            <!-- ── Thông tin hàng hóa ──────────────────────────── -->
            <div class="sod-section sod-detail-section-goods">
              <div class="goods-card">
                <div class="goods-top">
                  <h3>Thông tin hàng hóa</h3>
                  <div class="goods-top-links">
                    <span class="goods-link" @click="openSOStockLookup()">
                      <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></svg>
                      Tra cứu số lượng tồn
                    </span>
                    <span class="goods-link" v-if="orderDetail.can_write" @click="openSOGoodsEditor()">
                      <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.12 2.12 0 0 1 3 3L12 15l-4 1 1-4Z"/></svg>
                      Cập nhật hàng hóa
                    </span>
                  </div>
                </div>
                <div class="goods-tablewrap">
                  <table class="goods-table goods-table-wide">
                    <colgroup>
                      <col style="width:48px"><col style="width:140px"><col style="width:180px"><col style="width:185px">
                      <col style="width:100px">
                      <col style="width:90px"><col style="width:80px"><col style="width:120px"><col style="width:130px">
                      <col style="width:110px"><col style="width:130px"><col style="width:140px"><col style="width:130px">
                      <col style="width:90px"><col style="width:130px"><col style="width:140px">
                      <col style="width:100px"><col style="width:100px"><col style="width:150px">
                    </colgroup>
                    <thead>
                      <tr>
                        <th class="gt-center">STT</th><th>Mã hàng hóa</th><th>Tên hàng hóa</th><th>Mô tả</th>
                        <th class="gt-center">Account</th>
                        <th>Đơn vị tính</th><th class="gt-center">Số lượng</th><th class="gt-right">Đơn giá</th>
                        <th class="gt-right">Thành tiền</th><th class="gt-center">Tỷ lệ CK</th>
                        <th class="gt-right">Tiền chiết khấu</th><th class="gt-right">Thành tiền sau CK</th>
                        <th class="gt-right">Đơn giá sau CK</th><th class="gt-center">Thuế suất</th>
                        <th class="gt-right">Tiền thuế</th><th class="gt-right">Tổng tiền</th>
                        <th class="gt-center">Số lượng đặt</th><th class="gt-center">Số lượng giao</th><th>Kho</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-if="!orderDetail.items.length"><td colspan="19" class="gt-empty">Chưa có hàng hóa.</td></tr>
                      <tr v-for="item in orderDetail.items" :key="item.idx">
                        <td class="gt-center">{{ item.idx }}</td>
                        <td class="gt-code">{{ item.item_code }}</td>
                        <td>{{ item.item_name || item.item_code }}</td>
                        <td class="gt-desc">
                          <div class="gt-desc-html" :class="{ collapsed: !soItemDescExpanded.includes(item.idx) }">{{ stripHtml(item.description || '') }}</div>
                          <a v-if="item.description && item.description.length > 60" class="gt-more" @click="toggleSOItemDesc(item.idx)">{{ soItemDescExpanded.includes(item.idx) ? 'thu gọn' : 'xem thêm' }}</a>
                        </td>
                        <td class="gt-center">
                          <span v-if="item.custom_dcnet_account_id" class="item-account-badge">{{ item.custom_dcnet_account_id }}</span>
                          <span v-else class="gt-muted">—</span>
                        </td>
                        <td>{{ item.uom }}</td>
                        <td class="gt-center">{{ item.qty }}</td>
                        <td class="gt-right">{{ formatValue(item.price_list_rate, 'grand_total') }}</td>
                        <td class="gt-right">{{ formatValue(item.gross_amount, 'grand_total') }}</td>
                        <td class="gt-center">{{ item.discount_percentage ? item.discount_percentage + '%' : '' }}</td>
                        <td class="gt-right">{{ formatValue(item.discount_amount, 'grand_total') }}</td>
                        <td class="gt-right">{{ formatValue(item.net_amount, 'grand_total') }}</td>
                        <td class="gt-right">{{ formatValue(item.net_rate, 'grand_total') }}</td>
                        <td class="gt-center">{{ item.tax_rate ? item.tax_rate + '%' : '' }}</td>
                        <td class="gt-right">{{ formatValue(item.tax_amount, 'grand_total') }}</td>
                        <td class="gt-right">{{ formatValue(item.total_with_tax, 'grand_total') }}</td>
                        <td class="gt-center">{{ item.qty }}</td>
                        <td class="gt-center">{{ item.delivered_qty || 0 }}</td>
                        <td>{{ item.warehouse || '' }}</td>
                      </tr>
                    </tbody>
                    <tfoot v-if="orderDetail.items.length">
                      <tr class="gt-total-row">
                        <td colspan="6" class="gt-total-label">Tổng cộng</td>
                        <td class="gt-center">{{ orderDetailTotalQty() }}</td>
                        <td></td>
                        <td class="gt-right">{{ formatValue(orderDetail.document.base_total, 'grand_total') }}</td>
                        <td></td>
                        <td class="gt-right">{{ formatValue(orderDetail.document.discount_amount, 'grand_total') }}</td>
                        <td class="gt-right">{{ formatValue(orderDetail.document.net_total, 'grand_total') }}</td>
                        <td></td><td></td>
                        <td class="gt-right">{{ formatValue(orderDetailTotalTax(), 'grand_total') }}</td>
                        <td class="gt-right">{{ formatValue(orderDetail.document.grand_total, 'grand_total') }}</td>
                        <td class="gt-center">{{ orderDetailTotalQty() }}</td>
                        <td class="gt-center">{{ orderDetailTotalDelivered() }}</td>
                        <td></td>
                      </tr>
                    </tfoot>
                  </table>
                </div>
                <div class="goods-pager">
                  <span class="goods-pager-total">Tổng số <b>{{ orderDetail.items.length }}</b></span>
                  <div class="goods-pager-right">
                    <span class="goods-pager-label">Số dòng/trang</span>
                    <span class="goods-pager-select">20 <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg></span>
                    <span class="goods-pager-range">1 - {{ orderDetail.items.length }}</span>
                    <button class="goods-pager-nav" disabled>«</button>
                    <button class="goods-pager-nav" disabled>‹</button>
                    <button class="goods-pager-nav" disabled>›</button>
                    <button class="goods-pager-nav" disabled>»</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- ── Tình trạng thực hiện đơn hàng ─────────────────── -->
            <div class="sod-section">
              <h3 class="sod-section-title">Tình trạng thực hiện đơn hàng</h3>
              <div class="sod-detail-grid">
                <div class="sod-drow">
                  <span class="sod-dlabel">Tình trạng</span>
                  <span class="sod-dval">
                    <span v-if="orderDetail.document.display_execution_status" class="sod-dstatus sod-dstatus--check">{{ orderDetail.document.display_execution_status }}</span>
                    <span v-else class="sod-dval-empty">—</span>
                  </span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Tình trạng ghi doanh số</span>
                  <span class="sod-dval">{{ orderDetail.document.display_revenue_status || 'Đơn nháp' }}</span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Ngày ghi số</span>
                  <span class="sod-dval">{{ orderDetail.document.custom_revenue_recognition_date ? formatValue(orderDetail.document.custom_revenue_recognition_date, 'transaction_date') : '—' }}</span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Chu kỳ thanh toán</span>
                  <span class="sod-dval">{{ orderDetail.document.payment_terms_template || '—' }}</span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Tình trạng giao hàng</span>
                  <span class="sod-dval">
                    <span v-if="orderDetail.document.delivery_status">{{ orderDetail.document.delivery_status }}</span>
                    <span v-else class="sod-dval-empty">— Không chọn —</span>
                  </span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Ngày nghiệm thu tính cước</span>
                  <span class="sod-dval">{{ orderDetail.document.custom_acceptance_date ? formatValue(orderDetail.document.custom_acceptance_date, 'transaction_date') : '—' }}</span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Hạn thanh toán</span>
                  <span class="sod-dval">{{ orderDetail.payment.due_date ? formatValue(orderDetail.payment.due_date, 'delivery_date') : '—' }}</span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Đã xuất hóa đơn</span>
                  <span class="sod-dval">
                    <span :class="['sod-dbool', orderDetail.invoices && orderDetail.invoices.length ? 'sod-dbool--checked' : '']">{{ orderDetail.invoices && orderDetail.invoices.length ? '✓' : '' }}</span>
                  </span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Số hóa đơn <i class="sod-info-hint" data-tooltip="Danh sách hóa đơn đã xuất">i</i></span>
                  <span class="sod-dval">
                    <template v-if="orderDetail.invoices && orderDetail.invoices.length">
                      <a v-for="inv in orderDetail.invoices.slice(0,3)" :key="inv.name" class="sod-dlink" style="margin-right:6px">{{ inv.name }}</a>
                    </template>
                    <span v-else class="sod-dval-empty">—</span>
                  </span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Ngày hóa đơn <i class="sod-info-hint" data-tooltip="Ngày xuất hóa đơn gần nhất">i</i></span>
                  <span class="sod-dval">{{ orderDetail.invoices && orderDetail.invoices.length ? formatValue(orderDetail.invoices[0].posting_date, 'transaction_date') : '—' }}</span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Tình trạng thanh toán</span>
                  <span class="sod-dval">{{ orderDetail.payment.status || 'Chưa thanh toán' }}</span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Giá trị chưa xuất hóa đơn</span>
                  <span class="sod-dval">{{ formatValue(orderDetail.document.grand_total - (orderDetail.invoices || []).reduce((s,i)=>s+(i.grand_total||0),0), 'grand_total') }}</span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Giá trị đã xuất hóa đơn</span>
                  <span class="sod-dval">{{ formatValue((orderDetail.invoices||[]).reduce((s,i)=>s+(i.grand_total||0),0), 'grand_total') }}</span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Thực thu</span>
                  <span class="sod-dval">{{ formatValue(orderDetail.payment.paid, 'grand_total') }}</span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Còn phải thu</span>
                  <span class="sod-dval">{{ formatValue(orderDetail.payment.outstanding, 'grand_total') }}</span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Ngày thanh toán</span>
                  <span class="sod-dval">{{ orderDetail.payment_entries && orderDetail.payment_entries.length ? formatValue(orderDetail.payment_entries[0].posting_date, 'transaction_date') : '—' }}</span>
                </div>

                <div class="sod-drow"></div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Dự kiến chi</span>
                  <span class="sod-dval">{{ formatValue(orderDetail.document.custom_expected_cost || 0, 'grand_total') }}</span>
                </div>

                <div class="sod-drow"></div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Hạn sản xuất</span>
                  <span class="sod-dval">{{ orderDetail.document.custom_production_deadline ? formatValue(orderDetail.document.custom_production_deadline, 'transaction_date') : '—' }}</span>
                </div>
              </div>
            </div>

            <!-- ── Thông tin hóa đơn ──────────────────────────────── -->
            <div class="sod-section">
              <h3 class="sod-section-title">Thông tin hóa đơn</h3>
              <div class="sod-detail-grid">
                <div class="sod-drow">
                  <span class="sod-dlabel">Khách hàng (Hóa đơn)</span>
                  <span class="sod-dval"><a class="sod-dlink">{{ orderDetail.document.customer_name || orderDetail.document.customer || '—' }}</a></span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Người mua hàng</span>
                  <span class="sod-dval">
                    <a v-if="orderDetail.document.contact_person" class="sod-dlink">{{ orderDetail.document.contact_display || orderDetail.document.contact_person }}</a>
                    <span v-else class="sod-dval-empty">— Không chọn —</span>
                  </span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Quốc gia (Hóa đơn)</span>
                  <span class="sod-dval">{{ orderDetail.document.billing_address_country || 'Việt Nam' }}</span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Tỉnh/Thành phố (Hóa đơn)</span>
                  <span class="sod-dval">{{ orderDetail.document.billing_city || '—' }}</span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Quận/Huyện (Hóa đơn)</span>
                  <span class="sod-dval">{{ orderDetail.document.billing_county || '—' }}</span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Phường/Xã (Hóa đơn)</span>
                  <span class="sod-dval">{{ orderDetail.document.billing_ward || '—' }}</span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Số nhà, Đường phố (Hóa đơn)</span>
                  <span class="sod-dval">{{ orderDetail.document.billing_address_line1 || '—' }}</span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Mã vùng (Hóa đơn)</span>
                  <span class="sod-dval">{{ orderDetail.document.billing_zip || '—' }}</span>
                </div>

                <div class="sod-drow sod-drow--full" style="min-height:54px">
                  <span class="sod-dlabel" style="padding-top:10px">Địa chỉ (Hóa đơn)</span>
                  <span class="sod-dval sod-dval--top" style="white-space:pre-wrap">{{ formatSOAddress(orderDetail.document.address_display || orderDetail.document.shipping_address_name) || '—' }}</span>
                </div>
              </div>
            </div>

            <!-- ── Thông tin giao hàng ─────────────────────────────── -->
            <div class="sod-section">
              <h3 class="sod-section-title">Thông tin giao hàng</h3>
              <div class="sod-detail-grid">
                <div class="sod-drow">
                  <span class="sod-dlabel">Người nhận hàng</span>
                  <span class="sod-dval">{{ orderDetail.shipping.recipient || '—' }}</span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Điện thoại</span>
                  <span class="sod-dval">{{ orderDetail.shipping.phone || '—' }}</span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Quốc gia (Giao hàng)</span>
                  <span class="sod-dval">{{ orderDetail.document.shipping_address_country || '—' }}</span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Tỉnh/Thành phố (Giao hàng)</span>
                  <span class="sod-dval">{{ orderDetail.document.shipping_city || '—' }}</span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Quận/Huyện (Giao hàng)</span>
                  <span class="sod-dval">{{ orderDetail.document.shipping_county || '—' }}</span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Phường/Xã (Giao hàng)</span>
                  <span class="sod-dval">{{ orderDetail.document.shipping_ward || '—' }}</span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Số nhà, Đường phố (Giao hàng)</span>
                  <span class="sod-dval">{{ orderDetail.document.shipping_address_line1 || '—' }}</span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Mã vùng (Giao hàng)</span>
                  <span class="sod-dval">{{ orderDetail.document.shipping_zip || '—' }}</span>
                </div>

                <div class="sod-drow sod-drow--full" style="min-height:54px">
                  <span class="sod-dlabel" style="padding-top:10px">Địa chỉ (Giao hàng)</span>
                  <span class="sod-dval sod-dval--top" style="white-space:pre-wrap">{{ formatSOAddress(orderDetail.shipping.address) || '—' }}</span>
                </div>
              </div>
            </div>

            <!-- ── Thông tin hệ thống ──────────────────────────────── -->
            <div class="sod-section">
              <h3 class="sod-section-title">Thông tin hệ thống</h3>
              <div class="sod-detail-grid">
                <div class="sod-drow">
                  <span class="sod-dlabel">Người thực hiện</span>
                  <span class="sod-dval"><a class="sod-dlink">{{ orderDetail.document.owner || '—' }}</a></span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Đơn vị</span>
                  <span class="sod-dval">{{ orderDetail.document.company || '—' }}</span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Nhân viên được ghi DS <i class="sod-info-hint" data-tooltip="Nhân viên phụ trách ghi doanh số">i</i></span>
                  <span class="sod-dval"><a class="sod-dlink">{{ orderDetail.document.custom_revenue_owner || orderDetail.document.owner || '—' }}</a></span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Đơn vị được ghi DS <i class="sod-info-hint" data-tooltip="Đơn vị phụ trách ghi doanh số">i</i></span>
                  <span class="sod-dval">{{ orderDetail.document.custom_revenue_company || orderDetail.document.company || '—' }}</span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Người tạo</span>
                  <span class="sod-dval"><a class="sod-dlink">{{ orderDetail.document.owner || '—' }}</a></span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Ngày tạo</span>
                  <span class="sod-dval">{{ orderDetail.document.creation ? formatValue(orderDetail.document.creation, 'creation') : '—' }}</span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Đúng tuyến</span>
                  <span class="sod-dval">
                    <span :class="['sod-dbool', orderDetail.document.custom_on_route ? 'sod-dbool--checked' : '']">{{ orderDetail.document.custom_on_route ? '✓' : '' }}</span>
                  </span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Ngày sửa</span>
                  <span class="sod-dval">{{ orderDetail.document.modified ? formatValue(orderDetail.document.modified, 'creation') : '—' }}</span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Có ghế thăm</span>
                  <span class="sod-dval">
                    <span :class="['sod-dbool', orderDetail.document.custom_has_visit ? 'sod-dbool--checked' : '']">{{ orderDetail.document.custom_has_visit ? '✓' : '' }}</span>
                  </span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Ngừng theo dõi</span>
                  <span class="sod-dval">
                    <span :class="['sod-dbool', orderDetail.document._liked_by ? 'sod-dbool--checked' : '']">{{ orderDetail.document._liked_by ? '✓' : '' }}</span>
                  </span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Người sửa</span>
                  <span class="sod-dval"><a class="sod-dlink">{{ orderDetail.document.modified_by || '—' }}</a></span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Đồng bộ đơn giá sau CK <i class="sod-info-hint" data-tooltip="Tự động đồng bộ đơn giá sau chiết khấu">i</i></span>
                  <span class="sod-dval">
                    <span :class="['sod-dbool', orderDetail.document.custom_sync_net_rate ? 'sod-dbool--checked' : '']">{{ orderDetail.document.custom_sync_net_rate ? '✓' : '' }}</span>
                  </span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Dùng chung</span>
                  <span class="sod-dval">
                    <span :class="['sod-dbool', orderDetail.document.custom_shared ? 'sod-dbool--checked' : '']">{{ orderDetail.document.custom_shared ? '✓' : '' }}</span>
                  </span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Là đơn hàng cha</span>
                  <span class="sod-dval">
                    <span :class="['sod-dbool', orderDetail.document.custom_is_parent_order ? 'sod-dbool--checked' : '']">{{ orderDetail.document.custom_is_parent_order ? '✓' : '' }}</span>
                  </span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Bố cục</span>
                  <span class="sod-dval">{{ orderDetail.document.custom_layout || orderDetail.document.order_type || '—' }}</span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Người liên quan</span>
                  <span class="sod-dval">
                    <template v-if="orderDetail.contacts && orderDetail.contacts.length">
                      <a v-for="c in orderDetail.contacts.slice(0,3)" :key="c.name" class="sod-dlink" style="margin-right:6px">{{ c.full_name || c.name }}</a>
                    </template>
                    <span v-else class="sod-dval-empty">—</span>
                  </span>
                </div>

                <div class="sod-drow">
                  <span class="sod-dlabel">Đối tác/CTV giới thiệu</span>
                  <span class="sod-dval">
                    <span v-if="orderDetail.document.custom_referral_partner">{{ orderDetail.document.custom_referral_partner }}</span>
                    <span v-else class="sod-dval-empty">— Không chọn —</span>
                  </span>
                </div>
                <div class="sod-drow">
                  <span class="sod-dlabel">Giá trị trả lại</span>
                  <span class="sod-dval">{{ formatValue(orderDetail.document.custom_return_value || 0, 'grand_total') }}</span>
                </div>
              </div>
            </div>

          </div>
        </template>

        <div v-else-if="orderDetailTab === 'sales'" class="profile-tab-layout profile-group-layout">
          <nav class="profile-subnav">
            <button :class="{ active: orderRelatedSection === 'quotations' }" @click="orderRelatedSection = 'quotations'"><CRMIcon name="quotation" />Báo giá <b v-if="orderDetail.quotations.length">{{ orderDetail.quotations.length }}</b></button>
            <button :class="{ active: orderRelatedSection === 'delivery_notes' }" @click="orderRelatedSection = 'delivery_notes'"><CRMIcon name="package" />Phiếu giao hàng <b v-if="orderDetail.delivery_notes.length">{{ orderDetail.delivery_notes.length }}</b></button>
            <button :class="{ active: orderRelatedSection === 'invoices' }" @click="orderRelatedSection = 'invoices'"><CRMIcon name="document" />Hóa đơn <b v-if="orderDetail.invoices_count">{{ orderDetail.invoices_count }}</b></button>
            <button :class="{ active: orderRelatedSection === 'payment_entries' }" @click="orderRelatedSection = 'payment_entries'"><CRMIcon name="dollar" />Thanh toán <b v-if="orderDetail.payment_entries.length">{{ orderDetail.payment_entries.length }}</b></button>
          </nav>
          <section class="profile-records">
            <div class="profile-records-heading"><div><h2>{{ orderRelatedSectionLabel(orderRelatedSection) }}</h2><button data-tooltip="Làm mới" @click="loadOrderDetail(orderDetail.document.name)"><CRMIcon name="refresh" /></button></div></div>

            <template v-if="orderRelatedSection === 'quotations'">
              <div v-if="orderDetail.quotations.length" class="profile-table-wrap">
                <table class="profile-related-table">
                  <thead><tr><th>Số báo giá</th><th>Ngày báo giá</th><th>Hiệu lực đến ngày</th><th>Tổng tiền</th><th>Tình trạng</th><th>Mô tả</th></tr></thead>
                  <tbody><tr v-for="row in orderDetail.quotations" :key="row.name" @click="openRelated('Quotation', row)">
                    <td><a href="#" @click.prevent.stop="openRelated('Quotation', row)">{{ row.name }}</a></td>
                    <td>{{ formatValue(row.transaction_date, 'date') }}</td><td>—</td>
                    <td>{{ formatValue(row.grand_total, 'grand_total') }}</td><td>{{ row.status || '—' }}</td><td>—</td>
                  </tr></tbody>
                </table>
              </div>
              <div v-else class="sales-empty"><span>Không có bản ghi nào</span></div>
            </template>
            <template v-else-if="orderRelatedSection === 'delivery_notes'">
              <div v-if="orderDetail.delivery_notes.length" class="profile-table-wrap">
                <table class="profile-related-table">
                  <thead><tr><th>Số phiếu giao hàng</th><th>Ngày giao hàng</th><th>Tổng tiền</th><th>Tình trạng</th></tr></thead>
                  <tbody><tr v-for="row in orderDetail.delivery_notes" :key="row.name" @click="openRelated('Delivery Note', row)">
                    <td><a href="#" @click.prevent.stop="openRelated('Delivery Note', row)">{{ row.name }}</a></td>
                    <td>{{ formatValue(row.posting_date, 'date') }}</td>
                    <td>{{ formatValue(row.grand_total, 'grand_total') }}</td><td>{{ row.status || '—' }}</td>
                  </tr></tbody>
                </table>
              </div>
              <div v-else class="sales-empty"><span>Không có bản ghi nào</span></div>
            </template>
            <template v-else-if="orderRelatedSection === 'invoices'">
              <div v-if="orderDetail.invoices.length" class="profile-table-wrap">
                <table class="profile-related-table">
                  <thead><tr><th>Số hóa đơn</th><th>Ngày hóa đơn</th><th>Tổng tiền</th><th>Còn phải thu</th><th>Tình trạng</th></tr></thead>
                  <tbody><tr v-for="row in orderDetail.invoices" :key="row.name" @click="openRelated('Sales Invoice', row)">
                    <td><a href="#" @click.prevent.stop="openRelated('Sales Invoice', row)">{{ row.name }}</a></td>
                    <td>{{ formatValue(row.posting_date, 'date') }}</td>
                    <td>{{ formatValue(row.grand_total, 'grand_total') }}</td>
                    <td>{{ formatValue(row.outstanding_amount, 'grand_total') }}</td><td>{{ row.status || '—' }}</td>
                  </tr></tbody>
                </table>
              </div>
              <div v-else class="sales-empty"><span>Không có bản ghi nào</span></div>
            </template>
            <template v-else-if="orderRelatedSection === 'payment_entries'">
              <div v-if="orderDetail.payment_entries.length" class="profile-table-wrap">
                <table class="profile-related-table">
                  <thead><tr><th>Số phiếu</th><th>Ngày ghi sổ</th><th>Số tiền</th><th>Hình thức</th><th>Tình trạng</th></tr></thead>
                  <tbody><tr v-for="row in orderDetail.payment_entries" :key="row.name" @click="openRelated('Payment Entry', row)">
                    <td><a href="#" @click.prevent.stop="openRelated('Payment Entry', row)">{{ row.name }}</a></td>
                    <td>{{ formatValue(row.posting_date, 'date') }}</td>
                    <td>{{ formatValue(row.paid_amount, 'grand_total') }}</td>
                    <td>{{ row.mode_of_payment || '—' }}</td><td>{{ row.status || '—' }}</td>
                  </tr></tbody>
                </table>
              </div>
              <div v-else class="sales-empty"><span>Không có bản ghi nào</span></div>
            </template>
          </section>
        </div>

        <div v-else-if="orderDetailTab === 'contacts'" class="profile-contacts-panel">
          <div class="profile-contacts-card">
            <header class="contacts-table-heading">
              <div><h2>Liên hệ</h2><button data-tooltip="Làm mới" @click="loadOrderDetail(orderDetail.document.name)"><CRMIcon name="refresh" /></button></div>
              <div>
                <button @click="openSOContactDialog">＋ Thêm nhanh</button>
                <button @click="openSOContactPicker">☑ Chọn</button>
              </div>
            </header>
            <div v-if="!orderDetail.contacts.length" class="crm-empty" style="margin-top:40px">Không có bản ghi nào</div>
            <table v-else class="customer-table">
              <thead><tr><th>Họ tên</th><th>Chức danh</th><th>Điện thoại</th><th>Email</th><th>Tổ chức</th></tr></thead>
              <tbody>
                <tr v-for="c in orderDetail.contacts" :key="c.name" @click="openRelated('Contact', c)" style="cursor:pointer">
                  <td>{{ c.full_name || c.name }}</td>
                  <td>{{ c.designation || '—' }}</td>
                  <td>{{ c.mobile_no || '—' }}</td>
                  <td>{{ c.email_id || '—' }}</td>
                  <td>{{ c.company_name || '—' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div v-else-if="orderDetailTab === 'cashflow'" class="profile-tab-layout profile-group-layout">
          <nav class="profile-subnav">
            <button :class="{ active: orderCashflowSection === 'actual_receipt' }" @click="orderCashflowSection = 'actual_receipt'"><CRMIcon name="dollar" />Thực thu <b v-if="orderActualReceipts.length">{{ orderActualReceipts.length }}</b></button>
            <button :class="{ active: orderCashflowSection === 'planned_payment' }" @click="orderCashflowSection = 'planned_payment'"><CRMIcon name="document" />Dự kiến chi</button>
            <button :class="{ active: orderCashflowSection === 'actual_payment' }" @click="orderCashflowSection = 'actual_payment'"><CRMIcon name="dollar" />Thực chi <b v-if="orderActualPayments.length">{{ orderActualPayments.length }}</b></button>
          </nav>
          <section class="profile-records">
            <div class="profile-records-heading">
              <div><h2>{{ orderCashflowSectionLabel(orderCashflowSection) }}</h2><button data-tooltip="Làm mới" @click="loadOrderDetail(orderDetail.document.name)"><CRMIcon name="refresh" /></button></div>
              <button v-if="orderCashflowSection === 'planned_payment'" class="crm-button primary" type="button" @click="openSOPlannedExpenseDialog">+ Thêm</button>
            </div>

            <template v-if="orderCashflowSection === 'actual_receipt'">
              <div v-if="orderActualReceipts.length" class="profile-table-wrap">
                <table class="profile-related-table">
                  <thead><tr><th>Số phiếu</th><th>Ngày ghi sổ</th><th>Số tiền</th><th>Hình thức</th><th>Tình trạng</th></tr></thead>
                  <tbody><tr v-for="row in orderActualReceipts" :key="row.name" @click="openRelated('Payment Entry', row)">
                    <td><a href="#" @click.prevent.stop="openRelated('Payment Entry', row)">{{ row.name }}</a></td>
                    <td>{{ formatValue(row.posting_date, 'date') }}</td>
                    <td>{{ formatValue(row.paid_amount, 'grand_total') }}</td>
                    <td>{{ row.mode_of_payment || '—' }}</td><td>{{ row.status || '—' }}</td>
                  </tr></tbody>
                </table>
              </div>
              <div v-else class="sales-empty"><span>Không có bản ghi nào</span></div>
            </template>
            <template v-else-if="orderCashflowSection === 'planned_payment'">
              <div v-if="soPlannedExpensesLoading" class="sales-empty"><span>Đang tải...</span></div>
              <div v-else-if="soPlannedExpenses.length" class="profile-table-wrap">
                <table class="profile-related-table">
                  <thead><tr><th>Nội dung chi</th><th>Tỷ lệ (%)</th><th>Số tiền</th><th>Ngày dự kiến chi</th><th>Đơn vị</th></tr></thead>
                  <tbody><tr v-for="row in soPlannedExpenses" :key="row.name">
                    <td>{{ row.description }}</td>
                    <td>{{ row.percentage || 0 }}%</td>
                    <td>{{ formatValue(row.amount, 'grand_total') }}</td>
                    <td>{{ row.planned_date ? formatValue(row.planned_date, 'date') : '—' }}</td>
                    <td>{{ row.department_name || '—' }}</td>
                  </tr></tbody>
                </table>
              </div>
              <div v-else class="sales-empty"><span>Không có bản ghi nào</span></div>
            </template>
            <template v-else-if="orderCashflowSection === 'actual_payment'">
              <div v-if="orderActualPayments.length" class="profile-table-wrap">
                <table class="profile-related-table">
                  <thead><tr><th>Số phiếu</th><th>Ngày ghi sổ</th><th>Số tiền</th><th>Hình thức</th><th>Tình trạng</th></tr></thead>
                  <tbody><tr v-for="row in orderActualPayments" :key="row.name" @click="openRelated('Payment Entry', row)">
                    <td><a href="#" @click.prevent.stop="openRelated('Payment Entry', row)">{{ row.name }}</a></td>
                    <td>{{ formatValue(row.posting_date, 'date') }}</td>
                    <td>{{ formatValue(row.paid_amount, 'grand_total') }}</td>
                    <td>{{ row.mode_of_payment || '—' }}</td><td>{{ row.status || '—' }}</td>
                  </tr></tbody>
                </table>
              </div>
              <div v-else class="sales-empty"><span>Không có bản ghi nào</span></div>
            </template>
          </section>
        </div>

        <template v-else-if="orderDetailTab === 'actual_delivery'">
          <div class="sod-related-grid sod-related-grid--compact"><section class="sod-related-card"><header><span class="sod-related-icon blue"><CRMIcon name="package" /></span><h3>Phiếu thực xuất / giao hàng</h3><b>{{ orderDetail.delivery_notes.length }}</b></header><div v-if="!orderDetail.delivery_notes.length" class="sod-related-empty">Chưa có phiếu thực xuất</div><button v-for="d in orderDetail.delivery_notes" :key="d.name" type="button" class="sod-related-row" @click="openRelated('Delivery Note', d)"><span><strong>{{ d.name }}</strong><small>{{ formatValue(d.posting_date, 'posting_date') }} · {{ d.status }}</small></span><strong>{{ formatValue(d.grand_total, 'grand_total') }}</strong></button></section></div>
        </template>

        <div v-else-if="orderDetailTab === 'support'" class="profile-tab-layout profile-group-layout">
          <nav class="profile-subnav">
            <button :class="{ active: orderSupportSection === 'warranty' }" @click="orderSupportSection = 'warranty'"><CRMIcon name="settings" />Phiếu bảo hành <b v-if="orderDetail.warranty_claims.length">{{ orderDetail.warranty_claims.length }}</b></button>
            <button :class="{ active: orderSupportSection === 'care_cards' }" @click="orderSupportSection = 'care_cards'"><CRMIcon name="care" />Thẻ chăm sóc <b v-if="orderDetail.care_cards.length">{{ orderDetail.care_cards.length }}</b></button>
            <button :class="{ active: orderSupportSection === 'consult_cards' }" @click="orderSupportSection = 'consult_cards'"><CRMIcon name="quotation" />Thẻ tư vấn</button>
          </nav>
          <section class="profile-records">
            <div class="profile-records-heading">
              <div><h2>{{ orderSupportSectionLabel(orderSupportSection) }}</h2><button data-tooltip="Làm mới" @click="loadOrderDetail(orderDetail.document.name)"><CRMIcon name="refresh" /></button></div>
              <button v-if="orderSupportSection === 'warranty'" @click="openSOWarrantyClaimDialog">+ Thêm</button>
              <button v-else-if="orderSupportSection === 'care_cards'" @click="createCareCardForOrder(orderDetail.document.name)">+ Thêm</button>
              <button v-else @click="notifyOrderConsultCardUnavailable">+ Thêm</button>
            </div>

            <template v-if="orderSupportSection === 'warranty'">
              <div v-if="orderDetail.warranty_claims.length" class="profile-table-wrap">
                <table class="profile-related-table">
                  <thead><tr><th>Số phiếu</th><th>Ngày</th><th>Nội dung khiếu nại</th><th>Tình trạng</th></tr></thead>
                  <tbody><tr v-for="row in orderDetail.warranty_claims" :key="row.name" @click="openRelated('Warranty Claim', row)">
                    <td><a href="#" @click.prevent.stop="openRelated('Warranty Claim', row)">{{ row.name }}</a></td>
                    <td>{{ formatValue(row.complaint_date, 'date') }}</td>
                    <td>{{ row.complaint }}</td>
                    <td>{{ row.status || '—' }}</td>
                  </tr></tbody>
                </table>
              </div>
              <div v-else class="sales-empty"><span>Không có bản ghi nào</span></div>
            </template>
            <template v-else-if="orderSupportSection === 'care_cards'">
              <div v-if="orderDetail.care_cards.length" class="profile-table-wrap">
                <table class="profile-related-table">
                  <thead><tr><th>Số thẻ</th><th>Hàng hóa</th><th>Tình trạng</th><th>Ngày chăm sóc</th><th>Mức độ hài lòng</th></tr></thead>
                  <tbody><tr v-for="row in orderDetail.care_cards" :key="row.name" @click="openCareCardFromOrder(row.name)">
                    <td><a href="#" @click.prevent.stop="openCareCardFromOrder(row.name)">{{ row.name }}</a></td>
                    <td>{{ row.item || '—' }}</td>
                    <td>{{ row.status || '—' }}</td>
                    <td>{{ row.care_date ? formatValue(row.care_date, 'date') : '—' }}</td>
                    <td>{{ row.satisfaction_level || '—' }}</td>
                  </tr></tbody>
                </table>
              </div>
              <div v-else class="sales-empty"><span>Không có bản ghi nào</span></div>
            </template>
            <template v-else-if="orderSupportSection === 'consult_cards'">
              <div class="sales-empty"><span>Không có bản ghi nào</span></div>
            </template>
          </section>
        </div>

        <div v-else-if="orderDetailTab === 'other'" class="profile-tab-layout profile-group-layout">
          <nav class="profile-subnav">
            <button :class="{ active: orderOtherSection === 'sales_returns' }" @click="orderOtherSection = 'sales_returns'"><CRMIcon name="customer" />Trả lại hàng bán <b v-if="orderDetail.sales_returns.length">{{ orderDetail.sales_returns.length }}</b></button>
            <button :class="{ active: orderOtherSection === 'revenue_recognition' }" @click="orderOtherSection = 'revenue_recognition'"><CRMIcon name="dollar" />Ghi nhận doanh số <b v-if="orderDetail.revenue_recognition_requests.length">{{ orderDetail.revenue_recognition_requests.length }}</b></button>
            <button :class="{ active: orderOtherSection === 'invoices' }" @click="orderOtherSection = 'invoices'"><CRMIcon name="document" />Hóa đơn <b v-if="orderDetail.invoices_count">{{ orderDetail.invoices_count }}</b></button>
            <button :class="{ active: orderOtherSection === 'esignature' }" @click="orderOtherSection = 'esignature'"><CRMIcon name="edit" />Lịch sử ký điện tử</button>
            <button :class="{ active: orderOtherSection === 'purchase_requests' }" @click="orderOtherSection = 'purchase_requests'"><CRMIcon name="cart" />Yêu cầu mua hàng <b v-if="orderDetail.purchase_requests.length">{{ orderDetail.purchase_requests.length }}</b></button>
          </nav>
          <section class="profile-records">
            <div class="profile-records-heading"><div><h2>{{ orderOtherSectionLabel(orderOtherSection) }}</h2><button title="Làm mới" @click="loadOrderDetail(orderDetail.document.name)"><CRMIcon name="refresh" /></button></div></div>

            <template v-if="orderOtherSection === 'sales_returns'">
              <div v-if="orderDetail.sales_returns.length" class="profile-table-wrap">
                <table class="profile-related-table">
                  <thead><tr><th>Số chứng từ</th><th>Trả cho hóa đơn</th><th>Giá trị trả lại</th><th>Tình trạng</th><th>Ngày ghi sổ</th></tr></thead>
                  <tbody><tr v-for="row in orderDetail.sales_returns" :key="row.name" @click="openRelated('Sales Invoice', row)">
                    <td><a href="#" @click.prevent.stop="openRelated('Sales Invoice', row)">{{ row.name }}</a></td>
                    <td>{{ row.return_against || '—' }}</td>
                    <td>{{ formatValue(Math.abs(row.grand_total || 0), 'grand_total') }}</td>
                    <td>{{ row.status || '—' }}</td>
                    <td>{{ formatValue(row.posting_date, 'date') }}</td>
                  </tr></tbody>
                </table>
              </div>
              <div v-else class="sales-empty"><span>Không có bản ghi nào</span></div>
            </template>
            <template v-else-if="orderOtherSection === 'revenue_recognition'">
              <div v-if="orderDetail.revenue_recognition_requests.length" class="profile-table-wrap">
                <table class="profile-related-table">
                  <thead><tr><th>Ngày</th><th>Doanh số ghi nhận</th><th>Hàng hóa</th><th>Nhân viên</th><th>Đơn vị</th><th>Tình trạng</th><th>Doanh số thực hiện được</th><th>Ghi chú</th></tr></thead>
                  <tbody><tr v-for="row in orderDetail.revenue_recognition_requests" :key="row.name">
                    <td>{{ formatValue(row.creation, 'creation') }}</td>
                    <td>{{ formatValue(row.custom_revenue_recognized_amount, 'grand_total') }}</td>
                    <td>{{ row.revenue_item_label || '—' }}</td>
                    <td>{{ row.owner || '—' }}</td>
                    <td>{{ row.revenue_department_label || '—' }}</td>
                    <td>{{ orderRevenueRequestStatusLabel(row.status) }}</td>
                    <td>{{ formatValue(row.custom_revenue_achieved_amount, 'grand_total') }}</td>
                    <td>{{ row.custom_revenue_note || '—' }}</td>
                  </tr></tbody>
                </table>
              </div>
              <div v-else class="sales-empty"><span>Không có bản ghi nào</span></div>
            </template>
            <template v-else-if="orderOtherSection === 'invoices'">
              <div v-if="orderDetail.invoices.length" class="profile-table-wrap">
                <table class="profile-related-table">
                  <thead><tr><th>Số hóa đơn</th><th>Ngày hóa đơn</th><th>Tổng tiền</th><th>Còn phải thu</th><th>Tình trạng</th></tr></thead>
                  <tbody><tr v-for="row in orderDetail.invoices" :key="row.name" @click="openRelated('Sales Invoice', row)">
                    <td><a href="#" @click.prevent.stop="openRelated('Sales Invoice', row)">{{ row.name }}</a></td>
                    <td>{{ formatValue(row.posting_date, 'date') }}</td>
                    <td>{{ formatValue(row.grand_total, 'grand_total') }}</td>
                    <td>{{ formatValue(row.outstanding_amount, 'grand_total') }}</td><td>{{ row.status || '—' }}</td>
                  </tr></tbody>
                </table>
              </div>
              <div v-else class="sales-empty"><span>Không có bản ghi nào</span></div>
            </template>
            <template v-else-if="orderOtherSection === 'esignature'">
              <div class="sales-empty"><span>Không có bản ghi nào</span></div>
            </template>
            <template v-else-if="orderOtherSection === 'purchase_requests'">
              <div v-if="orderDetail.purchase_requests.length" class="profile-table-wrap">
                <table class="profile-related-table">
                  <thead><tr><th>Số yêu cầu</th><th>Ngày yêu cầu</th><th>Loại</th><th>Tình trạng</th></tr></thead>
                  <tbody><tr v-for="row in orderDetail.purchase_requests" :key="row.name" @click="openRelated('Material Request', row)">
                    <td><a href="#" @click.prevent.stop="openRelated('Material Request', row)">{{ row.name }}</a></td>
                    <td>{{ formatValue(row.transaction_date, 'date') }}</td>
                    <td>{{ row.material_request_type || '—' }}</td><td>{{ row.status || '—' }}</td>
                  </tr></tbody>
                </table>
              </div>
              <div v-else class="sales-empty"><span>Không có bản ghi nào</span></div>
            </template>
          </section>
        </div>

        <div v-else-if="orderDetailTab === 'notes'" class="profile-tab-layout profile-group-layout">
          <nav class="profile-subnav">
            <button :class="{ active: orderNoteSection === 'notes' }" @click="orderNoteSection = 'notes'"><CRMIcon name="contact" />Ghi chú</button>
            <button :class="{ active: orderNoteSection === 'attachments' }" @click="orderNoteSection = 'attachments'"><CRMIcon name="package" />Tài liệu đính kèm <b v-if="orderDetail.attachments.length">{{ orderDetail.attachments.length }}</b></button>
          </nav>
          <section v-if="orderNoteSection === 'notes'" class="profile-records">
            <div class="profile-records-heading"><div><h2>Ghi chú</h2></div><button data-tooltip="Làm mới" @click="loadOrderDetail(orderDetail.document.name)"><CRMIcon name="refresh" /></button></div>
            <div class="customer-note-box">
              <textarea v-model="orderDetailComment" rows="3" placeholder="Nhập nội dung ghi chú..." @keydown.ctrl.enter.prevent="saveOrderDetailComment"></textarea>
              <div class="customer-note-actions">
                <span>Nhấn Ctrl + Enter để lưu nhanh</span>
                <button class="crm-button primary" type="button" :disabled="!orderDetailComment.trim()" @click="saveOrderDetailComment"><CRMIcon name="send" /> Lưu ghi chú</button>
              </div>
            </div>
            <div v-if="orderDetail.comments.length" class="profile-timeline-list">
              <article v-for="entry in orderDetail.comments" :key="entry.name">
                <strong>{{ entry.comment_by_fullname || entry.comment_by || 'CRM' }}</strong>
                <span>{{ formatValue(entry.creation, 'creation') }}</span>
                <p>{{ stripHtml(entry.content || '') }}</p>
              </article>
            </div>
            <p v-else class="profile-empty">Không có ghi chú nào.</p>
          </section>
          <section v-else class="profile-records">
            <div class="profile-records-heading">
              <div><h2>Tài liệu đính kèm</h2><button data-tooltip="Làm mới" @click="loadOrderDetail(orderDetail.document.name)"><CRMIcon name="refresh" /></button></div>
              <div><button @click="addSOAttachmentLink">Thêm liên kết</button><button :disabled="soAttachUploading" @click="$refs.soFileInput.click()">{{ soAttachUploading ? 'Đang tải...' : 'Thêm tệp' }}</button><input ref="soFileInput" type="file" style="display:none" @change="uploadSOFile"></div>
            </div>
            <div class="profile-table-wrap">
              <table class="profile-related-table"><thead><tr><th>Tên tài liệu</th><th>Người đính kèm</th><th>Ngày đính kèm</th><th>Dung lượng</th><th></th></tr></thead><tbody><tr v-for="file in orderDetail.attachments" :key="file.name"><td><a :href="file.file_url" target="_blank" rel="noopener">{{ file.file_name }}</a></td><td>{{ file.owner || '—' }}</td><td>{{ formatValue(file.creation, 'creation') }}</td><td>{{ file.file_size ? formatFileSize(file.file_size) : '—' }}</td><td><button class="profile-row-action" @click="deleteSOAttachment(file.name)">Xóa</button></td></tr></tbody></table>
              <p v-if="!orderDetail.attachments.length" class="profile-empty contacts-empty">Không có bản ghi nào</p>
            </div>
          </section>
        </div>

        <div v-else-if="orderDetailTab === 'activities'" class="profile-activity-panel">
          <div class="profile-activity-card">
            <header class="activity-table-heading">
              <div><h2>Hoạt động</h2><button data-tooltip="Làm mới" @click="loadOrderDetail(orderDetail.document.name)"><CRMIcon name="refresh" /></button></div>
              <div>
                <button @click="openOrderActivityDialog('task')"><CRMIcon name="task" /> Thêm Nhiệm vụ</button>
                <button @click="openOrderActivityDialog('meeting')"><CRMIcon name="calendar" /> Thêm Lịch hẹn</button>
                <button @click="openOrderActivityDialog('call')"><CRMIcon name="phone" /> Thêm Cuộc gọi</button>
              </div>
            </header>
            <div class="activity-table-scroll">
              <table class="activity-table">
                <thead><tr><th>Tên hoạt động</th><th>Loại hoạt động</th><th>Trạng thái</th><th>Người thực hiện</th><th>Ngày kết thúc</th></tr></thead>
                <tbody><tr v-for="a in visibleOrderActivities" :key="a.activity_doctype + '-' + a.name">
                  <td><button @click="openActivityRecord(a.name, a.activity_doctype, orderDetail.document.customer, orderDetail.document.customer_name)">{{ a.subject || a.description || a.name }}</button></td>
                  <td>{{ a.activity_doctype === 'Event' ? (a.event_category === 'Call' ? 'Cuộc gọi' : 'Lịch hẹn') : 'Nhiệm vụ' }}</td>
                  <td><span class="activity-status" :class="'status-' + String(a.status || '').toLowerCase()">{{ orderActivityStatusLabel(a.status) }}</span></td>
                  <td>{{ a.assigned_by_full_name || a.owner || '—' }}</td>
                  <td>{{ formatValue(a.date || a.ends_on, 'date') }}</td>
                </tr></tbody>
              </table>
              <p v-if="!orderDetail.activities.length" class="profile-empty activity-empty-row">Không có bản ghi nào</p>
            </div>
            <footer class="activity-pagination">
              <strong>Tổng số {{ orderDetail.activities.length.toLocaleString('vi-VN') }}</strong>
              <div><label>Số dòng/trang</label>
                <select v-model.number="orderActivityPageLength"><option :value="10">10</option><option :value="20">20</option><option :value="50">50</option></select>
                <span>{{ orderActivityPageStart }} - {{ orderActivityPageEnd }}</span>
                <button :disabled="orderActivityPage <= 1" @click="changeOrderActivityPage(1)">|‹</button>
                <button :disabled="orderActivityPage <= 1" @click="changeOrderActivityPage(orderActivityPage - 1)">‹</button>
                <button :disabled="orderActivityPage >= orderActivityPageCount" @click="changeOrderActivityPage(orderActivityPage + 1)">›</button>
                <button :disabled="orderActivityPage >= orderActivityPageCount" @click="changeOrderActivityPage(orderActivityPageCount)">›|</button>
              </div>
            </footer>
          </div>
        </div>

        <template v-else-if="orderDetailTab === 'chat'">
          <div class="customer-conversation-shell">
            <header class="customer-conversation-heading">
              <div><h2>Trao đổi</h2><p>Theo dõi và cập nhật nội dung trao đổi về đơn hàng này.</p></div>
              <span>{{ orderDetail.comments.length }} bình luận</span>
            </header>
            <div v-if="orderDetail.comments.length" class="customer-comment-feed">
              <article v-for="c in orderDetail.comments" :key="c.name" class="customer-comment">
                <span class="customer-comment-avatar" aria-hidden="true">{{ (c.comment_by_fullname || c.comment_by || 'CRM').slice(0, 1).toUpperCase() }}</span>
                <div class="customer-comment-content">
                  <div class="customer-comment-meta"><strong>{{ c.comment_by_fullname || c.comment_by }}</strong><time>{{ formatValue(c.creation, 'creation') }}</time></div>
                  <div class="customer-comment-bubble"><p>{{ stripHtml(c.content || '') }}</p></div>
                </div>
              </article>
            </div>
            <div v-else class="customer-conversation-empty"><CRMIcon name="message" /><strong>Chưa có nội dung trao đổi</strong><span>Hãy bắt đầu bằng bình luận đầu tiên về đơn hàng này.</span></div>
            <div class="customer-comment-composer">
              <span class="customer-comment-avatar current" aria-hidden="true">{{ (boot?.full_name || boot?.user || 'CRM').slice(0, 1).toUpperCase() }}</span>
              <div class="customer-comment-editor">
                <textarea v-model="orderDetailComment" rows="3" aria-label="Nội dung trao đổi" placeholder="Viết bình luận..." @keydown.ctrl.enter.prevent="saveOrderDetailComment"></textarea>
                <div class="customer-comment-actions">
                  <button type="button" data-tooltip="Mở tài liệu đính kèm" @click="orderDetailTab = 'notes'"><CRMIcon name="package" /> Đính kèm</button>
                  <span>Ctrl + Enter để gửi</span>
                  <button type="button" class="crm-button primary" :disabled="!orderDetailComment.trim()" @click="saveOrderDetailComment"><CRMIcon name="send" /> Gửi</button>
                </div>
              </div>
            </div>
          </div>
        </template>

      </div>
    </div>
  </div>

      <teleport to="body"><div v-if="soPrintDialogOpen" class="crm-modal-backdrop" @click.self="closeSalesOrderPrintDialog">
        <div class="crm-modal sod-print-modal" role="dialog" aria-modal="true" :aria-label="'In đơn hàng ' + orderDetailName">
          <header>
            <div>
              <h2>In đơn hàng — {{ orderDetailName }}</h2>
              <p>Chọn mẫu để xem trước, tải Word hoặc in đơn hàng.</p>
            </div>
            <button type="button" @click="closeSalesOrderPrintDialog" aria-label="Đóng">×</button>
          </header>
          <div class="sod-print-toolbar">
            <strong>Mẫu hợp đồng</strong>
            <button type="button" class="crm-button primary" @click="openSalesOrderTemplateBuilder">＋ Tạo mẫu mới</button>
          </div>
          <div class="sod-print-list">
            <div v-if="soPrintTemplatesLoading" class="sod-print-empty">Đang tải danh sách mẫu...</div>
            <div v-else-if="!soPrintTemplates.length" class="sod-print-empty">
              Chưa có mẫu nào. Nhấn “Tạo mẫu mới” để bắt đầu.
            </div>
            <article v-for="template in soPrintTemplates" :key="template.name" class="sod-print-row">
              <div class="sod-print-info">
                <div class="sod-print-name">
                  {{ template.template_name || template.name }}
                  <span class="sod-print-status" :class="'is-' + String(template.status || 'Draft').toLowerCase()">
                    {{ template.status === 'Approved' ? 'Đã duyệt' : template.status === 'Pending' ? 'Chờ duyệt' : template.status === 'Archived' ? 'Lưu trữ' : 'Nháp' }}
                  </span>
                </div>
                <div class="sod-print-meta">
                  <span v-if="template.template_category">{{ template.template_category }}</span>
                  <span v-if="template.service_type">· {{ template.service_type }}</span>
                  <span v-if="template.template_file">· DOCX</span>
                </div>
              </div>
              <div class="sod-print-actions">
                <button type="button" class="crm-button" :disabled="soPrintActionTemplate === template.name" @click="previewSalesOrderTemplate(template)">
                  <CRMIcon name="eye" /> Xem trước
                </button>
                <button type="button" class="crm-button primary" :disabled="soPrintActionTemplate === template.name" @click="printSalesOrderTemplate(template)">
                  <CRMIcon name="print" /> In
                </button>
                <button v-if="template.can_delete" type="button" class="crm-button sod-print-delete" :disabled="soPrintActionTemplate === template.name" data-tooltip="Xóa mẫu" aria-label="Xóa mẫu" @click="deleteSalesOrderPrintTemplate(template)">
                  <CRMIcon name="trash" />
                </button>
              </div>
            </article>
          </div>
        </div>
      </div></teleport>

      <teleport to="body"><div v-if="soPrintPreviewOpen" class="crm-modal-backdrop sod-print-preview-backdrop" @click.self="closeSalesOrderPrintPreview">
        <div class="crm-modal sod-print-preview-modal" role="dialog" aria-modal="true" :aria-label="'Xem trước ' + soPrintPreviewTitle">
          <header>
            <div>
              <h2>Xem trước: {{ soPrintPreviewTitle }}</h2>
              <p>Đơn hàng {{ orderDetailName }}</p>
            </div>
            <button type="button" @click="closeSalesOrderPrintPreview" aria-label="Đóng">×</button>
          </header>
          <div class="sod-print-preview-stage">
            <iframe
              class="sod-print-paper"
              :srcdoc="soPrintPreviewHtml"
              :data-tooltip="'Xem trước ' + soPrintPreviewTitle"
              sandbox
            ></iframe>
          </div>
          <footer>
            <button type="button" class="crm-button" @click="closeSalesOrderPrintPreview">Đóng</button>
            <button type="button" class="crm-button primary" @click="printSalesOrderPreview">In</button>
          </footer>
        </div>
      </div></teleport>

      <teleport to="body"><div v-if="soStockLookupOpen" class="crm-modal-backdrop" @click.self="closeSOStockLookup">
        <div class="crm-modal stock-lookup-modal">
          <header>
            <h2>Tra cứu số lượng tồn</h2>
            <button type="button" @click="closeSOStockLookup" aria-label="Đóng">×</button>
          </header>
          <div class="stock-lookup-body">
            <div v-if="soStockLookupLoading" class="stock-lookup-loading">Đang tải số lượng tồn...</div>
            <table v-else class="goods-table stock-lookup-table">
              <colgroup>
                <col style="width:160px"><col style="width:1fr"><col style="width:110px">
                <col style="width:160px"><col style="width:110px"><col style="width:110px"><col style="width:120px">
              </colgroup>
              <thead>
                <tr>
                  <th>Mã hàng hóa</th>
                  <th>Diễn giải</th>
                  <th class="gt-center">Đơn vị tính</th>
                  <th>Kho</th>
                  <th class="gt-right">Số lượng</th>
                  <th class="gt-right">SL đã giao</th>
                  <th class="gt-right">Số lượng tồn</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="!soStockLookupItems.length">
                  <td colspan="7" class="gt-empty">Không có dữ liệu hàng hóa.</td>
                </tr>
                <template v-for="row in soStockLookupItems" :key="row.item_code">
                  <tr v-if="!row.warehouses.length">
                    <td class="gt-code">{{ row.item_code }}</td>
                    <td>{{ row.item_name }}</td>
                    <td class="gt-center">{{ row.uom || '—' }}</td>
                    <td class="gt-muted">-</td>
                    <td class="gt-right">{{ formatValue(row.qty, 'grand_total') }}</td>
                    <td class="gt-right">{{ formatValue(row.delivered_qty, 'grand_total') }}</td>
                    <td class="gt-right">{{ formatValue(row.balance_qty, 'grand_total') }}</td>
                  </tr>
                  <tr v-for="(wh, wi) in row.warehouses" :key="row.item_code + '::' + wh.warehouse">
                    <td class="gt-code">{{ wi === 0 ? row.item_code : '' }}</td>
                    <td>{{ wi === 0 ? row.item_name : '' }}</td>
                    <td class="gt-center">{{ wi === 0 ? (row.uom || '—') : '' }}</td>
                    <td>{{ wh.warehouse }}</td>
                    <td class="gt-right">{{ wi === 0 ? formatValue(row.qty, 'grand_total') : '' }}</td>
                    <td class="gt-right">{{ wi === 0 ? formatValue(row.delivered_qty, 'grand_total') : '' }}</td>
                    <td class="gt-right">{{ formatValue(wh.actual_qty, 'grand_total') }}</td>
                  </tr>
                </template>
              </tbody>
            </table>
          </div>
          <footer class="stock-lookup-footer">
            <span class="stock-lookup-total">Tổng số <b>{{ soStockLookupItems.length }}</b></span>
            <button type="button" class="crm-button primary" @click="closeSOStockLookup">Đóng</button>
          </footer>
        </div>
      </div></teleport>

      <teleport to="body"><div v-if="soGoodsEditorOpen" class="crm-modal-backdrop" @click.self="closeSOGoodsEditor">
        <div class="crm-modal goods-editor-modal">
          <header>
            <h2>Chọn Hàng hóa<span v-if="soGoodsEditorItems.length" class="picker-selected-badge">{{ soGoodsEditorItems.length }}</span></h2>
            <button type="button" @click="closeSOGoodsEditor" aria-label="Đóng">×</button>
          </header>
          <div class="goods-editor-toolbar">
            <span class="goods-editor-total">Cộng đơn hàng: <strong>{{ formatValue(soGoodsEditorTotalAmount(), 'grand_total') }}</strong></span>
            <button type="button" class="goods-editor-clear" v-if="soGoodsEditorItems.length > 1" @click="clearSOGoodsEditorItems">🗑 Xóa tất cả</button>
          </div>
          <div class="goods-editor-tablewrap">
            <table class="opportunity-items-table so-items-table goods-editor-table">
              <thead>
                <tr>
                  <th>STT</th>
                  <th>Mã hàng hóa</th>
                  <th>Tên hàng hóa</th>
                  <th>Mô tả</th>
                  <th>Đơn vị tính</th>
                  <th>Số lượng</th>
                  <th>Đơn giá</th>
                  <th>Tỷ lệ CK (%)</th>
                  <th>Đơn giá sau CK</th>
                  <th>Thành tiền</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in soGoodsEditorItems" :key="index">
                  <td class="item-stt-cell">
                    <span class="item-stt-num">{{ index + 1 }}</span>
                    <button type="button" class="item-row-del" @click="removeSOGoodsEditorItem(index)">×</button>
                  </td>
                  <td><input list="so-goods-editor-options" v-model="item.item_code" @change="autoFillSOGoodsEditorItem(item)" placeholder="Mã hàng"></td>
                  <td><input v-model="item.item_name" placeholder="Tên hàng hóa / dịch vụ"></td>
                  <td><input v-model="item.description" placeholder="Mô tả..."></td>
                  <td><input v-model="item.uom" placeholder="Cái"></td>
                  <td><input type="number" min="0" step="any" v-model.number="item.qty" @input="soGoodsEditorRowAmount(item)"></td>
                  <td><input type="number" min="0" step="any" v-model.number="item.price_list_rate" @input="soGoodsEditorRowAmount(item)" placeholder="0"></td>
                  <td><input type="number" min="0" max="100" step="any" v-model.number="item.discount_percentage" @input="soGoodsEditorRowAmount(item)" placeholder="0"></td>
                  <td><input type="number" min="0" step="any" v-model.number="item.rate" @input="item.amount = Math.round((parseFloat(item.qty)||0)*(parseFloat(item.rate)||0))" placeholder="0"></td>
                  <td class="item-calc-cell">{{ formatValue(item.amount, 'grand_total') }}</td>
                </tr>
                <tr v-if="!soGoodsEditorItems.length" class="picker-empty-row">
                  <td colspan="10">Chưa có hàng hóa. Bấm "Chọn hàng hóa" hoặc "Thêm dòng".</td>
                </tr>
                <tr class="items-total-row" v-if="soGoodsEditorItems.length">
                  <td></td>
                  <td colspan="4" style="text-align:left;padding-left:8px">Tổng cộng</td>
                  <td>{{ soGoodsEditorTotalQty() }}</td>
                  <td></td>
                  <td></td>
                  <td></td>
                  <td>{{ formatValue(soGoodsEditorTotalAmount(), 'grand_total') }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <datalist id="so-goods-editor-options">
            <option v-for="opt in soItemList" :key="opt.name" :value="opt.name">{{ opt.item_name }}</option>
          </datalist>
          <div class="goods-editor-actions">
            <button type="button" class="crm-button primary" @click="openSOItemPicker('goods-editor')">＋ Chọn hàng hóa</button>
            <button type="button" class="crm-button" @click="addSOGoodsEditorItem">＋ Thêm dòng</button>
          </div>
          <footer>
            <button type="button" class="crm-button" :disabled="soGoodsEditorSaving" @click="closeSOGoodsEditor">Hủy</button>
            <button type="button" class="crm-button primary" :disabled="soGoodsEditorSaving" @click="saveSOGoodsEditor">{{ soGoodsEditorSaving ? 'Đang lưu...' : 'Lưu' }}</button>
          </footer>
        </div>
      </div></teleport>

      <teleport to="body"><div v-if="soItemPickerOpen" class="crm-modal-backdrop" @click.self="closeSOItemPicker">
        <div class="crm-modal item-picker-modal">
          <header>
            <h2>Chọn hàng hóa<span v-if="soItemPickerSelected.length" class="picker-selected-badge">{{ soItemPickerSelected.length }} đã chọn</span></h2>
            <button type="button" @click="closeSOItemPicker" aria-label="Đóng">×</button>
          </header>
          <div class="item-picker-toolbar">
            <div class="item-picker-search-wrap">
              <input v-model="soItemPickerSearch" @input="soItemPickerPage = 1" placeholder="Tìm theo mã hoặc tên hàng hóa..." class="item-picker-search" autofocus>
            </div>
            <select v-model="soItemPickerCategoryFilter" @change="soItemPickerPage = 1" class="item-picker-cat">
              <option value="">Tất cả loại hàng hóa</option>
              <option v-for="cat in soItemPickerCategories" :key="cat" :value="cat">{{ cat }}</option>
            </select>
          </div>
          <div class="item-picker-table-wrap">
            <table class="item-picker-table">
              <colgroup><col><col><col><col><col></colgroup>
              <thead>
                <tr>
                  <th class="picker-check-col">
                    <input type="checkbox"
                      :checked="soItemPickerRows.length > 0 && soItemPickerRows.every(r => soItemPickerSelected.includes(r.name))"
                      :indeterminate="soItemPickerRows.some(r => soItemPickerSelected.includes(r.name)) && !soItemPickerRows.every(r => soItemPickerSelected.includes(r.name))"
                      @change="e => { if(e.target.checked) soItemPickerRows.forEach(r => { if(!soItemPickerSelected.includes(r.name)) soItemPickerSelected.push(r.name) }); else soItemPickerSelected = soItemPickerSelected.filter(n => !soItemPickerRows.find(r => r.name === n)) }">
                  </th>
                  <th>Mã hàng hóa</th>
                  <th>Tên hàng hóa</th>
                  <th>Loại hàng hóa</th>
                  <th>Đơn vị tính</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in soItemPickerRows" :key="item.name"
                  @click="toggleSOItemPickerRow(item.name)"
                  :class="{ selected: soItemPickerSelected.includes(item.name) }">
                  <td class="picker-check-col"><input type="checkbox" :checked="soItemPickerSelected.includes(item.name)" @click.stop="toggleSOItemPickerRow(item.name)"></td>
                  <td><span class="picker-code">{{ item.name }}</span></td>
                  <td>{{ item.item_name }}</td>
                  <td><span class="picker-tag" v-if="item.item_group && item.item_group !== 'All Item Groups'">{{ item.item_group }}</span><span v-else class="picker-tag-muted">—</span></td>
                  <td>{{ item.stock_uom || '—' }}</td>
                </tr>
                <tr v-if="!soItemPickerRows.length" class="picker-empty-row">
                  <td colspan="5">Không tìm thấy hàng hóa nào phù hợp</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="item-picker-footer">
            <span>Tổng <strong>{{ soItemPickerFiltered.length }}</strong> hàng hóa</span>
            <div class="item-picker-pagination">
              <span>Dòng/trang</span>
              <select v-model.number="soItemPickerPageLength" @change="soItemPickerPage = 1">
                <option :value="10">10</option><option :value="20">20</option><option :value="50">50</option>
              </select>
              <span>{{ (soItemPickerPage-1)*soItemPickerPageLength+1 }}–{{ Math.min(soItemPickerPage*soItemPickerPageLength, soItemPickerFiltered.length) }}</span>
              <button type="button" :disabled="soItemPickerPage <= 1" @click="soItemPickerPage = 1" data-tooltip="Trang đầu">«</button>
              <button type="button" :disabled="soItemPickerPage <= 1" @click="soItemPickerPage--" data-tooltip="Trang trước">‹</button>
              <button type="button" :disabled="soItemPickerPage >= soItemPickerPageCount" @click="soItemPickerPage++" data-tooltip="Trang sau">›</button>
              <button type="button" :disabled="soItemPickerPage >= soItemPickerPageCount" @click="soItemPickerPage = soItemPickerPageCount" data-tooltip="Trang cuối">»</button>
            </div>
          </div>
          <footer>
            <button type="button" class="crm-button" @click="closeSOItemPicker">Hủy</button>
            <button type="button" class="crm-button primary" :disabled="!soItemPickerSelected.length" @click="confirmSOItemPicker">
              {{ soItemPickerSelected.length ? 'Thêm ' + soItemPickerSelected.length + ' hàng hóa' : 'Chọn hàng hóa' }}
            </button>
          </footer>
        </div>
      </div></teleport>

      <teleport to="body"><div v-if="soPlannedExpenseDialogOpen" class="column-dialog-backdrop customer-summary-dialog-backdrop" @click.self="closeSOPlannedExpenseDialog">
        <section class="so-pe-dialog" role="dialog" aria-modal="true">
          <header>
            <h2>Thêm dự kiến chi</h2>
            <button data-tooltip="Đóng" aria-label="Đóng" @click="closeSOPlannedExpenseDialog">×</button>
          </header>
          <div class="so-pe-body">
            <label class="so-pe-field">
              <span>Nội dung chi <b>*</b></span>
              <input v-model="soPlannedExpenseForm.description" type="text" placeholder="Nhập nội dung chi">
            </label>
            <label class="so-pe-field">
              <span>Tỷ lệ (%)</span>
              <input v-model.number="soPlannedExpenseForm.percentage" type="number" min="0" max="100">
            </label>
            <label class="so-pe-field">
              <span>Số tiền</span>
              <input v-model.number="soPlannedExpenseForm.amount" type="number" min="0">
            </label>
            <label class="so-pe-field">
              <span>Ngày dự kiến chi</span>
              <input v-model="soPlannedExpenseForm.planned_date" type="date">
            </label>
            <label class="so-pe-field">
              <span>Đơn vị</span>
              <button type="button" class="so-pe-org-trigger" @click="openSOOrgPicker">
                <span>{{ soPlannedExpenseForm.department_label || '- Chọn đơn vị -' }}</span>
                <CRMIcon name="all" />
              </button>
            </label>
          </div>
          <footer>
            <button type="button" class="crm-button" @click="closeSOPlannedExpenseDialog">Hủy</button>
            <button type="button" class="crm-button primary" :disabled="soPlannedExpenseSaving || !soPlannedExpenseForm.description.trim()" @click="saveSOPlannedExpense">
              {{ soPlannedExpenseSaving ? 'Đang lưu...' : 'Lưu' }}
            </button>
          </footer>

          <div v-if="soOrgPickerOpen" class="so-pe-org-overlay" @click.self="closeSOOrgPicker">
            <section class="so-pe-org-picker">
              <header>
                <h3>Chọn cơ cấu tổ chức</h3>
                <button data-tooltip="Đóng" aria-label="Đóng" @click="closeSOOrgPicker">×</button>
              </header>
              <div class="so-pe-org-tree">
                <OrgUnitNode
                  v-for="node in soOrgTree"
                  :key="node.value"
                  :node="node"
                  :selected-value="soPlannedExpenseForm.department"
                  @toggle="toggleOrgNode"
                  @select="selectSOOrgNode"
                />
                <p v-if="!soOrgTree.length" class="org-node-empty">Đang tải...</p>
              </div>
            </section>
          </div>
        </section>
      </div></teleport>

      <teleport to="body"><div v-if="soContactDialogOpen" class="crm-modal-backdrop" @click.self="closeSOContactDialog">
        <form class="crm-modal contact-modal" @submit.prevent="saveSOContact">
          <header><div><h2>Thêm nhanh liên hệ</h2><p>Liên kết trực tiếp với {{ orderDetail.document.customer_name }}</p></div><button type="button" @click="closeSOContactDialog">×</button></header>
          <div class="contact-modal-grid">
            <label><span>Tên <b>*</b></span><input v-model="soContactForm.first_name" required autofocus></label>
            <label><span>Họ</span><input v-model="soContactForm.last_name"></label>
            <label><span>Email cá nhân</span><input v-model="soContactForm.email_id" type="email"></label>
            <label><span>ĐT di động</span><input v-model="soContactForm.mobile_no"></label>
            <label><span>ĐT cơ quan</span><input v-model="soContactForm.phone"></label>
            <label><span>Chức danh</span><input v-model="soContactForm.designation"></label>
            <label class="contact-primary-check">
              <input v-model.number="soContactForm.is_primary_contact" :true-value="1" :false-value="0" type="checkbox">
              <span class="contact-primary-box" aria-hidden="true"></span>
              <span class="contact-primary-copy"><strong>Đặt làm liên hệ chính</strong><small>Liên hệ này sẽ được ưu tiên khi giao dịch với khách hàng.</small></span>
            </label>
          </div>
          <footer><button class="crm-button" type="button" :disabled="soContactSaving" @click="closeSOContactDialog">Hủy</button><button class="crm-button primary" type="submit" :disabled="soContactSaving || !soContactForm.first_name?.trim()">{{ soContactSaving ? 'Đang lưu...' : 'Lưu liên hệ' }}</button></footer>
        </form>
      </div></teleport>

      <teleport to="body"><div v-if="soContactPickerOpen" class="crm-modal-backdrop" @click.self="soContactPickerOpen = false">
        <section class="crm-modal contact-picker-modal">
          <header><div><h2>Chọn liên hệ</h2><p>Chọn Contact đã tồn tại để liên kết với {{ orderDetail.document.customer_name }}</p></div><button type="button" @click="soContactPickerOpen = false">×</button></header>
          <div class="contact-picker-search"><CRMIcon name="search" /><input v-model="soContactPickerSearch" placeholder="Tìm theo tên, email hoặc điện thoại" @keyup.enter="searchSOContacts"><button @click="searchSOContacts">Tìm kiếm</button></div>
          <div class="contact-picker-list">
            <button v-for="contact in soContactPickerRows" :key="contact.name" :disabled="soContactSaving" @click="linkSOContact(contact)">
              <span class="contact-avatar">{{ (contact.full_name || contact.name).slice(0, 1) }}</span>
              <span><strong>{{ contact.full_name || contact.name }}</strong><small>{{ contact.email_id || contact.mobile_no || contact.phone || 'Chưa có thông tin liên lạc' }}</small></span>
              <b>Chọn</b>
            </button>
            <p v-if="soContactPickerLoading" class="crm-empty">Đang tìm...</p>
            <p v-else-if="!soContactPickerRows.length" class="crm-empty">Không có liên hệ chưa liên kết phù hợp.</p>
          </div>
        </section>
      </div></teleport>

      <teleport to="body"><div v-if="orderActivityDialogOpen" class="crm-modal-backdrop" @click.self="orderActivityDialogOpen = false">
        <form class="crm-modal activity-modal" @submit.prevent="saveOrderActivity">
          <header><div><h2>{{ orderActivityForm.name ? 'Sửa ' : 'Thêm ' }}{{ orderActivityTypeLabel(orderActivityForm.activity_type).toLowerCase() }}</h2><p>Hoạt động của đơn hàng {{ orderDetail.document.name }}</p></div><button type="button" @click="orderActivityDialogOpen = false">×</button></header>
          <div class="activity-modal-grid">
            <label class="wide"><span>Tên hoạt động <b>*</b></span><input v-model="orderActivityForm.subject" required autofocus></label>
            <template v-if="orderActivityForm.activity_type === 'task'">
              <label><span>Hạn hoàn thành</span><input v-model="orderActivityForm.due_date" type="date"></label>
              <label><span>Người thực hiện</span><select v-model="orderActivityForm.allocated_to"><option v-for="user in orderDetail.activity_users" :key="user.name" :value="user.name">{{ user.full_name || user.name }}</option></select></label>
              <label><span>Trạng thái</span><select v-model="orderActivityForm.status"><option value="Open">Đang thực hiện</option><option value="Closed">Đã hoàn thành</option><option value="Cancelled">Đã hủy</option></select></label>
              <label><span>Ưu tiên</span><select v-model="orderActivityForm.priority"><option value="High">Cao</option><option value="Medium">Trung bình</option><option value="Low">Thấp</option></select></label>
            </template>
            <template v-else>
              <label><span>Bắt đầu</span><input v-model="orderActivityForm.starts_on" type="datetime-local" required></label>
              <label><span>Kết thúc</span><input v-model="orderActivityForm.ends_on" type="datetime-local"></label>
              <label><span>Trạng thái</span><select v-model="orderActivityForm.status"><option value="Open">Đang thực hiện</option><option value="Completed">Đã hoàn thành</option><option value="Closed">Đã đóng</option><option value="Cancelled">Đã hủy</option></select></label>
              <label><span>Người thực hiện</span><select v-model="orderActivityForm.allocated_to"><option v-for="user in orderDetail.activity_users" :key="user.name" :value="user.name">{{ user.full_name || user.name }}</option></select></label>
            </template>
            <label class="wide"><span>Mô tả</span><textarea v-model="orderActivityForm.description"></textarea></label>
          </div>
          <footer><button class="crm-button" type="button" :disabled="orderActivitySaving" @click="orderActivityDialogOpen = false">Hủy</button><button class="crm-button primary" type="submit" :disabled="orderActivitySaving || !orderActivityForm.subject?.trim()">{{ orderActivitySaving ? 'Đang lưu...' : 'Lưu hoạt động' }}</button></footer>
        </form>
      </div></teleport>
</main>

        <main v-else-if="route === 'orders'" class="orders-list-layout so-list-page">

          <!-- Row 1: Title + add button (full width, above the 3-column split) -->
          <div class="orders-toolbar-r1">
            <div class="otr1-left">
              <h1>Tất cả đơn hàng</h1>
              <span class="orders-total-badge">{{ total }}</span>
              <span v-if="soSavedFilterActive" class="otr1-filter-active">● {{ SO_SAVED_FILTERS.find(f=>f.key===soSavedFilterActive)?.label }}</span>
            </div>
            <div class="otr1-right">
              <button class="crm-button" @click="exportResource('orders', { search })">⇤ Xuất Excel</button>
              <button v-if="boot?.resources?.[route]?.can_create" class="crm-button primary otr1-add-btn" @click="createDocument()">+ Thêm</button>
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
                <button class="crm-btn-icon" :class="{active: soItemsPanelVisible}" @click="soItemsPanelVisible = !soItemsPanelVisible" data-tooltip="Ẩn/hiện Hàng hóa"><CRMIcon name="package" /></button>
                <button class="crm-btn-icon" :class="{active: soFilterOpen}" @click="soFilterOpen = !soFilterOpen" data-tooltip="Bộ lọc">
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
                    <th class="ot-col-status">Tình trạng ghi DT</th>
                    <th class="ot-col-no">Số đơn hàng/HĐ</th>
                    <th class="ot-col-title">Diễn giải</th>
                    <th class="ot-col-amount">Giá trị đơn hàng</th>
                    <th class="ot-col-date">Ngày đặt hàng</th>
                    <th class="ot-col-date">Ngày ghi số</th>
                    <th class="ot-col-owner">Người thực hiện</th>
                    <th class="ot-col-co">Đơn vị</th>
                    <th class="ot-col-delivery">Tình trạng giao</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="loading"><td colspan="10" class="ot-loading">Đang tải...</td></tr>
                  <tr v-else-if="!rows.length"><td colspan="10" class="ot-loading">Chưa có dữ liệu phù hợp.</td></tr>
                  <tr v-else v-for="row in rows" :key="row.name"
                    :class="{ 'ot-selected': selected?.name === row.name }"
                    @click="selectRow(row); loadSODetail(row.name)"
                    @dblclick="openDocument(row)">
                    <td class="ot-chk-col" @click.stop><input type="checkbox"></td>
                    <td>
                      <span :class="'ot-rev ot-rev--' + soRevenueStatusClass(row.display_revenue_status)">
                        {{ row.display_revenue_status || 'Đơn nháp' }}
                      </span>
                    </td>
                    <td><a class="ot-link" @click.stop="openDocument(row)">{{ row.name }}</a></td>
                    <td class="ot-title-cell" :data-tooltip="row.title">{{ row.title || '—' }}</td>
                    <td class="ot-amount-cell">{{ formatValue(row.grand_total, 'grand_total') }}</td>
                    <td>{{ formatValue(row.transaction_date, 'transaction_date') }}</td>
                    <td>{{ row.custom_revenue_recognition_date ? formatValue(row.custom_revenue_recognition_date, 'transaction_date') : '—' }}</td>
                    <td><span class="ot-owner">{{ row.owner || '—' }}</span></td>
                    <td class="ot-co-cell" :data-tooltip="row.company">{{ row.company || '—' }}</td>
                    <td>
                      <span v-if="row.delivery_status" :class="'ot-tag ot-tag--' + soDeliveryStatusClass(row.delivery_status)">{{ row.delivery_status }}</span>
                      <span v-else>—</span>
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
                <span>Giá trị đơn hàng: <strong>{{ formatValue(rows.reduce((s,r) => s+(r.grand_total||0), 0), 'grand_total') }}</strong></span>
                <span class="of-agg-div">|</span>
                <span>Thực thu: <strong>0</strong></span>
                <span class="of-agg-div">|</span>
                <span>Còn phải thu: <strong>0</strong></span>
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

          <!-- ── Items detail panel ─────────────────────────── -->
          <aside v-if="selected && soItemsPanelVisible" class="orders-detail-panel">
            <div class="odp-header">
              <div class="odp-header-title">
                <span>Hàng hóa</span>
                <span class="odp-count">{{ soDetailItems.length }}</span>
              </div>
              <div class="odp-header-actions">
                <button class="crm-btn-icon" @click="loadSODetail(selected.name)" data-tooltip="Làm mới">
                  <svg viewBox="0 0 16 16" fill="none" width="12" height="12"><path d="M2.5 8a5.5 5.5 0 1 1 1.1 3.3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M2.5 11.5V8H6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </button>
                <button class="crm-btn-icon" @click="openDocument()" data-tooltip="Mở form">
                  <svg viewBox="0 0 16 16" fill="none" width="12" height="12"><path d="M6 2H3a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1v-3M9 2h5v5M14 2l-7 7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </button>
              </div>
            </div>

            <div class="odp-so-meta">
              <div class="odp-so-name">{{ selected.name }}</div>
              <div class="odp-so-customer">{{ selected.customer_name || selected.customer }}</div>
            </div>

            <div class="odp-items-list">
              <div v-if="soDetailLoading" class="odp-empty">Đang tải...</div>
              <template v-else-if="soDetailItems.length">
                <div v-for="(item, idx) in soDetailItems" :key="item.item_code + idx" class="odp-item" :class="{ 'odp-item--open': soExpandedItem === idx }">
                  <div class="odp-item-main" @click="toggleSODetailItem(idx)">
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
                  <div v-if="soExpandedItem === idx" class="odp-item-detail">
                    <div class="odp-item-detail-grid">
                      <div class="odp-item-detail-cell">
                        <div class="odp-item-detail-label">Đơn giá sau CK</div>
                        <div class="odp-masked">{{ formatValue(item.net_rate, 'grand_total') }}</div>
                      </div>
                      <div class="odp-item-detail-cell">
                        <div class="odp-item-detail-label">Thành tiền sau CK</div>
                        <div class="odp-masked odp-masked--total">{{ formatValue(item.net_amount, 'grand_total') }}</div>
                      </div>
                    </div>
                    <div v-if="item.description" class="odp-item-detail-row">
                      <div class="odp-item-detail-label">Mô tả</div>
                      <div class="odp-item-detail-value">{{ item.description }}</div>
                    </div>
                    <div v-if="item.custom_a_end" class="odp-item-detail-row">
                      <div class="odp-item-detail-label">Điểm lắp đặt A-End</div>
                      <div class="odp-item-detail-value">{{ item.custom_a_end }}</div>
                    </div>
                    <div v-if="item.custom_z_end" class="odp-item-detail-row">
                      <div class="odp-item-detail-label">Điểm lắp đặt Z-End</div>
                      <div class="odp-item-detail-value">{{ item.custom_z_end }}</div>
                    </div>
                  </div>
                </div>
              </template>
              <div v-else class="odp-empty">Chưa có hàng hóa</div>
            </div>

            <div class="odp-footer">
              <div class="odp-footer-row">
                <span>Số lượng: <strong>{{ soDetailItems.reduce((s,i) => s+(i.qty||0), 0) }}</strong></span>
                <span>SL giao: <strong>0</strong></span>
              </div>
              <div class="odp-footer-total">
                Tổng tiền: <strong>{{ formatValue(soDetailItems.reduce((s,i) => s+(i.amount||0), 0), 'grand_total') }}</strong>
              </div>
            </div>
          </aside>

          <!-- ── Filter panel ──────────────────────────────── -->
          <aside v-if="soFilterOpen" class="orders-filter-panel">
            <div class="ofp-header">
              <span class="ofp-title">Bộ lọc</span>
              <button class="crm-btn-icon" @click="soFilterOpen = false" data-tooltip="Đóng">
                <svg viewBox="0 0 16 16" fill="none" width="11" height="11"><path d="M3 3l10 10M13 3L3 13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
              </button>
            </div>
            <div class="ofp-body">
              <div class="ofp-section">
                <div class="ofp-section-title">ĐÃ LƯU</div>
                <div v-for="sf in SO_SAVED_FILTERS" :key="sf.key"
                  class="ofp-saved-item"
                  :class="{active: soSavedFilterActive === sf.key}"
                  @click="activateSavedFilter(sf.key)">
                  {{ sf.label }}
                </div>
              </div>
              <div class="ofp-section">
                <div class="ofp-section-title">TIÊU CHÍ LỌC</div>
                <label v-for="fc in SO_FILTER_CRITERIA" :key="fc.field" class="ofp-crit-item">
                  <input type="checkbox"
                    :checked="ordersEnabledFilters.includes(fc.field)"
                    @change="toggleOrdersFilter(fc.field)"
                    class="ofp-crit-chk">
                  <span>{{ fc.label }}</span>
                </label>
              </div>
              <div v-if="ordersEnabledFilters.length" class="ofp-section">
                <div class="ofp-section-title">GIÁ TRỊ LỌC</div>
                <div v-for="field in ordersEnabledFilters" :key="field" class="ofp-filter-row">
                  <label class="ofp-filter-label">{{ SO_FILTER_CRITERIA.find(f=>f.field===field)?.label }}</label>
                  <template v-if="field === 'custom_revenue_status'">
                    <select v-model="ordersFilterValues[field]" @change="loadRows" class="ofp-filter-sel">
                      <option value="">Tất cả</option>
                      <option value="Bản nhập">Đơn nháp</option><option value="Đã ghi">Đã ghi</option><option value="Hủy">Hủy</option>
                    </select>
                  </template>
                  <template v-else-if="field === 'delivery_status'">
                    <select v-model="ordersFilterValues[field]" @change="loadRows" class="ofp-filter-sel">
                      <option value="">Tất cả</option>
                      <option>Not Delivered</option><option>Partly Delivered</option>
                      <option>Fully Delivered</option><option>Closed</option>
                    </select>
                  </template>
                  <template v-else-if="['transaction_date','custom_revenue_recognition_date'].includes(field)">
                    <input type="date" v-model="ordersFilterValues[field]" @change="loadRows" class="ofp-filter-inp">
                  </template>
                  <template v-else>
                    <input v-model="ordersFilterValues[field]" @keyup.enter="loadRows" class="ofp-filter-inp" placeholder="Lọc...">
                  </template>
                </div>
              </div>
            </div>
          </aside>
          </div>

        </main>

        <!-- SO Action Modal -->
        <div v-if="soActionModalOpen" class="soa-overlay" @mousedown.self="closeSOActionModal">
          <div class="soa-modal">
            <div class="soa-modal-header">
              <span class="soa-modal-title">Tạo nhiệm vụ</span>
              <div class="soa-modal-actions">
                <button class="sod-btn" @click="closeSOActionModal" :disabled="soActionModalSaving">Hủy</button>
                <button class="sod-btn sod-btn-primary" @click="confirmSOActionModal" :disabled="soActionModalSaving">
                  {{ soActionModalSaving ? 'Đang lưu...' : 'Lưu' }}
                </button>
              </div>
            </div>
            <div class="soa-modal-body">
              <div class="hd-ef-section-title">Thông tin nhiệm vụ</div>

              <!-- Tiêu đề -->
              <div class="hd-ef-row">
                <span class="hd-ef-lbl">Tiêu đề <span class="hd-ef-req">*</span></span>
                <div class="hd-ef-input-wrap">
                  <input class="hd-ef-input" v-model="soActionModalForm.title" placeholder="Tiêu đề nhiệm vụ">
                  <button v-if="soActionModalForm.title" class="hd-ef-clear-btn" @click="soActionModalForm.title = ''">
                    <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                  </button>
                </div>
              </div>

              <!-- Hạn hoàn thành -->
              <div class="hd-ef-row">
                <span class="hd-ef-lbl">Hạn hoàn thành</span>
                <div class="hd-ef-date-wrap">
                  <input type="date" class="hd-ef-input hd-ef-date-input" v-model="soActionModalForm.date">
                </div>
              </div>

              <!-- Mức độ ưu tiên -->
              <div class="hd-ef-row">
                <span class="hd-ef-lbl">Mức độ ưu tiên <span class="hd-ef-req">*</span></span>
                <div class="hd-ef-select-wrap">
                  <select class="hd-ef-select" v-model="soActionModalForm.priority">
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
                <span class="hd-ef-lbl">Trạng thái <span class="hd-ef-req">*</span></span>
                <div class="hd-ef-select-wrap">
                  <select class="hd-ef-select" v-model="soActionModalForm.status">
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
                <div class="hd-ef-users-wrap" v-click-outside="soActionModalCloseUserDd">
                  <div class="hd-ef-tags-box" @click="soActionModalOnUserFocus">
                    <span v-for="u in soActionModalForm.related_users" :key="u.name" class="hd-ef-tag">
                      <span class="hd-ef-tag-avatar">{{ (u.full_name || u.name).charAt(0).toUpperCase() }}</span>
                      {{ u.full_name || u.name }}
                      <button class="hd-ef-tag-remove" @click.stop="soActionModalRemoveUser(u.name)">
                        <svg viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                      </button>
                    </span>
                    <div class="hd-ef-user-search-wrap">
                      <input class="hd-ef-user-input" placeholder="Thêm người liên quan..." v-model="soActionModalUserQuery" @input="soActionModalOnUserInput" @focus.stop="soActionModalOnUserFocus">
                      <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="hd-ef-user-ico"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                    </div>
                  </div>
                  <div v-if="soActionModalUserDdOpen && soActionModalUserDropdown.length" class="hd-ef-user-dd">
                    <div v-for="u in soActionModalUserDropdown" :key="u.name" class="hd-ef-user-dd-item" :class="{ 'hd-ef-dd-selected': soActionModalIsUserSel(u.name) }" @mousedown.prevent="soActionModalToggleUser(u)">
                      <span class="hd-ef-dd-avatar" :class="{ 'hd-ef-dd-avatar--sel': soActionModalIsUserSel(u.name) }">{{ (u.full_name || u.name).charAt(0).toUpperCase() }}</span>
                      <div class="hd-ef-dd-info"><span class="hd-ef-dd-name">{{ u.full_name }}</span></div>
                      <svg v-if="soActionModalIsUserSel(u.name)" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="hd-ef-dd-check"><polyline points="20 6 9 17 4 12"/></svg>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Loại nhiệm vụ -->
              <div class="hd-ef-row">
                <span class="hd-ef-lbl">Loại nhiệm vụ</span>
                <div class="hd-ef-tt-wrap" v-click-outside="soActionModalCloseTt">
                  <button class="hd-ef-tt-btn" @click.stop="soActionModalToggleTt" type="button">
                    <span :class="{ 'hd-ef-tt-placeholder': !soActionModalForm.task_type }">{{ soActionModalForm.task_type || 'Chọn loại nhiệm vụ' }}</span>
                    <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
                  </button>
                  <div v-if="soActionModalTtOpen" class="hd-ef-tt-dd">
                    <div class="hd-ef-tt-search-wrap">
                      <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="hd-ef-tt-search-ico"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
                      <input class="hd-ef-tt-search-input" placeholder="Tìm kiếm" v-model="soActionModalTtQuery" @click.stop>
                    </div>
                    <div class="hd-ef-tt-list">
                      <div v-for="opt in soActionModalFilteredTt" :key="opt" class="hd-ef-tt-item" :class="{ 'hd-ef-tt-item--sel': soActionModalForm.task_type === opt }" @click.stop="soActionModalSelectTt(opt)">
                        <span>{{ opt }}</span>
                        <svg v-if="soActionModalForm.task_type === opt" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="hd-ef-tt-check"><polyline points="20 6 9 17 4 12"/></svg>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <template v-if="soActionModalForm.task_type === 'Đề nghị ghi doanh số'">
                <div class="hd-ef-section-title">Thông tin ghi nhận doanh số</div>
                <div class="hd-ef-row">
                  <span class="hd-ef-lbl">Hàng hóa</span>
                  <div class="hd-ef-select-wrap">
                    <select class="hd-ef-select" v-model="soActionModalForm.revenue_item">
                      <option value="">- Không chọn -</option>
                      <option v-for="item in orderDetail.items" :key="item.name" :value="item.item_code">{{ item.item_name || item.item_code }}</option>
                    </select>
                    <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="hd-ef-select-ico"><path d="m6 9 6 6 6-6"/></svg>
                  </div>
                </div>
                <div class="hd-ef-row">
                  <span class="hd-ef-lbl">Đơn vị</span>
                  <div class="hd-ef-input-wrap">
                    <button type="button" class="so-pe-org-trigger" @click="openSOOrgPicker(soActionModalForm)">
                      <span>{{ soActionModalForm.department_label || '- Chọn đơn vị -' }}</span>
                      <CRMIcon name="all" />
                    </button>
                  </div>
                </div>
                <div class="hd-ef-row">
                  <span class="hd-ef-lbl">Doanh số ghi nhận</span>
                  <div class="hd-ef-input-wrap">
                    <input type="number" class="hd-ef-input" v-model.number="soActionModalForm.recognized_amount">
                  </div>
                </div>
                <div class="hd-ef-row">
                  <span class="hd-ef-lbl">Doanh số thực hiện được</span>
                  <div class="hd-ef-input-wrap">
                    <input type="number" class="hd-ef-input" v-model.number="soActionModalForm.achieved_amount">
                  </div>
                </div>
                <div class="hd-ef-row hd-ef-row-top">
                  <span class="hd-ef-lbl">Ghi chú</span>
                  <div class="hd-ef-input-wrap">
                    <textarea class="hd-ef-input" rows="2" v-model="soActionModalForm.note"></textarea>
                  </div>
                </div>
              </template>

            </div>

            <div v-if="soOrgPickerOpen" class="so-pe-org-overlay" @click.self="closeSOOrgPicker">
              <section class="so-pe-org-picker">
                <header>
                  <h3>Chọn cơ cấu tổ chức</h3>
                  <button title="Đóng" aria-label="Đóng" @click="closeSOOrgPicker">×</button>
                </header>
                <div class="so-pe-org-tree">
                  <OrgUnitNode
                    v-for="node in soOrgTree"
                    :key="node.value"
                    :node="node"
                    :selected-value="soActionModalForm.department"
                    @toggle="toggleOrgNode"
                    @select="selectSOOrgNode"
                  />
                  <p v-if="!soOrgTree.length" class="org-node-empty">Đang tải...</p>
                </div>
              </section>
            </div>
          </div>
        </div>
`;
