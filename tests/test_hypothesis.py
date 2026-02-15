"""
Tests for Hypothesis class and related functionality
"""

import pytest
from datetime import datetime
from core.scientific_agent import Hypothesis, HypothesisStatus, Evidence


class TestHypothesis:
    """Test hypothesis creation and status transitions."""
    
    def test_hypothesis_creation_with_all_fields(self):
        """Test creating a hypothesis with all required fields."""
        h = Hypothesis(
            id="h_test_1",
            statement="Test hypothesis statement",
            variables={"var1": "value1"},
            relationships=["rel1"],
            domain="test_domain",
            timestamp=datetime.now(),
            confidence=0.8,
            complexity=0.5,
            novelty=0.6,
            testability=0.9
        )
        
        assert h.id == "h_test_1"
        assert h.statement == "Test hypothesis statement"
        assert h.confidence == 0.8
        assert h.status == HypothesisStatus.PROPOSED
        assert len(h.supporting_evidence) == 0
        assert len(h.disconfirming_evidence) == 0
    
    def test_hypothesis_status_transitions(self):
        """Test hypothesis status transitions through the workflow."""
        h = Hypothesis(
            id="h_test_2",
            statement="Status transition test",
            variables={},
            relationships=[],
            domain="test",
            timestamp=datetime.now(),
            confidence=0.5,
            complexity=0.5,
            novelty=0.5,
            testability=0.5
        )
        
        # Initial status
        assert h.status == HypothesisStatus.PROPOSED
        
        # Transition to testing
        h.status = HypothesisStatus.TESTING
        assert h.status == HypothesisStatus.TESTING
        
        # Transition to supported
        h.status = HypothesisStatus.SUPPORTED
        assert h.status == HypothesisStatus.SUPPORTED
    
    def test_hypothesis_refuted_status(self):
        """Test hypothesis refutation workflow."""
        h = Hypothesis(
            id="h_test_3",
            statement="Refuted hypothesis",
            variables={},
            relationships=[],
            domain="test",
            timestamp=datetime.now(),
            confidence=0.5,
            complexity=0.5,
            novelty=0.5,
            testability=0.5
        )
        
        h.status = HypothesisStatus.TESTING
        h.status = HypothesisStatus.REFUTED
        assert h.status == HypothesisStatus.REFUTED
    
    def test_hypothesis_with_evidence(self):
        """Test adding supporting and disconfirming evidence."""
        h = Hypothesis(
            id="h_test_4",
            statement="Hypothesis with evidence",
            variables={},
            relationships=[],
            domain="test",
            timestamp=datetime.now(),
            confidence=0.5,
            complexity=0.5,
            novelty=0.5,
            testability=0.5
        )
        
        # Add supporting evidence
        supporting = Evidence(
            id="ev_support_1",
            hypothesis_id=h.id,
            content={"result": "positive"},
            timestamp=datetime.now(),
            strength="strong",
            source="test_source",
            quality_score=0.9,
            replicability=0.8
        )
        h.supporting_evidence.append(supporting)
        
        # Add disconfirming evidence
        disconfirming = Evidence(
            id="ev_disconfirm_1",
            hypothesis_id=h.id,
            content={"result": "negative"},
            timestamp=datetime.now(),
            strength="weak",
            source="test_source",
            quality_score=0.6,
            replicability=0.5
        )
        h.disconfirming_evidence.append(disconfirming)
        
        assert len(h.supporting_evidence) == 1
        assert len(h.disconfirming_evidence) == 1
        assert h.supporting_evidence[0].strength == "strong"
        assert h.disconfirming_evidence[0].strength == "weak"
    
    def test_invalid_hypothesis_missing_fields(self):
        """Test that creating a hypothesis without required fields raises error."""
        with pytest.raises(TypeError):
            # Missing required fields should raise TypeError
            Hypothesis(
                id="h_invalid",
                statement="Incomplete hypothesis"
            )
    
    def test_hypothesis_confidence_bounds(self):
        """Test that confidence values are within valid range."""
        h = Hypothesis(
            id="h_test_5",
            statement="Confidence test",
            variables={},
            relationships=[],
            domain="test",
            timestamp=datetime.now(),
            confidence=0.0,  # Minimum
            complexity=0.5,
            novelty=0.5,
            testability=1.0  # Maximum
        )
        
        assert 0.0 <= h.confidence <= 1.0
        assert 0.0 <= h.testability <= 1.0
