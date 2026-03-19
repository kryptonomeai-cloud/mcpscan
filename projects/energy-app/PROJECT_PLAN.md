# ⚡ Volt — Smart Energy Platform
## Full Project Plan v1.0

_"Know your energy. Control your costs. Reduce your impact."_

---

## 1. Vision & Positioning

### What
A cross-platform smart energy app (iOS, Android, Web) that gives UK households complete visibility and control over their energy — consumption, costs, solar, EV charging, and carbon impact. Works with **any UK energy supplier** via smart meter data, with premium features for Octopus Energy + Ohme EV charger users.

### Why
- **30M+ UK smart meters** installed — yet most people can't see their data properly
- Existing apps are either supplier-locked (Octo Aid = Octopus only) or basic (Loop = slow/limited)
- No single app combines: energy monitoring + EV charging + solar + AI insights + carbon tracking
- The UK energy market is shifting to time-of-use tariffs (Agile, Tracker, Go, Flux) — users need tools to optimise

### Who
- **Primary:** UK smart meter customers who want to reduce bills
- **Power users:** Octopus Energy customers on smart tariffs (Agile/Tracker/Go/Flux)
- **EV owners:** Ohme + other smart charger users wanting to optimise charging costs
- **Solar owners:** Anyone with panels + battery wanting to maximise self-consumption
- **Green-conscious:** People who want to minimise their carbon footprint

### Competitors
| App | Supplier | Platforms | Strengths | Weaknesses |
|-----|----------|-----------|-----------|------------|
| **Octo Aid** | Octopus only | iOS | 4.7★, live demand, EV scheduling | Octopus-locked, £1.99/mo pro, no Android |
| **Loop** | Any (n3rgy/DCC) | iOS, Android, Web | Free, any supplier, solar simulator | Slow data (24h lag), basic UI, no AI |
| **Hugo Energy** | Any (n3rgy) | iOS, Android | Budget tracking, projections | No live data, next-day only |
| **Bright (Hildebrand)** | Any (CAD device) | iOS, Android | Near-real-time via CAD hardware | Requires separate hardware purchase |
| **Ivie** | Any (Chameleon IHD) | iOS, Android | Live via IHD bridge, smart home links | Unreliable data, immature |
| **Octopus App** | Octopus only | iOS, Android | Official, account management | Basic analytics, no AI, no EV integration |

### Our Edge
1. **Any supplier + premium Octopus features** — universal via n3rgy, deep Octopus via API
2. **EV charging integration** — Ohme, myenergi Zappi (future: Pod Point, Easee)
3. **AI-powered insights** — personalised savings recommendations
4. **Carbon intensity** — real-time grid carbon data from National Grid ESO
5. **Solar + battery** — GivEnergy, Solis, Sunsynk integrations
6. **Beautiful UI** — dark mode, smooth animations, glanceable widgets
7. **Cross-platform from day 1** — iOS, Android, Web

---

## 2. Tech Stack

### Frontend: React Native + Expo (SDK 53)
**Why:** Single codebase for iOS, Android, AND web. Expo Router for file-based navigation. You already know React/Next.js — minimal learning curve. Expo EAS for builds and OTA updates.

| Component | Library |
|-----------|---------|
| Framework | Expo SDK 53 + Expo Router v4 |
| Styling | NativeWind (Tailwind for RN) |
| Charts | react-native-wagmi-charts (candlestick/line) + victory-native (bar/pie) |
| Animations | react-native-reanimated 3 |
| State | Zustand + React Query (TanStack) |
| Forms | React Hook Form + Zod |
| Icons | lucide-react-native |
| Storage | expo-secure-store (tokens) + MMKV (cache) |

### Backend: Supabase
**Why:** Open-source Firebase alternative. Postgres DB, auth, real-time subscriptions, edge functions. Self-hostable if needed. Free tier generous (500MB DB, 1GB storage, 50K monthly active users).

