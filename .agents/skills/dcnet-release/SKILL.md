---
name: dcnet-release
description: |
  Tạo PR develop→main, tag SemVer, GitHub Release với release notes tiếng Việt.
  Tổng hợp commits + PRs, phân loại theo conventional commits.

  Dùng khi:
  - User nói "/dcnet-release" hoặc "/dcnet-release v0.1.0"
  - User muốn tạo release, phát hành version mới
  - User nói "release", "phát hành", "tạo release", "tag version"

  Triggers: "dcnet-release", "release", "phát hành", "tạo release", "tag version"
allowed-tools: Bash, Read, Grep, TodoWrite
---

# /dcnet-release — Tạo Release tự động

> Tạo PR develop→main, tag SemVer, GitHub Release với release notes tiếng Việt.
> Tự động — chỉ dừng khi gặp lỗi blocking.

## Cách dùng

```
/dcnet-release v0.1.0      # Release version cụ thể
/dcnet-release              # Auto bump minor từ tag cuối
/dcnet-release patch        # Bump patch: v0.1.0 → v0.1.1
/dcnet-release minor        # Bump minor: v0.1.0 → v0.2.0
/dcnet-release major        # Bump major: v0.1.0 → v1.0.0
```

---

## Quy trình (5 bước)

### Bước 1 — Pre-flight checks

Chạy LẦN LƯỢT các kiểm tra. Nếu bất kỳ check nào fail → DỪNG ngay, thông báo lỗi.

**1.1. Verify branch hiện tại là `develop`:**

```bash
CURRENT_BRANCH=$(git branch --show-current)
```

Nếu không phải `develop` → DỪNG: "❌ Phải ở branch `develop`. Hiện tại đang ở `$CURRENT_BRANCH`."

**1.2. Pull latest:**

```bash
git pull origin develop
```

**1.3. Check uncommitted changes:**

```bash
git status --porcelain
```

Nếu có output → DỪNG: "❌ Có uncommitted changes. Hãy commit hoặc stash trước."

**1.4. Verify `gh` CLI:**

```bash
gh auth status
```

Nếu fail → DỪNG: "❌ `gh` chưa authenticated. Chạy `gh auth login` trước."

**1.5. Detect version:**

```bash
LAST_TAG=$(git tag --sort=-v:refname | head -1)
```

- Nếu `LAST_TAG` rỗng (chưa có tag nào) → mặc định `v0.1.0`
- Nếu user truyền `vX.Y.Z` (match regex `^v[0-9]+\.[0-9]+\.[0-9]+$`) → dùng trực tiếp
- Nếu user truyền `patch` → bump patch từ `LAST_TAG`
- Nếu user truyền `minor` hoặc không truyền gì → bump minor từ `LAST_TAG`
- Nếu user truyền `major` → bump major từ `LAST_TAG`

**Bump logic:**
- Parse `LAST_TAG` thành MAJOR.MINOR.PATCH (bỏ prefix `v`)
- `patch`: MAJOR.MINOR.(PATCH+1)
- `minor`: MAJOR.(MINOR+1).0
- `major`: (MAJOR+1).0.0
- Gắn prefix `v` lại

**1.6. Validate version chưa tồn tại:**

```bash
git tag -l $VERSION
```

Nếu có output → DỪNG: "❌ Tag `$VERSION` đã tồn tại. Gợi ý version tiếp theo: `$NEXT_VERSION`."

**1.7. Check có changes giữa develop và main:**

```bash
git log main..develop --oneline | head -1
```

Nếu không có output → DỪNG: "❌ Không có thay đổi mới giữa `develop` và `main`. Không cần release."

**Output bước 1:** Thông báo version sẽ release, VD: "🚀 Chuẩn bị release `v0.1.0` (tag trước: chưa có)"

---

### Bước 2 — Thu thập changes

**2.1. Xác định range:**

```bash
# Nếu có LAST_TAG
LAST_TAG_DATE=$(git log -1 --format=%aI $LAST_TAG)
COMMIT_RANGE="$LAST_TAG..HEAD"

# Nếu chưa có tag (lần đầu)
COMMIT_RANGE=""  # sẽ dùng --since
```

