# dcnet_permission

Custom Frappe app của DCNET giúp **quản lý phân quyền dễ dàng hơn** — tập trung Role, Permission và User Access vào một khu vực quản lý trực quan, giảm thao tác thủ công trên Permission Manager / Role Profile mặc định của Frappe.

> GitHub repo: [`dcnet-cloud/dcnet-permission`](https://github.com/dcnet-cloud/dcnet-permission) (hyphen) · Frappe app module: `dcnet_permission` (underscore).

## Trạng thái

🚧 **Khởi tạo** — repo + git workflow guard đã setup, chưa có code Frappe. Dev chạy `bench new-app dcnet_permission` (hoặc bổ sung skeleton) trên nhánh `feature/*`.

## Cài đặt (sau khi có code)

```bash
bench get-app --branch main https://github.com/dcnet-cloud/dcnet-permission.git
bench --site <site> install-app dcnet_permission
```

## Quy trình phát triển (Git Flow)

```
feature/*  ─┐
fix/*       ├──→ PR → develop → PR (owner) → main → tag v1.x.x
refactor/*  │
chore/*     │
docs/*     ─┘

hotfix/* → PR → main (owner) → tag patch
             └→ PR → develop (sync)
```

| Target | Cho phép merge từ |
|--------|-------------------|
| `main` | `develop`, `hotfix/*` |
| `develop` | `feature/*`, `fix/*`, `refactor/*`, `chore/*`, `docs/*`, `test/*` |

- **Branch:** tạo nhánh từ `develop` — `git checkout -b feature/<tên> develop`
- **PR title:** Conventional Commits — `feat: ...`, `fix(scope): ...`
- **PR body:** bắt buộc 2 section `🎯 Bối cảnh nghiệp vụ` + `⚙️ Chức năng thực hiện` (30–250 ký tự mỗi section) — `gitflow-guard` validate.
- **Push thẳng `main`/`develop`:** chỉ owner (`vovanduc`) — `direct-push-guard` chặn còn lại.
- PR mới tự post vào Discord forum qua `discord-pr-notify`.

## Workflows bảo vệ

| Workflow | Vai trò |
|----------|---------|
| `gitflow-guard.yml` | Validate base/head branch, tên nhánh, PR title, PR body |
| `direct-push-guard.yml` | Chặn push trực tiếp `main`/`develop` (whitelist owner) |
| `discord-pr-notify.yml` | Post PR mới vào Discord forum (org secret `DISCORD_PR_WEBHOOK`) |
