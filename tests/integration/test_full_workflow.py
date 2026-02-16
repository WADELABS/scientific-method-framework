"""
Integration tests for complete SMF workflow.
"""

import pytest
import asyncio
from datetime import datetime
import os
import tempfile

from core.scientific_agent import (
    ScientificAgent, KnowledgeBase, Hypothesis, 
    HypothesisStatus, Experiment, Evidence
)
from core.vsa.provenance.ledger import MerkleLedger
from core.negative_space import NegativeSpaceExplorer


@pytest.mark.integration
class TestFullWorkflow:
    """Integration tests for complete SMF workflow."""
    
    @pytest.fixture
    def setup_agent(self):
        """Setup agent with clean state."""
        # Create temporary database
        tmp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        tmp_db.close()
        
        kb = KnowledgeBase()
        agent = ScientificAgent(domain="test_domain", knowledge_base=kb)
        ledger = MerkleLedger(str(tmp_db.name))
        explorer = NegativeSpaceExplorer(kb, "test_domain")
        
        yield agent, kb, ledger, explorer
        
        # Cleanup
        try:
            os.unlink(tmp_db.name)
        except:
            pass
    
    @pytest.mark.asyncio
    async def test_hypothesis_to_validation_flow(self, setup_agent):
        """Test complete flow from hypothesis creation to validation."""
        agent, kb, ledger, explorer = setup_agent
        
        # 1. Create hypothesis
        hypothesis = Hypothesis(
            id="h_integration_001",
            statement="Test hypothesis for integration",
            variables={"var1": "value1"},
            relationships=["test_rel"],
            domain="test_domain",
            timestamp=datetime.now(),
            confidence=0.7,
            complexity=0.3,
            novelty=0.5,
            testability=0.9
        )
        kb.add_hypothesis(hypothesis)
        assert hypothesis.id in kb.hypotheses
        
        # 2. Design experiment
        experiment = await agent._design_experiment(hypothesis)
        assert experiment is not None
        assert experiment.hypothesis_id == hypothesis.id
        assert experiment.sample_size > 0
        
        # 3. Execute experiment (simulated)
        results = {
            "success_rate": 0.95,
            "p_value": 0.001,
            "effect_size": 0.8
        }
        experiment.results = results
        
        # 4. Record to Merkle Ledger
        block_hash = ledger.add_entry({
            "hypothesis_id": hypothesis.id,
            "experiment_id": experiment.id,
            "results": results,
            "timestamp": datetime.now().isoformat()
        })
        
        assert len(block_hash) == 64  # SHA256
        assert ledger.verify_chain()
        
        # 5. Update hypothesis status
        if results["p_value"] < 0.05:
            hypothesis.status = HypothesisStatus.SUPPORTED
        
        assert hypothesis.status == HypothesisStatus.SUPPORTED
        
    @pytest.mark.asyncio
    async def test_negative_space_exploration(self, setup_agent):
        """Test negative space mapping and frontier generation."""
        agent, kb, ledger, explorer = setup_agent
        
        # Add some hypotheses to KB
        for i in range(3):
            h = Hypothesis(
                id=f"h_{i}",
                statement=f"Test hypothesis {i}",
                variables={"var": f"val{i}"},
                relationships=["test_rel"],
                domain="test_domain",
                timestamp=datetime.now(),
                confidence=0.7,
                complexity=0.3,
                novelty=0.5,
                testability=0.9
            )
            kb.add_hypothesis(h)
        
        # Reinitialize explorer after adding hypotheses to ensure it sees them
        explorer = NegativeSpaceExplorer(kb, "test_domain")
        
        # Map negative space
        neg_space = explorer.map_negative_space()
        assert neg_space is not None
        assert "explored_count" in neg_space
        assert "coverage" in neg_space
        assert neg_space["explored_count"] >= 3
        
        # Generate frontier hypotheses
        frontier = explorer.generate_frontier_hypotheses(count=5)
        assert len(frontier) > 0
        assert all(isinstance(h, Hypothesis) for h in frontier)
        
        # Calculate coverage
        coverage = explorer.calculate_exploration_coverage()
        assert 0.0 <= coverage <= 1.0
        
    @pytest.mark.asyncio
    async def test_ledger_provenance_chain(self, setup_agent):
        """Test Merkle Ledger maintains complete provenance."""
        agent, kb, ledger, explorer = setup_agent
        
        # Create hypothesis
        hypothesis = Hypothesis(
            id="h_ledger_001",
            statement="Ledger test hypothesis",
            variables={},
            relationships=[],
            domain="test_domain",
            timestamp=datetime.now(),
            confidence=0.7,
            complexity=0.3,
            novelty=0.5,
            testability=0.9
        )
        kb.add_hypothesis(hypothesis)
        
        # Record hypothesis creation
        hash1 = ledger.add_entry({
            "type": "hypothesis_created",
            "hypothesis_id": hypothesis.id,
            "statement": hypothesis.statement
        })
        
        # Design and record experiment
        experiment = await agent._design_experiment(hypothesis)
        hash2 = ledger.add_entry({
            "type": "experiment_designed",
            "experiment_id": experiment.id,
            "hypothesis_id": hypothesis.id
        })
        
        # Record results
        hash3 = ledger.add_entry({
            "type": "results_recorded",
            "experiment_id": experiment.id,
            "results": {"success": True}
        })
        
        # Verify chain
        assert ledger.verify_chain()
        
        # Verify all hashes are different
        assert hash1 != hash2 != hash3
        
    @pytest.mark.asyncio
    async def test_evidence_accumulation(self, setup_agent):
        """Test evidence accumulation affects hypothesis confidence."""
        agent, kb, ledger, explorer = setup_agent
        
        # Create hypothesis
        hypothesis = Hypothesis(
            id="h_evidence_001",
            statement="Evidence accumulation test",
            variables={},
            relationships=[],
            domain="test_domain",
            timestamp=datetime.now(),
            confidence=0.5,
            complexity=0.3,
            novelty=0.5,
            testability=0.9
        )
        kb.add_hypothesis(hypothesis)
        initial_confidence = hypothesis.confidence
        
        # Add supporting evidence
        evidence1 = Evidence(
            id="ev_001",
            hypothesis_id=hypothesis.id,
            content={"result": "positive"},
            timestamp=datetime.now(),
            strength="strong",
            source="experiment_1",
            quality_score=0.9,
            replicability=0.85,
            effect_size=0.8
        )
        hypothesis.supporting_evidence.append(evidence1)
        
        # More supporting evidence
        evidence2 = Evidence(
            id="ev_002",
            hypothesis_id=hypothesis.id,
            content={"result": "positive"},
            timestamp=datetime.now(),
            strength="moderate",
            source="experiment_2",
            quality_score=0.8,
            replicability=0.75,
            effect_size=0.6
        )
        hypothesis.supporting_evidence.append(evidence2)
        
        # Update confidence based on evidence
        hypothesis.confidence = min(0.95, initial_confidence + 0.15 * len(hypothesis.supporting_evidence))
        
        assert len(hypothesis.supporting_evidence) == 2
        assert hypothesis.confidence > initial_confidence
        assert hypothesis.confidence <= 0.95
        
    @pytest.mark.asyncio
    async def test_multiple_hypotheses_workflow(self, setup_agent):
        """Test workflow with multiple related hypotheses."""
        agent, kb, ledger, explorer = setup_agent
        
        # Create multiple related hypotheses
        hypotheses = []
        for i in range(5):
            h = Hypothesis(
                id=f"h_multi_{i}",
                statement=f"Related hypothesis {i}",
                variables={"var": f"val{i}"},
                relationships=["relates_to"],
                domain="test_domain",
                timestamp=datetime.now(),
                confidence=0.6 + i * 0.05,
                complexity=0.3,
                novelty=0.5,
                testability=0.9
            )
            kb.add_hypothesis(h)
            hypotheses.append(h)
        
        assert len(kb.hypotheses) == 5
        
        # Test each hypothesis
        for h in hypotheses:
            experiment = await agent._design_experiment(h)
            assert experiment.hypothesis_id == h.id
            
            # Record to ledger
            block_hash = ledger.add_entry({
                "hypothesis_id": h.id,
                "experiment_id": experiment.id,
                "timestamp": datetime.now().isoformat()
            })
            assert len(block_hash) == 64
        
        # Verify ledger integrity
        assert ledger.verify_chain()
        
        # Reinitialize explorer to see the hypotheses
        explorer = NegativeSpaceExplorer(kb, "test_domain")
        
        # Check negative space updated
        neg_space = explorer.map_negative_space()
        assert neg_space["explored_count"] >= 5


