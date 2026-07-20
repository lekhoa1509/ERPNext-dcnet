# Implementation Plan: `/dcnet-release` Skill

**Spec:** `docs/superpowers/specs/2026-03-22-dcnet-release-skill-design.md`
**Ngày:** 22/03/2026

---

## Step 1: Tạo SKILL.md

**Action:** Tạo file `.claude/skills/dcnet-release/SKILL.md`

**Content:** YAML frontmatter + 5 bước workflow hoàn chỉnh

```yaml
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
```

**Body structure:**
1. Title + description + usage syntax
2. Bước 1: Pre-flight checks (branch, uncommitted, gh auth, version detect + bump logic)
3. Bước 2: Thu thập changes (commits range, PRs with `--limit 500`, conventional commit classification, stats)
4. Bước 3: Tạo PR (title format, body = release notes template, check existing PR → close old)
5. Bước 4: Merge PR (wait checks 5min, merge --merge, get MERGE_SHA)
6. Bước 5: Tag + Release + Sync (tag on MERGE_SHA, gh release create, merge main→develop)
7. Release notes template (Vietnamese, full format from spec)
8. Edge cases table
9. Important rules

**Checkpoint:** File exists at `.claude/skills/dcnet-release/SKILL.md`, has YAML frontmatter with correct triggers.

---

## Step 2: Cập nhật `docs/git-flow.md` Section 7

**Action:** Edit lines 317-343

**old_string:** Section 7 hiện tại (version scheme `v2026.03`, PR title `release: TX — ...`)

**new_string:**
```markdown
## 7. Release — phát hành version

### Version Scheme: SemVer

- Format: `v{MAJOR}.{MINOR}.{PATCH}` (VD: `v0.1.0`, `v0.2.0`, `v1.0.0`)
- Version đầu tiên: `v0.1.0`
- Mặc định: bump minor từ tag cuối

### Quy trình (dùng `/dcnet-release`)

```bash
# Tự động: tạo PR develop→main, merge, tag, GitHub Release
/dcnet-release v0.1.0      # Release version cụ thể
/dcnet-release              # Auto bump minor
/dcnet-release patch        # Bump patch
/dcnet-release minor        # Bump minor
/dcnet-release major        # Bump major
```

### Quy trình thủ công (backup)

```bash
# 1. Đảm bảo develop đã test xong, ổn định
# 2. Tạo PR develop → main
gh pr create --base main --head develop \
  --title "release(v0.1.0): Phát hành phiên bản v0.1.0" \
  --body "Release notes..."

# 3. Merge PR, tag, tạo GitHub Release
gh pr merge --merge
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
gh release create v0.1.0 --title "v0.1.0" --notes "..."

# 4. Sync develop
git checkout develop && git merge main --no-edit && git push origin develop
```
```

**Checkpoint:** `grep -c "SemVer" docs/git-flow.md` returns 1. `grep -c "v2026.03" docs/git-flow.md` returns 0.

---

## Step 3: Cập nhật `CLAUDE.md` — thêm skill vào bảng

**Action:** Edit sau dòng `/dcnet-merge`

**old_string:**
```
| `/dcnet-merge [PR#...]` | Review, merge PRs vào develop, tổng hợp chức năng | Feature summary table |
| `/dcnet-competitor-analysis {platform} {module}` |
```

**new_string:**
```
| `/dcnet-merge [PR#...]` | Review, merge PRs vào develop, tổng hợp chức năng | Feature summary table |
| `/dcnet-release [version]` | Tạo PR develop→main, tag SemVer, GitHub Release với notes tiếng Việt | PR + Tag + Release |
| `/dcnet-competitor-analysis {platform} {module}` |
```

**Checkpoint:** `grep -c "dcnet-release" CLAUDE.md` returns 1.

---

## Step 4: Commit tất cả thay đổi

**Action:** Git add + commit

```bash
git add .claude/skills/dcnet-release/SKILL.md docs/git-flow.md CLAUDE.md
git commit -m "feat(00): add /dcnet-release skill for automated GitHub releases

- SKILL.md with 5-step workflow: pre-flight, collect changes, create PR, merge, tag+release
- Update git-flow.md Section 7: v{YEAR}.{MONTH} → SemVer
- Add /dcnet-release to CLAUDE.md skills table

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

**Checkpoint:** `git log --oneline -1` shows the commit. `git diff HEAD --name-only` is empty.

---

## Step 5: Test skill invocation (dry run)

**Action:** Verify skill loads correctly

1. Check YAML frontmatter parses: `head -15 .claude/skills/dcnet-release/SKILL.md`
2. Check file structure: `wc -l .claude/skills/dcnet-release/SKILL.md` (expected: 200-300 lines)
3. Verify all git commands in SKILL.md are valid syntax (manual scan)

**Checkpoint:** File is well-formed, YAML frontmatter has `name`, `description`, `allowed-tools`, `triggers` in description.