**2.2. Lấy commits:**

```bash
# Có tag trước
git log $LAST_TAG..develop --oneline --format="%h %s"

# Chưa có tag (lần đầu) — dùng ngày bắt đầu dự án
git log develop --oneline --format="%h %s" --since="2026-03-10"
# Fallback nếu không có commits
git log develop --oneline --format="%h %s" --max-count=100
```

**2.3. Lấy merged PRs:**

```bash
gh pr list --state merged --base develop --limit 500 --json number,title,body,mergedAt,headRefName
```

- Nếu có `LAST_TAG_DATE`: filter PRs có `mergedAt` > `LAST_TAG_DATE`
- Nếu chưa có tag: lấy tất cả (limit 500)

**2.4. Phân loại commits theo conventional commit type:**

Parse commit message, lấy phần trước dấu `:` hoặc `(`:

| Prefix | Tiêu đề tiếng Việt |
|--------|---------------------|
| `feat` | Tính năng mới |
| `fix` | Sửa lỗi |
| `refactor` | Cải thiện code |
| `docs` | Tài liệu |
| `chore` | Bảo trì |
| `test` | Kiểm thử |
| `style` | Định dạng code |
| `perf` | Hiệu suất |
| `ci` | CI/CD |
| Không match | Thay đổi khác |

**2.5. Thu thập thống kê (dùng cùng range):**

```bash
# Contributors
git log $COMMIT_RANGE --format="%aN" | sort -u

# Files changed
git diff --stat $LAST_TAG..develop 2>/dev/null || git diff --stat HEAD~$(git rev-list --count develop --since="2026-03-10")..develop

# Đếm commits và PRs từ danh sách đã thu thập
```

**Output bước 2:** Danh sách commits phân loại + PRs + thống kê, sẵn sàng để tạo release notes.

---

### Bước 3 — Tạo PR develop→main

**3.1. Check PR đang tồn tại:**

```bash
EXISTING_PR=$(gh pr list --base main --head develop --state open --json number -q '.[0].number')
```

Nếu có PR đang mở → tự động đóng:

```bash
gh pr close $EXISTING_PR --comment "Đóng để tạo PR release mới với notes cập nhật."
```

**3.2. Lấy repo info cho link so sánh:**

```bash
REPO_URL=$(gh repo view --json url -q '.url')
```

**3.3. Tạo release notes theo template:**

Compose release notes body (tiếng Việt) theo format bên dưới (xem section "Template Release Notes").

**3.4. Tạo PR:**

```bash
gh pr create --base main --head develop \
  --title "release($VERSION): Phát hành phiên bản $VERSION" \
  --body "$RELEASE_NOTES"
```

Lưu PR number từ output.

**Output bước 3:** PR number + link, VD: "✅ Tạo PR #XX: release(v0.1.0)"

---

### Bước 4 — Merge PR

**4.1. Chờ CI checks (nếu có):**

```bash
gh pr checks $PR_NUMBER --watch --fail-level all
```

Timeout 5 phút. Nếu fail → DỪNG: "❌ CI checks fail. Xem chi tiết tại: $PR_URL"

Nếu không có checks (empty output) → tiếp tục.

**4.2. Merge:**

```bash
gh pr merge $PR_NUMBER --merge
```

KHÔNG dùng `--squash` hoặc `--rebase` — giữ nguyên history.

**4.3. Lấy merge commit SHA:**

```bash
MERGE_SHA=$(gh pr view $PR_NUMBER --json mergeCommit -q '.mergeCommit.oid')
```

**4.4. Update local main:**

```bash
git checkout main && git pull origin main
```

**Output bước 4:** "✅ PR #XX đã merge. Merge commit: $MERGE_SHA"

---

### Bước 5 — Tag + GitHub Release + Sync develop

**5.1. Tạo annotated tag trên đúng merge commit:**

```bash
git tag -a $VERSION -m "Release $VERSION" $MERGE_SHA
```

**5.2. Push tag:**

```bash
git push origin $VERSION
```

**5.3. Tạo GitHub Release:**

