# HEARTBEAT.md

## Priority: Volt Energy App Build
- Check `projects/energy-app/` for build progress
- If no active sub-agent is building Volt, spawn one to continue Phase 1
- Phase 1 tasks: Expo scaffold, Supabase setup, Octopus API client, Dashboard UI
- Reference: `projects/energy-app/PROJECT_PLAN.md`
- Max 2 sub-agents at a time for Volt (one build, one research)

## Freqtrade Monitor
- Check if freqtrade container is running and has made any trades
- Report trade activity only if there are new trades
