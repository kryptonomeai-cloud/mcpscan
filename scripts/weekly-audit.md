# Weekly System Audit Checklist

Run every Sunday at 04:00 UTC via cron. For EVERY item, run the actual command and verify.

## 1. System Health
- [ ] `sw_vers` — OS version, check for major updates
- [ ] `uptime` — verify reasonable uptime, load averages
- [ ] `df -h /` — disk usage (warn if >80%)
- [ ] `vm_stat` — memory pressure check

## 2. Security Posture
- [ ] `/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate` — firewall ON
- [ ] `fdesetup status` — FileVault ON
- [ ] `csrutil status` — SIP enabled
- [ ] `openclaw security audit --deep` — 0 critical findings
- [ ] `lsof -iTCP -sTCP:LISTEN -nP` — listening ports match baseline
- [ ] `docker exec crowdsec cscli decisions list` — review active blocks

## 3. Services & Docker
- [ ] `docker ps` — all expected containers running
- [ ] Compare container list against baseline
- [ ] Check container health status (healthy/unhealthy)

## 4. LaunchAgents & Daemons
- [ ] `ls ~/Library/LaunchAgents/` — match baseline count
- [ ] `ls /Library/LaunchAgents/` — match baseline
- [ ] `ls /Library/LaunchDaemons/` — match baseline
- [ ] Flag any new/removed items

## 5. Backups
- [ ] `tmutil destinationinfo` — Time Machine configured (or note if not)
- [ ] iCloud backup — check latest backup timestamp
- [ ] Verify backup ran within last 24h

## 6. Updates
- [ ] `openclaw update status` — note if update available
- [ ] `brew outdated` — count outdated packages
- [ ] `brew doctor` — check for warnings
- [ ] `softwareupdate -l` — macOS updates

## 7. OpenClaw Health
- [ ] `openclaw health --json` — all channels probe OK
- [ ] Cron jobs — check for error status
- [ ] Session count — note if growing excessively
- [ ] MEMORY.md size — warn if >200 lines

## 8. Ollama / AI Models
- [ ] Verify Ollama responding on :11434
- [ ] List loaded models

## 9. Baseline Updates
- [ ] If new services detected, update `configs/process-baseline.json`
- [ ] Document any intentional changes

## 10. Report
- [ ] Append detailed findings to `memory/weekly-audit-log.md`
- [ ] Fix what can be fixed automatically
- [ ] Report only failures/warnings to user
