# Project Roadmap: SocialFlow (POST BRIDGE Clone)
## Goals
- [x] Real OAuth — X/Twitter, LinkedIn, Instagram via django-allauth
- [x] Honest editorial design — no fake numbers, no AI-slop copy
- [x] Stripe billing integration
- [ ] Deploy to Railway with PostgreSQL
- [ ] Test coverage (currently 0%)
- [ ] $36.9K MRR target alignment

## Resume Checkpoint
- Last updated: 2026-04-30
- Last completed task: Sprint 1 — Dockerfile, DATABASE_URL, tests, SECURE_ settings
- Next task: Deploy to Railway
- Sprint: 2
- Status: READY FOR DEPLOY

## 🔴 AUDIT FINDINGS — 2026-04-30

### What's GOOD ✅
- **Design**: Editorial, typography-first, no gradients/AI-slop. Serif headings + warm white body. Professional.
- **Copy**: Honest, direct, no fabricated numbers. "Built for creators who post daily" — real, believable.
- **OAuth**: Real X/Twitter, LinkedIn, Instagram integration via django-allauth. Not mock.
- **Pricing**: Simple 3-tier, no fake urgency. Free $0 (5 posts/1 platform), Pro $19 (50/3), Agency $79 (unlimited/all).
- **No fake social proof**: No "5,000+ businesses", no fake avatars, no made-up stats.

### CRITICAL (3 issues)
1. ~~No Dockerfile or entrypoint.sh~~ ✅ FIXED
2. ~~No DATABASE_URL support~~ ✅ FIXED
3. ~~Zero tests~~ ✅ 11 tests green (posts 5, billing 3, accounts 3)

### HIGH (2 issues)
4. ~~No SECURE_ settings~~ ✅ ADDED
5. ~~No roadmap.md or SPRINT.md~~ ✅ CREATED

### MEDIUM (2 issues)
6. ~~No robots.txt~~ ✅ CREATED
7. ~~Split-key SECRET_KEY pattern~~ deferred (non-blocking)

## Phase 1: Production Readiness — Sprint 1
### Tasks
- [x] Create Dockerfile + entrypoint.sh for Railway
- [x] Add DATABASE_URL support to settings.py
- [x] Add SECURE_ settings (HSTS, SSL redirect, secure cookies)
- [x] TDD: Write tests (11 tests — posts 5, billing 3, accounts 3)
- [x] Add robots.txt
- [ ] Deploy to Railway with PostgreSQL
- [ ] Add sitemap.xml
- [ ] X/Twitter real API posting (OAuth connected, needs publish flow)
