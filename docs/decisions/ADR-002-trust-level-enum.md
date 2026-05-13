# ADR-002: Trust Level as an Enum with Ordinal Comparison

**Date:** 2026-04-05  
**Status:** Accepted  
**Deciders:** Arman Gandham

---

## Context

The system gates access to digital services based on a participant's institutional trust level. We need to compare trust levels (e.g. "is this user's trust sufficient for this service?") and progress them over time as sessions succeed.

Two options considered:
1. Model trust as a continuous float (0.0–1.0)
2. Model trust as a discrete enum: `LOW | MEDIUM | HIGH`

## Decision

Use a **discrete enum** with ordinal integer values (`LOW=1, MEDIUM=2, HIGH=3`) rather than a continuous float.

## Rationale

- Ordinal comparison (`adult.trust_score.value >= service.trust_required.value`) is simple, readable, and directly testable.
- Discrete levels map to real-world intervention stages: LOW (first contact), MEDIUM (active support), HIGH (independent use). A float would create false precision — we cannot meaningfully distinguish trust score 0.62 from 0.64.
- Progression is clear: one successful session advances the level by one step. This mirrors the incremental trust-building model described in the article.
- Discrete levels are easier to explain to non-technical stakeholders (champions, policy makers) and to surface in dashboards.

## Consequences

- **Positive:** Simple, auditable trust progression logic. Easy to unit test.
- **Positive:** Policy makers can set trust thresholds per service using plain language (e.g. "this service requires MEDIUM trust").
- **Negative:** Loses granularity — two participants both at LOW could have very different trust profiles. Mitigated by retaining `institutional_trust_score` (float) in `CulturalProfile` for analytics purposes; the enum governs access control only.

---
