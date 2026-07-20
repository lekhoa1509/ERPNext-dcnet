#!/usr/bin/env python3
"""
DCNET Flow Development Installer
Automatically sets up Frappe bench with ERPNext v16 and custom apps
"""

import subprocess
import os
import sys

# Configuration
FRAPPE_BRANCH = os.environ.get("FRAPPE_BRANCH", "version-16")
SITE_NAME = os.environ.get("SITE_NAME", "flow.local")
DB_ROOT_PASSWORD = "123"  # Must match MYSQL_ROOT_PASSWORD in docker-compose.yml
ADMIN_PASSWORD = "123456"

# Local app paths (relative to /workspace)
# Note: CRM functionality is built into ERPNext module (not using separate Frappe CRM)
APPS = {
    "erpnext": "/workspace/dcnet_core",
    "hrms": "/workspace/dcnet_hrms",
    "dcnet_apps": "/workspace/dcnet_apps",
    "dcnet_theme": "/workspace/dcnet-theme",
    "vn_accounting": "/workspace/dcnet-accounting",
    "vn_banking": "/workspace/dcnet-banking",
    "einvoice": "/workspace/dcnet-einvoice",
    "dcnet_contract": "/workspace/dcnet-contract",
    "dcnet_migrate": "/workspace/dcnet-migrate",
    "dcnet_process": "/workspace/dcnet-process",
    "dcnet_crm": "/workspace/dcnet-crm",
    "dcnet_organization": "/workspace/dcnet-organization",
}

# Install order matters. `dcnet-contract-backup` is intentionally not listed
# because it declares the same app/package name as `dcnet-contract`.
# `dcnet_htkk` is a scaffold that conflicts with the HTKK module already
# shipped by `dcnet_apps`, so it is not installed as a separate app.
INSTALL_APPS = list(APPS.keys())

def run(cmd, cwd=None, check=True):
    """Run a shell command"""
    print(f"\n{'='*60}")
    print(f"Running: {cmd}")
    print(f"{'='*60}\n")
    result = subprocess.run(cmd, shell=True, cwd=cwd, check=check)
    return result.returncode == 0

def main():
    bench_path = "/workspace/development/frappe-bench"

    # Check if bench already exists
    if os.path.exists(bench_path):
        print(f"Bench already exists at {bench_path}")
        print("To reinstall, delete the frappe-bench folder first")

        # Just start bench if it exists
        os.chdir(bench_path)
        run("bench start", check=False)
        return

    print("\n" + "="*60)
    print("DCNET Flow Development Setup")
    print(f"Frappe Branch: {FRAPPE_BRANCH}")
    print("="*60 + "\n")

    # Step 1: Initialize bench
    print("\n[1/6] Initializing Frappe bench...")
    run(f"bench init --frappe-branch {FRAPPE_BRANCH} --skip-redis-config-generation frappe-bench")

    os.chdir(bench_path)

    # Step 2: Configure bench for development
    print("\n[2/6] Configuring bench...")
    run("bench set-config -g db_host mariadb")
    run("bench set-config -g redis_cache redis://redis-cache:6379")
    run("bench set-config -g redis_queue redis://redis-queue:6379")
    run("bench set-config -g redis_socketio redis://redis-queue:6379")
    run("bench set-config -g developer_mode 1")

    # Step 3: Get apps from local paths (symlink + pip install)
    print("\n[3/6] Getting apps from local repositories...")
    apps_dir = f"{bench_path}/apps"

    for app_name, app_path in APPS.items():
        if os.path.exists(app_path):
            print(f"  - Linking {app_name} from {app_path}")

            # Create symlink in apps folder
            target_path = f"{apps_dir}/{app_name}"
            if not os.path.exists(target_path):
                os.symlink(app_path, target_path)

            # Install in editable mode
            run(f"./env/bin/pip install -e {target_path}")

            # Add to apps.txt if not exists
            apps_txt = f"{bench_path}/sites/apps.txt"
            with open(apps_txt, "r") as f:
                content = f.read()
                apps_list = content.splitlines()
            if app_name not in apps_list:
                with open(apps_txt, "a") as f:
                    # Ensure newline before appending if file doesn't end with one
                    if content and not content.endswith("\n"):
                        f.write("\n")
                    f.write(f"{app_name}\n")
        else:
            print(f"  - WARNING: {app_path} not found, skipping {app_name}")

    # Step 4: Install additional dependencies
    print("\n[4/7] Installing additional dependencies...")
    # Install onscan.js required by ERPNext POS
    run(f"cd {bench_path}/apps/frappe && yarn add onscan.js")

    # Step 5: Create site
    print("\n[5/7] Creating site...")
    run(f"bench new-site {SITE_NAME} --db-root-username root --mariadb-root-password {DB_ROOT_PASSWORD} --admin-password {ADMIN_PASSWORD}")

    # Step 6: Install apps on site
    print("\n[6/7] Installing apps on site...")
    for app_name in INSTALL_APPS:
        if os.path.exists(f"{bench_path}/apps/{app_name}"):
            run(f"bench --site {SITE_NAME} install-app {app_name}")

    # Step 7: Set as default site
    print("\n[7/7] Finalizing setup...")
    # Patch Procfile: add 2 extra workers so auto_pipeline + parse jobs don't deadlock
    procfile_path = f"{bench_path}/Procfile"
    with open(procfile_path, "a") as f:
        f.write("\nworker_long: bench worker --queue long,short,default 1>> logs/worker_long.log 2>> logs/worker_long.error.log\n")
        f.write("\nworker_long2: bench worker --queue long,short,default 1>> logs/worker_long2.log 2>> logs/worker_long2.error.log\n")

    run(f"bench use {SITE_NAME}")
    run(f"bench --site {SITE_NAME} enable-scheduler")
    run(f"bench --site {SITE_NAME} set-config developer_mode 1")
    run(f"bench --site {SITE_NAME} set-config max_file_size 104857600")
    run(
        f"bench --site {SITE_NAME} execute frappe.db.set_single_value "
        "--args '[\"System Settings\", \"max_file_size\", 100]'"
    )

    print("\n" + "="*60)
    print("Setup Complete!")
    print("="*60)
    print(f"""
Site: {SITE_NAME}
Admin Password: {ADMIN_PASSWORD}

To start development server:
  cd frappe-bench
  bench start

Access at: http://localhost:8000

Installed Apps:
  - Frappe ({FRAPPE_BRANCH})
  - ERPNext v16 (from dcnet_core) - includes CRM module
  - DCNET Apps (from dcnet_apps)
  - DCNET Theme (from dcnet-theme)
  - VN Accounting (from dcnet-accounting)
  - VN Banking (from dcnet-banking)
  - EInvoice (from dcnet-einvoice)
  - DCNET Contract (from dcnet-contract)
  - HTKK (from dcnet_apps)
  - DCNET Migrate (from dcnet-migrate)
  - DCNET Process (from dcnet-process)
  - DCNET CRM (from dcnet-crm)
  - DCNET Organization (from dcnet-organization)
""")

    # Start bench
    print("\nStarting bench server...")
    run("bench start", check=False)

if __name__ == "__main__":
    main()
