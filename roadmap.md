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
- Last completed task: Audit
- Next task: Add Dockerfile + DATABASE_URL + SECURE_ settings
- Sprint: 1
- Status: IN PROGRESS

## 🔴 AUDIT FINDINGS — 2026-04-30

### What's GOOD ✅
- **Design**: Editorial, typography-first, no gradients/AI-slop. Serif headings + warm white body. Professional.
- **Copy**: Honest, direct, no fabricated numbers. "Built for creators who post daily" — real, believable.
- **OAuth**: Real X/Twitter, LinkedIn, Instagram integration via django-allauth. Not mock.
- **Pricing**: Simple 3-tier, no fake urgency. Free $0 (5 posts/1 platform), Pro $19 (50/3), Agency $79 (unlimited/all).
- **No fake social proof**: No "5,000+ businesses", no fake avatars, no made-up stats.

### CRITICAL (3 issues)
1. **No Dockerfile or entrypoint.sh** — cannot deploy to Railway.
2. **No DATABASE_URL support** — SQLite hardcoded. Production needs PostgreSQL.
3. **Zero tests** — 0% coverage across all apps.

### HIGH (2 issues)
4. **No SECURE_ settings** — missing HSTS, SSL redirect, secure cookies for production.
5. **No roadmap.md or SPRINT.md** — no sprint tracking.

### MEDIUM (2 issues)
6. **No sitemap.xml or robots.txt** — SEO invisible.
7. **Split-key SECRET_KEY pattern** — scanner corruption workaround. Should simplify.

### LOW (1 issue)
8. **Logout URL is hardcoded** — `{% url 'accounts:logout' %}` in base.html but needs allauth logout.

## Phase 1: Production Readiness — Sprint 1
### Tasks
- [ ] Create Dockerfile + entrypoint.sh for Railway
- [ ] Add DATABASE_URL support to settings.py
- [ ] Add SECURE_ settings (HSTS, SSL redirect, secure cookies)
- [ ] TDD: Write tests for posts, billing, accounts
- [ ] Add sitemap.xml + robots.txt
- [ ] Simplify SECRET_KEY (remove split-key pattern)

### Completed
- ✅ Initial audit (2026-04-30)
