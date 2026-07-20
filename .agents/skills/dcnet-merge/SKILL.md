---
name: dcnet-merge
description: |
  Review, merge PR vào develop, và tổng hợp chức năng đã merge.

  Dùng khi:
  - User nói "/dcnet-merge" hoặc "/dcnet-merge 24 31"
  - User muốn review và merge PR vào develop
  - User nói "merge PR", "gộp PR", "review và merge"
  - User muốn tổng hợp chức năng đã merge

  Triggers: "dcnet-merge", "merge PR", "gộp PR", "review và merge",
  "merge vào develop", "merge tất cả PR"
allowed-tools: Bash, Read, Glob, Grep, Agent
---

# /dcnet-merge — Review, Merge & Tổng hợp PR

> Review PR, merge vào develop, rồi tổng hợp chức năng đã merge.

## Cách dùng

```
/dcnet-merge                  # Review & merge tất cả PR đang mở hướng develop
/dcnet-merge 24 31            # Review & merge các PR cụ thể
/dcnet-merge --list            # Chỉ liệt kê PR đang mở (không merge)
```

## Quy trình

### Bước 1: Xác định PR

Nếu user cung cấp số PR, dùng số đó. Nếu không, liệt kê tất cả PR đang mở hướng `develop`:

```bash
gh pr list --base develop --state open --json number,title,author,headRefName,additions,deletions,changedFiles
```

Nếu có flag `--list`, chỉ hiển thị danh sách rồi DỪNG.

### Bước 2: Review từng PR

Với MỖI PR, chạy các lệnh sau:

```bash
# Lấy thông tin PR
gh pr view {number} --json title,body,state,author,baseRefName,headRefName,files,additions,deletions,changedFiles

# Lấy toàn bộ diff
gh pr diff {number}

# Kiểm tra CI
gh pr checks {number}
```

Thực hiện code review tập trung vào:
- Vấn đề bảo mật (SQL injection, XSS, v.v.)
- Anti-pattern ERPNext (xem dcnet_quality skills)
- Lỗi logic và bug
- Thay đổi ngoài phạm vi mô tả PR
- Khả năng xung đột khi merge

Kết quả review ngắn gọn cho mỗi PR:
- Phát hiện chính (chỉ critical/high)
- Kết luận: merge hoặc yêu cầu sửa

### Bước 3: Hỏi xác nhận từ user

Sau khi review TẤT CẢ PR, trình bày bảng tóm tắt và **HỎI user xác nhận trước khi merge**:

```
## Kết quả review

| PR | Tiêu đề | Kết luận | Vấn đề |
|----|---------|----------|--------|
| #X | ... | Sẵn sàng merge | — |
| #Y | ... | Chặn | 2 vấn đề nghiêm trọng |

Merge PR #X vào develop? (Y/n)
```

**QUAN TRỌNG:** KHÔNG merge bất cứ gì cho đến khi user xác nhận rõ ràng.
- Nếu user nói "ok", "y", "merge", "được" → tiến hành merge
- Nếu user nói "không", "skip", "bỏ qua" → bỏ qua PR đó
- User có thể chọn lọc: "merge #X nhưng skip #Y"

### Bước 4: Merge (chỉ sau khi user xác nhận)

Với mỗi PR được user duyệt:

```bash
gh pr merge {number} --merge
```

Nếu merge thất bại do conflict:
1. Checkout nhánh PR
2. Merge `origin/develop` vào nhánh đó
3. Giải quyết conflict
4. Commit và push
5. Merge PR

Sau khi merge TẤT CẢ, cập nhật local develop:

```bash
git checkout develop && git pull origin develop
```

Dọn dẹp các nhánh feature local đã checkout trong quá trình giải quyết conflict.

### Bước 5: Xuất bảng tổng hợp chức năng

Sau khi tất cả PR được duyệt đã merge, xuất **bảng tổng hợp chức năng** theo đúng template sau.
Chỉ bao gồm PR đã merge thành công, KHÔNG bao gồm PR bị bỏ qua:

---

## Chức năng mới từ PR #X + PR #Y [+ PR #Z ...]

### PR #X — {tiêu đề} ({tác giả})

| # | Chức năng | Loại | Files chính |
|---|-----------|------|-------------|
| 1 | **{mô tả chức năng}** | {loại} | `{files chính}` |
| 2 | **{mô tả chức năng}** | {loại} | `{files chính}` |

### PR #Y — {tiêu đề} ({tác giả})

| # | Chức năng | Loại | Files chính |
|---|-----------|------|-------------|
| {n} | **{mô tả chức năng}** | {loại} | `{files chính}` |

---

### Tóm tắt: {tổng số} chức năng, chia {N} nhóm

- **{Nhóm 1} ({số lượng}):** {danh sách ngắn}
- **{Nhóm 2} ({số lượng}):** {danh sách ngắn}
- **{Nhóm 3} ({số lượng}):** {danh sách ngắn}

---

## Quy tắc template

### Bảng chức năng

- Đánh số chức năng liên tục qua TẤT CẢ PR (1, 2, 3... liên tục)
- **Chức năng**: In đậm, mô tả ngắn gọn bằng tiếng Việt
- **Loại**: Một trong: `Custom Field`, `Client JS + API`, `Scheduled Task`, `Script Report`, `Module`, `Utility`, `Update`, `Cleanup`, `Config`, `Fix`, `DocType`, `Workflow`, `Print Format`
- **Files chính**: File quan trọng (đường dẫn tương đối, backtick), tối đa 2-3 file mỗi chức năng

### Nhóm tóm tắt

- Nhóm chức năng theo lĩnh vực (VD: "Kho hàng", "Dashboard", "CRM", "Hạ tầng")
- Kèm số lượng mỗi nhóm
- Danh sách ngắn, phân cách bằng dấu phẩy

### Quy tắc đếm

- Mỗi chức năng riêng biệt hướng người dùng hoặc tiện ích dev = 1 mục
- Một report có filter + chart = 1 chức năng (không phải 3)
- Một cron job = 1 chức năng
- Một module tiện ích (như notification_helper) = 1 chức năng
- Bản dịch/label đi kèm một chức năng = phần của chức năng đó, KHÔNG tách riêng
- Custom field cho một form = 1 chức năng (không tính theo từng field)

## Xử lý lỗi

- Nếu PR có vấn đề nghiêm trọng CHẶN merge, liệt kê vấn đề và bỏ qua. Tiếp tục với các PR khác.
- Nếu TẤT CẢ PR bị chặn, xuất kết quả review và dừng (không có bảng tổng hợp).
- Nếu một số PR merge được, một số không, xuất bảng tổng hợp cho PR đã merge, sau đó liệt kê riêng các PR bị chặn.
