# Git Flow - DCNET Flow

> Team: Đức, Phương, Đạt, Cường, Hậu

---

## 1. Sơ đồ nhánh

```
main ─────────────────────────────────────────────── (production, bàn giao)
  │
  └── develop ────────────────────────────────────── (tích hợp, test)
        │
        ├── feature/02-dashboard ────── merge → develop
        ├── feature/07-kho-hang ─────── merge → develop
        ├── feature/33-lead ─────────── merge → develop
        └── fix/12-ban-hang-tinh-gia ── merge → develop

  hotfix/sua-loi-login ── từ main ── merge → main + develop
```

### Nguyên tắc

| Nhánh | Tạo từ | Merge vào | Ai merge | Ghi chú |
| --- | --- | --- | --- | --- |
| `main` | - | - | Đức | Chỉ nhận merge từ `develop` qua PR, dùng để deploy bàn giao |
| `develop` | `main` | `main` (PR) | Đức | Nhánh tích hợp, tất cả feature merge vào đây |
| `feature/*` | `develop` | `develop` (PR) | Dev tạo + Đức review | 1-5 ngày, xong là merge |
| `fix/*` | `develop` | `develop` (PR) | Dev tạo | Bug fix nhỏ, không phải hotfix |
| `hotfix/*` | `main` | `main` + `develop` | Đức | Chỉ dùng khi production bị lỗi nghiêm trọng |

---

## 2. Đặt tên nhánh

### Feature branch

```
feature/{STT}-{tên-ngắn}
```

| Ví dụ | Module | Giải thích |
| --- | --- | --- |
| `feature/02-dashboard` | 02-Dashboard | Toàn bộ module dashboard |
| `feature/07-kho-setup` | 07-Kho hàng | Setup warehouse, stock entry |
| `feature/07-kho-barcode` | 07-Kho hàng | Tính năng barcode riêng |
| `feature/33-lead-form` | 33-Lead | Form tạo lead |
| `feature/33-lead-import` | 33-Lead | Import lead từ Excel |
| `feature/14-trade-in` | 14-Trade-in | Toàn bộ trade-in |

**Quy tắc:**
- Bắt đầu bằng `feature/` + STT module
- Tên ngắn gọn, dùng tiếng Anh, phân cách bằng `-`
- 1 feature branch = 1 chức năng cụ thể (không gộp nhiều module)
- Nếu module nhỏ thì 1 branch cho cả module (VD: `feature/02-dashboard`)
- Nếu module lớn thì tách ra (VD: `feature/07-kho-setup` + `feature/07-kho-barcode`)

### Fix branch

```
fix/{STT}-{mô-tả-ngắn}
```

Ví dụ: `fix/12-ban-hang-tinh-gia`, `fix/33-lead-duplicate-check`

### Hotfix branch

```
hotfix/{mô-tả-ngắn}
```

Ví dụ: `hotfix/login-redirect-loop`, `hotfix/migrate-error`

---

## 3. Luồng làm việc hàng ngày

### 3.1. Bắt đầu ngày mới

```bash
# 1. Chuyển sang develop, lấy code mới nhất
git checkout develop
git pull origin develop

# 2. Quay lại feature branch của mình
git checkout feature/02-dashboard

# 3. Rebase develop mới nhất vào feature branch
git rebase develop
```

> **Tại sao rebase?** Giữ history sạch sẽ, tuyến tính. Khi merge vào develop sẽ không tạo merge commit thừa, dễ đọc lịch sử hơn.

**Lưu ý:** Chỉ rebase nhánh feature của chính mình. Không bao giờ rebase `develop` hoặc `main`.

### 3.2. Làm việc trong ngày

```bash
# Code bình thường, commit thường xuyên với từng thay đổi logic
git add dcnet_apps/dcnet_apps/dcnet_dashboard/report/revenue_by_customer_source/revenue_by_customer_source.py
git commit -m "feat(02): add revenue by customer source report"

# Commit tiếp
git add dcnet_apps/dcnet_apps/dcnet_dashboard/report/revenue_by_order_source/
git commit -m "feat(02): add revenue by order source report"
```

