# BA Methodology Reference

> Phương pháp Business Analysis áp dụng cho DCNET Flow.
> Kết hợp: Requirements Engineering + BPMN Process Modeling + Stakeholder Analysis

---

## 1. Decision Framework

Khi nhận yêu cầu phân tích, xác định loại:

```
Requirements Type:
├── Feature mới → User stories + acceptance criteria
├── Cải tiến quy trình → AS-IS/TO-BE BPMN models
├── Tích hợp hệ thống → Interface specifications
├── Tuân thủ quy định → Regulatory requirements matrix
└── Yêu cầu stakeholder → Impact analysis + prioritization
```

---

## 2. Requirements Gathering Workflow

### 7 bước thu thập yêu cầu:

1. **Identify Stakeholders** — Ai liên quan? (Roles trong DCNET: BLD, TP, NV, KT, Kho)
2. **Discovery** — Đọc spec, interview, observe current process
3. **Document Pain Points** — Vấn đề hiện tại (VD: nhập tay, sai số, chậm)
4. **Define Success Metrics** — Thành công = gì? (VD: giảm 50% thời gian nhập kho)
5. **Draft Requirements** — Viết requirements sơ bộ
6. **Validate** — Review với stakeholders
7. **Prioritize** — MoSCoW hoặc tương đương

### MoSCoW Prioritization

| Priority | Nghĩa | DCNET mapping |
|----------|--------|---------------|
| **Must** | Bắt buộc, không có thì không đi live | USE + CFG features |
| **Should** | Quan trọng, nên có trong release | EXT features (core) |
| **Could** | Nice-to-have, có thể để phase sau | EXT features (nice-to-have) |
| **Won't** | Không làm trong scope này | Deferred to T8+ |

---

## 3. User Story Format

### Template

```
As a [Role],
I want [Goal/Action],
So that [Benefit/Value].
```

### Acceptance Criteria (Given/When/Then)

```
Given [Precondition],
When [Action],
Then [Expected Result].
```

### DCNET Example

```
As a BP Mua hàng,
I want to create Purchase Plan with monthly quantity breakdown,
So that I can plan procurement for the whole year by product category.

Given a Purchase Plan is created and linked to a Supplier,
When I click "Create Purchase Order",
Then a PO is auto-created with items from the Plan.
```

### User Story Mapping for ERPNext

| Spec Feature | User Story | ERPNext DocType | Acceptance Criteria |
|-------------|-----------|-----------------|---------------------|
| 3.1.3 Tạo PO | As BP MH, I want to create PO from plan... | Purchase Order | PO created with items, supplier, warehouse |
| 3.1.6 Nhập hàng | As NV Kho, I want to receive goods partially... | Purchase Receipt | PR linked to PO, partial qty accepted |

---

## 4. Business Process Modeling (AS-IS / TO-BE)

### Phase 1: Map Current State (AS-IS)

1. Xác định quy trình hiện tại từ spec khách hàng
2. Ghi nhận bottlenecks và pain points
3. Đánh dấu manual steps vs automated steps

> **DCNET lưu ý:** Khách đang dùng BRAVO → quy trình AS-IS lấy từ spec + phỏng đoán.
> Ghi rõ: "AS-IS dựa trên spec, cần xác nhận với khách."

### Phase 2: Design Future State (TO-BE)

1. Map sang ERPNext DocTypes + Workflows
2. Xác định automation points
3. Tính improvement metrics

### Phase 3: Gap Analysis

| Aspect | AS-IS | TO-BE | Gap | Action |
|--------|-------|-------|-----|--------|
| Nhập kho | Nhập tay BRAVO | Purchase Receipt submit | Chuyển đổi UX | Training |
| Duyệt PO | Email/giấy | Workflow Approval | Thêm workflow | Config |
| Tracking | Excel | PO Dashboard | Tự động | USE |

---

## 5. RACI Matrix

### Template

| Activity | BLD | TP Mua hàng | NV Mua hàng | TP Kho | NV Kho | Kế toán |
|----------|-----|-------------|-------------|--------|--------|---------|
| Tạo KH mua hàng | A | R | C | C | I | I |
| Duyệt PO | A | R | - | I | I | I |
| Nhập kho | I | C | I | A | R | I |
| Ghi nhận GL | I | I | I | I | I | R/A |

