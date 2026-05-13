# BDD Feature Files — Digital Inclusion Platform
## Gherkin Given/When/Then format

These scenarios translate the article's core arguments into verifiable system behaviours.
Each scenario maps to a claim made in the published article.

---

## Feature: Champion Matching

```gherkin
Feature: Language-compatible champion matching
  As an excluded adult with a non-English primary language
  I want to be matched with a champion who speaks my language
  So that I can receive support in a language I am comfortable with

  Background:
    Given the platform has the following champions available:
      | Name       | Languages          | Community Area |
      | Fatima K   | Urdu, English      | Sparkhill      |
      | David M    | English            | Edgbaston      |
      | Amina H    | Somali, English    | Handsworth     |

  Scenario: Urdu-speaking adult is matched to Urdu-speaking champion
    Given I am an excluded adult with primary language "Urdu"
    And I have completed my cultural profile
    When the system runs champion matching
    Then I should be matched with "Fatima K"
    And the session language should be "Urdu"

  Scenario: English-speaking adult is matched to available English champion
    Given I am an excluded adult with primary language "English"
    And I have completed my cultural profile
    When the system runs champion matching
    Then I should be matched with a champion who speaks "English"

  Scenario: Adult with no available language match receives an error
    Given I am an excluded adult with primary language "Bengali"
    And I have completed my cultural profile
    When the system runs champion matching
    Then the system should return an error "No champion available for language: Bengali"
    And the platform should log this as an unmet language need

  Scenario: Adult without a cultural profile cannot be matched
    Given I am an excluded adult
    And I have not completed my cultural profile
    When the system attempts champion matching
    Then the system should return an error "Adult must have a cultural profile before matching."
```

---

## Feature: Trust-Gated Service Access

```gherkin
Feature: Trust-gated access to digital services
  As a digital inclusion platform
  I want to gate access to high-trust services by participant trust level
  So that participants are not prematurely exposed to services that reinforce distrust

  Background:
    Given the following digital services exist:
      | Service Name               | Trust Required |
      | NHS Appointment Booking    | LOW            |
      | Pension Credit Application | MEDIUM         |
      | Universal Credit Portal    | HIGH           |

  Scenario: Low-trust participant can access low-trust service
    Given I am an excluded adult with trust level "LOW"
    When I attempt to access "NHS Appointment Booking"
    Then access should be granted
    And the session should be created successfully

  Scenario: Low-trust participant cannot access high-trust service
    Given I am an excluded adult with trust level "LOW"
    When I attempt to access "Universal Credit Portal"
    Then access should be denied
    And the system should suggest starting with "NHS Appointment Booking"

  Scenario: Trust level increases after successful session
    Given I am an excluded adult with trust level "LOW"
    And I complete a session with outcome "SUCCESSFUL"
    When the system updates my trust score
    Then my trust level should be "MEDIUM"

  Scenario: Trust level does not increase after unsuccessful session
    Given I am an excluded adult with trust level "LOW"
    And I complete a session with outcome "UNSUCCESSFUL"
    When the system updates my trust score
    Then my trust level should remain "LOW"

  Scenario: Trust level is capped at HIGH
    Given I am an excluded adult with trust level "HIGH"
    And I complete a session with outcome "SUCCESSFUL"
    When the system updates my trust score
    Then my trust level should remain "HIGH"
```

---

## Feature: Cultural Profile Assessment

```gherkin
Feature: Multilingual cultural profile intake
  As an excluded adult arriving at a library session
  I want to complete my profile in my primary language
  So that the system understands my barriers and assigns appropriate support

  Scenario: Adult completes profile in Urdu
    Given I am an adult with primary language "Urdu"
    When I access the intake form
    Then the intake form should be presented in "Urdu"
    And I should be able to complete all fields without requiring English

  Scenario: Profile records institutional trust score
    Given I am completing my cultural profile
    When I answer that I have had negative experiences with government services
    Then my institutional trust score should be recorded as below 0.3

  Scenario: Language barrier is automatically detected
    Given I am an adult with primary language "Punjabi"
    And my English proficiency is "none"
    When my cultural profile is created
    Then "LanguageBarrier" should be in my barriers list

  Scenario: Profile is required before any service access
    Given I am an adult who has not completed a cultural profile
    When I attempt to access any digital service
    Then access should be denied with message "Complete your cultural profile first"
```

---

## Feature: Inclusion Analytics for Policy Makers

```gherkin
Feature: Regional inclusion reporting
  As a policy maker
  I want to view demographic exclusion data by region
  So that I can identify underserved communities and allocate resources

  Scenario: Policy maker views Birmingham exclusion heatmap
    Given the system has session data for the past 6 months
    When I request an inclusion report for "Birmingham"
    Then the report should include exclusion rates broken down by:
      | Dimension          |
      | Primary language   |
      | Age group          |
      | Barrier type       |
    And the report should identify the top 3 unmet language needs

  Scenario: Unmet language needs are flagged automatically
    Given no champion speaks "Somali"
    And 12 adults with primary language "Somali" have attempted matching this month
    When the weekly analytics job runs
    Then an alert should be generated: "Unmet language need: Somali (12 participants)"
    And the alert should be visible on the policy maker dashboard
```