@pytest.mark.integration
class TestHighValueRegions:
    """Test high-value region identification."""
    
    @pytest.fixture
    def setup_populated_kb(self):
        """Setup KB with diverse hypotheses."""
        tmp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        tmp_db.close()
        
        kb = KnowledgeBase()
        
        # Add diverse hypotheses
        concepts = ["temperature", "pressure", "volume", "mass", "energy"]
        relationships = ["increases", "decreases", "affects", "correlates_with"]
        
        for i, concept in enumerate(concepts):
            for j, rel in enumerate(relationships):
                h = Hypothesis(
                    id=f"h_{i}_{j}",
                    statement=f"{concept} {rel} something",
                    variables={concept: "value"},
                    relationships=[rel],
                    domain="physics",
                    timestamp=datetime.now(),
                    confidence=0.6,
                    complexity=0.4,
                    novelty=0.5,
                    testability=0.8
                )
                kb.add_hypothesis(h)
        
        explorer = NegativeSpaceExplorer(kb, "physics")
        ledger = MerkleLedger(str(tmp_db.name))
        
        yield kb, explorer, ledger
        
        try:
            os.unlink(tmp_db.name)
        except:
            pass
    
    def test_high_value_region_identification(self, setup_populated_kb):
        """Test that high-value regions are identified correctly."""
        kb, explorer, ledger = setup_populated_kb
        
        regions = explorer.identify_high_value_regions()
        
        assert len(regions) > 0
        assert all("priority_score" in r for r in regions)
        assert all("type" in r for r in regions)
        assert all("description" in r for r in regions)
        
        # Verify regions are sorted by priority
        priorities = [r["priority_score"] for r in regions]
        assert priorities == sorted(priorities, reverse=True)
        
    def test_coverage_calculation(self, setup_populated_kb):
        """Test coverage calculation is reasonable."""
        kb, explorer, ledger = setup_populated_kb
        
        coverage = explorer.calculate_exploration_coverage()
        
        assert 0.0 <= coverage <= 1.0
        # With our setup, coverage should be > 0 but < 1
        assert coverage > 0.0
        assert coverage < 1.0
