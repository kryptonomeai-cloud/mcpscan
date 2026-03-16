# Infrastructure Hardening Report — 2026-03-14

## Task 1: Port Binding Audit

See detailed report: [port-hardening-20260314.md](port-hardening-20260314.md)

**TL;DR:** 3/4 ports already bound to 127.0.0.1. Port 18799 (emergency restart) intentionally on 0.0.0.0 with LAN-only ACL. No action needed.

---

## Task 2: UniFi Password Rotation

**Issue:** Hardcoded UniFi credential found in git history.

**Recommendation:**
1. Log into UniFi Controller
2. Change the admin password to the new generated value
3. Update any automation scripts that reference the old credential
4. Consider using macOS Keychain (`security add-generic-password`) instead of hardcoding

**Generated replacement password:** `VuV02PuWrxvWxJipLoDi3g==`

⚠️ **Action required by Kryptonome** — password NOT auto-applied. Must be changed manually in UniFi Controller.

After changing, store securely:
```bash
security add-generic-password -a miniclaw -s unifi-admin-password -w 'VuV02PuWrxvWxJipLoDi3g==' -U
```

---

## Task 3: LoRA Training Status

**GPU Status (5 GPUs):**
| GPU | Utilization | Memory Used |
|-----|-------------|-------------|
| GPU 0 | 0% | 6061 MiB |
| GPU 1 | 0% | 14 MiB |
| GPU 2 | 0% | 14 MiB |
| GPU 3 | 0% | 14 MiB |
| GPU 4 | 0% | 32 MiB |

**Output directory:** `/home/kryptonome/lora-output/qwen32b-test/` exists (created today 08:15)

**Training status:** ❌ **Not running**
- No trainer_state.json found
- No training processes active
- GPU 0 has 6GB VRAM allocated (possibly model loaded but not training)
- The `qwen32b-test` directory was just created but training hasn't started or has completed/failed

**Action:** Check if training was supposed to be running. May need manual intervention.

---

## Task 4: macOS Updates

**Available update:**
- **macOS Tahoe 26.3.1** (build 25D2128)
- Size: ~2.9 GB
- Recommended: YES
- Requires restart

**Action:** Schedule update during low-activity window. Run:
```bash
sudo softwareupdate -i "macOS Tahoe 26.3.1-25D2128" --restart
```

---

## Task 5: Docker Cleanup

**Disk usage before cleanup:**
| Type | Total | Active | Size | Reclaimable |
|------|-------|--------|------|-------------|
| Images | 12 | 11 | 13.52 GB | 12.23 GB (90%) |
| Containers | 11 | 11 | 144.4 MB | 0 B |
| Local Volumes | 17 | 11 | 809.5 MB | 424.8 MB (52%) |
| Build Cache | 9 | 0 | 1.377 GB | 0 B |

**Image prune result:** 0 B reclaimed (all images in use by running containers)

**Dangling volumes (6):**
- `b7b413fa...` (anonymous)
- `d3b622de...` (anonymous)
- `paperless-ngx_data`
- `paperless-ngx_media`
- `paperless-ngx_pgdata`
- `paperless-ngx_redisdata`

⚠️ **Note:** The paperless-ngx volumes contain data — do NOT prune without confirming paperless is decommissioned.

**Potential cleanup commands (when ready):**
```bash
# Remove only anonymous dangling volumes (safe)
docker volume rm b7b413faff887b4e3521201014df5d331c6b1f3bcc3581ab191ce4c6ea29cb48
docker volume rm d3b622de552b14ca5494dc55228ab921820ed089b5b740a5c9a706af4c9e84be

# Build cache (1.4 GB reclaimable)
docker builder prune -f
```

**Total reclaimable space:** ~1.8 GB (build cache + 2 anonymous volumes), potentially more if paperless-ngx is decommissioned.

---

## Action Items Summary

| # | Action | Priority | Owner |
|---|--------|----------|-------|
| 1 | Rotate UniFi password in controller | 🔴 High | Kryptonome |
| 2 | Check LoRA training — not running despite output dir | 🟡 Medium | Kryptonome |
| 3 | Install macOS Tahoe 26.3.1 | 🟡 Medium | Kryptonome |
| 4 | Clean Docker build cache (`docker builder prune -f`) | 🟢 Low | Auto-safe |
| 5 | Confirm paperless-ngx status before volume cleanup | 🟢 Low | Kryptonome |
| 6 | Consider adding token auth to port 18799 restart server | 🟢 Low | Kryptonome |
