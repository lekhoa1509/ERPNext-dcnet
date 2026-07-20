# Gap Analysis: Lead Module

> **Module:** Lead Management
> **Source Spec:** docs/modules/lead/LEAD_SPEC.md
> **ERPNext Version:** v15.8.0
> **Analysis Date:** 2026-01-12

---

## Executive Summary

| Metric | Value |
| --- | --- |
| **Total Requirements** | 16 features |
| **Available in ERPNext** | 9 features (56%) |
| **Needs Customization** | 5 features (31%) |
| **Needs New Development** | 2 features (13%) |
| **Complexity Score** | Medium (24/50) |

---

## Requirements Coverage Matrix

### Category 1: Lead List Management

| # | Requirement | Source | ERPNext Feature | Coverage | Gap Type | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Display lead list with columns | LEAD_SPEC #L15-33 | Lead List View | 60% | 🔧 Customize | Need custom fields: branch, date_received, last_contact, total_interactions |
| 2 | Hide/show columns | LEAD_SPEC #L35 | Standard List Settings | 100% | ✅ Available | Out-of-box |
| 3 | Update tags in list | LEAD_SPEC #L36 | Standard Tags | 100% | ✅ Available | Out-of-box |
| 4 | Search by name, email | LEAD_SPEC #L39 | Standard Search | 100% | ✅ Available | Out-of-box |
| 5 | Filter by status, branch, tags, etc. | LEAD_SPEC #L40-48 | Standard Filters | 90% | 🔧 Customize | Need custom fields for branch, age filters |

### Category 2: Lead Creation

| # | Requirement | Source | ERPNext Feature | Coverage | Gap Type | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 6 | Create lead with basic info | LEAD_SPEC #L52-62 | Lead DocType | 80% | 🔧 Customize | Need custom fields: branch, date_received, birth_date |
| 7 | Advanced info (status, source, address) | LEAD_SPEC #L64-71 | Lead + Address DocTypes | 90% | 🔧 Customize | Address fields available, need price_list link |
| 8 | Check duplicate by phone/email | LEAD_SPEC #L74 | - | 0% | ❌ Build New | Need custom Python validation |

### Category 3: Import/Export

| # | Requirement | Source | ERPNext Feature | Coverage | Gap Type | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 9 | Import leads from Excel | LEAD_SPEC #L78-83 | Data Import Tool | 100% | ✅ Available | Standard ERPNext feature |
| 10 | Export leads to Excel | LEAD_SPEC #L130-135 | Data Export | 100% | ✅ Available | Standard ERPNext feature |

### Category 4: Lead Assignment

| # | Requirement | Source | ERPNext Feature | Coverage | Gap Type | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 11 | Manual lead assignment by admin | LEAD_SPEC #L86-89 | Assignment Rules + Manual | 100% | ✅ Available | Configure assignment, no auto-assign |

### Category 5: Lead Details & Consultation

| # | Requirement | Source | ERPNext Feature | Coverage | Gap Type | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 12 | View lead details (basic info) | LEAD_SPEC #L92-94 | Lead Form | 100% | ✅ Available | Standard fields |
| 13 | View transaction history | LEAD_SPEC #L95 | Timeline/Communications | 90% | ✅ Available | Standard ERPNext timeline |
| 14 | View documents & comments | LEAD_SPEC #L97-98 | File Attachments + Comments | 100% | ✅ Available | Standard features |
| 15 | Consultation history (child table) | LEAD_SPEC #L99-103 | - | 0% | ❌ Build New | Need custom Child DocType: Consultation Log |
| 16 | Auto convert Lead → Customer on Sales Order | LEAD_SPEC #L104 | make_customer() method | 80% | 🔧 Customize | ERPNext has method, need auto-trigger |

### Category 6: Lead Updates & Deletion

| # | Requirement | Source | ERPNext Feature | Coverage | Gap Type | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 17 | Update lead info | LEAD_SPEC #L108-112 | Standard Edit | 100% | ✅ Available | Standard CRUD |
| 18 | Delete lead | LEAD_SPEC #L116-119 | Standard Delete | 100% | ✅ Available | Standard CRUD |

### Category 7: Integration

| # | Requirement | Source | ERPNext Feature | Coverage | Gap Type | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 19 | Auto-create leads from nhanh_vn webhook | LEAD_SPEC #L122-127 | REST API | 50% | 🔧 Customize | REST API available, need custom webhook endpoint |
| 20 | Expose API for lead creation | LEAD_SPEC #L138-143 | REST API | 80% | ✅ Available | REST API available, need configure |

**Legend:**
- ✅ **Available** (80-100% coverage) - Out-of-box ERPNext feature
- 🔧 **Customize** (50-79% coverage) - Extend existing ERPNext feature
- ⚙️ **Extend** (20-49% coverage) - Major modification
- ❌ **Build New** (0-19% coverage) - Custom development

