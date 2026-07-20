# Module Credit Management - Use Cases

> **Phiên bản**: v1.0
> **Ngày cập nhật**: 2026-01-14
> **Nguồn**: ERP_SPECIFICATION.md Section 2.6-2.8

---

## 📋 Danh sách Use Cases

| ID | Use Case | Actor | Priority |
|----|----------|-------|----------|
| UC-CM-001 | Cập nhật hạn mức công nợ khách hàng | Manager | High |
| UC-CM-002 | Tạo lệnh xuất hàng với credit check | NVKD | Critical |
| UC-CM-003 | Phê duyệt ngoại lệ vượt hạn mức | Kế toán trưởng | Critical |
| UC-CM-004 | Xem thông tin tín dụng khách hàng | NVKD | High |
| UC-CM-005 | Theo dõi công nợ quá hạn | Kế toán | High |
| UC-CM-006 | Xem báo cáo Aging | Manager | Medium |
| UC-CM-007 | Cảnh báo hóa đơn sắp quá hạn | System | Medium |

---

## UC-CM-001: Cập nhật hạn mức công nợ khách hàng

**Nguồn:** ERP_SPECIFICATION.md line 137-150

### Mô tả
Manager cập nhật hạn mức tín dụng cho khách hàng đại lý.

### Actor
- **Primary:** Manager, Kinh doanh
- **Secondary:** System

### Preconditions
- User đã đăng nhập với quyền Manager
- Khách hàng đã tồn tại trong hệ thống

### Main Flow
1. User vào menu "Hạn mức công nợ"
2. System hiển thị danh sách khách hàng và hạn mức hiện tại
3. User click "Tạo mới" hoặc "Chỉnh sửa"
4. System hiển thị form:
   - Ngày áp dụng
   - Tài khoản công nợ
   - Mã khách hàng (select)
   - Tên khách hàng (auto-fill)
   - Giá trị hạn mức (VND)
   - File đính kèm (optional)
5. User nhập thông tin và click "Lưu"
6. System validate:
   - Giá trị hạn mức > 0
   - Ngày áp dụng hợp lệ
7. System lưu vào database
8. System hiển thị thông báo "Cập nhật thành công"

### Postconditions
- Hạn mức mới được áp dụng từ ngày chỉ định
- Tất cả lệnh xuất mới sẽ dùng hạn mức này để check

### Business Rules
- BR-001: Một khách hàng chỉ có 1 hạn mức active tại một thời điểm
- BR-002: Hạn mức mới có thể override hạn mức cũ (theo ngày áp dụng)

---

## UC-CM-002: Tạo lệnh xuất hàng với credit check

**Nguồn:** ERP_SPECIFICATION.md line 110-134, 152-162

### Mô tả
NVKD tạo lệnh xuất hàng, hệ thống tự động kiểm tra tín dụng khách hàng.

### Actor
- **Primary:** NVKD
- **Secondary:** System, Kế toán trưởng (nếu cần override)

### Preconditions
- User đã đăng nhập với quyền NVKD
- Khách hàng có hạn mức công nợ
- Đơn hàng bán đã được tạo

### Main Flow
1. User vào "Đơn hàng bán" → Click "Tạo lệnh xuất"
2. System hiển thị form "Lệnh xuất hàng" với:
   - Thông tin khách hàng (auto-fill từ đơn hàng)
   - Danh sách mặt hàng (auto-fill từ đơn hàng)
   - Panel "Thông tin tín dụng" bên phải
3. System auto-load credit info:
   - Hạn mức
   - Công nợ hiện tại
   - Lệnh xuất chưa xuất
   - Available credit
4. User nhập/chỉnh sửa thông tin cần thiết
5. User click "Lưu"
6. System thực hiện **Credit Check**:

   **Check 1: Hóa đơn quá hạn**
   ```sql
   SELECT COUNT(*) FROM invoice
   WHERE customer_id = ?
   AND due_date < CURRENT_DATE
   AND outstanding_amount > 0
   ```

   **Check 2: Hạn mức**
   ```python
   total_exposure = current_debt + pending_orders + current_order_value
   if total_exposure > credit_limit:
       fail()
   ```

7. **IF Pass:** Status → `approved`, hiển thị "✅ Đã duyệt, sẵn sàng xuất hàng"
8. **IF Fail:** Status → `pending_override`, hiển thị cảnh báo + gửi email Kế toán trưởng

### Alternative Flow: Pass Credit Check
**7a.** System chuyển status → `approved`
**7b.** System hiển thị "✅ Lệnh xuất đã được duyệt"
**7c.** System reserve credit (giữ hạn mức)
**7d.** Lệnh xuất sẵn sàng cho kho xuất hàng

