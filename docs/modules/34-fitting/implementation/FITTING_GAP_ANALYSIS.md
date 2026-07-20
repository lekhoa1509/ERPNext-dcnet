# Fitting Module - Gap Analysis

**Nguồn:** FEATURE_SPECIFICATION.md Section 5.1, 5.2.2, 5.4, 5.5, 14.2
**Ngày tạo:** 2026-01-24
**Trạng thái:** Draft

---

## 1. Tổng quan

### 1.1 Mục tiêu
Phân tích khoảng cách giữa yêu cầu nghiệp vụ Fitting với chức năng ERPNext có sẵn.

### 1.2 Phạm vi
- 13 Use Cases từ spec khách hàng
- 8 trạng thái workflow
- 14+ thông số kỹ thuật
- 5 báo cáo

---

## 2. Existing Implementation (Hiện tại)

### 2.1 Fitting Session DocType
**Path:** `dcnet_apps/fitting/doctype/fitting_session/`

| Field | Fieldtype | Hiện tại | Yêu cầu |
|-------|-----------|----------|---------|
| naming_series | Select | FIT-SESS-.YYYY.- | FIT-.YYYY.-.##### |
| customer | Link | Customer only | Dynamic Link (Lead/Customer) |
| customer_name | Data | ✅ Fetch from customer | ✅ |
| contact_person | Link | Contact | ❌ Không cần |
| session_date | Date | ✅ | Cần Datetime |
| status | Select | 4 options | 8 options |
| measurements | Table | ✅ (nhưng DocType trống) | 14+ fields |
| notes | Text Editor | ✅ | ✅ |

**Status hiện tại (4):**
- Scheduled, In Progress, Completed, Cancelled

**Status yêu cầu (8):**
- new, confirmed, in_progress, completed, has_order, follow_up, no_show, cancelled

### 2.2 Fitting Measurement DocType
**Path:** `dcnet_apps/fitting/doctype/fitting_measurement/`

**Trạng thái:** ❌ **EMPTY** - Chưa có JSON definition

### 2.3 Fitting Service DocType
**Trạng thái:** ❌ **NOT EXIST** - Chưa tạo

---

## 3. Gap Analysis Matrix

### 3.1 Use Case Coverage

| UC | Chức năng | ERPNext Coverage | Gap | Effort |
|----|-----------|------------------|-----|--------|
| UC-01 | Tạo đơn Fitting mới | 40% | Party dynamic link, source, company | Medium |
| UC-02 | Xem danh sách đơn Fitting | 90% | List View có sẵn | Low |
| UC-03 | Xem chi tiết đơn Fitting | 70% | Form View, cần thêm tabs | Low |
| UC-04 | Xác nhận lịch hẹn | 0% | Cần workflow action buttons | Medium |
| UC-05 | Cập nhật trạng thái | 30% | Cần 8-state workflow | Medium |
| UC-06 | Nhập thông số kỹ thuật | 10% | Cần Fitting Measurement DocType | High |
| UC-07 | Thêm dịch vụ phát sinh | 0% | Cần Fitting Service DocType | High |
| UC-08 | Ghi đề xuất nâng cấp | 50% | Field trong Measurement | Low |
| UC-09 | Tạo đơn hàng từ Fitting | 0% | Cần API create Sales Order | High |
| UC-10 | Phân công NV Fitting | 20% | Cần assigned_fitter field | Low |
| UC-11 | Xem báo cáo Fitting | 0% | Cần 5 Script Reports | High |
| UC-12 | Nhận đăng ký từ Website | 0% | Cần Whitelist API | Medium |
| UC-13 | Xem Calendar lịch hẹn | 40% | Calendar View config | Medium |

**Summary:**
- **Có sẵn 70-90%:** 2 UC (List View, Detail View)
- **Cần bổ sung 30-60%:** 5 UC
- **Cần xây mới 70-100%:** 6 UC

### 3.2 DocType Fields Gap

#### Fitting Session - Missing Fields

| Field | Fieldtype | Section | Priority |
|-------|-----------|---------|----------|
| party_type | Link | Thông tin chung | Critical |
| party | Dynamic Link | Thông tin chung | Critical |
| phone | Data | Thông tin chung | High |
| email | Data | Thông tin chung | High |
| scheduled_datetime | Datetime | Lịch hẹn | Critical |
| company | Link | Lịch hẹn | Critical |
| source | Select | Lịch hẹn | High |
| assigned_fitter | Link | Phân công | High |
| assigned_sale | Link | Phân công | Medium |
| confirmed_at | Datetime | Trạng thái | Medium |
| started_at | Datetime | Trạng thái | Medium |
| completed_at | Datetime | Trạng thái | Medium |
| cancelled_at | Datetime | Trạng thái | Low |
| cancel_reason | Text | Trạng thái | Low |
| services | Table | Dịch vụ | Critical |
| total_amount | Currency | Dịch vụ | Critical |
| calendar_event | Link | Tích hợp | Medium |
| sales_order | Link | Tích hợp | High |
| internal_notes | Text Editor | Notes | Low |

#### Fitting Measurement - New DocType Required

| Field | Fieldtype | Description |
|-------|-----------|-------------|
| height | Int | Chiều cao (cm) |
| weight | Float | Cân nặng (kg) |
| hand_size | Select | S/M/L/XL |
| skill_level | Select | Người mới/Người đã chơi |
| club_head_speed | Float | Tốc độ đầu gậy |
| ball_speed | Float | Tốc độ bóng |
| swing_shape | Text | Hình swing |
| ball_flight | Select | Low/Mid/High |
| ball_trajectory | Select | Đường cao bóng |
| iron_distance | Int | Khoảng cách gậy sắt |
| driver_distance | Int | Khoảng cách driver |
| current_club_condition | Text | Tình trạng bộ gậy |
| special_requirements | Text | Nhu cầu riêng |
| upgrade_recommendations | Text | Đề xuất nâng cấp |

