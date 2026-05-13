"""
Digital Inclusion Platform — Automated Test Suite
pytest · Target: 80%+ line coverage

Run: pytest tests/ --cov=src --cov-report=term-missing
"""

import pytest
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from uuid import uuid4


# ============================================================
# Domain models (src/models.py equivalent inline for tests)
# ============================================================

class TrustLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class BarrierType(Enum):
    LANGUAGE = "language"
    TRUST = "trust"
    DEVICE = "device"
    SKILL = "skill"
    CULTURAL = "cultural"


class SessionOutcome(Enum):
    SUCCESSFUL = "successful"
    PARTIAL = "partial"
    UNSUCCESSFUL = "unsuccessful"


@dataclass
class CulturalProfile:
    primary_language: str
    english_proficiency: str  # none | basic | intermediate | fluent
    institutional_trust_score: float  # 0.0–1.0
    ethnicity: str = ""


@dataclass
class ExcludedAdult:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    cultural_profile: Optional[CulturalProfile] = None
    trust_score: TrustLevel = TrustLevel.LOW
    barriers: List[BarrierType] = field(default_factory=list)
    digital_confidence: int = 0  # 0–10


@dataclass
class DigitalChampion:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    languages: List[str] = field(default_factory=list)
    community_area: str = ""


@dataclass
class DigitalService:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    supported_languages: List[str] = field(default_factory=list)
    trust_required: TrustLevel = TrustLevel.LOW
    usability_score: float = 0.0  # ISO 25010


@dataclass
class SupportSession:
    champion: DigitalChampion
    participant: ExcludedAdult
    service: DigitalService
    outcome: Optional[SessionOutcome] = None


# ============================================================
# Business logic (src/matching.py equivalent)
# ============================================================

class MatchingError(Exception):
    pass


class InclusionPlatform:

    def match_champion(
        self, adult: ExcludedAdult, champions: List[DigitalChampion]
    ) -> DigitalChampion:
        """Match an excluded adult to a language-compatible champion."""
        if not adult.cultural_profile:
            raise MatchingError("Adult must have a cultural profile before matching.")
        lang = adult.cultural_profile.primary_language
        compatible = [c for c in champions if lang in c.languages]
        if not compatible:
            raise MatchingError(f"No champion available for language: {lang}")
        return compatible[0]

    def can_access_service(self, adult: ExcludedAdult, service: DigitalService) -> bool:
        """Check if an adult's trust level is sufficient for a service."""
        return adult.trust_score.value >= service.trust_required.value

    def create_session(
        self,
        adult: ExcludedAdult,
        champion: DigitalChampion,
        service: DigitalService,
    ) -> SupportSession:
        """Create a validated support session."""
        if not adult.cultural_profile:
            raise MatchingError("Adult must have a cultural profile.")
        lang = adult.cultural_profile.primary_language
        if lang not in champion.languages:
            raise MatchingError("Language mismatch: champion cannot support this participant.")
        if not self.can_access_service(adult, service):
            raise MatchingError("Trust level insufficient for this service.")
        return SupportSession(champion=champion, participant=adult, service=service)

    def update_trust_after_session(
        self, adult: ExcludedAdult, outcome: SessionOutcome
    ) -> ExcludedAdult:
        """Update trust score based on session outcome."""
        if outcome == SessionOutcome.SUCCESSFUL:
            current = adult.trust_score.value
            if current < TrustLevel.HIGH.value:
                adult.trust_score = TrustLevel(current + 1)
        return adult

    def assess_iso25010_usability(self, service: DigitalService, profile: CulturalProfile) -> dict:
        """Score a service against ISO 25010 usability sub-characteristics for a user profile."""
        lang_score = 1.0 if profile.primary_language in service.supported_languages else 0.0
        trust_score = profile.institutional_trust_score
        overall = (lang_score * 0.5 + trust_score * 0.5) * service.usability_score
        return {
            "learnability": lang_score,
            "trust_alignment": trust_score,
            "overall_usability": round(overall, 3),
        }


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def platform():
    return InclusionPlatform()


