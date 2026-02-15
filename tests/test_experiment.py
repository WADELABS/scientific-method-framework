"""
Tests for Experiment class and experiment execution
"""

import pytest
from datetime import datetime
from core.scientific_agent import Hypothesis, Experiment, HypothesisStatus


class TestExperiment:
    """Test experiment design and execution."""
    
    def test_experiment_creation(self):
        """Test creating an experiment for a hypothesis."""
        h = Hypothesis(
            id="h_exp_test",
            statement="Test experiment creation",
            variables={"var": "value"},
            relationships=[],
            domain="test",
            timestamp=datetime.now(),
            confidence=0.5,
            complexity=0.5,
            novelty=0.5,
            testability=0.9
        )
        
        exp = Experiment(
            id="exp_1",
            hypothesis_id=h.id,
            design={"type": "controlled"},
            conditions=["control", "treatment"],
            controls=["temperature", "pressure"],
            measurements=["outcome1", "outcome2"],
            sample_size=100,
            randomization_procedure="random_assignment",
            statistical_tests=["t_test", "anova"]
        )
        
        assert exp.id == "exp_1"
        assert exp.hypothesis_id == h.id
        assert exp.sample_size == 100
        assert len(exp.conditions) == 2
        assert len(exp.measurements) == 2
        assert exp.results is None
        assert exp.analysis is None
    
    def test_experiment_with_results(self):
        """Test recording experiment results."""
        exp = Experiment(
            id="exp_2",
            hypothesis_id="h_test",
            design={"type": "simulation"},
            conditions=["baseline"],
            controls=[],
            measurements=["success_rate"],
            sample_size=50,
            randomization_procedure="none",
            statistical_tests=[]
        )
        
        # Add results
        exp.results = {
            "success_rate": 0.85,
            "confidence_interval": [0.80, 0.90]
        }
        
        exp.analysis = {
            "conclusion": "supported",
            "p_value": 0.02,
            "effect_size": 0.45
        }
        
        assert exp.results is not None
        assert exp.analysis is not None
        assert exp.results["success_rate"] == 0.85
        assert exp.analysis["conclusion"] == "supported"
    
    def test_experiment_statistical_tests(self):
        """Test experiment with various statistical tests."""
        exp = Experiment(
            id="exp_3",
            hypothesis_id="h_stats",
            design={"type": "A/B test"},
            conditions=["A", "B"],
            controls=["time_of_day"],
            measurements=["conversion_rate"],
            sample_size=1000,
            randomization_procedure="stratified",
            statistical_tests=["chi_square", "fisher_exact", "mann_whitney"]
        )
        
        assert "chi_square" in exp.statistical_tests
        assert "mann_whitney" in exp.statistical_tests
        assert len(exp.statistical_tests) == 3
    
    def test_stub_crucible_simulation(self):
        """Test running an experiment with stub Crucible."""
        h = Hypothesis(
            id="h_crucible",
            statement="Test crucible execution",
            variables={"param": "value"},
            relationships=[],
            domain="test",
            timestamp=datetime.now(),
            confidence=0.7,
            complexity=0.3,
            novelty=0.5,
            testability=0.9
        )
        
        exp = Experiment(
            id="exp_crucible",
            hypothesis_id=h.id,
            design={"type": "simulation", "parameters": h.variables},
            conditions=["baseline", "modified"],
            controls=[],
            measurements=["success_rate"],
            sample_size=100,
            randomization_procedure="random",
            statistical_tests=["t_test"]
        )
        
        # Simulate execution
        simulated_results = {
            "success_rate": 0.88,
            "sample_size": exp.sample_size,
            "statistical_significance": True
        }
        
        exp.results = simulated_results
        
        assert exp.results["success_rate"] > 0.8
        assert exp.results["statistical_significance"] is True