---

## ERPNext DocType Mapping

| Requirement | ERPNext DocType | Extends Standard? | New Fields Needed | Custom Scripts |
| --- | --- | --- | --- | --- |
| Lead Management | Lead | ✅ Yes | 8 custom fields | lead.js, lead.py |
| Consultation History | Lead Consultation Log | ❌ No (new) | - | consultation_log.js |
| Lead → Customer | Customer | ✅ Yes | - | sales_order.py (hook) |
| Address | Address | ✅ Yes | - | - |

### Custom Fields Required for Lead DocType:

| Field Name | Type | Description | Source Requirement |
| --- | --- | --- | --- |
| `custom_branch` | Link (Branch) | Chi nhánh | LEAD_SPEC #L68 |
| `custom_date_received` | Date | Ngày nhận lead | LEAD_SPEC #L56 |
| `custom_last_contact` | Datetime | Liên hệ lần cuối | LEAD_SPEC #L26 |
| `custom_total_interactions` | Int | Tổng số tương tác | LEAD_SPEC #L28 |
| `custom_birth_date` | Date | Ngày sinh | LEAD_SPEC #L61 |
| `custom_price_list` | Link (Price List) | Bảng giá áp dụng | LEAD_SPEC #L70 |
| `custom_sales_person` | Link (Sales Person) | Sale chăm sóc | LEAD_SPEC #L71 |
| `custom_age_group` | Select | Độ tuổi (for filtering) | LEAD_SPEC #L47 |

---

## API & Integration Analysis

| Integration Point | Requirement | ERPNext Support | Gap | Implementation |
| --- | --- | --- | --- | --- |
| nhanh_vn Webhook | Auto create Lead from external | REST API available | Custom endpoint | Use @frappe.whitelist() + custom validation |
| Expose API | Allow external systems to create customers | REST API framework | Configure auth | Use standard REST API + token auth |
| Data Import | Import leads from Excel | Data Import Tool | None | Use standard tool |
| Data Export | Export leads to Excel | Data Export | None | Use standard export |

---

## Business Logic Comparison

### Flow 1: Lead Creation with Duplicate Check

**Requirements (from SPEC):**
```
1. User creates Lead with phone/email
2. System checks duplicate by phone/email
3. If duplicate exists, show error
4. If unique, save Lead with auto-generated code
```

**ERPNext Standard:**
```
1. ✅ Lead creation supported
2. ❌ No auto duplicate check by phone/email
3. ❌ No duplicate validation
4. ✅ Auto-generated naming series (LEAD-00001)
```

**Gap Summary:**
- Need: Custom Python validation in `validate()` method
- Implementation: Check `frappe.db.exists()` for phone/email before save

---

### Flow 2: Lead to Customer Conversion

**Requirements (from SPEC):**
```
1. User creates Sales Order from Lead
2. System automatically converts Lead to Customer
3. Sales Order linked to new Customer
```

**ERPNext Standard:**
```
1. ✅ Can create Sales Order with Lead as party_type
2. ⚙️ Manual conversion via make_customer() method
3. ❌ No auto-conversion trigger
```

**Gap Summary:**
- Need: Hook into Sales Order `on_submit()` to auto-convert Lead
- Implementation: Override `on_submit()` in Sales Order

---

### Flow 3: Consultation History Tracking

**Requirements (from SPEC):**
```
1. View consultation history in Lead detail
2. Track: Product consulted, Consultant, Date, Content
3. Add new consultation entries
```

**ERPNext Standard:**
```
1. ❌ No consultation history feature
2. ❌ No standard child table for consultations
3. ✅ Timeline for general activities (but not structured)
```

**Gap Summary:**
- Need: Create custom Child DocType "Lead Consultation Log"
- Fields: product (Link to Item), consultant (Link to User), date, content (Text)
- Implementation: Add child table to Lead DocType

---

## Data Model Gap

### Entity: Lead

