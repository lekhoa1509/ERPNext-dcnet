#!/bin/bash
# Auto-start script for Frappe Bench
# This script can run as entrypoint (foreground) or background mode
#
# Usage:
#   ./start-bench.sh           # Foreground mode (for docker compose)
#   ./start-bench.sh --background  # Background mode (for devcontainer)

BENCH_DIR="/workspace/development/frappe-bench"
INSTALLER_DIR="/workspace/development"
BACKGROUND_MODE=false

# Parse arguments
if [ "$1" = "--background" ]; then
    BACKGROUND_MODE=true
fi

# Check if frappe-bench exists
if [ ! -d "$BENCH_DIR" ]; then
    echo ""
    echo "============================================================"
    echo "  DCNET Flow - First Time Setup"
    echo "============================================================"
    echo ""
    echo "frappe-bench not found. Running installer..."
    echo "This may take 10-15 minutes on first run."
    echo ""

    cd "$INSTALLER_DIR"

    # Run installer and capture exit code
    if python installer.py; then
        echo ""
        echo "Installation completed successfully!"
    else
        echo ""
        echo "============================================================"
        echo "  Installation failed!"
        echo "============================================================"
        echo ""
        echo "Please run manually:"
        echo "  docker compose exec frappe bash"
        echo "  cd /workspace/development"
        echo "  python installer.py"
        echo ""
        # Keep container alive for debugging
        if [ "$BACKGROUND_MODE" = false ]; then
            echo "Container will stay alive for debugging..."
            exec sleep infinity
        fi
        exit 1
    fi
fi

# Verify frappe-bench exists after potential installation
if [ ! -d "$BENCH_DIR" ]; then
    echo "ERROR: frappe-bench still not found after installation attempt."
    echo "Please run: cd /workspace/development && python installer.py"
    if [ "$BACKGROUND_MODE" = false ]; then
        exec sleep infinity
    fi
    exit 1
fi

# Create /sites symlink for HRMS frontend build compatibility
# HRMS socket.js uses relative path ../../../../sites/common_site_config.json
# which resolves to /sites/ when hrms is symlinked from /workspace/dcnet_hrms
if [ -d "$BENCH_DIR/sites" ] && [ ! -e "/sites" ]; then
    ln -sf "$BENCH_DIR/sites" /sites
    echo "Created /sites symlink for HRMS frontend compatibility"
fi

cd "$BENCH_DIR"

if [ "$BACKGROUND_MODE" = true ]; then
    # Background mode (for devcontainer postStartCommand)
    if pgrep -f "bench start" > /dev/null; then
        echo "Bench is already running"
        exit 0
    fi

    echo "Starting Frappe Bench in background..."
    nohup bench start > /tmp/bench.log 2>&1 &

    echo "Bench started in background. Access at http://flow.local:8000"
    echo "View logs: tail -f /tmp/bench.log"
else
    # Foreground mode (for docker compose)
    echo ""
    echo "============================================================"
    echo "  DCNET Flow - Starting Bench"
    echo "============================================================"
    echo ""
    echo "Access at: http://localhost:8000"
    echo "Admin password: 123456"
    echo ""

    # Run bench in foreground (keeps container alive)
    exec bench start
fi
