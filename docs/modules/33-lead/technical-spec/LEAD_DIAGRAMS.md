# Module Lead - Diagrams

> **Nguồn:** `/docs/feature/FEATURE_SPECIFICATION.md` Section 3 - Quản lý Lead
> **Lưu ý:** Diagrams dựa trên đặc tả YÊU CẦU, không dựa trên code hiện tại

---

## 1. ERD - Entity Relationship Diagram

```mermaid
erDiagram
    LEAD ||--o{ LICH_SU_TU_VAN : has
    LEAD ||--o{ TAI_LIEU : has
    LEAD ||--o{ BINH_LUAN_HOAT_DONG : has
    LEAD ||--o{ LICH_SU_GIAO_DICH : has
    LEAD ||--o{ HANG_HOA_DA_MUA : has
    LEAD }o--o{ TAG : has
    LEAD }o--|| NHAN_VIEN : assigned_to
    LEAD }o--|| NGUOI_TAO : created_by
    LEAD }o--|| NGUON_LEAD : from
    LEAD }o--|| CHI_NHANH : belongs_to
    LEAD }o--|| BANG_GIA : uses
    LEAD }o--|| SALE : managed_by
    LEAD }o--|| DIA_CHI : located_in

    LEAD {
        string ma_khach_hang PK "auto"
        string ten
        string dt
        string email
        string gioi_tinh
        date ngay_sinh
        string trang_thai
        datetime ngay_nhan
        datetime thoi_gian_tao
        datetime lien_he_lan_cuoi
        int tong_so_tuong_tac
    }

    LICH_SU_TU_VAN {
        int id PK
        int lead_id FK
        int san_pham_id FK
        int nhan_vien_id FK
        datetime ngay_tu_van
        text noi_dung
    }

    TAI_LIEU {
        int id PK
        int lead_id FK
        string ten_tai_lieu
        string file_path
    }

    BINH_LUAN_HOAT_DONG {
        int id PK
        int lead_id FK
        string loai "gọi/sms/email/FB/Zalo"
        text noi_dung
        datetime thoi_gian
    }

    TAG {
        int id PK
        string ten
        string mau
    }
```

---

## 2. Workflow - Tạo và quản lý Lead

```mermaid
flowchart TD
    A[Bắt đầu] --> B[Tạo Lead mới]
    B --> C[Nhập thông tin cơ bản]
    C --> D[Nhập thông tin nâng cao]
    D --> E{Admin phân công?}
    E -->|Có| F[Gán NV phụ trách]
    E -->|Chưa| G[Để trống NV]
    F --> H[Lưu Lead]
    G --> H
    H --> I[Hiển thị trong Danh sách]
```

---

## 3. Workflow - Xem và cập nhật Lead

```mermaid
flowchart TD
    A[Chọn Lead từ danh sách] --> B[Xem chi tiết Lead]
    B --> C{Chọn action}
    C -->|Xem| D[Thông tin cơ bản]
    C -->|Xem| E[Lịch sử giao dịch]
    C -->|Xem| F[Hàng hóa đã mua]
    C -->|Xem| G[Tài liệu đi kèm]
    C -->|Xem| H[Bình luận hoạt động]
    C -->|Xem| I[Lịch sử tư vấn]
    C -->|Cập nhật| J[Cập nhật thông tin cơ bản]
    C -->|Cập nhật| K[Cập nhật tài liệu]
    C -->|Cập nhật| L[Cập nhật người phụ trách]
    C -->|Tạo đơn| M[Tạo đơn hàng]
    M --> N[Lead tự động chuyển thành Khách hàng]
```

---

## 4. Workflow - Lịch sử tư vấn

```mermaid
sequenceDiagram
    participant NV as Nhân viên
    participant Lead as Lead
    participant TuVan as Lịch sử tư vấn

    NV->>Lead: Mở chi tiết Lead
    NV->>TuVan: Thêm tư vấn mới
    Note over TuVan: Chọn sản phẩm đã tư vấn<br/>Nhập nội dung tư vấn<br/>Ghi nhận ngày tháng
    TuVan->>Lead: Lưu lịch sử
    Lead->>NV: Hiển thị danh sách tư vấn
```

---

## 5. Workflow - Tài liệu đi kèm

