# Fitting Module - Tổng hợp Diagrams

> **Mục đích:** Tổng hợp tất cả Mermaid diagrams để dễ review
> **Phiên bản:** 1.0
> **Ngày cập nhật:** 06/01/2026
> 
> **Preview online:** Paste vào https://mermaid.live hoặc VS Code extension "Mermaid Preview"

---

## 📌 Nguồn tài liệu

| Tài liệu | Section | Nội dung |
| --- | --- | --- |
| FEATURE_SPECIFICATION.md | 5.2.2 | Tạo đơn hàng Fitting, Thông tin kỹ thuật |
| FEATURE_SPECIFICATION.md | 5.4 | Xem chi tiết đơn Fitting, Dịch vụ phát sinh |
| FEATURE_SPECIFICATION.md | 14.2 | Báo cáo Fitting |

**Tài liệu liên quan:**
- [FITTING_USE_CASE_SPEC.md](./FITTING_USE_CASE_SPEC.md) - Chi tiết Use Cases
- [FITTING_WORKFLOW.md](./FITTING_WORKFLOW.md) - Workflow & ERD

---

## 1. Workflow tổng quan

```mermaid
flowchart TD
    A[Khách đăng ký Fitting] --> B{Nguồn đăng ký}
    B -->|Website| C[API đẩy vào CRM]
    B -->|Tại cửa hàng| D[NV tạo đơn trực tiếp]
    B -->|Điện thoại| D

    C --> E[Tạo Đơn Fitting]
    D --> E

    E --> F[Xác nhận lịch hẹn]
    F --> G[Thực hiện Fitting]
    G --> H[Nhập thông số kỹ thuật]
    H --> I{Khách mua hàng?}

    I -->|Có| J[Tạo Đơn hàng SP]
    I -->|Chưa| K[Lưu hồ sơ, follow-up sau]

    J --> L[Hoàn thành]
    K --> L
```

---

## 2. State Machine - Trạng thái đơn Fitting

```mermaid
stateDiagram-v2
    [*] --> NEW
    NEW --> CONFIRMED: Xác nhận lịch
    NEW --> CANCELLED: Khách hủy

    CONFIRMED --> IN_PROGRESS: Khách đến
    CONFIRMED --> NO_SHOW: Khách không đến
    CONFIRMED --> CANCELLED: Khách hủy

    NO_SHOW --> CONFIRMED: Đặt lại lịch
    NO_SHOW --> CANCELLED: Không liên lạc được

    IN_PROGRESS --> COMPLETED: Nhập xong thông số

    COMPLETED --> WITH_ORDER: Tạo đơn SP
    COMPLETED --> FOLLOW_UP: Khách chưa mua

    FOLLOW_UP --> WITH_ORDER: Khách quay lại mua

    WITH_ORDER --> [*]
    CANCELLED --> [*]

    NEW: Mới
    CONFIRMED: Đã xác nhận
    IN_PROGRESS: Đang fitting
    NO_SHOW: Vắng mặt
    COMPLETED: Hoàn thành
    WITH_ORDER: Có đơn hàng
    FOLLOW_UP: Chờ follow-up
    CANCELLED: Hủy
```

---

## 3. ERD - Entity Relationship Diagram

```mermaid
erDiagram
    FITTING_ORDER ||--o{ FITTING_SERVICE : has
    FITTING_ORDER ||--|| CUSTOMER : belongs_to
    FITTING_ORDER ||--o| EMPLOYEE : assigned_to
    FITTING_ORDER ||--o| SALES_ORDER : generates
    FITTING_ORDER ||--|| FITTING_SPECS : has
    FITTING_SERVICE ||--|| PRODUCT : uses

    FITTING_ORDER {
        int id PK
        string code
        int customer_id FK
        int employee_id FK
        datetime scheduled_at
        datetime completed_at
        string status
        string source
        int branch_id FK
        decimal service_fee
        text notes
        timestamps created_updated
    }

    FITTING_SPECS {
        int id PK
        int fitting_order_id FK
        decimal height_cm
        decimal weight_kg
        string glove_size
        string player_level
        decimal club_head_speed
        decimal ball_speed
        string swing_shape
        string ball_flight
        string ball_height
        decimal iron_distance
        decimal driver_distance
        text current_clubs
        text customer_needs
        text upgrade_recommendations
        timestamps created_updated
    }

    FITTING_SERVICE {
        int id PK
        int fitting_order_id FK
        int product_id FK
        string service_type
        int quantity
        decimal unit_price
        decimal total_price
        text specs_note
        timestamps created_updated
    }
```

---

## 4. Sequence Diagram - Tạo đơn Fitting

```mermaid
sequenceDiagram
    actor KH as Khách hàng
    participant WEB as Website NM
    participant CRM as CRM
    participant NV as Nhân viên

    alt Đăng ký qua Website hiện tại
        KH->>WEB: Chọn Ngày + Giờ hẹn
        WEB->>WEB: Lưu booking
        Note over WEB,CRM: ❓ Cần API/Webhook sync
        WEB-->>CRM: Sync đơn fitting mới
        CRM->>NV: Thông báo đơn mới
        NV->>KH: Gọi xác nhận + lấy thêm thông tin
    else Đăng ký tại cửa hàng/ĐT
        KH->>NV: Yêu cầu fitting
        NV->>CRM: Tạo đơn fitting
        NV->>KH: Xác nhận lịch ngay
    end
```

---

## 5. Sequence Diagram - Thực hiện Fitting

```mermaid
sequenceDiagram
    actor KH as Khách hàng
    participant NV as NV Fitting
    participant CRM as CRM
    participant KHO as Kho

    KH->>NV: Đến theo lịch hẹn
    NV->>CRM: Cập nhật: Đang fitting

    NV->>NV: Đo các thông số kỹ thuật
    NV->>CRM: Nhập thông số vào hệ thống

    NV->>KH: Tư vấn gậy phù hợp

    alt Khách đồng ý mua
        NV->>CRM: Tạo dịch vụ phát sinh
        NV->>KHO: Check tồn kho grip/shaft
        NV->>CRM: Tạo đơn hàng SP
        CRM->>CRM: Link đơn SP với đơn Fitting
    else Khách chưa quyết định
        NV->>CRM: Cập nhật: Chờ follow-up
        CRM->>NV: Tạo task nhắc follow-up
    end
```

---

## 6. Flowchart - Dịch vụ phát sinh

```mermaid
flowchart LR
    A[Kết quả Fitting] --> B{Dịch vụ phát sinh}

    B --> C[Mua grip mới]
    B --> D[Lắp shaft]
    B --> E[Đặt gậy theo thông số]
    B --> F[Combo fitting + gậy]

    C --> G[Tạo line item]
    D --> G
    E --> G
    F --> G

    G --> H[Tính giá]
    H --> I[Thêm vào đơn hàng]
```

## Quick Preview Commands

```bash
# VS Code với extension "Markdown Preview Mermaid Support"
# Hoặc paste từng block vào https://mermaid.live

# Export SVG/PNG từ CLI (cần cài mermaid-cli)
npx @mermaid-js/mermaid-cli mmdc -i FITTING_DIAGRAMS.md -o fitting-diagrams.svg
```

---

---

## 📚 Tham khảo

- [FEATURE_SPECIFICATION.md](./../../feature/FEATURE_SPECIFICATION.md) - Đặc tả chức năng gốc
- [FITTING_USE_CASE_SPEC.md](./FITTING_USE_CASE_SPEC.md) - Use Cases
- [FITTING_WORKFLOW.md](./FITTING_WORKFLOW.md) - Workflow & ERD

---

*Cập nhật: 06/01/2026*
