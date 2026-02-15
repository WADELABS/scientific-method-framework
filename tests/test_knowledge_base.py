"""
Tests for KnowledgeBase functionality
"""

import pytest
from datetime import datetime
from core.scientific_agent import (
    KnowledgeBase, Hypothesis, Theory, Evidence, Experiment
)


class TestKnowledgeBase:
    """Test KnowledgeBase storage and retrieval."""
    
    def test_knowledge_base_initialization(self):
        """Test creating an empty knowledge base."""
        kb = KnowledgeBase()
        
        assert len(kb.hypotheses) == 0
        assert len(kb.theories) == 0
        assert len(kb.evidence) == 0
        assert len(kb.experiments) == 0
    
    def test_add_hypothesis(self):
        """Test adding a hypothesis to the knowledge base."""
        kb = KnowledgeBase()
        
        h = Hypothesis(
            id="h_kb_1",
            statement="Test hypothesis",
            variables={},
            relationships=[],
            domain="test",
            timestamp=datetime.now(),
            confidence=0.7,
            complexity=0.5,
            novelty=0.5,
            testability=0.9
        )
        
        kb.add_hypothesis(h)
        
        assert h.id in kb.hypotheses
        assert kb.hypotheses[h.id] == h
        assert len(kb.hypotheses) == 1
    
    def test_add_multiple_hypotheses(self):
        """Test adding multiple hypotheses."""
        kb = KnowledgeBase()
        
        h1 = Hypothesis(
            id="h_kb_2",
            statement="First hypothesis",
            variables={},
            relationships=[],
            domain="test",
            timestamp=datetime.now(),
            confidence=0.7,
            complexity=0.5,
            novelty=0.5,
            testability=0.9
        )
        
        h2 = Hypothesis(
            id="h_kb_3",
            statement="Second hypothesis",
            variables={},
            relationships=[],
            domain="test",
            timestamp=datetime.now(),
            confidence=0.6,
            complexity=0.4,
            novelty=0.7,
            testability=0.8
        )
        
        kb.add_hypothesis(h1)
        kb.add_hypothesis(h2)
        
        assert len(kb.hypotheses) == 2
        assert h1.id in kb.hypotheses
        assert h2.id in kb.hypotheses
    
    def test_retrieve_hypothesis(self):
        """Test retrieving a hypothesis by ID."""
        kb = KnowledgeBase()
        
        h = Hypothesis(
            id="h_kb_4",
            statement="Retrieve test",
            variables={},
            relationships=[],
            domain="test",
            timestamp=datetime.now(),
            confidence=0.7,
            complexity=0.5,
            novelty=0.5,
            testability=0.9
        )
        
        kb.add_hypothesis(h)
        retrieved = kb.hypotheses.get("h_kb_4")
        
        assert retrieved is not None
        assert retrieved.id == h.id
        assert retrieved.statement == h.statement
    
    def test_add_theory(self):
        """Test adding a theory to the knowledge base."""
        kb = KnowledgeBase()
        
        h = Hypothesis(
            id="h_theory",
            statement="Theory hypothesis",
            variables={},
            relationships=[],
            domain="test",
            timestamp=datetime.now(),
            confidence=0.8,
            complexity=0.5,
            novelty=0.5,
            testability=0.9
        )
        
        theory = Theory(
            id="t_kb_1",
            name="Test Theory",
            core_principles=["Principle 1", "Principle 2"],
            explanatory_scope=["domain1", "domain2"],
            predictive_power=0.85,
            parsimony=0.8,
            coherence=0.9,
            empirical_support=0.80,
            hypotheses=[h],
            evidence=[]
        )
        
        kb.add_theory(theory)
        
        assert theory.id in kb.theories
        assert kb.theories[theory.id] == theory
        assert len(kb.theories) == 1
    
    def test_knowledge_base_with_experiments(self):
        """Test storing experiments in knowledge base."""
        kb = KnowledgeBase()
        
        exp = Experiment(
            id="exp_kb_1",
            hypothesis_id="h_test",
            design={},
            conditions=[],
            controls=[],
            measurements=[],
            sample_size=100,
            randomization_procedure="random",
            statistical_tests=[]
        )
        
        kb.experiments[exp.id] = exp
        
        assert exp.id in kb.experiments
        assert len(kb.experiments) == 1
    
    def test_knowledge_base_with_evidence(self):
        """Test storing evidence in knowledge base."""
        kb = KnowledgeBase()
        
        evidence = Evidence(
            id="ev_kb_1",
            hypothesis_id="h_test",
            content={"data": "test"},
            timestamp=datetime.now(),
            strength="strong",
            source="experiment",
            quality_score=0.9,
            replicability=0.85
        )
        
        kb.evidence[evidence.id] = evidence
        
        assert evidence.id in kb.evidence
        assert len(kb.evidence) == 1