| Component | Tech |
|-----------|------|
| Database | Supabase Postgres |
| Auth | Supabase Auth (email + social) |
| Real-time | Supabase Realtime (push price changes) |
| Edge Functions | Deno (API proxy, data aggregation) |
| Storage | Supabase Storage (user exports) |
| Cron | Supabase pg_cron (rate fetching) |

### External APIs
| API | Purpose | Auth | Rate Limits |
|-----|---------|------|-------------|
| Octopus REST | Consumption, tariffs, prices | API key (basic auth) | ~100 req/5min |
| Octopus GraphQL | Live demand, balance, EV dispatch | JWT (60min, refresh 7d) | Similar |
| n3rgy Consumer | Universal smart meter data | MPAN/MPRN | TBD |
| Ohme | EV charger control + stats | Firebase token | Unofficial |
| Carbon Intensity | Grid carbon (NESO) | None (public) | 30 req/min |
| GivEnergy | Solar/battery | API key | TBD |
| SolisCloud | Solar/battery | API key + secret | TBD |

### CI/CD & Distribution
| Tool | Purpose |
|------|---------|
| GitHub Actions | CI: lint, test, type-check |
| EAS Build | iOS + Android builds (cloud) |
| EAS Submit | App Store + Play Store submission |
| EAS Update | OTA JS updates (skip store review) |
| Vercel | Web version hosting |
| TestFlight / Play Console | Beta distribution |

---

## 3. Feature Roadmap

### Phase 1: Foundation (Weeks 1-3) — "See Your Energy"
**Goal:** Core app with Octopus Energy integration. Dashboard, usage charts, rates.

| Feature | Priority | Complexity |
|---------|----------|------------|
| Onboarding flow (API key entry, account detection) | P0 | Medium |
| Dashboard: current rate, today's spend, standing charge | P0 | Medium |
| Usage charts: half-hourly, daily, weekly, monthly | P0 | High |
| Tariff rate display (current + upcoming for Agile/Tracker) | P0 | Medium |
| Dark mode UI with energy-themed design | P0 | Medium |
| Pull-to-refresh + background data sync | P0 | Low |
| Settings: account management, data preferences | P0 | Low |

**Review Cycle 1:** Internal testing, UX review, performance profiling

### Phase 2: Intelligence (Weeks 4-5) — "Understand Your Energy"
**Goal:** Bill forecasting, tariff comparison, smart insights.

| Feature | Priority | Complexity |
|---------|----------|------------|
| Bill forecast: predicted monthly cost | P0 | High |
| Peak vs off-peak breakdown | P0 | Medium |
| "Best time" engine: cheapest windows for high-power tasks | P1 | High |
| Tariff comparison: "You'd save £X on Agile/Tracker/Go" | P1 | High |
| Standing charge tracker | P1 | Low |
| Push notifications: rate alerts, cheap windows | P1 | Medium |
| CSV/JSON data export | P2 | Low |

**Review Cycle 2:** Beta user testing (5-10 people), analytics review

### Phase 3: EV & Charging (Weeks 6-7) — "Charge Smarter"
**Goal:** Ohme integration, charge cost tracking, solar-aware charging.

| Feature | Priority | Complexity |
|---------|----------|------------|
| Ohme account linking (Firebase auth) | P0 | Medium |
| Live charge status: power, current, voltage, SoC | P0 | Medium |
| Charge session cost calculation | P0 | Medium |
| Charge history + cost per kWh/mile | P1 | Medium |
| Start/stop/pause charging from app | P1 | Medium |
| "Best time to charge" recommendations | P1 | High |
| Solar surplus charging trigger | P2 | High |

**Review Cycle 3:** EV owner testing, Ohme reliability assessment

### Phase 4: Carbon & Green (Week 8) — "Go Green"
**Goal:** Carbon intensity, green score, environmental impact.

