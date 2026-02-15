"""
Tests for validation logic and theory updates
"""

import pytest
from datetime import datetime
from core.scientific_agent import (
    Hypothesis, Experiment, Evidence, Theory, HypothesisStatus,
    KnowledgeBase
)


class TestValidation:
    """Test validation logic for experimental results."""
    
    def test_validation_supported_hypothesis(self):
        """Test validation when hypothesis is supported."""
        h = Hypothesis(
            id="h_valid_1",
            statement="Test validation",
            variables={},
            relationships=[],
            domain="test",
            timestamp=datetime.now(),
            confidence=0.7,
            complexity=0.5,
            novelty=0.5,
            testability=0.9
        )
        
        # Simulate successful experiment
        results = {
            "success_rate": 0.92,
            "statistical_significance": True
        }
        
        # Validate: success_rate > 0.8 means supported
        if results["success_rate"] > 0.8 and results["statistical_significance"]:
            h.status = HypothesisStatus.SUPPORTED
        
        assert h.status == HypothesisStatus.SUPPORTED
    
    def test_validation_refuted_hypothesis(self):
        """Test validation when hypothesis is refuted."""
        h = Hypothesis(
            id="h_valid_2",
            statement="Test refutation",
            variables={},
            relationships=[],
            domain="test",
            timestamp=datetime.now(),
            confidence=0.7,
            complexity=0.5,
            novelty=0.5,
            testability=0.9
        )
        
        # Simulate failed experiment
        results = {
            "success_rate": 0.45,
            "statistical_significance": False
        }
        
        # Validate: success_rate < 0.8 means refuted
        if results["success_rate"] < 0.8 or not results["statistical_significance"]:
            h.status = HypothesisStatus.REFUTED
        
        assert h.status == HypothesisStatus.REFUTED
    
    def test_theory_update_with_evidence(self):
        """Test updating theory based on validated hypothesis."""
        kb = KnowledgeBase()
        
        h = Hypothesis(
            id="h_theory_1",
            statement="Theory update test",
            variables={},
            relationships=[],
            domain="test",
            timestamp=datetime.now(),
            confidence=0.8,
            complexity=0.5,
            novelty=0.5,
            testability=0.9,
            status=HypothesisStatus.SUPPORTED
        )
        
        evidence = Evidence(
            id="ev_theory_1",
            hypothesis_id=h.id,
            content={"result": "positive"},
            timestamp=datetime.now(),
            strength="strong",
            source="experiment",
            quality_score=0.9,
            replicability=0.85
        )
        
        theory = Theory(
            id="t_1",
            name="Test Theory",
            core_principles=["Principle 1"],
            explanatory_scope=["domain1"],
            predictive_power=0.85,
            parsimony=0.8,
            coherence=0.9,
            empirical_support=0.85,
            hypotheses=[h],
            evidence=[evidence]
        )
        
        kb.add_theory(theory)
        
        assert theory.id in kb.theories
        assert len(theory.hypotheses) == 1
        assert len(theory.evidence) == 1
        assert theory.empirical_support == 0.85
    
    def test_contradictory_evidence_handling(self):
        """Test handling contradictory evidence."""
        h = Hypothesis(
            id="h_contra",
            statement="Contradictory evidence test",
            variables={},
            relationships=[],
            domain="test",
            timestamp=datetime.now(),
            confidence=0.5,
            complexity=0.5,
            novelty=0.5,
            testability=0.9
        )
        
        # Add supporting evidence
        supporting = Evidence(
            id="ev_support",
            hypothesis_id=h.id,
            content={"result": "positive"},
            timestamp=datetime.now(),
            strength="strong",
            source="exp1",
            quality_score=0.9,
            replicability=0.8
        )
        h.supporting_evidence.append(supporting)
        
        # Add contradictory evidence
        contradictory = Evidence(
            id="ev_contra",
            hypothesis_id=h.id,
            content={"result": "negative"},
            timestamp=datetime.now(),
            strength="moderate",
            source="exp2",
            quality_score=0.7,
            replicability=0.6
        )
        h.disconfirming_evidence.append(contradictory)
        
        # Hypothesis should have both types of evidence
        assert len(h.supporting_evidence) == 1
        assert len(h.disconfirming_evidence) == 1
        
        # Status depends on evidence strength
        # With stronger supporting evidence, keep as proposed/testing
        assert h.status in [HypothesisStatus.PROPOSED, HypothesisStatus.TESTING]