**Legend:**
- **R** (Responsible): Người thực hiện
- **A** (Accountable): Người chịu trách nhiệm cuối cùng (1 per row)
- **C** (Consulted): Cần tham vấn trước khi làm
- **I** (Informed): Cần thông báo sau khi xong

**Rules:**
- Mỗi hàng PHẢI có đúng 1 "A"
- "A" có thể kiêm "R"
- Không để ô trống (dùng "-" nếu không liên quan)

---

## 6. Stakeholder Analysis

### Power-Interest Grid

```
         High Interest          Low Interest
  ┌─────────────────────┬─────────────────────┐
  │   MANAGE CLOSELY    │   KEEP SATISFIED    │
  │   (Key Players)     │   (Meet Their Needs)│
  │                     │                     │
High│   BLD, TP Mua hàng  │   BLD (khác bộ phận)│
Power│   TP Kho, Kế toán TT│                     │
  ├─────────────────────┼─────────────────────┤
  │   KEEP INFORMED     │   MONITOR           │
  │   (Show Consider.)  │   (Minimal Effort)  │
Low │                     │                     │
Power│   NV Mua hàng       │   IT Support        │
  │   NV Kho             │                     │
  └─────────────────────┴─────────────────────┘
```

### Stakeholder Register

| Stakeholder | Role | Interest | Power | Strategy |
|-------------|------|----------|-------|----------|
| BLD | Ban lãnh đạo | High | High | Manage closely, regular reports |
| TP Mua hàng | Trưởng phòng | High | High | Key user, involve in UAT |
| NV Kho | Nhân viên kho | High | Low | Training, change management |
| Kế toán | Kế toán tổng hợp | Medium | Medium | Verify GL entries, report format |

---

## 7. Requirements Traceability

### Traceability Matrix Format

```
Spec → Requirement → Process Step → DocType → Field → Test Case
```

| Level | What | Example |
|-------|------|---------|
| L1 | Spec Feature | 3.1.3 Tạo PO |
| L2 | Requirement | PO phải có Ship mode, Confirm ship date |
| L3 | Process Step | QT2 Step 1: Tạo PO |
| L4 | DocType.Field | Purchase Order.custom_ship_mode |
| L5 | Test Case | TC-05-003: Tạo PO với Ship mode = Sea |

### Coverage Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Requirements Coverage | Traced requirements / Total requirements | 100% |
| Process Coverage | Features in process / Total features | > 90% |
| Test Coverage | Test cases / Requirements | >= 1:1 |

---

## 8. Anti-Patterns to Avoid

| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Solution in requirements | Ràng buộc implementation | Focus "what" not "how" |
| Missing acceptance criteria | Không biết khi nào "done" | Mỗi story cần testable criteria |
| No stakeholder validation | Build sai thứ | Review thường xuyên |
| Waterfall requirements | Không thể adapt | Iterative refinement |
| Technical jargon | Business không validate được | Dùng ngôn ngữ nghiệp vụ |
| Gold plating | Thêm feature không có trong spec | Chỉ làm những gì spec yêu cầu |

---

## 9. DCNET-Specific Conventions

### Roles mapping (DCNET → ERPNext Permission Roles)

| DCNET Role | ERPNext Role | Modules |
|------------|-------------|---------|
| BLD (Ban lãnh đạo) | System Manager | All |
| TP Mua hàng | Purchase Manager | Buying |
| NV Mua hàng | Purchase User | Buying |
| TP Kho | Stock Manager | Stock |
| NV Kho | Stock User | Stock |
| Kế toán TT | Accounts Manager | Accounts |
| NV Kế toán | Accounts User | Accounts |
| Sale | Sales User | Selling |
| Admin | Administrator | Setup |

### Process naming convention

```
QT{N}: {Tên quy trình}
VD: QT1: Lập kế hoạch mua hàng
    QT2: Đặt hàng NCC
    QT3: Nhập kho
```

### Document ID convention

```
BA-{STT}-{date}
VD: BA-05-20260217 = BA Analysis for module 05, created 17/02/2026
```