```bash
gh release create $VERSION --title "$VERSION" --notes "$RELEASE_NOTES"
```

Dùng cùng `$RELEASE_NOTES` đã tạo ở Bước 3.

**5.4. Sync develop với main:**

```bash
git checkout develop
git merge main --no-edit
git push origin develop
```

**5.5. Thông báo thành công:**

```
🎉 Release $VERSION thành công!

📋 PR: $PR_URL
🏷️ Tag: $VERSION
📦 Release: $REPO_URL/releases/tag/$VERSION
🔀 So sánh: $REPO_URL/compare/$LAST_TAG...$VERSION
```

---

## Template Release Notes

Khi compose release notes, dùng template sau. **Bỏ qua sections rỗng** (không có items).

```markdown
# Phát hành phiên bản $VERSION

📅 Ngày phát hành: DD/MM/YYYY
🏷️ Tag: $VERSION
🔀 So sánh: [`$LAST_TAG...$VERSION`]($REPO_URL/compare/$LAST_TAG...$VERSION)

---

## Tính năng mới

- **feat(scope): mô tả commit** — chi tiết (#PR_NUMBER)

## Sửa lỗi

- **fix(scope): mô tả** — chi tiết (#PR_NUMBER)

## Cải thiện code

- **refactor(scope): mô tả** — chi tiết

## Tài liệu

- **docs(scope): mô tả** — chi tiết

## Bảo trì

- **chore(scope): mô tả** — chi tiết

## Kiểm thử

- **test(scope): mô tả** — chi tiết

## Hiệu suất

- **perf(scope): mô tả** — chi tiết

## CI/CD

- **ci(scope): mô tả** — chi tiết

## Thay đổi khác

- **mô tả commit** — chi tiết

---

## Pull Requests đã merge

| # | Tiêu đề | Nhánh |
|---|---------|-------|
| #N | tiêu đề PR | feature/XX-name |

## Thống kê

- 📝 Tổng commits: N
- 🔀 PRs merged: N
- 👥 Contributors: Name1, Name2, Name3
- 📁 Files changed: N
```

### Nguyên tắc format

- Mỗi commit liệt kê với **scope (STT)**, mô tả, link PR number `(#N)` nếu có
- Nhóm theo conventional commit type → tiêu đề tiếng Việt
- Sections rỗng → **KHÔNG hiển thị** (bỏ qua hoàn toàn)
- Nếu chưa có `LAST_TAG` → bỏ dòng "So sánh" trong header
- Ngày format: DD/MM/YYYY (VD: 22/03/2026)

---

## Edge Cases

| Tình huống | Xử lý |
|---|---|
| Chưa có tag nào (lần đầu) | Commits từ 10/03/2026 hoặc 100 gần nhất, version `v0.1.0`, bỏ link so sánh |
| develop = main (không có changes) | DỪNG: "Không có thay đổi mới để release" |
| PR develop→main đã tồn tại | Tự động đóng PR cũ, tạo mới |
| `gh` chưa auth | DỪNG, hướng dẫn `gh auth login` |
| Uncommitted changes | DỪNG, yêu cầu commit/stash |
| Version trùng tag | DỪNG, gợi ý version tiếp |
| Merge conflict | DỪNG, hướng dẫn resolve thủ công |
| Commit không theo convention | Xếp vào "Thay đổi khác" |
| CI checks fail | DỪNG, link đến PR |
| CI checks timeout (>5 phút) | DỪNG, link đến PR |

---

## Quy tắc quan trọng

1. **KHÔNG squash/rebase** khi merge PR → dùng `--merge` để giữ history
2. **KHÔNG tạo tag trước khi merge** → tag phải trỏ đúng merge commit
3. **LUÔN sync develop sau release** → `git merge main --no-edit` trên develop
4. **LUÔN dùng annotated tag** → `git tag -a` (không dùng lightweight tag)
5. **Release notes = PR body** → cùng nội dung, không viết lại
6. **Bỏ sections rỗng** trong release notes → không hiển thị section không có items
7. **Ngày format DD/MM/YYYY** → theo chuẩn Việt Nam
