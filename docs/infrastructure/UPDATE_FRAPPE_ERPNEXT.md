# Update Frappe & ERPNext lên bản mới nhất

> Cập nhật: 11/02/2026 | Frappe v16.6.0 | ERPNext v16.5.0

## 1. Update Frappe (trong devcontainer)

Frappe nằm trong container, không nằm trong repo flow_next.

```bash
# Vào container
docker exec -it devcontainer-frappe-1 bash

# Update frappe
cd /workspace/development/frappe-bench/apps/frappe
git pull origin version-16

# Cài lại Python dependencies (bắt buộc - tránh lỗi thiếu module)
cd /workspace/development/frappe-bench
bench setup requirements --python

# Migrate
bench --site flow.local migrate
```

> **Nếu container bị crash** sau git pull (thiếu module mới như `nh3`):
> ```bash
> # Chạy từ máy host, dùng docker compose run thay vì exec
> docker compose -f .devcontainer/docker-compose.yml run --rm --entrypoint bash frappe \
>   -c "cd /workspace/development/frappe-bench && bench setup requirements --python"
>
> # Sau đó start lại
> docker compose -f .devcontainer/docker-compose.yml up -d frappe
> ```

## 2. Update ERPNext (dcnet_core)

`dcnet_core/` là bản copy của ERPNext nằm trong monorepo flow_next (không phải git submodule).
**Không dùng được `git merge`** vì unrelated histories. Dùng rsync thay thế.

### Bước 1: Backup file đã customize

```bash
# Xem danh sách file DCNET đã sửa (so với lần update gần nhất)
git log --oneline --diff-filter=M -- dcnet_core/ | head -10

# Backup (thay đổi danh sách tùy thời điểm)
mkdir -p /tmp/dcnet_backup
cp dcnet_core/erpnext/hooks.py /tmp/dcnet_backup/
cp dcnet_core/erpnext/locale/vi.po /tmp/dcnet_backup/
cp dcnet_core/erpnext/desktop_icon/crm.json /tmp/dcnet_backup/
```

### Bước 2: Stash working changes

```bash
git stash --include-untracked -m "WIP: before erpnext update"
```

### Bước 3: Sync upstream vào dcnet_core

```bash
# Thêm remote (chỉ cần 1 lần)
git remote add erpnext-upstream https://github.com/frappe/erpnext.git

# Tạo worktree tạm từ upstream
git fetch erpnext-upstream version-16
git worktree add /tmp/erpnext-v16 erpnext-upstream/version-16

# Sync vào dcnet_core (xóa file cũ, giữ .git)
rsync -a --delete --exclude='.git' /tmp/erpnext-v16/ dcnet_core/
```

### Bước 4: Restore file custom + cleanup

```bash
cp /tmp/dcnet_backup/hooks.py dcnet_core/erpnext/hooks.py
cp /tmp/dcnet_backup/vi.po dcnet_core/erpnext/locale/vi.po
cp /tmp/dcnet_backup/crm.json dcnet_core/erpnext/desktop_icon/crm.json

# Cleanup
git worktree remove /tmp/erpnext-v16
rm -rf /tmp/dcnet_backup
```

### Bước 5: Commit + migrate

```bash
git add dcnet_core/
git commit -m "chore: update ERPNext vX.X.X → vY.Y.Y"

# Restore stash
git stash pop

# Cài dependencies + migrate
docker exec devcontainer-frappe-1 bash -c \
  "cd /workspace/development/frappe-bench && bench setup requirements --python && bench --site flow.local migrate"
```

## 3. Kiểm tra sau update

```bash
# Trong container
docker exec devcontainer-frappe-1 bash -c \
  "cd /workspace/development/frappe-bench && bench version"

# Clear cache
docker exec devcontainer-frappe-1 bash -c \
  "cd /workspace/development/frappe-bench && bench --site flow.local clear-cache"
```

## Ghi chú

- Cả Frappe và ERPNext đều release weekly
- Luôn chạy `bench setup requirements --python` rồi `bench migrate` sau update
- Nếu lỗi, rollback bằng `git revert` commit update
- File custom hiện tại: `hooks.py`, `locale/vi.po`, `desktop_icon/crm.json`