@pytest.fixture
def urdu_adult():
    return ExcludedAdult(
        name="Test Participant",
        cultural_profile=CulturalProfile(
            primary_language="Urdu",
            english_proficiency="basic",
            institutional_trust_score=0.2,
            ethnicity="Pakistani",
        ),
        trust_score=TrustLevel.LOW,
        barriers=[BarrierType.LANGUAGE, BarrierType.TRUST],
    )


@pytest.fixture
def english_adult():
    return ExcludedAdult(
        name="English Speaker",
        cultural_profile=CulturalProfile(
            primary_language="English",
            english_proficiency="fluent",
            institutional_trust_score=0.5,
        ),
        trust_score=TrustLevel.MEDIUM,
    )


@pytest.fixture
def urdu_champion():
    return DigitalChampion(
        name="Champion A",
        languages=["Urdu", "English"],
        community_area="Sparkhill",
    )


@pytest.fixture
def english_only_champion():
    return DigitalChampion(
        name="Champion B",
        languages=["English"],
        community_area="Edgbaston",
    )


@pytest.fixture
def nhs_service():
    return DigitalService(
        name="NHS Appointment Booking",
        supported_languages=["English", "Urdu"],
        trust_required=TrustLevel.LOW,
        usability_score=0.7,
    )


@pytest.fixture
def gov_service_high_trust():
    return DigitalService(
        name="Universal Credit Portal",
        supported_languages=["English"],
        trust_required=TrustLevel.HIGH,
        usability_score=0.5,
    )


# ============================================================
# TESTS: Champion Matching
# ============================================================

class TestChampionMatching:

    def test_matches_champion_by_language(self, platform, urdu_adult, urdu_champion, english_only_champion):
        matched = platform.match_champion(urdu_adult, [english_only_champion, urdu_champion])
        assert matched == urdu_champion

    def test_raises_when_no_language_match(self, platform, urdu_adult, english_only_champion):
        with pytest.raises(MatchingError, match="No champion available for language: Urdu"):
            platform.match_champion(urdu_adult, [english_only_champion])

    def test_raises_when_no_cultural_profile(self, platform, urdu_champion):
        adult_no_profile = ExcludedAdult(name="No Profile")
        with pytest.raises(MatchingError, match="cultural profile"):
            platform.match_champion(adult_no_profile, [urdu_champion])

    def test_returns_first_compatible_champion(self, platform, urdu_adult):
        c1 = DigitalChampion(name="C1", languages=["Urdu"])
        c2 = DigitalChampion(name="C2", languages=["Urdu"])
        result = platform.match_champion(urdu_adult, [c1, c2])
        assert result == c1


# ============================================================
# TESTS: Service Access (Trust Gating)
# ============================================================

class TestServiceAccess:

    def test_low_trust_can_access_low_trust_service(self, platform, urdu_adult, nhs_service):
        assert platform.can_access_service(urdu_adult, nhs_service) is True

    def test_low_trust_cannot_access_high_trust_service(self, platform, urdu_adult, gov_service_high_trust):
        assert platform.can_access_service(urdu_adult, gov_service_high_trust) is False

    def test_medium_trust_can_access_medium_service(self, platform, english_adult):
        service = DigitalService(name="Pension Portal", trust_required=TrustLevel.MEDIUM)
        assert platform.can_access_service(english_adult, service) is True

    def test_high_trust_can_access_all_services(self, platform, nhs_service, gov_service_high_trust):
        high_trust_adult = ExcludedAdult(trust_score=TrustLevel.HIGH)
        assert platform.can_access_service(high_trust_adult, nhs_service) is True
        assert platform.can_access_service(high_trust_adult, gov_service_high_trust) is True


# ============================================================
# TESTS: Session Creation
# ============================================================

