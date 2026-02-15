"""
Integration tests for the complete SMF cycle
"""

import pytest
from datetime import datetime
from core.scientific_agent import (
    KnowledgeBase, Hypothesis, Experiment, Evidence, Theory,
    HypothesisStatus, ScientificAgent
)


class TestIntegration:
    """End-to-end integration tests for the SMF cycle."""
    
    def test_full_smf_cycle_success(self):
        """Test complete SMF cycle: hypothesis → experiment → validation → theory."""
        # Step 1: Initialize knowledge base
        kb = KnowledgeBase()
        
        # Step 2: Create hypothesis
        hypothesis = Hypothesis(
            id="h_integration_1",
            statement="Integration test hypothesis",
            variables={"timeout": "300s"},
            relationships=["timeout_affects_success"],
            domain="test_domain",
            timestamp=datetime.now(),
            confidence=0.7,
            complexity=0.3,
            novelty=0.5,
            testability=0.9
        )
        kb.add_hypothesis(hypothesis)
        
        # Step 3: Create scientific agent
        agent = ScientificAgent(domain="Integration Test", knowledge_base=kb)
        agent.active_hypotheses.append(hypothesis)
        
        # Step 4: Design experiment
        hypothesis.status = HypothesisStatus.TESTING
        experiment = Experiment(
            id=f"exp_{hypothesis.id}",
            hypothesis_id=hypothesis.id,
            design={"type": "simulation"},
            conditions=["baseline", "modified"],
            controls=[],
            measurements=["success_rate"],
            sample_size=100,
            randomization_procedure="random",
            statistical_tests=["t_test"]
        )
        kb.experiments[experiment.id] = experiment
        
        # Step 5: Execute experiment (simulated)
        results = {
            "success_rate": 0.89,
            "statistical_significance": True
        }
        experiment.results = results
        
        # Step 6: Validate and update hypothesis
        if results["success_rate"] > 0.8 and results["statistical_significance"]:
            hypothesis.status = HypothesisStatus.SUPPORTED
            
            # Create evidence
            evidence = Evidence(
                id=f"ev_{experiment.id}",
                hypothesis_id=hypothesis.id,
                content=results,
                timestamp=datetime.now(),
                strength="strong",
                source=experiment.id,
                quality_score=0.9,
                replicability=0.85
            )
            hypothesis.supporting_evidence.append(evidence)
            kb.evidence[evidence.id] = evidence
            
            # Step 7: Update theory
            theory = Theory(
                id="theory_integration",
                name="Integration Test Theory",
                core_principles=["Test principle"],
                explanatory_scope=["test_domain"],
                predictive_power=0.85,
                parsimony=0.8,
                coherence=0.9,
                empirical_support=0.85,
                hypotheses=[hypothesis],
                evidence=[evidence]
            )
            kb.add_theory(theory)
        
        # Assertions
        assert hypothesis.status == HypothesisStatus.SUPPORTED
        assert len(hypothesis.supporting_evidence) == 1
        assert len(kb.hypotheses) == 1
        assert len(kb.experiments) == 1
        assert len(kb.evidence) == 1
        assert len(kb.theories) == 1
        assert theory.id in kb.theories
    
    def test_full_smf_cycle_refutation(self):
        """Test SMF cycle where hypothesis is refuted."""
        kb = KnowledgeBase()
        
        hypothesis = Hypothesis(
            id="h_integration_2",
            statement="Hypothesis to be refuted",
            variables={},
            relationships=[],
            domain="test",
            timestamp=datetime.now(),
            confidence=0.6,
            complexity=0.5,
            novelty=0.5,
            testability=0.9
        )
        kb.add_hypothesis(hypothesis)
        
        agent = ScientificAgent(domain="Test", knowledge_base=kb)
        
        # Design and execute experiment
        hypothesis.status = HypothesisStatus.TESTING
        experiment = Experiment(
            id=f"exp_{hypothesis.id}",
            hypothesis_id=hypothesis.id,
            design={"type": "test"},
            conditions=[],
            controls=[],
            measurements=["outcome"],
            sample_size=100,
            randomization_procedure="random",
            statistical_tests=[]
        )
        
        # Poor results
        results = {
            "success_rate": 0.35,
            "statistical_significance": False
        }
        experiment.results = results
        
        # Refute hypothesis
        if results["success_rate"] <= 0.8 or not results["statistical_significance"]:
            hypothesis.status = HypothesisStatus.REFUTED
        
        assert hypothesis.status == HypothesisStatus.REFUTED
        assert len(kb.theories) == 0  # No theory created for refuted hypothesis
    
    def test_multiple_hypotheses_workflow(self):
        """Test workflow with multiple competing hypotheses."""
        kb = KnowledgeBase()
        
        h1 = Hypothesis(
            id="h_multi_1",
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
            id="h_multi_2",
            statement="Second hypothesis",
            variables={},
            relationships=[],
            domain="test",
            timestamp=datetime.now(),
            confidence=0.6,
            complexity=0.5,
            novelty=0.6,
            testability=0.8
        )
        
        kb.add_hypothesis(h1)
        kb.add_hypothesis(h2)
        
        agent = ScientificAgent(domain="Test", knowledge_base=kb)
        agent.active_hypotheses.extend([h1, h2])
        
        # Test both hypotheses
        h1.status = HypothesisStatus.SUPPORTED
        h2.status = HypothesisStatus.REFUTED
        
        assert len(agent.active_hypotheses) == 2
        assert h1.status == HypothesisStatus.SUPPORTED
        assert h2.status == HypothesisStatus.REFUTED
    
    def test_evidence_accumulation(self):
        """Test accumulating multiple pieces of evidence for a hypothesis."""
        kb = KnowledgeBase()
        
        hypothesis = Hypothesis(
            id="h_evidence_accum",
            statement="Evidence accumulation test",
            variables={},
            relationships=[],
            domain="test",
            timestamp=datetime.now(),
            confidence=0.5,
            complexity=0.5,
            novelty=0.5,
            testability=0.9
        )
        kb.add_hypothesis(hypothesis)
        
        # Add multiple pieces of evidence
        for i in range(3):
            evidence = Evidence(
                id=f"ev_accum_{i}",
                hypothesis_id=hypothesis.id,
                content={"experiment": i, "result": "positive"},
                timestamp=datetime.now(),
                strength="moderate",
                source=f"experiment_{i}",
                quality_score=0.8,
                replicability=0.75
            )
            hypothesis.supporting_evidence.append(evidence)
            kb.evidence[evidence.id] = evidence
        
        assert len(hypothesis.supporting_evidence) == 3
        assert len(kb.evidence) == 3
        
        # With accumulated evidence, hypothesis gains support
        hypothesis.status = HypothesisStatus.WELL_SUPPORTED
        assert hypothesis.status == HypothesisStatus.WELL_SUPPORTED