| Field | Required by Spec | ERPNext Standard | Action |
| --- | --- | --- | --- |
| Mã (auto) | ✅ LEAD_SPEC #L55 | ✅ `name` field | Use standard naming series |
| Tên | ✅ LEAD_SPEC #L57 | ✅ `lead_name` | Use standard |
| Giới tính | ✅ LEAD_SPEC #L58 | ✅ `gender` | Use standard |
| ĐT | ✅ LEAD_SPEC #L59 | ✅ `phone` / `mobile_no` | Use standard |
| Email | ✅ LEAD_SPEC #L60 | ✅ `email_id` | Use standard |
| Ngày sinh | ✅ LEAD_SPEC #L61 | ❌ Not exists | Add custom field: `custom_birth_date` |
| Nhân viên phụ trách | ✅ LEAD_SPEC #L62 | ✅ `lead_owner` | Use standard |
| Trạng thái | ✅ LEAD_SPEC #L65 | ✅ `status` | Use standard (customize options) |
| Tags | ✅ LEAD_SPEC #L66 | ✅ Standard Tags | Use standard |
| Nguồn | ✅ LEAD_SPEC #L67 | ✅ `source` | Use standard |
| Chi nhánh | ✅ LEAD_SPEC #L68 | ❌ Not exists | Add custom field: `custom_branch` (Link to Branch) |
| Địa chỉ | ✅ LEAD_SPEC #L69 | ✅ Address DocType | Use standard Address linking |
| Bảng giá | ✅ LEAD_SPEC #L70 | ❌ Not exists | Add custom field: `custom_price_list` |
| Sale chăm sóc | ✅ LEAD_SPEC #L71 | ❌ Not exists | Add custom field: `custom_sales_person` |
| Ngày nhận lead | ✅ LEAD_SPEC #L56 | ❌ Not exists | Add custom field: `custom_date_received` |
| Liên hệ lần cuối | ✅ LEAD_SPEC #L26 | ❌ Not exists | Add custom field: `custom_last_contact` |
| Tổng số tương tác | ✅ LEAD_SPEC #L28 | ❌ Not exists | Add custom field: `custom_total_interactions` |
| Lịch sử tư vấn | ✅ LEAD_SPEC #L99-103 | ❌ Not exists | Create Child DocType: `Lead Consultation Log` |

---

### Entity: Lead Consultation Log (New Child DocType)

| Field | Type | Description | Required |
| --- | --- | --- | --- |
| parent | Link (Lead) | Link to parent Lead | Yes |
| product | Link (Item) | Sản phẩm đã tư vấn | Yes |
| consultant | Link (User) | Nhân viên tư vấn | Yes |
| consultation_date | Date | Ngày tháng tư vấn | Yes |
| content | Text | Nội dung tư vấn | No |

---

## Complexity Assessment

### Technical Complexity: Medium

**Factors:**
- **Data Model:** 6/10
  - Need 8 custom fields on Lead
  - Need 1 new Child DocType (Consultation Log)
  - Moderate complexity

- **Business Logic:** 5/10
  - Duplicate check validation (simple query)
  - Auto Lead→Customer conversion (hook into Sales Order)
  - Moderate complexity

- **UI Customization:** 4/10
  - List view: Add custom columns (standard ERPNext)
  - Form: Add custom fields (standard)
  - Child table UI (standard)
  - Low complexity

- **Integration:** 6/10
  - Webhook endpoint for nhanh_vn (custom but straightforward)
  - REST API configuration (standard)
  - Moderate complexity

- **Migration Effort:** 3/10
  - If migrating from legacy CRM
  - Data mapping required
  - Low to moderate complexity

**Overall Complexity Score:** 24/50 = **Medium**

**Risk Factors:**
- ⚠️ Medium: Duplicate check validation (need test thoroughly for race conditions)
- ⚠️ Medium: Auto Lead→Customer conversion (need ensure no data loss)
- ✅ Low: Most features use standard ERPNext patterns

---

## Dependencies

### ERPNext Modules Required:
- **CRM** (Lead, Opportunity, Customer) - Core module
- **Selling** (Sales Order, Quotation) - For conversion
- **Setup** (Branch DocType - may need create if not exists)
- **Stock** (Item) - For consultation product linking

### Third-party Dependencies:
- **Python packages:** None (standard Frappe/ERPNext)
- **JS libraries:** None (standard ERPNext UI)

### Custom Modules:
- May need create **Branch** DocType if not in standard ERPNext

---

## Recommendations

### Approach: **Customize Existing (70%) + Build New (30%)**

**Rationale:**
- ERPNext Lead DocType provides solid foundation (~60% of requirements)
- Standard features (tags, filters, import/export, CRUD) work out-of-box
- Main customizations:
  - Add 8 custom fields (straightforward)
  - Create 1 child table (standard pattern)
  - Add duplicate check validation (simple Python)
  - Hook Lead→Customer conversion (standard override)
- Integration with nhanh_vn requires custom webhook (moderate effort)

**Estimated Coverage:**
- **Use ERPNext standard:** 56% (9 out of 16 features)
- **Customize existing:** 31% (5 features - custom fields, hooks)
- **New development:** 13% (2 features - duplicate check, consultation log)

**Development Approach:**
1. Start with ERPNext standard Lead (Week 1)
2. Add custom fields via Fixtures (Week 1-2)
3. Implement custom business logic (Week 2-3)
4. Build consultation log child table (Week 3)
5. Integrate nhanh_vn webhook (Week 4)
6. Testing & UAT (Week 5-6)

**Estimated Timeline:** 6-8 weeks with 1-2 developers

---

**Next Steps:**
1. Review with customer for alignment on custom fields
2. Create detailed implementation plan with task breakdown
3. Estimate timeline and resources
4. Set up ERPNext development environment
5. Begin Phase 1: Data Model Setup