```mermaid
flowchart LR
    A[Chi tiết Lead] --> B{Tài liệu}
    B -->|Thêm| C[Upload file mới]
    B -->|Xem| D[Xem danh sách tài liệu]
    B -->|Xóa| E[Xóa tài liệu]
    C --> F[Lưu tài liệu]
    E --> F
```

---

## 6. Workflow - Bình luận hoạt động

```mermaid
flowchart TD
    A[Chi tiết Lead] --> B[Thêm bình luận]
    B --> C{Chọn loại hoạt động}
    C -->|Gọi| D[Ghi nhận cuộc gọi]
    C -->|SMS| E[Ghi nhận tin nhắn]
    C -->|Email| F[Ghi nhận email]
    C -->|Facebook| G[Ghi nhận tương tác FB]
    C -->|Zalo| H[Ghi nhận tương tác Zalo]
    D --> I[Nhập nội dung]
    E --> I
    F --> I
    G --> I
    H --> I
    I --> J[Lưu bình luận]
```

---

## 7. Danh sách Lead - UI Layout

```mermaid
flowchart LR
    subgraph "Danh sách Lead"
        A[Bộ lọc] --> B[Bảng dữ liệu]
        B --> C[Các cột hiển thị]
        C --> D[Mã KH / Tên / ĐT / Email]
        C --> E[Trạng thái / Tags]
        C --> F[Thời gian / Liên hệ / Tương tác]
        C --> G[Người tạo / Nguồn / Chi nhánh]
        C --> H[Địa chỉ / Giới tính]
    end

    subgraph "Tính năng"
        I[Ẩn/hiện cột]
        J[Cập nhật tags]
        K[Chuyển trạng thái]
    end
```

---

## 8. Filter - Bộ lọc

```mermaid
flowchart TD
    A[Bộ lọc] --> B[Tìm kiếm: Tên, Email]
    A --> C[Filter]
    C --> D[Trạng thái]
    C --> E[Trạng thái phụ trách<br/>có/chưa NV]
    C --> F[Thời gian tạo]
    C --> G[Chi nhánh]
    C --> H[NV phụ trách]
    C --> I[Người tạo]
    C --> J[Độ tuổi]
    C --> K[Tags]
```

---

## 9. Form tạo Lead - Sections

```mermaid
flowchart TD
    A[Form tạo Lead] --> B[Thông tin cơ bản]
    A --> C[Thông tin nâng cao]

    B --> D[Mã auto]
    B --> E[Ngày nhận]
    B --> F[Tên]
    B --> G[Giới tính]
    B --> H[ĐT]
    B --> I[Email]
    B --> J[Ngày sinh]
    B --> K[Nhân viên phụ trách]

    C --> L[Trạng thái]
    C --> M[Tags]
    C --> N[Nguồn]
    C --> O[Chi nhánh]
    C --> P[Địa chỉ<br/>Tỉnh/Quận/Phường]
    C --> Q[Bảng giá]
    C --> R[Sale chăm sóc]
```

---

## 10. Chi tiết Lead - Tabs

```mermaid
flowchart LR
    A[Chi tiết Lead] --> B[Tab: Thông tin cơ bản]
    A --> C[Tab: Lịch sử giao dịch]
    A --> D[Tab: Hàng hóa đã mua]
    A --> E[Tab: Tài liệu đi kèm]
    A --> F[Tab: Bình luận hoạt động]
    A --> G[Tab: Lịch sử tư vấn]

    G --> H[Sản phẩm đã tư vấn]
    G --> I[Nhân viên tư vấn]
    G --> J[Ngày tháng tư vấn]
    G --> K[Nội dung tư vấn]

    F --> L[Gọi / SMS / Email / FB / Zalo]
```

---

## 11. Workflow - Import danh sách Lead

```mermaid
flowchart TD
    A[Chọn Import Lead] --> B[Upload file Excel]
    B --> C[Validate file]
    C --> D{File hợp lệ?}
    D -->|Không| E[Báo lỗi định dạng]
    E --> B
    D -->|Có| F[Parse dữ liệu]
    F --> G[Check trùng SĐT/Email]
    G --> H[Preview kết quả]
    H --> I{User xác nhận?}
    I -->|Không| J[Hủy import]
    I -->|Có| K[Tạo Lead mới]
    K --> L[Báo cáo kết quả]
    L --> M[Thành công / Lỗi / Trùng]
```

