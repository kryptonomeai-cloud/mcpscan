#!/bin/bash
# Process Security Audit Script for Mac mini
# Outputs JSON-ish sections for comparison against baseline

echo "=== LISTENING PORTS ==="
lsof -iTCP -sTCP:LISTEN -nP 2>/dev/null | awk 'NR>1 {print $1, $2, $9}' | sort -u

echo "=== LAUNCHAGENTS (user) ==="
ls ~/Library/LaunchAgents/ 2>/dev/null

echo "=== LAUNCHAGENTS (system) ==="
ls /Library/LaunchAgents/ 2>/dev/null

echo "=== LAUNCHDAEMONS ==="
ls /Library/LaunchDaemons/ 2>/dev/null

echo "=== DOCKER CONTAINERS ==="
docker ps --format '{{.Names}} {{.Image}} {{.Status}}' 2>/dev/null || echo "Docker not running"

echo "=== USER PROCESSES ==="
ps aux | grep -vE '(^USER|/System/|/usr/libexec/|/usr/sbin/|/sbin/|kernel_task|WindowServer|loginwindow|Finder|Dock|SystemUIServer|grep)' | awk '{print $1, $2, $11}' | head -60
