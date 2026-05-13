# UML Artefact Suite
## Digital Inclusion Platform — System Diagrams

All diagrams use PlantUML syntax. Render at https://plantuml.com/plantuml or paste into any PlantUML-compatible tool.

---

## 1. Class Diagram

```plantuml
@startuml class_diagram
title Digital Inclusion Platform — Class Diagram

skinparam classAttributeIconSize 0
skinparam style strictuml

package "User Domain" {
  abstract class User {
    +id: UUID
    +name: String
    +preferredLanguage: String
    +culturalProfile: CulturalProfile
    +register(): void
    +updateProfile(): void
  }

  class ExcludedAdult extends User {
    +ageGroup: AgeGroup
    +digitalConfidenceLevel: Int
    +communityAffiliation: String
    +assessSkillLevel(): SkillAssessment
  }

  class DigitalChampion extends User {
    +languages: List<String>
    +communityArea: String
    +certifications: List<String>
    +supportSessions: List<Session>
    +scheduleSupportSession(): Session
  }

  class PolicyMaker extends User {
    +organisation: String
    +accessLevel: AccessLevel
    +viewAnalytics(): Report
  }
}

package "Cultural Profile" {
  class CulturalProfile {
    +ethnicity: String
    +primaryLanguage: String
    +englishProficiency: ProficiencyLevel
    +institutionalTrustScore: Float
    +preferredCommunicationStyle: String
  }

  enum ProficiencyLevel {
    NONE
    BASIC
    INTERMEDIATE
    FLUENT
  }
}

package "Service Domain" {
  class DigitalService {
    +id: UUID
    +name: String
    +provider: String
    +supportedLanguages: List<String>
    +accessibilityRating: Float
    +usabilityScore: Float
    +getLocalizedVersion(lang: String): LocalizedService
    +assessCulturalSuitability(profile: CulturalProfile): Float
  }

  class Session {
    +id: UUID
    +champion: DigitalChampion
    +participant: ExcludedAdult
    +service: DigitalService
    +date: DateTime
    +outcome: SessionOutcome
    +trustBuilt: Boolean
    +recordOutcome(): void
  }

  class SkillAssessment {
    +userId: UUID
    +iso25010UsabilityScore: Float
    +barriersIdentified: List<Barrier>
    +recommendedInterventions: List<Intervention>
    +generateReport(): Report
  }
}

package "Analytics" {
  class InclusionReport {
    +region: String
    +period: DateRange
    +exclusionRate: Float
    +demographicBreakdown: Map<String, Float>
    +barrierAnalysis: List<Barrier>
    +generate(): PDF
  }

  class Barrier {
    +type: BarrierType
    +severity: Float
    +affectedGroups: List<String>
  }

  enum BarrierType {
    LANGUAGE
    TRUST
    DEVICE_ACCESS
    CONNECTIVITY
    SKILL
    CULTURAL
  }
}

User "1" --> "1" CulturalProfile
Session "many" --> "1" DigitalChampion
Session "many" --> "1" ExcludedAdult
Session "1" --> "1" DigitalService
ExcludedAdult "1" --> "many" SkillAssessment
InclusionReport "1" --> "many" Barrier

@enduml
```

---

## 2. Sequence Diagram

```plantuml
@startuml sequence_diagram
title Digital Inclusion Onboarding — Sequence Diagram

actor "Excluded Adult" as EA
participant "Library Portal" as LP
participant "Cultural Profiling\nService" as CPS
participant "Matching Engine" as ME
participant "Digital Champion" as DC
participant "Digital Service\n(e.g. NHS Booking)" as DS
database "Analytics DB" as DB

EA -> LP: Arrive at library / access portal
LP -> CPS: Request cultural profile assessment
CPS -> EA: Present multilingual intake form
EA -> CPS: Submit language + community preferences
CPS -> CPS: Calculate institutionalTrustScore
CPS -> DB: Store cultural profile
CPS --> LP: Return CulturalProfile

LP -> ME: Request champion matching
ME -> DB: Query available champions by language + community
ME --> LP: Return matched DigitalChampion

LP -> DC: Notify: new participant assigned
DC -> EA: Schedule support session (preferred language)

loop Support Sessions
  DC -> EA: Guide through target digital service
  EA -> DS: Attempt task (e.g. book appointment)
  DS --> EA: Confirmation / response
  DC -> DB: Log session outcome + trustBuilt flag
end

DB -> DB: Aggregate inclusion metrics
DB --> LP: Update ExcludedAdult.digitalConfidenceLevel

LP --> PolicyMaker: Weekly InclusionReport generated

@enduml
```

