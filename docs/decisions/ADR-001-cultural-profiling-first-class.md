# ADR-001: Use Cultural Profiling as a First-Class System Concept

**Date:** 2026-04-01  
**Status:** Accepted  
**Deciders:** Arman Gandham

---

## Context

The system must support users from diverse linguistic and cultural backgrounds, many of whom have low institutional trust in government digital services. Standard user models in digital platforms treat all users uniformly — they track authentication state and preferences, but do not model cultural or trust dimensions.

Without modelling these dimensions explicitly, the matching engine cannot make appropriate champion assignments, the service gateway cannot apply trust-based access control, and the analytics layer cannot produce meaningful exclusion metrics.

## Decision

Cultural profile will be modelled as a **first-class domain object** (`CulturalProfile`), not as a secondary attribute or metadata field. Every `ExcludedAdult` must have a cultural profile before any matching or service access can occur.

The `CulturalProfile` includes: `primary_language`, `english_proficiency`, `institutional_trust_score`, and `ethnicity`. These map directly to the barrier types identified in the article: language barriers, trust barriers, and access barriers.

## Consequences

- **Positive:** The matching engine, trust gateway, and analytics pipeline all have a shared, validated model of each user's cultural context. This avoids implicit assumptions and makes exclusion barriers explicit and measurable.
- **Positive:** ISO 25010 usability assessments can be computed per-user rather than globally, enabling culturally-specific usability scores.
- **Negative:** Onboarding requires completing a cultural profile — adds friction. Mitigated by making the intake form multilingual and champion-assisted.
- **Trade-off:** Collecting ethnicity data requires explicit consent and GDPR-compliant handling.

---
