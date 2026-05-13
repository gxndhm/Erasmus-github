# ISO 25010 Quality Traceability Matrix
## Digital Inclusion Platform — Quality Characteristics

This document maps every major feature of the Digital Inclusion Platform to a specific ISO 25010 quality sub-characteristic, with rationale grounded in the article's argument.

---

## ISO 25010 Product Quality Model Reference

```
Functional Suitability    → Completeness, Correctness, Appropriateness
Performance Efficiency    → Time Behaviour, Resource Utilisation, Capacity
Compatibility             → Co-existence, Interoperability
Usability                 → Learnability, Operability, User Error Protection,
                           User Interface Aesthetics, Accessibility
Reliability               → Maturity, Availability, Fault Tolerance, Recoverability
Security                  → Confidentiality, Integrity, Non-repudiation, Authenticity
Maintainability           → Modularity, Reusability, Analysability, Modifiability, Testability
Portability               → Adaptability, Installability, Replaceability
```

---

## Traceability Matrix

| # | Feature | ISO 25010 Characteristic | Sub-characteristic | Rationale |
|---|---------|--------------------------|-------------------|-----------|
| F-01 | Multilingual intake form | Usability | **Accessibility** | Participants with non-English primary languages cannot complete an English-only form. Accessibility here is not optional — it is the entry point to inclusion. |
| F-02 | Cultural profiling at onboarding | Usability | **Learnability** | Understanding a user's language proficiency and trust score enables the system to calibrate content and pacing. Low-learnability systems exclude low-confidence users. |
| F-03 | Language-compatible champion matching | Functional Suitability | **Appropriateness** | The system must match participants to champions who can actually communicate with them. An inappropriate match (language mismatch) defeats the entire purpose of the session. |
| F-04 | Trust-gated service access | Security | **Integrity** | Forcing a low-trust user into a high-friction government service before trust is established risks reinforcing distrust. Trust gating preserves the integrity of the inclusion journey. |
| F-05 | Session outcome logging | Reliability | **Maturity** | Logging outcomes allows the system to learn from failures and improve matching quality over time. Mature systems improve; immature ones repeat failures. |
| F-06 | Trust score progression after sessions | Functional Suitability | **Correctness** | The trust level must correctly reflect a user's accumulated positive interactions. Incorrect progression (e.g., not advancing after successful sessions) would misrepresent the user's readiness. |
| F-07 | ISO 25010 usability scoring per service | Usability | **User Error Protection** | Scoring services for usability per cultural profile helps route participants away from services with high error risk for their profile, preventing discouraging failures. |
| F-08 | Regional inclusion reports for policy makers | Functional Suitability | **Completeness** | Policy makers need complete, demographically broken-down data to identify and address exclusion gaps. Incomplete reporting leads to incomplete policy responses. |
| F-09 | GDPR-compliant data handling | Security | **Confidentiality** | Cultural profile data (ethnicity, language, trust score) is sensitive personal data. Confidentiality is a legal requirement and a trust prerequisite — participants must believe their data is protected. |
| F-10 | Modular domain layer (User, Session, Service) | Maintainability | **Modularity** | Separating concerns into distinct domain objects (as per ADR-001) ensures the system can evolve — e.g., adding new cultural dimensions — without cascading changes. |
| F-11 | Formal verification of core invariants | Reliability | **Fault Tolerance** | Alloy-verified invariants (language compatibility, trust gating) mean the system structurally cannot enter invalid states, regardless of upstream errors or unexpected inputs. |
| F-12 | CI/CD with ≥80% test coverage | Maintainability | **Testability** | Automated tests with coverage enforcement ensure that changes to the system are safe and that regressions are caught before deployment. |
| F-13 | Champion briefing documents in local languages | Usability | **User Interface Aesthetics** | Champions must be able to present the platform naturally in participants' cultural and linguistic contexts. Material that does not match the champion's or participant's register reduces engagement. |
| F-14 | Performance benchmarks for matching engine | Performance Efficiency | **Time Behaviour** | The matching engine must return results quickly enough for real-time use during in-person library sessions. Latency that requires the champion to wait undermines the session flow. |
| F-15 | Re-engagement pathway for withdrawn participants | Reliability | **Recoverability** | Participants who withdraw must be recoverable into the system without losing their trust history. Losing progress is a barrier to re-engagement. |

---

## Coverage Summary

| ISO 25010 Characteristic | Features Mapped |
|---|---|
| Functional Suitability | F-03, F-06, F-08 |
| Performance Efficiency | F-14 |
| Usability | F-01, F-02, F-07, F-13 |
| Reliability | F-05, F-11, F-15 |
| Security | F-04, F-09 |
| Maintainability | F-10, F-12 |
| Compatibility | *(not yet implemented — future: NHS API integration)* |
| Portability | *(not yet implemented — future: mobile-first deployment)* |

---

## Connection to Article Argument

The article identifies three structural failures in UK digital inclusion policy:
1. **Language barriers** → F-01, F-02, F-03, F-13 (Usability: Accessibility, Learnability)
2. **Institutional trust barriers** → F-04, F-06, F-09 (Security: Integrity, Confidentiality)
3. **Design exclusion (deficit model)** → F-07, F-08, F-11 (Reliability: Fault Tolerance; Functional Suitability: Completeness)

Every feature in this matrix is a software engineering response to a documented real-world exclusion mechanism.