#### Fitting Service - New DocType Required

| Field | Fieldtype | Description |
|-------|-----------|-------------|
| service_type | Select | grip/shaft/custom_club/combo |
| item | Link | Item DocType |
| item_name | Data | Fetch from item |
| quantity | Int | Số lượng |
| rate | Currency | Đơn giá |
| amount | Currency | Thành tiền |
| specs_note | Text | Thông số đặc biệt |

### 3.3 Workflow Gap

| Aspect | Current | Required | Gap |
|--------|---------|----------|-----|
| States | 4 | 8 | +4 states |
| Transitions | Manual | Workflow Actions | Workflow fixture |
| Permissions | Basic | Role-based | Permission matrix |
| Timestamps | None | Auto-set | Controller logic |

**Missing Transitions:**
- new → confirmed (Xác nhận lịch)
- confirmed → in_progress (Bắt đầu fitting)
- confirmed → no_show (Vắng mặt)
- in_progress → completed (Hoàn thành)
- completed → has_order (Tạo đơn hàng)
- completed → follow_up (Chờ follow-up)
- Any → cancelled (Hủy)

### 3.4 Integration Gap

| Integration | ERPNext Feature | Gap |
|-------------|-----------------|-----|
| Lead/Customer | Dynamic Link pattern | Cần implement |
| Calendar | Event DocType | Cần sync logic |
| Sales Order | Make SO from Doc | Cần custom method |
| Website | Webform/API | Cần whitelist API |

### 3.5 Reports Gap

| Report | ERPNext Feature | Gap |
|--------|-----------------|-----|
| fitting_revenue | Query Report | Cần tạo mới |
| fitting_sessions_monthly | Query Report | Cần tạo mới |
| fitting_customer_count | Query Report | Cần tạo mới |
| fitting_accessories_usage | Query Report | Cần tạo mới |
| fitting_staff_performance | Query Report | Cần tạo mới |

---

## 4. ERPNext Patterns Available

### 4.1 Reusable Patterns

| Pattern | ERPNext Source | Apply to Fitting |
|---------|----------------|------------------|
| Dynamic Link | Quotation.party_type + party | Lead/Customer selection |
| Make From | Sales Order → Delivery Note | Fitting → Sales Order |
| Calendar View | Event, Appointment | Fitting Calendar |
| Child Table | Sales Order Item | Fitting Measurement, Service |
| Workflow | Purchase Order | 8-state workflow |
| Query Report | Sales Analytics | 5 Fitting Reports |

### 4.2 Code References

```python
# Dynamic Link pattern - from Quotation
party_type = Link("DocType", label="Party Type")
party = Dynamic Link("party_type", label="Party")

# Make From pattern - from Sales Order
@frappe.whitelist()
def make_sales_invoice(source_name):
    return _make_sales_invoice(source_name)

# Calendar View pattern - from Event
frappe.views.calendar['Fitting Session'] = {
    field_map: {
        start: 'scheduled_datetime',
        end: 'scheduled_datetime',
        title: 'customer_name'
    }
}
```

---

## 5. Build vs Extend Analysis

| Component | Strategy | Rationale |
|-----------|----------|-----------|
| Fitting Session | **Extend** | Có DocType, cần thêm fields |
| Fitting Measurement | **Build** | DocType trống, cần tạo |
| Fitting Service | **Build** | Chưa tồn tại |
| Workflow | **Build** | Fixture mới |
| Calendar View | **Extend** | Frappe Calendar có sẵn |
| Reports | **Build** | 5 Query Reports mới |
| API | **Build** | Whitelist methods |

---

## 6. Risk Assessment

### 6.1 Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Dynamic Link complexity | Medium | Low | Follow Quotation pattern |
| Calendar sync issues | Medium | Medium | Event DocType integration |
| Sales Order mapping | High | Low | Clear field mapping |
| Performance with reports | Low | Low | Index optimization |

### 6.2 Business Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Lead conversion logic | High | Clear business rules |
| Status transition | Medium | Workflow validation |
| Data migration | Low | Migration script |

---

## 7. Summary

### 7.1 Coverage Score

| Category | ERPNext Coverage | Build Effort |
|----------|------------------|--------------|
| DocTypes | 30% | High |
| Workflow | 20% | Medium |
| UI (Standard) | 70% | Low |
| UI (frappe-ui) | 0% | High |
| Reports | 0% | Medium |
| API | 0% | Medium |
| **Overall** | **~25%** | **High** |

### 7.2 Effort Estimate

| Component | Effort (days) |
|-----------|---------------|
| Fitting Measurement DocType | 1 |
| Fitting Service DocType | 1 |
| Update Fitting Session DocType | 2 |
| Controller + Workflow | 2 |
| Calendar View | 1 |
| 5 Reports | 3 |
| API Endpoints | 2 |
| Option A: Frappe Standard UI | 2 |
| Option B: frappe-ui Vue Pages | 5 |
| Testing & QA | 3 |
| **Total (Option A only)** | **17 days** |
| **Total (Both Options)** | **22 days** |

---

## 8. Recommendations

1. **Prioritize Core DocTypes** - Fitting Measurement và Fitting Service trước
2. **Use Dynamic Link Pattern** - Theo Quotation của ERPNext
3. **Workflow Fixture** - Tách riêng để dễ maintain
4. **Option A First** - Frappe Standard trước, frappe-ui sau
5. **Incremental Delivery** - MVP với UC-01 đến UC-06 trước

---

**Next:** [FITTING_IMPLEMENTATION_PLAN.md](./FITTING_IMPLEMENTATION_PLAN.md)