| Feature | Priority | Complexity |
|---------|----------|------------|
| Real-time carbon intensity (NESO API) | P0 | Low |
| 96-hour carbon forecast | P0 | Low |
| Regional carbon breakdown | P1 | Low |
| Green score (gamification) | P1 | Medium |
| Monthly carbon report | P1 | Medium |
| "Grid is green right now" notifications | P2 | Low |
| Achievements & badges | P2 | Medium |

**Review Cycle 4:** Feature completeness review, App Store prep

### Phase 5: Universal Access (Weeks 9-10) — "Any Supplier"
**Goal:** n3rgy integration for non-Octopus customers. Web version.

| Feature | Priority | Complexity |
|---------|----------|------------|
| n3rgy Consumer API integration | P0 | High |
| MPAN/MPRN-based onboarding | P0 | Medium |
| DCC consent flow | P0 | High |
| Web version (Expo for Web) | P1 | Medium |
| PWA support (installable) | P1 | Medium |
| Graceful feature degradation (no Agile rates for non-Octopus) | P1 | Medium |

**Review Cycle 5:** Cross-supplier testing, web browser compatibility

### Phase 6: Solar & Battery (Weeks 11-13) — "Your Energy Ecosystem"
**Goal:** Solar inverter + battery integrations.

| Feature | Priority | Complexity |
|---------|----------|------------|
| GivEnergy integration (solar + battery) | P1 | High |
| SolisCloud integration | P1 | High |
| Solar generation vs consumption view | P0 | Medium |
| Self-consumption % tracking | P0 | Medium |
| Battery charge/discharge scheduling | P2 | High |
| Export income tracking | P1 | Medium |
| Battery arbitrage calculator | P2 | High |

**Review Cycle 6:** Solar owner testing, integration reliability

### Phase 7: AI & Premium (Weeks 14-16) — "Your Energy AI"
**Goal:** AI-powered insights, premium features, monetisation.

| Feature | Priority | Complexity |
|---------|----------|------------|
| AI Energy Coach (personalised recommendations) | P0 | High |
| Natural language queries ("How much did I spend last Tuesday?") | P1 | High |
| Anomaly detection ("Usage spike at 3am — check for issues") | P1 | High |
| Household comparison (anonymised benchmarking) | P2 | Medium |
| Premium tier gating (Stripe/RevenueCat) | P0 | Medium |
| Referral system | P2 | Medium |
| Apple Watch / WearOS widget | P2 | High |

**Review Cycle 7:** AI accuracy testing, premium conversion analysis

### Phase 8: Polish & Launch (Weeks 17-18) — "Ship It"
**Goal:** App Store submission, marketing site, public launch.

| Feature | Priority | Complexity |
|---------|----------|------------|
| App Store screenshots + metadata | P0 | Medium |
| Play Store listing | P0 | Medium |
| Marketing website (Next.js on Vercel) | P0 | Medium |
| Privacy policy + terms | P0 | Low |
| Analytics (PostHog / Mixpanel) | P0 | Medium |
| Crash reporting (Sentry) | P0 | Low |
| Performance optimisation pass | P0 | Medium |
| Accessibility audit (VoiceOver/TalkBack) | P1 | Medium |

**LAUNCH** 🚀

---

## 4. Design Language

