export default `
        <main v-if="route === 'dashboard'" class="crm-dashboard crm-dashboard-reference">
          <header class="crm-dashboard-toolbar" aria-labelledby="crm-dashboard-title">
            <div>
              <h1 id="crm-dashboard-title">Bàn làm việc</h1>
              <p>Tổng quan hoạt động kinh doanh và chăm sóc khách hàng</p>
            </div>
            <div class="crm-dashboard-toolbar-actions">
              <button class="crm-button crm-refresh-button" :disabled="loading" @click="loadDashboard" aria-label="Làm mới dữ liệu dashboard">
                <CRMIcon name="refresh" /> <span>{{ loading ? 'Đang cập nhật' : 'Làm mới' }}</span>
              </button>
              <button class="crm-button primary crm-dashboard-cta" @click="createDocument('Lead')">
                <CRMIcon name="plus" /> Thêm tiềm năng
              </button>
            </div>
          </header>

          <section class="crm-kpis" aria-label="Chỉ số kinh doanh">
            <button class="crm-kpi-card blue" @click="navigate('leads')">
              <span class="crm-kpi-heading"><CRMIcon name="lead" /><small>Tiềm năng</small></span>
              <strong>{{ dashboard.kpis.leads }}</strong>
              <span class="crm-kpi-note">Hồ sơ đang quản lý <CRMIcon name="arrow-right" /></span>
            </button>
            <button class="crm-kpi-card violet" @click="navigate('opportunities')">
              <span class="crm-kpi-heading"><CRMIcon name="opportunity" /><small>Cơ hội</small></span>
              <strong>{{ dashboard.kpis.opportunities }}</strong>
              <span class="crm-kpi-note">Trong phễu bán hàng <CRMIcon name="arrow-right" /></span>
            </button>
            <button class="crm-kpi-card cyan" @click="navigate('customers')">
              <span class="crm-kpi-heading"><CRMIcon name="customer" /><small>Khách hàng</small></span>
              <strong>{{ dashboard.kpis.customers }}</strong>
              <span class="crm-kpi-note">Hồ sơ khách hàng <CRMIcon name="arrow-right" /></span>
            </button>
            <button class="crm-kpi-card green" @click="navigate('orders')">
              <span class="crm-kpi-heading"><CRMIcon name="order" /><small>Đơn hàng</small></span>
              <strong>{{ dashboard.kpis.orders }}</strong>
              <span class="crm-kpi-note">Đơn chưa hủy <CRMIcon name="arrow-right" /></span>
            </button>
            <button class="crm-kpi-card amber" @click="navigate('orders')">
              <span class="crm-kpi-heading"><CRMIcon name="trend" /><small>Giá trị đơn hàng</small></span>
              <strong class="crm-kpi-money">{{ formatValue(dashboard.kpis.order_value, 'order_value') }} ₫</strong>
              <span class="crm-kpi-note">Tổng giá trị ghi nhận <CRMIcon name="arrow-right" /></span>
            </button>
          </section>

          <section class="crm-dashboard-bento">
            <article class="crm-card crm-funnel-card">
              <div class="crm-card-heading">
                <div><h2>Phễu cơ hội</h2><p>Phân bổ cơ hội theo từng giai đoạn bán hàng</p></div>
                <button @click="navigate('opportunities')">Xem tất cả <CRMIcon name="arrow-right" /></button>
              </div>
              <div v-if="dashboard.funnel.length" class="crm-funnel-summary" aria-label="Tổng hợp phễu cơ hội">
                <span><span class="crm-summary-icon blue"><CRMIcon name="opportunity" /></span><span><small>Tổng cơ hội</small><strong>{{ funnelTotal }}</strong></span></span>
                <span><span class="crm-summary-icon amber"><CRMIcon name="trend" /></span><span><small>Tổng giá trị</small><strong>{{ formatValue(funnelValue, 'opportunity_amount') }} ₫</strong></span></span>
              </div>
              <div v-if="dashboard.funnel.length" class="crm-funnel">
                <div class="crm-funnel-labels" aria-hidden="true"><span>Giai đoạn</span><span>Số lượng</span><span>Giá trị</span></div>
                <button v-for="(stage, index) in dashboard.funnel" :key="stage.stage || 'unclassified'" @click="navigate('opportunities')">
                  <span class="crm-funnel-stage"><span><i :style="{ background: funnelColor(index) }"></i>{{ stage.stage || 'Chưa phân loại' }}</span><b><i :style="{ width: funnelWidth(stage.count), background: funnelColor(index) }"></i></b></span>
                  <strong>{{ stage.count }}</strong>
                  <small>{{ formatValue(stage.amount, 'opportunity_amount') }} ₫</small>
                </button>
              </div>
              <div v-else class="crm-dashboard-empty"><span><CRMIcon name="opportunity" /></span><strong>Chưa có dữ liệu cơ hội</strong><p>Các cơ hội mới sẽ được tổng hợp theo giai đoạn tại đây.</p><button @click="createDocument('Opportunity')">Tạo cơ hội đầu tiên</button></div>
            </article>

            <aside class="crm-dashboard-side-stack">
              <article class="crm-card crm-mix-card">
                <div class="crm-card-heading">
                  <div><h2>Cơ cấu cơ hội</h2><p>Tỷ trọng theo giai đoạn</p></div>
                  <button @click="navigate('opportunities')">Chi tiết <CRMIcon name="arrow-right" /></button>
                </div>
                <div v-if="dashboard.funnel.length" class="crm-mix-content">
                  <div class="crm-funnel-donut" :style="funnelDonutStyle" role="img" :aria-label="funnelTotal + ' cơ hội được phân bổ theo giai đoạn'">
                    <span><strong>{{ funnelTotal }}</strong><small>Cơ hội</small></span>
                  </div>
                  <div class="crm-funnel-legend">
                    <span v-for="(stage, index) in dashboard.funnel.slice(0, 6)" :key="stage.stage || index">
                      <i :style="{ background: funnelColor(index) }"></i><b>{{ stage.stage || 'Chưa phân loại' }}</b><small>{{ stage.count }}</small>
                    </span>
                  </div>
                </div>
                <p v-else class="crm-mix-empty">Chưa có dữ liệu để hiển thị cơ cấu.</p>
              </article>

              <article class="crm-card crm-quick-card">
                <div class="crm-card-heading"><div><h2>Thao tác nhanh</h2><p>Tạo hồ sơ nghiệp vụ mới</p></div></div>
                <div class="crm-actions">
                  <button @click="createDocument('Lead')"><span><CRMIcon name="lead" /></span><span><b>Tạo tiềm năng</b><small>Ghi nhận đầu mối mới</small></span><CRMIcon name="arrow-right" /></button>
                  <button @click="createDocument('Opportunity')"><span><CRMIcon name="opportunity" /></span><span><b>Tạo cơ hội</b><small>Theo dõi thương vụ mới</small></span><CRMIcon name="arrow-right" /></button>
                  <button @click="createDocument('Customer')"><span><CRMIcon name="customer" /></span><span><b>Tạo khách hàng</b><small>Thêm hồ sơ khách hàng</small></span><CRMIcon name="arrow-right" /></button>
                  <button @click="createDocument('Quotation')"><span><CRMIcon name="quotation" /></span><span><b>Tạo báo giá</b><small>Chuẩn bị đề xuất bán hàng</small></span><CRMIcon name="arrow-right" /></button>
                </div>
              </article>
            </aside>
          </section>
        </main>
`;