### Alternative Flow: Fail Credit Check
**7a.** System chuyển status → `pending_override`
**7b.** System hiển thị popup cảnh báo:
```
⚠️ KHÔNG ĐỦ ĐIỀU KIỆN XUẤT HÀNG

Lý do:
❌ Vượt hạn mức 30,000,000 VND

Chi tiết:
- Hạn mức: 500,000,000 VND
- Công nợ hiện tại: 350,000,000 VND
- Lệnh xuất chưa xuất: 100,000,000 VND
- Đơn hiện tại: 80,000,000 VND
─────────────────────────────────
Tổng rủi ro: 530,000,000 VND

Lệnh xuất đã được gửi đến Kế toán trưởng phê duyệt.
```
**7c.** System gửi email notification đến Kế toán trưởng
**7d.** Lệnh xuất chờ phê duyệt

### Postconditions
- Lệnh xuất được tạo với status phù hợp
- Nếu approved: Credit được reserve
- Nếu pending: Email gửi đến approver

### Business Rules
- BR-003: 2 điều kiện bắt buộc (no overdue + within limit)
- BR-004: Công nợ dự kiến = SUM(approved orders not shipped)
- BR-005: Hiển thị chi tiết credit info khi check fail

---

## UC-CM-003: Phê duyệt ngoại lệ vượt hạn mức

**Nguồn:** ERP_SPECIFICATION.md line 158-162

### Mô tả
Kế toán trưởng xem xét và phê duyệt/từ chối lệnh xuất hàng vượt hạn mức hoặc có nợ quá hạn.

### Actor
- **Primary:** Kế toán trưởng
- **Secondary:** System, NVKD (nhận notification)

### Preconditions
- User đã đăng nhập với quyền Kế toán trưởng
- Có lệnh xuất ở status = `pending_override`

### Main Flow
1. **Trigger:** Kế toán trưởng nhận email "Cần phê duyệt lệnh xuất #SO-2026"
2. User click link trong email hoặc vào "Lệnh xuất chờ duyệt"
3. System hiển thị danh sách lệnh xuất `pending_override`
4. User click vào lệnh xuất cần xem xét
5. System hiển thị popup "Override Approval" với:
   - Thông tin khách hàng
   - Lý do chặn (overdue / exceed limit)
   - Chi tiết tín dụng
   - Textarea "Lý do phê duyệt" (required)
   - Button [Phê duyệt] [Từ chối]
6. User đọc thông tin, nhập lý do
7. User click "Phê duyệt" hoặc "Từ chối"
8. **IF Phê duyệt:**
   - System chuyển status → `approved`
   - System log: approver, reason, timestamp
   - System reserve credit
   - System gửi notification đến NVKD "✅ Lệnh xuất đã được duyệt"
9. **IF Từ chối:**
   - System chuyển status → `rejected`
   - System log: approver, reason, timestamp
   - System gửi notification đến NVKD "❌ Lệnh xuất bị từ chối: [reason]"

### Postconditions
- Lệnh xuất có decision (approved/rejected)
- Audit log ghi đầy đủ thông tin override
- NVKD nhận notification

### Business Rules
- BR-006: Chỉ Kế toán trưởng mới có quyền override
- BR-007: Bắt buộc nhập lý do override (audit trail)
- BR-008: Một lệnh xuất chỉ được override 1 lần

---

## UC-CM-004: Xem thông tin tín dụng khách hàng

### Mô tả
NVKD xem thông tin tín dụng của khách hàng trước khi tạo đơn hàng.

### Actor
- **Primary:** NVKD
- **Secondary:** System

### Preconditions
- User đã đăng nhập
- Khách hàng có trong hệ thống

### Main Flow
1. User vào "Khách hàng" → Chọn khách hàng → Tab "Tín dụng"
2. System hiển thị:

```
┌──────────────────────────────────────────┐
│ 💳 THÔNG TIN TÍN DỤNG                   │
├──────────────────────────────────────────┤
│ Hạn mức:              500,000,000 VND    │
│ Công nợ hiện tại:     350,000,000 VND    │
│ Lệnh xuất chưa xuất:  100,000,000 VND    │
│ ────────────────────────────────────────│
│ Tổng rủi ro:          450,000,000 VND    │
│ Tín dụng khả dụng:     50,000,000 VND    │
│ Tỷ lệ sử dụng:         90% 🔴           │
├──────────────────────────────────────────┤
│ HÓA ĐƠN QUÁ HẠN                         │
│ - #INV-001: 20 triệu (quá hạn 15 ngày) │
│ - #INV-005: 10 triệu (quá hạn 5 ngày)  │
│ ────────────────────────────────────────│
│ Tổng nợ quá hạn: 30,000,000 VND ⚠️     │
└──────────────────────────────────────────┘
```

3. User xem thông tin để đánh giá có nên nhận đơn hàng mới không

### Postconditions
- User có thông tin để ra quyết định

### Business Rules
- BR-009: NVKD chỉ xem được credit info của KH được assign

---

## UC-CM-005: Theo dõi công nợ quá hạn