### Theme: "Dark Energy"
- **Background:** Near-black (#0A0B0F) with subtle blue tint
- **Primary accent:** Electric cyan (#06D6A0) — energy, vitality
- **Secondary accent:** Warm amber (#FFB703) — for costs/warnings
- **Error/high usage:** Coral red (#FF6B6B)
- **Green/savings:** Emerald (#10B981)
- **Text:** White (#FAFAFA) primary, grey (#9CA3AF) secondary
- **Cards:** Dark grey (#1A1B23) with subtle border glow on active

### Design Principles
1. **Glanceable** — Key number visible in <1 second (current rate, today's cost)
2. **Animated** — Smooth transitions, live-updating numbers, pulsing indicators
3. **Data-dense but not cluttered** — Show more info to power users via progressive disclosure
4. **Delightful** — Subtle haptics on interactions, celebration animations for savings milestones

### UI References
- Tesla app (dark, data-rich, car status)
- Robinhood (real-time data, beautiful charts)
- Oura Ring (health dashboard, weekly reports, green scoring)
- Monzo (spending breakdown, clean categories)

---

## 5. Architecture

```
┌─────────────────────────────────────────┐
│              Mobile App (Expo)           │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐  │
│  │Dashboard │ │ Charging │ │ Solar   │  │
│  │ Charts   │ │ EV/Ohme  │ │ Battery │  │
│  │ Insights │ │ Schedule │ │ Export  │  │
│  └────┬─────┘ └────┬─────┘ └────┬────┘  │
│       │             │            │       │
│  ┌────┴─────────────┴────────────┴────┐  │
│  │        API Client Layer            │  │
│  │  (React Query + Zustand cache)     │  │
│  └────────────────┬───────────────────┘  │
└───────────────────┼──────────────────────┘
                    │
         ┌──────────┴──────────┐
         │  Supabase Backend   │
         │  ┌───────────────┐  │
         │  │ Edge Functions │  │
         │  │ (API proxy)   │  │
         │  └───────┬───────┘  │
         │  ┌───────┴───────┐  │
         │  │   Postgres    │  │
         │  │ (user data,   │  │
         │  │  cache, prefs)│  │
         │  └───────────────┘  │
         └──────────┬──────────┘
                    │
    ┌───────────────┼───────────────────┐
    │               │                   │
┌───┴────┐   ┌─────┴──────┐   ┌───────┴───────┐
│Octopus │   │   n3rgy    │   │ Carbon        │
│REST +  │   │ Consumer   │   │ Intensity API │
│GraphQL │   │ API        │   │ (NESO)        │
└────────┘   └────────────┘   └───────────────┘
    │
    ├── Ohme API (EV charging)
    ├── GivEnergy API (solar/battery)
    ├── SolisCloud API (solar/battery)
    └── myenergi API (Zappi/Eddi)
```

### Data Flow
1. **User links account** → API keys stored in Supabase (encrypted)
2. **Edge function** fetches consumption data on schedule (every 30min)
3. **Data cached** in Postgres, served to app via real-time subscriptions
4. **Rate data** fetched daily (Agile: ~4pm for next day's rates)
5. **Carbon data** fetched every 30min from NESO
6. **EV data** fetched on-demand when charger tab is active

---

## 6. Monetisation

### Free Tier
- Dashboard (current rate, today's cost)
- 7-day usage charts
- Carbon intensity
- Basic notifications

### Pro Tier — £2.99/mo or £24.99/yr
- Full usage history (unlimited)
- AI Energy Coach
- Bill forecast & tariff comparison
- EV charging integration
- Solar/battery dashboard
- Green score & achievements
- CSV/JSON export
- Priority support

### Revenue Streams
1. **Subscriptions** (primary) — RevenueCat for cross-platform
2. **Referral commissions** — Octopus pays ~£50/referral, solar installers pay more
3. **Data insights** (anonymised, opt-in) — aggregated usage patterns for energy companies
4. **White-label** (future) — licence to energy companies wanting their own branded version

---

## 7. Timeline & Milestones

| Week | Phase | Deliverable | Review |
|------|-------|------------|--------|
| 1 | Foundation | Project setup, Expo scaffold, Supabase, auth | — |
| 2 | Foundation | Dashboard UI, Octopus API integration | — |
| 3 | Foundation | Usage charts, rate display, pull-to-refresh | ✅ Review 1 |
| 4 | Intelligence | Bill forecast, peak/off-peak breakdown | — |
| 5 | Intelligence | Tariff comparison, notifications | ✅ Review 2 |
| 6 | EV & Charging | Ohme integration, live charge status | — |
| 7 | EV & Charging | Charge history, cost tracking | ✅ Review 3 |
| 8 | Carbon & Green | Carbon intensity, green score | ✅ Review 4 |
| 9 | Universal | n3rgy integration, any-supplier support | — |
| 10 | Universal | Web version, PWA | ✅ Review 5 |
| 11-13 | Solar & Battery | GivEnergy, Solis, solar dashboard | ✅ Review 6 |
| 14-16 | AI & Premium | AI coach, premium tier, payments | ✅ Review 7 |
| 17-18 | Launch | App Store, Play Store, marketing site | 🚀 LAUNCH |

### Review Cycle Process
Each review includes:
1. **Feature walkthrough** — Demo all new features
2. **UX audit** — Is it intuitive? Any friction?
3. **Performance check** — Bundle size, load times, memory
4. **Bug triage** — Fix critical, log non-critical
5. **User feedback** (from beta testers when available)
6. **Competitor check** — What have they shipped since last review?
7. **Pivot/adjust** — Reprioritise based on learnings

---

## 8. Research Sprints (Parallel)

These happen alongside development, feeding into future phases:

| Sprint | Timing | Research Area |
|--------|--------|---------------|
| R1 | Weeks 1-3 | n3rgy API deep-dive, DCC consent flow, data latency testing |
| R2 | Weeks 3-5 | Ohme API reliability, auth token refresh, rate limits |
| R3 | Weeks 5-7 | Solar inverter APIs (GivEnergy, Solis, Sunsynk) — auth, endpoints, data quality |
| R4 | Weeks 7-9 | AI/ML for usage prediction — model selection, training data, inference cost |
| R5 | Weeks 9-11 | Smart Energy Data Service (new gov service) — evaluate as alternative to n3rgy |
| R6 | Weeks 11-13 | myenergi (Zappi/Eddi) API, Pod Point API, Easee API |
| R7 | Weeks 13-15 | Heat pump integration research (Vaillant, Samsung, Daikin) |
| R8 | Weeks 15-17 | Apple Watch / WearOS — widget design, complication data |

---

## 9. Risk Register

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Ohme API breaks (unofficial) | High | Medium | Maintain `ohmepy` fork, pin version, monitor HA core changes |
| n3rgy rate limits or downtime | High | Low | Cache aggressively, fallback messaging |
| Octopus API changes | Medium | Low | Version pin, monitor their changelog |
| App Store rejection | Medium | Low | Follow guidelines, no private API use |
| Low conversion to Pro | High | Medium | A/B test pricing, ensure free tier is genuinely useful |
| Competitor launches similar product | Medium | Medium | Ship fast, focus on UX and AI as differentiators |
| GDPR/data privacy concerns | High | Low | Local-first where possible, transparent data policy |

---

## 10. Success Metrics

### Launch (Month 1)
- 1,000 downloads
- 4.5+ App Store rating
- <3s cold start time
- <500KB initial bundle (JS)

### Growth (Month 3)
- 10,000 MAU
- 5% Pro conversion rate
- 50+ referral commissions
- <1% crash rate

### Scale (Month 6)
- 50,000 MAU
- Featured in App Store "Energy" category
- Solar + EV integrations live
- AI coach generating measurable savings

---

## 11. Naming

**Working name: Volt**
- Short, memorable, energy-related
- volt.energy / getvolt.app (domain check needed)
- Alternatives considered: Watt, Zap, Joule, Griddy, Spark, Flux

---

## 12. Immediate Next Steps

1. **Scaffold Expo project** with Router, NativeWind, base navigation
2. **Set up Supabase** — project, auth, initial schema
3. **Build Octopus API client** — REST consumption + GraphQL auth
4. **Design dashboard UI** — Figma or direct in code
5. **Domain + branding** — Secure name, logo concept
6. **GitHub repo** — Private, CI/CD pipeline