**Nguyên tắc commit:**
- Commit thường xuyên, mỗi commit là 1 thay đổi logic hoàn chỉnh
- Dùng `git add <file>` cụ thể, tránh `git add .` hoặc `git add -A` (dễ vô tình thêm file không mong muốn)
- Kiểm tra `git status` và `git diff --staged` trước khi commit

### 3.3. Push code cuối ngày

```bash
# Push feature branch lên remote
git push origin feature/02-dashboard
```

Nếu đã rebase mà push bị reject (do history thay đổi):

```bash
git push origin feature/02-dashboard --force-with-lease
```

> `--force-with-lease` an toàn hơn `--force` vì nó kiểm tra xem có ai khác push vào nhánh này trước mình không. Nếu có, lệnh sẽ bị từ chối thay vì ghi đè.

### 3.4. Khi xong feature — tạo PR

```bash
# Cập nhật develop mới nhất trước khi tạo PR
git checkout develop
git pull origin develop
git checkout feature/02-dashboard
git rebase develop

# Giải quyết conflict nếu có (xem mục 5)

# Push và tạo PR
git push origin feature/02-dashboard --force-with-lease
gh pr create --base develop --title "feat(02): Dashboard module" --body "..."
```

---

## 4. Commit message

### Format

Theo chuẩn [Conventional Commits](https://www.conventionalcommits.org/):

```
{type}({scope}): {mô tả ngắn bằng tiếng Anh}
```

- **type**: loại thay đổi (xem bảng dưới)
- **scope**: STT module hoặc tên component (tùy chọn)
- **mô tả**: viết bằng tiếng Anh, bắt đầu bằng động từ nguyên thể (add, fix, update...), không viết hoa chữ đầu, không chấm cuối

### Type

| Type | Khi nào dùng | Ví dụ |
| --- | --- | --- |
| `feat` | Tính năng mới | `feat(02): add revenue by customer source report` |
| `fix` | Sửa lỗi | `fix(33): resolve lead duplicate validation error` |
| `refactor` | Đổi code nhưng không đổi chức năng | `refactor(07): simplify stock entry validation` |
| `docs` | Thay đổi tài liệu | `docs(02): update dashboard technical spec` |
| `chore` | Config, build, dependencies | `chore: update hooks.py fixtures filter` |
| `test` | Thêm/sửa test | `test(33): add lead import test cases` |
| `style` | Format code (không đổi logic) | `style(07): fix linting errors in stock report` |

### Ví dụ thực tế

```
feat(02): add 3 script reports for dashboard charts
feat(02): create number cards and dashboard chart fixtures
feat(07): setup warehouse hierarchy for multi-branch
fix(12): add missing order_source field to sales invoice
docs(14): update trade-in gap analysis
chore: add DCNET Dashboard to modules.txt
refactor(33): extract lead scoring to separate module
```

### Commit message nên tránh

```
# Quá chung chung
fix: fix bug                    # Bug gì? Ở đâu?
feat: update code               # Update gì?
chore: changes                  # Thay đổi gì?

# Nên viết cụ thể
fix(33): prevent duplicate lead creation on concurrent submit
feat(02): add date range filter to revenue report
chore: add Sales Order to custom field fixtures filter
```

---

## 5. Xử lý conflict

### 5.1. Conflict khi rebase develop

```bash
git checkout feature/02-dashboard
git rebase develop

# Nếu có conflict, Git sẽ báo:
# CONFLICT (content): Merge conflict in dcnet_apps/dcnet_apps/hooks.py
# Automatic merge failed; fix conflicts and then commit the result.
```

**Các bước xử lý:**

```bash
# 1. Xem những file nào bị conflict
git status
# Các file "both modified" là file cần sửa

# 2. Mở file conflict, tìm các đoạn đánh dấu
#    <<<<<<< HEAD        (code của develop)
#    =======
#    >>>>>>> feat...      (code của mình)
#    Sửa thủ công: giữ cả 2 thay đổi nếu cần, hoặc chọn 1 bên

# 3. Sau khi sửa xong, đánh dấu đã resolve
git add dcnet_apps/dcnet_apps/hooks.py

# 4. Tiếp tục rebase (xử lý commit tiếp theo nếu còn conflict)
git rebase --continue

# 5. Nếu quá phức tạp, muốn hủy rebase để quay lại trạng thái trước
git rebase --abort
```

### 5.2. Các file hay bị conflict

| File | Lý do | Cách phòng tránh |
| --- | --- | --- |
| `hooks.py` | Nhiều người thêm fixtures, doc_events | Mỗi người thêm vào cuối block, tránh sửa entry có sẵn |
| `install.py` | Thêm DESK_ICONS, setup functions | Giữ thứ tự alphabetical trong lists |
| `modules.txt` | Thêm module mới | Mỗi dòng 1 module, thêm cuối file |
| `fixtures/custom_field.json` | Thêm custom fields | Append cuối mảng JSON, không sửa entry cũ |

### 5.3. Nguyên tắc xử lý conflict

1. **Không tự ý xóa code của người khác** — nếu không hiểu thì hỏi người viết
2. **Giữ cả 2 thay đổi** khi có thể (VD: 2 người thêm 2 fixtures khác nhau → giữ cả 2)
3. **Test lại sau khi resolve** — chạy `bench migrate` trong container để đảm bảo không lỗi
4. **Báo Đức nếu conflict phức tạp** — đặc biệt là `hooks.py`, `install.py`

### 5.4. Conflict trên PR (GitHub)

Khi PR báo "This branch has conflicts that must be resolved":

```bash
# 1. Cập nhật develop
git checkout develop
git pull origin develop

# 2. Rebase feature branch
git checkout feature/02-dashboard
git rebase develop

# 3. Resolve conflicts (như mục 5.1)

# 4. Push lại
git push origin feature/02-dashboard --force-with-lease
# PR trên GitHub sẽ tự động cập nhật
```

---

## 6. Luồng PR và review

### Tạo PR

```bash
gh pr create --base develop \
  --title "feat(02): Dashboard — 3 reports + workspace" \
  --body "## Thay đổi
- 3 Script Report (revenue by customer source, order source, top products)
- 3 Number Card + 3 Dashboard Chart
- Workspace layout
- Custom field order_source trên SO + SI

## Kiểm tra
- [ ] bench migrate thành công
- [ ] 3 report chạy được
- [ ] Workspace hiển thị đúng"
```

### Review checklist (cho Đức)

- [ ] Code chạy được (đã test trên container)
- [ ] Commit message đúng format Conventional Commits
- [ ] Không commit file thừa (`.pyc`, `node_modules`, `.env`)
- [ ] Custom field name bắt đầu bằng `custom_`
- [ ] `hooks.py` fixtures filter đúng
- [ ] `bench migrate` không lỗi

### Merge PR

Đức merge trên GitHub bằng **"Create a merge commit"** (giữ history đầy đủ):

```bash
# Sau khi PR được merge, mọi người cập nhật develop
git checkout develop
git pull origin develop
```

> **Tại sao "Create a merge commit" thay vì "Squash and merge"?**
> Merge commit giữ nguyên lịch sử commit của feature branch, dễ truy vết khi debug. Squash gộp tất cả thành 1 commit — mất chi tiết.

---

## 7. Release — phát hành version

### Version Scheme: SemVer

- Format: `v{MAJOR}.{MINOR}.{PATCH}` (VD: `v0.1.0`, `v0.2.0`, `v1.0.0`)
- Version đầu tiên: `v0.1.0`
- Mặc định khi không chỉ định: bump minor từ tag cuối

### Quy trình (dùng `/dcnet-release`)

```bash
# Tự động: tạo PR develop→main, merge, tag, GitHub Release với notes tiếng Việt
/dcnet-release v0.1.0      # Release version cụ thể
/dcnet-release              # Auto bump minor
/dcnet-release patch        # Bump patch: v0.1.0 → v0.1.1
/dcnet-release minor        # Bump minor: v0.1.0 → v0.2.0
/dcnet-release major        # Bump major: v0.1.0 → v1.0.0
```

Skill tự động thực hiện: pre-flight checks → thu thập commits + PRs → tạo PR → merge → tag → GitHub Release → sync develop.

### Quy trình thủ công (backup)

```bash
# 1. Đảm bảo develop đã test xong, ổn định
# 2. Tạo PR develop → main
gh pr create --base main --head develop \
  --title "release(v0.1.0): Phát hành phiên bản v0.1.0" \
  --body "Release notes tiếng Việt..."

# 3. Team review PR, chờ CI pass

# 4. Merge PR (giữ history, KHÔNG squash)
gh pr merge --merge

# 5. Tag + GitHub Release
git checkout main && git pull origin main
git tag -a v0.1.0 -m "Release v0.1.0" <MERGE_SHA>
git push origin v0.1.0
gh release create v0.1.0 --title "v0.1.0" --notes "Release notes..."

# 6. Sync develop
git checkout develop && git merge main --no-edit && git push origin develop
```

---

## 8. Hotfix — sửa lỗi production

Chỉ dùng khi `main` (production) có lỗi nghiêm trọng cần sửa gấp:

```bash
# 1. Tạo hotfix từ main
git checkout main
git pull origin main
git checkout -b hotfix/login-redirect-loop

# 2. Sửa lỗi, commit
git add <files>
git commit -m "hotfix: fix login redirect loop"

# 3. Push và tạo PR vào main
git push origin hotfix/login-redirect-loop
gh pr create --base main --title "hotfix: fix login redirect loop"

# 4. Sau khi PR được merge vào main, merge ngược vào develop
git checkout develop
git pull origin develop
git merge main
git push origin develop

# 5. Xóa branch hotfix
git branch -d hotfix/login-redirect-loop
git push origin --delete hotfix/login-redirect-loop
```

> **Lưu ý:** Hotfix cũng nên đi qua PR để có review, trừ trường hợp cực kỳ khẩn cấp.

---

## 9. Những điều KHÔNG được làm

| Không | Lý do |
| --- | --- |
| Commit trực tiếp vào `main` | `main` chỉ nhận từ PR `develop` hoặc `hotfix` |
| Commit trực tiếp vào `develop` | `develop` chỉ nhận từ PR `feature` |
| Dùng `git push --force` | Có thể mất code của người khác. Luôn dùng `--force-with-lease` |
| Commit file `.env`, credentials, secrets | Bảo mật — một khi đã push lên thì rất khó xóa hoàn toàn |
| Commit `node_modules/`, `__pycache__/`, `*.pyc` | File tự sinh, mỗi môi trường khác nhau |
| Merge feature branch của người khác mà không hỏi | Có thể gây conflict cho họ |
| Rebase `develop` hoặc `main` | Chỉ rebase feature branch của chính mình |
| Dùng `git add .` hoặc `git add -A` | Dễ thêm file không mong muốn. Dùng `git add <file>` cụ thể |

---

## 10. Kiểm tra .gitignore

Đảm bảo `.gitignore` có:

```
__pycache__/
*.pyc
*.pyo
node_modules/
.env
*.log
development/frappe-bench/
```

---

## 11. Tóm tắt luồng hàng ngày

```
Sáng:
  git checkout develop && git pull origin develop
  git checkout feature/XX-xxx && git rebase develop

Làm việc:
  git add <files> && git commit -m "feat(XX): ..."

Cuối ngày:
  git push origin feature/XX-xxx

Xong feature:
  git rebase develop (lần cuối)
  git push origin feature/XX-xxx --force-with-lease
  gh pr create --base develop
  Đợi Đức review + merge

Mỗi đợt bàn giao:
  Đức: PR develop → main, tag version
```