class TestSessionCreation:

    def test_creates_valid_session(self, platform, urdu_adult, urdu_champion, nhs_service):
        session = platform.create_session(urdu_adult, urdu_champion, nhs_service)
        assert session.participant == urdu_adult
        assert session.champion == urdu_champion
        assert session.service == nhs_service
        assert session.outcome is None

    def test_raises_on_language_mismatch(self, platform, urdu_adult, english_only_champion, nhs_service):
        with pytest.raises(MatchingError, match="Language mismatch"):
            platform.create_session(urdu_adult, english_only_champion, nhs_service)

    def test_raises_on_trust_insufficient(self, platform, urdu_adult, urdu_champion, gov_service_high_trust):
        with pytest.raises(MatchingError, match="Trust level insufficient"):
            platform.create_session(urdu_adult, urdu_champion, gov_service_high_trust)

    def test_raises_when_no_profile(self, platform, urdu_champion, nhs_service):
        adult = ExcludedAdult(name="No Profile")
        with pytest.raises(MatchingError):
            platform.create_session(adult, urdu_champion, nhs_service)


# ============================================================
# TESTS: Trust Progression
# ============================================================

class TestTrustProgression:

    def test_successful_session_increases_trust(self, platform, urdu_adult):
        assert urdu_adult.trust_score == TrustLevel.LOW
        updated = platform.update_trust_after_session(urdu_adult, SessionOutcome.SUCCESSFUL)
        assert updated.trust_score == TrustLevel.MEDIUM

    def test_partial_session_does_not_change_trust(self, platform, urdu_adult):
        updated = platform.update_trust_after_session(urdu_adult, SessionOutcome.PARTIAL)
        assert updated.trust_score == TrustLevel.LOW

    def test_unsuccessful_session_does_not_change_trust(self, platform, urdu_adult):
        updated = platform.update_trust_after_session(urdu_adult, SessionOutcome.UNSUCCESSFUL)
        assert updated.trust_score == TrustLevel.LOW

    def test_trust_caps_at_high(self, platform):
        high_trust_adult = ExcludedAdult(trust_score=TrustLevel.HIGH)
        updated = platform.update_trust_after_session(high_trust_adult, SessionOutcome.SUCCESSFUL)
        assert updated.trust_score == TrustLevel.HIGH

    def test_two_successful_sessions_reach_high_trust(self, platform, urdu_adult):
        platform.update_trust_after_session(urdu_adult, SessionOutcome.SUCCESSFUL)
        platform.update_trust_after_session(urdu_adult, SessionOutcome.SUCCESSFUL)
        assert urdu_adult.trust_score == TrustLevel.HIGH


# ============================================================
# TESTS: ISO 25010 Usability Assessment
# ============================================================

class TestISO25010Assessment:

    def test_full_language_support_scores_learnability_1(self, platform, nhs_service):
        profile = CulturalProfile(
            primary_language="Urdu",
            english_proficiency="basic",
            institutional_trust_score=1.0,
        )
        result = platform.assess_iso25010_usability(nhs_service, profile)
        assert result["learnability"] == 1.0

    def test_unsupported_language_scores_learnability_0(self, platform, nhs_service):
        profile = CulturalProfile(
            primary_language="Somali",
            english_proficiency="none",
            institutional_trust_score=0.5,
        )
        result = platform.assess_iso25010_usability(nhs_service, profile)
        assert result["learnability"] == 0.0

    def test_trust_alignment_reflects_profile_score(self, platform, nhs_service):
        profile = CulturalProfile(
            primary_language="English",
            english_proficiency="fluent",
            institutional_trust_score=0.3,
        )
        result = platform.assess_iso25010_usability(nhs_service, profile)
        assert result["trust_alignment"] == 0.3

    def test_overall_usability_is_bounded(self, platform, nhs_service):
        profile = CulturalProfile(
            primary_language="English",
            english_proficiency="fluent",
            institutional_trust_score=1.0,
        )
        result = platform.assess_iso25010_usability(nhs_service, profile)
        assert 0.0 <= result["overall_usability"] <= 1.0