### Mô tả
Kế toán theo dõi danh sách khách hàng có hóa đơn quá hạn.

### Actor
- **Primary:** Kế toán
- **Secondary:** System

### Main Flow
1. User vào "Công nợ" → "Công nợ quá hạn"
2. System hiển thị danh sách:
   - Mã KH
   - Tên KH
   - Số hóa đơn quá hạn
   - Tổng giá trị quá hạn
   - Số ngày quá hạn trung bình
   - Hành động (View detail, Send reminder)
3. User filter theo:
   - Độ tuổi nợ (0-30, 31-60, 61-90, 90+)
   - Nhóm khách hàng
   - NVKD phụ trách
4. User click "View detail" → Xem chi tiết từng hóa đơn quá hạn

### Postconditions
- User có danh sách KH cần đôn đốc thanh toán

---

## UC-CM-006: Xem báo cáo Aging

### Mô tả
Manager xem báo cáo công nợ theo độ tuổi (Aging Report).

### Actor
- **Primary:** Manager, Kế toán
- **Secondary:** System

### Main Flow
1. User vào "Báo cáo" → "Công nợ Aging"
2. System yêu cầu chọn:
   - Ngày báo cáo (default: hôm nay)
   - Nhóm khách hàng (optional)
3. User click "Xem báo cáo"
4. System generate báo cáo:

| Mã KH | Tên KH | 0-30 | 31-60 | 61-90 | 90+ | Tổng |
|-------|--------|------|-------|-------|-----|------|
| KH-001 | Đại lý A | 100 | 50 | 20 | 10 | 180 |
| KH-002 | Đại lý B | 200 | 0 | 0 | 0 | 200 |
| ... | ... | ... | ... | ... | ... | ... |
| **TỔNG** | | **500** | **150** | **50** | **30** | **730** |

5. User export Excel nếu cần

### Postconditions
- User có insight về chất lượng công nợ

### Business Rules
- BR-010: Aging tính từ `due_date`, không phải `invoice_date`

---

## UC-CM-007: Cảnh báo hóa đơn sắp quá hạn

### Mô tả
Hệ thống tự động gửi cảnh báo cho NVKD khi hóa đơn của KH sắp đến hạn thanh toán.

### Actor
- **Primary:** System
- **Secondary:** NVKD

### Trigger
- Cron job chạy hàng ngày lúc 9:00 AM
- Kiểm tra hóa đơn có `due_date` trong 3 ngày tới

### Main Flow
1. System query:
```sql
SELECT * FROM invoice
WHERE DATEDIFF(due_date, CURRENT_DATE) <= 3
AND outstanding_amount > 0
```
2. FOR EACH invoice:
   - Get NVKD phụ trách khách hàng
   - Send in-app notification
   - Send email (optional)
3. NVKD nhận notification:
```
🔔 Hóa đơn #INV-2026-001 của KH Đại lý ABC
sắp đến hạn thanh toán (còn 2 ngày)
Giá trị: 50,000,000 VND
Hạn thanh toán: 16/01/2026
[Xem chi tiết] [Gửi nhắc nhở]
```

### Postconditions
- NVKD biết để đôn đốc KH thanh toán trước hạn

### Business Rules
- BR-011: Chỉ gửi cảnh báo 1 lần (3 ngày trước due date)
- BR-012: Không gửi cảnh báo nếu KH đã thanh toán

---

## 🔐 Permissions Matrix

| Use Case | NVKD | Manager | Kế toán | Kế toán trưởng |
|----------|------|---------|---------|----------------|
| UC-CM-001: Cập nhật hạn mức | ❌ | ✅ | ❌ | ✅ |
| UC-CM-002: Tạo lệnh xuất (credit check) | ✅ | ✅ | ❌ | ✅ |
| UC-CM-003: Phê duyệt override | ❌ | ❌ | ❌ | ✅ |
| UC-CM-004: Xem credit info KH | ✅ (own) | ✅ (all) | ✅ (all) | ✅ (all) |
| UC-CM-005: Theo dõi nợ quá hạn | ✅ (own) | ✅ (all) | ✅ (all) | ✅ (all) |
| UC-CM-006: Báo cáo Aging | ❌ | ✅ | ✅ | ✅ |
| UC-CM-007: Nhận cảnh báo | ✅ (own KH) | ✅ | ✅ | ✅ |

---

## 📊 Use Case Priority

### Critical (Must Have)
- UC-CM-002: Tạo lệnh xuất với credit check
- UC-CM-003: Phê duyệt override

### High (Should Have)
- UC-CM-001: Cập nhật hạn mức
- UC-CM-004: Xem credit info
- UC-CM-005: Theo dõi nợ quá hạn

### Medium (Nice to Have)
- UC-CM-006: Báo cáo Aging
- UC-CM-007: Cảnh báo tự động

---

**© 2025 DCNET Corporation - Powered by DCNET Cloud**
