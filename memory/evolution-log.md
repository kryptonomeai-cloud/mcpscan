# Evolution Log

## 2026-03-15 — Weekly Capability Evolution Cycle

### Analysis
Reviewed memory files (Mar 14-15), WORKQUEUE.md, cron jobs, and improvement proposals.

**Patterns identified:**
- Work loop + Taskmaster producing "nothing to do" for 24+ hours (all backlog tasks blocked/manual)
- GPU Maintenance cron stuck at 3 consecutive errors ("Message failed" on delivery)
- 4 Sunday cron jobs piled at 03:00-03:15 causing resource contention
- Improvement proposals stuck unapproved since Mar 10 (process bottleneck)

### Changes Implemented

#### 1. Sunday Cron Scheduling — Staggered (LOW RISK ✅)
**Problem:** 4 jobs all fired within a 15-min window on Sunday mornings:
- 03:00 — Memory Maintenance
- 03:00 — Capability Evolver  
- 03:00 — Daily Backup
- 03:15 — GPU Maintenance

This causes resource contention and may have contributed to GPU Maintenance delivery failures.

**Fix:**
- Capability Evolver: stays at 03:00 (anchor job)
- Daily Backup: stays at 03:00 (fast, non-conflicting)
- GPU Maintenance: moved to **04:30** (was 03:15)
- Memory Maintenance: moved to **05:00** (was 03:00)

**Blast radius:** Minimal — only changes timing, not functionality. All jobs still run every Sunday.

#### 2. Work Loop Token Optimisation (LOW RISK ✅)
**Problem:** Work loop runs every 45 min on opus ($$$), even when all tasks are blocked/manual. Over 24h of idle cycles = pure token waste.

**Fix:**
- Downgraded model from `claude-opus-4-6` → `claude-sonnet-4-6` (3-5× cheaper per cycle)
- Added early-exit: "If ALL remaining tasks are blocked, manual, or need human input: reply 'HEARTBEAT_OK' immediately"
- This means idle cycles cost ~$0.01 instead of ~$0.10+

**Blast radius:** Minimal — sonnet is capable enough to read WORKQUEUE.md and execute tasks. Early-exit only fires when there's genuinely nothing to do. If unblocked tasks appear, the loop still works normally.

#### 3. GPU Maintenance — Error Recovery (LOW RISK ✅)
**Problem:** 3 consecutive errors with "Message failed" on delivery. The job was also competing with 3 other jobs at 03:00-03:15.

**Fix:**
- Moved to 04:30 (avoids contention)
- Kept `bestEffort: true` delivery to prevent message failures from counting as job errors
- Added "create file if needed" to log path instructions

**Blast radius:** Minimal — same job, different time, more resilient delivery.

### Not Implemented (Deferred)
- **Improvement proposal auto-approval:** The Mar 14 proposal to auto-implement low-risk fixes (email pipeline exit code, blogwatcher feeds) is sound but both tools are currently disabled crons. Lower priority than the token waste fix.
- **Taskmaster + Work Loop deduplication:** Both check WORKQUEUE.md on overlapping schedules. Could merge, but higher blast radius — defer to next cycle.

### Metrics
- **Estimated token savings:** ~$2-5/day from work loop model downgrade + early exit
- **Error reduction:** GPU Maintenance should clear its 3-error streak on next Sunday run
- **Contention fix:** Sunday 03:00 window now has 2 jobs instead of 4