---

## 3. State Machine Diagram

```plantuml
@startuml state_machine
title Excluded Adult — Digital Inclusion Journey State Machine

[*] --> Unaware : Person has no digital engagement

state Unaware {
  note: No internet use\nHigh institutional distrust\nNo device access
}

Unaware --> InitialContact : Community champion outreach\nor library visit

state InitialContact {
  note: First touchpoint\nCultural profiling begins\nLanguage preference recorded
}

InitialContact --> SkillAssessment : Intake form completed

state SkillAssessment {
  note: ISO 25010 usability baseline\nBarriers identified\nTrust score measured
}

SkillAssessment --> ActiveSupport : Champion matched\nand sessions scheduled

state ActiveSupport {
  note: Weekly sessions with champion\nTarget service practice\nTrust building underway
  state "Session In Progress" as SIP
  state "Between Sessions" as BES
  SIP --> BES : Session ends
  BES --> SIP : Next session begins
}

ActiveSupport --> SkillsConsolidation : Completes 3+ sessions\nwithout assistance

state SkillsConsolidation {
  note: Independent use of 1+ services\nModerate confidence level\nMay assist others informally
}

SkillsConsolidation --> DigitallyIncluded : Consistent independent\nuse across services

state DigitallyIncluded {
  note: High confidence\nMultiple services used independently\nInstitutional trust established
}

DigitallyIncluded --> DigitalChampionCandidate : Volunteers to support others

state DigitalChampionCandidate {
  note: Champion training programme\nCommunity embedding begins
}

ActiveSupport --> Withdrawn : Drops out (distrust,\nhealth, access barriers)
Withdrawn --> InitialContact : Re-engagement\noutreach

@enduml
```

---

## 4. Use Case Diagram

```plantuml
@startuml use_case
title Digital Inclusion Platform — Use Case Diagram

left to right direction

actor "Excluded Adult" as EA
actor "Digital Champion" as DC
actor "Policy Maker" as PM
actor "Library System" as LS

rectangle "Digital Inclusion Platform" {
  usecase "Complete cultural\nprofile assessment" as UC1
  usecase "View available\ndigital services" as UC2
  usecase "Book support\nsession" as UC3
  usecase "Access service\nwith champion support" as UC4
  usecase "Complete skill\nself-assessment" as UC5
  usecase "Receive multilingual\ncontent" as UC6

  usecase "Manage participant\nprofiles" as UC7
  usecase "Log session\noutcomes" as UC8
  usecase "View inclusion\nmetrics dashboard" as UC9
  usecase "Schedule sessions" as UC10

  usecase "Generate\nregional reports" as UC11
  usecase "View exclusion\nheatmaps" as UC12
  usecase "Export policy\nevidence" as UC13

  usecase "Sync participant\nrecords" as UC14
  usecase "Trigger referrals" as UC15
}

EA --> UC1
EA --> UC2
EA --> UC3
EA --> UC4
EA --> UC5
EA --> UC6

DC --> UC7
DC --> UC8
DC --> UC9
DC --> UC10

PM --> UC11
PM --> UC12
PM --> UC13

LS --> UC14
LS --> UC15

UC4 .> UC6 : <<include>>
UC3 .> UC10 : <<include>>
UC11 .> UC9 : <<extend>>

@enduml
```