---

## 12. Workflow - Export danh sách Lead

```mermaid
flowchart TD
    A[Truy cập Danh sách Lead] --> B{Áp dụng Filter?}
    B -->|Có| C[Chọn điều kiện filter]
    B -->|Không| D[Lấy tất cả Lead]
    C --> D
    D --> E{Quyền hạn}
    E -->|Admin| F[Tất cả Lead theo filter]
    E -->|Nhân viên| G[Lead được phân công]
    F --> H[Chọn Export Lead]
    G --> H
    H --> I[Xuất file Excel]
    I --> J[Tải file về máy]
```

---

## 13. Workflow - Tự động tạo Lead từ nhanh_vn

```mermaid
sequenceDiagram
    participant NH as nhanh_vn
    participant SYS as System
    participant DB as Database

    NH->>SYS: Webhook/API call (khách hàng mới)
    SYS->>SYS: Parse dữ liệu
    SYS->>DB: Check trùng (SĐT/Email)
    alt Không trùng
        SYS->>DB: Tạo Lead mới
        SYS->>DB: Gán nguồn (FB/Zalo/Website...)
        SYS->>NH: Response: Created
    else Trùng
        SYS->>DB: Cập nhật thông tin (nếu cần)
        SYS->>DB: Ghi log
        SYS->>NH: Response: Duplicated
    end
```

---

## 14. Workflow - Expose API tạo khách hàng

```mermaid
sequenceDiagram
    participant EXT as External System
    participant API as API Gateway
    participant SYS as System
    participant DB as Database

    EXT->>API: POST /api/leads
    API->>API: Validate API Key/Token
    alt Token không hợp lệ
        API->>EXT: 401 Unauthorized
    else Token hợp lệ
        API->>SYS: Forward request
        SYS->>SYS: Validate dữ liệu
        alt Dữ liệu không hợp lệ
            SYS->>EXT: 400 Bad Request
        else Dữ liệu hợp lệ
            SYS->>DB: Check trùng
            alt Trùng
                SYS->>EXT: 409 Conflict
            else Không trùng
                SYS->>DB: Tạo Lead mới
                SYS->>EXT: 201 Created (lead_id)
            end
        end
    end
```

---

## 15. Workflow - Check trùng thông tin

```mermaid
flowchart TD
    A[Nhận dữ liệu Lead mới] --> B{Có SĐT?}
    B -->|Có| C[Tìm Lead có SĐT giống]
    B -->|Không| D{Có Email?}
    C --> E{Tìm thấy?}
    E -->|Có| F[Cảnh báo trùng]
    E -->|Không| D
    D -->|Có| G[Tìm Lead có Email giống]
    D -->|Không| H[Không trùng - Tiếp tục]
    G --> I{Tìm thấy?}
    I -->|Có| F
    I -->|Không| H
    F --> J{User quyết định}
    J -->|Bỏ qua| K[Hủy tạo Lead]
    J -->|Cập nhật| L[Cập nhật Lead hiện có]
    J -->|Tạo mới| M[Tạo Lead mới dù trùng]
```

---

## 16. Tổng hợp chức năng Module Lead

```mermaid
mindmap
  root((Module Lead))
    Quản lý cơ bản
      Tạo Lead mới
      Xem danh sách Lead
      Xem chi tiết Lead
      Cập nhật Lead
      Xóa Lead
    Tính năng nhanh
      Cập nhật Tags tại DS
      Chuyển trạng thái tại DS
      Ẩn/hiện cột
    Lịch sử & Tài liệu
      Lịch sử tư vấn
      Tài liệu đi kèm
      Bình luận hoạt động
    Chuyển đổi
      Tạo đơn hàng
      Lead → Customer
    Import/Export
      Import từ Excel
      Export ra Excel
      Check trùng
    Tích hợp
      Auto từ nhanh_vn
      Expose API
```

---

**Nguồn:** `/docs/feature/FEATURE_SPECIFICATION.md` Section 3 - Quản lý Lead
**Ngày cập nhật:** 2026-01-06
**Trạng thái:** Đặc tả YÊU CẦU - Code phải implement theo diagrams này
