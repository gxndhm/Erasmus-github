# ADR-003: Validate Language Compatibility at Session Creation, Not at Scheduling

**Date:** 2026-04-10  
**Status:** Accepted  
**Deciders:** Arman Gandham

---

## Context

Language compatibility between a champion and participant could be enforced at two points:
1. At **scheduling** — when the system suggests available champions
2. At **session creation** — when the session object is instantiated

Option 1 (scheduling-only) relies on the scheduling UI never presenting incompatible champions. Option 2 (session creation) adds a hard invariant check regardless of how the session was initiated.

## Decision

Enforce language compatibility as a **hard invariant at session creation**, raising `MatchingError` if violated, in addition to filtering at the scheduling layer.

## Rationale

This is a defence-in-depth approach. The scheduling layer filters as a convenience; the session creation layer enforces correctness. This is consistent with the **fail-fast** principle: an invalid session should be impossible to create, not just unlikely to be created.

The formal specification (Alloy) proves this property holds across all reachable states. The test suite verifies it with explicit test cases (`test_raises_on_language_mismatch`).

Allowing a session to exist with a language mismatch — even briefly — would violate the core trust-building mission of the platform: a participant unexpectedly assigned a champion who cannot speak their language would reinforce, not reduce, institutional distrust.

## Consequences

- **Positive:** The language compatibility invariant is provably maintained at all system layers.
- **Positive:** Easier to audit — a single place where sessions are validated.
- **Negative:** Slightly more coupling in the `create_session` method. Mitigated by keeping validation logic in the domain layer, not the persistence layer.

---
