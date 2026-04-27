# Product Manager Feedback

## Product clarity gaps
- Core user outcome is not explicit yet: what concrete artifact is produced after a run (JSON, CSV, database row, API payload).
- Definition of done for a scrape run is unclear (success threshold, latency target, deduplication policy, storage policy).

## Recommended product definition
- **North-star output**: daily normalized bid records.
- **Core KPI set**:
  - scrape success rate (% valid pages found)
  - extraction completeness (% required fields present)
  - duplicate rate
  - end-to-end run duration
  - cost per 1,000 pages

## User-facing priorities
1. Reliable daily run
2. Traceable outputs (run ID, logs, failed URLs, retry counts)
3. Simple consumption path (CSV first, optional DB sink)

## Proposed roadmap

### Phase 0 (Week 1) — Stabilization
- Fix dependency metadata and command mismatches
- Align naming/docs across package
- Enforce Python version in dev + CI
- Add CI gates: lint, tests, minimal coverage threshold

### Phase 1 (Weeks 2–4) — Reliability MVP
- Add scrape result model (`status`, `url`, `error_code`, `latency_ms`, `content`)
- Add retry/backoff and timeout policy
- Add persistent output (`jsonl`/`csv`) with run manifest
- Add structured logging per URL

### Phase 2 (Month 2) — Scale and quality
- Implement bounded worker pool and browser/session reuse
- Add deduplication and checkpoint resume
- Improve parser coverage and validation rules
- Add integration test lane with Selenium container

### Phase 3 (Month 3) — Productization
- Add scheduler mode (cron/container job)
- Add metrics dashboard (success/failure trend)
- Add storage adapters (local file + optional Postgres)
- Publish v1 docs with examples and troubleshooting

## Suggested next sprint backlog
1. Dependency/packaging correctness
2. Docker runtime command and path validation
3. Production command path cleanup
4. `ScrapeResult` model + structured logs
5. 8–12 focused tests for failure/edge cases
